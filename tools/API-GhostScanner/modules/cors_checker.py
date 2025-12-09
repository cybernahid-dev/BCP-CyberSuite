# cors_checker.py — safely check CORS headers using OPTIONS/GET
import requests

DEFAULT_ORIGIN = "https://example.com"  # harmless origin to test

def check_cors(url):
    """
    Returns a dict describing Access-Control-Allow-* headers and permissiveness.
    """
    try:
        headers = {"Origin": DEFAULT_ORIGIN, "User-Agent": "API-GhostScanner/1.0"}
        # Try OPTIONS first, fallback to GET
        try:
            r = requests.options(url, headers=headers, timeout=6, allow_redirects=True, verify=False)
        except Exception:
            r = requests.get(url, headers=headers, timeout=6, allow_redirects=True, verify=False)
        acao = r.headers.get("Access-Control-Allow-Origin")
        acac = r.headers.get("Access-Control-Allow-Credentials")
        acam = r.headers.get("Access-Control-Allow-Methods")
        acah = r.headers.get("Access-Control-Allow-Headers")
        permissive = False
        if acao == "*" or (acao and "example.com" not in acao and "*" in acao):
            permissive = True
        # certificateless or blocked endpoints simply return None values
        return {
            "status_code": getattr(r, "status_code", None),
            "acao": acao,
            "acac": acac,
            "acam": acam,
            "acah": acah,
            "permissive": permissive
        }
    except Exception as e:
        return {"error": str(e)}
