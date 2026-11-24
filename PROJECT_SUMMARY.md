# Project summary: Spanish rental-law assistant (Assignment 3)

A study guide to the project: what each part does, why it was chosen, and the final numbers. `REPORT.md` is the submitted report; this file explains the same work more simply. All figures are for the final run on the BOE text downloaded on 23 November 2026.

## 1. The goal

An assistant that answers questions about **renting a home in Spain** using only the official law, cites the exact article, and says "the corpus does not cover this" when the law it has doesn't answer. Then measure how often it is right, how often it invents something, and how often it correctly refuses.

- **Users:** tenants and small landlords with a concrete problem (deposit, leaving early, ignored repair, rent rise).
- **Why refusing beats guessing:** a wrong answer can cost a tenant money or their home; "I don't know" only sends them to a lawyer or the housing office.

## 2. Corpus

Official consolidated BOE texts, downloaded as XML from the BOE open-data API. The four files are committed in `corpus/` as a dated snapshot (BOE texts may be reused freely, citing the source), so `main.py index` always rebuilds the evaluated index.

| Document | Words | Role |
|---|---|---|
| LAU (Ley 29/1994) | ~23,600 | The base rental law: duration, deposit, repairs, leaving early |
| Ley 12/2023 de vivienda | ~31,600 | Stressed zones, large landlords, rent limits |
| RDL 7/2019 | ~9,800 | The 2019 reform |
| **Initial corpus** | **~65,000** | (requirement: 3+ documents, 50,000+ words) |
| LPH (Ley 49/1960) | ~11,900 | Owners' associations: kept out on purpose, added with `add_document` for the before/after demo |

**The law changed during the project.** The first download (12 Nov) contained a change to LAU art. 10 due on 15 Nov 2026 (RDL 28/2026). Congress repealed that decree on 12 Nov, before it took effect. On 23 Nov the laws were downloaded again, the index rebuilt (5 chunks removed), q20 replaced and the evaluation re-run.

**Limitation:** RDL 7/2019 is an amending law, so it carries old (2019) wording of rules that were changed again later (for example the tourist-flat rule of the LPH, changed by LO 1/2025).

## 3. Ingestion (`index.py`)

1. **Download** the XML for each law into `corpus/` (skipped if the file is already there).
2. **Clean:** keep only the latest version of each article (the XML holds every past version), drop editorial notes, keep TÍTULO/CAPÍTULO as the heading path.
3. **Future text:** text not yet in force ("Téngase en cuenta que, con efectos de…") is split into its own chunk labelled `[redacción futura, en vigor desde el …]`. The current corpus has none, because the only case was repealed.
4. **Chunk:** one chunk per article; articles over 400 words split on paragraph boundaries. **267 chunks** (LAU 112, Ley 12/2023 118, RDL 7/2019 37), plus 54 for the LPH.
5. **Metadata on every chunk:** law, article, heading, part, BOE link, word count, content hash.
6. **Embed** with `gemini-embedding-2` (768 dimensions) into ChromaDB in `index/`. A chunk is embedded only if it isn't stored yet with the same hash, and query embeddings are cached, so re-runs cost no quota.

**Known issue:** the *Disposiciones* at the end of each law carry the last TÍTULO of the law as their heading. Their `location` (which is what citations use) is correct.

## 4. Test set (`eval/questions.csv`)

35 questions: **22 single** (one article), **7 multi** (two articles), **6 unanswerable** (on topic, not in the three laws). First drafted with AI help from the article texts, then reviewed. Two were replaced:
- **q34**, "can the building ban tourist flats?", was marked unanswerable but RDL 7/2019 answers it. It became "can an owner who owes community fees vote?" (checked: none of the three laws covers it; the LPH does).
- **q20** asked about the repealed art. 10 change. It became "the five years of my contract are over and nobody said anything: what happens now?" (current art. 10).

## 5. Retrieval comparison

"Hit at k" = the expected article is among the first k results.

| Design | hit@1 | hit@3 | hit@5 | two-article questions with both articles @5 |
|---|---|---|---|---|
| **One chunk per article** (chosen) | 0.759 | **0.966** | **1.000** | **5/7** |
| 200-word pieces, 50 overlap | 0.690 | 0.828 | 0.897 | 4/7 |

