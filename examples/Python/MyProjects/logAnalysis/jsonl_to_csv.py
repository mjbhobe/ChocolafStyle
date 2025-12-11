import json
import csv
import pathlib

script_dir = pathlib.Path(__file__).parent

INPUT_FILE = script_dir / "data" / "newrelic_sample_logs_50000.jsonl"
OUTPUT_FILE = script_dir / "data" / "newrelic_sample_logs_50000.csv"


def jsonl_to_csv(jsonl_path, csv_path):
    all_keys = set()
    rows = []

    # ---- 1. Read JSONL and collect keys ----
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            rows.append(obj)
            all_keys.update(obj.keys())  # collect all keys seen anywhere

    fieldnames = sorted(all_keys)

    # ---- 2. Write CSV ----
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for obj in rows:
            writer.writerow(obj)

    print(f"Converted {len(rows)} JSONL rows → {csv_path}")
    print(f"Total columns: {len(fieldnames)}")


if __name__ == "__main__":
    jsonl_to_csv(str(INPUT_FILE), str(OUTPUT_FILE))
