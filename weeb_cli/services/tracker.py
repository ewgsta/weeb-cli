import requests
import webbrowser
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from threading import Thread
from weeb_cli.services.logger import logger

ANILIST_CLIENT_ID = "24285"
ANILIST_REDIRECT_URI = "http://localhost:8765/callback"

class TokenHandler(BaseHTTPRequestHandler):
    token = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path.startswith("/callback"):
            html = """
            <html><head><script>
            const hash = window.location.hash.substring(1);
            const params = new URLSearchParams(hash);
            const token = params.get('access_token');
            if (token) {
                fetch('/token?access_token=' + token).then(() => {
                    document.body.innerHTML = '<h2>Başarılı! Bu pencereyi kapatabilirsiniz.</h2>';
                });
            }
            </script></head><body><h2>Yetkilendiriliyor...</h2></body></html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path.startswith("/token"):
            query = parse_qs(urlparse(self.path).query)
            if "access_token" in query:
                TokenHandler.token = query["access_token"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

class AniListTracker:
    def __init__(self):
        self._db = None
        self._token = None
        self._user_id = None
    
    @property
    def db(self):
        if self._db is None:
            from weeb_cli.services.database import db
            self._db = db
        return self._db
    
    @property
    def token(self):
        if self._token is None:
            self._token = self.db.get_config("anilist_token")
        return self._token
    
    @property
    def user_id(self):
        if self._user_id is None:
            self._user_id = self.db.get_config("anilist_user_id")
        return self._user_id
    
    def is_authenticated(self):
        return self.token is not None
    
    def get_auth_url(self):
        return f"https://anilist.co/api/v2/oauth/authorize?client_id={ANILIST_CLIENT_ID}&redirect_uri={ANILIST_REDIRECT_URI}&response_type=token"
    
    def start_auth_server(self, timeout=120):
        TokenHandler.token = None
        server = HTTPServer(("localhost", 8765), TokenHandler)
        server.timeout = 1
        
        auth_url = self.get_auth_url()
        webbrowser.open(auth_url)
        
        start = time.time()
        while time.time() - start < timeout:
            server.handle_request()
            if TokenHandler.token:
                server.server_close()
                return TokenHandler.token
        
        server.server_close()
        return None
    
    def authenticate(self, token):
        self._token = token
        self.db.set_config("anilist_token", token)
        
        user = self._get_viewer()
        if user:
            self._user_id = str(user["id"])
            self.db.set_config("anilist_user_id", self._user_id)
            self.db.set_config("anilist_username", user["name"])
            return True
        return False
    
    def logout(self):
        self._token = None
        self._user_id = None
        self.db.set_config("anilist_token", None)
        self.db.set_config("anilist_user_id", None)
        self.db.set_config("anilist_username", None)
    
    def get_username(self):
        return self.db.get_config("anilist_username")
    
    def _graphql(self, query, variables=None):
        if not self.token:
            return None
        
        try:
            resp = requests.post(
                "https://graphql.anilist.co",
                json={"query": query, "variables": variables or {}},
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=10
            )
            if resp.status_code == 200:
                return resp.json().get("data")
            logger.error(f"AniList API error: {resp.status_code}")
        except Exception as e:
            logger.error(f"AniList request failed: {e}")
        return None
    
    def _get_viewer(self):
        query = """
        query {
            Viewer {
                id
                name
            }
        }
        """
        data = self._graphql(query)
        return data.get("Viewer") if data else None
    
    def search_anime(self, title):
        query = """
        query ($search: String) {
            Media(search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                episodes
            }
        }
        """
        data = self._graphql(query, {"search": title})
        return data.get("Media") if data else None
    
    def update_progress(self, anime_title, episode, total_episodes=None):
        if not self.is_authenticated():
            self._queue_update(anime_title, episode, total_episodes)
            return False
        
        media = self.search_anime(anime_title)
        if not media:
            logger.warning(f"AniList: Anime not found: {anime_title}")
            return False
        
        media_id = media["id"]
        
        query = """
        mutation ($mediaId: Int, $progress: Int, $status: MediaListStatus) {
            SaveMediaListEntry(mediaId: $mediaId, progress: $progress, status: $status) {
                id
                progress
                status
            }
        }
        """
        
        status = "CURRENT"
        if total_episodes and episode >= total_episodes:
            status = "COMPLETED"
        
        variables = {
            "mediaId": media_id,
            "progress": episode,
            "status": status
        }
        
        result = self._graphql(query, variables)
        if result:
            logger.info(f"AniList: Updated {anime_title} to episode {episode}")
            return True
        return False
    
    def _queue_update(self, anime_title, episode, total_episodes):
        pending = self.db.get_config("anilist_pending") or []
        if isinstance(pending, str):
            import json
            pending = json.loads(pending) if pending else []
        pending.append({
            "title": anime_title,
            "episode": episode,
            "total": total_episodes,
            "timestamp": time.time()
        })
        self.db.set_config("anilist_pending", pending)
        logger.info(f"AniList: Queued update for {anime_title} ep {episode}")
    
    def sync_pending(self):
        if not self.is_authenticated():
            return 0
        
        pending = self.db.get_config("anilist_pending") or []
        if isinstance(pending, str):
            import json
            pending = json.loads(pending) if pending else []
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
        
        self.db.set_config("anilist_pending", failed)
        return synced
    
    def get_pending_count(self):
        pending = self.db.get_config("anilist_pending") or []
        if isinstance(pending, str):
            import json
            pending = json.loads(pending) if pending else []
        return len(pending)

anilist_tracker = AniListTracker()
