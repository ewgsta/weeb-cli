import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.search import search
from weeb_cli.services.progress import progress_tracker
from weeb_cli.services.cache import get_cache
from .episode_utils import normalize_search_results
from .anime_details import show_anime_details

console = Console()

SEARCH_STYLE = questionary.Style([
    ('qmark', 'fg:cyan bold'),
    ('question', 'fg:white'),
    ('answer', 'fg:cyan bold'),
])

SELECT_STYLE = questionary.Style([
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan'),
    ('selected', 'fg:cyan bold'),
])

def search_anime():
    while True:
        console.clear()
        show_header(i18n.t("menu.options.search"), show_source=True)
        
        _show_search_history()
        
        try:
            query = _get_search_query()
            if query is None:
                return
            
            if not query.strip():
                continue

            progress_tracker.add_search_history(query.strip())
            
            results = _fetch_search_results(query.strip())
            if results is None:
                time.sleep(1)
                continue

            selected = _select_anime_from_results(results)
            if selected is None:
                continue
            
            show_anime_details(selected)
            
        except KeyboardInterrupt:
            return

def _show_search_history():
    history = progress_tracker.get_search_history()
    if history:
        console.print(f"[dim]{i18n.t('search.recent')}: {', '.join(history[:5])}[/dim]\n", justify="left")

def _get_search_query():
    return questionary.text(
        i18n.t("search.prompt") + ":",
        qmark=">",
        style=SEARCH_STYLE
    ).ask()

def _fetch_search_results(query):
    cache = get_cache()
    cache_key = f"search:{query}"
    data = cache.get(cache_key, max_age=1800)
    
    if data is None:
        with console.status(i18n.t("search.searching"), spinner="dots"):
            data = search(query)
            if data:
                cache.set(cache_key, data)
    
    if data is None:
        return None

    data = normalize_search_results(data)
    
    if not data or not isinstance(data, list):
        console.print(f"[red]{i18n.t('search.no_results')}[/red]")
        time.sleep(1.5)
        return None
    
    return data

def _select_anime_from_results(results):
    choices = []
    for item in results:
        title = item.get("title") or item.get("name")
        if title:
            choices.append(questionary.Choice(title, value=item))
    
    if not choices:
        console.print(f"[red]{i18n.t('search.no_results')}[/red]")
        time.sleep(1.5)
        return None

    selected = questionary.select(
        i18n.t("search.results"),
        choices=choices,
        pointer=">",
        use_shortcuts=False,
        style=SELECT_STYLE
    ).ask()

    return selected if selected != "cancel" else None
