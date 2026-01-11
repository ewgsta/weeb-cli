import requests
from packaging import version
from weeb_cli import __version__
from rich.console import Console
import webbrowser
import questionary
from weeb_cli.i18n import i18n
import sys

console = Console()

def check_for_updates():
    try:
        url = "https://api.github.com/repos/ewgsta/weeb-cli/releases/latest"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            latest_tag = data.get("tag_name", "").lstrip("v")
            html_url = data.get("html_url", "")
            
            if not latest_tag:
                return False, None, None
                
            current_ver = version.parse(__version__)
            latest_ver = version.parse(latest_tag)
            
            if latest_ver > current_ver:
                return True, latest_tag, html_url
                
    except Exception:
        pass
        
    return False, None, None

def update_prompt():
    is_available, latest_ver, url = check_for_updates()
    
    if is_available:
        console.clear()
        console.print(f"\n[green bold]{i18n.get('update.available')} (v{latest_ver})[/green bold]")
        console.print(f"[dim]{i18n.get('update.current')}: v{__version__}[/dim]\n")
        
        should_update = questionary.confirm(
            i18n.get("update.prompt"),
            default=True
        ).ask()
        
        if should_update:
            if url:
                console.print(f"[blue]{i18n.get('update.opening')}[/blue]")
                webbrowser.open(url)
                sys.exit(0)
            else:
                console.print(f"[red]{i18n.get('update.error')}[/red]")
