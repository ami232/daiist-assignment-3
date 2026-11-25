# Before/after and guardrail runs (12 Nov 2026)

Raw terminal output from `main.py ask`, copied for REPORT.md. Only the LangChainBetaWarning lines are removed.
The official evaluation numbers were taken before any of these runs.

## 1. Before: Q3 2026 is not in the corpus

```
$ uv run python main.py ask "How much revenue did Knight-Swift report in Q3 2026?"
  call search({'company': 'KNX', 'query': 'Q3 2026 revenue OR third quarter 2026 revenue'})
  result [KNX 10-K 2025, Item 7 > Non-GAAP Presentation]
Revenue | $364,914 | $387,232 Total operating expenses | 372,554 | 396,690 Impairments 1 | (2,454) | — Ad...

The filings I have do not cover this. I searched the Knight-Swift Transportation (KNX) 2025 Form 10-K, but it only contains annual data for 2025 and prior periods and does not include quarterly data for 2026.

(6.0s, 3663 tokens)
```

## 2. Adding the 10-Q, with the approval step

```
$ uv run python main.py ask "Please add the document corpus/KNX_10-Q_2026-09-30.htm"
  Allow add_document({'path': 'corpus/KNX_10-Q_2026-09-30.htm'})? [y/N] y
  embedded 50/144
  embedded 100/144
  embedded 144/144
  call add_document({'path': 'corpus/KNX_10-Q_2026-09-30.htm'})
  result Added KNX 10-Q 2026-Q3: 144 chunks from Item 2. It is now searchable.

Answer withheld: it contains figures that are not in the retrieved passages (09, 30). Check the filings directly.

(126.7s, 2360 tokens)
```

Guardrail false positive: the confirmation repeated the file's date, and the check only accepted numbers from search results. Fixed in agent.py: numbers from the user's question and the file path they asked to add are now accepted.

## 3. After, first try: guardrail fires

```
$ uv run python main.py ask "How much revenue did Knight-Swift report in Q3 2026?"
  call search({'company': 'KNX', 'query': 'Q3 2026 revenue OR third quarter 2026 revenue'})
  result [KNX 10-Q 2026-Q3, Item 2 > Company Outlook]
Our Company outlook for the fourth quarter of 2026 includes the following:

[KNX 10-Q 2026-Q3, Item 2 > Resu...
  call search({'company': 'KNX', 'query': 'Total revenue $2,200,926 third quarter 2026 table column headers'})
  result [KNX 10-Q 2026-Q3, Item 2 > Non-GAAP Presentation]
Total revenue | $2,200,926 | $1,927,057 | $6,146,861 | $5,613,359 Truckload and LTL fuel surcharge | (...

Answer withheld: it contains figures that are not in the retrieved passages (1852830000, 2200926000). Check the filings directly.

(4.0s, 7507 tokens)
```

The search found the right passage ($2,200,926, in thousands), but the model multiplied it out to $2,200,926,000. Same pattern as q18 and q19 in the evaluation. Fix: rule 3 in AGENTS.md now says to keep the filing's own unit (option A, guardrail unchanged).

## 4. After the rule fix

```
$ uv run python main.py ask "How much revenue did Knight-Swift report in Q3 2026?"
  call search({'company': 'KNX', 'query': 'revenue Q3 2026'})
  result [KNX 10-Q 2026-Q3, Item 2 > Results of Operations — Summary]
Operating Results: Third Quarter 2026 compared to Third Quarter 2025 The $110.4 million incr...

Knight-Swift reported total revenue of $2,200,926 thousand in the third quarter of 2026 [KNX 10-Q 2026-Q3, Item 2 > Key Financial Data and Operating Metrics].

(5.3s, 3384 tokens)
```

```
$ uv run python main.py ask "Which made more revenue in 2025, J.B. Hunt or Knight-Swift?"
  call search({'query': 'total revenue 2025', 'company': 'JBHT'})
  result [JBHT 10-K 2025, Item 7 > Operating Revenue by Segment]
Years Ended December 31, (in millions) 2025 | 2024 JBI | $5,975 | $5,956 DCS | 3,376 | 3,396 ICS ...
  call search({'query': 'total revenue 2025', 'company': 'KNX'})
  result [KNX 10-K 2025, Item 7 > Key Financial Highlights]
During 2025, consolidated total revenue was $7.5 billion, which is a 0.8% increase over 2024. Consolid...

- J.B. Hunt generated total consolidated operating revenues of $12.00 billion ($11,999 million) in 2025 [JBHT 10-K 2025, Item 7 > Consolidated Operating Revenues].
- Knight-Swift reported total revenue of $7,469,689 thousand ($7.5 billion) in 2025 [KNX 10-K 2025, Item 7 > Key Financial Highlights & Consolidating Tables].
- J.B. Hunt made more revenue than Knight-Swift in 2025.

(15.5s, 7142 tokens)
```

```
$ uv run python main.py ask "How much cash did Old Dominion and J.B. Hunt use for investing in 2025?"
  call search({'company': 'ODFL', 'query': 'cash used for investing activities 2025'})
  result [ODFL 10-K 2025, Item 7 > Liquidity and Capital Resources]
A summary of our cash flows is presented below: (In thousands) | 2025 | 2024 Cash and cash equ...
  call search({'query': 'cash used for investing activities 2025', 'company': 'JBHT'})
  result [JBHT 10-K 2025, Item 7 > LIQUIDITY AND CAPITAL RESOURCES]
Net cash provided by operating activities totaled $1.68 billion in 2025, compared to $1.48 bil...

- For Old Dominion, cash flows used in investing activities totaled $366,411 thousand forthe year ended December 31, 2025 [ODFL 10-K 2025, Item 7 > Liquidity and Capital Resources].
- For J.B. Hunt, net cash used in investing activities totaled $575 million for the year ended December 31, 2025 [JBHT 10-K 2025, Item 7 > LIQUIDITY AND CAPITAL RESOURCES].

(12.0s, 7337 tokens)
```

Both questions were withheld by the guardrail in the evaluation run and now pass. The q18 answer still merges two headings into one citation ("Key Financial Highlights & Consolidating Tables").
