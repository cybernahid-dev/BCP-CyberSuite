import json
import os

class DataStore:
    def __init__(self, target):
        self.target = target               # FIXED
        self.data = {}                     # FIXED: store everything in a dict
        self.path = f"data/{self.target.replace('://','_')}"

        os.makedirs(self.path, exist_ok=True)

    def save(self, key, value):
        """ Save module output """
        self.data[key] = value             # SAVE INTO MAIN DATA DICT
        
        try:
            with open(f"{self.path}/{key}.json", "w") as f:
                json.dump(value, f, indent=4, default=str)
        except Exception as e:
            print(f"[ERROR] Failed to save {key}: {e}")

    def get_all(self):
        return self.data                   # Return everything (for report)
