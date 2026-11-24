# Ship decision (my answers, 23 Nov 2026)

**Would I let tenants rely on it?** Not yet: fix first, then release (option c).

**For what (once fixed):**
- Finding which article of the law covers their problem.
- A first explanation before talking to a lawyer or the regional housing office.

Not for final decisions (stopping rent payments, leaving the flat, keeping or claiming a deposit).

**Safeguards:**
1. Grounding fix: every condition and citation in an answer must appear in a retrieved passage.
2. Show the article text and the BOE link next to every answer.
3. Disclaimer: not legal advice; confirm with a lawyer or the regional housing office.
4. Keep the corpus updated when the law changes.
5. Force a second search before the agent refuses.
6. My own: re-run the 35-question test after every fix and every corpus update.

**Why:** because it finds the right article every time, but about 1 in 9 answers adds a condition the law doesn't support, and in q04/q25 that condition was about leaving the flat, which is exactly the kind of decision that costs a tenant money.

## Numbers behind it (final run, 23 Nov 2026 corpus)

| | |
|---|---|
| Right conclusion (judge, after my review) | 34/35 (33/35 with the original q20) |
| Nothing made up | 31/35 |
| Correct refusals / wrong refusals | 6/6 · 0/29 (1/29 with the original q20) |
| Expected article retrieved by the agent | 29/29 |
| Tokens per question | ~6,430 (6,150 input + 280 output) |
| Cost per question | $0 on the free tier; ≈ $0.0025 at standard gemini-3.5-flash-lite prices ($0.30 / $2.50 per 1M input / output tokens) |
| Seconds per question | median 36.8, mean 45.2 in the free-tier run (rate-limit retries); about 4–6 s without throttling |
