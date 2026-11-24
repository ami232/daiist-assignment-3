# Subagent transcript (Claude Code, corpus-researcher)

Run from Claude Code in this repo on 2026-11-21 (`claude -p`, tools allowed: the subagent and `mcp__corpus__search`).

**User:** Use the corpus-researcher subagent to answer this question: My ferry trip was scheduled to take 3 hours but it arrived 2 and a half hours late. What compensation can I ask for?

**Main agent → Agent(corpus-researcher):** "Answer this traveller question using only the corpus (search tool), following the citation format [source, location] copied exactly from the search results: "My ferry trip was scheduled to take 3 hours but it arrived 2 and a half hours late. What compensation can I ask for?" ..."

**corpus-researcher → mcp__corpus__search** `{"query": "sea passenger compensation delay in arrival percentage ticket price"}`
→ `[1] [sea-1177-2010, Article 18] (similarity 0.807) Article 18: Re-routing and reimbursement in the event of cancelled or delayed departures ...` (plus 4 more passages, including `[sea-1177-2010, Article 19]`)

**corpus-researcher → mcp__corpus__search** `{"query": "sea compensation exceptions weather conditions extraordinary circumstances"}`
→ `[1] [sea-1177-2010, Recitals] (similarity 0.781) ...` (plus 4 more passages, including `[sea-1177-2010, Article 20]`)

**corpus-researcher → main agent (2 tool uses, 12,532 tokens, 14 s):** "**50% of the ticket price.** Your journey was scheduled for 3 hours, so it falls in the 'up to 4 hours' band ... Your 2.5-hour delay qualifies for 50% [sea-1177-2010, Article 19]. ..."

**Final answer:**

> You're entitled to **50% of the ticket price.** The corpus-researcher subagent found this in the ferry regulation.
>
> Your trip was scheduled for 3 hours, which puts it in the "up to 4 hours" band. In that band, a delay of at least 1 hour gives you at least 25%. A delay of more than double that (more than 2 hours) gives you 50%. Yours was 2.5 hours, so you get 50% [sea-1177-2010, Article 19].
>
> **Conditions:**
> - The amount is based on the price you actually paid. If you have a return ticket, it's based on half that price [sea-1177-2010, Article 19].
> - The carrier must pay within 1 month of your request. It can pay in vouchers, but must pay in money if you ask for it [sea-1177-2010, Article 19].
> - You get nothing if the carrier proves the delay was caused by weather that put the ship's safe operation at risk, or by extraordinary circumstances that couldn't have been avoided [sea-1177-2010, Article 20].
> - You also get nothing if you were told about the delay before you bought the ticket, or if the delay was your fault [sea-1177-2010, Article 20].

Total: 26 s, USD 0.33 (Claude Code session).
