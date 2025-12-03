from tools import PantherIP, PantherPortScan, PantherWiFi, PantherPhish, PantherSMS, PantherVuln

def main():
    print("=== Bangladesh Cyber Panthers Suite ===")
    print("1. PantherIP (IP Info & Geo)")
    print("2. PantherPortScan (Advanced Port Scanner)")
    print("3. PantherWiFi (WiFi Analyzer)")
    print("4. PantherPhish (Phishing Detector)")
    print("5. PantherSMS (SMS Spam Detector)")
    print("6. PantherVuln (Vulnerability Scanner)")
    
    choice = input("Choose a tool (1-6): ")
    
    if choice == "1":
        PantherIP.run()
    elif choice == "2":
        PantherPortScan.run()
    elif choice == "3":
        PantherWiFi.run()
    elif choice == "4":
        PantherPhish.run()
    elif choice == "5":
        PantherSMS.run()
    elif choice == "6":
        PantherVuln.run()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
