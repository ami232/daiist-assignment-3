"""Every number in REPORT.md, recomputed from the committed files. Offline: no API calls.

If a result file changes, the sentence in REPORT.md that quotes it must change too, or this test fails.
The index is opened from a temporary copy, so running the test leaves index/ untouched.
"""

import csv
import inspect
import json
import re
import shutil
import statistics
from collections import Counter
from pathlib import Path

import pytest

import agent
import evaluate
import index

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval"
REPORT = (ROOT / "REPORT.md").read_text(encoding="utf-8")
PLAIN = REPORT.replace("**", "")  # bold marks don't change a number
SUMMARY = json.loads((EVAL / "summary.json").read_text(encoding="utf-8"))
ANALYSIS = SUMMARY["analysis"]
QUESTIONS = evaluate.read_csv(EVAL / "questions.csv")
ANSWERS = [json.loads(line) for line in (EVAL / "answers.jsonl").open(encoding="utf-8")]
BY_ID = {a["id"]: a for a in ANSWERS}
RETRIEVAL = {(r["design"], r["questions"]): r for r in csv.DictReader((EVAL / "retrieval.csv").open(encoding="utf-8"))}
TRANSCRIPT = (EVAL / "subagent_transcript.txt").read_text(encoding="utf-8")
U_SPACE = "reg_2021_664_u-space.html"


def says(text: str) -> None:
    assert text in PLAIN, f"REPORT.md should say: {text}"


def f3(x) -> str:
    return f"{float(x):.3f}"


def searches(a: dict) -> int:
    return sum(name == "search" for name, _ in a["tool_calls"])


@pytest.fixture(scope="module")
def index_copy(tmp_path_factory):
    """index/ copied to a temporary folder, because ChromaDB rewrites its files when it opens them."""
    copy = tmp_path_factory.mktemp("index") / "index"
    shutil.copytree(ROOT / "index", copy)
    saved, index.INDEX_DIR = index.INDEX_DIR, copy
    yield
    index.INDEX_DIR = saved


def stored(design: str) -> dict[str, list]:
    """source -> [(chunk number, location, words)] in chunk order."""
    got = index.collection(design).get(include=["documents", "metadatas"])
    out: dict[str, list] = {}
    for doc, m in zip(got["documents"], got["metadatas"]):
        out.setdefault(m["source"], []).append((m["chunk"], m["location"], doc.split()))
    return {s: sorted(c, key=lambda c: c[0]) for s, c in out.items()}


def rebuilt_words(chunks: list, size: int) -> int:
    """Words in the extracted text, rebuilt from the chunks: a chunk that continues the previous one
    (same location, previous chunk full, overlapping words equal) adds only its words after the overlap."""
    overlap, total, prev = size // 5, 0, None
    for _, loc, words in chunks:
        continues = (prev is not None and prev[0] == loc and len(prev[1]) == size
                     and words[:overlap] == prev[1][-overlap:])
        total += len(words) - overlap if continues else len(words)
        prev = (loc, words)
    return total


# ---------- 2-3. corpus and ingestion ----------

def test_corpus_words_and_chunk_counts(index_copy):
    w150, w400 = stored("w150"), stored("w400")
    words = {s: rebuilt_words(w150[s], 150) for s in w150}
    assert set(w400) == set(w150) - {U_SPACE}, "add_document only adds to the chosen design"
    assert all(rebuilt_words(w400[s], 400) == words[s] for s in w400), "both designs give the same words"

    regs = ["Reg 2019/947", "Reg 2019/945", "EASA AMC-GM Part-UAS"]
    for s in regs:
        says(f"| {words[s]:,} |")
    says(f"| Total | | | | {sum(words[s] for s in regs):,} |")
    says(f"Regulation (EU) 2021/664 on U-space ({words[U_SPACE]:,} words)")
    says("rebuilt from the chunks stored in `index/`")
    says("a fresh download and extraction of all three gave these counts and the same chunks as the committed index")

    c150, c400 = ({s: len(c) for s, c in d.items()} for d in (w150, w400))
    says(f"| `w150` (150 words) | {' | '.join(str(c150[s]) for s in regs)} | {sum(c150[s] for s in regs)} "
         f"(+{c150[U_SPACE]} from Reg 2021/664) |")
    says(f"| `w400` (400 words) | {' | '.join(str(c400[s]) for s in regs)} | {sum(c400[s] for s in regs)} |")
    says(f"({c150[U_SPACE]} chunks)")


