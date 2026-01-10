import typer
import questionary
from weeb_cli.ui.menu import show_main_menu
from weeb_cli.commands.hello import say_hello
from weeb_cli.commands.settings import open_settings
from weeb_cli.config import config
from weeb_cli.i18n import i18n

app = typer.Typer(add_completion=False)

def run_setup():
    """First run setup to select language."""
    langs = {
        "Türkçe": "tr",
        "English": "en"
    }
    
    selected = questionary.select(
        "Select Language / Dil Seçiniz",
        choices=list(langs.keys()),
        use_indicator=True
    ).ask()
    
    if selected:
        i18n.set_language(langs[selected])

@app.command()
def start():
    # If language is not set (first run), run setup
    if not config.get("language"):
        run_setup()

    # Define actions mapping: Key (for i18n lookup) -> Function
    actions = {
        "hello": say_hello,
        "settings": open_settings
    }
    show_main_menu(actions)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        start()

if __name__ == "__main__":
    app()
