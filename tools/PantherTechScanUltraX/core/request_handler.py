import requests

class RequestHandler:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def fetch(self, url):
        try:
            r = requests.get(url, timeout=self.timeout, verify=False)
            return r.text, r.headers
        except Exception as e:
            return "", {}
