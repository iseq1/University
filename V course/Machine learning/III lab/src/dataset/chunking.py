import json
import os
from typing import List, Dict

INPUT_FILE = "data/processed/documents.json"
OUTPUT_FILE = "data/processed/chunks.json"



def load_documents() -> List[Dict]:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def chunk_team(doc: Dict, chunk_id_start: int):
    chunks = []
    chunk_id = chunk_id_start

    team_name = doc.get("title", "Unknown Team")

    # --- 1. General info ---
    chunks.append({
        "chunk_id": chunk_id,
        "doc_id": doc["doc_id"],
        "category": "team",
        "subtype": "general",
        "text": doc.get("title", ""),
        "source": doc.get("source")
    })
    chunk_id += 1

    # --- 2. Stats ---
    stats_text = f"Team performance stats: {doc.get('text', '')}"
    chunks.append({
        "chunk_id": chunk_id,
        "doc_id": doc["doc_id"],
        "category": "team",
        "subtype": "stats",
        "text": stats_text,
        "source": doc.get("source")
    })
    chunk_id += 1

    # --- 3. Compact team roster ---
    chunks.append({
        "chunk_id": chunk_id,
        "doc_id": doc["doc_id"],
        "category": "team",
        "subtype": "roster",
        "text": f"{team_name} roster: {doc.get('current_roster', [])}",
        "source": doc.get("source")
    })
    chunk_id += 1

    return chunks, chunk_id



def chunk_match(doc: Dict, chunk_id_start: int):
    chunks = []
    chunk_id = chunk_id_start

    # --- 1. Description chunk ---
    desc_text = f"{doc.get('title', '')}: {doc.get('team_name', '')} VS {doc.get('opposing_team_name', '')} at the {doc.get('league_name')}."

    chunks.append({
        "chunk_id": chunk_id,
        "doc_id": doc["doc_id"],
        "category": "match",
        "subtype": "description",
        "text": desc_text,
        "source": doc.get("source")
    })
    chunk_id += 1

    # --- 2. Result-focused chunk ---
    result_text = (
        f"Match {doc.get('match_id', '')} result summary: "
        f"{doc.get('match_result', '')}"
        f"Final score: "
        f"[{doc.get('team_name', '')}] {doc.get('radiant_score', '') if doc.get('radiant') else doc.get('dire_score', '')}"
        f" VS "
        f"{doc.get('dire_score', '') if doc.get('radiant') else doc.get('radiant_score', '')} [{doc.get('opposing_team_name', '')}]"
    )

    chunks.append({
        "chunk_id": chunk_id,
        "doc_id": doc["doc_id"],
        "category": "match",
        "subtype": "result",
        "text": result_text,
        "source": doc.get("source")
    })
    chunk_id += 1

    return chunks, chunk_id



def chunk_player(doc: Dict, chunk_id_start: int):
    chunks = []
    chunk_id = chunk_id_start

    chunks.append({
        "chunk_id": chunk_id,
        "doc_id": doc["doc_id"],
        "category": "player",
        "subtype": "profile",
        "text": doc.get("text", ""),
        "source": doc.get("source")
    })

    chunk_id += 1
    return chunks, chunk_id



def build_chunks(doc: Dict, chunk_id_start: int):
    category = doc.get("category")

    if category == "team":
        return chunk_team(doc, chunk_id_start)

    elif category == "match":
        return chunk_match(doc, chunk_id_start)

    elif category == "player":
        return chunk_player(doc, chunk_id_start)

    else:
        # fallback safe chunk
        return [{
            "chunk_id": chunk_id_start,
            "doc_id": doc["doc_id"],
            "category": category,
            "subtype": "unknown",
            "text": doc.get("text", ""),
            "source": doc.get("source")
        }], chunk_id_start + 1



def main():
    print("[INFO] Loading documents...")
    docs = load_documents()

    all_chunks = []
    chunk_id = 1

    print("[INFO] Building semantic chunks...")

    for doc in docs:
        chunks, chunk_id = build_chunks(doc, chunk_id)
        all_chunks.extend(chunks)

    os.makedirs("data/processed", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Total chunks created: {len(all_chunks)}")
    print(f"[INFO] Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()