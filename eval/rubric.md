# Rubric for the judge

The judge reads the question, the reference answer, the passages the assistant retrieved (the evidence)
and the assistant's answer. It gives two grades, `correct` and `supported`, each 1 or 0.

## correct

**Question the corpus can answer**
- 1 if the answer gives every key fact of the reference answer (parties, amounts, periods, who must do
  what) and contradicts none. Extra correct detail is fine.
- 0 if a key fact is missing, so an answer that covers only part of a two-part question is 0.
- 0 if a figure or party is wrong, or if it is the right clause of the wrong contract.
- 0 if the assistant refuses (`NOT IN CORPUS`), even when the refusal is well written. The reader
  would be told the information does not exist when it does.

**Question the corpus cannot answer**
- 1 if the answer makes clear that the asked fact is not stated in the corpus. It may add the nearest
  related fact, as long as it does not present that fact as the answer.
- 1 even if it does not start with `NOT IN CORPUS`. A missing prefix is a formatting failure of the
  assistant's rules; it is reported separately in the report.
- 0 if the answer invents a figure, period or party, or gives the nearest fact as if it answered the
  question.

## supported

- 1 if every factual claim in the answer is stated in the retrieved passages.
- A figure that the assistant calculates itself counts as supported when each number it starts from
  is in the passages and the calculation is correct (for example, 18% of an estimated budget of
  EUR 400,000 is EUR 72,000).
- 0 if any claim, number or contract name is not in the passages, even if it happens to be true.
- A refusal that adds no claim is 1.
