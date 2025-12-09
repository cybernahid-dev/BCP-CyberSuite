# modules/crtsh_scanner.py
import requests

CRT_URL = "https://crt.sh/?q=%25.{domain}&output=json"

def search_crtsh(domain):
    try:
        r = requests.get(CRT_URL.format(domain=domain), timeout=12, headers={"User-Agent":"LeakHunterX/1.0"})
        if r.status_code != 200:
            return []
        data = r.json()
        names = set()
        out = []
        for it in data:
            nv = it.get("name_value") or ""
            for n in str(nv).splitlines():
                n = n.strip()
                if n and n not in names:
                    names.add(n); out.append(n)
        return out
    except Exception:
        return []
