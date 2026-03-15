import re, requests
def extract_vidoza(url):
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        m = re.search(r'<source\s+src="([^"]+\.mp4)"', html)
        return m.group(1) if m else None
    except: return None
