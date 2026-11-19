"""
Assignment 3: the add-document demo. `uv run python demo_add_document.py`

Takes a question the corpus cannot answer (q31: the minimum wage in 2025), adds the document
that can answer it (Real Decreto 87/2025, in demo/), and asks again. Steps:

  1. BEFORE   ask the question                          -> the agent should refuse
  2. NO       ask the agent to add the document; you are asked and the script says NO
              (so you see that nothing is added without approval)
  3. YES      ask again; YOU are asked in the terminal: type y
  4. AFTER    ask the question again                    -> the agent should now answer, citing the new document
  5. TWICE    ask to add the same file again            -> skipped: already indexed
  6. RENAMED  ask to add a copy of it with another name -> skipped too (same content)

It changes index/ (only on step 3). When it is done it tells you how to put index/ back, so that
the committed index stays the one the evaluation was run on. The transcript is saved in
eval/add_document_demo.md (and .json) for the report.
"""

import json
import shutil
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import agent  # noqa: E402
import index as ix  # noqa: E402

DOC = ROOT / "demo" / "Real_Decreto_87-2025_SMI_2025.pdf"
COPY = ROOT / "demo" / "copia_del_decreto.pdf"
OUT_MD = ROOT / "eval" / "add_document_demo.md"
OUT_JSON = ROOT / "eval" / "add_document_demo.json"
QUESTION = "¿Cuál era el salario mínimo interprofesional en 2025?"
SOURCE_ID = "real_decreto_87-2025_smi_2025"  # what index.py names a source from the file name
SHORT = 400  # characters of a tool result kept in the transcript


class Approver:
    """Remembers every approval request and what was answered."""

    def __init__(self, mode: str):
        self.mode, self.asked = mode, []  # mode: 'no', 'yes', 'terminal'

    def __call__(self, tool_name: str, args: dict) -> bool:
        if self.mode == "terminal":
            decision = agent.ask_in_terminal(tool_name, args)
        else:
            decision = self.mode == "yes"
        self.asked.append({"tool": tool_name, "args": args, "approved": decision})
        return decision


def index_state() -> dict:
    return {"chunks": len(ix.read_chunks()), "documents": sorted(ix.load_documents()),
            "index_mb": round(ix.index_size_mb(), 2)}


def step(number: int, label: str, prompt: str, mode: str, records: list[dict]) -> dict:
    print("\n" + "=" * 78)
    print(f"STEP {number}: {label}")
    print(f"You ask: {prompt}")
    if mode == "terminal":
        print("(the assistant will ask for your approval below: type y and press Enter)")
    print("=" * 78, flush=True)
    approver = Approver(mode)
    before = index_state()
    result = agent.ask(prompt, approve=approver)
    after = index_state()
    print("\n" + (result.error and f"ERROR: {result.error}" or agent.render(result)))
    record = {
        "step": number, "label": label, "prompt": prompt, "approval_requests": approver.asked,
        "answer": result.answer, "sources": result.sources, "refused": result.refused,
        "guardrail": result.guardrail, "model": result.model, "seconds": result.seconds,
        "error": result.error,
        "tool_calls": [{"tool": c["tool"], "args": c["args"], "status": c["status"],
                        "result": c["result"][:SHORT]} for c in result.trace],
        "index_before": before, "index_after": after,
    }
    records.append(record)
    return record


def check(ok: bool, text: str) -> bool:
    print(f"  [{'OK' if ok else 'CHECK'}] {text}")
    return ok


def add_calls(record: dict) -> list[dict]:
    return [c for c in record["tool_calls"] if c["tool"] == "add_document"]


