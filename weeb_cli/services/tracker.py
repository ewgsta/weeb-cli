import requests
import webbrowser
import time
import json
import socket
from urllib.parse import parse_qs
from weeb_cli.services import logger

ANILIST_CLIENT_ID = "34596"
ANILIST_REDIRECT_URI = "http://localhost:8765/callback"
ANILIST_PORT = 8765

CALLBACK_HTML_SUCCESS = '''HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Connection: close\r
\r
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weeb CLI - AniList</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500&family=Zen+Kaku+Gothic+New:wght@300;400&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:#050505;color:#e6e6e6;font-family:'Zen Kaku Gothic New',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center}
        .noise{position:fixed;top:0;left:0;width:100%;height:100%;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;z-index:1}
        .container{position:relative;z-index:2;text-align:center;padding:3rem}
        .logo{font-family:'Shippori Mincho',serif;font-size:2.5rem;font-weight:500;margin-bottom:0.5rem}
        .subtitle{font-size:0.85rem;color:#02a9ff;margin-bottom:2rem;font-weight:500}
        .checkmark{width:48px;height:48px;margin:0 auto 1.5rem;stroke:#4ade80;stroke-width:2;fill:none}
        .checkmark path{stroke-dasharray:100;stroke-dashoffset:100;animation:draw 0.5s ease forwards}
        @keyframes draw{to{stroke-dashoffset:0}}
        .status{font-size:1.1rem;color:#4ade80;margin-bottom:1.5rem}
        .hint{font-size:0.75rem;color:#555;margin-top:2rem}
        .spinner{width:24px;height:24px;border:2px solid #333;border-top-color:#e6e6e6;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 1.5rem}
        @keyframes spin{to{transform:rotate(360deg)}}
    </style>
</head>
<body>
    <div class="noise"></div>
    <div class="container">
        <div class="logo">Weeb CLI</div>
        <div class="subtitle">AniList</div>
        <div id="content">
            <div class="spinner"></div>
        </div>
    </div>
    <script>
        const hash = window.location.hash.substring(1);
        const params = new URLSearchParams(hash);
        const token = params.get('access_token');
        if (token) {
            fetch('/token?t=' + encodeURIComponent(token))
                .then(() => {
                    document.getElementById('content').innerHTML = '<svg class="checkmark" viewBox="0 0 24 24"><path d="M4 12l6 6L20 6"/></svg>';
                });
        } else {
            document.getElementById('content').innerHTML = '<svg class="checkmark" viewBox="0 0 24 24" style="stroke:#f87171"><path d="M6 6l12 12M6 18L18 6"/></svg>';
        }
    </script>
</body>
</html>'''

CALLBACK_HTML_ERROR = '''HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Connection: close\r
\r
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weeb CLI - AniList</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500&family=Zen+Kaku+Gothic+New:wght@300;400&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:#050505;color:#e6e6e6;font-family:'Zen Kaku Gothic New',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center}
        .noise{position:fixed;top:0;left:0;width:100%;height:100%;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;z-index:1}
        .container{position:relative;z-index:2;text-align:center;padding:3rem}
        .logo{font-family:'Shippori Mincho',serif;font-size:2.5rem;font-weight:500;margin-bottom:0.5rem}
        .subtitle{font-size:0.85rem;color:#02a9ff;margin-bottom:2rem;font-weight:500}
        .status{font-size:1.1rem;color:#f87171;margin-bottom:1.5rem}
        .hint{font-size:0.75rem;color:#555;margin-top:2rem}
    </style>
</head>
<body>
    <div class="noise"></div>
    <div class="container">
        <div class="logo">Weeb CLI</div>
        <div class="subtitle">AniList</div>
        <div class="status">Yetkilendirme basarisiz</div>
    </div>
</body>
</html>'''


