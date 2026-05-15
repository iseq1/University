import requests
from openai import OpenAI

from retrieve import RAGRetriever


# =========================
# MODELS CONFIG
# =========================

MODELS = {
    "strong": "meta-llama/llama-3-8b-instruct",
    "fast": "mistralai/mistral-7b-instruct",
    "baseline": "qwen/qwen-2.5-7b-instruct"
}

OLLAMA_URL = "http://localhost:11434/api/generate"


# =========================
# PROMPT
# =========================

def build_prompt(query, contexts):
    context_text = "\n\n".join([c["text"] for c in contexts])

    return f"""
Answer using ONLY context.

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:
"""


# =========================
# LLM CALL
# =========================

import requests

def call_llm(prompt: str, model: str = "meta-llama/llama-3-8b-instruct"):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a Dota 2 esports assistant. Answer ONLY based on provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        }
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()["choices"][0]["message"]["content"]


# =========================
# PIPELINE
# =========================

class RAGPipeline:
    def __init__(self):
        self.retriever = RAGRetriever()
        self.retriever.load()

    def retrieve(self, query):
        return self.retriever.search(query, top_k=5)

    def run(self, query, model_type="strong"):
        model = MODELS[model_type]

        print(f"\n[INFO] Using model: {model}")

        contexts = self.retrieve(query)

        prompt = build_prompt(query, contexts)

        print(prompt)

        answer = call_llm(prompt, model)

        print("\n================ ANSWER ================\n")
        print(answer)
        print("\n=======================================\n")

        return answer


# =========================
# CLI
# =========================

def main():
    pipeline = RAGPipeline()

    print("\n=== MULTI-MODEL RAG READY ===")

    while True:
        query = input("\nQuery (or exit): ")

        if query == "exit":
            break

        print("\nSelect model: strong | fast | baseline")
        model = input("Model: ")

        pipeline.run(query, model)


if __name__ == "__main__":
    main()