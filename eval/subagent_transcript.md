# Subagent transcript (Claude Code, `corpus-researcher` with the `corpus` MCP server)

Run with Claude Code 2.1.332 in this repository: `claude -p "<question>" --mcp-config .mcp.json --allowedTools mcp__corpus__search Agent`.

**User:** Use the corpus-researcher agent: our county just got a Snow Squall Warning. What does it mean and when does the NWS issue one?

**Claude Code → corpus-researcher (delegation prompt):** A county emergency manager's county just received a Snow Squall Warning. Answer from the corpus only: (1) What does a Snow Squall Warning mean (what hazard, what conditions)? (2) When/under what criteria does the NWS issue one (e.g., visibility, wind, temperature/flash freeze criteria, duration, whether criteria are national or local/regional, how it is issued — e.g., polygon/storm-based, lead time, valid duration)? Also note whether there is a Snow Squall Watch or Advisory, and how it relates to Blizzard Warnings if the corpus says. Search multiple phrasings (e.g., "snow squall warning", "snow squall criteria", "whiteout visibility", "flash freeze", "Storm Data snow squall"). Cite every claim exactly as the search tool shows the citation, e.g. [NWSI-10-513, section 6.3, p. 7]. If newer and older documents disagree, prefer the newest and say so. If something isn't covered, say explicitly what is missing. Return a concise answer plus the verbatim citations.

- `mcp__corpus__search` query: "snow squall warning"
- `mcp__corpus__search` query: "snow squall criteria visibility flash freeze"
- `mcp__corpus__search` query: "Storm Data snow squall event definition"
  - first result: `[1] (NWSI-10-513, section App-A, pp. 32-33)`
  - first result: `[1] (NWSI-10-513, section App-A, pp. 32-33)`
  - first result: `[1] (NWSI-10-513, section 7.2.1, p. 19)`
- `mcp__corpus__search` query: "snow squall warning valid time duration polygon storm-based"
  - first result: `[1] (NWSI-10-513, section App-A, pp. 32-33)`
- `mcp__corpus__search` query: "snow squall watch advisory no watch product"
  - first result: `[1] (NWSI-10-513, section App-A, pp. 32-33)`
- `mcp__corpus__search` query: "SQW format technical description segment tags"
  - first result: `[1] (NWSI-10-513, section 7.2.5, p. 19)`
- `mcp__corpus__search` query: "SQW universal geographic code county form 7.3.1"
  - first result: `[1] (NWSI-10-513, section 7.3.1, p. 20)`
- `mcp__corpus__search` query: "blizzard warning criteria sustained winds visibility 3 hours"
  - first result: `[1] (NWSI-10-513, section App-B, p. 35)`
- `mcp__corpus__search` query: "Snow Squall Warnings may be issued during Winter Weather Advisories if conditions are expected to worsen during a brief"
  - first result: `[1] (NWSI-10-513, section App-A, pp. 32-33)`
- `mcp__corpus__search` query: "snow squall safety drivers whiteout brief intense snow"
  - first result: `[1] (NWSI-10-513, section App-A, pp. 32-33)`

**Final answer:**

A Snow Squall Warning means a short, intense burst of moderate to heavy snow with gusty winds is expected, causing sudden whiteouts [NWSI-10-513, section 7, p. 19]. Snow squalls move fast and usually last less than an hour. They rarely leave much snow, but the sudden loss of visibility, gusty winds and falling temperatures can make driving "extremely dangerous" [NWSI-10-513, section App-B, p. 36].

**When the NWS issues one:** the local office issues it when radar, satellite or reliable reports (such as DOTs or webcams) show a squall meeting at least one of two conditions [NWSI-10-513, section 7.2.1, p. 19]:
- visibility of 1/4 mile or less in snow, with road temperatures below freezing; or
- temperatures dropping fast enough to cause a flash freeze, with a significant drop in visibility from falling or blowing snow.

These criteria come from the national directive. The directive sets no wind-speed threshold. Forecasters also weigh time of day and other societal factors, and they may issue a Special Weather Statement instead when they expect lesser impacts [NWSI-10-513, section 7.2.1, p. 19].

**How the warning works:**
- **Timing:** it is issued as events happen and is valid for only 30 to 60 minutes. If the squall continues, the office issues a new warning [NWSI-10-513, section 7.2.3, p. 19].
- **Area:** it covers a drawn area along the squall's path and includes the squall's location and motion [NWSI-10-513, section 7.3.5, pp. 21-22]. It may also give highway mile markers and expected arrival times along the path [NWSI-10-513, section 7.3.3, p. 20].
- **Severity:** check the IMPACT line. "General" means "Travel will become difficult and potentially dangerous within minutes." "Significant" means "Dangerous and life-threatening travel conditions are expected to develop rapidly in the warning area." Only "Significant" warnings send Wireless Emergency Alerts to phones [NWSI-10-513, section 7.3.5, pp. 21-22].
- **Source:** "RADAR INDICATED" means the squall is not yet confirmed. "OBSERVED" means spotters, webcams or other reports have confirmed it [NWSI-10-513, section 7.3.4, p. 21].
- **Blizzard Warnings:** it is not the same as a Blizzard Warning, which requires blizzard conditions for 3 or more hours [NWSI-10-513, section App-B, p. 35]. Snow Squall Warnings are not issued while a Winter Storm or Blizzard Warning is in effect [NWSI-10-513, section 7.3.3, p. 20].

**What the corpus does not cover:** a Snow Squall Watch or Advisory, any stated lead time for the warning, and snow-squall advice from the winter safety guide.

The closing and bus decisions stay with you. The short duration and "Significant" vs. "General" tag in your warning are the key details to check.
