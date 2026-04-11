"""Settings screen with categorized configuration options."""

import asyncio
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import (
    Static, Switch, Button, Input, Label, OptionList, Select,
)
from textual.widgets.option_list import Option

from weeb_cli.i18n import i18n
from weeb_cli.config import config


class SettingsScreen(Screen):
    """Settings screen with toggle switches and configuration inputs."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="content"):
            yield Static(
                f"[bold]{i18n.t('settings.title')}[/bold]",
                classes="title",
            )

            # Language & Source
            with Vertical(classes="settings-section"):
                yield Static(i18n.t("settings.language"), classes="section-title")
                yield OptionList(
                    Option("Turkce", id="lang-tr"),
                    Option("English", id="lang-en"),
                    Option("Deutsch", id="lang-de"),
                    Option("Polski", id="lang-pl"),
                    id="language-select",
                )

            with Vertical(classes="settings-section"):
                yield Static(i18n.t("settings.source"), classes="section-title")
                yield OptionList(id="source-select")

            # Toggles
            with Vertical(classes="settings-section"):
                yield Static("Options", classes="section-title")

                with Horizontal(classes="toggle-row"):
                    yield Label(i18n.t("settings.show_description"), classes="toggle-label")
                    yield Switch(
                        value=config.get("show_description", True),
                        id="toggle-description",
                    )

                with Horizontal(classes="toggle-row"):
                    yield Label(i18n.t("settings.discord_rpc"), classes="toggle-label")
                    yield Switch(
                        value=config.get("discord_rpc_enabled", False),
                        id="toggle-discord",
                    )

                with Horizontal(classes="toggle-row"):
                    yield Label(i18n.t("settings.aniskip"), classes="toggle-label")
                    yield Switch(
                        value=config.get("aniskip_enabled", False),
                        id="toggle-aniskip",
                    )

                with Horizontal(classes="toggle-row"):
                    yield Label(i18n.t("settings.shortcuts"), classes="toggle-label")
                    yield Switch(
                        value=config.get("shortcuts_enabled", True),
                        id="toggle-shortcuts",
                    )

            # Download settings
            with Vertical(classes="settings-section"):
                yield Static(i18n.t("settings.download_settings"), classes="section-title")

                with Horizontal(classes="toggle-row"):
                    yield Label(i18n.t("settings.aria2"), classes="toggle-label")
                    yield Switch(
                        value=config.get("aria2_enabled", True),
                        id="toggle-aria2",
                    )

                with Horizontal(classes="toggle-row"):
                    yield Label(i18n.t("settings.ytdlp"), classes="toggle-label")
                    yield Switch(
                        value=config.get("ytdlp_enabled", True),
                        id="toggle-ytdlp",
                    )

                yield Label(i18n.t("settings.max_conn"))
                yield Input(
                    str(config.get("aria2_max_connections", 16)),
                    id="input-max-conn",
                    type="integer",
                )

                yield Label(i18n.t("settings.concurrent_downloads"))
                yield Input(
                    str(config.get("max_concurrent_downloads", 3)),
                    id="input-concurrent",
                    type="integer",
                )

                yield Label(i18n.t("settings.download_dir"))
                yield Input(
                    str(config.get("download_dir", "")),
                    id="input-download-dir",
                )

            # Trackers
            with Vertical(classes="settings-section"):
                yield Static(i18n.t("settings.trackers"), classes="section-title")
                yield Static("", id="tracker-status")
                yield Button(
                    i18n.t("settings.anilist_login"),
                    id="btn-anilist",
                )
                yield Button(
                    i18n.t("settings.mal_login"),
                    id="btn-mal",
                )
                yield Button(
                    i18n.t("settings.kitsu_login"),
                    id="btn-kitsu",
                )

            # Backup & Cache
            with Horizontal():
                yield Button(
                    i18n.t("settings.backup_restore"),
                    id="btn-backup",
                )
                yield Button(
                    i18n.t("settings.cache_title"),
                    id="btn-cache",
                )

    def on_mount(self) -> None:
        self._load_sources()
        self._load_tracker_status()

    def _load_sources(self) -> None:
        from weeb_cli.services.scraper import scraper

        current_lang = config.get("language", "tr")
        sources = scraper.get_sources_for_lang(current_lang)

        source_list = self.query_one("#source-select", OptionList)
        source_list.clear_options()
        current_source = config.get("scraping_source", "")

        for s in sources:
            marker = " [*]" if s == current_source else ""
            source_list.add_option(Option(f"{s}{marker}", id=f"src-{s}"))

    def _load_tracker_status(self) -> None:
        from weeb_cli.services.tracker import anilist_tracker, mal_tracker, kitsu_tracker

        lines = []
        if anilist_tracker.is_authenticated():
            lines.append("[green]✓[/green] AniList")
        if mal_tracker.is_authenticated():
            lines.append("[green]✓[/green] MAL")
        if kitsu_tracker.is_authenticated():
            lines.append("[green]✓[/green] Kitsu")

        status = self.query_one("#tracker-status", Static)
        if lines:
            status.update("\n".join(lines))
        else:
            status.update(f"[dim]{i18n.t('settings.anilist_not_connected')}[/dim]")

    def on_switch_changed(self, event: Switch.Changed) -> None:
        switch_id = event.switch.id
        value = event.value

        toggle_map = {
            "toggle-description": "show_description",
            "toggle-discord": "discord_rpc_enabled",
            "toggle-aniskip": "aniskip_enabled",
            "toggle-shortcuts": "shortcuts_enabled",
            "toggle-aria2": "aria2_enabled",
            "toggle-ytdlp": "ytdlp_enabled",
        }

        config_key = toggle_map.get(switch_id)
        if config_key:
            config.set(config_key, value)

            if switch_id == "toggle-discord":
                from weeb_cli.services.discord_rpc import discord_rpc
                if value:
                    discord_rpc.connect()
                else:
                    discord_rpc.disconnect()
            elif switch_id == "toggle-aniskip":
                from weeb_cli.services.aniskip import aniskip_service
                aniskip_service.set_enabled(value)

            tool_name = config_key.replace("_enabled", "").replace("_", " ").title()
            msg_key = "settings.toggle_on" if value else "settings.toggle_off"
            self.notify(i18n.t(msg_key, tool=tool_name), timeout=2)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        input_id = event.input.id
        value = event.value

        if input_id == "input-max-conn":
            try:
                val = int(value)
                if 1 <= val <= 16:
                    config.set("aria2_max_connections", val)
                    self.notify(f"Max connections: {val}", timeout=2)
            except ValueError:
                pass
        elif input_id == "input-concurrent":
            try:
                val = int(value)
                if 1 <= val <= 5:
                    config.set("max_concurrent_downloads", val)
                    self.notify(f"Concurrent downloads: {val}", timeout=2)
            except ValueError:
                pass
        elif input_id == "input-download-dir":
            if value.strip():
                config.set("download_dir", value.strip())
                self.notify(f"Download dir: {value.strip()}", timeout=2)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_id = event.option.id or ""

        if option_id.startswith("lang-"):
            lang_code = option_id.replace("lang-", "")
            i18n.set_language(lang_code)

            from weeb_cli.services.scraper import scraper
            sources = scraper.get_sources_for_lang(lang_code)
            if sources:
                config.set("scraping_source", sources[0])

            self.notify(i18n.t("settings.language_changed"), timeout=2)
            self._load_sources()

        elif option_id.startswith("src-"):
            source = option_id.replace("src-", "")
            from weeb_cli.services.cache import get_cache

            current = config.get("scraping_source", "")
            if source != current:
                cache = get_cache()
                cache.invalidate_provider(current)
                config.set("scraping_source", source)
                self.notify(
                    i18n.t("settings.source_changed", source=source),
                    timeout=2,
                )
                self._load_sources()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id

        if btn_id == "btn-anilist":
            self.run_worker(self._connect_tracker("anilist"), name="anilist")
        elif btn_id == "btn-mal":
            self.run_worker(self._connect_tracker("mal"), name="mal")
        elif btn_id == "btn-kitsu":
            self.run_worker(self._connect_tracker("kitsu"), name="kitsu")
        elif btn_id == "btn-backup":
            self._handle_backup()
        elif btn_id == "btn-cache":
            self._handle_cache()

    async def _connect_tracker(self, tracker_name: str) -> None:
        from weeb_cli.services.tracker import anilist_tracker, mal_tracker, kitsu_tracker

        tracker_map = {
            "anilist": anilist_tracker,
            "mal": mal_tracker,
            "kitsu": kitsu_tracker,
        }

        tracker = tracker_map.get(tracker_name)
        if not tracker:
            return

        if tracker.is_authenticated():
            tracker.logout()
            self.notify(
                i18n.t(f"settings.{tracker_name}_logged_out"),
                timeout=2,
            )
        else:
            self.notify(
                i18n.t(f"settings.{tracker_name}_opening_browser"),
                timeout=3,
            )
            with self.app.suspend():
                try:
                    result = tracker.login()
                    if result:
                        self.notify(
                            i18n.t(f"settings.{tracker_name}_login_success"),
                            timeout=2,
                        )
                    else:
                        self.notify(
                            i18n.t(f"settings.{tracker_name}_login_failed"),
                            severity="error",
                            timeout=2,
                        )
                except Exception:
                    self.notify(
                        i18n.t(f"settings.{tracker_name}_login_failed"),
                        severity="error",
                        timeout=2,
                    )

        self._load_tracker_status()

    def _handle_backup(self) -> None:
        from weeb_cli.services.database import db

        try:
            backup_path = db.create_backup()
            self.notify(
                f"{i18n.t('settings.backup_success')} -> {backup_path}",
                timeout=3,
            )
        except Exception:
            self.notify(
                i18n.t("settings.backup_failed"),
                severity="error",
                timeout=2,
            )

    def _handle_cache(self) -> None:
        from weeb_cli.services.cache import get_cache

        cache = get_cache()
        cache.clear()
        self.notify(i18n.t("settings.cache_cleared"), timeout=2)

    def action_go_back(self) -> None:
        self.app.pop_screen()
