# add_document demo (q28), 2026-11-18

Run in a terminal with `uv run python main.py ask "..."` on the structural index.
Library `UserWarning` lines about sampling defaults are removed; nothing else is edited.

## 1. Before: question not covered by the corpus

```
> uv run python main.py ask "What risk weight applies under the standardised approach to retail exposures fully secured by residential property?"

The corpus does not cover this question. I searched for the risk weight applicable under the standardised approach to retail exposures fully secured by residential property.

(searches: ['standardised approach retail exposures fully secured by residential property risk weight', 'Article 125 CRR risk weight residential property standardised approach']; tokens in/out: 10393/79; 99.6s)
```

## 2. Adding the document (human approval)

```
> uv run python main.py ask "Please add the document docs/CRR_risk_weights_standardised_approach.xhtml to the corpus"

The agent wants to run add_document with {'path': 'docs/CRR_risk_weights_standardised_approach.xhtml'}.
Approve? [y/N] y
The corpus does not cover this question. I searched for the document addition and corpus status.

(searches: []; tokens in/out: 3671/82; 21.4s; citation guardrail fired)
```

The document was added (the collection went from 983 to 1047 chunks), but the final answer is
wrong: the citation guardrail treated the add-document confirmation as an uncited answer and
pushed the agent into the refusal phrase. Bug: the guardrail must not apply to turns that only
add a document.

That run also exposed an index bug: the 64 new chunks took the collection past 1000 items,
Chroma tried to flush its HNSW files, which fail silently under a non-ASCII path, and dropped
the vectors. After fixing both (citation check skipped on add-only turns; HNSW kept in SQLite
plus a local vector store) and rebuilding the index, steps 2 and 3 were run again on 2026-11-19.

### 2b. Adding the document again, 2026-11-19 (after the fixes)

```
> uv run python main.py ask "Please add the document docs/CRR_risk_weights_standardised_approach.xhtml to the corpus"

The agent wants to run add_document with {'path': 'docs/CRR_risk_weights_standardised_approach.xhtml'}.
Approve? [y/N] y
The document `docs/CRR_risk_weights_standardised_approach.xhtml` has been successfully added to the corpus.

(searches: []; tokens in/out: 2368/55; 206.1s)
```

The structural collection went from 983 to 1047 chunks and reopened intact.

## 3. After: same question

```
> uv run python main.py ask "What risk weight applies under the standardised approach to retail exposures fully secured by residential property?"

Under the standardised approach in the CRR, the risk weight for exposures secured by mortgages on residential property depends on the specific criteria and exposure-to-value (ETV) ratio under Article 125, rather than a single fixed percentage:

1. **General/Loan-Split Approach:**
   - For an exposure secured by residential property as referred to in Article 124(2), point (a)(i) or (ii), the part of the exposure up to **55 % of the property value** shall be assigned a risk weight of **20 %** [CRR, Article 125(1)].
   - The remaining part of the exposure, if any, shall be risk-weighted as an exposure to the counterparty that is not secured by residential property [CRR, Article 125(1)].

2. **Exposure-to-Value (ETV) Bucket Approach:**
   - For exposures as referred to in Article 124(2), point (a)(iii), the exposure shall be assigned the risk weight set in accordance with the respective exposure-to-value risk weight bucket in Table 1 [CRR, Article 125(2)]:
     - **ETV ≤ 50 %:** **30 %** [CRR, Article 125(2)]
     - **50 % < ETV ≤ 60 %:** **35 %** [CRR, Article 125(2)]
     - **60 % < ETV ≤ 80 %:** **45 %** [CRR, Article 125(2)]
     - **80 % < ETV ≤ 90 %:** **60 %** [CRR, Article 125(2)]
     - **90 % < ETV ≤ 100 %:** **75 %** [CRR, Article 125(2)]
     - **ETV > 100 %:** **105 %** [CRR, Article 125(2)]

3. **Derogations and Competent Authority Adjustments:**
   - Where the competent authority or designated authority has set a higher risk weight or a lower percentage of the property value/ETV in accordance with Article 124(9), institutions must use that specific risk weight or percentage [CRR, Article 125(1), Article 125(2)].
   - Under certain conditions regarding national loss rates published pursuant to Article 430a(3), institutions may alternatively apply the 20 % loan-split treatment to exposures secured by residential property situated within that Member State [CRR, Article 125(2)].

This rule comes from the CRR (Regulation (EU) No 575/2013), which is a regulation and applies directly.

(searches: ['retail exposures fully secured by residential property risk weight']; tokens in/out: 4991/838; 143.4s)
```

Checked against the added document: the 20 % up to 55 % of the property value and the Table 1
buckets (30 / 35 / 45 / 60 / 75 / 105 %) match Article 125 literally. The before/after flip
(refusal -> cited answer) comes only from the added document.
