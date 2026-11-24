# Assignment 3 Report

- **Name**: Juan Felipe Ortiz Lejarde
- **Student ID**: 20417
- **Group**: BBADBA 5A

## Use case


**What Chedar is (public pages: chedar.io, learn.chedar.io)**
I'm an intern at Chedar which is a web SaaS that film and multimedia production companies use to build and track production budgets (chedar.io, learn.chedar.io). It covers estimates, cost tracking, invoicing, supplier invoices and POs, accounting export, and team settings. The help centre we have built has 251 English articles and can be found at  https://learn.chedar.io/en

**Who asks and what they do with the answer**
Producers, production managers, accountants and freelancers at production companies, plus Chedar support staff drafting their replies. Users act on the answer in the app straight away, and many answers end up in invoices, credit notes, e-invoices and accountant exports that leave the company.

**Evidence from real support questions**
92 anonymised questions sampled from 1,864 client questions (2024-01 to 2026-10).

By area: estimates 22, settings and users 20, invoicing and credit notes 18, cost tracking 9, bank and accounting 8, purchase orders 5, supplier invoices 5, payroll and intermittents 5.
61 need one article, 16 need two, and 15 can't be answered from the help centre.
Top topics across all 1,864 (rough keyword counts): splitting VAT rates on a supplier invoice (79), Working vs Actuals tabs (73), inviting a freelancer (62), editing an issued invoice (59).
Frequent but out of reach: pricing and refunds, missing 2023 invoices (36), onboarding material (34), and legal or VAT validity questions.

**Cost of a wrong answer vs "I don't know"**
A wrong answer puts bad steps or tax figures into invoices and filings, which are hard to undo once issued. Users who trust the assistant won't check with support, so the error spreads. "I don't know" plus a referral costs a few hours. So when retrieval is weak, the assistant should refuse. If a bad answer provided by the agents is sent through our support channel, it may impact the reputation with the clients.

**Scope**
- Answers only from the Chedar help centre, with the article URL cited.
- Anything outside it (pricing, refunds, legal or tax advice, account-specific data, bugs) gets a referral to support.

## Corpus

- Source: Chedar help centre, https://learn.chedar.io (English, /en/docs/...)
- Size: 251 articles, 188,216 words (whitespace-split).
- Date fetched: 2026-11-22
- Licence: proprietary Chedar content, indexed and published here with Chedar's permission.



| section | articles | words | example URL |
|---|---|---|---|
| screens | 59 | 105,301 | https://learn.chedar.io/en/docs/screens/account/choose-company |
| film-budget-templates | 26 | 12,130 | https://learn.chedar.io/en/docs/film-budget-templates/360/dependencies |
| suppliers-purchases-purchase-orders | 28 | 10,521 | https://learn.chedar.io/en/docs/suppliers-purchases-purchase-orders/purchases-p-os/add-p-o |
| settings | 20 | 7,628 | https://learn.chedar.io/en/docs/settings/account-settings/3-t-cs |
| invoicing-proposals | 20 | 7,587 | https://learn.chedar.io/en/docs/invoicing-proposals/client/add-client |
| knowledge | 8 | 6,907 | https://learn.chedar.io/en/docs/knowledge/cost-reports |
| estimates | 12 | 5,076 | https://learn.chedar.io/en/docs/estimates/add-ons |
| getting-started | 9 | 5,016 | https://learn.chedar.io/en/docs/getting-started/accounting-first-week |
| actuals | 10 | 4,265 | https://learn.chedar.io/en/docs/actuals/4-exp-type |
| film-budget | 13 | 4,168 | https://learn.chedar.io/en/docs/film-budget/assign |
| purchases | 8 | 3,412 | https://learn.chedar.io/en/docs/purchases/cannot-approve |
| f-a-q | 6 | 2,971 | https://learn.chedar.io/en/docs/f-a-q/f-a-q-budget/bid-letter-automatic-save |
| sales | 4 | 2,341 | https://learn.chedar.io/en/docs/sales/import-clients |
| film-project | 6 | 2,085 | https://learn.chedar.io/en/docs/film-project/create |
| transactions | 5 | 1,825 | https://learn.chedar.io/en/docs/transactions/filter-transactions |
| account | 3 | 1,451 | https://learn.chedar.io/en/docs/account/freelancer-start |
| team | 3 | 1,166 | https://learn.chedar.io/en/docs/team/create-subteam |
| whats-new | 1 | 1,049 | https://learn.chedar.io/en/docs/whats-new/2026-10 |
| dashboard | 2 | 812 | https://learn.chedar.io/en/docs/dashboard/dashboard |
| costs | 2 | 783 | https://learn.chedar.io/en/docs/costs/portfolio-margin |
| templates | 2 | 723 | https://learn.chedar.io/en/docs/templates/edit-template |
| banking | 1 | 341 | https://learn.chedar.io/en/docs/banking/export-transactions |
| ressources | 1 | 280 | https://learn.chedar.io/en/docs/ressources/chatbot |
| accounting | 1 | 258 | https://learn.chedar.io/en/docs/accounting/fec-export |
| introduction | 1 | 120 | https://learn.chedar.io/en/docs/introduction |
| **Total** | **251** | **188,216** | |

