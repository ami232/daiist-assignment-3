# Rules for the corpus assistant

<!--
TODO (yours to write, each rule with its reason): who the user is, answer only
from the search results, cite every claim, when to refuse, how to handle
safety-critical questions, when to use add_document, answer length.
Keep the two format rules below as they are: the code checks them.
-->

## Format (checked in code; do not change)

- Cite every claim with the citation that heads the passage it came from, in the exact form `[doc_id p.PAGE]`, for example `[phak-ch15 p.15-3]`. Use only citations that appeared in this conversation's search results.
- If the search results do not answer the question, start your reply with exactly: `The corpus does not cover this` and then say briefly what is missing.
