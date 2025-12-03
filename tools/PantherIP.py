import requests
import json

def run():
    ip = input("Enter IP address: ")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            print("\n--- IP Information ---")
            print(f"IP: {data['query']}")
            print(f"Country: {data['country']} | Region: {data['regionName']} | City: {data['city']}")
            print(f"ISP: {data['isp']} | Org: {data['org']}")
            print(f"Timezone: {data['timezone']}")
        else:
            print("Failed to fetch info.")
    except Exception as e:
        print(f"Error: {e}")