def test_rebuild_matches_the_fresh_extraction(index_copy):
    # what `main.py index` logged on 23 November 2026 after downloading the three files again
    logged = {"Reg 2019/947": 19100, "Reg 2019/945": 20428, "EASA AMC-GM Part-UAS": 16807}
    w150 = stored("w150")
    assert {s: rebuilt_words(w150[s], 150) for s in logged} == logged


def test_index_settings_and_size():
    files = [p for p in (ROOT / "index").rglob("*") if p.is_file() and p.name != ".gitkeep"]
    says(f"ChromaDB in `index/chroma` ({sum(p.stat().st_size for p in files) / 1e6:.1f} MB")
    says(f"`{index.EMBED_MODEL}`, {index.EMBED_DIM} dimensions")
    assert index.DESIGNS == {"w150": 150, "w400": 400} and index.CHOSEN_DESIGN == "w150"
    says("word windows of 150 or 400 words with 20% overlap (step 120 or 320)")


# ---------- 4. test set ----------

def test_test_set_counts():
    kinds = Counter(q["kind"] for q in QUESTIONS)
    says(f"{len(QUESTIONS)} questions in `eval/questions.csv`: {kinds['single']} single, {kinds['multi']} multi "
         f"(two passages) and {kinds['unanswerable']} unanswerable.")


# ---------- 5. retrieval ----------

DESIGN_LABELS = {"w150": "`w150` (150-word chunks)", "w400": "`w400` (400-word chunks)",
                 "bm25": "`bm25` (keywords only, `w150` chunks)", "w150+bm25": "`w150+bm25` (hybrid)"}


def test_retrieval_tables():
    for design, label in DESIGN_LABELS.items():
        r = RETRIEVAL[(design, "all")]
        assert r["n"] == "26"
        says(f"| {label} | {f3(r['hit@1'])} | {f3(r['hit@3'])} | {f3(r['hit@5'])} | {f3(r['all@5'])} "
             f"| {f3(r['mrr@5'])} | {int(r['avg_words_top5']):,} |")
        s, m = RETRIEVAL[(design, "single")], RETRIEVAL[(design, "multi")]
        assert (s["n"], m["n"]) == ("20", "6")
        says(f"| `{design}` | {f3(s['hit@1'])} | {f3(s['mrr@5'])} | {f3(m['hit@5'])} | {f3(m['all@3'])} "
             f"| {f3(m['all@5'])} |")


def test_retrieval_prose():
    w150, w400 = RETRIEVAL[("w150", "all")], RETRIEVAL[("w400", "all")]
    hybrid, bm25 = RETRIEVAL[("w150+bm25", "all")], RETRIEVAL[("bm25", "all")]
    says(f"MRR@5 {f3(w150['mrr@5'])} against {f3(w400['mrr@5'])}")
    says(f"all@5 {f3(RETRIEVAL[('w400', 'multi')]['all@5'])} against {f3(RETRIEVAL[('w150', 'multi')]['all@5'])}")
    says(f"MRR@5 {f3(hybrid['mrr@5'])} against {f3(w150['mrr@5'])}")
    says(f"only {round(float(bm25['hit@5']) * 26)} of the 26 questions (hit@5 {f3(bm25['hit@5'])})")
    assert all(float(hybrid[c]) <= float(w150[c]) for c in ("hit@1", "hit@3", "hit@5", "all@5", "mrr@5"))

    params = inspect.signature(index.bm25_ranking).parameters
    assert (params["k1"].default, params["b"].default) == (1.5, 0.75)
    params = inspect.signature(index.retrieve_hybrid).parameters
    assert (params["rrf_k"].default, params["pool"].default) == (60, 50)
    says("BM25 with k1 = 1.5 and b = 0.75")
    says("reciprocal rank fusion, with k = 60, over the top 50 of each")


