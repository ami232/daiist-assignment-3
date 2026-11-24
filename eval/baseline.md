# Baseline: plain gemini-3.8-flash compared with the agent

Both baselines use the agent's model (gemini-3.8-flash) with no tools, no retrieval and no AGENTS.md. They stand for "asking a general AI".
- **baseline:** gets only the question.
- **baseline with context:** gets the question with "(Germany, residential lease)" appended.

The same judge (gemini-3.1-pro-preview) and the same JUDGE_PROMPT grade all three, and the judge sees the original question. The baselines' passages are given to the judge as none, so "supported" doesn't apply to them and only "correct" is compared. The agent is shown with the judge's grades and with the human labels; the baselines have no human labels.

| | single | multi | unanswerable | all |
|---|---|---|---|---|
| **Correct**, baseline (judge) | 7/25 | 2/7 | 0/7 | 9/39 |
| **Correct**, baseline with context (judge) | 20/25 | 4/7 | 0/7 | 24/39 |
| **Correct**, agent (judge) | 24/25 | 6/7 | 5/7 | 35/39 |
| **Correct**, agent (human labels) | 22/25 | 6/7 | 4/7 | 32/39 |
| Unanswerable refused, baseline (code) | – | – | 0/7 | – |
| Unanswerable refused, baseline with context (code) | – | – | 0/7 | – |
| Unanswerable refused, agent (code) | – | – | 6/7 | – |
| Cites any § or BGH case, baseline (code) | 8/25 | 3/7 | 2/7 | 13/39 |
| Cites any § or BGH case, baseline with context (code) | 25/25 | 7/7 | 5/7 | 37/39 |
| Cites any § or BGH case, agent (code) | 25/25 | 7/7 | 7/7 | 39/39 |

- Cost per question, baseline: 1,798 tokens, 20.6 s on average.
- Cost per question, baseline with context: 2,012 tokens, 28.7 s on average.
- Cost per question, agent: 37,545 tokens, 41.1 s on average.

## BGH case numbers the baselines cite

"In corpus" means one of the 17 indexed judgments. The others were checked by hand against the portal's table of contents, rechtsprechung-im-internet.de's rii-toc.xml with 35,815 BGH decisions dated 2010-01-05 to 2026-11-17 (eval/baseline_case_check.json). A case missing from the table is not proof it doesn't exist: the portal starts in 2010 and doesn't publish every decision.

