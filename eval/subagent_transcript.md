# Subagent run: corpus-researcher in VS Code (GitHub Copilot, Agent mode)

12 Nov 2026. MCP server `corpus` started from `.vscode/mcp.json`. Subagent defined in `.claude/agents/corpus-researcher.md`.

**Prompt:**

> Use the corpus-researcher subagent to answer: What could go wrong with Saia's expansion plans?

**Transcript (copied from the Copilot chat):**

```
Search Tools

search
Completed with input: {
  "company": "SAIA",
  "query": "What risks could threaten or delay Saia's expansion plans, including opening new terminals, ramping capacity, costs, execution, competition and demand?"
}

Delegated task

Search for `^\[SAIA 10-K 2025|terminal|expansion|profitable|employees|labor|capital`

Read , lines 1 to 12
Completed with input: {
  "path": "/var/folders/f3/swbrcshn3cv8dppsdmc5jz3m0000gn/T/1794493231487-copilot-tool-output-5e324468560044e3bac9621277295b3e.txt",
  "view_range": [
    1,
    12
  ]
}
```

**Answer:**

Saia’s 2025 10-K flags several risks to its expansion plans:

- New terminals or markets may not open as planned or become profitable, while requiring significant investment in facilities, equipment, technology, staff, and startup costs. [SAIA 10-K 2025, Item 1A > Business and Operational Risks]
- Expansion costs may arrive before the additional revenue; higher-than-expected costs or lower revenues could depress profitability and strain liquidity and cash flows. [SAIA 10-K 2025, Item 1A > Business and Operational Risks]
- Growth could disrupt existing operations or customer service, and divert management attention from running the business. [SAIA 10-K 2025, Item 1A > Business and Operational Risks]
- Real-estate shortages, permitting delays, equipment supply disruptions, or increased union-organizing risk could add costs or limit capacity and expansion. [SAIA 10-K 2025, Item 1A > Business and Operational Risks]

**Notes:**

- The task was delegated ("Delegated task") and the corpus `search` tool was called with `company: SAIA`.
- After the search, Copilot also ran a text search and a file read on its own temporary copy of the search result. The `tools: mcp__corpus__search` line in the subagent file uses Claude Code's tool naming, so VS Code may not have limited the subagent to that one tool.
- Every claim is cited to Saia's Item 1A. No figures were given.
