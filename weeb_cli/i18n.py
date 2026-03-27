"""Internationalization (i18n) support for Weeb CLI.

This module provides multi-language support through JSON-based translation files.
Supports Turkish (tr), English (en), German (de), and Polish (pl).

The translation system uses dot-notation for nested keys and supports
string interpolation with keyword arguments.

Example:
    Basic usage::

        from weeb_cli.i18n import i18n
        
        # Get translated string
        message = i18n.t("menu.search", "Search Anime")
        
        # With interpolation
        greeting = i18n.t("welcome.user", name="John")
        
        # Change language
        i18n.set_language("tr")

Attributes:
    LOCALES_DIR (Path): Directory containing translation JSON files.
    i18n (I18n): Global i18n instance for application-wide use.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from weeb_cli.config import config


def get_locales_dir() -> Path:
    """Get the locales directory path.
    
    Handles both development and frozen (PyInstaller) environments.
    
    Returns:
        Path to the locales directory containing translation files.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
        possible_path = base_path / "weeb_cli" / "locales"
        if possible_path.exists():
            return possible_path
        return base_path / "locales"
    
    return Path(__file__).parent / "locales"


LOCALES_DIR = get_locales_dir()


class I18n:
    """Internationalization manager for multi-language support.
    
    Loads and manages translation strings from JSON files, providing
    a simple interface for retrieving localized text with support for
    nested keys and string interpolation.
    
    Attributes:
        language (str): Current language code (e.g., 'en', 'tr', 'de', 'pl').
        translations (Dict[str, Any]): Loaded translation dictionary.
    """
    
    def __init__(self) -> None:
        """Initialize i18n with language from config or default to English."""
        try:
            self.language: str = config.get("language", "en")
        except Exception:
            self.language = "en"
        self.translations: Dict[str, Any] = {}
        self.load_translations()

    def set_language(self, language_code: str) -> None:
        """Set the active language and reload translations.
        
        Args:
            language_code: Language code (e.g., 'en', 'tr', 'de', 'pl').
        """
        self.language = language_code
        config.set("language", language_code)
        self.load_translations()

    def load_translations(self) -> None:
        """Load translation file for the current language.
        
        Falls back to English if the requested language file doesn't exist.
        Silently handles file read errors by using an empty dictionary.
        """
        file_path = LOCALES_DIR / f"{self.language}.json"
        if not file_path.exists():
            file_path = LOCALES_DIR / "en.json"
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except Exception:
            self.translations = {}

    def get(self, key_path: str, default: Optional[str] = None, **kwargs: Any) -> str:
        """Get translated string by dot-notation key path.
        
        Supports nested keys using dot notation (e.g., 'menu.search.title')
        and string interpolation using keyword arguments.
        
        Args:
            key_path: Dot-separated path to translation key (e.g., 'menu.search').
            default: Default value if key not found. If None, returns key_path.
            **kwargs: Variables for string interpolation using .format().
        
        Returns:
            Translated and interpolated string, or default/key_path if not found.
        
        Example:
            >>> i18n.get("welcome.message", name="John")
            "Welcome, John!"
            >>> i18n.get("missing.key", "Default Text")
            "Default Text"
        """
        keys = key_path.split(".")
        value: Any = self.translations
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default if default is not None else key_path

        if value is None:
            return default if default is not None else key_path

        if isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value
        
        return value
    
    # Alias for convenience
    t = get


i18n = I18n()