def test_which_multi_passages_are_found(index_copy):
    vecs = json.loads(evaluate.QUERY_VECS.read_text(encoding="utf-8"))
    multi = [q for q in QUESTIONS if q["kind"] == "multi"]
    found, missing = {}, []
    for design in ("w150", "w400"):
        found[design] = []
        for q in multi:
            hits = index.retrieve(q["question"], design, k=5, query_vec=vecs[q["question"]], sources=evaluate.CORPUS)
            gone = [loc for src, loc in evaluate.expected(q) if not any(evaluate.is_hit(h, [(src, loc)]) for h in hits)]
            if not gone:
                found[design].append(q["id"])
            elif design == "w150":
                missing.append(f"`{gone[0]}` in {q['id']}")
    says(f"`w150` finds both passages for {len(found['w150'])} of 6 ({', '.join(found['w150'])})")
    says(f"`w400` for {len(found['w400'])} of 6 ({', '.join(found['w400'])})")
    says("With `w150` the top 5 misses " + ", ".join(missing[:-1]) + " and " + missing[-1] + ".")


# ---------- 6-7. tools, subagent, harness ----------

def test_the_demo_chunks_do_not_change_dense_retrieval(index_copy):
    says("Every design searches only the three corpus documents")
    says("with them included, the dense designs' hit@k, all@k and MRR@5 are the same")
    vecs = json.loads(evaluate.QUERY_VECS.read_text(encoding="utf-8"))
    for design in index.DESIGNS:
        for q in (q for q in QUESTIONS if q["kind"] != "unanswerable"):
            exp, v = evaluate.expected(q), vecs[q["question"]]
            ranks = []
            for sources in (evaluate.CORPUS, None):
                hits = index.retrieve(q["question"], design, k=5, query_vec=v, sources=sources)
                first = next((r for r, h in enumerate(hits, start=1) if evaluate.is_hit(h, exp)), None)
                every = [all(any(evaluate.is_hit(h, [e]) for h in hits[:k]) for e in exp) for k in (1, 3, 5)]
                ranks.append((first, every))
            assert ranks[0] == ranks[1], (design, q["id"])


def test_search_example_and_harness_settings():
    says(next(line for line in BY_ID["q05"]["retrieved_text"].splitlines()
              if line.startswith("[3] Reg 2019/947, UAS.OPEN.040")))
    assert agent.MODEL == "gemini-3.1-flash-lite"
    src = inspect.getsource(agent.run)
    assert "ModelCallLimitMiddleware(run_limit=6" in src and 'tool_name="search", run_limit=3' in src
    says("at most 6 model calls and 3 `search` calls per agent run")


def test_transcript_matches_the_full_log():
    block = REPORT.split("**Transcript from Claude Code**", 1)[1].split("```text", 1)[1].split("```", 1)[0]
    command = next(line for line in block.splitlines() if line.startswith("$ claude"))
    assert command in TRANSCRIPT
    report_part = block.split("corpus-researcher report:", 1)[1].split("● Claude Code answer:", 1)
    for part in (report_part[0], report_part[1].split("(2 turns", 1)[0]):
        for line in part.splitlines():
            if line.strip():
                assert line.strip() in TRANSCRIPT, f"not in the full transcript: {line.strip()[:80]}"
    queries = re.findall(r'"query": "(.+?)"', TRANSCRIPT)
    assert len(queries) == 4 and all(f'search(query="{q}")' in block for q in queries)
    for header in re.findall(r"^\[(\d)\] (.+?) \(score ([\d.]+)\)$", TRANSCRIPT, re.MULTILINE):
        assert f"[{header[0]}] {header[1]} ({header[2]})" in block
    result = re.search(r"=== result: success, (\d+) turns, ([\d.]+) s, (\$[\d.]+) of Claude usage ===", TRANSCRIPT)
    says(f"({result[1]} turns, {result[2]} s, {result[3]} of Claude usage; the subagent made {len(queries)} search calls)")
    says(f"The subagent made {len(queries)} searches, although its instructions allow at most 3")
    assert "max 3 searches" in (ROOT / ".claude/agents/corpus-researcher.md").read_text(encoding="utf-8")
    says("CLI 2.1.330")
    assert "Claude Code 2.1.330" in TRANSCRIPT


