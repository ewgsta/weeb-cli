import os
import re
import json
from typing import List, Optional, Dict
from hashlib import md5
from base64 import b64decode

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider

try:
    from curl_cffi import requests as curl_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

try:
    from Crypto.Cipher import AES
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    from appdirs import user_cache_dir
    HAS_APPDIRS = True
except ImportError:
    HAS_APPDIRS = False

BASE_URL = "https://turkanime.tv"
_session = None
_base_url = None
_key_cache = None
_csrf_cache = None

SUPPORTED_PLAYERS = [
    "YADISK", "MAIL", "ALUCARD(BETA)", "PIXELDRAIN", "AMATERASU(BETA)",
    "HDVID", "ODNOKLASSNIKI", "GDRIVE", "MP4UPLOAD", "DAILYMOTION",
    "SIBNET", "VK", "VIDMOLY", "YOURUPLOAD", "SENDVID", "MYVI", "UQLOAD"
]


def _init_session():
    global _session, _base_url
    
    if _session is not None:
        return _session
    
    if HAS_CURL_CFFI:
        _session = curl_requests.Session(impersonate="firefox", allow_redirects=True)
    else:
        import requests
        _session = requests.Session()
    
    _base_url = BASE_URL
    
    try:
        res = _session.get(BASE_URL + "/", timeout=30)
        if res.status_code == 200:
            final_url = res.url if hasattr(res, 'url') else BASE_URL
            _base_url = final_url.rstrip('/')
    except Exception:
        _base_url = BASE_URL
    
    return _session


def _fetch(path: str, headers: Dict[str, str] = None) -> str:
    global _base_url
    session = _init_session()
    
    if path is None:
        return ""
    
    if _base_url is None:
        _base_url = BASE_URL
    
    path = path if path.startswith("/") else "/" + path
    url = _base_url + path
    
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    if headers:
        default_headers.update(headers)
    
    try:
        response = session.get(url, headers=default_headers, timeout=30)
        return response.text
    except Exception:
        return ""


def _obtain_key() -> bytes:
    global _key_cache
    
    if _key_cache:
        return _key_cache
    
    if HAS_APPDIRS:
        try:
            cache_file = os.path.join(user_cache_dir(), "turkanimu_key.cache")
            if os.path.isfile(cache_file):
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = f.read().strip().encode()
                    if cached:
                        _key_cache = cached
                        return _key_cache
        except Exception:
            pass
    
    try:
        embed_html = _fetch("/embed/#/url/")
        js_files = re.findall(r"/embed/js/embeds\..*?\.js", embed_html)
        
        if len(js_files) < 2:
            return b""
        
        js1 = _fetch(js_files[1])
        js1_imports = re.findall("[a-z0-9]{16}", js1)
        
        if not js1_imports:
            return b""
        
        j2 = _fetch(f'/embed/js/embeds.{js1_imports[0]}.js')
        if "'decrypt'" not in j2 and len(js1_imports) > 1:
            j2 = _fetch(f'/embed/js/embeds.{js1_imports[1]}.js')
        
        match = re.search(
            r'function a\d_0x[\w]{1,4}\(\)\{var _0x\w{3,8}=\[(.*?)\];', j2
        )
        if not match:
            return b""
        
        obfuscate_list = match.group(1)
        _key_cache = max(
            obfuscate_list.split("','"),
            key=lambda i: len(re.sub(r"\\x\d\d", "?", i))
        ).encode()
        
        if HAS_APPDIRS and _key_cache:
            try:
                cache_dir = user_cache_dir()
                os.makedirs(cache_dir, exist_ok=True)
                cache_file = os.path.join(cache_dir, "turkanimu_key.cache")
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(_key_cache.decode("utf-8"))
            except Exception:
                pass
        
        return _key_cache
        
    except Exception:
        return b""


def _decrypt_cipher(key: bytes, data: bytes) -> str:
    if not HAS_CRYPTO:
        return ""
    
    def salted_key(data: bytes, salt: bytes, output: int = 48):
        data += salt
        k = md5(data).digest()
        final_key = k
        while len(final_key) < output:
            k = md5(k + data).digest()
            final_key += k
        return final_key[:output]
    
    def unpad(data: bytes) -> bytes:
        return data[:-(data[-1] if isinstance(data[-1], int) else ord(data[-1]))]
    
    try:
        b64 = b64decode(data)
        cipher = json.loads(b64)
        cipher_text = b64decode(cipher["ct"])
        iv = bytes.fromhex(cipher["iv"])
        salt = bytes.fromhex(cipher["s"])
        
        crypt = AES.new(salted_key(key, salt, output=32), iv=iv, mode=AES.MODE_CBC)
        return unpad(crypt.decrypt(cipher_text)).decode("utf-8")
    except Exception:
        return ""


