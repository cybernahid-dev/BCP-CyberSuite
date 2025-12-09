import re

def analyze_js(content):
    findings = {}

    findings["endpoints"] = re.findall(r"https?://[^\s\"']+", content)
    findings["api_keys"] = re.findall(r"[A-Za-z0-9_\-]{16,45}", content)
    findings["tokens"] = re.findall(r"token=\"?[A-Za-z0-9\.\-_]+\"?", content)

    return findings