- Note: "screens" has 59 articles but over half the words (105,301, 56%). The average article is about 750 words; a screens article is about 1,780.


## Ingestion

`index.py` reads `llms.txt` from learn.chedar.io and uses a regex to collect every English article link (`/en/docs/...`), with duplicates removed. That gives 251 articles. Adding `.md` to each URL returns plain Markdown, so there is no HTML to parse. Each article is saved to `corpus/` as one file, and its first line, `<!-- source: URL -->`, keeps the URL for citations. The crawl has a 0.2 s delay, 3 retries, and files already saved are skipped.

**Cleaning**
- The Markdown is used as is. I manually reviewed the md files to check for any problems after the crawl.
- Embedding inputs get a prefix, because gemini-embedding-2 has no task_type. Documents use `title: <title> | text: <chunk>` and queries use `task: search result | query: <query>`.

**Chunking**
- A: one chunk per heading section, with the heading kept in the text. A section under 120 words joins the next one, and the last one joins the previous. A section over 450 words is split at blank lines.
- B: fixed 350-word windows with a 50-word overlap, ignoring structure. Each window takes the heading path in force where it starts.
- C: hybrid search over A's chunks. It takes the top 20 by vector and the top 20 by BM25 (k1 1.5, b 0.75), merged with reciprocal rank fusion (k = 60).
- Why these sizes: articles average about 750 words, so a 450-word limit keeps most sections whole and still cuts the long ones. Under 120 words, a section is often just a heading and a line or two, too little to match a question. B's 350 words sits in the same range, so A vs B tests structure, not size. These were starting values and were not tuned.

**Metadata and counts**
Each chunk is stored in ChromaDB (cosine space) with `source`, `title`, `section` and `location` (the full heading path, e.g. `# Title > ## Step`). The chunk id is `<file name>#<number>`, which lets reruns skip chunks already embedded. A has 819 chunks and B has 719. C has no collection of its own and uses A's 819.

**Problems fixed**
- Oversized tables and lists: 15 articles had rows with no blank lines between them, making one "paragraph" over 450 words (19 cases: 13 lists, 6 tables). Splitting at blank lines couldn't keep these under the limit, so they're now cut line by line.
- Batched embeddings: gemini-embedding-2 merged a plain list of strings into one input and returned one vector for the whole batch. The code now sends one `Content` per text and raises an error if the number of vectors doesn't match the number of texts.


## Test set

**Source**
I took 36 questions from the 92 anonymised support questions, with names, companies and amounts removed and everything rewritten in generic English. I picked the most frequent ones, some that need two articles, and some the help centre can't answer. The set was written before any tuning.

**What each question has**
Expected source URL(s), expected section and a short reference answer, drafted from the articles and manually reviewed at Chedar

| kind | count |
|---|---|
| single (one article) | 19 |
| multi (two articles) | 11 |
| unanswerable | 6 |
| **total** | **36** |

Retrieval is scored on the 30 answerable questions only.

