#!/usr/bin/env python3
# scanners/ai_tech_guess.py
# Advanced AI-like heuristic module for tech detection
# Fixes previous bug: now accepts headers as dict and html as text
# Returns list of detections: {"name","confidence","evidence","source"}

import re
from urllib.parse import urlparse

# Small heuristic DB — extendable
HEURISTICS = {
    "WordPress": {
        "html_tokens": ["wp-content", "wp-includes", "/wp-json", "wp-emoji"],
        "headers": ["x-pingback", "x-powered-by:WordPress"],
        "confidence": 0.85
    },
    "Joomla": {
        "html_tokens": ["Joomla!", "/administrator/"],
        "confidence": 0.7
    },
    "Drupal": {
        "html_tokens": ["Drupal.settings", "/sites/default"],
        "confidence": 0.75
    },
    "nginx": {
        "headers": ["server:nginx"],
        "confidence": 0.8
    },
    "Apache": {
        "headers": ["server:apache"],
        "confidence": 0.75
    },
    "Cloudflare": {
        "headers": ["cf-ray", "cf-cache-status", "server:cloudflare"],
        "confidence": 0.92
    },
    "React": {
        "html_tokens": ["data-reactroot", "react-dom", "react/js"],
        "js_tokens": ["react"],
        "confidence": 0.75
    },
    "Vue.js": {
        "html_tokens": ["__vue__", "vue.runtime"],
        "js_tokens": ["vue"],
        "confidence": 0.75
    },
    "Angular": {
        "html_tokens": ["ng-app", "angular.js"],
        "js_tokens": ["angular"],
        "confidence": 0.7
    },
    "jQuery": {
        "html_tokens": ["jquery", "jQuery"],
        "js_tokens": ["jquery"],
        "confidence": 0.6
    }
}

# additional patterns
API_PATTERNS = [
    re.compile(r"fetch\(\s*['\"](https?://[^'\"\)]+)['\"]", re.IGNORECASE),
    re.compile(r"axios\.(get|post)\(\s*['\"](https?://[^'\"\)]+)['\"]", re.IGNORECASE),
    re.compile(r"new XMLHttpRequest\(\)", re.IGNORECASE),
    re.compile(r"\/api\/[a-zA-Z0-9_\-\/]*", re.IGNORECASE)
]


def _norm_headers(headers):
    """Return list of 'k:v' lowercased strings for matching"""
    if not headers:
        return []
    out = []
    try:
        for k, v in headers.items():
            out.append(f"{k.lower()}:{str(v).lower()}")
    except Exception:
        # headers might be a string
        s = str(headers).lower()
        out.append(s)
    return out


def ai_guess(html_text, headers):
    """
    html_text: string (page HTML)
    headers: dict-like from HTTP response.headers
    Returns: list of dicts: {name, confidence, evidence, source}
    """
    results = []
    html = (html_text or "").lower()
    hdrs = _norm_headers(headers)

    # 1) Header-based heuristics
    hdr_join = " ".join(hdrs)
    for name, rules in HEURISTICS.items():
        # headers match
        matched = False
        if "headers" in rules:
            for pat in rules["headers"]:
                if pat.lower() in hdr_join:
                    results.append({
                        "name": name,
                        "confidence": rules.get("confidence", 0.6),
                        "evidence": f"header:{pat}",
                        "source": "headers"
                    })
                    matched = True
                    break
        if matched:
            continue

        # html tokens match
        for tok in rules.get("html_tokens", []):
            if tok.lower() in html:
                results.append({
                    "name": name,
                    "confidence": rules.get("confidence", 0.6),
                    "evidence": f"html:{tok}",
                    "source": "html"
                })
                matched = True
                break
        if matched:
            continue

        # js token quick check
        for jtok in rules.get("js_tokens", []):
            if jtok.lower() in html:
                results.append({
                    "name": name,
                    "confidence": rules.get("confidence", 0.5),
                    "evidence": f"js_token:{jtok}",
                    "source": "js"
                })
                matched = True
                break

    # 2) API endpoint heuristics (detect likely API endpoints in HTML/inline scripts)
    apis = set()
    for pat in API_PATTERNS:
        for m in pat.findall(html):
            # m might be tuple due to groups — flatten
            if isinstance(m, tuple):
                for sub in m:
                    if isinstance(sub, str) and sub.startswith("http"):
                        apis.add(sub)
            elif isinstance(m, str):
                apis.add(m)
    if apis:
        results.append({
            "name": "API Endpoints",
            "confidence": 0.65,
            "evidence": ", ".join(list(apis)[:6]),
            "source": "content"
        })

    # 3) Cookie / fingerprint heuristics (CF, session cookies etc)
    for h in hdrs:
        if "set-cookie" in h and ("__cfduid" in h or "cf_bm" in h or "cf_clearance" in h):
            results.append({
                "name": "Cloudflare (cookie)",
                "confidence": 0.9,
                "evidence": "set-cookie: cf cookie",
                "source": "headers"
            })
            break

    # 4) Server header parsing
    for h in hdrs:
        if h.startswith("server:"):
            srv = h.split(":",1)[1].strip()
            if srv:
                results.append({
                    "name": f"Server: {srv}",
                    "confidence": 0.4,
                    "evidence": f"server header: {srv}",
                    "source": "headers"
                })

    # Aggregate results: keep highest confidence per name
    agg = {}
    for r in results:
        key = r["name"]
        if key not in agg or r["confidence"] > agg[key]["confidence"]:
            agg[key] = r

    out = sorted(agg.values(), key=lambda x: x["confidence"], reverse=True)
    return out