def test_citation_check_numbers():
    fired = [a for a in ANSWERS if a["guardrail"] != "passed"]
    assert all(a["guardrail"].startswith("retried:") for a in fired)
    says(f"In the v1 run it fired on {len(fired)} of {len(ANSWERS)} questions. All {len(fired)} passed after the retry")
    labels = {"two citations in one bracket": "Two citations in one bracket, `[A, x; B, y]`",
              "passage number as source": "The passage number used as the source, `[5, AMC1 UAS.OPEN.30(1)]`",
              "location finer than the stored one": "A location finer than the stored one, `Article 14(5)(a)(i)`",
              "two locations after one source": "Two locations after one source",
              "no citations (refusal without the exact phrase)":
                  "No citation at all: a refusal that didn't start with the exact phrase"}
    by_pattern: dict[str, list] = {}
    for a in fired:
        for p in evaluate.guardrail_patterns(a["guardrail"]):
            by_pattern.setdefault(p, []).append(a["id"])
    assert set(by_pattern) == set(labels)
    for p, ids in by_pattern.items():
        says(f"| {labels[p]} | {len(ids)} ({', '.join(ids)}) |")
    form = ("two citations in one bracket", "passage number as source", "two locations after one source")
    n_form, n_all = sum(len(by_pattern[p]) for p in form), sum(len(ids) for ids in by_pattern.values())
    says(f"{({6: 'Six', 7: 'Seven', 8: 'Eight'})[n_form]} of the {n_all} problems are about the citation's format")
    q25 = BY_ID["q25"]
    assert "Article 14(5)(a)(i)" in q25["guardrail"] and "Part 2(1)" in q25["guardrail"]
    assert {("Reg 2019/947", "Article 14"),
            ("Reg 2019/945", "PART 2 Requirements for a class C1 Unmanned aircraft system")} <= set(
        map(tuple, q25["citations"]))
    assert "[5, AMC1 UAS.OPEN.30(1)]" in BY_ID["q04"]["guardrail"]
    assert searches(BY_ID["q23"]) == 4 and BY_ID["q23"]["retrieved_text"].count("Tool call limit exceeded") == 1
    says("q23 requested 4; 3 ran")


# ---------- 8. evaluation ----------

def results() -> list[dict]:
    return evaluate.grade_all(QUESTIONS, BY_ID)


def test_outcomes_by_kind():
    rows = results()
    counts = Counter((r["kind"], evaluate.outcome(r)) for r in rows)
    total = Counter(evaluate.outcome(r) for r in rows)
    assert dict(total) == {k: v for k, v in SUMMARY["outcomes"].items() if v}
    assert len(ANSWERS) == 32 and len(evaluate.read_jsonl(evaluate.JUDGE)) == 26
    says(f"The agent answered all {len(ANSWERS)} questions")
    says(f"It grades the {len(evaluate.read_jsonl(evaluate.JUDGE))} answers to answerable questions")

    def cell(kind, outcome, applies):
        return str(counts[(kind, outcome)]) if applies else "–"

    for label, outcome, kinds in [("Correct", "correct", ("single", "multi")),
                                  ("Unsupported", "unsupported", ("single", "multi")),
                                  ("Wrong", "wrong", ("single", "multi")),
                                  ("Wrong refusal", "wrong refusal", ("single", "multi")),
                                  ("Correct refusal", "correct refusal", ("unanswerable",)),
                                  ("Answered an unanswerable question", "answered unanswerable", ("unanswerable",))]:
        cells = " | ".join(cell(k, outcome, k in kinds) for k in ("single", "multi", "unanswerable"))
        says(f"| {label} | {cells} | {total[outcome]} |")


