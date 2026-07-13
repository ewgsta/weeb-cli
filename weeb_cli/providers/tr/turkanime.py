"""
Turkanime provider for weeb-cli.

This provider supports turkanime.tv, a Turkish anime streaming site.
Uses curl-cffi for Firefox impersonation to bypass Cloudflare protection.

Features:
- Cloudflare bypass with curl-cffi (Firefox TLS fingerprint)
- Dynamic key extraction and caching
- CSRF token management
- Support for multiple fansubs and video servers
- AES decryption for video URLs
"""

import os
import re
import json
from typing import List, Optional, Dict
from hashlib import md5
from base64 import b64decode
from html import unescape

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider
from weeb_cli.config import CONFIG_DIR
from weeb_cli.services.logger import debug

try:
    from curl_cffi import requests as curl_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False
    import requests as fallback_requests

try:
    from Crypto.Cipher import AES
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

BASE_URL = "https://turkanime.tv"
KEY_CACHE_FILE = CONFIG_DIR / "turkanime_key.cache"
CSRF_CACHE_FILE = CONFIG_DIR / "turkanime_csrf.cache"

_session = None
_base_url = None
_key_cache = None
_csrf_cache = None

# Supported video players by priority
SUPPORTED_PLAYERS = [
    "YADISK", "MAIL", "ALUCARD(BETA)", "PIXELDRAIN", "AMATERASU(BETA)",
    "HDVID", "ODNOKLASSNIKI", "GDRIVE", "MP4UPLOAD", "DAILYMOTION",
    "SIBNET", "VK", "VIDMOLY", "YOURUPLOAD", "SENDVID", "MYVI", "UQLOAD"
]


def _init_session():
    """Initialize HTTP session with Cloudflare bypass.
    
    Uses curl-cffi with Firefox impersonation for TLS fingerprint spoofing.
    Falls back to regular requests if curl-cffi is not available.
    
    Returns:
        Configured session object.
    """
    global _session, _base_url
    
    if _session is not None:
        return _session
    
    debug("[Turkanime] Initializing session")
    
    if HAS_CURL_CFFI:
        _session = curl_requests.Session(impersonate="firefox", allow_redirects=True)
        debug("[Turkanime] Using curl-cffi with Firefox impersonation")
    else:
        _session = fallback_requests.Session()
        debug("[Turkanime] Warning: curl-cffi not available, using fallback (may fail with Cloudflare)")
    
    _base_url = BASE_URL
    
    # Verify connection and handle redirects
    try:
        res = _session.get(BASE_URL + "/", timeout=30)
        if res.status_code == 200:
            final_url = res.url if hasattr(res, 'url') else BASE_URL
            _base_url = final_url.rstrip('/')
            debug(f"[Turkanime] Base URL set to: {_base_url}")
    except Exception as e:
        debug(f"[Turkanime] Failed to verify connection: {e}")
        _base_url = BASE_URL
    
    return _session


def _fetch(path: str, headers: Dict[str, str] = None, data: Dict = None) -> str:
    """Make HTTP request with proper headers.
    
    Args:
        path: URL path (absolute or relative).
        headers: Additional headers to merge.
        data: POST data (if provided, makes POST request).
    
    Returns:
        Response text content.
    """
    global _base_url
    session = _init_session()
    
    if path is None:
        return ""
    
    if _base_url is None:
        _base_url = BASE_URL
    
    # Build full URL
    if not path.startswith("http"):
        path = path if path.startswith("/") else "/" + path
        url = _base_url + path
    else:
        url = path
    
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    if headers:
        default_headers.update(headers)
    
    try:
        if data:
            debug(f"[Turkanime] POST {url}")
            response = session.post(url, headers=default_headers, data=data, timeout=30)
        else:
            debug(f"[Turkanime] GET {url}")
            response = session.get(url, headers=default_headers, timeout=30)
        return response.text
    except Exception as e:
        debug(f"[Turkanime] Request failed: {e}")
        return ""


