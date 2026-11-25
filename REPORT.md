# Assignment 3 Report

- **Name**: Rakan Hourani
- **Student ID**: 19907
- **Group**: BBADBA 5A 

## Use case


I decided to build this assistant for a freelance web developer, who builds things like logins, sessions and file uploads for clients and doesn't have a security team to check in with. They are able to use the answer straight in their code, like to choose a hashing setting or configuring a cookie.

Since the answer goes straight into the client's app, a wrong answer means shipping a vulnerability, which could lead to stolen accounts or leaked data. If the assistant says it doesn't know, the developer only loses a few minutes checking the official OWASP guide, so a refusal is much cheaper than a confident wrong answer, and this is why the assistant is built to say when the documents don't cover a question.

## Corpus

The corpus is made up of 15 OWASP Cheat Sheets, which are practical security guides written by the OWASP community. I downloaded them from the OWASP GitHub repository at a fixed version so the results can be reproduced. They contain no personal data.

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Authentication | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 5 301 |
| Password Storage | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 2 913 |
| Forgot Password | https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 1 532 |
| Multifactor Authentication | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 5 293 |
| Session Management | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 7 850 |
| Cross-Site Request Forgery Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 6 678 |
| Cross Site Scripting Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 4 288 |
| SQL Injection Prevention | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 1 729 |
| Input Validation | https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 1 186 |
| File Upload | https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 2 048 |
| HTTP Security Response Headers | https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 2 781 |
| Content Security Policy | https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 2 307 |
| Server-Side Request Forgery Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 3 625 |
| Secrets Management | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 7 461 |
| Logging | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | 25/11/2026 | CC BY-SA 4.0 | 4 257 |
| **Total** | | | | **59 249** |


## Ingestion

The cheat sheets are Markdown files, so I cleaned them into plain text by removing links (keeping the text), images, HTML tags and comments. I also dropped the ‘References’ sections since they are only lists of links. Then I split each document by its headings, so that every piece of text knows which section it belongs to.

I fixed two extraction problems. The main one was that when I removed HTML tags it was also deleting code examples. I fixed this by protecting the code before removing the tags. The second was that comment lines starting with # inside code blocks were being read as headings, which created fake sections. To fix this, the code was adjusted so that headings inside code blocks are skipped.

I compared two ways of chunking. The first one cuts the text every 250 words with a 50 word overlap and ignores the structure. The second one keeps one section per chunk, splits sections longer than 300 words at their paragraph breaks, joins sections shorter than 60 words to the next one, and adds the document title and section path in front of the text it embeds. Every chunk stores its id, document, section, URL and word count. The embeddings are made with gemini-embedding-2 and each one is saved as soon as it arrives, so running the index again only embeds the new chunks.


## Test set

I wrote 34 questions from the documents, each one with the document and section that answers it and a reference answer. 22 are answered by one passage, 6 need two passages and 6 are unanswerable, meaning they are close to the topic but the corpus does not cover them. In order to make sure they were really unanswerable, I searched all 15 documents for these terms and none of them came up.

Two examples:
Single: ‘What iteration count should I use for PBKDF2 with HMAC-SHA256?’, which is answered by Password Storage > PBKDF2 (600 000 iterations).

Two passages: ‘Is the SameSite cookie attribute enough to protect against CSRF, and which value should my session cookie use?’, which needs the CSRF cheat sheet and the Session Management cheat sheet.

## Retrieval

I measured how often the passage that answers each question is in the top 1, 3 and 5 results of search, for the 28 answerable questions, before the agent is involved.

| Design | Hit@1 | Hit@3 | Hit@5 | Both passages found (two-passage questions) | Words added to the prompt (k=5) |
|---|---|---|---|---|---|
| Fixed 250 words + vector search | 0.857 | 1.000 | 1.000 | 1.000 | 1 217 |
| Sections + vector search | 0.929 | 1.000 | 1.000 | 0.833 | 801 |
| Sections + hybrid search (vector + keywords) | 0.750 | 0.964 | 1.000 | 0.667 | 839 |

All three designs find the right passage within the top 5 for every question, so I chose between them on the top 1 and the size of the prompt. Sections with vector search finds the right passage first 93% of the time and adds about 400 fewer words to the prompt than fixed chunks, which makes each question cheaper. Fixed chunks were better at finding both passages of the two-part questions, since their bigger chunks sometimes hold both, but this did not make up for the extra words. Hybrid search did worse than expected, since the keyword part pushed up chunks that repeat words like ‘password’ or ‘session’ without answering the question. I chose sections with vector search and k=5.

## Tools and subagent

The MCP server has two tools. The search tool’s description says what the corpus covers, when it should be used, and that it returns the 5 best passages, each with an id to cite, its cheat sheet and section, and its URL. The add document tool’s description says that it takes the path of a Markdown or text file, runs it through the same pipeline as the index, and what happens if the file is already indexed.

