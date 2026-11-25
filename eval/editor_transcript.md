# Subagent transcript (Claude Code)

Run in Claude Code (desktop app) in this repository, with the `corpus` MCP server from `.mcp.json` and the subagent `.claude/agents/corpus-researcher.md`. The subagent ran 4 tool calls (`mcp__corpus__search`), 19.7k tokens, 19 s.

**User:**

> @agent-corpus-researcher How did the NTSB characterize the role of crew fatigue in Colgan Air Flight 3407 and Asiana Airlines Flight 214? Search each report separately using the corpus search tool. Explain what the NTSB concluded in each case, including any uncertainty, and cite the PDF pages that support your answer.

**Tool calls (in order):**

1. `mcp__corpus__search("Colgan Air 3407 crew fatigue findings")`
2. `mcp__corpus__search("Asiana 214 flight crew fatigue")`
3. `mcp__corpus__search("Asiana 214 probable cause contributing factors fatigue")`
4. `mcp__corpus__search("Colgan Air 3407 probable cause contributing to the accident")`

**Subagent answer:**

**Short answer:** The NTSB treated fatigue differently in the two reports. For Colgan 3407 it found that fatigue likely impaired the pilots, but said it could not determine how much, and fatigue is not part of the probable cause or the contributing factors. For Asiana 214 it found that fatigue likely degraded the crew's performance, and "flight crew fatigue" is listed as contributing factor (5).

**Colgan 3407**
- Finding 24: "The pilots' performance was likely impaired because of fatigue, but the extent of their impairment and the degree to which it contributed to the performance deficiencies that occurred during the flight cannot be conclusively determined." [AAR1001 p.166-167]
- That uncertainty comes from the analysis. The errors "cannot be solely attributed to fatigue" because other explanations exist: another Colgan crew made the same monitoring error 1 month later, and the captain had a history of failures during testing. Even so, fatigue's role "cannot be ruled out." [AAR1001 p.121-122]
- Findings 25-26: the pilots did not manage their rest well because they used an inappropriate facility, and Colgan did not proactively address fatigue hazards at a predominantly commuter base. [AAR1001 p.166-167]
- The probable cause is the captain's inappropriate response to the stick shaker. None of the four contributing factors mentions fatigue. [AAR1001 p.169]
- A Board Member Statement disagrees. Its author argues that fatigue was a factor and that the report "discount[s] it as a contributing factor." This is one member's opinion, not an NTSB finding, and the passage does not name the member. [AAR1001 p.176] [AAR1001 p.180]

**Asiana 214**
- All three pilots were likely fatigued because of circadian disruption. The accident happened during their circadian trough, and the PF had about 5.5 hours of sleep against a reported need of about 7.5. [AAR1401 p.103-104]
- Each pilot's errors "might be attributable, at least in part, to fatigue." The NTSB concludes the crew "was experiencing fatigue, which likely degraded their performance during the approach." [AAR1401 p.104]
- Contributing factor (5) is "flight crew fatigue, which likely degraded their performance." [AAR1401 p.18]
- The NTSB "encourages Asiana to expedite" its fatigue risk management system (FRMS). This is encouragement in the analysis, not a numbered recommendation. [AAR1401 p.104-105]