def _obtain_key() -> bytes:
    """Extract and cache the AES decryption key.
    
    The key is dynamically embedded in JavaScript files and changes periodically.
    This function reverse engineers the obfuscated code to extract it.
    
    Process:
    1. Fetch /embed/#/url/ and find imported JS files
    2. Find the JS file containing 'decrypt'
    3. Extract obfuscated list and find the longest element (the key)
    
    Returns:
        AES encryption key as bytes, or empty bytes on failure.
    """
    global _key_cache
    
    if _key_cache:
        debug("[Turkanime] Using cached key")
        return _key_cache
    
    # Try to load from cache file
    try:
        if KEY_CACHE_FILE.exists():
            with open(KEY_CACHE_FILE, "r", encoding="utf-8") as f:
                cached = f.read().strip().encode()
                if cached:
                    _key_cache = cached
                    debug("[Turkanime] Loaded key from cache file")
                    return _key_cache
    except Exception as e:
        debug(f"[Turkanime] Failed to load key cache: {e}")
    
    debug("[Turkanime] Extracting fresh key from embed JS")
    
    try:
        embed_html = _fetch("/embed/#/url/")
        js_files = re.findall(r"/embed/js/embeds\..*?\.js", embed_html)
        
        if len(js_files) < 2:
            debug("[Turkanime] Not enough JS files found")
            return b""
        
        js1 = _fetch(js_files[1])
        js1_imports = re.findall("[a-z0-9]{16}", js1)
        
        if not js1_imports:
            debug("[Turkanime] No imports found in first JS")
            return b""
        
        # Find JS file containing 'decrypt'
        j2 = _fetch(f'/embed/js/embeds.{js1_imports[0]}.js')
        if "'decrypt'" not in j2 and len(js1_imports) > 1:
            j2 = _fetch(f'/embed/js/embeds.{js1_imports[1]}.js')
        
        match = re.search(
            r'function a\d_0x[\w]{1,4}\(\)\{var _0x\w{3,8}=\[(.*?)\];', j2
        )
        if not match:
            debug("[Turkanime] Obfuscated list not found")
            return b""
        
        obfuscate_list = match.group(1)
        _key_cache = max(
            obfuscate_list.split("','"),
            key=lambda i: len(re.sub(r"\\x\d\d", "?", i))
        ).encode()
        
        debug(f"[Turkanime] Extracted key: {len(_key_cache)} bytes")
        
        # Save to cache
        if _key_cache:
            try:
                KEY_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(KEY_CACHE_FILE, "w", encoding="utf-8") as f:
                    f.write(_key_cache.decode("utf-8"))
                debug("[Turkanime] Saved key to cache file")
            except Exception as e:
                debug(f"[Turkanime] Failed to save key cache: {e}")
        
        return _key_cache
        
    except Exception as e:
        debug(f"[Turkanime] Key extraction failed: {e}")
        return b""


def _decrypt_cipher(key: bytes, data: bytes) -> str:
    """Decrypt CryptoJS.AES encrypted data (Python implementation).
    
    Implements the same algorithm as CryptoJS.AES.decrypt with:
    - Salted key derivation (OpenSSL compatible)
    - CBC mode decryption
    - PKCS7 padding removal
    
    Args:
        key: AES encryption key.
        data: Base64 encoded encrypted data.
    
    Returns:
        Decrypted plaintext string, or empty string on failure.
    
    References:
        - https://stackoverflow.com/a/36780727
        - https://gist.github.com/ysfchn/e96304fb41375bad0fdf9a5e837da631
    """
    if not HAS_CRYPTO:
        debug("[Turkanime] PyCryptodome not available")
        return ""
    
    def salted_key(data: bytes, salt: bytes, output: int = 48):
        """Generate key and IV from password and salt (OpenSSL compatible)."""
        data += salt
        k = md5(data).digest()
        final_key = k
        while len(final_key) < output:
            k = md5(k + data).digest()
            final_key += k
        return final_key[:output]
    
    def unpad(data: bytes) -> bytes:
        """Remove PKCS7 padding."""
        return data[:-(data[-1] if isinstance(data[-1], int) else ord(data[-1]))]
    
    try:
        b64 = b64decode(data)
        cipher = json.loads(b64)
        cipher_text = b64decode(cipher["ct"])
        iv = bytes.fromhex(cipher["iv"])
        salt = bytes.fromhex(cipher["s"])
        
        crypt = AES.new(salted_key(key, salt, output=32), iv=iv, mode=AES.MODE_CBC)
        return unpad(crypt.decrypt(cipher_text)).decode("utf-8")
    except Exception as e:
        debug(f"[Turkanime] Decryption failed: {e}")
        return ""


