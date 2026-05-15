import json
import os
from datetime import datetime, UTC

INPUT_FILE = "data/raw/team_dataset.json"
OUTPUT_FILE = "data/processed/documents.json"


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_documents(dataset):
    documents = []
    doc_id = 0

    for team in dataset:

        # =====================
        # TEAM DOCUMENT
        # =====================
        doc_id += 1

        documents.append({
            "doc_id": doc_id,
            "title": f"{team['name']}",
            "text": (
                f"{team['name']} has rating {team.get('rating')}. "
                f"Wins: {team.get('wins')} Losses: {team.get('losses')}."
            ),
            "current_roster": f"{[p.get('name') for p in team.get("players", []) if p.get('is_current_team_member')]}",
            "category": "team",
            "source": "OpenDota",
            "scraped_at": team["scraped_at"]
        })

        # =====================
        # MATCH DOCUMENTS
        # =====================
        for m in team.get("matches", []):

            doc_id += 1

            documents.append({
                "doc_id": doc_id,
                "title": f"{team['name']} match {m.get('match_id')}",
                "match_id": f"{m.get('match_id')}",
                "text": (
                    f"Match {team['name']} VS {m.get('opposing_team_name')} at the {m.get('league_name')}. "
                    f"{team['name']} is {'radiant' if m.get('radiant') else 'dire'}. "
                    f"{team['name']} is {'win' if (m.get('radiant') and m.get('radiant_win')) or (not m.get('radiant') and not m.get('radiant_win')) else 'loss'}. "
                    f"Radiant score: {m.get('radiant_score')}. "
                    f"Dire score: {m.get('dire_score')}."
                ),
                "league_name": m.get("league_name"),
                "team_name": team['name'],
                "opposing_team_name": m.get("opposing_team_name"),
                "match_result": f"{team['name']} is {'win' if (m.get('radiant') and m.get('radiant_win')) or (not m.get('radiant') and not m.get('radiant_win')) else 'loss'}. ",
                "category": "match",
                "duration": m.get("duration"),
                "radiant": m.get("radiant"),
                "radiant_score": m.get("radiant_score"),
                "dire_score": m.get("dire_score"),
                "start_time_unix": m.get("start_time"),
                "start_time_iso": datetime.fromtimestamp(m.get("start_time"), UTC).isoformat(),
                "source": "OpenDota",
                "scraped_at": team["scraped_at"]
            })

        # =====================
        # PLAYER DOCUMENTS
        # =====================
        for p in team.get("players", []):

            doc_id += 1

            documents.append({
                "doc_id": doc_id,
                "title": f"Player {p.get('name')}",
                "nickname": f"{p.get('name')}",
                "text": (
                    f"Player {p.get('name')} played {p.get('games_played')} games "
                    f"for team {team['name']}."
                ),
                "category": "player",
                "currently_team": team['name'],
                "source": "OpenDota",
                "scraped_at": team["scraped_at"]
            }) if p.get('is_current_team_member') else None

    return documents


def save_documents(docs):
    os.makedirs("data/processed", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Saved {len(docs)} documents")


def main():
    dataset = load_data()
    docs = build_documents(dataset)
    save_documents(docs)


if __name__ == "__main__":
    main()