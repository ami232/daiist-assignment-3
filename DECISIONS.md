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
