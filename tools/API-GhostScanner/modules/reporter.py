# reporter.py — JSON + HTML report and terminal summary
import os, json
from jinja2 import Template

HTML_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><title>API-GhostScanner Report — {{ target }}</title>
<style>
body{background:#0b0b0b;color:#eee;font-family:Inter,Arial;padding:18px}
.container{max-width:1100px;margin:0 auto}
.hero{background:linear-gradient(90deg,#2a0000,#3a0000);padding:18px;border-radius:8px}
.card{background:#111;padding:12px;border-radius:8px;margin-top:12px}
table{width:100%;border-collapse:collapse}
th,td{padding:8px;border-bottom:1px solid #222}
th{color:#ffb3b3}
a{color:#ff8b8b}
pre{background:#080808;padding:10px;border-radius:6px}
.pill{display:inline-block;padding:6px 10px;border-radius:999px;background:#220000;color:#ffb3b3;margin-right:6px}
</style>
</head><body>
<div class="container">
  <div class="hero"><h1>API-GhostScanner Report</h1><div class="small">Target: {{ target }} • Generated: {{ ts }}</div></div>

  <div class="card">
    <h3>Summary</h3>
    <p><span class="pill">APIs</span> {{ apis_count }} <span class="pill">JS files</span> {{ js_files }} <span class="pill">Swagger</span> {{ swagger_count }} <span class="pill">Risk</span> {{ risk }}</p>
  </div>

  <div class="card"><h3>Discovered APIs (sample)</h3>
    {% if apis %}<ul>{% for a in apis[:40] %}<li><a href="{{ a }}">{{ a }}</a></li>{% endfor %}</ul>{% else %}<p>None found</p>{% endif %}
  </div>

  <div class="card"><h3>JS Patterns / Tokens (sample)</h3>
    <pre>{{ js_patterns }}</pre>
  </div>

  <div class="card"><h3>CORS Checks (sample)</h3>
    {% for c in cors[:40] %}
      <div><strong>{{ c.api }}</strong> — {{ c.cors }}</div>
    {% endfor %}
  </div>

  <div class="card"><h3>Swagger Probes</h3>
    <ul>{% for s in swagger %}<li>{{ s.url }} — status: {{ s.status }} — api_doc: {{ s.is_api_doc }}</li>{% endfor %}</ul>
  </div>

  <div class="card"><h3>Notes</h3><pre>{{ notes }}</pre></div>

  <footer style="text-align:center;color:#777;padding:18px">BCP CyberSuite • Developer: cybernahid-dev • Bangladesh Cyber Panthers</footer>
</div>
</body></html>
"""

def save_json_report(path, data):
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        print(f"[✔] JSON report saved → {path}")
    except Exception as e:
        print("Failed to save JSON:", e)

def save_html_report(path, results):
    try:
        tpl = Template(HTML_TEMPLATE)
        html = tpl.render(
            target=results.get("target"),
            ts=results.get("timestamp"),
            apis=results.get("discovered_apis", []),
            apis_count=len(results.get("discovered_apis", [])),
            js_files=len(results.get("js_files", [])),
            swagger=results.get("swagger", []),
            swagger_count=sum(1 for s in results.get("swagger", []) if s.get("is_api_doc")),
            js_patterns="\n".join(results.get("js_patterns", [])[:200]),
            cors=results.get("cors", []),
            risk=results.get("analysis", {}).get("risk_score", 0),
            notes="\n".join(results.get("analysis", {}).get("notes", []))
        )
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"[✔] HTML report saved → {path}")
    except Exception as e:
        print("Failed to save HTML:", e)

def print_summary(results, json_path, html_path):
    print("\n" + "━"*60)
    print("API-GhostScanner — Summary")
    print("━"*60)
    print("Target:", results.get("target"))
    print("APIs discovered:", len(results.get("discovered_apis", [])))
    print("JS files fetched:", len(results.get("js_files", [])))
    print("Swagger docs found:", sum(1 for s in results.get("swagger", []) if s.get("is_api_doc")))
    print("Risk score:", results.get("analysis", {}).get("risk_score"))
    print("Notes:")
    for n in results.get("analysis", {}).get("notes", []):
        print(" -", n)
    print("\nReports:")
    print(" - JSON:", json_path)
    print(" - HTML:", html_path)
    print("━"*60)
