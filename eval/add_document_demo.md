# Adding a document: before and after

**Unanswerable question (q02):** If I scrape off the moldy part of my jam, can I eat the rest?

**Document added:** USDA FSIS, "Molds on Food: Are They Dangerous?"
(https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/molds-food-are-they-dangerous),
US federal government work (public domain). Saved by hand from the browser as
`extra_docs/usda_molds_on_food.html`, because fsis.usda.gov blocks automated downloads.
6 chunks, about 1,900 words.

## Before (evaluation run, eval/answers.jsonl)

> The FDA documents I have don't cover this.

## Adding it (agent.py, with human approval)

```
$ uv run python agent.py "Please add the document extra_docs/usda_molds_on_food.html to the index."

The agent wants to add this document to the index:
  extra_docs/usda_molds_on_food.html
Approve? [y/N] y
  embedded 6/6
```

The index went from 526 to 532 chunks.

## After (`main.py ask`)

> No, you should discard the jam [usda_molds_on_food | Section: How Should You Handle Food with Mold on It? (part 2)].
>
> Microbiologists recommend against scooping out the mold and using the remaining condiment because the mold could be producing a mycotoxin [usda_molds_on_food | Section: How Should You Handle Food with Mold on It? (part 2)].

(1 tool call, 3,932 + 107 tokens, 6.6 s)

## Adding the same document again

```
Already indexed: usda_molds_on_food.html (6 chunks, source 'usda_molds_on_food'). Nothing changed.
```

## Issue found

After the add-only request, the citation guardrail fired on the agent's confirmation message
("the answer makes claims without any citation") and the retry produced "The FDA documents I have
don't cover this." A turn that only adds a document has nothing to cite, so agent.py now skips the
citation check when add_document was called and search was not.
