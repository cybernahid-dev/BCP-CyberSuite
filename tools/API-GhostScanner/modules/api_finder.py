# api_finder.py — heuristic extraction of API-like URLs from arbitrary text
import re
from urllib.parse import urljoin, urlparse

URL_RE = re.compile(r'https?://[A-Za-z0-9\-\._~:/\?#\[\]@!\$&\'\(\)\*\+,;=%]+')
REL_RE = re.compile(r'["\'](/api/[^"\'\s]+)["\']', re.IGNORECASE)
GRAPHQL_RE = re.compile(r'["\'](/graphql)["\']', re.IGNORECASE)

def find_apis_in_text(text, base=None):
    found = set()
    if not text:
        return []
    # absolute URLs first
    for u in URL_RE.findall(text):
        u = u.strip(" '\"")
        # simple heuristics: include ones that look like API endpoints
        if any(token in u.lower() for token in ["/api/", "/graphql", "/v1/", "/v2/", "/oauth", "/auth/"]):
            found.add(u)
    # relative api paths
    for r in REL_RE.findall(text):
        if base:
            found.add(urljoin(base, r))
        else:
            found.add(r)
    for g in GRAPHQL_RE.findall(text):
        if base:
            found.add(urljoin(base, g))
        else:
            found.add(g)
    return list(found)

def canonicalize_url(u):
    # if domain provided without scheme, return domain only
    if u.startswith("http://") or u.startswith("https://"):
        parsed = urlparse(u)
        return parsed.netloc
    return u.strip().rstrip("/")
