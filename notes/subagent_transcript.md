Run on 23 November 2026 with VS Code Copilot chat (agent mode), subagent corpus-researcher, MCP server corpus (search tool).

Notes:
- First attempt used .claude/agents/corpus-researcher.md (Claude Code format). Copilot's subagent did not call search and answered from memory (its citations were not in the corpus format).
- Second attempt used .github/agents/corpus-researcher.agent.md (VS Code format, written with AI help). My prompt told the subagent to call search and list its queries. The run below is that attempt.
- Copilot chose the subagent's model (gpt-6-luna), not Gemini.

Transcript:
My message: Use the corpus-researcher subagent. It must call the search tool at least once and list the exact queries it used and the source and location of each retrieved passage before answering. Question: does a small business have to report a breach to the supervisory authority if it decides the breach is unlikely to harm anyone?

Delegated task
I’m waiting for the corpus researcher to search the source and report the exact queries and passage locations.
Background agent Research breach reporting rule is complete
Read agent Research breach reporting rule
Completed with input: {
  "agent_id": "587e8347-ebd1-4245-b970-388bec6333d9",
  "since_turn": 0
}
**Search query used:** “Does a controller have to notify the supervisory authority of a personal data breach when it considers the breach unlikely to result in a risk or harm to individuals? GDPR Article 33, small business”
**Retrieved passages:**
- edpb_breach — Section II.A.1, page 10
- gdpr — Article 33, paragraphs 1–4, page 52
- edpb_breach — Section IV.A, paragraphs 100–101, page 23
- edpb_breach — Section VII.A, page 30
- edpb_breach — Section II.D, paragraphs 75–76, page 18
**Answer:** If the business assesses that the breach is unlikely to result in a risk to people’s rights and freedoms, it does not have to notify the supervisory authority. The GDPR’s threshold is risk to rights and freedoms, not simply whether the business thinks someone will be harmed. The cited passages provide no separate small-business exception. [gdpr: Article 33, paragraphs 1-4, page 52] [edpb_breach: Section II.D, paragraphs 75-76, page 18]
search
Completed with input: {
  "query": "Does a controller have to notify the supervisory authority of a personal data breach when it considers the breach unlikely to result in a risk or harm to individuals? GDPR Article 33, small business"
}

Tab title: Research breach reporting rule (read-only)

Prompt the main Copilot agent gave the subagent:
Answer the user's question: "does a small business have to report a breach to the supervisory authority if it decides the breach is unlikely to harm anyone?" Use only the GDPR / EDPB corpus. You must call the corpus search tool at least once. Before giving the answer, list the exact search query or queries used and the source and location of each retrieved passage. Cite every claim exactly as the corpus shows. Keep concise and state if applicability depends on the text's risk threshold.

Tool call shown in the subagent's own chat: search - corpus (MCP Server)

Search query: "Does a controller have to notify the supervisory authority of a personal data breach when it considers the breach unlikely to result in a risk or harm to individuals? GDPR Article 33, small business"

Retrieved passages:
- edpb_breach - Section II.A.1, page 10
- gdpr - Article 33, paragraphs 1-4, page 52
- edpb_breach - Section IV.A, paragraphs 100-101, page 23
- edpb_breach - Section VII.A, page 30
- edpb_breach - Section II.D, paragraphs 75-76, page 18

Answer: The text's threshold is whether the breach is unlikely to result in a risk to people's rights and freedoms. If the business assesses that it is unlikely to do so, it does not have to notify the supervisory authority; if that threshold is not met, notification is required. The passages give no separate small-business exception. [gdpr: Article 33, paragraphs 1-4, page 52] [edpb_breach: Section II.D, paragraphs 75-76, page 18]