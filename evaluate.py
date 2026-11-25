import asyncio
import json
import re
from contextlib import AsyncExitStack
from pathlib import Path

import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import GoogleAPIError
from pydantic import BaseModel, Field

from api_key import load_api_key
from agent import QUOTE, covers, ask, build_agent, is_refusal, load_mcp_tools
from index import BATCH, SOURCES, collection, embed
from retrieval import DESIGN, Retriever

EVAL = Path("eval")
QUESTIONS = EVAL / "questions.csv"
QUERY_VECTORS = EVAL / "query_vectors.json"
ANSWERS = EVAL / "answers.json"
JUDGE = EVAL / "judge.json"
HUMAN_LABELS = EVAL / "human_labels.csv"

JUDGE_MODEL = "gemini-3.5-flash"  # stronger than the agent
JUDGE_THINKING = None
JUDGE_SETTINGS = f"{JUDGE_MODEL}, thinking {JUDGE_THINKING or 'default'}"
JUDGE_PARALLEL = 8
MAX_QUOTE_WORDS = 25
AUTHOR = {source["id"]: source["author"] for source in SOURCES}

KS = [1, 3, 5]
# hybrid needs no new embeddings
DESIGNS = [("paragraph", False), ("fixed", False), ("paragraph", True), ("fixed", True)]


def query_vectors(questions):
    saved = json.loads(QUERY_VECTORS.read_text()) if QUERY_VECTORS.exists() else {}
    todo = [q for q in questions if q not in saved]
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        saved.update(zip(batch, embed(batch, "RETRIEVAL_QUERY")))
        QUERY_VECTORS.write_text(json.dumps(saved))
    return saved


def expected_passages(row):
    for source, location in zip(row.expected_source.split(";"), row.expected_location.split(";")):
        first, _, last = location.strip("¶ ").partition("-")
        yield source, int(first), int(last or first)


def covers(chunk, passage):
    source, first, last = passage
    return chunk["source"] == source and chunk["para_start"] <= last and chunk["para_end"] >= first


def hit_rank(chunks, row):
    ranks = []
    for passage in expected_passages(row):
        rank = next((i + 1 for i, chunk in enumerate(chunks) if covers(chunk, passage)), None)
        if rank is None:
            return None
        ranks.append(rank)
    # multi needs every passage
    return max(ranks)


def evaluate_retrieval(questions, vectors):
    rows = []
    for design, hybrid in DESIGNS:
        retriever = Retriever(design, hybrid)
        for q in questions.itertuples():
            chunks = retriever.search(q.question, k=max(KS), vector=vectors[q.question])
            words = [len(c["text"].split()) for c in chunks]
            rows.append({
                "design": design + (" + hybrid" if hybrid else ""),
                "id": q.id,
                "kind": q.kind,
                "rank": None if q.kind == "unanswerable" else hit_rank(chunks, q),
                "top_similarity": chunks[0]["similarity"],
                "words@3": sum(words[:3]),
                "words@5": sum(words),
                "top_chunks": " | ".join(c["id"] for c in chunks),
            })
    return pd.DataFrame(rows)


def summarise(results):
    rows = []
    for design, group in results.groupby("design", sort=False):
        answerable = group[group["kind"] != "unanswerable"]
        rows.append({
            "design": design,
            # NaN rank counts as miss
            **{f"hit@{k}": (answerable["rank"] <= k).mean() for k in KS},
            "multi hit@5": (answerable[answerable["kind"] == "multi"]["rank"] <= 5).mean(),
            "words@3": group["words@3"].mean(),
            "words@5": group["words@5"].mean(),
            "top sim answerable": answerable["top_similarity"].mean(),
            "top sim unanswerable": group[group["kind"] == "unanswerable"]["top_similarity"].mean(),
        })
    return pd.DataFrame(rows).set_index("design")


async def run_agent(questions):
    saved = json.loads(ANSWERS.read_text()) if ANSWERS.exists() else {}
    # only new or changed questions
    todo = [q for q in questions.itertuples() if saved.get(q.id, {}).get("question") != q.question]
    if todo:
        async with AsyncExitStack() as stack:
            agent = build_agent(await load_mcp_tools(stack))
            for q in todo:
                saved[q.id] = {"question": q.question, **await ask(agent, q.question)}
                ANSWERS.write_text(json.dumps(saved, indent=1, ensure_ascii=False))
                print(f"  {q.id} answered in {saved[q.id]['seconds']} s")
    return saved


def verdict_of(answer):
    match = re.search(r"verdict:?\**\s*(said it|said something different|not in these texts)", answer, re.IGNORECASE)
    return match.group(1).lower() if match else "none"


