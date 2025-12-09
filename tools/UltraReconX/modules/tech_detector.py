#!/usr/bin/env python3
# tech_detector.py
# UltraReconX — Technology Fingerprinting Module (high-quality starter)
# Developed by: cybernahid-dev | Team: Bangladesh Cyber Panthers

import re
import requests
import hashlib
from urllib.parse import urljoin

# ------- Tiny signature DB (extend as needed) -------
SIGNATURES = {
    "WordPress": {
        "headers": ["x-powered-by:WordPress", "set-cookie:wordpress_"],
        "html": ["wp-content", "/wp-json", "wp-emoji"],
        "js": ["wp-"],
        "confidence": 0.8
    },
    "Joomla": {
        "html": ["Joomla!", "/administrator/"],
        "js": [],
        "confidence": 0.7
    },
    "Drupal": {
        "html": ["Drupal.settings", "/user/login"],
        "js": [],
        "confidence": 0.75
    },
    "Magento": {
        "html": ["Mage.Cookies", "/skin/frontend"],
        "js": [],
        "confidence": 0.7
    },
    "Shopify": {
        "html": ["cdn.shopify.com", "shopify-section"],
        "js": [],
        "confidence": 0.8
    },
    "Cloudflare": {
        "headers": ["server:cloudflare", "cf-ray", "cf-cache-status"],
        "html": [],
        "confidence": 0.9
    },
    "nginx": {
        "headers": ["server:nginx"],
        "html": [],
        "confidence": 0.8
    },
    "Apache": {
        "headers": ["server:apache"],
        "html": [],
        "confidence": 0.75
    },
    "React": {
        "html": ["data-reactroot", "react-dom"],
        "js": ["react"],
        "confidence": 0.75
    },
    "Angular": {
        "html": ["ng-app", "angular.js"],
        "js": ["angular"],
        "confidence": 0.75
    },
    "Vue.js": {
        "html": ["__vue__", "vue"],
        "js": ["vue"],
        "confidence": 0.75
    },
    "jQuery": {
        "html": ["jquery", "jQuery"],
        "js": ["jquery"],
        "confidence": 0.7
    },
    "Bootstrap": {
        "html": ["bootstrap.min.css", "bootstrapcdn"],
        "js": ["bootstrap"],
        "confidence": 0.7
    },
    "Google Analytics": {
        "html": ["google-analytics", "gtag('config'", "ga('create'"],
        "js": ["gtag", "analytics.js"],
        "confidence": 0.7
    }
}

# some common CDN / hosting hints
CDN_HINTS = {
    "Cloudflare": ["cloudflare", "cdn-cgi", "cf-cache-status"],
    "Fastly": ["fastly"],
    "Akamai": ["akamaiedge", "akamai"],
    "Amazon CloudFront": ["cloudfront", "amazonaws.com"]
}

# quick user-agent like header we can add for fetching favicon
DEFAULT_UA = "BCP-LeakHunter/1.0 (+https://github.com/cybernahid-dev)"

# --------- helpers ----------
def _norm_headers(headers):
    return {k.lower(): v for k, v in (headers or {}).items()}

def _check_signatures_from_headers(norm_headers):
    found = []
    s_text = " ".join([f"{k}:{v}" for k,v in norm_headers.items()])
    for name, sig in SIGNATURES.items():
        for h in sig.get("headers", []):
            if h.lower() in s_text:
                found.append((name, sig.get("confidence", 0.5), f"header:{h}"))
                break
    return found

def _check_signatures_from_html(html_text):
    found = []
    txt = (html_text or "").lower()
    for name, sig in SIGNATURES.items():
        score = 0.0
        reasons = []
        for token in sig.get("html", []):
            if token.lower() in txt:
                score = max(score, sig.get("confidence", 0.5))
                reasons.append(f"html:{token}")
        # js tokens in HTML (script src etc)
        for jtok in sig.get("js", []):
            if jtok.lower() in txt:
                score = max(score, sig.get("confidence", 0.4))
                reasons.append(f"js_token:{jtok}")
        if reasons:
            found.append((name, score, ", ".join(reasons)))
    return found

