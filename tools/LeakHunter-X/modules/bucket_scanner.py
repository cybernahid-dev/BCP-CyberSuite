# modules/bucket_scanner.py
# Passive public bucket existence checker (read-only)
import requests, re

COMMON_BUCKET_PATTERNS = [
    "{target}",
    "{target}-backup",
    "{target}-assets",
    "www-{target}",
    "static-{target}"
]

def _check_url(url):
    try:
        r = requests.get(url, timeout=8, allow_redirects=True)
        if r.status_code in (200, 403, 301, 302):
            return True, r.status_code
    except:
        pass
    return False, None

def find_public_buckets(target):
    found = []
    # S3 style candidate names
    for p in COMMON_BUCKET_PATTERNS:
        name = p.format(target=target.replace(".", "-"))
        # S3 URL attempts
        urls = [
            f"https://{name}.s3.amazonaws.com",
            f"https://{name}.s3.us-east-1.amazonaws.com",
            f"https://{name}.s3.amazonaws.com/index.html",
            f"https://storage.googleapis.com/{name}/",
            f"https://{name}.blob.core.windows.net/",
        ]
        for u in urls:
            ok, code = _check_url(u)
            if ok:
                found.append({"url": u, "status": code})
    return found
