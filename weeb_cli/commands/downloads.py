import questionary
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.table import Table
from weeb_cli.services.downloader import queue_manager
from weeb_cli.services.local_library import local_library
from weeb_cli.services.player import player
from weeb_cli.services.progress import progress_tracker
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
import time

console = Console()

AUTOCOMPLETE_STYLE = questionary.Style([
    ('qmark', 'fg:cyan'),
    ('question', 'fg:white bold'),
    ('answer', 'fg:cyan bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:white bg:ansiblack bold'),
    ('selected', 'fg:white'),
])

def show_downloads():
    local_library.smart_index_all()
    
    while True:
        console.clear()
        show_header(i18n.get("downloads.title"))
        
        sources = local_library.get_all_sources()
        active_queue = [i for i in queue_manager.queue if i["status"] in ["pending", "processing"]]
        
        choices = []
        
        indexed_count = len(local_library.get_indexed_anime())
        if indexed_count > 0:
            choices.append(questionary.Choice(
                f"⌕ {i18n.get('downloads.search_all')} ({indexed_count} anime)",
                value={"type": "search_all"}
            ))
        
        for source in sources:
            if source["available"]:
                library = local_library.scan_library(source["path"])
                count = len(library)
                if count > 0:
                    choices.append(questionary.Choice(
                        f"● {source['name']} ({count} anime)",
                        value={"type": "source", "data": source}
                    ))
            else:
                indexed = [a for a in local_library.get_indexed_anime() if a["source_path"] == source["path"]]
                count = len(indexed)
                if count > 0:
                    choices.append(questionary.Choice(
                        f"○ {source['name']} ({count} anime) - {i18n.get('downloads.offline')}",
                        value={"type": "offline", "data": source}
                    ))
        
        if active_queue:
            is_running = queue_manager.is_running()
            status = i18n.get("downloads.queue_running") if is_running else i18n.get("downloads.queue_stopped")
            choices.append(questionary.Choice(
                f"{i18n.get('downloads.active_downloads')} ({len(active_queue)}) - {status}",
                value={"type": "active"}
            ))
        
        if queue_manager.queue:
            choices.append(questionary.Choice(
                i18n.get("downloads.manage_queue"),
                value={"type": "manage"}
            ))
        
        if not choices:
            console.print(f"[dim]{i18n.get('downloads.empty')}[/dim]")
            try:
                input(i18n.get("common.continue_key"))
            except KeyboardInterrupt:
                pass
            return
        
        try:
            action = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if action is None:
                return
            
            if action["type"] == "search_all":
                search_all_sources()
            elif action["type"] == "source":
                library = local_library.scan_library(action["data"]["path"])
                show_completed_library(library, action["data"]["name"])
            elif action["type"] == "offline":
                show_offline_library(action["data"])
            elif action["type"] == "active":
                show_queue_live()
            elif action["type"] == "manage":
                manage_queue()
                
        except KeyboardInterrupt:
            return

def fuzzy_match(query: str, text: str) -> float:
    from difflib import SequenceMatcher
    query = query.lower()
    text = text.lower()
    
    if query == text:
        return 1.0
    if query in text:
        return 0.9
    
    return SequenceMatcher(None, query, text).ratio()

