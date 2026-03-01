import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header

console = Console()

def trackers_menu():
    while True:
        console.clear()
        show_header(i18n.t("settings.trackers"))
        
        opt_anilist = "AniList"
        opt_mal = "MyAnimeList"
        opt_kitsu = "Kitsu"
        
        try:
            sel = questionary.select(
                i18n.t("downloads.action_prompt"),
                choices=[opt_anilist, opt_mal, opt_kitsu],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_anilist:
                anilist_settings_menu()
            elif sel == opt_mal:
                mal_settings_menu()
            elif sel == opt_kitsu:
                kitsu_settings_menu()
                
        except KeyboardInterrupt:
            return

def anilist_settings_menu():
    from weeb_cli.services.tracker import anilist_tracker
    
    while True:
        console.clear()
        show_header("AniList")
        
        if anilist_tracker.is_authenticated():
            _handle_authenticated_anilist()
        else:
            _handle_unauthenticated_anilist()

def _handle_authenticated_anilist():
    from weeb_cli.services.tracker import anilist_tracker
    
    username = anilist_tracker.get_username()
    console.print(f"[green]{i18n.t('settings.anilist_connected', user=username)}[/green]\n")
    
    pending = anilist_tracker.get_pending_count()
    if pending > 0:
        console.print(f"[yellow]{i18n.t('settings.anilist_pending', count=pending)}[/yellow]\n")
    
    opt_sync = i18n.t("settings.anilist_sync")
    opt_logout = i18n.t("settings.anilist_logout")
    
    choices = []
    if pending > 0:
        choices.append(opt_sync)
    choices.append(opt_logout)
    
    try:
        sel = questionary.select(
            i18n.t("downloads.action_prompt"),
            choices=choices,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if sel is None:
            return
        
        if sel == opt_sync:
            with console.status(i18n.t("common.processing"), spinner="dots"):
                synced = anilist_tracker.sync_pending()
            console.print(f"[green]{i18n.t('settings.anilist_synced', count=synced)}[/green]")
            time.sleep(1)
        elif sel == opt_logout:
            confirm = questionary.confirm(
                i18n.t("settings.confirm_logout"),
                default=False
            ).ask()
            if confirm:
                anilist_tracker.logout()
                console.print(f"[green]{i18n.t('settings.anilist_logged_out')}[/green]")
                time.sleep(1)
                return
                
    except KeyboardInterrupt:
        return

def _handle_unauthenticated_anilist():
    from weeb_cli.services.tracker import anilist_tracker
    
    console.print(f"[dim]{i18n.t('settings.anilist_not_connected')}[/dim]\n")
    
    opt_login = i18n.t("settings.anilist_login")
    
    try:
        sel = questionary.select(
            i18n.t("downloads.action_prompt"),
            choices=[opt_login],
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if sel is None:
            return
        
        if sel == opt_login:
            console.print(f"\n[cyan]{i18n.t('settings.anilist_opening_browser')}[/cyan]")
            console.print(f"[dim]{i18n.t('settings.anilist_waiting')}[/dim]\n")
            
            with console.status(i18n.t("common.processing"), spinner="dots"):
                token = anilist_tracker.start_auth_server(timeout=120)
            
            if token:
                success = anilist_tracker.authenticate(token)
                if success:
                    console.print(f"[green]{i18n.t('settings.anilist_login_success')}[/green]")
                else:
                    console.print(f"[red]{i18n.t('settings.anilist_login_failed')}[/red]")
            else:
                console.print(f"[yellow]{i18n.t('settings.anilist_timeout')}[/yellow]")
            time.sleep(1)
                
    except KeyboardInterrupt:
        return

def mal_settings_menu():
    from weeb_cli.services.tracker import mal_tracker
    
    while True:
        console.clear()
        show_header("MyAnimeList")
        
        if mal_tracker.is_authenticated():
            _handle_authenticated_mal()
        else:
            _handle_unauthenticated_mal()

def _handle_authenticated_mal():
    from weeb_cli.services.tracker import mal_tracker
    
    username = mal_tracker.get_username()
    console.print(f"[green]{i18n.t('settings.mal_connected', user=username)}[/green]\n")
    
    pending = mal_tracker.get_pending_count()
    if pending > 0:
        console.print(f"[yellow]{i18n.t('settings.mal_pending', count=pending)}[/yellow]\n")
    
    opt_sync = i18n.t("settings.mal_sync")
    opt_logout = i18n.t("settings.mal_logout")
    
    choices = []
    if pending > 0:
        choices.append(opt_sync)
    choices.append(opt_logout)
    
    try:
        sel = questionary.select(
            i18n.t("downloads.action_prompt"),
            choices=choices,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if sel is None:
            return
        
        if sel == opt_sync:
            with console.status(i18n.t("common.processing"), spinner="dots"):
                synced = mal_tracker.sync_pending()
            console.print(f"[green]{i18n.t('settings.mal_synced', count=synced)}[/green]")
            time.sleep(1)
        elif sel == opt_logout:
            confirm = questionary.confirm(
                i18n.t("settings.confirm_logout"),
                default=False
            ).ask()
            if confirm:
                mal_tracker.logout()
                console.print(f"[green]{i18n.t('settings.mal_logged_out')}[/green]")
                time.sleep(1)
                return
                
    except KeyboardInterrupt:
        return

def _handle_unauthenticated_mal():
    from weeb_cli.services.tracker import mal_tracker
    
    console.print(f"[dim]{i18n.t('settings.mal_not_connected')}[/dim]\n")
    
    opt_login = i18n.t("settings.mal_login")
    
    try:
        sel = questionary.select(
            i18n.t("downloads.action_prompt"),
            choices=[opt_login],
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if sel is None:
            return
        
        if sel == opt_login:
            console.print(f"\n[cyan]{i18n.t('settings.mal_opening_browser')}[/cyan]")
            console.print(f"[dim]{i18n.t('settings.mal_waiting')}[/dim]\n")
            
            with console.status(i18n.t("common.processing"), spinner="dots"):
                user = mal_tracker.start_auth_flow(timeout=120)
            
            if user:
                console.print(f"[green]{i18n.t('settings.mal_login_success')}[/green]")
            else:
                console.print(f"[red]{i18n.t('settings.mal_login_failed')}[/red]")
            time.sleep(1)
                
    except KeyboardInterrupt:
        return


def kitsu_settings_menu():
    from weeb_cli.services.tracker import kitsu_tracker
    
    while True:
        console.clear()
        show_header("Kitsu")
        
        try:
            if kitsu_tracker.is_authenticated():
                should_continue = _handle_authenticated_kitsu()
                if not should_continue:
                    return
            else:
                should_continue = _handle_unauthenticated_kitsu()
                if not should_continue:
                    return
        except KeyboardInterrupt:
            return

def _handle_authenticated_kitsu():
    from weeb_cli.services.tracker import kitsu_tracker
    
    username = kitsu_tracker.get_username()
    console.print(f"[green]{i18n.t('settings.kitsu_connected', user=username)}[/green]\n")
    
    pending = kitsu_tracker.get_pending_count()
    if pending > 0:
        console.print(f"[yellow]{i18n.t('settings.kitsu_pending', count=pending)}[/yellow]\n")
    
    opt_sync = i18n.t("settings.kitsu_sync")
    opt_logout = i18n.t("settings.kitsu_logout")
    
    choices = []
    if pending > 0:
        choices.append(opt_sync)
    choices.append(opt_logout)
    
    try:
        sel = questionary.select(
            i18n.t("downloads.action_prompt"),
            choices=choices,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if sel is None:
            return False
        
        if sel == opt_sync:
            with console.status(i18n.t("common.processing"), spinner="dots"):
                synced = kitsu_tracker.sync_pending()
            console.print(f"[green]{i18n.t('settings.kitsu_synced', count=synced)}[/green]")
            time.sleep(1)
            return True
        elif sel == opt_logout:
            confirm = questionary.confirm(
                i18n.t("settings.confirm_logout"),
                default=False
            ).ask()
            if confirm:
                kitsu_tracker.logout()
                console.print(f"[green]{i18n.t('settings.kitsu_logged_out')}[/green]")
                time.sleep(1)
            return True
                
    except KeyboardInterrupt:
        return False

def _handle_unauthenticated_kitsu():
    from weeb_cli.services.tracker import kitsu_tracker
    
    console.print(f"[dim]{i18n.t('settings.kitsu_not_connected')}[/dim]\n")
    
    opt_login = i18n.t("settings.kitsu_login")
    
    try:
        sel = questionary.select(
            i18n.t("downloads.action_prompt"),
            choices=[opt_login],
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if sel is None:
            return False
        
        if sel == opt_login:
            console.print(f"\n[cyan]{i18n.t('settings.kitsu_enter_credentials')}[/cyan]\n")
            
            email = questionary.text(
                i18n.t("settings.kitsu_email"),
                validate=lambda x: len(x) > 0
            ).ask()
            
            if not email:
                return False
            
            password = questionary.password(
                i18n.t("settings.kitsu_password"),
                validate=lambda x: len(x) > 0
            ).ask()
            
            if not password:
                return False
            
            with console.status(i18n.t("common.processing"), spinner="dots"):
                success = kitsu_tracker.authenticate(email, password)
            
            if success:
                console.print(f"[green]{i18n.t('settings.kitsu_login_success')}[/green]")
            else:
                console.print(f"[red]{i18n.t('settings.kitsu_login_failed')}[/red]")
            time.sleep(1)
            return True
                
    except KeyboardInterrupt:
        return False
