"""Search screen for anime search and results display."""

import asyncio
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Input, ListView, ListItem, Label, Static, LoadingIndicator
from textual.message import Message
from typing import Any, Dict, List, Optional

from weeb_cli.i18n import i18n
from weeb_cli.services.search import search
from weeb_cli.services.progress import progress_tracker
from weeb_cli.services.cache import get_cache
from weeb_cli.commands.search.episode_utils import normalize_search_results


class AnimeResultItem(ListItem):
    """A single anime search result."""

    def __init__(self, anime: Dict[str, Any]) -> None:
        self.anime = anime
        super().__init__()

    def compose(self) -> ComposeResult:
        title = self.anime.get("title") or self.anime.get("name") or "Unknown"
        yield Label(title)


class SearchScreen(Screen):
    """Anime search screen with input and results list."""

    class AnimeSelected(Message):
        """Message emitted when an anime is selected from results."""

        def __init__(self, anime: Dict[str, Any]) -> None:
            self.anime = anime
            super().__init__()

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="content"):
            yield Static(i18n.t("menu.options.search"), id="content-title", classes="title")

            history = progress_tracker.get_search_history()
            if history:
                yield Static(
                    f"[dim]{i18n.t('search.recent')}: {', '.join(history[:5])}[/dim]",
                    id="search-history",
                )

            yield Input(
                placeholder=i18n.t("search.prompt"),
                id="search-box",
            )
            yield Vertical(id="search-results")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value.strip()
        if query:
            progress_tracker.add_search_history(query)
            self.run_worker(self._do_search(query), name="search")

    async def _do_search(self, query: str) -> None:
        results_container = self.query_one("#search-results", Vertical)
        results_container.remove_children()
        results_container.mount(LoadingIndicator())

        from weeb_cli.config import config

        cache = get_cache()
        provider = config.get("scraping_source", "None")
        cache_key = f"search:{provider}:{query}"
        data = cache.get(cache_key, max_age=1800)

        if data is None:
            data = await asyncio.to_thread(search, query)
            if data:
                cache.set(cache_key, data)

        results_container.remove_children()

        if data:
            data = normalize_search_results(data)

        if not data or not isinstance(data, list):
            results_container.mount(
                Static(f"[red]{i18n.t('search.no_results')}[/red]")
            )
            return

        results_list = ListView(id="results-list")
        results_container.mount(results_list)

        for item in data:
            title = item.get("title") or item.get("name")
            if title:
                results_list.append(AnimeResultItem(item))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, AnimeResultItem):
            from weeb_cli.ui.screens.anime_detail import AnimeDetailScreen
            self.app.push_screen(AnimeDetailScreen(item.anime))

    def action_go_back(self) -> None:
        self.app.pop_screen()