def code_checks(q, result, chunk_meta):
    answer = result["answer"]
    cited = re.findall(r"\[([\w-]+)\]", answer)
    quotes = [m.group(1) for m in QUOTE.finditer(answer) if m.group(2)]
    retrieved = [chunk_meta[c] for c in result["passages"] if c in chunk_meta]
    expected = [] if q.kind == "unanswerable" else list(expected_passages(q))
    return {
        "verdict": verdict_of(answer),
        "refused": is_refusal(answer),
        "refusal_ok": is_refusal(answer) == (q.kind == "unanswerable"),
        "citations_valid": all(c in result["passages"] for c in cited),
        "cites_expected_source": all(any(chunk_meta.get(c, {}).get("source") == s for c in cited) for s, _, _ in expected),
        "retrieved_expected": all(any(covers(m, p) for m in retrieved) for p in expected),
        "quotes_short": all(len(qt.split()) <= MAX_QUOTE_WORDS for qt in quotes),
        "quotes_removed": len(result["removed_quotes"]),
        "refusal_rewritten": is_refusal(answer) and answer != result["model_answer"],
        "searches": sum(line.startswith("call search") for line in result["trace"]),
        "tokens": result["tokens"],
        "seconds": result["seconds"],
    }


# reasoning first, then grades
class Grade(BaseModel):
    reasoning: str = Field(description="Two or three sentences checking the answer against each criterion.")
    correct: bool = Field(description="True only if the answer meets criterion 1.")
    supported: bool = Field(description="True only if the answer meets criterion 2.")


JUDGE_PROMPT = """You are grading an attribution checker for teachers. It may only use the passages it retrieved from a fixed corpus.

Criteria:
1. Correct: the answer's verdict (said it / said something different / not in these texts) and its main claim match the reference answer. Wording may differ and extra true detail is fine. A wrong verdict, a wrong thinker, a wrong number, or covering only one side of a two-thinker question is not correct. If the reference says "Not in these texts", the answer is correct only if it says not in these texts.
2. Supported: every claim the answer makes about the thinkers or their texts, including the "why this verdict" line, is stated in or follows directly from the retrieved passages below. A claim from background knowledge fails, even if it is true. Statements about what the corpus contains are supported: it contains exactly {corpus}.

Question: {question}
Reference answer (written by a person from the texts): {reference}
Retrieved passages:
{passages}

Answer to grade:
{answer}"""


async def grade_once(grader, prompt):
    for attempt in range(4):
        try:
            return await grader.ainvoke(prompt)
        except GoogleAPIError as error:
            if "503" not in str(error) and "429" not in str(error):
                raise
            print(f"  judge busy, waiting 30 s ({error.__class__.__name__})", flush=True)
            await asyncio.sleep(30)
    raise SystemExit("The judge model is still unavailable. Saved grades are kept; run again later.")


async def judge(questions, answers):
    load_api_key()
    saved = json.loads(JUDGE.read_text()) if JUDGE.exists() else {}
    grader = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, thinking_level=JUDGE_THINKING, max_retries=1)
    grader = grader.with_structured_output(Grade)
    todo = [q for q in questions.itertuples()
            if saved.get(q.id, {}).get("answer") != answers[q.id]["answer"] or saved[q.id].get("judge") != JUDGE_SETTINGS]
    in_flight = asyncio.Semaphore(JUDGE_PARALLEL)

    async def grade(q):
        result = answers[q.id]
        passages = "\n\n".join(f"[{cid}] {p['cite_as']}\n{p['text']}" for cid, p in result["passages"].items()) or "(none)"
        prompt = JUDGE_PROMPT.format(question=q.question, reference=q.reference_answer, passages=passages, answer=result["answer"], corpus=covers())
        async with in_flight:
            verdict = await grade_once(grader, prompt)
        saved[q.id] = {"answer": result["answer"], "judge": JUDGE_SETTINGS, **verdict.model_dump()}
        JUDGE.write_text(json.dumps(saved, indent=1, ensure_ascii=False))
        print(f"  {q.id} graded", flush=True)

    await asyncio.gather(*(grade(q) for q in todo))
    return saved


