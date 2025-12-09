def detect_waf(headers, html=""):
    """
    Advanced WAF Detection Engine
    Detects common WAFs using headers + HTML analysis.
    """

    if not isinstance(headers, dict):
        return "Unknown (Invalid header format)"

    # Convert all headers to lowercase strings
    headers_l = {k.lower(): str(v).lower() for k, v in headers.items()}
    html_l = html.lower() if isinstance(html, str) else ""

    waf_signatures = {
        "cloudflare": [
            "cf-ray", "cf-cache-status", "cloudflare"
        ],
        "sucuri": [
            "sucuri", "x-sucuri-id"
        ],
        "imperva/incapsula": [
            "incap-", "x-cdn", "incapsula"
        ],
        "akami": [
            "akamai", "akamai-ghost"
        ],
        "f5 big-ip": [
            "bigip", "f5"
        ],
        "modsecurity": [
            "mod_security", "modsecurity", "x-mod-security"
        ],
        "barracuda": [
            "barra", "barracuda"
        ],
        "aws waf": [
            "aws", "awswaf"
        ],
        "fortinet waf": [
            "fortiwaf", "fortinet"
        ],
        "ddos-guard": [
            "ddos-guard"
        ]
    }

    # Flatten all header strings for scanning
    all_header_text = " ".join([f"{k} {v}" for k, v in headers_l.items()])

    detected = []

    # Check signatures
    for waf, sigs in waf_signatures.items():
        for sig in sigs:
            if sig in all_header_text or sig in html_l:
                detected.append(waf)
                break

    # Return results
    if not detected:
        return "No WAF detected"

    # Remove duplicates and join cleanly
    return ", ".join(sorted(set(detected)))
