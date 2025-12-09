import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_js_from_pages(url):
    """
    Extracts JavaScript file URLs and inline JavaScript from a webpage.
    Returns a dictionary with lists of external and inline JS.
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        external_js = []
        inline_js = []

        # Extract external .js files
        for script in soup.find_all("script", src=True):
            full_url = urljoin(url, script["src"])
            external_js.append(full_url)

        # Extract inline scripts
        for script in soup.find_all("script", src=False):
            if script.string:
                inline_js.append(script.string.strip())

        return {
            "external_js": external_js,
            "inline_js": inline_js
        }

    except Exception as e:
        return {
            "error": str(e),
            "external_js": [],
            "inline_js": []
        }
