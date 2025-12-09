# analyzer.py — analyze discovered data and apply heuristics to prioritize
def analyze_findings(results):
    """
    Simple heuristic scoring:
      - more discovered_apis => higher surface
      - permissive CORS -> +score
      - swagger found -> +score
      - token leaks in js_patterns -> +score
    """
    score = 10
    notes = []
    apis = results.get("discovered_apis", [])
    cors = results.get("cors", [])
    swagger = results.get("swagger", [])
    js_patterns = results.get("js_patterns", [])

    score += min(len(apis) * 3, 40)
    if any(c.get("cors", {}).get("permissive") for c in cors if isinstance(c, dict)):
        score += 20
        notes.append("At least one endpoint has permissive CORS headers.")
    if any(s.get("is_api_doc") for s in swagger if isinstance(s, dict)):
        score += 15
        notes.append("OpenAPI/Swagger document detected.")
    # token heuristics
    tokens = [p for p in js_patterns if p.lower().startswith("bearertoken:") or "awskey:" in p.lower()]
    if tokens:
        score += 20
        notes.append(f"Possible tokens/keys found in JS ({len(tokens)} hits).")
    score = min(score, 100)
    return {"risk_score": score, "notes": notes, "summary": {
        "apis_count": len(apis),
        "js_files": len(results.get("js_files", [])),
        "js_patterns": len(js_patterns),
        "swagger_hits": sum(1 for s in swagger if s.get("is_api_doc"))
    }}
