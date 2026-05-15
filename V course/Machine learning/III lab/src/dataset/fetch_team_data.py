import requests
import json
import os
from datetime import datetime

TEAMS_FILE = "data/raw/teams.json"
OUTPUT_FILE = "data/raw/team_dataset.json"

BASE_URL = "https://api.opendota.com/api"


def load_teams():
    with open(TEAMS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_team_matches(team_id):
    url = f"{BASE_URL}/teams/{team_id}/matches"
    r = requests.get(url)

    if r.status_code != 200:
        return []

    return r.json()


def fetch_team_players(team_id):
    url = f"{BASE_URL}/teams/{team_id}/players"
    r = requests.get(url)

    if r.status_code != 200:
        return []

    return r.json()


def normalize_team(team):
    team_id = team.get("team_id")

    print(f"[INFO] Processing team {team.get('name')}")

    matches = fetch_team_matches(team_id)
    players = fetch_team_players(team_id)

    return {
        "team_id": team_id,
        "name": team.get("name"),
        "rating": team.get("rating"),
        "wins": team.get("wins"),
        "losses": team.get("losses"),

        "matches": [
            {
                "match_id": m.get("match_id"),
                "radiant": m.get("radiant"),
                "radiant_win": m.get("radiant_win"),
                "radiant_score": m.get("radiant_score"),
                "dire_score": m.get("dire_score"),
                "duration": m.get("duration"),
                "leagueid": m.get("leagueid"),
                "league_name": m.get("league_name"),
                "opposing_team_id": m.get("opposing_team_id"),
                "opposing_team_name": m.get("opposing_team_name"),
                "start_time": m.get("start_time"),
            }
            for m in matches[:100]
        ],

        "players": [
            {
                "account_id": p.get("account_id"),
                "name": p.get("name"),
                "games_played": p.get("games_played"),
                "wins": p.get("wins"),
                "is_current_team_member": p.get("is_current_team_member"),
            }
            for p in players
        ],

        "scraped_at": datetime.utcnow().isoformat()
    }


def main():
    teams = load_teams()

    dataset = []

    for team in teams:
        try:
            dataset.append(normalize_team(team))
        except Exception as e:
            print(f"[WARN] Failed for team {team.get('name')}: {e}")

    os.makedirs("data/raw", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Saved dataset with {len(dataset)} teams")


if __name__ == "__main__":
    main()