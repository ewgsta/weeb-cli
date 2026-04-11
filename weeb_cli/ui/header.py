"""Application header display for Weeb CLI.

Provides header functionality for both Textual screens
and backward-compatible rich console output.
"""

from weeb_cli.config import config
from weeb_cli import __version__


def get_header_text(title="Weeb CLI", show_version=False, show_source=False):
    """Get formatted header text string.

    Args:
        title: Header title text.
        show_version: Whether to show version number.
        show_source: Whether to show current scraping source.

    Returns:
        Formatted header string with optional version and source info.
    """
    parts = []

    if show_source:
        cfg_source = config.get("scraping_source")
        if not cfg_source:
            from weeb_cli.providers.registry import get_default_provider
            lang = config.get("language", "tr")
            cfg_source = get_default_provider(lang) or "animecix"
        parts.append(cfg_source.capitalize())

    if show_version:
        parts.append(f"v{__version__}")

    if parts:
        joined = " | ".join(parts)
        return f" {title}  | {joined}"

    return f" {title} "
