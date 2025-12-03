import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, port))
        print(f"[OPEN] Port {port}")
        s.close()
    except:
        pass

def run():
    ip = input("Enter target IP: ")
    print("Scanning top 100 ports...")
    ports = [21,22,23,25,53,80,110,443,445,8080,3306,5900, etc] # Add more as needed
    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in ports:
            executor.submit(scan_port, ip, port)
