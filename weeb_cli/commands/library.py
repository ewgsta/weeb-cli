import questionary
from pathlib import Path
from rich.console import Console
from rich.table import Table
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.local_library import local_library
from weeb_cli.config import config

console = Console()

def show_library_menu():
    while True:
        console.clear()
        show_header(i18n.t("menu.options.library"))
        
        virtual_count = len(local_library.get_virtual_library())
        indexed_count = len(local_library.get_indexed_anime())
        
        console.print(f"[cyan]{i18n.t('library.online_library')}:[/cyan] {virtual_count} anime")
        console.print(f"[cyan]{i18n.t('library.local_library')}:[/cyan] {indexed_count} anime\n")
        
        opt_online = i18n.t("library.online_library")
        opt_local = i18n.t("library.local_library")
        
        try:
            choice = questionary.select(
                i18n.t("library.select_type"),
                choices=[opt_online, opt_local],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if choice is None:
                return
            
            if choice == opt_online:
                show_virtual_library()
            elif choice == opt_local:
                show_local_library()
                
        except KeyboardInterrupt:
            return

def show_virtual_library():
    while True:
        console.clear()
        show_header(i18n.t("library.online_library"))
        
        library = local_library.get_virtual_library()
        
        if not library:
            console.print(f"[dim]{i18n.t('library.online_empty')}[/dim]")
            try:
                input(i18n.t("common.continue_key"))
            except KeyboardInterrupt:
                pass
            return
        
        console.print(f"[cyan]{i18n.t('library.total_anime')}:[/cyan] {len(library)}\n")
        
        choices = []
        for item in library:
            title = item["anime_title"]
            provider = item["provider_name"]
            year = f" ({item['year']})" if item.get("year") else ""
            
            choices.append(questionary.Choice(
                title=f"{title}{year} - [{provider}]",
                value=item
            ))
        
        try:
            selected = questionary.select(
                i18n.t("library.select_anime"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected is None:
                return
            
            open_virtual_anime(selected)
            
        except KeyboardInterrupt:
            return

def show_local_library():
    from weeb_cli.commands.downloads import show_anime_episodes
    
    while True:
        console.clear()
        show_header(i18n.t("library.local_library"))
        
        indexed = local_library.get_indexed_anime()
        
        if not indexed:
            console.print(f"[dim]{i18n.t('library.local_empty')}[/dim]")
            try:
                input(i18n.t("common.continue_key"))
            except KeyboardInterrupt:
                pass
            return
        
        console.print(f"[cyan]{i18n.t('library.total_anime')}:[/cyan] {len(indexed)}\n")
        
        choices = []
        for item in indexed:
            title = item["title"]
            source = item["source_name"]
            ep_count = item["episode_count"]
            available = Path(item["folder_path"]).exists()
            
            status = "✓" if available else "✗"
            
            choices.append(questionary.Choice(
                title=f"{status} {title} - {ep_count} {i18n.t('downloads.episode_short')} [{source}]",
                value=item
            ))
        
        try:
            selected = questionary.select(
                i18n.t("library.select_anime"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected is None:
                return
            
            anime_path = selected["folder_path"]
            if not Path(anime_path).exists():
                console.print(f"[red]{i18n.t('library.local_not_available')}[/red]")
                try:
                    input(i18n.t("common.continue_key"))
                except KeyboardInterrupt:
                    pass
                continue
            
            anime_info = {
                "title": selected["title"],
                "path": anime_path,
                "episodes": local_library._scan_anime_folder(Path(anime_path)),
                "episode_count": selected["episode_count"],
                "source": selected["source_name"]
            }
            show_anime_episodes(anime_info)
            
        except KeyboardInterrupt:
            return

def open_virtual_anime(item):
    from weeb_cli.commands.search.anime_details import show_anime_details
    from weeb_cli.providers.registry import get_provider
    
    anime_id = item["anime_id"]
    provider_name = item["provider_name"]
    current_provider = config.get("scraping_source", "")
    
    if current_provider != provider_name:
        console.print(f"[yellow]{i18n.t('library.switching_provider', provider=provider_name)}[/yellow]")
        config.set("scraping_source", provider_name)
    
    provider = get_provider(provider_name)
    if not provider:
        console.print(f"[red]{i18n.t('library.provider_not_found', provider=provider_name)}[/red]")
        try:
            input(i18n.t("common.continue_key"))
        except KeyboardInterrupt:
            pass
        return
    
    anime_data = {
        "id": anime_id,
        "slug": anime_id,
        "title": item["anime_title"],
        "name": item["anime_title"],
        "cover": item.get("cover_url"),
        "type": item.get("anime_type"),
        "year": item.get("year")
    }
    
    show_anime_details(anime_data)
