# Judge rubric

You grade one answer from an assistant that answers a financial analyst's questions about the FY2025 Form 10-K reports of Tesla, Ford and GM. You receive the question and its kind (`single`, `multi` or `unanswerable`), the reference answer, the passages the assistant retrieved (the only evidence it had), and the assistant's answer. Grade two criteria, each 1 or 0, on a binary scale.

## Criterion 1: correct

**1 when** the answer correctly answers what the user asked and matches the reference answer in its essentials.
- `single`: it gives the requested figure or fact.
- `multi`: it correctly answers every part of the comparison or analysis.
- `unanswerable`: it correctly recognises that the corpus does not contain the information and does not invent an answer.

**0 when** the answer contains wrong figures, confuses financial concepts, answers only part of a question that needs several figures or companies, or presents a forecast as an actual result. Also 0 when it refuses a question the corpus can answer (a wrong refusal). For `unanswerable` questions, 0 if it invents, estimates or presents as the answer a figure that is not available.

**Borderline cases:**
- Rounding: a rounded figure is correct if it keeps its meaning and reasonable precision. For example, $185.0 billion is correct against $185.019 billion.
- Gross vs. net: incorrect if the confusion changes the meaning of the answer. For example, comparing Ford's $3 billion gross tariff costs with GM's $3.1 billion tariff costs without making clear that they are different measures is not correct.
- `multi` questions: every part must be answered correctly. If the answer gets Ford right but not GM, the score is 0.
- Additional information: not penalised if it is correct, relevant, and does not contradict or change the main answer.
- `unanswerable` questions: the assistant may mention related information that the corpus does contain, as long as it makes clear that it does not answer the requested figure. For example, it may say that it does not have Tesla's CEO total compensation but that the report mentions the 2025 CEO Performance Award.
- Own calculations: a result calculated from corpus figures is accepted if the arithmetic is correct and it answers the question.
- Forecasts vs. actual results: presenting a forecast, estimate or outlook as a result already achieved is incorrect.

## Criterion 2: supported

**1 when** every factual statement in the answer is supported by the retrieved passages. Figures, dates, comparisons and explanations must be justifiable from that evidence. Own calculations are accepted when they are done correctly using only figures supported by the retrieved passages, whether or not they are labelled as derived calculations.

**0 when** at least one relevant factual statement is not supported by the retrieved passages, contradicts the evidence, or brings in information from the model's general knowledge, news or outside sources. Also 0 when the assistant completes an answer with figures that do not appear in the retrieved passages, even if those figures are true according to other sources.

**Borderline cases:**
- Correct statement without a citation: if the statement is supported by the retrieved passages, supported = 1 even without a formal citation. This criterion grades support by the evidence, not citation format.
- Own calculations: supported if every figure used appears in the retrieved passages and the arithmetic is correct. For example, the difference in employees between Ford and Tesla computed from their retrieved figures. A missing "(own calculation ...)" label does not make it 0: like citations, the label is format, not evidence.
- Additional information: any extra statements must also be supported by the retrieved passages. One unsupported additional statement makes the score 0.
- `unanswerable` questions: a clear refusal needs no supporting passage. Any additional information it includes must be supported by the retrieved passages.
- Correct information missing from the passages: even if a statement is true in reality or appears elsewhere in the original report, it is supported = 0 if the retrieved passages do not support it.

Judge only against the reference answer and the retrieved passages shown here, not against your own knowledge of these companies.
