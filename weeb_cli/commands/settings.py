import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.config import config
import time
from weeb_cli.ui.header import show_header
import os
from weeb_cli.services.dependency_manager import dependency_manager

console = Console()


def toggle_config(key, name):
    current = config.get(key)
    new_val = not current
    
    if new_val:
        dep_name = name.lower()
        if "aria2" in dep_name: dep_name = "aria2"
        elif "yt-dlp" in dep_name: dep_name = "yt-dlp"
        
        path = dependency_manager.check_dependency(dep_name)
        if not path:
             console.print(f"[cyan]{i18n.t('setup.downloading', tool=name)}...[/cyan]")
             if not dependency_manager.install_dependency(dep_name):
                 console.print(f"[red]{i18n.t('setup.failed', tool=name)}[/red]")
                 time.sleep(1)
                 return

    config.set(key, new_val)
    
    msg_key = "settings.toggle_on" if new_val else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=name)}[/green]")
    time.sleep(0.5)

def open_settings():
    while True:
        console.clear()
        show_header(i18n.get("settings.title"))
        
        lang = config.get("language")
        source = config.get("scraping_source", "local")
        display_source = "weeb" if source == "local" else source

        aria2_state = i18n.get("common.enabled") if config.get("aria2_enabled") else i18n.get("common.disabled")
        ytdlp_state = i18n.get("common.enabled") if config.get("ytdlp_enabled") else i18n.get("common.disabled")
        desc_state = i18n.get("common.enabled") if config.get("show_description", True) else i18n.get("common.disabled")
        discord_rpc_state = i18n.get("common.enabled") if config.get("discord_rpc_enabled", False) else i18n.get("common.disabled")
        shortcuts_state = i18n.get("common.enabled") if config.get("shortcuts_enabled", True) else i18n.get("common.disabled")
        
        opt_lang = i18n.get("settings.language")
        opt_source = f"{i18n.get('settings.source')} [{display_source}]"
        opt_download = i18n.get("settings.download_settings")
        opt_drives = i18n.get("settings.external_drives")
        opt_desc = f"{i18n.get('settings.show_description')} [{desc_state}]"
        opt_discord_rpc = f"{i18n.get('settings.discord_rpc')} [{discord_rpc_state}]"
        opt_shortcuts_toggle = f"{i18n.get('settings.shortcuts')} [{shortcuts_state}]"
        opt_aria2 = f"{i18n.get('settings.aria2')} [{aria2_state}]"
        opt_ytdlp = f"{i18n.get('settings.ytdlp')} [{ytdlp_state}]"
        
        opt_aria2_conf = f"  ↳ {i18n.get('settings.aria2_config')}"
        opt_ytdlp_conf = f"  ↳ {i18n.get('settings.ytdlp_config')}"
        opt_shortcuts_conf = f"  ↳ {i18n.get('settings.shortcuts_config')}"
        opt_backup = i18n.get("settings.backup_restore")
        
        choices = [opt_lang, opt_source, opt_download, opt_drives, opt_desc, opt_discord_rpc, opt_shortcuts_toggle]
        
        if config.get("shortcuts_enabled", True):
            choices.append(opt_shortcuts_conf)
        
        choices.append(opt_aria2)
        if config.get("aria2_enabled"):
            choices.append(opt_aria2_conf)
            
        choices.append(opt_ytdlp)
        if config.get("ytdlp_enabled"):
            choices.append(opt_ytdlp_conf)
        
        opt_trackers = i18n.get("settings.trackers")
        choices.append(opt_trackers)
        choices.append(opt_backup)
        
        try:
            answer = questionary.select(
                i18n.get("settings.title"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
                style=questionary.Style([
                    ('pointer', 'fg:cyan bold'),
                    ('highlighted', 'fg:cyan'),
                    ('selected', 'fg:cyan bold'),
                ])
            ).ask()
        except KeyboardInterrupt:
            return

        if answer == opt_lang:
            change_language()
        elif answer == opt_source:
            change_source()
        elif answer == opt_download:
            download_settings_menu()
        elif answer == opt_drives:
            external_drives_menu()
        elif answer == opt_desc:
            toggle_description()
        elif answer == opt_discord_rpc:
            toggle_discord_rpc()
        elif answer == opt_shortcuts_toggle:
            toggle_shortcuts()
        elif answer == opt_shortcuts_conf:
            shortcuts_menu()
        elif answer == opt_aria2:
            toggle_config("aria2_enabled", "Aria2")
        elif answer == opt_aria2_conf:
            aria2_settings_menu()
        elif answer == opt_ytdlp:
            toggle_config("ytdlp_enabled", "yt-dlp")
        elif answer == opt_ytdlp_conf:
            ytdlp_settings_menu()
        elif answer == opt_trackers:
            trackers_menu()
        elif answer == opt_backup:
            backup_restore_menu()
        elif answer is None:
            return

def toggle_description():
    current = config.get("show_description", True)
    config.set("show_description", not current)
    msg_key = "settings.toggle_on" if not current else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=i18n.get('settings.show_description'))}[/green]")
    time.sleep(0.5)

