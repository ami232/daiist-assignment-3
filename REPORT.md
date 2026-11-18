# Assignment 3 Report

- **Name**: Cloe Chapotot
- **Student ID**: 18549
- **Group**: [BBADBA 5A]

## Use case

The user is IE University students (bachelor's and master's) who want a quick answer about the university's rules. Examples are attendance, grades and appeals, academic integrity, using AI in coursework, and how to report harassment. The answer from the system helps them decide what to do next, such as whether to submit a justification, which deadline to meet, or whether to appeal a grade.

- A wrong answer can cost a student a course or a deadline. For example, wrongly saying an absence is justified, or giving the wrong deadline for submitting a justification (7 days), can lead to a fail grade or a lost appeal. Wrong advice on AI use can lead to an academic misconduct case.
- "I don't know" costs a few minutes: the student asks Program Management or the Virtual Help Desk. So the system should say "I don't know" and point to the right office whenever the documents don't answer the question.


## Corpus

| Document | URL | Date | Licence | Words (approx.) |
|---|---|---|---|---|
| Attendance Policy, Bachelor Programs | https://docs.ie.edu/documents/Attendance_Policy_Bachelor_Programs.pdf | 2026-27 | © IE University, | 1,000 |
| Academic Regulations for Bachelor Degree Programmes | https://docs.ie.edu/www.ie.edu/university/IEU_ACADEMIC%20REGULATIONS%20FOR%20BACHELOR%20DEGREE%20PROGRAMMES.pdf | July 2026 | © IE University, | 16,800 |
| Academic Regulations for Master Degree Programmes | https://docs.ie.edu/IEU_ACADEMIC%20REGULATIONS%20FOR%20MASTER%20%20DEGREE%20PROGRAMMES%202025.pdf | Sept 2025 | © IE University, | 10,200 |
| The IE Student Code of Conduct | https://docs.ie.edu/documents/The%20IE%20Student%20Code%20of%20Conduct.pdf?_gl=1* | 2026-27 | © IE University, | 10,800 |
| Student Guidelines on AI (v4) | https://docs.ie.edu/Student%20Guidelines%20on%20AI_v4.pdf | July 2025 | © IE University, | 1,000 |
| Code for the Prevention of Harassment | https://docs.ie.edu/sustainability/resources/Code-for-the-Prevention-of-Harassment.pdf| 29 July 2009 | © IE University, | 1,900 |
| Equal Opportunities and Diversity Plan | https://docs.ie.edu/sustainability/resources/IE-Equal-Opportunities-and-Diversity-Plan.pdf | 29 July 2009 | © IE University, | 1,800 |
| Environmental Policy | https://docs.ie.edu/sustainability/resources-2021/Environmental-Policy-2025.pdf| 5 Oct 2023 | © IE University, | 2,600 |
| Climate and Sustainability Plan (CASP v3) | https://docs.ie.edu/sustainability/resources-2021/CASP%20v3.pdf | 2025 | © IE University, | 2,000 |
| **Total** | | | | **about 48,000** |

## Ingestion

index.py downloads the 9 PDFs into corpus/ and reads them page by page with pypdf. I clean the text by fixing broken characters, rejoining words split by a hyphen at the end of a line, and removing page numbers, the DocuSign stamp and the tables of contents. I also detect headings, so every piece of text knows which section it belongs to. I tested two chunking designs. The structured design uses chunks of up to 200 words with a 40-word overlap, never crosses an article or section, and ends at a sentence. The fixed design uses 150-word windows with a 30-word overlap and ignores the structure. Each chunk is embedded with its document title and section using gemini-embedding-2 (768 dimensions) and stored in ChromaDB, with each vector saved as soon as it is made.

One extraction problem I fixed: in the Harassment Code and the Equal Opportunities Plan, each page repeated the text of the earlier pages, giving about 9,800 and 8,100 words. I dropped any line of 4 or more words that had already appeared on an earlier page, which brought them down to about 2,200 and 2,000 words, their real length.

Each chunk stores its source, file, url, page range, section path, heading, a short location label, design and chunk index. After cleaning, the corpus is about 49,000 words, and it produces 348 structured chunks and 384 fixed chunks.

## Test set

