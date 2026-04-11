"""Library screen with online and local library tabs."""

import asyncio
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import (
    Static, DataTable, TabbedContent, TabPane, Label, LoadingIndicator,
)
from typing import Any, Dict, List

from weeb_cli.i18n import i18n
from weeb_cli.services.local_library import local_library
from weeb_cli.config import config


class LibraryScreen(Screen):
    """Library screen with online and local library tabs."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="content"):
            yield Static(
                f"[bold]{i18n.t('menu.options.library')}[/bold]",
                classes="title",
            )
            yield Static("", id="library-stats")
            yield TabbedContent(
                TabPane(i18n.t("library.online_library"), id="tab-online"),
                TabPane(i18n.t("library.local_library"), id="tab-local"),
                id="library-tabs",
            )

    def on_mount(self) -> None:
        self.run_worker(self._load_data(), name="load-library")

    async def _load_data(self) -> None:
        virtual_library = await asyncio.to_thread(local_library.get_virtual_library)
        indexed_anime = await asyncio.to_thread(local_library.get_indexed_anime)

        stats = self.query_one("#library-stats", Static)
        stats.update(
            f"[cyan]{i18n.t('library.online_library')}:[/cyan] {len(virtual_library)} anime  "
            f"[cyan]{i18n.t('library.local_library')}:[/cyan] {len(indexed_anime)} anime"
        )

        # Online library tab
        online_pane = self.query_one("#tab-online", TabPane)
        online_pane.remove_children()

        if not virtual_library:
            online_pane.mount(
                Static(f"[dim]{i18n.t('library.online_empty')}[/dim]")
            )
        else:
            table = DataTable(id="online-table")
            online_pane.mount(table)
            table.add_columns("#", i18n.t("watchlist.anime_title"), "Provider")
            for i, item in enumerate(virtual_library, 1):
                title = item["anime_title"]
                provider = item["provider_name"]
                year = f" ({item['year']})" if item.get("year") else ""
                table.add_row(
                    str(i),
                    f"{title}{year}",
                    provider,
                    key=f"online-{item['anime_id']}-{provider}",
                )

        # Local library tab
        local_pane = self.query_one("#tab-local", TabPane)
        local_pane.remove_children()

        if not indexed_anime:
            local_pane.mount(
                Static(f"[dim]{i18n.t('library.local_empty')}[/dim]")
            )
        else:
            table = DataTable(id="local-table")
            local_pane.mount(table)
            table.add_columns(
                "#",
                i18n.t("watchlist.anime_title"),
                i18n.t("downloads.episode_short"),
                i18n.t("downloads.status"),
            )
            for i, item in enumerate(indexed_anime, 1):
                available = Path(item["folder_path"]).exists()
                status_icon = "[green]✓[/green]" if available else "[red]✗[/red]"
                table.add_row(
                    str(i),
                    item["title"],
                    str(item["episode_count"]),
                    status_icon,
                    key=f"local-{i}",
                )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        key = str(event.row_key.value)

        if key.startswith("online-"):
            parts = key.split("-", 2)
            if len(parts) >= 3:
                anime_id = parts[1]
                provider = parts[2]
                self._open_virtual_anime(anime_id, provider)
        elif key.startswith("local-"):
            idx = int(key.split("-")[1]) - 1
            indexed = local_library.get_indexed_anime()
            if 0 <= idx < len(indexed):
                self._open_local_anime(indexed[idx])

    def _open_virtual_anime(self, anime_id: str, provider_name: str) -> None:
        virtual_library = local_library.get_virtual_library()
        item = None
        for v_item in virtual_library:
            if v_item["anime_id"] == anime_id and v_item["provider_name"] == provider_name:
                item = v_item
                break

        if not item:
            return

        current_provider = config.get("scraping_source", "")
        if current_provider != provider_name:
            config.set("scraping_source", provider_name)

        anime_data = {
            "id": anime_id,
            "slug": anime_id,
            "title": item["anime_title"],
            "name": item["anime_title"],
            "cover": item.get("cover_url"),
            "type": item.get("anime_type"),
            "year": item.get("year"),
        }

        from weeb_cli.ui.screens.anime_detail import AnimeDetailScreen
        self.app.push_screen(AnimeDetailScreen(anime_data))

    def _open_local_anime(self, item: Dict[str, Any]) -> None:
        anime_path = item["folder_path"]
        if not Path(anime_path).exists():
            self.notify(
                i18n.t("library.local_not_available"),
                severity="error",
                timeout=2,
            )
            return

        episodes = local_library._scan_anime_folder(Path(anime_path))
        anime_data = {
            "id": item["title"],
            "slug": item["title"],
            "title": item["title"],
            "name": item["title"],
        }

        from weeb_cli.ui.screens.anime_detail import AnimeDetailScreen
        self.app.push_screen(AnimeDetailScreen(anime_data))

    def action_go_back(self) -> None:
        self.app.pop_screen()