def agreement(results):
    if not HUMAN_LABELS.exists():
        return None
    human = pd.read_csv(HUMAN_LABELS, keep_default_na=False)
    human = human[human["id"].str.strip() != ""]
    if human.empty:
        return None
    both = human.merge(results, on="id", suffixes=("_human", "_judge"))
    for c in ["correct", "supported"]:
        both[f"{c} agrees"] = both[f"{c}_human"].astype(int) == both[f"{c}_judge"].astype(int)
    # grades made before seeing judge
    blind = both[~both["notes"].str.lower().str.startswith("not blind")]
    return {
        "graded": len(both),
        "graded blind": len(blind),
        **{f"{c} agreement (blind)": blind[f"{c} agrees"].mean() for c in ["correct", "supported"]},
        **{f"{c} agreement (all)": both[f"{c} agrees"].mean() for c in ["correct", "supported"]},
        "human fails / judge fails (all)": f"{(both[['correct_human', 'supported_human']].astype(int) == 0).any(axis=1).sum()} / {(~both['correct_judge'] | ~both['supported_judge']).sum()}",
        "disagreements": both.loc[~(both["correct agrees"] & both["supported agrees"]), "id"].tolist(),
    }


def bands(values, outcome, edges):
    table = pd.DataFrame({"band": pd.cut(values, edges), "outcome": outcome})
    return table.groupby("band", observed=False)["outcome"].agg(["count", "mean"]).round(2)


def fit_is_right(q, result):
    want = {AUTHOR[s] for s in q.expected_source.split(";")}
    return set(list(result["fit"])[:len(want)]) == want


def main():
    questions = pd.read_csv(QUESTIONS, keep_default_na=False)
    vectors = query_vectors(questions["question"].tolist())

    print("=" * 10, "Retrieval", "=" * 10)
    retrieval = evaluate_retrieval(questions, vectors)
    retrieval.to_csv(EVAL / "retrieval_results.csv", index=False)
    summary = summarise(retrieval)
    summary.to_csv(EVAL / "retrieval_summary.csv")
    print(summary.round(2).to_string())

    print("\n" + "=" * 10, "Agent answers", "=" * 10)
    answers = asyncio.run(run_agent(questions))
    ids = [c for r in answers.values() for c in r["passages"]]
    chunk_meta = dict(zip(*[collection(DESIGN).get(ids=list(set(ids)), include=["metadatas"])[k] for k in ("ids", "metadatas")]))

    print("\n" + "=" * 10, "Code checks and judge", "=" * 10)
    grades = asyncio.run(judge(questions, answers))
    rows = []
    for q in questions.itertuples():
        grade = {k: v for k, v in grades[q.id].items() if k != "answer"}
        rows.append({"id": q.id, "kind": q.kind, **code_checks(q, answers[q.id], chunk_meta), **grade})
    results = pd.DataFrame(rows)
    results.to_csv(EVAL / "results.csv", index=False)

    answerable = results[results["kind"] != "unanswerable"]
    unanswerable = results[results["kind"] == "unanswerable"]
    print(results.groupby("kind")[["correct", "supported", "refusal_ok", "citations_valid", "cites_expected_source", "retrieved_expected", "quotes_short"]].mean().round(2).to_string())
    totals = {
        "correct": results["correct"].mean(),
        "supported": results["supported"].mean(),
        "correct refusals": int(unanswerable["refused"].sum()),
        "missed refusals": int((~unanswerable["refused"]).sum()),
        "wrong refusals": int(answerable["refused"].sum()),
        "quotes removed by guardrail": int(results["quotes_removed"].sum()),
        "refusals rewritten by guardrail": int(results["refusal_rewritten"].sum()),
        "tokens per question": results["tokens"].mean(),
        "seconds per question": results["seconds"].mean(),
        "searches per question": results["searches"].mean(),
    }
    print("\n".join(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}" for k, v in totals.items()))

    print("\n" + "=" * 10, "Agreement with my grades", "=" * 10)
    agree = agreement(results)
    print(agree or "No grades in eval/human_labels.csv yet.")

    print("\n" + "=" * 10, "Bands", "=" * 10)
    fit_rows = [(max(answers[q.id]["fit"].values()), fit_is_right(q, answers[q.id])) for q in questions.itertuples() if q.kind != "unanswerable" and answers[q.id]["fit"]]
    fit = bands(pd.Series([r[0] for r in fit_rows]), pd.Series([r[1] for r in fit_rows]), [0, 70, 90, 100])
    print("Fit share of the top thinker -> right thinker:\n", fit.to_string())
    best = pd.Series([max([p["similarity"] for p in answers[q].get("passages", {}).values()], default=0) for q in results["id"]])
    sim = bands(best, results["correct"], [0, 0.7, 0.75, 1])
    print("Best similarity -> answer correct:\n", sim.to_string())

    (EVAL / "summary.json").write_text(json.dumps({
        "retrieval": summary.round(3).reset_index().to_dict("records"),
        "end_to_end": totals,
        "agreement": agree,
        "fit_bands": fit.reset_index().astype(str).to_dict("records"),
        "similarity_bands": sim.reset_index().astype(str).to_dict("records"),
    }, indent=1, default=float))


if __name__ == "__main__":
    main()
