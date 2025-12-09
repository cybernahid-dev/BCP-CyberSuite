# js_parser.py — extract JS files and patterns from JS content
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

JS_SRC_RE = re.compile(r'<script[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
FETCH_RE = re.compile(r'\bfetch\((?:\s*)[\'"]([^\'"]+)[\'"]', re.IGNORECASE)
XHR_RE = re.compile(r'\bXMLHttpRequest\b', re.IGNORECASE)
AXIOS_RE = re.compile(r'\baxios\.(?:get|post|request)\b', re.IGNORECASE)
URL_RE = re.compile(r'https?://[A-Za-z0-9\-\._~:/\?#\[\]@!\$&\'\(\)\*\+,;=%]+')

def extract_js_urls(html, base_url):
    try:
        soup = BeautifulSoup(html, "html.parser")
        scripts = []
        for tag in soup.find_all("script", src=True):
            src = tag["src"].strip()
            if src.startswith("//"):
                scripts.append("https:" + src)
            elif src.startswith("http"):
                scripts.append(src)
            else:
                scripts.append(urljoin(base_url, src))
        return list(dict.fromkeys(scripts))
    except Exception:
        return []

def extract_patterns_from_js(js_text):
    patterns = []
    # fetch / XHR / axios endpoints
    for m in FETCH_RE.findall(js_text):
        patterns.append(m)
    # absolute URLs
    for m in URL_RE.findall(js_text):
        patterns.append(m)
    # bearer tokens or keys (short heuristics)
    # Bearer token
    token_re = re.compile(r'(?:Bearer|bearer)\s+([A-Za-z0-9\-\._~\+/=]+)')
    for t in token_re.findall(js_text):
        patterns.append("BearerToken:" + t[:32])
    # AWS-ish keys
    aws_re = re.compile(r'AKIA[0-9A-Z]{16}')
    for t in aws_re.findall(js_text):
        patterns.append("AWSKey:" + t)
    # return unique
    return list(dict.fromkeys([p for p in patterns if p]))
