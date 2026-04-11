"""Downloads screen with source list, queue management and live progress."""

import asyncio
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import (
    Static, Button, DataTable, ListView, ListItem, Label,
    Input, LoadingIndicator,
)
from typing import Any, Dict, List

from weeb_cli.i18n import i18n
from weeb_cli.services.downloader import queue_manager
from weeb_cli.services.local_library import local_library
from weeb_cli.services.player import player
from weeb_cli.services.progress import progress_tracker


class DownloadsScreen(Screen):
    """Downloads screen with source browsing and queue management."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="content"):
            yield Static(
                f"[bold]{i18n.t('menu.options.downloads')}[/bold]",
                classes="title",
            )
            yield Vertical(id="download-sources")
            yield Static("", id="queue-title")
            yield DataTable(id="download-queue")
            with Horizontal(id="queue-controls"):
                yield Button(
                    i18n.t("downloads.start_queue"),
                    id="btn-start-queue",
                    variant="success",
                )
                yield Button(
                    i18n.t("downloads.stop_queue"),
                    id="btn-stop-queue",
                    variant="warning",
                )
                yield Button(
                    i18n.t("downloads.clear_completed"),
                    id="btn-clear",
                )
                yield Button(
                    i18n.t("downloads.retry_failed", "Retry Failed"),
                    id="btn-retry",
                )

    def on_mount(self) -> None:
        self.run_worker(self._load_sources(), name="load-sources")
        self._setup_queue_table()
        self.set_interval(2.0, self._refresh_queue)

    async def _load_sources(self) -> None:
        await asyncio.to_thread(local_library.smart_index_all)
        sources = await asyncio.to_thread(local_library.get_all_sources)

        container = self.query_one("#download-sources", Vertical)
        container.remove_children()

        indexed_anime = await asyncio.to_thread(local_library.get_indexed_anime)
        indexed_count = len(indexed_anime)

        if indexed_count > 0:
            container.mount(
                Static(
                    f"[cyan]{i18n.t('downloads.search_all')} ({indexed_count} anime)[/cyan]"
                )
            )

        for source in sources:
            if source["available"]:
                library = await asyncio.to_thread(
                    local_library.scan_library, source["path"]
                )
                count = len(library)
                if count > 0:
                    container.mount(
                        Static(f"[green]●[/green] {source['name']} ({count} anime)")
                    )
            else:
                indexed = [
                    a for a in indexed_anime if a["source_path"] == source["path"]
                ]
                if indexed:
                    container.mount(
                        Static(
                            f"[dim]○ {source['name']} ({len(indexed)} anime) "
                            f"- {i18n.t('downloads.offline')}[/dim]"
                        )
                    )

        if not container.children:
            container.mount(
                Static(f"[dim]{i18n.t('downloads.empty')}[/dim]")
            )

    def _setup_queue_table(self) -> None:
        table = self.query_one("#download-queue", DataTable)
        table.add_columns(
            i18n.t("watchlist.anime_title"),
            i18n.t("details.episode"),
            i18n.t("downloads.status"),
            i18n.t("downloads.progress"),
        )

    def _refresh_queue(self) -> None:
        table = self.query_one("#download-queue", DataTable)
        table.clear()

        active = [i for i in queue_manager.queue if i["status"] == "processing"]
        pending = [i for i in queue_manager.queue if i["status"] == "pending"]
        finished = [i for i in queue_manager.queue if i["status"] in ["completed", "failed"]]
        finished = finished[-10:]

        display_list = active + pending + finished

        queue_title = self.query_one("#queue-title", Static)
        if display_list:
            is_running = queue_manager.is_running()
            status = (
                i18n.t("downloads.queue_running")
                if is_running
                else i18n.t("downloads.queue_stopped")
            )
            queue_title.update(
                f"[bold]{i18n.t('downloads.active_downloads')} "
                f"({len(active)}) - {status}[/bold]"
            )
        else:
            queue_title.update("")

        for item in display_list:
            status = item["status"]
            title = item.get("anime_title", "?")[:28]
            ep = str(item.get("episode_number", "?"))
            progress = item.get("progress", 0)

            style_map = {
                "processing": "cyan",
                "completed": "green",
                "failed": "red",
                "pending": "dim",
            }
            color = style_map.get(status, "white")

            bars = int(progress / 5)
            bar_str = "█" * bars + "░" * (20 - bars)
            p_text = f"{progress}%" if status == "processing" else ""

            status_text = i18n.t(f"downloads.status_{status}", status.upper())

            table.add_row(
                f"[{color}]{title}[/{color}]",
                ep,
                f"[{color}]{status_text}[/{color}]",
                f"[{color}]{bar_str} {p_text}[/{color}]",
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        status_msg = ""

        if btn_id == "btn-start-queue":
            queue_manager.start_queue()
            status_msg = i18n.t("downloads.queue_started")
        elif btn_id == "btn-stop-queue":
            queue_manager.stop_queue()
            status_msg = i18n.t("downloads.queue_stopped")
        elif btn_id == "btn-clear":
            queue_manager.clear_completed()
            status_msg = i18n.t("downloads.cleared")
        elif btn_id == "btn-retry":
            count = queue_manager.retry_failed()
            status_msg = f"{count} {i18n.t('downloads.retrying_downloads')}"

        if status_msg:
            self.notify(status_msg, timeout=2)

        self._refresh_queue()

    def action_go_back(self) -> None:
        self.app.pop_screen()
