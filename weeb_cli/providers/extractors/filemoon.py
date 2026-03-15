import re, requests
from weeb_cli.services.logger import debug

def decode_packer(p, r, c, d):
    def replace(m):
        try:
            idx = int(m.group(0), r)
            return d[idx] if idx < len(d) and d[idx] else m.group(0)
        except: return m.group(0)
    return re.compile(r'\b[0-9a-zA-Z]+\b').sub(replace, p)

def extract_filemoon(url):
    h = {"User-Agent": "Mozilla/5.0", "Referer": "https://aniworld.to/"}
    try:
        s = requests.Session()
        html = s.get(url, headers=h, timeout=10).text
        ifm = re.search(r'<iframe[^>]*src="([^"]+)"', html)
        if not ifm: return None
        iurl = ifm.group(1)
        if iurl.startswith('//'): iurl = 'https:' + iurl
        ihtml = s.get(iurl, headers={"User-Agent": h["User-Agent"], "Referer": "https://filemoon.to/"}, timeout=10).text
        ev = re.search(r"eval\(function\(p,a,c,k,e,d\){[\s\S]+?}\('([\s\S]+?)',(\d+),(\d+),'([\s\S]+?)'\.split\('\|'\)\)\)", ihtml)
        if not ev: return None
        p, r, c, d = ev.groups()
        un = decode_packer(p, int(r), int(c), d.split('|'))
        m3 = re.search(r'file:"([^"]+\.m3u8[^"]*)"', un)
        if m3: return m3.group(1)
        sm = re.search(r'sources:\[{file:"([^"]+)"', un)
        return sm.group(1) if sm else None
    except Exception as e:
        debug(f"[Filemoon] Error: {e}"); return None