def _extract_js_srcs(html, base_url):
    # simple regex to catch script srcs
    js_links = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html or "", re.IGNORECASE)
    cleaned = []
    for l in js_links:
        if l.startswith("//"):
            cleaned.append("https:" + l)
        elif l.startswith("http"):
            cleaned.append(l)
        else:
            cleaned.append(urljoin(base_url, l))
    return list(dict.fromkeys(cleaned))

def _favicon_hash(domain, scheme="https"):
    """Try fetch /favicon.ico and return md5 hex or None."""
    try:
        url = f"{scheme}://{domain.rstrip('/')}/favicon.ico"
        r = requests.get(url, timeout=6, headers={"User-Agent": DEFAULT_UA}, allow_redirects=True, verify=False)
        if r.status_code == 200 and r.content:
            h = hashlib.md5(r.content).hexdigest()
            return h
    except Exception:
        pass
    return None

def _cdn_and_hosting_checks(norm_headers, html_text):
    found = []
    s = " ".join([k + ":" + v for k,v in norm_headers.items()]) + " " + (html_text or "")
    for name, tokens in CDN_HINTS.items():
        for t in tokens:
            if t.lower() in s.lower():
                found.append((name, f"hint:{t}"))
                break
    # quick hosting hint from Server header
    server = norm_headers.get("server","")
    if server:
        if "google" in server.lower() or "gws" in server.lower():
            found.append(("Google Hosting", f"server:{server}"))
    return found

# --------- main function ----------
def detect_technologies(html, headers, domain=None, prefer_https=True):
    """
    Detect technologies from http headers + html + domain.
    Returns structured list of detections:
    [
      {
        "name": "WordPress",
        "confidence": 0.8,
        "evidence": "html:wp-content"
      },
      ...
    ]
    """
    out = []
    norm_headers = _norm_headers(headers or {})

    # 1) Headers-based
    for name, conf, reason in _check_signatures_from_headers(norm_headers):
        out.append({"name": name, "confidence": conf, "evidence": reason, "source": "headers"})

    # 2) HTML-based
    for name, conf, reason in _check_signatures_from_html(html):
        out.append({"name": name, "confidence": conf, "evidence": reason, "source": "html"})

    # 3) JS src analysis (script src tokens)
    js_srcs = _extract_js_srcs(html, (("https://" if prefer_https else "http://") + (domain or "")))
    # quick scans for known cdn patterns
    for js in js_srcs:
        low = js.lower()
        for name, sig in SIGNATURES.items():
            for jtok in sig.get("js", []):
                if jtok.lower() in low:
                    out.append({"name": name, "confidence": sig.get("confidence",0.5), "evidence": f"script_src:{jtok}", "source": "js_src"})
                    break

    # 4) CDN / hosting heuristics
    cdnhits = _cdn_and_hosting_checks(norm_headers, html)
    for (name, reason) in cdnhits:
        out.append({"name": name, "confidence": 0.7, "evidence": reason, "source": "cdn_hint"})

    # 5) Server header raw
    server_header = norm_headers.get("server")
    if server_header:
        if "nginx" in server_header.lower():
            out.append({"name":"nginx","confidence":0.8,"evidence":f"server:{server_header}","source":"headers"})
        if "apache" in server_header.lower():
            out.append({"name":"Apache","confidence":0.75,"evidence":f"server:{server_header}","source":"headers"})

    # 6) x-powered-by
    xpb = norm_headers.get("x-powered-by","")
    if xpb:
        out.append({"name": xpb.strip(), "confidence": 0.5, "evidence": f"x-powered-by:{xpb}", "source":"headers"})

    # 7) favicon fingerprint (best-effort)
    favicon_md5 = None
    try:
        favicon_md5 = _favicon_hash(domain or "", "https" if prefer_https else "http")
    except Exception:
        favicon_md5 = None
    if favicon_md5:
        out.append({"name":"favicon-md5", "confidence":0.4, "evidence":favicon_md5, "source":"favicon"})

    # normalize & aggregate: keep highest confidence per tech
    agg = {}
    for d in out:
        key = d["name"]
        if key not in agg or d["confidence"] > agg[key]["confidence"]:
            agg[key] = d

    # produce sorted list by confidence desc
    results = sorted(list(agg.values()), key=lambda x: x["confidence"], reverse=True)
    return results
