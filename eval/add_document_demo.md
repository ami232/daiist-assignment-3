# Add-document demo

Document: `corpus/held_back/eliquis.json`

- First `add_document`: Indexed eliquis: 96 chunks (96 embedded, 0 already indexed, 0 removed).
- Second `add_document` (already indexed): Indexed eliquis: 96 chunks (0 embedded, 96 already indexed, 0 removed).

## q40: What is the usual Eliquis dose for atrial fibrillation?

**Before** (gemini-3.5-flash-lite):

The current FDA drug label corpus does not contain the information for Eliquis (apixaban). Therefore, I cannot provide the usual dose for atrial fibrillation from the available labels. Please consult your supervising pharmacist or refer to the official Eliquis prescribing information.

**After** (gemini-3.5-flash-lite, 2583 tokens, 2.35 s):

For the reduction of the risk of stroke and systemic embolism in patients with nonvalvular atrial fibrillation, the usual doses of Eliquis (apixaban) are:

* **Recommended dose for most patients:** 5 mg orally twice daily [eliquis, Dosage and Administration].
* **Reduced dose (2.5 mg orally twice daily):** Indicated for patients who have at least two of the following characteristics [eliquis, Dosage and Administration]:
  * Age $\ge$ 80 years [eliquis, Dosage and Administration]
  * Body weight $\le$ 60 kg [eliquis, Dosage and Administration]
  * Serum creatinine $\ge$ 1.5 mg/dL [eliquis, Dosage and Administration]

## q41: What should a customer do if they miss an Eliquis dose?

**Before** (gemini-3.5-flash-lite):

The available FDA drug labels in our database do not contain information regarding Eliquis (apixaban) or instructions for a missed dose of Eliquis. 

Please consult the supervising pharmacist for guidance, as the search results only provide information for other medications (such as Jantoven, Prilosec, and Cipro).

**After** (gemini-3.5-flash-lite, 2415 tokens, 2.12 s):

If a dose of Eliquis is not taken at the scheduled time, the customer should take the dose as soon as possible on the same day and then resume twice-daily administration. They should not double the dose to make up for a missed dose [eliquis, Dosage and Administration].
