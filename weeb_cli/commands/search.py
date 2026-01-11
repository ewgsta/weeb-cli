import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.search import search
import time

console = Console()

def search_anime():
    while True:
        console.clear()
        show_header(i18n.get("menu.options.search"), show_source=True)
        
        try:
            query = questionary.text(
                i18n.get("search.prompt") + ":",
                qmark=">",
                style=questionary.Style([
                    ('qmark', 'fg:cyan bold'),
                    ('question', 'fg:white'),
                    ('answer', 'fg:cyan bold'), 
                ])
            ).ask()
            
            if query is None: 
                return
            
            if not query.strip():
                continue

            with console.status(i18n.get("search.searching"), spinner="dots"):
                data = search(query)
            
            if data is None:
                time.sleep(1)
                continue

            if isinstance(data, dict):
                if "results" in data and isinstance(data["results"], list):
                    data = data["results"]
                elif "data" in data:
                    inner = data["data"]
                    if isinstance(inner, list):
                        data = inner
                    elif isinstance(inner, dict):
                        if "results" in inner and isinstance(inner["results"], list):
                            data = inner["results"]
                        elif "animes" in inner and isinstance(inner["animes"], list):
                            data = inner["animes"]
                        elif "items" in inner and isinstance(inner["items"], list):
                            data = inner["items"]
            
            if not data or not isinstance(data, list):
                console.print(f"[red]{i18n.get('search.no_results')}[/red]")
                time.sleep(1.5)
                continue

            choices = []
            for item in data:
                 title = item.get("title") or item.get("name")
                 if title:
                     choices.append(questionary.Choice(title, value=item))
            
            if not choices:
                console.print(f"[red]{i18n.get('search.no_results')}[/red]")
                time.sleep(1.5)
                continue



            selected = questionary.select(
                i18n.get("search.results"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
                style=questionary.Style([
                    ('pointer', 'fg:cyan bold'),
                    ('highlighted', 'fg:cyan'),
                    ('selected', 'fg:cyan bold'),
                ])
            ).ask()

            if selected == "cancel" or selected is None:
                continue
            
            show_anime_details(selected)
            
        except KeyboardInterrupt:
            return

from weeb_cli.services.details import get_details

def show_anime_details(anime):
    slug = anime.get("slug") or anime.get("id")
    if not slug:
        console.print(f"[red]{i18n.get('details.error_slug')}[/red]")
        time.sleep(1)
        return

    console.clear()
    show_header(anime.get("title") or anime.get("name"))
    with console.status(i18n.get("common.processing"), spinner="dots"):
        details = get_details(slug)
    
    if isinstance(details, dict) and "data" in details:
        if isinstance(details["data"], dict):
            details = details["data"]
        elif isinstance(details["data"], list):
            details = { "episodes": details["data"] }

    if not details:
        console.print(f"[red]{i18n.get('details.not_found')}[/red]")
        time.sleep(1)
        return

    title = details.get("title") or anime.get("title")
    desc = details.get("description") or details.get("synopsis") or details.get("desc")
    if desc:
        console.print(f"\n[dim]{desc[:300]}...[/dim]\n", justify="center")

    episodes = details.get("episodes") or details.get("episodes_list") or details.get("results") or []
    if not episodes:
        console.print(f"[yellow]{i18n.get('details.no_episodes')}[/yellow]")
        input(i18n.get("common.continue_key"))
        return

    ep_choices = []
    for ep in episodes:
        num = ep.get('number') or ep.get('ep_num') or '?'
        name = f"{i18n.get('details.episode')} {num}"
        ep_choices.append(questionary.Choice(name, value=ep))

    try:
        selected_ep = questionary.select(
            i18n.get("details.select_episode") + ":",
            choices=ep_choices,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if selected_ep:
            ep_num = selected_ep.get('number') or selected_ep.get('ep_num')
            console.print(f"[green]{i18n.t('details.selected', episode=ep_num)}[/green]")
            input(i18n.get("common.continue_key"))
            
    except KeyboardInterrupt:
        return
