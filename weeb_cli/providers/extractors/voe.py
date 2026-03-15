import base64, json, re, requests
from typing import Optional
from weeb_cli.services.logger import debug

def rot13(s):
    res = ""
    for c in s:
        if 'a' <= c <= 'z': res += chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
        elif 'A' <= c <= 'Z': res += chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
        else: res += c
    return res

def caesar_shift(s, shift): return "".join(chr(ord(c) + shift) for c in s)

def deobfuscate(encoded):
    res = rot13(encoded)
    for sep in ['@$', '^^', '~@', '%?', '*~', '!!', '#&']: res = res.replace(sep, '')
    res = base64.b64decode(res).decode('utf-8')
    res = caesar_shift(res, -3)[::-1]
    return json.loads(base64.b64decode(res).decode('utf-8'))

def extract_voe(url):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://aniworld.to/"}
    try:
        s = requests.Session()
        html = s.get(url, headers=headers, timeout=10, allow_redirects=True).text
        m = re.search(r"window\.location\.href\s*=\s*'([^']+)'", html)
        if m: html = s.get(m.group(1), headers=headers, timeout=10).text
        js = re.search(r'<script\s+type="application/json"[^>]*>([\s\S]*?)</script>', html)
        if not js: return None
        data = deobfuscate(js.group(1).strip())
        val = data.get("file") or data.get("source")
        if not val and data.get("fallback_mp4"):
            f = data.get("fallback_mp4")
            val = f[0] if isinstance(f, list) else f
        return val
    except Exception as e:
        debug(f"[VOE] Error: {e}"); return None
