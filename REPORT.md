# Assignment 3 Report

- **Name**: Celia Sanmartin
- **Student ID**: 18798
- **Group**: BBADBA 5B

## Use case

A hospital pharmacist or junior doctor who needs to check, with a citation, what the official EU product information (SmPC) says about an oral anticoagulant: dose, contraindications, interactions, switching from warfarin, pregnancy. They use the answer to decide what to confirm before advising or prescribing. A wrong answer (a wrong dose, a missed contraindication) can cause bleeding or clotting, so "I don't know, read the label" costs far less than a confident wrong answer. That is why the assistant must cite every claim and refuse when the corpus does not cover the question.

## Corpus

Official EMA "Product information" PDFs (Annex I = SmPC, the SmPC pages only), downloaded in November 2026. EMA allows reuse of its web content if the source is acknowledged (EMA legal notice).

| Document | URL | Words (SmPC pages) | Note |
|---|---|---|---|
| Eliquis (apixaban) | https://www.ema.europa.eu/en/medicines/human/EPAR/eliquis | 48,762 | 4 SmPC variants in the file |
| Pradaxa (dabigatran) | https://www.ema.europa.eu/en/medicines/human/EPAR/pradaxa | 44,782 | 3 SmPC variants |
| Xarelto (rivaroxaban) | https://www.ema.europa.eu/en/medicines/human/EPAR/xarelto | 72,701 | several variants |
| Lixiana (edoxaban) | https://www.ema.europa.eu/en/medicines/human/EPAR/lixiana | 12,587 | added later with `add_document` |

The three base documents have 166,245 words. Caveat: each EMA file bundles one SmPC per presentation, and the variants repeat most of their text, so the unique text is much smaller than the word count.

## Ingestion

I read each PDF with pypdf, keep only the SmPC pages (the PDF outline entry containing "MANUFACTURER" marks the end of Annex I), and cut the file into its SmPC variants at the heading "1. NAME OF THE MEDICINAL PRODUCT". Cleaning fixes three extraction problems: the page number glued to the start of each page, hard line breaks in the middle of sentences, and words split with a hyphen at the line end ("non-" + "fatal"). One example of the problem I fixed: before cleaning, the page number ended up inside the text of the first sentence of the page, and sentences were cut into short lines, which broke the chunks.

Each chunk stores id, text, source (file name) and location (`SmPC 1 of 4, pp. 36-37`, plus the section in design B). Embeddings come from `gemini-embedding-2` (3072 dimensions) and are stored in ChromaDB (`index/`, one collection per design, cosine distance). Design A has 476 chunks, design B 137 chunks (181 after adding Lixiana). Known limits: tables are flattened by the extraction, and about 10 chunks of design A straddle two variants.

## Test set

32 questions in `eval/questions.csv`, written by Claude from the text of the PDFs: 18 single, 7 multi and 7 unanswerable. Each row has the expected source, the expected location and a reference answer. There are no Xarelto questions, because the Xarelto text was not given to Claude when the questions were written. I did not check every reference answer page by page against the PDFs. Indirect check: I graded the agent's 32 answers against the reference answers by hand, and the agent's answers, built only from the retrieved passages, matched the references on all the answerable questions I marked correct, so a wrong reference would have shown up as a disagreement.

Two examples:

- **q02 (single):** "In non-valvular atrial fibrillation, in which patients should the apixaban dose be reduced to 2.5 mg twice daily?" Reference: at least two of age ≥ 80, weight ≤ 60 kg, serum creatinine ≥ 1.5 mg/dL.
- **q26 (unanswerable):** "What is the recommended dose of edoxaban for stroke prevention in non-valvular atrial fibrillation?" Reference: the corpus does not cover edoxaban, so the assistant must say it does not know.

## Retrieval

Two designs: **A**, fixed windows of 400 words with 50 overlap, over all variants; **B**, one chunk per SmPC section (4.1, 4.2, …, long sections cut at 400 words), SmPC variant 1 only. A retrieved chunk is a hit if it has the right source, belongs to SmPC 1 and overlaps the expected page; a multi question needs every part found. Measured on the 25 answerable questions:

| Design | hit@1 | hit@3 | hit@5 | Chunks | Avg words/chunk | Words added to the prompt (5 chunks) |
|---|---|---|---|---|---|---|
| A: fixed400 | 0.28 | 0.40 | 0.44 | 476 | 399 | about 1,995 |
| B: section | 0.52 | 0.68 | 0.80 | 137 (181 with Lixiana) | 308 | about 1,540 |

I chose **B (section)**: it is better at every k and adds about 23% fewer words to the prompt. Caveat: the strict hit rule counts the repeated text of variants 2-4 as a miss for design A, so part of the gap comes from removing duplicates, not only from cutting by section.

## Tools and subagent

`server.py` is an MCP server (stdio) with two tools.

