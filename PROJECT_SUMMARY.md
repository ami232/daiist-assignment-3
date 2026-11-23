# Project summary — Spanish rental-law assistant (Assignment 3)

A RAG assistant that answers questions about **renting a home in Spain**, citing the exact article of the official law, and saying "the corpus does not cover this" when it can't answer. This file explains every choice made, what was tested, and where each piece lives. Use it to study for the comprehension check and to write `REPORT.md`.

> Results tables at the end are filled from `eval/summary.md` after `main.py evaluate` runs.

---

## 1. Use case

| | |
|---|---|
| **Who asks** | Tenants (students, young workers, families) and small landlords in Spain. |
| **What they do with the answer** | Decide whether to sign a contract, how much deposit to pay, whether a rent rise or agency fee is legal, how much notice to give before leaving, whether they must accept an eviction or a non-renewal. |
| **Cost of a wrong answer** | High and hard to undo: paying illegal fees or deposits, accepting an illegal rent increase, leaving a home they had the right to keep, losing the deposit, or a landlord being fined. |
| **Cost of "I don't know"** | Low: the user checks with a lawyer, the regional housing office or a consumer association. |

**Therefore:** the system must prefer refusing over guessing, and every claim must be checkable through a citation.

---

## 2. Corpus

Official **consolidated texts from the BOE** (Spain's official gazette), downloaded as XML from the BOE open-data API. BOE content may be reused freely, citing the source (BOE legal notice / Real Decreto 1495/2011). Laws contain no personal data.

| Document | BOE id | Words (current text) | Role |
|---|---|---|---|
| Ley 29/1994 de Arrendamientos Urbanos (LAU) | BOE-A-1994-26003 | ~25,900 | Core: duration, rent, deposit, repairs, ending a contract |
| Ley 12/2023 por el derecho a la vivienda | BOE-A-2023-12203 | ~32,500 | Stressed zones, "gran tenedor", information duties, rent caps |
| Real Decreto-ley 7/2019 de medidas urgentes en materia de vivienda y alquiler | BOE-A-2019-3108 | ~10,000 | 2019 reform; reference price index system |
| **Total indexed** | | **~68,400** | (requirement: ≥ 3 docs, ≥ 50,000 words) |
| *Ley 49/1960 de Propiedad Horizontal (LPH)* | *BOE-A-1960-10906* | *~12,000* | *Not indexed at first; added later with `add_document` (before/after demo)* |

**Why this corpus:** the three texts together are the national rules for residential renting. The LAU is the backbone, Ley 12/2023 and RDL 7/2019 explain the reforms, and the Propiedad Horizontal law is a natural "missing" document. It covers neighbours' communities, which tenants ask about but the LAU doesn't regulate.

**Known limitation:** RDL 7/2019 mostly *amends* the LAU, and the consolidated LAU already includes those amendments. Some rules therefore appear twice, and the agent sometimes cites the amending decree instead of the LAU article. The subagent transcript shows this.

---

## 3. Ingestion (`index.py`)

1. **Download** each law's consolidated XML into `corpus/` (git-ignored; re-downloaded by `main.py index`).
2. **Extract and clean:**
   - Each article (`<bloque>`) holds **every historical version**; only the **latest** is kept. Without this, the word count was ~3× higher and old rules would mix with current ones.
   - Editorial notes (`nota_pie`: "Se modifica por…") are dropped.
   - TÍTULO and CAPÍTULO headings are not indexed on their own; they are kept as the article's heading path.
   - Whitespace and non-breaking spaces are normalised.
3. **Extraction problem fixed — future amendments mixed into current text.** BOE puts amendments that are *not yet in force* inside the current article, after a line "Téngase en cuenta que, con efectos de 15 de noviembre de 2026, se modifica…". This happens in **LAU Article 10** (RDL 28/2026). The pipeline splits that text into its own chunk, labelled `Artículo 10. Prórroga del contrato [redacción futura, en vigor desde el 15 de noviembre de 2026]`. The agent's rules say to treat it as not yet applicable.
   - Related: Constitutional Court annulments (STC 79/2024) of parts of Ley 12/2023 Articles 19 and 27 and Disposición final quinta are kept as notices, and the agent is told never to present annulled text as valid law.
4. **Chunk.** Two designs are compared:
   - **`articles`** (chosen): one chunk per article/provision. Articles over 400 words are split on paragraph boundaries into parts. **272 chunks**, ~281 words on average.
   - **`fixed200`**: 200-word windows with a 50-word overlap, ignoring structure. **445 chunks**, ~216 words on average.
5. **Metadata on every chunk:** `source` (law), `location` (article + title), `heading` (TÍTULO / CAPÍTULO), `part`, `doc_id`, `url` (BOE link), `words`, `hash` (detects changed text), `design`. The chunk text also starts with "SOURCE — LOCATION (heading)", which helps both embedding and citation.
6. **Embed** with `gemini-embedding-2` at 768 dimensions (task type RETRIEVAL_DOCUMENT; queries use RETRIEVAL_QUERY), in batches of 50.
   - Each batch is saved to ChromaDB (`index/`, cosine distance) as soon as it comes back.
   - A chunk is only embedded if its id and hash aren't already stored, so re-running `main.py index` costs nothing.
   - Daily-quota errors stop cleanly and keep everything embedded so far.
7. **Query cache:** `index/query_cache.json` stores every query embedding, so repeated questions (evaluation re-runs, `check.py`) cost no quota.

Index size: ~15 MB (limit 90 MB).

**Known cosmetic issue (to fix in a later quota window):** the *Disposiciones* at the end of the LAU inherit the last TÍTULO heading in their chunk header.

---

## 4. Test set (`eval/questions.csv`)

**35 questions:**

| Kind | Count | Examples |
|---|---|---|
| `single` | 22 | "¿Cuántos meses de fianza me pueden exigir…?" → LAU Art. 36 |
| `multi` (needs 2 passages) | 7 | "Si el arrendador es una empresa, ¿cuánto dura como mínimo el contrato y durante cuánto tiempo no se actualiza la fianza?" → LAU Art. 9 + Art. 36 |
| `unanswerable` (near-topic) | 6 | "¿Qué barrios de Barcelona están declarados zona tensionada?" (the law says how zones are declared, not which) |

What the questions cover:
- Mostly Spanish, with 3 in English, to test cross-language retrieval.
- Deposits, guarantees, duration, leaving early, fees, repairs, rent updates, subletting, death of the tenant, improvement works, temporary rentals, verbal contracts, termination causes, *gran tenedor*, stressed zones, information duties.
- One question about the **future Article 10 text**, and one about the **2024 rent-update cap**.

Unanswerable questions:
- IRAV value for October 2026
- the Barcelona zones
- Bono Alquiler Joven
- eviction trial duration
- tourist flats and the neighbours' community (**answered after adding the LPH**: the before/after demo)
- the legal interest rate value

> ⚠️ **This is a draft written with AI assistance from the article texts.** The assignment says the test set must be yours. Read every row, rewrite questions in your own words, check each reference answer against the article, and add or replace questions.

---

## 5. Retrieval comparison

| Design | hit@1 | hit@3 | hit@5 | all expected passages @5 (all 29 answerable; two-article questions: 5/7 vs 3/7) | words added to prompt (top 5) |
|---|---|---|---|---|---|
| **articles** | 0.79 | **1.00** | 1.00 | **0.93** | 1,427 |
| fixed200 | 0.76 | 0.90 | 1.00 | 0.86 | 1,074 |

**Decision: `articles`.**
- It finds the right passage in the top 3 for every answerable question.
- It retrieves both passages of multi-passage questions more often.
- Its chunks match how answers are cited (one article per chunk).
- The cost is ~33% more words per prompt (about 350 extra words, a small token cost).

A "hit" means the retrieved chunk's law and article match the expected source and location.

---

## 6. MCP server (`server.py`)

Registered as `corpus` in `.mcp.json` and `.vscode/mcp.json`. It loads the committed index, never re-embeds the corpus and logs only to stderr.

- **`search(query)`**: top 5 article chunks, each headed `SOURCE | LOCATION | URL | score`, followed by the text. The tool description tells the model what the corpus is, to query in Spanish legal terms, and to cite as `[SOURCE, LOCATION]`.
- **`add_document(path)`**: imports `index.index_file` (the same pipeline, not rewritten) and accepts BOE `.xml`, `.pdf`, `.txt` or `.md`.
  - **Already indexed and unchanged** → nothing embedded; it says so.
  - **Indexed but changed** → new chunks embedded and outdated chunks removed (detected through the content hash).
  - **New** → chunked by article, embedded, stored.

---

## 7. Agents

### Subagent (`.claude/agents/corpus-researcher.md`)
- Tool: `mcp__corpus__search` only.
- Instructions: search in Spanish legal terms, search at least twice before refusing, answer in ≤150 words with `[SOURCE, LOCATION]` citations, flag future text, never present annulled text.
- Transcript from Claude Code: `eval/subagent_transcript.md`.

### Harness (`agent.py`)
- LangChain `create_agent` on **`gemini-3.5-flash-lite`** (override with `AGENT_MODEL`). `gemini-2.5-flash` is no longer available to new keys. `gemini-3.5-flash` was tried first but its free tier allows only 20 requests a day, which ran out after 10 questions (those 10 answers are kept in `eval/answers_gemini-3.5-flash_first10.jsonl`). Flash-lite ignores `temperature=0` (fixed sampling), so re-runs can differ slightly.
- Tools come from `server.py` over MCP stdio, and **`AGENTS.md` is the system prompt**.
- Guardrails:
  1. **Approval before `add_document`.** A human must type "yes". With no terminal (evaluation, `check.py`), it is denied automatically.
  2. **Call limits:** at most 6 tool calls and 8 model calls per question.
  3. **Citation guard (own choice).** Every `[SOURCE, LOCATION]` must match a passage `search` actually returned in this run. If an answer has invalid citations or none, the agent gets one retry. If it still fails, the answer is **replaced by a refusal**. This turns "unsupported claim" failures into "I don't know", which is the cheaper error for this use case.
- `answer(question)` returns the answer, tool trace, retrieved passages and full evidence text, tokens, seconds and guard outcome.

### `AGENTS.md` rules (each with its reason)
1. Search first and answer only from the results.
2. Cite every claim.
3. Say plainly when the corpus does not cover the question.
4. Search at least twice before refusing.
5. Separate the law in force today from future or annulled text.
6. Answer in the user's language, direct answer first, then the exceptions.
7. Not a lawyer: suggest confirming concrete disputes.
8. Only add documents the user explicitly asks for.

---

## 8. Evaluation (`evaluate.py`)

Each stage saves its results and resumes where it stopped:

1. **Retrieval** hit@1/3/5 per design → `eval/retrieval.csv`
2. **Agent** answers for all 35 questions → `eval/answers.jsonl`
3. **Code checks:**
   - valid citations
   - correct refusals (unanswerable questions)
   - wrong refusals (answerable questions)
   - answered an unanswerable question
   - expected passage retrieved
   - expected passage cited
4. **LLM judge** (`gemini-3-flash-preview`, falling back to `gemini-3.8-flash`; never the agent's model). The rubric gives two binary scores and gets the retrieved text as evidence:
   - *correct*: agrees with the reference with no contradicting claim, or a proper refusal for unanswerable questions;
   - *supported*: every legal claim appears in the evidence.

   → `eval/judge.jsonl`
5. **Agreement with your grades:** % agreement and Cohen's κ, using `eval/human_labels.csv`.
6. **Before/after:** add the LPH and re-ask q34 (owner in debt voting at the junta) → `eval/add_document_demo.md`. Run once with `uv run python evaluate.py --demo`.
7. **Summary** with suggested failure causes, tokens and seconds per question → `eval/summary.md`, `eval/results.csv`

Failure categories: retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question. The code *suggests* one per failure; the final classification must be done by hand.

---

## 9. Results

Full numbers: `eval/summary.md`. Run of 12 Nov 2026, agent `gemini-3.5-flash-lite`, 35 questions.

**Retrieval** (articles design is served): hit@1 0.79 · hit@3 1.00 · hit@5 1.00 · all passages of multi questions in top 5: 0.93.

**End to end (code checks, no LLM needed)**

| metric | result |
|---|---|
| citations valid (every citation matches a retrieved passage) | 35/35 |
| expected passage retrieved by the agent | 29/29 |
| expected passage cited | 28/29 |
| correct refusals on unanswerable questions | 6/6 |
| wrong refusals on answerable questions | 1/29 (q20) |
| citation guard retried / blocked | 0 / 0 |
| searches per question (mean) | 1.3 |
| tokens per question (mean) | 6,272 (≈5,990 input + 280 output) |
| seconds per question | mean 46.9, median 38.6 (includes free-tier retries) |

**Cost per question:** $0 on the free tier. On a paid tier it would be about 5,990 × input price + 280 × output price per question, plus one cached query embedding. Input dominates because AGENTS.md and 5 article-sized passages go into every call.

**LLM judge:** only 4 of 35 answers could be judged (all 4 correct and supported) before both judge models hit their free daily quota. The judge stage resumes where it stopped, so run `uv run python evaluate.py` again on another day to finish it, then compute agreement once you have graded.

**The two flagged failures (check them yourself):**
- **q20 (future prórroga rules from 15 Nov 2026): wrong refusal.** The agent searched once, retrieved the future-text chunk of LAU art. 10 and still said the corpus "does not cover it in detail". It broke AGENTS.md rule 4 (search twice before refusing) and rule 5 (use future text, with its date). Likely category: *wrong answer from the right passage* (the model, not retrieval).
- **q34, old version (can the building ban tourist flats?): bad test question, now replaced.** It was labelled unanswerable, but RDL 7/2019 *Artículo segundo* carries the new text of LPH art. 17.12, so the agent answered it correctly. RDL 7/2019 also rewrites LPH arts. 9.1.f (reserve fund) and 10.1.b (accessibility works), so questions on those topics are answerable too. It was replaced (18 Nov) by *¿Puede votar en la junta de propietarios un propietario que debe cuotas de comunidad?* (LPH art. 15.2). This was checked against the 3 original laws with 2 queries each and nothing relevant came back. The agent now refuses it correctly: correct refusals 6/6.

**Add-document demo (`eval/add_document_demo.md`):** question q34, *¿Puede votar en la junta un propietario que debe cuotas de comunidad?*. **Before** (3 laws): the agent searched twice and said *"El corpus no cubre esta pregunta"*, explaining that the topic is in the LPH, which is not indexed. **Added** the LPH (54 chunks). Adding it again embedded 0 chunks (idempotent). **After:** *"No, si las deudas están vencidas al iniciarse la junta"*, with the exception (debt challenged in court or the amount deposited) and the right to attend and speak, all cited to [LPH (Ley 49/1960), Artículo quince]. The demo removes the LPH first, so it can be re-run with `uv run python evaluate.py --demo --no-judge`.

**Subagent:** `eval/subagent_transcript.md`. It answered the rent-update question correctly with LAU art. 18, DA undécima and RDL 7/2019.

**`check.py`:** all 4 checks pass (key, index + test set, server search, `main.py ask`). The only warning is that `eval/human_labels.csv` has no grades yet.

---

## 10. What is still yours to do

The assignment says these must be your own work. They also come up in the in-class comprehension check.

1. **Use case paragraph** in REPORT.md, in your words (Section 1 above is a starting point).
2. **Review and own the test set** (`eval/questions.csv`).
3. **Grade 20+ answers yourself** in `eval/human_labels.csv`, *before* reading `eval/judge.jsonl`. Use `eval/to_grade.md`, which shows answers without the judge's verdicts.
4. **Final failure classification** and the **ship decision** (would you let tenants rely on it, for what, with which safeguard).
5. **Write REPORT.md**, including the AI-use disclosure (code written with Claude Code; decisions listed above were proposed by the assistant on request and must be reviewed and justified by you).
6. Optional: run **Verify Assignment 3** on GitHub Actions with the `GEMINI_API_KEY` secret.

## File map

| File | What it does |
|---|---|
| `index.py` | Download, clean, chunk (2 designs), embed, store, search helpers |
| `server.py` | MCP server: `search`, `add_document` |
| `agent.py` | LangChain harness with three guardrails |
| `evaluate.py` | Retrieval comparison, agent run, code checks, judge, agreement, demo, summary |
| `AGENTS.md` | System prompt and rules |
| `.claude/agents/corpus-researcher.md` | Subagent definition |
| `eval/` | Questions, answers, verdicts, summaries, transcripts |
| `index/` | ChromaDB with saved vectors (committed) |
