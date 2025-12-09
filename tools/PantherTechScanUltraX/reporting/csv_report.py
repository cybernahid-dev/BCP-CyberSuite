import csv, os

def generate_csv_report(store):
    os.makedirs("reports/csv", exist_ok=True)
    out = f"reports/csv/{store.target}-report.csv"

    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for key, value in store.data.items():
            writer.writerow([key, str(value)])
