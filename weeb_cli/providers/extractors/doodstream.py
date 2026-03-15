import re, requests, time, random, string
def extract_doodstream(url):
    try:
        h = {"User-Agent": "Mozilla/5.0", "Referer": "https://aniworld.to/"}
        html = requests.get(url, headers=h, timeout=10).text
        m = re.search(r"\$.get\('(/pass_md5/[^']+)'", html)
        if not m: return None
        purl = f"https://dood.so{m.group(1)}"
        base = requests.get(purl, headers={"Referer": url, "User-Agent": h["User-Agent"]}, timeout=10).text
        tok = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        return f"{base}{tok}?token={purl.split('/')[-1]}&expiry={int(time.time() * 1000)}"
    except: return None
