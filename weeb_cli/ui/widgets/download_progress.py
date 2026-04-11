"""Download progress widget for Weeb CLI."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, ProgressBar, Static
from typing import Any, Dict


class DownloadProgressItem(Static):
    """Single download item with progress bar and status info."""

    def __init__(self, item: Dict[str, Any], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.item = item

    def compose(self) -> ComposeResult:
        status = self.item.get("status", "pending")
        title = self.item.get("anime_title", "Unknown")[:28]
        ep = self.item.get("episode_number", "?")
        progress = self.item.get("progress", 0)
        speed = self.item.get("speed", "") if status == "processing" else ""
        eta = self.item.get("eta", "") if status == "processing" else ""

        style_map = {
            "processing": "cyan",
            "completed": "green",
            "failed": "red",
            "pending": "dim",
        }
        color = style_map.get(status, "white")

        with Horizontal():
            yield Label(f"[{color}]{title} - E{ep}[/{color}]", classes="dl-title")
            yield ProgressBar(total=100, show_percentage=True, classes="dl-bar")
            yield Label(f"[{color}]{speed}[/{color}]", classes="dl-speed")
            yield Label(f"[{color}]{eta}[/{color}]", classes="dl-eta")

    def update_progress(self, item: Dict[str, Any]) -> None:
        """Update the download progress display."""
        self.item = item
        bar = self.query_one(ProgressBar)
        bar.progress = item.get("progress", 0)
