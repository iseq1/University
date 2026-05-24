import json
import os
import pickle
from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer



CHUNKS_PATH = "dataset/data/processed/chunks.json"
OUTPUT_DIR = "dataset/data/vector_store"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"



class EmbeddingPipeline:
    def __init__(self,
                 model_name: str = EMBEDDING_MODEL_NAME,
                 chunks_path: str = CHUNKS_PATH,
                 output_dir: str = OUTPUT_DIR):

        self.model_name = model_name
        self.chunks_path = chunks_path
        self.output_dir = output_dir

        self.model = None
        self.chunks = []
        self.embeddings = None


    def load_model(self):
        print(f"[INFO] Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)


    def load_chunks(self):
        print(f"[INFO] Loading chunks from: {self.chunks_path}")

        with open(self.chunks_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        print(f"[INFO] Loaded {len(self.chunks)} chunks")


    def generate_embeddings(self, batch_size: int = 32):
        if self.model is None:
            raise Exception("Model not loaded. Call load_model() first.")

        texts = [chunk["text"] for chunk in self.chunks]

        print("[INFO] Generating embeddings...")

        self.embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        print(f"[INFO] Embeddings shape: {self.embeddings.shape}")


    def save(self):
        os.makedirs(self.output_dir, exist_ok=True)

        # Save embeddings
        embeddings_path = os.path.join(self.output_dir, "embeddings.npy")
        np.save(embeddings_path, self.embeddings)

        # Save chunks metadata (for retrieval mapping)
        chunks_path = os.path.join(self.output_dir, "chunks.pkl")
        with open(chunks_path, "wb") as f:
            pickle.dump(self.chunks, f)

        # Save config
        config_path = os.path.join(self.output_dir, "config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({
                "model_name": self.model_name,
                "num_chunks": len(self.chunks),
                "embedding_dim": self.embeddings.shape[1]
            }, f, indent=2)

        print(f"[INFO] Saved embeddings to {embeddings_path}")
        print(f"[INFO] Saved metadata to {chunks_path}")


    def run(self):
        self.load_model()
        self.load_chunks()
        self.generate_embeddings()
        self.save()



def main():
    pipeline = EmbeddingPipeline()
    pipeline.run()


if __name__ == "__main__":
    main()