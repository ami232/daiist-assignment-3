# Adding a document: before and after

Unanswerable question u01, document added: `docs_to_add/apixaban.json` (FDA label for apixaban, openFDA, public domain).

## 1. Before adding the document

**Question:** What is the recommended dose of apixaban for non-valvular atrial fibrillation?

**Tool calls:**
- `search({'query': 'apixaban dose non-valvular atrial fibrillation'})` -> [warfarin:dosage_and_administration:4] Source: Warfarin FDA drug label (warfarin.json) | Section: Dosage and Administration

**Answer:**

> The corpus does not cover this. I looked for the recommended dose of apixaban for non-valvular atrial fibrillation, but the available documents only contain information regarding warfarin. Please consult the official FDA label for apixaban or speak with a pharmacist.

(3869 tokens, 3.5 s)

## 2. Add request without approval (guardrail)

**Question:** Please add the document docs_to_add/apixaban.json to the corpus.

**Tool calls:**
- `add_document({'path': 'docs_to_add/apixaban.json'})` -> Not added: the user did not approve adding this document.

**Answer:**

> The document was not added because I am only authorized to add documents when explicitly instructed to do so, and I require confirmation to proceed. Please confirm if you would like me to add `docs_to_add/apixaban.json` to the corpus.

(2310 tokens, 3.58 s)

## 3. Add request, approved by a person in the terminal

**Question:** Please add the document docs_to_add/apixaban.json to the corpus.

**Tool calls:**
- `add_document({'path': 'docs_to_add/apixaban.json'})` -> Added 'apixaban' from apixaban.json: 105 chunks, 18608 words.

**Answer:**

> The document for apixaban has been successfully added to the corpus.

(2286 tokens, 81.74 s)

## 4. Adding the same file again

`add_document('docs_to_add/apixaban.json')` -> Already indexed: 'apixaban' (105 chunks) has the same content. Nothing changed.

## 5. After adding the document

**Question:** What is the recommended dose of apixaban for non-valvular atrial fibrillation?

**Tool calls:**
- `search({'query': 'apixaban recommended dose non-valvular atrial fibrillation'})` -> [apixaban:dosage_and_administration:1] Source: Apixaban FDA drug label (apixaban.json) | Section: Dosage and Administration

**Answer:**

> The recommended dose of apixaban for most patients with non-valvular atrial fibrillation is 5 mg orally twice daily [apixaban:dosage_and_administration:1, apixaban:dosage_and_administration:5]. The recommended dose is 2.5 mg orally twice daily for patients who have at least two of the following characteristics: age greater than or equal to 80 years, body weight less than or equal to 60 kg, or serum creatinine greater than or equal to 1.5 mg/dL [apixaban:dosage_and_administration:1, apixaban:dosage_and_administration:5]. Please consult the prescriber or pharmacist to confirm the appropriate dose for a specific patient.

(4165 tokens, 196.65 s)
