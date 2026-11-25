"""
Assignment 3: evaluation (`main.py evaluate`).

Runs, in order, and writes everything into eval/:

  1. retrieval   hit rate @1/3/5 for four designs, chosen by the numbers
  2. answers     the agent on every question (cached; --refresh to re-run)
  3. checks      what code can check: citation validity, refusals, retrieval hits
  4. judge       an LLM judge with a rubric and the retrieved text as evidence
  5. agreement   judge vs eval/human_labels.csv, raw agreement and Cohen's kappa
  6. failures    every failure classified by cause
  7. cost        tokens and seconds per question

The add-document before/after is a separate one-shot stage, because adding the
document destroys the "before" state and spends ~209 embeddings:

    uv run python evaluate.py --stage demo
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

import index as pipeline

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
BEFORE_AFTER = EVAL_DIR / "before_after.md"

KS = (1, 3, 5)
RETRIEVE_N = max(KS)
RRF_K = 60

# The held-back document and the question it is meant to unlock, for stage `demo`.
DEMO_DOCUMENT = ROOT / "corpus" / "BOCG-15-A-1-2.PDF"
DEMO_QUESTION_ID = ""   # blank = the first unanswerable question in questions.csv

JUDGE_MODEL_ENV = "GEMINI_JUDGE_MODEL"
JUDGE_MAX_RETRIES = 4       # the free tier returns 503 under load; a blank verdict is not a result
REFUSAL = "NO CONSTA EN EL CORPUS"

# Keyword -> trámite, for the metadata-filter design. A deliberately simple heuristic:
# the point is to test whether filtering helps at all, not to build a query classifier.
TRAMITE_CUES = (
    ("proyecto", ("proyecto de ley", "el proyecto", "texto inicial", "presentó el gobierno",
                  "remitió el gobierno", "versión original", "originalmente")),
    ("aprobacion_definitiva", ("texto aprobado", "aprobación definitiva", "ley aprobada",
                               "texto final", "finalmente", "quedó aprobado", "en vigor")),
    ("informe_ponencia", ("ponencia", "informe de la ponencia")),
    ("debate_pleno", ("debate", "pleno", "dijo", "argumentó", "intervención", "portavoz",
                      "votación", "se aprobó con", "defendió")),
)


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def banner(title: str) -> None:
    print(f"\n{'=' * 72}\n  {title}\n{'=' * 72}")


def read_questions() -> list[dict]:
    if not QUESTIONS.is_file():
        return []
    with QUESTIONS.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if (row.get("question") or "").strip()]


def write_csv(path: Path, rows: list[dict]) -> None:
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list({key: None for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    """(expected_source, expected_location) pairs; `;` separates several."""
    sources = [s.strip() for s in (row.get("expected_source") or "").split(";") if s.strip()]
    locations = [s.strip() for s in (row.get("expected_location") or "").split(";") if s.strip()]
    if not sources:
        return []
    if len(locations) < len(sources):
        locations += [""] * (len(sources) - len(locations))
    return list(zip(sources, locations))


def tokenize(text: str) -> list[str]:
    folded = unicodedata.normalize("NFKD", text.lower())
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", folded)


def infer_tramite(question: str) -> str:
    lowered = question.lower()
    for tramite, cues in TRAMITE_CUES:
        if any(cue in lowered for cue in cues):
            return tramite
    return ""


# --------------------------------------------------------------------------
# BM25, for the hybrid design (no extra dependency)
# --------------------------------------------------------------------------

class BM25:
    def __init__(self, documents: list[list[str]], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.documents = documents
        self.count = len(documents)
        self.lengths = np.array([len(d) for d in documents], dtype=np.float32)
        self.avg_length = float(self.lengths.mean()) if self.count else 0.0
        self.frequencies = [Counter(d) for d in documents]
        document_frequency = Counter()
        for document in documents:
            document_frequency.update(set(document))
        self.idf = {
            term: math.log(1 + (self.count - n + 0.5) / (n + 0.5))
            for term, n in document_frequency.items()
        }

    def scores(self, query: list[str]) -> np.ndarray:
        out = np.zeros(self.count, dtype=np.float32)
        if not self.count:
            return out
        for term in query:
            idf = self.idf.get(term)
            if idf is None:
                continue
            for position, frequency in enumerate(self.frequencies):
                f = frequency.get(term, 0)
                if not f:
                    continue
                denominator = f + self.k1 * (1 - self.b + self.b * self.lengths[position] / self.avg_length)
                out[position] += idf * (f * (self.k1 + 1)) / denominator
        return out


def reciprocal_rank_fusion(*rankings: list[int], k: int = RRF_K) -> list[int]:
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank + 1)
    return [item for item, _ in sorted(scores.items(), key=lambda pair: -pair[1])]


# --------------------------------------------------------------------------
# Stage 1: retrieval
# --------------------------------------------------------------------------

def load_strategy(strategy: str) -> dict | None:
    collection = pipeline._collection(strategy)
    if collection.count() == 0:
        return None
    data = collection.get(include=["documents", "metadatas", "embeddings"])
    vectors = np.asarray(data["embeddings"], dtype=np.float32)
    return {
        "ids": data["ids"],
        "texts": data["documents"],
        "metadatas": data["metadatas"],
        "vectors": vectors,
        "bm25": BM25([tokenize(t) for t in data["documents"]]),
    }


_SECTION_PAGES: dict[tuple[str, str], set[int]] | None = None


def _section_pages() -> dict[tuple[str, str], set[int]]:
    """(doc_id, seccion) -> the pages that section spans, read from the structured chunks.

    `fixed_200` chunks carry no `seccion`, and their `location_label` is just
    "doc · p. N", so a section name can never appear in it: scored on the label
    alone that design is incapable of registering a hit, which made the A/B
    comparison meaningless rather than merely unfavourable. Page overlap is the
    unit both designs can satisfy, and it asks the question the hit rate is meant
    to ask: did retrieval return the passage that holds the answer?
    """
    global _SECTION_PAGES
    if _SECTION_PAGES is None:
        mapping: dict[tuple[str, str], set[int]] = {}
        path = ROOT / "index" / "chunks.jsonl"
        if path.is_file():
            for line in path.open(encoding="utf-8"):
                if not line.strip():
                    continue
                chunk = json.loads(line)
                seccion = (chunk.get("seccion") or "").strip().lower()
                page = chunk.get("page")
                if not seccion or page is None:
                    continue
                page_to = chunk.get("page_to") or page
                key = (chunk.get("doc_id"), seccion)
                mapping.setdefault(key, set()).update(range(int(page), int(page_to) + 1))
        _SECTION_PAGES = mapping
    return _SECTION_PAGES


def is_hit(pairs: list[tuple[str, str]], hits: list[dict], strict: bool) -> bool:
    """A pair matches when the doc_id matches and the chunk covers the expected location.

    "Covers" means the section name appears in the label, or - for a chunk with no
    section label at all - the chunk's pages overlap the expected section's pages.
    """
    section_pages = _section_pages()

    def matched(source: str, location: str) -> bool:
        wanted = section_pages.get((source, location.strip().lower()), set())
        for metadata in hits:
            if metadata.get("doc_id") != source:
                continue
            if not location or location.lower() in (metadata.get("location_label") or "").lower():
                return True
            if (metadata.get("seccion") or "").strip() or not wanted:
                continue
            page = metadata.get("page")
            if page is None:
                continue
            page_to = metadata.get("page_to") or page
            if wanted & set(range(int(page), int(page_to) + 1)):
                return True
        return False

    results = [matched(source, location) for source, location in pairs]
    return all(results) if strict else any(results)


def evaluate_retrieval(rows: list[dict]) -> tuple[list[dict], list[dict], str]:
    answerable = [r for r in rows if r["kind"].strip().lower() != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"].strip().lower() == "unanswerable"]
    if not answerable:
        return [], [], pipeline.DEFAULT_STRATEGY

    stores = {name: load_strategy(name) for name in pipeline.STRATEGIES}
    stores = {name: store for name, store in stores.items() if store}
    if not stores:
        print("  index/ holds no vectors. Run `uv run python main.py index` first.")
        return [], [], pipeline.DEFAULT_STRATEGY

    questions = [r["question"] for r in rows]
    vectors = pipeline.embed_texts(questions, task_type="RETRIEVAL_QUERY")
    query_vectors = {q: v for q, v in zip(questions, vectors)}

    detail: list[dict] = []
    top1_similarity: dict[str, list[float]] = {"answerable": [], "unanswerable": []}

    def dense_order(store: dict, vector: np.ndarray, allowed: np.ndarray | None = None) -> tuple[list[int], np.ndarray]:
        similarities = store["vectors"] @ vector
        if allowed is not None:
            similarities = np.where(allowed, similarities, -np.inf)
        return list(np.argsort(-similarities)), similarities

    for row in rows:
        vector = query_vectors[row["question"]]
        pairs = expected_pairs(row)
        kind = row["kind"].strip().lower()
        for name, store in stores.items():
            order, similarities = dense_order(store, vector)
            designs = {name: order}
            if name == pipeline.DEFAULT_STRATEGY:
                tramite = infer_tramite(row["question"])
                if tramite:
                    allowed = np.array([m.get("tramite") == tramite for m in store["metadatas"]])
                    if allowed.any():
                        designs[f"{name}+filtro"] = dense_order(store, vector, allowed)[0]
                    else:
                        designs[f"{name}+filtro"] = order
                else:
                    designs[f"{name}+filtro"] = order
                lexical = list(np.argsort(-store["bm25"].scores(tokenize(row["question"]))))
                designs[f"{name}+hibrido"] = reciprocal_rank_fusion(order[:30], lexical[:30])

            for design, ordering in designs.items():
                record = {"id": row["id"], "kind": kind, "design": design,
                          "tramite_inferido": infer_tramite(row["question"])}
                for k in KS:
                    hits = [store["metadatas"][i] for i in ordering[:k]]
                    record[f"hit@{k}"] = int(is_hit(pairs, hits, strict=True)) if pairs else ""
                    record[f"any@{k}"] = int(is_hit(pairs, hits, strict=False)) if pairs else ""
                record["top1"] = store["metadatas"][ordering[0]].get("location_label", "")
                detail.append(record)
                if design == pipeline.DEFAULT_STRATEGY:
                    bucket = "unanswerable" if kind == "unanswerable" else "answerable"
                    top1_similarity[bucket].append(float(similarities[ordering[0]]))

    designs = list(dict.fromkeys(d["design"] for d in detail))
    summary: list[dict] = []
    for design in designs:
        subset = [d for d in detail if d["design"] == design and d["hit@1"] != ""]
        multi = [d for d in subset if d["kind"] == "multi"]
        line = {"design": design, "questions": len(subset)}
        for k in KS:
            line[f"hit@{k}"] = round(sum(d[f"hit@{k}"] for d in subset) / len(subset), 3) if subset else 0
        for k in KS:
            line[f"multi_estricto@{k}"] = round(sum(d[f"hit@{k}"] for d in multi) / len(multi), 3) if multi else ""
            line[f"multi_laxo@{k}"] = round(sum(d[f"any@{k}"] for d in multi) / len(multi), 3) if multi else ""
        summary.append(line)

    best = max(summary, key=lambda line: (line["hit@1"], line["hit@3"]))["design"] if summary else pipeline.DEFAULT_STRATEGY
    print(f"  {'diseño':<26}{'hit@1':>8}{'hit@3':>8}{'hit@5':>8}{'multi estricto@5':>19}")
    for line in summary:
        print(f"  {line['design']:<26}{line['hit@1']:>8}{line['hit@3']:>8}{line['hit@5']:>8}"
              f"{str(line['multi_estricto@5']):>19}")
    print(f"\n  mejor diseño por hit@1: {best}")

    if top1_similarity["answerable"] and top1_similarity["unanswerable"]:
        a = sum(top1_similarity["answerable"]) / len(top1_similarity["answerable"])
        u = sum(top1_similarity["unanswerable"]) / len(top1_similarity["unanswerable"])
        print(f"  similitud top-1 media: contestables {a:.3f} vs incontestables {u:.3f} "
              f"(margen {a - u:+.3f}) -> ¿serviría un umbral de rechazo?")
    return detail, summary, best


# --------------------------------------------------------------------------
# Stage 2: agent answers
# --------------------------------------------------------------------------

def run_agent(rows: list[dict], refresh: bool, limit: int | None) -> list[dict]:
    from agent import answer

    path = EVAL_DIR / "answers.csv"
    cached: dict[str, dict] = {}
    if path.is_file() and not refresh:
        with path.open(newline="", encoding="utf-8") as handle:
            cached = {r["id"]: r for r in csv.DictReader(handle) if r.get("id")}

    results: list[dict] = []
    todo = rows[:limit] if limit else rows
    for position, row in enumerate(todo, start=1):
        previous = cached.get(row["id"])
        if previous and previous.get("question") == row["question"]:
            results.append(previous)
            continue
        print(f"  [{position}/{len(todo)}] {row['id']}: {row['question'][:62]}")
        try:
            result = answer(row["question"], approve=False)
        except Exception as error:  # noqa: BLE001 - one bad question must not stop the run
            print(f"      failed: {type(error).__name__}: {error}")
            result = {"answer": f"ERROR: {type(error).__name__}: {error}", "citations": [],
                      "tool_calls": [], "retrieved_doc_ids": [], "guardrail": "error",
                      "refused": False, "tokens": {}, "seconds": 0}
        evidence = "\n\n".join(call.get("result", "") for call in result.get("tool_calls", []))
        results.append({
            "id": row["id"], "question": row["question"], "kind": row["kind"],
            "answer": result["answer"],
            "citations": " | ".join(result.get("citations", [])),
            "retrieved_doc_ids": " ".join(result.get("retrieved_doc_ids", [])),
            "guardrail": result.get("guardrail") or "",
            "refused": int(bool(result.get("refused"))),
            "tool_calls": len(result.get("tool_calls", [])),
            "input_tokens": (result.get("tokens") or {}).get("input_tokens", 0),
            "output_tokens": (result.get("tokens") or {}).get("output_tokens", 0),
            "total_tokens": (result.get("tokens") or {}).get("total_tokens", 0),
            "seconds": result.get("seconds", 0),
            "evidence": evidence[:40000],
        })
    write_csv(path, results)
    return results


# --------------------------------------------------------------------------
# Stage 3: what code can check
# --------------------------------------------------------------------------

def code_checks(rows: list[dict], answers: list[dict]) -> list[dict]:
    by_id = {r["id"]: r for r in rows}
    valid_ids = set()
    valid_labels = []
    for strategy in pipeline.STRATEGIES:
        store = load_strategy(strategy)
        if store:
            valid_ids.update(store["ids"])
            valid_labels += [m.get("location_label", "") for m in store["metadatas"]]
    labels = {label.lower() for label in valid_labels}
    # server.py cites "<location_label> · CVE:<cve>", but the index stores the label
    # without that suffix, so an exact string test can never resolve a citation.
    # Split the CVE off, resolve the label, and check the CVE belongs to that chunk.
    cve_by_label: dict[str, set[str]] = {}
    for strategy in pipeline.STRATEGIES:
        store = load_strategy(strategy)
        if store:
            for metadata in store["metadatas"]:
                key = (metadata.get("location_label") or "").lower()
                cve_by_label.setdefault(key, set()).add((metadata.get("cve") or "").lower())

    def resolves(citation: str) -> bool:
        text = citation.strip().strip("[]").strip()
        label, _, cve = text.partition("· CVE:")
        label = label.strip().lower()
        if label not in labels:
            return False
        cve = cve.strip().lower()
        return not cve or cve in cve_by_label.get(label, set())

    checks: list[dict] = []
    for record in answers:
        row = by_id.get(record["id"], {})
        kind = (row.get("kind") or "").strip().lower()
        citations = [c for c in (record.get("citations") or "").split(" | ") if c.strip()]
        # The agent only flagged a refusal when the fixed phrase OPENED the answer,
        # so a refusal that explained itself first (q07) was counted as an answer.
        # The phrase anywhere in the text is a refusal; whether it LEADS is a
        # separate, reportable thing, because regla 5 requires it to lead.
        answer_text = str(record.get("answer") or "")
        refused = str(record.get("refused", "0")) == "1" or REFUSAL in answer_text
        refusal_leads = answer_text.lstrip().startswith(REFUSAL)

        resolvable = sum(1 for c in citations if resolves(c))
        cited_docs = set(re.findall(r"\b((?:BOCG|DSCD)-[\w-]+)\b", " ".join(citations)))
        retrieved = set((record.get("retrieved_doc_ids") or "").split())
        invented = sorted(cited_docs - retrieved) if cited_docs else []

        pairs = expected_pairs(row)
        expected_sources = {s for s, _ in pairs}
        retrieval_hit = bool(expected_sources & retrieved) if expected_sources else ""

        checks.append({
            "id": record["id"], "kind": kind,
            "refused": int(refused),
            # For an unanswerable question a refusal is simply correct. No judge needed.
            "refusal_correct": int(refused) if kind == "unanswerable" else ("" if not refused else 0),
            "wrong_refusal": int(refused and kind != "unanswerable"),
            "refusal_leads": int(refusal_leads) if refused else "",
            "citations": len(citations),
            "citations_resolvable": resolvable,
            "citations_unresolvable": len(citations) - resolvable,
            "invented_doc_ids": " ".join(invented),
            "has_citation": int(bool(citations)),
            "cited_but_not_retrieved": int(bool(invented)),
            "retrieval_hit": retrieval_hit,
            "guardrail": record.get("guardrail", ""),
        })
    return checks


# --------------------------------------------------------------------------
# Stage 4: the LLM judge
# --------------------------------------------------------------------------

JUDGE_RUBRIC = """Eres un evaluador estricto. Juzgas la respuesta de un asistente que solo
puede responder citando un expediente parlamentario del Congreso de los Diputados.

