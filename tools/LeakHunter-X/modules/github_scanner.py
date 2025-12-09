# modules/github_scanner.py
import requests, re, os
from urllib.parse import quote_plus

# Basic public GitHub code search (best-effort)
# For heavy usage set GITHUB_TOKEN env var and use 'Authorization' header
GITHUB_API = "https://api.github.com/search/code?q={q}&per_page=50"

def _gh_headers():
    headers = {"User-Agent":"LeakHunterX/1.0"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def search_github(target):
    items = []
    # Search for likely leaked tokens / keys patterns that mention the domain/org
    queries = [
        f"{target}+extension:env",
        f"{target}+aws_access_key_id",
        f"{target}+api_key",
        f"{target}+secret_key",
        f"{target}+private_key",
        f"{target}+config",
    ]
    for q in queries:
        url = GITHUB_API.format(q=quote_plus(q))
        try:
            r = requests.get(url, headers=_gh_headers(), timeout=12)
            if r.status_code == 200:
                data = r.json()
                for it in data.get("items", []):
                    items.append({
                        "name": it.get("name"),
                        "path": it.get("path"),
                        "repo": it.get("repository", {}).get("full_name"),
                        "html_url": it.get("html_url")
                    })
        except Exception:
            continue
    # dedupe by html_url
    seen = set(); uniq = []
    for i in items:
        u = i.get("html_url")
        if u and u not in seen:
            uniq.append(i); seen.add(u)
    return uniq