def _get_real_url(url_cipher: str) -> str:
    if HAS_APPDIRS:
        try:
            cache_file = os.path.join(user_cache_dir(), "turkanimu_key.cache")
            if os.path.isfile(cache_file):
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_key = f.read().strip().encode()
                    plaintext = _decrypt_cipher(cached_key, url_cipher.encode())
                    if plaintext:
                        return "https:" + json.loads(plaintext)
        except Exception:
            pass
    
    key = _obtain_key()
    if not key:
        return ""
    
    plaintext = _decrypt_cipher(key, url_cipher.encode())
    if not plaintext:
        return ""
    
    try:
        return "https:" + json.loads(plaintext)
    except Exception:
        return ""


def _decrypt_jsjiamiv7(ciphertext: str, key: str) -> str:
    _CUSTOM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/"
    _STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    _TRANSLATE = str.maketrans(_CUSTOM, _STD)
    
    t = ciphertext.translate(_TRANSLATE)
    t += "=" * (-len(t) % 4)
    
    try:
        data = b64decode(t).decode("utf-8")
    except Exception:
        return ""
    
    S = list(range(256))
    j = 0
    klen = len(key)
    
    for i in range(256):
        j = (j + S[i] + ord(key[i % klen])) & 0xff
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    out = []
    for ch in data:
        i = (i + 1) & 0xff
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(ch) ^ S[(S[i] + S[j]) & 0xff]))
    
    return "".join(out)


def _obtain_csrf() -> Optional[str]:
    global _csrf_cache
    
    if _csrf_cache:
        return _csrf_cache
    
    try:
        res = _fetch("/js/player.js")
        
        key_match = re.findall(r"csrf-token':[^\n\)]+'([^']+)'\)", res, re.IGNORECASE)
        candidates = re.findall(r"'([a-zA-Z\d\+\/]{96,156})',", res)
        
        if not key_match or not candidates:
            return None
        
        key = key_match[0]
        
        for ct in candidates:
            decrypted = _decrypt_jsjiamiv7(ct, key)
            if re.search(r"^[a-zA-Z/\+]+$", decrypted):
                _csrf_cache = decrypted
                return _csrf_cache
        
        return None
    except Exception:
        return None


def _unmask_real_url(url_mask: str) -> str:
    if "turkanime" not in url_mask:
        return url_mask
    
    csrf = _obtain_csrf()
    if not csrf:
        return url_mask
    
    try:
        mask = url_mask.split("/player/")[1]
        headers = {"Csrf-Token": csrf, "cf_clearance": "dull"}
        res = _fetch(f"/sources/{mask}/false", headers)
        
        data = json.loads(res)
        url = data["response"]["sources"][-1]["file"]
        
        if url.startswith("//"):
            url = "https:" + url
        
        return url
    except Exception:
        return url_mask


