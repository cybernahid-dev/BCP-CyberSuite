import json, os

def print_terminal_summary(target, report_path):
    try:
        with open(report_path, "r") as f:
            data = json.load(f)
    except:
        print("ERROR: Cannot load report.")
        return

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"    UltraReconX — Passive Intelligence Report")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    print(f"[✓] Target: {target}")
    print(f"[✓] IP Address: {data.get('dns',{}).get('A','N/A')}")
    print(f"[✓] Cloudflare Protected: {data.get('cloudflare','Unknown')}")
    print(f"[✓] CMS: {data.get('cms','Not Detected')}")
    print(f"[✓] Tech: {', '.join(data.get('tech', [])) or 'None'}\n")

    # -------------------------
    # SUBDOMAINS
    # -------------------------
    subs = data.get("subdomains", [])
    print("──────────────────────────────")
    print(f" Subdomains Found: {len(subs)}")
    print("──────────────────────────────")
    for s in subs[:10]:
        print(f" • {s}")
    if len(subs) > 10:
        print(f" • ... ({len(subs)-10} more)")
    print()

    # -------------------------
    # PAGES DISCOVERED (Short)
    # -------------------------
    pages = data.get("pages", [])
    page_file = os.path.join(os.path.dirname(report_path), f"{target}-pages.txt")

    with open(page_file, "w") as pf:
        for p in pages:
            pf.write(p + "\n")

    print("──────────────────────────────")
    print(f" Pages Discovered: {len(pages)}")
    print("──────────────────────────────")
    for p in pages[:10]:
        print(f" • {p}")
    if len(pages) > 10:
        print(f" • ... ({len(pages)-10} more)")
    print(f"\nFull page list saved → {page_file}\n")

    # -------------------------
    # JS Secrets Short Summary
    # -------------------------
    js_findings = data.get("js_findings", [])
    print("──────────────────────────────")
    print(" JS Secrets Summary")
    print("──────────────────────────────")
    if js_findings:
        for f in js_findings[:10]:
            print(f" • {f}")
        if len(js_findings) > 10:
            print(f" • ... ({len(js_findings)-10} more)")
    else:
        print(" • No JS-related secrets found.")
    print()

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("            Scan Completed Successfully")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
