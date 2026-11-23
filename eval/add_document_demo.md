# add_document demo (q33)

**Question:** Do I have to get comparison quotes before hiring a cleaning company?

Before: the base index (201 chunks) has no passage on comparison quotes. Then `corpus/holdout/jb-KORE303622026.xml` (BGH VIII ZR 6/24, 20 May 2026) is added through the `add_document` tool, with approval, and the question is asked again. Afterwards the holdout is removed so the committed index stays at the base corpus.

## Before (from the evaluation run)

**Trace** (8 model calls, 128,635 tokens, 83.1 s):

```text
call search({'query': 'Muss der Vermieter Vergleichsangebote einholen Wirtschaftlichkeitsgebot Reinigungsfirma Gebäudereinigung'})
result German search query: Verpflichtet der Grundsatz der Wirtschaftlichkeit den Vermieter dazu, vor der Beauftragung einer Reinigungsfirma mit der Gebäudereinigung mehrere Vergleichsangebote einzuholen? Führt das Unterlassen der Einholung von Vergleichsangeboten zu einem Verstoß gegen das Wirtschaftlichkeitsgebot bei den umlagefähigen Betriebskosten?
         BGH VIII ZR 230/21, Leitsatz | BGH VIII ZR 230/21, Rn. 27–30 | BGH VIII ZR 230/21, Rn. 31–34 | BGH VIII ZR 117/21, Rn. 35–38 | BGH VIII ZR 230/21, Rn. 23–26
call search({'query': 'Vergleichsangebote einholen Vermieter Wirtschaftlichkeitsgebot'})
result German search query: Ist der Vermieter im Rahmen des Wirtschaftlichkeitsgebots bei der Entstehung und Abrechnung von Betriebskosten verpflichtet, vor der Vergabe von Aufträgen mehrere Vergleichsangebote einzuholen? Verletzt die unterlassene Einholung von Vergleichsangeboten die Pflicht zur wirtschaftlichen Betriebsführung gegenüber dem Mieter?
         BGH VIII ZR 230/21, Leitsatz | BGH VIII ZR 230/21, Rn. 27–30 | BGH VIII ZR 230/21, Rn. 31–34 | BGH VIII ZR 117/21, Rn. 35–38 | BGH VIII ZR 230/21, Rn. 23–26
call search({'query': '§ 556 BGB Wirtschaftlichkeitsgebot'})
result German search query: Verletzt der Vermieter bei der Abrechnung der Betriebskosten nach § 556 BGB das Wirtschaftlichkeitsgebot, und welche Maßstäbe gelten für die Umlage der entstandenen Kosten auf den Mieter?
         BGH VIII ZR 230/21, Rn. 27–30 | BGH VIII ZR 230/21, Leitsatz | BGH VIII ZR 230/21, Rn. 31–34 | BGH VIII ZR 117/21, Rn. 35–38 | § 556 BGB
call search({'query': 'Vergleichsangebote BGH Betriebskosten Wirtschaftlichkeitsgebot'})
result German search query: Verpflichtet das Wirtschaftlichkeitsgebot den Vermieter bei der Abrechnung der Betriebskosten zur Einholung von Vergleichsangeboten, und welche Anforderungen stellt der Bundesgerichtshof an die Darlegungs- und Beweislast bei einem gerügten Verstoß?
         BGH VIII ZR 230/21, Leitsatz | BGH VIII ZR 230/21, Rn. 27–30 | BGH VIII ZR 230/21, Rn. 31–34 | BGH VIII ZR 117/21, Rn. 35–38 | BGH VIII ZR 230/21, Rn. 23–26
call search({'query': 'BGH VIII ZR 230/21 Darlegungs- und Beweislast Wirtschaftlichkeitsgebot'})
result German search query: BGH VIII ZR 230/21 zur Darlegungs- und Beweislast bei einer Verletzung des Wirtschaftlichkeitsgebots im Rahmen der Abrechnung von Betriebskosten zwischen Vermieter und Mieter.
         BGH VIII ZR 230/21, Leitsatz | BGH VIII ZR 230/21, Rn. 27–30 | BGH VIII ZR 230/21, Rn. 31–34 | BGH VIII ZR 230/21, Rn. 40–43 | BGH VIII ZR 230/21, Rn. 23–26
call search({'query': '§ 2 Nr. 9 BetrKV Gebäudereinigung'})
result German search query: Welche Kosten der Gebäudereinigung sind nach § 2 Nr. 9 BetrKV als Betriebskosten auf den Mieter umlagefähig?
         § 2 Nr. 1–5 BetrKV | BGH VIII ZR 117/21, Leitsatz | § 2 Nr. 5–13 BetrKV | § 1 BetrKV | BGH VIII ZR 62/19, Leitsatz
```

