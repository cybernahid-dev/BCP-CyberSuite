#!/usr/bin/env python3
# LeakHunter-X (starter edition)
# Dev: cybernahid-dev | Team: Bangladesh Cyber Panthers
# Passive leak & exposure scanner (ethical)

import os, json, time
from modules import github_scanner, crtsh_scanner, bucket_scanner, paste_scanner, ai_detector, reporter

BASE_DIR = os.path.dirname(__file__)
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def main():
    print("\nLeakHunter-X — Passive Leak & Exposure Scanner (starter)\n")
    target = input("[?] Enter target domain/company or GitHub org (example.com or cybernahid-dev): ").strip()
    if not target:
        print("Invalid target. Exiting."); return

    out = {"target": target, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "results": {}}

    print("[1/6] GitHub public search (code / commits) ...")
    gh = github_scanner.search_github(target)
    out["results"]["github_leaks"] = gh
    print(f"    → {len(gh)} potential items")

    print("[2/6] Certificate transparency (crt.sh) subdomain gather ...")
    ct = crtsh_scanner.search_crtsh(target)
    out["results"]["crtsh"] = ct
    print(f"    → {len(ct)} names")

    print("[3/6] Public bucket checks (S3/GCS/AZURE) ...")
    buckets = bucket_scanner.find_public_buckets(target)
    out["results"]["buckets"] = buckets
    print(f"    → {len(buckets)} public buckets found")

    print("[4/6] Paste sites quick scan ...")
    pastes = paste_scanner.search_pastes(target)
    out["results"]["pastes"] = pastes
    print(f"    → {len(pastes)} paste hits")

    print("[5/6] AI/Heuristic leak detector (analyze findings) ...")
    analysis = ai_detector.analyze(out)
    out["results"]["analysis"] = analysis

    # Save JSON report
    json_path = os.path.join(REPORTS_DIR, f"{target}-leakhunter.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"[✔] JSON report saved: {json_path}")

    # HTML & CSV/terminal summary
    reporter.save_html(out, REPORTS_DIR)
    reporter.print_summary(out, json_path)
    print("\n[✔] LeakHunter-X finished.\n")

if __name__ == "__main__":
    main()
