import re, requests
def extract_streamtape(url):
    try:
        h = {"User-Agent": "Mozilla/5.0", "Referer": "https://aniworld.to/"}
        html = requests.get(url, headers=h, timeout=10).text
        m = re.search(r"document\.getElementById\('robotlink'\)\.innerHTML\s*=\s*'([^']+)'\s*\+\s*'([^']+)'", html)
        return f"https:{m.group(1)}{m.group(2)}" if m else None
    except: return None
