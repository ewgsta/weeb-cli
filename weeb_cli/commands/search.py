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
        console.print("[red]Error: Invalid anime ID/Slug.[/red]")
        time.sleep(1)
        return

    console.clear()
    title = details.get("title") or anime.get("title")
    show_header(anime.get("title") or anime.get("name"))
    
    with console.status(i18n.get("common.processing"), spinner="dots"):
        details = get_details(slug)
    
    if not details:
        console.print("[red]Details not found.[/red]")
        time.sleep(1)
        return
    
    desc = details.get("description") or details.get("synopsis")
    if desc:
        console.print(f"\n[dim]{desc[:300]}...[/dim]\n", justify="center")

    episodes = details.get("episodes", [])
    if not episodes:
        console.print("[yellow]No episodes available.[/yellow]")
        input(i18n.get("common.continue_key"))
        return

    ep_choices = []
    for ep in episodes:
        name = f"Episode {ep.get('number', '?')}"
        ep_choices.append(questionary.Choice(name, value=ep))

    selected_ep = questionary.select(
        "Select Episode:",
        choices=ep_choices,
        pointer=">",
        use_shortcuts=False
    ).ask()
    
    if selected_ep:
        console.print(f"[green]Selected: {selected_ep}[/green]")
        input(i18n.get("common.continue_key"))
