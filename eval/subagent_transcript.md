# Subagent transcript (Claude Code, 2026-11-20)

Subagent: `.claude/agents/corpus-researcher.md` (tools: `mcp__corpus__search` only). Test question q25.

## User

> Use the corpus-researcher subagent to answer: Is an AI tool that grades students' exams considered high-risk?

## Delegation (prompt written by the main agent for the subagent)

> Question: Under the EU AI Act (Regulation 2024/1689), is an AI system that grades/evaluates students' exams classified as high-risk?
>
> Use mcp__corpus__search (it indexes GDPR, AI Act, Data Act binding articles and annexes, no recitals). Search several phrasings, e.g.: "Annex III education and vocational training high-risk AI systems", "AI systems used to evaluate learning outcomes", "Article 6 classification rules for high-risk AI systems", "Article 6(3) exceptions not high-risk narrow procedural task", and if relevant "obligations of deployers of high-risk AI systems".
>
> Report back:
> 1. The direct answer (yes/no/with conditions).
> 2. The exact provisions that support it, citing as '<regulation> <location>' (e.g. 'AI Act Annex III point 3(b)'), with short verbatim quotes of the key wording.
> 3. Any exceptions (e.g. Article 6(3)) that could take such a tool out of high-risk, and their conditions (including the profiling caveat).
> 4. Briefly, the main consequences if it is high-risk (key obligations), only if the corpus returns them.
> Only state what the retrieved passages support; if something isn't in the results, say so. Do not invent citations.

## Answer (main agent, from the subagent's report)

Yes. Under the AI Act, an AI tool that grades students' exams is high-risk by default. It can escape that only through a narrow exception, and the exception is never available if the tool profiles students.

**Why it's high-risk**

- AI Act Annex III, point 3(b) lists "AI systems intended to be used to evaluate learning outcomes, including when those outcomes are used to steer the learning process of natural persons in educational and vocational training institutions at all levels."
- AI Act Article 6(2) says "AI systems referred to in Annex III shall be considered to be high-risk."
- If the tool also proctors exams, Annex III point 3(d) covers it too ("monitoring and detecting prohibited behaviour of students during tests").

**The exception (AI Act Article 6(3))**

An Annex III system is not high-risk if it "does not pose a significant risk of harm… including by not materially influencing the outcome of decision making." It must also meet at least one of these conditions:

- (a) it does a narrow procedural task;
- (b) it improves the result of work a human has already completed;
- (c) it detects patterns or deviations in past decisions, without replacing or influencing a human assessment without proper human review;
- (d) it does a preparatory task before an assessment.

The exception is lost whenever the system "performs profiling of natural persons", in which case it is "always" high-risk.

- A tool that sets or materially influences the grade almost certainly doesn't fit the exception. The subagent said this is its reading of the text, not something a passage states outright.
- A tool that only pre-sorts answers before a teacher grades them might fit, as long as it doesn't profile students.
- A provider who relies on the exception must document its assessment before release and still register the system (AI Act Article 6(4), referring to Article 49(2)).

**What being high-risk means in practice**

- Providers (AI Act Article 16) need a quality management system, documentation and logs, a conformity assessment, an EU declaration of conformity, CE marking and registration.
- Deployers such as schools (AI Act Article 26) must use the tool according to its instructions, give human oversight to trained staff who have the authority to act, monitor how the tool runs and report serious incidents, and tell students the high-risk system is being used on them (Article 26(11)).

**Limits of this answer**

- The corpus doesn't include the Commission's Article 6(5) guidelines, which were due by 2 February 2026 and give practical examples of what is and isn't high-risk.
- The subagent didn't retrieve the detailed requirements in Section 2 of the AI Act's chapter on high-risk systems.
- It didn't check how the GDPR's rules on automated decision-making apply to students.
- For a specific product, the classification should be confirmed by a lawyer.

## Subagent's own tool calls

From `/tasks` (corpus-researcher, spawned by the main agent, finished in 22 s, 16.1k tokens). Five tool calls: four searches (the only tool it has) and the hand-back of its report.

| # | Tool | Query (as shown, truncated by the UI) |
|---|---|---|
| 1 | corpus search | "Annex III education and vocational train…" |
| 2 | corpus search | "Article 6 classification rules for high-…" |
| 3 | corpus search | "Article 6(3) AI system not high-risk nar…" |
| 4 | corpus search | "obligations of deployers of high-risk AI…" |
| 5 | SubagentHandback | report returned to the main agent |

Expected passages for q25: AI Act Article 6(2) and Annex III point 3. Both were retrieved and cited.
