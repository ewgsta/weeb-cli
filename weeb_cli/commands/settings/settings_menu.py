import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.config import config
from .settings_config import change_language, change_source, toggle_description, toggle_discord_rpc, toggle_shortcuts
from .settings_download import download_settings_menu, aria2_settings_menu, ytdlp_settings_menu, toggle_config
from .settings_drives import external_drives_menu
from .settings_trackers import trackers_menu
from .settings_backup import backup_restore_menu
from .settings_shortcuts import shortcuts_menu
from .settings_cache import cache_settings_menu

console = Console()

SELECT_STYLE = questionary.Style([
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan'),
    ('selected', 'fg:cyan bold'),
])

def open_settings():
    while True:
        console.clear()
        show_header(i18n.t("settings.title"))
        
        choices = _build_settings_menu()
        
        try:
            answer = questionary.select(
                i18n.t("settings.title"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
                style=SELECT_STYLE
            ).ask()
        except KeyboardInterrupt:
            return

        if answer is None:
            return
        
        _handle_settings_action(answer)

def _build_settings_menu():
    lang = config.get("language")
    source = config.get("scraping_source", "local")
    display_source = "weeb" if source == "local" else source

    aria2_state = i18n.t("common.enabled") if config.get("aria2_enabled") else i18n.t("common.disabled")
    ytdlp_state = i18n.t("common.enabled") if config.get("ytdlp_enabled") else i18n.t("common.disabled")
    desc_state = i18n.t("common.enabled") if config.get("show_description", True) else i18n.t("common.disabled")
    discord_rpc_state = i18n.t("common.enabled") if config.get("discord_rpc_enabled", False) else i18n.t("common.disabled")
    shortcuts_state = i18n.t("common.enabled") if config.get("shortcuts_enabled", True) else i18n.t("common.disabled")
    
    choices = [
        i18n.t("settings.language"),
        f"{i18n.t('settings.source')} [{display_source}]",
        i18n.t("settings.download_settings"),
        i18n.t("settings.external_drives"),
        f"{i18n.t('settings.show_description')} [{desc_state}]",
        f"{i18n.t('settings.discord_rpc')} [{discord_rpc_state}]",
        f"{i18n.t('settings.shortcuts')} [{shortcuts_state}]",
    ]
    
    if config.get("shortcuts_enabled", True):
        choices.append(f"  ↳ {i18n.t('settings.shortcuts_config')}")
    
    choices.append(f"{i18n.t('settings.aria2')} [{aria2_state}]")
    if config.get("aria2_enabled"):
        choices.append(f"  ↳ {i18n.t('settings.aria2_config')}")
        
    choices.append(f"{i18n.t('settings.ytdlp')} [{ytdlp_state}]")
    if config.get("ytdlp_enabled"):
        choices.append(f"  ↳ {i18n.t('settings.ytdlp_config')}")
    
    choices.extend([
        i18n.t("settings.trackers"),
        i18n.t("settings.cache"),
        i18n.t("settings.backup_restore")
    ])
    
    return choices

def _handle_settings_action(answer):
    action_map = {
        i18n.t("settings.language"): change_language,
        i18n.t("settings.download_settings"): download_settings_menu,
        i18n.t("settings.external_drives"): external_drives_menu,
        i18n.t("settings.trackers"): trackers_menu,
        i18n.t("settings.cache"): cache_settings_menu,
        i18n.t("settings.backup_restore"): backup_restore_menu,
    }
    
    if answer in action_map:
        action_map[answer]()
    elif answer.startswith(i18n.t('settings.source')):
        change_source()
    elif answer.startswith(i18n.t('settings.show_description')):
        toggle_description()
    elif answer.startswith(i18n.t('settings.discord_rpc')):
        toggle_discord_rpc()
    elif answer.startswith(i18n.t('settings.shortcuts')) and not answer.startswith("  ↳"):
        toggle_shortcuts()
    elif answer == f"  ↳ {i18n.t('settings.shortcuts_config')}":
        shortcuts_menu()
    elif answer.startswith(i18n.t('settings.aria2')) and not answer.startswith("  ↳"):
        toggle_config("aria2_enabled", "Aria2")
    elif answer == f"  ↳ {i18n.t('settings.aria2_config')}":
        aria2_settings_menu()
    elif answer.startswith(i18n.t('settings.ytdlp')) and not answer.startswith("  ↳"):
        toggle_config("ytdlp_enabled", "yt-dlp")
    elif answer == f"  ↳ {i18n.t('settings.ytdlp_config')}":
        ytdlp_settings_menu()
