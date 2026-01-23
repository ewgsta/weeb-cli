import time
import requests
from typing import Optional
from pypresence import Presence
from weeb_cli.config import config

class DiscordRPC:
    def __init__(self):
        self.client_id = "1449760321764855858"
        self.rpc: Optional[Presence] = None
        self.connected = False
        self.current_anime = None
        self.current_episode = None
        self.start_time = None
        
    def is_enabled(self):
        return config.get("discord_rpc_enabled", False)
    
    def connect(self):
        if not self.is_enabled():
            return False
            
        if self.connected:
            return True
            
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            return True
        except Exception:
            self.connected = False
            return False
    
    def disconnect(self):
        if self.rpc and self.connected:
            try:
                self.rpc.close()
            except Exception:
                pass
            finally:
                self.connected = False
                self.rpc = None
    
    def _get_anime_image(self, anime_title: str) -> Optional[str]:
        try:
            search_url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"
            response = requests.get(search_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data") and len(data["data"]) > 0:
                    anime = data["data"][0]
                    images = anime.get("images", {})
                    jpg = images.get("jpg", {})
                    return jpg.get("large_image_url") or jpg.get("image_url")
        except Exception:
            pass
        
        return None
    
    def update_presence(self, anime_title: str, episode_number: int, total_episodes: Optional[int] = None):
        if not self.is_enabled():
            return
            
        if not self.connected:
            if not self.connect():
                return
        
        self.current_anime = anime_title
        self.current_episode = episode_number
        
        if self.start_time is None:
            self.start_time = int(time.time())
        
        lang = config.get("language", "tr")
        
        if lang == "tr":
            state_text = f"{episode_number}. bölümü izliyor"
            if total_episodes:
                details_text = f"{total_episodes} bölümde"
            else:
                details_text = "Anime izliyor"
        else:
            state_text = f"Watching episode {episode_number}"
            if total_episodes:
                details_text = f"Out of {total_episodes} episodes"
            else:
                details_text = "Watching anime"
        
        image_url = self._get_anime_image(anime_title)
        
        try:
            presence_data = {
                "details": details_text,
                "state": state_text,
                "start": self.start_time,
                "large_text": anime_title,
            }
            
            if image_url:
                presence_data["large_image"] = image_url
            
            self.rpc.update(**presence_data)
        except Exception:
            self.connected = False
    
    def clear_presence(self):
        if self.rpc and self.connected:
            try:
                self.rpc.clear()
            except Exception:
                pass
        
        self.current_anime = None
        self.current_episode = None
        self.start_time = None

discord_rpc = DiscordRPC()