- **search(query)**: "Search the corpus: the SmPC of apixaban (Eliquis), rivaroxaban (Xarelto), dabigatran (Pradaxa) and any added document. Returns the 5 closest passages, each with its source document, its location (SmPC variant and pages) and its distance, so the answer can be cited. If none of the passages answers the question, say you do not know; never answer from memory."
- **add_document(path)**: adds a PDF to the index. It checks that the file exists and is a PDF, and if the document is already indexed it does nothing and says so.

One search result (from `check.py`, with design A, before I switched to B):

> [1] eliquis-epar-product-information_en | SmPC 1 of 4, p. 3 | distance 0.219
> at least two of the following characteristics: age ≥ 80 years, body weight ≤ 60 kg, or serum creatinine ≥ 1.5 mg/dL (133 micromole/L). Therapy should be continued long-term. …

Subagent `.claude/agents/corpus-researcher.md`, with only the search tool (`tools: mcp__corpus__search`). Instructions: always search before answering, run a second search with other wording if needed, answer only from the passages and cite `[source | location]`, say "I don't know" if the corpus does not cover it, 1-4 sentences plus citations.

Transcript, from Claude Code in the VS Code terminal. The subagent is `corpus-researcher` (`.claude/agents/corpus-researcher.md`) and its only tool is the corpus MCP `search`. Each search asked me for approval; I approved. Parts I left out are marked with [...].

```
> Use the corpus-researcher subagent to answer: What does the Eliquis SmPC say about taking
  apixaban together with strong CYP3A4 and P-gp inhibitors?

● corpus-researcher(Eliquis CYP3A4/P-gp interactions)
  Backgrounded agent

Tool use · from the corpus-researcher agent
corpus — Search Tool: (MCP)
query: apixaban strong inhibitors of both CYP3A4 and P-gp azole antimycotics HIV protease inhibitors not recommended
Do you want to proceed?  1. Yes

[...]
query: diltiazem naproxen clarithromycin moderate inhibitors apixaban no dose adjustment
[...]

● Agent "Eliquis CYP3A4/P-gp interactions" finished · 1m 31s

The Eliquis SmPC says apixaban is not recommended with strong inhibitors of both CYP3A4 and
P-gp. It does not go as far as a contraindication. Taking them together roughly doubles
apixaban levels. The subagent ran five corpus searches and quoted the SmPC directly; every
point below comes from the Eliquis SmPC in the corpus.

[...]

## Drugs that are not strong inhibitors of both pathways (section 4.5, pp. 11-12)
> "Active substances which are not considered strong inhibitors of both CYP3A4 and P-gp, (e.g.,
  amiodarone, clarithromycin, diltiazem, fluconazole, naproxen, quinidine, verapamil) are
  expected to increase apixaban plasma concentration to a lesser extent. No dose adjustment for
  apixaban is required when coadministered with agents that are not strong inhibitors of both
  CYP3A4 and P-gp."

| Drug | How it inhibits (SmPC wording) | AUC | Cmax |
| Diltiazem 360 mg once daily       | Moderate CYP3A4, weak P-gp | x1.4 | x1.3 |
| Naproxen 500 mg single dose       | P-gp only, not CYP3A4      | x1.5 | x1.6 |
| Clarithromycin 500 mg twice daily | P-gp + strong CYP3A4       | x1.6 | x1.3 |

## Why these drugs matter (section 5.2, pp. 32-33)
> "Apixaban is metabolised mainly via CYP3A4/5 with minor contributions from CYP1A2, 2C8, 2C9,
  2C19, and 2J2 ... Apixaban is a substrate of transport proteins, P-gp and breast cancer
  resistance protein (BCRP)."
```

This agrees with the answer of the main agent for q06 (apixaban is not recommended with strong inhibitors of both CYP3A4 and P-gp, about a 2-fold increase in exposure).

## Adding a document

Asking for a document that is already indexed does nothing: `add_document` answers "Already indexed: lixiana. Nothing was added."

The unanswerable question is q26 (and q27) about **edoxaban**, which the three base documents do not cover. I added the **Lixiana SmPC** (67 pages, 12,587 words, 44 chunks).

| Question | Before | After |
|---|---|---|
| q26: dose of edoxaban in NVAF | "I don't know. The provided product information covers apixaban (Eliquis) and dabigatran (Pradaxa), but does not contain information regarding the recommended dose of edoxaban." | "60 mg once daily" with a reduced dose of 30 mg (moderate or severe renal impairment, body weight ≤ 60 kg, some P-gp inhibitors) `[lixiana | SmPC 1 of 1, pp. 3-4]` |
| q27: INR when switching from a VKA | "I don't know." | Start edoxaban when the INR is ≤ 2.5 `[lixiana | SmPC 1 of 1, pp. 4-5]` |

What actually happened: when I asked the agent to add the file, it showed the approval prompt ("The agent wants to run add_document(...). Approve? [y/N]") and I approved, but my "no search, no answer" guardrail replaced the result with "I don't know" and nothing was stored. I fixed the guardrail so that it also lets `add_document` calls through, and then added the document by calling `add_document` directly. I did not repeat the agent flow after the fix.

