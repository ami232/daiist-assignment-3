# Judge rubric

You grade one answer of a GDPR assistant for small businesses. You are given the question, the reference
answer, the passages the assistant retrieved, and the assistant's answer. Give two verdicts: `verdict` and
`supported`.

## verdict (correct, partial or incorrect)

The answer must contain every core point of the reference answer, not just the main one. Supporting details
are optional.

- **correct**: all core points are present and nothing is contradicted.
- **partial**: some core points are present, some are missing, and nothing is contradicted. On a two-part
  question, an answer that is right on one part only is partial.
- **incorrect**: a core point is contradicted, or the main conclusion is wrong.

### Unanswerable questions

The documents do not answer these questions. The reference answer says what the assistant should say. A proper
refusal is **correct**, even if the answer adds related passages, provided it:

- says clearly that the documents do not answer the question;
- does not state the missing answer as fact;
- describes the added passages as related, not as the answer.

It is **incorrect** if it presents the added passages as answering the question (for example "Art. 42 means
ISO 27001 makes you compliant").

## supported (true or false)

True only if every substantive claim in the answer (deadlines, duties, conditions) can be traced to a passage
the assistant actually retrieved. A true fact that comes from the assistant's own memory is not supported.
General advice such as "ask a lawyer" is not a claim about the law, so it does not make an answer unsupported.

## Citations

You are told which citations could not be found in the retrieved passages and which of them do not exist
anywhere in the corpus (fabricated).

- A citation that cannot be found in the retrieved passages makes the claim it supports **unsupported**. It
  does not make the answer wrong by itself: judge the content separately.
- A fabricated citation is more serious. It is counted on its own, and an answer that would be **correct**
  is **partial** instead.
