"""Command handlers for Weeb CLI.

This package contains all CLI command implementations using Typer framework.
Commands provide both interactive (TUI) and non-interactive (API) interfaces.

Command Modules:
    api: Non-interactive JSON API for scripts and automation
    search: Anime search with history and filtering
    downloads: Download queue management and monitoring
    watchlist: Watch history and progress tracking
    library: Local and virtual library management
    settings: Configuration and user preferences
    setup: Initial setup wizard
    serve: Torznab server for *arr integration

Interactive Commands:
    Most commands provide rich terminal UI with menus, prompts, and
    progress indicators using Rich and Questionary libraries.

API Commands:
    The api subcommand provides JSON output for headless operation
    and integration with external tools.

Example:
    Interactive mode::

        $ weeb-cli start
    
    API mode::

        $ weeb-cli api search "anime name" --provider animecix
        $ weeb-cli api episodes <anime-id> --provider animecix
"""

__all__ = [
    "api",
    "search",
    "downloads",
    "watchlist",
    "library",
    "settings",
    "setup",
    "serve",
]
