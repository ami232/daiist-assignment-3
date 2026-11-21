# Decision log (draft for REPORT.md)

Decisions made by Máximo during development, with the alternatives and the evidence considered. It is the basis for writing REPORT.md in his own words.

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

## 4. Figure notes and footnotes

- **Decision:** drop them.
- **Reason:** they add ~5,500 words (~10% more embeddings), and almost all of them are sources, abbreviations or descriptions of charts the system cannot see. Some definitions are lost (e.g. "battery pack price").

## 5. Chunking designs to compare

- **Decision:** A = fixed windows of 150 words with a 30-word overlap (469 chunks) versus B = one chunk per report section, max. 250 words, with a "report · chapter · heading" header (322 chunks).
- **Reason:** it compares two different chunking philosophies (fixed size versus document structure) and fits in one day of free-tier quota (~790 embeddings).
- **Rejected:** fixed 100 versus fixed 250 (~980 embeddings, compares size only) and fixed versus hybrid search (does not compare chunkings; hybrid search can be added later as a third design at no embedding cost).
- The final design will be chosen from hit rate @1/3/5.

## 6. Embeddings and storage (technical choices proposed by Claude, to review)

- `gemini-embedding-2` model with 768-dimensional vectors instead of 3,072, so `index/` stays small (7.5 MB in total). Task type `RETRIEVAL_DOCUMENT` for chunks and `RETRIEVAL_QUERY` for questions.
- Storage "similar to ChromaDB": JSONL files in `index/` (chunks per design plus one shared vector cache) and cosine-similarity search with numpy. It is transparent, fits in git and does not depend on Chroma versions.
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
| A · fixed 150 (overlap 30) | 58% | 73% | 85% | 750 |
| B · structured (sections ≤250 + header) | 77% | 88% | 100% | 988 |

- `single`: fixed 75% / 95% / 100%; structured 100% / 100% / 100%.
- `multi` (strict): fixed 0% / 0% / 33%; structured 0% / 50% / 100%. Strict hit@1 is 0% by construction for both designs, because one chunk rarely covers two passages; partial@1 (fixed 50%, structured 33%) shows that one passage is usually found first.
- **Why fixed fails:** all four of its misses at k=5 (q21-q24) are multi questions where the GEVO 2025 passage is never retrieved; the GEVO 2026 chunk with the same topic always wins. This is the **"wrong edition"** problem, also visible in single questions (q13, a 2024 UK figure: top-1 is a 2026 chunk). Fixed chunks carry no title or year in their text, and they cut sections in the middle.
- **Why structured works:** each chunk starts with "report title · chapter · heading", so the edition year and topic are part of the embedded text. IEA headings often state the key figure (e.g. "Close to 55% of new cars sold in China were electric in 2025"), and whole sections keep the answer together.
- **Decision (Máximo): structured design, k = 5.** It wins at every k, and k=5 is the smallest k that finds both passages of every multi question, at ~990 words (~1,300 tokens) per search, about 30% more than fixed. k=3 would drop to 50% on multi questions.
- **Caveat:** 26 questions is a small sample (one question ≈ 4 points), and the questions were written from body text, which helps any design. The "wrong edition" pattern is the robust finding.
