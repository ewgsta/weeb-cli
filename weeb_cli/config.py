import json
import os
from pathlib import Path

APP_NAME = "weeb-cli"
CONFIG_DIR = Path.home() / f".{APP_NAME}"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "language": None,  
    "aria2_enabled": True,
    "ytdlp_enabled": True,
    "aria2_max_connections": 16,
    "aria2_download_dir": str(Path.home() / "Downloads"),
    "ytdlp_format": "bestvideo+bestaudio/best",
    "scraping_source": "",
    "api_url": "https://weeb-api.ewgsta.me"
}

class Config:
    def __init__(self):
        self._ensure_config_exists()
        self.data = self._load()

    def _ensure_config_exists(self):
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILE.exists():
            self._save(DEFAULT_CONFIG)

    def _load(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return DEFAULT_CONFIG.copy()

    def _save(self, data):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save(self.data)

config = Config()
