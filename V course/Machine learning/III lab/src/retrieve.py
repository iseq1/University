import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer



VECTOR_DIR = "dataset/data/vector_store"

INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
META_PATH = os.path.join(VECTOR_DIR, "faiss_meta.pkl")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"



class RAGRetriever:
    def __init__(self):
        self.index = None
        self.chunks = None
        self.model = None


    def load(self):
        print("[INFO] Loading FAISS index...")

        self.index = faiss.read_index(INDEX_PATH)

        print("[INFO] Loading chunk metadata...")

        with open(META_PATH, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"[INFO] Loaded {len(self.chunks)} chunks")

        print("[INFO] Loading embedding model...")

        self.model = SentenceTransformer(EMBEDDING_MODEL)


    def embed_query(self, query: str):
        return self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True
        )


    def search(self, query: str, top_k: int = 5):
        query_vec = self.embed_query(query)

        scores, indices = self.index.search(query_vec, top_k)

        results = []

        print("\n[DEBUG] QUERY:", query)

        for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):

            chunk = self.chunks[idx]

            result = {
                "rank": rank + 1,
                "score": float(score),
                "chunk_id": chunk["chunk_id"],
                "doc_id": chunk["doc_id"],
                "category": chunk.get("category"),
                "subtype": chunk.get("subtype"),
                "text": chunk["text"]
            }

            results.append(result)

            # DEBUG PRINT
            print("\n--------------------")
            print(f"Rank: {rank + 1}")
            print(f"Score: {score:.4f}")
            print(f"Category: {chunk.get('category')} | {chunk.get('subtype')}")
            print(f"Text: {chunk['text'][:250]}...")

        return results


    def search_filtered(self, query: str, category: str = None, top_k: int = 5):
        results = self.search(query, top_k=top_k * 3)

        if category:
            results = [r for r in results if r["category"] == category]

        return results[:top_k]



def main():
    retriever = RAGRetriever()
    retriever.load()

    print("\n=== RAG READY ===\n")

    while True:
        query = input("\nEnter query (or 'exit'): ")

        if query.lower() == "exit":
            break

        retriever.search(query, top_k=5)


if __name__ == "__main__":
    main()