def main() -> None:
    if not DOC.is_file():
        sys.exit(f"The document is missing: {DOC.relative_to(ROOT)}. See the instructions for step 8c.")
    if SOURCE_ID in ix.load_documents():
        sys.exit("The decree is already in your index (an earlier run?). Put index/ back first:\n"
                 "  git checkout -- index/ && rm -f index/documents.json\nThen run this again.")
    start = index_state()
    print(f"Index before: {start['chunks']} chunks (design B), {start['index_mb']} MB, "
          f"documents added so far: {start['documents'] or 'none'}")

    records: list[dict] = []
    add_prompt = f"Por favor, añade este documento al corpus: {DOC}"
    s1 = step(1, "BEFORE: a question the corpus cannot answer", QUESTION, "no", records)
    s2 = step(2, "NO: the assistant is asked to add the document and the answer is NO", add_prompt, "no", records)
    s3 = step(3, "YES: you approve adding the document", add_prompt, "terminal", records)
    s4 = step(4, "AFTER: the same question again", QUESTION, "no", records)
    s5 = step(5, "TWICE: add the same file again", add_prompt, "yes", records)
    shutil.copyfile(DOC, COPY)
    try:
        s6 = step(6, "RENAMED: add a copy of the file under another name",
                  f"Por favor, añade este documento al corpus: {COPY}", "yes", records)
    finally:
        COPY.unlink(missing_ok=True)

    end = index_state()
    print("\n" + "=" * 78 + "\nWHAT HAPPENED\n" + "=" * 78)
    results = [
        check(s1["refused"] and not s1["error"], "1. before: the agent refused (documents do not cover 2025)"),
        check(bool(add_calls(s2)) and all(c["status"] == "not_approved" for c in add_calls(s2))
              and s2["index_after"] == s2["index_before"],
              "2. no: add_document was requested, not approved, and the index did not change"),
        check(any(a["approved"] for a in s3["approval_requests"]) and SOURCE_ID in s3["index_after"]["documents"],
              f"3. yes: you approved and the document is now indexed "
              f"(+{s3['index_after']['chunks'] - s3['index_before']['chunks']} chunks)"),
        check(not s4["refused"] and "39,47" in s4["answer"] and any(SOURCE_ID in s["id"] for s in s4["sources"]),
              "4. after: the agent answers 39,47 euros/day and cites the new document"),
        check(any("Skipped" in c["result"] for c in add_calls(s5)) and s5["index_after"] == s5["index_before"],
              "5. twice: skipped, already indexed, index unchanged"),
        check(any("Skipped" in c["result"] for c in add_calls(s6)) and s6["index_after"] == s6["index_before"],
              "6. renamed copy: skipped (same content), index unchanged"),
    ]
    print(f"\nIndex: {start['chunks']} -> {end['chunks']} chunks, {start['index_mb']} -> {end['index_mb']} MB")

    OUT_JSON.write_text(json.dumps({"question": QUESTION, "document": DOC.name, "index_start": start,
                                    "index_end": end, "steps": records}, ensure_ascii=False, indent=1),
                        encoding="utf-8")
    lines = ["# Add-document demo", "",
             f"Question: *{QUESTION}* Document added: `{DOC.name}` (Real Decreto 87/2025, BOE-A-2025-2576).",
             f"Index: {start['chunks']} -> {end['chunks']} chunks.", ""]
    for r in records:
        lines += [f"## Step {r['step']}: {r['label']}", "", f"**Prompt:** {r['prompt']}", ""]
        for a in r["approval_requests"]:
            lines.append(f"**Approval asked for `{a['tool']}`:** {'yes' if a['approved'] else 'no'}")
        for c in r["tool_calls"]:
            lines.append(f"- tool call `{c['tool']}` {json.dumps(c['args'], ensure_ascii=False)} -> {c['status']}: "
                         f"{c['result'][:160].replace(chr(10), ' ')}")
        lines += ["", "**Answer:**", "", r["answer"] or f"(error: {r['error']})", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nsaved: {OUT_MD.relative_to(ROOT)}, {OUT_JSON.relative_to(ROOT)}")
    if not all(results):
        print("Some checks say CHECK: send me the output; the model may simply have answered differently.")
    print("\nNOW PUT index/ BACK so the committed index is the one the evaluation used:\n"
          "  git checkout -- index/ && rm -f index/documents.json\n"
          "  git status --short index/        (should print nothing)")


if __name__ == "__main__":
    main()
