# Adding a document: before and after

Document: FDA, *Cosmetics Labeling Guide*, https://www.fda.gov/cosmetics/cosmetics-labeling-regulations/cosmetics-labeling-guide (US government work, public domain).

### 1. Before: q29 on the EU corpus

**Question:** What labelling requirements does the US FDA impose to sell a perfume in the United States?

- Tool calls: []
- Guardrail: did not fire
- 1066 tokens, 7.7 s

**Answer:**

The corpus does not cover this question. The provided corpus contains only EU cosmetics law (Regulation (EC) No 1223/2009 and related regulations), and I am restricted to answering based solely on those documents.

### 2. Add the document, approval refused

**Question:** Please add the document corpus/added/fda_cosmetics_labeling_guide.html to the corpus.

- Approval asked: run `add_document` with {"path": "corpus/added/fda_cosmetics_labeling_guide.html"} -> refused
- Tool calls: [{"tool": "add_document", "args": {"path": "corpus/added/fda_cosmetics_labeling_guide.html"}}]
- Guardrail: did not fire
- 2169 tokens, 11.6 s

**Answer:**

I cannot add that document because it is not part of the EU cosmetics law corpus. My instructions are to only add documents when requested and to focus exclusively on EU cosmetics law.

### 3. Add the document, approval given

**Question:** Please add the document corpus/added/fda_cosmetics_labeling_guide.html to the corpus.

- Approval asked: run `add_document` with {"path": "corpus/added/fda_cosmetics_labeling_guide.html"} -> approved
- Tool calls: [{"tool": "add_document", "args": {"path": "corpus/added/fda_cosmetics_labeling_guide.html"}}]
- Guardrail: did not fire
- 2228 tokens, 107.0 s

**Answer:**

The document `corpus/added/fda_cosmetics_labeling_guide.html` has been added to the corpus. Please note that this document contains US FDA regulations, which are outside the scope of EU cosmetics law (Regulation (EC) No 1223/2009). I will continue to prioritize EU law for your compliance queries.

### 4. After: q29 again, same rules

**Question:** What labelling requirements does the US FDA impose to sell a perfume in the United States?

- Tool calls: []
- Guardrail: did not fire
- 1066 tokens, 5.1 s

**Answer:**

The corpus does not cover this question. The provided corpus contains only EU cosmetics law (Regulation (EC) No 1223/2009 and related regulations), and I am restricted to answering based solely on those documents.

Rule 5 of AGENTS.md describes the corpus as EU law only, so step 4 refuses without searching. Step 4b adds one line to the system prompt, as the team would when it adds a document: *Corpus update: the corpus now also contains the FDA Cosmetics Labeling Guide (US labelling rules); search it for questions about the United States.*

### 4b. After: q29 again, corpus description updated

**Question:** What labelling requirements does the US FDA impose to sell a perfume in the United States?

- Tool calls: [{"tool": "search", "args": {"query": "FDA Cosmetics Labeling Guide perfume requirements"}}]
- Guardrail: did not fire
- 3523 tokens, 22.4 s

**Answer:**

To sell a perfume in the United States, you must comply with the Federal Food, Drug, and Cosmetic (FD&C) Act and the Fair Packaging and Labeling (FP&L) Act [fda_cosmetics_labeling_guide | introduction].

Key requirements include:
*   **Language:** All required statements must be in English, unless the product is distributed solely in a territory where another language is predominant [fda_cosmetics_labeling_guide | section 'Foreign language statements']. If the label contains any foreign language, all required statements must also appear in that language [fda_cosmetics_labeling_guide | section 'Foreign language statements'].
*   **Fragrance Declaration:** Fragrance compounds may be declared as "fragrance" in the ingredient list [fda_cosmetics_labeling_guide | section 'Fragrance and flavor']. Alternatively, individual components may be listed by their appropriate label names [fda_cosmetics_labeling_guide | section 'Fragrance and flavor'].
*   **Placement and Readability:** Required information must be prominent, conspicuous, and easily readable on a panel displayed under customary conditions of purchase [fda_cosmetics_labeling_guide | section 'Obscuring designs, vignettes']. It must not be obscured by designs or crowded by other printed matter [fda_cosmetics_labeling_guide | section 'Obscuring designs, vignettes'].

The FDA Cosmetics Labeling Guide provides further details on requirements such as the identity of the product, the name and place of business, and the net quantity of contents [fda_cosmetics_labeling_guide | introduction].

### 5. The same file again (server tool called directly)

fda_cosmetics_labeling_guide.html is already indexed (114 passages); nothing changed.

### 6. Clean-up

Removed the 114 FDA passages again, so the indexed corpus matches the test set, where q29 is unanswerable.
