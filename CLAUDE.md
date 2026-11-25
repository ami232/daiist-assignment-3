# Development notes

These notes are for working on the code. AGENTS.md is the corpus assistant's system prompt and is graded, so keep development notes out of it.

## Quota rules
- Gemini embeddings: about 1,000 texts a day. Run `uv run python index.py --dry-run` first: it counts chunks and never calls Gemini. A real run asks for approval before embedding anything that isn't cached. `--yes` or `INDEX_YES=1` skips the question. `main.py index` passes no flags, so it asks.
- Every vector goes into `index/embeddings.jsonl` (float32, base64) as soon as its batch returns. The key is sha256(model | exact text sent). Queries use the same cache (`embed_query`). Never delete this file: it is the quota.
- ChromaDB (`index/chroma`) is rebuilt from the cache. There is one collection per design, `chunks_<design>`.

## Gotchas
- With `gemini-embedding-2`, google-genai packs a `list[str]` into a single Content, which would give one blended vector per batch. `embed_texts` therefore wraps each text in its own `types.Content`, and it checks that one vector comes back per text before saving anything.
- `gemini-embedding-2` takes the task as a text prefix, not `task_type`. Documents are sent as `title: … | text: …` and queries as `task: search result | query: …`. Changing these strings changes the cache keys, so everything would be re-embedded.
- The page-drop rules are tied to the PDF checksums in `DOCS`. If NIST republishes a file, `download_corpus` stops instead of silently mis-cleaning it.
- Library code in index.py logs to stderr only, because server.py's stdout carries the MCP protocol.
- langchain-mcp-adapters 0.3.1 (the latest uv resolves) imports `mcp.shared.context.RequestContext`, which mcp 2.x no longer has. agent.py therefore wraps the server's tools itself (`mcp_tools`) over one stdio `ClientSession`. Don't add the adapter back unless a release supports mcp 2.x.
- The shared pieces live in `retrieval.py` (vector, BM25 and hybrid search, the routing filter, result formatting and the citation checker). Which configuration the server serves is set in `retrieval.CHOSEN`. Set it from the numbers in `eval/retrieval.csv`, not by hand-tuning on the test set.
- To test the harness without quota, monkeypatch `agent._model` with a scripted `GenericFakeChatModel` (`bind_tools` returning self). An empty index returns no hits without embedding the query.
- evaluate.py caches agent answers, judge verdicts and the baseline in `eval/*.jsonl`. The keys include the model, AGENTS.md, `CHOSEN` and the rubric, so changing any of them re-runs only what's affected. The key uses the exact AGENTS.md text: even a one-character edit re-runs all 43 answers and makes them differ from the graded ones. Don't touch AGENTS.md or the rubric after grading.
- The retrieval evaluation loads only the original four documents (`Retriever(only_docs=...)`). A document added later, like CSF 2.0 in the demo, would otherwise shift BM25's statistics and the numbers.
- After another process (the MCP server's add_document) writes to ChromaDB, this process's cached client is stale ("Error finding id"). `Retriever.reload` reopens with `get_collection(fresh=True)`.
- Section names come from each document's table of contents (`DocSpec.sections`), located in reading order. Never guess them with a regex: table rows look like headings.
