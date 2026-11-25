# Adding a document

Question: **What are the CSF Tiers and what is their purpose?**
Document: `corpus/holdout/NIST.CSWP.29.pdf` (NIST CSWP 29, CSF 2.0)

## 1. Before: the question is unanswerable

I don't know based on the indexed documents. 

I searched for CSF Tiers and implementation tiers across the indexed publications (NIST AI 100-1, NIST AI 600-1, NIST SP 800-61r3, and NIST SP 800-218). While NIST SP 800-61r3 is structured as a CSF 2.0 Community Profile [NIST.SP.800-61r3, p17-18] and NIST AI 600-1 mentions establishing risk tiers for generative AI [NIST.AI.600-1, GV-1.3-001], the core CSF Implementation Tiers and their specific definitions/purposes are described in the main NIST Cybersecurity Framework (CSF) document, which is not in the indexed set.

- tool calls: search({"query": "CSF Tiers implementation tiers purpose"}), search({"query": "tier implementation tier CSF Tiers"}), search({"query": "\"Tier\" \"Tiers\""})
- approvals: none
- retrieved: NIST.SP.800-61r3:A250:0005, NIST.SP.800-61r3:A250:0002, NIST.SP.800-61r3:A250:0017, NIST.SP.800-61r3:A250:0010, NIST.SP.800-61r3:A250:0038, NIST.SP.800-61r3:A250:0044, NIST.SP.800-61r3:A250:0003, NIST.SP.800-61r3:A250:0031, NIST.AI.100-1:A250:0000, NIST.AI.600-1:A250:0030, NIST.SP.800-61r3:A250:0025, NIST.SP.800-61r3:A250:0043, NIST.SP.800-61r3:A250:0041
- guardrail: {'fired': False, 'reason': '', 'retried': False, 'withheld': False}
- {'input_tokens': 21920, 'output_tokens': 1509} | 14.39 s

## 2. Add the document (approval required)

Added NIST.CSWP.29 (NIST CSWP 29: The NIST Cybersecurity Framework (CSF) 2.0): 44 chunks stored, 0 new embeddings.

- tool calls: add_document({"path": "corpus/holdout/NIST.CSWP.29.pdf"})
- approvals: [{'approval': 'add_document', 'args': {'path': 'corpus/holdout/NIST.CSWP.29.pdf'}, 'approved': True}]
- retrieved: none
- guardrail: {'fired': False, 'reason': '', 'retried': False, 'withheld': False}
- {'input_tokens': 5113, 'output_tokens': 2225} | 16.5 s

## 3. After: the same question

The CSF Tiers characterize the rigor of an organization’s cybersecurity risk governance and management practices [NIST.CSWP.29, p12-13]. 

### The CSF Tiers
The four Tiers describe a progression from informal, ad hoc responses to approaches that are agile, risk-informed, and continuously improving [NIST.CSWP.29, p12-13]:
1. **Tier 1: Partial** [NIST.CSWP.29, p12-13], [NIST.CSWP.29, p28-29]
2. **Tier 2: Risk Informed** [NIST.CSWP.29, p12-13], [NIST.CSWP.29, p28-29]
3. **Tier 3: Repeatable** [NIST.CSWP.29, p12-13]
4. **Tier 4: Adaptive** [NIST.CSWP.29, p12-13]

### Purpose of the Tiers
The Tiers serve several purposes:
- **Inform Profiles:** Organizations can use the Tiers to inform their Current and Target Profiles [NIST.CSWP.29, p12-13].
- **Provide Context:** They provide context for how an organization views cybersecurity risks and the processes in place to manage those risks [NIST.CSWP.29, p12-13].
- **Set Tone and Direction:** Selecting Tiers helps set the overall tone for how an organization will manage its cybersecurity risks [NIST.CSWP.29, p12-13].
- **Benchmarking and Communication:** Tiers complement an organization's cybersecurity risk management methodology and can be used to communicate internally as a benchmark for an enterprise-wide approach to managing cybersecurity risks [NIST.CSWP.29, p12-13].

- tool calls: search({"query": "CSF Tiers implementation tiers purpose"})
- approvals: none
- retrieved: NIST.CSWP.29:A250:0015, NIST.CSWP.29:A250:0038, NIST.CSWP.29:A250:0007, NIST.CSWP.29:A250:0043, NIST.CSWP.29:A250:0012
- guardrail: {'fired': False, 'reason': '', 'retried': False, 'withheld': False}
- {'input_tokens': 5277, 'output_tokens': 1420} | 10.19 s

## 4. Add it again: duplicate detection

The file `corpus/holdout/NIST.CSWP.29.pdf` is already indexed as NIST.CSWP.29 (44 chunks). Nothing was embedded.

- tool calls: add_document({"path": "corpus/holdout/NIST.CSWP.29.pdf"})
- approvals: [{'approval': 'add_document', 'args': {'path': 'corpus/holdout/NIST.CSWP.29.pdf'}, 'approved': True}]
- retrieved: none
- guardrail: {'fired': False, 'reason': '', 'retried': False, 'withheld': False}
- {'input_tokens': 4139, 'output_tokens': 1205} | 8.63 s
