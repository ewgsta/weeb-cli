import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.details import get_details
from weeb_cli.config import config
from .episode_utils import normalize_details
from .watch_flow import handle_watch_flow
from .download_flow import handle_download_flow

console = Console()

def show_anime_details(anime):
    from weeb_cli.services.local_library import local_library
    from weeb_cli.config import config as app_config
    
    slug = anime.get("slug") or anime.get("id")
    if not slug:
        console.print(f"[red]{i18n.t('details.error_slug')}[/red]")
        time.sleep(1)
        return

    while True:
        console.clear()
        show_header(anime.get("title") or anime.get("name") or "Anime")
        
        with console.status(i18n.t("common.processing"), spinner="dots"):
            details = get_details(slug)
        
        details = normalize_details(details)

        if not details:
            console.print(f"[red]{i18n.t('details.not_found')}[/red]")
            time.sleep(1)
            return
        
        _display_anime_info(details)
        
        try:
            provider_name = app_config.get("scraping_source", "")
            in_library = local_library.is_in_virtual_library(slug, provider_name)
            
            action = _get_user_action(in_library)
            if action is None:
                return
            
            if action == i18n.t("details.download"):
                handle_download_flow(slug, details)
            elif action == i18n.t("details.watch"):
                handle_watch_flow(slug, details)
            elif action == i18n.t("details.add_to_library"):
                anime_title = details.get("title", "")
                cover = anime.get("cover") or details.get("cover")
                anime_type = anime.get("type") or details.get("type")
                year = anime.get("year") or details.get("year")
                
                if local_library.add_to_virtual_library(slug, anime_title, provider_name, cover, anime_type, year):
                    console.print(f"[green]{i18n.t('details.added_to_library')}[/green]")
                else:
                    console.print(f"[yellow]{i18n.t('details.already_in_library')}[/yellow]")
                time.sleep(1)
            elif action == i18n.t("details.remove_from_library"):
                local_library.remove_from_virtual_library(slug, provider_name)
                console.print(f"[green]{i18n.t('details.removed_from_library')}[/green]")
                time.sleep(1)
                
        except KeyboardInterrupt:
            return

def _display_anime_info(details):
    console.clear()
    show_header(details.get("title", ""))
    
    desc = details.get("description") or details.get("synopsis") or details.get("desc")
    show_desc = config.get("show_description", True)
    
    if show_desc and desc:
        if len(desc) > 500:
            desc = desc[:497] + "..."
        console.print(f"\n[dim]{desc}[/dim]\n", justify="left")

def _get_user_action(in_library=False):
    opt_watch = i18n.t("details.watch")
    opt_dl = i18n.t("details.download")
    opt_add = i18n.t("details.add_to_library")
    opt_remove = i18n.t("details.remove_from_library")
    
    choices = [opt_watch, opt_dl]
    
    if in_library:
        choices.append(opt_remove)
    else:
        choices.append(opt_add)
    
    return questionary.select(
        i18n.t("details.action_prompt"),
        choices=choices,
        pointer=">",
        use_shortcuts=False
    ).ask()
