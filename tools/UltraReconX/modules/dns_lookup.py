# dns_lookup.py
import socket
import dns.resolver

def dns_info(domain):
    out = {}
    try:
        out["A"] = [r.address for r in dns.resolver.resolve(domain, "A")]
    except:
        out["A"] = []
    try:
        out["AAAA"] = [r.address for r in dns.resolver.resolve(domain, "AAAA")]
    except:
        out["AAAA"] = []
    try:
        out["MX"] = [str(r.exchange) for r in dns.resolver.resolve(domain, "MX")]
    except:
        out["MX"] = []
    try:
        out["NS"] = [str(r.target) for r in dns.resolver.resolve(domain, "NS")]
    except:
        out["NS"] = []
    try:
        out["TXT"] = [str(r) for r in dns.resolver.resolve(domain, "TXT")]
    except:
        out["TXT"] = []
    return out