**Example, multi (q23)**
- Question: "After issuing a deposit invoice, the estimate changed. How do I update the balance invoice without losing the deposit?"
- Expected sources: `.../invoicing-proposals/proposals/proposal-list` and `.../invoicing-proposals/proposals/sync`
- Reference: Click Refresh on the proposal row. It updates the total and recalculates the installments not yet invoiced, and issued invoices (the deposit) are never touched. Then Generate the balance installment, set the dates, tick Mark as ready and Issue invoice.

**Example, unanswerable (q35)**
- Question: "Can I extend my trial period by a few days?"
- Expected sources: none
- Reference: The help centre doesn't cover this. Contact Chedar support.

## Retrieval

A hit means an expected source URL appears in the top-k chunks. For the 11 multi questions, "any" counts at least one expected URL and "all" counts every one. Scored on the 30 answerable questions.

| design | k | hit rate (any) | multi: any | multi: all | avg words added to prompt |
|---|---|---|---|---|---|
| A | 1 | 80% | 64% | 0% | 243 |
| A | 3 | 93% | 82% | 0% | 695 |
| A | 5 | 97% | 91% | 27% | 1195 |
| B | 1 | 83% | 73% | 0% | 286 |
| B | 3 | 90% | 82% | 18% | 828 |
| B | 5 | 93% | 82% | 18% | 1419 |
| C | 1 | 73% | 55% | 0% | 264 |
| C | 3 | 93% | 82% | 18% | 735 |
| C | 5 | 97% | 91% | 36% | 1261 |

- At k=5, A and C tie on hit rate (97%), but C finds every source for more multi questions (36% vs 27%).
- At k=1, B is best (83%) and C is worst (73%).
- B adds the most words to the prompt at every k (1419 vs 1195 for A at k=5) and has the lowest hit rate at k=5 (93%).
- "Multi: all" stays low everywhere (36% at most). Finding both articles is the hard part.


**Chosen design: A (heading sections)**
- The agent reads the top 5. At k=5, A ties with C for the best hit rate (97%) and adds the fewest words to the prompt (1,195, against 1,261 for C and 1,419 for B).
- C finds every expected article for one more multi question (4/11 vs 3/11). On a sample this small, that gain isn't worth running and merging two searches, and C is worse at k=1 (73% vs 80%). B is better only at k=1 and is the worst design at k=5.
- Help-centre articles are already split into headed sections, one per task, so cutting at headings keeps each set of steps in one chunk.

## Tools and subagent

**Tool descriptions** (shortened; full docstrings in `server.py`)

`search(query)`:
```
Search the Chedar help centre (learn.chedar.io) and return the most relevant passages.
[...covers estimates and budget templates, POs, supplier and client invoices, cost
tracking, bank and accounting exports, settings, users and permissions...]
Use this tool for any question about how to do something in Chedar or what a
Chedar feature does, before answering. Write the query in English, as a short
description of what the user wants to do. Search again with other words if the
passages don't answer.
Returns up to 5 numbered passages, best first, each with the article title, URL,
section and a similarity score. Cite the URL and section of every passage you rely
on. If nothing relevant comes back, the help centre does not cover the question.
```

`add_document(path)`: adds one local text or Markdown file to the index through the same chunking and embedding pipeline. A chunk whose id (file name + chunk number) is already stored is skipped, so re-adding a file changes nothing and says so. Only to be called when the user asks, because it spends embedding quota.

**One search result** (query "How do I send a proposal to a client?", design A, all 5 results, chunk text cut to about 30 words)

