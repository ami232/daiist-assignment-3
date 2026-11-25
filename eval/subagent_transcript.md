# Subagent transcript: corpus-researcher in Claude Code

Session run in Claude Code on 2026-11-25, in this repository. `.mcp.json` starts `server.py` as the
`corpus` MCP server; `.claude/agents/corpus-researcher.md` defines the subagent with only
`mcp__corpus__search`. Extracted from the Claude Code session log (the subagent's own messages and tool
calls; result passages shortened to their headers).

**User → Claude Code**

```
Use the corpus-researcher subagent to answer: My flight from Madrid to Lisbon was cancelled 3 days before departure. What compensation can I get?
```

**Claude Code → corpus-researcher** (delegation)

```
My flight from Madrid to Lisbon was cancelled 3 days before departure. What compensation can I get?
```

**corpus-researcher → mcp__corpus__search** (two calls, in parallel)

```
search(query="compensation for cancellation informed less than two weeks before departure re-routing conditions")
  [1] source_id: reg_261_2004 | location: Article 5 (part 1/2)
  [2] source_id: guidelines_261_2004 | location: Section 4.4.12
  [3] source_id: guidelines_261_2004 | location: Section 4.4.3 to Section 4.4.4
  [4] source_id: guidelines_261_2004 | location: Section 4.4.13
  [5] source_id: guidelines_261_2004 | location: Section 4.4.6

search(query="amount of compensation 250 euros flights 1500 km or less")
  [1] source_id: reg_261_2004 | location: Article 7
  [2] source_id: guidelines_261_2004 | location: Section 4.4.3 to Section 4.4.4
  [3] source_id: guidelines_261_2004 | location: Section 4.4.5
  [4] source_id: reg_261_2004 | location: Article 5 (part 1/2)
  [5] source_id: guidelines_261_2004 | location: Section 4.4.10
```

**corpus-researcher → Claude Code** (final answer)

```
You were told 3 days before departure, which is less than 7 days. So you are entitled to compensation unless one of the exceptions below applies [reg_261_2004, Article 5].

**Amount:** 250 euros for flights of 1 500 km or less [reg_261_2004, Article 7]. My sources do not give the Madrid–Lisbon distance. It is measured by the great circle route method [reg_261_2004, Article 7].

**What can remove or reduce it:**
- **Alternative flight within the limits:** you lose the right if the airline offered you a new flight that left no more than 1 hour before your original departure time and arrived less than 2 hours after your original arrival time [reg_261_2004, Article 5]. Compensation is still due if the new flight arrived more than 2 but less than 3 hours late [guidelines_261_2004, Section 4.4.13].
- **50 % reduction:** for a flight of 1 500 km or less, the airline may halve the amount if the new flight arrives no more than 2 hours late [reg_261_2004, Article 7].
- **Extraordinary circumstances:** the airline owes nothing if it proves the cancellation was caused by extraordinary circumstances it could not have avoided even with all reasonable measures [reg_261_2004, Article 5]. Whether that applies depends on the cause, which only the airline can show.

You are also entitled to assistance [reg_261_2004, Article 5]. Payment is in cash or by bank transfer, bank order or cheque. Vouchers are allowed only if you sign your agreement [reg_261_2004, Article 7].
```

Citation check (same rule as agent.py): every cited pair (reg_261_2004 Article 5, Article 7;
guidelines_261_2004 Section 4.4.13) is among the passages the two searches returned.
