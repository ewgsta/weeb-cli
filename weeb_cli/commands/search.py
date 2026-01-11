import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.search import search
from weeb_cli.services.details import get_details
from weeb_cli.services.watch import get_streams
from weeb_cli.services.player import player
from weeb_cli.services.progress import progress_tracker
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

    while True:
        console.clear()
        show_header(anime.get("title") or anime.get("name") or "Anime")
        
        with console.status(i18n.get("common.processing"), spinner="dots"):
            details = get_details(slug)
        
        if isinstance(details, dict):
            if "data" in details and isinstance(details["data"], dict):
                details = details["data"]
            
            if "details" in details and isinstance(details["details"], dict):
                details = details["details"]

        if not details:
            console.print(f"[red]{i18n.get('details.not_found')}[/red]")
            time.sleep(1)
            return
        
        desc = details.get("description") or details.get("synopsis") or details.get("desc")
        if desc:
            console.print(f"\n[dim]{desc[:300]}...[/dim]\n", justify="left")

        opt_watch = i18n.get("details.watch")
        opt_dl = i18n.get("details.download")
        
        try:
            action = questionary.select(
                i18n.get("details.action_prompt"),
                choices=[opt_watch, opt_dl],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if action is None:
                return
            
            if action == opt_dl:
                handle_download_flow(slug, details)
            elif action == opt_watch:
                handle_watch_flow(slug, details)
                
        except KeyboardInterrupt:
            return

def get_episodes_safe(details):
    episodes = None
    for k in ["episodes", "episodes_list", "episode_list", "results", "chapters"]:
        if k in details and isinstance(details[k], list):
            episodes = details[k]
            break
            
    if not episodes:
        for v in details.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and ("number" in v[0] or "ep_num" in v[0] or "url" in v[0]):
                episodes = v
                break
    return episodes

def handle_watch_flow(slug, details):
    episodes = get_episodes_safe(details)
    if not episodes:
        console.print(f"[yellow]{i18n.get('details.no_episodes')}[/yellow]")
        time.sleep(1.5)
        return

    prog_data = progress_tracker.get_anime_progress(slug)
    completed_ids = set(prog_data.get("completed", []))
    last_watched = prog_data.get("last_watched", 0)
    next_ep_num = last_watched + 1

    while True:
        ep_choices = []
        for ep in episodes:
            num_val = ep.get('number') or ep.get('ep_num')
            try:
                num = int(num_val)
            except:
                num = -1
            
            prefix = "   "
            if num in completed_ids:
                prefix = "✓  "
            elif num == next_ep_num:
                prefix = "●  "
            
            name = f"{prefix}{i18n.get('details.episode')} {num_val}"
            ep_choices.append(questionary.Choice(name, value=ep))

        try:
            selected_ep = questionary.select(
                i18n.get("details.select_episode") + ":",
                choices=ep_choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected_ep is None:
                return

            ep_id = selected_ep.get("id")
            ep_num = selected_ep.get("number")
            
            if not ep_id:
                console.print(f"[red]{i18n.get('details.invalid_ep_id')}[/red]")
                time.sleep(1)
                continue

            with console.status(i18n.get("common.processing"), spinner="dots"):
                stream_resp = get_streams(slug, ep_id)
            stream_url = None
            if stream_resp and isinstance(stream_resp, dict):
                 data_node = stream_resp
                 for _ in range(3):
                     if "data" in data_node and isinstance(data_node["data"], (dict, list)):
                         data_node = data_node["data"]
                     else:
                         break
                 
                 sources = None
                 if isinstance(data_node, list):
                     sources = data_node
                 elif isinstance(data_node, dict):
                     sources = data_node.get("links") or data_node.get("sources")
                 
                 if sources and isinstance(sources, list):
                     first = sources[0]
                     if isinstance(first, dict):
                        stream_url = first.get("url")
                 elif isinstance(data_node, dict) and "url" in data_node:
                     stream_url = data_node["url"]
            
            if not stream_url:
                console.print(f"[red]{i18n.get('details.stream_not_found')}[/red]")
                time.sleep(1.5)
                continue
            
            console.print(f"[green]{i18n.get('details.player_starting')}[/green]")
            title = f"{details.get('title', 'Anime')} - Ep {ep_num}"
            
            success = player.play(stream_url, title=title)
            
            if success:
                try:
                    ans = questionary.confirm(i18n.get("details.mark_watched")).ask()
                    if ans:
                        n = int(ep_num)
                        progress_tracker.mark_watched(slug, n)
                        
                        completed_ids.add(n)
                        if n >= next_ep_num:
                            next_ep_num = n + 1
                except:
                    pass
            
        except KeyboardInterrupt:
            return

def handle_download_flow(slug, details):
    episodes = get_episodes_safe(details)
    if not episodes:
        console.print(f"[yellow]{i18n.get('details.no_episodes')}[/yellow]")
        time.sleep(1.5)
        return

    opt_all = i18n.get("details.download_options.all")
    opt_manual = i18n.get("details.download_options.manual")
    opt_range = i18n.get("details.download_options.range")

    try:
        mode = questionary.select(
            i18n.get("details.download_options.prompt"),
            choices=[opt_all, opt_manual, opt_range],
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if mode is None:
            return
            
        selected_eps = []
        
        if mode == opt_all:
            selected_eps = episodes
            
        elif mode == opt_manual:
             choices = []
             for ep in episodes:
                 name = f"{i18n.get('details.episode')} {ep.get('number')}"
                 choices.append(questionary.Choice(name, value=ep))
                 
             selected_eps = questionary.checkbox(
                 "Select Episodes:",
                 choices=choices
             ).ask()
             
        elif mode == opt_range:
             r_str = questionary.text(i18n.get("details.download_options.range_input")).ask()
             if not r_str: return
             nums = set()
             try:
                 parts = r_str.split(',')
                 for p in parts:
                     p = p.strip()
                     if '-' in p:
                         s, e = p.split('-')
                         for x in range(int(s), int(e)+1): nums.add(x)
                     elif p.isdigit():
                         nums.add(int(p))
             except:
                 console.print(f"[red]{i18n.get('details.download_options.range_error')}[/red]")
                 time.sleep(1)
                 return
             
             selected_eps = [ep for ep in episodes if int(ep.get('number', -1)) in nums]

        if not selected_eps:
             return
             
        console.print(f"[green]{i18n.get('details.download_options.started')}[/green]")
        console.print(f"[dim]{i18n.t('details.queueing', count=len(selected_eps))}[/dim]")
        input(i18n.get("common.continue_key"))
        
    except KeyboardInterrupt:
        return
