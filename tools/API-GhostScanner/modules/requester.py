# requester.py — safe HTTP helpers + local-target detection
import requests
from urllib.parse import urlparse
import socket

DEFAULT_UA = "API-GhostScanner/1.0 (+https://github.com/cybernahid-dev)"
TIMEOUT = 8

def safe_get(url, headers=None, allow_redirects=True):
    try:
        h = {"User-Agent": DEFAULT_UA}
        if headers:
            h.update(headers)
        return requests.get(url, headers=h, timeout=TIMEOUT, allow_redirects=allow_redirects, verify=False)
    except Exception:
        return None

def safe_head(url, headers=None):
    try:
        h = {"User-Agent": DEFAULT_UA}
        if headers:
            h.update(headers)
        return requests.head(url, headers=h, timeout=6, allow_redirects=True, verify=False)
    except Exception:
        return None

def is_local_target(target):
    """
    Return True if target is localhost/127.0.0.1/::1 or private network
    """
    try:
        parsed = urlparse(target if "://" in target else "http://" + target)
        hostname = parsed.hostname
        if not hostname:
            return False
        if hostname in ("localhost", "127.0.0.1", "::1"):
            return True
        ip = socket.gethostbyname(hostname)
        # private ranges start with:
        if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172."):
            return True
        return False
    except Exception:
        return False
