# Judge rubric, written by María Román in her own words. Lines starting with # are ignored.
# The judge sees: the question, the reference answer, the retrieved passages and the assistant's answer.
# It gives two scores, 0 or 1, and one sentence of reason.

correct = 1 when the answer gives the key facts of the reference answer and does not contradict it.
  A key fact is what the question asks to know. If the answer leaves out something that only adds precision inside that fact, it is a detail and it does not count against the answer.
  For a multi question, there must be a fact from each of the two sources.
  For an unanswerable question, correct = 1 only if the assistant says "I don't know: the corpus does not cover this" (or says the same thing) and gives no substantive answer.

supported = 1 when every claim in the answer is written in the retrieved passages.
  Ignore the reference answer and go sentence by sentence. The only thing to compare with is the retrieved passages.
  If any claim is not written there, supported = 0, even if it is true in the law.
  A refusal claims nothing, so supported = 1.

A hard case: the question asks who to notify of a serious undesirable effect and what goes in the safety report. The answer says whom to notify and what goes in the report, but leaves out the content of the notification (known effects, product name, corrective measures), which is in the reference answer. The question did not ask for that content, so it is a detail and correct = 1. With a strict reading, almost every multi question with a long reference answer would fall to 0, and the same criterion was applied to the other answers.

If the reference answer gives an answer and the assistant says "I don't know", correct = 0, even if the retrieved passages did not contain the answer (supported is still 1, because a refusal claims nothing). The judge decides whether a question has an answer by looking only at the reference answer, not at the passages: a question is unanswerable only when the reference answer is "I don't know: the corpus does not cover this".
