import json
from datetime import datetime
from requests.structures import CaseInsensitiveDict


def convert(obj):
    """Safely convert ANY non-serializable object to JSON-safe dict/list/str."""
    
    # Already JSON-safe
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj

    # Dictionaries
    if isinstance(obj, dict) or isinstance(obj, CaseInsensitiveDict):
        return {str(k): convert(v) for k, v in obj.items()}

    # Lists / Tuples / Sets
    if isinstance(obj, (list, tuple, set)):
        return [convert(i) for i in obj]

    # Bytes → string
    if isinstance(obj, bytes):
        try:
            return obj.decode("utf-8", errors="ignore")
        except:
            return str(obj)

    # Other unknown objects → make string
    return str(obj)


def generate_json_report(store):
    """Generate fully sanitized JSON report without any serialization errors."""

    try:
        output_file = "report.json"

        # Ensure store has .data attribute
        if not hasattr(store, "data"):
            print("[ERROR] DataStore missing .data attribute — fixed required!")
            return

        safe_data = convert(store.data)

        # Add metadata
        safe_data["_generated_at"] = datetime.now().isoformat()

        with open(output_file, "w") as f:
            json.dump(safe_data, f, indent=4)

        print(f"[✔] JSON report saved as: {output_file}")

    except Exception as e:
        print(f"[ERROR] JSON report failed: {e}")
