# modules/paste_scanner.py
# best-effort paste sites scanner (Pastebin / Ghostbin pattern)
import requests
from bs4 import BeautifulSoup

PASTEBIN_ARCHIVE = "https://pastebin.com/archive"

def search_pastes(target, max_pages=1):
    results = []
    try:
        r = requests.get(PASTEBIN_ARCHIVE, timeout=10, headers={"User-Agent":"LeakHunterX/1.0"})
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select("table.maintable tr td a"):
            href = a.get("href")
            if not href: continue
            url = "https://pastebin.com" + href
            try:
                rr = requests.get(url, timeout=8, headers={"User-Agent":"LeakHunterX/1.0"})
                if rr.status_code == 200 and target.lower() in rr.text.lower():
                    snippet = rr.text[:800].replace("\n"," ")
                    results.append({"url": url, "snippet": snippet})
            except:
                continue
    except Exception:
        pass
    return results
