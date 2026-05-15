import os
import pickle
import json
import numpy as np
import faiss


# =========================
# CONFIG
# =========================

VECTOR_DIR = "dataset/data/vector_store"
EMBEDDINGS_PATH = os.path.join(VECTOR_DIR, "embeddings.npy")
CHUNKS_PATH = os.path.join(VECTOR_DIR, "chunks.pkl")

OUTPUT_INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
OUTPUT_META_PATH = os.path.join(VECTOR_DIR, "faiss_meta.pkl")


# =========================
# INDEX BUILDER CLASS
# =========================

class FAISSIndexBuilder:
    def __init__(self):
        self.embeddings = None
        self.chunks = None
        self.index = None

    # -------------------------
    # LOAD DATA
    # -------------------------

    def load_data(self):
        print("[INFO] Loading embeddings...")

        self.embeddings = np.load(EMBEDDINGS_PATH)

        print(f"[INFO] Embeddings shape: {self.embeddings.shape}")

        print("[INFO] Loading chunks...")

        with open(CHUNKS_PATH, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"[INFO] Loaded {len(self.chunks)} chunks")

    # -------------------------
    # BUILD INDEX
    # -------------------------

    def build_index(self):
        print("[INFO] Building FAISS index...")

        dim = self.embeddings.shape[1]

        # Inner product (cosine similarity since embeddings are normalized)
        self.index = faiss.IndexFlatIP(dim)

        self.index.add(self.embeddings)

        print(f"[INFO] FAISS index built with {self.index.ntotal} vectors")

    # -------------------------
    # SAVE INDEX
    # -------------------------

    def save(self):
        print("[INFO] Saving FAISS index...")

        faiss.write_index(self.index, OUTPUT_INDEX_PATH)

        with open(OUTPUT_META_PATH, "wb") as f:
            pickle.dump(self.chunks, f)

        print(f"[INFO] Index saved to {OUTPUT_INDEX_PATH}")
        print(f"[INFO] Metadata saved to {OUTPUT_META_PATH}")

    # -------------------------
    # TEST SEARCH
    # -------------------------

    def test_search(self, query_vector):
        D, I = self.index.search(query_vector, k=5)

        print("\n[DEBUG] TOP-5 RESULTS:")

        for rank, idx in enumerate(I[0]):
            chunk = self.chunks[idx]

            print(f"\nRank {rank + 1}")
            print(f"Category: {chunk['category']}")
            print(f"Subtype: {chunk.get('subtype')}")
            print(f"Text: {chunk['text'][:200]}...")


    # -------------------------
    # RUN PIPELINE
    # -------------------------

    def run(self):
        self.load_data()
        self.build_index()
        self.save()


# =========================
# MAIN
# =========================

def main():
    builder = FAISSIndexBuilder()
    builder.run()


if __name__ == "__main__":
    main()