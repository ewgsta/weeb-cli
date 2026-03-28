"""Settings command submodules.

This package contains the implementation of the settings command,
organized by configuration category.

Modules:
    settings_menu: Main settings menu and navigation
    settings_config: General configuration options
    settings_download: Download-related settings
    settings_cache: Cache management settings
    settings_trackers: Tracker authentication and configuration
    settings_drives: External drive management
    settings_shortcuts: Keyboard shortcuts configuration
    settings_backup: Backup and restore functionality

Each module handles a specific category of settings with dedicated
UI and validation logic.
"""

from .settings_menu import open_settings

__all__ = [
    "open_settings",
    "settings_menu",
    "settings_config",
    "settings_download",
    "settings_cache",
    "settings_trackers",
    "settings_drives",
    "settings_shortcuts",
    "settings_backup",
]
