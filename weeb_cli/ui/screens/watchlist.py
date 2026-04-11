"""Watchlist screen showing watch stats and anime progress."""

import asyncio
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import (
    Static, DataTable, TabbedContent, TabPane, Label, LoadingIndicator,
)
from typing import Any, Dict, List

from weeb_cli.i18n import i18n
from weeb_cli.services.progress import progress_tracker
from weeb_cli.ui.widgets.stats_panel import StatsPanel


class WatchlistScreen(Screen):
    """Watchlist screen with stats and in-progress/completed tabs."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="content"):
            yield Static(
                f"[bold]{i18n.t('menu.options.watchlist')}[/bold]",
                classes="title",
            )
            yield Vertical(id="stats-container")
            yield TabbedContent(
                TabPane(i18n.t("watchlist.in_progress"), id="tab-progress"),
                TabPane(i18n.t("watchlist.completed"), id="tab-completed"),
                id="watchlist-tabs",
            )

    def on_mount(self) -> None:
        self.run_worker(self._load_data(), name="load-watchlist")

    async def _load_data(self) -> None:
        stats = await asyncio.to_thread(progress_tracker.get_stats)

        # Stats panel
        stats_container = self.query_one("#stats-container", Vertical)
        stats_container.remove_children()
        stats_container.mount(StatsPanel(stats))

        if stats.get("last_watched"):
            last = stats["last_watched"]
            stats_container.mount(
                Static(
                    f"[dim]{i18n.t('watchlist.last_watched')}: "
                    f"{last['title']} - {i18n.t('details.episode')} {last['last_watched']}[/dim]"
                )
            )

        # In Progress tab
        in_progress = await asyncio.to_thread(progress_tracker.get_in_progress_anime)
        progress_pane = self.query_one("#tab-progress", TabPane)
        progress_pane.remove_children()

        if not in_progress:
            progress_pane.mount(
                Static(f"[dim]{i18n.t('watchlist.no_in_progress')}[/dim]")
            )
        else:
            table = DataTable(id="progress-table")
            progress_pane.mount(table)
            table.add_columns(
                "#",
                i18n.t("watchlist.anime_title"),
                i18n.t("watchlist.episodes_watched"),
                i18n.t("watchlist.next"),
            )
            for i, anime in enumerate(in_progress, 1):
                watched = len(anime.get("completed", []))
                total = anime.get("total_episodes", 0)
                total_str = str(total) if total > 0 else "?"
                title = anime.get("title", anime["slug"])
                next_ep = anime.get("last_watched", 0) + 1

                table.add_row(
                    str(i),
                    title,
                    f"{watched}/{total_str}",
                    str(next_ep),
                    key=anime["slug"],
                )

        # Completed tab
        completed = await asyncio.to_thread(progress_tracker.get_completed_anime)
        completed_pane = self.query_one("#tab-completed", TabPane)
        completed_pane.remove_children()

        if not completed:
            completed_pane.mount(
                Static(f"[dim]{i18n.t('watchlist.no_completed')}[/dim]")
            )
        else:
            table = DataTable(id="completed-table")
            completed_pane.mount(table)
            table.add_columns(
                "#",
                i18n.t("watchlist.anime_title"),
                i18n.t("watchlist.episodes_watched"),
            )
            for i, anime in enumerate(completed, 1):
                watched = len(anime.get("completed", []))
                total = anime.get("total_episodes", watched)
                title = anime.get("title", anime["slug"])
                table.add_row(str(i), title, f"{watched}/{total}", key=anime["slug"])

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        slug = str(event.row_key.value)
        anime_data = {
            "id": slug,
            "slug": slug,
            "title": slug,
            "name": slug,
        }

        # Try to get title from progress data
        progress = progress_tracker.get_anime_progress(slug)
        if progress:
            anime_data["title"] = progress.get("title", slug)
            anime_data["name"] = progress.get("title", slug)

        from weeb_cli.ui.screens.anime_detail import AnimeDetailScreen
        self.app.push_screen(AnimeDetailScreen(anime_data))

    def action_go_back(self) -> None:
        self.app.pop_screen()
