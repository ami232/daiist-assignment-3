# Decision log (draft for REPORT.md)

Decisions made by Máximo during development, with the alternatives and the evidence considered. How decisions were made: at each decision point Claude (the AI assistant that wrote the code) explained the possible options, with evidence and a recommendation, and Máximo chose which one to take. It is the basis for writing REPORT.md in his own words.

## 1. Use case (2026-11-21)

- **Chosen:** a consultant at a professional-services firm who prepares electric-vehicle market reports for clients in the automotive sector.
- **Cost of an error:** a wrong figure in a client report feeds investment decisions (sizing a battery plant, launching a model) and damages the firm's credibility. "I don't know" costs about 10 minutes of checking the source.
- **Alternatives rejected:** the English football regulator (licence not confirmed, legal language), the F1 regulations (FIA copyright), NIST cybersecurity guidance, NHTSA recall reports.

## 2. Corpus (2026-11-21)

- IEA reports under CC BY 4.0, downloaded from the IEA's official blob storage (iea.org blocks scripted downloads with a Cloudflare bot check).
- Global EV Outlook 2026 (executive summary, ch. 1, 2, 5 and 9), Global EV Outlook 2025 (executive summary, ch. 1-2) and Global Critical Minerals Outlook 2026 (executive summary and the lithium, nickel, cobalt and graphite outlooks).
- About 73k words in the selected pages and about 56k words of body text after cleaning.
- "Electric Car Markets in a Time of Uncertainty" (July 2026) is held out for the add_document demo.

## 3. Extraction: problem found and fix

- With `pypdf`, words were split ("sale s", "r ecently") and chart labels were mixed into the text. Switched to **PyMuPDF**, which gives the font size of every line: body text is ~11 pt, headings ≥14 pt, and noise (running headers, chart axes, notes) ≤9 pt. Only body text and headings are kept.
- Other fixes: reading order on the two-column pages of the minerals report, "CO₂" coming out as "CO", and paragraphs cut by a page or column break, which are now joined.
- Found later, while testing the MCP server (2026-11-22): the PDF of GEVO 2026 repeats the last two lines of p. 18 at the top of p. 19, so one chunk contained a sentence twice. When a paragraph continues on the next page and the new page starts with the same 8+ words, the repetition is now removed. It changed 1 structured chunk; in the fixed design the windows after that point shifted (71 chunks re-embedded).

## 4. Figure notes and footnotes

- **Decision:** drop them.
- **Reason:** they add ~5,500 words (~10% more embeddings), and almost all of them are sources, abbreviations or descriptions of charts the system cannot see. Some definitions are lost (e.g. "battery pack price").

## 5. Chunking designs to compare

- **Decision:** A = fixed windows of 150 words with a 30-word overlap (469 chunks) versus B = one chunk per report section, max. 250 words, with a "report · chapter · heading" header (322 chunks).
- **Reason:** it compares two different chunking philosophies (fixed size versus document structure) and fits in one day of free-tier quota (~790 embeddings).
- **Rejected:** fixed 100 versus fixed 250 (~980 embeddings, compares size only) and fixed versus hybrid search (does not compare chunkings; hybrid search can be added later as a third design at no embedding cost).
- The final design will be chosen from hit rate @1/3/5.

## 6. Embeddings and storage (2026-11-22)

