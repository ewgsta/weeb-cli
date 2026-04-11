"""Anime detail screen with episode list, watch/download actions."""

import asyncio
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen, ModalScreen
from textual.widgets import (
    Static, Button, Label, ListView, ListItem,
    LoadingIndicator, OptionList, TabbedContent, TabPane,
)
from textual.widgets.option_list import Option
from typing import Any, Dict, List, Optional

from weeb_cli.i18n import i18n
from weeb_cli.services.details import get_details
from weeb_cli.services.progress import progress_tracker
from weeb_cli.services.watch import get_streams
from weeb_cli.services.player import player
from weeb_cli.config import config
from weeb_cli.commands.search.episode_utils import (
    normalize_details, get_episodes_safe,
    group_episodes_by_season, make_season_episode_id,
)
from weeb_cli.commands.search.stream_utils import sort_streams, extract_streams_from_response
from weeb_cli.ui.widgets.episode_list import EpisodeList


class StreamSelectModal(ModalScreen[Optional[Dict]]):
    """Modal dialog for stream/source selection."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, streams: List[Dict[str, Any]]) -> None:
        self.streams = streams
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="stream-dialog"):
            yield Static(
                i18n.t("details.select_source"),
                classes="dialog-title",
            )
            options = []
            for s in self.streams:
                server = s.get("server", "Unknown")
                quality = s.get("quality", "auto")
                options.append(Option(f"{server} ({quality})"))
            yield OptionList(*options, id="stream-options")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        idx = event.option_index
        if 0 <= idx < len(self.streams):
            self.dismiss(self.streams[idx])

    def action_cancel(self) -> None:
        self.dismiss(None)


class ConfirmModal(ModalScreen[bool]):
    """Simple yes/no confirm dialog."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Static(self.message, classes="dialog-title")
            with Horizontal(classes="dialog-buttons"):
                yield Button(i18n.t("common.yes", "Yes"), id="btn-yes", variant="primary")
                yield Button(i18n.t("common.no", "No"), id="btn-no")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-yes")

    def action_cancel(self) -> None:
        self.dismiss(False)


