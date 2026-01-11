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

            choices.append(questionary.Choice(i18n.get("search.cancel"), value="cancel"))

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
            
            show_details_placeholder(selected)
            
        except KeyboardInterrupt:
            return

def show_details_placeholder(anime):
    console.print(f"[yellow]{i18n.get('common.wip')}: {anime.get('title') or 'Anime'}[/yellow]")
    input(i18n.get("common.continue_key"))
