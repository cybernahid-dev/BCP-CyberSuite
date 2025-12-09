#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BCP-CyberSuite Master Launcher v4.0
Developed by: cybernahid-dev
Team: Bangladesh Cyber Panthers
Repository: https://github.com/cybernahid-dev/BCP-CyberSuite
"""

import os
import sys
import time
import subprocess
import platform
from datetime import datetime

# ANSI Color Codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display BCP-CyberSuite Banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    ██████╗  ██████╗██████╗     ██████╗██╗   ██╗██████╗ ███████╗███████╗██╗   ██╗║
║    ██╔══██╗██╔════╝██╔══██╗   ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔════╝██║   ██║║
║    ██████╔╝██║     ██████╔╝   ██║      ╚████╔╝ ██████╔╝█████╗  ███████╗██║   ██║║
║    ██╔══██╗██║     ██╔═══╝    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ╚════██║██║   ██║║
║    ██████╔╝╚██████╗██║        ╚██████╗   ██║   ██████╔╝███████╗███████║╚██████╔╝║
║    ╚═════╝  ╚═════╝╚═╝         ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ║
║                                                                                  ║
║            {Colors.MAGENTA}Next-Gen Autonomous Cyber Recon & Offensive Intelligence Framework{Colors.CYAN}            ║
║                          {Colors.YELLOW}v4.0 • Bangladesh Cyber Panthers{Colors.CYAN}                           ║
╚══════════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print(f"{Colors.YELLOW}[*] Checking dependencies...{Colors.END}")
    
    required_packages = [
        'requests', 'dnspython', 'beautifulsoup4', 'lxml',
        'urllib3', 'jinja2', 'colorama', 'tqdm', 'python-dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"{Colors.RED}[!] Missing dependencies: {', '.join(missing)}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Installing missing packages...{Colors.END}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print(f"{Colors.GREEN}[+] Dependencies installed successfully!{Colors.END}")
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}[!] Failed to install dependencies. Please run:{Colors.END}")
            print(f"{Colors.WHITE}pip install -r requirements.txt{Colors.END}")
            return False
    else:
        print(f"{Colors.GREEN}[+] All dependencies are satisfied!{Colors.END}")
    
    return True

def get_system_info():
    """Display system information"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}System Information:{Colors.END}")
    print(f"{Colors.WHITE}OS: {platform.system()} {platform.release()}{Colors.END}")
    print(f"{Colors.WHITE}Python: {platform.python_version()}{Colors.END}")
    print(f"{Colors.WHITE}Processor: {platform.processor()}{Colors.END}")
    print(f"{Colors.WHITE}Architecture: {platform.machine()}{Colors.END}")
    print(f"{Colors.WHITE}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")

def update_framework():
    """Update BCP-CyberSuite to latest version"""
    print(f"{Colors.YELLOW}[*] Updating BCP-CyberSuite...{Colors.END}")
    try:
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        print(f"{Colors.GREEN}[+] Framework updated successfully!{Colors.END}")
        print(f"{Colors.YELLOW}[*] Updating dependencies...{Colors.END}")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"])
        print(f"{Colors.GREEN}[+] All updates completed!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Update failed: {str(e)}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Try: git pull origin main{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def show_tool_info(tool_name, tool_path):
    """Display information about a specific tool"""
    clear_screen()
    print_banner()
    
    tool_descriptions = {
        "UltraReconX": f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}
{Colors.CYAN}{Colors.BOLD}║                   UltraReconX - Elite Recon Engine           ║{Colors.END}
{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.WHITE}{Colors.BOLD}Description:{Colors.END}
  Advanced reconnaissance engine for comprehensive target intelligence gathering.
  Combines passive and active techniques for maximum information discovery.

{Colors.WHITE}{Colors.BOLD}Features:{Colors.END}
  • DNS Intelligence & WHOIS Lookup
  • Subdomain Enumeration (20+ sources)
  • Certificate Transparency Logs
  • JavaScript Secret Detection
  • Live Page Screenshot & Analysis
  • AI-Powered Fingerprinting
  • Real-time Infrastructure Metrics

{Colors.WHITE}{Colors.BOLD}Usage:{Colors.END}
  python3 {tool_path} -t target.com -o report.html

{Colors.WHITE}{Colors.BOLD}Output Formats:{Colors.END}
  JSON, HTML, CSV, TXT

{Colors.YELLOW}Press Enter to launch this tool or 'b' to go back...{Colors.END}
""",
        
        "PantherTechScanUltraX": f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}
{Colors.CYAN}{Colors.BOLD}║           PantherTechScanUltraX - Full Stack Scanner         ║{Colors.END}
{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.WHITE}{Colors.BOLD}Description:{Colors.END}
  Comprehensive offensive scanner with AI-enhanced technology detection
  and vulnerability assessment capabilities.

{Colors.WHITE}{Colors.BOLD}Features:{Colors.END}
  • Full Port Scan (0-65535) with Service Detection
  • AI-Tech Guessing 2.0 (Enhanced Wappalyzer)
  • WAF Detection & Bypass Testing
  • Deep Crawler with JavaScript Analysis
  • API Endpoint Discovery
  • Vulnerability Assessment
  • HTML/Header Technology Extraction

{Colors.WHITE}{Colors.BOLD}Usage:{Colors.END}
  python3 {tool_path} -u https://target.com -p full

{Colors.WHITE}{Colors.BOLD}Scan Modes:{Colors.END}
  quick, standard, full, aggressive

{Colors.YELLOW}Press Enter to launch this tool or 'b' to go back...{Colors.END}
""",
        
        "LeakHunter-X": f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}
{Colors.CYAN}{Colors.BOLD}║               LeakHunter-X - Sensitive Data Hunter          ║{Colors.END}
{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.WHITE}{Colors.BOLD}Description:{Colors.END}
  Advanced sensitive data detection engine for identifying leaks,
  exposed credentials, and security misconfigurations.

