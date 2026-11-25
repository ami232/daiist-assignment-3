# Grading sheet

Grade each answer into `eval/human_labels.csv` (`id,correct,supported,notes`) before reading `eval/results.csv`. `correct`: 1 if right against the reference (for unanswerable questions, 1 only for a refusal). `supported`: 1 if every claim is in the retrieved passages. A note for every 0.

## q01 (single)

**Question:** Which cocoa products fall under the EUDR?

**Reference:** Annex I lists cocoa beans (1801), cocoa shells, husks, skins and other cocoa waste (1802, not including waste as defined in Directive 2008/98/EC), cocoa paste (1803), cocoa butter, fat and oil (1804), cocoa powder without added sugar (1805) and chocolate and other food preparations containing cocoa (1806).

**Answer:**

The following cocoa products listed in Annex I to the EUDR fall under the regulation:

* **1801:** Cocoa beans, whole or broken, raw or roasted [EUDR Annex I (part 1/12)]
* **1802:** Cocoa shells, husks, skins and other cocoa waste [EUDR Annex I (part 1/12)]
* **1803:** Cocoa paste, whether or not defatted [EUDR Annex I (part 1/12)]
* **1804:** Cocoa butter, fat and oil [EUDR Annex I (part 1/12)]
* **1805:** Cocoa powder, not containing added sugar or other sweetening matter [EUDR Annex I (part 1/12)]
* **1806:** Chocolate and other food preparations containing cocoa [EUDR Annex I (part 1/12)]

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.86
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[2] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.835
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;

---

