# Retrieval scoring rule

Fixed before any measurement. Do not change after seeing results.

## Labels

Each answerable question in `questions.csv` has:

- `expected_location`: the passage(s) that answer it, written as `source:label`
  (e.g. `gdpr:Article 33`). Several passages are separated by `;`.
- `equivalent_locations`: other passages that state the same answer
  (e.g. `gdpr:Recital 85`). They were chosen from the text of the corpus,
  before any retrieval was run.

## Matching

A retrieved chunk matches `source:label` when its source is the same and its
`section` equals the label or is a sub-section of it. `Section 3.1.2` matches
`Section 3.1.2.1`. `Article 8` does not match `Article 80`.

A label starting with `=` is exact: `=edpb_consent:Section 7.1` matches only
Section 7.1 itself, not its sub-sections.
One retrieved chunk can cover at most one required passage.

## Outcome per question at a given k (top-k chunks)

- **single**
  - hit: a chunk matching the expected location is in the top k.
  - equivalent: no expected match, but a chunk matching an equivalent location is.
  - miss: neither.
- **multi** (exactly two required passages)
  - hit: BOTH required passages are in the top k.
  - equivalent: every required passage is covered, but at least one only
    through an equivalent location.
  - miss: at least one required passage is not covered.
  - At k=1 a multi question cannot be a hit, because two passages cannot
    be in one chunk.
- **unanswerable**: not scored for retrieval. It is graded only on whether the
  agent correctly says the documents cannot answer it.

## Metrics

- Strict recall (primary) = hits / answerable questions.
- Lenient recall (secondary, always reported next to it)
  = (hits + equivalents) / answerable questions.
- Reported at k = 1, 3, 5, overall and split by kind (single / multi).

Example: q01 retrieves Recital 85 but not Article 33. That is "equivalent":
a strict miss and a lenient success.

Retrieval is scored separately from answer correctness.

## Multi-question requirements

- q07: required `gdpr:Article 33; edpb_breach:Section II.B.1`
- q09: required `gdpr:Article 8; edpb_consent:Section 7.1.3`,
  equivalent = `=edpb_consent:Section 7.1`


## Clarifications added before the first measurement

- In a multi question, an equivalent location stands in for one specific required
  passage. A prefix `N>` names it (1-based, in the order of `expected_location`),
  e.g. `1>=edpb_consent:Section 7.1` replaces the first required passage. An
  equivalent without a prefix may replace any required passage.
- Designs compared: `dense` (vector search) and `hybrid` (vector search + BM25
  keyword search, merged by reciprocal rank fusion). Any other indexed chunking
  design is also run as dense and hybrid. The constants in `evaluate.py` are not
  tuned after the first run.
  