# Add-document demo

Question: How fast do we have to take down terrorist content after an authority orders it?

Document: Terrorist Content Online, Regulation (EU) 2021/784, https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021R0784

### 1. Before

Upon receiving an order from a national judicial or administrative authority to act against specific illegal content, intermediary service providers must inform the issuing authority (or any other authority specified in the order) without undue delay of any effect given to the order, specifying if and when effect was given [dsa-article-0011]. 

The corpus does not cover a specific numerical deadline for taking down terrorist content, but instead requires informing the authority about the action taken without undue delay [dsa-article-0011].

Citations:
- [dsa-article-0011] DSA Article 9(1)

Tool calls:
- search({"query": "terrorist content order take down"})
- search({"query": "without undue delay order illegal content article 9"})

### 2. Add request, approval denied

The document was not added because it was not approved.

Citations:
- none

Tool calls:
- add_document({"path": "corpus/tco.xhtml"})

Approval asked for: [{'path': 'corpus/tco.xhtml'}]

### 3. Add request, approved

Added corpus/tco.xhtml: added 'tco': 35 chunks (0 newly embedded). Search now covers it.

Citations:
- none

Tool calls:
- add_document({"path": "corpus/tco.xhtml"})

Approval asked for: [{'path': 'corpus/tco.xhtml'}]

### 4. Same file again (direct tool call)

'tco' is already indexed with identical content. Nothing added.

### 5. After

You must remove terrorist content or disable access to it as soon as possible, and in any event within one hour of receiving a removal order from a competent authority [tco-article-0004].

Check with a lawyer before acting.

Citations:
- [tco-article-0004] TCO Article 3(1)-(3)

Tool calls:
- search({"query": "terrorist content order authority take down"})

### 6. Clean-up

TCO chunks removed from index/ again (vectors kept in the cache, so re-adding costs nothing), so the evaluation runs on the original corpus.
