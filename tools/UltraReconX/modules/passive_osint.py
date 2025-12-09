# passive_osint.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.I)
SOCIAL_PATTERNS = ["facebook.com","twitter.com","linkedin.com","github.com","youtube.com","instagram.com"]

def fetch(url, timeout=8):
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent":"UltraReconX/1.0"})
        return r.text
    except:
        return ""

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("javascript:") or href.startswith("#"):
            continue
        full = urljoin(base_url, href)
        links.add(full)
    return links

def passive_osint(domain, page_limit=60):
    base = "http://" + domain
    visited = set()
    to_visit = {base}
    pages = []
    emails = set()
    socials = set()

    while to_visit and len(visited) < page_limit:
        url = to_visit.pop()
        visited.add(url)
        html = fetch(url)
        if not html:
            continue
        pages.append({"url":url, "content": html[:2000]})
        # emails
        for m in EMAIL_REGEX.findall(html):
            emails.add(m)
        # socials
        for sp in SOCIAL_PATTERNS:
            if sp in html:
                socials.add(sp)
        # links
        for link in extract_links(html, url):
            if link not in visited and link.startswith("http"):
                to_visit.add(link)

    return pages, sorted(emails), sorted(socials)
