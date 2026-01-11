import json
import os
import sys
from pathlib import Path
from weeb_cli.config import config

def get_locales_dir():
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
        possible_path = base_path / "weeb_cli" / "locales"
        if possible_path.exists():
            return possible_path
        return base_path / "locales"
    
    return Path(__file__).parent / "locales"

LOCALES_DIR = get_locales_dir()

class I18n:
    def __init__(self):
        self.language = config.get("language", "en")
        self.translations = {}
        self.load_translations()

    def set_language(self, language_code):
        self.language = language_code
        config.set("language", language_code)
        self.load_translations()

    def load_translations(self):
        file_path = LOCALES_DIR / f"{self.language}.json"
        if not file_path.exists():
            file_path = LOCALES_DIR / "en.json"
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except Exception as e:
            print(f"Error loading translations: {e}")
            self.translations = {}

    def get(self, key_path, **kwargs):
        keys = key_path.split(".")
        value = self.translations
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return key_path

        if value is None:
            return key_path

        if isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value
        
        return value
    
    t = get

i18n = I18n()
