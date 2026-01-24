from weeb_cli.config import config

DEFAULT_SHORTCUTS = {
    "search": "s",
    "downloads": "d",
    "watchlist": "w",
    "settings": "c",
    "exit": "q",
    "next_episode": "n",
    "prev_episode": "p",
    "back": "b",
    "help": "h"
}

class ShortcutManager:
    def __init__(self):
        self._shortcuts = None
    
    def is_enabled(self):
        return config.get("shortcuts_enabled", True)
    
    def get_shortcuts(self):
        if not self.is_enabled():
            return {}
        
        if self._shortcuts is None:
            self._shortcuts = {}
            for key, default_value in DEFAULT_SHORTCUTS.items():
                value = config.get(f"shortcut_{key}", default_value)
                self._shortcuts[key] = value
        return self._shortcuts
    
    def get_shortcut(self, action):
        if not self.is_enabled():
            return None
        shortcuts = self.get_shortcuts()
        return shortcuts.get(action, DEFAULT_SHORTCUTS.get(action))
    
    def set_shortcut(self, action, key):
        config.set(f"shortcut_{action}", key)
        self._shortcuts = None
    
    def reset_shortcuts(self):
        for action in DEFAULT_SHORTCUTS.keys():
            config.set(f"shortcut_{action}", DEFAULT_SHORTCUTS[action])
        self._shortcuts = None
    
    def get_all_shortcuts_display(self):
        shortcuts = self.get_shortcuts()
        return {action: key for action, key in shortcuts.items()}

shortcut_manager = ShortcutManager()
