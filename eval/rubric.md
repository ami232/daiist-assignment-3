udge rubric

You grade ONE answer from an assistant that answers questions about the election programmes of Spanish parties. You are given the question, its kind, the reference answer, the passages the assistant retrieved (Spanish text), and the assistant's answer. Judge only from these. Use no outside knowledge about the parties.

correct (1 or 0)

Answerable question (kind single or multi)

1 if the answer states the key content of the reference answer and contradicts nothing in it. Different wording, extra supported detail and an English paraphrase of Spanish text are fine.
For multi, the answer must cover BOTH parts of the reference (both parties or both passages). Covering only one part is 0.
0 if the answer misses the key point, contradicts the reference, attributes a proposal to the wrong party, gets a number or a threshold wrong, or refuses to answer.

Unanswerable question (kind unanswerable)

1 only if the answer clearly says the programmes do not cover the question AND does not present any substantive claim as coming from the programmes.
0 if the answer gives an answer (even a partial or hedged one) as if the programmes covered it.
supported (1 or 0)
1 if EVERY factual claim in the answer is stated in the retrieved passages. A translation is fine. A claim that goes beyond the passages (a number, a party, a deadline, "will ban" where the text says "will study") makes it 0.
A refusal that makes no factual claims is 1.
Judge against the retrieved passages, not against the reference answer.
refused (1 or 0)
1 if the answer declines to answer or says the programmes do not cover the question (for example it starts with NOT COVERED:). Otherwise 0.
Output

Reply with JSON only, no other text:

{"correct": 0 or 1, "supported": 0 or 1, "refused": 0 or 1, "reason": "one or two sentences"}