def _get_real_url(url_cipher: str) -> str:
    """Decrypt video URL from cipher text.
    
    Args:
        url_cipher: Encrypted URL string.
    
    Returns:
        Decrypted video URL with https: prefix.
    """
    # Try cached key first
    if KEY_CACHE_FILE.exists():
        try:
            with open(KEY_CACHE_FILE, "r", encoding="utf-8") as f:
                cached_key = f.read().strip().encode()
                plaintext = _decrypt_cipher(cached_key, url_cipher.encode())
                if plaintext:
                    debug("[Turkanime] Decrypted URL with cached key")
                    return "https:" + json.loads(plaintext)
        except Exception as e:
            debug(f"[Turkanime] Cached key failed: {e}")
    
    # Get fresh key
    key = _obtain_key()
    if not key:
        debug("[Turkanime] Failed to obtain key")
        return ""
    
    plaintext = _decrypt_cipher(key, url_cipher.encode())
    if not plaintext:
        debug("[Turkanime] Decryption failed")
        return ""
    
    try:
        url = "https:" + json.loads(plaintext)
        debug(f"[Turkanime] Decrypted URL successfully")
        return url
    except Exception as e:
        debug(f"[Turkanime] URL parsing failed: {e}")
        return ""


def _decrypt_jsjiamiv7(ciphertext: str, key: str) -> str:
    """Decrypt jsjiamiv7 obfuscated data.
    
    Implements reverse of jsjiamiv7 obfuscator:
    1. Translate custom base64 alphabet to standard
    2. Base64 decode
    3. RC4 decryption (KSA + PRGA algorithm)
    
    Args:
        ciphertext: Obfuscated ciphertext.
        key: RC4 encryption key.
    
    Returns:
        Decrypted plaintext string.
    
    Reference:
        - https://en.wikipedia.org/wiki/RC4
    """
    _CUSTOM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/"
    _STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    _TRANSLATE = str.maketrans(_CUSTOM, _STD)
    
    # Translate and pad
    t = ciphertext.translate(_TRANSLATE)
    t += "=" * (-len(t) % 4)
    
    try:
        data = b64decode(t).decode("utf-8")
    except Exception as e:
        debug(f"[Turkanime] jsjiamiv7 decode failed: {e}")
        return ""
    
    # RC4 KSA (Key Scheduling Algorithm)
    S = list(range(256))
    j = 0
    klen = len(key)
    
    for i in range(256):
        j = (j + S[i] + ord(key[i % klen])) & 0xff
        S[i], S[j] = S[j], S[i]
    
    # RC4 PRGA (Pseudo-Random Generation Algorithm)
    i = j = 0
    out = []
    for ch in data:
        i = (i + 1) & 0xff
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(ch) ^ S[(S[i] + S[j]) & 0xff]))
    
    return "".join(out)