Te doy: la pregunta, su TIPO, la respuesta de referencia escrita por una persona, el TEXTO
RECUPERADO que el asistente tenía delante, y su RESPUESTA.

HECHOS QUE DEBES DAR POR CIERTOS, por encima de tu propio juicio:

- El TIPO es verdad comprobada. Si TIPO es `single` o `multi`, la pregunta SÍ tiene respuesta
  en el corpus y la respuesta de referencia la contiene. Negarse entonces ("NO CONSTA EN EL
  CORPUS" o equivalente) es un fallo: correct=0. Solo si TIPO es `unanswerable` la negativa
  es la respuesta correcta.
- Un TEXTO RECUPERADO vacío NO significa que el corpus esté vacío ni que la pregunta sea
  incontestable: significa que el asistente no buscó. Si TIPO es `single` o `multi`, eso es
  correct=0.
- Si la RESPUESTA empieza por "ERROR:" es un fallo del sistema, no una respuesta:
  correct=0, supported=0, stage_correct=0.

Juzga tres dimensiones, cada una 1 o 0. Si dudas, pon 0 y explica por qué.

1. "correct": ¿coincide en lo esencial con la respuesta de referencia, respetando los hechos
   de arriba?
2. "supported": ¿aparece CADA afirmación en el TEXTO RECUPERADO? Comprueba uno por uno los
   nombres propios, nombres de pila, fechas, cifras y porcentajes: si la respuesta añade un
   dato que no está literalmente en el texto —por ejemplo el nombre de pila de una persona
   cuando el texto solo da el apellido— es supported=0, aunque sea cierto en el mundo real.
3. "stage_correct": ¿distingue correctamente la fase del trámite? Presentar el texto del
   proyecto del Gobierno como si fuera la ley aprobada es stage_correct=0. Si la respuesta no
   depende de la fase, pon 1.

Devuelve SOLO este JSON, sin texto alrededor:
{"correct": 0 o 1, "supported": 0 o 1, "stage_correct": 0 o 1, "razon": "una frase"}"""


def judge(rows: list[dict], answers: list[dict], refresh: bool) -> list[dict]:
    import os

    from google import genai

    from api_key import load_api_key

    path = EVAL_DIR / "judge.csv"
    cached: dict[str, dict] = {}
    if path.is_file() and not refresh:
        with path.open(newline="", encoding="utf-8") as handle:
            # A verdict with no score is a failed call, not a result: retry it.
            cached = {r["id"]: r for r in csv.DictReader(handle)
                      if r.get("id") and str(r.get("correct", "")).strip() != ""}

    by_id = {r["id"]: r for r in rows}
    model = os.environ.get(JUDGE_MODEL_ENV) or __import__("agent").CHAT_MODEL
    client = genai.Client(api_key=load_api_key())
    verdicts: list[dict] = []

    for position, record in enumerate(answers, start=1):
        if record["id"] in cached:
            verdicts.append(cached[record["id"]])
            continue
        row = by_id.get(record["id"], {})
        prompt = (
            f"{JUDGE_RUBRIC}\n\n"
            f"PREGUNTA: {record['question']}\n\n"
            f"TIPO: {row.get('kind', '')}\n\n"
            f"RESPUESTA DE REFERENCIA: {row.get('reference_answer', '')}\n\n"
            f"TEXTO RECUPERADO:\n{record.get('evidence', '')[:40000]}\n\n"
            f"RESPUESTA DEL ASISTENTE:\n{record['answer']}"
        )
        payload = None
        for attempt in range(JUDGE_MAX_RETRIES):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                raw = (response.text or "").strip()
                payload = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
                break
            except Exception as error:  # noqa: BLE001 - retry transient load, then record
                transient = "503" in str(error) or "UNAVAILABLE" in str(error) or "429" in str(error)
                if transient and attempt < JUDGE_MAX_RETRIES - 1:
                    time.sleep(5.0 * (attempt + 1))
                    continue
                payload = {"correct": "", "supported": "", "stage_correct": "",
                           "razon": f"judge failed: {type(error).__name__}: {error}"}
                break
        verdicts.append({"id": record["id"], "kind": record.get("kind", ""), **payload})
        print(f"  [{position}/{len(answers)}] {record['id']} -> {payload.get('correct')}/"
              f"{payload.get('supported')}/{payload.get('stage_correct')}")
    write_csv(path, verdicts)
    return verdicts


# --------------------------------------------------------------------------
# Stage 5: agreement with your own grades
# --------------------------------------------------------------------------

def cohen_kappa(a: list[int], b: list[int]) -> float:
    if not a:
        return float("nan")
    n = len(a)
    observed = sum(1 for x, y in zip(a, b) if x == y) / n
    expected = sum(
        (a.count(label) / n) * (b.count(label) / n) for label in {0, 1}
    )
    return (observed - expected) / (1 - expected) if expected < 1 else float("nan")


def agreement(verdicts: list[dict]) -> list[dict]:
    if not HUMAN_LABELS.is_file():
        print("  eval/human_labels.csv not found.")
        return []
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as handle:
        human = {r["id"]: r for r in csv.DictReader(handle) if (r.get("id") or "").strip()}
    if not human:
        print("  eval/human_labels.csv is empty — grade 20+ answers yourself, "
              "BEFORE reading eval/judge.csv.")
        return []

    by_id = {v["id"]: v for v in verdicts}
    rows: list[dict] = []
    for dimension in ("correct", "supported"):
        mine, theirs = [], []
        for question_id, label in human.items():
            verdict = by_id.get(question_id)
            if not verdict or str(verdict.get(dimension, "")) == "" or str(label.get(dimension, "")).strip() == "":
                continue
            mine.append(int(str(label[dimension]).strip()))
            theirs.append(int(verdict[dimension]))
        if not mine:
            continue
        raw = sum(1 for x, y in zip(mine, theirs) if x == y) / len(mine)
        kappa = cohen_kappa(mine, theirs)
        rows.append({"dimension": dimension, "n": len(mine),
                     "acuerdo": round(raw, 3), "kappa": round(kappa, 3) if kappa == kappa else ""})
        print(f"  {dimension:<12} n={len(mine):<4} acuerdo={raw:.3f}  kappa={kappa:.3f}")
    if len(human) < 20:
        print(f"  only {len(human)} human grades; the brief asks for 20+")
    return rows


# --------------------------------------------------------------------------
# Stage 6: failures
# --------------------------------------------------------------------------

def classify(checks: list[dict], verdicts: list[dict]) -> list[dict]:
    """Propose a primary cause for each failure. The final call is yours, in REPORT.md."""
    by_id = {v["id"]: v for v in verdicts}
    failures: list[dict] = []
    for check in checks:
        verdict = by_id.get(check["id"], {})
        correct = str(verdict.get("correct", ""))
        supported = str(verdict.get("supported", ""))
        stage_ok = str(verdict.get("stage_correct", ""))
        if correct == "1" and supported == "1" and stage_ok == "1":
            continue
        if correct == "" and not check["wrong_refusal"]:
            continue

        if check["wrong_refusal"]:
            cause = "wrong_refusal"
        elif check["cited_but_not_retrieved"]:
            cause = "unsupported_claim"
        elif check["retrieval_hit"] == 0 or check["retrieval_hit"] == "0":
            cause = "retrieval_miss"
        elif stage_ok == "0":
            cause = "stage_confusion"
        elif supported == "0":
            cause = "unsupported_claim"
        else:
            cause = "wrong_from_right_passage"
        failures.append({
            "id": check["id"], "kind": check["kind"], "causa_propuesta": cause,
            "causa_final": "", "correct": correct, "supported": supported,
            "stage_correct": stage_ok, "retrieval_hit": check["retrieval_hit"],
            "guardrail": check["guardrail"], "razon_juez": verdict.get("razon", ""),
        })
    counts = Counter(f["causa_propuesta"] for f in failures)
    for cause, n in counts.most_common():
        print(f"  {cause:<28}{n:>4}")
    if not failures:
        print("  no failures recorded (or the judge has not run yet)")
    return failures


# --------------------------------------------------------------------------
# The add-document demo (one shot)
# --------------------------------------------------------------------------

def demo(rows: list[dict]) -> int:
    from agent import answer

    target = next((r for r in rows if r["id"] == DEMO_QUESTION_ID), None) if DEMO_QUESTION_ID else None
    target = target or next((r for r in rows if r["kind"].strip().lower() == "unanswerable"), None)
    if not target:
        print("  No unanswerable question in eval/questions.csv to demonstrate with.")
        return 1
    if not DEMO_DOCUMENT.is_file():
        print(f"  Missing {DEMO_DOCUMENT.relative_to(ROOT)}; run `main.py index` to download it.")
        return 1

    print(f"  question: {target['question']}")
    before = answer(target["question"], approve=False)
    print("  -- adding the document (this spends embeddings) --")
    # approve=True pre-authorises the harness gate, but rule 8 of AGENTS.md tells the
    # model never to call add_document without explicit approval *in the conversation*,
    # so it asks instead of acting. The approval has to be stated in the turn as well.
    added = answer(
        f"Añade el documento {DEMO_DOCUMENT.relative_to(ROOT)} al índice. "
        f"Apruebo explícitamente esta operación: procede a llamar a add_document.",
        approve=True,
    )
    after = answer(target["question"], approve=False)

    BEFORE_AFTER.write_text(
        f"# Adding a document: before and after\n\n"
        f"**Question ({target['id']}, {target['kind']}):** {target['question']}\n\n"
        f"**Document added:** `{DEMO_DOCUMENT.relative_to(ROOT)}`\n\n"
        f"## Before\n\n```\n{before['answer']}\n```\n\n"
        f"- guardrail: `{before.get('guardrail')}` · tool calls: {len(before.get('tool_calls', []))}"
        f" · {before.get('seconds')}s\n\n"
        f"## Adding it\n\n```\n{added['answer']}\n```\n\n"
        f"## After\n\n```\n{after['answer']}\n```\n\n"
        f"- citations: {', '.join(after.get('citations', [])) or 'none'}\n"
        f"- guardrail: `{after.get('guardrail')}` · tool calls: {len(after.get('tool_calls', []))}"
        f" · {after.get('seconds')}s\n",
        encoding="utf-8",
    )
    print(f"  written: {BEFORE_AFTER.relative_to(ROOT)}")
    return 0


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent end to end.")
    parser.add_argument("--stage", choices=["all", "retrieval", "answers", "judge", "demo"], default="all")
    parser.add_argument("--refresh", action="store_true", help="ignore cached answers and verdicts")
    parser.add_argument("--limit", type=int, help="only the first N questions (for a smoke test)")
    args = parser.parse_args()

    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_questions()
    if not rows:
        print("eval/questions.csv has no questions yet. Write the test set first "
              "(30+, with 5+ unanswerable and 5+ multi) — see eval/README.md.")
        return 0
    print(f"{len(rows)} questions: " + ", ".join(
        f"{n} {k}" for k, n in Counter(r['kind'].strip().lower() for r in rows).items()))

    if args.stage == "demo":
        banner("Adding a document: before and after")
        return demo(rows)

    skipped: list[str] = []
    summary: dict = {"questions": len(rows)}

    if args.stage in {"all", "retrieval"}:
        banner("1. Retrieval: hit rate @1/3/5 per design")
        detail, retrieval_summary, best = evaluate_retrieval(rows)
        write_csv(EVAL_DIR / "retrieval.csv", detail)
        write_csv(EVAL_DIR / "retrieval_summary.csv", retrieval_summary)
        summary["retrieval"] = retrieval_summary
        summary["best_design"] = best
        if not detail:
            skipped.append("retrieval (no index or no answerable questions)")
    if args.stage == "retrieval":
        return 0

    banner("2. Agent answers")
    answers = run_agent(rows, refresh=args.refresh, limit=args.limit)
    if args.stage == "answers":
        return 0

    banner("3. Code checks")
    checks = code_checks(rows, answers)
    write_csv(EVAL_DIR / "code_checks.csv", checks)
    totals = {
        "respuestas": len(checks),
        "rechazos": sum(c["refused"] for c in checks),
        "rechazos_correctos": sum(1 for c in checks if c["refusal_correct"] == 1),
        "rechazos_indebidos": sum(c["wrong_refusal"] for c in checks),
        "rechazos_sin_frase_al_inicio": sum(1 for c in checks if c["refused"] and c["refusal_leads"] == 0),
        "sin_cita": sum(1 for c in checks if not c["has_citation"] and not c["refused"]),
        "citas_no_resolubles": sum(c["citations_unresolvable"] for c in checks),
        "citas_inventadas": sum(c["cited_but_not_retrieved"] for c in checks),
    }
    for key, value in totals.items():
        print(f"  {key:<24}{value:>5}")
    summary["code_checks"] = totals

    banner("4. LLM judge")
    try:
        verdicts = judge(rows, answers, refresh=args.refresh)
    except Exception as error:  # noqa: BLE001
        print(f"  judge unavailable: {type(error).__name__}: {error}")
        verdicts, skipped = [], skipped + ["judge"]
    if verdicts:
        for dimension in ("correct", "supported", "stage_correct"):
            scored = [int(v[dimension]) for v in verdicts if str(v.get(dimension, "")) != ""]
            if scored:
                rate = sum(scored) / len(scored)
                print(f"  {dimension:<16}{rate:.3f}  ({sum(scored)}/{len(scored)})")
                summary[dimension] = round(rate, 3)

    banner("5. Agreement with your own grades")
    rows_agreement = agreement(verdicts)
    write_csv(EVAL_DIR / "agreement.csv", rows_agreement)
    summary["agreement"] = rows_agreement

    banner("6. Failures by cause")
    failures = classify(checks, verdicts)
    write_csv(EVAL_DIR / "failures.csv", failures)
    summary["failures"] = dict(Counter(f["causa_propuesta"] for f in failures))

    banner("7. Cost per question")
    tokens = [int(a.get("total_tokens", 0) or 0) for a in answers]
    seconds = [float(a.get("seconds", 0) or 0) for a in answers]
    if tokens:
        summary["cost"] = {
            "tokens_medios": round(sum(tokens) / len(tokens), 1),
            "segundos_medios": round(sum(seconds) / len(seconds), 2),
            "segundos_p90": round(sorted(seconds)[int(0.9 * (len(seconds) - 1))], 2),
            "tokens_por_100_preguntas": int(sum(tokens) / len(tokens) * 100),
        }
        for key, value in summary["cost"].items():
            print(f"  {key:<28}{value:>10}")

    (EVAL_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    if not BEFORE_AFTER.is_file():
        skipped.append("add-document demo — run `uv run python evaluate.py --stage demo`")
    if skipped:
        print(f"\n{'!' * 72}\n  INCOMPLETE — not run: " + "; ".join(skipped) + f"\n{'!' * 72}")
    print(f"\nWritten to {EVAL_DIR.relative_to(ROOT)}/: retrieval.csv, retrieval_summary.csv, "
          f"answers.csv, code_checks.csv, judge.csv, agreement.csv, failures.csv, summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
