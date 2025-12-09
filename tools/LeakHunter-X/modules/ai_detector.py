# modules/ai_detector.py
# Rules-based heuristic that inspects findings and highlights suspicious ones
import re

KEY_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),   # AWS access key id
    re.compile(r"AIza[0-9A-Za-z\-_]{35}"), # Google API key
    re.compile(r"ssh-rsa|-----BEGIN RSA PRIVATE KEY-----"),
    re.compile(r"api[_-]?key", re.I),
    re.compile(r"secret", re.I),
    re.compile(r"private[_-]?key", re.I)
]

def _scan_text_for_keys(text):
    findings = []
    for p in KEY_PATTERNS:
        for m in p.findall(text or ""):
            findings.append(m)
    return findings

def analyze(out):
    summary = {"high_risk": [], "medium_risk": [], "notes": []}
    # Scan GitHub results by requesting html (best-effort small)
    import requests, time
    for gh in out.get("results", {}).get("github_leaks", []):
        url = gh.get("html_url")
        if not url: continue
        try:
            r = requests.get(url, timeout=8, headers={"User-Agent":"LeakHunterX/1.0"})
            if r.status_code == 200:
                keys = _scan_text_for_keys(r.text)
                if keys:
                    summary["high_risk"].append({"source": url, "keys": keys})
        except:
            continue
        time.sleep(0.3)
    # Pastes quick scan
    for p in out.get("results", {}).get("pastes", []):
        txt = p.get("snippet","")
        keys = _scan_text_for_keys(txt)
        if keys:
            summary["medium_risk"].append({"source": p.get("url"), "keys": keys})
    # Buckets presence is high interest
    if out.get("results", {}).get("buckets"):
        summary["notes"].append("Public buckets detected — review contents manually (read-only).")
    return summary