def _obtain_csrf() -> Optional[str]:
    """Extract and cache CSRF token from player.js.
    
    The CSRF token is encrypted with jsjiamiv7 and embedded in player.js.
    
    Returns:
        CSRF token string, or None on failure.
    """
    global _csrf_cache
    
    if _csrf_cache:
        debug("[Turkanime] Using cached CSRF token")
        return _csrf_cache
    
    # Try to load from cache file
    try:
        if CSRF_CACHE_FILE.exists():
            with open(CSRF_CACHE_FILE, "r", encoding="utf-8") as f:
                cached = f.read().strip()
                if cached:
                    _csrf_cache = cached
                    debug("[Turkanime] Loaded CSRF from cache file")
                    return _csrf_cache
    except Exception as e:
        debug(f"[Turkanime] Failed to load CSRF cache: {e}")
    
    debug("[Turkanime] Extracting fresh CSRF token")
    
    try:
        res = _fetch("/js/player.js")
        
        key_match = re.findall(r"csrf-token':[^\n\)]+'([^']+)'\)", res, re.IGNORECASE)
        candidates = re.findall(r"'([a-zA-Z\d\+\/]{96,156})',", res)
        
        if not key_match or not candidates:
            debug("[Turkanime] CSRF extraction failed: key or candidates not found")
            return None
        
        key = key_match[0]
        
        for ct in candidates:
            decrypted = _decrypt_jsjiamiv7(ct, key)
            if re.search(r"^[a-zA-Z/\+]+$", decrypted):
                _csrf_cache = decrypted
                debug(f"[Turkanime] Extracted CSRF token")
                
                # Save to cache
                try:
                    CSRF_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                    with open(CSRF_CACHE_FILE, "w", encoding="utf-8") as f:
                        f.write(_csrf_cache)
                    debug("[Turkanime] Saved CSRF to cache file")
                except Exception as e:
                    debug(f"[Turkanime] Failed to save CSRF cache: {e}")
                
                return _csrf_cache
        
        debug("[Turkanime] No valid CSRF found in candidates")
        return None
    except Exception as e:
        debug(f"[Turkanime] CSRF extraction failed: {e}")
        return None


def _unmask_real_url(url_mask: str) -> str:
    """Unmask real URL for Turkanime's custom players.
    
    Players like Alucard, Amaterasu, Bankai, HDVID use masked URLs.
    This function uses CSRF token to unmask them.
    
    Args:
        url_mask: Masked URL from Turkanime player.
    
    Returns:
        Real video URL, or original mask if unmask fails.
    """
    if "turkanime" not in url_mask:
        return url_mask
    
    csrf = _obtain_csrf()
    if not csrf:
        debug("[Turkanime] Cannot unmask: CSRF not available")
        return url_mask
    
    try:
        mask = url_mask.split("/player/")[1]
        headers = {"Csrf-Token": csrf, "cf_clearance": "dull"}
        res = _fetch(f"/sources/{mask}/false", headers)
        
        data = json.loads(res)
        url = data["response"]["sources"][-1]["file"]
        
        if url.startswith("//"):
            url = "https:" + url
        
        debug(f"[Turkanime] Unmasked URL successfully")
        return url
    except Exception as e:
        debug(f"[Turkanime] Unmask failed: {e}")
        return url_mask