{Colors.WHITE}{Colors.BOLD}Features:{Colors.END}
  • API Keys & Token Detection
  • Hardcoded Credentials Scanner
  • Weak CORS Configuration Testing
  • Security Header Analysis
  • Git Repository Leak Detection
  • Environment Variable Exposure
  • Advanced Entropy-Based Secret Detection

{Colors.WHITE}{Colors.BOLD}Usage:{Colors.END}
  python3 {tool_path} -u https://target.com -d deep

{Colors.WHITE}{Colors.BOLD}Detection Levels:{Colors.END}
  basic, standard, deep, paranoid

{Colors.YELLOW}Press Enter to launch this tool or 'b' to go back...{Colors.END}
""",
        
        "API-GhostScanner": f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}
{Colors.CYAN}{Colors.BOLD}║              API-GhostScanner - API Security Engine         ║{Colors.END}
{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.WHITE}{Colors.BOLD}Description:{Colors.END}
  Specialized API security assessment tool for discovering hidden endpoints,
  testing vulnerabilities, and analyzing authentication mechanisms.

{Colors.WHITE}{Colors.BOLD}Features:{Colors.END}
  • Hidden API Discovery
  • Ghost Endpoint Detection
  • Parameter Injection Testing
  • Rate Limit Analysis & Bypass
  • Authentication Strength Testing
  • Swagger/OpenAPI Parser
  • JWT/OAuth Security Assessment

{Colors.WHITE}{Colors.BOLD}Usage:{Colors.END}
  python3 {tool_path} -u https://api.target.com -a comprehensive

{Colors.WHITE}{Colors.BOLD}Assessment Modes:{Colors.END}
  discovery, basic, standard, comprehensive

{Colors.YELLOW}Press Enter to launch this tool or 'b' to go back...{Colors.END}
"""
    }
    
    if tool_name in tool_descriptions:
        print(tool_descriptions[tool_name])
    else:
        print(f"{Colors.RED}[!] No information available for {tool_name}{Colors.END}")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return
    
    choice = input(f"\n{Colors.GREEN}Your choice: {Colors.END}").strip().lower()
    
    if choice == 'b':
        return
    else:
        launch_tool(tool_path)

