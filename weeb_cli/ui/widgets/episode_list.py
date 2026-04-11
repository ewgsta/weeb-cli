"""Episode list widget for Weeb CLI.

Shared widget used by both watch flow and download flow
to display episode lists with watched/next/unwatched markers.
"""

from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label
from textual.message import Message
from typing import Any, Dict, List, Optional, Set

from weeb_cli.i18n import i18n


class EpisodeItem(ListItem):
    """A single episode list item with status marker."""

    def __init__(
        self,
        episode: Dict[str, Any],
        is_watched: bool = False,
        is_next: bool = False,
    ) -> None:
        self.episode = episode
        self.is_watched = is_watched
        self.is_next = is_next
        super().__init__()

    def compose(self) -> ComposeResult:
        num = self.episode.get("number") or self.episode.get("ep_num") or "?"

        prefix = "   "
        style = ""
        if self.is_watched:
            prefix = i18n.t("details.watched_prefix", "✓  ")
            style = "dim"
        elif self.is_next:
            prefix = i18n.t("details.next_prefix", "●  ")
            style = "bold cyan"

        text = f"{prefix}{i18n.t('details.episode')} {num}"

        size = self.episode.get("size")
        if size:
            from weeb_cli.services.local_library import local_library
            text += f" ({local_library.format_size(size)})"

        yield Label(text, classes=style)


class EpisodeList(ListView):
    """Episode list widget with watched/next/unwatched markers.

    Attributes:
        episodes: List of episode dictionaries.
        completed_ids: Set of completed episode IDs.
        next_ep_num: Next episode number to watch.
    """

    class EpisodeSelected(Message):
        """Message emitted when an episode is selected."""

        def __init__(self, episode: Dict[str, Any]) -> None:
            self.episode = episode
            super().__init__()

    def __init__(
        self,
        episodes: List[Dict[str, Any]],
        completed_ids: Optional[Set[int]] = None,
        next_ep_num: int = 1,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.episodes = episodes
        self.completed_ids = completed_ids or set()
        self.next_ep_num = next_ep_num

    def compose(self) -> ComposeResult:
        for ep in self.episodes:
            num_val = ep.get("number") or ep.get("ep_num")
            try:
                num = int(num_val)
            except (TypeError, ValueError):
                num = -1

            is_watched = num in self.completed_ids
            is_next = num == self.next_ep_num

            yield EpisodeItem(ep, is_watched=is_watched, is_next=is_next)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, EpisodeItem):
            self.post_message(self.EpisodeSelected(item.episode))

    def refresh_episodes(
        self,
        completed_ids: Optional[Set[int]] = None,
        next_ep_num: Optional[int] = None,
    ) -> None:
        """Update episode markers and re-render."""
        if completed_ids is not None:
            self.completed_ids = completed_ids
        if next_ep_num is not None:
            self.next_ep_num = next_ep_num
        self.clear()
        for ep in self.episodes:
            num_val = ep.get("number") or ep.get("ep_num")
            try:
                num = int(num_val)
            except (TypeError, ValueError):
                num = -1
            is_watched = num in self.completed_ids
            is_next = num == self.next_ep_num
            self.append(EpisodeItem(ep, is_watched=is_watched, is_next=is_next))
