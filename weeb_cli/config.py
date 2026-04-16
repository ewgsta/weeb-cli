"""Configuration management for Weeb CLI.

This module provides a centralized configuration system that stores settings
in a SQLite database with fallback to default values. Supports both interactive
and headless (API) modes.

Configuration is stored persistently in the database and can be accessed
throughout the application using the global `config` instance.

Example:
    Basic usage::

        from weeb_cli.config import config
        
        # Get configuration value
        download_dir = config.get("download_dir")
        aria2_enabled = config.get("aria2_enabled", True)
        
        # Set configuration value
        config.set("language", "tr")
        
        # Enable headless mode (no database access)
        config.set_headless(True)

Attributes:
    APP_NAME (str): Application name for directory naming.
    CONFIG_DIR (Path): User configuration directory (~/.weeb-cli).
    DEFAULT_CONFIG (dict): Default configuration values.
    config (Config): Global configuration instance.
"""

import os
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from weeb_cli.services.database import Database

APP_NAME = "weeb-cli"
CONFIG_DIR = Path.home() / f".{APP_NAME}"


def get_default_download_dir() -> str:
    """Get the default download directory path.
    
    Uses localized folder name from i18n translations.
    
    Returns:
        Absolute path to default download directory in current working directory.
    """
    from weeb_cli.i18n import i18n

    folder_name = i18n.t("downloads.default_folder_name", "weeb-downloads")
    return os.path.join(os.getcwd(), folder_name)


DEFAULT_CONFIG = {
    "language": None,
    "aria2_enabled": True,
    "ytdlp_enabled": True,
    "aria2_max_connections": 16,
    "max_concurrent_downloads": 3,
    "download_dir": None,
    "ytdlp_format": "bestvideo+bestaudio/best",
    "scraping_source": None,
    "show_description": True,
    "debug_mode": False,
    "download_max_retries": 3,
    "download_retry_delay": 10,
    "discord_rpc_enabled": True,
    "shortcuts_enabled": False,
    "aniskip_enabled": False,
}


class Config:
    """Configuration manager with database persistence.
    
    Provides a simple key-value interface for application settings with
    automatic persistence to SQLite database. Supports headless mode for
    API usage without database access.
    
    Attributes:
        _db (Optional[Database]): Lazy-loaded database instance.
        _headless (bool): Whether running in headless mode (no database).
    """
    
    def __init__(self) -> None:
        """Initialize configuration manager."""
        self._db: Optional['Database'] = None
        self._headless: bool = False

    @property
    def db(self) -> 'Database':
        """Get database instance with lazy loading.
        
        Returns:
            Database instance for configuration storage.
        """
        if self._db is None:
            from weeb_cli.services.database import db
            self._db = db
        return self._db

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value by key.
        
        Attempts to retrieve value from database first, then falls back to
        provided default or DEFAULT_CONFIG. Special handling for download_dir
        to generate localized default path.
        
        Args:
            key: Configuration key name.
            default: Default value if key not found in database.
        
        Returns:
            Configuration value, default, or None.
        
        Example:
            >>> config.get("language", "en")
            "tr"
            >>> config.get("aria2_max_connections")
            16
        """
        if not self._headless:
            try:
                val = self.db.get_config(key)
                if val is not None:
                    return val
            except Exception as e:
                from weeb_cli.services.logger import debug
                debug(f"[Config] DB read failed for '{key}': {e}")

        # Special handling for download_dir
        if key == "download_dir":
            return default if default is not None else get_default_download_dir()

        # Use provided default, fallback to DEFAULT_CONFIG, then None
        if default is not None:
            return DEFAULT_CONFIG.get(key, default)
        return DEFAULT_CONFIG.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Persists the value to database for future retrieval.
        
        Args:
            key: Configuration key name.
            value: Value to store (must be JSON-serializable).
        
        Example:
            >>> config.set("language", "tr")
            >>> config.set("aria2_max_connections", 32)
        """
        self.db.set_config(key, value)

    def set_headless(self, headless: bool = True) -> None:
        """Enable or disable headless mode.
        
        In headless mode, configuration is read from DEFAULT_CONFIG only,
        without database access. Useful for API commands and testing.
        
        Args:
            headless: Whether to enable headless mode.
        """
        self._headless = headless


config = Config()
