#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PantherTechScanUltraX – Full Power Ultra Edition
# Developed by: cybernahid-dev
# Team: Bangladesh Cyber Panthers
# Repository: BCP-CyberSuite
# Purpose: Ethical Recon, Fingerprinting, OSINT & Security Analysis

import os
import time

from core.request_handler import RequestHandler
from core.datastore import DataStore
from scanners.portscan import full_port_scan
from scanners.tech_fingerprint import fingerprint_tech
from scanners.ai_tech_guess import ai_guess
from scanners.waf_detector import detect_waf
from scanners.dns_scanner import dns_info
from scanners.crawler import crawl
from scanners.js_analyzer import analyze_js
from scanners.api_hunter import find_apis
from scanners.subdomain_bruteforce import subdomain_scan
from reporting.html_report import generate_html_report
from reporting.json_report import generate_json_report
from reporting.csv_report import generate_csv_report


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    clear()
    print("""
 _____               _____         _     
/  ___|             |_   _|       | |    
\ `--.  ___ __ _ _ __ | | ___  ___| |__  
 `--. \/ __/ _` | '_ \| |/ _ \/ __| '_ \ 
/\__/ / (_| (_| | | | | |  __/ (__| | | |
\____/ \___\__,_|_| |_\_/\___|\___|_| |_|
                                         
                                         
      PantherTechScanUltraX – Ultra Edition

      Developed by: cybernahid-dev
      Team: Bangladesh Cyber Panthers
      Repository: BCP-CyberSuite
    """)
    target = input("\n[?] Enter target domain or IP: ").strip()
    if not target:
        print("Invalid target!")
        return

    print("\n[+] Initializing request handler...")
    req = RequestHandler()

    print("[+] Creating datastore...")
    store = DataStore(target)

    print("\n[⚡] Starting full-port scan (0–65535)...")
    ports = full_port_scan(target)
    store.save("ports", ports)

    print("[⚡] Fetching HTML for analysis...")
    html, headers = req.fetch(f"http://{target}")
    store.save("html", html)
    store.save("headers", headers)

    print("[⚡] Running technology fingerprinting...")
    tech = fingerprint_tech(f"http://{target}")
    store.save("tech", tech)

    print("[⚡] AI heuristic tech detection...")
    ai = ai_guess(html, headers)
    store.save("ai_guess", ai)

    print("[⚡] Detecting WAF...")
    waf = detect_waf(headers, html)
    store.save("waf", waf)

    print("[⚡] Running DNS Intelligence...")
    dns_data = dns_info(target)
    store.save("dns", dns_data)

    print("[⚡] Starting Deep Spider Crawler...")
    pages = crawl(f"http://{target}")
    store.save("pages", pages)

    print("[⚡] Extracting JS Files...")
    js_findings = analyze_js(html)
    store.save("js", js_findings)

    print("[⚡] Hunting API Endpoints...")
    apis = find_apis(html)
    store.save("apis", apis)

    print("[⚡] Subdomain Enumeration...")
    subs = subdomain_scan(target)
    store.save("subdomains", subs)

    print("\n[✔] All modules completed. Generating reports...")

    generate_html_report(store)
    generate_json_report(store)
    generate_csv_report(store)

    print("\n[✔] Reports saved in /reports/")
    print("[✔] PantherTechScanUltraX task completed.\n")


if __name__ == "__main__":
    main()
