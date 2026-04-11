"""Setup screen for first-run language selection and dependency check."""

import asyncio
from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.screen import Screen
from textual.widgets import Static, OptionList, Label, LoadingIndicator
from textual.widgets.option_list import Option

from weeb_cli.i18n import i18n


class SetupScreen(Screen):
    """First-run setup screen for language selection and dependency installation."""

    BINDINGS = []

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="setup-container"):
                yield Static("Weeb CLI", classes="setup-title")
                yield Static("Select Language / Dil Seciniz", id="setup-subtitle")
                yield OptionList(
                    Option("Turkce", id="tr"),
                    Option("English", id="en"),
                    Option("Deutsch", id="de"),
                    Option("Polski", id="pl"),
                    id="lang-select",
                )
                yield Label("", id="setup-status")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        lang_code = event.option.id
        if lang_code:
            i18n.set_language(lang_code)
            self.run_worker(self._run_setup(), name="setup")

    async def _run_setup(self) -> None:
        """Run dependency check and installation."""
        status = self.query_one("#setup-status", Label)
        lang_select = self.query_one("#lang-select", OptionList)
        lang_select.display = False

        subtitle = self.query_one("#setup-subtitle", Static)
        subtitle.update(i18n.t("setup.checking_deps"))

        from weeb_cli.services.dependency_manager import dependency_manager

        tools = ["yt-dlp", "ffmpeg", "aria2", "mpv"]

        for tool in tools:
            status.update(f"{i18n.t('setup.checking_tool', tool=tool)}")
            path = await asyncio.to_thread(dependency_manager.check_dependency, tool)

            if path:
                status.update(f"[green]✓[/green] {tool}: {i18n.t('setup.found_short')}")
            else:
                status.update(f"[yellow]⚠[/yellow] {tool}: {i18n.t('setup.not_found_short')}")
                status.update(f"{i18n.t('setup.installing_tool', tool=tool)}")
                result = await asyncio.to_thread(dependency_manager.install_dependency, tool)
                if result:
                    status.update(f"[green]✓[/green] {tool}: {i18n.t('setup.installed')}")
                else:
                    status.update(f"[red]✗[/red] {tool}: {i18n.t('setup.failed_short')}")

            await asyncio.sleep(0.3)

        status.update(f"[bold green]{i18n.t('setup.complete')}[/bold green]")
        await asyncio.sleep(1)

        self.dismiss(True)
