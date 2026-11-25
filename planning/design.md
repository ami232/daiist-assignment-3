# Design Document — "Asistente Autónomo"

> Draft v0.1 (2026-11-19). Traces to `requirements.md`. 🟨 marks decisions reserved for the student. Everything else is an engineering choice that can be changed freely.

## Overview

A local RAG pipeline over four Spanish laws pulled from the **BOE open-data API**. The API returns XML structured by article, so we parse it directly instead of scraping HTML or PDFs, and each chunk carries an exact legal citation.

One ingestion module (`index.py`) is the single source of truth for loading, cleaning, chunking and embedding. Three things reuse it:
- the `main.py index` stage;
- the MCP server's `add_document`;
- the evaluation's per-design collections.

All Gemini calls are **quota-aware**: deterministic chunk IDs, write-after-every-batch, and an on-disk query-embedding cache.

## System architecture

### Component map

| ID | Component | File | Responsibility | Talks to |
|---|---|---|---|---|
| C1 | Source registry | `sources.py` (or a constant in `index.py`) | List of documents: short ID, BOE id, block range, `held_out` flag | C2 |
| C2 | BOE fetcher | `index.py` | Download `/texto` + `/metadatos` XML into `corpus/` (skip if present) | BOE API, C3 |
| C3 | Extractor / cleaner | `index.py` | XML → `Block` list: last version only, notes stripped, hierarchy path | C4 |
| C4 | Chunker | `index.py` | `Block`s → `Chunk`s for a named design (`fixed`, `article`) | C5 |
| C5 | Embedder + store | `index.py` (+ `rag.py` helpers) | Embed missing chunk IDs in batches, upsert into Chroma, persist | Gemini Embeddings, ChromaDB |
| C6 | Retriever | `rag.py` | Query → top-k chunks: dense (Chroma), optional BM25 hybrid, optional metadata filter. Query-embedding cache | C5, cache |
| C7 | MCP server | `server.py` | `search(query)`, `add_document(path)`; loads index at startup | C6, C2–C5 |
| C8 | Subagent | `.claude/agents/corpus-researcher.md` | Claude Code subagent limited to `search` | C7 |
| C9 | Harness | `agent.py` | LangChain `create_agent` + Gemini chat + MCP tools + guardrails; `answer()` API + CLI | C7, Gemini Chat |
| C10 | Evaluator | `evaluate.py` | Hit@k per design; runs C9 on every question; code checks; LLM judge; human agreement; costs | C6, C9, Gemini Chat |
| C11 | Rules | `AGENTS.md` | System prompt (rules + reasons) 🟨 | C8, C9 |

`rag.py` is a small shared module, so that `server.py` and `evaluate.py` don't duplicate retrieval code. `main.py` and `check.py` are left as they are.

### Architecture diagram

```
                 BOE open-data API (XML, consolidated text + metadata)
                                 │  C2 fetch (once; cached in corpus/)
                                 ▼
 ┌──────────────────────────── index.py ────────────────────────────┐
 │ C1 SOURCES ─► C2 fetch ─► C3 extract/clean ─► C4 chunk(design) ─► │
 │                                         C5 embed_missing + upsert │
 └───────────────────────────────┬──────────────────────────────────┘
                                 │ imported by
          ┌──────────────────────┼─────────────────────────┐
          ▼                      ▼                         ▼
   main.py index          server.py (C7, MCP stdio)   evaluate.py (C10)
                          ├ search ──► rag.py (C6) ◄──┤ hit@k per design
                          └ add_document ─► index.py  │
                                 ▲                     │ answer()
               MCP stdio         │                     ▼
   Claude Code ── C8 subagent ───┤               agent.py (C9)
                                 └───── MCP stdio ── LangChain create_agent
                                                     + Gemini chat + guardrails
 index/  (ChromaDB persistent: one collection per design; query_cache.sqlite)
 eval/   (questions.csv, answers.jsonl, retrieval.csv, judge.csv, summary.json, human_labels.csv)
```

## Data flows