One chunk per article wins on every measure, and matches how lawyers cite. The cost is about 350 more words per question.

## 6. Tools and agents

- **`server.py`** (MCP): `search(query)` returns the 5 best chunks with law, article and BOE link; `add_document(path)` runs a file through the same pipeline. If the file is already indexed and unchanged, it embeds nothing and says so.
- **Subagent** (`.claude/agents/corpus-researcher.md`): can only search. One real transcript is in the report.
- **Agent** (`agent.py`): LangChain on `gemini-3.5-flash-lite`, with `AGENTS.md` (8 rules) as its system prompt.
- **Guardrails:**
  1. `add_document` needs a human to type "yes" (denied automatically with no terminal).
  2. At most 6 tool calls and 8 model calls per question.
  3. **Citation guard:** every citation must match an article the search returned in that run; one retry, then the answer is replaced by a refusal.
- **The guard in practice:** it never fired on the 35 legal answers or on 5 questions written to provoke it. It did fire once, wrongly, on a reply that needed no citation ("the user did not approve adding the document"): a false positive.

## 7. Before/after demo (q34)

- **Before** (three laws): "El corpus no cubre esta pregunta…"
- **After adding the LPH:** "No, if the debts are due when the meeting starts; yes if the debt was challenged in court or deposited; they can still attend", citing LPH art. 15.
- Adding the LPH again embedded nothing.

## 8. Evaluation (final run)

| | Result |
|---|---|
| Citations valid / expected article retrieved / expected article cited | 35/35 · 29/29 · 29/29 |
| Correct (LLM judge) | 34/35 (q04 wrong) |
| Something made up | 4/35 (q04, q07, q25, q32) |
| Correct refusals / wrong refusals | 6/6 · 0/29 |

**Human vs judge (20 answers graded before seeing the judge):** 95% agreement on "correct" and 80% on "supported". Cohen's κ is 0 for both, because one grader (me) gave the same grade to every answer: when one side never varies, any agreement could be luck. After reviewing the 4 disagreements, I agreed with the judge on all of them.

## 9. Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 0 | — |
| Wrong answer from the right passage | 0 | — |
| Unsupported claim | 4 | q04 and q25 (the same invented compensation clause, from the old version of LAU art. 11), q07 (wrong section number), q32 (extra explanation in a correct refusal) |
| Wrong refusal | 1 | original q20 (refused after one search) |
| Bad test question | 1 | original q34 |

**Lesson:** search works; the agent's writing is the weak point. First fix: grounding, so that nothing appears in an answer unless it is in a retrieved passage.

## 10. Decision

**Not yet: fix first, then release**, and only for finding the right article and a first explanation, never for final decisions. Safeguards: the grounding fix, the BOE link next to every answer, a disclaimer, keeping the corpus updated, a forced second search before refusing, and re-running the 35-question test after every change.

**Cost:** ~6,430 tokens per question, which is $0 on the free tier or ≈ $0.0025 at standard prices. **Speed:** 4–6 s normally (37 s median in the test run because of free-tier waits).

## 11. Likely comprehension-check questions

- What is chunking, and why one chunk per article?
- What is an embedding, and what does hit@3 mean?
- What do the MCP server's two tools do, and what happens if a document is already indexed?
- How does the citation guard work, and what was its false positive?
- What is Cohen's κ, and why is yours 0 even though you agree 95%?
- What happened with q34, q20 and the repeal of RDL 28/2026?

## File map

| File | What it does |
|---|---|
| `index.py` | Download, clean, chunk (2 designs), embed, store, search |
| `server.py` | MCP server: `search`, `add_document` |
| `agent.py` | LangChain agent with three guardrails |
| `evaluate.py` | Retrieval comparison, agent run, code checks, LLM judge, agreement, demo, summary |
| `guardrail_test.py` | Shows the citation guard firing on bad citations |
| `corpus/` | The four BOE texts (23 Nov 2026 snapshot) |
| `index/` | ChromaDB index and query cache |
| `eval/` | Test set, answers, judge verdicts, my grades and review, failures, decision, demo, transcripts |
