import re
import json
import time
import urllib.request
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    import base64
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

HIANIME_BASE = "https://hianime.to"
KEY_URL = "https://raw.githubusercontent.com/ryanwtf88/megacloud-keys/refs/heads/master/key.txt"
MEGAPLAY_URL = "https://megaplay.buzz/stream/s-2/"
VIDWISH_URL = "https://vidwish.live/stream/s-2/"
REFERER = "https://megacloud.tv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

_cached_key = None
_key_fetched_at = 0
KEY_CACHE_DURATION = 3600


def _http_get(url: str, headers: dict = None, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers=headers or HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _get_json(url: str, headers: dict = None) -> Optional[dict]:
    try:
        data = _http_get(url, headers)
        return json.loads(data)
    except Exception:
        return None


def _get_html(url: str, headers: dict = None) -> str:
    try:
        data = _http_get(url, headers)
        return data.decode('utf-8')
    except Exception:
        return ""


def _get_decryption_key() -> Optional[str]:
    global _cached_key, _key_fetched_at
    
    now = time.time()
    if _cached_key and (now - _key_fetched_at) < KEY_CACHE_DURATION:
        return _cached_key
    
    try:
        data = _http_get(KEY_URL)
        _cached_key = data.decode('utf-8').strip()
        _key_fetched_at = now
        return _cached_key
    except Exception:
        return _cached_key


def _decrypt_aes(encrypted: str, key: str) -> Optional[List[dict]]:
    if not HAS_CRYPTO:
        return None
    
    try:
        key_bytes = key.encode('utf-8')
        encrypted_bytes = base64.b64decode(encrypted)
        
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return json.loads(decrypted.decode('utf-8'))
    except Exception:
        pass
    
    try:
        key_bytes = bytes.fromhex(key)
        encrypted_bytes = base64.b64decode(encrypted)
        
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return json.loads(decrypted.decode('utf-8'))
    except Exception:
        return None


def _extract_token(url: str) -> Optional[str]:
    html = _get_html(url, {
        **HEADERS,
        "Referer": f"{HIANIME_BASE}/"
    })
    
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    meta = soup.select_one('meta[name="_gg_fb"]')
    if meta and meta.get('content'):
        return meta['content']
    
    data_dpi = soup.select_one('[data-dpi]')
    if data_dpi and data_dpi.get('data-dpi'):
        return data_dpi['data-dpi']
    
    for script in soup.select('script[nonce]'):
        nonce = script.get('nonce')
        if nonce and len(nonce) >= 10:
            return nonce
    
    patterns = [
        r'window\.\w+\s*=\s*["\']([a-zA-Z0-9_-]{10,})["\']',
        r'data-k\s*=\s*["\']([a-zA-Z0-9_-]{10,})["\']',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    
    return None


def _get_fallback_source(ep_id: str, server_type: str, server_name: str) -> Optional[dict]:
    providers = [
        ("megaplay", MEGAPLAY_URL),
        ("vidwish", VIDWISH_URL)
    ]
    
    if server_name.lower() == "hd-2":
        providers = providers[::-1]
    
    for name, base_url in providers:
        try:
            url = f"{base_url}{ep_id}/{server_type}"
            html = _get_html(url, {
                **HEADERS,
                "Referer": f"https://{name}.{'buzz' if name == 'megaplay' else 'live'}/"
            })
            
            if not html:
                continue
            
            match = re.search(r'data-id=["\'](\d+)["\']', html)
            if not match:
                continue
            
            real_id = match.group(1)
            domain = "megaplay.buzz" if name == "megaplay" else "vidwish.live"
            sources_url = f"https://{domain}/stream/getSources?id={real_id}"
            
            data = _get_json(sources_url, {
                **HEADERS,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://{domain}/"
            })
            
            if data and data.get('sources', {}).get('file'):
                return {
                    "file": data['sources']['file'],
                    "tracks": data.get('tracks', []),
                    "server": name
                }
        except Exception:
            continue
    
    return None


def extract_stream(server_id: int, episode_id: str, server_type: str = "sub", server_name: str = "hd-1") -> Optional[dict]:
    ep_id = episode_id.split('ep=')[-1] if 'ep=' in episode_id else episode_id.split('::')[-1]
    
    sources_url = f"{HIANIME_BASE}/ajax/v2/episode/sources?id={server_id}"
    ajax_data = _get_json(sources_url, {**HEADERS, "Referer": HIANIME_BASE})
    
    if not ajax_data or 'link' not in ajax_data:
        return _get_fallback_source(ep_id, server_type, server_name)
    
    embed_link = ajax_data['link']
    
    match = re.search(r'/([^/?]+)\?', embed_link)
    source_id = match.group(1) if match else None
    
    match = re.search(r'^(https?://[^/]+(?:/[^/]+){3})', embed_link)
    base_url = match.group(1) if match else None
    
    if not source_id or not base_url:
        return _get_fallback_source(ep_id, server_type, server_name)
    
    token_url = f"{base_url}/{source_id}?k=1&autoPlay=0&oa=0&asi=1"
    token = _extract_token(token_url)
    
    if not token:
        return _get_fallback_source(ep_id, server_type, server_name)
    
    get_sources_url = f"{base_url}/getSources?id={source_id}&_k={token}"
    sources_data = _get_json(get_sources_url, {
        **HEADERS,
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"{base_url}/{source_id}"
    })
    
    if not sources_data:
        return _get_fallback_source(ep_id, server_type, server_name)
    
    encrypted = sources_data.get('sources')
    
    if isinstance(encrypted, list) and encrypted:
        return {
            "file": encrypted[0].get('file'),
            "tracks": sources_data.get('tracks', []),
            "intro": sources_data.get('intro'),
            "outro": sources_data.get('outro'),
            "server": server_name
        }
    
    if isinstance(encrypted, str):
        key = _get_decryption_key()
        if key:
            decrypted = _decrypt_aes(encrypted, key)
            if decrypted and decrypted[0].get('file'):
                return {
                    "file": decrypted[0]['file'],
                    "tracks": sources_data.get('tracks', []),
                    "intro": sources_data.get('intro'),
                    "outro": sources_data.get('outro'),
                    "server": server_name
                }
    
    return _get_fallback_source(ep_id, server_type, server_name)