### F1 Build index (`main.py index`)
1. C1 yields `Source(id="LETA", boe_id="BOE-A-2007-13409", range=None, held_out=False)` …
2. C2 → `corpus/BOE-A-2007-13409.xml` and `.meta.xml` (skipped if present).
3. C3 → `Block(source, boe_id, block_id, location="Artículo 38 ter", path="Título V > Capítulo II", text, fecha_vigencia)`.
   - For each `<bloque>`, take the last `<version>`.
   - Drop `nota_pie*`, `preambulo`, `firma*`, and empty blocks.
   - Headings (`encabezado`) update the path but don't emit text.
4. C4: for each design in `DESIGNS`, produce `Chunk`s. ID = `sha1(design|boe_id|block_id|part|text)[:16]`.
5. C5: `missing = ids − collection.get(ids).ids`. Embed in batches of up to 50 → `collection.upsert` after each batch → log progress to stderr. On a 429 error, stop and print the number still pending.
6. Print the summary: words per document, chunks per design, pending.

### F2 Search (MCP `search`)
1. query → C6: `embed_query(query)`, looked up first in `index/query_cache.sqlite`.
2. Chroma `query(n_results=k)` on the shipped collection, with the optional hybrid/filter step.
3. Format each result:
   ```
   [n] LETA — Artículo 38 ter (Título V > Capítulo II) · BOE-A-2007-13409 · consolidado a 2026-09-02
   <text>
   https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409#a3-5
   ```
   and append the BOE informational-text notice.

