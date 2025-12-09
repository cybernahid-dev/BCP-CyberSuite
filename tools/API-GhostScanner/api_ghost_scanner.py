#!/usr/bin/env python3
# api_ghost_scanner.py
# API-GhostScanner — Passive API discovery & security surface analyzer
# Dev: cybernahid-dev | Team: Bangladesh Cyber Panthers
# NOTE: Passive only. Always have permission to scan.

import os
import argparse
import time
import json
from modules.requester import safe_get, safe_head, is_local_target
from modules.js_parser import extract_js_urls, extract_patterns_from_js
from modules.api_finder import find_apis_in_text, canonicalize_url
from modules.cors_checker import check_cors
from modules.swagger_detector import probe_swagger_endpoints
from modules.analyzer import analyze_findings
from modules.reporter import save_json_report, save_html_report, print_summary

CONSENT_FILE = "/tmp/bcp_api_ghost_consent.txt"

POLITE_DELAY = 0.35  # seconds between external fetches

def require_consent(target):
    # Safe allow local targets automatically
    if is_local_target(target):
        return True
    if os.path.exists(CONSENT_FILE):
        # optional further verification: ensure target listed in file?
        return True
    # interactive prompt
    print("\n[!] Consent required for scanning non-local targets.")
    print("    You must have explicit permission to scan this target.")
    ans = input(f"Type the full target domain ({target}) to confirm and continue: ").strip()
    if ans == target:
        # create a short-lived consent file for convenience
        with open(CONSENT_FILE, "w") as fh:
            fh.write(f"User confirmed scanning {target} on {time.asctime()}\n")
        return True
    print("Consent not provided. Exiting.")
    return False

def main():
    p = argparse.ArgumentParser(description="API-GhostScanner — passive API discovery")
    p.add_argument("--target", "-t", help="domain or url to scan (example.com)", required=False)
    p.add_argument("--once", action="store_true", help="run a single pass and exit")
    p.add_argument("--delay", type=float, default=POLITE_DELAY, help="polite delay between fetches")
    args = p.parse_args()

    target = args.target
    if not target:
        target = input("[?] Enter target domain or host (example.com): ").strip()
    if not target:
        print("No target provided. Exiting."); return

    # canonicalize
    target = canonicalize_url(target)

    if not require_consent(target):
        return

    results = {
        "target": target,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "discovered_apis": [],
        "js_files": [],
        "js_patterns": [],
        "swagger": [],
        "cors": [],
        "notes": []
    }

    base_urls = [f"https://{target}", f"http://{target}"]

    # 1) Fetch homepage(s) headers and body to seed extraction
    visited_pages = []
    for base in base_urls:
        try:
            r = safe_get(base)
            if r and r.status_code == 200:
                body = r.text
                visited_pages.append({"url": base, "status": r.status_code, "text_snippet": body[:3000]})
                # extract possible API URLs from page HTML
                apis = find_apis_in_text(body, base)
                for a in apis:
                    if a not in results["discovered_apis"]:
                        results["discovered_apis"].append(a)
                # extract JS file URLs
                js_urls = extract_js_urls(body, base)
                for j in js_urls:
                    if j not in results["js_files"]:
                        results["js_files"].append(j)
        except Exception as e:
            results["notes"].append(f"homepage fetch error for {base}: {e}")
        time.sleep(args.delay)

    # 2) Fetch and analyze JS files (safe limited)
    for js in list(results["js_files"]):
        try:
            r = safe_get(js)
            if not r:
                results["notes"].append(f"Could not fetch JS: {js}")
                continue
            text = r.text
            patterns = extract_patterns_from_js(text)
            for ptn in patterns:
                if ptn not in results["js_patterns"]:
                    results["js_patterns"].append(ptn)
                # extract api-like urls inside JS text
                inner = find_apis_in_text(text, js)
                for a in inner:
                    if a not in results["discovered_apis"]:
                        results["discovered_apis"].append(a)
        except Exception as e:
            results["notes"].append(f"js fetch error {js}: {e}")
        time.sleep(args.delay)

    # 3) Swagger / OpenAPI probe
    swagger_hits = probe_swagger_endpoints(target)
    results["swagger"] = swagger_hits
    for s in swagger_hits:
        if s.get("url") and s.get("status") in (200,):
            if s["url"] not in results["discovered_apis"]:
                results["discovered_apis"].append(s["url"])

    # 4) CORS checks for discovered APIs (safe: HEAD/OPTIONS)
    cors_results = []
    for api in list(results["discovered_apis"])[:150]:  # limit to first 150 to be polite
        try:
            cors = check_cors(api)
            cors_results.append({"api": api, "cors": cors})
        except Exception as e:
            cors_results.append({"api": api, "error": str(e)})
        time.sleep(args.delay)
    results["cors"] = cors_results

    # 5) Post-process & analyze findings
    analysis = analyze_findings(results)
    results["analysis"] = analysis

    # 6) Save and output
    repo = os.path.dirname(__file__)
    out_dir_json = os.path.join(repo, "reports")
    os.makedirs(out_dir_json, exist_ok=True)
    json_path = os.path.join(out_dir_json, f"{target}-apighost.json")
    save_json_report(json_path, results)
    html_path = os.path.join(out_dir_json, f"{target}-apighost.html")
    save_html_report(html_path, results)

    # Terminal summary
    print_summary(results, json_path, html_path)

    if not args.once:
        print("\n[!] Run finished. To run periodically, use cron/systemd or --once flag to do a single pass.")

if __name__ == "__main__":
    main()