```
[1] Move an estimate to Proposals
URL: https://learn.chedar.io/en/docs/invoicing-proposals/proposals/create-proposal
Section: # Move an estimate to Proposals
Score: 0.730
# Move an estimate to Proposals Do this when the client has accepted an estimate and you want to bill it. The estimate goes onto the **Proposals** page, where you ...

[2] First steps: from your first project to your first invoice
URL: https://learn.chedar.io/en/docs/getting-started/first-week
Section: # First steps: ... > ## 4. Download the client PDF
Score: 0.728
## 4. Download the client PDF 1. In the estimate, click **Summary**. 2. Click **Preview PDF** to see what your client will receive. 3. Click **Download PDF**. ...

[3] Move an estimate to Proposals
URL: https://learn.chedar.io/en/docs/invoicing-proposals/proposals/create-proposal
Section: # Move an estimate to Proposals > ## What you get
Score: 0.707
## What you get The proposal is a new row with the estimate name, the project, an empty **Client** column and the total. ...

[4] Record the client's purchase order on a proposal
URL: https://learn.chedar.io/en/docs/invoicing-proposals/proposals/add-p-o
Section: # Record the client's purchase order on a proposal
Score: 0.707
# Record the client's purchase order on a proposal When your client sends a purchase order (PO) for an estimate, record it on the proposal before you invoice. ...

[5] First steps: from your first project to your first invoice
URL: https://learn.chedar.io/en/docs/getting-started/first-week
Section: # First steps: ... > ## 6. Issue the first invoice
Score: 0.704
## 6. Issue the first invoice 1. Go to **Proposals**. Your estimate is listed with the status **To invoice**. 2. Click **Generate** on its row. ...
```
- The top two are close in score (0.730 vs 0.728). In Chedar, "proposal" means the billing step, not a document you email, which is why the matches are about estimates and the client PDF.
- The section paths of [2] and [5] are shortened here with "..."; the real output has the full title.

**Subagent** (`.claude/agents/corpus-researcher.md`)
- `tools: mcp__corpus__search` only. It has no `add_document`, so it cannot change the index.
- Description: delegate any question about how Chedar works (estimates, POs, invoicing, cost tracking, exports, settings).
- Instructions, in 4 rules:
  1. Search with a short English description; if the passages don't answer, search once or twice more with other words.
  2. Answer only from the retrieved passages; never guess numbers, tax rates or accounting rules.
  3. Reply in a few lines, with numbered steps for a how-to, and cite URL and section after every claim.
  4. If nothing answers it, say "The Chedar help centre does not cover this" and list the closest articles.

**Transcript from the editor**
Claude Code (desktop app), opened on this repo; run on 2026-11-24. Tool results are shortened with "…".

```
> Use the corpus-researcher subagent to find how to split several VAT rates on one supplier invoice.

● Agent(corpus-researcher) "Split VAT rates on invoice"
    prompt: How do I split several VAT rates on one supplier invoice in Chedar? Search the help
            centre and return a short cited answer (URL + section per claim). If the help centre
            doesn't cover it, say so.

  ⎿ corpus - search(query: "split several VAT rates on one supplier invoice")
      [1] Split VAT rates on a supplier invoice
      URL: https://learn.chedar.io/en/docs/purchases/split-vat
      Section: # Split VAT rates on a supplier invoice
      Score: 0.855
      Some invoices carry several VAT rates, for example 20 % on equipment and 10 % on catering. …
  ⎿ corpus - search(query: "multiple tax rates on a purchase invoice lines")
      [1] Split VAT rates on a supplier invoice
      URL: https://learn.chedar.io/en/docs/purchases/split-vat
      Score: 0.770 …
  ⎿ Done (2 tool uses)

● Short answer: in the supplier invoice, add one line per VAT rate under VAT split. The cost lines
  must add up to the Net amount and the VAT lines to the Tax amount.
  (https://learn.chedar.io/en/docs/purchases/split-vat, section "Split VAT rates on a supplier invoice")

  Before you start: you need the Production manager, Member or Company admin role, and the invoice
  must be in Inbox or In review. A Production manager can only work on invoices in Inbox.
  (same URL, section "Before you start")

  Steps (same URL, section "Steps"):
  1. Go to Supplier invoices and open the invoice.
  2. Check Net amount, Tax amount and Total amount. These cover all the rates together.
  3. In Cost split, set Project and Accounting code (or Estimate cost line), enter the Amount,
     then click + Cost split.
  4. Add cost lines until they add up to the Net amount.
  5. In VAT split, pick the VAT account for the first rate, enter that rate's VAT in Tax amount,
     then click + VAT split.
  6. Repeat step 5 for each other rate. A line that would go over the total is refused with
     "This would exceed the bill total. Reduce the amount".
  7. Click Save as draft, Submit for review, or Approve if there is no review step.

  Points to watch: (3 more cited tips, cut here)
```


