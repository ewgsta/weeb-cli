"""User Interface components for Weeb CLI.

This package contains terminal UI components built with Textual
framework for creating a modern, reactive dashboard TUI.

Modules:
    app: Main Textual application class
    header: Application header utilities
    menu: Entry point wrapper for the TUI

Subpackages:
    screens: Individual application screens (search, watchlist, etc.)
    widgets: Reusable UI widgets (sidebar, episode list, etc.)
    styles: TCSS theme and styling files
"""

__all__ = ["app", "header", "menu", "screens", "widgets"]