def test_retrieval_inside_the_agent_runs():
    r = ANALYSIS["agent_retrieval"]
    assert r == evaluate.agent_retrieval(QUESTIONS, BY_ID)
    says(f"at least one expected passage was retrieved for {r['any_expected']} of the {r['answerable']} answerable "
         f"questions, and every expected passage for {r['all_expected']}")
    assert r["missed_every_expected_passage"] == ["q04"]
    assert {(s, loc.split(" UAS operations")[0]) for s, loc in map(tuple, BY_ID["q04"]["citations"])} == {
        ("EASA AMC-GM Part-UAS", "AMC1 UAS.OPEN.30(1)"), ("EASA AMC-GM Part-UAS", "GM1 UAS.OPEN.30(1)")}
    says("q04 retrieved none of its expected passages and answered from the EASA guidance on the same rule")
    multi_missed = [i for i in r["missed_an_expected_passage"] if i != "q04"]
    says(f"{', '.join(multi_missed[:-1])} and {multi_missed[-1]} each missed one of their two passages, so only "
         f"{len(r['multi_with_all_expected'])} of the 6 multi questions ({', '.join(r['multi_with_all_expected'])}) "
         "had both")


def test_rates_and_intervals():
    labels = {"handled_correctly": "Handled correctly (correct answers + correct refusals)",
              "correct_of_answerable": "Correct, of the 26 answerable",
              "unsupported_of_answerable": "Unsupported, of the 26 answerable",
              "refused_of_unanswerable": "Refused, of the 6 unanswerable",
              "citations_valid": "Citations valid"}
    for key, label in labels.items():
        r = ANALYSIS["rates_wilson95"][key]
        assert r["ci"] == evaluate.wilson(r["k"], r["n"])
        says(f"| {label} | {r['k']} / {r['n']} = {f3(r['rate'])} | {f3(r['ci'][0])}–{f3(r['ci'][1])} |")
    h = ANALYSIS["rates_wilson95"]["handled_correctly"]
    says(f"0.812, 95% interval {f3(h['ci'][0])}–{f3(h['ci'][1])}")
    u = ANALYSIS["rates_wilson95"]["refused_of_unanswerable"]
    says(f"the refusal rate of 5/6 has a 95% interval of {f3(u['ci'][0])}–{f3(u['ci'][1])}")


def test_agreement_with_my_grades():
    a = evaluate.agreement(results())
    assert a == SUMMARY["judge_vs_me"]
    n = a["graded_by_me"]
    says(f"I graded {n} answers myself (q01–q20, `eval/human_labels.csv`)")
    kappa_correct = "undefined" if a["kappa_correct"] is None else f"{a['kappa_correct']:.2f}"
    says(f"| *correct* | {a['agree_correct']:.0%} ({round(a['agree_correct'] * n)} / {n}) | {kappa_correct} |")
    says(f"| *supported* | {a['agree_supported']:.0%} ({round(a['agree_supported'] * n)} / {n}) | "
         f"{a['kappa_supported']:.2f} |")
    says("The three disagreements are " + ", ".join(a["disagreements"][:-1]) + " and " + a["disagreements"][-1])
    labels = evaluate.read_csv(EVAL / "human_labels.csv")
    assert all(q["kind"] == "single" for q in QUESTIONS if q["id"] in {h["id"] for h in labels})


