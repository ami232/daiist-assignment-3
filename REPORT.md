# Evaluating a RAG System for EU Travel Rights

**Name:** Nicolas Loescher Montal  
**Student ID:** 20322  
**Group:** PPLEDBA 5A

I built and evaluated a RAG system for EU travel rights. I ran 32 questions against the live index, saved the retrieval results in JSON logs, and graded the answers myself alongside an LLM judge.

## Use Case

I focused on travellers who need to know whether a flight or train disruption entitles them to a refund or compensation. A wrong amount or a missed exception can affect a claim, so I instructed the system to refuse when it could not find enough evidence to answer.

## Corpus

The initial corpus contained three legal texts and one guidelines document, totalling 66,538 words after cleaning.

| Document | Type | Official Journal | Words |
| --- | --- | --- | ---: |
| [Regulation (EC) No 261/2004 — Air passenger rights](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261) | Legislation | OJ L 46, 17.2.2004 | 4,365 + 75 |
| [Commission Interpretative Guidelines on Regulation 261/2004](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05687) | Guidance | OJ C, C/2024/5687, 25.9.2024 | 19,121 + 2,784 |
| [Regulation (EU) 2021/782 — Rail passenger rights](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021R0782) | Legislation | OJ L 172, 17.5.2021 | 23,011 + 510 |
| [Directive (EU) 2015/2302 — Package travel](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32015L2302) | Legislation | OJ L 326, 11.12.2015 | 16,486 + 186 |
| **Core total** | | | **66,538** |

I used the original EUR-Lex editions, which limits coverage of later amendments. I verified the files with checksums before processing and excluded tables of contents from the word counts.

**Reuse:** EUR-Lex material was reused with attribution to EUR-Lex and the original Official Journal publications listed above.

## Ingestion

The pipeline extracts text from PDFs and HTML. I checked the reading order in two-column PDFs, fixed broken hyphenation, and removed running headers and navigation pages. I redacted signatory names and kept case IDs for citation. Each chunk has location metadata and is stored in ChromaDB. The index is 22 MB, and a cache prevents the same chunks from being embedded twice.

## Test Set

I wrote 32 questions and froze the set before tuning. Nineteen could be answered from one passage, seven needed multiple passages, and six were unanswerable from the corpus. I checked the answerable questions against the chunk metadata to confirm that the relevant evidence was in the index. The unanswerable questions covered topics such as ferry rules and future amendments.

## Retrieval Strategy

I compared fixed windows of 200 words with chunks based on document structure. The results are recorded in `eval/retrieval.json`.

| Design | Hit@1 | Hit@3 | Hit@5 | All evidence for multi questions @3 | Words in top 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A · Fixed 200-word windows (40-word overlap), 395 chunks | 0.885 | 0.962 | 1.000 | 0.714 | 1,045 |
| B · Articles and sections (max 450 words), 286 chunks | 0.808 | 1.000 | 1.000 | 0.429 | 1,466 |

Hit@k is measured on the 26 answerable questions. Both designs found every expected passage within the five chunks the search tool returns, so Hit@5 could not separate them. Design B was better at k=3, but Design A put the right passage first more often, found both passages for more of the multi-passage questions (5 of 7 against 3 of 7 at k=3), and adds about 30% fewer words to each prompt. I chose Design A on those three numbers.

## Tools and Subagent

The MCP server exposes two tools. `search` returns relevant passages and citation IDs, with a reminder to treat the passages as source material. `add_document` adds new sources after checking for duplicates.

The retrieval subagent can only use `search`. In the demonstration, it made six search calls, identified compensation bands and exceptions, and flagged details it could not establish from the passages. The calls and its final reply are included in Appendix A.

## Dynamic Indexing

