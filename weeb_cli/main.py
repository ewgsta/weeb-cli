import typer
import questionary
import sys
import time
from rich.console import Console
from weeb_cli.ui.menu import show_main_menu
from weeb_cli.commands.search import search_anime
from weeb_cli.commands.watchlist import show_watchlist
from weeb_cli.commands.settings import open_settings
from weeb_cli.config import config
from weeb_cli.i18n import i18n
from weeb_cli.commands.setup import start_setup_wizard
from weeb_cli.services.dependency_manager import dependency_manager
from weeb_cli.services.updater import update_prompt
from weeb_cli.ui.prompt import prompt
from weeb_cli.commands.api import api_app
from weeb_cli.commands.serve import serve_app

app = typer.Typer(add_completion=False)
app.add_typer(api_app, name="api")
app.add_typer(serve_app, name="serve")
console = Console()

def check_network():
    with console.status(f"[dim]{i18n.t('common.ctrl_c_hint')}[/dim]", spinner="dots"):
        time.sleep(1)

def run_setup():
    langs = {
        "Türkçe": "tr",
        "English": "en"
    }
    
    choices = [(k, v) for k, v in langs.items()]
    
    selected_code = prompt.select(
        "Select Language / Dil Seçiniz",
        choices
    )
    
    i18n.set_language(selected_code)
    
    console.print(f"[dim]{i18n.t('common.ctrl_c_hint')}[/dim]")
    start_setup_wizard()

def check_ffmpeg_silent():
    if not dependency_manager.check_dependency("ffmpeg"):
         console.print(f"[cyan]{i18n.t('setup.downloading', tool='FFmpeg')}...[/cyan]")
         dependency_manager.install_dependency("ffmpeg")

@app.command()
def start():
    if not config.get("language"):
        run_setup()

    update_prompt()
    check_incomplete_downloads()

    check_network()
    check_ffmpeg_silent()
    sync_anilist_pending()

    try:
        show_main_menu()
    finally:
        from weeb_cli.services.discord_rpc import discord_rpc
        discord_rpc.disconnect()

def check_incomplete_downloads():
    from weeb_cli.services.downloader import queue_manager
    
    if queue_manager.has_incomplete_downloads():
        count = queue_manager.get_incomplete_count()
        try:
            ans = questionary.confirm(
                i18n.t("downloads.resume_prompt", count=count),
                default=True
            ).ask()
            
            if ans:
                queue_manager.resume_incomplete()
                console.print(f"[green]{i18n.t('downloads.resumed')}[/green]")
            else:
                queue_manager.cancel_incomplete()
        except KeyboardInterrupt:
            queue_manager.cancel_incomplete()

def sync_anilist_pending():
    from weeb_cli.services.tracker import anilist_tracker, mal_tracker, kitsu_tracker
    
    if anilist_tracker.is_authenticated():
        pending = anilist_tracker.get_pending_count()
        if pending > 0:
            synced = anilist_tracker.sync_pending()
            if synced > 0:
                console.print(f"[dim]AniList: {synced} {i18n.t('settings.anilist_synced').split()[1]}[/dim]")
    
    if mal_tracker.is_authenticated():
        pending = mal_tracker.get_pending_count()
        if pending > 0:
            synced = mal_tracker.sync_pending()
            if synced > 0:
                console.print(f"[dim]MAL: {synced} {i18n.t('settings.mal_synced').split()[1]}[/dim]")
    
    if kitsu_tracker.is_authenticated():
        pending = kitsu_tracker.get_pending_count()
        if pending > 0:
            synced = kitsu_tracker.sync_pending()
            if synced > 0:
                console.print(f"[dim]Kitsu: {synced} {i18n.t('settings.kitsu_synced').split()[1]}[/dim]")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        start()

if __name__ == "__main__":
    app()
