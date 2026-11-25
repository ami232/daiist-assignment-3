# **Assignment 3 Report**

**SEC filing account briefs for B2B sales**  
**Name:** Allan Stalker  
**Group:** BBADBA 5A  
**Student ID:** 19004

## **Use case**

My project revolves around building a sales assistant to prepare B2B sellers for meetings with their trucking company clients. The typical questions the seller needs answered are about what the company does, what problems the company is facing, and how its results compare against another competitor. The goal is for a seller to get a quick, verified answer, rather than having to read a company’s entire annual report before a meeting.

The idea originated from a personal use case as I worked as a tech seller at IBM for 3 months and will work there again. One of the biggest bottlenecks experienced sellers told me about was situations where they were starting with a new client or when they had an abundant amount of clients. The sellers said “You know very little about the client, however the information online is abundant and you do not need to know everything about the client either, you need the key information.” So the vision was to be able to walk into a client’s meeting already understanding the clients business and the problems they want to solve. However this takes time doing the manual research, so my project is set out to achieve this in an efficient and accurate manner.

For a seller, the main risk is to give a client the wrong fact or figure, you lose the trust and credibility with the client and hurt the chances of a sale right then and there. If the sales assistant can not find the information, it is programmed to state that, and the seller can look elsewhere. This is far better than the alternative of giving a confident wrong answer.

The vision API session gave me a good view on this. A wrong answer in this case is an “escape”, because it reaches the client. A refusal here is “overkill”, because it only costs the seller a few minutes of checking. An escape costs a lot more than the alternative, so I built the system to prefer overkill. Another key point is that it is augmentation rather than automation. The tool is there to make the seller more efficient, but the seller is still the one speaking in the meeting.

The reason this approach is fit for the use case is that annual reports and filings change often, even some documents every quarter and to keep the tool up to date the seller simply has to add the new files. A fine tune approach would have meant having to retrain the model. A purely LLM based approach would have two main limitations. Firstly, is the hallucination aspect, llms will spit out the wrong information because it is programmed to answer no matter what. Secondly, is the token cost of using the latest models, which is the ones most sellers have available to them.

## **Corpus**

For the corpus I chose four trucking and logistics companies. They are in the same industry, which is a decision which was made to resemble a seller managing a territory with related accounts. Another reason I chose this corpus is that I found the filings easier to follow than some other industries. A company’s SEC filings are very long documents and as a seller you do not need all the information. For increased speed I kept, Item 1 for the business, Item 1A for risks, and Item 7 for results and management’s discussion. I kept these specifically because those are the parts I would actually use to prepare for a meeting and keeping all of the SEC filing makes the tool less efficient and more costly.

