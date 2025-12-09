import dns.resolver

def dns_info(domain):
    records = {}

    try:
        records["A"] = [r.address for r in dns.resolver.resolve(domain, "A")]
    except:
        records["A"] = []

    try:
        records["AAAA"] = [r.address for r in dns.resolver.resolve(domain, "AAAA")]
    except:
        records["AAAA"] = []

    try:
        records["MX"] = [str(r.exchange) for r in dns.resolver.resolve(domain, "MX")]
    except:
        records["MX"] = []

    try:
        records["NS"] = [str(r.target) for r in dns.resolver.resolve(domain, "NS")]
    except:
        records["NS"] = []

    try:
        records["TXT"] = [str(r) for r in dns.resolver.resolve(domain, "TXT")]
    except:
        records["TXT"] = []

    return records
