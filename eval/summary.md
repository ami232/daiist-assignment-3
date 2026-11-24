# End-to-end evaluation

Agent: gemini-3.8-flash with retrieval design B (k=5). Judge: gemini-3.1-pro-preview. 39 questions.

Correct and supported come from the judge; refusals and the three code checks are computed in code.

| | single | multi | unanswerable | all |
|---|---|---|---|---|
| Correct (judge) | 24/25 | 6/7 | 5/7 | 35/39 |
| Supported (judge) | 24/25 | 2/7 | 6/7 | 32/39 |
| Unsupported (judge) | 1/25 | 5/7 | 1/7 | 7/39 |
| Says the documents don't cover it, anywhere (code) | 1/25 | 0/7 | 6/7 | 7/39 |
| … and leads with it, first 600 characters (code) | 0/25 | 0/7 | 2/7 | 2/39 |
| Correct refusals: unanswerable, says not covered | 0/25 | 0/7 | 6/7 | 6/39 |
| Wrong refusals: answerable, leads with not covered | 0/25 | 0/7 | 0/7 | 0/39 |
| Wrong refusals: unanswerable, never says not covered | 0/25 | 0/7 | 1/7 | 1/39 |
| Answerable with a gap caveat later in the answer | 1/25 | 0/7 | 0/7 | 1/39 |
| (a) All citations valid (code) | 22/25 | 6/7 | 7/7 | 35/39 |
| (c) Cites an expected source (code) | 23/25 | 7/7 | – | 30/32 |
| Citation guardrail fired | 20/25 | 4/7 | 2/7 | 26/39 |
| Answer flagged by the guardrail | 3/25 | 1/7 | 0/7 | 4/39 |

| Per question | single | multi | unanswerable | all |
|---|---|---|---|---|
| Tokens, average | 35,803 | 40,200 | 41,115 | 37,545 |
| Tokens, max | 154,394 | 114,720 | 128,635 | 154,394 |
| Seconds, average | 41.5 | 44.7 | 36.0 | 41.1 |
| Seconds, max | 87.7 | 79.6 | 83.1 | 87.7 |
| Model calls, average | 4.2 | 4.4 | 4.4 | 4.3 |

Agent totals for the run: 1,345,169 input + 119,104 output tokens. Seconds include the translation step in the search tool and the guardrail's retry; tokens are the agent model's only (the translation step adds ~270 tokens per search, see retrieval_results.md).

## Agreement with your labels (eval/human_labels.csv)

- correct: 36/39 agree (92%)
- supported: 32/39 agree (82%)

**q05 correct:** you 0, judge 1. Your note: misses the Nr. 17 limitation (137/15 Rn. 11). Judge: The assistant correctly answers 'Yes' and explains that the phrase 'die Betriebskosten' is sufficient to pass on the standard operating costs without attaching a list. It also correctly notes the exception for 'other operating costs' (sonstige Betriebskosten), which aligns perfectly with the reference answer.

**q07 correct:** you 0, judge 1. Your note: misses the § 242 exception (209/15 Rn. 28). Judge: The assistant reaches the same conclusion as the reference answer, stating that the tenant is generally barred from challenging the costs after the 12-month deadline has passed. It correctly notes that this preclusion applies even to non-allocable costs and mentions the exception for when the tenant is not responsible for the delay. Although it omits the § 242 BGB exception mentioned in the reference answer, this is acceptable because that specific exception was not included in the retrieved passages.

**q33 correct:** you 0, judge 1. Your note: gives a substantive "no duty" answer from the documents' silence. Judge: The assistant correctly identifies that the question is unanswerable based on the provided documents. It refuses to give a substantive answer to the specific question, mentions the related rule regarding three quotes for fiber-optic installations, and advises consulting a lawyer, which perfectly aligns with the reference answer.

**q04 supported:** you 0, judge 1. Your note: says bank statements; 118/19 only says Zahlungsbelege. Judge: All claims made by the assistant are directly supported by the provided text. The text confirms that the right to inspect extends to payment receipts (Zahlungsbelege) alongside invoices, no special interest is needed, the accounting method (Abflussprinzip or Leistungsprinzip) does not matter, and the tenant has a temporary right to refuse payment if inspection is denied.

**q26 supported:** you 1, judge 0. Your note: –. Judge: The assistant claims that the landlord must separate the combined costs on the invoice to bill only the maintenance share. While this is practically and legally correct, the retrieved passages do not mention invoices or the procedure for separating combined costs. Therefore, this claim is not supported by the provided text.

**q27 supported:** you 1, judge 0. Your note: –. Judge: Most of the assistant's claims are supported by the retrieved passages, including the billability of the tree removal and sand replacement, the exclusion of initial setup costs, and the principle of economic efficiency. However, the claim that the lease agreement must 'specifically name garden maintenance or reference § 2 Nr. 10 BetrKV' is not found in the provided text, which only states in § 556 Abs. 1 BGB that parties can agree the tenant bears operating costs.

**q28 supported:** you 1, judge 0. Your note: misses the § 242 exception, same as q07. Judge: The assistant includes claims that are not present in the retrieved passages. Specifically, it provides examples of fundamental formal defects ('missing essential minimum information such as an orderly summary of total costs, applicable allocation keys, or the deduction of prepayments') which do not appear in the provided text. Furthermore, the specific claim that 'Simply failing to notice or check the line item for 14 months does not excuse the delay' is an interpretation not explicitly stated in the passages.

**q29 supported:** you 1, judge 0. Your note: –. Judge: Most of the assistant's claims are well-supported by the retrieved passages. However, the assistant claims that a landlord may 'only' bill operating costs if there is an 'express agreement' and introduces the specific legal term 'Umlagevereinbarung'. The provided text only states that if the parties have agreed that the tenant bears the costs and pays advances, the landlord must account for them annually; it does not contain the word 'Umlagevereinbarung' or state that an 'express' agreement is the exclusive prerequisite.

**q32 supported:** you 1, judge 0. Your note: –. Judge: Most of the assistant's claims are well-supported by the provided text, including the formulas, the 15% reduction right, and the rules regarding vacancies. However, the assistant claims that 'High vacancies cause circulation and distribution heat losses to fall heavily on the few remaining users.' While the passages mention fixed costs and high consumption cost allocations due to vacancies, and separately mention circulation and distribution heat losses as parameters in a formula, they do not state that high vacancies cause these specific heat losses to fall heavily on the remaining users.

**q33 supported:** you 0, judge 1. Your note: gives a substantive "no duty" answer from the documents' silence. Judge: All claims made by the assistant are supported by the retrieved passages. The assistant correctly cites § 556 BGB for the agreement on operating costs, the principle of economic efficiency, and the specific requirement for three quotes for fiber-optic installations. It also correctly cites the BGH decisions regarding the landlord's collateral duty and the tenant's burden of proof, and accurately notes the absence of a general requirement for comparison quotes in the provided texts.

add_document demo (q33, before and after): eval/add_document_demo.md