def search_all_sources():
    while True:
        console.clear()
        show_header(i18n.get("downloads.search_all"))
        
        all_indexed = local_library.get_indexed_anime()
        
        anime_map = {}
        for anime in all_indexed:
            progress = local_library.get_anime_progress(anime["title"])
            watched = len(progress.get("completed", []))
            total = anime["episode_count"]
            available = local_library.is_source_available(anime["source_path"])
            
            status_icon = "●" if available else "○"
            
            if watched >= total and total > 0:
                watch_status = " [✓]"
            elif watched > 0:
                watch_status = f" [{watched}/{total}]"
            else:
                watch_status = ""
            
            label = f"{status_icon} {anime['title']} [{anime['source_name']}]{watch_status}"
            anime_map[label] = anime
        
        all_choices = list(anime_map.keys())
        
        if not all_choices:
            console.print(f"[dim]{i18n.get('downloads.no_indexed')}[/dim]")
            time.sleep(1.5)
            return
        
        try:
            selected_label = questionary.autocomplete(
                i18n.get("downloads.search_anime"),
                choices=all_choices,
                match_middle=True,
                style=AUTOCOMPLETE_STYLE,
            ).ask()
            
            if selected_label is None:
                return
            
            if selected_label in anime_map:
                anime_info = anime_map[selected_label]
                
                if not local_library.is_source_available(anime_info["source_path"]):
                    console.print(f"[yellow]{i18n.t('downloads.connect_drive', name=anime_info['source_name'])}[/yellow]")
                    time.sleep(1.5)
                    continue
                
                anime_data = {
                    "title": anime_info["title"],
                    "path": anime_info["folder_path"],
                    "episode_count": anime_info["episode_count"],
                    "episodes": local_library._scan_anime_folder(Path(anime_info["folder_path"]))
                }
                show_anime_episodes(anime_data)
            
        except KeyboardInterrupt:
            return

def show_offline_library(source):
    while True:
        console.clear()
        show_header(f"{source['name']} ({i18n.get('downloads.offline')})")
        
        indexed = [a for a in local_library.get_indexed_anime() if a["source_path"] == source["path"]]
        
        if not indexed:
            console.print(f"[dim]{i18n.get('downloads.no_indexed')}[/dim]")
            time.sleep(1.5)
            return
        
        ep_short = i18n.get("downloads.episode_short")
        anime_map = {}
        for anime in indexed:
            progress = local_library.get_anime_progress(anime["title"])
            watched = len(progress.get("completed", []))
            total = anime["episode_count"]
            
            if watched >= total and total > 0:
                status = " [✓]"
            elif watched > 0:
                status = f" [{watched}/{total}]"
            else:
                status = ""
            
            label = f"{anime['title']} [{total} {ep_short}]{status}"
            anime_map[label] = anime
        
        all_choices = list(anime_map.keys())
        
        choices = [
            questionary.Choice(f"⌕ {i18n.get('downloads.search_anime')}", value="search"),
        ]
        for label in all_choices:
            choices.append(questionary.Choice(label, value=label))
        
        try:
            selected = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
            ).ask()
            
            if selected is None:
                return
            
            if selected == "search":
                search_result = questionary.autocomplete(
                    i18n.get("downloads.search_anime"),
                    choices=all_choices,
                    match_middle=True,
                    style=AUTOCOMPLETE_STYLE,
                ).ask()
                
                if search_result and search_result in anime_map:
                    anime_info = anime_map[search_result]
                    if not local_library.is_source_available(anime_info["source_path"]):
                        console.print(f"[yellow]{i18n.t('downloads.connect_drive', name=source['name'])}[/yellow]")
                        console.print(f"[dim]{i18n.get('downloads.drive_not_connected')}[/dim]")
                        time.sleep(2)
                    else:
                        anime_data = {
                            "title": anime_info["title"],
                            "path": anime_info["folder_path"],
                            "episode_count": anime_info["episode_count"],
                            "episodes": local_library._scan_anime_folder(Path(anime_info["folder_path"]))
                        }
                        show_anime_episodes(anime_data)
            elif selected in anime_map:
                anime_info = anime_map[selected]
                if not local_library.is_source_available(anime_info["source_path"]):
                    console.print(f"[yellow]{i18n.t('downloads.connect_drive', name=source['name'])}[/yellow]")
                    console.print(f"[dim]{i18n.get('downloads.drive_not_connected')}[/dim]")
                    time.sleep(2)
                else:
                    anime_data = {
                        "title": anime_info["title"],
                        "path": anime_info["folder_path"],
                        "episode_count": anime_info["episode_count"],
                        "episodes": local_library._scan_anime_folder(Path(anime_info["folder_path"]))
                    }
                    show_anime_episodes(anime_data)
            
        except KeyboardInterrupt:
            return

