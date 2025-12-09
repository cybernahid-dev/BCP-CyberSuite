# swagger_detector.py — probe common OpenAPI/Swagger endpoints (read-only)
import requests

COMMON_SWAGGER_PATHS = [
    "/openapi.json", "/openapi.yaml", "/swagger.json", "/v2/api-docs",
    "/swagger/v1/swagger.json", "/api-docs", "/api-docs.json", "/swagger.json"
]

def probe_swagger_endpoints(domain):
    results = []
    bases = [f"https://{domain}", f"http://{domain}"]
    for base in bases:
        for p in COMMON_SWAGGER_PATHS:
            url = base.rstrip("/") + p
            try:
                r = requests.get(url, timeout=6, allow_redirects=True, verify=False)
                status = getattr(r, "status_code", None)
                content_type = r.headers.get("Content-Type","")
                # cheap check for json/openapi yaml
                is_api_doc = False
                if status == 200 and ("application/json" in content_type or r.text.strip().startswith("{")):
                    is_api_doc = True
                results.append({"url": url, "status": status, "is_api_doc": is_api_doc})
            except Exception as e:
                results.append({"url": url, "status": None, "error": str(e)})
    return results