def launch_tool(tool_path):
    """Launch a specific tool"""
    if os.path.exists(tool_path):
        print(f"{Colors.GREEN}[+] Launching tool...{Colors.END}")
        time.sleep(1)
        
        # Get the directory of the tool
        tool_dir = os.path.dirname(tool_path)
        
        # Change to tool directory and run it
        original_dir = os.getcwd()
        try:
            os.chdir(tool_dir)
            tool_file = os.path.basename(tool_path)
            
            print(f"{Colors.YELLOW}[*] Starting tool in: {tool_dir}{Colors.END}")
            print(f"{Colors.CYAN}{'='*60}{Colors.END}")
            
            # Run the tool
            os.system(f'python3 {tool_file}')
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error launching tool: {str(e)}{Colors.END}")
        finally:
            os.chdir(original_dir)
        
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        input(f"\n{Colors.YELLOW}Press Enter to return to main menu...{Colors.END}")
    else:
        print(f"{Colors.RED}[!] Tool not found at: {tool_path}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Make sure the tool is properly installed{Colors.END}")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def main_menu():
    """Display main menu and handle user input"""
    
    # Define available tools with correct paths based on your structure
    TOOLS = {
        "1": {
            "name": "UltraReconX",
            "path": "tools/UltraReconX/UltraReconX.py",
            "description": "Elite Reconnaissance Engine"
        },
        "2": {
            "name": "PantherTechScanUltraX",
            "path": "tools/PantherTechScanUltraX/PantherTechScanUltraX.py",
            "description": "Full Stack Offensive Scanner"
        },
        "3": {
            "name": "LeakHunter-X",
            "path": "tools/LeakHunter-X/LeakHunterX.py",
            "description": "Sensitive Data Hunter"
        },
        "4": {
            "name": "API-GhostScanner",
            "path": "tools/API-GhostScanner/api_ghost_scanner.py",
            "description": "API Security Engine"
        }
    }
    
    while True:
        clear_screen()
        print_banner()
        get_system_info()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║               BCP-CYBERSUITE MAIN LAUNCHER v4.0              ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        print(f"\n{Colors.WHITE}{Colors.BOLD}Available Tools:{Colors.END}\n")
        
        for key, tool in TOOLS.items():
            print(f"  {Colors.GREEN}[{key}]{Colors.END} {Colors.CYAN}{tool['name']:25}{Colors.END} - {tool['description']}")
        
        print(f"\n  {Colors.GREEN}[5]{Colors.END} {Colors.CYAN}System Information{Colors.END}      - Framework status & health")
        print(f"  {Colors.GREEN}[6]{Colors.END} {Colors.CYAN}Update BCP Suite ⟳{Colors.END}     - Latest features & fixes")
        print(f"  {Colors.GREEN}[0]{Colors.END} {Colors.CYAN}Exit{Colors.END}                    - Return to terminal")
        
        print(f"\n{Colors.CYAN}{'─'*60}{Colors.END}")
        
        try:
            choice = input(f"\n{Colors.YELLOW}{Colors.BOLD}Select an option [0-6]: {Colors.END}").strip()
            
            if choice == "0":
                print(f"\n{Colors.GREEN}[+] Thank you for using BCP-CyberSuite!{Colors.END}")
                print(f"{Colors.CYAN}[*] Stay secure with Bangladesh Cyber Panthers{Colors.END}\n")
                sys.exit(0)
                
            elif choice == "5":
                clear_screen()
                print_banner()
                get_system_info()
                print(f"\n{Colors.GREEN}[+] Framework Directory: {os.getcwd()}{Colors.END}")
                print(f"{Colors.GREEN}[+] Available Memory: {os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.**3):.2f} GB{Colors.END}")
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
            elif choice == "6":
                update_framework()
                
            elif choice in TOOLS:
                tool = TOOLS[choice]
                show_tool_info(tool['name'], tool['path'])
                
            else:
                print(f"{Colors.RED}[!] Invalid choice. Please select a valid option.{Colors.END}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[!] Interrupted by user{Colors.END}")
            confirm = input(f"{Colors.CYAN}Are you sure you want to exit? (y/n): {Colors.END}").strip().lower()
            if confirm == 'y':
                print(f"\n{Colors.GREEN}[+] Thank you for using BCP-CyberSuite!{Colors.END}\n")
                sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {str(e)}{Colors.END}")
            time.sleep(2)

def main():
    """Main entry point"""
    try:
        # Check if running as root (not recommended)
        if os.geteuid() == 0:
            print(f"{Colors.RED}[!] Warning: Running as root is not recommended!{Colors.END}")
            print(f"{Colors.YELLOW}[*] Consider running as a regular user{Colors.END}")
            time.sleep(2)
        
        # Clear screen and show banner
        clear_screen()
        print_banner()
        
        # Check dependencies
        if not check_dependencies():
            print(f"{Colors.RED}[!] Please install missing dependencies and try again.{Colors.END}")
            sys.exit(1)
        
        # Start main menu
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Framework terminated by user{Colors.END}")
        print(f"{Colors.CYAN}[*] Goodbye!{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[!] Critical error: {str(e)}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Please report this issue on GitHub{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