| Document | URL | Filed | Licence | Words indexed |
| :---- | :---- | :---- | :---- | ----: |
| Old Dominion Freight Line, FY2025 10-K | [SEC filing](https://www.sec.gov/Archives/edgar/data/878927/000119312526067161/odfl-20251231.htm) | 24 Feb 2026 | Public EDGAR filing, available for reuse | 17,901 |
| J.B. Hunt Transport Services, FY2025 10-K | [SEC filing](https://www.sec.gov/Archives/edgar/data/728535/000143774926005294/jbht20251231_10k.htm) | 24 Feb 2026 | Same | 10,747 |
| Saia, FY2025 10-K | [SEC filing](https://www.sec.gov/Archives/edgar/data/1177702/000119312526067030/saia-20251231.htm) | 24 Feb 2026 | Same | 21,579 |
| Knight-Swift Transportation, FY2025 10-K | [SEC filing](https://www.sec.gov/Archives/edgar/data/1492691/000149269126000016/knx-20251231.htm) | 19 Feb 2026 | Same | 35,547 |
| **Total** |  |  |  | **85,774** |

These are public company filings and do not contain private customer records or anything confidential. The SEC says that public EDGAR filing content can be accessed and reused freely ([SEC Webmaster FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions)). The four Q3 2026 10-Q files were downloaded separately, but were not part of the starting index. They are for the add-document test. That gives a total of 4 documents and 85,774 words.

## **Ingestion**

The filings are HTML files from SEC EDGAR, so in order to use them, I used BeautifulSoup to turn them into text. First I removed hidden XBRL data, page numbers, repeated headers and table of contents lines. I kept tables in a readable form by putting each row on its own line and separating cells with “\|”. I also had to make sure the code found the real Item 1, 1A and 7, rather than the headings in the table of contents.

One issue I came across was that some headings were split into strange words, for example “B USINESS” and “RI SK FACTORS”. This meant that the code was missing sections that I knew were in the filing. I only found this because I read the extracted text before indexing it, which is the first check the class RAG notebook recommends. The fix I used was to join the inline text without adding new spaces. Knight-Swift documents had another issue where the name appeared at the top of almost every page. To work around this, I removed short lines repeated at least eight times so they did not end up in the chunks.

Regarding chunk size, I chose chunks of about 150 words, cutting them near the end of a sentence. They never cross a subheading, and pieces shorter than 40 words get merged back. I wanted one topic per chunk so the search result would be useful by itself and the citation could point to a specific place. Each chunk stores the company, ticker, filing type, period, Item, heading, location and word count. I also put the company and section in the text sent to the embedding model. This helps separate similar wording used by different companies.

In the end, the final index has **701 chunks**. The split by company is 144 from ODFL, 94 from JBHT, 169 from SAIA and 294 from KNX. I used gemini-embedding-2 and stored the vectors in ChromaDB. The index/ folder is about **20 MB**, below the 90 MB limit. Embeddings are saved in batches so reaching the daily free limit does not mean starting over. The code downloads each filing by its fixed SEC accession number, so anyone who runs it gets the same corpus. In MLOps terms that pins the data version.

## **Test set**

For testing, I wrote 30 questions as if I were a seller preparing for meetings, as this is a tool for seller prep. Not all meetings are the same, so I used different situations. The situations included a first meeting, finding a problem my product could solve, preparing for a CFO meeting and comparing two accounts. I wrote the questions and reference answers before running the final evaluation. To ensure the answers I wrote were in the index I used find\_location.py to check.

My test set has **15 single-source**, **7 multi-source** and **8 unanswerable** questions. I chose to make some unanswerable ones because of what I mentioned before, overkill is better than escape, so I needed to test my model did just that. I made some unanswerable ones close to real information to test that it did not escape even in these kinds of situations. For example, J.B. Hunt reports revenue per load, but that does not tell a seller how much it pays BNSF per load. I wrote questions like this because that is the kind of detail I would want as a seller, but the filings cannot give it.

An example of one multi-source question is q21: **Are Old Dominion and Knight-Swift unionized?** My reference says Old Dominion has no employees under a collective bargaining agreement, while Knight-Swift has one at its Mexican subsidiary. An unanswerable example is q25: **How much does J.B. Hunt pay BNSF per load?** The answer I expect is that the filings do not cover it.

To improve my test set, I did a review check. During review I changed q21 and q22 because they repeated passages from other questions and I wanted to test different passages and not focus on the same ones. Additionally, I replaced three easy vendor questions and changed q19 so it asked about investing cash instead of capital spending. A great lesson I learned during the writing of the test question was that I realised how easy it is to ask something slightly different from what a filing actually reports. An important limitation to acknowledge is that, the RAG notebook from class says a small set like this is enough to compare settings in class, but a production system needs a few hundred real user questions. That is the main limit on every number below.

## **Retrieval**

For the retrieval part, I compared four ways of searching the same chunks. Dense search uses the embeddings to match meaning. Hybrid combines that with BM25 keyword search. I tested both with and without a filter for the company named in the question. This did not require embedding the documents again.

| Design | hit@1 | hit@3 | hit@5 | Multi all@5 | Words@5 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Dense | 73% | 100% | 100% | 100% | 648 |
| Dense \+ company filter (chosen) | 73% | 100% | 100% | 100% | 648 |
| Hybrid | 59% | 77% | 86% | 57% | 614 |
| Hybrid \+ company filter | 59% | 82% | 91% | 71% | 604 |

Here, hit@k is the percentage of the 22 answerable questions where an expected passage was in the top k results. It is a form of recall, how often the evidence the model needs is in what it gets. Multi all@5 means both required passages were retrieved for a comparison question. Words@5 is the average text added to the model’s prompt.

With only 22 answerable questions these numbers are noisy, so I used a bootstrap (1,000 resamples of the questions) to get 95% intervals, as in the data pipelines and MLOps sessions. Dense \+ filter beat hybrid \+ filter at hit@3 by between 4 and 36 points, so that gap is bigger than the noise because even in the unluckiest case, dense \+ filter still wins by 4 points. Dense and dense \+ filter got the same result on every question, so the numbers cannot choose between them. My hit@1, which is first result accuracy, was 73% and has an interval of 55% to 91%. I reran the whole evaluation again after adding version tracking, and every retrieval number came out exactly the same. That is what should happen, because search does not involve a model writing text.

In the end, I chose **dense \+ company filter**. I chose it because it has the same scores as dense alone (the highest) and the filter stops a question about one company from pulling figures from another. That is key when a seller is comparing accounts. It is important to note that this assumes the seller names the company. Due to the results being the same the final decision is a business choice. I believe that the hybrid did worse because words such as “drivers”, “2025” and the company names appear in lots of places and hybrid adds a keyword search and gives higher scores to any words in question which match text. So if you ask “What does Saia say about hiring drivers?”, keyword search ranks higher in any chunk with “Saia” and “drivers”, even the wrong ones. Hit@1 was only 73%, but hit@3 reached 100%, so I kept five results in the search tool. The RAG notebook suggests the same: retrieve generously, then check the answers.

## **Tools and subagent**

I wanted the seller’s questions to always go through the filings and never through the model’s memory. Server.py is the link between the model and my index. It gives the model two tools, search and add\_document. The model never sees my code. It only reads each tool’s description, so the descriptions are important because they tell it when it should search and when it can add a document.

**Tool descriptions (from server.py):**

search(query, company="")

Search the annual reports (SEC Form 10-K, fiscal 2025\) of four US trucking and  
logistics companies: Old Dominion Freight Line (ODFL), J.B. Hunt Transport  
Services (JBHT), Saia (SAIA) and Knight-Swift Transportation (KNX). The corpus  
holds Item 1 (business: services, segments, customers, strategy, employees,  
equipment), Item 1A (risk factors) and Item 7 (management's discussion of 2025  
results, costs, capital spending and outlook), plus any document added later.

Use it before answering any question about these companies. Ask one specific  
question per call; for questions about two companies, search once per company.

Args:  
    query: the question in plain words, e.g. "Saia capital expenditure plans for 2026".  
    company: optional ticker (ODFL, JBHT, SAIA or KNX) to search only that company.

Returns up to 5 passages, best first. Each starts with its citation,  
\[source, location\], e.g. \[SAIA 10-K 2025, Item 7 \> Outlook\]. Cite answers with it.

add\_document(path)

Add one SEC filing (an EDGAR .htm file of a 10-K or 10-Q) to the searchable corpus.

The file is cleaned, cut into chunks with their source and location, embedded  
and stored in the index, so search finds it from then on. If a filing with the  
same company, form and period is already indexed, nothing is added.

Args:  
    path: path of the file on this computer, e.g. "corpus/SAIA\_10-Q\_2026-09-30.htm".

Returns what was added: the source label, the number of chunks and sections.

I also made the corpus-researcher subagent in .claude/agents/corpus-researcher.md. I instructed it to use only mcp\_\_corpus\_\_search, search each company separately, give citations and refuse when the filings did not answer. In VS Code Copilot Agent mode, I tested it with the Saia expansion question. It delegated the task and returned four cited points from Item 1A.

There was a limitation in that test. Copilot also searched and read a temporary copy of the returned result. This suggests VS Code did not fully enforce the search-only restriction written in Claude Code’s subagent format. The final answer still came from the filing, but I would not claim the tool restriction worked perfectly.

**Search result example:** for q13, the Saia Item 7 result reports **\$544.1 million** in net capital expenditures in 2025, with a citation to \[SAIA 10-K 2025, Item 7 \> Years ended\]. These are the first two of the five passages it returned for search(company=“SAIA”, query=“capital expenditures 2025 additions to property and equipment”):

\[SAIA 10-K 2025, Item 7 \> Years ended\]  
Land and structures: Additions \| \$208.2 \| \$504.0 \| \$267.3 Sales \| (19.5) \| (0.2) \|  
(0.1) Revenue equipment, net \| 312.0 \| 473.1 \| 133.3 Technology and other \| 43.4 \|  
64.0 \| 36.7 Total \| \$544.1 \| \$1,040.9 \| \$437.2 In addition to the amounts disclosed  
in the table above, the Company had an additional \$10.5 million in capital  
expenditures for revenue equipment that was received but not paid for prior to  
December 31, 2025\.

\[SAIA 10-K 2025, Item 7 \> Years ended\]  
The Company was in compliance with its debt covenants at December 31, 2025\. Net  
capital expenditures pertain primarily to investments in tractors, trailers, other  
revenue equipment, information technology as well as land and structures.  
Projected net capital expenditures for 2026 are expected to be \$350 million to  
\$400 million compared to 2025 net capital expenditures of \$544.1 million. \[...\]

The full result and tool trace are saved in eval/answers.json.

**Subagent instructions (.claude/agents/corpus-researcher.md):**

\---  
name: corpus-researcher  
description: Answers questions about Old Dominion, J.B. Hunt, Saia and  
  Knight-Swift from their SEC filings (10-K business, risk factors, MD\&A),  
  with citations. Use it for any fact about these trucking companies, e.g. to  
  prepare a sales meeting.  
tools: mcp\_\_corpus\_\_search  
\---

You research four US trucking and logistics companies (Old Dominion Freight  
Line, J.B. Hunt, Saia, Knight-Swift) in their SEC filings. You receive one  
question.

Use only the \`search\` tool. Search once per company or topic the question  
involves, with a short specific query; pass the company's ticker (ODFL, JBHT,  
SAIA or KNX) when the question is about one company.

Reply with a short answer, at most five sentences, built only from the passages  
the tool returned. Put the passage's citation, exactly as printed (e.g.  
\`\[SAIA 10-K 2025, Item 7 \> Outlook\]\`), after every claim. Copy numbers exactly  
as written. If the passages do not answer the question, reply "The filings I  
have do not cover this." and say what you searched. Never answer from memory.

**Transcript (VS Code, GitHub Copilot, Agent mode):**

Prompt: *Use the corpus-researcher subagent to answer: What could go wrong with Saia’s expansion plans?*

Search Tools

search  
Completed with input: {  
  "company": "SAIA",  
  "query": "What risks could threaten or delay Saia's expansion plans, including  
            opening new terminals, ramping capacity, costs, execution,  
            competition and demand?"  
}

Delegated task

Search for \`^\\\[SAIA 10-K 2025\|terminal\|expansion\|profitable\|employees\|labor\|capital\`

Read , lines 1 to 12  
Completed with input: {  
  "path": "/var/folders/.../T/1794493231487-copilot-tool-output-5e32...txt",  
  "view\_range": \[1, 12\]  
}

Saia's 2025 10-K flags several risks to its expansion plans:

\- New terminals or markets may not open as planned or become profitable, while  
  requiring significant investment in facilities, equipment, technology, staff,  
  and startup costs. \[SAIA 10-K 2025, Item 1A \> Business and Operational Risks\]  
\- Expansion costs may arrive before the additional revenue; higher-than-expected  
  costs or lower revenues could depress profitability and strain liquidity and  
  cash flows. \[SAIA 10-K 2025, Item 1A \> Business and Operational Risks\]  
\- Growth could disrupt existing operations or customer service, and divert  
  management attention from running the business. \[SAIA 10-K 2025, Item 1A \>  
  Business and Operational Risks\]  
\- Real-estate shortages, permitting delays, equipment supply disruptions, or  
  increased union-organizing risk could add costs or limit capacity and  
  expansion. \[SAIA 10-K 2025, Item 1A \> Business and Operational Risks\]

The full transcript is also saved in eval/subagent\_transcript.md.

It is interesting to note that I made one small change outside my own files. For the GitHub check in .github/workflows/verify.yml, it failed at first even though my key worked. The MCP only passes a short list of safe environment variables to the server it starts, so server.py could not see the key that GitHub stores as a secret. On my laptop it reads .env instead, which is why check.py passed there. I added one step that writes the secret into a temporary .env on GitHub’s machine before the check runs, and then it passed.

## **Adding a document**

For add\_document I decided that if a filing is already indexed, the tool should not add it again. In order to ensure that, it checks the company, form and reporting period. I chose this because duplicate chunks could appear several times in the top five and push out a different useful passage. The tool should tell the seller it was already there rather than adding a duplicate.

I tested adding a file with q30: **How much revenue did Knight-Swift report in Q3 2026?** At first, the index only had the 2025 10-Ks, so the answer was:

The filings I have do not cover this.

I then approved adding corpus/KNX\_10-Q\_2026-09-30.htm. The tool added **144 chunks** from Item 2, MD\&A. The first answer after adding it was withheld because the model changed a number from thousands into a full dollar amount. After I changed the agent rule about numbers, the answer was:

Knight-Swift reported total revenue of \$2,200,926 thousand in the third quarter of 2026 \[KNX 10-Q 2026-Q3, Item 2 \> Key Financial Data and Operating Metrics\].

This was a positive result as this is what I was looking for from the test. The information was not available before and became answerable once the right filing was indexed. The full sequence, including the first failed answer, is in eval/before\_after.md.

After the test I retired the 10-Q again with index.py \--remove “KNX 10-Q 2026-Q3”, so the index matches the 10-Ks my test set was written for. The RAG notebook makes the same point about keeping the knowledge base current: when a new version of a document arrives, the old one has to be retired, or search keeps returning it. In real use, next year’s 10-K would replace this one, and the period stored with each chunk tells the seller which year a fact is from.

## **Harness and guardrails**

My LangChain harness uses AGENTS.md as the system prompt and connects to the MCP server. The three rules I cared about most were to search before answering, cite every factual claim, and say **“The filings I have do not cover this.”** when there is no answer. This is key as not doing these 3 is what kills a sale. I also told it to keep the company and year clear, avoid guessing, search separately for comparisons and keep replies short. Each of the 10 rules in AGENTS.md has its reason written next to it. I wrote these from the point of view of a seller who needs information they can check so it can best resemble the actual use case.

The add\_document tool needs approval. The harness asks Allow add\_document({…})? \[y/N\] before running it. In evaluation I set this to deny, since a test should not quietly change the documents it is being tested on. I also set a limit of eight model calls for a question to stop loops.

My extra guardrail checks numbers in the final answer against the retrieved passages and the user’s input. If a number with at least two digits is not there, the answer gets withheld. I added this because a made-up figure is probably the worst mistake the bot could make for my use case. The same rule is in AGENTS.md, but the text generation notebook warns that a system instruction is not a guarantee and should never be the only thing enforcing a business rule. That is why the check is in code.

It caught a problem in q18. Knight-Swift’s filing gave **\$7,469,689 thousand**, but the model changed it to **\$7.47 billion**. That may be a reasonable conversion, but it broke my rule to copy the reported figure. The guardrail withheld the answer. q19 had the same problem when it multiplied **\$366,411 thousand** into dollars. I decided to keep the guardrail strict rather than let it convert units. I then made rule 3 clearer: copy the figure and unit exactly. Rerunning q18, q19 and the Q3 question after this change worked. The same notebook warns that summaries are especially prone to merging or rounding numbers, and that is exactly what happened here. In the full rerun described under Evaluation, q19 passed but q18 was withheld again, because the model added its own “\$7.47 billion” even with the new rule. So the rule helped, but the check in code was still needed.

Borrowing again from the vision API session, the system now has three answers instead of two: answer, refuse, or escalate to a person with “Answer withheld, check the filings”. The call limit works as the budget guard from that session, and the code caches answers, query vectors and embeddings so a rerun costs nothing. Every answer is also stamped with the prompt version and model and logged in logs/requests.jsonl, so a bad answer can be traced back, which is what the MLOps session recommends for LLM applications.

## **Evaluation**

Regarding the evaluation, I tested the full agent on all 30 questions, before adding the 10-Q. First I used code checks to see whether the agent searched, whether it refused when it should and whether its citations matched retrieved locations. Then an LLM judge, the “LLM as a judge” idea from the agents session, compared each answer with my reference answer and passages. The judge used gemini-3.5-flash, while the answering agent used gemini-3.5-flash-lite. The judge graded five answers per request because the free tier only allows 20 judge requests a day.

I wrote the judge rubric to be strict. **Correct** means the answer has every point in my reference, with the right figures, company and year. Missing one point gives a 0, even if the answer is partly right. **Supported** means every claim is in the retrieved passages and the citations point to those passages. A refusal or a withheld answer is supported, but withholding an answer that exists is not correct.

I graded all 30 answers myself before looking at the judge’s results. With the first draft rubric, agreement was **87% for Correct** and **97% for Supported**. It was too generous with incomplete answers. With my revised rubric, agreement rose to **97% for Correct** and **100% for Supported** on all 30 answers. The judge caught a missing outside-carriers point in q09 that I had first accepted. I re-read it and changed my grade. q08 was the only answer where we still disagreed.

| Measure | Official run result |
| :---- | :---- |
| Questions tested | 30 |
| Fully correct, my grades | 21 / 30 (70%) |
| Correct, revised AI judge | 22 / 30 |
| Human Supported grades | 30 / 30 |
| Unsupported claims in revised judge results | 0 / 30 |
| Correct refusals on unanswerable questions | 8 / 8 |
| Wrong refusals | 0 |
| Answers to unanswerable questions | 0 |
| Answers withheld by numbers guardrail | 2 (q18, q19) |
| Invalid citations found by code | 2 (q12, q14) |
| Code checks passed | 26 / 30 |
| Mean answer time | 10.6 seconds |
| Mean tokens per question | 4,093 |
| 95% interval, my grades | 53% to 87% |
| 95% interval, AI judge | 57% to 90% |
| Coverage: answered without refusing or escalating | 20 / 22 answerable |
| Correct among those answered (AI judge) | 14 / 20 |

For a seller, the strong part is that the bot did not invent answers to questions the filings could not cover. The weaker part is completeness. It often found the right passage but left something out. Also, the judge agreement is not the same thing as answer accuracy. It tells me the judge mostly grades like I do. Results are in eval/results.csv, eval/summary.json, eval/human\_labels.csv and eval/judge.json.

The intervals matter. With 30 questions, my 70% has a 95% bootstrap interval of 53% to 87%. The honest summary is that somewhere between half and nine in ten answers are fully right, and more questions would narrow that.

**Testing the fix as a new version.** The MLOps session says a prompt change is a new version and should be compared on the same test cases before it is promoted. So I ran all 30 questions again with the new rule 3 (run v2-rule3, prompt version c6755045 instead of 537ac78b) and judged them with the same rubric. The fix did what it was meant to do for q19, which now gives \$366,411 thousand and passes, so withheld answers fell from 2 to 1\. But overall the judge scored 20 of 30 instead of 22\. The 95% interval of that difference was \-23 to \+10 points, so the change is within the noise and I cannot say either version is better.

I read the four answers that went from correct to wrong (q04, q11, q14 and q15). None of them was wrong or unsupported. Each one left out a smaller point my reference asks for, either the 1989 start of the BNSF partnership or the percentage change from 2024\. Across all 30 answers, v2 gave a percentage 12 times compared with 19 times in v1. My guess is that telling the model to copy figures exactly made it add fewer extra figures, but one run cannot prove that, because the model’s output changes from run to run anyway. q20 shows the judge varies too. It passed in v2 with an answer that still leaves out the third party point it failed on before. v2 also took 27.7 seconds per question instead of 10.6, but that came mostly from free tier rate limits during the run, not from the prompt. Each run is logged in eval/runs.csv with the prompt, models, retrieval design, index size and test set version that produced it, so any number in this report can be traced back. The main run shows “not recorded” for the prompt because its answers were made before I added the version stamps.

## **Failures**

| Cause | Count | Questions |
| :---- | :---- | :---- |
| Retrieval miss | 0 | None |
| Wrong answer from right passage | 4 | q01, q06, q08, q09 |
| Unsupported claim | 0 | None |
| Wrong refusal | 0 | None |
| Bad test question | 3 | q02, q20, q21 |
| Withheld by guardrail after unit conversion | 2 | q18, q19 |

Firstly, the main thing I found is that **search was not the problem**. Dense \+ filter found the expected passages for all 22 answerable questions within the top three. Most mistakes happened when the model wrote the final answer. In q06 it left out what higher driver pay could mean for profits and fleet growth. In q09 it missed outside carriers. q08 is still the one I disagreed about with the judge. My reference expects it to say expansion may never pay off, while the bot discussed costs and delays without saying that clearly.

I also made mistakes when writing the test itself. In q02 I asked how many terminals Saia had, but my reference also expected offices and a warehouse. q20 and q21 had the same issue, where I expected details beyond the question. Under my strict rubric these failed. I kept the grades rather than changing the test after seeing results, but I would write those references more carefully next time.

Most of the risks in the RAG notebook’s “what can go wrong” list show up in this project: bad extraction (fixed in ingestion), similar passages from different companies (the company filter and the titles), questions that need several passages (five results and one search per company), unanswerable questions (the refusal rule), prompt injection (rule 9\) and wrong citations (the merged headings).

One limit of my own process: I chose the retrieval design and the rule 3 fix while looking at the same 30 questions I report on. The MLOps session warns that the test set should confirm a choice, not make it, because choosing on it flatters the result. A fair next step is a fresh set of questions written after these choices, and used only once.

The most important fix was the unit conversion problem in q18 and q19. I chose to fix the instruction while keeping the guardrail strict because a wrong figure could actually hurt a seller in a meeting. I would next work on making the answers more complete for broad risk questions. I would also fix the two citations where the model combined headings into a location that did not exist exactly in the index.

## **Decision**

**My decision is a limited yes. I would use this as a first research tool for meeting preparation, but not as something a seller can quote without checking.** It is useful for quickly understanding the client’s business, risks and results. It is also useful when comparing the four accounts. For example, comparing the four gives me a rough idea of what is normal in the industry. The 100% hit@3 result and the 8 out of 8 correct refusals make me comfortable using it to find where to look. So there is a lot of value in speeding up a large part of the research process and creating an overall view of the company.

However, only 21 of 30 answers were fully correct by my grading. I would not trust it to give every detail from a long risk section, and I would always open the citation before using a financial figure in a real meeting. The key is that anything I want to use in a meeting directly with a client must be checked, but using it for my general understanding, to feel more prepared, is a good use. I would also not use it for people to contact, contract terms, private CRM notes or recent news. Those are outside its documents. It also depends on the seller’s experience level in the industry. A seller with a lot of experience knows roughly what these values should be, so they can quickly spot a number that looks wrong and check it. A new seller does not know the industry yet, so they might not notice when an answer leaves something out.

The safeguards I find the most value in and would keep are the citations, the number check, and refusing instead of guessing. I would also make the seller name the company in the question because my chosen retrieval filter depends on that. Sellers would also need some training to use the tool well, for example always naming the company. During testing a question took 10.6 seconds and about 4,093 tokens on average, about 3,900 in and 200 out. It ran within the free tier, so there was no API bill in these tests. At paid prices of about \$0.30 per million input tokens and \$2.50 per million output tokens ([source](https://eesel.ai/blog/gemini-3-5-flash-lite-pricing)), that is roughly \$1.70 per 1,000 questions. For the few minutes before a meeting, the speed is fine.

For the prompt, I followed the MLOps rule. v2 did not beat v1 by more than the noise, so on the numbers alone it should not be promoted. I kept it in AGENTS.md anyway, because it targets the costliest error, a figure the filing does not show, and it never made an answer wrong or unsupported. The main results in this report come from v1, and v2 is logged as its own run. Before calling v2 an improvement, I would run each version several times and add a rule to give the change from the year before when the filing reports it. If a sales team used it, I would keep logging every request with its versions, re-index each quarter when new filings come out, and only promote a new prompt if it beats the current one on the same test cases by more than the noise. Overall, the human still checks anything important, and the tool is not a starting point for a new seller but an advantage for sellers who already know the industry. Once new sellers learn the industry and what to expect, they can use it with less risk, because their checks come from experience.

## **AI use**

I acknowledge the use of Claude, to write and debug most of the Python code in index.py, retrieve.py, server.py, agent.py and evaluate.py, starting from the class examples. The prompts used include asking it to suggest a public corpus that fits my use case, check my test question locations against the index, and review my report drafts against the grading criteria and the class material. The output of these prompts was used as the code in this repository and as review comments on my writing. The decisions were mine: the use case, the companies and sections, the test questions and reference answers, the retrieval design, the AGENTS.md rules, the judge rubric, my 30 grades, how to fix the unit problem, and the analysis and decision in this report. I wrote the report and had an AI proof check, fix grammar and make sure it was clearly communicated. I ran everything on my own laptop and made sure I understand how each part works.Overall, I would frame my use of AI as an execution tool. I have the idea, the decisions and AI would be here to help me build the project and improve my understanding.

