import requests
import re

TECH_SIGNATURES = {
    "WordPress": ["wp-content", "wp-json"],
    "Cloudflare": ["cf-ray", "__cfduid"],
    "Laravel": ["laravel_session"],
    "Django": ["csrftoken"],
    "React": ["react", "jsx"],
    "Vue.js": ["vue", "v-cloak"],
    "Bootstrap": ["bootstrap.min.css"],
    "jQuery": ["jquery.min.js"],
}

def fingerprint_tech(url):
    try:
        r = requests.get(url, timeout=5)
        body = r.text.lower()
        headers = str(r.headers).lower()

        found = []

        for tech, patterns in TECH_SIGNATURES.items():
            for p in patterns:
                if p.lower() in body or p.lower() in headers:
                    found.append(tech)
                    break

        return found
    except:
        return []
