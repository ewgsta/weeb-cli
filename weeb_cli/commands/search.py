import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.search import search
from weeb_cli.services.details import get_details
from weeb_cli.services.watch import get_streams
from weeb_cli.services.player import player
from weeb_cli.services.progress import progress_tracker
from weeb_cli.services.downloader import queue_manager
from weeb_cli.services.scraper import scraper
import time

console = Console()

PLAYER_PRIORITY = [
    "ALUCARD", "AMATERASU", "SIBNET", "MP4UPLOAD", "UQLOAD",
    "MAIL", "DAILYMOTION", "SENDVID", "ODNOKLASSNIKI", "VK",
    "VIDMOLY", "YOURUPLOAD", "MYVI", "GDRIVE", "PIXELDRAIN", "HDVID", "YADISK"
]

def _get_player_priority(server_name: str) -> int:
    server_upper = server_name.upper()
    for i, p in enumerate(PLAYER_PRIORITY):
        if p in server_upper:
            return i
    return 999

def _sort_streams(streams: list) -> list:
    return sorted(streams, key=lambda s: _get_player_priority(s.get("server", "")))

def search_anime():
    while True:
        console.clear()
        show_header(i18n.get("menu.options.search"), show_source=True)
        
        history = progress_tracker.get_search_history()
        if history:
            console.print(f"[dim]{i18n.get('search.recent')}: {', '.join(history[:5])}[/dim]\n", justify="left")
        
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

            progress_tracker.add_search_history(query.strip())

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
            
            source = details.get("source")
            
            if "details" in details and isinstance(details["details"], dict):
                details = details["details"]
                if source:
                    details["source"] = source

        if not details:
            console.print(f"[red]{i18n.get('details.not_found')}[/red]")
            time.sleep(1)
            return
        
        from weeb_cli.config import config
        desc = details.get("description") or details.get("synopsis") or details.get("desc")
        show_desc = config.get("show_description", True)

        opt_watch = i18n.get("details.watch")
        opt_dl = i18n.get("details.download")
        
        console.clear()
        show_header(details.get("title", ""))
        
        if show_desc and desc:
            console.print(f"\n[dim]{desc}[/dim]\n", justify="left")
        
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

def _group_episodes_by_season(episodes):
    seasons = {}
    for ep in episodes:
        season = ep.get('season', 1)
        if season not in seasons:
            seasons[season] = []
        seasons[season].append(ep)
    
    for season in seasons:
        seasons[season] = sorted(seasons[season], key=lambda x: int(x.get('number') or x.get('ep_num') or 0))
    
    return seasons

def _make_season_episode_id(season, ep_num):
    return season * 1000 + ep_num

