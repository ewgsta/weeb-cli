import questionary
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

def show_downloads():
    while True:
        console.clear()
        show_header(i18n.get("downloads.title"))
        
        library = local_library.scan_library()
        active_queue = [i for i in queue_manager.queue if i["status"] in ["pending", "processing"]]
        
        opt_completed = i18n.get("downloads.completed_downloads")
        opt_active = i18n.get("downloads.active_downloads")
        opt_manage = i18n.get("downloads.manage_queue")
        
        choices = []
        
        if library:
            choices.append(questionary.Choice(
                f"{opt_completed} ({len(library)} anime)",
                value="completed"
            ))
        
        if active_queue:
            is_running = queue_manager.is_running()
            status = i18n.get("downloads.queue_running") if is_running else i18n.get("downloads.queue_stopped")
            choices.append(questionary.Choice(
                f"{opt_active} ({len(active_queue)}) - {status}",
                value="active"
            ))
        
        if queue_manager.queue:
            choices.append(questionary.Choice(opt_manage, value="manage"))
        
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
            
            if action == "completed":
                show_completed_library(library)
            elif action == "active":
                show_queue_live()
            elif action == "manage":
                manage_queue()
                
        except KeyboardInterrupt:
            return

def show_completed_library(library):
    while True:
        console.clear()
        show_header(i18n.get("downloads.completed_downloads"))
        
        choices = []
        for anime in library:
            progress = local_library.get_anime_progress(anime["title"])
            watched = len(progress.get("completed", []))
            total = anime["episode_count"]
            
            if watched >= total:
                status = "[green]✓[/green]"
            elif watched > 0:
                status = f"[cyan]{watched}/{total}[/cyan]"
            else:
                status = f"[dim]0/{total}[/dim]"
            
            choices.append(questionary.Choice(
                f"{anime['title']} [{total} {i18n.get('details.episode')}] {status}",
                value=anime
            ))
        
        try:
            selected = questionary.select(
                i18n.get("downloads.select_anime"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected is None:
                return
            
            show_anime_episodes(selected)
            
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
    success = player.play(episode["path"], title=title)
    
    if success:
        try:
            ans = questionary.confirm(i18n.get("details.mark_watched")).ask()
            if ans:
                local_library.mark_episode_watched(
                    anime["title"],
                    episode["number"],
                    anime["episode_count"]
                )
        except:
            pass

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
                queue_manager.queue = [i for i in queue_manager.queue if i["status"] in ["pending", "processing"]]
                queue_manager._save_queue()
                console.print(f"[green]{i18n.get('downloads.cleared')}[/green]")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            return

def show_queue_live():
    def generate_table():
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column(i18n.get("watchlist.anime_title"), width=30)
        table.add_column(i18n.get("details.episode"), justify="right", width=5)
        table.add_column(i18n.get("downloads.status"), width=15)
        table.add_column(i18n.get("downloads.progress"), width=20)
        
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
            
            table.add_row(
                f"[{style}]{item['anime_title'][:28]}[/{style}]",
                f"{item['episode_number']}",
                f"[{style}]{status_text}[/{style}]",
                f"[{style}]{bar_str} {p_text}[/{style}]"
            )
            
        return table

    try:
        with Live(generate_table(), refresh_per_second=1) as live:
            while True:
                live.update(generate_table())
                time.sleep(1)
    except KeyboardInterrupt:
        return
