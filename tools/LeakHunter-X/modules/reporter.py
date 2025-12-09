# modules/reporter.py
import os, json, html

def save_html(out, reports_dir):
    target = out.get("target")
    html_path = os.path.join(reports_dir, f"{target}-leakhunter.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write("<html><head><meta charset='utf-8'><title>LeakHunter-X Report</title></head><body>")
        fh.write(f"<h1>LeakHunter-X Report — {html.escape(target)}</h1>")
        fh.write(f"<p>Timestamp: {html.escape(out.get('timestamp',''))}</p>")
        fh.write("<h2>GitHub Findings</h2><ul>")
        for g in out["results"].get("github_leaks", []):
            fh.write(f"<li><a href='{g.get('html_url')}' target='_blank'>{html.escape(str(g.get('repo')))} / {html.escape(str(g.get('path')))}</a></li>")
        fh.write("</ul>")
        fh.write("<h2>CRT.SH Names</h2><ul>")
        for n in out["results"].get("crtsh", []):
            fh.write(f"<li>{html.escape(n)}</li>")
        fh.write("</ul>")
        fh.write("<h2>Buckets</h2><ul>")
        for b in out["results"].get("buckets", []):
            fh.write(f"<li>{html.escape(str(b.get('url')))} (status {b.get('status')})</li>")
        fh.write("</ul>")
        fh.write("<h2>Pastes</h2><ul>")
        for p in out["results"].get("pastes", []):
            fh.write(f"<li><a href='{p.get('url')}' target='_blank'>{html.escape(p.get('url'))}</a></li>")
        fh.write("</ul>")
        fh.write("<h2>Analysis</h2>")
        fh.write(f"<pre>{html.escape(json.dumps(out['results'].get('analysis',{}), indent=2))}</pre>")
        fh.write("</body></html>")
    return html_path

def print_summary(out, json_path):
    target = out.get("target")
    print("\n" + "━"*60)
    print(" LeakHunter-X — Summary")
    print("━"*60)
    print(f"Target: {target}")
    gh = out["results"].get("github_leaks", [])
    print(f"GitHub potential findings: {len(gh)}")
    print(f"CRT.sh names: {len(out['results'].get('crtsh', []))}")
    print(f"Public buckets: {len(out['results'].get('buckets', []))}")
    print(f"Pastes found: {len(out['results'].get('pastes', []))}")
    print("\nAnalysis Summary:")
    print(json.dumps(out['results'].get('analysis', {}), indent=2))
    print("\nReports:")
    print(f" - JSON: {json_path}")
    html_path = os.path.join(os.path.dirname(json_path), f"{target}-leakhunter.html")
    print(f" - HTML: {html_path}")
    print("━"*60)
