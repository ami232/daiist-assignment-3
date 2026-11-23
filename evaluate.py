"""
Assignment 3: evaluation (`main.py evaluate`).

Retrieval evaluation (hit rate per design) and end-to-end evaluation (agent answers, code checks,
LLM judge, agreement with human labels, add_document demo). `main.py evaluate` runs both.

expected_location in eval/questions.csv names ONE Rn. or § per passage, `;` between passages:
    "BGH VIII ZR 107/20, Rn. 18"   "BGH VIII ZR 107/20, Leitsatz"
    "§ 2 Nr. 10 BetrKV"            "§ 556 Abs. 3 BGB"   "§ 7 HeizkostenV"   "Anlage CO2KostAufG"
A retrieved chunk is a hit when it comes from that document and covers that Rn./§ (chunk
metadata `covers`, written by index.py). Matching never looks at chunk ids or location strings,
so hit rates stay comparable across chunking designs.
"""

from __future__ import annotations

import csv
import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
CHUNKS_FILE = ROOT / "index" / "chunks.jsonl"
KS = (1, 3, 5)

STATUTES = ("BGB", "BetrKV", "HeizkostenV", "CO2KostAufG")
_JUDGMENT = re.compile(r"^(BGH VIII ZR \d+/\d+),\s*(?:Rn\.?\s*(\d+)|(Leitsatz))$")
_STATUTE = re.compile(
    r"^(§\s*\d+[a-z]?|Anlage|Anhang EV)"
    r"(?:\s+Abs\.\s*(\d+[a-z]?))?(?:\s+(?:Satz|S\.)\s*\d+)?"
    r"(?:\s+Nr\.\s*(\d+[a-z]?))?(?:\s+(?:Satz|S\.)\s*\d+)?"
    rf"\s+({'|'.join(STATUTES)})$"
)


def parse_location(location: str) -> dict:
    """One expected location -> {doc_id, rn | leitsatz | para, abs, nr}. Raises ValueError if unparseable."""
    loc = " ".join(location.replace("§§", "§").split())
    if m := _JUDGMENT.match(loc):
        return {"doc_id": m.group(1), "rn": m.group(2), "leitsatz": bool(m.group(3))}
    if m := _STATUTE.match(loc):
        para = re.sub(r"§\s*", "§ ", m.group(1))
        return {"doc_id": m.group(4), "para": para, "abs": m.group(2), "nr": m.group(3)}
    raise ValueError(
        f"Can't parse expected_location {location!r}. Use one Rn. or § per passage, e.g. "
        f"'BGH VIII ZR 107/20, Rn. 18' or '§ 2 Nr. 10 BetrKV'."
    )


def covers(meta: dict, target: dict) -> bool:
    """Does a chunk (its metadata) cover this target passage?"""
    if meta.get("doc_id") != target["doc_id"]:
        return False
    keys = set(meta.get("covers", "").strip("|").split("|"))
    if "rn" in target:
        return "Leitsatz" in keys if target["leitsatz"] else f"Rn. {target['rn']}" in keys
    para, abs_, nr = target["para"], target["abs"], target["nr"]
    if para in keys:  # the whole § is in this chunk
        return True
    if abs_ and nr:
        qualified = f"{para} Abs. {abs_} Nr. {nr}"
        abs_has_items = any(k.startswith(f"{para} Abs. {abs_} Nr. ") for k in keys)
        return qualified in keys or (f"{para} Abs. {abs_}" in keys and not abs_has_items)
    if abs_:
        return f"{para} Abs. {abs_}" in keys
    if nr:
        return f"{para} Nr. {nr}" in keys or any(k.startswith(f"{para} Abs. ") and k.endswith(f" Nr. {nr}") for k in keys)
    return f"{para}*" in keys  # expected the whole §, chunk holds part of it


def covers_holding(meta: dict, target: dict) -> bool:
    """'Holding' match: the exact passage, or the Leitsatz of the expected judgment (statutes: exact only)."""
    if covers(meta, target):
        return True
    return "rn" in target and meta.get("doc_id") == target["doc_id"] and "|Leitsatz|" in meta.get("covers", "")


def targets_of(expected_location: str) -> list[dict]:
    return [parse_location(part) for part in expected_location.split(";") if part.strip()]