## Harness and guardrails

`agent.py` is my own LangChain harness (`create_agent` with `gemini-flash-lite-latest`, temperature 0) that starts `server.py` over stdio and uses `AGENTS.md` as the system prompt. The nine rules in `AGENTS.md`, each with its reason: always search first; answer only from the retrieved passages; cite every claim as `[source | location]`; say "I don't know" when the corpus does not cover it (including edoxaban or warfarin before Lixiana, prices, other countries' labels); do not refuse what the passages answer (one retry search); mention the SmPC variant and report disagreements between variants; questions about two medicines need passages for both; call `add_document` only if the user asks and gives a path; answer in the language of the question, in 1-4 sentences followed by citations, without prescribing decisions.

- **Approval:** before `add_document` the terminal asks the human "Approve? [y/N]". Without a terminal (as in the evaluation) the answer is "no".
- **Extra guardrails:** (1) "no search, no answer": if the agent did not call `search` (or `add_document`), the answer is replaced by "I don't know: I could not find supporting passages in the corpus."; (2) a cap of 6 tool calls per question.
- **A case where it fired:** q28, "What is the reimbursed price of Eliquis in Spain?". The agent tried to answer without searching and the guardrail turned it into a refusal.

## Evaluation

`python main.py evaluate` runs the agent on the 32 questions and applies code checks and an LLM judge.

- **Code checks:** the answer cites at least one `[source | location]`; every cited source was retrieved in that run and every cited page is inside the retrieved passages; the agent searched; unanswerable questions must be refused and answerable ones must not.
- **Judge:** `gemini-flash-lite-latest` (temperature 0). It receives the question, its type, the reference answer, the retrieved passages as evidence and the answer, and returns `correct` (matches the reference; for unanswerable questions only a clear refusal is correct) and `supported` (every claim is in the evidence), 1 or 0, with a reason.
- **My own grades:** 32 answers graded by me in `eval/human_labels.csv` before reading the judge.

| Measure | Result |
|---|---|
| Code checks passed | 31/32 |
| Answerable, judge: correct | 25/25 |
| Answerable, judge: supported | 24/25 |
| Correct refusals (unanswerable) | 7/7 |
| Wrong refusals (answerable) | 0 |
| Agreement with the judge, correct | 97% (31/32) |
| Agreement with the judge, supported | 88% (28/32) |

Where we disagree: q06 (I gave `correct` 0 because the answer starts with "Yes" while the conclusion is "not recommended"), and on `supported` q10, q27 and q30 (I gave 0 because the answer adds facts that are not in the reference or the passages) and q22 (I gave 1, the judge 0). The judge is more lenient than I am and it is the same model family as the agent, so I would not trust its perfect score alone.

## Failures

Six of the 32 questions have a problem, even though the judge calls all of them correct:

| Cause | Questions | Count |
|---|---|---|
| Unsupported extra detail (a note on the 75 mg dose, a mention that the corpus includes rivaroxaban) | q10, q27, q30 | 3 |
| Misleading opening ("Yes" to a question whose answer is "not recommended") | q06 | 1 |
| Retrieval incomplete on a multi question (one of the two medicines missing) | q22 | 1 |
| Citation with a page that was not in the retrieved passages | q13 | 1 |
| Wrong answer from the right passage, wrong refusal, answer to an unanswerable question | none | 0 |

What to fix first: (1) tell the agent in `AGENTS.md` to answer yes/no questions with the right polarity first and to add no facts outside the passages; (2) for questions about two medicines, run one search per medicine; (3) build the citation pages from the chunk locations instead of letting the model write them. The first version of my citation check also gave false failures (it read section numbers as pages); I fixed it and it went from 27/32 to 31/32.

## Decision

I would let users rely on it only as a **lookup aid with citations** for pharmacists and doctors, never as the source of a prescribing decision. Safeguards: the user opens the cited page of the SmPC before acting, new documents need human approval, and the assistant refuses what the corpus does not cover. The remaining errors above are small, but this is a medical use case, so the error rate is still too high for unsupervised use. Cost and latency per question: about 12,764 tokens (agent plus judge), about 0.0013 USD with an assumed price of 0.10 / 0.40 USD per million input / output tokens (to be checked), and a median of 9.2 s per answer.

## AI use

I used Claude (Anthropic) in the Claude app as an assistant through the whole assignment. Claude wrote the use-case text, the 32 test questions and reference answers, `AGENTS.md`, the code (`index.py`, `retrieve.py`, `server.py`, `agent.py`, `evaluate.py`) and this report from my results, and guided me step by step on the setup and the debugging. I ran every command, checked the outputs, graded the 32 answers by hand in `human_labels.csv`, and ran the add-a-document test. I asked for this help because I understood from the professor that AI could write these parts as long as I learn and can explain them. Inside the system I use Gemini models: `gemini-embedding-2` for embeddings and `gemini-flash-lite-latest` for the agent and the judge.