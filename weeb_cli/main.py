import typer
import questionary
import sys
import requests
from rich.console import Console
from weeb_cli.ui.menu import show_main_menu
from weeb_cli.commands.search import search_anime
from weeb_cli.commands.watchlist import open_watchlist
from weeb_cli.commands.settings import open_settings
from weeb_cli.config import config
from weeb_cli.i18n import i18n
from weeb_cli.commands.setup import start_setup_wizard

app = typer.Typer(add_completion=False)
console = Console()

def check_network():
    console.print(f"[dim]{i18n.t('common.ctrl_c_hint')}[/dim]")
    try:
        with console.status("", spinner="square"):
            try:
                requests.get("https://www.google.com", timeout=5)
            except:
                requests.get("https://1.1.1.1", timeout=5)
    except:
        console.print(f"[red]{i18n.t('common.network_error')}[/red]")
        sys.exit(1)

def run_setup():
    langs = {
        "Türkçe": "tr",
        "English": "en"
    }
    
    selected = questionary.select(
        "Select Language / Dil Seçiniz",
        choices=list(langs.keys()),
        use_indicator=True,
        pointer=">"
    ).ask()
    
    if selected:
        lang_code = langs[selected]
        i18n.set_language(lang_code)
        
        console.print(f"[dim]{i18n.t('common.ctrl_c_hint')}[/dim]")
        start_setup_wizard()

@app.command()
def start():
    if not config.get("language"):
        run_setup()

    check_network()

    actions = {
        "search": search_anime,
        "watchlist": open_watchlist,
        "settings": open_settings
    }
    show_main_menu(actions)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        start()

if __name__ == "__main__":
    app()