def hits_at_k(retrieved: list[dict], expected_location: str, ks=KS, match=covers) -> dict:
    """Hit at each k for one question, given the retrieved chunks' metadata in rank order.

    'all': every expected passage is covered within the top k (the headline number; for
    single questions it equals 'any'). 'any': at least one is. `match` is covers (exact
    passage) or covers_holding (passage or the judgment's Leitsatz).
    """
    targets = targets_of(expected_location)
    found_at = [next((rank for rank, meta in enumerate(retrieved, 1) if match(meta, t)), None) for t in targets]
    return {
        k: {
            "all": all(r is not None and r <= k for r in found_at),
            "any": any(r is not None and r <= k for r in found_at),
        }
        for k in ks
    }


def load_chunks(path: Path = CHUNKS_FILE) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_test_set(questions: Path = QUESTIONS, chunks_file: Path = CHUNKS_FILE) -> list[str]:
    """Problems with eval/questions.csv locations: unparseable, wrong source, or covered by no chunk."""
    chunks = load_chunks(chunks_file)
    problems = []
    with questions.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["kind"].strip().lower() == "unanswerable":
                continue
            sources = {s.strip() for s in row["expected_source"].split(";") if s.strip()}
            try:
                targets = targets_of(row["expected_location"])
            except ValueError as error:
                problems.append(f"{row['id']}: {error}")
                continue
            if not targets:
                problems.append(f"{row['id']}: no expected_location")
            for t in targets:
                if t["doc_id"] not in sources:
                    problems.append(f"{row['id']}: location in {t['doc_id']} but expected_source is {sorted(sources)}")
                if not any(covers(c, t) for c in chunks):
                    problems.append(f"{row['id']}: no indexed chunk covers {t} (dropped Tatbestand / part I, or a typo?)")
    return problems


# ---------------------------------------------------------------- retrieval evaluation

CACHE_DIR = ROOT / "eval" / "cache"
RETRIEVAL_JSON = ROOT / "eval" / "retrieval_results.json"
RETRIEVAL_MD = ROOT / "eval" / "retrieval_results.md"
DESIGNS = {"A": "baseline (EN → dense)", "B": "translated (DE → dense)", "C": "hybrid (DE → BM25 + dense, RRF)",
           "D": "hybrid, max 2 chunks/doc"}
METRICS = {"exact": "exact passage", "holding": "holding (passage or Leitsatz)"}


def load_questions(path: Path = QUESTIONS) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def _rate(flags: list[bool]) -> float:
    return sum(flags) / len(flags) if flags else float("nan")


def evaluate_retrieval() -> dict:
    import retrieval  # needs the API key; imported here so the matching helpers work without it

    questions = [q for q in load_questions() if q["kind"].strip().lower() != "unanswerable"]
    corpus = retrieval.Corpus()
    translations = retrieval.JsonCache(CACHE_DIR / "translations.json")
    embeddings = retrieval.JsonCache(CACHE_DIR / "query_embeddings.json")

    per_question: dict[str, list[dict]] = {d: [] for d in DESIGNS}
    for design in DESIGNS:
        for q in questions:
            res = retrieval.search(corpus, q["question"], design, k=max(KS),
                                   translations=translations, embeddings=embeddings)
            chunks = res["chunks"]
            per_question[design].append({
                "id": q["id"], "kind": q["kind"], "question": q["question"], "query": res["query"],
                "expected": q["expected_location"],
                "hits": hits_at_k(chunks, q["expected_location"]),
                "hits_holding": hits_at_k(chunks, q["expected_location"], match=covers_holding),
                "words": {k: sum(len(c["text"].split()) for c in chunks[:k]) for k in KS},
                "retrieved": [c["location"] for c in chunks],
            })

    summary = {}
    for design, rows in per_question.items():
        single = [r for r in rows if r["kind"] == "single"]
        multi = [r for r in rows if r["kind"] == "multi"]
        summary[design] = {"words": {k: sum(r["words"][k] for r in rows) / len(rows) for k in KS}}
        for metric, field in (("exact", "hits"), ("holding", "hits_holding")):
            summary[design][metric] = {
                "overall": {k: _rate([r[field][k]["all"] for r in rows]) for k in KS},
                "single": {k: _rate([r[field][k]["all"] for r in single]) for k in KS},
                "multi_all": {k: _rate([r[field][k]["all"] for r in multi]) for k in KS},
                "multi_any": {k: _rate([r[field][k]["any"] for r in multi]) for k in KS},
            }

    calls = [translations.get(retrieval._key(retrieval.TRANSLATE_MODEL, "thinking=low", retrieval.TRANSLATE_PROMPT, q["question"]))
             for q in questions]
    translation_cost = {
        "model": retrieval.TRANSLATE_MODEL,
        "questions": len(calls),
        "input_tokens_avg": sum(c["input_tokens"] for c in calls) / len(calls),
        "output_tokens_avg": sum(c["output_tokens"] for c in calls) / len(calls),
        "seconds_avg": sum(c["seconds"] for c in calls) / len(calls),
        "seconds_max": max(c["seconds"] for c in calls),
    }
    result = {
        "n": {"answerable": len(questions), "single": sum(q["kind"] == "single" for q in questions),
              "multi": sum(q["kind"] == "multi" for q in questions)},
        "summary": summary, "translation": translation_cost, "per_question": per_question,
    }
    RETRIEVAL_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    RETRIEVAL_MD.write_text(retrieval_report(result), encoding="utf-8")
    return result