| case | cited in | in corpus | on the portal | decided | what the baseline claims | actual topic | matches |
|---|---|---|---|---|---|---|---|
| VIII ZR 103/06 | q16 (baseline with context) | no | no (2006, before the portal starts) | unknown | Repeatedly ruled that an on-call caretaker fee is maintenance/management (q16) | Not checkable from local files; no corpus judgment cites it | can't check |
| VIII ZR 107/13 | q07 (baseline with context) | no | yes | 2014-04-09 | Tenant loses the refund claim once the 12-month objection deadline passes (q07) | Summary dismissal for an invented previous-landlord reference; notice to an insolvent tenant (Leitsatz, local portal file) | no |
| VIII ZR 107/20 | q01 (baseline with context), q27 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 115/04 | q17 (baseline with context) | no | no (2004, before the portal starts) | 2004-11-17 (cited in BGH VIII ZR 249/15) | Commercial share must be deducted first (Vorwegabzug) where commercial use raises costs (q17) | Cited in 249/15 for the purpose of the annual statement: the tenant must learn the balance; the Vorwegabzug point can't be confirmed locally | unclear |
| VIII ZR 118/19 | q04 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 137/03 | q31 (baseline with context) | no | no (2004, before the portal starts) | claimed 2004-04-07 | "die Betriebskosten" alone is a valid clause (q31) | Not found. The same date and point match VIII ZR 167/03 (7 April 2004), cited in BGH VIII ZR 137/15, Rn. 11, for referring to Anlage 3 to § 27 II. BV | likely wrong number |
| VIII ZR 137/09 | q31 (baseline), q02 (baseline with context), q31 (baseline with context) | no | yes | 2010-01-13 | Waste management / sorting services are waste disposal costs under § 2 Nr. 8 BetrKV (q02, q31) | Removal of unlawfully dumped bulky waste (Sperrmüll) is a § 2 Nr. 8 waste disposal cost (cited in BGH VIII ZR 117/21 and 230/21) | partly (right category, different facts; the sorting holding is VIII ZR 117/21) |
| VIII ZR 137/15 | q05 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 156/10 | q11 (baseline with context) | no | not found | – | WEG approval of the annual statement is not a precondition for billing the tenant (q11) | Not in the portal table; the corpus holding on this point is VIII ZR 249/15 | not found |
| VIII ZR 202/06 | q05 (baseline) | no | no (2007, before the portal starts) | 2007-06-27 (cited in BGH VIII ZR 137/15, 62/19, 47/25, 117/21) | Landmark ruling that the bare term "Betriebskosten" suffices without listing or citing the statute (q05) | A reference to Anlage 3 to § 27 II. BV or the BetrKV suffices (137/15 Rn. 11); the bare-term holding is VIII ZR 137/15 (2016) | partly (real case, right date, holding attributed one step too far) |
| VIII ZR 202/10 | q29 (baseline with context) | no | yes | 2011-06-29 | Formal vs. substantive validity of a statement for a WEG flat (q29) | Topic not in local files (no local copy, not cited in the corpus) | can't check |
| VIII ZR 209/15 | q07 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 216/15 | q03 (baseline with context) | no | not found | – | Smoke detector rental fees are capital costs and can't be passed on (q03) | Not in the portal table; that holding is VIII ZR 379/20 (2022), in the corpus | not found |
| VIII ZR 220/17 | q08 (baseline with context), q30 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 223/10 | q12 (baseline with context) | no | yes | 2011-04-13 | The WEG manager is not the landlord's vicarious agent (q12) | Topic not in local files; the corpus holding on this point is VIII ZR 249/15 | can't check |
| VIII ZR 227/09 | q18 (baseline with context) | no | yes | 2010-06-23 | A statement is formally valid when it shows only the adjusted total (q18) | Topic not in local files; the corpus holding on this point is VIII ZR 93/15 | can't check |
| VIII ZR 249/15 | q12 (baseline), q29 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 266/14 | q30 (baseline with context) | no | yes | 2015-11-18 | You can't raise the base rent just because the flat turns out bigger (q30) | Rent increases under § 558 use the actual size, subject to the cap (Kappungsgrenze) (Leitsatz, local portal file; cited in BGH VIII ZR 220/17) | partly (right case and topic, holding stated loosely) |
| VIII ZR 268/14 | q19 (baseline with context) | no | not found | – | Landmark ruling that vacancy-driven heat losses can't be passed to remaining tenants (q19) | Not in the portal table; the corpus holdings on vacancy are VIII ZR 151/20 and 9/14 | not found |
| VIII ZR 278/19 | q29 (baseline with context) | no | not found | – | Formal vs. substantive validity of a statement for a WEG flat (q29) | Not in the portal table | not found |
| VIII ZR 340/10 | q10 (baseline with context) | no | yes | 2011-07-06 | A Betriebskostenspiegel alone is usually not enough to prove a breach of the economy principle (q10) | Economy principle; the tenant bears the burden of proving the breach (cited in BGH VIII ZR 230/21 Leitsatz and 117/21) | consistent |
| VIII ZR 36/14 | q25 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 379/11 | q26 (baseline) | no | not found | – | Set the precedent that smoke detector rental can't be passed on (q26) | Not in the portal table; the precedent is VIII ZR 379/20 (2022), in the corpus, so this is likely a garbled 379/20 | not found (likely garbled 379/20) |
| VIII ZR 379/20 | q14 (baseline with context), q26 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 62/19 | q16 (baseline with context) | yes | – | – | – | – | – |
| VIII ZR 93/15 | q18 (baseline), q18 (baseline with context) | yes | – | – | – | – | – |

Out-of-corpus BGH cases the baselines cite: 16. **Exist (9):** 6 are on the portal table of contents, and 3 more are confirmed because a corpus judgment cites them. **Not found (5):** 156/10, 216/15, 268/14, 278/19 and 379/11 carry a year of 2010 or later but are missing from the table. That strongly suggests they are invented, but doesn't prove it. **Can't be checked locally (2):** 103/06 and 137/03 predate the portal. 137/03 is probably a garbled number: its date, 7 April 2004, and its topic match VIII ZR 167/03, which BGH VIII ZR 137/15, Rn. 11 cites. **Topics of the 9 that exist:** 1 consistent with the baseline's claim (340/10), 3 partly matching (137/09, 202/06, 266/14), 1 on a different subject altogether (107/13), and 4 that can't be told from local files. Two of the not-found numbers are cited for the smoke-detector-rental holding of VIII ZR 379/20 in the corpus: 379/11 looks like a garbled version of that number, and 216/15 has no visible link to it. Sources: corpus/raw/bgh_toc/rii-toc.xml, corpus/raw/bgh_screen/ and the corpus judgments' own citations; no API calls.

