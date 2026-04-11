"""Command handlers and API endpoints for Weeb CLI.

This package contains CLI command implementations using the Typer framework.
The interactive Textual UI is managed separately from the API endpoints.

Command Modules:
    api: Non-interactive JSON API for scripts and automation
    serve: Torznab server for *arr integration
    serve_restful: RESTful JSON API server
    setup: Initial setup wizard and dependency installer

Example:
    Interactive mode:
        $ weeb-cli start
    
    API mode:
        $ weeb-cli api search "anime name" --provider animecix
        $ weeb-cli serve --port 8080
"""

__all__ = [
    "api",
    "serve",
    "serve_restful",
    "setup",
]
