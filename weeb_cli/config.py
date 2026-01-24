import os
from pathlib import Path

APP_NAME = "weeb-cli"
CONFIG_DIR = Path.home() / f".{APP_NAME}"

DEFAULT_CONFIG = {
    "language": None,  
    "aria2_enabled": True,
    "ytdlp_enabled": True,
    "aria2_max_connections": 16,
    "max_concurrent_downloads": 3,
    "download_dir": os.path.join(os.getcwd(), "weeb-downloads"),
    "ytdlp_format": "bestvideo+bestaudio/best",
    "scraping_source": "animecix",
    "show_description": True,
    "debug_mode": False,
    "download_max_retries": 3,
    "download_retry_delay": 10,
    "discord_rpc_enabled": False,
    "shortcuts_enabled": True
}

class Config:
    def __init__(self):
        self._db = None
    
    @property
    def db(self):
        if self._db is None:
            from weeb_cli.services.database import db
            self._db = db
        return self._db
    
    def get(self, key, default=None):
        val = self.db.get_config(key)
        if val is None:
            return DEFAULT_CONFIG.get(key, default)
        return val
    
    def set(self, key, value):
        self.db.set_config(key, value)

config = Config()
