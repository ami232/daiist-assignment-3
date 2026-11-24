# Retrieval notes (for REPORT.md)

Numbers from `eval/retrieval.csv`, 29 answerable questions (22 single, 7 multi), k up to 5.
Query vectors come from the cache; both hit tests use the same search results.

## Two hit tests

- **Lenient:** a retrieved chunk of the expected document whose locations *include* the expected location.
- **Strict:** a retrieved chunk of the expected document whose *main* location is the expected one. The main location is the article or annex with the most words in the chunk.

For multi questions the main number needs both passages in the top k.

| Design | Mode | Lenient hit@1 | Lenient hit@3 | Lenient hit@5 | Strict hit@1 | Strict hit@3 | Strict hit@5 | Words in prompt at k=5 |
|---|---|---|---|---|---|---|---|---|
| A fixed (250 words, 50 overlap) | vector | 69% | 90% | 97% | 52% | 79% | 86% | 1,237 |
| A fixed | hybrid | 55% | 79% | 90% | 41% | 66% | 76% | 1,237 |
| B structure (one chunk per article or annex part) | vector | 55% | 86% | 97% | 55% | 86% | 97% | 1,394 |
| B structure | hybrid | 48% | 66% | 72% | 48% | 66% | 72% | 1,452 |

Multi questions, both passages in the top 5: A vector 86% lenient and 71% strict; B vector 86% under both tests.

## Choice: design B (structure) with vector search, k = 5

Decision by the author: the strict hit test is the fair one, because design A's lenient hits count chunks that span several articles. A fixed window often covers two or three articles, and under the lenient test it counts as a hit for each of them, even when the expected article is only the tail or the head of the chunk. Design B has one location per chunk, so its numbers are the same under both tests.

- Under the lenient test A vector and B vector tie on hit@5 (97%) and A wins the tie-break on hit@1 (69% against 55%).
- Under the strict test B vector wins outright: 97% against 86% on hit@5, and 55% against 52% on hit@1.
- B adds about 13% more words to the prompt at k=5 (1,394 against 1,237).
- Selection rule in `evaluate.py`: strict test, best hit@5, tie-break hit@1, then fewer words. It writes the choice to `index/config.json`.

## Hybrid search is worse in both designs

BM25 scores word overlap. The test questions are phrased as a bid manager would ask them, not in the wording of the articles, so BM25 alone ranks the expected passage badly (for q05 it is rank 29 of 30, while vector search has it at rank 3). Reciprocal rank fusion gives both rankings the same weight, so the weak BM25 ranking pushes good vector hits out of the top 5. B hybrid finds both passages of a multi question in the top 5 in only 29% of cases.

## Misses at k = 5 with the chosen design

B vector misses one question: q26, where the ESPD form passage (`reg_2016_7 | Annex 2`) is not in the top 5 (the Article 59 passage is at rank 2). Per-question ranks for every configuration are in `eval/retrieval_detail.csv`.
