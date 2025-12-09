import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited = set()

def crawl(url, limit=100):
    if url in visited or len(visited) > limit:
        return []

    visited.add(url)

    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []

        for a in soup.find_all("a", href=True):
            full = urljoin(url, a["href"])
            if full.startswith("http"):
                links.append(full)
                crawl(full)

        return list(visited)

    except:
        return list(visited)
