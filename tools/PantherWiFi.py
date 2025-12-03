import subprocess

def run():
    print("Scanning nearby WiFi networks...")
    try:
        result = subprocess.check_output(['termux-wifi-scaninfo']).decode()
        print(result)
    except Exception as e:
        print(f"Error: {e}")
