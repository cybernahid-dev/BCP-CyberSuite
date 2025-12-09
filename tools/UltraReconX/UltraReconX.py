#!/usr/bin/env python3
import os
import json
import socket
import requests
import datetime

from modules.js_extractor import extract_js_from_pages
from modules.tech_detector import detect_technologies



# -----------------------------
# Helper
# -----------------------------
def save_report(domain, results):
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"{report_dir}/{domain}_{timestamp}.json"

    with open(filepath, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n[✔] Report saved: {filepath}")


# -----------------------------
# DNS Lookup
# -----------------------------
def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"A": ip}
    except:
        return {"A": "N/A"}


# -----------------------------
# WHOIS Lookup (Basic)
# -----------------------------
def whois_lookup(domain):
    try:
        import subprocess
        result = subprocess.check_output(["whois", domain], text=True)
        return result
    except:
        return "WHOIS not available"


# -----------------------------
# Certificate Transparency
# -----------------------------
def fetch_ct_logs(domain):
    url = f"https://crt.sh/?q={domain}&output=json"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []


# -----------------------------
# Passive OSINT
# -----------------------------
def passive_osint(domain):
    return {
        "urlscan": f"https://urlscan.io/search/#domain:{domain}",
        "virustotal": f"https://www.virustotal.com/gui/domain/{domain}"
    }


# -----------------------------
# Subdomain Enumeration (Basic)
# -----------------------------
def enum_subdomains(domain):
    common = ["www", "mail", "api", "dev", "test", "blog", "shop"]
    found = []

    for sub in common:
        host = f"{sub}.{domain}"
        try:
            socket.gethostbyname(host)
            found.append(host)
        except:
            pass

    return found


# -----------------------------
# Fetch HTTP headers
# -----------------------------
def fetch_headers(domain):
    try:
        r = requests.get("http://" + domain, timeout=5)
        return dict(r.headers)
    except:
        return {}


# -----------------------------
# Crawl pages (Basic)
# -----------------------------
def crawl_pages(domain):
    try:
        r = requests.get("http://" + domain, timeout=5)
        return r.text, 1  # page content + pages crawled count
    except:
        return "", 0


# -----------------------------
# MAIN
# -----------------------------
def main():
    show_banner()

    target = input("\n[?] Enter target domain (example.com): ").strip()
    print(f"\n[+] Starting UltraReconX for: {target}\n")

    results = {}

    # [1] DNS
    print("[1/7] DNS lookup...")
    results["dns"] = dns_lookup(target)

    # [2] WHOIS
    print("[2/7] WHOIS lookup...")
    results["whois"] = whois_lookup(target)

    # [3] Certificate Transparency
    print("[3/7] Certificate Transparency...")
    results["ct_logs"] = fetch_ct_logs(target)

    # [4] Passive OSINT
    print("[4/7] Passive OSINT...")
    results["osint"] = passive_osint(target)

    # [5] Subdomain Enumeration
    print("[5/7] Subdomain Enumeration...")
    results["subdomains"] = enum_subdomains(target)

    # Fetch headers (needed for tech detector)
    headers = fetch_headers(target)

    # Crawl pages
    page_html, crawled = crawl_pages(target)
    results["pages_crawled"] = crawled

    # [6] JS Secret Detection
    print("[6/7] JS Secret Detection...")
    results["js_secrets"] = extract_js_from_pages(target)

    # [7] Technology Fingerprinting
    print("[7/7] Technology Fingerprinting...")
    results["tech_detected"] = detect_technologies(target, headers)

    # Save full report
    save_report(target, results)

    print("\n[✔] UltraReconX Completed Successfully!")
    print("[✔] All tasks finished.\n")


if __name__ == "__main__":
    main()