- The subagent used only its one tool (`search`), searched a second time with other words (its rule 1), and cited a URL and section for every claim (rule 3).

## ## Adding a document

Full log of the run: `eval/add_document_demo.json`.

**Already indexed**
Chunk ids are `<file name>#<n>`, and `add_document` skips any id already stored. To test it, I asked the agent to add `corpus/film-budget__assign.md`, which was already in the index. I approved the prompt, and the log showed `1 chunks, 1 already stored, 0 to embed`, so nothing was re-embedded and no quota was spent. The agent replied: "The file `corpus/film-budget__assign.md` is already indexed and ready to be searched."

**Unanswerable question (q36)**
"Why does an empty dropdown appear when I try to assign a producer to a new estimate?" The help centre has an article on assigning an estimate, but it never says why the list can be empty or how to add someone to it.

**Document added**
`new_docs/empty-team-member-list.md` is a 340-word draft in the help-centre style, with the sections "Why the list is empty", "Add the person to your team" and "Assign the estimate". I wrote it from the Chedar app's code and English interface text, checked on the work server. Its URL (`.../f-a-q/f-a-q-budget/empty-team-member-list`) is a placeholder, since it isn't a live page. Design A made it 2 chunks, because the short intro merged into the first section. The agent asked for approval before calling `add_document`, I said yes, and the log showed `2 to embed, stored 2/2`.

**Before** (2 searches, nothing relevant found)
> I couldn't find this in the Chedar help centre (learn.chedar.io). Please contact Chedar support for help with this question.

