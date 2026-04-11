"""Weeb CLI - Textual Application.

Main application class that manages screens, global keybindings,
and application lifecycle (network check, dependency check, tracker sync).
"""

import asyncio
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Static

from weeb_cli.config import config
from weeb_cli.i18n import i18n


class WeebApp(App):
    """Main Textual application for Weeb CLI.

    Manages the application lifecycle, screens, and global keybindings.
    The app starts with a setup screen if no language is configured,
    then transitions to the main dashboard.
    """

    TITLE = "Weeb CLI"
    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    async def on_mount(self) -> None:
        """Initialize the application on mount."""
        if not config.get("language"):
            from weeb_cli.ui.screens.setup import SetupScreen
            await self.push_screen(SetupScreen(), callback=self._on_setup_complete)
        else:
            await self._start_main()

    def _on_setup_complete(self, result: bool) -> None:
        """Handle setup completion."""
        self.run_worker(self._start_main(), name="start-main")

    async def _start_main(self) -> None:
        """Start the main application flow."""
        # Initialize AniSkip service
        try:
            from weeb_cli.services.aniskip import aniskip_service
            aniskip_enabled = config.get("aniskip_enabled", False)
            aniskip_service.set_enabled(aniskip_enabled)
        except Exception:
            pass

        # Background tasks
        self.run_worker(self._check_updates(), name="check-updates", exclusive=True)
        self.run_worker(self._check_network(), name="check-network")
        self.run_worker(self._check_ffmpeg(), name="check-ffmpeg")
        self.run_worker(self._sync_trackers(), name="sync-trackers")
        self.run_worker(self._check_downloads(), name="check-downloads")

        # Push main screen
        from weeb_cli.ui.screens.main import MainScreen
        await self.push_screen(MainScreen())

    async def _check_updates(self) -> None:
        """Check for updates in background."""
        try:
            from weeb_cli.services.updater import check_update_available
            result = await asyncio.to_thread(check_update_available)
            if result:
                self.notify(
                    f"{i18n.t('update.available')} - {result}",
                    timeout=5,
                )
        except Exception:
            pass

    async def _check_network(self) -> None:
        """Verify network connectivity."""
        import requests

        urls = ["https://1.1.1.1", "https://google.com", "https://api.github.com"]
        connected = False

        for url in urls:
            try:
                await asyncio.to_thread(requests.get, url, timeout=3)
                connected = True
                break
            except Exception:
                continue

        if not connected:
            self.notify(
                i18n.t("errors.network", "Network connection error."),
                severity="error",
                timeout=5,
            )

    async def _check_ffmpeg(self) -> None:
        """Ensure FFmpeg is available."""
        try:
            from weeb_cli.services.dependency_manager import dependency_manager
            has_ffmpeg = await asyncio.to_thread(
                dependency_manager.check_dependency, "ffmpeg"
            )
            if not has_ffmpeg:
                self.notify(
                    i18n.t("setup.downloading", tool="FFmpeg"),
                    timeout=3,
                )
                await asyncio.to_thread(dependency_manager.install_dependency, "ffmpeg")
        except Exception:
            pass

    async def _sync_trackers(self) -> None:
        """Sync pending tracker updates."""
        try:
            from weeb_cli.services.tracker import anilist_tracker, mal_tracker, kitsu_tracker

            for name, tracker in [
                ("AniList", anilist_tracker),
                ("MAL", mal_tracker),
                ("Kitsu", kitsu_tracker),
            ]:
                if tracker.is_authenticated():
                    pending = await asyncio.to_thread(tracker.get_pending_count)
                    if pending > 0:
                        synced = await asyncio.to_thread(tracker.sync_pending)
                        if synced > 0:
                            self.notify(
                                f"{name}: {synced} synced",
                                timeout=3,
                            )
        except Exception:
            pass

    async def _check_downloads(self) -> None:
        """Check for incomplete downloads."""
        try:
            from weeb_cli.services.downloader import queue_manager

            has_incomplete = await asyncio.to_thread(
                queue_manager.has_incomplete_downloads
            )
            if has_incomplete:
                count = await asyncio.to_thread(queue_manager.get_incomplete_count)
                self.notify(
                    i18n.t("downloads.resume_prompt", count=count),
                    timeout=5,
                )
                await asyncio.to_thread(queue_manager.resume_incomplete)
        except Exception:
            pass