class AnimeDetailScreen(Screen):
    """Screen showing anime details with episode list and actions."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def __init__(self, anime: Dict[str, Any]) -> None:
        self.anime = anime
        self.details: Optional[Dict] = None
        self.episodes: List[Dict] = []
        self.seasons: Dict[int, List[Dict]] = {}
        self.current_season: int = 1
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="content"):
            title = self.anime.get("title") or self.anime.get("name") or "Anime"
            yield Static(f"[bold]{title}[/bold]", id="anime-title", classes="title")
            yield Static("", id="anime-description")
            with Horizontal(id="anime-actions"):
                yield Button(
                    i18n.t("details.watch"),
                    id="btn-watch",
                    classes="action-primary",
                )
                yield Button(
                    i18n.t("details.download"),
                    id="btn-download",
                    classes="action-secondary",
                )
                yield Button(
                    i18n.t("details.add_to_library"),
                    id="btn-library",
                    classes="action-secondary",
                )
            yield Static("", id="status-line")
            yield Vertical(id="episode-container")

    def on_mount(self) -> None:
        self.run_worker(self._load_details(), name="load-details")

    async def _load_details(self) -> None:
        slug = self.anime.get("slug") or self.anime.get("id")
        if not slug:
            self.query_one("#status-line", Static).update(
                f"[red]{i18n.t('details.error_slug')}[/red]"
            )
            return

        container = self.query_one("#episode-container", Vertical)
        container.remove_children()
        container.mount(LoadingIndicator())

        details = await asyncio.to_thread(get_details, slug)
        details = normalize_details(details)

        if not details:
            container.remove_children()
            container.mount(
                Static(f"[red]{i18n.t('details.not_found')}[/red]")
            )
            return

        self.details = details

        desc = details.get("description") or details.get("synopsis") or details.get("desc")
        show_desc = config.get("show_description", True)
        if show_desc and desc:
            if len(desc) > 500:
                desc = desc[:497] + "..."
            self.query_one("#anime-description", Static).update(f"[dim]{desc}[/dim]")

        # Update library button
        from weeb_cli.services.local_library import local_library
        provider_name = config.get("scraping_source", "")
        in_library = local_library.is_in_virtual_library(slug, provider_name)
        btn_lib = self.query_one("#btn-library", Button)
        if in_library:
            btn_lib.label = i18n.t("details.remove_from_library")

        self.episodes = get_episodes_safe(details)
        if not self.episodes:
            container.remove_children()
            container.mount(
                Static(f"[yellow]{i18n.t('details.no_episodes')}[/yellow]")
            )
            return

        self.seasons = group_episodes_by_season(self.episodes)
        season_numbers = sorted(self.seasons.keys())

        container.remove_children()

        if len(season_numbers) > 1:
            tabs = TabbedContent(id="season-tabs")
            container.mount(tabs)
            for s_num in season_numbers:
                pane = TabPane(f"{i18n.t('details.season', 'Season')} {s_num}", id=f"s-{s_num}")
                tabs.add_pane(pane)
                ep_list = self._build_episode_list(s_num)
                pane.mount(ep_list)
            self.current_season = season_numbers[0]
        else:
            self.current_season = season_numbers[0] if season_numbers else 1
            ep_list = self._build_episode_list(self.current_season)
            container.mount(ep_list)

    def _build_episode_list(self, season: int) -> EpisodeList:
        slug = self.anime.get("slug") or self.anime.get("id")
        prog_data = progress_tracker.get_anime_progress(slug)
        completed_ids = set(prog_data.get("completed", []))

        season_eps = self.seasons.get(season, self.episodes)

        # Calculate next episode
        last_watched = 0
        for ep_id in completed_ids:
            if ep_id >= season * 1000 and ep_id < (season + 1) * 1000:
                ep_num = ep_id % 1000
                if ep_num > last_watched:
                    last_watched = ep_num
        if season == 1 and not any(cid >= 1000 for cid in completed_ids):
            last_watched = prog_data.get("last_watched", 0)
        next_ep = last_watched + 1

        # Map episode IDs
        mapped_ids = set()
        for cid in completed_ids:
            if cid >= season * 1000 and cid < (season + 1) * 1000:
                mapped_ids.add(cid % 1000)
            elif season == 1 and cid < 1000:
                mapped_ids.add(cid)

        return EpisodeList(
            episodes=season_eps,
            completed_ids=mapped_ids,
            next_ep_num=next_ep,
            id=f"ep-list-{season}",
        )

    def on_episode_list_episode_selected(self, event: EpisodeList.EpisodeSelected) -> None:
        self.run_worker(
            self._play_episode(event.episode),
            name="play-episode",
        )

    async def _play_episode(self, episode: Dict[str, Any]) -> None:
        slug = self.anime.get("slug") or self.anime.get("id")
        ep_id = episode.get("id")
        ep_num = episode.get("number") or episode.get("ep_num")

        if not ep_id:
            self.query_one("#status-line", Static).update(
                f"[red]{i18n.t('details.invalid_ep_id')}[/red]"
            )
            return

        self.query_one("#status-line", Static).update(
            f"[dim]{i18n.t('common.processing')}[/dim]"
        )

        stream_resp = await asyncio.to_thread(get_streams, slug, ep_id)
        streams_list = extract_streams_from_response(stream_resp)

        if not streams_list:
            from weeb_cli.services.scraper import scraper
            error_msg = i18n.t("details.stream_not_found")
            if scraper.last_error:
                error_msg += f" [{scraper.last_error}]"
            self.query_one("#status-line", Static).update(f"[red]{error_msg}[/red]")
            return

        # Validate streams
        valid_streams = []
        if config.get("scraping_source") == "docchi":
            valid_streams = streams_list
        else:
            self.query_one("#status-line", Static).update(
                f"[dim]{i18n.t('details.validating_streams')}...[/dim]"
            )
            from weeb_cli.services.stream_validator import stream_validator
            for stream in streams_list:
                is_valid, error = await asyncio.to_thread(
                    stream_validator.validate_url, stream.get("url"), 3
                )
                if is_valid:
                    valid_streams.append(stream)

        if not valid_streams:
            self.query_one("#status-line", Static).update(
                f"[red]{i18n.t('details.no_valid_streams')}[/red]"
            )
            return

        valid_streams = sort_streams(valid_streams)
        self.query_one("#status-line", Static).update("")

        # Show stream selection modal
        selected_stream = await self.app.push_screen_wait(StreamSelectModal(valid_streams))
        if not selected_stream:
            return

        stream_url = selected_stream.get("url")
        if not stream_url:
            return

        # Play with MPV (suspend TUI)
        title = f"{self.details.get('title', 'Anime')} - S{self.current_season}E{ep_num}"

        headers = {}
        if self.details and self.details.get("source") == "hianime":
            headers["Referer"] = "https://hianime.to"

        auto_watched = {"triggered": False}

        def on_watched_callback():
            if not auto_watched["triggered"]:
                total_eps = (self.details or {}).get("total_episodes") or len(self.episodes)
                n = int(ep_num)
                season_ep_id = make_season_episode_id(self.current_season, n)
                progress_tracker.mark_watched(
                    slug,
                    season_ep_id,
                    title=(self.details or {}).get("title"),
                    total_episodes=total_eps,
                )
                auto_watched["triggered"] = True

        self.query_one("#status-line", Static).update(
            f"[green]{i18n.t('details.player_starting')}[/green]"
        )

        # Use app.suspend() to hand terminal to MPV
        with self.app.suspend():
            play_success = player.play(
                stream_url,
                title=title,
                headers=headers,
                anime_title=(self.details or {}).get("title", "Anime"),
                episode_number=int(ep_num) if ep_num else None,
                total_episodes=(self.details or {}).get("total_episodes") or len(self.episodes),
                slug=slug,
                on_watched=on_watched_callback,
            )

        if play_success and not auto_watched["triggered"]:
            mark = await self.app.push_screen_wait(
                ConfirmModal(i18n.t("details.mark_watched"))
            )
            if mark:
                n = int(ep_num)
                total_eps = (self.details or {}).get("total_episodes") or len(self.episodes)
                season_ep_id = make_season_episode_id(self.current_season, n)
                progress_tracker.mark_watched(
                    slug,
                    season_ep_id,
                    title=(self.details or {}).get("title"),
                    total_episodes=total_eps,
                )
                self.query_one("#status-line", Static).update(
                    f"[green]✓ {i18n.t('details.marked_watched')}[/green]"
                )
                # Update trackers async
                self.run_worker(
                    self._update_trackers(),
                    name="update-trackers",
                )

        # Refresh episode list
        self._refresh_episode_lists()

    async def _update_trackers(self) -> None:
        from weeb_cli.services.tracker import anilist_tracker, mal_tracker, kitsu_tracker

        slug = self.anime.get("slug") or self.anime.get("id")
        updated_prog = progress_tracker.get_anime_progress(slug)
        total_watched = len(updated_prog.get("completed", []))
        total_eps = (self.details or {}).get("total_episodes", 0)

        trackers = [
            ("AniList", anilist_tracker),
            ("MAL", mal_tracker),
            ("Kitsu", kitsu_tracker),
        ]

        updated = []
        for name, tracker in trackers:
            if tracker.is_authenticated():
                try:
                    result = await asyncio.to_thread(
                        tracker.update_progress,
                        (self.details or {}).get("title"),
                        total_watched,
                        total_eps,
                    )
                    if result:
                        updated.append(name)
                except Exception:
                    pass

        if updated:
            trackers_str = ", ".join(updated)
            self.query_one("#status-line", Static).update(
                f"[green]✓ {trackers_str} {i18n.t('watchlist.tracker_updated')}[/green]"
            )

    def _refresh_episode_lists(self) -> None:
        slug = self.anime.get("slug") or self.anime.get("id")
        prog_data = progress_tracker.get_anime_progress(slug)
        completed_ids = set(prog_data.get("completed", []))

        for season in self.seasons:
            try:
                ep_list = self.query_one(f"#ep-list-{season}", EpisodeList)
                mapped_ids = set()
                for cid in completed_ids:
                    if cid >= season * 1000 and cid < (season + 1) * 1000:
                        mapped_ids.add(cid % 1000)
                    elif season == 1 and cid < 1000:
                        mapped_ids.add(cid)

                last_watched = max(
                    (cid % 1000 for cid in completed_ids
                     if cid >= season * 1000 and cid < (season + 1) * 1000),
                    default=0,
                )
                ep_list.refresh_episodes(mapped_ids, last_watched + 1)
            except Exception:
                pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-watch":
            pass  # Episode select handles watch
        elif event.button.id == "btn-download":
            self.run_worker(self._handle_download(), name="download")
        elif event.button.id == "btn-library":
            self._handle_library_toggle()

    async def _handle_download(self) -> None:
        if not self.episodes:
            return

        from weeb_cli.services.downloader import queue_manager

        slug = self.anime.get("slug") or self.anime.get("id")
        anime_title = (self.details or {}).get("title") or "Unknown Anime"

        added = await asyncio.to_thread(
            queue_manager.add_to_queue, anime_title, self.episodes, slug
        )

        status = self.query_one("#status-line", Static)
        if added > 0:
            status.update(f"[green]{i18n.t('downloads.queued', count=added)}[/green]")
            await asyncio.to_thread(queue_manager.start_queue)
        else:
            status.update(f"[yellow]{i18n.t('downloads.already_in_queue')}[/yellow]")

    def _handle_library_toggle(self) -> None:
        from weeb_cli.services.local_library import local_library

        slug = self.anime.get("slug") or self.anime.get("id")
        provider_name = config.get("scraping_source", "")
        in_library = local_library.is_in_virtual_library(slug, provider_name)
        status = self.query_one("#status-line", Static)
        btn = self.query_one("#btn-library", Button)

        if in_library:
            local_library.remove_from_virtual_library(slug, provider_name)
            status.update(f"[green]{i18n.t('details.removed_from_library')}[/green]")
            btn.label = i18n.t("details.add_to_library")
        else:
            anime_title = (self.details or {}).get("title", "")
            cover = self.anime.get("cover") or (self.details or {}).get("cover")
            anime_type = self.anime.get("type") or (self.details or {}).get("type")
            year = self.anime.get("year") or (self.details or {}).get("year")

            if local_library.add_to_virtual_library(
                slug, anime_title, provider_name, cover, anime_type, year
            ):
                status.update(f"[green]{i18n.t('details.added_to_library')}[/green]")
            else:
                status.update(f"[yellow]{i18n.t('details.already_in_library')}[/yellow]")
            btn.label = i18n.t("details.remove_from_library")

    def action_go_back(self) -> None:
        self.app.pop_screen()
