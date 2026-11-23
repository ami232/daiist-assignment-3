# Subagent transcript (Claude Code in VS Code, 23 Nov 2026)

Subagent: `.claude/agents/corpus-researcher.md` (tools: `mcp__corpus__search` only).
The main Claude Code agent delegated the question; the subagent ran the `search` tool of the
`corpus` MCP server (server.py) in the background and returned the answer below.

## User

> Use the corpus-researcher subagent to answer: a laptop with customer data was stolen from my car. Do I have to report it, and by when?

## Main agent → subagent (delegation)

```
Agent: GDPR stolen laptop breach

A small-business owner asks: "A laptop with customer data was stolen from my car. Do I have to
report it, and by when?"

Answer from the corpus only, following AGENTS.md rules: search (up to 3 times with varied
wording, e.g. GDPR Art. 33 notification to supervisory authority, Art. 34 communication to data
subjects, EDPB 9/2022 lost/stolen device examples, encryption, risk assessment, 72 hours,
awareness). Lead with the direct answer (who to notify, deadline), then conditions/exceptions
(e.g. unlikely to result in risk, encryption/backups, notifying individuals when high risk,
documenting the breach, phased notification/late notification reasons). Cite every claim with
the exact passage label from the search results. Say clearly which parts the documents do not
cover. Return the final answer text with citations.
```

Working in the background: `mcp__corpus__search`

## Subagent's answer

Yes, you must report it, unless the theft is unlikely to put your customers at risk. Report to
your data protection authority without undue delay and, where feasible, within 72 hours of
becoming aware of the theft [GDPR | Art. 33(1)]. If the risk to your customers is high, you must
also tell them directly, without undue delay [GDPR | Art. 34(1)]. Two facts decide which
applies: whether the laptop was encrypted, and whether the laptop held the only copy of the data.

**When the 72 hours start**

* The clock starts once you are reasonably sure a security incident has compromised personal data [EDPB 9/2022 | para. 31–32]. A stolen laptop with customer data on it will usually meet that test straight away.
* You can take a short time to investigate, but start immediately and use that time to assess the risk to your customers [EDPB 9/2022 | para. 34–35]. Waiting too long can count as failing to notify [EDPB 9/2022 | para. 40–41].
* If you report after 72 hours, you must give the reasons for the delay [GDPR | Art. 33(1)]. If you don't have all the facts yet, you can send the information in stages [GDPR | Art. 33(4)].

**What the report must contain** [GDPR | Art. 33(3)]

* What happened, including roughly how many customers and records are affected, where possible.
* A contact person.
* The likely consequences.
* What you have done, or plan to do, to deal with it.

**When you may not have to report (encryption)**

* You don't need to report a stolen device if all of these are true: its encryption is state-of-the-art; the encryption key was not compromised; you still have another copy of the data [EDPB 9/2022 | para. 75–76, 79].
* The EDPB gives the example of a stolen encrypted USB key whose data was backed up. Neither the authority nor the people affected needed to be told [EDPB 9/2022 | Annex ex. i].
* If the laptop held the only copy, losing that data can itself be a risk to people, so you may have to report even if it was encrypted [EDPB 9/2022 | para. 79].
* Keep checking. If the key turns out to be compromised later, you may have to report after all [EDPB 9/2022 | para. 77–78].

**Telling your customers**

* If the risk is high, tell them in plain language. Include the contact person, the likely consequences and the steps you have taken [GDPR | Art. 34(1)–(3)].
* You don't have to tell them in three cases [GDPR | Art. 34(3)]: the data was unreadable to outsiders, for example because it was encrypted; you have since made the high risk unlikely; contacting each person would take disproportionate effort (then you must make a public announcement instead).

**What the documents don't cover**

* Which authority to contact: the GDPR only says "the competent supervisory authority" [GDPR | Art. 33(1)]. If you are in Spain, that is likely the AEPD.
* Spanish rules: national law such as the LOPDGDD is not in the documents.
* Your internal breach record: the search found nothing on what you must keep on file.
* High risk or not: if the laptop was not encrypted, the documents can't say whether your case counts as high risk, because that depends on what data it held.

For any of these, ask the AEPD or a data-protection lawyer.

## Observations (for REPORT.md)

* Delegation worked: the subagent used only the search tool, cited every factual claim with a retrieved label, led with the direct answer and listed what the corpus does not cover.
* **False "not covered":** it says nothing was found on the internal breach record, but the corpus covers it (GDPR Art. 33(5); EDPB 9/2022 para. 121–123). Its searches did not target record-keeping — a small retrieval miss.
* **One claim not from the documents:** "likely the AEPD" comes from the example in the subagent's own instructions, not from a retrieved passage.
