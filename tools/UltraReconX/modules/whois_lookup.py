# whois_lookup.py
# tries python-whois then fallback to system `whois` command

import subprocess, json

def whois_lookup(domain):
    # try python-whois first (if available)
    try:
        import whois
        w = whois.whois(domain)
        # convert to dict, safe serialization
        return json.loads(json.dumps(w, default=str))
    except Exception:
        # fallback to system `whois`
        try:
            out = subprocess.check_output(["whois", domain], stderr=subprocess.DEVNULL, timeout=15)
            return {"raw": out.decode(errors="ignore")}
        except Exception as e:
            raise RuntimeError(f"whois failed: {e}")
