from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header

console = Console()

def show_watchlist():
    console.clear()
    show_header(i18n.get("menu.options.watchlist"))
    try:
        console.print(f"[yellow]{i18n.get('common.wip')}[/yellow]")
        input(i18n.get("common.continue_key"))
    except KeyboardInterrupt:
        pass