def toggle_discord_rpc():
    from weeb_cli.services.discord_rpc import discord_rpc
    
    current = config.get("discord_rpc_enabled", False)
    new_val = not current
    config.set("discord_rpc_enabled", new_val)
    
    if new_val:
        discord_rpc.connect()
    else:
        discord_rpc.disconnect()
    
    msg_key = "settings.toggle_on" if new_val else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool='Discord RPC')}[/green]")
    time.sleep(0.5)

def toggle_shortcuts():
    current = config.get("shortcuts_enabled", True)
    new_val = not current
    config.set("shortcuts_enabled", new_val)
    
    msg_key = "settings.toggle_on" if new_val else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=i18n.get('settings.shortcuts'))}[/green]")
    time.sleep(0.5)

def change_language():
    from weeb_cli.services.scraper import scraper
    
    langs = {"Türkçe": "tr", "English": "en"}
    try:
        selected = questionary.select(
            "Select Language / Dil Seçiniz:",
            choices=list(langs.keys()),
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if selected:
            lang_code = langs[selected]
            i18n.set_language(lang_code)
            
            # Dil için varsayılan kaynağı ayarla
            sources = scraper.get_sources_for_lang(lang_code)
            if sources:
                config.set("scraping_source", sources[0])
            
            console.print(f"[green]{i18n.get('settings.language_changed')}[/green]")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def change_source():
    from weeb_cli.services.scraper import scraper
    
    current_lang = config.get("language", "tr")
    sources = scraper.get_sources_for_lang(current_lang)
    
    if not sources:
        console.print(f"[yellow]{i18n.get('settings.no_sources')}[/yellow]")
        time.sleep(1)
        return
        
    try:
        selected = questionary.select(
            i18n.get("settings.source"),
            choices=sources,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if selected:
            config.set("scraping_source", selected)
            console.print(f"[green]{i18n.t('settings.source_changed', source=selected)}[/green]")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        


def aria2_settings_menu():
    while True:
        console.clear()
        show_header(i18n.get("settings.aria2_config"))
        
        curr_conn = config.get("aria2_max_connections", 16)
        
        opt_conn = f"{i18n.get('settings.max_conn')} [{curr_conn}]"
        
        try:
            sel = questionary.select(
                i18n.get("settings.aria2_config"),
                choices=[opt_conn],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel == opt_conn:
                val = questionary.text(f"{i18n.get('settings.enter_conn')}:", default=str(curr_conn)).ask()
                if val and val.isdigit():
                    config.set("aria2_max_connections", int(val))
            elif sel is None:
                return
        except KeyboardInterrupt:
            return

def download_settings_menu():
    while True:
        console.clear()
        show_header(i18n.get("settings.download_settings"))
        
        curr_dir = config.get("download_dir")
        console.print(f"[dim]Current: {curr_dir}[/dim]\n", justify="left")
        
        curr_concurrent = config.get("max_concurrent_downloads", 3)
        curr_retries = config.get("download_max_retries", 3)
        curr_delay = config.get("download_retry_delay", 10)
        
        opt_name = i18n.get("settings.change_folder_name")
        opt_path = i18n.get("settings.change_full_path")
        opt_concurrent = f"{i18n.get('settings.concurrent_downloads')} [{curr_concurrent}]"
        opt_retries = f"{i18n.get('settings.max_retries')} [{curr_retries}]"
        opt_delay = f"{i18n.get('settings.retry_delay')} [{curr_delay}s]"
        
        try:
            sel = questionary.select(
                i18n.get("settings.download_settings"),
                choices=[opt_name, opt_path, opt_concurrent, opt_retries, opt_delay],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel == opt_name:
                val = questionary.text("Folder Name:", default="weeb-downloads").ask()
                if val:
                    new_path = os.path.join(os.getcwd(), val)
                    config.set("download_dir", new_path)
            elif sel == opt_path:
                val = questionary.text("Full Path:", default=curr_dir).ask()
                if val:
                    config.set("download_dir", val)
            elif sel == opt_concurrent:
                val = questionary.text(i18n.get("settings.enter_concurrent"), default=str(curr_concurrent)).ask()
                if val and val.isdigit():
                    n = int(val)
                    if 1 <= n <= 5:
                        config.set("max_concurrent_downloads", n)
            elif sel == opt_retries:
                val = questionary.text(i18n.get("settings.enter_max_retries"), default=str(curr_retries)).ask()
                if val and val.isdigit():
                    n = int(val)
                    if 0 <= n <= 10:
                        config.set("download_max_retries", n)
            elif sel == opt_delay:
                val = questionary.text(i18n.get("settings.enter_retry_delay"), default=str(curr_delay)).ask()
                if val and val.isdigit():
                    config.set("download_retry_delay", int(val))
            elif sel is None:
                return
        except KeyboardInterrupt:
            return


def ytdlp_settings_menu():
    while True:
        console.clear()
        show_header(i18n.get("settings.ytdlp_config"))
        
        curr_fmt = config.get("ytdlp_format", "best")
        opt_fmt = f"{i18n.get('settings.format')} [{curr_fmt}]"
        
        try:
            sel = questionary.select(
                i18n.get("settings.ytdlp_config"), 
                choices=[opt_fmt], 
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel == opt_fmt:
                val = questionary.text(f"{i18n.get('settings.enter_format')}:", default=curr_fmt).ask()
                if val:
                    config.set("ytdlp_format", val)
            elif sel is None:
                return
        except KeyboardInterrupt:
            return


def external_drives_menu():
    from weeb_cli.services.local_library import local_library
    from pathlib import Path
    
    while True:
        console.clear()
        show_header(i18n.get("settings.external_drives"))
        
        drives = local_library.get_external_drives()
        
        opt_add = i18n.get("settings.add_drive")
        
        choices = [questionary.Choice(opt_add, value="add")]
        
        for drive in drives:
            path = Path(drive["path"])
            status = "● " if path.exists() else "○ "
            choices.append(questionary.Choice(
                f"{status}{drive['name']} ({drive['path']})",
                value=drive
            ))
        
        try:
            sel = questionary.select(
                i18n.get("settings.external_drives"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == "add":
                add_external_drive()
            else:
                manage_drive(sel)
                
        except KeyboardInterrupt:
            return

def add_external_drive():
    from weeb_cli.services.local_library import local_library
    
    try:
        path = questionary.text(
            i18n.get("settings.enter_drive_path"),
            qmark=">"
        ).ask()
        
        if not path:
            return
        
        from pathlib import Path
        if not Path(path).exists():
            console.print(f"[yellow]{i18n.get('settings.drive_not_found')}[/yellow]")
            time.sleep(1)
            return
        
        name = questionary.text(
            i18n.get("settings.enter_drive_name"),
            default=os.path.basename(path) or path,
            qmark=">"
        ).ask()
        
        if name:
            local_library.add_external_drive(path, name)
            console.print(f"[green]{i18n.get('settings.drive_added')}[/green]")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        pass

def manage_drive(drive):
    from weeb_cli.services.local_library import local_library
    
    while True:
        console.clear()
        show_header(drive["name"])
        
        console.print(f"[dim]{drive['path']}[/dim]\n")
        
        opt_rename = i18n.get("settings.rename_drive")
        opt_remove = i18n.get("settings.remove_drive")
        
        try:
            sel = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=[opt_rename, opt_remove],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_rename:
                new_name = questionary.text(
                    i18n.get("settings.enter_drive_name"),
                    default=drive["name"],
                    qmark=">"
                ).ask()
                if new_name:
                    local_library.rename_external_drive(drive["path"], new_name)
                    drive["name"] = new_name
                    console.print(f"[green]{i18n.get('settings.drive_renamed')}[/green]")
                    time.sleep(0.5)
                    
            elif sel == opt_remove:
                confirm = questionary.confirm(
                    i18n.get("settings.confirm_remove"),
                    default=False
                ).ask()
                if confirm:
                    local_library.remove_external_drive(drive["path"])
                    console.print(f"[green]{i18n.get('settings.drive_removed')}[/green]")
                    time.sleep(0.5)
                    return
                    
        except KeyboardInterrupt:
            return


def trackers_menu():
    while True:
        console.clear()
        show_header(i18n.get("settings.trackers"))
        
        opt_anilist = "AniList"
        opt_mal = "MyAnimeList"
        
        try:
            sel = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=[opt_anilist, opt_mal],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_anilist:
                anilist_settings_menu()
            elif sel == opt_mal:
                mal_settings_menu()
                
        except KeyboardInterrupt:
            return


def anilist_settings_menu():
    from weeb_cli.services.tracker import anilist_tracker
    
    while True:
        console.clear()
        show_header("AniList")
        
        if anilist_tracker.is_authenticated():
            username = anilist_tracker.get_username()
            console.print(f"[green]{i18n.t('settings.anilist_connected', user=username)}[/green]\n")
            
            pending = anilist_tracker.get_pending_count()
            if pending > 0:
                console.print(f"[yellow]{i18n.t('settings.anilist_pending', count=pending)}[/yellow]\n")
            
            opt_sync = i18n.get("settings.anilist_sync")
            opt_logout = i18n.get("settings.anilist_logout")
            
            choices = []
            if pending > 0:
                choices.append(opt_sync)
            choices.append(opt_logout)
            
            try:
                sel = questionary.select(
                    i18n.get("downloads.action_prompt"),
                    choices=choices,
                    pointer=">",
                    use_shortcuts=False
                ).ask()
                
                if sel is None:
                    return
                
                if sel == opt_sync:
                    with console.status(i18n.get("common.processing"), spinner="dots"):
                        synced = anilist_tracker.sync_pending()
                    console.print(f"[green]{i18n.t('settings.anilist_synced', count=synced)}[/green]")
                    time.sleep(1)
                elif sel == opt_logout:
                    confirm = questionary.confirm(
                        i18n.get("settings.confirm_logout"),
                        default=False
                    ).ask()
                    if confirm:
                        anilist_tracker.logout()
                        console.print(f"[green]{i18n.get('settings.anilist_logged_out')}[/green]")
                        time.sleep(1)
                        return
                        
            except KeyboardInterrupt:
                return
        else:
            console.print(f"[dim]{i18n.get('settings.anilist_not_connected')}[/dim]\n")
            
            opt_login = i18n.get("settings.anilist_login")
            
            try:
                sel = questionary.select(
                    i18n.get("downloads.action_prompt"),
                    choices=[opt_login],
                    pointer=">",
                    use_shortcuts=False
                ).ask()
                
                if sel is None:
                    return
                
                if sel == opt_login:
                    console.print(f"\n[cyan]{i18n.get('settings.anilist_opening_browser')}[/cyan]")
                    console.print(f"[dim]{i18n.get('settings.anilist_waiting')}[/dim]\n")
                    
                    with console.status(i18n.get("common.processing"), spinner="dots"):
                        token = anilist_tracker.start_auth_server(timeout=120)
                    
                    if token:
                        success = anilist_tracker.authenticate(token)
                        if success:
                            console.print(f"[green]{i18n.get('settings.anilist_login_success')}[/green]")
                        else:
                            console.print(f"[red]{i18n.get('settings.anilist_login_failed')}[/red]")
                    else:
                        console.print(f"[yellow]{i18n.get('settings.anilist_timeout')}[/yellow]")
                    time.sleep(1)
                        
            except KeyboardInterrupt:
                return


def mal_settings_menu():
    from weeb_cli.services.tracker import mal_tracker
    
    while True:
        console.clear()
        show_header("MyAnimeList")
        
        if mal_tracker.is_authenticated():
            username = mal_tracker.get_username()
            console.print(f"[green]{i18n.t('settings.mal_connected', user=username)}[/green]\n")
            
            pending = mal_tracker.get_pending_count()
            if pending > 0:
                console.print(f"[yellow]{i18n.t('settings.mal_pending', count=pending)}[/yellow]\n")
            
            opt_sync = i18n.get("settings.mal_sync")
            opt_logout = i18n.get("settings.mal_logout")
            
            choices = []
            if pending > 0:
                choices.append(opt_sync)
            choices.append(opt_logout)
            
            try:
                sel = questionary.select(
                    i18n.get("downloads.action_prompt"),
                    choices=choices,
                    pointer=">",
                    use_shortcuts=False
                ).ask()
                
                if sel is None:
                    return
                
                if sel == opt_sync:
                    with console.status(i18n.get("common.processing"), spinner="dots"):
                        synced = mal_tracker.sync_pending()
                    console.print(f"[green]{i18n.t('settings.mal_synced', count=synced)}[/green]")
                    time.sleep(1)
                elif sel == opt_logout:
                    confirm = questionary.confirm(
                        i18n.get("settings.confirm_logout"),
                        default=False
                    ).ask()
                    if confirm:
                        mal_tracker.logout()
                        console.print(f"[green]{i18n.get('settings.mal_logged_out')}[/green]")
                        time.sleep(1)
                        return
                        
            except KeyboardInterrupt:
                return
        else:
            console.print(f"[dim]{i18n.get('settings.mal_not_connected')}[/dim]\n")
            
            opt_login = i18n.get("settings.mal_login")
            
            try:
                sel = questionary.select(
                    i18n.get("downloads.action_prompt"),
                    choices=[opt_login],
                    pointer=">",
                    use_shortcuts=False
                ).ask()
                
                if sel is None:
                    return
                
                if sel == opt_login:
                    console.print(f"\n[cyan]{i18n.get('settings.mal_opening_browser')}[/cyan]")
                    console.print(f"[dim]{i18n.get('settings.mal_waiting')}[/dim]\n")
                    
                    with console.status(i18n.get("common.processing"), spinner="dots"):
                        user = mal_tracker.start_auth_flow(timeout=120)
                    
                    if user:
                        console.print(f"[green]{i18n.get('settings.mal_login_success')}[/green]")
                    else:
                        console.print(f"[red]{i18n.get('settings.mal_login_failed')}[/red]")
                    time.sleep(1)
                        
            except KeyboardInterrupt:
                return


def backup_restore_menu():
    from weeb_cli.services.database import db
    from pathlib import Path
    
    while True:
        console.clear()
        show_header(i18n.get("settings.backup_restore"))
        
        db_size = db.db_path.stat().st_size / 1024
        console.print(f"[dim]{i18n.get('settings.db_location')}: {db.db_path}[/dim]")
        console.print(f"[dim]{i18n.get('settings.db_size')}: {db_size:.2f} KB[/dim]\n")
        
        opt_backup = i18n.get("settings.create_backup")
        opt_restore = i18n.get("settings.restore_backup")
        
        try:
            sel = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=[opt_backup, opt_restore],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_backup:
                create_backup()
            elif sel == opt_restore:
                restore_backup()
                
        except KeyboardInterrupt:
            return

def create_backup():
    from weeb_cli.services.database import db
    from pathlib import Path
    from datetime import datetime
    
    default_name = f"weeb-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.db"
    
    try:
        path = questionary.text(
            i18n.get("settings.backup_path"),
            default=default_name,
            qmark=">"
        ).ask()
        
        if not path:
            return
        
        backup_path = Path(path)
        if not backup_path.suffix:
            backup_path = backup_path.with_suffix('.db')
        
        with console.status(i18n.get("common.processing"), spinner="dots"):
            success = db.backup_database(backup_path)
        
        if success:
            console.print(f"[green]{i18n.get('settings.backup_success')}[/green]")
            console.print(f"[dim]{backup_path.absolute()}[/dim]")
        else:
            console.print(f"[red]{i18n.get('settings.backup_failed')}[/red]")
        
        time.sleep(2)
        
    except KeyboardInterrupt:
        pass

def restore_backup():
    from weeb_cli.services.database import db
    from pathlib import Path
    
    try:
        path = questionary.text(
            i18n.get("settings.restore_path"),
            qmark=">"
        ).ask()
        
        if not path:
            return
        
        backup_path = Path(path)
        
        if not backup_path.exists():
            console.print(f"[red]{i18n.get('settings.backup_not_found')}[/red]")
            time.sleep(1.5)
            return
        
        confirm = questionary.confirm(
            i18n.get("settings.restore_confirm"),
            default=False
        ).ask()
        
        if not confirm:
            return
        
        with console.status(i18n.get("common.processing"), spinner="dots"):
            success = db.restore_database(backup_path)
        
        if success:
            console.print(f"[green]{i18n.get('settings.restore_success')}[/green]")
            console.print(f"[yellow]{i18n.get('settings.restart_required')}[/yellow]")
        else:
            console.print(f"[red]{i18n.get('settings.restore_failed')}[/red]")
        
        time.sleep(2)
        
    except KeyboardInterrupt:
        pass

# dursun zaman dokunduğunda sana yine yakınlaştığımda bana öyle baktığındaaaaaaa sessizzceeee  uyandığında sana yine dokunduğumda dursun zaman


def shortcuts_menu():
    from weeb_cli.services.shortcuts import shortcut_manager, DEFAULT_SHORTCUTS
    
    while True:
        console.clear()
        show_header(i18n.get("settings.shortcuts"))
        
        shortcuts = shortcut_manager.get_shortcuts()
        
        console.print(f"[dim]{i18n.get('settings.shortcuts_hint')}[/dim]\n")
        
        opt_search = f"{i18n.get('settings.shortcut_search')} [{shortcuts['search']}]"
        opt_downloads = f"{i18n.get('settings.shortcut_downloads')} [{shortcuts['downloads']}]"
        opt_watchlist = f"{i18n.get('settings.shortcut_watchlist')} [{shortcuts['watchlist']}]"
        opt_settings = f"{i18n.get('settings.shortcut_settings')} [{shortcuts['settings']}]"
        opt_exit = f"{i18n.get('settings.shortcut_exit')} [{shortcuts['exit']}]"
        opt_next = f"{i18n.get('settings.shortcut_next_episode')} [{shortcuts['next_episode']}]"
        opt_prev = f"{i18n.get('settings.shortcut_prev_episode')} [{shortcuts['prev_episode']}]"
        opt_back = f"{i18n.get('settings.shortcut_back')} [{shortcuts['back']}]"
        opt_help = f"{i18n.get('settings.shortcut_help')} [{shortcuts['help']}]"
        opt_reset = i18n.get("settings.shortcuts_reset")
        
        choices = [
            opt_search,
            opt_downloads,
            opt_watchlist,
            opt_settings,
            opt_exit,
            opt_next,
            opt_prev,
            opt_back,
            opt_help,
            opt_reset
        ]
        
        try:
            sel = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_reset:
                confirm = questionary.confirm(
                    i18n.get("settings.shortcuts_reset_confirm"),
                    default=False
                ).ask()
                if confirm:
                    shortcut_manager.reset_shortcuts()
                    console.print(f"[green]{i18n.get('settings.shortcuts_reset_success')}[/green]")
                    time.sleep(1)
            else:
                action_map = {
                    opt_search: "search",
                    opt_downloads: "downloads",
                    opt_watchlist: "watchlist",
                    opt_settings: "settings",
                    opt_exit: "exit",
                    opt_next: "next_episode",
                    opt_prev: "prev_episode",
                    opt_back: "back",
                    opt_help: "help"
                }
                
                action = action_map.get(sel)
                if action:
                    change_shortcut(action)
                    
        except KeyboardInterrupt:
            return

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
            console.print(f"[yellow]{i18n.get('settings.shortcut_single_char')}[/yellow]")
            time.sleep(1)
            return
        
        shortcut_manager.set_shortcut(action, new_key)
        console.print(f"[green]{i18n.get('settings.shortcut_changed')}[/green]")
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        pass