[3] Cite as: [Guidance §9 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Composite products
Similarity: 0.832
Composite products may contain multiple relevant products under different commodities. For instance, a chocolate bar [HS 1806 ] may comprise derived products of cocoa (cocoa powder [HS 1805 ] and cocoa butter [HS 1804 ]) and oil palm (palm oil [HS 1511 ]). In such cases, the operator placing the product on the EU market or exporting from it will only be required to conduct due diligence on the relevant products listed under the commodity deemed relevant in Annex I of the EUDR. For instance, for chocolate bars [HS 1806 ], the relevant commodity linked to it is cocoa. This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

---

[4] Cite as: [EUDR Article 1]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Subject matter and scope
Similarity: 0.818
1. This Regulation lays down rules regarding the placing and making available on the Union market as well as the export from the Union of relevant products, as listed in Annex I, that contain, have been fed with or have been made using relevant commodities, namely cattle, cocoa, coffee, oil palm, rubber, soya and wood, with a view to: (a) minimising the Union’s contribution to deforestation and forest degradation worldwide, and thereby contributing to a reduction in global deforestation; (b) reducing the Union’s contribution to greenhouse gas emissions and global biodiversity loss.
2. Except as provided for in Article 37(3), this Regulation does not apply to relevant products listed in Annex I produced before the date indicated in Article 38(1).

---

[5] Cite as: [FAQ 1.3, p. 13]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How does it work for bulk-traded or composite products? What about composite products containing different commodities?
Similarity: 0.813
For products traded in bulk, such as soy or palm oil for instance, this means that the operator needs to ensure that all plots of land involved in a shipment are identified and that the commodities are not mixed at any step of the process with commodities of unknown origin or from areas deforested or degraded after the cut-off date of 31 December 2020.
For relevant composite products, such as e.g. imported wooden furniture with different wood components, the operator needs to geolocate all the plots of land where the relevant commodity (wood, for example) used for the manufacturing process has been produced.
The relevant commodities’ components may be neither of unknown origin nor from areas deforested or degraded after the cut-off date.
In the case of composite products containing multiple different relevant commodities or products (for example, a chocolate bar containing cocoa powder, cocoa butter and palm oil), the operator placing such a product on the EU market or exporting from it will need to conduct due diligence only on the main commodity and (derived) products deemed relevant under the EUDR, this being the commodity contained in the left column of Annex I.
For example, for chocolate bars (Code 1806), the relevant commodity linked to it is cocoa.
This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.
```

</details>

## q02 (single)

**Question:** What is the cut-off date after which deforestation makes our cocoa non-compliant?

**Reference:** 31 December 2020: products are deforestation-free only if the commodities were produced on land not subject to deforestation after 31 December 2020 (Article 2(13)).

**Answer:**

The cut-off date is **31 December 2020** [EUDR Article 2(13)(a)]. 

Cocoa is non-compliant if it was produced on land that has been subject to deforestation (the conversion of forest to agricultural use) after this date [EUDR Article 2(3), (13)(a)]. Compliance checks look backwards from this date to determine whether the crop land previously was a forest [FAQ 5.12, p. 67].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 5.12, p. 67]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | When checking compliance with the ‘deforestation-free’ requirement, what is the point in time the checks should focus on?
Similarity: 0.766
The assessment of whether the commodity has contributed to deforestation is conducted by looking backwards in time to see if the crop land used to be a forest (in line with definition in Art. 2) since the cut-off date of the Regulation (namely, 31 December 2020).

---

[2] Cite as: [EUDR Article 1]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Subject matter and scope
Similarity: 0.744
1. This Regulation lays down rules regarding the placing and making available on the Union market as well as the export from the Union of relevant products, as listed in Annex I, that contain, have been fed with or have been made using relevant commodities, namely cattle, cocoa, coffee, oil palm, rubber, soya and wood, with a view to: (a) minimising the Union’s contribution to deforestation and forest degradation worldwide, and thereby contributing to a reduction in global deforestation; (b) reducing the Union’s contribution to greenhouse gas emissions and global biodiversity loss.
2. Except as provided for in Article 37(3), this Regulation does not apply to relevant products listed in Annex I produced before the date indicated in Article 38(1).

---

[3] Cite as: [FAQ 1.25, p. 21]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the ‘date or time range of production’?
Similarity: 0.737
Operators are required to collect information on the date or time range of production under the obligations set out in Art. 9 EUDR.
This information is needed to establish whether the relevant product is deforestation-free.
That is why it applies to the commodities covered by the Regulation that are placed on the EU market or to the commodities that are used for the production of relevant products covered by the regulation.
For commodities other than cattle, the date of production refers to the date of harvesting of the commodities, and the time range of production refers to the period/duration of the production process (for instance, in the case of timber, “time range of pro duction” would refer to the duration of the relevant harvesting operations).
The date of production and the time range of production should both be related to the designated plots of land.
If more precise information is not available, due to the specificities of the production, the crop year and/or harvesting season could be used.
For relevant products under the commodity “cattle”, the time range of production refers to the lifetime of the animal s from the moment the cattle w ere born until the time of slaughtering.
If live cattle (HS Code 0102 21, 0102 29) are placed on the EU market (e.g., by importing or by the first selling of a cow after it was born in the EU), all geolocations (or postal addresses, if applicable) until the first placing on the EU market will have to be collected and submitted with the DDS or SD.
To note that, according to Art. 1(2) EUDR, and in line with the definition of “produced” in Art. 2(14), the E UDR does not apply to cattle and cattle derived products if the cattle was born before the entry into force of the Regulation, i.e. before 29 June 2023.

---

[4] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.736
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;

---

[5] Cite as: [EUDR Article 2 (part 1/6)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Definitions
Similarity: 0.734
For the purposes of this Regulation, the following definitions apply:
(1) ‘relevant commodities’ means cattle, cocoa, coffee, oil palm, rubber, soya and wood;
(2) ‘relevant products’ means products listed in Annex I that contain, have been fed with or have been made using relevant commodities;
(3) ‘deforestation’ means the conversion of forest to agricultural use, whether human-induced or not;
(4) ‘forest’ means land spanning more than 0,5 hectares with trees higher than 5 metres and a canopy cover of more than 10 %, or trees able to reach those thresholds in situ, excluding land that is predominantly under agricultural or urban land use;
(5) ‘agricultural use’ means the use of land for the purpose of agriculture, including for agricultural plantations and set-aside agricultural areas, and for rearing livestock;
(6) ‘agricultural plantation’ means land with tree stands in agricultural production systems, such as fruit tree plantations, oil palm plantations, olive orchards and agroforestry systems where crops are grown under tree cover; it includes all plantations of relevant commodities other than wood; agricultural plantations are excluded from the definition of ‘forest’;
(7) ‘forest degradation’ means structural changes to forest cover, taking the form of the conversion of: (a) primary forests or naturally regenerating forests into plantation forests or into other wooded land; or (b) primary forests into planted forests;
(8) ‘primary forest’ means naturally regenerated forest of native tree species, where there are no clearly visible indications of human activities and the ecological processes are not significantly disturbed;
(9) ‘naturally regenerating forest’ means forest predominantly composed of trees established through natural regeneration; it includes any of the following: (a) forests for which it is not possible to distinguish whether planted or naturally regenerated; (b) forests with a mix of naturally regenerated native tree species and planted or seeded trees, and where the naturally regenerated trees are expected to constitute the major part of the growing stock at stand maturity; (c) coppice from trees originally established through natural regeneration; (d) naturally regenerated trees of introduced species;

=====

[1] Cite as: [FAQ 5.12, p. 67]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | When checking compliance with the ‘deforestation-free’ requirement, what is the point in time the checks should focus on?
Similarity: 0.835
The assessment of whether the commodity has contributed to deforestation is conducted by looking backwards in time to see if the crop land used to be a forest (in line with definition in Art. 2) since the cut-off date of the Regulation (namely, 31 December 2020).

---

[2] Cite as: [EUDR Article 2 (part 1/6)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Definitions
Similarity: 0.829
For the purposes of this Regulation, the following definitions apply:
(1) ‘relevant commodities’ means cattle, cocoa, coffee, oil palm, rubber, soya and wood;
(2) ‘relevant products’ means products listed in Annex I that contain, have been fed with or have been made using relevant commodities;
(3) ‘deforestation’ means the conversion of forest to agricultural use, whether human-induced or not;
(4) ‘forest’ means land spanning more than 0,5 hectares with trees higher than 5 metres and a canopy cover of more than 10 %, or trees able to reach those thresholds in situ, excluding land that is predominantly under agricultural or urban land use;
(5) ‘agricultural use’ means the use of land for the purpose of agriculture, including for agricultural plantations and set-aside agricultural areas, and for rearing livestock;
(6) ‘agricultural plantation’ means land with tree stands in agricultural production systems, such as fruit tree plantations, oil palm plantations, olive orchards and agroforestry systems where crops are grown under tree cover; it includes all plantations of relevant commodities other than wood; agricultural plantations are excluded from the definition of ‘forest’;
(7) ‘forest degradation’ means structural changes to forest cover, taking the form of the conversion of: (a) primary forests or naturally regenerating forests into plantation forests or into other wooded land; or (b) primary forests into planted forests;
(8) ‘primary forest’ means naturally regenerated forest of native tree species, where there are no clearly visible indications of human activities and the ecological processes are not significantly disturbed;
(9) ‘naturally regenerating forest’ means forest predominantly composed of trees established through natural regeneration; it includes any of the following: (a) forests for which it is not possible to distinguish whether planted or naturally regenerated; (b) forests with a mix of naturally regenerated native tree species and planted or seeded trees, and where the naturally regenerated trees are expected to constitute the major part of the growing stock at stand maturity; (c) coppice from trees originally established through natural regeneration; (d) naturally regenerated trees of introduced species;

---

[3] Cite as: [EUDR Article 2 (part 2/6)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Definitions
Similarity: 0.808
(10) ‘planted forest’ means forest predominantly composed of trees established through planting and/or deliberate seeding, provided that the planted or seeded trees are expected to constitute more than 50 % of the growing stock at maturity; it includes coppice from trees that were originally planted or seeded;
(11) ‘plantation forest’ means a planted forest that is intensively managed and meets, at planting and stand maturity, all the following criteria: one or two species, even age class, and regular spacing; it includes short rotation plantations for wood, fibre and energy, and excludes forests planted for protection or ecosystem restoration, as well as forests established through planting or seeding, which at stand maturity resemble or will resemble naturally regenerating forests;
(12) ‘other wooded land’ means land not classified as ‘forest’ spanning more than 0,5 hect
[...]
```

</details>

## q03 (single)

**Question:** As a medium-sized cocoa importer, from what date do we have to comply with the EUDR?

**Reference:** From 30 December 2026. Only micro and small undertakings established as such by 31 December 2024 get until 30 June 2027 (Article 38(2)-(3)).

**Answer:**

As a medium-sized cocoa importer, you must comply with the EUDR obligations (such as due diligence statements and geolocation requirements under Articles 3 to 13) from **30 December 2026** [EUDR Article 38(2), Guidance §3]. 

*(Note: The deferred date of 30 June 2027 only applies to micro- and small enterprises established by 31 December 2024 [EUDR Article 38(3), Guidance §3].)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [Guidance §3 (part 3/6)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Date of effect and time-frame for application
Similarity: 0.826
Date of placing relevant commodity or relevant product on the EU market
Relevant products | Date of production of relevant commodity | Before 30 December 2026, and before 30 June 2027 for micro- and small operators | From 30 December 2026 (inclusive) for large and medium enterprises, and from 30 June 2027 (inclusive) for micro- and small operators
Cattle, Cocoa, Coffee, Oil palm, Rubber and Soya products listed in Annex I of Regulation (EU) 2023/1115 | Before 29 June 2023 | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is not applicable
From 29 June 2023 (inclusive) | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is applicable
Wood products listed in Annex I of Regulation (EU) 2023/1115 and not listed in the Annex of Regulation (EU) No 995/2010 (EUTR) | Before 29 June 2023 | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is not applicable
From 29 June 2023 (inclusive) | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is applicable
For timber and timber products covered by the Annex of the EUTR, special rules apply, pursuant to Article 37(3) of EUDR:

---

[2] Cite as: [Guidance §3 (part 1/6)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Date of effect and time-frame for application
Similarity: 0.821
Relevant legislation: EUDR – Article 1(2) Subject matter and scope; Article 37 – Repeal; Article 38 – Entry into force and date of application
The EUDR entered into force on 29 June 2023. Most obligations on operators, downstream operators and traders, as well as on competent authorities including those in Articles 3 to 13, Articles 16 to 24, Articles 26, 31, and 32, apply from 30 December 2026, in accordance with Regulation (EU) 2025/2650 () amending the provisions of the EUDR relating to the date of application.
For operators that were established as micro-undertakings or small undertakings by 31 December 2024 (in accordance with Article 3(1) or (2), first subparagraph, of Directive 2013/34/EU, respectively) the obligations in Articles 3 to 13, Articles 16 to 24, Articles 26, 31 and 32, apply from 30 June 2027, except as regards the products covered in the Annex of the Regulation (EU) No 995/2010 laying down the obligations of operators who place timber and timber products on the market () (EUTR). This means that there is a transitional period between the entry into force of the Regulation (29 June 2023) and the entry into application (30 December 2026, deferred to 30 June 2027 for small undertakings or micro-undertakings established by 31 December 2024) that exempts operators and traders placing or making available on or export from the Union market relevant commodities and products in the transitional period from the main obligations under the EUDR.
The following rules apply for all commodities and associated relevant products with the exception of timber and timber products covered by the Annex of the EUTR (detailed explanations are provided in the Frequently Asked Questions document, Section 9):
— | if a relevant commodity or a relevant product is placed on the market during the transitional period applying to the respective operator, the obligations of the EUDR do not apply to the operator.

---

[3] Cite as: [EUDR Article 38]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Entry into force and date of application
Similarity: 0.818
1. This Regulation shall enter into force on the twentieth day following that of its publication in the Official Journal of the European Union.
2. Subject to paragraph 3 of this Article, Articles 3 to 13, Articles 16 to 24 and Articles 26, 31 and 32 shall apply from 30 December 2026.
3. Except as regards the products covered by the Annex to Regulation (EU) No 995/2010, for operators, whether natural persons or micro- or small undertakings within the meaning of Article 3(1) or Article 3(2), first subparagraph, respectively, of Directive 2013/34/EU, irrespective of their legal form, who were established as such by 31 December 2024, the Articles referred to in paragraph 2 of this Article shall apply from 30 June 2027.

---

[4] Cite as: [Guidance §3 (part 2/6)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Date of effect and time-frame for application
Similarity: 0.803
— | Furthermore, any relevant product placed or made available on the market by downstream operators or traders after the entry into application that is made entirely from commodities or products placed on the market during the transitional period will not be subject to the obligations of the EUDR. This also means that the deferred entry into application for small and micro enterprise operators (30 June 2027) will, in cases of them placing on the market, also exempt downstream operators and traders further down the supply chain that are trading with these products or their derived products from the obligations of the EUDR.
— | In the cases described above, the obligation of the operators will be limited to gathering adequately conclusive and verifiable evidence to prove that the relevant product was originally placed on the market before the (deferred) entry into application of the Regulation.
— | For parts of a relevant derived product that have been produced with other relevant products placed on the market from 30 December 2026 (or from 30 June 2027 by a micro or small undertakings), the operators and downstream operators placing on the market and the traders will be subject to the standard obligations of the Regulation notwithstanding that some other parts may fall into the transitional period.
According to Article 1(2) EUDR, the EUDR does not apply if relevant products were produced before 29 June 2023. The time and place of production refers to the production date and production place of the relevant commodity, this applies both for the commodities and the derived products. In most cases, the production date will be the time of harvest of the commodity, with the exception of cattle products in which case the relevant time of production is the date on which the cattle is born.
The table below demonstrates the applicable legislation to relevant products falling within scope of the Regulation (EU) 2023/1115, with the exception of timber and timber products covered by the Annex of the EUTR:

---

[5] Cite as: [FAQ 9.1 (part 2/3), p. 85]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are the obligations for downstream operators and traders when they place or make available on the EU market or export a relevant product which is made of a relevant product or a relevant commodity that was placed on the EU market during the transitional period (i.e., the period between the entry into force of the Regulation (29 June 2023) and
Similarity: 0.802
In this case, the obligations of the downstream operator and subsequent downstream operators and traders placing or making available on the EU market or exporting a derived product (chocolate), will be limited to gathering adequately conclusive and verifiable evidence to prove that the relevant derived product (cocoa butter) was placed on the EU market before the entry into application of the Regulation.
For parts of the final releva nt product that have been produced with other relevant products placed on the EU market from 30 December 2026, the downstream operator and subsequent downstream operators or traders will be subject to the standard obligations of the Regulation.
This is without prejudice to Art. 37(2), with regard to timber and timber products. 3.
An operator places on the EU market a relevant commodity or a product in the transitional period, which is then ‘made available’ on the market by one or more traders from 30 December 2026.
In this scenario, the obligations of the trader and subsequent downstream operators and traders will be limited to gathering adequately conclusive and verifiable evidence to prove that such relevant commodity, or relevant product, was placed on the EU market before the entry into application of the Regulation.
This is without prejudice to Art. 37(2) EUDR, with regard to timber and timber products.
Specifically for natural persons and micro and small (upstream) operators, which are subject to the deferred entry into application outlined in Art. 38(3) EUDR, the deferred entry into application for those operators, whether natural persons or micro - or small undertakings, limits the obligations of downstream operators and traders in those supply chains:
Example:
A downstream operator (company B) places on the EU market a product made of a relevant commodity which was placed on the EU market by a n operator that is a natural person or small or micro undertaking (person/company A) before 30 June 2027.
```

</details>

## q04 (single)

**Question:** How long do we have to keep our due diligence records?

**Reference:** Five years from the date the products were placed on the EU market or exported; documentation of due diligence and mitigation measures must be kept for at least five years.

**Answer:**

You must keep all documentation related to due diligence for **at least five years** [EUDR Article 12(5), FAQ 5.8, p. 66]. 

* **Operators:** Must keep information gathered under Art. 9, risk assessment and mitigation documentation, and due diligence statements for five years from the date of placing on the market or export (or from the date of submission for statements) [FAQ 5.8, p. 66].
* **Downstream operators and traders:** Must keep the information listed in Art. 5(3) (including due diligence reference numbers) for at least five years from the date of placing or making available on the market [FAQ 5.8, p. 66].

*(Note: Details regarding record retention periods also rest on FAQ 5.8, which reflects the Commission's views).*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 5.8, p. 66]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How long should documentation be kept?
Similarity: 0.746
How long should the operator keep the documentation used for the due diligence exercise? Do operators, downstream operators and traders have to keep the relevant information about the relevant products they place or make available on the EU market or export? What is considered as the beginning of this duration? (UPDATED) Operators should collect, organise, and keep for five years from the date of the placing on the EU market or export of the relevant commodities and relevant products the information gathered based on Art. 9 EUDR, accompanied by evidence.
Based on the provisions of Art. 10(4) and Art. 11(3) EUDR, operators should be able to demonstrate how due diligence was carried out and what mitigation measures were put in place in case risk was identified.
Relevant documentation about these measures must be saved for at least five years after the due diligence exercise was carried out.
Operators must also keep record of the due diligence statements for five years from the date when the statement is submitted in the Information System, which is prior to the date of placing the product on the EU market or exporting it.
Downstream operators and traders must keep the information listed in Art. 5(3) EUDR for at least five years, including the due diligence reference number(s) or declaration identifier(s) if their supplier is an operator, from the date of the placing, making available on the EU market or exporting of relevant products.

---

[2] Cite as: [EUDR Article 12(5)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Establishment and maintenance of due diligence systems, reporting and record keeping
Similarity: 0.71
5. Operators shall keep for at least five years all documentation related to due diligence, such as all records, measures and procedures pursuant to Article 8. They shall make that documentation available to the competent authorities upon request.

---

[3] Cite as: [Guidance §8 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Regular maintenance of a due diligence system
Similarity: 0.71
Relevant legislation: EUDR – Article 12 – Establishment and maintenance of due diligence systems, reporting and record keeping
To exercise due diligence in accordance with Article 8, operators, including micro or small primary operators, must establish and keep up to date a framework of documenting, analysing, verifying and reporting procedures and measures (‘due diligence system’). The aim of due diligence under the EUDR is to achieve a required outcome by evidencing consistent processes in businesses operations. It is important that in accordance with Article 12(2) an operator shall review its due diligence system at least once a year to ensure that those responsible are following the procedures that apply to them, the processes in place are effective and the required outcome is being achieved. Operators should also update the due diligence system if during the review or at any other point they become aware of new developments which could influence the aims of the due diligence system, such as the effectiveness and comprehensiveness of steps or procedures within the system. Any updates to the due diligence system must be recorded and records kept for 5 years.
The review can be carried out by someone within the organisation of the operator (should be independent from those carrying out the procedures) or by an external body. It should identify any weaknesses and failures and the operator’s management should set deadlines for addressing them.
In the case of a relevant product due diligence system, the review should for example check if there are documented procedures:
— | For collecting and recording the information, data and documents necessary to demonstrate compliance.
— | For assessing the risk of the relevant product or any component of the relevant product containing relevant products or relevant commodities that are not deforestation-free or have not been produced in accordance with the relevant legislation of the country of production.
— | Describing proposed actions to take according to the level of risk.

---

[4] Cite as: [FAQ 7.14, p. 80]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How long will be data of the DDS be saved in the Information system? Is it necessary to export and save data for purpose of archiving?
Similarity: 0.702
The storage of personal data is limited in time by the Commission Implementing Regulation on the functioning of the Information System.
Th e foreseen storage period can be further extended on the individual request of the Information system users or relevant authorities if this is necessary to comply with their responsibilities and obligations under the EUDR.
In line with this, data that does not constitute personal data, as defined, is also stored and accessible in the Information System for the same amount of time.
Users of the information system have the option to export the contents of a DDS into a PDF file, as well as extract geolocation coordinates into a separate file to support their internal record-keeping purposes.

---

[5] Cite as: [FAQ 1.23, p. 20]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is supply chain traceability?
Similarity: 0.697
The information, documents and data which operators need to collect and keep for 5 years to demonstrate compliance with the Regulation are listed in Art. 9 and Annex II as well as in Art. 2(28) EUDR as regards data related to geolocation.
Operators must exercise due diligence with regard to all relevant products supplied by each particular supplier.
Therefore, they must put in place a due diligence system, which includes the collection of information, data and documents needed to fulfil the requirements set out in Art. 9, risk assessment measures as described in Art. 10, and risk mitigation measures as referred to in Art. 11 EUDR.
The requirements for the establishment and maintenance of due diligence systems, reporting and record keeping are listed in Art. 12 EUDR.
In case of operators subject to simplified due diligence (Art. 13 EUDR), the operator ’s due diligence system is limited to the operator’s simplified due diligence obligations (see also FAQ 5.1).
The operators will have to communicate to downstream operators or to traders further down the supply chain the reference numbers of the due diligence statements or, if applicable, the declaration identifiers associated to products covered by a simplified declaration pursuant to Art. 4(7) EUDR.
Downstream o perators and traders further down the supply chain ensure traceability by collecting and keeping information related to their direct business partners (suppliers and commercial clients).
For obligations of downstream operators and traders see FAQ 3.4.
Operators are required to ensure that the information on traceability that they supply to enforcing authorities in the Member States through the due diligence statement or simplified declaration submitted to the Information System is correct.
The development and functioning of the Information System will be in line with the relevant data protection provisions.
In addition, the system will be equipped with security measures that will ensure the integrity and confidentiality of the information shared.
```

</details>

## q05 (single)

**Question:** Our suppliers' cocoa farms are bigger than 4 hectares. Is a single GPS point per farm enough?

**Reference:** No. Plots of more than 4 hectares (other than for cattle) need polygons with latitude and longitude points of six decimal digits describing the perimeter; a single point is allowed only for plots under 4 hectares.

**Answer:**

No, a single GPS point is not enough [FAQ 1.16, p. 17]. 

For plots of land larger than 4 hectares (for commodities other than cattle), geolocation must be provided using polygons consisting of sufficient latitude and longitude points to describe the perimeter of each plot of land, rather than a unique central point [FAQ 1.16, p. 17]. 

*Note: This answer rests solely on the Commission FAQ, which reflects the Commission's views and is not legally binding [FAQ 1.16, p. 17].*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 1.14, p. 16]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Can a polygon cover several plots of land?
Similarity: 0.729
Polygons are to be used to describe the perimeter of the plots of land where the commodity has been produced.
Each polygon should indicate one single plot of land, whether contiguous or not.
Where relevant products are made of commodities from several plots of land, several polygons must be provided in one due diligence statement.
A polygon cannot be used to trace the perimeter of a n area of land that might include plots of land only in some of its parts.

---

[2] Cite as: [FAQ 1.16, p. 17]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Should polygons be provided by means of circumference?
Similarity: 0.727
There is neither an obligation nor a possibility to provide the plot of land information by means of circumference.
For plots of land of more than four hectares (for the production of the relevant commodities other than cattle), geolocation has to be provided using polygons (not a unique central point with a circumference) with sufficient latitude and longitude points to describe the perimeter of each plot of land.

---

[3] Cite as: [FAQ 1.8, p. 15]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Does geolocation need to be provided by means of polygons in all cases?
Similarity: 0.723
No.
For plots of land of a size below four hectares (only), geolocation can be described with one latitude and longitude point only.
In case of cattle, no polygons but only single geolocation points required, notably for all ‘establishments’ (as defin ed in Art. 2(29) EUDR), where cattle have been held.

---

[4] Cite as: [FAQ 1.1 (part 2/2), p. 12]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Why and how must operators collect coordinates?
Similarity: 0.717
These do not require mobile network coverage, only a solid GNSS signal, like those provided by Galileo.
For plots of land of more than 4 hectares used for the production of commodities other than cattle, the geolocation must be provided using polygons, meaning latitude and longitude points of six decimal digits to describe the perimeter of each plot of land.
For plots of land under 4 hectares, operators can use a polygon or a single point of latitude and longitude of six decimal digits to provide geolocation.
Establishments where cattle are kept can be described with a single point of geolocation coordinate.
Please note that the Regulation does not impose direct obligations on producers in third country (unless they are directly placing products on the EU market).
For obligations of downstream operators and traders, see FAQ 3.4.

---

[5] Cite as: [FAQ 1.7, p. 15]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the size of the area (hectares) that can be covered by a polygon?
Similarity: 0.708
There is not a fixed threshold on the minimum or maximum size for plots of land in the Regulation, as long as the plot of land captures the precise area of production and enjoys sufficiently homogeneous conditions to allow an evaluation of the aggregate le vel of risk of deforestation and forest degradation associated with relevant products produced on that land.
See also FAQ 1.2. in relation to the geographic coordinates for plots of under 4 ha.
There is no limit in the area of polygons that can be imported into the Information System, but the total file size of the declaration (either simplified or as a DDS) cannot exceed 25 Mb.
```

</details>

## q06 (single)

**Question:** Can we use a mass balance chain of custody for our cocoa?

**Reference:** No. Mass balance that mixes deforestation-free commodities with commodities of unknown or non-compliant origin is not allowed; compliant commodities must be segregated at every step, although full identity preservation is not required.

**Answer:**

The corpus does not cover this. An answer was drafted, but it could not be traced to the passages the search returned, so it was withheld. Check the cited sources or ask the competent authority.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 1.4, p. 14]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Are mass balance chains of custody allowed?
Similarity: 0.804
The Regulation requires that the commodities used for all products falling under the scope be traceable to the plot of land.
Mass balance chains of custody that allow for the mixing, at any step of the supply chain, of deforestation-free commodities with commodities of unknown origin or non-deforestation- free commodities are not allowed under the Regulation, because they do not guarantee that the commodities placed on the EU market, or exported, are deforestation-free.
Therefore, the commodities placed on the EU market, or exported, need to be segregated from commodities of unknown origin or from non-deforestation-free commodities at every step of the supply chain.
As mass balance is therefore to be ruled out, full identity preservation is not needed.

---

[2] Cite as: [FAQ 1.17, p. 18]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How should the place of production of mixed goods be declared?
Similarity: 0.74
The operator needs to declare the place of production of all goods effectively shipped to the EU.
For example, if compliant goods from multiple places of production are mixed into the same silo, stack, pile, tank, etc., and then some of those goods are placed on the EU market:
• The place of production declared should include the place of production of all goods that entered the silo since it was last empty (and could therefore potentially be included in the shipment) • If the silos are not regularly emptied, the operator would need to declare the place of production of all goods that entered the silo during a period of time that ensures that commodities of unknown place of production are not mixed up in the process.
For instance, when downloading part of the goods stored in the silo, this could be safely done by declaring the geolocation of all previous goods that entered the silo up to a minimum of 200% of the silo capacity, provided that the silo works in first-in first-out system or an equivalent system that ensures the chronological exhaustion of raw materials in the order of their entry.
This approach applies to relevant commodities or products stored in stacks, tanks, etc. and all continuous processing.
• Other approaches are possible for first-in first-out as well as for other storage systems as long as it is ensured that commodities from an unknown place of production or which are incompliant with EUDR are not mixed up in the process.
• Declaring the place of production of x amount of goods that entered the silo, where x is the amount placed on the EU is not allowed under the Regulation, as it would violate the prohibition under the Regulation of placing products of unknown origin on the Union market.
This is without prejudice to the transitional provisions as described in Chapter 9.

---

[3] Cite as: [FAQ 1.3, p. 13]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How does it work for bulk-traded or composite products? What about composite products containing different commodities?
Similarity: 0.738
For products traded in bulk, such as soy or palm oil for instance, this means that the operator needs to ensure that all plots of land involved in a shipment are identified and that the commodities are not mixed at any step of the process with commodities of unknown origin or from areas deforested or degraded after the cut-off date of 31 December 2020.
For relevant composite products, such as e.g. imported wooden furniture with different wood components, the operator needs to geolocate all the plots of land where the relevant commodity (wood, for example) used for the manufacturing process has been produced.
The relevant commodities’ components may be neither of unknown origin nor from areas deforested or degraded after the cut-off date.
In the case of composite products containing multiple different relevant commodities or products (for example, a chocolate bar containing cocoa powder, cocoa butter and palm oil), the operator placing such a product on the EU market or exporting from it will need to conduct due diligence only on the main commodity and (derived) products deemed relevant under the EUDR, this being the commodity contained in the left column of Annex I.
For example, for chocolate bars (Code 1806), the relevant commodity linked to it is cocoa.
This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

---

[4] Cite as: [FAQ 9.1 (part 2/3), p. 85]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are the obligations for downstream operators and traders when they place or make available on the EU market or export a relevant product which is made of a relevant product or a relevant commodity that was placed on the EU market during the transitional period (i.e., the period between the entry into force of the Regulation (29 June 2023) and
Similarity: 0.733
In this case, the obligations of the downstream operator and subsequent downstream operators and traders placing or making available on the EU market or exporting a derived product (chocolate), will be limited to gathering adequately conclusive and verifiable evidence to prove that the relevant derived product (cocoa butter) was placed on the EU market before the entry into application of the Regulation.
For parts of the final releva nt product that have been produced with other relevant products placed on the EU market from 30 December 2026, the downstream operator and subsequent downstream operators or traders will be subject to the standard obligations of the Regulation.
This is without prejudice to Art. 37(2), with regard to timber and timber products. 3.
An operator places on the EU market a relevant commodity or a product in the transitional period, which is then ‘made available’ on the market by one or more traders from 30 December 2026.
In this scenario, the obligations of the trader and subsequent downstream operators and traders will be limited to gathering adequately conclusive and verifiable evidence to prove that such relevant commodity, or relevant product, was placed on the EU market before the entry into application of the Regulation.
This is without prejudice to Art. 37(2) EUDR, with regard to timber and timber products.
Specifically for natural persons and micro and small (upstream) operators, which are subject to the deferred entry into application outlined in Art. 38(3) EUDR, the deferred entry into application for those operators, whether natural persons or micro - or small undertakings, limits the obligations of downstream operators and traders in those supply chains:
Example:
A downstream operator (company B) places on the EU market a product made of a relevant commodity which was placed on the EU market by a n operator that is a natural person or small or micro undertaking (person/company A) before 30 June 2027.

---

[5] Cite as: [FAQ 1.5, p. 14]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if part of a product is non-compliant?
Similarity: 0.729
If part of a relevant product is non-compliant, the non-compliant part needs to be identified and separated from the rest before the relevant product is placed on the EU market or exported, and that part may be neither placed on the EU market nor exported.
If identification and separation cannot be done, for instance because the non-compliant products have been mixed with the rest, then the whole relevant product is non-compliant as it cannot be guaranteed that the conditions of Art. 3 EUDR are met and therefore it may be neither placed on the EU market nor exported.
For instance, when bulk commodities have all been mixed and are linked to several hundred plots of land, the fact that one of the plots of land has been deforested after 2020 would make the whole relevant batch non-compliant.
A product would however not be non-compliant where 100% of relevant commodities or relevant products placed on the EU market 1) can be traced to the plot of land, 2) are legal and deforestation free within the meaning EUDR, and 3) at no point in time has been mixed with commodities of unknown origin or non-deforestation-free.
```

</details>

## q07 (single)

**Question:** We import chocolate bars made with cocoa powder, cocoa butter and palm oil. Which ingredients need due diligence?

**Reference:** Only the cocoa: for chocolate (code 1806) the relevant commodity is cocoa, so due diligence covers the cocoa powder and cocoa butter, not the palm oil.

**Answer:**

*Note: This answer rests on the Commission's Guidance and FAQ, which reflect the Commission's views and are not legally binding.*

For chocolate bars (HS 1806), due diligence and information requirements extend only to the cocoa components (cocoa powder and cocoa butter) under the commodity cocoa [Guidance §9 (part 2/2), FAQ 1.3, p. 13]. 

Even though the chocolate bar contains palm oil, the operator placing it on the EU market is required to conduct due diligence only on the relevant products linked to the main commodity listed in Annex I for that product code, which in this case is cocoa [Guidance §9 (part 2/2), FAQ 1.3, p. 13]. Therefore, the cocoa powder and cocoa butter need due diligence, while the palm oil component in this composite product does not [Guidance §9 (part 2/2), FAQ 1.3, p. 13].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.777
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[2] Cite as: [Guidance §9 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Composite products
Similarity: 0.776
Composite products may contain multiple relevant products under different commodities. For instance, a chocolate bar [HS 1806 ] may comprise derived products of cocoa (cocoa powder [HS 1805 ] and cocoa butter [HS 1804 ]) and oil palm (palm oil [HS 1511 ]). In such cases, the operator placing the product on the EU market or exporting from it will only be required to conduct due diligence on the relevant products listed under the commodity deemed relevant in Annex I of the EUDR. For instance, for chocolate bars [HS 1806 ], the relevant commodity linked to it is cocoa. This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

---

[3] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.771
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;

---

[4] Cite as: [EUDR Article 1]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Subject matter and scope
Similarity: 0.769
1. This Regulation lays down rules regarding the placing and making available on the Union market as well as the export from the Union of relevant products, as listed in Annex I, that contain, have been fed with or have been made using relevant commodities, namely cattle, cocoa, coffee, oil palm, rubber, soya and wood, with a view to: (a) minimising the Union’s contribution to deforestation and forest degradation worldwide, and thereby contributing to a reduction in global deforestation; (b) reducing the Union’s contribution to greenhouse gas emissions and global biodiversity loss.
2. Except as provided for in Article 37(3), this Regulation does not apply to relevant products listed in Annex I produced before the date indicated in Article 38(1).

---

[5] Cite as: [FAQ 1.3, p. 13]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How does it work for bulk-traded or composite products? What about composite products containing different commodities?
Similarity: 0.765
For products traded in bulk, such as soy or palm oil for instance, this means that the operator needs to ensure that all plots of land involved in a shipment are identified and that the commodities are not mixed at any step of the process with commodities of unknown origin or from areas deforested or degraded after the cut-off date of 31 December 2020.
For relevant composite products, such as e.g. imported wooden furniture with different wood components, the operator needs to geolocate all the plots of land where the relevant commodity (wood, for example) used for the manufacturing process has been produced.
The relevant commodities’ components may be neither of unknown origin nor from areas deforested or degraded after the cut-off date.
In the case of composite products containing multiple different relevant commodities or products (for example, a chocolate bar containing cocoa powder, cocoa butter and palm oil), the operator placing such a product on the EU market or exporting from it will need to conduct due diligence only on the main commodity and (derived) products deemed relevant under the EUDR, this being the commodity contained in the left column of Annex I.
For example, for chocolate bars (Code 1806), the relevant commodity linked to it is cocoa.
This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.
```

</details>

## q08 (single)

**Question:** What is the maximum fine for a company that breaks the EUDR?

**Reference:** Member States set the fines, but for legal persons the maximum must be at least 4% of the company's total annual EU-wide turnover in the previous financial year, increased where necessary (e.g. repeated infringements) to remove the economic benefit.

**Answer:**

For legal persons, the maximum fine must be **at least 4%** of the company's total annual Union-wide turnover in the financial year preceding the fining decision, and it must be increased where necessary to exceed any potential economic benefit gained [EUDR Article 25(2)]. 

Member States have the discretion to set higher national fines [FAQ 10.2, p. 94]. In addition to fines, penalties may include product and revenue confiscation, temporary exclusion from public funding, and temporary trading bans [EUDR Article 25(2)].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 25(1)–(2)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Penalties
Similarity: 0.887
1. Without prejudice to the obligations of Member States under Directive 2008/99/EC of the European Parliament and of the Council (5), Member States shall lay down rules on penalties applicable to infringements of this Regulation by operators, downstream operators and traders and shall take all measures necessary to ensure that they are implemented. Member States shall notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendments affecting them.
2. The penalties provided for in paragraph 1 shall be effective, proportionate and dissuasive. Those penalties shall include: (a) fines proportionate to the environmental damage and the value of the relevant commodities or relevant products concerned, calculating the level of such fines in such way as to ensure that they effectively deprive those responsible of the economic benefits derived from their infringements, and gradually increasing the level of such fines for repeated infringements; in the case of a legal person, the maximum amount of such a fine shall be at least 4 % of the operator’s, downstream operator’s or trader’s total annual Union-wide turnover in the financial year preceding the fining decision, calculated in accordance with the calculation of aggregate turnover for undertakings laid down in Article 5(1) of Council Regulation (EC) No 139/2004 (6), and shall be increased, where necessary, to exceed the potential economic benefit gained; (b) confiscation of the relevant products concerned from the operator, downstream operator and/or trader; (c) confiscation of revenues gained by the operator, downstream operator and/or trader from a transaction with the relevant products concerned; (d) temporary exclusion for a maximum period of 12 months from public procurement processes and from access to public funding, including tendering procedures, grants and concessions; (e) temporary prohibition from placing or making available on the market or exporting relevant commodities and relevant products, in the event of a serious infringement or of repeated infringements; (f) prohibition from exercising the simplified due diligence set out in Article 13 in the event of a serious infringement or of repeated infringements.

---

[2] Cite as: [FAQ 10.2, p. 94]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the maximum level of fine?
Similarity: 0.86
Member States have the discretion to define the penalties, including the level of fine.
For legal persons the maximum level of the penalty cannot be lower than 4 % of the operator’s, downstream operator’s or trader’s total annual Union-wide turnover in the financial year preceding the fining decision, calculated in accordance with the calculation of aggregate turnover for undertakings laid down in Art. 5(1) of Council Regulation (EC) No 139/2004.
The level of fine should increase where necessary, particularly in case of repeated infringements.
The penalties should ensure that they effectively deprive those responsible of the economic benefits derived from their infringements, in accordance with the effective, proportionate, and dissuasive principle.

---

[3] Cite as: [FAQ 10.1, p. 94]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What does it mean that the penalties laid down by the EU Member States are without prejudice to the obligations of Member States under Directive 2008/99/EC of the European Parliament and of the Council?
Similarity: 0.832
The EU Member States must lay down the national framework of penalties, which should include at least the penalties listed in Art. 25(2) EUDR and must take all measures necessary to ensure that the rules are implemented.
The level and type of penalties cannot be in contradiction with the Environmental Crime Directive.
The provisions of the Directive are subject to the succession of law.

---

[4] Cite as: [FAQ 10.5, p. 95]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | I have cut down a few small trees on my property where I now raise some cows. I intend to sell the timber and the meat of the cows on a local market in the EU. Will there be penalties imposed on me for selling them as I cut the trees?
Similarity: 0.818
Generally, the responsibility for enforcement of the provisions lies with the Member States.
Requiring operators, downstream operators and traders to take corrective measures, as stipulated in Art. 24 EUDR, falls under the discretion of Competent Authorities of Member States.
In the EU, the principle of proportionality is one of the general principles of Union law which applies to the interpretation and enforcement of Union legislation.
Cutting down trees can only constitute a breach of the deforestation-free requirement under the Regulation if the trees are part of a forest as defined in the Regulation.
This is the case if the trees are part of land which is not under predominantly agric ultural or urban land use spanning more than 0,5 hectares with trees higher than 5 metres and a canopy cover of more than 10 %, or trees able to reach those thresholds in situ.
If one of these criteria is not met, the area is not a forest and the cutting d own the trees does not breach a provision of the deforestation-free requirement of the Regulation.

---

[5] Cite as: [EUDR Article 25(3)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Penalties
Similarity: 0.793
3. Member States shall notify the Commission of final judgments against legal persons for infringements of this Regulation and the penalties imposed on them, within 30 days from the date on which the judgments become final, taking into account the relevant data protection rules. The Commission shall publish on its website a list of such judgments, which shall contain the following elements: (a) the name of the legal person; (b) the date of the final judgment; (c) a summary of the activities for which the legal person was found to have infringed this Regulation; and (d) the nature and, where financial, the amount of the penalty imposed.
```

</details>

## q09 (single)

**Question:** Is a very small shipment of cocoa exempt from the EUDR?

**Reference:** No. There is no volume or value threshold; any quantity of a product listed in Annex I is covered.

**Answer:**

No, there is **no threshold volume or value** below which commercial shipments of cocoa are exempt from the EUDR [FAQ 2.3, p. 25]. 

*Note: This answer rests on the Commission's FAQ, which is not legally binding.*

**Details:**
* **Commercial shipments:** Any quantity of cocoa included in Annex I (such as cocoa beans, paste, butter, or chocolate) placed on the market or exported in the course of a commercial activity is subject to the Regulation [FAQ 2.3, p. 25, EUDR Annex I].
* **Exceptions:** A shipment is exempt only if it is for private use or consumption (e.g., non-commercial consumer parcels or personal travel goods) [FAQ 3.16, p. 45], or if it consists strictly of samples of negligible quantity used solely for objective testing, sensory evaluation, or soliciting orders as outlined in draft rules [FAQ 2.14, p. 32].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 3.16, p. 45]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What does the sentence “not intended directly for private use or consumption within the customs territory of the Union” mean in the definition of Art. 2(38) EUDR?
Similarity: 0.767
(NEW) The EUDR applies to ‘products intended to be placed on the Union market’ ‘in the course of a commercial activity’ regardless of whether the client of that commercial activity is a business (B2B) or a private individual (B2C).
This means that products ‘intended for private use or consumption within the customs territory of the Union’ (i.e.
C2C: consumer to consumer) are not covered by the EUDR.
Examples of such private uses/consumption are:
• A person bringing relevant products from a vacation trip outside the EU for their private use or consumption, in reasonable quantities for a private use and thus not for resale.
• A person in a third country sending products to a person in the EU (e.g., parcels between relatives).
For all shipments of relevant products to be placed on the Union market, EUDR Competent Authorities and customs authorities may control whether the products are intended for private use or consumption and thus exempted from EUDR according to Art. 2(38) EUDR.
This assessment is made on a case-by-case basis, depending on the specific circumstances, such as quantities of relevant products and frequency of such private uses6.

---

[2] Cite as: [FAQ 2.3, p. 25]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Does the Regulation apply regardless of quantity or value?
Similarity: 0.766
There is no threshold volume or value of a relevant commodity or relevant product, including within processed products, below which the Regulation would not apply.
Operators, downstream operators and traders placing or making available on the EU market or exporting a relevant product included in Annex I, whatever its quantity, are subject to the obligations of the Regulation.

---

[3] Cite as: [FAQ 2.14, p. 32]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Are samples and products used for examination, analysis or testing purposes in scope of the EUDR?
Similarity: 0.758
In a draft Delegated Act published for public feedback, it is proposed that samples of products, which are of negligible value and quantity and can be consumed or used only to solicit orders for goods of the type they represent under the condition that the manner of presentation and quantity, for products of the same type or qualit y, rule out its consumption or use for any purpose other than that of seeking orders, are not in the scope of the Regulation.
The same, meaning that EUDR obligations do not apply, applies to products which are to undergo examination, analysis or tests to determine their composition, quality or other technical characteristics for purposes of information or industrial or commercial research under the condition that the products to be analysed, examined or tested are either completely used up or destroyed in the course of the examination, analysis or testing, or kept or returned for no other reason and purposes than complying with legal or contractual obligations related to examination, analysis or testing.
Examples of supplies of samples and products used for examination, analysis or testing purposes include:
• A supplier sending tyres to a vehicle manufacturer for the recipient to test its quality and durability – the tyres will be destroyed in the course of testing.
• A supplier sending small quantities of a new ingredient (e.g. cocoa or coffee beans) to a food manufacturer for the purpose of sensory evaluation, and to test its quality and food safety within the business.
The ingredient is completely used up in the course of analysis and testing.
In this case, the supplier and the food manufacturer are out of scope if the ingredient is clearly intended to be used for analysis and testing purposes given the contractual arrangements and surrounding circumstances.
• A coffee company importing a small sample of coffee beans from a new area of production to use and consume them in their business in order to decide whether to order a large amount of coffee beans from the same area.

---

[4] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.75
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[5] Cite as: [Guidance §1(c)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Export
Similarity: 0.749
Under Article 2(37), ‘export’ refers to the customs export procedure as laid down in Article 269 of Regulation (EU) No 952/2013 () and refers to Union goods to be taken out of the customs territory of the Union.
Article 269 of Regulation (EU) No 952/2013 states that the export procedure shall not apply to: (a) goods placed under the outward processing procedure; (b) goods taken out of the customs territory of the Union after having been placed under the end-use procedure; (c) goods delivered, VAT or excise duty exempted, as aircraft or ship supplies, regardless of the destination of the aircraft or ship, for which a proof of such supply is required; (d) goods placed under the internal transit procedure; (e) goods moved temporarily out of the customs territory of the Union in accordance with Article 155 of Regulation (EU) No 952/2013.
Re-export as laid down in Article 270 of Regulation (EU) No 952/2013 is not within the scope of the EUDR. Re-export in this regard means, that the relevant commodity or relevant product has not acquired ‘Union goods’ status and is taken out of the customs territory of the Union after lodging e.g. re-export declaration.
‘Relevant products leaving the market’ should therefore be understood as occurring when relevant products are declared to be placed under the customs procedure ‘export’ in the course of a commercial activity.
```

</details>

## q10 (single)

**Question:** Can a sustainability certification scheme replace our due diligence?

**Reference:** No. Certification can support the risk assessment where it covers the required information, but the operator must still exercise due diligence and remains responsible for any breach.

**Answer:**

**No, a sustainability certification scheme cannot replace your due diligence.** 

*(Note: This answer rests on the Commission Guidance and FAQ, which reflect the Commission's views and are not legally binding.)*

While certification and third-party verification schemes can provide useful information for your risk assessment under Article 10, they cannot substitute your legal responsibility as an operator to exercise due diligence under Article 8 [Guidance §10 (part 2/2)]. Using such a scheme does not grant a "green lane"—you remain fully liable if the due diligence requirements are breached [Guidance §10 (part 2/2), FAQ 5.7, p. 66].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [Guidance §10 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | The role of certifications and third-party verification schemes in risk assessment and risk mitigation
Similarity: 0.795
Relevant legislation: EUDR – Recital (52); Article 10(2)(n) – Risk assessment
Certification and third-party verified schemes are often used to meet specific customer requirements for relevant commodities and relevant products. This may include a standard that describes practices that must be implemented during production of the certified commodities, comprising principles, criteria and indicators; requirements for checking compliance with the standard and awarding certificates; and separate chain-of-custody certification to provide assurance along the supply chain that a product contains only (or in some cases a specified percentage of) certified or third-party verified material from identified and certified or third-party verified producers.
The EUDR acknowledges that certification and other third-party verified schemes may provide useful information on compliance with the Regulation in the risk assessment further to Article 10 by supporting evidence that products are legal and deforestation-free. This is subject to the condition that this information meets the relevant requirements set out in Article 9, as stipulated in Article 10(2)(n).
Indeed, certifications and third-party verified schemes are operated by an organisation that is not a participant in the production or the supply chain of the relevant commodity. Furthermore, some of these schemes are often used to verify that certain standards or rules are being followed, but do not necessarily go as far as certifying the product itself.
This guidance is directed primarily to stakeholders considering making use of certification or third-party verified schemes given their potential added value in providing complementary information, such as on geolocation coordinates and supporting the operators’ risk assessment undertaken as part of their due diligence exercise that relevant products are legal and deforestation-free. The EUDR does not oblige: (1) operators to make use of such schemes, (2) producers to sign up to them, nor (3) producer countries to develop such schemes. Making use of third-party verification schemes is not a legal requirement, but a voluntary decision of the operator. If operators decide to make use of these schemes, this guidance is designed to help them assess the degree to which these schemes can support to meet the requirements of the EUDR.

---

[2] Cite as: [Guidance §10 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | The role of certifications and third-party verification schemes in risk assessment and risk mitigation
Similarity: 0.786
Certification and third-party verified schemes can play an important role in promoting sustainable agricultural and forestry practices and responsible sourcing, in fostering supply chain transparency and in facilitating compliance. To note that self-declaration schemes that do not rely on third party attestation procedures are outside of the scope of this guidance and are, by definition, less robust because of the lack of independence and impartiality.
This guidance is also relevant for national competent authorities by underlining that while such schemes can be used in the risk assessment procedure under Article 10, they cannot substitute the operator’s responsibility as regards due diligence further to Article 8. This means that the use of such schemes does not imply a ‘green lane’, since the operator is still required to exercise due diligence and is held liable if it fails to comply with the due diligence requirements of the EUDR.
There is a great diversity of schemes in terms of their scope, their objectives, their structure and their operating methods. One important distinction is (1) whether or not they rely on a third-party attestation procedure, thereby grouping them into certification and third-party verified schemes on the one hand and (2) self-declaration schemes on the other. The latter are outside of the scope of this guidance document and are, by definition, less robust because of the lack of independence and impartiality.

---

[3] Cite as: [Guidance §10(a) (part 2/3)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | The role of certifications and third-party verification schemes
Similarity: 0.775
— | validity, authenticity, and relevance of the scope of the certification or third-party verification (e.g. whether it covers the relevant commodities and products regulated under the EUDR),
— | inclusion and compliance with relevant legal requirements, such as the alignment with the definition of deforestation-free and the cut-off date of 31 December 2020, as stipulated in Articles 2 and 3 of the EUDR,
— | assessment of the risk of non-compliance regarding legality and the deforestation-free requirements of the relevant product,
— | traceability of the relevant products, including via geolocation back to the plot of land,
— | possibility to mix known origin and unknown origin material within the chain of custody (CoC) model (which is not acceptable under the EUDR) (). A relevant product with CoC certification may also contain a mix of certified and non-certified material from a variety of sources, for which information about whether checks on the non-certified portion have been performed and whether those checks provide adequate evidence of compliance with the EUDR requirements must be obtained. The due diligence procedure must therefore be completed for the relevant product in entirety,
— | possibility to use mass balance where compliant products are mixed with products of unknown origin (which is not acceptable under the EUDR) (),
— | ability of the scheme to provide required information accompanied by evidence that is ‘adequately conclusive and verifiable’, as set out in Article 9.
Secondly, under (2) ‘the implementation by schemes’, operators should consider:
— | accessibility of information regarding the scheme governance, engagement of stakeholders with the scheme, and summaries of audits,
— | free and publicly accessible database about certification holders, their scope of coverage, validity, date of suspending or terminating certification status and related audit reports,
— | transparent periodic, random and independent checks (including through audits) on compliance of the certification or third-party verification scheme with their own standards, rules and procedures,

---

[4] Cite as: [Guidance §10(a) (part 1/3)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | The role of certifications and third-party verification schemes
Similarity: 0.769
In considering whether to make use of information supplied by a certification scheme or third-party verified scheme in the risk assessment procedure under Article 10 as supporting evidence that the product is legal and deforestation-free, an operator should, as a first step, determine whether the scheme’s standards are in accordance with relevant provisions of the EUDR. In this regard, it should be pointed out that operators may also use third party verification schemes or certification schemes for compliance with only certain requirements of the Regulation.
Certification and third-party verification schemes generally require third-party organisations to be able to demonstrate their qualifications to perform assessments through a process of accreditation that sets standards for the skills of auditors and the systems that the certification organisations must adhere to. Certified or verified products generally carry a label with the certification or verification organisation’s name and type as well as the requirements for the auditing process. The scheme may also require that partners have this information included in the formal documents accompanying the shipment. These organisations will normally be able to provide information on coverage of the certification and how it was applied in the country of production of the relevant products, including details about the nature and frequency of field audits.
Certification and third-party verification schemes can be assessed according to three main elements: (1) ‘the relevant standards’, i.e. operating requirement, scope, procedures, policies for companies adhering to these schemes, (2) ‘the implementation by the schemes’, i.e. the extent to which the standards are implemented, including by deploying the necessary measures to ensure compliance also via audits and (3) ‘governance features’/credibility assessment of the schemes such as transparency, assurance processes, oversight etc. Such information should be regularly reassessed by the operator, especially in relation to the requirements of the EUDR.
Regarding EUDR requirements, insofar as this is relevant to the information provided by the certification or third-party verification scheme, operators should scrutinise the following aspects of the certification or third-party verification schemes under (1) ‘the relevant standards’:

---

[5] Cite as: [FAQ 5.7, p. 66]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the role of certification or verification schemes?
Similarity: 0.765
Certification schemes can be used by supply chain members to help their risk assessment to the extent the certification covers the information needed to comply with their obligations under the regulation.
Operators will still be required to exercise due di ligence, and they will remain responsible for any breach.
The European Commission’s Guidance document provides further explanations on the role of certification and third-party verification schemes in risk assessment and risk mitigation.
```

</details>

## q11 (single)

**Question:** What should we do if a supplier in Côte d'Ivoire will not give us the geolocation of the farms?

**Reference:** If the required information cannot be obtained from suppliers, the products must not be placed on the EU market or exported; doing so would violate the Regulation.

**Answer:**

If you cannot obtain geolocation data from your supplier, **you must not place the cocoa on the EU market or export it** [FAQ 1.19, p. 19; FAQ 1.27, p. 23]. 

Collecting geolocation coordinates of the plots of land of production is a mandatory requirement under the Regulation [FAQ 1.1 (part 1/2), p. 12]. If an operator cannot collect this information, doing so anyway violates the Regulation [FAQ 1.27, p. 23]. 

*Note: This answer is based on the Commission's FAQ, which is not legally binding [FAQ 1.19, p. 19; FAQ 1.27, p. 23].*

<details><summary>Retrieved passages</summary>

```
Error executing tool search: 1 validation error for searchArguments
query
  Field required [type=missing, input_value={'queries': ['geolocation...er due diligence EUDR']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing

=====

[1] Cite as: [FAQ 1.10, p. 15]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if property registers or titles are unavailable?
Similarity: 0.805
How can operators obtain geolocation data in countries where property registers are incomplete and where farmers may lack IDs or titles over their land? (UPDATED) Farmers can collect the geolocation of their plots of land regardless of whether they are entered or not in a land registry or the lack of IDs or titles over their land.
Unless they are direct suppliers of the operators or operators themselves, no personal information is required from the farmers and the geolocation of the plot used to supply commodities for placing on the EU market is sufficient.
As regards the legality requirement in relation to land use right (Art. 2(40) (a) EUDR) the Regulation requires compliance with relevant national laws.
If farmers are legally allowed to sell their product under national laws (which might lack a property register and where some farmers might lack IDs), then that would also mean that operators would meet the legality requirement when sourcing from those farmers.
If possession of a land title is not required under domestic law to produce and commercialise agricultural products, then it is not required under the Regulation.
Operators, nonetheless, would need to verify that there is no risk of illegality in their supply chains, meaning that relevant laws applicable in the country of production are complied with.
There are many different means that operators already use today to collect the legality (and geolocation) information: some resort to mapping directly their suppliers, while others rely on intermediaries like cooperatives, certification bodies, national traceability systems or other companies.
Operators are legally responsible for ensuring that the geolocation and legality information is correct, regardless of the means or intermediaries they use to collect that information.

---

[2] Cite as: [FAQ 1.1 (part 1/2), p. 12]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Why and how must operators collect coordinates?
Similarity: 0.804
The Regulation requires operators placing covered products on the EU market or exporting them to collect geographic coordinates of the plots of land where the commodities were produced.
This does not apply to downstream operators who place on the market or export such products (for more information on downstream operators, see Chapter 3 of this document).
Traceability to the plot of land (i.e., the requirement to collect the geographic coordinates of the plots of land where the commodities were produced) is necessary to demonstrate that there has been no deforestation at the specific location of production.
Geographic information linking products to the plot of land is already used by part of the industry and a number of certification organisations.
Remotely sensed information (air photos, satellite images) or other information (e.g., photograph in the field with linked geotags and time stamps) may be used for verifying if the geolocation of declared commodities and products is linked to deforestation.
The geolocation coordinates need to be provided in the due diligence statements (hereinafter referred to as “ due diligence statement” or “ DDS”) or, where applicable, in the simplified declarations (hereinafter referred to as “simplified declaration” or “SD”) that operators are required to submit to the Information System ahead of the placing on the EU market or export from the EU of the products.
It is therefore a core part of the Regulation, which prohibits the placing on the EU market, or the export, of any product covered by the Regulation’s scope whose geolocation coordinates have not yet been collected and submitted as part of a due diligence statement.
The only exception is the SD of micro or small primary operators (MSPO), for whom the geolocation may be replaced by a postal address, provided that the postal address clearly corresponds to the geographic location of the plots of land or establishment concerned (see FAQ 3.28 for more details).
Collecting the geolocation coordinates of a plot of land can be done via mobile phones, handheld Global Navigation Satellite System (GNSS) devices and widespread and free-to-use digital applications (e.g.
Geographic Information Systems (GIS)).

---

[3] Cite as: [FAQ 1.19, p. 19]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How will geolocation allow claims to be checked in practice?
Similarity: 0.794
How will geolocation allow for checking the validity of a no-deforestation claim in practice? Is it aligning satellite navigation positioning and deforestation maps? Will there be baseline maps that forest areas or areas that have undergone deforestation and forest degradation? How will it work if geolocation of farms, plantations or concessions are not available? It is the responsibility of the operator to collect the geolocation coordinates of the plots of land where the commodities were produced.
If the operator cannot collect the geolocation of all plots of land contributing to a relevant product, then they should not place that product on the EU market or export it, in accordance with Art. 3 EUDR.
Operators (and non-SME downstream operators and traders) and enforcing authorities may cross-check the geolocation coordinates against satellite images or forest cover maps to assess if the products meet the deforestation-free requirement of the Regulation.

---

[4] Cite as: [FAQ 1.31, p. 24]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How can producers share the geolocation data when certain governments prohibit the sharing of such data?
Similarity: 0.792
One of the core requirements for operators under this Regulation is to collect the geolocation information on the plot(s) of land where commodities and products placed on or exported from the EU market have been produced (Art. 9(1)(d) EUDR).
Operators cannot rely on the existence of national laws prohibiting the sharing of such (public) data with operators in order to be exempt from the obligation to collect and upload that data into the Information System.
Operators must submit the geoloca tion information as part of their obligations; otherwise, the operators cannot comply with the requirements on due diligence according to Art. 8 and, therefore cannot place on or export relevant products from the EU market. °°°°

---

[5] Cite as: [FAQ 1.27, p. 23]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if upstream suppliers do not provide required information?
Similarity: 0.791
If an operator, downstream operator or a trader placing or making available a commodity on the EU market or exporting it is unable to obtain the information required by the Regulation from its suppliers, they must refrain from placing or making available the relevant products on the EU market or exporting them from the EU as that would result in a violation of the Regulation.
```

</details>

## q12 (single)

**Question:** Do we still need farm coordinates for cocoa from a country classified as low risk?

**Reference:** Yes. There is no exception from the geolocation (traceability) requirement for low-risk countries.

**Answer:**

Yes, farm coordinates (or plot geolocation) are still required, even for cocoa from a country classified as low risk [FAQ 1.28, p. 23]. 

There is no exception to the traceability requirement via geolocation based on country risk classification [FAQ 1.28, p. 23]. While low-risk countries benefit from simplified due diligence (meaning operators are exempt from risk assessment and risk mitigation under Articles 10 and 11), the obligation to collect information—including geographic coordinates of the plots of land where the cocoa was produced—still applies under Article 9 [FAQ 1.28, p. 23, Guidance §4(e)]. 

*(Note: This answer rests on the Commission FAQ and Guidance, which reflect the Commission's views and are not legally binding.)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 1.28, p. 23]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Should coordinates be provided for land in countries classif ied as low-risk?
Similarity: 0.763
(UPDATED) There is no exception for the traceability requirement via geolocation (or, in the case of a micro or small primary operator, the postal address).
The operators also have to assess the complexity of the relevant supply chain and the risk of circumvention of the Regulation and the risk of mixing with products of unknown origin or origin in high-risk or standard-risk countries or parts thereof (Art. 13 EUDR).
If the operator obtains or is made aware of any relevant information that would point to a risk that the relevant products do not comply with the Regulation or that the Regulation is circumvented, the operator must fulfil all the obligations under Art. 10 and 11 EUDR and must immediately communicate any relevant information to the Competent Authority.

---

[2] Cite as: [FAQ 1.1 (part 1/2), p. 12]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Why and how must operators collect coordinates?
Similarity: 0.762
The Regulation requires operators placing covered products on the EU market or exporting them to collect geographic coordinates of the plots of land where the commodities were produced.
This does not apply to downstream operators who place on the market or export such products (for more information on downstream operators, see Chapter 3 of this document).
Traceability to the plot of land (i.e., the requirement to collect the geographic coordinates of the plots of land where the commodities were produced) is necessary to demonstrate that there has been no deforestation at the specific location of production.
Geographic information linking products to the plot of land is already used by part of the industry and a number of certification organisations.
Remotely sensed information (air photos, satellite images) or other information (e.g., photograph in the field with linked geotags and time stamps) may be used for verifying if the geolocation of declared commodities and products is linked to deforestation.
The geolocation coordinates need to be provided in the due diligence statements (hereinafter referred to as “ due diligence statement” or “ DDS”) or, where applicable, in the simplified declarations (hereinafter referred to as “simplified declaration” or “SD”) that operators are required to submit to the Information System ahead of the placing on the EU market or export from the EU of the products.
It is therefore a core part of the Regulation, which prohibits the placing on the EU market, or the export, of any product covered by the Regulation’s scope whose geolocation coordinates have not yet been collected and submitted as part of a due diligence statement.
The only exception is the SD of micro or small primary operators (MSPO), for whom the geolocation may be replaced by a postal address, provided that the postal address clearly corresponds to the geographic location of the plots of land or establishment concerned (see FAQ 3.28 for more details).
Collecting the geolocation coordinates of a plot of land can be done via mobile phones, handheld Global Navigation Satellite System (GNSS) devices and widespread and free-to-use digital applications (e.g.
Geographic Information Systems (GIS)).

---

[3] Cite as: [Guidance §4(e)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Simplified due diligence, i.e. sourcing from low-risk countries
Similarity: 0.746
Operators sourcing from low-risk countries are required to exercise due diligence in line with Article 8, fulfil information requirements of Article 9 and establish a due diligence system in line with Article 12.
However, in accordance with Article 13, they are not required to fulfil the obligations under Article 10 and Article 11 where, after having assessed:
(i) | the complexity of the relevant supply chain; and
(ii) | the risk of circumvention or mixing with products of unknown origin, or origin in high-risk or standard-risk countries or parts thereof, they have ascertained that all relevant commodities and products they place on the market or export have been produced exclusively in such countries or parts thereof that were classified as low risk in accordance with Article 29 ().
For simplified due diligence under Article 13, no further steps of assessing the information or mitigating risk are required unless, in the course of information collection or in the course of the assessment required by Article 13 itself, operators are made aware of relevant new information indicating that a relevant product that they intend to place on the market or export is at risk of not complying with the Regulation.
Micro or small primary operators are, generally, not required to carry out risk assessment and risk mitigation as they are by definition an operator sourcing from low-risk country, unless they obtain or are made aware of any relevant information pointing to a non-negligible risk that the relevant products are non-compliant.

---

[4] Cite as: [FAQ 1.10, p. 15]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if property registers or titles are unavailable?
Similarity: 0.744
How can operators obtain geolocation data in countries where property registers are incomplete and where farmers may lack IDs or titles over their land? (UPDATED) Farmers can collect the geolocation of their plots of land regardless of whether they are entered or not in a land registry or the lack of IDs or titles over their land.
Unless they are direct suppliers of the operators or operators themselves, no personal information is required from the farmers and the geolocation of the plot used to supply commodities for placing on the EU market is sufficient.
As regards the legality requirement in relation to land use right (Art. 2(40) (a) EUDR) the Regulation requires compliance with relevant national laws.
If farmers are legally allowed to sell their product under national laws (which might lack a property register and where some farmers might lack IDs), then that would also mean that operators would meet the legality requirement when sourcing from those farmers.
If possession of a land title is not required under domestic law to produce and commercialise agricultural products, then it is not required under the Regulation.
Operators, nonetheless, would need to verify that there is no risk of illegality in their supply chains, meaning that relevant laws applicable in the country of production are complied with.
There are many different means that operators already use today to collect the legality (and geolocation) information: some resort to mapping directly their suppliers, while others rely on intermediaries like cooperatives, certification bodies, national traceability systems or other companies.
Operators are legally responsible for ensuring that the geolocation and legality information is correct, regardless of the means or intermediaries they use to collect that information.

---

[5] Cite as: [FAQ 1.19, p. 19]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How will geolocation allow claims to be checked in practice?
Similarity: 0.726
How will geolocation allow for checking the validity of a no-deforestation claim in practice? Is it aligning satellite navigation positioning and deforestation maps? Will there be baseline maps that forest areas or areas that have undergone deforestation and forest degradation? How will it work if geolocation of farms, plantations or concessions are not available? It is the responsibility of the operator to collect the geolocation coordinates of the plots of land where the commodities were produced.
If the operator cannot collect the geolocation of all plots of land contributing to a relevant product, then they should not place that product on the EU market or export it, in accordance with Art. 3 EUDR.
Operators (and non-SME downstream operators and traders) and enforcing authorities may cross-check the geolocation coordinates against satellite images or forest cover maps to assess if the products meet the deforestation-free requirement of the Regulation.
```

</details>

## q13 (single)

**Question:** Our cocoa beans are grown in one country and ground into paste in another. Whose laws count for the legality requirement?

**Reference:** Only the laws of the country of production, i.e. the country where the cocoa was harvested, not the country of further manufacturing.

**Answer:**

The legality requirement covers only the laws of the country where the cocoa beans were grown and harvested (the country of production), not the laws of the country where they were ground into paste [FAQ 1.29.1, p. 23]. 

*(Note: This answer rests on the Commission FAQ, which reflects the Commission's views and is not legally binding.)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 1.29.1, p. 23]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | A commodity is harvested in country A and transported to country B for further manufacturing (e.g. cocoa beans from A are manufactured into cocoa powder in B) before the cocoa powder is placed on the EU market in country C. The laws applicable in which country are relevant?
Similarity: 0.77
In the given example, country A is the country of production, meaning the legality requirement only covers laws that are applicable in country A.

---

[2] Cite as: [FAQ 3.3 (part 1/2), p. 35]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What does ‘relevant legislation of the country of production’ mean?
Similarity: 0.765
Relevant commodities and products can only be placed on the EU market if they comply with the three requirements of Art. 3 EUDR, namely (1) they are deforestation-free (Art. 3(a)), (2) comply with the relevant legislation of the country of production (Art. 3(b)), and (3) are covered by a due diligence statement or a simplified declaration (Art.3(c)). ‘Relevant legislation’ may include, among others, national laws (including relevant secondary law) and international law as applicable in domestic law. ‘Country of production’ means the country in which a relevant commodity was produced (see Art. 2(24) EUD R). ‘Produced’ means grown, harvested, obtained from or raised on relevant plots of land or, as regards cattle, on establishments (see Art. 2(14) EUDR).
Consequentially, legislation of other countries in which further steps of a manufacturing process may h ave taken place are not relevant for the legality requirement (for instance, soy beans harvested in country A (country of production) being manufactured into soymeal in country B prior to being placed on the EU market in country C).
The Regulation provides a list of legislative areas without specifying particular legal acts, as these differ from country to country and may be subject to amendments.
According to the definition, the legislation listed in Art. 2(40) letters (a) to (h) must be interpreted as bei ng concerned with the legal status of the area of production.
Additionally, for the different fields of legislation, the meaning and purpose stipulated in Art. 1(1)(a) and (b) EUDR should be taken into account.
Therefore, among others, legislation with a link to the protection of forests, the reduction of greenhouse gas emissions or the protection of biodiversity is relevant.
Relevant documentation is required for the purposes of the information collection and risk assessment pursuant to Art. 9(1)(h) and 10 EUDR.
Such documentation may, for example, consist of official documents from public authorities, contractual agreements, court decisions or impact assessments and audits which may have been carried out.

---

[3] Cite as: [Guidance §6]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Legality
Similarity: 0.748
Relevant legislation: EUDR – Article 2(40) – Definitions and Article 3(b) – Prohibition
According to Article 3 of the EUDR, relevant commodities and relevant products shall not be placed or made available on the market or exported, unless all the following conditions are fulfilled:
(a) | they are deforestation-free;
(b) | they have been produced in accordance with the relevant legislation of the country of production; and
(c) | they are covered by a due diligence statement or a simplified declaration.
Relevant products must meet all three criteria separately and individually; otherwise, operators shall refrain from placing on the market or exporting them.

---

[4] Cite as: [Guidance §6(b) (part 1/4)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Due diligence regarding legality
Similarity: 0.742
Operators must be aware of what legislation exists in each of the countries they are sourcing from as to the legal status of the area of production. The relevant legislation can, among others, consist of:
— | national and regional laws, including relevant secondary legislation, and
— | international law, including multi- and bilateral treaties and agreements, as applicable in domestic law by codifying and implementing them, respectively.
Under Article 9(1)(h) of the EUDR, information, including documents and data showing compliance with applicable legislation in the country of production, must be collected as part of the due diligence obligation. Paragraph 1(h) further specifies that such information must be adequately conclusive and verifiable.
In this context, the nature and extent of the information to be collected depends on the specific supply chain, production area and country of production. Operators may use, as listed below, a broad range of credible information sources that, taken as a whole, allow a reasoned conclusion that the relevant commodities have been produced in accordance with the relevant legislation of the country of production. In line with Article 9(2), operators must make available to the competent authorities upon request the information, documents and data collected under this point. To facilitate enforcement, operators should be able to explain the presence of certain documents and the absence of others.
In-depth evidence collection should be prioritised for supply chains, production areas and countries of production where an initial examination of the information available to the operator indicates a higher risk of non-compliance with Article 3(b). By contrast, for supply chains, production areas and countries of production where the initial examination of available information indicates a negligible risk of non-compliance with Article 3(b), operators should not be required to carry out an in-depth data collection. For instance, they should not be required to systematically collect comprehensive legal documentation for each individual plot of land, to obtain specific types of documents such as individual land titles, or to compile an exhaustive list of all potentially relevant laws, legal documents or data.

---

[5] Cite as: [Guidance §6(a) (part 1/3)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Relevant legislation of the country of production
Similarity: 0.736
The basis for determining whether a relevant commodity or relevant product has been produced in accordance with the relevant legislation of the country of production is the legislation of the country in which the commodity, or in the case of a product, the commodity contained in a relevant product was grown, harvested, obtained from or raised on relevant plots of land or, as regards cattle, in establishments.
The EUDR takes a flexible approach by listing a number of areas of law without specifying particular laws, as these differ from country to country and may be subject to amendments. However, only the applicable laws concerning the legal status of the area of production constitute relevant legislation pursuant to Article 2(40) of the EUDR. This means that, generally, the relevance of laws for the legality requirement in Article 3(b) of the EUDR is not determined by the fact that they may apply generally during the production process of commodities or apply to the supply chains of relevant products and relevant commodities, but by the fact that these laws specifically impact or influence the legal status of the area in which the commodities were produced.
Additionally, Article 2(40) of the EUDR must be read in the light of the objectives of the EUDR as laid down in Article 1(1)(a) and (b), meaning that legislation is also relevant if its contents can be directly linked to halting deforestation and forest degradation in the context of the Union’s commitment to address climate change and biodiversity loss.
Points (a) to (h) of Article 2(40) further specify this relevant legislation. The following list gives some concrete examples which are for illustration purposes only and cannot be considered exhaustive:
— | Land use rights, including laws on harvesting and producing on the land or on the management of the land; such as: — legislation on land transfer in particular for agricultural land or forests, — legislation on land lease transaction.
— | legislation on land transfer in particular for agricultural land or forests,
— | legislation on land lease transaction.
```

</details>

## q14 (single)

**Question:** Who is liable if one of our cocoa shipments turns out not to comply?

**Reference:** The operator that places the product on the market keeps responsibility (Art. 4(3)); it must refrain from placing it and immediately inform the competent authorities and its customers.

**Answer:**

The corpus does not cover this. An answer was drafted, but it could not be traced to the passages the search returned, so it was withheld. Check the cited sources or ask the competent authority.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 25(1)–(2)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Penalties
Similarity: 0.727
1. Without prejudice to the obligations of Member States under Directive 2008/99/EC of the European Parliament and of the Council (5), Member States shall lay down rules on penalties applicable to infringements of this Regulation by operators, downstream operators and traders and shall take all measures necessary to ensure that they are implemented. Member States shall notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendments affecting them.
2. The penalties provided for in paragraph 1 shall be effective, proportionate and dissuasive. Those penalties shall include: (a) fines proportionate to the environmental damage and the value of the relevant commodities or relevant products concerned, calculating the level of such fines in such way as to ensure that they effectively deprive those responsible of the economic benefits derived from their infringements, and gradually increasing the level of such fines for repeated infringements; in the case of a legal person, the maximum amount of such a fine shall be at least 4 % of the operator’s, downstream operator’s or trader’s total annual Union-wide turnover in the financial year preceding the fining decision, calculated in accordance with the calculation of aggregate turnover for undertakings laid down in Article 5(1) of Council Regulation (EC) No 139/2004 (6), and shall be increased, where necessary, to exceed the potential economic benefit gained; (b) confiscation of the relevant products concerned from the operator, downstream operator and/or trader; (c) confiscation of revenues gained by the operator, downstream operator and/or trader from a transaction with the relevant products concerned; (d) temporary exclusion for a maximum period of 12 months from public procurement processes and from access to public funding, including tendering procedures, grants and concessions; (e) temporary prohibition from placing or making available on the market or exporting relevant commodities and relevant products, in the event of a serious infringement or of repeated infringements; (f) prohibition from exercising the simplified due diligence set out in Article 13 in the event of a serious infringement or of repeated infringements.

---

[2] Cite as: [FAQ 3.11, p. 43]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Who is liable if a product does not comply with Article 3 EUDR?
Similarity: 0.722
Operators retain responsibility for the compliance of the relevant product they place on the EU market or export (Art. 4(3) EUDR).
In cases of non-compliance, operators have to refrain from placing the product on the market or exporting it and have to imme diately inform Competent Authorities and downstream operators and traders to whom they supplied the relevant product (Art. 4(4)(a), (5) EUDR).
Downstream operators and traders have information and, in case of non-SMEs and substantiated concerns, verification duties according to Art. 5(5) and (6) EUDR.

---

[3] Cite as: [EUDR Article 24]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Corrective action in the event of non-compliance
Similarity: 0.716
1. Without prejudice to Article 25, where competent authorities establish that an operator, downstream operator or trader has not complied with this Regulation or that a relevant product placed or made available on the market or exported is non-compliant, they shall without delay require the operator, downstream operator or trader to take appropriate and proportionate corrective action to bring the non-compliance to an end within a specified and reasonable period of time.
2. For the purposes of paragraph 1, the corrective action required to be taken by the operator, downstream operator or trader shall include at least one of the following, as applicable: (a) rectifying any formal non-compliance, in particular with the requirements of Chapter 2; (b) preventing the relevant product from being placed or made available on the market or exported; (c) withdrawing or recalling the relevant product immediately; (d) donating the relevant product to charitable or public interest purposes or, if that is not possible, disposing of it in accordance with Union law on waste management.
3. Irrespective of the corrective action taken under paragraph 2, the operator, downstream operator or trader shall address any shortcomings in the due diligence system with a view to preventing the risk of further non-compliance with this Regulation.
4. If the operator, downstream operator or trader fails to take corrective action as referred to in paragraph 2 within the period of time specified by the competent authority under paragraph 1, or where non-compliance as referred to in paragraph 1 persists, after that period of time competent authorities shall secure application of the required corrective action referred to in paragraph 2 by all means available to them under the law of the Member State concerned.

---

[4] Cite as: [FAQ 3.14 (part 1/2), p. 44]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Who is the operator or trader when one company contracts another company to provide relevant products that are linked to their commercial activities? For example, an onsite cafeteria, small shop or a stand established besides a main business.
Similarity: 0.704
Depending on the detailed contractual agreements, the company responsible for supplying relevant products for use in the cafeteria, small shop, stand etc.
(making available a relevant product on the EU market) is responsible for EUDR compliance.
The obliga tions of the company would depend on their size and position in the supply chain.
For example: 1) Contractor C is an SME company which, under its contractual agreement with Supermarket B, is responsible for purchasing from an EU manufacturer and supplying chocolate (HS 1806) to customers at Supermarket B shops.
In this situation, Contractor C is an SME trader which is only subject to the obligations under Art. 5(1), (3) -(5) and (7) EUDR.
C is not subject to due diligence requirements and does not retain responsibility for the EUDR compliance of the chocolate. 2) Contractor A runs onsite restaurants on behalf of non-SME EU Supermarket B.
Contractor A is a non-SME and, under its contractual agreement with Supermarket B, is responsible for purchasing and supplying chocolate (HS 1806) at an onsite restaurant on the es tablishment of Supermarket B.
Contractor A buys the chocolate from an EU manufacturer, so in this situation, Contractor A is a non-SME trader subject to the obligations under Art. 5 EUDR.
Contractor A is not responsible for the EUDR compliance of the chocolate but must verify that due diligence has been exercised for the chocolate in case of substantiated concerns (Art. 5(7) EUDR). 3) Contractor D is a non-SME company that runs confectionary stands at Supermarket B shops.
The confectionary includes chocolate (HS 1806).
Under their contractual agreements, Supermarket B buys the chocolate bars from a producer in a third country and Contractor D only sells chocolate bars on behalf of Supermarket B without ever owning them.
In this situation, Supermarket B is therefore an operator responsible for exercising due diligence for the chocolate bars and submitting a DDS for each batch of chocolate bars.
Contractor D is not responsible for the EUDR compliance of the chocolate bars.

---

[5] Cite as: [FAQ 3.27 (part 2/2), p. 52]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | When should I update my SD? Are there situations when I need to submit a new SD?
Similarity: 0.699
The information provided in the SD must be truthful at the time of submission and at the time of updating.
If C ompetent Authoritie s detect that estimates or other information were provided for the purpose of misclassifying an operator as an MSPO, circumventing the Regulation’s requirements or negatively impacting enforcement, they may take steps to pursue such breaches of the Regulation, and impose penalties.
```

</details>

## q15 (single)

**Question:** Can one due diligence statement cover several cocoa shipments?

**Reference:** Yes. A DDS can cover multiple batches or shipments, but it must be submitted before any of them is placed on the market, cover their full quantity, and stay within the 25 MB upload limit; the operator is responsible for all of them.

**Answer:**

Yes. According to Commission guidance (which is non-binding), a single due diligence statement can cover multiple physical batches or shipments of multiple different relevant products [FAQ 5.19 (part 1/3), p. 69]. 

However, several limits apply:
* The quantity of all products placed on the market or exported must be fully covered by the statement [FAQ 5.19 (part 1/3), p. 69].
* Once the covered quantity is fully placed on the market or exported, a new statement must be filed for additional quantities [FAQ 5.19 (part 1/3), p. 69].
* A due diligence statement should not cover shipments over a period longer than one year [FAQ 5.19 (part 1/3), p. 69].
* In principle, it should cover commodities that have already been produced/harvested [FAQ 5.19 (part 1/3), p. 69].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 5.19 (part 1/3), p. 69]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How often should due diligence statements be submitted in the Information System, and can they cover multiple shipments/batches? What about situations where relevant products may be placed on the market successively over a period of time?
Similarity: 0.729
A due diligence statement can cover multiple physical batches/shipments of multiple different relevant products.
In these situations, the operator has to confirm that due diligence was carried out for all relevant products intended to be placed on the Unio n market or exported and that no or only a negligible risk was found that the relevant products do not comply with Art. 3, point (a) or (b), EUDR (Annex II) and that the operator assumes responsibility for the compliance of the relevant products with Art. 3 EUDR (Art. 4(3) EUDR).
In addition, there are legal requirements and practical considerations that must be taken into account: 1.
The quantity of all relevant products placed on the Union market or exported must be covered by a due diligence statement (Art. 3(c) EUDR) and that statement must be submitted prior to any batches/shipments of relevant products being placed on the market or exported (Art. 4(2) EUDR). 2.
Once the quantity of products covered by the due diligence statement has been fully placed on the market or exported, a new statement must be filed for additional quantities by the same operator. 3.
In accordance with Art. 12(2) of the EUDR, operators shall review their due diligence system once a year.
Therefore, a due diligence statement should not cover shipments/batches over a period longer than one year from the time of submission of the statemen t.
In addition, a longer time period could lead to difficulties in demonstrating the correspondence between declared products and products actually (intended to be) placed on the market or exported. 4.
With a due diligence statement, the operator confirms that due diligence was carried out for all relevant products jointly or individually that are intended to be placed on the Union market or exported and that there is no or negligible risks of non - compliance of the relevant products.
Therefore, in principle a due diligence statement should cover commodities that have already been produced, i.e., grown, harvested, obtained from or raised on relevant plots of land or, as regards cattle, on establishments.

---

[2] Cite as: [EUDR Annex II]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.722
Due diligence statement
Information to be contained in the due diligence statement in accordance with Article 4(2):
1. Operator’s name, address and, in the event of relevant commodities and relevant products entering or leaving the market, the Economic Operators Registration and Identification (EORI) number in accordance with Article 9 of Regulation (EU) No 952/2013.
2. Harmonised System code, free-text description, including the trade name as well as, where applicable, the full scientific name, and quantity of the relevant product that the operator intends to place on the market or export. For relevant products entering or leaving the market, the quantity is to be expressed in kilograms of net mass and, where applicable, in the supplementary unit set out in Annex I to Regulation (EEC) No 2658/87 against the indicated Harmonised System code or, in all other cases, expressed in net mass specifying a percentage estimate or deviation or, where applicable, volume or number of items. A supplementary unit is applicable where it is defined consistently for all possible subheadings under the Harmonised System code referred to in the due diligence statement.
3. Country of production and the geolocation of all plots of land where the relevant commodities were produced. For relevant products that contain or have been made using cattle, and for such relevant products that have been fed with relevant products, the geolocation shall refer to all the establishments where the cattle were kept. Where the relevant product contains or has been made using commodities produced in different plots of land, the geolocation of all plots of land shall be included in accordance with Article 9(1), point (d).
5. The text: ‘By submitting this due diligence statement the operator confirms that due diligence in accordance with Regulation (EU) 2023/1115 was carried out and that no or only a negligible risk was found that the relevant products do not comply with Article 3, point (a) or (b), of that Regulation.’.
6. Signature in the following format: ‘Signed for and on behalf of: Date: Name and function: Signature:’.

---

[3] Cite as: [Guidance §9 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Composite products
Similarity: 0.72
Composite products may contain multiple relevant products under different commodities. For instance, a chocolate bar [HS 1806 ] may comprise derived products of cocoa (cocoa powder [HS 1805 ] and cocoa butter [HS 1804 ]) and oil palm (palm oil [HS 1511 ]). In such cases, the operator placing the product on the EU market or exporting from it will only be required to conduct due diligence on the relevant products listed under the commodity deemed relevant in Annex I of the EUDR. For instance, for chocolate bars [HS 1806 ], the relevant commodity linked to it is cocoa. This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

---

[4] Cite as: [Guidance §4 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Due diligence
Similarity: 0.72
Relevant legislation: EUDR – Article 2(26) – Definitions; Article 4, 4a and 5 – Obligations of operators, downstream operators and traders; Article 8 – Due diligence; Article 9 – Information requirements; Article 10 – Risk assessment
According to Article 4(1), all operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, shall exercise due diligence in accordance with Article 8 prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Article 3. In order to do so, and in accordance with Article 12(1), operators shall establish and keep up to date a framework of procedures and measures – a ‘due diligence system’.
The due diligence requirements set out in Article 8 require operators to:
— | collect information, documents and, where relevant, data from each supplier about the relevant products which are subject to the EUDR (listed in Annex I) pursuant to Article 8 and 9,
— | verify and analyse that information along with other contextual information and on that basis carry out a risk assessment pursuant to Article 10, and
— | adopt risk mitigation measures pursuant to Article 11, unless the risk assessment carried out in accordance with Article 10 concludes that there is no or only negligible risk that the relevant products are non-compliant.
Operators are responsible for a thorough examination and analysis of their own business activities, which requires the collection of information, data and documents needed to fulfil the information requirements of Article 9, analysing it as part of the risk assessment (Article 10), and adopt risk mitigation measures (Article 11) as necessary, unless the risk of non-compliance is assessed as being negligible.
All operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, are obliged to fulfil the information requirements set out in Article 9.

---

[5] Cite as: [FAQ 1.3, p. 13]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How does it work for bulk-traded or composite products? What about composite products containing different commodities?
Similarity: 0.716
For products traded in bulk, such as soy or palm oil for instance, this means that the operator needs to ensure that all plots of land involved in a shipment are identified and that the commodities are not mixed at any step of the process with commodities of unknown origin or from areas deforested or degraded after the cut-off date of 31 December 2020.
For relevant composite products, such as e.g. imported wooden furniture with different wood components, the operator needs to geolocate all the plots of land where the relevant commodity (wood, for example) used for the manufacturing process has been produced.
The relevant commodities’ components may be neither of unknown origin nor from areas deforested or degraded after the cut-off date.
In the case of composite products containing multiple different relevant commodities or products (for example, a chocolate bar containing cocoa powder, cocoa butter and palm oil), the operator placing such a product on the EU market or exporting from it will need to conduct due diligence only on the main commodity and (derived) products deemed relevant under the EUDR, this being the commodity contained in the left column of Annex I.
For example, for chocolate bars (Code 1806), the relevant commodity linked to it is cocoa.
This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.
```

</details>

## q16 (single)

**Question:** By when do we have to submit the due diligence statement for imported cocoa?

**Reference:** Before lodging the customs declaration: the DDS reference number must be obtained beforehand and included in the customs declaration.

**Answer:**

The due diligence statement (DDS) for imported cocoa must be submitted, and its reference number obtained, **prior to the lodging of the customs declaration** [FAQ 5.20, p. 70]. 

Under Article 4(2) of the EUDR, operators shall not place relevant products on the market or export them without prior submission of a due diligence statement through the information system [EUDR Article 4(2), FAQ 5.19, p. 69].

*(Note: This answer is based on the Commission FAQ, which reflects the Commission's views and is not legally binding [FAQ 5.20, p. 70].)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 5.20 (part 1/2), p. 70]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the latest date for submitting a DDS or a SD?
Similarity: 0.738
According to Art. 4(1) EUDR, operators shall exercise due diligence in accordance with Art. 8 EUDR prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Art. 3 EUDR.
For relevant products entering the Union market (import) or leaving the Union market (export) the reference number of the DDS shall be made available to customs authorities.
For this purpose, the person lodging the customs declaration (known as “customs declarant”) shall include the DDS reference number on the customs declaration lodged f or that relevant product, in accordance with Art. 26 EUDR.
Therefore, the DDS shall be submitted, and the reference number of the DDS shall be obtained prior to the lodging of the customs declaration8.
The same applies to the submission of the SD prior to the first placing on the market or export by a MSPO.
Where a DDS covers multiple shipments/batches the same DDS reference number can be referred to in several customs declarations as long as the legal requirements of the EUDR are respected.
It is equally possible to include multiple DDS reference numbers in one customs declaration.
For commodities produced within the EU and other cases of products being placed on the EU market domestically, the exact date of placing on the market should be understood when 1. the product is physically available on the Union market (i.e., the commodity has been produced and in the case of a derived product, the product has been manufactured), 2. two or more legal or natural persons enter into an agreement in which the operator promises the supply of the relevant product and 3. in cases where there is a physical supply or delivery of the product, the delivery process has started (for example by initiating the loading of the cargo truck or ship of relevant products).
The contractual agreement could provide for the supply in return for payment or free of charge.

---

[2] Cite as: [FAQ 5.21, p. 71]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the earliest date for submitting a DDS or SD?
Similarity: 0.736
According to Art. 4(1) EUDR, operators shall exercise due diligence in accordance with Art. 8 EUDR prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Art. 3 EUDR.
The earliest a DDS can be submitted is after due diligence has been exercised and when all information that is needed for submission is available (including the quantity planned to be placed or made available on the market or exported).
It should also be n oted that as set out in FAQ 5.19., a due diligence statement should not cover shipments/batches over a period longer than one year from the time of submission of the statement. 8 In the mid- to long-term, it will be possible for operators to submit at once their customs declarations and the DDS pursuant to Art. 28(2) of the EUDR.
This situation is not yet applicable and thus not reflected yet in this document.
Separate guidance and FAQs will be made available in due time in this respect.
As a SD can be submitted prior to exercising due diligence, there is flexibility as to the earliest date when the submission can take place (for the latest date see FAQ 5.20 above).

---

[3] Cite as: [FAQ 5.19 (part 1/3), p. 69]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How often should due diligence statements be submitted in the Information System, and can they cover multiple shipments/batches? What about situations where relevant products may be placed on the market successively over a period of time?
Similarity: 0.727
A due diligence statement can cover multiple physical batches/shipments of multiple different relevant products.
In these situations, the operator has to confirm that due diligence was carried out for all relevant products intended to be placed on the Unio n market or exported and that no or only a negligible risk was found that the relevant products do not comply with Art. 3, point (a) or (b), EUDR (Annex II) and that the operator assumes responsibility for the compliance of the relevant products with Art. 3 EUDR (Art. 4(3) EUDR).
In addition, there are legal requirements and practical considerations that must be taken into account: 1.
The quantity of all relevant products placed on the Union market or exported must be covered by a due diligence statement (Art. 3(c) EUDR) and that statement must be submitted prior to any batches/shipments of relevant products being placed on the market or exported (Art. 4(2) EUDR). 2.
Once the quantity of products covered by the due diligence statement has been fully placed on the market or exported, a new statement must be filed for additional quantities by the same operator. 3.
In accordance with Art. 12(2) of the EUDR, operators shall review their due diligence system once a year.
Therefore, a due diligence statement should not cover shipments/batches over a period longer than one year from the time of submission of the statemen t.
In addition, a longer time period could lead to difficulties in demonstrating the correspondence between declared products and products actually (intended to be) placed on the market or exported. 4.
With a due diligence statement, the operator confirms that due diligence was carried out for all relevant products jointly or individually that are intended to be placed on the Union market or exported and that there is no or negligible risks of non - compliance of the relevant products.
Therefore, in principle a due diligence statement should cover commodities that have already been produced, i.e., grown, harvested, obtained from or raised on relevant plots of land or, as regards cattle, on establishments.

---

[4] Cite as: [FAQ 5.4 (part 2/2), p. 64]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are my obligations if I am re-importing a product that was previously exported from the EU?
Similarity: 0.725
The above applies equally where the product that is imported is made of relevant products that were previously exported from the EU market and have been subject to due diligence (example: cocoa beans are exported from the EU to a third country to manufacture chocolate, and the chocolate is subsequently released for free circulation in the EU).
For parts of relevant products that have not been subject to due diligence, operators must exercise due diligence and submit a DDS.

---

[5] Cite as: [EUDR Article 4(1)–(4)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Obligations of operators
Similarity: 0.723
1. Operators shall exercise due diligence in accordance with Article 8 prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Article 3.
2. Operators shall not place relevant products on the market or export them without prior submission of a due diligence statement. Operators who, on the basis of the due diligence exercised in accordance with Article 8, conclude that the relevant products comply with Article 3 shall, before placing the relevant products on the market or exporting them, make available a due diligence statement to the competent authorities through the information system referred to in Article 33. Such electronically available and transmittable due diligence statement shall contain the information set out in Annex II for the relevant products and a declaration by the operator that the operator exercised due diligence and that no or only a negligible risk was found.
3. By making the due diligence statement available to competent authorities or, in the case of micro or small primary operators, by submitting the simplified declaration referred to in Article 4a, the operator shall assume responsibility for the compliance of the relevant product with Article 3. Operators shall keep a record of the due diligence statements for five years from the date the statement is submitted through the information system referred to in Article 33.
4. Operators shall not place relevant products on the market or export them where one or more of the following cases apply: (a) the relevant products are non-compliant; (b) the exercise of due diligence has revealed a non-negligible risk that the relevant products are non-compliant; (c) the operator was unable to fulfil the obligations referred to in paragraphs 1 and 2.
```

</details>

## q17 (single)

**Question:** Can we change a due diligence statement after we have submitted it?

**Reference:** Yes, it can be withdrawn or amended within 72 hours of receiving the reference number, unless the number was already used in a customs declaration, the product was already placed on the market or exported, or a check has been announced.

**Answer:**

Yes, a due diligence statement can be withdrawn or amended within 72 hours after the reference number has been made available by the Information System [FAQ 7.6, p. 77]. 

*Note: This answer rests solely on the Commission FAQ, which reflects the Commission's views and is not legally binding.*

However, amendment or withdrawal is **not** possible if:
* The reference number has already been used in a customs declaration [FAQ 7.6, p. 77].
* The product has already been placed or made available on the EU market, or exported [FAQ 7.6, p. 77].
* The operator has been notified of an impending check on the statement, for the duration of that check [FAQ 7.6, p. 77].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 7.6, p. 77]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Can a due diligent statement be amended?
Similarity: 0.743
In accordance with Art. 5 of Commission Implementing Regulation 2024/3084 14, the withdrawal or amendment of a submitted due diligence statement is possible within 72 hours after the due diligence reference number has been made available to the user by the Information System.
Withdrawal or amendment will not be possible if the DDS reference 14 An updated reference will be added once available. number has already been used in a customs declaration, if the corresponding product has already been placed or made available on the EU market or exported, or, if the operator was notified about the intention to carry out a check on the DDS, for the period of the check.

---

[2] Cite as: [FAQ 5.21, p. 71]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the earliest date for submitting a DDS or SD?
Similarity: 0.705
According to Art. 4(1) EUDR, operators shall exercise due diligence in accordance with Art. 8 EUDR prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Art. 3 EUDR.
The earliest a DDS can be submitted is after due diligence has been exercised and when all information that is needed for submission is available (including the quantity planned to be placed or made available on the market or exported).
It should also be n oted that as set out in FAQ 5.19., a due diligence statement should not cover shipments/batches over a period longer than one year from the time of submission of the statement. 8 In the mid- to long-term, it will be possible for operators to submit at once their customs declarations and the DDS pursuant to Art. 28(2) of the EUDR.
This situation is not yet applicable and thus not reflected yet in this document.
Separate guidance and FAQs will be made available in due time in this respect.
As a SD can be submitted prior to exercising due diligence, there is flexibility as to the earliest date when the submission can take place (for the latest date see FAQ 5.20 above).

---

[3] Cite as: [FAQ 5.19 (part 1/3), p. 69]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How often should due diligence statements be submitted in the Information System, and can they cover multiple shipments/batches? What about situations where relevant products may be placed on the market successively over a period of time?
Similarity: 0.703
A due diligence statement can cover multiple physical batches/shipments of multiple different relevant products.
In these situations, the operator has to confirm that due diligence was carried out for all relevant products intended to be placed on the Unio n market or exported and that no or only a negligible risk was found that the relevant products do not comply with Art. 3, point (a) or (b), EUDR (Annex II) and that the operator assumes responsibility for the compliance of the relevant products with Art. 3 EUDR (Art. 4(3) EUDR).
In addition, there are legal requirements and practical considerations that must be taken into account: 1.
The quantity of all relevant products placed on the Union market or exported must be covered by a due diligence statement (Art. 3(c) EUDR) and that statement must be submitted prior to any batches/shipments of relevant products being placed on the market or exported (Art. 4(2) EUDR). 2.
Once the quantity of products covered by the due diligence statement has been fully placed on the market or exported, a new statement must be filed for additional quantities by the same operator. 3.
In accordance with Art. 12(2) of the EUDR, operators shall review their due diligence system once a year.
Therefore, a due diligence statement should not cover shipments/batches over a period longer than one year from the time of submission of the statemen t.
In addition, a longer time period could lead to difficulties in demonstrating the correspondence between declared products and products actually (intended to be) placed on the market or exported. 4.
With a due diligence statement, the operator confirms that due diligence was carried out for all relevant products jointly or individually that are intended to be placed on the Union market or exported and that there is no or negligible risks of non - compliance of the relevant products.
Therefore, in principle a due diligence statement should cover commodities that have already been produced, i.e., grown, harvested, obtained from or raised on relevant plots of land or, as regards cattle, on establishments.

---

[4] Cite as: [EUDR Annex II]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.697
Due diligence statement
Information to be contained in the due diligence statement in accordance with Article 4(2):
1. Operator’s name, address and, in the event of relevant commodities and relevant products entering or leaving the market, the Economic Operators Registration and Identification (EORI) number in accordance with Article 9 of Regulation (EU) No 952/2013.
2. Harmonised System code, free-text description, including the trade name as well as, where applicable, the full scientific name, and quantity of the relevant product that the operator intends to place on the market or export. For relevant products entering or leaving the market, the quantity is to be expressed in kilograms of net mass and, where applicable, in the supplementary unit set out in Annex I to Regulation (EEC) No 2658/87 against the indicated Harmonised System code or, in all other cases, expressed in net mass specifying a percentage estimate or deviation or, where applicable, volume or number of items. A supplementary unit is applicable where it is defined consistently for all possible subheadings under the Harmonised System code referred to in the due diligence statement.
3. Country of production and the geolocation of all plots of land where the relevant commodities were produced. For relevant products that contain or have been made using cattle, and for such relevant products that have been fed with relevant products, the geolocation shall refer to all the establishments where the cattle were kept. Where the relevant product contains or has been made using commodities produced in different plots of land, the geolocation of all plots of land shall be included in accordance with Article 9(1), point (d).
5. The text: ‘By submitting this due diligence statement the operator confirms that due diligence in accordance with Regulation (EU) 2023/1115 was carried out and that no or only a negligible risk was found that the relevant products do not comply with Article 3, point (a) or (b), of that Regulation.’.
6. Signature in the following format: ‘Signed for and on behalf of: Date: Name and function: Signature:’.

---

[5] Cite as: [FAQ 5.16, p. 68]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Will there be a set of pre-determined format or list of questions to perform due diligence?
Similarity: 0.69
No.
Operators must comply with their due diligence obligations in accordance with Art. 8, 9, 10 and 11 EUDR.
Achieving no or negligible risk is a pre-requisite for placing/ exporting relevant products on/from the EU market.
Please note that due diligence is not a “tick-the-box exercise”.
Hence, it may depend on the specific context and supply chain, provided that the different steps of due diligence as described in the Regulation (i.e. information requirement, risk assessment and risk mitigation, in line with Art. 9, 10 and 11 EUDR, unless Art. 13 EUDR applies) are covered.
```

</details>

## q18 (single)

**Question:** Do we have to put the DDS reference number on the bill of lading?

**Reference:** No. It must be included in the customs declaration; no EUDR provision requires it on other shipping documents.

**Answer:**

No, there is no specific provision in the EUDR requiring you to put the due diligence statement (DDS) reference number on the bill of lading or other shipping documents [FAQ 7.21, p. 82]. 

Instead, the DDS reference number must be made available to customs authorities by including it on the **customs declaration** [FAQ 7.21, p. 82]. 

*(Note: This answer rests on the Commission FAQ, which reflects the Commission's views and is not legally binding.)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 7.21, p. 82]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Is there a need to include the EUDR reference number or declaration identifier in the shipping documents such as delivery note or invoice and send the documents along with the shipments? Is it a mandate for customs clearance for imports/exports?
Similarity: 0.755
In accordance with Art. 26(4) EUDR, the DDS reference number or SD declaration identifier associated with the product which enters or leaves the Union market must be made available to the customs authorities, except for the case of the export by a downstream operator.
To comply with this requirement, importers or exporters of the product must include the associated DDS reference numbers or declaration identifiers on the customs declaration.
Regarding other shipment documents, including for intra-EU transport, there is no specific provision in the EUDR that requires the inclusion of DDS reference numbers or declaration identifiers.

---

[2] Cite as: [EUDR Annex II]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.741
Due diligence statement
Information to be contained in the due diligence statement in accordance with Article 4(2):
1. Operator’s name, address and, in the event of relevant commodities and relevant products entering or leaving the market, the Economic Operators Registration and Identification (EORI) number in accordance with Article 9 of Regulation (EU) No 952/2013.
2. Harmonised System code, free-text description, including the trade name as well as, where applicable, the full scientific name, and quantity of the relevant product that the operator intends to place on the market or export. For relevant products entering or leaving the market, the quantity is to be expressed in kilograms of net mass and, where applicable, in the supplementary unit set out in Annex I to Regulation (EEC) No 2658/87 against the indicated Harmonised System code or, in all other cases, expressed in net mass specifying a percentage estimate or deviation or, where applicable, volume or number of items. A supplementary unit is applicable where it is defined consistently for all possible subheadings under the Harmonised System code referred to in the due diligence statement.
3. Country of production and the geolocation of all plots of land where the relevant commodities were produced. For relevant products that contain or have been made using cattle, and for such relevant products that have been fed with relevant products, the geolocation shall refer to all the establishments where the cattle were kept. Where the relevant product contains or has been made using commodities produced in different plots of land, the geolocation of all plots of land shall be included in accordance with Article 9(1), point (d).
5. The text: ‘By submitting this due diligence statement the operator confirms that due diligence in accordance with Regulation (EU) 2023/1115 was carried out and that no or only a negligible risk was found that the relevant products do not comply with Article 3, point (a) or (b), of that Regulation.’.
6. Signature in the following format: ‘Signed for and on behalf of: Date: Name and function: Signature:’.

---

[3] Cite as: [FAQ 5.20 (part 1/2), p. 70]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the latest date for submitting a DDS or a SD?
Similarity: 0.738
According to Art. 4(1) EUDR, operators shall exercise due diligence in accordance with Art. 8 EUDR prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Art. 3 EUDR.
For relevant products entering the Union market (import) or leaving the Union market (export) the reference number of the DDS shall be made available to customs authorities.
For this purpose, the person lodging the customs declaration (known as “customs declarant”) shall include the DDS reference number on the customs declaration lodged f or that relevant product, in accordance with Art. 26 EUDR.
Therefore, the DDS shall be submitted, and the reference number of the DDS shall be obtained prior to the lodging of the customs declaration8.
The same applies to the submission of the SD prior to the first placing on the market or export by a MSPO.
Where a DDS covers multiple shipments/batches the same DDS reference number can be referred to in several customs declarations as long as the legal requirements of the EUDR are respected.
It is equally possible to include multiple DDS reference numbers in one customs declaration.
For commodities produced within the EU and other cases of products being placed on the EU market domestically, the exact date of placing on the market should be understood when 1. the product is physically available on the Union market (i.e., the commodity has been produced and in the case of a derived product, the product has been manufactured), 2. two or more legal or natural persons enter into an agreement in which the operator promises the supply of the relevant product and 3. in cases where there is a physical supply or delivery of the product, the delivery process has started (for example by initiating the loading of the cargo truck or ship of relevant products).
The contractual agreement could provide for the supply in return for payment or free of charge.

---

[4] Cite as: [FAQ 5.21, p. 71]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the earliest date for submitting a DDS or SD?
Similarity: 0.733
According to Art. 4(1) EUDR, operators shall exercise due diligence in accordance with Art. 8 EUDR prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Art. 3 EUDR.
The earliest a DDS can be submitted is after due diligence has been exercised and when all information that is needed for submission is available (including the quantity planned to be placed or made available on the market or exported).
It should also be n oted that as set out in FAQ 5.19., a due diligence statement should not cover shipments/batches over a period longer than one year from the time of submission of the statement. 8 In the mid- to long-term, it will be possible for operators to submit at once their customs declarations and the DDS pursuant to Art. 28(2) of the EUDR.
This situation is not yet applicable and thus not reflected yet in this document.
Separate guidance and FAQs will be made available in due time in this respect.
As a SD can be submitted prior to exercising due diligence, there is flexibility as to the earliest date when the submission can take place (for the latest date see FAQ 5.20 above).

---

[5] Cite as: [FAQ 3.6.1, p. 37]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Are operators obliged to communicate the “verification number” of their DDS or SD to clients?
Similarity: 0.726
Operators must provide the due diligence statements reference numbers (or declaration identifiers in the case of a SD) associated with their relevant products to their direct clients only if the clients are (first) downstream operators or traders, Art. 4(7) EUDR.
There is no obligation to pass on reference numbers or declaration identifiers to other clients, such as to final consumers or to companies that manufacture products outside of the scope of EUDR.
Under the EUDR as amended in December 2025, there is no legal obligation on operators to provide additional information which would enable downstream operators or traders to exercise due diligence on the relevant products they buy, as there are no due dili gence obligations downstream (see FAQ 3.4 for more information).
There is also no legal obligation under EUDR to share verification numbers downstream, which serve as an additional security layer for the data contained in declarations.
Where non-SME downstream operators and non-SME traders verify the exercise of due diligence pursuant to Art. 5(6) EUDR in case of substantiated concerns, they may request their direct supplier to share verification numbers (see FAQ 3.6.1 and FAQ 7.25 for more information).
```

</details>

## q19 (single)

**Question:** In what file format do we upload the farm geolocation data?

**Reference:** GeoJSON only.

**Answer:**

*Note: This answer rests solely on the Commission FAQ, which reflects the Commission's views and is not legally binding.*

You can provide geolocation data in the Information System either by manual entry or by uploading a file in **GeoJSON** format [FAQ 7.8, p. 78]. 

The system supports the WGS-84 coordinate format with the EPSG-4326 projection [FAQ 7.8, p. 78]. Coordinates must use at least 6 decimal digits for both latitude and longitude [FAQ 7.17, p. 81]. GeoJSON is currently the only file format allowed for uploads [FAQ 7.26, p. 83].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 7.17, p. 81]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if the geolocation file consists of different number of digits than required by the Regulation?
Similarity: 0.76
According to Art. 2(28) the geolocation coordinates shall be provided by using at least 6 decimal digits both for latitude and longitude coordinates.
When the user uploads geolocation files into the Information System, the system automatically validates the number of digits.
To ensure a smooth data upload the system provides flexibility by automatically adjusting to six digits, and if the number of the provided digits is less than 6 then fills the remaining digits with zeroes.

---

[2] Cite as: [FAQ 7.8, p. 78]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Which data format is needed for the geolocation to be uploaded in the Information System?
Similarity: 0.759
Operators can provide geolocations in the Information System either by manual entry or by uploading them in a file.
The format of the supported files in the Information System is GeoJson.
The Information System supports currently WGS-84 coordinate format, with EPSG- 4326 projection.

---

[3] Cite as: [FAQ 7.26, p. 83]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Why is only GeoJSON format allowed for uploading geolocation data in a file?
Similarity: 0.735
GeoJSON is a general standard and the only non-proprietary system which allows submission of the extra properties needed, and where a very specific coordinate system is enforced.
Using multiple formats in the Information System would increase the risk of e rroneous or inaccurate information.
The exclusive use of GeoJSON was announced in April 2024, allowing all stakeholders to prepare their respective systems accordingly.

---

[4] Cite as: [EUDR Annex II]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.724
Due diligence statement
Information to be contained in the due diligence statement in accordance with Article 4(2):
1. Operator’s name, address and, in the event of relevant commodities and relevant products entering or leaving the market, the Economic Operators Registration and Identification (EORI) number in accordance with Article 9 of Regulation (EU) No 952/2013.
2. Harmonised System code, free-text description, including the trade name as well as, where applicable, the full scientific name, and quantity of the relevant product that the operator intends to place on the market or export. For relevant products entering or leaving the market, the quantity is to be expressed in kilograms of net mass and, where applicable, in the supplementary unit set out in Annex I to Regulation (EEC) No 2658/87 against the indicated Harmonised System code or, in all other cases, expressed in net mass specifying a percentage estimate or deviation or, where applicable, volume or number of items. A supplementary unit is applicable where it is defined consistently for all possible subheadings under the Harmonised System code referred to in the due diligence statement.
3. Country of production and the geolocation of all plots of land where the relevant commodities were produced. For relevant products that contain or have been made using cattle, and for such relevant products that have been fed with relevant products, the geolocation shall refer to all the establishments where the cattle were kept. Where the relevant product contains or has been made using commodities produced in different plots of land, the geolocation of all plots of land shall be included in accordance with Article 9(1), point (d).
5. The text: ‘By submitting this due diligence statement the operator confirms that due diligence in accordance with Regulation (EU) 2023/1115 was carried out and that no or only a negligible risk was found that the relevant products do not comply with Article 3, point (a) or (b), of that Regulation.’.
6. Signature in the following format: ‘Signed for and on behalf of: Date: Name and function: Signature:’.

---

[5] Cite as: [FAQ 1.19, p. 19]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How will geolocation allow claims to be checked in practice?
Similarity: 0.721
How will geolocation allow for checking the validity of a no-deforestation claim in practice? Is it aligning satellite navigation positioning and deforestation maps? Will there be baseline maps that forest areas or areas that have undergone deforestation and forest degradation? How will it work if geolocation of farms, plantations or concessions are not available? It is the responsibility of the operator to collect the geolocation coordinates of the plots of land where the commodities were produced.
If the operator cannot collect the geolocation of all plots of land contributing to a relevant product, then they should not place that product on the EU market or export it, in accordance with Art. 3 EUDR.
Operators (and non-SME downstream operators and traders) and enforcing authorities may cross-check the geolocation coordinates against satellite images or forest cover maps to assess if the products meet the deforestation-free requirement of the Regulation.
```

</details>

## q20 (single)

**Question:** If the authorities suspect one of our cocoa shipments, how long can they suspend it?

**Reference:** The suspension should end within three working days (72 hours for perishable products), but it can be extended by further three-day periods while the authority checks compliance.

**Answer:**

Competent authorities can suspend a shipment presenting a high risk of non-compliance for an initial period of **three working days** (or **72 hours** in the case of perishable products) [FAQ 9.11, p. 92]. 

However, the authorities can extend this suspension by additional periods of three days based on checks carried out during that time to establish whether the product is compliant [FAQ 9.11, p. 92]. 

*Note: This answer rests on the Commission's FAQ, which reflects the Commission's views and is not legally binding [FAQ 9.11, p. 92].*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [Guidance §9 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Composite products
Similarity: 0.717
Composite products may contain multiple relevant products under different commodities. For instance, a chocolate bar [HS 1806 ] may comprise derived products of cocoa (cocoa powder [HS 1805 ] and cocoa butter [HS 1804 ]) and oil palm (palm oil [HS 1511 ]). In such cases, the operator placing the product on the EU market or exporting from it will only be required to conduct due diligence on the relevant products listed under the commodity deemed relevant in Annex I of the EUDR. For instance, for chocolate bars [HS 1806 ], the relevant commodity linked to it is cocoa. This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

---

[2] Cite as: [FAQ 9.11, p. 92]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What constitutes high-risk, and how long can a suspension take place?
Similarity: 0.716
Art. 17 EUDR allows Competent Authorities to take immediate actions – including suspension - in situations that present high risk of non-compliance.
What constitutes high- risk, and how long can the suspension take place? Competent Authorities may identify situations where relevant products present a high risk of being non-compliant with the requirements of the Regulation on the basis of different circumstances, including on the spot checks, the outcome of their risk analys is in their risk - based plans, or risks identified through the information system, or on the basis of information coming from another competent Authority, substantiated concerns etc.
In such cases, the Competent Authorities can introduce interim measures as defined in Art. 23 EUDR, including the suspension of placing or making available the product on the EU market.
This suspension should end within three working days, or 72 hours in case of perishable products.
However, the Competent Authority can come to the conclusion, based on checks carried out in this period of time, that the suspension should be extended by additional periods of three days to establish if the product is compliant with the Regulation.

---

[3] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.707
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[4] Cite as: [FAQ 1.3, p. 13]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How does it work for bulk-traded or composite products? What about composite products containing different commodities?
Similarity: 0.703
For products traded in bulk, such as soy or palm oil for instance, this means that the operator needs to ensure that all plots of land involved in a shipment are identified and that the commodities are not mixed at any step of the process with commodities of unknown origin or from areas deforested or degraded after the cut-off date of 31 December 2020.
For relevant composite products, such as e.g. imported wooden furniture with different wood components, the operator needs to geolocate all the plots of land where the relevant commodity (wood, for example) used for the manufacturing process has been produced.
The relevant commodities’ components may be neither of unknown origin nor from areas deforested or degraded after the cut-off date.
In the case of composite products containing multiple different relevant commodities or products (for example, a chocolate bar containing cocoa powder, cocoa butter and palm oil), the operator placing such a product on the EU market or exporting from it will need to conduct due diligence only on the main commodity and (derived) products deemed relevant under the EUDR, this being the commodity contained in the left column of Annex I.
For example, for chocolate bars (Code 1806), the relevant commodity linked to it is cocoa.
This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

---

[5] Cite as: [EUDR Article 1]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Subject matter and scope
Similarity: 0.698
1. This Regulation lays down rules regarding the placing and making available on the Union market as well as the export from the Union of relevant products, as listed in Annex I, that contain, have been fed with or have been made using relevant commodities, namely cattle, cocoa, coffee, oil palm, rubber, soya and wood, with a view to: (a) minimising the Union’s contribution to deforestation and forest degradation worldwide, and thereby contributing to a reduction in global deforestation; (b) reducing the Union’s contribution to greenhouse gas emissions and global biodiversity loss.
2. Except as provided for in Article 37(3), this Regulation does not apply to relevant products listed in Annex I produced before the date indicated in Article 38(1).
```

</details>

## q21 (single)

**Question:** What does due diligence under the EUDR consist of?

**Reference:** Collecting the information, data and documents required by Article 9, risk assessment (Article 10) and risk mitigation (Article 11), done before placing the products on the market or exporting them.

**Answer:**

Prior to placing relevant products on the market or exporting them, operators must exercise due diligence to prove that the products comply with legality and deforestation-free requirements [EUDR Article 8(1), Guidance §4]. 

Under Article 8, due diligence consists of three core steps:
1. **Information collection:** Gathering the data, documents, and information needed to fulfill Article 9 requirements (such as supplier details, product description, quantity, country of production, and geolocation of all plots of land where the relevant commodities were produced) [EUDR Article 8(2)(a)].
2. **Risk assessment:** Verifying and analyzing that information against contextual criteria to assess whether there is a risk that the products are non-compliant [EUDR Article 8(2)(b), Guidance §4].
3. **Risk mitigation:** Adopting adequate measures and procedures to reach no or negligible risk, unless the risk assessment concludes there is already no or negligible risk [EUDR Article 8(2)(c), Guidance §4].

Operators must establish and maintain a "due diligence system" of procedures and measures, review it annually, and submit a due diligence statement confirming negligible risk prior to placing products on the market [EUDR Article 4(2), 12(1)–(2)]. 

*(Note: Portions of this answer are supported by the Commission Guidance and FAQ, which reflect the Commission's non-binding views).*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 8]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Due diligence
Similarity: 0.849
1. Prior to placing relevant products on the market or exporting them, operators shall exercise due diligence with regard to all relevant products.
2. The due diligence shall include: (a) the collection of information, data and documents needed to fulfil the requirements set out in Article 9; (b) risk assessment measures as referred to in Article 10; (c) risk mitigation measures as referred to in Article 11.

---

[2] Cite as: [Guidance §4 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Due diligence
Similarity: 0.817
Relevant legislation: EUDR – Article 2(26) – Definitions; Article 4, 4a and 5 – Obligations of operators, downstream operators and traders; Article 8 – Due diligence; Article 9 – Information requirements; Article 10 – Risk assessment
According to Article 4(1), all operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, shall exercise due diligence in accordance with Article 8 prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Article 3. In order to do so, and in accordance with Article 12(1), operators shall establish and keep up to date a framework of procedures and measures – a ‘due diligence system’.
The due diligence requirements set out in Article 8 require operators to:
— | collect information, documents and, where relevant, data from each supplier about the relevant products which are subject to the EUDR (listed in Annex I) pursuant to Article 8 and 9,
— | verify and analyse that information along with other contextual information and on that basis carry out a risk assessment pursuant to Article 10, and
— | adopt risk mitigation measures pursuant to Article 11, unless the risk assessment carried out in accordance with Article 10 concludes that there is no or only negligible risk that the relevant products are non-compliant.
Operators are responsible for a thorough examination and analysis of their own business activities, which requires the collection of information, data and documents needed to fulfil the information requirements of Article 9, analysing it as part of the risk assessment (Article 10), and adopt risk mitigation measures (Article 11) as necessary, unless the risk of non-compliance is assessed as being negligible.
All operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, are obliged to fulfil the information requirements set out in Article 9.

---

[3] Cite as: [FAQ 5.16, p. 68]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Will there be a set of pre-determined format or list of questions to perform due diligence?
Similarity: 0.79
No.
Operators must comply with their due diligence obligations in accordance with Art. 8, 9, 10 and 11 EUDR.
Achieving no or negligible risk is a pre-requisite for placing/ exporting relevant products on/from the EU market.
Please note that due diligence is not a “tick-the-box exercise”.
Hence, it may depend on the specific context and supply chain, provided that the different steps of due diligence as described in the Regulation (i.e. information requirement, risk assessment and risk mitigation, in line with Art. 9, 10 and 11 EUDR, unless Art. 13 EUDR applies) are covered.

---

[4] Cite as: [EUDR Article 12(1)–(4)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Establishment and maintenance of due diligence systems, reporting and record keeping
Similarity: 0.77
1. In order to exercise due diligence in accordance with Article 8, operators shall establish and keep up to date a framework of procedures and measures to ensure that the relevant products they place on the market or export comply with Article 3 (‘due diligence system’).
2. Operators shall review the due diligence system at least once a year. Where operators become aware of new developments which could influence the due diligence system, they shall update the due diligence system to take account of those developments. Operators shall keep a record of such updates in their due diligence systems for five years.
3. Operators who do not fall within the categories of SMEs, including microenterprises, or natural persons shall, on an annual basis, publicly report as widely as possible, including via the internet, on their due diligence system, including on the steps taken by them to fulfil their obligations as set out in Article 8. Operators who fall also within the scope of other Union legal acts that lay down requirements regarding value chain due diligence may fulfil their reporting obligations under this paragraph by including the required information when reporting in the context of those other Union legal acts.
4. Without prejudice to Union data protection legislation, the reporting as referred to in paragraph 3 shall include the following information concerning relevant commodities and relevant products: (a) a summary of the information referred to in Article 9(1), points (a), (b) and (c); (b) the conclusions of the risk assessment carried out pursuant to Article 10 and measures undertaken pursuant to Article 11 and a description of the information and evidence obtained and used to assess the risk; (c) where applicable, a description of the process of consultation of indigenous peoples, local communities and other customary tenure rights holders or of the civil society organisations that are present in the area of production of the relevant commodities and relevant products.

---

[5] Cite as: [EUDR Article 4(1)–(4)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Obligations of operators
Similarity: 0.765
1. Operators shall exercise due diligence in accordance with Article 8 prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Article 3.
2. Operators shall not place relevant products on the market or export them without prior submission of a due diligence statement. Operators who, on the basis of the due diligence exercised in accordance with Article 8, conclude that the relevant products comply with Article 3 shall, before placing the relevant products on the market or exporting them, make available a due diligence statement to the competent authorities through the information system referred to in Article 33. Such electronically available and transmittable due diligence statement shall contain the information set out in Annex II for the relevant products and a declaration by the operator that the operator exercised due diligence and that no or only a negligible risk was found.
3. By making the due diligence statement available to competent authorities or, in the case of micro or small primary operators, by submitting the simplified declaration referred to in Article 4a, the operator shall assume responsibility for the compliance of the relevant product with Article 3. Operators shall keep a record of the due diligence statements for five years from the date the statement is submitted through the information system referred to in Article 33.
4. Operators shall not place relevant products on the market or export them where one or more of the following cases apply: (a) the relevant products are non-compliant; (b) the exercise of due diligence has revealed a non-negligible risk that the relevant products are non-compliant; (c) the operator was unable to fulfil the obligations referred to in paragraphs 1 and 2.
```

</details>

## q22 (single)

**Question:** What share of operators sourcing from standard-risk countries must the authorities check each year?

**Reference:** At least 3% of the operators (and non-SME downstream operators and traders) dealing in products from standard-risk countries, per relevant commodity.

**Answer:**

Each Member State must ensure that its competent authorities' annual checks cover at least **3%** of the operators, non-SME downstream operators, and non-SME traders sourcing from countries or parts thereof classified as standard risk [EUDR Article 16(8)].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 29(1)–(3)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Assessment of countries
Similarity: 0.775
1. This Regulation establishes a three-tier system for the assessment of countries or parts thereof. For that purpose, Member States and third countries, or parts thereof, shall be classified into one of the following risk categories: (a) ‘high risk’ refers to countries or parts thereof, for which the assessment referred to in paragraph 3 results in the identification of a high risk of producing in such countries or in parts thereof, relevant commodities for which the relevant products do not comply with Article 3, point (a); (b) ‘low risk’ refers to countries or parts thereof, for which the assessment referred to in paragraph 3 concludes that there is sufficient assurance that instances of producing in such countries or in parts thereof, relevant commodities for which the relevant products do not comply with Article 3, point (a), are exceptional; (c) ‘standard risk’ refers to countries or parts thereof which do not fall in either the category ‘high risk’ or the category ‘low risk’.
2. On 29 June 2023, all countries shall be assigned a standard level of risk. The Commission shall classify countries or parts thereof, that present a low or high risk in accordance with paragraph 1 of this Article. The list of the countries or parts thereof, that present a low or high risk shall be published by means of implementing acts to be adopted in accordance with the examination procedure referred to in Article 36(2), no later than 30 June 2025. That list shall be reviewed, and updated if appropriate, as often as necessary in light of new evidence.
3. The classification of low-risk and high-risk countries or parts thereof, pursuant to paragraph 1 shall be based on an objective and transparent assessment by the Commission, taking into account the latest scientific evidence and internationally recognised sources. The classification shall be based primarily on the following assessment criteria: (a) rate of deforestation and forest degradation; (b) rate of expansion of agriculture land for relevant commodities; (c) production trends of relevant commodities and of relevant products.

---

[2] Cite as: [EUDR Article 16(9)–(12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Obligation to carry out checks
Similarity: 0.766
9. Each Member State shall ensure that the annual checks carried out by its competent authorities pursuant to paragraph 1 of this Article cover at least 9 % of the operators, non-SME downstream operators and non-SME traders placing or making available on the market or exporting relevant products that contain or have been made using relevant commodities as well as 9 % of the quantity of each of the relevant products that contain or have been made using relevant commodities produced in a country or parts thereof classified as high risk in accordance with Article 29.
10. Each Member State shall ensure that the annual checks carried out by its competent authorities pursuant to paragraph 1 of this Article cover at least 1 % of the operators, non-SME downstream operators and non-SME traders placing or making available on the market or exporting relevant products that contain or have been made using relevant commodities produced in a country or parts thereof classified as low risk in accordance with Article 29.
11. The quantified objectives of checks to be carried out by competent authorities shall be met separately for each of the relevant commodities. The quantified objectives shall be calculated by reference to the total number of operators, non-SME downstream operators and non-SME traders who placed or made available on the market or exported relevant products in the previous year, and to quantity, where applicable. Operators shall be considered as having been checked where the competent authority has checked the elements referred to in Article 18(1), points (a) and (b). Downstream operators and traders shall be considered as having been checked where the competent authority has checked the elements referred to in Article 19(1).
12. Without prejudice to checks planned in advance pursuant to paragraph 5 of this Article, competent authorities shall carry out checks referred to in paragraph 1 of this Article when they obtain or are made aware of relevant information, including based on substantiated concerns submitted by third parties under Article 31, concerning a potential case of non-compliance with this Regulation.

---

[3] Cite as: [FAQ 6.9, p. 75]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How can we mitigate the risk of operators avoiding certain supply chains or certain producer countries/regions that are benchmarked as 'high risk'?
Similarity: 0.762
Operators sourcing from standard and high-risk countries or parts of countries are subject to the same standard due diligence obligations.
The only difference is that shipments from high- risk countries will be subject to enhanced scrutiny from Competent Authorities (9% of operators sourcing from high-risk areas).
In that sense, drastic changes of supply chains are not warranted or expected.
Furthermore, high risk classification will entail a specific dialogue with the Commission to address jointly the root causes of deforestation and forest degradation, and with the objective to reduce their level of risk.

---

[4] Cite as: [FAQ 5.1 (part 1/2), p. 62]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are my obligations as an operator?
Similarity: 0.761
As a general rule, operators will have to set up and maintain a Due Diligence System in accordance with Art. 12 EUDR.
N.B.:
This obligation does not apply to downstream operators or traders.
The exercise of due diligence under EUDR consists of three steps.
As step one, operators will need to collect the information referred to in Art. 9 EUDR, such as the commodity or product which they intend to place on the EU market or export, including under customs procedures ‘release for free circulation’ and ‘export’, as well as the respective quantity, direct supplier and direct commercial client, country of production, evidence of legal harvest, among others.
A key requirement, in this step, is to obtain the geographic coordinates of the plots of land where the relevant commodity was produced and to provide relevant information – product, CN code, quan tity, country of production, geolocation coordinates – in the due diligence statement to be submitted via the Information System.
In the case of a simplified declaration, geolocation coordinates may be replaced by postal address information.
If the operator cannot collect the required information, it must refrain from placing the affected products on the European Union market or exporting from it.
Failing to do so would result in a violation of the Regulation, which could lead to potential penalties.
In step two, companies will use the information gathered under step one to assess the risk that the products they intend to place on the market or export are non-compliant.
As part of their Due Diligence Systems, they will verify and evaluate the risk of non-compliant products entering the supply chain, taking into account the criteria described in Art. 10 EUDR.
Operators need to demonstrate how the information gathered was checked against the risk assessment criteria and how they determined the risk.
In step three, they will need to take adequate and proportionate mitigation measures in case they find under step two more than a negligible risk of non-compliance in order to make sure that the risk becomes negligible, taking into account the criteria described in Art. 11 EUDR.

---

[5] Cite as: [Guidance §10 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | The role of certifications and third-party verification schemes in risk assessment and risk mitigation
Similarity: 0.759
Relevant legislation: EUDR – Recital (52); Article 10(2)(n) – Risk assessment
Certification and third-party verified schemes are often used to meet specific customer requirements for relevant commodities and relevant products. This may include a standard that describes practices that must be implemented during production of the certified commodities, comprising principles, criteria and indicators; requirements for checking compliance with the standard and awarding certificates; and separate chain-of-custody certification to provide assurance along the supply chain that a product contains only (or in some cases a specified percentage of) certified or third-party verified material from identified and certified or third-party verified producers.
The EUDR acknowledges that certification and other third-party verified schemes may provide useful information on compliance with the Regulation in the risk assessment further to Article 10 by supporting evidence that products are legal and deforestation-free. This is subject to the condition that this information meets the relevant requirements set out in Article 9, as stipulated in Article 10(2)(n).
Indeed, certifications and third-party verified schemes are operated by an organisation that is not a participant in the production or the supply chain of the relevant commodity. Furthermore, some of these schemes are often used to verify that certain standards or rules are being followed, but do not necessarily go as far as certifying the product itself.
This guidance is directed primarily to stakeholders considering making use of certification or third-party verified schemes given their potential added value in providing complementary information, such as on geolocation coordinates and supporting the operators’ risk assessment undertaken as part of their due diligence exercise that relevant products are legal and deforestation-free. The EUDR does not oblige: (1) operators to make use of such schemes, (2) producers to sign up to them, nor (3) producer countries to develop such schemes. Making use of third-party verification schemes is not a legal requirement, but a voluntary decision of the operator. If operators decide to make use of these schemes, this guidance is designed to help them assess the degree to which these schemes can support to meet the requirements of the EUDR.

=====

[1] Cite as: [EUDR Article 16(9)–(12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Obligation to carry out checks
Similarity: 0.82
9. Each Member State shall ensure that the annual checks carried out by its competent authorities pursuant to paragraph 1 of this Article cover at least 9 % of the operators, non-SME downstream operators and non-SME traders placing or making available on the market or exporting relevant products that contain or have been made using relevant commodities as well as 9 % of the quantity of each of the relevant products that contain or have been made using relevant commodities produced in a country or parts thereof classified as high risk in accordance with Article 29.
10. Each Member State shall ensure that the annual checks carried out by its competent authorities pursuant to paragraph 1 of this Article cover at least 1 % of the operators, non-SME downstream operators and non-SME traders placing or making available on the market or exporting relevant products that contain or have been made using relevant commodities produced in a country or parts thereof classified as low risk in accordance with Article 29.
11. The quantified objectives of checks to be carried out by competent authorities shall be met separately for each of the relevant commodities. The quantified objectives shall be calculated by reference to the total number of operators, non-SME downstream operators and non-SME traders who placed or made available on the market or exported relevant products in the previous year,
[...]
```

</details>

## q23 (single)

**Question:** What can an operator skip under simplified due diligence?

**Reference:** The risk assessment and risk mitigation obligations of Articles 10 and 11, if all products come from low-risk countries and the operator has assessed the supply chain and found a negligible risk of circumvention or mixing; documentation must be available on request.

**Answer:**

Under simplified due diligence, operators can skip the obligations under **Article 10 (Risk assessment)** and **Article 11 (Risk mitigation)** `[EUDR Article 13(1)]`. 

Operators still must collect information (Article 9), establish a due diligence system (Article 12), and assess the complexity of the supply chain and the risk of circumvention or mixing with products of unknown or higher-risk origins [FAQ 5.1, p. 62, Guidance §4(e)]. *(Note: The FAQ and Guidance reflect the Commission's views and are not legally binding.)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 13]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Simplified due diligence
Similarity: 0.728
1. When placing relevant products on the market or exporting them, operators shall not be required to fulfil the obligations under Articles 10 and 11 where, after having assessed the complexity of the relevant supply chain and the risk of circumvention of this Regulation or the risk of mixing with products of unknown origin or origin in high-risk or standard-risk countries or parts thereof, they have ascertained that all relevant commodities and relevant products have been produced in countries or parts thereof that were classified as low risk in accordance with Article 29. In such cases, the operator shall make available to the competent authority upon request relevant documentation demonstrating that there is a negligible risk of circumvention of this Regulation or of mixing with products of unknown origin or origin in high-risk or standard-risk countries or parts thereof.
2. Notwithstanding paragraph 1 of this Article, if the operator obtains or is made aware of any relevant information, including as a result of the assessment carried out under paragraph 1 of this Article, and including substantiated concerns submitted under Article 31, that would point to a risk that the relevant products do not comply with this Regulation or that this Regulation is circumvented, the operator shall fulfil all of the obligations under Articles 10 and 11 and shall immediately communicate any relevant information to the competent authority.
3. Where a competent authority is made aware of any information that would point to a risk of circumvention of this Regulation, including in cases in which relevant commodities or relevant products produced in a standard-risk or high-risk country or a part thereof are subsequently processed in a low-risk country or a part thereof from where they are placed on or leave the market, the competent authority shall take immediate action in accordance with Article 17(1) and, where necessary, adopt interim measures in accordance with Article 23.

---

[2] Cite as: [Guidance §4(e)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Simplified due diligence, i.e. sourcing from low-risk countries
Similarity: 0.723
Operators sourcing from low-risk countries are required to exercise due diligence in line with Article 8, fulfil information requirements of Article 9 and establish a due diligence system in line with Article 12.
However, in accordance with Article 13, they are not required to fulfil the obligations under Article 10 and Article 11 where, after having assessed:
(i) | the complexity of the relevant supply chain; and
(ii) | the risk of circumvention or mixing with products of unknown origin, or origin in high-risk or standard-risk countries or parts thereof, they have ascertained that all relevant commodities and products they place on the market or export have been produced exclusively in such countries or parts thereof that were classified as low risk in accordance with Article 29 ().
For simplified due diligence under Article 13, no further steps of assessing the information or mitigating risk are required unless, in the course of information collection or in the course of the assessment required by Article 13 itself, operators are made aware of relevant new information indicating that a relevant product that they intend to place on the market or export is at risk of not complying with the Regulation.
Micro or small primary operators are, generally, not required to carry out risk assessment and risk mitigation as they are by definition an operator sourcing from low-risk country, unless they obtain or are made aware of any relevant information pointing to a non-negligible risk that the relevant products are non-compliant.

---

[3] Cite as: [Guidance §4 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Due diligence
Similarity: 0.717
Operators, including micro or small primary operators, placing on the market or exporting relevant products produced in low-risk countries benefitting from simplified due diligence in line with Article 13 are not required to fulfil the obligations under Article 10 and Article 11 in order to achieve a negligible risk, unless operators obtain or are made aware of information indicating that a relevant product that they intend to place on the market or export is at risk of not complying with the Regulation. See point (c) and (e) for more details.

---

[4] Cite as: [FAQ 5.1 (part 2/2), p. 62]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are my obligations as an operator?
Similarity: 0.713
These measures need to be documented.
Policies, controls, measures and procedures to be used for risk mitigation are specified in more detail in Art. 11(1), (2) EUDR.
Operators sourcing commodities entirely from areas classified as low risk will be subject to simplified due diligence obligations.
According to Art. 13 EUDR, they will still need to collect information in line with Art. 9 and assess the complexity of the supply chain and the risk of circumvention and the risk of mixing the product with products of unknown origin or origin of standard or high risk countries, b ut they will not be required to assess and mitigate risks (Art. 10 and 11 EUDR) unless the operator obtains or is made aware of any relevant information, including substantiated concerns submitted under Art. 31, that would point to a risk that the relevant products do not comply with this Regulation (Art. 13(2) EUDR).
In the context of simplified due diligence and following the assessment under Art. 13(1) EUDR, the requirement under Art. 9(1)(g) EUDR to provide adequately conclusive and verifiable information that the relevant products are deforestation-free can be fulfilled by collecting the geolocation (or, in the case of MSPOs, the postal address) of plots of land (or establishments in the case of cattle).
For more information about due diligence more generally and information requirements under Art. 9(1)(h) EUDR, see Chapters 4 and 6 of the Commission Notice Guidance document.

---

[5] Cite as: [Guidance §4 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Due diligence
Similarity: 0.701
Relevant legislation: EUDR – Article 2(26) – Definitions; Article 4, 4a and 5 – Obligations of operators, downstream operators and traders; Article 8 – Due diligence; Article 9 – Information requirements; Article 10 – Risk assessment
According to Article 4(1), all operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, shall exercise due diligence in accordance with Article 8 prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Article 3. In order to do so, and in accordance with Article 12(1), operators shall establish and keep up to date a framework of procedures and measures – a ‘due diligence system’.
The due diligence requirements set out in Article 8 require operators to:
— | collect information, documents and, where relevant, data from each supplier about the relevant products which are subject to the EUDR (listed in Annex I) pursuant to Article 8 and 9,
— | verify and analyse that information along with other contextual information and on that basis carry out a risk assessment pursuant to Article 10, and
— | adopt risk mitigation measures pursuant to Article 11, unless the risk assessment carried out in accordance with Article 10 concludes that there is no or only negligible risk that the relevant products are non-compliant.
Operators are responsible for a thorough examination and analysis of their own business activities, which requires the collection of information, data and documents needed to fulfil the information requirements of Article 9, analysing it as part of the risk assessment (Article 10), and adopt risk mitigation measures (Article 11) as necessary, unless the risk of non-compliance is assessed as being negligible.
All operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, are obliged to fulfil the information requirements set out in Article 9.
```

</details>

## q24 (single)

**Question:** What evidence proves that our cocoa was imported before the EUDR started to apply?

**Reference:** For imported products, the customs declaration is accepted as evidence of having been placed on the EU market before the date of application.

**Answer:**

For imported products, the **customs declaration** of the relevant commodities or products is accepted as evidence that they were placed on the EU market before the date of application [FAQ 9.2, p. 87]. 

*Note: This answer rests on the Commission FAQ, which reflects the Commission's views and is not legally binding.*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 8.3, p. 85]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How to prove that the product was produced before the Regulation entered into force? What are the rules for the production of cattle products?
Similarity: 0.8
Who bears the burden of proof that the relevant commodity or relevant product which an operator wants to place on the EU market or export was produced before entry into force and the Regulation does not apply? The Regulation is applicable as stipulated in Art. 1(1) unless the conditions of Art. 1(2) are met, meaning unless the commodity contained in the product or which has been used to make the product was produced before 29 June 2023, as stipulated in Art. 2(1 4).
For cattle, the relevant date of production is the date on which the cattle is born, meaning that the Regulation does not apply to cattle and cattle products if the cattle was born before the entry into force.
The operator bears the burden of proof for this exception and must be able to provide relevant information as reasonable proof that the conditions of Art. 1(2) EUDR are met.
While in this case the operator is not obliged to submit a due diligence statement, the operator should keep necessary documents proving non-applicability of the Regulation and its obligations. °°°°

---

[2] Cite as: [FAQ 9.2, p. 87]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What evidence is necessary to prove that the product was placed on the EU market before the date of entry into application (i.e. what documents are accepted as evidence of ‘placing on the market’)? Do such products need to be declared in the Information System?
Similarity: 0.798
In case of imported products, the customs declaration of the relevant commodities or relevant products in question will be accepted as evidence of having been placed on the EU market before the date of application.
For EU produced goods, other documentatio n should be accepted as evidence, for example documentation relating to the production date, if the production date aligns with the time of placing on the market, e.g. felling tickets, ear tag and passport of cattle, invoices, or other documentation related to the production or selling date of the commodity.
The date of placing on the EU market can be supported e.g. by contracts between the parties, product order documents, shipment accompanying documents about the delivery to the customer including CMRs (Convention on the Contract for the International Carriage of Goods by road), bill of lading, delivery notes, air-way-bill, and any other documents showing evidence that goods are transferred between 2 parties which can be linked directly to the relevant product in question.
For details on the time of placing on the EU market, please refer to FAQ 5.20.
For products falling in the transitional period, no DDS needs to be submitted in the Information System.
In case of export or re-import of a product which was initially placed on the EU market during the transitional period (itself or in the form of an ups tream relevant product), a “conventional DDS reference number”, meaning a universal reference number that can be entered in the customs declaration in cases of products falling in the transitional period can be used in the customs declaration submitted for export or re-import.
The format of the conventional DDS reference number is 99EU9999999999.
Further information about it can be found here.
It should be noted that no conventional number needs to be provided in case of export by a downstream operator; instead, a dedicated TARIC certificate code will be available in this situation (see FAQ 5.6.1).

---

[3] Cite as: [FAQ 5.6, p. 65]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Does placing on the market of products not produced in the EU require customs clearing?
Similarity: 0.796
Would a customs declaration be sufficient documentation in this context? Yes, placing on the market relevant commodities or relevant products produced outside of the EU requires customs clearance prior to placing on the market.
In this context, only a customs declaration (neither a bill of lading nor a nother commercial or logistics document) would be considered as adequate evidence, if it can be directly linked to the product in question.

---

[4] Cite as: [FAQ 5.4 (part 2/2), p. 64]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are my obligations if I am re-importing a product that was previously exported from the EU?
Similarity: 0.795
The above applies equally where the product that is imported is made of relevant products that were previously exported from the EU market and have been subject to due diligence (example: cocoa beans are exported from the EU to a third country to manufacture chocolate, and the chocolate is subsequently released for free circulation in the EU).
For parts of relevant products that have not been subject to due diligence, operators must exercise due diligence and submit a DDS.

---

[5] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.795
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;
```

</details>

## q25 (single)

**Question:** What does 'negligible risk' mean under the EUDR?

**Reference:** The level of risk where, after a full assessment of product-specific and general information and any needed mitigation, the products show no cause for concern of not complying with Art. 3(a) or (b).

**Answer:**

Under the EUDR, **‘negligible risk’** means that, following a full assessment of product-specific and general information (and the application of appropriate mitigation measures where necessary), relevant commodities and products show **no cause for concern** of not complying with the requirements of being deforestation-free and legally produced [FAQ 5.9, p. 67, Guidance §4(b)]. 

* Reaching a conclusion of ‘negligible risk’ is a mandatory pre-condition resulting from due diligence before an operator can place products on or export them from the EU market [FAQ 5.10, p. 67].
* If any risk criteria reveal a non-negligible level of risk, the product is deemed to carry a non-negligible risk and cannot be placed on or exported from the EU market [Guidance §4(b)].

*(Note: This explanation rests partly on Commission Guidance and FAQs, which reflect the Commission's views and are not legally binding).*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 5.9, p. 67]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are the criteria for ‘negligible risk products’?
Similarity: 0.874
‘Negligible risk’ refers to the level of risk that applies to relevant products to be placed on the EU market or exported from the EU, where, on the basis of a full assessment of product - specific and general information, and, where necessary, of the application of the appropriate mitigation measures, those commodities or products show no cause for concern as to not being in compliance with Art. 3 points (a) or (b) EUDR.

---

[2] Cite as: [FAQ 5.10, p. 67]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Are ‘negligible risk products’ exempt?
Similarity: 0.855
Can we understand “negligible risk” under Art. 2(26) EUDR read together with Art. 10(1) as providing an exemption from the Regulation? (UPDATED) No.
Operators may only reach a conclusion on ‘negligible risk’ (which is a pre-condition for placing or making available on the EU market or exporting relevant products) as a result of conducting due diligence (pursuant to Art. 4(1) EUDR).
Conducting due diligence is a core obligation of operators under this Regulation, which is not subject to any exemption.
Please note that the ‘negligible risk’ element does not apply to commodities (there is no ‘risk status’ for each commodity in the Regulation).

---

[3] Cite as: [Guidance §4(b)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Negligible risk
Similarity: 0.854
The concept of negligible risk should be understood in accordance with Article 2(26) which means that on the basis of a full assessment of product-specific and general information pursuant to Article 10, and, where necessary, of the application of the appropriate mitigation measures pursuant to Article 11, the commodities or products show no cause for concern as being not in compliance with Article 3(a) (deforestation-free) or (b) (produced legally, in accordance with the applicable legislation in the country of production).
The list of risk assessment criteria in Article 10(2) is not exhaustive; operators may choose to apply further criteria if these would help determine the likelihood that a relevant commodity or product had been illegally produced or was not deforestation-free, or if it would help prove legal or deforestation-free production.
In case the risk assessment and risk mitigation exercise concludes that any of the risk criteria reveal a non-negligible level of risk, then the product should be deemed as carrying a non-negligible risk, therefore the operator shall not place it on or export it from the Union market.

---

[4] Cite as: [FAQ 5.11, p. 67]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Could certain commodities from a given country be considered ‘negligible risk’?
Similarity: 0.82
Could palm oil, rubber, coffee, cacao, or timber from a given country be considered ‘negligible risk’? No.
See question above.

---

[5] Cite as: [EUDR Article 2 (part 1/6)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Definitions
Similarity: 0.816
For the purposes of this Regulation, the following definitions apply:
(1) ‘relevant commodities’ means cattle, cocoa, coffee, oil palm, rubber, soya and wood;
(2) ‘relevant products’ means products listed in Annex I that contain, have been fed with or have been made using relevant commodities;
(3) ‘deforestation’ means the conversion of forest to agricultural use, whether human-induced or not;
(4) ‘forest’ means land spanning more than 0,5 hectares with trees higher than 5 metres and a canopy cover of more than 10 %, or trees able to reach those thresholds in situ, excluding land that is predominantly under agricultural or urban land use;
(5) ‘agricultural use’ means the use of land for the purpose of agriculture, including for agricultural plantations and set-aside agricultural areas, and for rearing livestock;
(6) ‘agricultural plantation’ means land with tree stands in agricultural production systems, such as fruit tree plantations, oil palm plantations, olive orchards and agroforestry systems where crops are grown under tree cover; it includes all plantations of relevant commodities other than wood; agricultural plantations are excluded from the definition of ‘forest’;
(7) ‘forest degradation’ means structural changes to forest cover, taking the form of the conversion of: (a) primary forests or naturally regenerating forests into plantation forests or into other wooded land; or (b) primary forests into planted forests;
(8) ‘primary forest’ means naturally regenerated forest of native tree species, where there are no clearly visible indications of human activities and the ecological processes are not significantly disturbed;
(9) ‘naturally regenerating forest’ means forest predominantly composed of trees established through natural regeneration; it includes any of the following: (a) forests for which it is not possible to distinguish whether planted or naturally regenerated; (b) forests with a mix of naturally regenerated native tree species and planted or seeded trees, and where the naturally regenerated trees are expected to constitute the major part of the growing stock at stand maturity; (c) coppice from trees originally established through natural regeneration; (d) naturally regenerated trees of introduced species;

=====

[1] Cite as: [Guidance §4(b)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Negligible risk
Similarity: 0.847
The concept of negligible risk should be understood in accordance with Article 2(26) which means that on the basis of a full assessment of product-specific and general information pursuant to Article 10, and, where necessary, of the application of the appropriate mitigation measures pursuant to Article 11, the commodities or products show no cause for concern as being not in compliance with Article 3(a) (deforestation-free) or (b) (produced legally, in accordance with the applicable legislation in the country of production).
The list of risk assessment criteria in Article 10(2) is not exhaustive; operators may choose to apply further criteria if these would help determine the likelihood that a relevant commodity or product had been illegally produced or was not deforestation-free, or if it would help prove legal or deforestation-free production.
In case the risk assessment and risk mitigation exercise concludes that any of the risk criteria reveal a non-negligible level of risk, then the product should be deemed as carrying a non-negligible risk, therefore the operator shall not place it on or export it from the Union market.

---

[2] Cite as: [EUDR Article 2 (part 1/6)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Definitions
Similarity: 0.845
For the purposes of this Regulation, the following definitions apply:
(1) ‘relevant commodities’ means cattle, cocoa, coffee, oil palm, rubber, soya and wood;
(2) ‘relevant products’ means products listed in Annex I that contain, have been fed with or have been made using relevant commodities;
(3) ‘deforestation’ means the conversion of forest to agricultural use, whether human-induced or not;
(4) ‘forest’ means land spanning more than 0,5 hectares with trees higher than 5 metres and a canopy cover of more than 10 %, or trees able to reach those thresholds in situ, excluding land that is predominantly under agricultural or urban land use;
(5) ‘agricultural use’ means the use of land for the purpose of agriculture, including for agricultural plantations and set-aside agricultural areas, and for rearing livestock;
(6) ‘agricultural plantation’ means land with tree stands in agricultural production systems, such as fruit tree plantations, oil palm plantations, olive orchards and agroforestry systems where crops are grown under tree cover; it includes all plantations of relevant commodities other than wood; agricultural plantations are excluded from the definition of ‘forest’;
(7) ‘forest degradation’ means structural changes to forest cover, taking the form of the conversion of: (a) primary forests or naturally regenerating forests into plantation forests or into other wooded land; or (b) primary forests into planted forests;
(8) ‘primary forest’ means naturally regenerated forest of native tree species, where there are no clearly visible indications of human activities and the ecological processes are not significantly disturbed;
(9) ‘naturally regenerating forest’ means forest predominantly composed of trees established through natural regeneration; it includes any of the following: (a) forests for which it is not possible to distinguish whether planted or naturally regenerated; (b) forests with a mix of naturally regenerated native tree species and planted or seeded trees, and where the naturally regenerated trees are expected to constitute the major part of the growing stock at stand maturity; (c) coppice from trees originally established through natural regeneration; (d) naturally regenerated trees of introduced species;

---

[3] Cite as: [FAQ 5.9, p. 67]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are the criteria for ‘negligible risk products’?
Similarity: 0.834
‘Negligible risk’ refers to the level of risk that applies to relevant products to be placed on the EU market or exported from the EU, where, on the basis of a full assessment of product - specific and general information, and, where necessary, of the application of the appropriate mitigation measures, those commodities or products show no cause for concern as to not being in compliance with Art. 3 points (a) or (b) EUDR.

---

[4] Cite as: [EUDR Article 29(1)–(3)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Assessment of countries
Similarity: 0.829
1. This Regulation establishes a three-tier system for the assessment of countries or parts thereof. For that purpose, Member States and third countries, or parts thereof, shall be classified into one of the following risk categories: (a) ‘high risk’ refers to countries or parts thereof, for which the assessment referred to in paragraph 3 results in the identification of a high risk of producing in such countries or in parts thereof, relevant commodities for which the relevant products do not comply with Article 3, point (a); (b) ‘low risk’ refers to countries or parts thereof, for which the assessment referred to in paragraph 3 concludes that there is sufficient assurance that instances of producing in such countries or in parts thereof, relevant commodities for which the relevant products do not comply with Article 3, point (a), are exceptional; (c) ‘standard risk’ refers to countries or parts thereof which do not fall in either the category ‘high risk’ or the category ‘low risk’.
2. On 29 June 2023, all countries shall be assigned a standard level of risk. The Commission shall classify countries or parts thereof, that present a low or high risk in accordance with paragraph 1 of this Article. The list of the countries or parts thereof, that present a low or high risk shall be published by means of implementing acts to be adopted in accordance with the examination procedure referred to in Article 36(2), no later than 30 June 2025. That list shall be reviewed, and updated if appropriate, as often as necessary in light of new evidence.
3. The classification of low-risk and high-risk countries or parts thereof, pursuant to paragraph 1 shall be based on an objective and transparent assessment by the Commission, taking into account the latest scientific evidence and internationally recognised sources. The classification shall be based primarily on the following assessment criteria: (a) rate of deforestation and forest degradation; (b) rate of expansion of agriculture
[...]
```

</details>

## q26 (multi)

**Question:** We are a medium-sized importer buying cocoa from Côte d'Ivoire. What does our due diligence involve, and from when?

**Reference:** Collect the Article 9 information, assess risk (Article 10) and mitigate it (Article 11) before placing the cocoa on the market, from 30 December 2026.

**Answer:**

Your due diligence involves establishing and keeping up to date a due diligence system comprising three steps:
1. **Information collection:** Gathering information, documents, and data from suppliers pursuant to Articles 8 and 9 (including geolocation of the plots of production in Côte d'Ivoire) [Guidance §4 (part 1/2)].
2. **Risk assessment:** Verifying and analyzing that information along with contextual data to assess whether the cocoa complies with the EUDR (def-free, produced on land without forest conversion after 31 December 2020, and in accordance with local legislation) [Guidance §4 (part 1/2)].
3. **Risk mitigation:** Adopting measures to mitigate risks unless the risk assessment concludes there is no or only negligible risk [Guidance §4 (part 1/2)].

**From when:** For medium enterprises, obligations apply from **30 December 2026** (inclusive) for cocoa produced from relevant commodities harvested or produced from 29 June 2023 onwards [Guidance §3 (part 3/6), Guidance §3 (part 1/6)]. 

*(Note: Guidance-based statements reflect the Commission's views and are not legally binding.)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [Guidance §4 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Due diligence
Similarity: 0.735
Relevant legislation: EUDR – Article 2(26) – Definitions; Article 4, 4a and 5 – Obligations of operators, downstream operators and traders; Article 8 – Due diligence; Article 9 – Information requirements; Article 10 – Risk assessment
According to Article 4(1), all operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, shall exercise due diligence in accordance with Article 8 prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Article 3. In order to do so, and in accordance with Article 12(1), operators shall establish and keep up to date a framework of procedures and measures – a ‘due diligence system’.
The due diligence requirements set out in Article 8 require operators to:
— | collect information, documents and, where relevant, data from each supplier about the relevant products which are subject to the EUDR (listed in Annex I) pursuant to Article 8 and 9,
— | verify and analyse that information along with other contextual information and on that basis carry out a risk assessment pursuant to Article 10, and
— | adopt risk mitigation measures pursuant to Article 11, unless the risk assessment carried out in accordance with Article 10 concludes that there is no or only negligible risk that the relevant products are non-compliant.
Operators are responsible for a thorough examination and analysis of their own business activities, which requires the collection of information, data and documents needed to fulfil the information requirements of Article 9, analysing it as part of the risk assessment (Article 10), and adopt risk mitigation measures (Article 11) as necessary, unless the risk of non-compliance is assessed as being negligible.
All operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, are obliged to fulfil the information requirements set out in Article 9.

---

[2] Cite as: [Guidance §3 (part 3/6)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Date of effect and time-frame for application
Similarity: 0.728
Date of placing relevant commodity or relevant product on the EU market
Relevant products | Date of production of relevant commodity | Before 30 December 2026, and before 30 June 2027 for micro- and small operators | From 30 December 2026 (inclusive) for large and medium enterprises, and from 30 June 2027 (inclusive) for micro- and small operators
Cattle, Cocoa, Coffee, Oil palm, Rubber and Soya products listed in Annex I of Regulation (EU) 2023/1115 | Before 29 June 2023 | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is not applicable
From 29 June 2023 (inclusive) | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is applicable
Wood products listed in Annex I of Regulation (EU) 2023/1115 and not listed in the Annex of Regulation (EU) No 995/2010 (EUTR) | Before 29 June 2023 | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is not applicable
From 29 June 2023 (inclusive) | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is applicable
For timber and timber products covered by the Annex of the EUTR, special rules apply, pursuant to Article 37(3) of EUDR:

---

[3] Cite as: [FAQ 5.1.1, p. 63]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Can an operator use the ir due diligence systems established under EUDR for complying with other EU due diligence-related laws, such as the CSDDD or the Forced Labour Regulation?
Similarity: 0.725
An operator can use a due diligence system established under EUDR to support compliance with legal obligations established under other relevant EU legislation.
For instance, the three step due diligence process under EUDR can be helpful towards compliance with certain requirements of the Corporate Sustainability Due Diligence Directive (CSDDD) and the Forced Labour Regulation (FLR), although the scope and requirements under these two laws differ.
Under EUDR, for the purpose of assessing compliance of EUDR-relevant products with Art. 3 EUDR, the due diligence process includes information collection, risk assessment, and risk mitigation.
While these elements are also required by CSDDD, additional elements of due diligence, such as meaningful stakeholder engagement and establishing a notificati on mechanism and a complaints procedure, are required.
The Commission will publish guidelines on CSDDD in accordance with Art. 19 CSDDD.
The application date for measures under CSDDD is 26 July 2029, Art. 37(1) CSDDD.
The Forced Labour Regulation (FLR) applies from 14 December 2027, Art. 39 FLR.
It prohibits economic operators from placing and making available on the Union market or exporting from the Union market products made with forced labour.
This applies also to economic operators in scope of EUDR.
Contrary to EUDR, the FLR does not impose due diligence obligations.
However, due diligence could help identify, mitigate, prevent and bring to an end the risk of forced labour in supply chains.
To facilitate compliance with the FLR, the Commission will issue guidance on due diligence to address forced labour risks in supply chains.
This process includes additional elements but also involves information collection, risk assessment and risk mitigation of forced labour.

---

[4] Cite as: [Guidance §3 (part 1/6)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Date of effect and time-frame for application
Similarity: 0.72
Relevant legislation: EUDR – Article 1(2) Subject matter and scope; Article 37 – Repeal; Article 38 – Entry into force and date of application
The EUDR entered into force on 29 June 2023. Most obligations on operators, downstream operators and traders, as well as on competent authorities including those in Articles 3 to 13, Articles 16 to 24, Articles 26, 31, and 32, apply from 30 December 2026, in accordance with Regulation (EU) 2025/2650 () amending the provisions of the EUDR relating to the date of application.
For operators that were established as micro-undertakings or small undertakings by 31 December 2024 (in accordance with Article 3(1) or (2), first subparagraph, of Directive 2013/34/EU, respectively) the obligations in Articles 3 to 13, Articles 16 to 24, Articles 26, 31 and 32, apply from 30 June 2027, except as regards the products covered in the Annex of the Regulation (EU) No 995/2010 laying down the obligations of operators who place timber and timber products on the market () (EUTR). This means that there is a transitional period between the entry into force of the Regulation (29 June 2023) and the entry into application (30 December 2026, deferred to 30 June 2027 for small undertakings or micro-undertakings established by 31 December 2024) that exempts operators and traders placing or making available on or export from the Union market relevant commodities and products in the transitional period from the main obligations under the EUDR.
The following rules apply for all commodities and associated relevant products with the exception of timber and timber products covered by the Annex of the EUTR (detailed explanations are provided in the Frequently Asked Questions document, Section 9):
— | if a relevant commodity or a relevant product is placed on the market during the transitional period applying to the respective operator, the obligations of the EUDR do not apply to the operator.

---

[5] Cite as: [Guidance preamble (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896)
Similarity: 0.719
Official Journal of the European Union | EN C series
C/2026/3896 | 20.7.2026
(C/2026/3896)
Table of contents
1. | DEFINITIONS OF ‘PLACING ON THE MARKET’, ‘MAKING AVAILABLE ON THE MARKET’ AND ‘EXPORT’ | 3
(a) | Placing on the market | 4
(b) | Making available on the market | 4
(c) | Export | 5
2. | DEFINITION OF ‘OPERATOR’, ‘DOWNSTREAM OPERATOR’, ‘MICRO OR SMALL PRIMARY OPERATOR’ AND ‘TRADER’ | 5
(a) | Operator | 5
(b) | Micro or Small Primary Operator | 7
(c) | Downstream Operator | 7
(d) | Trader | 7
3. | DATE OF EFFECT AND TIME-FRAME FOR APPLICATION | 8
4. | DUE DILIGENCE | 10
(a) | Risk assessment and risk mitigation (Article 10 and 11) | 11
(b) | Negligible risk | 12
(c) | Obligations for micro or small primary operators | 12
(d) | Obligations for downstream operators and traders | 13
(e) | Simplified due diligence, i.e. sourcing from low-risk countries | 13
(f) | Interplay with Corporate Sustainability Due Diligence Directive and the Forced Labour Regulation | 14
5. | CLARIFICATION OF ‘COMPLEXITY OF THE SUPPLY CHAIN’ | 14
6. | LEGALITY | 15
(a) | Relevant legislation of the country of production | 15
(b) | Due diligence regarding legality | 17
7. | PRODUCT SCOPE | 19
(a) | Clarification – Packing and packaging materials | 19
(b) | Clarification – Waste and recovered and recycled products | 20
8. | REGULAR MAINTENANCE OF A DUE DILIGENCE SYSTEM | 22
9. | COMPOSITE PRODUCTS | 22
10. | THE ROLE OF CERTIFICATIONS AND THIRD-PARTY VERIFICATION SCHEMES IN RISK ASSESSMENT AND RISK MITIGATION | 24
(a) | The role of certifications and third-party verification schemes | 24
(b) | Background information | 26
11. | AGRICULTURAL USE | 27
1. | Introduction | 27
2. | Clarification of conversion of forest to land the purpose of which is not agricultural use | 28
3. | Definition of ‘Forest’ | 29
4. | Definition of ‘Agricultural use’ and exceptions | 30
```

</details>

## q27 (multi)

**Question:** If the authorities suspect a cocoa shipment, how long can it be held, and what penalties can follow if it does not comply?

**Reference:** Suspension for three working days, extendable by three-day periods. Penalties include fines with a maximum of at least 4% of EU turnover, confiscation of the products and of the revenues, exclusion from public procurement for up to 12 months, and bans on placing products on the market for serious or repeated infringements.

**Answer:**

The corpus does not cover this. An answer was drafted, but it could not be traced to the passages the search returned, so it was withheld. Check the cited sources or ask the competent authority.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 25(1)–(2)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Penalties
Similarity: 0.775
1. Without prejudice to the obligations of Member States under Directive 2008/99/EC of the European Parliament and of the Council (5), Member States shall lay down rules on penalties applicable to infringements of this Regulation by operators, downstream operators and traders and shall take all measures necessary to ensure that they are implemented. Member States shall notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendments affecting them.
2. The penalties provided for in paragraph 1 shall be effective, proportionate and dissuasive. Those penalties shall include: (a) fines proportionate to the environmental damage and the value of the relevant commodities or relevant products concerned, calculating the level of such fines in such way as to ensure that they effectively deprive those responsible of the economic benefits derived from their infringements, and gradually increasing the level of such fines for repeated infringements; in the case of a legal person, the maximum amount of such a fine shall be at least 4 % of the operator’s, downstream operator’s or trader’s total annual Union-wide turnover in the financial year preceding the fining decision, calculated in accordance with the calculation of aggregate turnover for undertakings laid down in Article 5(1) of Council Regulation (EC) No 139/2004 (6), and shall be increased, where necessary, to exceed the potential economic benefit gained; (b) confiscation of the relevant products concerned from the operator, downstream operator and/or trader; (c) confiscation of revenues gained by the operator, downstream operator and/or trader from a transaction with the relevant products concerned; (d) temporary exclusion for a maximum period of 12 months from public procurement processes and from access to public funding, including tendering procedures, grants and concessions; (e) temporary prohibition from placing or making available on the market or exporting relevant commodities and relevant products, in the event of a serious infringement or of repeated infringements; (f) prohibition from exercising the simplified due diligence set out in Article 13 in the event of a serious infringement or of repeated infringements.

---

[2] Cite as: [FAQ 10.1, p. 94]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What does it mean that the penalties laid down by the EU Member States are without prejudice to the obligations of Member States under Directive 2008/99/EC of the European Parliament and of the Council?
Similarity: 0.752
The EU Member States must lay down the national framework of penalties, which should include at least the penalties listed in Art. 25(2) EUDR and must take all measures necessary to ensure that the rules are implemented.
The level and type of penalties cannot be in contradiction with the Environmental Crime Directive.
The provisions of the Directive are subject to the succession of law.

---

[3] Cite as: [EUDR Article 24]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Corrective action in the event of non-compliance
Similarity: 0.745
1. Without prejudice to Article 25, where competent authorities establish that an operator, downstream operator or trader has not complied with this Regulation or that a relevant product placed or made available on the market or exported is non-compliant, they shall without delay require the operator, downstream operator or trader to take appropriate and proportionate corrective action to bring the non-compliance to an end within a specified and reasonable period of time.
2. For the purposes of paragraph 1, the corrective action required to be taken by the operator, downstream operator or trader shall include at least one of the following, as applicable: (a) rectifying any formal non-compliance, in particular with the requirements of Chapter 2; (b) preventing the relevant product from being placed or made available on the market or exported; (c) withdrawing or recalling the relevant product immediately; (d) donating the relevant product to charitable or public interest purposes or, if that is not possible, disposing of it in accordance with Union law on waste management.
3. Irrespective of the corrective action taken under paragraph 2, the operator, downstream operator or trader shall address any shortcomings in the due diligence system with a view to preventing the risk of further non-compliance with this Regulation.
4. If the operator, downstream operator or trader fails to take corrective action as referred to in paragraph 2 within the period of time specified by the competent authority under paragraph 1, or where non-compliance as referred to in paragraph 1 persists, after that period of time competent authorities shall secure application of the required corrective action referred to in paragraph 2 by all means available to them under the law of the Member State concerned.

---

[4] Cite as: [FAQ 3.27 (part 2/2), p. 52]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | When should I update my SD? Are there situations when I need to submit a new SD?
Similarity: 0.742
The information provided in the SD must be truthful at the time of submission and at the time of updating.
If C ompetent Authoritie s detect that estimates or other information were provided for the purpose of misclassifying an operator as an MSPO, circumventing the Regulation’s requirements or negatively impacting enforcement, they may take steps to pursue such breaches of the Regulation, and impose penalties.

---

[5] Cite as: [FAQ 1.27, p. 23]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if upstream suppliers do not provide required information?
Similarity: 0.742
If an operator, downstream operator or a trader placing or making available a commodity on the EU market or exporting it is unable to obtain the information required by the Regulation from its suppliers, they must refrain from placing or making available the relevant products on the EU market or exporting them from the EU as that would result in a violation of the Regulation.

=====

[1] Cite as: [FAQ 9.11, p. 92]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What constitutes high-risk, and how long can a suspension take place?
Similarity: 0.844
Art. 17 EUDR allows Competent Authorities to take immediate actions – including suspension - in situations that present high risk of non-compliance.
What constitutes high- risk, and how long can the suspension take place? Competent Authorities may identify situations where relevant products present a high risk of being non-compliant with the requirements of the Regulation on the basis of different circumstances, including on the spot checks, the outcome of their risk analys is in their risk - based plans, or risks identified through the information system, or on the basis of information coming from another competent Authority, substantiated concerns etc.
In such cases, the Competent Authorities can introduce interim measures as defined in Art. 23 EUDR, including the suspension of placing or making available the product on the EU market.
This suspension should end within three working days, or 72 hours in case of perishable products.
However, the Competent Authority can come to the conclusion, based on checks carried out in this period of time, that the suspension should be extended by additional periods of three days to establish if the product is compliant with the Regulation.

---

[2] Cite as: [EUDR Article 17]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Relevant products requiring immediate action
Similarity: 0.83
1. Competent authorities shall identify situations where relevant products present such high risk of non-compliance with Article 3 that they require immediate action by competent authorities before those relevant products are placed or made available on the market or exported. Competent authorities shall register such identified situations in the information system referred to in Article 33.
2. When competent authorities identify the situations referred to in paragraph 1 of this Article, including when a due diligence statement relating to the relevant products concerned is submitted by an operator, the information system referred to in Article 33 shall identify the high risk of non-compliance with Article 3 and inform competent authorities, which shall: (a) take immediate interim measures under Article 23 to suspend the placing or making available of those relevant products on the market; or (b) once the electronic interface referred to in Article 28(1) is in place, in the case of relevant products entering or leaving the market, require customs authorities to suspend the release for free circulation or export of those relevant products under Article 26(7).
3. The suspensions referred to in paragraph 2 of this Article shall end within three working days or within 72 hours in the case of perishable relevant products, starting from the moment when the high risk of non-compliance is identified in the information system referred to in Article 33. Where the competent authorities, based on the result of the checks carried out within that period, conclude that they require additional time in which to establish whether the relevant products comply with Article 3, they shall extend the period of suspension, by additional periods of three working days, by means of additional interim measures taken under Article 23 or, in the case of relevant products entering or leaving the market, by notifying the customs authorities of the need to maintain the suspension under Article 26(7).

---

[3] Cite as: [EUDR Article 26(7)–(10)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Controls
Similarity: 0.807
7. Where the status referred to in paragraph 6 of this Article indicates that the relevant product entering or leaving the market has been identified, pursuant to Article 17(2), as requiring to be checked before it is placed on the market or exported, customs authorities shall suspend the release for free circulation or export of that relevant product.
8. Where all other requirements and formalities under Union or national law relating to the release for free circulation or export have been fulfilled, customs authorities shall allow a relevant product entering or leaving the market to be released for free circulation or exported in any of the following circumstances: (a) the status referred to in paragraph 6 of this Article does not indicate that the relevant product has been identified, pursuant to Article 17(2), as requiring to be checked before it is placed or made available on the market or exported; (b) the release for free circulation or export has been suspended in accordance with paragraph 7 of this Article, and the competent authorities have not requested to maintain the suspension in accordance with Article 17(3); (c) the release for free circulation or export has been suspended in accordance with paragraph 7 and the competent authorities have notified customs authorities that the suspension of the release for free circulation or export of the relevant products can be lifted.
9. Where the competent authorities conclude that a relevant product entering or leaving the market is non-compliant, they shall notify the customs authorities accordingly and the customs authorities shall not allow the release for free circulation or export of that relevant product.
10. The release for free circulation or export shall not be deemed proof of compliance with Union law and, in particular, with this Regulation.

---

[4] Cite as: [EUDR Article 23]
Document: Regulation (EU) 2023
[...]
```

</details>

## q28 (multi)

**Question:** For cocoa from a low-risk country, which due diligence steps can we skip, and do we still need the farm coordinates?

**Reference:** Risk assessment and mitigation (Articles 10 and 11) can be skipped if the risk of circumvention or mixing is negligible, but geolocation is still required.

**Answer:**

Yes, you still need the farm coordinates (geolocation): there is no exception to the traceability requirement via geolocation for low-risk countries 
[FAQ 1.28, p. 23]. 

Under **simplified due diligence** for low-risk countries, you can skip **risk assessment (Article 10)** and **risk mitigation (Article 11)** steps [Guidance §4(e), FAQ 5.1, p. 62]. 

However, you must still:
* Collect the information requirements under Article 9 (including geolocation coordinates) [Guidance §4(e), FAQ 5.1, p. 62].
* Establish a due diligence system (Article 12) [Guidance §4(e)].
* Assess supply chain complexity and the risk of circumvention or mixing with products of unknown origin or from standard/high-risk countries (Article 13) [Guidance §4(e), FAQ 5.1, p. 62]. 

*Note: Guidance and FAQ answers reflect the Commission's views and are not legally binding.*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 1.28, p. 23]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Should coordinates be provided for land in countries classif ied as low-risk?
Similarity: 0.758
(UPDATED) There is no exception for the traceability requirement via geolocation (or, in the case of a micro or small primary operator, the postal address).
The operators also have to assess the complexity of the relevant supply chain and the risk of circumvention of the Regulation and the risk of mixing with products of unknown origin or origin in high-risk or standard-risk countries or parts thereof (Art. 13 EUDR).
If the operator obtains or is made aware of any relevant information that would point to a risk that the relevant products do not comply with the Regulation or that the Regulation is circumvented, the operator must fulfil all the obligations under Art. 10 and 11 EUDR and must immediately communicate any relevant information to the Competent Authority.

---

[2] Cite as: [FAQ 1.1 (part 1/2), p. 12]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Why and how must operators collect coordinates?
Similarity: 0.747
The Regulation requires operators placing covered products on the EU market or exporting them to collect geographic coordinates of the plots of land where the commodities were produced.
This does not apply to downstream operators who place on the market or export such products (for more information on downstream operators, see Chapter 3 of this document).
Traceability to the plot of land (i.e., the requirement to collect the geographic coordinates of the plots of land where the commodities were produced) is necessary to demonstrate that there has been no deforestation at the specific location of production.
Geographic information linking products to the plot of land is already used by part of the industry and a number of certification organisations.
Remotely sensed information (air photos, satellite images) or other information (e.g., photograph in the field with linked geotags and time stamps) may be used for verifying if the geolocation of declared commodities and products is linked to deforestation.
The geolocation coordinates need to be provided in the due diligence statements (hereinafter referred to as “ due diligence statement” or “ DDS”) or, where applicable, in the simplified declarations (hereinafter referred to as “simplified declaration” or “SD”) that operators are required to submit to the Information System ahead of the placing on the EU market or export from the EU of the products.
It is therefore a core part of the Regulation, which prohibits the placing on the EU market, or the export, of any product covered by the Regulation’s scope whose geolocation coordinates have not yet been collected and submitted as part of a due diligence statement.
The only exception is the SD of micro or small primary operators (MSPO), for whom the geolocation may be replaced by a postal address, provided that the postal address clearly corresponds to the geographic location of the plots of land or establishment concerned (see FAQ 3.28 for more details).
Collecting the geolocation coordinates of a plot of land can be done via mobile phones, handheld Global Navigation Satellite System (GNSS) devices and widespread and free-to-use digital applications (e.g.
Geographic Information Systems (GIS)).

---

[3] Cite as: [Guidance §4(e)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Simplified due diligence, i.e. sourcing from low-risk countries
Similarity: 0.738
Operators sourcing from low-risk countries are required to exercise due diligence in line with Article 8, fulfil information requirements of Article 9 and establish a due diligence system in line with Article 12.
However, in accordance with Article 13, they are not required to fulfil the obligations under Article 10 and Article 11 where, after having assessed:
(i) | the complexity of the relevant supply chain; and
(ii) | the risk of circumvention or mixing with products of unknown origin, or origin in high-risk or standard-risk countries or parts thereof, they have ascertained that all relevant commodities and products they place on the market or export have been produced exclusively in such countries or parts thereof that were classified as low risk in accordance with Article 29 ().
For simplified due diligence under Article 13, no further steps of assessing the information or mitigating risk are required unless, in the course of information collection or in the course of the assessment required by Article 13 itself, operators are made aware of relevant new information indicating that a relevant product that they intend to place on the market or export is at risk of not complying with the Regulation.
Micro or small primary operators are, generally, not required to carry out risk assessment and risk mitigation as they are by definition an operator sourcing from low-risk country, unless they obtain or are made aware of any relevant information pointing to a non-negligible risk that the relevant products are non-compliant.

---

[4] Cite as: [FAQ 1.10, p. 15]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if property registers or titles are unavailable?
Similarity: 0.735
How can operators obtain geolocation data in countries where property registers are incomplete and where farmers may lack IDs or titles over their land? (UPDATED) Farmers can collect the geolocation of their plots of land regardless of whether they are entered or not in a land registry or the lack of IDs or titles over their land.
Unless they are direct suppliers of the operators or operators themselves, no personal information is required from the farmers and the geolocation of the plot used to supply commodities for placing on the EU market is sufficient.
As regards the legality requirement in relation to land use right (Art. 2(40) (a) EUDR) the Regulation requires compliance with relevant national laws.
If farmers are legally allowed to sell their product under national laws (which might lack a property register and where some farmers might lack IDs), then that would also mean that operators would meet the legality requirement when sourcing from those farmers.
If possession of a land title is not required under domestic law to produce and commercialise agricultural products, then it is not required under the Regulation.
Operators, nonetheless, would need to verify that there is no risk of illegality in their supply chains, meaning that relevant laws applicable in the country of production are complied with.
There are many different means that operators already use today to collect the legality (and geolocation) information: some resort to mapping directly their suppliers, while others rely on intermediaries like cooperatives, certification bodies, national traceability systems or other companies.
Operators are legally responsible for ensuring that the geolocation and legality information is correct, regardless of the means or intermediaries they use to collect that information.

---

[5] Cite as: [FAQ 5.1 (part 2/2), p. 62]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are my obligations as an operator?
Similarity: 0.718
These measures need to be documented.
Policies, controls, measures and procedures to be used for risk mitigation are specified in more detail in Art. 11(1), (2) EUDR.
Operators sourcing commodities entirely from areas classified as low risk will be subject to simplified due diligence obligations.
According to Art. 13 EUDR, they will still need to collect information in line with Art. 9 and assess the complexity of the supply chain and the risk of circumvention and the risk of mixing the product with products of unknown origin or origin of standard or high risk countries, b ut they will not be required to assess and mitigate risks (Art. 10 and 11 EUDR) unless the operator obtains or is made aware of any relevant information, including substantiated concerns submitted under Art. 31, that would point to a risk that the relevant products do not comply with this Regulation (Art. 13(2) EUDR).
In the context of simplified due diligence and following the assessment under Art. 13(1) EUDR, the requirement under Art. 9(1)(g) EUDR to provide adequately conclusive and verifiable information that the relevant products are deforestation-free can be fulfilled by collecting the geolocation (or, in the case of MSPOs, the postal address) of plots of land (or establishments in the case of cattle).
For more information about due diligence more generally and information requirements under Art. 9(1)(h) EUDR, see Chapters 4 and 6 of the Commission Notice Guidance document.
```

</details>

## q29 (multi)

**Question:** Is cocoa butter covered by the EUDR, and can we mix compliant and unknown-origin cocoa butter in our tanks?

**Reference:** Yes, cocoa butter (1804) is in Annex I. No, mixing with unknown-origin material (mass balance) is not allowed; it must be segregated.

**Answer:**

The corpus does not cover this. An answer was drafted, but it could not be traced to the passages the search returned, so it was withheld. Check the cited sources or ask the competent authority.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.809
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[2] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.792
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;

---

[3] Cite as: [EUDR Annex I (part 6/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.772
acid oils from refining other than stearic acid, oleic acid and tall oil fatty acids, that have been synthesized using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 3823 70 00 Industrial fatty alcohols that have been synthesized using oil palm ex 3824 99 Other chemical products and preparations of the chemical or allied industries (including those consisting of mixtures of natural products), not elsewhere specified or included, that contain or have been made using oil palm (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC, Regulation (EC) No 726/2004 or Regulation (EU) 2019/6) (This provision shall apply from 30 December 2027) ex 3907 29 Other polyethers in primary forms, other than bis(polyoxyethylene) methylphosphonate, that have been made using oil palm (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC, Regulation (EC) No 726/2004 or Regulation (EU) 2019/6) (This provision shall apply from 30 December 2027)
Rubber (3) | ex 4001 Natural rubber, balata, gutta-percha, guayule, chicle and similar natural gums, in primary forms or in plates, sheets or strip ex 4005 Compounded rubber, unvulcanised, in primary forms or in plates, sheets or strip ex 4006 Unvulcanised rubber in other forms (e.g. rods, tubes and profile shapes) and articles (e.g. discs and rings) ex 4007 Vulcanised rubber thread and cord ex 4008 Plates, sheets, strips, rods and profile shapes, of vulcanised rubber other than hard rubber (not including used products and second-hand products) ex 4011 New pneumatic tyres, of rubber ex 4012 90 30 Tyre treads ex 4013 Inner tubes, of rubber ex 4015 Articles of apparel and clothing accessories (including gloves, mittens and mitts), for all purposes, of vulcanised rubber other than hard rubber (not including used products and second-hand products) ex 4017 Hard rubber (e.g. ebonite) in all forms including waste and scrap;

---

[4] Cite as: [EUDR Annex I (part 7/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.768
articles of hard rubber (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (not including used products and second-hand products)
Soya | 1201 90 00 Soya beans, whether or not broken: other 1208 10 Soya bean flour and meal 1507 Soya-bean oil and its fractions, whether or not refined, but not chemically modified 2304 Oilcake and other solid residues, whether or not ground or in the form of pellets, resulting from the extraction of soya-bean oil
Wood (4) | ex 4401 Fuel wood, in logs, in billets, in twigs, in faggots or in similar forms; wood in chips or particles; sawdust and wood waste and scrap, whether or not agglomerated in logs, briquettes, pellets or similar forms (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (not including single use packing material and packing containers used exclusively to support, protect or carry another product made available on the market or exported and presented with that product) ex 4402 Wood charcoal (including shell or nut charcoal), whether or not agglomerated ex 4403 Wood in the rough, whether or not stripped of bark or sapwood, or roughly squared (not including used products and second-hand products) ex 4404 Hoopwood; split poles; piles, pickets and stakes of wood, pointed but not sawn lengthwise; wooden sticks, roughly trimmed but not turned, bent or otherwise worked, suitable for the manufacture of walking sticks, umbrellas, tool handles or the like; chipwood and the like (not including used products and second-hand products) ex 4405 Wood wool;

---

[5] Cite as: [EUDR Annex I (part 3/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.767
(This provision shall apply from 30 December 2027) ex 2306 60 00 Oilcake and other solid residues of palm nuts or kernels, whether or not ground or in the form of pellets, resulting from the extraction of palm nut or kernel fats or oils ex 2905 16 Octanol (octyl alcohol) and isomers thereof, that have been synthesized using oil palm (This provision shall apply from 30 December 2027) ex 2905 17 00 Dodecan-1-ol (lauryl alcohol), hexadecan-1-ol (cetyl alcohol) and octadecan-1-ol (stearyl alcohol), that have been synthesized using oil palm (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC, Regulation (EC) No 726/2004 or Regulation (EU) 2019/6) (This provision shall apply from 30 December 2027) ex 2905 19 00 Other saturated monohydric alcohols, not elsewhere specified or included, that have synthesized using oil palm (This provision shall apply from 30 December 2027) ex 2905 45 Glycerol, with a purity of 95 % or more (calculated on the weight of the dry product), that has been synthesized using oil palm (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC, Regulation (EC) No 726/2004 or Regulation (EU) 2019/6) ex 2915 39 Esters of acetic acid, other than ethyl acetate, vinyl acetate, n-butyl acetate and dinoseb (ISO) acetate, that have been synthesized using oil palm (This provision shall apply from 30 December 2027) ex 2915 70 Palmitic acid, stearic acid, their salts and esters that have been synthesized using oil palm (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC, Regulation (EC) No 726/2004 or Regulation (EU) 2019/6) ex 2915 90 Saturated acyclic monocarboxylic acids, their anhydrides, halides, peroxides and peroxyacids; their halogenated, sulphonated, nitrated or nitrosated derivatives, other than formic acid, its salts and esters, acetic acid and its salts;

=====

[1] Cite as: [FAQ 1.17, p. 18]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How should the place of production of mixed goods be declared?
Similarity: 0.776
The operator needs to declare the place of production of all goods effectively shipped to the EU.
For example, if compliant goods from multiple places of production are mixed into the same silo, stack, pile, tank, etc., and then some of those goods are placed on the EU market:
• The place of production declared should include the place of production of all goods that entered the silo since it was last empty (and could therefore potentially be included in the shipment) • If the silos are not regularly emptied, the operator would need to declare the place of production of all goods that entered the silo during a period of time that ensures that commodities of unknown place of production are not mixed up in the process.
For instance, when downloading part of the goods stored in the silo, this could be safely done by declaring the geolocation of all previous goods that entered the silo up to a minimum of 200% of the silo capacity, provided that the silo works in first-in first-out system or an equivalent system that ensures the chronological exhaustion of raw materials in the order of their entry.
This approach applies to relevant commodities or products stored in stacks, tanks, etc. and all continuous processing.
• Other approaches are possible for first-in first-out as well as for other storage systems as long as it is ensured that commodities from an unknown place of production or which are incompliant with EUDR are not mixed up in the process.
• Declaring the place of production of x amount of goods that entered the silo, where x is the amount placed on the EU is not allowed under the R
[...]
```

</details>

## q30 (multi)

**Question:** We still hold cocoa beans imported before 30 December 2026. How do we prove that, and can we mix them with new compliant beans?

**Reference:** The customs declaration proves they were placed on the market before the date of application, and they can be mixed with compliant products if the Article 3 conditions are met and the evidence is kept.

**Answer:**

You can prove the beans were imported before 30 December 2026 by gathering adequately conclusive and verifiable evidence demonstrating they were placed on the EU market during the transitional period [FAQ 9.1, p. 85]. 

*(Note: This guidance reflects the Commission's view in the FAQ.)*

Yes, you can mix these transition-period beans with new compliant beans before placing them on the EU market, provided it can be proven that each batch within the mix was either placed on the EU market during the transition period or is fully compliant with the Regulation [FAQ 9.3, p. 87]. When mixing transition stocks with newer stocks, only the information relevant to the commodities newly placed on the market needs to be included in the due diligence statement, while the transition portion must remain accompanied by evidence of its pre-30 December 2026 status [FAQ 9.3, p. 87, FAQ 9.4, p. 88].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [FAQ 1.17, p. 18]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How should the place of production of mixed goods be declared?
Similarity: 0.658
The operator needs to declare the place of production of all goods effectively shipped to the EU.
For example, if compliant goods from multiple places of production are mixed into the same silo, stack, pile, tank, etc., and then some of those goods are placed on the EU market:
• The place of production declared should include the place of production of all goods that entered the silo since it was last empty (and could therefore potentially be included in the shipment) • If the silos are not regularly emptied, the operator would need to declare the place of production of all goods that entered the silo during a period of time that ensures that commodities of unknown place of production are not mixed up in the process.
For instance, when downloading part of the goods stored in the silo, this could be safely done by declaring the geolocation of all previous goods that entered the silo up to a minimum of 200% of the silo capacity, provided that the silo works in first-in first-out system or an equivalent system that ensures the chronological exhaustion of raw materials in the order of their entry.
This approach applies to relevant commodities or products stored in stacks, tanks, etc. and all continuous processing.
• Other approaches are possible for first-in first-out as well as for other storage systems as long as it is ensured that commodities from an unknown place of production or which are incompliant with EUDR are not mixed up in the process.
• Declaring the place of production of x amount of goods that entered the silo, where x is the amount placed on the EU is not allowed under the Regulation, as it would violate the prohibition under the Regulation of placing products of unknown origin on the Union market.
This is without prejudice to the transitional provisions as described in Chapter 9.

---

[2] Cite as: [FAQ 9.1 (part 2/3), p. 85]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are the obligations for downstream operators and traders when they place or make available on the EU market or export a relevant product which is made of a relevant product or a relevant commodity that was placed on the EU market during the transitional period (i.e., the period between the entry into force of the Regulation (29 June 2023) and
Similarity: 0.656
In this case, the obligations of the downstream operator and subsequent downstream operators and traders placing or making available on the EU market or exporting a derived product (chocolate), will be limited to gathering adequately conclusive and verifiable evidence to prove that the relevant derived product (cocoa butter) was placed on the EU market before the entry into application of the Regulation.
For parts of the final releva nt product that have been produced with other relevant products placed on the EU market from 30 December 2026, the downstream operator and subsequent downstream operators or traders will be subject to the standard obligations of the Regulation.
This is without prejudice to Art. 37(2), with regard to timber and timber products. 3.
An operator places on the EU market a relevant commodity or a product in the transitional period, which is then ‘made available’ on the market by one or more traders from 30 December 2026.
In this scenario, the obligations of the trader and subsequent downstream operators and traders will be limited to gathering adequately conclusive and verifiable evidence to prove that such relevant commodity, or relevant product, was placed on the EU market before the entry into application of the Regulation.
This is without prejudice to Art. 37(2) EUDR, with regard to timber and timber products.
Specifically for natural persons and micro and small (upstream) operators, which are subject to the deferred entry into application outlined in Art. 38(3) EUDR, the deferred entry into application for those operators, whether natural persons or micro - or small undertakings, limits the obligations of downstream operators and traders in those supply chains:
Example:
A downstream operator (company B) places on the EU market a product made of a relevant commodity which was placed on the EU market by a n operator that is a natural person or small or micro undertaking (person/company A) before 30 June 2027.

---

[3] Cite as: [FAQ 9.3, p. 87]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Can products placed on the EU market during the transition period be mixed with products that comply with the Regulation and which are placed on the EU market after the transition period if it can be proven that each batch within was either placed on the EU market during the transition period, or is compliant with the Regulation?
Similarity: 0.652
Provided that all conditions detailed in Art. 3(a) - (c) EUDR are fulfilled, products to be placed on the EU market from entry into application, and products placed on the EU market during the transition period (thus exempt), accompanied by evidence of having been placed on the EU market during the transition period, can be mixed together before being placed on the EU market.

---

[4] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.643
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;

---

[5] Cite as: [Guidance §9 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Composite products
Similarity: 0.641
Composite products may contain multiple relevant products under different commodities. For instance, a chocolate bar [HS 1806 ] may comprise derived products of cocoa (cocoa powder [HS 1805 ] and cocoa butter [HS 1804 ]) and oil palm (palm oil [HS 1511 ]). In such cases, the operator placing the product on the EU market or exporting from it will only be required to conduct due diligence on the relevant products listed under the commodity deemed relevant in Annex I of the EUDR. For instance, for chocolate bars [HS 1806 ], the relevant commodity linked to it is cocoa. This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

=====

[1] Cite as: [FAQ 9.3, p. 87]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Can products placed on the EU market during the transition period be mixed with products that comply with the Regulation and which are placed on the EU market after the transition period if it can be proven that each batch within was either placed on the EU market during the transition period, or is compliant with the Regulation?
Similarity: 0.803
Provided that all conditions detailed in Art. 3(a) - (c) EUDR are fulfilled, products to be placed on the EU market from entry into application, and products placed on the EU market during the transition period (thus exempt), accompanied by evidence of having been placed on the EU market during the transition period, can be mixed together before being placed on the EU market.

---

[2] Cite as: [FAQ 9.4, p. 88]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How will the mixing of commodities stocked during the transitional period with commodities to be placed on the EU market after 30 December 2026 work in practice, in particular in the Information System?
Similarity: 0.776
The due diligence statement has to be uploaded to the Information System only for the relevant products that are subject to the due diligence obligations under the Regulation.
If operators and traders mix commodities placed on the EU market during the transitional period wit h newer (post-transitional period) stocks, only the information relevant to commodities newly placed on the EU market should be part of the due diligence statement as this stock is subject to the due diligence exercise.
For “transition stocks”, see FAQ 9.3 above.

---

[3] Cite as: [FAQ 1.5, p. 14]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if part of a product is non-compliant?
Similarity: 0.749
If part of a relevant product is non-compliant, the non-compliant part needs to be identified and separated from the rest before the relevant product is placed on the EU market or exported, and that part may be neither placed on the EU market nor exported.
If identification and separation cannot be done, for instance because the non-compliant products have been mixed with the rest, then the whole relevant product is non-compliant as it cannot be guaranteed that the conditions of Art. 3 EUDR are met and therefore it may be neither placed on the EU market nor exported.
For instance, when bulk commodities have all been mixed and are linked to several hundred plots of land, the fact that one of the plots of land has been deforested after 2020 would make the whole relevant batch non-compliant.
A product would however not be non-compliant where 100% of relevant commodities or relevant products placed on the EU market 1) can be traced to the plot of land, 2) are legal and deforestation free within the meaning EUDR, and 3) at no point in time has been mixed with commodities of unknown origin or non-deforestation-free.

---

[4] Cite as: [FAQ 9.1 (part 3/3), p. 85]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What are the obligations for downstream operators and traders when they place or make available on the EU market or export a relevant product which is made of a relevant product or a relevant commodity that was placed on the EU m
[...]
```

</details>

## q31 (multi)

**Question:** As a medium-sized company, do we have to publish an annual report on our due diligence system?

**Reference:** No. The annual public report (Art. 12(3)) applies to operators that are not SMEs, and medium-sized undertakings count as SMEs under the EUDR.

**Answer:**

No, as a medium-sized enterprise, you do not have to publish an annual report on your due diligence system. 

Under Article 12(3) of the EUDR, the requirement to publicly report annually on the due diligence system applies only to operators who do not fall within the categories of SMEs (including medium enterprises) or microenterprises, or natural persons [EUDR Article 12(1)–(4)]. However, you must still establish, keep up to date, and review your due diligence system at least once a year [EUDR Article 12(1)–(2)].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 12(1)–(4)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Establishment and maintenance of due diligence systems, reporting and record keeping
Similarity: 0.71
1. In order to exercise due diligence in accordance with Article 8, operators shall establish and keep up to date a framework of procedures and measures to ensure that the relevant products they place on the market or export comply with Article 3 (‘due diligence system’).
2. Operators shall review the due diligence system at least once a year. Where operators become aware of new developments which could influence the due diligence system, they shall update the due diligence system to take account of those developments. Operators shall keep a record of such updates in their due diligence systems for five years.
3. Operators who do not fall within the categories of SMEs, including microenterprises, or natural persons shall, on an annual basis, publicly report as widely as possible, including via the internet, on their due diligence system, including on the steps taken by them to fulfil their obligations as set out in Article 8. Operators who fall also within the scope of other Union legal acts that lay down requirements regarding value chain due diligence may fulfil their reporting obligations under this paragraph by including the required information when reporting in the context of those other Union legal acts.
4. Without prejudice to Union data protection legislation, the reporting as referred to in paragraph 3 shall include the following information concerning relevant commodities and relevant products: (a) a summary of the information referred to in Article 9(1), points (a), (b) and (c); (b) the conclusions of the risk assessment carried out pursuant to Article 10 and measures undertaken pursuant to Article 11 and a description of the information and evidence obtained and used to assess the risk; (c) where applicable, a description of the process of consultation of indigenous peoples, local communities and other customary tenure rights holders or of the civil society organisations that are present in the area of production of the relevant commodities and relevant products.

---

[2] Cite as: [Guidance §8 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Regular maintenance of a due diligence system
Similarity: 0.69
Relevant legislation: EUDR – Article 12 – Establishment and maintenance of due diligence systems, reporting and record keeping
To exercise due diligence in accordance with Article 8, operators, including micro or small primary operators, must establish and keep up to date a framework of documenting, analysing, verifying and reporting procedures and measures (‘due diligence system’). The aim of due diligence under the EUDR is to achieve a required outcome by evidencing consistent processes in businesses operations. It is important that in accordance with Article 12(2) an operator shall review its due diligence system at least once a year to ensure that those responsible are following the procedures that apply to them, the processes in place are effective and the required outcome is being achieved. Operators should also update the due diligence system if during the review or at any other point they become aware of new developments which could influence the aims of the due diligence system, such as the effectiveness and comprehensiveness of steps or procedures within the system. Any updates to the due diligence system must be recorded and records kept for 5 years.
The review can be carried out by someone within the organisation of the operator (should be independent from those carrying out the procedures) or by an external body. It should identify any weaknesses and failures and the operator’s management should set deadlines for addressing them.
In the case of a relevant product due diligence system, the review should for example check if there are documented procedures:
— | For collecting and recording the information, data and documents necessary to demonstrate compliance.
— | For assessing the risk of the relevant product or any component of the relevant product containing relevant products or relevant commodities that are not deforestation-free or have not been produced in accordance with the relevant legislation of the country of production.
— | Describing proposed actions to take according to the level of risk.

---

[3] Cite as: [FAQ 5.14, p. 68]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | When will non-SME operators have to produce their first annual reports pursuant to Art. 12(3) EUDR?
Similarity: 0.677
The EUDR will be enforceable from 30 December 2026 (except for most micro and small operators, where the date is 30 June 2027).
Art. 12(3) requires relevant companies to publish an annual report about their activities to comply with requirements under the EUDR.
As 2027 will be the first year for which the EUDR applies, the first report (covering the year 2027) will have to be published after 30 December 2027.
Companies which have already reported relevant elements covered in Art. 12(3) EUDR in the context of their reporting obligations under other EU relevant legislation (such as the EU Corporate Sustainability Due Diligence Directive (CSDDD)7 or the Corporate Sustainability Reporting Directive (CSRD)) do not have to repeat the reporting.

---

[4] Cite as: [Guidance §4 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Due diligence
Similarity: 0.676
Relevant legislation: EUDR – Article 2(26) – Definitions; Article 4, 4a and 5 – Obligations of operators, downstream operators and traders; Article 8 – Due diligence; Article 9 – Information requirements; Article 10 – Risk assessment
According to Article 4(1), all operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, shall exercise due diligence in accordance with Article 8 prior to placing relevant products on the market or exporting them in order to prove that the relevant products comply with Article 3. In order to do so, and in accordance with Article 12(1), operators shall establish and keep up to date a framework of procedures and measures – a ‘due diligence system’.
The due diligence requirements set out in Article 8 require operators to:
— | collect information, documents and, where relevant, data from each supplier about the relevant products which are subject to the EUDR (listed in Annex I) pursuant to Article 8 and 9,
— | verify and analyse that information along with other contextual information and on that basis carry out a risk assessment pursuant to Article 10, and
— | adopt risk mitigation measures pursuant to Article 11, unless the risk assessment carried out in accordance with Article 10 concludes that there is no or only negligible risk that the relevant products are non-compliant.
Operators are responsible for a thorough examination and analysis of their own business activities, which requires the collection of information, data and documents needed to fulfil the information requirements of Article 9, analysing it as part of the risk assessment (Article 10), and adopt risk mitigation measures (Article 11) as necessary, unless the risk of non-compliance is assessed as being negligible.
All operators, including micro or small primary operators and operators benefitting from simplified due diligence in line with Article 13, are obliged to fulfil the information requirements set out in Article 9.

---

[5] Cite as: [FAQ 5.16, p. 68]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Will there be a set of pre-determined format or list of questions to perform due diligence?
Similarity: 0.659
No.
Operators must comply with their due diligence obligations in accordance with Art. 8, 9, 10 and 11 EUDR.
Achieving no or negligible risk is a pre-requisite for placing/ exporting relevant products on/from the EU market.
Please note that due diligence is not a “tick-the-box exercise”.
Hence, it may depend on the specific context and supply chain, provided that the different steps of due diligence as described in the Regulation (i.e. information requirement, risk assessment and risk mitigation, in line with Art. 9, 10 and 11 EUDR, unless Art. 13 EUDR applies) are covered.
```

</details>

## q32 (multi)

**Question:** How long must we keep our due diligence records, and can we export our statements from the Information System?

**Reference:** Five years; users can export a DDS to PDF and its geolocation coordinates to a separate file for their own records.

**Answer:**

You must keep all due diligence documentation, records, measures, updates, and due diligence statements for **at least five years** from the date of placing on the market, exporting, or submission [EUDR Article 12(5), FAQ 5.8, p. 66]. 

Yes, you can export your statements from the Information System: users can export the contents of a due diligence statement into a PDF file and extract geolocation coordinates into a separate file for internal record-keeping [FAQ 7.14, p. 80]. 

*(Note: Details regarding data storage durations in the Information System and the export functionality are drawn from the Commission FAQ, which reflects the Commission's views and is not legally binding [FAQ 7.14, p. 80].)*

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 12(5)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Establishment and maintenance of due diligence systems, reporting and record keeping
Similarity: 0.783
5. Operators shall keep for at least five years all documentation related to due diligence, such as all records, measures and procedures pursuant to Article 8. They shall make that documentation available to the competent authorities upon request.

---

[2] Cite as: [FAQ 5.8, p. 66]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How long should documentation be kept?
Similarity: 0.779
How long should the operator keep the documentation used for the due diligence exercise? Do operators, downstream operators and traders have to keep the relevant information about the relevant products they place or make available on the EU market or export? What is considered as the beginning of this duration? (UPDATED) Operators should collect, organise, and keep for five years from the date of the placing on the EU market or export of the relevant commodities and relevant products the information gathered based on Art. 9 EUDR, accompanied by evidence.
Based on the provisions of Art. 10(4) and Art. 11(3) EUDR, operators should be able to demonstrate how due diligence was carried out and what mitigation measures were put in place in case risk was identified.
Relevant documentation about these measures must be saved for at least five years after the due diligence exercise was carried out.
Operators must also keep record of the due diligence statements for five years from the date when the statement is submitted in the Information System, which is prior to the date of placing the product on the EU market or exporting it.
Downstream operators and traders must keep the information listed in Art. 5(3) EUDR for at least five years, including the due diligence reference number(s) or declaration identifier(s) if their supplier is an operator, from the date of the placing, making available on the EU market or exporting of relevant products.

---

[3] Cite as: [FAQ 7.14, p. 80]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How long will be data of the DDS be saved in the Information system? Is it necessary to export and save data for purpose of archiving?
Similarity: 0.777
The storage of personal data is limited in time by the Commission Implementing Regulation on the functioning of the Information System.
Th e foreseen storage period can be further extended on the individual request of the Information system users or relevant authorities if this is necessary to comply with their responsibilities and obligations under the EUDR.
In line with this, data that does not constitute personal data, as defined, is also stored and accessible in the Information System for the same amount of time.
Users of the information system have the option to export the contents of a DDS into a PDF file, as well as extract geolocation coordinates into a separate file to support their internal record-keeping purposes.

---

[4] Cite as: [EUDR Article 12(1)–(4)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Establishment and maintenance of due diligence systems, reporting and record keeping
Similarity: 0.766
1. In order to exercise due diligence in accordance with Article 8, operators shall establish and keep up to date a framework of procedures and measures to ensure that the relevant products they place on the market or export comply with Article 3 (‘due diligence system’).
2. Operators shall review the due diligence system at least once a year. Where operators become aware of new developments which could influence the due diligence system, they shall update the due diligence system to take account of those developments. Operators shall keep a record of such updates in their due diligence systems for five years.
3. Operators who do not fall within the categories of SMEs, including microenterprises, or natural persons shall, on an annual basis, publicly report as widely as possible, including via the internet, on their due diligence system, including on the steps taken by them to fulfil their obligations as set out in Article 8. Operators who fall also within the scope of other Union legal acts that lay down requirements regarding value chain due diligence may fulfil their reporting obligations under this paragraph by including the required information when reporting in the context of those other Union legal acts.
4. Without prejudice to Union data protection legislation, the reporting as referred to in paragraph 3 shall include the following information concerning relevant commodities and relevant products: (a) a summary of the information referred to in Article 9(1), points (a), (b) and (c); (b) the conclusions of the risk assessment carried out pursuant to Article 10 and measures undertaken pursuant to Article 11 and a description of the information and evidence obtained and used to assess the risk; (c) where applicable, a description of the process of consultation of indigenous peoples, local communities and other customary tenure rights holders or of the civil society organisations that are present in the area of production of the relevant commodities and relevant products.

---

[5] Cite as: [Guidance §8 (part 1/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Regular maintenance of a due diligence system
Similarity: 0.754
Relevant legislation: EUDR – Article 12 – Establishment and maintenance of due diligence systems, reporting and record keeping
To exercise due diligence in accordance with Article 8, operators, including micro or small primary operators, must establish and keep up to date a framework of documenting, analysing, verifying and reporting procedures and measures (‘due diligence system’). The aim of due diligence under the EUDR is to achieve a required outcome by evidencing consistent processes in businesses operations. It is important that in accordance with Article 12(2) an operator shall review its due diligence system at least once a year to ensure that those responsible are following the procedures that apply to them, the processes in place are effective and the required outcome is being achieved. Operators should also update the due diligence system if during the review or at any other point they become aware of new developments which could influence the aims of the due diligence system, such as the effectiveness and comprehensiveness of steps or procedures within the system. Any updates to the due diligence system must be recorded and records kept for 5 years.
The review can be carried out by someone within the organisation of the operator (should be independent from those carrying out the procedures) or by an external body. It should identify any weaknesses and failures and the operator’s management should set deadlines for addressing them.
In the case of a relevant product due diligence system, the review should for example check if there are documented procedures:
— | For collecting and recording the information, data and documents necessary to demonstrate compliance.
— | For assessing the risk of the relevant product or any component of the relevant product containing relevant products or relevant commodities that are not deforestation-free or have not been produced in accordance with the relevant legislation of the country of production.
— | Describing proposed actions to take according to the level of risk.
```

</details>

## q33 (unanswerable)

**Question:** Is Ghana classified as a low-risk country under the EUDR?

**Reference:** The corpus does not contain the country classification list; the assistant should say it cannot answer from the documents (the list is in Implementing Regulation (EU) 2025/1093).

**Answer:**

The corpus does not cover whether Ghana is classified as a low-risk country; please consult the latest implementing acts published by the European Commission or check with your national competent authority. All countries were initially assigned a standard level of risk on 29 June 2023 [EUDR Article 29(2)].

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 29(1)–(3)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Assessment of countries
Similarity: 0.797
1. This Regulation establishes a three-tier system for the assessment of countries or parts thereof. For that purpose, Member States and third countries, or parts thereof, shall be classified into one of the following risk categories: (a) ‘high risk’ refers to countries or parts thereof, for which the assessment referred to in paragraph 3 results in the identification of a high risk of producing in such countries or in parts thereof, relevant commodities for which the relevant products do not comply with Article 3, point (a); (b) ‘low risk’ refers to countries or parts thereof, for which the assessment referred to in paragraph 3 concludes that there is sufficient assurance that instances of producing in such countries or in parts thereof, relevant commodities for which the relevant products do not comply with Article 3, point (a), are exceptional; (c) ‘standard risk’ refers to countries or parts thereof which do not fall in either the category ‘high risk’ or the category ‘low risk’.
2. On 29 June 2023, all countries shall be assigned a standard level of risk. The Commission shall classify countries or parts thereof, that present a low or high risk in accordance with paragraph 1 of this Article. The list of the countries or parts thereof, that present a low or high risk shall be published by means of implementing acts to be adopted in accordance with the examination procedure referred to in Article 36(2), no later than 30 June 2025. That list shall be reviewed, and updated if appropriate, as often as necessary in light of new evidence.
3. The classification of low-risk and high-risk countries or parts thereof, pursuant to paragraph 1 shall be based on an objective and transparent assessment by the Commission, taking into account the latest scientific evidence and internationally recognised sources. The classification shall be based primarily on the following assessment criteria: (a) rate of deforestation and forest degradation; (b) rate of expansion of agriculture land for relevant commodities; (c) production trends of relevant commodities and of relevant products.

---

[2] Cite as: [FAQ 5.11, p. 67]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Could certain commodities from a given country be considered ‘negligible risk’?
Similarity: 0.758
Could palm oil, rubber, coffee, cacao, or timber from a given country be considered ‘negligible risk’? No.
See question above.

---

[3] Cite as: [FAQ 6.5, p. 73]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Will legality risks be considered?
Similarity: 0.757
Will the benchmarking take into account legality risks as well as deforestation and forest degradation? How will the legislation and forest policies of producer countries, particularly regarding 'legal deforestation', be assessed/taken into account during the benchmarking process? The list of criteria for benchmarking is set out in Art. 29 EUDR.
The assessment of the Commission will be based on an objective and transparent assessment analysis, based on the criteria defined in Art. 29(3) and 29(4) EUDR.
The relevant quantitative criteria are:
(a) the rate of deforestation and forest degradation, (b) the rate of expansion of agriculture land for relevant commodities, and (c) production trends of relevant commodities and of relevant products.
As envisaged in the Regulation, the assessment may also take into account other criteria including (a) information supplied by governments and third parties (NGOs, industry);
(b) agreements and other instruments between the country concerned and the Union and/or its Member States that address deforestation and forest degradation;
(c) the existence of national laws to fight deforestation and forest degradation and their enforcement;
(d) the availability of transparent data in the country;
(e) if applicable, the existence, compliance with, or effective enforcement of laws protecting the rights of indigen ous peoples;
(and (g) international sanctions imposed by the UN Security Council or the Council of the European Union on imports or exports of the relevant commodities and relevant products; etc.

---

[4] Cite as: [Guidance §4(e)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Simplified due diligence, i.e. sourcing from low-risk countries
Similarity: 0.753
Operators sourcing from low-risk countries are required to exercise due diligence in line with Article 8, fulfil information requirements of Article 9 and establish a due diligence system in line with Article 12.
However, in accordance with Article 13, they are not required to fulfil the obligations under Article 10 and Article 11 where, after having assessed:
(i) | the complexity of the relevant supply chain; and
(ii) | the risk of circumvention or mixing with products of unknown origin, or origin in high-risk or standard-risk countries or parts thereof, they have ascertained that all relevant commodities and products they place on the market or export have been produced exclusively in such countries or parts thereof that were classified as low risk in accordance with Article 29 ().
For simplified due diligence under Article 13, no further steps of assessing the information or mitigating risk are required unless, in the course of information collection or in the course of the assessment required by Article 13 itself, operators are made aware of relevant new information indicating that a relevant product that they intend to place on the market or export is at risk of not complying with the Regulation.
Micro or small primary operators are, generally, not required to carry out risk assessment and risk mitigation as they are by definition an operator sourcing from low-risk country, unless they obtain or are made aware of any relevant information pointing to a non-negligible risk that the relevant products are non-compliant.

---

[5] Cite as: [FAQ 6.1, p. 72]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is country benchmarking?
Similarity: 0.752
The benchmarking system operated by the Commission classifies countries, or parts thereof, in three categories (high, standard and low risk) according to the level of risk of producing commodities that are not deforestation-free in such countries.
The criteria for the identification of the risk status of countries or parts thereof are defined in Art. 29 EUDR.
Art. 29(2) EUDR mandates the Commission to develop a system and publish the list of countries, or parts thereof, that present a low or high risk.
It is based on an objective and transparent assessment analysis of quantitative and qualitative criteria, taking into account the latest scientific evidence, internationally recognised sources, and information verified on the ground.
```

</details>

## q34 (unanswerable)

**Question:** How much is the fine in Italy for a first EUDR infringement?

**Reference:** The corpus does not give national fine levels; Member States set penalties and the documents only give the EU minimum for the maximum fine. The assistant should say it does not know the Italian amount.

**Answer:**

The corpus does not cover this. The specific fine amounts for a first infringement in Italy are determined by national legislation rather than the EU Regulation or Commission FAQ, which only require Member States to set effective, proportionate, and dissuasive penalties (such as a maximum fine of at least 4% of annual Union-wide turnover for legal persons). You should check Italian national law or consult the Italian competent authority or legal counsel for the exact schedule of fines.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 25(1)–(2)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Penalties
Similarity: 0.77
1. Without prejudice to the obligations of Member States under Directive 2008/99/EC of the European Parliament and of the Council (5), Member States shall lay down rules on penalties applicable to infringements of this Regulation by operators, downstream operators and traders and shall take all measures necessary to ensure that they are implemented. Member States shall notify the Commission of those rules and of those measures and shall notify it, without delay, of any subsequent amendments affecting them.
2. The penalties provided for in paragraph 1 shall be effective, proportionate and dissuasive. Those penalties shall include: (a) fines proportionate to the environmental damage and the value of the relevant commodities or relevant products concerned, calculating the level of such fines in such way as to ensure that they effectively deprive those responsible of the economic benefits derived from their infringements, and gradually increasing the level of such fines for repeated infringements; in the case of a legal person, the maximum amount of such a fine shall be at least 4 % of the operator’s, downstream operator’s or trader’s total annual Union-wide turnover in the financial year preceding the fining decision, calculated in accordance with the calculation of aggregate turnover for undertakings laid down in Article 5(1) of Council Regulation (EC) No 139/2004 (6), and shall be increased, where necessary, to exceed the potential economic benefit gained; (b) confiscation of the relevant products concerned from the operator, downstream operator and/or trader; (c) confiscation of revenues gained by the operator, downstream operator and/or trader from a transaction with the relevant products concerned; (d) temporary exclusion for a maximum period of 12 months from public procurement processes and from access to public funding, including tendering procedures, grants and concessions; (e) temporary prohibition from placing or making available on the market or exporting relevant commodities and relevant products, in the event of a serious infringement or of repeated infringements; (f) prohibition from exercising the simplified due diligence set out in Article 13 in the event of a serious infringement or of repeated infringements.

---

[2] Cite as: [FAQ 10.1, p. 94]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What does it mean that the penalties laid down by the EU Member States are without prejudice to the obligations of Member States under Directive 2008/99/EC of the European Parliament and of the Council?
Similarity: 0.754
The EU Member States must lay down the national framework of penalties, which should include at least the penalties listed in Art. 25(2) EUDR and must take all measures necessary to ensure that the rules are implemented.
The level and type of penalties cannot be in contradiction with the Environmental Crime Directive.
The provisions of the Directive are subject to the succession of law.

---

[3] Cite as: [FAQ 10.2, p. 94]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is the maximum level of fine?
Similarity: 0.745
Member States have the discretion to define the penalties, including the level of fine.
For legal persons the maximum level of the penalty cannot be lower than 4 % of the operator’s, downstream operator’s or trader’s total annual Union-wide turnover in the financial year preceding the fining decision, calculated in accordance with the calculation of aggregate turnover for undertakings laid down in Art. 5(1) of Council Regulation (EC) No 139/2004.
The level of fine should increase where necessary, particularly in case of repeated infringements.
The penalties should ensure that they effectively deprive those responsible of the economic benefits derived from their infringements, in accordance with the effective, proportionate, and dissuasive principle.

---

[4] Cite as: [EUDR Article 25(3)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Penalties
Similarity: 0.738
3. Member States shall notify the Commission of final judgments against legal persons for infringements of this Regulation and the penalties imposed on them, within 30 days from the date on which the judgments become final, taking into account the relevant data protection rules. The Commission shall publish on its website a list of such judgments, which shall contain the following elements: (a) the name of the legal person; (b) the date of the final judgment; (c) a summary of the activities for which the legal person was found to have infringed this Regulation; and (d) the nature and, where financial, the amount of the penalty imposed.

---

[5] Cite as: [EUDR Article 24]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Corrective action in the event of non-compliance
Similarity: 0.737
1. Without prejudice to Article 25, where competent authorities establish that an operator, downstream operator or trader has not complied with this Regulation or that a relevant product placed or made available on the market or exported is non-compliant, they shall without delay require the operator, downstream operator or trader to take appropriate and proportionate corrective action to bring the non-compliance to an end within a specified and reasonable period of time.
2. For the purposes of paragraph 1, the corrective action required to be taken by the operator, downstream operator or trader shall include at least one of the following, as applicable: (a) rectifying any formal non-compliance, in particular with the requirements of Chapter 2; (b) preventing the relevant product from being placed or made available on the market or exported; (c) withdrawing or recalling the relevant product immediately; (d) donating the relevant product to charitable or public interest purposes or, if that is not possible, disposing of it in accordance with Union law on waste management.
3. Irrespective of the corrective action taken under paragraph 2, the operator, downstream operator or trader shall address any shortcomings in the due diligence system with a view to preventing the risk of further non-compliance with this Regulation.
4. If the operator, downstream operator or trader fails to take corrective action as referred to in paragraph 2 within the period of time specified by the competent authority under paragraph 1, or where non-compliance as referred to in paragraph 1 persists, after that period of time competent authorities shall secure application of the required corrective action referred to in paragraph 2 by all means available to them under the law of the Member State concerned.
```

</details>

## q35 (unanswerable)

**Question:** Which authority checks EUDR compliance in the Netherlands?

**Reference:** The corpus does not name national competent authorities; the assistant should say it cannot answer.

**Answer:**

The corpus does not cover this. The specific name of the Dutch competent authority designated under Article 14 of the Regulation is not contained in the corpus; you should check the European Commission's official list of competent authorities online or consult the Dutch national authorities.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Article 14]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Competent authorities
Similarity: 0.776
1. Member States shall designate one or more competent authorities responsible for fulfilling the obligations arising from this Regulation.
2. By 30 December 2023 at the latest, Member States shall inform the Commission of the names, addresses and contact details of the competent authorities referred to in paragraph 1. Member States shall inform the Commission without undue delay of any changes to that information.
3. The Commission shall make the list of the competent authorities publicly available on its website without undue delay. The Commission shall regularly update the list, based on updates received from Member States.
4. Member States shall ensure that the competent authorities have adequate powers, functional independence and the resources to fulfil the obligations set out in this Chapter.

---

[2] Cite as: [EUDR Article 33(1)–(2)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Information system
Similarity: 0.752
1. By 30 December 2024, the Commission shall establish and subsequently shall maintain an information system which shall contain the due diligence statements made available pursuant to Article 4(2).
2. Without prejudice to the fulfilment of obligations established in Chapters 2 and 3, the information system shall provide at least the following functionalities: (a) registration of operators and traders and their authorised representatives in the Union; for operators placing relevant products under the customs procedure ‘release for free circulation’ or ‘export’, the Economic Operators Registration and Identification (EORI) number established pursuant to Article 9 of Regulation (EU) No 952/2013, shall be included in their registration profile; (aa) registration of non-SME downstream operators and non-SME traders in accordance with Article 5(2); (b) registration of due diligence statements including the communication to the operator concerned of a reference number for each due diligence statement submitted through the information system; (c) registration of simplified declarations submitted by micro or small primary operators and assignment of a declaration identifier to the operator concerned; (d) where possible, the conversion of data from relevant systems to identify the geolocation; (e) registration of the outcome of checks on due diligence statements; (f) interconnection with customs through the European Union Single Window Environment for Customs, in accordance with Article 28, including to allow the notifications and requests referred to in Article 26(6) to (9); (g) provision of relevant information to support the risk-profiling for the plan of checks referred to in Article 16(5), including results of checks, the risk-profiling of operators, downstream operators, traders and relevant commodities and relevant products for the purpose of identifying, based on electronic data-processing techniques, operators, downstream operators and traders to be checked as referred to in Article 16(5), and relevant products to be checked by competent authorities; (h) facilitation of administrative assistance and cooperation between competent authorities, and between competent authorities and the Commission, to exchange information and data; (i) support communication between competent authorities and operators, downstream operators and traders for the purposes of implementation of this Regulation, including, where appropriate, through the use of digital supply management tools.

---

[3] Cite as: [FAQ 1.20, p. 20]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How will the Competent Authorities of the EU Member States check the validity of a no-deforestation claim?
Similarity: 0.752
The EU Member States’ Competent Authorities carry out checks in accordance with Art. 16 EUDR to establish that the relevant commodities and products that have been or are intended to be placed on or made available on the EU market or exported, come from deforestation - free plots of land and were produced legally.
This includes conducting checks on the validity of the due diligence statements, and the overall compliance of the operators, downstream operators and traders with the provisions of the Regulation.
For more information on the scope of checks by Competent Authorities, please refer to Arts. 18 and 19 EUDR.

---

[4] Cite as: [FAQ 1.22, p. 20]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Will Competent Authorities use the definitions in the Regulation?
Similarity: 0.75
In the context of the implementation of this Regulation, Competent Authorities of EU Member States will use the definitions set out in Art. 2 EUDR.
A Regulation is a binding legislative act in the EU.
It must be applied in a harmonized manner in its entirety in the 27 EU Member States.

---

[5] Cite as: [FAQ 5.2.1, p. 64]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What is an authorised representative? Can one authorised representative represent multiple operators? Which EUDR obligations can an authorised representative perform?
Similarity: 0.747
(UPDATED) An authorised representative is a natural or legal person that acts on behalf of an operator by submitting a due diligence statement or a simplified declaration for them (Art. 6 EUDR).
According to Art. 2(22) EUDR, an authorised representative must be established in the Union and must receive a written mandate from an operator in order to act on their behalf.
In principle, any natural or legal person (private or public) established in the EU can act as authorised representative, no matter whether they actively participate in a supply chain or not.
An authorised representative can be, for example, a cooperation or association (see FAQs 3.20 and 3.22), a national or regional authority which is not an EUDR competent authority or a member of the supply chain.
When submitting DDS or SD, authorised representatives must register in the Information System and choose the role ‘Representing Operator’.
Th is role allow s authorised representatives to be authenticated with their own credentials and submit due diligence statements or simplified declarations on behalf of their clients.
It is possible for an authorised representative to be mandated by multiple operators if the above-mentioned requirements are met.
The details of the operator shall be introduced in the fields when submitting a DDS or a SD allowing unique identification of the represented operator.
Even if an authorised representative submits a due diligence statement or a simplified declaration, the obligation to exercise due diligence remains with the operator.
Accordingly, the operator retains responsibility for compliance of relevant products with Art. 3 EUDR.
In the case of an operator being a natural person or a microenterprise, they may mandate the next operator or trader further down the supply chain that is not a natural person or a microenterprise to act as an authorised representative, see Art. 6(3) EUDR.

=====

[1] Cite as: [EUDR Article 14]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Competent authorities
Similarity: 0.812
1. Member States shall designate one or more competent authorities responsible for fulfilling the obligations arising from this Regulation.
2. By 30 December 2023 at the latest, Member States shall inform the Commission of the names, addresses and contact details of the competent authorities referred to in paragraph 1. Member States shall inform the Commission without undue delay of any changes to that information.
3. The Commission shall make the list of the competent authorities publicly available on its website without undue delay. The Commission shall regularly update the list, based on updates received from Member States.
4. Member States shall ensure that the competent authorities have adequate powers, functional independence and the resources to fulfil the obligations set out in this Chapter.

---

[2] Cite as: [FAQ 1.20, p. 20]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How will the Competent Authorities of the EU Member States check the validity of a no-deforestation claim?
Similarity: 0.782
The EU Member States’ Competent Authorities carry out checks in accordance with Art. 16 EUDR to establish that the relevant commodities and products that have been or are intended to be placed on or made available on the EU market or exported, come from deforestation - free plots of land and were produced legally.
This includes conducting checks on the validity of the due diligence statements, and the overall compliance of the operators, downstream operators and traders with the provisions of the Regulation.
For more information on the scope of checks by Competent Authorities, please refer to Arts. 18 and 19 EUDR.

---

[3] Cite as: [FAQ 1.22, p. 20]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Will Competent Authorities use the definitions in the Regulation?
Similarity: 0.779
In the context of the implementation of this Regulation, Competent Authorities of EU Member States will use the definitions set out in Art. 2 EUDR.
A Regulation is a binding legislative act in the EU.
It must be applied in a harmonized manner in its entirety in the 27 EU Member States.

---

[4] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.776
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[5] Cite as: [EUDR Article 33(1)–(2)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Information system
Similarity: 0.773
1. By 30 December 2024, the Commission shall establish and subsequently shall maintain an information system which shall contain the due diligence statements made available pursuant to Article 4(2).
2. Without prejudice to the fulfilment of obligations established in Chapters 2 and 3, the information system shall provide at least the following functionalities: (a) registration of operators and traders and their authorised representatives in the Union; for operators placing relevant products under the customs procedure ‘release for free circulation’ or ‘export’, the Ec
[...]
```

</details>

## q36 (unanswerable)

**Question:** Does the EUDR require us to pay the Living Income Differential on Ivorian cocoa?

**Reference:** The corpus does not mention the Living Income Differential; the assistant should say the documents do not cover it.

**Answer:**

The corpus does not cover this. 

The provided EUDR corpus contains no mentions of the Living Income Differential (LID) or pricing mechanisms for Ivorian cocoa; you should consult national competent authorities, trade legal counsel, or relevant Commission updates regarding pricing policies.

<details><summary>Retrieved passages</summary>

```
Error executing tool search: 1 validation error for searchArguments
query
  Field required [type=missing, input_value={'queries': ['Living Inco...ome Differential EUDR']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing

=====

[1] Cite as: [FAQ 1.1 (part 1/2), p. 12]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Why and how must operators collect coordinates?
Similarity: 0.582
The Regulation requires operators placing covered products on the EU market or exporting them to collect geographic coordinates of the plots of land where the commodities were produced.
This does not apply to downstream operators who place on the market or export such products (for more information on downstream operators, see Chapter 3 of this document).
Traceability to the plot of land (i.e., the requirement to collect the geographic coordinates of the plots of land where the commodities were produced) is necessary to demonstrate that there has been no deforestation at the specific location of production.
Geographic information linking products to the plot of land is already used by part of the industry and a number of certification organisations.
Remotely sensed information (air photos, satellite images) or other information (e.g., photograph in the field with linked geotags and time stamps) may be used for verifying if the geolocation of declared commodities and products is linked to deforestation.
The geolocation coordinates need to be provided in the due diligence statements (hereinafter referred to as “ due diligence statement” or “ DDS”) or, where applicable, in the simplified declarations (hereinafter referred to as “simplified declaration” or “SD”) that operators are required to submit to the Information System ahead of the placing on the EU market or export from the EU of the products.
It is therefore a core part of the Regulation, which prohibits the placing on the EU market, or the export, of any product covered by the Regulation’s scope whose geolocation coordinates have not yet been collected and submitted as part of a due diligence statement.
The only exception is the SD of micro or small primary operators (MSPO), for whom the geolocation may be replaced by a postal address, provided that the postal address clearly corresponds to the geographic location of the plots of land or establishment concerned (see FAQ 3.28 for more details).
Collecting the geolocation coordinates of a plot of land can be done via mobile phones, handheld Global Navigation Satellite System (GNSS) devices and widespread and free-to-use digital applications (e.g.
Geographic Information Systems (GIS)).

---

[2] Cite as: [FAQ 1.4, p. 14]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Are mass balance chains of custody allowed?
Similarity: 0.579
The Regulation requires that the commodities used for all products falling under the scope be traceable to the plot of land.
Mass balance chains of custody that allow for the mixing, at any step of the supply chain, of deforestation-free commodities with commodities of unknown origin or non-deforestation- free commodities are not allowed under the Regulation, because they do not guarantee that the commodities placed on the EU market, or exported, are deforestation-free.
Therefore, the commodities placed on the EU market, or exported, need to be segregated from commodities of unknown origin or from non-deforestation-free commodities at every step of the supply chain.
As mass balance is therefore to be ruled out, full identity preservation is not needed.

---

[3] Cite as: [FAQ 1.17, p. 18]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How should the place of production of mixed goods be declared?
Similarity: 0.578
The operator needs to declare the place of production of all goods effectively shipped to the EU.
For example, if compliant goods from multiple places of production are mixed into the same silo, stack, pile, tank, etc., and then some of those goods are placed on the EU market:
• The place of production declared should include the place of production of all goods that entered the silo since it was last empty (and could therefore potentially be included in the shipment) • If the silos are not regularly emptied, the operator would need to declare the place of production of all goods that entered the silo during a period of time that ensures that commodities of unknown place of production are not mixed up in the process.
For instance, when downloading part of the goods stored in the silo, this could be safely done by declaring the geolocation of all previous goods that entered the silo up to a minimum of 200% of the silo capacity, provided that the silo works in first-in first-out system or an equivalent system that ensures the chronological exhaustion of raw materials in the order of their entry.
This approach applies to relevant commodities or products stored in stacks, tanks, etc. and all continuous processing.
• Other approaches are possible for first-in first-out as well as for other storage systems as long as it is ensured that commodities from an unknown place of production or which are incompliant with EUDR are not mixed up in the process.
• Declaring the place of production of x amount of goods that entered the silo, where x is the amount placed on the EU is not allowed under the Regulation, as it would violate the prohibition under the Regulation of placing products of unknown origin on the Union market.
This is without prejudice to the transitional provisions as described in Chapter 9.

---

[4] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.575
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;

---

[5] Cite as: [FAQ 1.10, p. 15]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What if property registers or titles are unavailable?
Similarity: 0.575
How can operators obtain geolocation data in countries where property registers are incomplete and where farmers may lack IDs or titles over their land? (UPDATED) Farmers can collect the geolocation of their plots of land regardless of whether they are entered or not in a land registry or the lack of IDs or titles over their land.
Unless they are direct suppliers of the operators or operators themselves, no personal information is required from the farmers and the geolocation of the plot used to supply commodities for placing on the EU market is sufficient.
As regards the legality requirement in relation to land use right (Art. 2(40) (a) EUDR) the Regulation requires compliance with relevant national laws.
If farmers are legally allowed to sell their product under national laws (which might lack a property register and where some farmers might lack IDs), then that would also mean that operators would meet the legality requirement when sourcing from those farmers.
If possession of a land title is not required under domestic law to produce and commercialise agricultural products, then it is not required under the Regulation.
Operators, nonetheless, would need to verify that there is no risk of illegality in their supply chains, meaning that relevant laws applicable in the country of production are complied with.
There are many different means that operators already use today to collect the legality (and geolocation) information: some resort to mapping directly their suppliers, while others rely on intermediaries like cooperatives, certification bodies, national traceability systems or other companies.
Operators are legally responsible for ensuring that the geolocation and legality information is correct, regardless of the means or intermediaries they use to collect that information.
```

</details>

## q37 (unanswerable)

**Question:** How much will EUDR compliance add to the price of a tonne of cocoa beans?

**Reference:** The corpus contains no price or cost-per-tonne figures; the assistant should say it cannot answer.

**Answer:**

The corpus does not cover this. The price impact or cost per tonne of complying with the EUDR is not addressed in the Regulation, guidance, or FAQs; you may wish to consult market analysts, industry associations, or your commercial team.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.731
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[2] Cite as: [FAQ 1.1 (part 1/2), p. 12]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | Why and how must operators collect coordinates?
Similarity: 0.718
The Regulation requires operators placing covered products on the EU market or exporting them to collect geographic coordinates of the plots of land where the commodities were produced.
This does not apply to downstream operators who place on the market or export such products (for more information on downstream operators, see Chapter 3 of this document).
Traceability to the plot of land (i.e., the requirement to collect the geographic coordinates of the plots of land where the commodities were produced) is necessary to demonstrate that there has been no deforestation at the specific location of production.
Geographic information linking products to the plot of land is already used by part of the industry and a number of certification organisations.
Remotely sensed information (air photos, satellite images) or other information (e.g., photograph in the field with linked geotags and time stamps) may be used for verifying if the geolocation of declared commodities and products is linked to deforestation.
The geolocation coordinates need to be provided in the due diligence statements (hereinafter referred to as “ due diligence statement” or “ DDS”) or, where applicable, in the simplified declarations (hereinafter referred to as “simplified declaration” or “SD”) that operators are required to submit to the Information System ahead of the placing on the EU market or export from the EU of the products.
It is therefore a core part of the Regulation, which prohibits the placing on the EU market, or the export, of any product covered by the Regulation’s scope whose geolocation coordinates have not yet been collected and submitted as part of a due diligence statement.
The only exception is the SD of micro or small primary operators (MSPO), for whom the geolocation may be replaced by a postal address, provided that the postal address clearly corresponds to the geographic location of the plots of land or establishment concerned (see FAQ 3.28 for more details).
Collecting the geolocation coordinates of a plot of land can be done via mobile phones, handheld Global Navigation Satellite System (GNSS) devices and widespread and free-to-use digital applications (e.g.
Geographic Information Systems (GIS)).

---

[3] Cite as: [EUDR Article 1]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Subject matter and scope
Similarity: 0.713
1. This Regulation lays down rules regarding the placing and making available on the Union market as well as the export from the Union of relevant products, as listed in Annex I, that contain, have been fed with or have been made using relevant commodities, namely cattle, cocoa, coffee, oil palm, rubber, soya and wood, with a view to: (a) minimising the Union’s contribution to deforestation and forest degradation worldwide, and thereby contributing to a reduction in global deforestation; (b) reducing the Union’s contribution to greenhouse gas emissions and global biodiversity loss.
2. Except as provided for in Article 37(3), this Regulation does not apply to relevant products listed in Annex I produced before the date indicated in Article 38(1).

---

[4] Cite as: [Guidance §3 (part 3/6)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Date of effect and time-frame for application
Similarity: 0.711
Date of placing relevant commodity or relevant product on the EU market
Relevant products | Date of production of relevant commodity | Before 30 December 2026, and before 30 June 2027 for micro- and small operators | From 30 December 2026 (inclusive) for large and medium enterprises, and from 30 June 2027 (inclusive) for micro- and small operators
Cattle, Cocoa, Coffee, Oil palm, Rubber and Soya products listed in Annex I of Regulation (EU) 2023/1115 | Before 29 June 2023 | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is not applicable
From 29 June 2023 (inclusive) | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is applicable
Wood products listed in Annex I of Regulation (EU) 2023/1115 and not listed in the Annex of Regulation (EU) No 995/2010 (EUTR) | Before 29 June 2023 | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is not applicable
From 29 June 2023 (inclusive) | Regulation (EU) 2023/1115 (EUDR) is not applicable | Regulation (EU) 2023/1115 (EUDR) is applicable
For timber and timber products covered by the Annex of the EUTR, special rules apply, pursuant to Article 37(3) of EUDR:

---

[5] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.71
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;
```

</details>

## q38 (unanswerable)

**Question:** How many cocoa importers did the competent authorities check in 2025?

**Reference:** The corpus contains no enforcement statistics; the assistant should say it cannot answer.

**Answer:**

The corpus does not cover the number of cocoa importers checked by competent authorities in 2025. You can consult the national competent authorities of the EU Member States or check official European Commission enforcement reports for statistical data on past checks.

<details><summary>Retrieved passages</summary>

```
[1] Cite as: [EUDR Annex I (part 1/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.749
Relevant commodities and relevant products as referred to in Article 1
The following table lists goods as classified in the Combined Nomenclature set out in Annex I to Regulation (EEC) No 2658/87 that are referred to in Article 1 of this Regulation.
Except for by-products of a manufacturing process, where that process involved material that was not waste as defined in Article 3, point (1), of Directive 2008/98/EC, this Regulation does not apply to goods if they are produced entirely from material that has completed its lifecycle and would otherwise have been discarded as waste as defined in Article 3, point (1), of that Directive.
Relevant commodity | Relevant products (5)
Cattle (1) | ex 0102 Live cattle ex 0201 Meat of cattle, fresh or chilled ex 0202 Meat of cattle, frozen ex 0206 10 Edible offal of cattle, fresh or chilled ex 0206 21 00 Frozen cattle tongues (This provision shall apply from 30 December 2027) ex 0206 22 Edible cattle livers, frozen ex 0206 29 Edible cattle offal (excluding tongues and livers), frozen ex 1602 50 Other prepared or preserved meat, meat offal, blood, of cattle
Cocoa | 1801 Cocoa beans, whole or broken, raw or roasted 1802 Cocoa shells, husks, skins and other cocoa waste (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) 1803 Cocoa paste, whether or not defatted 1804 Cocoa butter, fat and oil 1805 Cocoa powder, not containing added sugar or other sweetening matter 1806 Chocolate and other food preparations containing cocoa
Coffee | 0901 Coffee, whether or not roasted or decaffeinated; coffee husks and skins;

---

[2] Cite as: [EUDR Annex I (part 2/12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026
Similarity: 0.736
coffee substitutes containing coffee in any proportion 2101 11 00 Extracts, essences, and concentrates of coffee (This provision shall apply from 30 December 2027)
Oil palm (2) | ex 1207 10 00 Palm nuts and kernels ex 1511 Palm oil and its fractions, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 21 Crude palm kernel and babassu oil and fractions thereof, whether or not refined, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1513 29 Palm kernel and babassu oil and their fractions, whether or not refined, other than crude oil, but not chemically modified (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) ex 1516 20 Palm, palm kernel and babassu oils and their fractions, partly or wholly hydrogenated, inter-esterified, re-esterified or elaidinised, whether or not refined, but not further prepared (not including products to the extent they are used in the manufacturing of medicinal products for human or veterinary use within the scope of Directive 2001/83/EC of the European Parliament and of the Council (6), Regulation (EC) No 726/2004 of the European parliament and of the Council (7), or Regulation (EU) 2019/6 of the European Parliament and of the Council (8)) (This provision shall apply from 30 December 2027) ex 1518 00 Palm, palm kernel and babassu oils and their fractions boiled, oxidised, dehydrated, sulphurised, blown, polymerised by heat in vacuum or in inert gas or otherwise chemically modified, excluding those of heading 1516; inedible mixtures or preparations of animal, vegetable or microbial fats or oils or of fractions of different fats or oils of this chapter, that contain or have been made using oil palm (not including waste as defined in Article 3, point (1), of Directive 2008/98/EC) (This provision shall apply from 30 December 2027) ex 1520 00 Crude glycerol, glycerol waters and lyes that have been produced using oil palm’;

---

[3] Cite as: [FAQ 2.4, p. 25]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | What about commodities produced in the EU?
Similarity: 0.733
Commodities produced inside the EU are subject to the same requirements as commodities produced outside the EU.
The Regulation applies to products listed in Annex I, whether they are produced or manufactured in the EU or imported.
For instance, if an EU company manufactures chocolate (code 1806, which is included in Annex I), then it will be considered as a downstream operator subject to the obligations of the Regulation, even if the cocoa powder used in the chocolate has already been placed on the EU market and fulfilled the due diligence requirements (see also FAQ 3.4. on downstream operators).

---

[4] Cite as: [Guidance §9 (part 2/2)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Composite products
Similarity: 0.733
Composite products may contain multiple relevant products under different commodities. For instance, a chocolate bar [HS 1806 ] may comprise derived products of cocoa (cocoa powder [HS 1805 ] and cocoa butter [HS 1804 ]) and oil palm (palm oil [HS 1511 ]). In such cases, the operator placing the product on the EU market or exporting from it will only be required to conduct due diligence on the relevant products listed under the commodity deemed relevant in Annex I of the EUDR. For instance, for chocolate bars [HS 1806 ], the relevant commodity linked to it is cocoa. This means that the due diligence obligation and information requirements extend only to relevant products listed in the right column of Annex I under the relevant commodity which the chocolate bar contains or has been made using, which in this case is the cocoa powder and cocoa butter under the commodity cocoa.

---

[5] Cite as: [FAQ 1.20, p. 20]
Document: Commission FAQ on the implementation of the EUDR, version 5 (April 2026) | How will the Competent Authorities of the EU Member States check the validity of a no-deforestation claim?
Similarity: 0.731
The EU Member States’ Competent Authorities carry out checks in accordance with Art. 16 EUDR to establish that the relevant commodities and products that have been or are intended to be placed on or made available on the EU market or exported, come from deforestation - free plots of land and were produced legally.
This includes conducting checks on the validity of the due diligence statements, and the overall compliance of the operators, downstream operators and traders with the provisions of the Regulation.
For more information on the scope of checks by Competent Authorities, please refer to Arts. 18 and 19 EUDR.

=====

[1] Cite as: [EUDR Article 16(5)–(8)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Obligation to carry out checks
Similarity: 0.775
5. For the purposes of carrying out the checks referred to in paragraph 1, the competent authorities shall establish annual plans containing at least the following: (a) national risk criteria, established in accordance with paragraph 3, for the purpose of determining the checks that are necessary, which build upon any indicative risk criteria at Union level established by the Commission in accordance with paragraph 4, and systematically include risk criteria in relation to countries or parts thereof classified as high risk; (b) the selection of operators, downstream operators and traders to be checked; that selection is to be based on the national risk criteria referred to in point (a), using, inter alia, information contained in the information system referred to in Article 33 and electronic data-processing techniques; for each operator, downstream operator or trader to be checked, competent authorities may identify specific due diligence statements to be checked.
6. The annual review of the plans by the competent authorities shall systematically build upon the results of the checks and the experience on implementation of the plans referred to in paragraph 5 in order to improve their effectiveness.
7. Competent authorities shall communicate their plans of checks, as well as updates thereto, to other competent authorities and the Commission. Competent authorities shall exchange information on and coordinate the development and application of the risk criteria referred to in paragraph 5 with competent authorities of other Member States and with the Commission, in order to improve the effectiveness of the enforcement of this Regulation.
8. Each Member State shall ensure that the annual checks carried out by its competent authorities pursuant to paragraph 1 of this Article cover at least 3 % of the operators, non-SME downstream operators and non-SME traders placing or making available on the market or exporting relevant products that contain or have been made using relevant commodities produced in a country of production or parts thereof classified as standard risk in accordance with Article 29.

---

[2] Cite as: [EUDR Article 16(1)–(4)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Obligation to carry out checks
Similarity: 0.771
1. The competent authorities shall carry out checks within their territory to establish whether operators, downstream operators and traders established in the Union comply with this Regulation. The competent authorities shall carry out checks within their territory to establish whether the relevant products that the operator, downstream operator or trader has placed or intends to place on the market, has made available or intends to make available on the market or has exported or intends to export comply with this Regulation.
2. The checks referred to in paragraph 1 of this Article shall be carried out in accordance with Articles 18 and 19.
3. The competent authorities shall use a risk-based approach to identify the checks to be carried out. Risk criteria shall be identified based on an analysis of risks of non-compliance with this Regulation, taking into account in particular the relevant commodities, the complexity and the length of supply chains, including whether mixing of relevant products is involved, and the stage of processing of the relevant product, whether the plots of land concerned are adjacent to forests, the assignment of risk to countries or parts thereof in accordance with Article 29, paying special attention to the situation of countries or parts thereof classified as high risk, the history of non-compliance of operators, downstream operators or traders with this Regulation, risks of circumvention, and any other relevant information. The analysis of risks shall build on the information referred to in Articles 9 and 10 and may build on the information contained in the information system referred to in Article 33, and may be supported by other relevant sources such as monitoring data, risk profiles from international organisations, substantiated concerns submitted under Article 31, or the conclusions of Commission expert group meetings.
4. The Commission shall, where appropriate, establish and regularly review and update indicative risk criteria at Union level, in accordance with paragraph 3, and communicate them to competent authorities.

---

[3] Cite as: [EUDR Article 16(9)–(12)]
Document: Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026 | Obligation to carry out checks
Similarity: 0.763
9. Each Member State shall ensure that the annual checks carried out by its competent authorities pursuant to paragraph 1 of this Article cover at least 9 % of the operators, non-SME downstream operators and non-SME traders placing or making available on the market or exporting relevant products that contain or have been made using relevant commodities as well as 9 % of the quantity of each of the relevant products that contain or have been made using relevant commodities produced in a country or parts thereof classified as high risk in accordance with Article 29.
10. Each Member State shall ensure that the annual checks
[...]
```

</details>
