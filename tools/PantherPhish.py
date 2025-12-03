import re
import requests

def run():
    url = input("Enter URL to scan: ")
    pattern = r"(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)\."
    match = re.findall(pattern, url)
    if match:
        domain = match[0]
        print(f"Domain detected: {domain}")
    try:
        response = requests.get(url)
        if len(response.text) < 1000:  # Simple heuristic
            print("Likely phishing: Very small content")
        else:
            print("Looks safe")
    except:
        print("Error accessing URL")