def test_version_note_and_refusals():
    v = ANALYSIS["version_note"]
    says(f"added one to {v['answers']} of the {v['of']} answers")
    assert evaluate.VERSION_NOTE.search(BY_ID["q05"]["answer"])
    says("including answers that do not depend on dates, such as q05 (150 m from residential areas in A3)")
    says(f"The sentence is in {v['answers']} of the {v['of']} answers and in {v['judged_with_note']} of the "
         f"{v['judged']} judged ones. The judge marked only {len(v['judged_with_note_unsupported'])} of those "
         f"{v['judged_with_note']} unsupported ({', '.join(v['judged_with_note_unsupported'])})")
    says(f"only to {len(v['judged_with_note_unsupported'])} of the {v['judged_with_note']} answers that contain the note")
    r = ANALYSIS["refusals"]
    assert r["exact_prefix"] == ["q27", "q28", "q29", "q30", "q31"] and r["refusal_in_other_words"] == ["q32"]
    assert r["partly_refused_answers"] == ["q23", "q26"]
    says("Five of the six unanswerable questions were refused with the exact phrase (q27–q31)")


def test_judge_stability():
    stab = SUMMARY["judge_stability"]
    assert stab == evaluate.judge_stability()
    again = evaluate.read_jsonl(EVAL / "judge_rerun.jsonl")
    assert len(again) == stab["rejudged"] == 26
    flipped = len(set(stab["flips_correct"]) | set(stab["flips_supported"]))
    says(f"A second pass over all {stab['rejudged']} judged answers")
    says(f"changed no verdict: {flipped} of {stab['rejudged']} flipped" if flipped == 0
         else f"{flipped} of {stab['rejudged']} flipped")
    unsupported = sorted(i for i, v in again.items() if v["supported"] == 0)
    assert unsupported == ANALYSIS["version_note"]["judged_with_note_unsupported"]
    says("both passes flag the same 4 answers")


def test_judge_audit_facts():
    q21 = BY_ID["q21"]
    assert {s for s, _ in map(tuple, q21["citations"])} == {"EASA AMC-GM Part-UAS"}
    assert all(loc.startswith("AMC1 UAS.OPEN.30(1)") for _, loc in map(tuple, q21["citations"]))
    parts = {loc.split(" ")[0] + " " + loc.split(" ")[1] for s, loc in map(tuple, q21["passages"])
             if s == "Reg 2019/945"}
    assert {"PART 2", "PART 3"} <= parts
    says("Reg 2019/945 `PART 2` and `PART 3` were retrieved")


def test_add_document_demo(index_copy):
    demo = (EVAL / "add_document_demo.md").read_text(encoding="utf-8")
    before = demo.split("## Before", 1)[1].split("##", 1)[0].strip()
    assert before == "The corpus does not cover this."
    says(f'- Before: "{before}"')
    assert "[reg_2021_664_u-space.html, Article 3]" in demo and "Article 7" in demo
    assert evaluate.DEMO_ID == "q31"


# ---------- 9. failures, cost, decision ----------

def test_failures_table():
    rows = evaluate.read_csv(EVAL / "failures.csv")
    for r in rows:
        says(f"| {r['id']} | {r['kind']} | {r['outcome']} | {r['cause']} |")
    causes = Counter(r["cause"] for r in rows)
    for label in ("Unsupported claim", "Retrieval miss", "Bad test question", "Wrong answer from the right passage",
                  "Wrong refusal"):
        says(f"| {label} | {causes[label.lower()]} |")


