"""Main menu entry point for Weeb CLI.

This module provides the show_main_menu() function as the entry point
for the interactive TUI. It launches the Textual application.
"""

from weeb_cli.ui.app import WeebApp


def show_main_menu():
    """Launch the Textual TUI application.

    This is the main entry point called from main.py.
    Replaces the old questionary-based menu loop.
    """
    app = WeebApp()
    app.run()