I wrote 50 questions from the nine documents (each answer checked against the PDF with the help of AI), phrased as a student would ask, with the expected document, location and a short reference answer. The set has 33 single-passage, 10 multi-passage and 7 unanswerable questions. The unanswerable ones are close to the corpus topic but not answered in it, and five of them concern the master’s attendance policy, which is held back for the add-document demo.

Example:
Single (q08): “How long does a bachelor professor have to communicate the grade of an assessment instrument?” Answer: at most 15 calendar days (Art. 35.1 of the bachelor regulations).
Unanswerable (q38): “In a live online session of my master’s programme, do I have to keep my camera on?” The corpus only has the bachelor camera rule, so the assistant should say it can’t confirm this for master’s.

## Retrieval

I compared two chunking designs on the 43 answerable questions. The 7 unanswerable questions are left out, because they have no right passage to find.

Structured: up to 200 words, 40 overlap. A chunk never crosses a section or article, and ends at a sentence.
Fixed: 150-word windows, 30 overlap. Ignores the document structure.
A result counts as a hit when the chunk comes from the expected document and matches the expected article, section or page. For 4 questions (q01, q43, q45, q46), the heading in my label was lost when the PDF was turned into text. For those, a chunk that contains the key fact of the answer also counts.

| Design | Hit@1 | Hit@3 | Hit@5 | Multi: both passages @5 | Words added (k=3 / k=5) |
|---|---|---|---|---|---|
| **Structured** | 0.84 | 0.95 | **0.98** | 0.50 | **430 / 713** |
| Fixed | 0.84 | 0.95 | 0.95 | 0.50 | 447 / 747 |

I chose structured because it ties at k = 1 and k = 3, finds one more question at k = 5, and adds fewer words to the prompt. It also cites by article, which is easier for a student to check. The difference is small (one question out of 43), so I chose it for these reasons together, not for the score alone. There's a weakness with questions that need two passages. In half of them, only one of the two passages reaches the top 5, in both designs.

## Tools and subagent

Tools (server.py):
- search(query) searches IE's student rules and returns the top 5 passages, each with a citation, a relevance score and the text.
- add_document(path) indexes a file through the index.py pipeline. The same file again changes nothing; a changed file replaces its old chunks.

One search result:
[1] Attendance Policy, Bachelor Programs, p. 2, Failing a course due to attendance
relevance: 0.85
Students whose attendance falls below 80% will receive a Fail (0.0) in the ordinary call and extraordinary call...

Subagent instructions (corpus-researcher, search tool only): search once per part of the question, answer only from the results, keep bachelor and master rules apart, and cite every claim. If the answer isn't there, say "I can't find this in the IE documents."

Subagent transcript (Claude Code, `corpus-researcher`, search tool only)

```text
> Use the corpus-researcher subagent to answer: I have a court summons on the day
  of a bachelor exam. Is my absence justified and can I take the exam another day?

corpus-researcher → search("justified absence court summons legal obligation bachelor")
corpus-researcher → search("missed exam due to justified absence take exam another date bachelor")

Answer:
Yes, your absence counts as justified. The bachelor attendance policy lists an
"Official summons to testify before a court or the police, to serve in electoral
duties, or issued by other equivalent authorities" as a justified absence, as long
as you have official documentation. You must submit that documentation to Program
management through the Virtual Help Desk within seven (7) days. If you do, the
absence is validated as justified and does not count toward the 20% maximum absence
limit, and you and your professors get a notification within 72 hours
[Attendance Policy, Bachelor Programs, pp. 1-2, Justified Absences]. Your professors
cannot approve or justify absences. All absence requests go through Program
management [Attendance Policy, Bachelor Programs, p. 2, Additional Provisions].

On retaking the exam, the passages I found don't set a rule for rescheduling an
exam after a justified absence. For an unforeseen absence, the academic heads judge
its importance from your supporting documents and "shall decide on the academic
measures to be taken in each case" [Academic Regulations for Bachelor Degree
Programmes, pp. 16-17, Article 15. "Attending academic activities in the programme"].
The academic heads can also classify you as "absent" in "exceptional and duly
justified circumstances", which stops that exam session from being used up
[Academic Regulations for Bachelor Degree Programmes, p. 38, Article 46. "Ordinary
and extraordinary examination sessions"]. To find out whether you can sit the exam
on another day, ask Program Management through the Virtual Help Desk.
```


## Adding a document

Already indexed: the same file with the same content changes nothing and costs no embeddings. A file with the same name but new content replaces its old chunks.