def test_q26_and_q32_evidence(index_copy):
    q26 = BY_ID["q26"]
    assert searches(q26) == 1 and not any(loc.startswith("UAS.OPEN.050") for _, loc in map(tuple, q26["passages"]))
    vecs = json.loads(evaluate.QUERY_VECS.read_text(encoding="utf-8"))
    question = next(q["question"] for q in QUESTIONS if q["id"] == "q26")
    hits = index.retrieve(question, "w150", k=5, query_vec=vecs[question], sources=evaluate.CORPUS)
    assert any(h["location"].startswith("UAS.OPEN.050") for h in hits)
    singles = sum(searches(a) == 1 for a in ANSWERS)
    says(f"{singles} of the {len(ANSWERS)} runs made a single search")
    q32 = BY_ID["q32"]
    assert q32["answer"].startswith("The corpus does not specify a set number of days")
    assert any(loc.startswith("UAS.SPEC.040") for _, loc in map(tuple, q32["citations"]))
    assert "without undue delay" in q32["retrieved_text"]


def test_cost_and_latency():
    tokens = [a["input_tokens"] + a["output_tokens"] for a in ANSWERS]
    t, s = ANALYSIS["tokens"], ANALYSIS["seconds"]
    assert t["mean"] == round(statistics.mean(tokens)) and t["median"] == statistics.median(tokens)
    says(f"| Tokens (input + output) | {t['mean']:,} ({t['mean_input']:,} + {t['mean_output']:,}) | "
         f"{round(t['median']):,} |")
    says(f"| Seconds | {s['mean']} | {s['median']} |")
    slow = sorted((a for a in ANSWERS if a["seconds"] > evaluate.SLOW_RUN_S), key=lambda a: -a["seconds"])
    says(f"Three runs took over 100 s: {slow[0]['id']} ({slow[0]['seconds']:.0f} s), {slow[1]['id']} "
         f"({slow[1]['seconds']:.0f} s) and {slow[2]['id']} ({slow[2]['seconds']:.0f} s)")
    assert len(slow) == 3
    says(f"Without those three runs the mean is {s['mean_without_runs_over_100s']} s")
    sr = ANALYSIS["searches"]
    says(f"The evaluation run made {sr['executed']} searches ({sr['requested']} requested, {sr['blocked']} blocked)")
    assert sr["requested"] == sum(searches(a) for a in ANSWERS)

    c = ANALYSIS["cost_paid_tier"]
    p = evaluate.PRICE_USD
    says(f"Gemini 3.1 Flash-Lite ${p['agent_input']:.2f} per million input tokens and ${p['agent_output']:.2f} "
         f"per million output tokens; Gemini Embedding 2 ${p['embedding_input']:.2f} per million tokens")
    says(f"the mean question costs ${c['usd_per_question_agent']} in model tokens plus at most "
         f"${c['usd_per_question_query_embeddings_max']:.7f} for its query embeddings")
    says(f"counting {evaluate.TOKENS_PER_WORD_MAX} tokens per word")
    says(f"ECB reference rate of {evaluate.USD_PER_EUR:.4f} USD per euro (20 November 2026)")
    says(f"€{c['eur_per_question']:.4f} per question, or €{c['eur_per_1000_questions']:.2f} per 1,000 questions")


# ---------- v2 ----------

V2_DIR = EVAL / "v2"
V2 = json.loads((V2_DIR / "summary.json").read_text(encoding="utf-8"))
V2_ANSWERS = {a["id"]: a for a in map(json.loads, (V2_DIR / "answers.jsonl").open(encoding="utf-8"))}


def outcomes_of(judge_file: Path, answers: dict, monkeypatch) -> dict:
    monkeypatch.setattr(evaluate, "JUDGE", judge_file)
    return {r["id"]: evaluate.outcome(r) for r in evaluate.grade_all(QUESTIONS, answers)}