def handle_watch_flow(slug, details):
    episodes = get_episodes_safe(details)
    if not episodes:
        console.print(f"[yellow]{i18n.get('details.no_episodes')}[/yellow]")
        time.sleep(1.5)
        return

    seasons = _group_episodes_by_season(episodes)
    season_numbers = sorted(seasons.keys())
    
    if len(season_numbers) <= 1:
        _handle_single_season_watch(slug, details, episodes, season=1)
        return
    
    prog_data = progress_tracker.get_anime_progress(slug)
    completed_ids = set(prog_data.get("completed", []))
    
    while True:
        console.clear()
        show_header(details.get("title", "Anime"))
        
        season_choices = []
        for s_num in season_numbers:
            s_episodes = seasons[s_num]
            total_in_season = len(s_episodes)
            
            watched_in_season = 0
            for ep in s_episodes:
                ep_num = int(ep.get('number') or ep.get('ep_num') or 0)
                ep_id = _make_season_episode_id(s_num, ep_num)
                if ep_id in completed_ids:
                    watched_in_season += 1
            
            if watched_in_season >= total_in_season:
                status = " [✓]"
            elif watched_in_season > 0:
                status = f" [{watched_in_season}/{total_in_season}]"
            else:
                status = f" [0/{total_in_season}]"
            
            label = f"{i18n.get('details.season', 'Sezon')} {s_num}{status}"
            season_choices.append(questionary.Choice(label, value=s_num))
        
        try:
            selected_season = questionary.select(
                i18n.get("details.select_season", "Sezon Seçin") + ":",
                choices=season_choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected_season is None:
                return
            
            _handle_single_season_watch(slug, details, seasons[selected_season], season=selected_season)
            
        except KeyboardInterrupt:
            return

def _handle_single_season_watch(slug, details, episodes, season=1):
    prog_data = progress_tracker.get_anime_progress(slug)
    completed_ids = set(prog_data.get("completed", []))
    
    last_watched_in_season = 0
    for ep_id in completed_ids:
        if ep_id >= season * 1000 and ep_id < (season + 1) * 1000:
            ep_num = ep_id % 1000
            if ep_num > last_watched_in_season:
                last_watched_in_season = ep_num
    
    if season == 1 and not any(cid >= 1000 for cid in completed_ids):
        last_watched_in_season = prog_data.get("last_watched", 0)
    
    next_ep_num = last_watched_in_season + 1

    while True:
        ep_choices = []
        for ep in episodes:
            num_val = ep.get('number') or ep.get('ep_num')
            try:
                num = int(num_val)
            except:
                num = -1
            
            ep_progress_id = _make_season_episode_id(season, num)
            
            prefix = "   "
            if ep_progress_id in completed_ids or (season == 1 and num in completed_ids):
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
            ep_num = selected_ep.get("number") or selected_ep.get("ep_num")
            
            if not ep_id:
                console.print(f"[red]{i18n.get('details.invalid_ep_id')}[/red]")
                time.sleep(1)
                continue

            with console.status(i18n.get("common.processing"), spinner="dots"):
                stream_resp = get_streams(slug, ep_id)
            
            streams_list = []
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
                    streams_list = sources
            
            if not streams_list:
                error_msg = i18n.get('details.stream_not_found')
                if scraper.last_error:
                    error_msg += f" [{scraper.last_error}]"
                console.print(f"[red]{error_msg}[/red]")
                time.sleep(1.5)
                continue
            
            streams_list = _sort_streams(streams_list)
            
            stream_choices = []
            for idx, s in enumerate(streams_list):
                server = s.get("server", "Unknown")
                quality = s.get("quality", "auto")
                label = f"{server} ({quality})"
                stream_choices.append(questionary.Choice(label, value=s))
            
            if len(streams_list) == 1:
                selected_stream = streams_list[0]
            else:
                selected_stream = questionary.select(
                    i18n.get("details.select_source"),
                    choices=stream_choices,
                    pointer=">",
                    use_shortcuts=False
                ).ask()
                
                if selected_stream is None:
                    continue
            
            stream_url = selected_stream.get("url")
            
            if not stream_url:
                console.print(f"[red]{i18n.get('details.stream_not_found')}[/red]")
                time.sleep(1.5)
                continue
            
            console.print(f"[green]{i18n.get('details.player_starting')}[/green]")
            title = f"{details.get('title', 'Anime')} - S{season}E{ep_num}"
            
            headers = {}
            if details.get("source") == "hianime":
                headers["Referer"] = "https://hianime.to"
            
            anime_title = details.get('title', 'Anime')
            episode_number = int(ep_num) if ep_num else None
            total_episodes = details.get("total_episodes") or len(episodes)
            
            success = player.play(
                stream_url, 
                title=title, 
                headers=headers,
                anime_title=anime_title,
                episode_number=episode_number,
                total_episodes=total_episodes
            )
            
            if success:
                try:
                    ans = questionary.confirm(i18n.get("details.mark_watched")).ask()
                    if ans:
                        n = int(ep_num)
                        total_eps = details.get("total_episodes") or len(episodes)
                        
                        season_ep_id = _make_season_episode_id(season, n)
                        progress_tracker.mark_watched(
                            slug, 
                            season_ep_id, 
                            title=details.get("title"),
                            total_episodes=total_eps
                        )
                        console.print(f"[green]✓ {i18n.get('details.marked_watched', 'İzlendi olarak işaretlendi')}[/green]")
                        
                        from weeb_cli.services.tracker import anilist_tracker, mal_tracker
                        
                        updated_prog = progress_tracker.get_anime_progress(slug)
                        total_watched = len(updated_prog.get("completed", []))
                        
                        for name, tracker in [("AniList", anilist_tracker), ("MAL", mal_tracker)]:
                            if tracker.is_authenticated():
                                result = tracker.update_progress(
                                    details.get("title"),
                                    total_watched,
                                    total_eps
                                )
                                if result:
                                    console.print(f"[green]✓ {name} güncellendi[/green]")
                                else:
                                    console.print(f"[yellow]⏳ {name}: Bekleyenlere eklendi[/yellow]")
                            else:
                                tracker.update_progress(
                                    details.get("title"),
                                    total_watched,
                                    total_eps
                                )
                        
                        completed_ids.add(season_ep_id)
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
        
        anime_title = details.get("title") or "Unknown Anime"
        
        opt_now = i18n.get("downloads.start_now")
        opt_queue = i18n.get("downloads.add_to_queue")
        
        action = questionary.select(
            i18n.get("downloads.action_prompt"),
            choices=[opt_now, opt_queue],
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if action is None:
            return
        
        added = queue_manager.add_to_queue(anime_title, selected_eps, slug)
        
        if added > 0:
            console.print(f"[green]{i18n.t('downloads.queued', count=added)}[/green]")
            
            if action == opt_now:
                queue_manager.start_queue()
        else:
            console.print(f"[yellow]{i18n.get('downloads.already_in_queue')}[/yellow]")
        
        time.sleep(1)
        
    except KeyboardInterrupt:
        return
