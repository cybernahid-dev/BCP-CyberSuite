import subprocess

def run():
    print("Checking Termux packages for updates...")
    try:
        result = subprocess.check_output(['pkg', 'list-all']).decode()
        print(result[:1000] + "\n...")  # print top 1000 chars
    except Exception as e:
        print(f"Error: {e}")
