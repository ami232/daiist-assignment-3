# Evaluation summary

Served: `{'design': 'A250', 'method': 'hybrid', 'use_route': True, 'k': 5}` | agent `gemini-3.5-flash` | judge `gemini-3.8-flash`

## Retrieval (hit rate, answerable questions; multi = both passages)

| config | hit@1 | hit@3 | hit@5 | multi hit@5 | words at k=5 |
|---|---|---|---|---|---|
| A250 vector | 0.457 | 0.743 | 0.829 | 0.375 | 1243 |
| A250 bm25 | 0.543 | 0.6 | 0.714 | 0.25 | 1238 |
| A250 hybrid | 0.657 | 0.743 | 0.8 | 0.25 | 1241 |
| A250 hybrid + route | 0.686 | 0.714 | 0.829 | 0.375 | 1241 |

## End to end

- **evaluated**: 43
- **correct**: 0.977
- **supported**: 0.93
- **unsupported_answers**: 3
- **correct_refusals**: 8/8
- **wrong_refusals**: 0/35
- **answered_unanswerable**: 0/8
- **answers_with_invalid_citations**: 0
- **guardrail_fired**: 0
- **guardrail_withheld**: 0
- **baseline_correct**: 0.442
- **per question**: {'input_tokens': 11875, 'output_tokens': 1006, 'seconds': 11.3, 'tool_calls': 1.67}
- **failure hints**: {'unsupported claim': ['q18', 'q27', 'q32']}
- **judge tags**: {'PARTIAL:': [], 'RETRIEVAL-MISS': [], 'WRONG-REFUSAL': [], 'CITATION-MISMATCH': ['q41']}
- **human vs judge**: {'correct': {'n': 28, 'agreement': 0.929, 'cohen_kappa': -0.037}, 'supported': {'n': 28, 'agreement': 0.893, 'cohen_kappa': -0.05}, 'disagreements': ['q27', 'q31', 'q32']}
