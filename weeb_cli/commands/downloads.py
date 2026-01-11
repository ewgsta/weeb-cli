from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import ProgressBar, BarColumn
from weeb_cli.services.downloader import queue_manager
from weeb_cli.i18n import i18n
import time

console = Console()

def show_downloads():
    console.clear()
    console.print(f"[bold cyan]{i18n.get('details.download')}[/bold cyan] ([dim]Ctrl+C to exit[/dim])\n")
    
    def generate_table():
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Anime", width=30)
        table.add_column("Ep", justify="right", width=5)
        table.add_column("Status", width=15)
        table.add_column("Progress", width=20)
        table.add_column("ETA", width=10)
        
        queue = queue_manager.queue
        
        active = [i for i in queue if i["status"] == "processing"]
        pending = [i for i in queue if i["status"] == "pending"]
        finished = [i for i in queue if i["status"] in ["completed", "failed"]]
        finished = finished[-5:] 
        
        display_list = active + pending + finished
        
        if not display_list:
            table.add_row("-", "-", "Empty", "-", "-")
            return table

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
            
            p_text = f"{progress}%" if status == "processing" else ""
            
            table.add_row(
                f"[{style}]{item['anime_title'][:28]}[/{style}]",
                f"{item['episode_number']}",
                f"[{style}]{status.upper()}[/{style}]",
                f"[{style}]{bar_str} {p_text}[/{style}]",
                f"{item.get('eta', '-')}"
            )
            
        return table

    try:
        with Live(generate_table(), refresh_per_second=1) as live:
            while True:
                live.update(generate_table())
                time.sleep(1)
    except KeyboardInterrupt:
        return