I held out the HTML version of [Regulation (EU) No 181/2011 on bus and coach passenger rights](https://eur-lex.europa.eu/eli/reg/2011/181/oj) to see whether I could add a source to the existing index. I asked the same question before and after indexing the regulation. The first run refused, and the second answered with a citation to the new source.

**Question from `eval/add_document_demo.json`**

> My long-distance coach was cancelled at the bus terminal. What must the bus company offer me?

**Before adding the regulation**

> NOT IN CORPUS: The corpus covers EU air passenger rights (Regulation (EC) No 261/2004), rail rights (Regulation (EU) 2021/782), and package travel (Directive (EU) 2015/2302), but it does not contain the rules for bus and coach passenger rights. To find out what a bus company must offer for a cancelled long-distance coach, you would need to consult EU bus and coach passenger rights regulations (such as Regulation (EU) No 181/2011) or national transport law.

**After adding the regulation**

> If a bus or coach regular service is cancelled (or expected to be delayed in departure from a terminal for more than 120 minutes), EU rules give you the right to choose between two options [32011R0181:A:w031:1]:
>
> 1. **Continuation or re-routing:** Transport to your final destination, at no additional cost and under comparable conditions, at the earliest opportunity [32011R0181:A:w031:1].
> 2. **Reimbursement and return:** Reimbursement of the ticket price (covering the parts of the journey not made, and any parts already made if they no longer serve your original travel plan), plus a free return service by bus or coach to your first point of departure at the earliest opportunity, where relevant [32011R0181:A:w032:1, 32011R0181:A:w033:1].
>
> * **Failure to offer a choice:** If the carrier fails to offer you this choice, you are entitled to compensation of **50% of the ticket price** in addition to the ticket reimbursement, payable within 1 month of your request [32011R0181:A:w032:1].
> * **Reimbursement payout:** Cash/money reimbursement must be paid within 14 days of the offer or request, unless you accept another form of reimbursement (such as a voucher) [32011R0181:A:w033:1].
> * **Assistance and Care:** If your scheduled journey is for **more than 3 hours** and the departure from the terminal is delayed for **more than 90 minutes**, the carrier must also offer you free of charge:
>   * Snacks, meals, or refreshments in reasonable relation to the waiting time (if available or reasonably supplied) [32011R0181:A:w035:1].
>   * A hotel room or other accommodation and transport between the terminal and place of accommodation if a stay of 1 or more nights becomes necessary (the carrier may limit accommodation costs to €80 per night for a maximum of 2 nights) [32011R0181:A:w035:1]. (This accommodation assistance does not apply if the cancellation is caused by severe weather conditions or major natural disasters endangering safe operation) [32011R0181:A:w036:1].
>
> *(Note: This information is based on Regulation (EU) No 181/2011 on bus and coach passenger rights [32011R0181:A:w032:1, 32011R0181:A:w035:1].)*

When I submitted the same file again, the duplicate check blocked re-indexing.

## Harness and Guardrails

The LangChain harness requires manual approval before adding a document and caps the number of tool calls. The citation verifier checks whether each cited ID appears in the retrieved context. During testing, three fabricated citations reached users. I revised the parser to check each ID separately when an answer groups multiple citations in one bracket. Rechecking the stored answers with the revised parser, it would withhold four answers (q03, q11, q20, q27). The original check had fired twice. In 28 of 32 answers, every cited ID existed in the index and had been returned to the agent. These checks prove a cited ID is real and was retrieved, not that it supports the claim, so support was graded separately.

## Evaluation

The LLM judge graded each answer on two criteria, using the retrieved passages as evidence. **Correct:** for an answerable question, the answer states the key facts of the reference answer, with its conditions and exceptions; a refusal or withheld answer counts as incorrect. For an unanswerable question, the answer must say the texts do not establish it, without supplying the missing facts from elsewhere. **Supported:** every factual claim appears in the retrieved passages, judged against the passages rather than the judge's own knowledge.

By my labels, the system answered 24 of the 26 answerable questions correctly (the judge counted 23) and refused all six unanswerable questions. I graded all responses before seeing the LLM judge’s ratings. My blind agreement with the judge was 93.8% on correctness and 71.9% on whether the retrieved text supported the answer. After reviewing the disagreements and revising eight labels, I recorded 96.9% agreement on both correctness (31 of 32) and support (31 of 32).

One disagreement involved a truncated passage. I judged the answer legally correct, but the retrieved excerpt did not support it in full. That example shows why I scored correctness and support separately.

## Failure Analysis

| Questions | Failure | What happened |
| --- | --- | --- |
| q03, q06 | Wrong refusal | The harness withheld two answers. q03 cited an ID that search never returned. q06 was correct, but the first parser missed two valid IDs grouped in one bracket. |
| q11, q20 | Unsupported claim | The answers cited IDs that search never returned (`32004R0261:A:article-8` in q11, `32004R0261:A:w16:1` in q20), and the first parser let them through. q20 also described Article 9 care that no retrieved passage contained. |
| q14 | Unsupported claim | The answer was correct, but it said refunds can be paid in vouchers; the retrieved passage was cut off before that clause. |
| q27–q30 | Unsupported claim in a refusal | The system refused correctly, but the explanations named laws or corpus contents that the retrieved text did not show; q27 also cited a malformed ID. |

I found no retrieval misses on the answerable questions. Finding the right passage still left room for errors, as q14 showed. The same issue came up in the refusals: the decision to refuse could be right while the explanation still introduced an unsupported claim.

## Decision and Cost

I would keep the system as a prototype. Three fabricated citations reached users during the evaluation. Before recommending wider use, I would check that the revised parser catches all three cases and rerun the full test set. I would also adjust chunk boundaries around complex clauses and check that refusal explanations stay within the retrieved evidence.

Median latency was 2.58 seconds (mean 5.61 seconds), and the agent used about 6,550 tokens per question (209,624 over 32 questions). Grading added about 3,600 judge tokens per question.

## AI Use Disclosure

I used AI for coding infrastructure, boilerplate, and help drafting and editing this report. I designed the architecture, chose the chunking strategy, wrote the test questions, manually graded the answers, and drew the final conclusions. I reviewed and adjusted the code to meet the assignment requirements.

## Appendix A — Subagent Transcript

Source: `eval/subagent_transcript.md`

The main agent (Claude Code, `claude-opus-5-5`, headless) delegated to `.claude/agents/corpus-researcher.md`, whose only tool is `mcp__corpus__search`. In the search results, passage text is abbreviated to the returned IDs; the full run, including the main agent's final reply, is in the source file.

**Delegation prompt (main agent → subagent)**

> A traveller asks: "My train from Madrid to Paris arrived 90 minutes late. What compensation do the EU texts give me, and are there exceptions where the railway does not have to pay?"
>
> Search the corpus (rail Regulation 2021/782 especially) and report:
> 1. The compensation rule for rail delays: delay thresholds and percentages of the ticket price, and what 90 minutes falls under. Include how the ticket price basis is defined (single vs return, through tickets), minimum payout thresholds, payment form/timing, and any rule about not being entitled if informed of the delay before buying.
> 2. Every exception/exemption where the railway does not have to pay compensation (e.g. extraordinary circumstances, weather, third-party behaviour, passenger fault, strikes) and any limits on those exceptions. Also any Member State exemptions for international or cross-border services that could affect a Madrid–Paris journey.
> 3. Keep compensation separate from refund/re-routing and assistance; mention those only briefly if the passages cover them and they are relevant to a 90-minute delay.
> 4. Facts about the traveller's case that the answer depends on and that they have not given (e.g. ticket price, single vs return, whether one through ticket, whether they were told of the delay before buying, cause of delay).
>
> Cite every material claim with the passage id exactly as the search tool printed it, in square brackets. Quote key words where interpretation is needed. Say clearly if anything is not covered by the passages you retrieved. Search multiple times with different wording if needed.

**The six search calls, in order, with the passage IDs each returned**

- **search**(`rail compensation for delay 60 to 119 minutes 25% of ticket price`) → `32021R0782:A:w054:1`, `32021R0782:A:w055:1`, `32021R0782:A:w057:1`, `32021R0782:A:w056:1`, `32021R0782:A:w058:1`
- **search**(`railway undertaking not obliged to pay compensation extraordinary circumstances weather third party passenger fault strike`) → `32021R0782:A:w059:1`, `32021R0782:A:w058:1`, `32021R0782:A:w019:1`, `32021R0782:A:w020:1`, `52024XC05687:A:w077:1`
- **search**(`Member States exempt rail services from application of regulation international cross-border`) → `32021R0782:A:w029:1`, `32021R0782:A:w004:1`, `32021R0782:A:w030:1`, `32021R0782:A:w005:1`, `32021R0782:A:w028:1`
- **search**(`rail delay 60 minutes assistance meals refreshments accommodation Article 20(2)`) → `32021R0782:A:w060:1`, `32021R0782:A:w059:1`, `52024XC05687:A:w055:1`, `32021R0782:A:w061:1`, `32021R0782:A:w054:1`
- **search**(`Article 18 reimbursement and re-routing expected delay at arrival of more than 60 minutes`) → `32021R0782:A:w050:1`, `32021R0782:A:w054:1`, `32021R0782:A:w052:1`, `32021R0782:A:w051:1`, `32004R0261:A:w019:1`
- **search**(`where it is reasonably to be expected that arrival at final destination will be delayed by 60 minutes reimbursement re-routing choice`) → `32021R0782:A:w050:1`, `32004R0261:A:w019:1`, `32021R0782:A:w049:1`, `32021R0782:A:w051:1`, `32021R0782:A:w054:1`

**Subagent's final reply**

> NEED DETAILS: A 90-minute delay falls in the rail Regulation's band of "25 % of the ticket price for a delay of 60 to 119 minutes" (50 % from 120 minutes); this is paid "without losing the right of transport", for a delay between the departure and final destination "stated in the ticket or through-ticket", and only if the ticket cost "has not been reimbursed in accordance with Article 18" [32021R0782:A:w054:1]. The basis is "the full price which the passenger actually paid for the delayed service"; for a return contract it is the price shown for that leg, or half the ticket price if no leg price is shown, and other multi-leg contracts are calculated in proportion to the full price [32021R0782:A:w055:1][32021R0782:A:w056:1]. Payment is due within one month of the request; it may come as vouchers or other services if their terms are flexible, but as money if you ask, it may not be cut by transaction fees, and a minimum payout threshold may be set at no more than EUR 4 per ticket [32021R0782:A:w057:1][32021R0782:A:w058:1]. There is no compensation at all if you were "informed of a delay before buying a ticket", or if a delay after continuation or re-routing "remains below 60 minutes" [32021R0782:A:w058:1]. The railway need not pay if it "can prove" the delay was "caused directly by, or was inherently linked with" one of three things [32021R0782:A:w058:1][32021R0782:A:w059:1]: (a) extraordinary circumstances "not connected with the operation of the railway, such as extreme weather conditions, major natural disasters or major public health crises" that it could not avoid despite due care; (b) fault on the passenger's part; or (c) third-party behaviour it could not avoid despite due care, "such as persons on the track, cable theft, on-board emergencies, law enforcement activities, sabotage or terrorism". Exception (c) does not cover the railway's own staff strikes, acts or omissions of another undertaking on the same infrastructure, or acts or omissions of infrastructure and station managers [32021R0782:A:w059:1]; a recital (explanatory text of the Regulation, not an operative article) adds that weather must have "the character of an exceptional natural catastrophe, as distinct from normal seasonal weather conditions such as autumnal storms", and that the railway should bring any supporting documents to passengers' attention [32021R0782:A:w019:1][32021R0782:A:w020:1]. On Member State exemptions: countries may exempt international services "of which a significant part, including at least one scheduled station stop, is operated outside the Union", and countries with older exemptions may exempt domestic services from Article 19 for up to five more years [32021R0782:A:w029:1][32021R0782:A:w028:1]; as worded, neither seems to fit Madrid–Paris, and delay the railway shows happened outside the Union does not count [32021R0782:A:w056:1]. Separate from compensation, an expected arrival delay of 60 minutes or more triggers a choice of refund or continuation/re-routing [32021R0782:A:w049:1][32021R0782:A:w050:1], plus free meals and refreshments "in reasonable relation to the waiting time" and accommodation if a stay becomes necessary (which may be capped at three nights in exception cases) [32021R0782:A:w060:1]; to apply all this, please tell me the price you paid, whether it was a single or return (and whether the ticket shows a price per leg), whether Madrid–Paris was one ticket or through-ticket, whether you were told of the delay before buying, and what cause the railway gave.
>
> NOT ESTABLISHED: Whether Spain or France has notified any exemption affecting this service, and any rail-specific Commission guidance (the only guidance in the corpus covers air travel); all citations are from Regulation (EU) 2021/782, legislation in its 2021 original text, not consolidated. This is information from the texts, not legal advice for your case.
