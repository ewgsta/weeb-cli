import json
import time
from typing import Optional, List, Dict, Any
from weeb_cli.services._base import LazyService
from weeb_cli.services import logger


class BaseTracker(LazyService):
    
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
        self._pending_key = f"{service_name}_pending"
    
    def is_authenticated(self) -> bool:
        raise NotImplementedError
    
    def update_progress(self, anime_title: str, episode: int, 
                       total_episodes: Optional[int] = None) -> bool:
        raise NotImplementedError
    
    def _queue_update(self, anime_title: str, episode: int, 
                     total_episodes: Optional[int]) -> None:
        pending = self._get_pending_list()
        pending.append({
            "title": anime_title,
            "episode": episode,
            "total": total_episodes,
            "timestamp": time.time()
        })
        self._save_pending_list(pending)
        logger.info(f"{self.service_name}: Queued update for {anime_title} ep {episode}")
    
    def _get_pending_list(self) -> List[Dict]:
        pending = self.db.get_config(self._pending_key) or []
        if isinstance(pending, str):
            pending = json.loads(pending) if pending else []
        return pending
    
    def _save_pending_list(self, pending: List[Dict]) -> None:
        self.db.set_config(self._pending_key, pending)
    
    def sync_pending(self) -> int:
        if not self.is_authenticated():
            return 0
        
        pending = self._get_pending_list()
        if not pending:
            return 0
        
        synced = 0
        failed = []
        
        for item in pending:
            success = self.update_progress(
                item["title"],
                item["episode"],
                item.get("total")
            )
            if success:
                synced += 1
            else:
                failed.append(item)
        
        self._save_pending_list(failed)
        return synced
    
    def get_pending_count(self) -> int:
        return len(self._get_pending_list())
    
    def logout(self) -> None:
        raise NotImplementedError
