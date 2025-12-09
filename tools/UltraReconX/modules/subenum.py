# subenum.py
import socket
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data" / "subdomains.txt"

def load_wordlist():
    try:
        with open(str(BASE), "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except:
        # fallback small list
        return ["www","mail","api","dev","test","admin","blog","cdn","static"]

def resolve(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except:
        return None

def subdomain_scan(domain, max_results=200):
    subs = []
    words = load_wordlist()
    for w in words:
        host = f"{w}.{domain}"
        ip = resolve(host)
        if ip:
            subs.append({"host":host, "ip":ip})
    return subs
