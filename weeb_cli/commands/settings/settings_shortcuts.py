import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header

console = Console()

def shortcuts_menu():
    from weeb_cli.services.shortcuts import shortcut_manager
    
    while True:
        console.clear()
        show_header(i18n.t("settings.shortcuts"))
        
        shortcuts = shortcut_manager.get_shortcuts()
        
        console.print(f"[dim]{i18n.t('settings.shortcuts_hint')}[/dim]\n")
        
        choices = _build_shortcut_choices(shortcuts)
        
        try:
            sel = questionary.select(
                i18n.t("downloads.action_prompt"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == i18n.t("settings.shortcuts_reset"):
                _reset_shortcuts()
            else:
                action = _get_action_from_selection(sel, shortcuts)
                if action:
                    change_shortcut(action)
                    
        except KeyboardInterrupt:
            return

def _build_shortcut_choices(shortcuts):
    return [
        f"{i18n.t('settings.shortcut_search')} [{shortcuts['search']}]",
        f"{i18n.t('settings.shortcut_downloads')} [{shortcuts['downloads']}]",
        f"{i18n.t('settings.shortcut_watchlist')} [{shortcuts['watchlist']}]",
        f"{i18n.t('settings.shortcut_settings')} [{shortcuts['settings']}]",
        f"{i18n.t('settings.shortcut_exit')} [{shortcuts['exit']}]",
        f"{i18n.t('settings.shortcut_next_episode')} [{shortcuts['next_episode']}]",
        f"{i18n.t('settings.shortcut_prev_episode')} [{shortcuts['prev_episode']}]",
        f"{i18n.t('settings.shortcut_back')} [{shortcuts['back']}]",
        f"{i18n.t('settings.shortcut_help')} [{shortcuts['help']}]",
        i18n.t("settings.shortcuts_reset")
    ]

def _get_action_from_selection(sel, shortcuts):
    action_map = {
        f"{i18n.t('settings.shortcut_search')} [{shortcuts['search']}]": "search",
        f"{i18n.t('settings.shortcut_downloads')} [{shortcuts['downloads']}]": "downloads",
        f"{i18n.t('settings.shortcut_watchlist')} [{shortcuts['watchlist']}]": "watchlist",
        f"{i18n.t('settings.shortcut_settings')} [{shortcuts['settings']}]": "settings",
        f"{i18n.t('settings.shortcut_exit')} [{shortcuts['exit']}]": "exit",
        f"{i18n.t('settings.shortcut_next_episode')} [{shortcuts['next_episode']}]": "next_episode",
        f"{i18n.t('settings.shortcut_prev_episode')} [{shortcuts['prev_episode']}]": "prev_episode",
        f"{i18n.t('settings.shortcut_back')} [{shortcuts['back']}]": "back",
        f"{i18n.t('settings.shortcut_help')} [{shortcuts['help']}]": "help"
    }
    return action_map.get(sel)

def _reset_shortcuts():
    from weeb_cli.services.shortcuts import shortcut_manager
    
    confirm = questionary.confirm(
        i18n.t("settings.shortcuts_reset_confirm"),
        default=False
    ).ask()
    if confirm:
        shortcut_manager.reset_shortcuts()
        console.print(f"[green]{i18n.t('settings.shortcuts_reset_success')}[/green]")
        time.sleep(1)

def change_shortcut(action):
    from weeb_cli.services.shortcuts import shortcut_manager, DEFAULT_SHORTCUTS
    
    current = shortcut_manager.get_shortcut(action)
    default = DEFAULT_SHORTCUTS.get(action, "")
    
    try:
        new_key = questionary.text(
            i18n.t("settings.enter_shortcut", action=action),
            default=current,
            qmark=">"
        ).ask()
        
        if not new_key:
            return
        
        if len(new_key) > 1:
            console.print(f"[yellow]{i18n.t('settings.shortcut_single_char')}[/yellow]")
            time.sleep(1)
            return
        
        shortcut_manager.set_shortcut(action, new_key)
        console.print(f"[green]{i18n.t('settings.shortcut_changed')}[/green]")
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        pass