def test_v2_against_v1(monkeypatch):
    v1 = outcomes_of(EVAL / "judge.jsonl", BY_ID, monkeypatch)
    v2 = outcomes_of(V2_DIR / "judge.jsonl", V2_ANSWERS, monkeypatch)
    assert dict(Counter(v2.values())) == {k: n for k, n in V2["outcomes"].items() if n}
    for label, key in [("Correct", "correct"), ("Unsupported", "unsupported"), ("Wrong", "wrong"),
                       ("Correct refusal", "correct refusal"), ("Answered an unanswerable question", "answered unanswerable")]:
        says(f"| {label} | {Counter(v1.values())[key]} | {Counter(v2.values())[key]} |")
    good = {"correct", "correct refusal"}
    fixed = sorted(i for i in v1 if v1[i] not in good and v2[i] in good)
    worse = sorted(i for i in v1 if v1[i] in good and v2[i] not in good)
    assert fixed == ["q07", "q08", "q10", "q21", "q26", "q32"] and worse == []
    assert sorted(i for i in v1 if v1[i] != v2[i]) == fixed
    says("Six questions changed, all from a failure to a pass, and none the other way")

    h1, h2 = ANALYSIS["rates_wilson95"]["handled_correctly"], V2["analysis"]["rates_wilson95"]["handled_correctly"]
    says(f"| Handled correctly (95% interval) | {h1['k']} / {h1['n']} ({f3(h1['ci'][0])}–{f3(h1['ci'][1])}) | "
         f"{h2['k']} / {h2['n']} ({f3(h2['ci'][0])}–{f3(h2['ci'][1])}) |")
    c2 = V2["analysis"]["rates_wilson95"]["citations_valid"]
    says(f"| Citations valid | 32 / 32 | {c2['k']} / {c2['n']} |")
    fired2 = sum(a["guardrail"] != "passed" for a in V2_ANSWERS.values())
    assert fired2 == V2["guardrail_fired"]
    says(f"| Citation check fired | {SUMMARY['guardrail_fired']} | {fired2} |")
    if fired2 == 0:
        says("v2 does both (section 9), and the check did not fire once in its 32 runs")

    def single(answers) -> int:
        return sum(searches(a) == 1 for a in answers)

    says(f"| Searches (runs with a single search) | {sum(searches(a) for a in ANSWERS)} ({single(ANSWERS)}) | "
         f"{sum(searches(a) for a in V2_ANSWERS.values())} ({single(V2_ANSWERS.values())}) |")
    m1 = len(ANALYSIS["agent_retrieval"]["multi_with_all_expected"])
    m2 = len(V2["analysis"]["agent_retrieval"]["multi_with_all_expected"])
    says(f"| Multi questions with both passages retrieved in the run | {m1} of 6 | {m2} of 6 |")
    t1, t2 = ANALYSIS["tokens"], V2["analysis"]["tokens"]
    says(f"| Tokens per question, mean / median | {t1['mean']:,} / {round(t1['median']):,} | "
         f"{t2['mean']:,} / {round(t2['median']):,} |")
    says(f"median {V2['analysis']['seconds']['median']} s, inflated by retry waits")
    says(f"v2 costs €{V2['analysis']['cost_paid_tier']['eur_per_1000_questions']:.2f} per 1,000")


def test_v2_fixes_as_described():
    q26 = V2_ANSWERS["q26"]
    assert searches(q26) == 1 and any(loc.startswith("UAS.OPEN.050") for _, loc in map(tuple, q26["passages"]))
    assert "informed of the risks" in q26["answer"]
    assert BY_ID["q26"]["tool_calls"][0][1]["query"].endswith("operator requirements for people taking part")
    assert q26["tool_calls"][0][1]["query"].endswith("operator ensure people taking part")
    says("worded slightly differently (\"…operator ensure people taking part\" instead of "
         "\"…operator requirements for people taking part\")")
    says(f"{sum(searches(a) == 1 for a in V2_ANSWERS.values())} of the 32 runs still made one search")
    q32 = V2_ANSWERS["q32"]
    assert q32["answer"].startswith("The corpus does not cover") and "without undue delay" in q32["answer"]
    header = next(line for line in V2_ANSWERS["q05"]["retrieved_text"].splitlines()
                  if line.startswith("Passage 3 ") and "UAS.OPEN.040" in line)
    says(header)
    assert V2["analysis"]["version_note"]["judged_with_note_unsupported"] == []

