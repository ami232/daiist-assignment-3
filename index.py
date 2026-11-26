"""Build saved-vector indexes from a student-approved corpus and design config."""

import argparse
import json
import sys
from pathlib import Path

from ingestion import VectorStore, chunks, extract

ROOT = Path(__file__).resolve().parent


def write_json(path: Path, data: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def validate_document(document: dict, root: Path = ROOT) -> Path:
    if (
        not document.get("url")
        or not document.get("license")
        or document.get("no_personal_data_confirmed") is not True
    ):
        raise ValueError(
            "Each document requires a public URL, reuse licence and personal-data review."
        )
    if not document.get("source"):
        raise ValueError("Each document needs a unique source ID.")
    path = (root / document["path"]).resolve()
    if not path.is_relative_to((root / "corpus").resolve()):
        raise ValueError("Files must be inside corpus/")
    if not path.is_file():
        raise ValueError(f"Missing corpus document: {document['path']}")
    return path


def prepare(
    config: dict, root: Path = ROOT, *, require_approval: bool = True
) -> tuple[int, dict]:
    if require_approval and not (
        config.get("student_approved") is True
        or config.get("execution_authorized") is True
    ):
        raise ValueError(
            "Jimena must approve corpus and design decisions before indexing."
        )
    documents = config["documents"]
    sources = [d["source"] for d in documents]
    if len(set(sources)) != len(sources):
        raise ValueError("Document source IDs must be unique")
    if len(documents) < 3:
        raise ValueError("At least three documents are required")
    total = 0
    for document in documents:
        path = validate_document(document, root)
        total += sum(len(text.split()) for _, text in extract(path))
    if total < 50000:
        raise ValueError(f"Corpus has {total} words; minimum 50000")
    if len(config["designs"]) < 2:
        raise ValueError("At least two designs required")
    designs = {}
    for design in config["designs"]:
        name = design["name"]
        if not name or name in designs:
            raise ValueError("Design names must be nonempty and unique")
        designs[name] = [
            c
            for d in documents
            for c in chunks(
                root / d["path"], d["source"], design["words"], design["overlap"]
            )
        ]
    if config.get("selected_design") not in designs:
        raise ValueError("selected_design must name one of your designs.")
    return total, designs


def build(config: dict, dry_run: bool = False, root: Path = ROOT) -> dict:
    total, designs = prepare(config, root, require_approval=not dry_run)
    summary = {
        "words": total,
        "chunks": {name: len(items) for name, items in designs.items()},
    }
    if dry_run:
        return summary
    from runtime import embedder, vector_model

    store = VectorStore(root / "index" / "vectors.sqlite3")
    try:
        summary["new_embedding_calls"] = store.add_many(
            designs,
            vector_model(config),
            embedder(config, "RETRIEVAL_DOCUMENT"),
            progress=lambda n: print(
                f"Saved {n} new Gemini vectors (previously saved vectors reused).",
                file=sys.stderr,
                flush=True,
            ),
        )
    finally:
        store.db.close()
    write_json(root / "index" / "manifest.json", {"config": config, "summary": summary})
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(ROOT / "corpus_config.json"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not Path(args.config).exists():
        raise SystemExit(
            "Pending corpus/design choices: corpus_config.json missing. No API call made."
        )
    print(
        json.dumps(
            build(json.loads(Path(args.config).read_text()), args.dry_run), indent=2
        )
    )