### F3 Add document (MCP `add_document`)
1. Validate the path: it exists, is under the repo or `corpus/`, and is a BOE XML file (or HTML/PDF, 🟨 if needed).
2. Read `boe_id` and `fecha_actualizacion` from the file, or from its sibling `.meta.xml`.
3. Apply the duplicate policy 🟨 (proposed: same id + same date → no-op; newer → delete that document's chunks, then add; new → add).
4. Reuse C3 → C4 (shipped design) → C5. Return `"Added: LETA2 (…). 12 new fragments, 0 skipped (already there)."`.

### F4 Ask (`main.py ask`)
1. `agent.py` starts `server.py` over stdio (`langchain-mcp-adapters` or the `mcp` client) and wraps the tools.
2. It runs `create_agent(model, tools, system_prompt=AGENTS.md, middleware=[…])`:
   - human approval on `add_document`;
   - the tool-call limit;
   - the extra guardrail 🟨.
3. It returns `{answer, citations, trace, usage, seconds}`; the CLI prints the answer and its citations.

### F5 Evaluate (`main.py evaluate`)
1. **Retrieval:** for each design × answerable question, compute top-5 and hits at 1/3/5, plus words added to the prompt. Writes `eval/retrieval.csv` and the summary.
2. **End to end:** for each question not yet in `eval/answers.jsonl`, call `answer()`. Approval auto-denied. Appends to the file.
3. **Code checks:** refusal phrase, citation validity, expected source cited.
4. **Judge:** one structured-output call per answer with the rubric 🟨 and the retrieved text → `eval/judge.csv`.
5. **Agreement** with `eval/human_labels.csv` (% agreement and κ on `correct` and `supported`).
6. **Summary:** `eval/summary.json` and the printed table (counts, mean tokens, mean seconds).

The before/after add-document demo is a separate step, `evaluate.py --demo-add` or a documented script. That keeps the shipped index from being changed by default evaluation runs.

## Integration points

### BOE open-data API
- `GET https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}/texto` (and `/metadatos`), header `Accept: application/xml`. No auth.
- Structure: `response/data/texto/bloque[@id,@tipo,@titulo]/version[@fecha_vigencia]/p[@class]|table|blockquote`.
- Gotchas found on 2026-11-19:
  - `id`s like `a3-3` stand for "Artículo 31 bis", so use `@titulo` for the location;
  - headings contain amendment notes;
  - every block keeps its full version history.
- Errors: retry 3× with exponential backoff. Content is cached in `corpus/`, so after the first run the API is no longer needed.

### Gemini embeddings (`gemini-embedding-2`)
- Called through `google-genai` `client.models.embed_content`, using `api_key.load_api_key()`.
- The free tier allows ≈1,000 texts a day, and each text in a batch counts.
- To confirm in Phase 0:
  - whether the model takes a task type or a query/document prefix;
  - the output dimensionality (use a reduced size such as 768 if supported, to keep `index/` small);
  - the maximum tokens per text.
- Errors: a 429 is fatal for the current run (stop and resume later); 5xx errors are retried.

### Gemini chat (harness + judge)
- Model: **to choose in Phase 0** from the models the key can access (a current Flash-class model). Use the same model for the agent and the judge, or a stronger judge if the quota allows.
- Called through `langchain-google-genai` (`ChatGoogleGenerativeAI`). Usage metadata gives the token counts.
- Rate limits: requests-per-minute throttling plus retry on 429. Evaluation is resumable.

### MCP (stdio)
- `server.py` is registered in `.mcp.json` (Claude Code) and `.vscode/mcp.json` (Copilot) as `corpus`.
- `agent.py` and `check.py` start it as `python server.py`.

## Data models

```python
@dataclass
class Source:          # C1
    id: str            # "LETA"
    boe_id: str        # "BOE-A-2007-13409"
    title: str
    block_range: tuple[str, str] | None   # ("tiv", "tvi") — first id included, last id excluded
    held_out: bool = False

@dataclass
class Block:           # C3 output
    source: str; boe_id: str; block_id: str
    location: str      # "Artículo 38 ter" / "Disposición adicional segunda"
    path: str          # "Título V > Capítulo II"
    text: str          # cleaned current text, including the article heading
    fecha_vigencia: str

@dataclass
class Chunk:           # C4 output → Chroma (id, document=text, metadata=all else)
    id: str; design: str; text: str
    source: str; boe_id: str; law_title: str
    location: str; path: str; block_id: str; part: str  # "1/3"
    fecha_actualizacion: str; url: str; n_words: int
```

Chroma layout: `index/chroma/` with one collection per design (`article_v1`, `fixed150_v1`, …), using cosine distance. `index/query_cache.sqlite` holds `(model, text) → vector`.

Eval files:

| File | Contents |
|---|---|
| `answers.jsonl` | id, answer, citations, trace, tokens, seconds |
| `retrieval.csv` | design, id, hit@1/3/5, words |
| `checks.csv` | per-answer code checks |
| `judge.csv` | per-answer judge verdicts |
| `summary.json` | aggregate results |

## Component interfaces

```python
# index.py
SOURCES: list[Source]; DESIGNS: dict[str, ChunkConfig]; SHIPPED_DESIGN: str
def fetch(source: Source) -> Path
def load_document(path: Path, block_range=None) -> tuple[DocMeta, list[Block]]
def chunk_blocks(blocks: list[Block], meta: DocMeta, design: str) -> list[Chunk]
def embed_and_store(chunks: list[Chunk], collection) -> dict  # {"added", "skipped", "pending"}
def index_file(path: Path, design: str, policy="skip_same_version") -> dict   # used by add_document
def main() -> None

# rag.py
def get_collection(design: str)
def embed_query(text: str) -> list[float]                 # cached
def retrieve(query: str, design: str, k=5, mode="dense", source_filter=None) -> list[Hit]
def format_hits(hits: list[Hit]) -> str

# agent.py
def build_agent(...) -> Agent
def answer(question: str, approve: Callable[[dict], bool] | None = None) -> dict
```

## Retrieval designs (to compare, 🟨 student chooses)

| Design | Chunking | Search | Embedding cost |
|---|---|---|---|
| A `fixed` | ~150–250-word windows, ~20% overlap, block-aware metadata (first location in window) | dense | 1 full index (≈400–600 texts) |
| B `article` | one chunk per article; split by numbered apartado when > ~400 words | dense | 1 full index (≈250–350 texts) |
| C | B | hybrid: dense + BM25 (`rank_bm25`), reciprocal-rank fusion | free |
| D | B | dense + `source` filter, from a cheap query classifier or the question's own wording | free |

The budget fits A + B over two days, with C and D free on top. The test set must exist **before** any of these runs.

## Embedding budget (61k words, measured in Phase 1 with the provisional parameters)

| Item | Texts |
|---|---|
| Design B `article` (max 400 w): median 247 w, 132 of 261 chunks come from split articles | 261 |
| Design A `fixed` (200 w, overlap 40) | 382 |
| 35 questions × 1 (cached once, reused across designs) | 35 |
| Agent runs: the agent rewrites queries; ~2 searches × 35 questions | ~70 |
| `check.py`, demos, debugging | ~50 |
| **Total** | **≈ 800, fits in one day if nothing is re-run** |

Article lengths (p25/p50/p75/p90): 116 / 258 / 448 / 736 words, max 2,367 (LGSS art. 308). Half the articles fit whole at 400 words.

Phase 1 placement change: the location lookup table is written to `index/outline.csv` (committed with the index), not to `corpus/`, so the test-set checks and `evaluate.py` can use it on a fresh clone.

## Error handling

| Category | Cases | Handling |
|---|---|---|
| Quota | embedding 429, chat 429 | Embeddings: stop and keep what's saved. Chat: back off (≤3 retries); evaluation resumes from the saved files |
| Source | BOE down, unexpected XML | Cached `corpus/`; explicit failure naming the BOE id and the block |
| Tool input | bad path, unsupported file, duplicate document | `add_document` returns a Spanish error string; never raises across MCP |
| Agent | over the tool limit, empty retrieval, invalid citation | Limit middleware ends the run with a refusal; guardrail repairs once or refuses |
| Protocol | stray stdout in the server | All logging goes to `logging` → stderr; no `print` in `server.py` or in imported module code paths |

## Testing strategy

- Unit checks (lightweight `tests/` or `__main__` asserts):
  - the extractor drops notes and keeps only the last version (golden check on LETA art. 38 ter);
  - chunk IDs are stable across runs;
  - the duplicate policy works.
- `check.py` locally after every phase; on GitHub Actions before submission.
- A retrieval sanity script: 5 hand queries → expected article in the top 3.
- An Ubuntu run via Actions to catch path and encoding issues. Windows consoles are cp1252, so set UTF-8 output explicitly.

## Phase 0 findings and open questions

Resolved (2026-11-19):
- **Installed stack:**

  | Package | Version |
  |---|---|
  | mcp | 2.3.0 (`mcp.server.mcpserver.MCPServer` imports fine) |
  | langchain | 1.4.8 |
  | langchain-core | 1.7.4 |
  | langgraph | 1.2.19 |
  | langchain-google-genai | 4.4.2 |
  | google-genai | 2.34.0 |
  | chromadb | 1.5.9 |

  `langchain.agents.middleware` provides `HumanInTheLoopMiddleware` (approval for `add_document`), `ToolCallLimitMiddleware` / `ModelCallLimitMiddleware` (call limit), `ModelRetryMiddleware` / `ToolRetryMiddleware` (429 handling) and a generic `AgentMiddleware` for the custom guardrail. No extra package is needed for the guardrails.
- **H1:** Orden PJC/297/2026 (BOE-A-2026-7296) is in the consolidated-text API. Arts. 18–19 hold the 2026 RETA bracket tables, as `<table>` elements, so the extractor must render table rows as text. The source registry marks it `held_out=True` with block range `a1-10`…`a1-11`. `add_document(path)` looks up the range in the registry by `boe_id`; an unknown document is indexed whole.

- **Session 10 reference:** `07-own-harness/` from the public course repo [ami232/daiist-agents](https://github.com/ami232/daiist-agents), copied into `planning/reference/`. Patterns to reuse:
  - MCP tools via `langchain.mcp.MCPAdapter(Path("server.py"))`, one adapter per server, inside an `AsyncExitStack`;
  - approval as a `@wrap_tool_call` middleware that returns an error `ToolMessage` on refusal, with an `auto_approve` flag;
  - `ModelCallLimitMiddleware(run_limit=…)`;
  - `ask(agent, q) -> (answer, trace)` via `tool_trace(messages)`;
  - a judge using `with_structured_output(Verdict)`, with reasoning before a boolean verdict, temperature 0, and the trace given as evidence.
- **Models (course defaults):** agent `gemini-3.5-flash-lite`, judge `gemini-3.5-flash` (stronger than the agent, as the course recommends). Confirm both are reachable with the key.
- **Dependency added:** `uv add "langchain[mcp]>=1.4.7"`. This brings in `fastmcp`; `MCPAdapter` imports (beta warning only). `langchain-mcp-adapters` is **not** needed.

Still open:
1. Confirm the chat models are reachable, plus the embedding task-type and dimensionality options for `gemini-embedding-2`. **Blocked on `.env`.**
2. `rank-bm25` is only needed if design C (hybrid) is chosen.
3. Evaluation must deny `add_document` rather than auto-approve every tool, as the course's `auto_approve=True` does, so the shipped index isn't changed. Approval should be per tool, with `add_document` denied in eval.