def show_completed_library(library, source_name=None):
    while True:
        console.clear()
        title = source_name or i18n.get("downloads.completed_downloads")
        show_header(title)
        
        ep_short = i18n.get("downloads.episode_short")
        anime_map = {}
        for anime in library:
            progress = local_library.get_anime_progress(anime["title"])
            watched = len(progress.get("completed", []))
            total = anime["episode_count"]
            
            if watched >= total and total > 0:
                status = " [✓]"
            elif watched > 0:
                status = f" [{watched}/{total}]"
            else:
                status = ""
            
            label = f"{anime['title']} [{total} {ep_short}]{status}"
            anime_map[label] = anime
        
        all_choices = list(anime_map.keys())
        
        choices = [
            questionary.Choice(f"⌕ {i18n.get('downloads.search_anime')}", value="search"),
        ]
        for label in all_choices:
            choices.append(questionary.Choice(label, value=label))
        
        try:
            selected = questionary.select(
                i18n.get("downloads.action_prompt"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
            ).ask()
            
            if selected is None:
                return
            
            if selected == "search":
                search_result = questionary.autocomplete(
                    i18n.get("downloads.search_anime"),
                    choices=all_choices,
                    match_middle=True,
                    style=AUTOCOMPLETE_STYLE,
                ).ask()
                
                if search_result and search_result in anime_map:
                    show_anime_episodes(anime_map[search_result])
            elif selected in anime_map:
                show_anime_episodes(anime_map[selected])
            
        except KeyboardInterrupt:
            return

def show_anime_episodes(anime):
    while True:
        console.clear()
        show_header(anime["title"])
        
        progress = local_library.get_anime_progress(anime["title"])
        completed_eps = set(progress.get("completed", []))
        last_watched = progress.get("last_watched", 0)
        next_ep = last_watched + 1
        
        episodes = anime["episodes"]
        
        choices = []
        for ep in episodes:
            num = ep["number"]
            size = local_library.format_size(ep["size"])
            
            prefix = "   "
            if num in completed_eps:
                prefix = "✓  "
            elif num == next_ep:
                prefix = "●  "
            
            choices.append(questionary.Choice(
                f"{prefix}{i18n.get('details.episode')} {num} ({size})",
                value=ep
            ))
        
        try:
            selected = questionary.select(
                i18n.get("details.select_episode"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected is None:
                return
            
            play_local_episode(anime, selected)
            
        except KeyboardInterrupt:
            return

def play_local_episode(anime, episode):
    console.print(f"[green]{i18n.get('details.player_starting')}[/green]")
    
    title = f"{anime['title']} - {i18n.get('details.episode')} {episode['number']}"
    anime_title = anime['title']
    episode_number = episode['number']
    total_episodes = anime.get('episode_count')
    
    success = player.play(
        episode["path"], 
        title=title,
        anime_title=anime_title,
        episode_number=episode_number,
        total_episodes=total_episodes
    )
    
    if success:
        try:
            ans = questionary.confirm(i18n.get("details.mark_watched")).ask()
            if ans:
                local_library.mark_episode_watched(
                    anime["title"],
                    episode["number"],
                    anime["episode_count"]
                )
                console.print(f"[green]✓ {i18n.get('details.marked_watched', 'İzlendi olarak işaretlendi')}[/green]")
                
                from weeb_cli.services.tracker import anilist_tracker, mal_tracker
                
                trackers_connected = []
                if anilist_tracker.is_authenticated():
                    trackers_connected.append(("AniList", anilist_tracker))
                if mal_tracker.is_authenticated():
                    trackers_connected.append(("MAL", mal_tracker))
                
                if trackers_connected:
                    tracker_names = ", ".join([t[0] for t in trackers_connected])
                    sync_ans = questionary.confirm(
                        i18n.get("details.sync_to_trackers", f"{tracker_names}'e de eklensin mi?")
                    ).ask()
                    
                    if sync_ans:
                        for name, tracker in trackers_connected:
                            result = tracker.update_progress(
                                anime["title"],
                                episode["number"],
                                anime["episode_count"]
                            )
                            if result:
                                console.print(f"[green]✓ {name} güncellendi[/green]")
                            else:
                                console.print(f"[yellow]⏳ {name}: Bekleyenlere eklendi[/yellow]")
                else:
                    anilist_tracker.update_progress(
                        anime["title"],
                        episode["number"],
                        anime["episode_count"]
                    )
                    mal_tracker.update_progress(
                        anime["title"],
                        episode["number"],
                        anime["episode_count"]
                    )
                
        except KeyboardInterrupt:
            pass
        except Exception as e:
            console.print(f"[dim]Tracker hatası: {e}[/dim]")

def manage_queue():
    while True:
        console.clear()
        show_header(i18n.get("downloads.manage_queue"))
        
        pending = queue_manager.get_pending_count()
        is_running = queue_manager.is_running()
        
        if pending > 0:
            status = i18n.get("downloads.queue_running") if is_running else i18n.get("downloads.queue_stopped")
            console.print(f"[cyan]{i18n.t('downloads.pending_count', count=pending)}[/cyan] - {status}\n")
        
        opt_view = i18n.get("downloads.view_queue")
        opt_start = i18n.get("downloads.start_queue")
        opt_stop = i18n.get("downloads.stop_queue")
        opt_clear = i18n.get("downloads.clear_completed")
        
        choices = [opt_view]
        if pending > 0:
            if is_running:
                choices.append(opt_stop)
            else:
                choices.append(opt_start)
        choices.append(opt_clear)
        
        try:
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
            elif action == opt_clear:
                queue_manager.clear_completed()
                console.print(f"[green]{i18n.get('downloads.cleared')}[/green]")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            return

def show_queue_live():
    def generate_table():
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column(i18n.get("watchlist.anime_title"), width=28)
        table.add_column(i18n.get("details.episode"), justify="right", width=4)
        table.add_column(i18n.get("downloads.status"), width=12)
        table.add_column(i18n.get("downloads.progress"), width=24)
        table.add_column("Hız", width=10)
        table.add_column("ETA", width=8)
        
        active = [i for i in queue_manager.queue if i["status"] == "processing"]
        pending = [i for i in queue_manager.queue if i["status"] == "pending"]
        finished = [i for i in queue_manager.queue if i["status"] in ["completed", "failed"]]
        finished = finished[-10:]
        
        display_list = active + pending + finished

        for item in display_list:
            status = item["status"]
            style = "white"
            if status == "processing":
                style = "cyan"
            elif status == "completed":
                style = "green"
            elif status == "failed":
                style = "red"
            elif status == "pending":
                style = "dim"
                
            progress = item.get("progress", 0)
            bars = int(progress / 5)
            bar_str = "█" * bars + "░" * (20 - bars)
            
            status_text = i18n.get(f"downloads.status_{status}", status.upper())
            p_text = f"{progress}%" if status == "processing" else ""
            speed = item.get("speed", "") if status == "processing" else ""
            eta = item.get("eta", "") if status == "processing" else ""
            
            table.add_row(
                f"[{style}]{item['anime_title'][:26]}[/{style}]",
                f"{item['episode_number']}",
                f"[{style}]{status_text}[/{style}]",
                f"[{style}]{bar_str} {p_text}[/{style}]",
                f"[{style}]{speed}[/{style}]",
                f"[{style}]{eta}[/{style}]"
            )
            
        return table

    try:
        with Live(generate_table(), refresh_per_second=1) as live:
            while True:
                live.update(generate_table())
                time.sleep(1)
    except KeyboardInterrupt:
        return