Test: I held back the Attendance Policy, Master Programs and added it with add_document, after approving it. This ran on a copy of the index, so the evaluation stays reproducible.

q38: "In a live online session of my master's programme, do I have to keep my camera on?"
Before: "I can't find this in the IE documents. … conditions must be detailed in the subject's syllabus [Academic Regulations for Master Degree Programmes, p. 14, Article 17.5]."
After: "Yes, … you are required to keep your camera on for the entire session [Attendance Policy Master Programs, p. 4, LIVE ONLINE SESSIONS]."

q37 and q39 also changed from refusals to correct answers.

## Harness and guardrails

AGENTS.md rules:
search before answering, and answer only from the results;
search once per part of the question;
cite every claim;
keep bachelor and master rules apart;
when the answer isn't there, start with "I can't find this in the IE documents.";
copy numbers exactly;
add documents only when asked.
Approval: add_document pauses until a person types "y". Without a terminal it is rejected. In a test the request was rejected and the index didn't change.

Limits: 6 tool calls and 10 model calls per question.

Extra guardrail, the citation check: every citation must match a passage that search actually returned in that run. If it doesn't, the answer is withheld and replaced by a refusal.

Where it fired: during testing, on q30. The model cited [1, Article 37.1] (a result number instead of the document), so the guardrail blocked it.
What it led to: the answer was actually right, so this was a false positive. I fixed it by adding a cite as: line to the search results and loosening the check. After that it didn't fire in the 50-question run.

## Evaluation

Code checks: valid citations, refusals where expected, and whether the expected document was cited.
Judge (gemini-3.5-flash-lite, a different model from the agent's):
correct: the answer has the key facts of the reference answer (or properly refuses an unanswerable question).
supported: every claim is in the retrieved passages.
Agreement with my own grades: 100% on both correct and supported, over 24 answers.

Results:
| Metric | Result |
|---|---|
| Correct | 38 / 43 |
| Incorrect | 4 |
| Unsupported | 1 |
| Wrong refusals | 0 |
| Correct refusals | 5 / 7 |
| Valid citations | 100% |

## Failures

| Question | Cause | Evidence |
|---|---|---|
| q28 (multi) | Retrieval miss | One search; the second passage (Art. 45.7, the 5.0 minimum Bachelor Score) was not retrieved |
| q29 (multi) | Retrieval miss | One search returned only the AI Guidelines; the Code of Conduct sanctions were never retrieved |
| q46 | Retrieval miss | The "45% of purchasing" passage (climate plan, p. 8) is in the index but did not reach the top 5 in two searches |
| q30 (multi) | Wrong answer from the right passage | Art. 36 (48-hour review, Appeals Board) was retrieved, but the answer left it out |
| q40 (unanswerable) | Answered instead of refusing | It applied general master's rules instead of saying the specific rule is missing |
| q36 (unanswerable) | Bad test question | Art. 42.7 of the master's regulations does answer it; the agent's answer is correct |
| q26 | Judge error, not an agent failure | The statement is in the retrieved passage, but a heading in the PDF splits it, so the judge missed it |

by cause:
| Cause | Count |
|---|---|
| Retrieval miss | 3 |
| Wrong answer from the right passage | 1 |
| Answered instead of refusing | 1 |
| Bad test question | 1 |
| Judge error | 1 |
| Wrong refusals | 0 |
| Invented (unsupported) claims | 0 |

What I would fix first is the questions that need two passages. Four of the five real failures are two-part questions, and the agent averages 1.14 searches per question despite the "search once per part" rule. The fix can be to make the harness split two-part questions and run one search per part, rather than relying on the prompt.

## Decision

I would let students rely on it, expecially for simple questions as they are usually "single" questions which the model hqs answered 33/34 correctly. and when a passage is missing it says so. I would implement the safeguard of always showing the citation of the original document and perhaps when is a multi-part answer, hava a warning so that it encourages the student to look into it further before making a decision. 

Cost and latency: on average, one question took about 4,254 tokens and 5.1 seconds, with 1.14 searches (gemini-3.1-flash-lite). That is fast and cheap enough for students to use day to day. On the free tier it cost nothing, but the limit of about 1,000 embeddings a day would cap usage.

## AI use

I have used Claude for creating code and understanding how to apply the agents to the case in hand. Also, I used it to create to help me match the proper answers from the documents I used for the questions. 
