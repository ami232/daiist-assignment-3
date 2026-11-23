"""Assignment 3: evaluation (`main.py evaluate`).

    uv run python evaluate.py retrieval   # only the retrieval comparison (cheap)
    uv run python main.py evaluate        # everything
"""

import csv
import json
import re
import statistics
import sys
import time
import subprocess
from pathlib import Path


from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI

from agent import MODEL, answer_question
from api_key import load_api_key
from index import DESIGNS, embed_texts, get_collection
from retrieve import DEFAULT_DESIGN

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
KS = (1, 3, 5)
PRICE_IN, PRICE_OUT = 0.10, 0.40  # USD per 1M tokens. ASSUMPTION: check the current price of MODEL.

LOC = re.compile(r"(?:SmPC (\d+)(?:-(\d+))?(?: of \d+)?,\s*)?pp?\.\s*(\d+)(?:\s*[-–]\s*(\d+))?")
RES = re.compile(r"^\[\d+\] (\S+) \| (.+?) \| distance", re.M)
CITE = re.compile(r"\[([^\[\]|]+?) \| ([^\[\]]+?)\]")
REFUSE = re.compile(
    r"(i don't know|i do not know|do not know|don't know|not covered|cannot find|could not find|"
    r"no information|not (?:provided|mentioned|specified|available) in)", re.I)


