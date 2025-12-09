# crtsh_lookup.py
import requests

CRTSH_URL = "https://crt.sh/?q=%25.{domain}&output=json"

def crtsh_lookup(domain):
    url = CRTSH_URL.format(domain=domain)
    r = requests.get(url, timeout=12, headers={"User-Agent":"UltraReconX/1.0"})
    if r.status_code != 200:
        return []
    try:
        data = r.json()
    except:
        return []
    # extract unique common names / names
    names = set()
    for item in data:
        name = item.get("name_value") or item.get("common_name")
        if name:
            # may contain multiple names separated by newline
            for n in str(name).splitlines():
                n = n.strip()
                if n:
                    names.add(n)
    return sorted(names)
