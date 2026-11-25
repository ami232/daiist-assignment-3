# Before and after adding `corpus/nis2.xhtml`

**Question:** What is the deadline for an essential entity to submit an early warning of a significant cybersecurity incident to its CSIRT?

### Before

I don't know based on the indexed documents. I searched for the deadline for an essential entity to submit an early warning of a significant cybersecurity incident to its CSIRT, but the indexed documents (the AI Act, the GDPR, and the Data Act) do not contain rules on cybersecurity incident reporting for essential entities under the NIS framework.

_Tool calls: search(deadline essential entity early warning significant incident CSIRT); search(early warning significant incident CSIRT essential entity). Guardrails: none. 9519 tokens, 14.5s._

### Adding the document (approval required)

The document `corpus/nis2.xhtml` has been successfully added to the corpus under the source name `NIS2` (86 passages indexed via keyword search).

_Tool calls: add_document(corpus/nis2.xhtml). Guardrails: approval_requested:add_document, approval_approve. 2943 tokens, 9.1s._

### After

An essential entity must submit an early warning of a significant incident to the CSIRT or competent authority without undue delay and in any event within 24 hours of becoming aware of the significant incident [NIS2 | Article 23(1) & Article 23(4)(a)].

Sources:
  - NIS2 | Article 23(1) & Article 23(4)(a)

_Tool calls: search(deadline essential entity submit early warning significant incident CSIRT); search(early warning significant incident essential entity CSIRT deadline); search(Article 23 NIS2 reporting obligations early warning significant incident). Guardrails: none. 16196 tokens, 18.9s._
