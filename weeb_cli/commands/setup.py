from rich.console import Console
from rich.panel import Panel
from ..services.dependency_manager import dependency_manager
from ..i18n import i18n

console = Console()

def start_setup_wizard(force=False):
    tools = ["yt-dlp", "ffmpeg", "aria2", "mpv"]
    
    with console.status(f"[cyan]{i18n.t('setup.checking_deps')}[/cyan]", spinner="dots") as status:
        for tool in tools:
            status.update(f"[cyan]{i18n.t('setup.checking_tool', tool=tool)}[/cyan]")
            
            path = dependency_manager.check_dependency(tool)
            if path and not force:
                console.print(f"[green]✓[/green] {tool}: {i18n.t('setup.found_short')}")
                continue
                
            console.print(f"[yellow]⚠[/yellow] {tool}: {i18n.t('setup.not_found_short')}")
            status.update(f"[cyan]{i18n.t('setup.installing_tool', tool=tool)}[/cyan]")
            
            if dependency_manager.install_dependency(tool):
                console.print(f"[green]✓[/green] {tool}: {i18n.t('setup.installed')}")
            else:
                console.print(f"[red]✗[/red] {tool}: {i18n.t('setup.failed_short')}")
    
    console.print(f"\n[bold green]{i18n.t('setup.complete')}[/bold green]")
    console.print(f"[dim]{i18n.t('setup.location', path=dependency_manager.bin_dir)}[/dim]")
