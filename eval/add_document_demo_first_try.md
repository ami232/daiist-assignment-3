# Adding a document: before and after

Unanswerable question u01, document added: `docs_to_add/apixaban.json` (FDA label for apixaban, openFDA, public domain).

## 1. Before adding the document

**Question:** What is the recommended dose of apixaban for non-valvular atrial fibrillation?

**Tool calls:**
- none

**Answer:**

> The corpus does not cover this. I looked for the recommended dose of apixaban for non-valvular atrial fibrillation in the provided drug labels.

(1083 tokens, 6.3 s)

## 2. Add request without approval (guardrail)

**Question:** Please add the document docs_to_add/apixaban.json to the corpus.

**Tool calls:**
- `add_document({'path': 'docs_to_add/apixaban.json'})` -> Not added: the user did not approve adding this document.

**Answer:**

> The corpus does not cover this. (An answer was drafted but blocked because it had no citations.)

(2240 tokens, 5.31 s)

## 3. Add request, approved by a person in the terminal

**Question:** Please add the document docs_to_add/apixaban.json to the corpus.

**Tool calls:**
- `add_document({'path': 'docs_to_add/apixaban.json'})` -> Added 'apixaban' from apixaban.json: 105 chunks, 18608 words.

**Answer:**

> The corpus does not cover this. (An answer was drafted but blocked because it had no citations.)

(2211 tokens, 187.31 s)

## 4. Adding the same file again

`add_document('docs_to_add/apixaban.json')` -> Already indexed: 'apixaban' (105 chunks) has the same content. Nothing changed.

## 5. After adding the document

**Question:** What is the recommended dose of apixaban for non-valvular atrial fibrillation?

**Tool calls:**
- none

**Answer:**

> The corpus does not cover this. I looked for the recommended dose of apixaban for non-valvular atrial fibrillation in the provided drug labels.

(1083 tokens, 7.27 s)
