"""Sidebar navigation widget for Weeb CLI."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option
from textual.message import Message

from weeb_cli.i18n import i18n


class SidebarItem(Option):
    """A single sidebar navigation option."""

    def __init__(self, label: str, action: str, icon: str = "") -> None:
        display = f"{icon} {label}" if icon else label
        super().__init__(display, id=action)
        self.action = action


class Sidebar(Vertical):
    """Navigation sidebar widget.

    Provides main navigation options with keyboard shortcuts
    and active page highlighting.
    """

    DEFAULT_CSS = """
    Sidebar {
        width: 28;
        dock: left;
        background: $surface-lighten-1;
        border-right: solid $surface-lighten-2;
        padding: 1 0;
    }
    """

    class Navigate(Message):
        """Message emitted when a sidebar item is selected."""

        def __init__(self, action: str) -> None:
            self.action = action
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Static("Weeb CLI", classes="sidebar-title")
        yield OptionList(
            SidebarItem(i18n.t("menu.options.search"), "search", ""),
            SidebarItem(i18n.t("menu.options.downloads"), "downloads", ""),
            SidebarItem(i18n.t("menu.options.watchlist"), "watchlist", ""),
            SidebarItem(i18n.t("menu.options.library"), "library", ""),
            SidebarItem(i18n.t("menu.options.settings"), "settings", ""),
            id="sidebar-nav",
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option = event.option
        if isinstance(option, SidebarItem):
            self.post_message(self.Navigate(option.action))

    def highlight_item(self, action: str) -> None:
        """Highlight the sidebar item matching the given action."""
        nav = self.query_one("#sidebar-nav", OptionList)
        for idx, option in enumerate(nav._options):
            if isinstance(option, SidebarItem) and option.action == action:
                nav.highlighted = idx
                break
