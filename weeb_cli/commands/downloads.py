import questionary
from rich.console import Console
from rich.live import Live
from rich.table import Table
from weeb_cli.services.downloader import queue_manager
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
import time

console = Console()

def show_downloads():
    while True:
        console.clear()
        show_header(i18n.get("downloads.title"))
        
        pending = queue_manager.get_pending_count()
        is_running = queue_manager.is_running()
        
        if pending > 0:
            status = i18n.get("downloads.queue_running") if is_running else i18n.get("downloads.queue_stopped")
            console.print(f"[cyan]{i18n.t('downloads.pending_count', count=pending)}[/cyan] - {status}\n")
        
        queue = queue_manager.queue
        
        if not queue:
            console.print(f"[dim]{i18n.get('downloads.empty')}[/dim]")
            try:
                input(i18n.get("common.continue_key"))
            except KeyboardInterrupt:
                pass
            return
        
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
