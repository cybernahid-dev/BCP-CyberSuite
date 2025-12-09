import re

def find_apis(html):
    apis = []

    fetch_calls = re.findall(r"fetch\(['\"](.*?)['\"]", html)
    xhr_calls = re.findall(r"open\(['\"](.*?)['\"]", html)

    apis.extend(fetch_calls)
    apis.extend(xhr_calls)

    return list(set(apis))
