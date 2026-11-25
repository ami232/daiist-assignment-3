# Judge rubric

You grade one answer from a question-answering assistant. The assistant answers only from four NIST publications: AI 100-1, AI 600-1, SP 800-61r3 and SP 800-218. You are given:
- the question;
- its kind: `single`, `multi` (needs two passages) or `unanswerable`;
- a reference answer, written by a person;
- the assistant's answer;
- the passages the assistant retrieved (the evidence).

Return two grades, each 0 or 1, and a one-sentence reason. Decide `supported` first, using only the passages, and then decide `correct` against the reference. Ignore citation formatting, answer length and tone.

## supported
1 if every factual claim in the answer can be found in the retrieved passages. Paraphrase is fine.
- 0 if any claim adds facts that are not in the passages, even if they are true. Typical examples: a list item, a number, a version, or a requirement from another standard.
- 0 if the answer states how strongly something is asked for differently from the passages (for example "must" where a passage says "consider", or a different priority level). Neutral restatements ("organizations should…") are fine.
- 0 for statements that an organization is compliant, or for legal conclusions.
- A correct refusal that makes no claims scores 1.
- Do not use your own knowledge of these documents. Judge only against the passages shown.
- Citations have the form [doc_id, location]. If a claim cites a passage that does not contain it, write CITATION-MISMATCH in the reason. This does not change the grade.
- If the answer is partly supported, `supported` is 0, and the reason names the unsupported claim.

## correct
1 if the answer is right against the reference answer.
- **single:** states the reference's key facts. Wording may differ, and extra true details are fine, except in lists (see below).
- **lists:** when the question asks for a list (functions, risks, characteristics, controls, groups), the answer's list must match the reference. A missing item or an extra item scores 0.
- **multi:** covers both parts of the reference. Getting only one part right scores 0.
- **unanswerable:** says the documents do not contain the answer (for example, starts with "I don't know based on the indexed documents.") and does not answer from general knowledge. Pointing to related passages from the retrieved text, with citations, is fine.
- **a refusal followed by an answer from memory:** if the answer says it does not know and then answers from general knowledge (for example "however, X is typically..."), both `correct` and `supported` are 0.
- **an answerable question that was refused:** `correct` is 0. In the reason, write RETRIEVAL-MISS if the retrieved passages did not contain the answer, or WRONG-REFUSAL if they did.
- **obligation strength:** misstating how strongly something is asked for makes `correct` 0. Examples: recommendation vs consideration, the priority level, a suggested action vs a requirement, an example vs a task. Neutral restatements ("the action is to…", "organizations should…") are fine; only an explicit upgrade or downgrade (must/required/mandatory vs consider/suggested/example) counts.
- **wrong details:** an answer that contradicts the reference, or picks the wrong identifier, priority, number or list item, scores 0.
- **a "moved" entry:** when the reference says an entry has no requirement of its own (for example a "moved" SSDF task), the answer must say so, and name where it moved if the reference does.
- **equivalent forms:** accept "12" for "Twelve", "Valid & Reliable" for "valid and reliable", and an identifier with or without its title. Stay strict on the identifiers themselves.

## PARTIAL
If the answer is honest but incomplete (it answers the part it can support and says what it could not find), `correct` is 0 and the reason starts with "PARTIAL:". Do not use PARTIAL for answers that are wrong or that present themselves as complete.

## Calibration
- Be strict about identifiers and numbers: "RS.MA-03" is not "RS.MA-02".
- Do not reward length or confident tone.