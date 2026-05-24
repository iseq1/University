import requests
import json
import os

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "teams.json"

API_URL = "https://api.opendota.com/api/teams"


def fetch_teams(limit=50):
    print("[INFO] Fetching teams...")

    response = requests.get(API_URL)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")

    teams = response.json()

    # сортируем по rating
    teams = sorted(teams, key=lambda x: x.get("rating", 0), reverse=True)

    return teams[:limit]


def save(data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Saved to {path}")


def main():
    teams = fetch_teams(limit=50)
    save(teams)


if __name__ == "__main__":
    main()