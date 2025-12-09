### 🚀 BCP-CyberSuite v4.0

Next-Gen Autonomous Cyber Recon & Offensive Intelligence Framework

![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![License MIT](https://img.shields.io/badge/License-MIT-green)
![GitHub Stars](https://img.shields.io/github/stars/cybernahid-dev/BCP-CyberSuite)
![GitHub Issues](https://img.shields.io/github/issues/cybernahid-dev/BCP-CyberSuite)
![Docker Pulls](https://img.shields.io/docker/pulls/cybernahid/bcp-cybersuite)
![Docker Image Size](https://img.shields.io/docker/image-size/cybernahid/bcp-cybersuite/latest)
![Version 4.0](https://img.shields.io/badge/Version-4.0-blueviolet)


Advanced • Modular • AI-Augmented • Enterprise-Grade

BCP-CyberSuite is a fully-modular, ultra-futuristic cyber-intelligence framework engineered for web applications, servers, APIs, cloud surfaces, and enterprise infrastructures. Powered by smart automation + AI heuristics + high-speed scanners.

---

### Table of Contents

- [✨ Features](#✨-features)
- [🚀 Quick Start](#🚀-quick-start)
- [📦 Installation](#📦-installation)
- [🧩 Modules](#🧩-modules)
- [📁 Project Structure](#📁-project-structure)
- [📊 Usage Examples](#📊-usage-examples)
- [📄 Reporting](#📄-reporting)
- [🤝 Contributing](#🤝-contributing)
- [📜 License](#📜-license)
- [⚠️ Legal & Ethical Use](#️-legal--ethical-use)
- [🏢 Developed By](#🏢-developed-by)
- [🌟 Support the Project](#🌟-support-the-project)
- [🔗 Useful Links](#🔗-useful-links)
- [🎯 Philosophy](#🎯-philosophy)

---

## ✨ Features

🔥 UltraReconX - Elite Reconnaissance Engine

· DNS intelligence & WHOIS analysis
· Subdomain enumeration (20+ sources)
· Certificate Transparency logs
· JavaScript secret detection
· AI-powered technology fingerprinting

⚡ PantherTechScanUltraX - Full-Stack Offensive Scanner

· Comprehensive port scanning (0-65535)
· AI-Tech Guessing 2.0 (Wappalyzer enhanced)
· WAF detection & bypass testing
· Deep crawler with JavaScript analysis
· Vulnerability assessment

👻 API-GhostScanner - API Security Assessment Engine

· Hidden API endpoint discovery
· Ghost endpoint detection
· Parameter injection testing
· Rate-limit analysis & bypass
· Authentication strength testing

🕵️ LeakHunter-X - Sensitive Data Hunter

· API keys & credentials detection
· Hardcoded secrets scanner
· Weak CORS/header analysis
· Advanced entropy-based detection
· Git repository exposure scanning

---

## 🚀 Quick Start

Option 1: Docker (Easiest)

```bash
# One command to run everything
docker run -it --rm cybernahid/bcp-cybersuite:latest
```

Option 2: From Source

```bash
# Clone and run
git clone https://github.com/cybernahid-dev/BCP-CyberSuite
cd BCP-CyberSuite
pip install -r requirements.txt
python3 bcp.py
```

---

## 📦 Installation

🐳 Docker (Recommended)

```bash
# Pull and run
docker pull cybernahid/bcp-cybersuite:latest
docker run -it --rm cybernahid/bcp-cybersuite:latest

# With persistent storage
mkdir -p reports databases
docker run -it --rm \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/databases:/app/databases \
  cybernahid/bcp-cybersuite:latest
```

🐧 Linux (Ubuntu/Debian/Kali)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip git

# Install BCP-CyberSuite
git clone https://github.com/cybernahid-dev/BCP-CyberSuite
cd BCP-CyberSuite
pip3 install -r requirements.txt
python3 bcp.py
```

📱 Termux (Android)

```bash
# Update and install
pkg update && pkg upgrade
pkg install python git

# Install framework
git clone https://github.com/cybernahid-dev/BCP-CyberSuite
cd BCP-CyberSuite
pip install -r requirements.txt
python bcp.py
```

🪟 Windows

```powershell
# Method 1: WSL2 (Recommended)
wsl --install
# Then follow Linux instructions above

# Method 2: Native Windows
# 1. Install Python from python.org
# 2. Install Git from git-scm.com
git clone https://github.com/cybernahid-dev/BCP-CyberSuite
cd BCP-CyberSuite
pip install -r requirements.txt
python bcp.py
```

🍎 macOS

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python git

# Install framework
git clone https://github.com/cybernahid-dev/BCP-CyberSuite
cd BCP-CyberSuite
pip3 install -r requirements.txt
python3 bcp.py
```

---

## 🧩 Modules

1. UltraReconX

```
Usage: python3 tools/UltraReconX/scanner.py -t target.com
Features:
  • Subdomain enumeration
  • DNS reconnaissance
  • Certificate transparency
  • JS file analysis
  • Technology stack detection
```

2. PantherTechScanUltraX

```
Usage: python3 tools/PantherTechScanUltraX/scanner.py -u https://target.com
Features:
  • Port scanning
  • Service detection
  • WAF identification
  • Vulnerability scanning
  • Technology fingerprinting
```

3. API-GhostScanner

```
Usage: python3 tools/API-GhostScanner/api_discover.py -u https://api.target.com
Features:
  • API endpoint discovery
  • Parameter fuzzing
  • Authentication testing
  • Rate-limit testing
  • Security header analysis
```

4. LeakHunter-X

```
Usage: python3 tools/LeakHunter-X/secret_scanner.py -u https://target.com
Features:
  • Secret/key detection
  • Hardcoded credential scanning
  • CORS misconfiguration testing
  • Security header analysis
  • Git exposure checking
```

---

## 📁 Project Structure

```
BCP-CyberSuite/
├── bcp.py                    # Main launcher
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yaml      # Docker orchestration
├── tools/                   # Core modules
│   ├── UltraReconX/        # Reconnaissance engine
│   ├── PantherTechScanUltraX/ # Offensive scanner
│   ├── API-GhostScanner/   # API security engine
│   └── LeakHunter-X/       # Data leak detector
├── reports/                # Generated reports (HTML/JSON)
├── databases/             # Scan databases and caches
└── scripts/              # Installation and utility scripts
```

---

## 📊 Usage Examples

Basic Reconnaissance

```bash
# Using UltraReconX
python3 tools/UltraReconX/scanner.py -t example.com -o recon_report.html

# Using Docker
docker run --rm cybernahid/bcp-cybersuite:latest recon -t example.com
```

Full Security Assessment

```bash
# Run all modules against a target
python3 bcp.py
# Select option 2 (PantherTechScanUltraX)
# Enter target: https://example.com
# Choose scan mode: full
```

API Security Testing

```bash
# Test API endpoints
python3 tools/API-GhostScanner/api_discover.py \
  -u https://api.example.com \
  -a comprehensive \
  -o api_report.html
```

Secret Detection

```bash
# Scan for leaks and secrets
python3 tools/LeakHunter-X/secret_scanner.py \
  -u https://example.com \
  -d deep \
  -o secrets_report.json
```

---

## 📄 Reporting

BCP-CyberSuite generates professional reports in multiple formats:

Report Types

· Executive Summary: High-level overview for management
· Technical Report: Detailed technical findings
· Remediation Guide: Step-by-step fix recommendations
· API Audit Report: Specialized API security assessment

Output Formats

```bash
# HTML Report (Interactive)
-o report.html

# JSON Report (Machine-readable)
-o report.json

# CSV Export (Spreadsheet)
-o data.csv

# Markdown (Documentation)
-o findings.md
```

Sample Report Structure

```
reports/
├── target_com/
│   ├── executive_summary.html
│   ├── technical_report.html
│   ├── api_audit.json
│   ├── vulnerabilities.csv
│   └── screenshots/
│       └── homepage.png
└── scan_logs/
    └── scan_20241209_143022.log
```

---

## 🤝 Contributing

We welcome contributions from the cybersecurity community!

How to Contribute

1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

Development Setup

```bash
# Clone repository
git clone https://github.com/cybernahid-dev/BCP-CyberSuite.git
cd BCP-CyberSuite

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
python -m pytest tests/

# Format code
black .
```

Code Standards

· Follow PEP 8 style guide
· Add docstrings to functions
· Include unit tests for new features
· Update documentation accordingly

---

## 📜 License

BCP-CyberSuite is released under the MIT License.

```
MIT License

Copyright (c) 2025 Bangladesh Cyber Panthers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Legal & Ethical Use

Important Notice

BCP-CyberSuite is designed for:

· Authorized security testing
· Educational purposes
· Security research
· Legitimate penetration testing engagements

⚠️ You must have explicit permission before scanning or testing any system you do not own or have authorization to test.

Authorized Usage

✅ Your own systems and networks
✅Systems you have written permission to test
✅CTF competitions and labs
✅Educational environments
✅Bug bounty programs (within scope)

Prohibited Usage

❌ Unauthorized scanning of systems
❌Malicious activities
❌Privacy violations
❌Network disruption
❌Illegal activities

The developers and Bangladesh Cyber Panthers are not responsible for any misuse of this tool.

---

## 🏢 Developed By

Bangladesh Cyber Panthers (BCP)

Leading cybersecurity research and development team from Bangladesh

Core Development Team:

· Project Lead: cybernahid-dev
· Framework Architecture: Bangladesh Cyber Panthers Security Division
· Quality Assurance: BCP Testing Team
· Documentation: BCP Technical Writers

Contact & Support:

· GitHub Issues: https://github.com/cybernahid-dev/BCP-CyberSuite/issues
· Email: cybernahid.dev@gmail.com
· Repository: https://github.com/cybernahid-dev/BCP-CyberSuite
· Docker Hub: https://hub.docker.com/r/cybernahid/bcp-cybersuite

---

## 🌟 Support the Project

If you find BCP-CyberSuite useful, please consider:

1. ⭐ Star the repository on GitHub
2. 🐛 Report bugs and issues
3. 💡 Suggest new features
4. 📢 Share with your network
5. 🔧 Contribute code or documentation

---

## 🔗 Useful Links

· Full Documentation - Detailed guides and tutorials
· Installation Guide - Complete installation instructions
· Troubleshooting - Common issues and solutions
· API Reference - Module API documentation
· Contributing Guide - How to contribute

---

## 🎯 Philosophy

"Maximum power, minimum effort."

BCP-CyberSuite embodies our philosophy that cybersecurity tools should be:

· Powerful yet Accessible - Enterprise capabilities without enterprise complexity
· Intelligent yet Transparent - AI-assisted without being a "black box"
· Comprehensive yet Modular - Complete coverage without bloat
· Professional yet Open - Industrial-grade tools available to all

---

Thank you for using BCP-CyberSuite! 🚀

Stay secure with Bangladesh Cyber Panthers 🔒


