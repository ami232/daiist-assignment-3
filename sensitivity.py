"""Exact, API-free effects of chunking choices on this corpus.

This measures structure and resource requirements, not retrieval or answer
accuracy. No simulated score is ever presented as an observed benchmark.
"""

import json
import statistics

from ingestion import digest, extract
from runtime import ROOT, read_config


def measure(words: int, overlap: int, documents: list[dict]) -> dict:
    lengths, texts = [], []
    for document in documents:
        for _, text in document["sections"]:
            tokens = text.split()
            for start in range(0, len(tokens), words - overlap):
                part = tokens[start : start + words]
                if not part:
                    continue
                lengths.append(len(part))
                texts.append(digest(" ".join(part)))
                if start + words >= len(tokens):
                    break
    count = len(lengths)
    return {
        "words": words,
        "overlap": overlap,
        "overlap_fraction": overlap / words,
        "chunks": count,
        "unique_texts": len(set(texts)),
        "indexed_words_including_overlap": sum(lengths),
        "mean_actual_chunk_words": statistics.mean(lengths),
        "max_actual_chunk_words": max(lengths),
        "raw_vector_bytes_768_float32": count * 768 * 4,
        "cosine_coordinates_768_per_exhaustive_query": count * 768,
    }


def main():
    config = read_config(approved=False)
    docs = [{**d, "sections": extract(ROOT / d["path"])} for d in config["documents"]]
    total = sum(len(text.split()) for d in docs for _, text in d["sections"])
    grid = [
        measure(words, round(words * fraction), docs)
        for words in [150, 200, 300, 400, 600, 900]
        for fraction in [0, 0.1, 0.2, 0.3, 0.5]
    ]
    for row in grid:
        row["duplication_factor"] = row["indexed_words_including_overlap"] / total
    baseline = next(r for r in grid if r["words"] == 300 and r["overlap"] == 60)
    alternative = next(r for r in grid if r["words"] == 600 and r["overlap"] == 120)
    # Count unique embeddings across both designs; identical short pages are shared.
    all_texts = set()
    for design in config["designs"]:
        from ingestion import chunks

        for document in config["documents"]:
            all_texts.update(
                digest(c["text"])
                for c in chunks(
                    ROOT / document["path"],
                    document["source"],
                    design["words"],
                    design["overlap"],
                )
            )
    result = {
        "scope": "Exact structural measurements; no Gemini calls, no accuracy claims.",
        "clean_words": total,
        "source_words": {
            d["source"]: sum(len(t.split()) for _, t in d["sections"]) for d in docs
        },
        "baseline": baseline,
        "alternative": alternative,
        "combined_unique_embedding_texts": len(all_texts),
        "grid": grid,
        "bounds": {
            "k_1_small_max_context_words": 300,
            "k_3_small_max_context_words": 900,
            "k_5_small_max_context_words": 1500,
            "k_5_large_max_context_words": 3000,
        },
        "limitations": [
            "Bounded page/section chunks mean counts are not simply total_words/chunk_size.",
            "Float32 vector bytes are a theoretical payload; SQLite JSON storage has additional overhead.",
            "Changing top-k reuses document embeddings but changes answer context.",
            "Changing embedding dimensions requires a fresh compatible index.",
            "Cosine ranking is not a calibrated answer probability.",
            "No effect on answer correctness or refusal rate can be inferred without evaluation.",
        ],
    }
    (ROOT / "review").mkdir(exist_ok=True)
    path = ROOT / "review" / "structural_sensitivity.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                k: result[k]
                for k in [
                    "clean_words",
                    "source_words",
                    "baseline",
                    "alternative",
                    "combined_unique_embedding_texts",
                ]
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
