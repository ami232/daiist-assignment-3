"""Extract source text and persist versioned chunk embeddings."""

import hashlib
import json
import math
import re
import sqlite3
from pathlib import Path


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract(path):
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        return [
            (f"PDF page {i + 1}", p.extract_text() or "")
            for i, p in enumerate(PdfReader(path).pages)
        ]
    if path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError(
            "Supported inputs: PDF, TXT, MD. Convert HTML to clean text first."
        )
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^<!-- source-location: (.+?) -->\s*$", text, flags=re.MULTILINE)
    if len(parts) > 1:
        return [
            (parts[i], parts[i + 1].strip())
            for i in range(1, len(parts), 2)
            if parts[i + 1].strip()
        ]
    return [("text", text)]


def chunks(path, source, words, overlap):
    if words < 1 or overlap < 0 or overlap >= words:
        raise ValueError("Require words > overlap >= 0")
    out = []
    for location, text in extract(path):
        tokens = re.findall(r"\S+", text)
        for start in range(0, len(tokens), words - overlap):
            piece = " ".join(tokens[start : start + words])
            if not piece:
                continue
            loc = f"{location}; words {start + 1}-{min(start + words, len(tokens))}"
            out.append(
                {
                    "id": digest(source + "\0" + loc + "\0" + piece),
                    "source": source,
                    "location": loc,
                    "text": piece,
                }
            )
            if start + words >= len(tokens):
                break
    return out


class VectorStore:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS vectors (id TEXT PRIMARY KEY, model TEXT NOT NULL, text TEXT NOT NULL, vector TEXT NOT NULL)"
        )
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS chunks (design TEXT, id TEXT, source TEXT, location TEXT, text TEXT, embedding_id TEXT, PRIMARY KEY(design,id))"
        )

    def add(self, design, items, model, embed):
        return self.add_many({design: items}, model, embed)

    def add_many(self, designs, model, embed, progress=None):
        # Save each embedding immediately, but activate all designs atomically.
        rows = []
        calls = 0
        for design, items in designs.items():
            for c in items:
                eid = digest(model + "\0" + c["text"])
                found = self.db.execute(
                    "SELECT 1 FROM vectors WHERE id=?", (eid,)
                ).fetchone()
                if not found:
                    vector = list(map(float, embed(c["text"])))
                    if (
                        not vector
                        or not all(math.isfinite(x) for x in vector)
                        or not any(vector)
                    ):
                        raise ValueError("Invalid embedding")
                    self.db.execute(
                        "INSERT INTO vectors VALUES (?,?,?,?)",
                        (eid, model, c["text"], json.dumps(vector)),
                    )
                    self.db.commit()
                    calls += 1
                    if progress and calls % 25 == 0:
                        progress(calls)
                rows.append(
                    (design, c["id"], c["source"], c["location"], c["text"], eid)
                )
        with self.db:
            for design in designs:
                self.db.execute("DELETE FROM chunks WHERE design=?", (design,))
            self.db.executemany("INSERT INTO chunks VALUES (?,?,?,?,?,?)", rows)
        return calls

    def search(self, design, model, query_vector, k=5):
        q = list(map(float, query_vector))
        qn = math.sqrt(sum(x * x for x in q))
        if not q or not qn or not all(math.isfinite(x) for x in q):
            raise ValueError("Invalid query vector")
        rows = self.db.execute(
            "SELECT c.id,c.source,c.location,c.text,v.vector FROM chunks c JOIN vectors v ON v.id=c.embedding_id WHERE c.design=? AND v.model=?",
            (design, model),
        )
        out = []
        for cid, source, loc, text, v in rows:
            v = json.loads(v)
            if len(v) != len(q):
                raise ValueError("Embedding dimension mismatch")
            score = sum(x * y for x, y in zip(q, v)) / (
                qn * math.sqrt(sum(x * x for x in v))
            )
            out.append(
                {
                    "id": cid,
                    "source": source,
                    "location": loc,
                    "text": text,
                    "score": score,
                }
            )
        return sorted(out, key=lambda c: (-c["score"], c["id"]))[:k]