# ---------- test set ----------
def load_questions():
    with open(EVAL / "questions.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cols = list(rows[0].keys())

    def col(*keys):
        for k in keys:
            for c in cols:
                if c.lower() == k:
                    return c
        for k in keys:
            for c in cols:
                if k in c.lower():
                    return c
        return None

    m = {"id": col("id"), "q": col("question"), "type": col("type", "kind", "categ"),
         "src": col("source"), "loc": col("location"), "gold": col("answer")}
    print("columns used:", m)
    return rows, m


def val(r, m, key):
    return (r.get(m[key]) or "").strip() if m.get(key) else ""


def is_unanswerable(r, m):
    return "unanswer" in val(r, m, "type").lower()


def parse_loc(text):
    mt = LOC.search(text)
    if not mt:
        return None
    return int(mt.group(1) or 1), int(mt.group(3)), int(mt.group(4) or mt.group(3))


def expected_items(r, m):
    srcs = [s.strip() for s in val(r, m, "src").split(";") if s.strip()]
    locs = [s.strip() for s in val(r, m, "loc").split(";") if s.strip()]
    items = []
    for i, loc in enumerate(locs):
        s = srcs[i] if len(srcs) == len(locs) else (srcs[0] if len(srcs) == 1 else None)
        p = parse_loc(loc)
        if p:
            items.append((s, p[1], p[2]))
    return items


def parse_chunk(source, location):
    p = parse_loc(location)
    return (source, p[0], p[1], p[2]) if p else (source, 0, 0, 0)


def matches(chunk, item):
    source, v1, p1, p2 = chunk
    s, e1, e2 = item
    src_ok = s is None or s.lower() in source.lower() or source.lower() in s.lower()
    return src_ok and v1 == 1 and p1 <= e2 and e1 <= p2


def hit(chunks, items):
    return bool(items) and all(any(matches(c, it) for c in chunks) for it in items)


# ---------- stage 1: retrieval hit rate ----------
def retrieval_stage(rows, m, out):
    qs = [r for r in rows if not is_unanswerable(r, m)]
    client = genai.Client(api_key=load_api_key())
    vecs = []
    for i in range(0, len(qs), 40):
        vecs += embed_texts(client, [val(r, m, "q") for r in qs[i:i + 40]])
        if i + 40 < len(qs):
            time.sleep(30)
    table, per_q = {}, []
    for design in DESIGNS:
        coll = get_collection(design)
        if coll.count() == 0:
            print(f"{design}: empty collection; run `uv run python main.py index` first")
            continue
        res = coll.query(query_embeddings=vecs, n_results=max(KS), include=["metadatas"])
        hits = {k: 0 for k in KS}
        for r, metas in zip(qs, res["metadatas"]):
            chunks = [parse_chunk(md["source"], md["location"]) for md in metas]
            items = expected_items(r, m)
            row = {"id": val(r, m, "id"), "design": design}
            for k in KS:
                h = int(hit(chunks[:k], items))
                row[f"hit@{k}"] = h
                hits[k] += h
            per_q.append(row)
        table[design] = {k: hits[k] / len(qs) for k in KS}
    out.append(f"RETRIEVAL ({len(qs)} answerable questions; hit = same source, SmPC 1, page overlap; multi = all parts found)")
    for d, t in table.items():
        out.append(f"  {d:10s} " + "  ".join(f"hit@{k} = {t[k]:.2f}" for k in KS) + f"   ({get_collection(d).count()} chunks)")
    with open(EVAL / "retrieval_hits.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "design"] + [f"hit@{k}" for k in KS])
        w.writeheader()
        w.writerows(per_q)
    best = max(table, key=lambda d: (table[d][5], table[d][3], table[d][1]))
    out.append(f"  best design by hit rate: {best}   (retrieve.DEFAULT_DESIGN is {DEFAULT_DESIGN})")
    if best != DEFAULT_DESIGN:
        out.append(f'  >>> set DEFAULT_DESIGN = "{best}" in retrieve.py and run again')
    return table


# ---------- stage 2: agent on every question ----------
def run_agent(rows, m):
    path = EVAL / "answers.jsonl"
    done = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            if not d.get("error"):
                done[d["id"]] = d
    for r in rows:
        qid = val(r, m, "id")
        if qid in done:
            continue
        try:
            o = answer_question(val(r, m, "q"), approve=lambda action: False)
            err = None
        except Exception as e:  # noqa: BLE001
            o, err = {"answer": "", "trace": [], "input_tokens": 0, "output_tokens": 0, "seconds": 0}, str(e)[:300]
        rec = {"id": qid, "question": val(r, m, "q"), "answer": o["answer"], "trace": o["trace"],
               "guardrail": o.get("guardrail"), "input_tokens": o["input_tokens"],
               "output_tokens": o["output_tokens"], "seconds": o["seconds"], "error": err}
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        if not err:
            done[qid] = rec
        print(f"  {qid}: {'ERROR ' + err if err else 'answered'}", file=sys.stderr)
    return done


def retrieved(rec):
    text = "\n\n".join(str(t["result"]) for t in rec["trace"] if t["tool"] == "search")
    return text, [parse_chunk(s, l) for s, l in RES.findall(text)]


# ---------- code checks ----------
def code_checks(rec, r, m):
    ans = rec["answer"].replace("’", "'")
    refused = bool(REFUSE.search(ans))
    evidence, chunks = retrieved(rec)
    pages = {}
    for s, _, p1, p2 in chunks:
        pages.setdefault(s, set()).update(range(p1, p2 + 1))
    cites = []
    for block in re.findall(r"\[([^\[\]]*\|[^\[\]]*)\]", ans):
        for part in block.split(";"):
            if "|" in part:
                s, loc = part.split("|", 1)
                cites.append((s.strip(), loc))
    valid = bool(cites)
    for s, loc in cites:
        nums = [int(x) for g in re.findall(r"pp?\.\s*([\d\s,&–-]+)", loc) for x in re.findall(r"\d+", g)]
        if s not in pages or not nums or not all(n in pages[s] for n in nums):
            valid = False
    searched = any(t["tool"] == "search" for t in rec["trace"])
    if is_unanswerable(r, m):
        ok = refused
    else:
        ok = (not refused) and valid and searched
    h = None if is_unanswerable(r, m) else hit(chunks, expected_items(r, m))
    return {"refused": refused, "cited": bool(cites), "valid_cites": valid, "searched": searched,
            "agent_retrieval_hit": h, "code_ok": ok}

# ---------- LLM judge ----------
RUBRIC = """You are grading the answer of a RAG assistant that must answer only from retrieved passages.
Rubric:
- correct (1 or 0): the answer's facts match the reference answer / the evidence passages. For a question the corpus cannot answer (type: unanswerable) the ONLY correct answer is a clear "I don't know" style refusal; any specific answer is 0.
- supported (1 or 0): every factual claim in the answer is stated in the EVIDENCE passages. An honest refusal is supported. Claims from outside knowledge are 0.
Reply ONLY with JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""


def judge_all(rows, m, answers):
    path = EVAL / "judge.jsonl"
    done = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            done[d["id"]] = d
    llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=load_api_key(), temperature=0, max_retries=6)
    for r in rows:
        qid = val(r, m, "id")
        if qid in done or qid not in answers:
            continue
        rec = answers[qid]
        evidence, _ = retrieved(rec)
        prompt = (f"{RUBRIC}\n\nQUESTION: {rec['question']}\nTYPE: {val(r, m, 'type')}\n"
                  f"REFERENCE ANSWER: {val(r, m, 'gold') or '(none: judge from the evidence)'}\n\n"
                  f"EVIDENCE:\n{evidence[:14000] or '(no passages were retrieved)'}\n\nANSWER:\n{rec['answer']}")
        verdict, tin, tout = {"correct": 0, "supported": 0, "reason": "judge failed"}, 0, 0
        for attempt in range(5):
            try:
                resp = llm.invoke(prompt)
                text = resp.content if isinstance(resp.content, str) else "".join(
                    p.get("text", "") if isinstance(p, dict) else str(p) for p in resp.content)
                verdict = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
                um = resp.usage_metadata or {}
                tin, tout = um.get("input_tokens", 0), um.get("output_tokens", 0)
                break
            except Exception as e:  # noqa: BLE001
                print(f"  judge retry {attempt + 1}: {str(e)[:80]}", file=sys.stderr)
                time.sleep(20)
        d = {"id": qid, "correct": int(verdict.get("correct", 0)), "supported": int(verdict.get("supported", 0)),
             "reason": verdict.get("reason", ""), "judge_in": tin, "judge_out": tout}
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
        done[qid] = d
    return done


def to_bit(x):
    x = (x or "").strip().lower()
    if x in ("1", "yes", "y", "true", "correct", "si", "sí"):
        return 1
    if x in ("0", "no", "n", "false", "incorrect"):
        return 0
    return None


def agreement(judge, out):
    path = EVAL / "human_labels.csv"
    labels = list(csv.DictReader(open(path, newline="", encoding="utf-8"))) if path.exists() else []
    n = ac = asup = 0
    for row in labels:
        j = judge.get(row.get("id", "").strip())
        hc, hs = to_bit(row.get("correct")), to_bit(row.get("supported"))
        if j is None or hc is None or hs is None:
            continue
        n += 1
        ac += int(hc == j["correct"])
        asup += int(hs == j["supported"])
    out.append(f"HUMAN vs JUDGE: {n} graded answers" + ("  (brief asks for at least 20!)" if n < 20 else ""))
    if n:
        out.append(f"  agreement on correct: {ac / n:.0%}   on supported: {asup / n:.0%}")


# ---------- main ----------
def main(args):
    rows, m = load_questions()
    out = []
    if args and args[0] == "retrieval":
        retrieval_stage(rows, m, out)
        print("\n".join(out))
        (EVAL / "retrieval_summary.txt").write_text("\n".join(out), encoding="utf-8")
        return
    subprocess.run([sys.executable, str(ROOT / "evaluate.py"), "retrieval"], cwd=ROOT, check=True)
    out.append((EVAL / "retrieval_summary.txt").read_text(encoding="utf-8"))
    answers = run_agent(rows, m)
    missing = [val(r, m, "id") for r in rows if val(r, m, "id") not in answers]
    if missing:
        out.append(f"WARNING: no answer for {missing} (server overloaded?). Run again to retry only those.")

    with open(EVAL / "for_grading.md", "w", encoding="utf-8") as f:  # grade THESE before opening judge.jsonl
        f.write("# Answers to grade (do this before reading the judge's verdicts)\n\n")
        for r in rows:
            qid = val(r, m, "id")
            if qid in answers:
                f.write(f"## {qid}  [{val(r, m, 'type')}]\n**Q:** {answers[qid]['question']}\n\n"
                        f"**Reference:** {val(r, m, 'gold') or '-'}\n\n**Answer:**\n{answers[qid]['answer']}\n\n---\n\n")

    judge = judge_all(rows, m, answers)
    results = []
    for r in rows:
        qid = val(r, m, "id")
        if qid not in answers:
            continue
        rec, c, j = answers[qid], None, judge.get(qid, {})
        c = code_checks(rec, r, m)
        tin = rec["input_tokens"] + j.get("judge_in", 0)
        tout = rec["output_tokens"] + j.get("judge_out", 0)
        cost = (tin * PRICE_IN + tout * PRICE_OUT) / 1e6
        unans = is_unanswerable(r, m)
        if unans and not c["refused"]:
            hint = "should have refused"
        elif not unans and c["refused"]:
            hint = "wrong refusal" if c["agent_retrieval_hit"] else "retrieval miss"
        elif not unans and not c["agent_retrieval_hit"] and not j.get("correct", 1):
            hint = "retrieval miss"
        elif not unans and not j.get("correct", 1):
            hint = "wrong answer from right passage (or bad test question)"
        elif not j.get("supported", 1):
            hint = "unsupported claim"
        elif not c["code_ok"]:
            hint = "code check failed (citation?)"
        else:
            hint = ""
        results.append({"id": qid, "type": val(r, m, "type"), **c, "judge_correct": j.get("correct"),
                        "judge_supported": j.get("supported"), "guardrail": rec["guardrail"],
                        "seconds": rec["seconds"], "tokens_in": tin, "tokens_out": tout,
                        "cost_usd": round(cost, 6), "failure_hint": hint})
    with open(EVAL / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)

    n = len(results)
    ans_r = [x for x in results if "unanswer" not in x["type"].lower()]
    un_r = [x for x in results if "unanswer" in x["type"].lower()]
    out.append(f"\nEND-TO-END (model {MODEL}, retrieval design {DEFAULT_DESIGN}, {n} questions)")
    out.append(f"  code checks pass: {sum(x['code_ok'] for x in results)}/{n}")
    out.append(f"  answerable: judge correct {sum(x['judge_correct'] or 0 for x in ans_r)}/{len(ans_r)}, "
               f"supported {sum(x['judge_supported'] or 0 for x in ans_r)}/{len(ans_r)}, "
               f"wrongly refused {sum(x['refused'] for x in ans_r)}")
    out.append(f"  unanswerable: correctly refused {sum(x['refused'] for x in un_r)}/{len(un_r)}")
    out.append(f"  guardrail triggered: {sum(1 for x in results if x['guardrail'])}")
    agreement(judge, out)
    out.append(f"COST: {sum(x['cost_usd'] for x in results) / n:.5f} USD/question (agent + judge; "
               f"prices {PRICE_IN}/{PRICE_OUT} per 1M tokens are an assumption), "
               f"{statistics.mean(x['tokens_in'] + x['tokens_out'] for x in results):.0f} tokens/question, "
               f"median {statistics.median(x['seconds'] for x in results):.1f} s/question")
    (EVAL / "summary.txt").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out[len(out) - 12:]))
    print("\nFiles in eval/: results.csv, judge.jsonl, for_grading.md, retrieval_hits.csv, summary.txt")


if __name__ == "__main__":
    main(sys.argv[1:])