**Answer:**

Based on the indexed statutes and Federal Court of Justice (*Bundesgerichtshof*, BGH) decisions, the legal requirements are as follows:

### 1. Agreement in the Lease (*Umlagevereinbarung*)
Whether you can pass on the costs of a cleaning company at all depends on the lease agreement:
* Operating costs can only be billed to the tenant if the parties have agreed in the contract that the tenant bears them (*Umlagevereinbarung*) (§ 556 BGB).
* Under the catalog of operating costs, building cleaning costs (*Kosten der Gebäudereinigung*), which cover the cleaning of jointly used areas such as hallways, staircases, and basements, constitute eligible operating costs (§ 2 Nr. 5–13 BetrKV).

### 2. The Principle of Economic Efficiency (*Grundsatz der Wirtschaftlichkeit*)
* In billing operating costs, the landlord must comply with the principle of economic efficiency (*Grundsatz der Wirtschaftlichkeit*) (§ 556 BGB).
* The landlord has a contractual collateral duty (*vertragliche Nebenpflicht*) to maintain a reasonable cost-benefit ratio (*angemessenes Kosten-Nutzen-Verhältnis*) when making decisions and taking measures that affect the amount of operating costs borne by the tenant (BGH VIII ZR 230/21, Rn. 27–30; BGH VIII ZR 117/21, Rn. 35–38).
* A breach of this duty can result in a claim for damages by the tenant aimed at reimbursement of unnecessary costs or indemnification from them (BGH VIII ZR 230/21, Rn. 27–30; BGH VIII ZR 117/21, Rn. 35–38).
* The burden of presentation and proof (*Darlegungs- und Beweislast*) for a breach of duty by the landlord rests on the tenant who asserts the claim (BGH VIII ZR 230/21, Leitsatz; BGH VIII ZR 117/21, Rn. 35–38).

### 3. Comparison Quotes (*Vergleichsangebote*)
* The statutory rules governing operating costs do not contain a general obligation to obtain comparison quotes (*Vergleichsangebote*) before hiring routine service providers (§ 556 BGB). By contrast, § 556 BGB explicitly requires obtaining three quotes only for specific complex measures, such as elaborate fiber-optic installations (§ 556 BGB).
* The retrieved documents and BGH judgments do not state that a landlord is obligated to solicit comparison quotes before hiring a cleaning service. 

Because the indexed documents do not cover whether or when obtaining comparison quotes is required to guard against economic efficiency objections for cleaning contracts, please consult a tenancy lawyer (*Fachanwalt für Miet- und Wohnungseigentumsrecht*).

## Adding the document (approved)

**Trace** (4 model calls, 11,005 tokens, 25.7 s):

```text
call add_document({'path': 'corpus/holdout/jb-KORE303622026.xml'})
result BGH VIII ZR 6/24: added, 21 chunks, 6,919 words.
call search({'query': 'BGH VIII ZR 6/24'})
result German search query: Entscheidung des BGH mit dem Aktenzeichen VIII ZR 6/24 zu den Anforderungen an die Betriebskostenabrechnung und die Umlage von Betriebskosten im Mietverhältnis zwischen Vermieter und Mieter.
         BGH VIII ZR 6/24, Leitsatz | BGH VIII ZR 6/24, Rn. 46–48 | BGH VIII ZR 6/24, Rn. 49–50 | BGH VIII ZR 6/24, Rn. 60–61 | BGH VIII ZR 6/24, Rn. 6, 18–21
```

**Answer:**

The document `corpus/holdout/jb-KORE303622026.xml` has been added to the search index and corresponds to the decision BGH VIII ZR 6/24 (see BGH VIII ZR 6/24, Leitsatz).

## After

**Trace** (5 model calls, 42,810 tokens, 55.6 s):

