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
- **First sign of the "wrong year" risk:** for the question "What was the EV sales share in Europe in 2024?", the fixed design ranks a chunk from the 2026 report first instead of the 2025 one.
