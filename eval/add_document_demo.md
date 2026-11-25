# add_document demo: q31

Question: Who said that government is the great fiction through which everybody tries to live at the expense of everybody else?

## Before (bastiat-government not indexed), 2026-11-12 18:05

```
  call search({'query': 'government is the great fiction through which everybody tries to live at the expense of everybody else'})
  result bastiat-seen-unseen-p5-w0, bastiat-seen-unseen-p244-w300, bastiat-seen-unseen-p40-w450, bastiat-seen-unseen-p59-w900, bastiat-seen-unseen-p214-w600

- **Verdict:** not in these texts
- **Answer:** No passage in the corpus addresses this. The corpus covers only Mill, On Liberty ch. I-II; Marx and Engels, Communist Manifesto; Paine, Agrarian Justice; Bastiat, That Which Is Seen, and That Which Is Not Seen; Smith, Wealth of Nations Book I ch. II and Book IV ch. II.

Guardrail: refusal written by the harness. The model had written:
- **Verdict:** not in these texts
- **Answer:** The indexed corpus does not contain the quoted statement about government as a great fiction, although it includes Frédéric Bastiat's writings on economic intervention and taxes.
(4430 tokens, 18.2 s)
```

## Adding the document (approval step), 2026-11-12

```
$ uv run python main.py ask "Add the document corpus/bastiat-government.txt to the index"
  Allow add_document({'path': 'corpus/bastiat-government.txt'})? [y/N] y
fixed: saved 20/27 new vectors
fixed: saved 27/27 new vectors
add_document: added bastiat-government, 27 chunks embedded
  call add_document({'path': 'corpus/bastiat-government.txt'})
  result {"status": "added", "source": "bastiat-government", "chunks": 27, "embedded": 27}

The document corpus/bastiat-government.txt has been successfully added to the index.
(2721 tokens, 7.1 s)
```

## First "after": still a refusal, although the right passage was retrieved

Search returned `bastiat-government-p44-w1350` first, which contains the sentence. The agent still refused,
because AGENTS.md, the search tool description and the refusal text all listed a fixed corpus without *Government*.
The quote check also removed the quoted title "That Which Is Seen, and That Which Is Not Seen".

```
  call search({'query': 'government is the great fiction through which everybody tries to live at the expense of everybody else'})
  result bastiat-government-p44-w1350, bastiat-government-p46-w1500, bastiat-seen-unseen-p5-w0, bastiat-government-p65-w2550, bastiat-government-p67-w2700

- **Verdict:** not in these texts
- **Answer:** No passage in the corpus addresses this. The corpus covers only Mill, On Liberty ch. I-II; Marx and Engels, Communist Manifesto; Paine, Agrarian Justice; Bastiat, That Which Is Seen, and That Which Is Not Seen; Smith, Wealth of Nations Book I ch. II and Book IV ch. II.

Guardrail: refusal written by the harness. The model had written:
- **Verdict:** not in these texts
- **Answer:** The corpus does not cover Bastiat's essay "Government" (1848) where this quote appears, containing only his "That Which Is Seen, and That Which Is Not Seen" (1850).
```

Fix: the corpus lists now say documents added later count too, the refusal text reads the list of works from the index, and quoted book titles are no longer removed.

## After the fix (asked twice, same result)

```
  call search({'query': 'government is the great fiction through which everybody tries to live at the expense of everybody else'})
  result bastiat-government-p44-w1350, bastiat-government-p46-w1500, bastiat-seen-unseen-p5-w0, bastiat-government-p65-w2550, bastiat-government-p67-w2700

- **Verdict:** said it
- **Answer:** Frédéric Bastiat wrote that government is the great fiction through which everyone tries to live at the expense of everyone else.
- **Source:** Frédéric Bastiat, Government (1848), Full essay, ¶44-46 [bastiat-government-p44-w1350]
- **Quote:** "Government is the great fiction, through which everybody endeavours to live at the expense of everybody else." [bastiat-government-p44-w1350]
- **Why this verdict:** The passage explicitly matches the claim about government being the great fiction for living at others' expense.

Fit: Frédéric Bastiat 100% (closeness to the passages, not who is right)
(4557 tokens, 2.5 s)
```
