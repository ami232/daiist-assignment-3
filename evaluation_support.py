"""Deterministic evaluation checks and blind human/judge comparison."""
import csv
import hashlib
import json
from pathlib import Path

from answer_guardrails import CITATION, canonical_citation, retrieved_passages


def digest(value):
    if isinstance(value, bytes):
        payload = value
    else:
        payload = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def corpus_fingerprint(store):
    h = hashlib.sha256()
    with store.connection() as db:
        rows = db.execute("SELECT c.id,c.source,c.location,c.text,c.embedding_key,v.vector FROM chunks c LEFT JOIN vectors v ON c.embedding_key=v.key ORDER BY c.id").fetchall()
    for row in rows:
        h.update(digest(list(row)[:-1]).encode())
        h.update(row["vector"] or b"missing-vector")
    return h.hexdigest()


def answer_review_hash(answer):
    passages = sorted(({name: passage.get(name) for name in ("id", "source", "location", "text", "citation")}
                       for passage in retrieved_passages(answer["trace"])), key=lambda x: x["id"])
    return digest({"question": answer["question"], "answer": answer["answer"], "passages": passages})


def code_checks(answer):
    passages = retrieved_passages(answer["trace"])
    allowed = {canonical_citation(p["citation"]) for p in passages}
    citations = [canonical_citation(match[0]) for match in CITATION.finditer(answer["answer"])]
    unknown = sorted(set(citations)-allowed)
    return {"successful_search": any(e["tool"] == "search" and e["status"] == "success" for e in answer["trace"]),
            "citation_identity_valid": not unknown, "unknown_citations": unknown,
            "citation_count": len(citations), "guardrail_blocked": answer["guardrail_blocked"],
            "declines_requested_answer": answer["guardrail_blocked"] or (answer.get("draft") or {}).get("status") == "unanswerable"}


def load_human_labels(path, known_ids, minimum=20):
    labels = {}
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not {"id", "correct", "supported", "notes"}.issubset(reader.fieldnames or []):
            raise ValueError("Human labels need id, correct, supported and notes")
        for row in reader:
            if not row["id"].strip():
                continue
            identifier = row["id"].strip()
            if identifier not in known_ids or identifier in labels:
                raise ValueError(f"Unknown or duplicate human label ID: {identifier}")
            if row["correct"].strip() not in {"0", "1"} or row["supported"].strip() not in {"0", "1"}:
                raise ValueError(f"{identifier}: enter your own 0/1 grades for both fields")
            label = {"id": identifier, "correct": int(row["correct"]), "supported": int(row["supported"]), "notes": row["notes"].strip()}
            if (not label["correct"] or not label["supported"]) and not label["notes"]:
                raise ValueError(f"{identifier}: explain every zero grade in notes")
            labels[identifier] = label
    if len(labels) < minimum:
        raise ValueError(f"Human review is incomplete: {len(labels)}/{minimum} graded answers. Grade them before viewing the LLM judge.")
    return labels


def compare_labels(human, judge):
    identifiers = sorted(set(human) & set(judge))
    if not identifiers:
        return {"compared_answers": 0, "correct_agreement": None, "supported_agreement": None, "both_fields_agreement": None}
    result = {"compared_answers": len(identifiers)}
    for field in ("correct", "supported"):
        result[field+"_agreement"] = sum(human[i][field] == judge[i][field] for i in identifiers)/len(identifiers)
        result[field+"_confusion"] = {f"human_{a}_judge_{b}": sum(human[i][field] == a and judge[i][field] == b for i in identifiers)
                                      for a in (0, 1) for b in (0, 1)}
    result["both_fields_agreement"] = sum(all(human[i][field] == judge[i][field] for field in ("correct", "supported")) for i in identifiers)/len(identifiers)
    return result


def verify_human_binding(binding, labels, answers, rubric_hash, labels_hash):
    if binding.get("rubric_sha256") != rubric_hash or binding.get("labels_sha256") != labels_hash:
        raise ValueError("Human labels or rubric changed. Review and bind the labels again before invoking the judge.")
    for identifier in labels:
        if binding.get("reviewed_answers", {}).get(identifier) != answer_review_hash(answers[identifier]):
            raise ValueError(f"{identifier}: human grade is not bound to the current answer and evidence. Review and bind labels again.")
