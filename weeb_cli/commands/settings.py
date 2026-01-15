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
        
        opt_lang = i18n.get("settings.language")
        opt_source = f"{i18n.get('settings.source')} [{display_source}]"
        opt_download = i18n.get("settings.download_settings")
        opt_drives = i18n.get("settings.external_drives")
        opt_desc = f"{i18n.get('settings.show_description')} [{desc_state}]"
        opt_aria2 = f"{i18n.get('settings.aria2')} [{aria2_state}]"
        opt_ytdlp = f"{i18n.get('settings.ytdlp')} [{ytdlp_state}]"
        
        opt_aria2_conf = f"  ↳ {i18n.get('settings.aria2_config')}"
        opt_ytdlp_conf = f"  ↳ {i18n.get('settings.ytdlp_config')}"
        
        choices = [opt_lang, opt_source, opt_download, opt_drives, opt_desc, opt_aria2]
        if config.get("aria2_enabled"):
            choices.append(opt_aria2_conf)
            
        choices.append(opt_ytdlp)
        if config.get("ytdlp_enabled"):
            choices.append(opt_ytdlp_conf)
        
        opt_anilist = i18n.get("settings.anilist")
        choices.append(opt_anilist)
        
        opt_mal = i18n.get("settings.mal")
        choices.append(opt_mal)
        
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
        elif answer == opt_aria2:
            toggle_config("aria2_enabled", "Aria2")
        elif answer == opt_aria2_conf:
            aria2_settings_menu()
        elif answer == opt_ytdlp:
            toggle_config("ytdlp_enabled", "yt-dlp")
        elif answer == opt_ytdlp_conf:
            ytdlp_settings_menu()
        elif answer == opt_anilist:
            anilist_settings_menu()
        elif answer == opt_mal:
            mal_settings_menu()
        elif answer is None:
            return

def toggle_description():
    current = config.get("show_description", True)
    config.set("show_description", not current)
    msg_key = "settings.toggle_on" if not current else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=i18n.get('settings.show_description'))}[/green]")
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
        
        opt_name = i18n.get("settings.change_folder_name")
        opt_path = i18n.get("settings.change_full_path")
        opt_concurrent = f"{i18n.get('settings.concurrent_downloads')} [{curr_concurrent}]"
        
        try:
            sel = questionary.select(
                i18n.get("settings.download_settings"),
                choices=[opt_name, opt_path, opt_concurrent],
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
