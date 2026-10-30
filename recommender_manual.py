"""Content-based recommendations using a small, explicit TF-IDF implementation."""

from __future__ import annotations

import math
import re
from collections import Counter

from dataset import load_documents


TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:['’][a-z0-9]+)*", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def build_idf(document_tokens: list[list[str]]) -> dict[str, float]:
    document_frequency = Counter()
    for tokens in document_tokens:
        document_frequency.update(set(tokens))

    total_documents = len(document_tokens)
    return {
        token: math.log((total_documents + 1) / (frequency + 1)) + 1
        for token, frequency in document_frequency.items()
    }


def vectorize(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    counts = Counter(tokens)
    token_count = len(tokens)
    if token_count == 0:
        return {}

    return {
        token: (count / token_count) * idf[token]
        for token, count in counts.items()
        if token in idf
    }


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0

    dot_product = sum(value * right.get(token, 0.0) for token, value in left.items())
    return dot_product / (left_norm * right_norm)


def main() -> None:
    documents = load_documents()
    document_tokens = [tokenize(summary) for _, summary in documents]
    idf = build_idf(document_tokens)

    query = input("Describe the kind of movie you want: ").strip()
    query_vector = vectorize(tokenize(query), idf)
    if not query_vector:
        print("No query words matched the dataset vocabulary.")
        return

    ranked = []
    for (title, _), tokens in zip(documents, document_tokens):
        score = cosine_similarity(query_vector, vectorize(tokens, idf))
        if score > 0:
            ranked.append((title, score))

    ranked.sort(key=lambda item: (-item[1], item[0]))
    if not ranked:
        print("No matching movies were found.")
        return

    for rank, (title, score) in enumerate(ranked[:6], start=1):
        print(f"{rank}. {title} — similarity {score:.3f}")


if __name__ == "__main__":
    main()
