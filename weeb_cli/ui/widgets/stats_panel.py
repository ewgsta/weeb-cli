"""Watchlist statistics panel widget for Weeb CLI."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static
from typing import Any, Dict

from weeb_cli.i18n import i18n


class StatCard(Static):
    """Single statistic card (value + label)."""

    def __init__(self, value: str, label: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._value = value
        self._label = label

    def compose(self) -> ComposeResult:
        yield Static(self._value, classes="stat-value")
        yield Static(self._label, classes="stat-label")


class StatsPanel(Static):
    """Panel displaying watchlist statistics."""

    def __init__(self, stats: Dict[str, Any], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.stats = stats

    def compose(self) -> ComposeResult:
        with Horizontal(id="watchlist-stats"):
            yield StatCard(
                str(self.stats.get("total_anime", 0)),
                i18n.t("watchlist.total_anime"),
                classes="stat-card",
            )
            yield StatCard(
                str(self.stats.get("total_episodes", 0)),
                i18n.t("watchlist.total_episodes"),
                classes="stat-card",
            )
            yield StatCard(
                f"{self.stats.get('total_hours', 0)}h",
                i18n.t("watchlist.total_hours"),
                classes="stat-card",
            )

    def update_stats(self, stats: Dict[str, Any]) -> None:
        """Update stats and re-render cards."""
        self.stats = stats
        self.refresh(recompose=True)
