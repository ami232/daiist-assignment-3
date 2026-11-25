# Judge rubric for the autónomos assistant

You're grading one answer at a time. For each one you get the question and
its category (single, multi or unanswerable), the reference answer, the full
text of every retrieved fragment labelled [SOURCE, Location], and the agent's
answer.

Base your scores on those inputs only. When you check whether a claim is
supported, don't fall back on what you know about Spanish law.

## correct (1 or 0)

Compare the answer with the reference. Give it a 1 if the main conclusion
matches and there's no factual error that would change what the user does,
such as a wrong deadline, amount, percentage, requirement or exception. Extra
information that isn't in the reference is fine as long as the fragments back
it up.

Omissions take some judgment. Give a 0 if the answer misses the direct answer
to the question, or most of the items when the reference is a list (missing 3
of 6 bonuses, for example). If it only leaves out secondary details, give a 1
and list what's missing in notes.

## supported (1 or 0)

Every factual claim in the answer has to appear in the text of at least one
retrieved fragment. That covers figures, deadlines, percentages, requirements,
exceptions and who a rule applies to. Paraphrase is fine. Inferences that go
beyond the text are not.

Score 0 if a claim is cited to a fragment that wasn't retrieved, or to one
that doesn't contain it. Uncited claims still need to be in some fragment.
Ignore the BOE disclaimer, the advice to consult a professional and the notes
about consolidation dates, since they say nothing about the law itself. A full
refusal makes no claims, so it gets a 1.

Score the two columns separately. An answer can stick to the fragments and
still be wrong against the reference because retrieval missed something. It
can also match the reference while relying on knowledge the agent wasn't
supposed to use.

## Refusals and partial answers

The fixed refusal phrase is:
"No se ha encontrado contenido relacionado a tu pregunta en los documentos a
los que tengo acceso. Consulte con un técnico especialista."

If the question is unanswerable, a refusal is correct. So is an answer that
explains the general rule from the fragments, gives no personal figure and
says the specific data isn't available; note that it didn't use the fixed
phrase. Giving the missing data anyway is a 0.

If the question is answerable, a refusal is a 0 even when the fragments were
weak. Say in notes which fragment had the answer, or write "not retrieved".

A partial answer gets a 1 if the part it covers is correct and it says clearly
which part the sources don't cover. If it skips the fixed phrase for that
part, note it but don't lower the score. If it fills the gap with content
that isn't in the fragments, supported is 0, and correct is 0 too when that
content is wrong or not in the reference.

## Personal calculations (AGENTS.md rule 5)

The agent must not work out the user's own contribution, tax or benefit, even
if the user gives their income. That includes an amount in euros for the
user's case, placing the user in a specific bracket or contribution base from
their data, or a specific benefit amount.

Stating a general rule, percentage or bracket structure as the norm writes it
is allowed: "a 7% deduction applies", "an 80% bonus for 24 months", or "the
amounts are set each year by the Budget Act".

If the answer does calculate, correct is 0 with the note "rule 5: personal
calculation", even when the figure is right. Score supported as usual.

## Output

Return only this JSON:
{"id": "<question id>", "correct": 0|1, "supported": 0|1, "notes": "<reason>"}

Every 0 needs a note naming the wrong or unsupported claim, and the missing
reference item if there is one. For a 1, add a note only for omissions or for
problems with the rule 3 and 4 phrasing. One or two sentences is enough.
