# Evaluation summary

Agent model: gemini-3.5-flash-lite. Judge model: gemini-3.1-flash-lite. Questions: 37.

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | multi: both passages in top 5 | words added to prompt (top 5) |
|---|---|---|---|---|---|
| fixed | 73% | 87% | 90% | 80% | 996 |
| article | 77% | 93% | 100% | 80% | 1229 |

## End to end

| outcome | count |
|---|---|
| correct | 28 |
| wrong or unsupported | 2 |
| wrong refusal | 0 |
| correct refusal | 7 |
| answered unanswerable | 0 |

- Code check, citations valid: 37/37
- Code check, refusal when (and only when) expected: 37/37
- Citation guardrail fired: 1 times
- Judge: correct 35/37, supported 36/37
- Cost per question: 3809 tokens, 12.3 s on average

## Judge vs. my own grades

On 20 answers: same 'correct' grade 100%, same 'supported' grade 100%. Disagreements: none.

## Failures (first guess, checked by hand in REPORT.md)

| id | outcome | likely cause |
|---|---|---|
| q17 | wrong or unsupported | wrong answer from right passage |
| q25 | wrong or unsupported | wrong answer from right passage |

## add_document demo

Question: An airline lost my checked suitcase on a flight. What is the maximum compensation the airline must pay?

Before: The corpus does not cover this. The corpus covers rail passenger rights, including luggage rules under train regulations, but does not contain provisions for lost luggage on flights.

add_document: Added 'air-liability-889-2002': 9 chunks embedded and stored. It can now be searched.

Again (already indexed): 'air-liability-889-2002' is already indexed (9 chunks). Nothing was changed.

After: The air carrier is liable for the destruction, loss, or damage to baggage up to a limit of 1,000 SDRs (Special Drawing Rights) [air-liability-889-2002, Article 1]. Passengers can benefit from a higher liability limit by making a special declaration at the latest at check-in and by paying a supplementary fee [air-liability-889-2002, Article 1].
