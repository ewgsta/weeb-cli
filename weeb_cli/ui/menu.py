import questionary
from rich.console import Console
import sys
from .header import show_header
from weeb_cli.i18n import i18n
from weeb_cli.commands.search import search_anime
from weeb_cli.commands.settings import open_settings
from weeb_cli.commands.watchlist import show_watchlist
from weeb_cli.commands.downloads import show_downloads, show_queue_live, manage_queue
from weeb_cli.services.downloader import queue_manager
from weeb_cli.services.shortcuts import shortcut_manager

console = Console()

def _handle_exit():
    active_count = queue_manager.get_active_count()
    pending_count = queue_manager.get_pending_count()
    
    if active_count > 0 or pending_count > 0:
        total = active_count + pending_count
        try:
            confirm = questionary.confirm(
                i18n.get("menu.exit_confirm_downloads", f"{total} aktif indirme var. Çıkmak istediğinize emin misiniz?"),
                default=False
            ).ask()
            
            if confirm:
                queue_manager.stop_queue()
                console.print(f"[yellow]{i18n.get('downloads.queue_stopped')}[/yellow]")
                console.print(f"[yellow] {i18n.get('common.success')}...[/yellow]")
                sys.exit(0)
            else:
                return False 
        except KeyboardInterrupt:
            return False
    else:
        console.print(f"[yellow] {i18n.get('common.success')}...[/yellow]")
        sys.exit(0)
    
    return True

def show_main_menu():
    console.clear()
    show_header("Weeb CLI", show_version=True, show_source=True)
    
    shortcuts = shortcut_manager.get_shortcuts()
    
    opt_search = f"{i18n.get('menu.options.search')} [{shortcuts['search']}]"
    opt_downloads = f"{i18n.get('menu.options.downloads')} [{shortcuts['downloads']}]"
    opt_watchlist = f"{i18n.get('menu.options.watchlist')} [{shortcuts['watchlist']}]"
    opt_settings = f"{i18n.get('menu.options.settings')} [{shortcuts['settings']}]"
    opt_exit = f"{i18n.get('menu.options.exit')} [{shortcuts['exit']}]"
    
    choices = [
        questionary.Choice(opt_search, shortcut_key=shortcuts['search']),
        questionary.Choice(opt_downloads, shortcut_key=shortcuts['downloads']),
        questionary.Choice(opt_watchlist, shortcut_key=shortcuts['watchlist']),
    ]
    
    active_queue = [i for i in queue_manager.queue if i["status"] in ["pending", "processing"]]
    opt_active = None
    if active_queue or queue_manager.queue:
        is_running = queue_manager.is_running()
        status = i18n.get("downloads.queue_running") if is_running else i18n.get("downloads.queue_stopped")
        opt_active = f"{i18n.get('downloads.active_downloads')} ({len(active_queue)}) - {status}"
        choices.append(questionary.Choice(opt_active))
    
    choices.extend([
        questionary.Choice(opt_settings, shortcut_key=shortcuts['settings']),
        questionary.Choice(opt_exit, shortcut_key=shortcuts['exit'])
    ])
    
    try:
        selected = questionary.select(
            i18n.get("menu.prompt"),
            choices=choices,
            pointer=">",
            use_shortcuts=True,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan'),
                ('selected', 'fg:cyan bold'),
            ])
        ).ask()
        
        console.clear()
        
        if selected == opt_search:
            search_anime()
        elif selected == opt_watchlist:
            show_watchlist()
        elif selected == opt_downloads:
            show_downloads()
        elif opt_active and selected == opt_active:
            show_active_downloads_menu()
        elif selected == opt_settings:
            open_settings()
        elif selected == opt_exit or selected is None:
            _handle_exit()
            
        show_main_menu()
        
    except KeyboardInterrupt:
        if not _handle_exit():
            show_main_menu()

def show_active_downloads_menu():
    while True:
        console.clear()
        show_header(i18n.get("downloads.active_downloads"))
        
        pending = queue_manager.get_pending_count()
        failed = queue_manager.get_failed_count()
        is_running = queue_manager.is_running()
        
        if pending > 0:
            status = i18n.get("downloads.queue_running") if is_running else i18n.get("downloads.queue_stopped")
            console.print(f"[cyan]{i18n.t('downloads.pending_count', count=pending)}[/cyan] - {status}\n")
        
        if failed > 0:
            console.print(f"[red]{failed} başarısız indirme[/red]\n")
        
        opt_view = i18n.get("downloads.view_queue")
        opt_start = i18n.get("downloads.start_queue")
        opt_stop = i18n.get("downloads.stop_queue")
        opt_clear = i18n.get("downloads.clear_completed")
        opt_retry = i18n.get("downloads.retry_failed", "Başarısızları Yeniden Dene")
        
        choices = [opt_view]
        if pending > 0:
            if is_running:
                choices.append(opt_stop)
            else:
                choices.append(opt_start)
        if failed > 0:
            choices.append(opt_retry)
        choices.append(opt_clear)
        
        try:
            import time
            action = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if action is None:
                return
            
            if action == opt_view:
                show_queue_live()
            elif action == opt_start:
                queue_manager.start_queue()
                console.print(f"[green]{i18n.get('downloads.queue_started')}[/green]")
                time.sleep(0.5)
            elif action == opt_stop:
                queue_manager.stop_queue()
                console.print(f"[yellow]{i18n.get('downloads.queue_stopped')}[/yellow]")
                time.sleep(0.5)
            elif action == opt_retry:
                count = queue_manager.retry_failed()
                console.print(f"[green]{count} indirme yeniden deneniyor...[/green]")
                time.sleep(0.5)
            elif action == opt_clear:
                queue_manager.clear_completed()
                console.print(f"[green]{i18n.get('downloads.cleared')}[/green]")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            return
