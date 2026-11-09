
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "generated" / "refund_policy.txt"


def retrieve(query, policy_text, top_k=3):
    chunks = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", policy_text)
        if sentence.strip()
    ]

    terms = {
        word.lower()
        for word in re.findall(r"[a-zA-Z]+", query)
        if len(word) > 2
    }

    scored = []

    for chunk in chunks:
        words = set(
            re.findall(r"[a-zA-Z]+", chunk.lower())
        )
        score = len(terms & words)
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)

    return [
        chunk
        for score, chunk in scored[:top_k]
        if score > 0
    ]


def answer(query):
    if not POLICY.exists():
        return (
            "Agriculture knowledge file not found. "
            "Run: python -m src.generate_data"
        )

    policy = POLICY.read_text(encoding="utf-8")
    passages = retrieve(query, policy)

    if not passages:
        return (
            "I could not find relevant information in the "
            "demo agriculture knowledge file. "
            "Please consult an agriculture expert. "
            "I will not invent agricultural advice."
        )

    return (
        "Based only on the Smart Agriculture demo knowledge file:\n- "
        + "\n- ".join(passages)
        + "\n\nThis is a simple RAG retrieval prototype, "
        "not an external LLM. Consult an agriculture expert "
        "before making farming decisions."
    )


if __name__ == "__main__":
    print("Smart Agriculture Knowledge Assistant")
    print("Type 'quit' to exit.\n")

    while True:
        query = input(
            "Ask an agriculture question (or 'quit'): "
        ).strip()

        if query.lower() in {"quit", "exit"}:
            print("Thank you for using Agriculture Assistant!")
            break

        if not query:
            print("Please enter a question.\n")
            continue

        print(answer(query))
        print()