def wait_for_anilist_callback(timeout=120):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(("127.0.0.1", ANILIST_PORT))
        sock.listen(1)
        sock.settimeout(timeout)
        
        token = None
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                conn, addr = sock.accept()
                conn.settimeout(10)
                
                data = conn.recv(4096).decode("utf-8", errors="ignore")
                first_line = data.split("\r\n")[0] if data else ""
                
                if "/token?" in first_line:
                    if "?t=" in first_line:
                        query_part = first_line.split("?")[1].split(" ")[0]
                        params = parse_qs(query_part)
                        token = params.get("t", [None])[0]
                    
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK"
                    conn.sendall(response.encode("utf-8"))
                    conn.close()
                    
                    if token:
                        sock.close()
                        return token
                else:
                    conn.sendall(CALLBACK_HTML_SUCCESS.encode("utf-8"))
                    conn.close()
                    
            except socket.timeout:
                continue
            except Exception:
                continue
        
        sock.close()
        return None
                
    except Exception as e:
        logger.error(f"AniList callback error: {e}")
        try:
            sock.close()
        except:
            pass
        return None

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
        return f"https://anilist.co/api/v2/oauth/authorize?client_id={ANILIST_CLIENT_ID}&response_type=token"
    
    def start_auth_server(self, timeout=120):
        auth_url = self.get_auth_url()
        webbrowser.open(auth_url)
        return wait_for_anilist_callback(timeout)
    
    def _exchange_code(self, code):
        try:
            resp = requests.post(
                "https://anilist.co/api/v2/oauth/token",
                json={
                    "grant_type": "authorization_code",
                    "client_id": ANILIST_CLIENT_ID,
                    "redirect_uri": ANILIST_REDIRECT_URI,
                    "code": code
                },
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                return data.get("access_token")
            else:
                logger.error(f"AniList token exchange failed: {resp.status_code}")
        except Exception as e:
            logger.error(f"AniList token exchange error: {e}")
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
            pending = json.loads(pending) if pending else []
        return len(pending)

anilist_tracker = AniListTracker()


MAL_PROXY_URL = "https://weeb-malproxy.vercel.app"
MAL_LOCAL_PORT = 8766

MAL_CALLBACK_SUCCESS = '''HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Connection: close\r
\r
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weeb CLI - MAL</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500&family=Zen+Kaku+Gothic+New:wght@300;400&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:#050505;color:#e6e6e6;font-family:'Zen Kaku Gothic New',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center}
        .noise{position:fixed;top:0;left:0;width:100%;height:100%;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;z-index:1}
        .container{position:relative;z-index:2;text-align:center;padding:3rem}
        .logo{font-family:'Shippori Mincho',serif;font-size:2.5rem;font-weight:500;margin-bottom:0.5rem}
        .subtitle{font-size:0.85rem;color:#2e51a2;margin-bottom:2rem;font-weight:500}
        .checkmark{width:48px;height:48px;margin:0 auto 1.5rem;stroke:#4ade80;stroke-width:2;fill:none}
        .checkmark path{stroke-dasharray:100;stroke-dashoffset:100;animation:draw 0.5s ease forwards}
        @keyframes draw{to{stroke-dashoffset:0}}
        .status{font-size:1.1rem;color:#4ade80;margin-bottom:1.5rem}
        .hint{font-size:0.75rem;color:#555;margin-top:2rem}
    </style>
</head>
<body>
    <div class="noise"></div>
    <div class="container">
        <div class="logo">Weeb CLI</div>
        <div class="subtitle">MyAnimeList</div>
        <svg class="checkmark" viewBox="0 0 24 24"><path d="M4 12l6 6L20 6"/></svg>
    </div>
</body>
</html>'''

MAL_CALLBACK_ERROR = '''HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Connection: close\r
\r
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weeb CLI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500&family=Zen+Kaku+Gothic+New:wght@300;400&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:#050505;color:#e6e6e6;font-family:'Zen Kaku Gothic New',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center}
        .noise{position:fixed;top:0;left:0;width:100%;height:100%;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;z-index:1}
        .container{position:relative;z-index:2;text-align:center;padding:3rem}
        .logo{font-family:'Shippori Mincho',serif;font-size:2.5rem;font-weight:500;margin-bottom:0.5rem}
        .subtitle{font-size:0.85rem;color:#2e51a2;margin-bottom:2rem;font-weight:500}
        .checkmark{width:48px;height:48px;margin:0 auto;stroke:#f87171;stroke-width:2;fill:none}
        .checkmark path{stroke-dasharray:100;stroke-dashoffset:100;animation:draw 0.5s ease forwards}
        @keyframes draw{to{stroke-dashoffset:0}}
    </style>
</head>
<body>
    <div class="noise"></div>
    <div class="container">
        <div class="logo">Weeb CLI</div>
        <div class="subtitle">MyAnimeList</div>
        <svg class="checkmark" viewBox="0 0 24 24"><path d="M6 6l12 12M6 18L18 6"/></svg>
    </div>
</body>
</html>'''


def wait_for_mal_callback(timeout=120):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(("127.0.0.1", MAL_LOCAL_PORT))
        sock.listen(1)
        sock.settimeout(timeout)
        
        while True:
            try:
                conn, addr = sock.accept()
                conn.settimeout(10)
                
                data = conn.recv(4096).decode("utf-8", errors="ignore")
                
                code = None
                if "GET " in data:
                    first_line = data.split("\r\n")[0]
                    if "?" in first_line:
                        query_part = first_line.split("?")[1].split(" ")[0]
                        params = parse_qs(query_part)
                        code = params.get("code", [None])[0]
                
                if code:
                    conn.sendall(MAL_CALLBACK_SUCCESS.encode("utf-8"))
                else:
                    conn.sendall(MAL_CALLBACK_ERROR.encode("utf-8"))
                
                conn.close()
                
                if code:
                    sock.close()
                    return code
                    
            except socket.timeout:
                sock.close()
                return None
            except Exception:
                continue
                
    except Exception as e:
        logger.error(f"MAL callback server error: {e}")
        try:
            sock.close()
        except:
            pass
        return None

class MALTracker:
    def __init__(self):
        self._db = None
        self._access_token = None
        self._refresh_token = None
        self._expires_at = None
    
    @property
    def db(self):
        if self._db is None:
            from weeb_cli.services.database import db
            self._db = db
        return self._db
    
    def _load_tokens(self):
        if self._access_token is None:
            self._access_token = self.db.get_config("mal_access_token")
            self._refresh_token = self.db.get_config("mal_refresh_token")
            expires = self.db.get_config("mal_expires_at")
            self._expires_at = float(expires) if expires else None
    
    @property
    def access_token(self):
        self._load_tokens()
        if self._expires_at and time.time() > self._expires_at - 300:
            self._refresh_access_token()
        return self._access_token
    
    def is_authenticated(self):
        self._load_tokens()
        return self._access_token is not None
    
    def start_auth_flow(self, timeout=120):
        try:
            resp = requests.get(f"{MAL_PROXY_URL}/auth/url", timeout=10)
            if resp.status_code != 200:
                return None
            
            data = resp.json()
            auth_url = data["auth_url"]
            code_verifier = data["code_verifier"]
        except Exception as e:
            logger.error(f"MAL: Failed to get auth URL: {e}")
            return None
        
        webbrowser.open(auth_url)
        
        code = wait_for_mal_callback(timeout)
        
        if code:
            return self._exchange_code(code, code_verifier)
        return None
    
    def _exchange_code(self, code, code_verifier):
        try:
            resp = requests.post(
                f"{MAL_PROXY_URL}/auth/token",
                json={"code": code, "code_verifier": code_verifier},
                timeout=30
            )
            
            if resp.status_code != 200:
                logger.error(f"MAL: Token exchange failed: {resp.status_code}")
                return None
            
            data = resp.json()
            self._save_tokens(data)
            return self._get_user()
            
        except Exception as e:
            logger.error(f"MAL: Token exchange error: {e}")
            return None
    
    def _save_tokens(self, data):
        self._access_token = data.get("access_token")
        self._refresh_token = data.get("refresh_token")
        expires_in = data.get("expires_in", 3600)
        self._expires_at = time.time() + expires_in
        
        self.db.set_config("mal_access_token", self._access_token)
        self.db.set_config("mal_refresh_token", self._refresh_token)
        self.db.set_config("mal_expires_at", str(self._expires_at))
    
    def _refresh_access_token(self):
        if not self._refresh_token:
            return False
        
        try:
            resp = requests.post(
                f"{MAL_PROXY_URL}/auth/refresh",
                json={"refresh_token": self._refresh_token},
                timeout=30
            )
            
            if resp.status_code != 200:
                logger.error(f"MAL: Token refresh failed")
                self.logout()
                return False
            
            data = resp.json()
            self._save_tokens(data)
            return True
            
        except Exception as e:
            logger.error(f"MAL: Token refresh error: {e}")
            return False
    
    def _get_user(self):
        if not self._access_token:
            return None
        
        try:
            resp = requests.get(
                f"{MAL_PROXY_URL}/user",
                params={"access_token": self._access_token},
                timeout=10
            )
            
            if resp.status_code == 200:
                user = resp.json()
                self.db.set_config("mal_username", user.get("name"))
                self.db.set_config("mal_user_id", str(user.get("id")))
                return user
        except Exception as e:
            logger.error(f"MAL: Get user error: {e}")
        return None
    
    def get_username(self):
        return self.db.get_config("mal_username")
    
    def logout(self):
        self._access_token = None
        self._refresh_token = None
        self._expires_at = None
        self.db.set_config("mal_access_token", None)
        self.db.set_config("mal_refresh_token", None)
        self.db.set_config("mal_expires_at", None)
        self.db.set_config("mal_username", None)
        self.db.set_config("mal_user_id", None)
    
    def search_anime(self, title):
        if not self.access_token:
            return None
        
        try:
            resp = requests.get(
                f"{MAL_PROXY_URL}/search",
                params={"access_token": self.access_token, "q": title, "limit": 5},
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("data", [])
                if results:
                    return results[0].get("node")
        except Exception as e:
            logger.error(f"MAL: Search error: {e}")
        return None
    
    def update_progress(self, anime_title, episode, total_episodes=None):
        if not self.is_authenticated():
            self._queue_update(anime_title, episode, total_episodes)
            return False
        
        anime = self.search_anime(anime_title)
        if not anime:
            logger.warning(f"MAL: Anime not found: {anime_title}")
            return False
        
        anime_id = anime["id"]
        status = "watching"
        if total_episodes and episode >= total_episodes:
            status = "completed"
        
        try:
            resp = requests.post(
                f"{MAL_PROXY_URL}/anime/update",
                json={
                    "access_token": self.access_token,
                    "anime_id": anime_id,
                    "episode": episode,
                    "status": status
                },
                timeout=10
            )
            
            if resp.status_code == 200:
                logger.info(f"MAL: Updated {anime_title} to episode {episode}")
                return True
        except Exception as e:
            logger.error(f"MAL: Update error: {e}")
        return False
    
    def _queue_update(self, anime_title, episode, total_episodes):
        pending = self.db.get_config("mal_pending") or []
        if isinstance(pending, str):
            pending = json.loads(pending) if pending else []
        pending.append({
            "title": anime_title,
            "episode": episode,
            "total": total_episodes,
            "timestamp": time.time()
        })
        self.db.set_config("mal_pending", pending)
        logger.info(f"MAL: Queued update for {anime_title} ep {episode}")
    
    def sync_pending(self):
        if not self.is_authenticated():
            return 0
        
        pending = self.db.get_config("mal_pending") or []
        if isinstance(pending, str):
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
        
        self.db.set_config("mal_pending", failed)
        return synced
    
    def get_pending_count(self):
        pending = self.db.get_config("mal_pending") or []
        if isinstance(pending, str):
            pending = json.loads(pending) if pending else []
        return len(pending)

mal_tracker = MALTracker()
