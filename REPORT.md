# Assignment 3 Report

- **Name**:
- **Student ID**:
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case

*Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

## Corpus

Three official texts on renting in Barcelona, in Spanish, downloaded from the BOE on 18/11/2026.

| Document | URL | Date (consolidated to) | Licence | Words |
|---|---|---|---|---|
| Ley 29/1994, de Arrendamientos Urbanos (LAU) | https://www.boe.es/buscar/pdf/1994/BOE-A-1994-26003-consolidado.pdf | 13/11/2026 | BOE reuse conditions (Ley 37/2007) | ~29,500 |
| Ley catalana 18/2007, del derecho a la vivienda | https://www.boe.es/buscar/pdf/2008/BOE-A-2008-3657-consolidado.pdf | 25/03/2026 | BOE reuse conditions (Ley 37/2007) | ~55,700 |
| Decreto-ley catalán 3/2023, viviendas de uso turístico | https://www.boe.es/buscar/pdf/2024/BOE-A-2024-281-consolidado.pdf | 08/11/2023 (no modifications since) | BOE reuse conditions (Ley 37/2007) | ~5,400 |

Total: ~90,600 words, 145 pages.

Word counts come from `pdftotext` and include page headers, footers and the index. 
Fuente de los datos: Agencia Estatal Boletín Oficial del Estado (https://www.boe.es).

## Ingestion

**Extract, clean, chunk** (`index.py`):
1. Read each BOE PDF page by page with `pypdf` and apply Unicode normalisation (e.g. the ligature "ﬁ" becomes "fi").
2. Remove the repeated page header and footer ("BOLETÍN OFICIAL DEL ESTADO / LEGISLACIÓN CONSOLIDADA / Página N") and the "no legal value" disclaimer.
3. Skip the cover and table of contents, so the text starts at "TEXTO CONSOLIDADO".
4. Rebuild paragraphs from wrapped lines (in these PDFs a line that continues ends with a space).
5. Follow the legal headings (Título › Capítulo › Sección › Artículo / Disposición, plus the preamble and annex) and make **one chunk per article**. Articles over 300 words are split between numbered apartados, never mid-sentence.
6. Start each chunk with a short header naming the law, its Título/Capítulo and the article.
7. Embed the chunks with Gemini (`gemini-embedding-2`) and store them in ChromaDB (`index/chroma`) in batches of 20, saving each batch straight away. Chunk ids are a hash of the text, so re-running only embeds new or changed chunks.

**Extraction problems fixed:**
- Long Sección titles in Llei 18/2007 run onto a second line, and the parser only kept the first line, so the rest of the title ended up inside the article text. I fixed it by joining the wrapped line back onto the title.
- The LAU PDF I had downloaded was corrupted (saved as text, so it couldn't be opened). I replaced it with a clean copy from boe.es.

**Chunk metadata:** source file, law short name, article and its heading, apartados covered, Título / Capítulo / Sección, first and last page, and a ready-made citation (e.g. `LAU, Artículo 36, apartados 1–5, p. 25`).

**Number of chunks:** 440 (LAU 129, Llei 18/2007 289, Decret-llei 3/2023 22), averaging 218 words.

## Test set

36 questions in `eval/questions.csv`, written in Spanish from the three corpus documents before any tuning. Each question was drafted from a specific article, and its reference answer was checked against the official BOE text. `multi` questions need two passages, sometimes from different laws. `unanswerable` questions stay on topic (rent indices, okupas, tourist flats) but ask for facts the documents don't contain.

| Kind | Count |
|---|---|
| `single` | 24 |
| `multi` | 6 |
| `unanswerable` | 6 |
| **Total** | **36** |

**Example (`multi`, q27):**
"Un propietario de Barcelona quiere alquilar su piso a turistas por estancias de 10 noches. ¿Se aplica la LAU? ¿Qué permiso necesita?"
Expected: the LAU does not apply (art. 5.e excludes tourist lets of 31 days or less), and Barcelona requires a prior urban-planning licence (Decreto-ley 3/2023, art. 1.1 and Annex).

**Example (`unanswerable`, q32):**
"¿Cuál es la pena por ocupar un piso vacío (usurpación)?"
Expected: the assistant says the documents don't cover it (the penalty is in the Código Penal, art. 245) instead of answering from memory.

## Retrieval

**Designs compared:** two chunkings × three search methods (`retrieve.py`, `evaluate.py`).
- **Chunkings.** *structure*: one chunk per article, as above. *fixed*: plain 300-word windows with 50 words of overlap that ignore the legal structure (326 chunks).
- **Search methods.** *dense*: Gemini embedding similarity. *bm25*: keyword matching. *hybrid*: both rankings merged with reciprocal rank fusion.

A hit means the expected article from the expected document is in the top k. A `multi` question counts only if every expected passage is there. Results are over the 30 answerable questions. "Words added" is the average number of words the top-k chunks add to the prompt.

| Design | hit@1 | hit@3 | hit@5 | words added (k=1 / 3 / 5) |
|---|---|---|---|---|
| structure + dense | **0.70** | 0.93 | **0.97** | 247 / 719 / 1,185 |
| structure + bm25 | 0.60 | 0.83 | 0.90 | 255 / 733 / 1,226 |
| **structure + hybrid** | 0.67 | **0.97** | **0.97** | 249 / 726 / **1,179** |
| fixed + dense | 0.53 | 0.83 | 0.87 | 300 / 899 / 1,499 |
| fixed + bm25 | 0.57 | 0.80 | 0.87 | 300 / 900 / 1,500 |
| fixed + hybrid | 0.60 | 0.93 | 0.97 | 300 / 900 / 1,500 |

**Chosen design: structure + hybrid, k = 5.**
- Structure chunking matches or beats fixed windows with every search method, while adding about 20% fewer words to the prompt.
- Hybrid has the best hit@3 and ties dense at k=5. Dense is better at hit@1 by a single question.
- k = 5 leaves room for both passages of two-passage questions.

Per-question results are in `eval/retrieval_per_question.csv`.

## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

AI helped me with much of the code especially creating the scripts to seperate the pdf text, clean it and chunk it accordingly whether it was structured or fixed and it especially helped out with scripts for th structured ones where i had to cut long articles and seperate them into smaller chunks of apartados. This was very improtant so nothing was chunked appropiately as I wanted to test it in different ways. I also used it to format this report so it would look nice in the md file styling. 