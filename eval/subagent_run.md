# Subagent run: medication-label-assistant

How this was produced: on 2026-11-25 the main Claude Code agent (working in this repo, with the
`corpus` MCP server from `.mcp.json`) delegated one question to the subagent defined in
`.claude/agents/medication-label-assistant.md`, whose only tool is `mcp__corpus__search`.
Claude Code reported 2 tool uses (search calls), about 19.5 s and 19,223 tokens. The individual
search queries were not visible to the main agent, so they are not shown here. For the report,
also capture your own transcript by asking the subagent yourself in a new Claude Code session.

Every quotation below was checked word for word against the cited label sections
(amiodarone 12.3, digoxin 7.2, amiodarone 7, digoxin 7.3): all found.

**Question:** My father takes Lanoxin (digoxin) and his cardiologist has just added amiodarone.
Does his digoxin dose need to change?

**Subagent's answer (verbatim):**

**Answer:** Yes. Both labels say the digoxin dose usually needs to come down once amiodarone is added, but they give different amounts. The Lanoxin label says to lower the dose by about 30-50% [digoxin 7.2]. The Pacerone label says to cut it in half or stop it [amiodarone 7]. Whether your father's dose changes, and by how much, is for his cardiologist to decide. The labels don't say what is right for a particular patient.

**Evidence:**
- **Why the dose matters:** Amiodarone raises the level of digoxin in the blood. Taken together, it "increases the serum digoxin concentration by 70% after one day" [amiodarone 12.3]. The Lanoxin label also lists amiodarone among drugs that raise digoxin levels by more than 50%, with a 70% rise [digoxin 7.2].
- **What the Lanoxin label says to do:** "Measure serum digoxin concentrations before initiating concomitant drugs. Reduce digoxin concentrations by decreasing dose by approximately 30-50% or by modifying the dosing frequency and continue monitoring." [digoxin 7.2]
- **What the Pacerone label says to do:** "Increased digoxin concentration. Reduce digoxin by half or discontinue. If continued, monitor for evidence of toxicity." [amiodarone 7]
- **The two labels differ:** The Lanoxin label gives a range of about 30-50% and allows changing how often the dose is taken. It also asks for a digoxin blood level before amiodarone is started, and continued checks after [digoxin 7.2]. The Pacerone label says to cut the dose by half or stop digoxin, and to watch for toxicity if it is kept [amiodarone 7]. Both point to a lower dose, but the amounts are not the same.
- **Effect on heart rate:** The Pacerone label also names digoxin as a drug that slows the heart. Together the two drugs can cause "bradycardia, sinus arrest, and AV block," and heart rate should be monitored [amiodarone 7].
- **How long the interaction lasts:** "Because of amiodarone's long half-life, expect drug interactions to persist for weeks to months after discontinuation of amiodarone." [amiodarone 7]
- **Dosing should be individual:** The Lanoxin label says digoxin dosing "should be individualized" when it is taken with drugs that interact with it [digoxin 7.3].

**Limitations:**
- The labels give general guidance. They can't say what your father's new dose should be. That depends on his digoxin blood level, kidney function, heart rate and other medicines, which his cardiologist will weigh.
- My searches did not bring up the signs of digoxin toxicity, so this answer doesn't list what to watch for. His doctor or pharmacist can explain that.
- Label versions used: Lanoxin 2024-12-05 (https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d91e3646-4c63-4512-ab22-db39c085c4dc) and Pacerone 2025-07-14 (https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=4c4ec9b0-13a5-49a8-b57b-b3f64e4316a7).
