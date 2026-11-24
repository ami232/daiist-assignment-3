# add_document demo: q32 before and after

Run on 2026-11-24 with `demo_add_document.py` (agent: `gemini-3.5-flash-lite`). q32 is one of the unanswerable questions of the test set; the held-out report *Electric Car Markets in a Time of Uncertainty* (IEA, July 2026, ECMU2026) answers it.

Documents in the index before: GCMO2026, GEVO2025, GEVO2026. After: ECMU2026, GCMO2026, GEVO2025, GEVO2026.

## 1. Before

**User:** By what percentage did global electric car sales change in the second quarter of 2026 compared with the second quarter of 2025?

- `search("global electric car sales second quarter 2026 2025 growth percentage GEVO2026")` → GEVO2026 p.45, GEVO2026 p.11, GEVO2026 p.11, GEVO2026 p.10, GEVO2026 p.41
- `search("second quarter 2026 global electric car sales growth percentage GEVO2026")` → GEVO2026 p.45, GEVO2026 p.11, GEVO2026 p.11, GEVO2026 p.41, GEVO2026 p.46-47

**Agent:**

> The corpus does not cover the percentage change in global electric car sales for the second quarter of 2026. It does report that global electric car sales in the first quarter of 2026 were 8% lower than over the same period in 2025 (GEVO2026, p. 11).

*2 tool calls, 3 model calls, 9123 tokens, 65.7s, citation check: passed*

## 2. Adding the document (approval asked in the terminal)

**User:** Please add the file corpus/ElectricCarMarketsinaTimeofUncertainty.pdf to the corpus.

- `add_document({"path": "corpus/ElectricCarMarketsinaTimeofUncertainty.pdf"})` → Added ECMU2026 (Electric Car Markets in a Time of Uncertainty): 44 passages from pp. 3-33. The index now holds 366 passages from 4 documents.

**Agent:**

> Answer blocked by the citation check ((ECMU2026, p. 3) was not returned by any search for this question). Check the sources by hand.

*1 tool calls, 3 model calls, 5352 tokens, 118.6s, citation check: blocked*

## 3. After

**User:** By what percentage did global electric car sales change in the second quarter of 2026 compared with the second quarter of 2025?

- `search("global electric car sales second quarter 2026 compared 2025")` → ECMU2026 p.9-10, GEVO2026 p.45, ECMU2026 p.5, ECMU2026 p.10-11, ECMU2026 p.5

**Agent:**

> Global electric car sales grew by 4% year-on-year in the second quarter of 2026 (ECMU2026, p. 9).

*1 tool calls, 2 model calls, 4943 tokens, 10.5s, citation check: passed*