## Caveats

- **baseline, jurisdiction:** 17 of 39 answers never mention German law (no German, BGB, BetrKV or Betriebskosten): q01, q04, q08, q09, q10, q13, q14, q16, q20, q22, q25, q30, q32, q33, q34, q37, q38.
- **baseline, judge bias:** on 3 answerable question(s) (q15, q25, q29) the judge failed the answer partly because no passages were retrieved, as if it had to refuse. Even if all of these flipped to correct, it would be at 12/39.
- **baseline with context, jurisdiction:** 0 of 39 answers never mention German law (no German, BGB, BetrKV or Betriebskosten).
- **baseline with context, judge bias:** on 3 answerable question(s) (q15, q19, q32) the judge failed the answer partly because no passages were retrieved, as if it had to refuse. Even if all of these flipped to correct, it would be at 27/39.
- **Missing context in the plain baseline:** the questions don't say "Germany", so the plain baseline often answers under UK or US law. The baseline with context removes that excuse, so the gap between it and the agent is the fairer measure of what retrieval adds.
- **Unanswerable questions:** JUDGE_PROMPT passes them only if the answer says the documents don't cover the question. A baseline has no documents, so it can pass only by declining to answer.

## Per question (judge's correct verdict)

| id | kind | baseline | baseline with context | agent | baseline cites § / BGH | baseline with context cites § / BGH |
|---|---|---|---|---|---|---|
| q01 | single | 0 | 1 | 1 | no | yes |
| q02 | single | 0 | 1 | 1 | no | yes |
| q03 | single | 0 | 1 | 1 | no | yes |
| q04 | single | 0 | 1 | 1 | no | yes |
| q05 | single | 1 | 1 | 1 | yes | yes |
| q06 | single | 0 | 1 | 1 | yes | yes |
| q07 | single | 0 | 0 | 1 | yes | yes |
| q08 | single | 0 | 1 | 1 | no | yes |
| q09 | single | 0 | 0 | 1 | no | yes |
| q10 | single | 0 | 1 | 1 | no | yes |
| q11 | single | 0 | 1 | 1 | yes | yes |
| q12 | single | 1 | 1 | 1 | yes | yes |
| q13 | single | 0 | 1 | 1 | no | yes |
| q14 | single | 0 | 1 | 1 | no | yes |
| q15 | single | 0 | 0 | 1 | yes | yes |
| q16 | single | 1 | 1 | 1 | no | yes |
| q17 | single | 0 | 0 | 1 | no | yes |
| q18 | single | 1 | 1 | 1 | yes | yes |
| q19 | single | 0 | 0 | 1 | no | yes |
| q20 | single | 0 | 1 | 1 | no | yes |
| q21 | single | 1 | 1 | 1 | yes | yes |
| q22 | single | 0 | 1 | 1 | no | yes |
| q23 | single | 1 | 1 | 1 | no | yes |
| q24 | single | 1 | 1 | 1 | no | yes |
| q25 | single | 0 | 1 | 0 | no | yes |
| q26 | multi | 1 | 1 | 1 | yes | yes |
| q27 | multi | 0 | 1 | 1 | no | yes |
| q28 | multi | 0 | 0 | 0 | yes | yes |
| q29 | multi | 0 | 1 | 1 | no | yes |
| q30 | multi | 0 | 0 | 1 | no | yes |
| q31 | multi | 1 | 1 | 1 | yes | yes |
| q32 | multi | 0 | 0 | 1 | no | yes |
| q33 | unanswerable | 0 | 0 | 1 | no | yes |
| q34 | unanswerable | 0 | 0 | 0 | no | no |
| q35 | unanswerable | 0 | 0 | 1 | yes | yes |
| q36 | unanswerable | 0 | 0 | 1 | yes | yes |
| q37 | unanswerable | 0 | 0 | 1 | no | yes |
| q38 | unanswerable | 0 | 0 | 0 | no | yes |
| q39 | unanswerable | 0 | 0 | 1 | no | no |

Answers and the judge's reasoning: eval/baseline_answers.jsonl, eval/baseline_context_answers.jsonl
