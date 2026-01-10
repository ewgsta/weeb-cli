import typer
from .ui.menu import show_main_menu
from .commands.hello import say_hello
from .ui.header import show_header

app = typer.Typer(add_completion=False)

@app.command()
def start():
    actions = {
        "Selam Ver": say_hello,
        "Uygulama Hakkında": lambda: print("Weeb CLI v0.0.1")
    }
    show_main_menu(actions)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        start()

if __name__ == "__main__":
    app()
