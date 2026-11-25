# Retrieval evaluation

32 answerable questions (25 single, 7 multi). Multi (all) = every expected passage within top k; (any) = at least one. Exact = a chunk covers the expected Rn./§. Holding = that, or the expected judgment's Leitsatz (statute targets: exact only).

| Design | k | Exact: overall | single | multi all | multi any | Holding: overall | single | multi all | multi any | Words added |
|---|---|---|---|---|---|---|---|---|---|---|
| A baseline (EN → dense) | 1 | 9% | 12% | 0% | 0% | 59% | 76% | 0% | 71% | 153 |
| A baseline (EN → dense) | 3 | 25% | 32% | 0% | 0% | 78% | 92% | 29% | 100% | 683 |
| A baseline (EN → dense) | 5 | 41% | 52% | 0% | 14% | 81% | 96% | 29% | 100% | 1242 |
| B translated (DE → dense) | 1 | 6% | 8% | 0% | 0% | 59% | 76% | 0% | 86% | 165 |
| B translated (DE → dense) | 3 | 38% | 48% | 0% | 29% | 81% | 96% | 29% | 100% | 745 |
| B translated (DE → dense) | 5 | 62% | 80% | 0% | 57% | 91% | 96% | 71% | 100% | 1344 |
| C hybrid (DE → BM25 + dense, RRF) | 1 | 16% | 20% | 0% | 0% | 50% | 64% | 0% | 14% | 260 |
| C hybrid (DE → BM25 + dense, RRF) | 3 | 53% | 68% | 0% | 43% | 66% | 84% | 0% | 86% | 881 |
| C hybrid (DE → BM25 + dense, RRF) | 5 | 66% | 84% | 0% | 86% | 72% | 88% | 14% | 100% | 1564 |
| D hybrid, max 2 chunks/doc | 1 | 16% | 20% | 0% | 0% | 50% | 64% | 0% | 14% | 260 |
| D hybrid, max 2 chunks/doc | 3 | 44% | 56% | 0% | 14% | 69% | 84% | 14% | 43% | 886 |
| D hybrid, max 2 chunks/doc | 5 | 44% | 56% | 0% | 57% | 72% | 84% | 29% | 71% | 1521 |

Chosen design: B at k=5 (retrieval.DEFAULT_DESIGN), on the holding metric: the agent can answer and cite from a judgment's Leitsatz, and B leads there with fewer words than C. A, C and D are kept as compared designs.

Translation step (B, C): gemini-3.8-flash, avg 190 input + 79 output tokens, avg 2.7 s (max 5.3 s) per question, measured on the first uncached call. BM25 + RRF run locally (milliseconds).