```text
call search({'query': 'Vergleichsangebote einholen Reinigung Gebäudereinigung Wirtschaftlichkeitsgebot'})
result German search query: Verpflichtet das Gebot der Wirtschaftlichkeit den Vermieter vor der Vergabe von Aufträgen zur Gebäudereinigung zum Einholen von Vergleichsangeboten? Welche Anforderungen gelten an die Darlegungs- und Beweislast bei der Umlage der Kosten für die Reinigung als Betriebskosten auf den Mieter?
         BGH VIII ZR 230/21, Leitsatz | BGH VIII ZR 6/24, Leitsatz | BGH VIII ZR 6/24, Rn. 37–40 | BGH VIII ZR 6/24, Rn. 35–36 | BGH VIII ZR 230/21, Rn. 27–30
call search({'query': 'BetrKV § 2 Nr. 9 Gebäudereinigung'})
result German search query: Umlage der Betriebskosten für die Gebäudereinigung nach BetrKV § 2 Nr. 9 im Mietverhältnis.
         § 2 Nr. 1–5 BetrKV | BGH VIII ZR 117/21, Leitsatz | BGH VIII ZR 62/19, Leitsatz | § 1 BetrKV | § 2 Nr. 5–13 BetrKV
call search({'query': '§ 556 BGB Vereinbarungen über Betriebskosten'})
result German search query: Welche Voraussetzungen und Rechtsfolgen gelten für Vereinbarungen über Betriebskosten zwischen Vermieter und Mieter nach § 556 BGB? In welchem Umfang können die Vertragsparteien die Umlage von Betriebskosten, die Leistung von Vorauszahlungen oder Pauschalen sowie die Abrechnungspflichten regeln?
         § 556 BGB | §§ 556a–556c BGB | §§ 560–561 BGB | BGH VIII ZR 137/15, Leitsatz | BGH VIII ZR 47/25, Rn. 51–53
```

**Answer:**

**No**, you are not legally required to obtain comparison quotes (*Vergleichsangebote*) before hiring a cleaning company.

---

### 1. The Principle of Economic Efficiency (*Wirtschaftlichkeitsgebot*)
Under German tenancy law, the principle of economic efficiency (*Wirtschaftlichkeitsgebot*) constitutes a contractual secondary duty (*vertragliche Nebenpflicht*) of the landlord to respect an appropriate cost-benefit ratio when making decisions that impact operating costs (**BGH VIII ZR 6/24, Rn. 35–36**).

Regarding quotes, the Federal Court of Justice has established:
* The principle of economic efficiency is **not** breached merely because a landlord does not obtain comparison quotes or does not acquire an adequate market overview before commissioning services (**BGH VIII ZR 6/24, Leitsatz**; **BGH VIII ZR 6/24, Rn. 37–40**).
* Instead, the decisive factor is whether the services were actually commissioned at prices that are not in line with market rates and are objectively excessive (*nicht marktgerechte, objektiv überhöhte Preise*), such that obtaining comparison quotes would have resulted in actual cost savings (**BGH VIII ZR 6/24, Leitsatz**; **BGH VIII ZR 6/24, Rn. 37–40**).
* Only after it is established that the prices are objectively excessive does it matter—in evaluating whether the landlord can exonerate themselves from liability—whether reasonable efforts were made to find a cost-effective provider, which is the point at which comparison quotes become relevant (**BGH VIII ZR 6/24, Rn. 35–36**; **BGH VIII ZR 6/24, Rn. 37–40**).

---

### 2. Burden of Proof (*Darlegungs- und Beweislast*)
If a tenant alleges a breach of the principle of economic efficiency:
* The tenant bears the full burden of pleading and proof (*Darlegungs- und Beweislast*) for showing that the landlord acted in breach of duty (**BGH VIII ZR 6/24, Rn. 37–40**; **BGH VIII ZR 230/21, Leitsatz**).
* The landlord is not subject to a secondary burden of proof (*sekundäre Darlegungslast*) that would obligate them to proactively demonstrate a price comparison (**BGH VIII ZR 6/24, Rn. 37–40**).

---

### 3. Decisive Contractual Prerequisite (*Umlagevereinbarung*)
Whether you can pass building cleaning costs on to your tenant at all depends on the terms of the lease agreement:
* Under **§ 556 BGB**, the parties must agree in the contract that the tenant bears operating costs (*Betriebskosten*).
* Cleaning costs for parts of the building shared by occupants (such as hallways, stairs, and basements) are categorized as building cleaning (*Gebäudereinigung*) under **§ 2 Nr. 5–13 BetrKV** (specifically item 9). These costs can only be allocated to the tenant if the lease agreement contains an effective allocation clause (*Umlagevereinbarung*) covering them.
