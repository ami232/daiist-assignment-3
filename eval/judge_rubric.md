# Judge rubric

- correct = 1: All essential information is correct, including numerical thresholds, conditions and exceptions. Paraphrasing is acceptable.
- correct = 0: The response contains factual errors, omits essential conditions, or refuses to answer a question that is answerable.
- supported = 1: All material factual claims are supported by the retrieved passages, even when paraphrased.
- supported = 0: The response includes material information not supported by the retrieved passages, even if that information might be true elsewhere.
- Unanswerable questions: The agent should acknowledge insufficient information. Partial answers are acceptable when they clearly distinguish supported facts from what cannot be determined.
- Refusals: a response that only says the corpus does not cover the question makes no factual claim, so supported = 1.
