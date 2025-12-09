import dns.resolver

COMMON_SUBS = [
    "www", "api", "mail", "admin", "dev", "test",
    "blog", "cdn", "portal", "beta", "ftp"
]

def subdomain_scan(domain):
    found = []

    for sub in COMMON_SUBS:
        full = f"{sub}.{domain}"
        try:
            dns.resolver.resolve(full, "A")
            found.append(full)
        except:
            pass

    return found
