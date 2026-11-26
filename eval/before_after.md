# Adding a document: before and after

Unanswerable question **q31**: "We're launching a cookie banner in France. Does the French regulator require refusing cookies to be as easy as accepting them?"

The three EU laws require consent for non-essential cookies (ePrivacy Directive, Article 5(3)) and make *withdrawing* consent as easy as giving it (GDPR, Article 7(3)), but none of them says what the French regulator requires of a banner's *refuse* option.

## Before (saved in eval/answers.jsonl, run during the evaluation)

Search: ['cookie banner refuse easy accept France ePrivacy GDPR']

> The corpus does not cover this question.

## Adding the document, with approval

Document: `extra_docs/CNIL_cookie_refusal_2021.md`, the CNIL's news item of 14 December 2021, "Refusing cookies should be as easy as accepting them: the CNIL continues its action and issues new orders" (https://cnil.fr/en/refusing-cookies-should-be-easy-accepting-them-cnil-continues-its-action-and-issues-new-orders), saved as Markdown.

```
$ printf 'y\n' | uv run python main.py ask "Please add the document extra_docs/CNIL_cookie_refusal_2021.md to the index."
The agent wants to run add_document with {"path": "extra_docs/CNIL_cookie_refusal_2021.md"}.
Approve? [y/N] y
  [article] embedded 2/2
add_document: CNIL cookie refusal 2021: 2 chunks, 2 embedded, 0 replaced
The corpus does not cover this question.

[1 search(es): ['CNIL cookie refusal 2021']; 5791+106 tokens; 9.25s; guardrail events: [{'guardrail': 'approval', 'tool': 'add_document', 'args': {'path': 'extra_docs/CNIL_cookie_refusal_2021.md'}, 'approved': True}, {'guardrail': 'citation_check', 'attempt': 1, 'problem': 'the answer has no citation tags', 'draft': 'The document `extra_docs/CNIL_cookie_refusal_2021.md` has been successfully added to the index (source: `CNIL cookie refusal 2021`).'}]]
```

The document was added (2 chunks embedded). The answer printed above is wrong: the citation-check guardrail treated the confirmation as an uncited legal answer and replaced it with the refusal. agent.py now skips the citation check when the run added a document.

## Same document again (already indexed), after that fix

```
$ printf 'y\n' | uv run python main.py ask "Add extra_docs/CNIL_cookie_refusal_2021.md to the index."
The agent wants to run add_document with {"path": "extra_docs/CNIL_cookie_refusal_2021.md"}.
Approve? [y/N] y
The document `extra_docs/CNIL_cookie_refusal_2021.md` is already present in the index as **CNIL cookie refusal 2021** (2 chunks). It is ready to be used for searching and answering your questions.

[0 search(es): []; 1646+90 tokens; 6.57s; guardrail events: [{'guardrail': 'approval', 'tool': 'add_document', 'args': {'path': 'extra_docs/CNIL_cookie_refusal_2021.md'}, 'approved': True}, {'guardrail': 'citation_check', 'skipped': 'the run added a document'}]]
```

Nothing was embedded: the content hash matched the indexed copy.

## After

```
$ uv run python main.py ask "We're launching a cookie banner in France. Does the French regulator require refusing cookies to be as easy as accepting them?"
Yes. The French data protection regulator (the CNIL) actively enforces the requirement that **refusing cookies must be as easy as accepting them** [CNIL cookie refusal 2021, § Refusing cookies should be as easy as accepting them: the CNIL continues its action and issues new orders]. 

Key compliance points based on the CNIL's enforcement practice include:
* **Equal Effort and Prominence:** Information banners must allow users to refuse cookies just as easily and visibly as they can accept them (e.g., providing a clear "Refuse All" option directly on the initial banner alongside the "Accept All" button) [CNIL cookie refusal 2021, § Refusing cookies should be as easy as accepting them: the CNIL continues its action and issues new orders].
* **Effective Refusal Mechanism:** Offering a refusal button is not enough; the mechanism must be fully effective so that no cookies subject to consent are deposited if the user refuses [CNIL cookie refusal 2021, § Refusing cookies should be as easy as accepting them: the CNIL continues its action and issues new orders].
* **Risk of Sanctions:** The CNIL routinely issues formal compliance orders and financial sanctions (which can reach up to 2% of annual worldwide turnover) against organizations whose cookie banners fail to meet this standard [CNIL cookie refusal 2021, § Refusing cookies should be as easy as accepting them: the CNIL continues its action and issues new orders].

Citations:
  [CNIL cookie refusal 2021, § Refusing cookies should be as easy as accepting them: the CNIL continues its action and issues new orders]

[1 search(es): ['cookie banner France accept refuse easy']; 3620+332 tokens; 4.58s; guardrail events: none]
```
