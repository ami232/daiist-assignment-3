# Assignment 3 Report

- **Name**: Ignacio Ascanio Aliño
- **Student ID**: 18719
- **Group**: BBADBA 5B 

## Use case

I built **MoneyGuide**, a retrieval-augmented educational assistant for people seeking U.S. consumer-finance guidance about budgeting, overdue bills, debt repayment, credit reports, and mortgage shopping. A user asks a practical question and uses the response to understand possible steps and identify official CFPB guidance; the assistant is not a lender, financial adviser, or source of personal account information.

Incorrect advice about which bills to pay can lead to fees, loss of utilities, repossession, or housing difficulties. Incorrect mortgage or credit-report guidance can cause expensive financial decisions. By contrast, a transparent **“I don't know based on the documents in this collection”** can delay a decision, but avoids falsely presenting an unsupported answer as authoritative. My intended use is educational explanation with source-page citations, not individualized financial or legal decisions.

## Corpus

The **baseline** corpus contains five public documents published by the U.S. Consumer Financial Protection Bureau (CFPB), totaling **88,617 extracted words**. The filenames match the `source` metadata in the ChromaDB index.

| Document | Official source URL | Document date | Reuse status | Extracted words |
|---|---|---|---|---:|
| *Your Money, Your Goals: A Financial Empowerment Toolkit* (`money_goals.pdf`) | [CFPB PDF](https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_financial-empowerment_toolkit.pdf) | June 2020 | CFPB-created material: public domain, with trademark and third-party exceptions | 62,504 |
| *Behind on Bills?* (`behind_on_bills.pdf`) | [CFPB PDF](https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_behind-on-bills_booklet_cobrand.pdf) | Not stated clearly in retrieved version | CFPB-created material: public domain, with trademark and third-party exceptions | 5,424 |
| *Debt Getting in Your Way?* (`debt_booklet.pdf`) | [CFPB PDF](https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_debt_booklet_cobrand.pdf) | Not stated clearly in retrieved version | CFPB-created material: public domain, with trademark and third-party exceptions | 4,964 |
| *Want Credit to Work for You?* (`credit_booklet.pdf`) | [CFPB PDF](https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_credit_booklet_cobrand.pdf) | Not stated clearly in retrieved version | CFPB-created material: public domain, with trademark and third-party exceptions | 5,562 |
| *Your Home Loan Toolkit: A Step-by-Step Guide* (`home_loan_toolkit.pdf`) | [CFPB PDF](https://files.consumerfinance.gov/f/documents/cfpb_your-home-loan-toolkit.pdf) | Updated August 2015 | CFPB-created material: public domain, with trademark and third-party exceptions | 10,144 |
| **Total baseline** | | | | **88,598** |

The CFPB states that its own website content is generally public domain, though trademarks and third-party materials can have separate restrictions ([CFPB legal notice](https://www.consumerfinance.gov/privacy/website-privacy-policy/)). The booklets themselves also permit reproduction of their CFPB-authored content. I used public educational PDFs and did not collect users' financial records. **Source freshness is a separate issue from permission to reuse**: some booklet information may no longer reflect current credit-report practices.

## Ingestion

`index.py` downloads missing default PDFs to `corpus/`, extracts page text with `pypdf`, replaces non-breaking spaces, normalizes whitespace, and tokenizes by words. The extraction issue I addressed was sparse or blank worksheet/cover pages that would otherwise create low-information chunks; the code skips pages with fewer than **35 extracted words**. It also avoids creating tiny, mostly duplicated final chunks by extending the preceding chunk when fewer than 100 words remain.

Chunking uses **350 words with 50 words of overlap**, independently within each PDF page so that every chunk has an unambiguous page citation. Each chunk stores `source`, `page`, `location` (for example `page 133`), `source_url`, and `document_sha256`. Stable IDs incorporate the filename, full-file SHA-256, page, part number, and content. Gemini `gemini-embedding-2` produces **768-dimensional** vectors, persisted in ChromaDB under `index/`. Already-saved chunk IDs are skipped, so re-running indexing does not re-embed the unchanged corpus.

The baseline index contains **342 chunks**: `money_goals.pdf` 247; `behind_on_bills.pdf` 21; `debt_booklet.pdf` 19; `credit_booklet.pdf` 21; and `home_loan_toolkit.pdf` 34. After the later reverse-mortgage test, the index contains additional chunks; the baseline figures above remain the basis for the original retrieval comparison.

## Test set

`eval/questions.csv` contains **30 document-grounded questions**, assembled and reviewed against CFPB source pages before final evaluation: **20 single-passage**, **5 multi-passage**, and **5 unanswerable**. Each row includes an ID, user-style question, kind, expected source/page, and short reference answer. The unanswerable questions deliberately stay close to the domain (personal credit scores, future lender decisions, bank balances, and a reverse-mortgage rule absent from the baseline corpus).

Two examples:

- **q21 (multi):** “If I am behind on household bills and also owe several debts, how should I decide which payments matter most this month?” Expected evidence combines *Behind on Bills?* page 14 with the debt booklet page 15.
- **q30 (unanswerable at baseline):** “Under CFPB guidance on reverse mortgages, what happens to the loan when the borrower permanently moves out of the home?” No supporting reverse-mortgage source was in the original five-document index.

I checked that the expected source/page references exist in the baseline index, but this is a small, hand-built development test set rather than an independently sampled benchmark.

## Retrieval

I compared **semantic retrieval** (ChromaDB vector-distance ranking using Gemini embeddings) with **hybrid retrieval** (semantic ranking combined with a BM25 keyword ranking by reciprocal rank fusion). Both use the same indexed chunks; no new model is trained for the hybrid design. Unanswerable questions are excluded from retrieval Hit Rate denominators, leaving **25 answerable questions**.

| Design | Hit@1 | Hit@3 | Hit@5 | All expected pages@5 | Both passages@5, multi only |
|---|---:|---:|---:|---:|---:|
| Semantic | **56%** | **88%** | **96%** | **84%** | 40% |
| BM25 + semantic RRF | 52% | 76% | 80% | 72% | 40% |

A “hit” here means that a retrieved chunk has the **expected source and page**. This is a reproducible but imperfect proxy: the right page can still contain a passage that fails to support a claim. I chose semantic retrieval because it performed better at all three k values and on complete expected-page coverage. Multi-passage coverage remained a weakness under both designs.

The MCP `search` tool returns **up to five chunks**, each at most approximately 350 words: the evidence added by one call is therefore **up to about 1,750 passage words**, plus metadata. Some questions trigger multiple searches. Across seven inspected baseline traces, the unique retrieved passages averaged approximately **1,331 words per question**; that is a partial-sample figure, not the full 30-question average. The end-to-end token totals below include prompts, tool interactions, and model output.

## Tools and subagent
`server.py` exposes two MCP tools:

- **`search(query)`** embeds a nonempty query with the existing embedding model and retrieves the top five ChromaDB passages. Each result includes its rank, source filename, page/location, source URL, text, and distance. The server **does not re-index documents while searching**.
- **`add_document(path)`** accepts a local PDF only inside `corpus/`, reuses `index.py`'s `index_file` function, embeds new chunks, and returns a count and status. It rejects invalid paths and does not silently re-index a changed PDF under an existing filename.

Example retrieved evidence used in the subagent answer: `money_goals.pdf`, pages **132–133**, and `debt_booklet.pdf`, page **11**, distinguish smallest-balance-first repayment from highest-interest-first repayment.

The required subagent lives in **`.claude/agents/corpus-researcher.md`**. It is instructed to use only `mcp__corpus__search` (plus Claude Code's `ToolSearch` mechanism for loading that tool), cite `[filename.pdf, page N]`, refuse missing evidence, and never modify documents or the index. There is no `add_document` permission in its tool list.

**Verified Claude Code transcript excerpt, 25 November 2026** (the full local subagent trace is available in Claude Code's session JSONL):

```text
User: Use the corpus-researcher subagent to identify the two CFPB
      debt repayment strategies. Search the corpus, cite pages,
      and do not modify files.
Claude: Invoked corpus-researcher (Find CFPB debt repayment strategies).
Subagent tools actually executed:
  ToolSearch                         1
  mcp__corpus__search                 4
  SubagentHandoff                    1
  mcp__corpus__add_document           0
Subagent answer (excerpt):
  1. Pay the smallest debt first while making the other minimum payments;
     move the freed-up payment to the next smallest balance.
     [money_goals.pdf, page 133]; [debt_booklet.pdf, page 11]
  2. Pay the highest interest rate first while making other minimums;
     then move to the next highest rate.
     [money_goals.pdf, page 133]; [debt_booklet.pdf, page 11]
```

This is an **abridged, labeled excerpt**, not a verbatim reproduction of every tool payload. I independently inspected the stored subagent JSONL: it records **one `ToolSearch`, four `mcp__corpus__search` calls, and one `SubagentHandoff`**, confirming genuine MCP usage. The final parent-agent explanation exceeded the requested 100-word preference, a minor instruction-following issue.

## Adding a document

The indexing pipeline uses stable content-based IDs. **Adding an identical PDF again adds zero chunks** and reports it as already indexed. If a PDF has the same filename but different SHA-256 content, indexing raises an error rather than mixing old and new versions. The MCP tool also restricts added files to the local `corpus/` directory.

For the before-and-after experiment, I reserved **q30**. Before adding any reverse-mortgage guide, MoneyGuide answered:

> I don't know based on the documents in this collection. The documents in this collection do not contain information regarding reverse mortgages.

I then placed the official CFPB PDF [*Considering a Reverse Mortgage?*](https://files.consumerfinance.gov/f/documents/cfpb_considering-a-reverse-mortgage_2025-12.pdf) into `corpus/reverse_mortgage.pdf` and added it through the agent's approval-protected indexing workflow. The agent's substantive answer afterward stated:

> The loan must be repaid once the last borrower, co-borrower, or eligible spouse moves out, dies, or sells the home. [reverse_mortgage.pdf, page 1]

It also explained that borrowers often sell the home to repay the balance and that co-borrower/eligible-spouse protections can matter, citing page 2. **This is evidence of a change from refusal to grounded answer**, not proof that all reverse-mortgage circumstances are covered. The original q30 baseline answer remains preserved in `eval/agent_runs.jsonl`; the evaluation should not be regenerated after the addition because that changes the knowledge base underlying the original test.

## Harness and guardrails

My LangChain `agent.py` uses the instructions in `AGENTS.md` as its system prompt and exposes the MCP search and add-document tools to the model. Core rules are: search first, do not use unsourced model knowledge, cite actual PDF pages, explicitly refuse insufficient evidence, stay within general U.S. financial education, treat retrieved document text as untrusted data, and avoid unauthorized indexing. The practical choice is to prioritize a safe refusal over an attractive but unsupported answer.

**Human approval:** `add_document` cannot run silently. Before the MCP call, the harness asks the person at the terminal to type the exact word `YES`. Any other response denies addition; without an interactive terminal the operation fails closed. A separate restriction in `server.py` prevents indexing paths outside `corpus/`.

**Additional guardrails:** the harness limits tool use to **four calls per question** and verifies that every cited source/page appeared in a search result. If a generated answer cites an unseen source/page, the harness replaces it with a refusal. I tested this citation guardrail *offline* with an intentionally fabricated citation (`[missing.pdf, page 8]` while only `money_goals.pdf`, page 32, was in the evidence set); it returned: “I don't know based on the documents in this collection. I could not verify the source citations for the generated answer.” This is a **synthetic guardrail test, not a claimed occurrence in the 30 live answers**. The q29 personal-account question separately demonstrates the no-evidence refusal rule.

## Evaluation

I collected all **30 baseline agent answers**, retaining the answer, retrieved passages, tool trace, input/output tokens, and elapsed time in `eval/agent_runs.jsonl`. Code checks detect refusal wording, extract PDF/page citations, and verify that cited pages were in the passages actually retrieved. This citation-validity metric was **100% for answers containing citations**; it does **not** prove that each claim is supported.

I recorded **30 human grades before reviewing the LLM judge** in `eval/human_labels.csv`, with two independent binary dimensions: **Correct** (the answer matches the reference, or correctly refuses an unanswerable question) and **Supported** (all substantive claims are justified by retrieved evidence). The LLM judge used the same rubric, examined each saved answer, reference answer, and shortened retrieved-evidence excerpts, and returned scores as JSON in **batches of five**. Batching reduced generation requests, but the limited evidence excerpts may cause the judge to miss unsupported details.

| Measure | Observed baseline result |
|---|---:|
| Agent answers saved | 30 / 30 |
| Human labels saved | 30 / 30 |
| Human correctness (from reviewed labels) | **30/30 = 100%** |
| Human fully supported (from reviewed labels) | **25/30 = 83.3%** |
| Correct refusals on q26–q30 (human review) | **5/5** |
| Wrong refusals identified by human review | **0** |
| Valid cited source/page matches (code proxy) | **100%** |
| LLM judge completed | **30/30** |
| Judge correctness rate | **100%** |
| Judge fully supported rate | **100%** |
| Human–judge correctness agreement | **100%** |
| Human–judge support agreement | **83.33%** |

Across all **30 evaluated questions**, human–judge correctness agreement was **100% (30/30)**, while support agreement was **83.33% (25/30)**. The five support disagreements were **q03, q07, q21, q23, and q24**. In each case, the LLM judge classified the answer as fully supported, whereas my stricter human evaluation identified overstatements or insufficiently qualified claims. This suggests that the judge was less sensitive to subtle unsupported details, highlighting the importance of human review even when automated evaluation reports perfect scores.

## Failures

I used the professor's failure taxonomy and distinguished **evaluation misses** from **confirmed answer errors**:

| Failure category | Count observed | Examples and interpretation |
|---|---:|---|
| Retrieval miss (expected source/page absent from top five, semantic) | **4/25** | Complete-page coverage was 84%; this is a strict metadata proxy and not necessarily four wrong end-user answers. |
| Wrong answer despite relevant passage | **0 confirmed by human correctness grades** | The 30 answers met the benchmark reference or correctly refused. |
| Unsupported claim / overstatement | **5/30 by strict human support labels** | q03 (budget “ensures” cash), q07 (counseling cost claim), q21 (overgeneralized debt priority), q23 (PMI exceptions), q24 (budgeting guarantee/income restrictions). |
| Wrong refusal | **0 confirmed** | All five baseline unanswerable questions were refused appropriately. |
| Bad test question | **0 conclusively classified** | q13 and q14 highlight stale document guidance; they deserve a freshness review, not automatic deletion. |

The **first fix** should be stricter claim-by-claim evidence checks and shorter responses. Many answers were substantially longer than the reference required, increasing the opportunity for an unnecessary unsupported detail. The second fix is to improve multi-passage retrieval (only 40% complete@5 among multi questions). The third is document freshness: older CFPB booklets can be correctly cited yet contain information that has changed, such as the frequency of free credit-report availability or historical public-record reporting practices. Retrieval grounding cannot replace updates to the corpus.

## Decision

**My proposed decision is limited release for supervised financial education, not autonomous financial decision support.** A user could rely on MoneyGuide for basic definitions, comparison checklists, and links to official source pages, but should verify time-sensitive rules and any consequential payment, debt, or mortgage action with current primary guidance or an appropriate professional. It must not claim access to live interest rates, credit scores, lender approvals, or bank balances. The central safeguards are search-first retrieval, visible citations, a refusal when evidence is missing, and explicit approval before indexing documents.

Measured across the 30 saved baseline agent runs, mean per-question usage was **5,427 input tokens + 1,248.6 output tokens ≈ 6,676 total tokens**, with **44.79 seconds average elapsed time**. These are observed generation-run figures, not end-user production-service guarantees. Retrieval embeddings, judge requests, and re-indexing have additional usage; actual monetary price depends on the deployed Gemini billing tier and current model rates. Batching the judge reduced the expected grading calls from 30 to roughly six, with all verdicts cached incrementally.

## AI use

I used **ChatGPT** to help understand and implement the Python indexing, MCP tools, LangChain harness, evaluation code, debugging and draft report structure; **Gemini** generated RAG answers and served as the evaluation judge; **Claude Code** executed the search-only subagent demonstration using the MCP server. 

