"""Main screen with sidebar navigation and content area."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static, ContentSwitcher

from weeb_cli.i18n import i18n
from weeb_cli.config import config
from weeb_cli import __version__
from weeb_cli.ui.widgets.sidebar import Sidebar


class MainScreen(Screen):
    """Main dashboard screen with sidebar navigation.

    The sidebar provides navigation between Search, Downloads,
    Watchlist, Library, and Settings. Content area shows the
    selected section.
    """

    BINDINGS = [
        ("s", "navigate('search')", "Search"),
        ("d", "navigate('downloads')", "Downloads"),
        ("w", "navigate('watchlist')", "Watchlist"),
        ("l", "navigate('library')", "Library"),
        ("c", "navigate('settings')", "Settings"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        # Header
        source = config.get("scraping_source", "")
        if not source:
            from weeb_cli.providers.registry import get_default_provider
            lang = config.get("language", "tr")
            source = get_default_provider(lang) or "animecix"

        yield Static(
            f" [bold]Weeb CLI[/bold] [dim]| {source.capitalize()} | v{__version__}[/dim]",
            id="app-header",
        )

        with Horizontal():
            yield Sidebar(id="sidebar")
            yield Vertical(
                Static(
                    f"[bold]{i18n.t('menu.prompt')}[/bold]\n\n"
                    f"[dim]{i18n.t('common.ctrl_c_hint')}[/dim]",
                    id="welcome-content",
                ),
                id="main-content",
            )

        # Footer
        from weeb_cli.services.downloader import queue_manager
        active = queue_manager.get_active_count()
        footer_text = f" {i18n.t('tui.footer_source', i18n.t('menu.options.settings'))}: {source}"
        if active > 0:
            footer_text += f" | {i18n.t('downloads.active_downloads')}: {active}"

        yield Static(footer_text, id="app-footer")

    def on_sidebar_navigate(self, event: Sidebar.Navigate) -> None:
        self._open_section(event.action)

    def action_navigate(self, section: str) -> None:
        self._open_section(section)

    def _open_section(self, section: str) -> None:
        screen_map = {
            "search": "weeb_cli.ui.screens.search.SearchScreen",
            "downloads": "weeb_cli.ui.screens.downloads.DownloadsScreen",
            "watchlist": "weeb_cli.ui.screens.watchlist.WatchlistScreen",
            "library": "weeb_cli.ui.screens.library.LibraryScreen",
            "settings": "weeb_cli.ui.screens.settings.SettingsScreen",
        }

        screen_path = screen_map.get(section)
        if not screen_path:
            return

        # Dynamic import to avoid circular imports
        module_path, class_name = screen_path.rsplit(".", 1)
        import importlib
        module = importlib.import_module(module_path)
        screen_class = getattr(module, class_name)

        self.app.push_screen(screen_class())

        # Update sidebar highlighting
        sidebar = self.query_one("#sidebar", Sidebar)
        sidebar.highlight_item(section)

    def action_quit(self) -> None:
        from weeb_cli.services.downloader import queue_manager

        active = queue_manager.get_active_count()
        pending = queue_manager.get_pending_count()

        if active > 0 or pending > 0:
            from weeb_cli.ui.screens.anime_detail import ConfirmModal
            self.app.push_screen(
                ConfirmModal(
                    i18n.t("menu.exit_confirm_downloads", count=active + pending)
                ),
                callback=self._handle_quit_confirm,
            )
        else:
            self.app.exit()

    def _handle_quit_confirm(self, confirmed: bool) -> None:
        if confirmed:
            from weeb_cli.services.downloader import queue_manager
            queue_manager.stop_queue()
            self.app.exit()
