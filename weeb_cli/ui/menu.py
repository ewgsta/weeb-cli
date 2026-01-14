import questionary
from rich.console import Console
import sys
from .header import show_header
from weeb_cli.i18n import i18n
from weeb_cli.commands.search import search_anime
from weeb_cli.commands.settings import open_settings
from weeb_cli.commands.watchlist import show_watchlist
from weeb_cli.commands.downloads import show_downloads

console = Console()

def show_main_menu():
    console.clear()
    show_header("Weeb API", show_version=True, show_source=True)
    
    opt_search = i18n.get("menu.options.search")
    opt_downloads = i18n.get("menu.options.downloads")
    opt_watchlist = i18n.get("menu.options.watchlist")
    opt_settings = i18n.get("menu.options.settings")
    opt_exit = i18n.get("menu.options.exit")
    
    try:
        selected = questionary.select(
            i18n.get("menu.prompt"),
            choices=[
                opt_search,
                opt_downloads,
                opt_watchlist,
                opt_settings,
                opt_exit
            ],
            pointer=">",
            use_shortcuts=False,
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
        elif selected == opt_settings:
            open_settings()
        elif selected == opt_exit or selected is None:
            console.print(f"[yellow] {i18n.get('common.success')}...[/yellow]")
            sys.exit(0)
            
        show_main_menu()
        
    except KeyboardInterrupt:
        sys.exit(0)