- **Vector size (decision):** `gemini-embedding-2` with **768** dimensions. Alternatives: 1,536 (~15 MB) and 3,072 (~30 MB, maximum quality). Reason: the model is trained so that shorter vectors lose very little quality, the structured design already reaches 100% hit@5 (so a gain could not even be measured), `index/` stays at 8.4 MB, and changing would cost a full re-embedding (~900 texts, about one day of free quota).
- **Task type (decision):** `RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for questions, Google's recommended setup for search, so a short question lands close to the long passage that answers it. Rejected: one generic vector for both (usually slightly worse for question → passage search, and it would need re-embedding).
- **Storage (decision):** JSONL files in `index/` (chunks per design plus one shared vector cache) and cosine-similarity search with numpy, the "similar to ChromaDB" option allowed by the brief. Reason: every chunk can be opened and read with its page, the search is ~20 lines that can be explained, and there is no extra dependency; at ~320 chunks a full scan takes milliseconds. Rejected: ChromaDB (a binary folder that cannot be read in git; its speed only matters at thousands or millions of chunks).
- Each vector is saved as soon as it arrives, keyed by a hash of (model, dimensions, task, text). Re-running `main.py index` spends no embeddings, and question vectors are cached too.
- **Problem found:** with `gemini-embedding-2`, a list of texts is embedded as **one** input and returns a single vector. It was spotted because only 10 vectors had been saved for 469 chunks. Fixed by sending each text as its own `Content` and checking that the number of vectors matches.
- **First sign of the "wrong year" risk (seen before the test set existed):** for the question "What was the EV sales share in Europe in 2024?", the fixed design ranks a chunk from the 2026 report first instead of the 2025 one.

## 7. Test set (`eval/questions.csv`)

- **Written by Máximo** from the PDFs, in English, before any retrieval tuning. Claude only checked it (format, counts, that each answer is in the indexed text on the stated page, and that unanswerable questions are not answered by the corpus) and suggested where coverage was thin. The questions themselves were not changed by Claude.
- **Counts:** 32 questions = 20 `single`, 6 `multi`, 6 `unanswerable`. By document (answerable passages): GEVO2026 most, then GEVO2025 and GCMO2026.
- **Location convention:** `expected_source` = document code (`GEVO2026`, `GEVO2025`, `GCMO2026`); `expected_location` = printed page number. For `multi`, both lists are `;`-separated in the same order.
- **Design choices:**
  - Answers are taken from body text, not charts (charts are not indexed), and every question states the year it refers to, because two editions of the same report are in the corpus.
  - `multi` questions compare the two editions (2024 vs 2025 figures) or cross documents (EV battery deployment + lithium demand; lithium price spike + sodium-ion batteries).
  - After a first review, two questions on the outlook chapter (ch. 9, the largest chapter and the most relevant one for a consultant) replaced two regional market questions.
  - **Unanswerable questions are near-misses:** the corpus contains related figures that could tempt the system into an unsupported answer (Spain's +80% sales growth vs Spain's sales *share*; the 2025 battery price decline vs the full-year 2026 change; other countries' 2040 targets vs a Spain 2040 projection). Two very specific questions first drafted (nickel content of a Tesla Model 3, maintenance cost of a VW ID.3) were replaced because they would be too easy to refuse.
  - `q32` (Q2 2026 global EV sales vs Q2 2025) is unanswerable with the initial corpus but answered by the held-out July 2026 report ("4% higher year-on-year"): it is the question for the add_document before/after demo.
  - `q01` is an easy, clearly answerable `single` question because `check.py` uses it to test the search tool and `main.py ask`.
- **Two examples:** q09 (`single`): "How much battery capacity was deployed in electric vehicles worldwide in 2025 and how much did deployment grow from 2024?" → GEVO2026 p. 92, "1.2 TWh, almost +30%". q23 (`multi`): "How did the electric share of new car sales in Europe change between 2024 and 2025?" → GEVO2025 p. 17 + GEVO2026 p. 21, "about 20% → 28%".

## 8. Retrieval metric

- **Hit definition (decision):** a retrieved chunk is a hit for an expected passage when it comes from the expected document **and** its page range includes the expected page (exact page, no ±1 tolerance, so errors are not hidden).
- **Multi-passage questions (decision):** strict — a `multi` question counts as a hit at k only if **both** expected passages are in the top k, because the agent cannot answer correctly with only one. The partial score (share of expected passages found) is reported as a secondary figure to explain failures.
- Unanswerable questions have no expected passage and are excluded from hit rate (they are evaluated end to end).
- Also reported: words added to the prompt at each k (sum of the words of the top-k chunks), because larger chunks may raise hit rate at a higher token cost.

## 9. Retrieval results and design choice

Results on the 26 answerable questions (`eval/retrieval_summary.md`, per question in `eval/retrieval_results.csv`):

| Design | hit@1 | hit@3 | hit@5 | words@5 |
|---|---|---|---|---|
| A · fixed 150 (overlap 30) | 58% | 69% | 81% | 750 |
| B · structured (sections ≤250 + header) | 77% | 88% | 100% | 984 |

- `single`: fixed 75% / 90% / 95%; structured 100% / 100% / 100%.
- `multi` (strict): fixed 0% / 0% / 33%; structured 0% / 50% / 100%. Strict hit@1 is 0% by construction for both designs, because one chunk rarely covers two passages; partial@1 (fixed 50%, structured 33%) shows that one passage is usually found first.
- **Why fixed fails:** four of its five misses at k=5 (q21-q24) are multi questions where the GEVO 2025 passage is never retrieved; the GEVO 2026 chunk with the same topic always wins. This is the **"wrong edition"** problem, also visible in single questions (q13, a 2024 UK figure: top-1 is a 2026 chunk). Fixed chunks carry no title or year in their text, and they cut sections in the middle. (The fifth miss, q03, appeared after the duplicated-lines fix in section 3 shifted the fixed windows: the table above is the re-run; before the fix fixed scored 58% / 73% / 85%. Structured did not change.)
- **Why structured works:** each chunk starts with "report title · chapter · heading", so the edition year and topic are part of the embedded text. IEA headings often state the key figure (e.g. "Close to 55% of new cars sold in China were electric in 2025"), and whole sections keep the answer together.
- **Decision (Máximo): structured design, k = 5.** It wins at every k, and k=5 is the smallest k that finds both passages of every multi question, at ~990 words (~1,300 tokens) per search, about 30% more than fixed. k=3 would drop to 50% on multi questions.
- **Caveat:** 26 questions is a small sample (one question ≈ 4 points), and the questions were written from body text, which helps any design. The "wrong edition" pattern is the robust finding.

## 10. MCP server and duplicate policy for add_document (2026-11-22)

- **Decision (Máximo): content-based policy.** `index/documents.json` stores a SHA-256 hash of each indexed file and its number of chunks.
  - Same content as a document already indexed → nothing is changed and no embeddings are spent ("Already indexed").
  - Same document (same document id: a known IEA report, or the file name for new documents), different content → the new version **replaces** the old one, so two versions with different figures never mix in search results.
  - Otherwise → added.
- **Reason:** the IEA publishes revised versions of its reports (GEVO 2026 has a "revised version" with corrections), and a consultant always wants the latest one; keeping both would let the agent cite a corrected figure. Rejected: always refuse (cannot update a corrected report) and always add (duplicate chunks, mixed versions).
- **Known limit:** a new document is identified by its file name, so two different reports saved with the same file name would be treated as versions of one document.
- **Accepted formats (decision):** PDF only, so a new report goes through the same font-size cleaning, chapters and headings as the rest of the corpus. Rejected: also .txt/.md (a second, simpler pipeline whose chunks would cite less precisely; not needed for IEA reports).
- **Index a new document goes to (decision):** the structured design only (the one the server searches). Reason: half the embeddings, and the fixed-vs-structured comparison stays on the same 3 documents the test set was written for. Rejected: both designs.
- **On failure (decision):** all or nothing. Chunks are written to the index only after every vector has arrived, so a failure (e.g. the daily quota running out mid-report) leaves the index unchanged and returns an error; vectors already received stay cached, so a retry does not pay for them again. Rejected: saving what arrived (half a report would be searchable, and the agent could wrongly say the document does not contain something that is on a missing page).
- Errors (missing file, wrong format, quota) are returned to the caller as tool errors instead of stopping the server.
- `search` returns the 5 best passages, each with a header "Source: <doc_id>, p. <page> | title (year) | chapter · section | relevance" so the agent can cite (doc_id, p. page) with the same codes as the test set.
- **Tool descriptions (reviewed and approved by Máximo):** Claude explained what each description needs to tell the model; Máximo reviewed them and approved them. `search` states what the corpus covers (reports, chapters, topics), that chart-only figures are not indexed, to use one focused query per fact with the year (two editions cover the same topics), how to cite, and that no matching passage means the corpus does not contain the answer. `add_document` states what it does, PDF only, the duplicate policy, and to call it only when the user asked to add that file.
- **Tested** over MCP stdio as `check.py` does: both tools listed; q01 answered by GEVO2026 pp. 18-19 at rank 1; adding a corpus PDF again → "Already indexed" in 0.0 s; missing file and non-PDF → error. Added / replaced tested on a scratch copy of the index with a one-page test PDF (the July 2026 report is still held out for the demo).

## 11. Subagent `corpus-researcher` (2026-11-22)

`.claude/agents/corpus-researcher.md`, a Claude Code subagent whose only tool is `mcp__corpus__search`.

- **When to delegate (decision):** any factual question on the corpus topics (EV sales, shares, stock, prices, batteries, critical minerals, projections), so Claude Code delegates automatically and the searches do not fill the main conversation. Rejected: only when the user names the subagent (predictable, but it would rarely be used).
- **Refusal rule (decision):** give a figure only if a retrieved passage states it for exactly what was asked (same place, year and metric); simple arithmetic between two cited figures is allowed, showing both; never own knowledge, estimates or a related figure instead (Europe for Spain, 2025 for 2026, sales for share, forecast for actual). Otherwise: "The corpus does not cover this." Reason: in this use case a wrong figure is expensive and a refusal costs ~10 minutes. Rejected: no arithmetic at all (would fail the multi questions that compare 2024 and 2025) and flagged approximations (exactly the near-miss trap the unanswerable questions test). The same rule will go into `AGENTS.md` for `agent.py`.
- **Partly answerable questions (decision):** answer the covered part with its citation and say which part is not covered. Rejected: refuse the whole question (throws away verified information).
- **Search budget (decision):** at most 3 searches per question: one per fact (multi questions need two) plus one reworded search. Each search adds ~1,300 tokens. Rejected: one search (too few for multi questions) and no limit (unpredictable cost).
- Answer format: 1-4 sentences, every figure cited as (doc_id, p. page), the same codes as the test set.
- **First test in Claude Code (q23, both runs in `eval/subagent_transcript.md`):** delegation worked, only `search` was used, 3 searches. The answer (about 20% → 28%) was correct and cited. One error: the European forecast of "around 25%" for 2025 was cited to GEVO2025, p. 26, where that 25% is the **global** share; the European forecast is on p. 10. The figure was right, but the citation pointed to a passage about another scope. This is the same family as the "wrong edition" problem (right topic, wrong scope), so it was fixed in the instructions, not in retrieval. (A second error first reported by Claude, a wrong GEVO2025, p. 10 citation, turned out to be a mistake in Claude's own check: that page does give the European figure.)
- **Scope rule added (decision):** before using or citing a figure, check that its sentence is about the same region as the question (world, Europe, EU, country); a global or EU figure is not a European one. The same rule will go into `AGENTS.md`.
- **Second run with the scope rule:** correct answer, every figure labelled "Europe as a whole" or "EU only" and supported at the cited page, and no scope errors; the global passages it retrieved were not used. One minor miss: it said no 2025 UK share was found, although a retrieved passage gives "over 1 in 3" (GEVO2026, p. 21). This is a side detail, not a wrong figure. Run 2 is the transcript for REPORT.md, with run 1 as the "before".