def retrieval_report(result: dict) -> str:
    n, s = result["n"], result["summary"]
    pct = lambda x: f"{100 * x:.0f}%"  # noqa: E731
    lines = [
        f"# Retrieval evaluation\n\n{n['answerable']} answerable questions ({n['single']} single, {n['multi']} multi). "
        "Multi (all) = every expected passage within top k; (any) = at least one. "
        "Exact = a chunk covers the expected Rn./§. Holding = that, or the expected judgment's Leitsatz "
        "(statute targets: exact only).\n",
        "| Design | k | Exact: overall | single | multi all | multi any | Holding: overall | single | multi all | multi any | Words added |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for d, name in DESIGNS.items():
        for k in KS:
            e, h = s[d]["exact"], s[d]["holding"]
            cells = [pct(m[c][k]) for m in (e, h) for c in ("overall", "single", "multi_all", "multi_any")]
            lines.append(f"| {d} {name} | {k} | " + " | ".join(cells) + f" | {s[d]['words'][k]:.0f} |")
    lines.append(
        "\nChosen design: B at k=5 (retrieval.DEFAULT_DESIGN), on the holding metric: the agent can answer and cite "
        "from a judgment's Leitsatz, and B leads there with fewer words than C. A, C and D are kept as compared designs."
    )
    t = result["translation"]
    lines.append(
        f"\nTranslation step (B, C): {t['model']}, avg {t['input_tokens_avg']:.0f} input + {t['output_tokens_avg']:.0f} "
        f"output tokens, avg {t['seconds_avg']:.1f} s (max {t['seconds_max']:.1f} s) per question, measured on the first "
        "uncached call. BM25 + RRF run locally (milliseconds)."
    )
    return "\n".join(lines) + "\n"


def misses(result: dict, design: str, k: int = max(KS)) -> str:
    out = []
    for r in result["per_question"][design]:
        if r["hits"][k]["all"]:
            continue
        partial = " (partial: one of two found)" if r["hits"][k]["any"] else ""
        out.append(f"{r['id']} [{r['kind']}]{partial} {r['question']}\n"
                   f"   expected : {r['expected']}\n   query    : {r['query']}\n"
                   + "\n".join(f"   #{i} {loc}" for i, loc in enumerate(r["retrieved"], 1)))
    return "\n\n".join(out) or "none"


# ---------------------------------------------------------------- end-to-end evaluation
#
# Same pattern as the lab's 07-own-harness/evaluate.py: run the agent on every question, check in code what
# code can check, and let a stronger model grade the rest against a rubric, with the retrieved passages as
# evidence and the reasoning written before each verdict. Answers and verdicts are cached, so a rerun
# (also check.py --evaluate) spends no tokens.

ANSWERS_CACHE = CACHE_DIR / "answers.json"
VERDICTS_CACHE = CACHE_DIR / "verdicts.json"
ANSWERS_JSONL = ROOT / "eval" / "answers.jsonl"
VERDICTS_JSONL = ROOT / "eval" / "verdicts.jsonl"
SUMMARY_MD = ROOT / "eval" / "summary.md"
TO_GRADE_MD = ROOT / "eval" / "to_grade.md"
DEMO_MD = ROOT / "eval" / "add_document_demo.md"
HUMAN_LABELS = ROOT / "eval" / "human_labels.csv"

JUDGE_MODEL = "gemini-3.1-pro-preview"  # stronger than the agent's gemini-3.8-flash; the only Pro open on this key
HOLDOUT_FILE = "corpus/holdout/jb-KORE303622026.xml"
HOLDOUT_DOC = "BGH VIII ZR 6/24"
DEMO_QID = "q33"

JUDGE_PROMPT = """You are grading an AI assistant that answers landlords' questions about German residential \
service charges (Betriebskosten). It must answer only from the retrieved passages below, cite them, and say \
when they don't cover the question.

Grade two criteria independently. For each, write your reasoning first, then the verdict.

1. correct
   - Answerable question: the answer reaches the same conclusion as the reference answer and states the \
conditions or exceptions the reference treats as decisive. Extra correct detail is fine; missing minor detail \
is fine; contradicting the reference fails.
   - Unanswerable question (kind "unanswerable"): passes only if the answer says the documents don't cover the \
question, without giving a substantive answer to it. Mentioning related rules the passages do contain is fine \
if it is clearly separate from the refusal.
2. supported
   - Every factual or legal claim in the answer is stated in the retrieved passages. Saying the documents don't \
cover something, and referring the user to a lawyer or tax advisor, are not claims. A claim that is true but \
not in the passages fails. Judge the content; a wrong citation label alone does not fail this criterion.

Question ({kind}): {question}

Reference answer (written by a person from the sources):
{reference}

Retrieved passages (everything the search tool returned to the assistant):
{passages}

Assistant's answer:
{answer}"""


def _grade_model():
    from pydantic import BaseModel, Field

    class Grade(BaseModel):
        """The judge's structured output: reasoning first, then the verdict, for each criterion."""
        correct_reasoning: str = Field(description="Two to four sentences comparing the answer with the reference "
                                                   "answer (for an unanswerable question: does it refuse?).")
        correct: bool = Field(description="True only if the answer meets criterion 1.")
        supported_reasoning: str = Field(description="Two to four sentences checking the answer's claims against the "
                                                     "retrieved passages; name any claim that is not in them.")
        supported: bool = Field(description="True only if every claim is in the retrieved passages.")

    return Grade


REFUSAL = re.compile(
    r"(?:documents?|corpus|sources?|passages?|search results?|materials?|statutes?|case law)\b[^.\n]{0,160}?"
    r"(?:do(?:es)?\s*n[o’']?t|do not|does not|did not|contain no|provide no|say nothing)\s*"
    r"(?:cover|contain|address|say|state|answer|mention|include|provide|deal|specify|regulate|govern)?"
    r"|not covered by|no (?:retrieved |relevant )?passages?\b"
    r"|(?:cannot|can't|can’t|could not|couldn't|couldn’t)\s+(?:answer|find)",
    re.I,
)
OPENING = 600  # characters: a refusal here is the answer's main message, later it is a caveat


def refusal(answer: str) -> dict:
    """Code check (b): does the answer say the documents don't cover the question?
    'anywhere' counts for unanswerable questions (related rules may come first); 'opening' means the answer
    leads with it, which for an answerable question is a wrong refusal rather than a caveat."""
    m = REFUSAL.search(answer)
    return {"anywhere": bool(m), "opening": bool(m) and m.start() < OPENING}


def cited_docs(answer: str) -> set[str]:
    import agent
    docs = {f"BGH {c}" for c in agent.CASE.findall(answer)}
    docs |= {m.group(0).split()[-1] for m in agent.CITATION.finditer(answer) if not m.group(0).startswith("BGH")}
    return docs


def _sha(*parts: str) -> str:
    import hashlib
    return hashlib.sha256("\n\x1e".join(parts).encode()).hexdigest()[:24]


def answer_key(question: str, variant: str = "evaluation") -> str:
    import agent
    return _sha(variant, question, (ROOT / "AGENTS.md").read_text(encoding="utf-8"), agent.MODEL)


def tool_results(trace: list[str]) -> list[str]:
    return [line.removeprefix("result ") for line in trace if line.startswith("result ")]


class DailyQuota(RuntimeError):
    pass


def _rate_limited(error: Exception) -> tuple[bool, bool]:
    text = f"{type(error).__name__} {error}"
    limited = any(s in text for s in ("429", "RESOURCE_EXHAUSTED", "ResourceExhausted", "503", "UNAVAILABLE", "overloaded"))
    daily = limited and any(s in text for s in ("PerDay", "per day", "PerDayPer"))
    return limited, daily


async def ask_with_retries(ag, agent_obj, question: str, attempts: int = 6) -> dict:
    import asyncio
    for attempt in range(attempts):
        try:
            answer, trace, stats = await ag.ask(agent_obj, question)
        except Exception as error:  # noqa: BLE001 - classify and retry rate limits only
            limited, daily = _rate_limited(error)
            if daily:
                raise DailyQuota(str(error)[:300]) from error
            if not limited or attempt == attempts - 1:
                raise
            wait = 30 * (attempt + 1)
            print(f"    rate limited, waiting {wait}s ({attempt + 1}/{attempts})", file=sys.stderr, flush=True)
            await asyncio.sleep(wait)
            continue
        if any("daily embedding quota" in r for r in tool_results(trace)):
            raise DailyQuota("the search tool hit the daily embedding quota")
        return {"question": question, "answer": answer, "trace": trace, "stats": stats}
    raise RuntimeError("unreachable")


async def run_answers(questions: list[dict]) -> dict:
    """Answer every question once (cached). add_document is denied automatically, so the index cannot change."""
    from contextlib import AsyncExitStack
    import agent as ag
    import retrieval

    cache = retrieval.JsonCache(ANSWERS_CACHE)
    todo = [q for q in questions if cache.get(answer_key(q["question"])) is None]
    if todo:
        print(f"Answering {len(todo)} of {len(questions)} questions (the rest are cached) ...", flush=True)
        async with AsyncExitStack() as stack:
            agent_obj = ag.build_agent(await ag.load_mcp_tools(stack), auto_deny=True)
            for i, q in enumerate(todo, 1):
                record = await ask_with_retries(ag, agent_obj, q["question"])
                cache.put(answer_key(q["question"]), record)
                s = record["stats"]
                print(f"  {i}/{len(todo)} {q['id']}: {s['model_calls']} calls, "
                      f"{s['input_tokens'] + s['output_tokens']:,} tokens, {s['seconds']} s", flush=True)
    return {q["id"]: cache.get(answer_key(q["question"])) for q in questions}


def passages_text(trace: list[str], lookup: dict) -> str:
    import agent
    locations = agent.retrieved_locations(tool_results(trace))
    if not locations:
        return "(the assistant did not search)"
    return "\n\n".join(f"[{loc}]\n{lookup[loc]['text'] if loc in lookup else '(chunk not in index)'}" for loc in locations)


async def judge_answers(questions: list[dict], answers: dict, lookup: dict) -> dict:
    """Grade every answer with the judge (cached by judge model, prompt, question, reference and answer)."""
    import asyncio
    import retrieval
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key

    cache = retrieval.JsonCache(VERDICTS_CACHE)
    judge = None
    verdicts = {}
    for q in questions:
        rec = answers[q["id"]]
        passages = passages_text(rec["trace"], lookup)
        key = _sha(JUDGE_MODEL, JUDGE_PROMPT, q["question"], q["reference_answer"], rec["answer"], passages)
        if (hit := cache.get(key)) is None:
            if judge is None:
                load_api_key()
                judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(_grade_model())
            prompt = JUDGE_PROMPT.format(kind=q["kind"], question=q["question"], reference=q["reference_answer"],
                                         passages=passages, answer=rec["answer"])
            for attempt in range(6):
                try:
                    hit = (await judge.ainvoke(prompt)).model_dump()
                    break
                except Exception as error:  # noqa: BLE001
                    limited, daily = _rate_limited(error)
                    if daily:
                        raise DailyQuota(str(error)[:300]) from error
                    if not limited or attempt == 5:
                        raise
                    await asyncio.sleep(30 * (attempt + 1))
            cache.put(key, hit)
            print(f"  judged {q['id']}", flush=True)
        verdicts[q["id"]] = hit
    return verdicts


def code_checks(q: dict, rec: dict, lookup: dict) -> dict:
    import agent
    problems = agent.check_citations_in(rec["answer"], tool_results(rec["trace"]), lookup)
    expected = {s.strip() for s in q["expected_source"].split(";") if s.strip()}
    cited = cited_docs(rec["answer"])
    return {
        "citations": len(list(agent.CITATION.finditer(rec["answer"]))),
        "citations_valid": not problems,
        "invalid_citations": problems,
        "refusal": refusal(rec["answer"]),
        "cites_expected_source": bool(expected & cited) if expected else None,
    }


def cited_passages(answer: str, trace: list[str], lookup: dict) -> list[dict]:
    """Retrieved chunks that back the answer's citations (for the blind grading file)."""
    import agent
    chunks = [lookup[loc] for loc in agent.retrieved_locations(tool_results(trace)) if loc in lookup]
    out = []
    for cite in dict.fromkeys(m.group(0) for m in agent.CITATION.finditer(answer)):
        for c in chunks:
            if agent.citation_ok(cite, [c]) and c not in out:
                out.append(c)
    return out


def write_to_grade(questions: list[dict], answers: dict, lookup: dict) -> None:
    lines = [
        "# Blind grading\n",
        "For each question, grade the agent's answer in `eval/human_labels.csv` (columns `id,correct,supported,notes`) "
        "before you look at the judge's verdicts:\n",
        "- `correct` 1/0: matches your reference answer (for unanswerable questions: a proper refusal).",
        "- `supported` 1/0: every claim is in the retrieved text.",
        "- `notes`: why, for every 0.\n",
        "Only the passages the answer cites are shown below; the judge saw everything the search tool returned "
        "(`eval/answers.jsonl`, field `trace`).\n\n---\n",
    ]
    for q in questions:
        rec = answers[q["id"]]
        lines += [f"## {q['id']} ({q['kind']})\n", f"**Question:** {q['question']}\n",
                  f"**Your reference answer:** {q['reference_answer']}\n", "**Agent's answer:**\n",
                  "\n".join("> " + l if l else ">" for l in rec["answer"].splitlines()) + "\n"]
        cited = cited_passages(rec["answer"], rec["trace"], lookup)
        lines.append("**Cited passages:**" + ("" if cited else " none matched a retrieved chunk") + "\n")
        for c in cited:
            body = c["text"].split("\n", 1)[1] if "\n" in c["text"] else c["text"]
            lines.append(f"<details><summary>{c['location']}</summary>\n\n{body}\n\n</details>\n")
        lines.append("---\n")
    TO_GRADE_MD.write_text("\n".join(lines), encoding="utf-8")


def read_human_labels() -> dict:
    if not HUMAN_LABELS.is_file():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def agreement(verdicts: dict, human: dict) -> dict:
    out = {}
    for col in ("correct", "supported"):
        pairs = [(qid, str(int(verdicts[qid][col])), human[qid][col].strip()) for qid in human
                 if qid in verdicts and human[qid].get(col, "").strip() in ("0", "1")]
        out[col] = {"n": len(pairs), "agree": sum(j == h for _, j, h in pairs),
                    "disagreements": [{"id": qid, "judge": int(j), "human": int(h), "notes": human[qid].get("notes", ""),
                                       "judge_reasoning": verdicts[qid][f"{col}_reasoning"]}
                                      for qid, j, h in pairs if j != h]}
    return out


def summarize(questions: list[dict], rows: dict) -> str:
    kinds = ["single", "multi", "unanswerable"]
    groups = {k: [r for r in rows.values() if r["kind"] == k] for k in kinds}
    groups["all"] = list(rows.values())
    answerable = lambda rs: [r for r in rs if r["kind"] != "unanswerable"]  # noqa: E731

    def n(rs, f):
        return sum(1 for r in rs if f(r))

    def cell(rs, f, base=None):
        base = rs if base is None else base
        return f"{n(rs, f)}/{len(base)}" if base else "–"

    lines = ["# End-to-end evaluation\n",
             f"Agent: {rows[questions[0]['id']]['agent_model']} with retrieval design B (k=5). "
             f"Judge: {JUDGE_MODEL}. {len(rows)} questions.\n",
             "Correct and supported come from the judge; refusals and the three code checks are computed in code.\n",
             "| | single | multi | unanswerable | all |", "|---|---|---|---|---|"]
    table = [
        ("Correct (judge)", lambda r: r["judge"]["correct"]),
        ("Supported (judge)", lambda r: r["judge"]["supported"]),
        ("Unsupported (judge)", lambda r: not r["judge"]["supported"]),
        ("Says the documents don't cover it, anywhere (code)", lambda r: r["checks"]["refusal"]["anywhere"]),
        ("… and leads with it, first 600 characters (code)", lambda r: r["checks"]["refusal"]["opening"]),
        ("Correct refusals: unanswerable, says not covered", lambda r: r["kind"] == "unanswerable" and r["checks"]["refusal"]["anywhere"]),
        ("Wrong refusals: answerable, leads with not covered", lambda r: r["kind"] != "unanswerable" and r["checks"]["refusal"]["opening"]),
        ("Wrong refusals: unanswerable, never says not covered", lambda r: r["kind"] == "unanswerable" and not r["checks"]["refusal"]["anywhere"]),
        ("Answerable with a gap caveat later in the answer", lambda r: r["kind"] != "unanswerable" and r["checks"]["refusal"]["anywhere"] and not r["checks"]["refusal"]["opening"]),
        ("(a) All citations valid (code)", lambda r: r["checks"]["citations_valid"]),
        ("(c) Cites an expected source (code)", lambda r: bool(r["checks"]["cites_expected_source"])),
        ("Citation guardrail fired", lambda r: r["stats"]["guardrail"]["fired"]),
        ("Answer flagged by the guardrail", lambda r: bool(r["stats"]["guardrail"]["unverified"])),
    ]
    for label, f in table:
        cells = []
        for k in kinds + ["all"]:
            rs = groups[k]
            if label.startswith("(c)"):
                rs_ = answerable(rs)
                cells.append(cell(rs_, f) if rs_ else "–")
            else:
                cells.append(cell(rs, f))
        lines.append(f"| {label} | " + " | ".join(cells) + " |")

    def stat(key, rs, fn):
        vals = [r["stats"][key] if key != "tokens" else r["stats"]["input_tokens"] + r["stats"]["output_tokens"] for r in rs]
        return fn(vals) if vals else 0

    lines += ["\n| Per question | single | multi | unanswerable | all |", "|---|---|---|---|---|"]
    for label, key, fn, fmt in [
        ("Tokens, average", "tokens", lambda v: sum(v) / len(v), "{:,.0f}"),
        ("Tokens, max", "tokens", max, "{:,.0f}"),
        ("Seconds, average", "seconds", lambda v: sum(v) / len(v), "{:.1f}"),
        ("Seconds, max", "seconds", max, "{:.1f}"),
        ("Model calls, average", "model_calls", lambda v: sum(v) / len(v), "{:.1f}"),
    ]:
        lines.append(f"| {label} | " + " | ".join(fmt.format(stat(key, groups[k], fn)) for k in kinds + ["all"]) + " |")
    total_in = sum(r["stats"]["input_tokens"] for r in rows.values())
    total_out = sum(r["stats"]["output_tokens"] for r in rows.values())
    lines.append(f"\nAgent totals for the run: {total_in:,} input + {total_out:,} output tokens. Seconds include the "
                 "translation step in the search tool and the guardrail's retry; tokens are the agent model's only "
                 "(the translation step adds ~270 tokens per search, see retrieval_results.md).")
    return "\n".join(lines) + "\n"


async def run_demo(before: dict) -> dict:
    """Before/after for q33: add the holdout through add_document (approved), ask again, remove the holdout."""
    from contextlib import AsyncExitStack
    import agent as ag
    import index
    import retrieval

    cache = retrieval.JsonCache(ANSWERS_CACHE)
    key_add, key_after = answer_key(f"Add the document {HOLDOUT_FILE}", "demo-add"), answer_key(before["question"], "demo-after")
    if cache.get(key_after) is None:
        try:
            async with AsyncExitStack() as stack:
                agent_obj = ag.build_agent(await ag.load_mcp_tools(stack), auto_approve=True)
                add = await ask_with_retries(ag, agent_obj, f"Add the document {HOLDOUT_FILE}")
                if not any(HOLDOUT_DOC in r and ("added" in r or "already indexed" in r) for r in tool_results(add["trace"])):
                    raise RuntimeError(f"add_document did not add the holdout: {add['trace']}")
                after = await ask_with_retries(ag, agent_obj, before["question"])
        finally:
            removed = index.delete_document(HOLDOUT_DOC)  # keep the committed index at the base corpus
            print(f"  demo: removed {removed} holdout chunks from the index", flush=True)
        cache.put(key_add, add)
        cache.put(key_after, after)
    add, after = cache.get(key_add), cache.get(key_after)

    def block(title, rec):
        trace = "\n".join(ag.short(l) for l in rec["trace"])
        s = rec["stats"]
        return (f"## {title}\n\n**Trace** ({s['model_calls']} model calls, {s['input_tokens'] + s['output_tokens']:,} "
                f"tokens, {s['seconds']} s):\n\n```text\n{trace}\n```\n\n**Answer:**\n\n{rec['answer']}\n")

    DEMO_MD.write_text(
        f"# add_document demo ({DEMO_QID})\n\n**Question:** {before['question']}\n\n"
        f"Before: the base index (201 chunks) has no passage on comparison quotes. Then `{HOLDOUT_FILE}` "
        f"({HOLDOUT_DOC}, 20 May 2026) is added through the `add_document` tool, with approval, and the question is "
        "asked again. Afterwards the holdout is removed so the committed index stays at the base corpus.\n\n"
        + block("Before (from the evaluation run)", before) + "\n"
        + block("Adding the document (approved)", add) + "\n"
        + block("After", after),
        encoding="utf-8",
    )
    return {"add": add, "after": after}


def evaluate_end_to_end() -> dict:
    import asyncio
    import agent as ag
    import index

    questions = load_questions()
    collection = index.get_collection()
    if index.stored_ids(collection, HOLDOUT_DOC):  # the "before" answers need the base corpus only
        print(f"  removing {HOLDOUT_DOC} left in the index by an earlier run", flush=True)
        index.delete_document(HOLDOUT_DOC, collection)

    answers = asyncio.run(run_answers(questions))
    lookup = ag.chunk_lookup()
    verdicts = asyncio.run(judge_answers(questions, answers, lookup))

    rows = {}
    for q in questions:
        rec = answers[q["id"]]
        rows[q["id"]] = {"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": rec["answer"],
                         "trace": rec["trace"], "stats": rec["stats"], "agent_model": ag.MODEL,
                         "checks": code_checks(q, rec, lookup), "judge": verdicts[q["id"]]}

    with ANSWERS_JSONL.open("w", encoding="utf-8") as f:
        for r in rows.values():
            f.write(json.dumps({k: r[k] for k in ("id", "kind", "question", "answer", "trace", "stats", "agent_model", "checks")},
                               ensure_ascii=False) + "\n")
    with VERDICTS_JSONL.open("w", encoding="utf-8") as f:
        for r in rows.values():
            v = r["judge"]
            f.write(json.dumps({"id": r["id"], "correct": int(v["correct"]), "supported": int(v["supported"]),
                                "correct_reasoning": v["correct_reasoning"], "supported_reasoning": v["supported_reasoning"],
                                "judge_model": JUDGE_MODEL}, ensure_ascii=False) + "\n")
    write_to_grade(questions, answers, lookup)

    summary = summarize(questions, rows)
    human = read_human_labels()
    if human:
        agree = agreement(verdicts, human)
        summary += "\n## Agreement with your labels (eval/human_labels.csv)\n\n"
        for col, a in agree.items():
            summary += f"- {col}: {a['agree']}/{a['n']} agree" + (f" ({a['agree'] / a['n']:.0%})" if a["n"] else "") + "\n"
        for col, a in agree.items():
            for d in a["disagreements"]:
                summary += (f"\n**{d['id']} {col}:** you {d['human']}, judge {d['judge']}. Your note: {d['notes'] or '–'}. "
                            f"Judge: {d['judge_reasoning']}\n")
    else:
        summary += "\nAgreement with your labels: eval/human_labels.csv has no rows yet (grade eval/to_grade.md first).\n"

    demo_q = next(q for q in questions if q["id"] == DEMO_QID)
    asyncio.run(run_demo(answers[demo_q["id"]]))
    summary += f"\nadd_document demo ({DEMO_QID}, before and after): eval/add_document_demo.md\n"
    SUMMARY_MD.write_text(summary, encoding="utf-8")
    return {"rows": rows, "summary": summary}


def main() -> None:
    problems = validate_test_set()
    print("test set locations OK" if not problems else "\n".join(problems))
    result = evaluate_retrieval()
    print("\n" + retrieval_report(result))
    print("Retrieval details: eval/retrieval_results.md and .json\n")
    try:
        e2e = evaluate_end_to_end()
    except DailyQuota as error:
        print(f"\nStopped: daily quota reached ({error}). Answers and verdicts so far are cached; "
              "run `main.py evaluate` again after the reset (09:00 in Spain) to continue.")
        sys.exit(1)
    print(e2e["summary"])


if __name__ == "__main__":
    main()