@register_provider("turkanime", lang="tr", region="TR")
class TurkAnimeProvider(BaseProvider):
    """Turkanime.tv provider implementation.
    
    Supports searching, fetching details, and extracting streams from turkanime.tv.
    Uses curl-cffi with Firefox impersonation for Cloudflare bypass.
    """
    
    def __init__(self):
        super().__init__()
        debug("[Turkanime] Provider initialized")
    
    def search(self, query: str) -> List[AnimeResult]:
        """Search for anime by query.
        
        Uses /arama endpoint with POST request for search.
        Falls back to /ajax/tamliste if search fails.
        
        Args:
            query: Search query string.
        
        Returns:
            List of anime results.
        """
        debug(f"[Turkanime] Searching for: {query}")
        
        # Try search endpoint first
        html = _fetch("/arama", data={"arama": query})
        if html:
            matches = re.findall(r'/anime/([^"\'>]+)["\'] [^>]*?title=["\']([^"]+?) izle', html)
            if matches:
                results = []
                for slug, title in matches[:20]:
                    title_clean = unescape(title)
                    results.append(AnimeResult(
                        id=slug,
                        title=title_clean
                    ))
                debug(f"[Turkanime] Found {len(results)} results via search")
                return results
            
            # Check if redirected to single result
            redirect_match = re.findall('window.location ?= ?"anime/(.*?)"', html)
            if redirect_match:
                slug = redirect_match[0]
                # Fetch title
                anime_html = _fetch(f'/anime/{slug}')
                title_match = re.findall(r'<title>(.*?)</title>', anime_html)
                if title_match:
                    title = title_match[0].split(" izle")[0].strip()
                    debug(f"[Turkanime] Single result redirect to: {slug}")
                    return [AnimeResult(id=slug, title=title)]
        
        # Fallback: filter full anime list
        debug("[Turkanime] Falling back to full list search")
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
        
        debug(f"[Turkanime] Found {len(results)} results via full list")
        return results[:20]
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """Get detailed information for an anime.
        
        Args:
            anime_id: Anime slug.
        
        Returns:
            AnimeDetails object with all information.
        """
        debug(f"[Turkanime] Getting details for: {anime_id}")
        html = _fetch(f'/anime/{anime_id}')
        if not html:
            return None
        
        # Extract title
        title_match = re.findall(r'<title>(.*?)</title>', html)
        title = title_match[0].split(" izle")[0].strip() if title_match else anime_id
        
        # Extract cover image
        img_match = re.findall(r'twitter:image" content="(.*?)"', html)
        cover = img_match[0] if img_match else None
        
        # Extract internal ID for episodes
        anime_id_match = re.findall(r'serilerb/(.*?)\.jpg', html)
        internal_id = anime_id_match[0] if anime_id_match else ""
        
        # Extract description
        description = None
        desc_match = re.search(r'twitter:description"\s+content="([^"]+)"', html)
        if not desc_match:
            desc_match = re.search(r'og:description"\s+content="([^"]+)"', html)
        if desc_match:
            import html as html_module
            description = html_module.unescape(desc_match.group(1)).strip()
        
        # Parse info table
        info = {}
        info_table = re.findall(r'<div id="animedetay">(<table.*?</table>)', html, re.DOTALL)
        if info_table:
            raw_m = re.findall(r"<tr>.*?<b>(.*?)</b>.*?width.*?>(.*?)</td>.*?</tr>", info_table[0], re.DOTALL)
            for key, val in raw_m:
                val = re.sub(r"<[^>]*>", "", val).strip()
                info[key] = val
        
        # Extract genres
        genres = []
        if "Anime Türü" in info:
            genres = [g.strip() for g in info["Anime Türü"].split("  ") if g.strip()]
        
        # Get episodes
        episodes = self._get_episodes_internal(internal_id) if internal_id else []
        
        debug(f"[Turkanime] Found {len(episodes)} episodes")
        
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
        """Get list of episodes for an anime.
        
        Args:
            anime_id: Anime slug.
        
        Returns:
            List of Episode objects.
        """
        debug(f"[Turkanime] Getting episodes for: {anime_id}")
        html = _fetch(f'/anime/{anime_id}')
        if not html:
            return []
        
        anime_id_match = re.findall(r'serilerb/(.*?)\.jpg', html)
        internal_id = anime_id_match[0] if anime_id_match else ""
        
        if not internal_id:
            debug("[Turkanime] Could not find internal ID")
            return []
        
        return self._get_episodes_internal(internal_id)
    
    def _get_episodes_internal(self, internal_id: str) -> List[Episode]:
        """Fetch episodes using internal anime ID.
        
        Args:
            internal_id: Internal anime identifier.
        
        Returns:
            List of Episode objects.
        """
        html = _fetch(f'/ajax/bolumler&animeId={internal_id}')
        if not html:
            return []
        
        matches = re.findall(r'/video/(.*?)\\?".*?title=\\?"(.*?)\\?"', html)
        
        episodes = []
        for i, (slug, title) in enumerate(matches, 1):
            title_clean = re.sub(r'\\["\']', '', title)
            ep_num = self._parse_episode_number(title_clean, i)
            episodes.append(Episode(
                id=slug,
                number=ep_num,
                title=title_clean
            ))
        
        debug(f"[Turkanime] Found {len(episodes)} episodes")
        return episodes
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """Get stream URLs for an episode.
        
        Extracts video URLs from multiple fansubs and players.
        Handles both single fansub and multi-fansub episodes.
        
        Args:
            anime_id: Anime slug.
            episode_id: Episode slug.
        
        Returns:
            List of StreamLink objects.
        """
        debug(f"[Turkanime] Getting streams for episode: {episode_id}")
        html = _fetch(f'/video/{episode_id}')
        if not html:
            return []
        
        streams = []
        
        # Check if single fansub or multiple
        if "birden fazla grup" not in html:
            # Single fansub
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
            
            debug(f"[Turkanime] Found {len(video_matches)} videos for fansub: {fansub}")
            
            for cipher_or_path, player in video_matches:
                stream = self._process_video(cipher_or_path, player, fansub)
                if stream:
                    streams.append(stream)
        else:
            # Multiple fansubs
            fansub_matches = re.findall(r"(ajax/videosec&.*?)'.*?</span> ?(.*?)</a>", html)
            
            debug(f"[Turkanime] Found {len(fansub_matches)} fansubs")
            
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
        
        debug(f"[Turkanime] Total streams found: {len(streams)}")
        return streams
    
    def _process_video(self, cipher_or_path: str, player: str, fansub: str) -> Optional[StreamLink]:
        """Process a video URL (decrypt if needed).
        
        Args:
            cipher_or_path: Either encrypted URL or path to fetch it.
            player: Player name.
            fansub: Fansub name.
        
        Returns:
            StreamLink object, or None if processing fails.
        """
        # Filter unsupported players
        if player.upper() not in SUPPORTED_PLAYERS:
            debug(f"[Turkanime] Unsupported player: {player}")
            return None
        
        # If path, fetch the cipher
        if "/" in cipher_or_path:
            src = _fetch(cipher_or_path)
            cipher_match = re.findall(r'/embed/#/url/(.*?)\?status', src)
            if not cipher_match:
                # Check for direct iframe (some videos are not encrypted)
                tmp = re.findall('<iframe src="(.*?)"', src)
                if tmp:
                    url = tmp[0]
                    if url.startswith("//"):
                        url = "https:" + url
                    debug(f"[Turkanime] Found direct iframe URL: {player}")
                    return StreamLink(
                        url=url,
                        quality="auto",
                        server=f"{fansub} - {player}"
                    )
                debug(f"[Turkanime] No cipher found in path")
                return None
            cipher = cipher_match[0]
        else:
            cipher = cipher_or_path
        
        # Decrypt URL
        url = _get_real_url(cipher)
        if not url:
            debug(f"[Turkanime] Decryption failed for {player}")
            return None
        
        # Fix uqload domain
        url = url.replace("uqload.io", "uqload.com")
        
        # Unmask Turkanime's custom players
        if "turkanime" in url:
            url = _unmask_real_url(url)
            if "turkanime" in url:
                debug(f"[Turkanime] Failed to unmask URL for {player}")
                return None
        
        debug(f"[Turkanime] Successfully processed {player}")
        return StreamLink(
            url=url,
            quality="auto",
            server=f"{fansub} - {player}"
        )
    
    def _parse_episode_number(self, title: str, fallback: int) -> int:
        """Extract episode number from title.
        
        Args:
            title: Episode title.
            fallback: Fallback episode number.
        
        Returns:
            Extracted or fallback episode number.
        """
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
