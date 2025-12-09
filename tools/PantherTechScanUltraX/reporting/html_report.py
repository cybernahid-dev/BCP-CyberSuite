import json
import os

def generate_html_report(store):
    target = store.target if hasattr(store, "target") else "Unknown Target"
    data = store.data

    # JSON-safe conversion
    def safe(item):
        try:
            json.dumps(item)
            return item
        except:
            return str(item)

    data = {k: safe(v) for k, v in data.items()}

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PantherTechScanUltraX Report</title>
        <style>
            body {{
                background: #0D0D0D;
                color: #E0E0E0;
                font-family: monospace;
                padding: 20px;
            }}
            .container {{
                width: 95%;
                margin: auto;
            }}
            h1 {{
                color: #00E5FF;
                text-shadow: 0 0 10px #00E5FF;
            }}
            .section {{
                background: #111;
                padding: 15px;
                margin-top: 20px;
                border-left: 5px solid #00E5FF;
                border-radius: 6px;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 14px;
                background: #000;
                padding: 10px;
                border-radius: 6px;
                box-shadow: 0 0 10px #00E5FF55;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>PantherTechScanUltraX – Scan Report</h1>
            <h2>Target: {target}</h2>
    """

    for key, value in data.items():
        html += f"""
            <div class="section">
                <h3>{key}</h3>
                <pre>{json.dumps(value, indent=4)}</pre>
            </div>
        """

    html += """
        </div>
    </body>
    </html>
    """

    path = "report.html"
    try:
        with open(path, "w") as f:
            f.write(html)
        print(f"[✔] HTML report saved as: {path}")
    except Exception as e:
        print(f"[ERROR] Failed to save HTML report: {e}")
