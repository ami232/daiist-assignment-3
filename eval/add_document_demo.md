# Adding a document: before and after

Question: **Under Regulation Best Interest, what does a broker-dealer's care obligation require?**

## Before

```
The corpus does not cover this. The corpus covers investment advisers under the Investment Advisers Act of 1940 and does not contain rules regarding broker-dealers under Regulation Best Interest; please consult your firm's compliance officer.


(1 searches, 2 model calls, 3942 tokens, 3.77s)
```

## Adding the file (approval asked at the terminal)

```
The document at `corpus/extra/reg-bi.xml` has been successfully added to the corpus.


(0 searches, 2 model calls, 2644 tokens, 13.76s)
```
Tool calls: add_document({'path': 'corpus/extra/reg-bi.xml'}) approved=True -> {"status": "added", "document": "reg-bi", "title": "\u00a7 240.15l-1 Regulation best interest.", "words": 919, "chunks": {"fixed": 6, "structure": 5}, "message": "Added '\u00a7 240.15l-1 Regulation best interest.' (919 words, 5 chunks in the structure design)."}

## After

```
Under Regulation Best Interest, the care obligation requires a broker, dealer, or associated person, when making a recommendation, to exercise reasonable diligence, care, and skill to:

* **Understand risks, rewards, and costs:** Understand the potential risks, rewards, and costs associated with the recommendation, and have a reasonable basis to believe that the recommendation could be in the best interest of at least some retail customers [REGBI:240.15l-1#2].
* **Suitability for the particular customer:** Have a reasonable basis to believe that the recommendation is in the best interest of a particular retail customer based on that customer's investment profile and the potential risks, rewards, and costs, without placing the financial or other interest of the broker, dealer, or associated person ahead of the customer's interest [REGBI:240.15l-1#2].
* **Avoid excessive trading:** Have a reasonable basis to believe that a series of recommended transactions—even if in the customer's best interest when viewed in isolation—is not excessive and is in the customer's best interest when taken together in light of the customer's investment profile, without placing the financial or other interest of the broker, dealer, or associated person ahead of the customer's interest [REGBI:240.15l-1#3].

*For specific situations or client implementations, please confirm with compliance.*

Sources:
  [REGBI:240.15l-1#2] § 240.15l-1 Regulation best interest. | 17 CFR 240.15l-1(a)
  [REGBI:240.15l-1#3] § 240.15l-1 Regulation best interest. | 17 CFR 240.15l-1(a)

(1 searches, 2 model calls, 4273 tokens, 2.56s)
```

## Adding the same file again

Tool calls: add_document -> {"status": "already_indexed", "document": "reg-bi", "title": "\u00a7 240.15l-1 Regulation best interest.", "message": "This exact file is already indexed as 'reg-bi'. Nothing was changed."}