**After** (1 search, found the new article)
> The team member list is empty because nobody has been added to your company's team list yet, or you are signed in as a freelancer (who cannot view the team list) (…/empty-team-member-list, section "Why is the list empty…").
> 1. Go to **Settings → Team**. 2. Click **+ Member**. 3. Fill in the team member's details and role, then save. 4. Open **All estimates**, click the **Assign** icon on the estimate's row, and select the team member. 5. Click **Save**. (each step cites the new article's section)

The after answer is correct and cited, but it gives only 2 of the article's 4 causes. It leaves out freelancer producers and removed members.

## ## Harness and guardrails

**AGENTS.md rules** (loaded as the system prompt)
1. Search before answering, and answer only from results. Why: users act on answers in budgets, POs and accounts, so a plausible guess costs more than "I don't know".
2. Cite the URL and section for every claim. Why: the user can check the article, and uncited answers get replaced anyway.
3. If the results don't answer, say the help centre doesn't cover it and point to Chedar support. Why: a confident wrong answer is worse than a referral.
4. Never guess numbers, tax or legal rates, or accounting rules, and quote them only if a passage states them. Why: they end up in invoices and legal filings.
5. Ask before adding a document, and call `add_document` only when the user asks. Why: it changes the shared index and spends quota.
6. Short answers: one line, then numbered steps in click order. Why: users read it while working in the app.
7. If a question is ambiguous, search the likely meaning and say which one was answered. Why: one answer with its assumption beats a question back.

**Approval step** (`agent.py`)
`NEEDS_APPROVAL = {"add_document"}`. The `approval_guardrail(approve)` middleware (`@wrap_tool_call`) calls `approve(name, args)` before the tool runs. If that returns False, the tool doesn't run and the model gets an error ToolMessage: "The user refused this tool call. Do not add the document; tell the user it was not added." The default approver, `ask_on_stdin`, asks `Allow add_document(...)? [y/N]` in the terminal, and with no terminal (eval, CI) the answer is no. Because the harness enforces it, the model can't skip it. Rule 5 is the soft version of the same check.

**Extra guardrails**
- Call limits: `ToolCallLimitMiddleware(run_limit=6)` blocks further tool calls, and the model answers with what it has. `ModelCallLimitMiddleware(run_limit=8, exit_behavior="end")` is a hard stop for loops.
- Citation check (`citation_guardrail`): if the answer cites no URL that came back from `search` in this run, it is replaced with "I couldn't find this in the Chedar help centre (learn.chedar.io). Please contact Chedar support for help with this question." The one exception is a reply about `add_document` with no search, which has nothing to cite. This stops a fluent answer from general knowledge that cites nothing (rules 1-3).

**One case where it fired** (the "before" run in Adding a document)
For q36 ("Why does an empty dropdown appear when I try to assign a producer to a new estimate?"), the agent searched twice and replied with no citation: "The Chedar help centre does not cover why an empty dropdown appears when assigning a producer to a new estimate. Please contact Chedar support for assistance." The log shows `citation guardrail fired: the answer cited no retrieved URL; replaced it`, and the user got the standard fallback. Since the reply was already a refusal, the guardrail only made the wording consistent. It matters more when the uncited reply is a guess. The same fallback appears for q32 and q35 in the evaluation run, and no trace reached the 6-tool-call limit.

## Evaluation

**Code checks**
- Citation validity: pulls every URL out of the answer and checks that each one was in the retrieved text. Valid only if the answer cites at least one URL and all cited URLs were retrieved. This catches made-up links.
- Refusal check: regex over the lowercased answer for "can't answer" phrases, e.g. "I could not find", "I don't have/know/see", "no relevant information/article/results", "not covered/documented/mentioned", "does not cover/mention/contain", "unable to answer/find/confirm", "no answer".
- Refusal on an unanswerable question = correct refusal. Refusal on an answerable question = wrong refusal.
- It is a keyword match, so it can miss a refusal worded differently.

**LLM judge**
- Model: `gemini-3.5-flash`, temperature 0, structured JSON output.
- Evidence it sees: question, question type, the reference answer, the retrieved text (stated as "the only evidence allowed") and the assistant's answer.

- Rubric, two 0/1 scores:
  - correct: 1 if the answer states the same facts as the reference (wording may differ, extra correct detail fine). For unanswerable, 1 only if it clearly says the help centre doesn't cover it (or asks to add a document) and invents nothing. 0 if it misses a key fact, contradicts the reference, answers an unanswerable question, or refuses an answerable one.
  - supported: 1 if every factual claim (steps, names, numbers, menu paths) appears in the retrieved text. 0 if any claim is missing from it, even if true in general. A refusal with no claims counts as supported.

**Agreement with judge**
- I graded 21 answers myself (`eval/human_labels.csv`): 15 answerable and all 6 unanswerable.
- correct: **81% agreement** (17/21). supported: **100% agreement** (21/21).
- Disagreements (all on correct, all where I gave 1 and the judge gave 0):
  - q09, q11, q13: the steps are right, but the answer leaves out a limit that was in the retrieved article (not finalized / 24-version cap, IBAN, finalized estimate can't move). The judge counts a missing limit as wrong. I count the answer as correct and note the limit, because the user can still do the task. This pattern goes into Failures.
  - q31: the judge followed the "unanswerable" label. I found that the help centre does answer it (the invoice list defaults to 1 January of this year), so the reference was wrong, not the bot.
- The judge is stricter than me on completeness and trusts the labels blindly. On whether a claim is supported, we never disagreed.

**Results (36 questions)**

| measure | result |
|---|---|
| correct (judge) | 25/36 |
| unsupported (judge) | 3/36 |
| correct refusals (code) | 3/6 unanswerable |
| wrong refusals (code) | 1/30 answerable |
| all citations valid (code) | 29/30 answerable |

**Cost and latency**
- Mean tokens per question: 5668.
- Mean seconds per question: 4.7.

## Failures

Failures are counted from my labels where and from the judge. 8 questions failed, plus 1 test-set error.

| Cause | Count | Questions |
|---|---|---|
| Answered an unanswerable question with a guess | 2 | q33, q36 |
| Partial retrieval on a two-article question | 2 | q25, q27 |
| Right article retrieved, key fact left out | 2 | q02, q17 |
| Wrong refusal | 1 | q14 |
| Unsupported claim | 1 | q24 |
| Test-set error (labelled unanswerable, but answerable) | 1 | q31 |

**Per question**
- **q33** (unanswerable): explained the missing discount with a rule the help centre never states, while its own retrieved article suggests the opposite ("discounts carried over"). This is the most dangerous failure, because a user would believe it and never report the bug.
- **q36** (unanswerable): guessed why the dropdown is empty. The guess happens to be right (I checked the app's code), but the help centre never says it.
- **q25** (multi): searched only once, found the FEC export article but not the Team article, and missed the main point (adding the accountant for free).
- **q27** (multi): missed the Wrap Report article, although a retrieved chunk links to it, and cited a URL that doesn't exist (`/actuals/portfolio-margin`), the run's only invalid citation.
- **q02, q17** (single): the right chunk was retrieved, but the answer covered only half the question (q17: "change" but not "reset").
- **q14** (multi): refused, although the retrieved article answers part of it.
- **q24** (multi): the steps are right, but it adds "Viewers can't see supplier invoices", which isn't in the retrieved text.
- **q31**: my labelling mistake, not a model failure (see Evaluation).

**A weakness that isn't a failure**
In 3 answers I graded correct (q09, q11, q13), the bot left out a limit from the chunk it retrieved, such as "the estimate must not be finalized". This has the same root cause as q02 and q17.

**What to fix first**
1. **Refusals on unanswerable questions (highest risk, low effort).** Add a rule to AGENTS.md: if no passage states the answer, don't infer it from neighbouring features, and refer to support. Then re-run the evaluation. A score threshold alone won't work, because the guessed answers had top scores of 0.72–0.79, the same as good ones.
2. **Limits and prerequisites (low effort, most cases).** Change rule 6 so each answer starts with a "Before you start" line from the cited chunk (roles, plan, "not if finalized"). This covers q02, q17, q09, q11 and q13.
3. **Two-article questions (medium effort).** Run one search per part of the question. This targets q25, q27 and q14, and the low "multi: all" score in Retrieval (27%).

## Decision


**Yes: Chedar users can rely on it for how-to questions about the app.**

**What for**
Questions about where to click and in what order (estimates, POs, invoices, settings, team), which is what most real support questions are. Every answer links to the help-centre article and section, so the user can check it in one click, and 29 of 30 answers to answerable questions had all citations valid.

**Not for**
Tax rates, legal validity, accounting rules, billing, refunds, trials, account-specific data or bugs. For these, the assistant refers the user to Chedar support (AGENTS.md rules 3 and 4).

**Safeguards**
- Citation guardrail: an answer with no valid citation is replaced by a referral to support.
- Every answer shows its source links.
- Before a wide rollout: only 3 of 6 unanswerable questions were refused. Add a stricter refusal rule, then re-run the evaluation.
- Re-run the evaluation whenever the help centre changes.

**Cost and latency**
About 5,668 tokens and 4.7 s per question on `gemini-3.5-flash-lite` (mean over 36 questions), against hours for an email to support.

## AI use

**Tools**
- Claude Code (Claude Opus 5.5) as an orchestrator, with subagents (Claude Sonnet) for drafting and code.
- Gemini, inside the system: `gemini-embedding-2` for embeddings, `gemini-3.5-flash-lite` for the agent and `gemini-3.5-flash` as the judge.

**What AI did**
- Wrote the code: `index.py`, `server.py`, `agent.py`, `evaluate.py`
- Fetched the corpus.
- Drafted the reference answers.
- Pulled the past support questions (anonymised, read-only) and read the app's code on the work server for the `new_docs/` article.

**What I did**
- Chose the use case and the test-set source: real support questions, of which I picked the most frequent, the multi-article and the unanswerable ones.
- Asked for permission from chedar
- Chose to compare three designs, and picked the final one.
- Reviewed the reference answers.
- Graded answers for `eval/human_labels.csv`. AI pre-filled grade suggestions on my grading sheet (without seeing the judge's verdicts); I went through every answer and set the final grades myself, changing them where I disagreed (e.g. q25, q27, q31).
- Wrote the failure analysis and made the ship decision.
