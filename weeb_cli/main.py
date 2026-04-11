"""CLI entry point for Weeb CLI.

This module provides the main CLI interface using Typer.
The interactive TUI is handled by the Textual application (WeebApp),
while API and serve commands remain as Typer subcommands.
"""

import typer
import sys
from weeb_cli.commands.api import api_app
from weeb_cli.commands.serve import serve_app

app = typer.Typer(add_completion=False)
app.add_typer(api_app, name="api")
app.add_typer(serve_app, name="serve")


@app.command()
def start():
    """Launch the interactive Textual TUI."""
    from weeb_cli.ui.menu import show_main_menu

    try:
        show_main_menu()
    finally:
        try:
            from weeb_cli.services.discord_rpc import discord_rpc
            discord_rpc.disconnect()
        except Exception:
            pass


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        start()


if __name__ == "__main__":
    app()
