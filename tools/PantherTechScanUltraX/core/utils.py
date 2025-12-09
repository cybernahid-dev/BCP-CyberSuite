# core/utils.py

import random

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []

def random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Linux; Android 10)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    ]
    return random.choice(agents)

def clean_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "http://" + url
