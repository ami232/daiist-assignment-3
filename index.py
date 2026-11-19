import json
import time
from pathlib import Path

from google import genai

from api_key import load_api_key
from vector_store import open_store, store_chunk


ROOT = Path(__file__).resolve().parent
CHUNKS_FILE = ROOT / "corpus" / "chunks.jsonl"
PAUSE_SECONDS = 0.75


def main():
    with CHUNKS_FILE.open(encoding="utf-8") as file:
        chunks = [json.loads(line) for line in file if line.strip()]

    if not chunks:
        raise ValueError("chunks.jsonl is empty. Run chunk_corpus.py first.")

    total = len(chunks)
    counts = {"saved": 0, "reused": 0}
    db = open_store()

    try:
        with genai.Client(api_key=load_api_key()) as client:
            for position, chunk in enumerate(chunks, start=1):
                try:
                    status = store_chunk(db, client, chunk)
                except Exception:
                    print(
                        f"Stopped at {position}/{total}: {chunk['id']}",
                        flush=True,
                    )
                    raise

                counts[status] += 1

                if position == 1 or position % 25 == 0 or position == total:
                    print(
                        f"{position}/{total} | "
                        f"saved: {counts['saved']} | reused: {counts['reused']}",
                        flush=True,
                    )

                if status == "saved" and position < total:
                    time.sleep(PAUSE_SECONDS)
    finally:
        db.close()


if __name__ == "__main__":
    main()