One search result, for ‘What iteration count should I use for PBKDF2 with HMAC-SHA256?’, starts with:
[Password_Storage_Cheat_Sheet:014] Password Storage Cheat Sheet > Password Hashing Algorithms > PBKDF2 URL: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html ... PBKDF2-HMAC-SHA256: 600,000 iterations (recommended) ...

The agent then answered: “For PBKDF2 with HMAC-SHA256, you should use 600,000 iterations [Password_Storage_Cheat_Sheet:014], [Password_Storage_Cheat_Sheet:001].”

The subagent, corpus-researcher, only has the search tool. Its instructions tell it to search before answering, to answer only from the passages, to cite the id after every claim, and to reply ‘The corpus does not cover this’ when the passages do not answer the question. 

## Adding a document

If a file with the same content is already indexed, nothing happens and the tool says so, since the content is compared through its hash. If a file with the same name but different content is added, its old chunks are replaced so that the index never keeps two versions of the same document. In addition, the evaluation hides added documents, so that the test always measures the same corpus.

The unanswerable question is q29, ‘How do I implement PKCE in an OAuth 2.0 authorization code flow?’, and the agent correctly refused it in the evaluation. The document that answers it is OWASP’s OAuth2 Cheat Sheet, which the index stage downloads to corpus/to_add/ without indexing it. The tool was tested with approval refused (nothing is added) and approved (12 chunks added).

## Harness and guardrails

The agent is built with LangChain’s create_agent on Gemini and uses the tools from my server over MCP. AGENTS.md is its system prompt and has 7 rules, each with a reason. The main ones are to search before every answer, since the model’s own memory of security advice could be wrong, to answer only from the passages, to cite every claim with its passage id, and to reply ‘The corpus does not cover this’ when the passages do not answer it, because a confident wrong answer costs more than a refusal.

The add document tool never runs until a person approves it. The agent stops, shows which file it wants to add, and only continues if the person types yes. In the evaluation nobody approves it, so it cannot change the corpus. In addition, the agent is limited to 6 model calls and 4 tool calls per question so that it cannot loop forever.

My extra guardrail is a citation check. After the agent answers, the code checks that the answer cites at least one passage and that every cited id was actually returned by search in that run. If not, the answer is replaced by a refusal, because an answer without a real source cannot be trusted for a security decision. It did not fire during the evaluation, since every answer cited passages that search returned. It did fire when I tested it with an answer that had no citation and with one that cited a made-up id, and in both cases the answer was replaced by a refusal.

## Evaluation

The evaluation checks every answer in code first: whether it is a refusal (it starts with ‘The corpus does not cover this’), and whether every citation points to a passage that search actually returned. Refusals are graded by code, since a refusal is only correct if the question is unanswerable. The other answers are graded by Gemini as a judge with a rubric: an answer is correct if it gives the key facts of the reference answer and nothing that contradicts it, and supported if every claim can be found in the retrieved passages, even if the claim is true.

The free tier only allows 20 requests a day on gemini-flash, so the agent and the judge were run with gemini-flash-lite.

| Result | |
|---|---|
| Correct overall | 32 / 34 |
| Correct answers to answerable questions | 26 / 28 |
| Unsupported answers | 0 |
| Correct refusals (unanswerable questions) | 6 / 6 |
| Wrong refusals (answerable questions) | 0 |
| Invalid citations | 0 |

The agent refused every unanswerable question and never refused one it could answer, and every citation pointed to a passage it had actually retrieved. The answers are saved in eval/to_grade.md so this can be done next.

## Failures

Both failures were graded as wrong answers from the right passage, since search found the correct section in both cases. However, looking at them, they are really bad test questions. In q02 (‘What maximum password length should I enforce if I hash passwords with bcrypt?’)  the reference answer mentioned the minimum work factor of 10, which the question never asked about. In q22 (‘Which Fetch Metadata request header is the main signal for CSRF protection?’) the reference also expected the fallback to origin verification for older browsers. They were both marked as wrong because an answer must give the key facts of the reference answer.

The first thing to fix is the test set itself, the reference answers should only contain what the question asks, or the questions should ask for both parts. There were no retrieval misses, unsupported claims or wrong refusals.

## Decision

I would let a freelance developer rely on it for questions about the topics in these 15 cheat sheets, as a quick first check while coding, with the safeguard that every answer has to cite a passage that search returned and that it refuses when the corpus does not cover the question, so the developer can always open the source. I would not use it for topics outside the corpus, and for high risk settings like password storage the developer should still check the cited section. 

## AI use

I used Claude for this assignment. It helped write the code for the assignment, and explained it to me step by step while I ran and tested it on Codespaces. It also proposed the use case options, the documents and a draft of the test questions, which I reviewed. It refined the text of this report based on what I had written, and helped me improve in the areas that were lacking based on what was being asked from us.