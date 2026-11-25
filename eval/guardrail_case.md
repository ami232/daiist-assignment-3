# Citation guardrail: a case where it fired

Run with `agent.py` (Harness) on 2026-11-25, model gemini-3.5-flash-lite. In the final evaluation the guardrail passed 35/35; it also passed 10 harder probe questions (multi-part, 'answer from memory', user-supplied article numbers). It fired on this question about the assistant itself.

**Question:** Hi! What kinds of questions can you help me with?

**Searches the agent made:**

```text
search(query='scope of Regulation 261 2004 2027 97 1107 2006')
  [1] source_id: reg_261_2004 | location: Article 3 (part 1/2) | similarity: 0.809
  [2] source_id: guidelines_261_2004 | location: Section 2.2.5 to Section 2.2.6 | similarity: 0.809
  [3] source_id: guidelines_261_2004 | location: Section 2.1.1 | similarity: 0.807
  [4] source_id: guidelines_261_2004 | location: Section 2.2.7 (part 1/2) | similarity: 0.797
  [5] source_id: guidelines_261_2004 | location: Section 2.2.1 to Section 2.2.2 (part 1/2) | similarity: 0.796
```

**1. First draft (rejected):**

```text
I can help you with questions about your air passenger rights under EU law. Specifically, I can assist with:

* **Denied boarding, cancellations, and long delays** (including compensation, refunds, re-routing, and your right to care like meals and hotel accommodation) [reg_261_2004, Article 1].
* **Class upgrades and downgrading** [reg_261_2004, Article 10].
* **Airline liability for accidents and for lost, damaged, or delayed baggage** [reg_2027_97, Article 1].
* **Rights of disabled passengers and passengers with reduced mobility** when travelling by air [reg_1107_2006, Article 1].

Feel free to ask about a specific situation you have experienced!
```

**2. Guardrail message sent back to the agent:**

```text
Your answer was rejected by the citation check: these citations are not in the passages you retrieved: [reg_261_2004, Article 1], [reg_261_2004, Article 10], [reg_2027_97, Article 1], [reg_1107_2006, Article 1]. Rewrite it citing only [source_id, section] pairs from your search results, or start with 'I can't answer this from my sources.' if they do not answer the question.
```

**3. Corrected answer (final):**

```text
I can help you with questions about passenger protection in the event of denied boarding, cancellation, delay, upgrading, and downgrading [guidelines_261_2004, Section 2.2.5], as well as questions regarding the geographical scope of these rules for flights departing from EU or non-EU airports [guidelines_261_2004, Section 2.1.1] and travel on scheduled or package tours [guidelines_261_2004, Section 2.2.7].
```

Guardrail status: `corrected`; 1 search, 3 model calls, 7322+337 tokens, 11.1 s.