@register_provider("turkanime", lang="tr", region="TR")
class TurkAnimeProvider(BaseProvider):
    
    def __init__(self):
        super().__init__()
    
    def search(self, query: str) -> List[AnimeResult]:
        html = _fetch("/ajax/tamliste")
        if not html:
            return []
        
        matches = re.findall(r'/anime/(.*?)".*?animeAdi">(.*?)<', html)
        
        results = []
        query_lower = query.lower()
        
        for slug, title in matches:
            title_clean = re.sub(r'<[^>]+>', '', title)
            if query_lower in title_clean.lower() or query_lower in slug.lower():
                results.append(AnimeResult(
                    id=slug,
                    title=title_clean
                ))
        
        return results[:20]
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        html = _fetch(f'/anime/{anime_id}')
        if not html:
            return None
        
        title_match = re.findall(r'<title>(.*?)</title>', html)
        title = title_match[0] if title_match else anime_id
        
        img_match = re.findall(r'twitter.image" content="(.*?)"', html)
        cover = img_match[0] if img_match else None
        
        anime_id_match = re.findall(r'serilerb/(.*?)\.jpg', html)
        internal_id = anime_id_match[0] if anime_id_match else ""
        
        description = None
        desc_match = re.search(r'twitter:description"\s+content="([^"]+)"', html)
        if not desc_match:
            desc_match = re.search(r'og:description"\s+content="([^"]+)"', html)
        if desc_match:
            import html as html_module
            description = html_module.unescape(desc_match.group(1)).strip()
        
        info = {}
        info_table = re.findall(r'<div id="animedetay">(<table.*?</table>)', html, re.DOTALL)
        if info_table:
            raw_m = re.findall(r"<tr>.*?<b>(.*?)</b>.*?width.*?>(.*?)</td>.*?</tr>", info_table[0], re.DOTALL)
            for key, val in raw_m:
                val = re.sub(r"<[^>]*>", "", val).strip()
                info[key] = val
        
        genres = []
        if "Anime Türü" in info:
            genres = [g.strip() for g in info["Anime Türü"].split("  ") if g.strip()]
        
        episodes = self._get_episodes_internal(internal_id) if internal_id else []
        
        return AnimeDetails(
            id=anime_id,
            title=title,
            description=description,
            cover=cover,
            genres=genres,
            status=info.get("Kategori"),
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        html = _fetch(f'/anime/{anime_id}')
        if not html:
            return []
        
        anime_id_match = re.findall(r'serilerb/(.*?)\.jpg', html)
        internal_id = anime_id_match[0] if anime_id_match else ""
        
        if not internal_id:
            return []
        
        return self._get_episodes_internal(internal_id)
    
    def _get_episodes_internal(self, internal_id: str) -> List[Episode]:
        html = _fetch(f'/ajax/bolumler&animeId={internal_id}')
        if not html:
            return []
        
        matches = re.findall(r'/video/(.*?)\\?".*?title=.*?"(.*?)\\?"', html)
        
        episodes = []
        for i, (slug, title) in enumerate(matches, 1):
            title_clean = re.sub(r'\\["\']', '', title)
            ep_num = self._parse_episode_number(title_clean, i)
            episodes.append(Episode(
                id=slug,
                number=ep_num,
                title=title_clean
            ))
        
        return episodes
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        html = _fetch(f'/video/{episode_id}')
        if not html:
            return []
        
        streams = []
        
        if not re.search(r".*birden fazla grup", html):
            fansub_match = re.findall(r"</span> ([^\\<>]*)</button>.*?iframe", html)
            fansub = fansub_match[0] if fansub_match else "Unknown"
            
            video_matches = re.findall(
                r'/embed/#/url/(.*?)\?status=0".*?</span> ([^ ]*?) ?</button>',
                html
            )
            video_matches += re.findall(
                r'(ajax/videosec&b=[A-Za-z0-9]+&v=.*?)\'.*?</span> ?(.*?)</button',
                html
            )
            
            for cipher_or_path, player in video_matches:
                stream = self._process_video(cipher_or_path, player, fansub)
                if stream:
                    streams.append(stream)
        else:
            fansub_matches = re.findall(r"(ajax/videosec&.*?)'.*?</span> ?(.*?)</a>", html)
            
            for path, fansub in fansub_matches:
                src = _fetch(path)
                
                video_matches = re.findall(
                    r'/embed/#/url/(.*?)\?status=0".*?</span> ([^ ]*?) ?</button>',
                    src
                )
                video_matches += re.findall(
                    r'(ajax/videosec&b=[A-Za-z0-9]+&v=.*?)\'.*?</span> ?(.*?)</button',
                    src
                )
                
                for cipher_or_path, player in video_matches:
                    stream = self._process_video(cipher_or_path, player, fansub)
                    if stream:
                        streams.append(stream)
        
        return streams
    
    def _process_video(self, cipher_or_path: str, player: str, fansub: str) -> Optional[StreamLink]:
        if player.upper() not in SUPPORTED_PLAYERS:
            return None
        
        if "/" in cipher_or_path:
            src = _fetch(cipher_or_path)
            cipher_match = re.findall(r'/embed/#/url/(.*?)\?status', src)
            if not cipher_match:
                return None
            cipher = cipher_match[0]
        else:
            cipher = cipher_or_path
        
        url = _get_real_url(cipher)
        if not url:
            return None
        
        url = url.replace("uqload.io", "uqload.com")
        
        if "turkanime" in url:
            url = _unmask_real_url(url)
            if "turkanime" in url:
                return None
        
        return StreamLink(
            url=url,
            quality="auto",
            server=f"{fansub} - {player}"
        )
    
    def _parse_episode_number(self, title: str, fallback: int) -> int:
        patterns = [
            r'(\d+)\.\s*[Bb]ölüm',
            r'[Bb]ölüm\s*(\d+)',
            r'[Ee]pisode\s*(\d+)',
            r'^(\d+)$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                return int(match.group(1))
        
        return fallback
