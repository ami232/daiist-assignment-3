# Requirements Document — "Asistente Autónomo" (Assignment 3)

> Status: draft v0.1 (2026-11-19). Items marked **🟨 DECISION (student)** must be decided and justified by the student. The brief reserves them, and they are tested in the written comprehension check. Claude can propose options but does not choose.

## Introduction

A Spanish-language question-answering assistant for **a young Spaniard who already runs a small business informally and wants to formalise it as a *trabajador autónomo***. The assistant answers only from Spanish state legislation (consolidated BOE texts) and cites the law and article for every claim. When the corpus does not cover a question, it says so instead of guessing. It runs locally as a RAG pipeline exposed through an MCP server. Three things use that server: a Claude Code subagent, a LangChain harness (`agent.py`), and an evaluation stage.

**Why a wrong answer matters:** an autónomo who acts on a wrong answer can pay surcharges or fines (late *alta* in Hacienda or the RETA (special social security scheme for the self-employed); invoices that don't meet the legal requirements), lose the *tarifa plana* (reduced flat-rate social security contribution for new autónomos), contribute in the wrong bracket, or miss benefits such as *cese de actividad* or sick-leave cover. "No lo sé, consulta a un gestor / la Seguridad Social / la AEAT" costs one consultation. A confident wrong answer costs money and legal exposure.

## Glossary

- **Autónomo**: a self-employed person registered in the RETA.
- **RETA**: the social security scheme for self-employed workers (LGSS Title IV).
- **TRADE**: *trabajador autónomo económicamente dependiente*, an autónomo who earns ≥75% of income from one client (LETA arts. 11–18).
- **Tarifa plana**: reduced contribution when starting an activity (LETA art. 38 ter).
- **Cese de actividad**: unemployment-type benefit for autónomos (LGSS Title V).
- **Alta censal**: registration in the tax census of businesses and professionals, Censo de Empresarios, Profesionales y Retenedores (RD 1065/2007 art. 9).
- **Consolidated text**: the BOE's informational version of a law with all its amendments merged in. It is *not* the official text (a BOE reuse condition).
- **Chunk**: a unit of retrieval: text plus metadata (source, location, date).
- **Location**: the citation-level position of a chunk: `Artículo N`, `Disposición adicional X`, plus where it sits in the law (Título > Capítulo > Sección).
- **Design**: one retrieval configuration (chunking + search method), compared by hit rate.
- **Hit@k**: the share of answerable questions where at least one of the top-k chunks has the expected source and location.
- **Refusal**: the assistant's standard statement that the corpus does not cover the question.
- **Judge**: an LLM that grades an answer against a reference answer and the retrieved evidence, using a rubric.
- **Harness**: `agent.py`, the LangChain agent with guardrails.

## Corpus (proposed, verified 2026-11-19 against the BOE open-data API)

| ID | Document | BOE id | Extract indexed | Words after cleaning | Last consolidated |
|---|---|---|---|---|---|
| LETA | Ley 20/2007, Estatuto del trabajo autónomo | BOE-A-2007-13409 | Whole articulado + disposiciones (61 blocks) | 16,424 | 2026-09-02 |
| LGSS | RDL 8/2015, Ley General de la Seguridad Social | BOE-A-2015-11724 | Título IV (RETA) + Título V (cese de actividad), arts. 305–350 | 18,173 | 2026-11-11 |
| RF | RD 1619/2012, Reglamento de facturación | BOE-A-2012-14696 | The Reglamento only (not the approving decree) | 11,852 | 2026-03-31 |
| RGAT | RD 1065/2007, Reglamento de gestión e inspección tributaria | BOE-A-2007-15984 | Título II, caps. I–IV (alta censal, domicilio fiscal, NIF, libros registro), arts. 2–29 | 14,567 | 2026-10-28 |
| | **Total indexed** | | | **61,016** | |

The raw per-título counts measured on day 1 (≈84k words) included BOE editorial annotations. In LETA these were 10,863 words of `<blockquote>` notes, ≈40% of the raw text. Cleaning removes them (see REQ-3).

**Held out for the add-document demo:**
- **H1 (chosen, verified 2026-11-19):** **Orden PJC/297/2026**, de 30 de marzo (BOE-A-2026-7296, consolidated 2026-07-16), Cap. I Sección 2ª, **arts. 18–19**. These hold the 2026 RETA contribution tables: 3 reduced-table and 12 general-table brackets with minimum and maximum bases, and the rates (28,30% common contingencies, 1,30% professional contingencies, 0,90% MEI, the intergenerational equity surcharge). ≈2,150 words, ≈10 chunks. Before it is added, the corpus only says the brackets are set annually (LGSS art. 308), so the question is unanswerable.
- **H2 (fallback):** RD 439/2007 Reglamento IRPF, arts. 109–112 (modelo 130 quarterly IRPF prepayments, ≈1,900 words).

**Licence:** BOE reuse conditions (Ley 37/2007, RD 1495/2011) allow commercial and non-commercial reuse provided that:
1. the source is cited;
2. the text is not distorted;
3. the update-date metadata is kept;
4. consolidated texts are stated to be *informational only*.

No personal data.

## Requirements

### REQ-1 Use case definition 🟨
**User Story:** As the student, I want a written use case, so that every later decision (refusal policy, ship decision) has a stated cost model.
1. THE report SHALL state who asks, what they do with the answer, and what a wrong answer costs compared with a refusal. **🟨 DECISION (student): wording and cost argument.**
2. THE report SHALL list in-scope topics (alta, cotización, tarifa plana and bonificaciones, facturación, censal obligations, TRADE, IT (sick leave) and *cese de actividad*). It SHALL list out-of-scope topics (SL/company law, IVA rates, IRPF calculation, regional aid, labour law for employees). **🟨 DECISION (student): final boundary.**

### REQ-2 Corpus acquisition
**User Story:** As a grader, I want the corpus downloaded reproducibly, so that `main.py index` runs with no manual steps.
1. WHEN `main.py index` runs, THE index stage SHALL download each source from the BOE open-data API (`/datosabiertos/api/legislacion-consolidada/id/{id}/texto` and `/metadatos`) into `corpus/` (git-ignored), and skip any file already present.
2. THE corpus SHALL contain ≥3 documents and ≥50,000 words after cleaning. THE index stage SHALL print the count per document.
3. THE index stage SHALL record each document's `fecha_actualizacion` (consolidation date) and URL.
4. IF a download fails, THEN THE index stage SHALL retry with backoff and, if it still fails, exit non-zero with the BOE id in the message.

### REQ-3 Extraction and cleaning
**User Story:** As the assistant, I want clean current-law text, so that answers never quote repealed wording or editorial notes.
1. FOR each `<bloque>`, THE extractor SHALL keep only the **last `<version>`** (the version in force).
2. THE extractor SHALL drop editorial notes (`p.nota_pie`, `p.nota_pie_2`, "Se añade por…/Redactado por…" blocks), the preamble, and signature blocks. It SHALL keep tables as plain text rows.
3. THE extractor SHALL apply the configured block range per document (e.g. LGSS `tiv`…`tvi`).
4. THE report SHALL describe one extraction problem that was fixed. Problems found and fixed in Phase 1, any of which can be used:
   - **BOE annotations inside the law text.** "Téngase en cuenta…" and "Se modifica por…" `<blockquote>`s made up 10.9k of LETA's 27.6k raw words, plus `nota_pie` paragraphs inside headings ("CAPÍTULO II … Se añade por el art. 1.8 de la Ley 31/2015").
   - **Every block carries its full version history.** Only the last `<version>` is in force.
   - **Two "Artículo 1"s in RD 1619/2012.** The approving decree and the Reglamento it approves each number articles from 1, so citations would be ambiguous. Caught by the duplicate-location check; fixed by indexing the Reglamento only.
   - **Repealed stubs.** For example, LETA arts. 31–32 bis, repealed by RDL 13/2022, now read "(Derogado)". They were dropped so their titles don't outrank art. 38 ter, which replaced them.
   - **Unreadable block ids.** For example, `a3-5` = "Artículo 38 ter". Locations are taken from the block title instead.
5. THE extractor SHALL drop blocks that contain only a repeal stub ("(Derogado)", "(Sin contenido)").

### REQ-4 Chunking with metadata 🟨
**User Story:** As a user, I want each retrieved passage to say exactly where it comes from, so that I can check it on the BOE.
1. EVERY chunk SHALL carry: `source` (short ID, e.g. `LETA`), `boe_id`, `law_title`, `location` (from the block's `titulo` attribute, e.g. `Artículo 38 ter`), `path` (Título > Capítulo > Sección), `block_id`, `part` (n of m when an article is split), `fecha_actualizacion`, `url` (BOE consolidated URL + `#block_id`), `n_words`.
2. THE chunker SHALL support at least two strategies, selected by name: **fixed-size word windows** (size and overlap configurable) and **structure-based** (one chunk per article/disposición, split by *apartado* when longer than a maximum).
3. **🟨 DECISION (student):** chunk sizes, overlap, maximum article length, and which strategy ships (REQ-6).

### REQ-5 Embedding and storage within quota
**User Story:** As the student, I want indexing to survive the free-tier limit, so that no embedding is paid for twice.
1. THE index stage SHALL embed with `gemini-embedding-2` and store vectors in ChromaDB under `index/`, one collection per chunking design.
2. Chunk IDs SHALL be deterministic (hash of design + boe_id + block_id + part + text). THE index stage SHALL embed only IDs not already stored.
3. THE index stage SHALL persist after every batch, so that a crash or quota error loses at most one batch.
4. IF the API returns a quota/rate error, THEN THE index stage SHALL stop cleanly, report how many chunks are still pending, and exit so that a re-run resumes.
5. Query embeddings SHALL be cached on disk (keyed by model + text). Re-running the evaluation SHALL NOT re-embed the same question.
6. `index/` SHALL stay under 90 MB and be committed.
7. THE per-file pipeline SHALL be exposed as importable functions (`load_document(path)`, `chunk_document(doc, design)`, `embed_and_store(chunks, collection)`).

### REQ-6 Retrieval comparison 🟨
**User Story:** As the student, I want hit rate at k = 1, 3, 5 for ≥2 designs, so that I choose the design by the numbers.
1. THE evaluation SHALL compute Hit@1/3/5 per design over all answerable questions. A hit SHALL be a top-k chunk whose `source` and `location` match `expected_source`/`expected_location` (any of several when `;`-separated).
2. THE evaluation SHALL report the average words added to the prompt at k for each design.
3. THE evaluation SHALL compare ≥2 designs. The candidates are below; free designs reuse an existing embedding set.
   - A: fixed windows (costs a full embedding)
   - B: structure-based (costs a full embedding)
   - C: B + hybrid BM25 (free)
   - D: B + `source` metadata filter (free)
4. **🟨 DECISION (student): which designs to compare and which one ships, justified by the table.**

### REQ-7 Test set 🟨 (student-authored)
**User Story:** As the student, I want my own test set written before tuning, so that the evaluation is honest.
1. `eval/questions.csv` SHALL have ≥30 questions in Spanish, phrased as the persona would ask. At least 5 SHALL be `multi` (two passages), at least 5 `unanswerable` (close to the topic), and the rest `single`.
2. `expected_source` SHALL use the `source` IDs, and `expected_location` the `location` strings, exactly as they appear in the chunk metadata.
3. **🟨 Written by the student, before any retrieval tuning.** Claude may only check the format and that the ids/locations exist.

### REQ-8 MCP server
**User Story:** As an agent, I want `search` and `add_document` tools, so that any MCP client can use the corpus.
1. `search(query: str)` SHALL return the top-k chunks of the shipped design. Each chunk SHALL include its text, `[source, location]` citation, URL and consolidation date. The output SHALL include the BOE "texto consolidado, carácter informativo" notice.
2. `add_document(path: str)` SHALL run the file through the **imported** `index.py` functions, embed only new chunks, store them in the shipped collection, and return a summary: document, chunks added, chunks skipped.
3. Already-indexed policy **🟨 DECISION (student; proposed default)**. The default:
   - same `boe_id` and same `fecha_actualizacion`: no-op, reported as "ya indexado";
   - newer consolidation date: replace that document's chunks;
   - otherwise: add.
4. THE server SHALL load `index/` at startup, never re-embed the corpus, write nothing to stdout except the protocol, and log to stderr.
5. IF `path` does not exist, cannot be parsed, or is outside the allowed folder, THEN `add_document` SHALL return an error message and not raise.
6. Tool docstrings SHALL describe the corpus, when to use the tool, and what it returns. `check.py` rejects TODO docstrings.

### REQ-9 Subagent
**User Story:** As a Claude Code user, I want a `corpus-researcher` subagent restricted to `search`, so that legal lookups are delegated and cited.
1. `.claude/agents/corpus-researcher.md` SHALL list only `mcp__corpus__search` and describe the corpus and when to delegate.
2. THE report SHALL include one real transcript of the subagent used from Claude Code.

### REQ-10 Harness (`agent.py`) 🟨
**User Story:** As a user, I want `main.py ask "…"` to answer with citations, and to ask me before the index is modified.
1. THE harness SHALL use LangChain `create_agent` with a Gemini chat model, the MCP tools loaded from `server.py`, and `AGENTS.md` as the system prompt.
2. WHEN the model calls `add_document`, THE harness SHALL pause and ask for human approval (y/n) in the terminal. IF the answer is no, or there is no TTY (as in evaluation), THEN THE tool SHALL NOT run.
3. THE harness SHALL enforce a tool-call limit per question (e.g. ≤4 searches).
4. THE harness SHALL implement one extra guardrail. **🟨 DECISION (student)**. Candidates:
   - (a) a citation validator: every `[source, location]` cited must appear in that turn's retrieved chunks, else repair once or refuse;
   - (b) a scope/advice guardrail: personalised tax calculations are redirected to a professional;
   - (c) a staleness notice when a cited chunk's consolidation date is older than X.
5. THE harness SHALL expose `answer(question) -> {answer, citations, trace, tokens, seconds}` for `evaluate.py`, and print the answer and citations for `main.py ask`.
6. `AGENTS.md` SHALL state the rules with a reason for each. At minimum: answer only from search results; cite every claim; use the fixed refusal phrase when the corpus does not cover a question. **🟨 DECISION (student): the rules and refusal wording.**

### REQ-11 End-to-end evaluation 🟨
**User Story:** As the student, I want to measure correct answers, unsupported claims and refusals, so that the ship decision rests on evidence.
1. THE evaluation SHALL run the harness on every question and save answers, traces, tokens and seconds to `eval/` (resumable; already-answered ids skipped).
2. Code checks SHALL compute, per answer:
   - whether a refusal was given (fixed phrase);
   - whether every citation is well-formed and present in the retrieved chunks;
   - whether the expected source/location was cited.
3. An LLM judge SHALL grade correctness and support against the reference answer and the retrieved text, using a written rubric. **🟨 DECISION (student): rubric.**
4. `eval/human_labels.csv` SHALL hold ≥20 student grades made before reading the judge's verdicts. THE evaluation SHALL report agreement with the judge (% agreement, plus Cohen's κ if feasible).
5. THE evaluation SHALL report counts: correct, unsupported, correct refusals, wrong refusals; plus mean tokens and seconds per question.
6. THE add-document demo SHALL show the answer to one `unanswerable` question before and after adding the held-out document (H1 or H2).

### REQ-12 Failure analysis and decision 🟨
1. EACH failed question SHALL be classified as one of: retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question. **🟨 student classification.**
2. THE report SHALL give counts by cause and say what to fix first.
3. **🟨 DECISION (student):** would users be allowed to rely on it, for what, and with which safeguard; cost and latency per question.

### REQ-13 Submission integrity (hard gate)
1. `uv run python main.py index`, `main.py ask "…"` and `main.py evaluate` SHALL each run end to end with no manual steps on Windows and on Ubuntu (GitHub Actions).
2. `uv run python check.py` SHALL pass. `check.py` SHALL NOT be edited.
3. `.env` SHALL never be committed. AI use SHALL be disclosed in REPORT.md.

## Non-functional targets

- `search` responds in < 3 s (one query embedding plus a local Chroma lookup). Server startup < 10 s.
- `main.py ask` finishes in < 60 s; `check.py` allows up to 300 s.
- Embedding budget: corpus re-index ≤ ~600 texts per design; ≤ 1,000 texts per day in total, including queries.
