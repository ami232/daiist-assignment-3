# Agent answers (gemini-3.5-flash, gemini-3.5-flash-lite, gemini-3.8-flash)

Grade these before reading any judge verdicts. The retrieved passages under each answer are
what the agent saw; use them to judge whether every claim is supported.

## q01 (single)

**Question:** What is the maximum number of Advil Liqui-Gels an adult can take in 24 hours?

**Reference:** No more than 6 capsules (200 mg each) in 24 hours unless a doctor says otherwise; start with 1 capsule every 4-6 hours, 2 if 1 doesn't work.

**Agent answer:**

According to the Advil label, adults (and children 12 years and over) must **not exceed 6 capsules in 24 hours**, unless directed by a doctor [advil, Dosage and Administration].

*gemini-3.8-flash, 1 search(es), 2034 tokens, 13.94 s*

- search `Advil directions adults maximum 24 hours` → [advil, Dosage and Administration], [advil, Warnings], [advil, Active Ingredient], [aleve, Dosage and Administration], [advil, Indications and Usage]

<details><summary>Retrieved passages</summary>

**search:** `Advil directions adults maximum 24 hours`

```text
[advil, Dosage and Administration] Advil (ibuprofen)
Advil (ibuprofen), Dosage and Administration: Directions do not take more than directed the smallest effective dose should be used adults and children 12 years and over: take 1 capsule every 4 to 6 hours while symptoms persist if pain or fever does not respond to 1 capsule, 2 capsules may be used do not exceed 6 capsules in 24 hours, unless directed by a doctor children under 12 years: ask a doctor

[advil, Warnings] Advil (ibuprofen)
Advil (ibuprofen), Warnings: The risk is higher if you use more than directed or for longer than directed.

[advil, Active Ingredient] Advil (ibuprofen)
Advil (ibuprofen), Active Ingredient: Active ingredient (in each capsule) Solubilized ibuprofen equal to 200 mg ibuprofen (NSAID)* (present as the free acid and potassium salt) *nonsteroidal anti-inflammatory drug

[aleve, Dosage and Administration] Aleve (naproxen sodium)
Aleve (naproxen sodium), Dosage and Administration: Directions - do not take more than directed - the smallest effective dose should be used - drink a full glass of water with each dose Adults and children 12 years and older - take 1 capsule every 8 to 12 hours while symptoms last - for the first dose you may take 2 capsules within the first hour - do not exceed 2 capsules in any 8- to 12-hour period - do not exceed 3 capsules in a 24-hour period Children under 12 years of age - ask a doctor

[advil, Indications and Usage] Advil (ibuprofen)
Advil (ibuprofen), Indications and Usage: Uses temporarily relieves minor aches and pains due to: headache toothache backache menstrual cramps the common cold muscular aches minor pain of arthritis temporarily reduces fever
```

</details>

## q02 (single)

**Question:** A customer is 22 weeks pregnant and asks for Advil. What does the label say?

**Reference:** Ask a health professional first. The label says it is especially important not to use ibuprofen at 20 weeks or later in pregnancy unless a doctor directs it.

**Agent answer:**

According to the Advil label:

* If pregnant or breast-feeding, ask a health professional before use `[advil, Pregnancy or Breast-feeding]`.
* It is **especially important not to use ibuprofen at 20 weeks or later in pregnancy** unless definitely directed to do so by a doctor, because it may cause problems in the unborn child or complications during delivery `[advil, Pregnancy or Breast-feeding]`. 

Because the customer is 22 weeks pregnant, she should not use Advil unless explicitly directed by a doctor.

*gemini-3.8-flash, 2 search(es), 5252 tokens, 30.6 s*

- search `Advil pregnancy 20 weeks` → [advil, Pregnancy or Breast-feeding], [naproxen, Pregnancy], [naproxen, Pregnancy], [naproxen, Pregnancy], [naproxen, Other Information]
- search `advil warnings pregnant` → [advil, Pregnancy or Breast-feeding], [advil, Warnings], [aleve, Pregnancy or Breast-feeding], [naproxen, Pregnancy], [naproxen, Pregnancy]

<details><summary>Retrieved passages</summary>

**search:** `Advil pregnancy 20 weeks`

```text
[advil, Pregnancy or Breast-feeding] Advil (ibuprofen)
Advil (ibuprofen), Pregnancy or Breast-feeding: If pregnant or breast-feeding, ask a health professional before use. It is especially important not to use ibuprofen at 20 weeks or later in pregnancy unless definitely directed to do so by a doctor because it may cause problems in the unborn child or complications during delivery.

[naproxen, Pregnancy] Naproxen (naproxen)
Naproxen (naproxen), Pregnancy: Premature Closure of Fetal Ductus Arteriosus: Published literature reports that the use of NSAIDs at about 30 weeks of gestation and later in pregnancy may cause premature closure of the fetal ductus arteriosus. Oligohydramnios/Neonatal Renal Impairment: Published studies and postmarketing reports describe maternal NSAID use at about 20 weeks gestation or later in pregnancy associated with fetal renal dysfunction leading to oligohydramnios, and in some cases, neonatal renal impairment. These adverse outcomes are seen, on average, after days to weeks of treatment, although oligohydramnios has been infrequently reported as soon as 48 hours after NSAID initiation. In many cases, but not all, the decrease in amniotic fluid was transient and reversible with cessation of the drug. There have been a limited number of case reports of maternal NSAID use and neonatal renal dysfunction without oligohydramnios, some of which were irreversible.

[naproxen, Pregnancy] Naproxen (naproxen)
Naproxen (naproxen), Pregnancy: 8.1 Pregnancy Risk Summary Use of NSAIDs, including Naproxen tablets, can cause premature closure of the fetal ductus arteriosus and fetal renal dysfunction leading to oligohydramnios and, in some cases, neonatal renal impairment. Because of these risks, limit dose and duration of Naproxen Tablets, use between about 20 and 30 weeks of gestation, and avoid Naproxen Tablets, use at about 30 weeks of gestation and later in pregnancy (see Clinical Considerations, Data). Premature Closure of Fetal Ductus Arteriosus Use of NSAIDs, including naproxen tablets, at about 30 weeks gestation or later in pregnancy increases the risk of premature closure of the fetal ductus arteriosus. Oligohydramnios/Neonatal Renal Impairment Use of NSAIDs at about 20 weeks gestation or later in pregnancy has been associated with cases of fetal renal dysfunction leading to oligohydramnios, and in some cases, neonatal renal impairment.

[naproxen, Pregnancy] Naproxen (naproxen)
Naproxen (naproxen), Pregnancy: The estimated background risk of major birth defects and miscarriage for the indicated population(s) is unknown. All pregnancies have a background risk of birth defect, loss, or other adverse outcomes. In the U.S. general population, the estimated background risk of major birth defects and miscarriage in clinically recognized pregnancies is 2% to 4% and 15% to 20%, respectively. Clinical Considerations Fetal/Neonatal Adverse Reactions Premature Closure of Fetal Ductus Arteriosus: Avoid use of NSAIDs in women at about 30 weeks gestation and later in pregnancy, because NSAIDs, including Naproxen Tablets, can cause premature closure of the fetal ductus arteriosus (see Data ). Oligohydramnios/Neonatal Renal Impairment: If an NSAID is necessary at about 20 weeks gestation or later in pregnancy, limit the use to the lowest effective dose and shortest duration possible. If Naproxen Tablets, treatment extends beyond 48 hours, consider monitoring with ultrasound for oligohydramnios.

[naproxen, Other Information] Naproxen (naproxen)
Naproxen (naproxen), Other Information: If you need to take NSAIDs for more than 2 days when you are between 20 and 30 weeks of pregnancy, your healthcare provider may need to monitor the amount of fluid in your womb around your baby. You should not take NSAIDs after about 30 weeks of pregnancy. - are breastfeeding or plan to breast feed. Tell your healthcare provider about all of the medicines you take, including prescription or over-the-counter medicines, vitamins or herbal supplements. NSAIDs and some other medicines can interact with each other and cause serious side effects. Do not start taking any new medicine without talking to your healthcare provider first. What are the possible side effects of NSAIDs?
```

**search:** `advil warnings pregnant`

```text
[advil, Pregnancy or Breast-feeding] Advil (ibuprofen)
Advil (ibuprofen), Pregnancy or Breast-feeding: If pregnant or breast-feeding, ask a health professional before use. It is especially important not to use ibuprofen at 20 weeks or later in pregnancy unless definitely directed to do so by a doctor because it may cause problems in the unborn child or complications during delivery.

[advil, Warnings] Advil (ibuprofen)
Advil (ibuprofen), Warnings: Warnings Allergy alert: Ibuprofen may cause a severe allergic reaction, especially in people allergic to aspirin. Symptoms may include: hives facial swelling asthma (wheezing) shock skin reddening rash blisters If an allergic reaction occurs, stop use and seek medical help right away. Stomach bleeding warning: This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs [aspirin, ibuprofen, naproxen, or others] have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning: NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal.

[aleve, Pregnancy or Breast-feeding] Aleve (naproxen sodium)
Aleve (naproxen sodium), Pregnancy or Breast-feeding: If pregnant or breast-feeding, ask a health professional before use. It is especially important not to use naproxen sodium during the last 3 months of pregnancy unless definitely directed to do so by a doctor because it may cause problems in the unborn child or complications during delivery.

[naproxen, Pregnancy] Naproxen (naproxen)
Naproxen (naproxen), Pregnancy: The estimated background risk of major birth defects and miscarriage for the indicated population(s) is unknown. All pregnancies have a background risk of birth defect, loss, or other adverse outcomes. In the U.S. general population, the estimated background risk of major birth defects and miscarriage in clinically recognized pregnancies is 2% to 4% and 15% to 20%, respectively. Clinical Considerations Fetal/Neonatal Adverse Reactions Premature Closure of Fetal Ductus Arteriosus: Avoid use of NSAIDs in women at about 30 weeks gestation and later in pregnancy, because NSAIDs, including Naproxen Tablets, can cause premature closure of the fetal ductus arteriosus (see Data ). Oligohydramnios/Neonatal Renal Impairment: If an NSAID is necessary at about 20 weeks gestation or later in pregnancy, limit the use to the lowest effective dose and shortest duration possible. If Naproxen Tablets, treatment extends beyond 48 hours, consider monitoring with ultrasound for oligohydramnios.

[naproxen, Pregnancy] Naproxen (naproxen)
Naproxen (naproxen), Pregnancy: If oligohydramnios occurs, discontinue Naproxen Tablets, and follow up according to clinical practice (see Data ). Labor or Delivery There are no studies on the effects of naproxen tablets during labor or delivery. In animal studies, NSAIDS, including naproxen, inhibit prostaglandin synthesis, cause delayed parturition, and increase the incidence of stillbirth. Data Human Data There is some evidence to suggest that when inhibitors of prostaglandin synthesis are used to delay preterm labor, there is an increased risk of neonatal complications such as necrotizing enterocolitis, patent ductus arteriosus, and intracranial hemorrhage. Naproxen treatment given in late pregnancy to delay parturition has been associated with persistent pulmonary hypertension, renal dysfunction, and abnormal prostaglandin E levels in preterm infants. Because of the known effects of nonsteroidal anti-inflammatory drugs on the fetal cardiovascular system (closure of ductus arteriosus), use during pregnancy (particularly starting at 30-weeks of gestation, or third trimester) should be avoided.
```

</details>

## q03 (single)

**Question:** How should a customer take the first dose of Aleve Liquid Gels?

**Reference:** Adults and children 12+ may take 2 capsules within the first hour for the first dose, then 1 capsule every 8-12 hours; no more than 3 capsules in 24 hours. Drink a full glass of water with each dose.

**Agent answer:**

According to the Aleve label directions for adults and children 12 years and older:

* **First dose:** Take 1 capsule, but for the first dose you may take 2 capsules within the first hour `[aleve, Dosage and Administration]`.
* **Administration:** Drink a full glass of water with each dose `[aleve, Dosage and Administration]`.
* **Dosing limits and precautions:**
  * Use the smallest effective dose and do not take more than directed `[aleve, Dosage and Administration]`.
  * Do not exceed 2 capsules in any 8- to 12-hour period `[aleve, Dosage and Administration]`.
  * Do not exceed 3 capsules in a 24-hour period `[aleve, Dosage and Administration]`.
* **Children under 12 years of age:** Ask a doctor `[aleve, Dosage and Administration]`.

*gemini-3.8-flash, 1 search(es), 2284 tokens, 8.11 s*

- search `Aleve Liquid Gels directions first dose` → [aleve, Dosage and Administration], [aleve, Active Ingredient], [aleve, Indications and Usage], [aleve, Inactive Ingredients], [flanax, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Aleve Liquid Gels directions first dose`

```text
[aleve, Dosage and Administration] Aleve (naproxen sodium)
Aleve (naproxen sodium), Dosage and Administration: Directions - do not take more than directed - the smallest effective dose should be used - drink a full glass of water with each dose Adults and children 12 years and older - take 1 capsule every 8 to 12 hours while symptoms last - for the first dose you may take 2 capsules within the first hour - do not exceed 2 capsules in any 8- to 12-hour period - do not exceed 3 capsules in a 24-hour period Children under 12 years of age - ask a doctor

[aleve, Active Ingredient] Aleve (naproxen sodium)
Aleve (naproxen sodium), Active Ingredient: Active ingredient (in each capsule) Naproxen sodium 220 mg (naproxen 200 mg) (NSAID) nonsteroidal anti-inflammatory drug

[aleve, Indications and Usage] Aleve (naproxen sodium)
Aleve (naproxen sodium), Indications and Usage: Uses temporarily relieves minor aches and pains due to: minor pain of arthritis muscular aches backache menstrual cramps headache toothache the common cold temporarily reduces fever

[aleve, Inactive Ingredients] Aleve (naproxen sodium)
Aleve (naproxen sodium), Inactive Ingredients: Inactive ingredients FD&C blue #1, gelatin, glycerin, lactic acid, mannitol, pharmaceutical ink, polyethylene glycol, povidone, propylene glycol, purified water, sorbitan, sorbitol

[flanax, Dosage and Administration] Flanax (naproxen sodium)
Flanax (naproxen sodium), Dosage and Administration: Directions do not take more than directed the smallest effective dose should be used drink a full glass of water with each dose adults and children 12 years and older take 1 tablet every 8 to 12 hours while symptoms last for the first dose you may take 2 tablets within the first hour do not exceed 2 tablets in any 8- to 12-hour period do not exceed 3 tablets in a 24-hour period children under 12 years: ask a doctor
```

</details>

## q04 (single)

**Question:** What is the most Tylenol Extra Strength an adult can take in a day?

**Reference:** 2 caplets (500 mg each) every 6 hours, no more than 6 caplets in 24 hours unless a doctor directs; do not use more than 10 days without a doctor.

**Agent answer:**

For adults (and children 12 years and over), the maximum recommended dose of TYLENOL Extra Strength is **no more than 6 caplets in 24 hours** (equivalent to 3,000 mg per day), unless directed by a doctor [tylenol, Dosage and Administration]. 

Additional dosing directions include:
* Take 2 caplets every 6 hours while symptoms last [tylenol, Dosage and Administration].
* Each caplet contains 500 mg of acetaminophen [tylenol, Active Ingredient].
* Do not use for more than 10 days unless directed by a doctor [tylenol, Dosage and Administration].

*gemini-3.8-flash, 1 search(es), 2147 tokens, 17.32 s*

- search `Tylenol Extra Strength adult maximum daily dose` → [tylenol, Dosage and Administration], [tylenol, Ask a Doctor Before Use], [tylenol, Active Ingredient], [tylenol, Overdosage], [tylenol, Indications and Usage]

<details><summary>Retrieved passages</summary>

**search:** `Tylenol Extra Strength adult maximum daily dose`

```text
[tylenol, Dosage and Administration] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Dosage and Administration: Directions - do not take more than directed (see overdose warning) adults and children 12 years and over - take 2 caplets every 6 hours while symptoms last - do not take more than 6 caplets in 24 hours, unless directed by a doctor - do not use for more than 10 days unless directed by a doctor children under 12 years ask a doctor

[tylenol, Ask a Doctor Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor Before Use: Ask a doctor before use if you have liver disease

[tylenol, Active Ingredient] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Active Ingredient: Active ingredient (in each caplet) Acetaminophen 500 mg

[tylenol, Overdosage] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Overdosage: Overdose warning : In case of overdose, get medical help or contact a Poison Control Center right away. (1-800-222-1222) Quick medical attention is critical for adults as well as for children even if you do not notice any signs or symptoms.

[tylenol, Indications and Usage] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Indications and Usage: Uses temporarily relieves minor aches and pains due to: - the common cold - headache - backache - minor pain of arthritis - toothache - muscular aches - premenstrual and menstrual cramps temporarily reduces fever
```

</details>

## q05 (single)

**Question:** What can cause liver damage with Tylenol Extra Strength?

**Reference:** Taking more than 4,000 mg acetaminophen in 24 hours, taking it with other acetaminophen products, or having 3 or more alcoholic drinks every day while using it.

**Agent answer:**

According to the TYLENOL Extra Strength label, severe liver damage may occur if you take:

* More than 4,000 mg of acetaminophen in 24 hours `[tylenol, Warnings]`
* With other drugs containing acetaminophen `[tylenol, Warnings]`
* 3 or more alcoholic drinks every day while using this product `[tylenol, Warnings]`

Additionally, patients should ask a doctor before use if they have liver disease `[tylenol, Ask a Doctor Before Use]`.

*gemini-3.8-flash, 1 search(es), 2092 tokens, 50.74 s*

- search `Tylenol Extra Strength liver warning damage` → [tylenol, Ask a Doctor Before Use], [tylenol, Warnings], [tylenol, Overdosage], [tylenol, Ask a Doctor or Pharmacist Before Use], [tylenol, Indications and Usage]

<details><summary>Retrieved passages</summary>

**search:** `Tylenol Extra Strength liver warning damage`

```text
[tylenol, Ask a Doctor Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor Before Use: Ask a doctor before use if you have liver disease

[tylenol, Warnings] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Warnings: Warnings Warnings Liver warning: This product contains acetaminophen. Severe liver damage may occur if you take - more than 4,000 mg of acetaminophen in 24 hours - with other drugs containing acetaminophen - 3 or more alcoholic drinks every day while using this product Allergy alert acetaminophen may cause severe skin reactions.Symptoms may include: - skin reddening - blisters - rash If a skin reaction occurs, stop use and seek medical help right away. Liver warning: This product contains acetaminophen. Severe liver damage may occur if you take - more than 4,000 mg of acetaminophen in 24 hours - with other drugs containing acetaminophen - 3 or more alcoholic drinks every day while using this product Allergy alert acetaminophen may cause severe skin reactions.Symptoms may include: - skin reddening - blisters - rash If a skin reaction occurs, stop use and seek medical help right away.

[tylenol, Overdosage] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Overdosage: Overdose warning : In case of overdose, get medical help or contact a Poison Control Center right away. (1-800-222-1222) Quick medical attention is critical for adults as well as for children even if you do not notice any signs or symptoms.

[tylenol, Ask a Doctor or Pharmacist Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin

[tylenol, Indications and Usage] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Indications and Usage: Uses temporarily relieves minor aches and pains due to: - the common cold - headache - backache - minor pain of arthritis - toothache - muscular aches - premenstrual and menstrual cramps temporarily reduces fever
```

</details>

## q06 (single)

**Question:** How long can reconstituted amoxicillin suspension be kept after mixing?

**Reference:** Discard any unused suspension after 14 days. Refrigeration is preferable but not required; shake well before each use.

**Agent answer:**

Any unused portion of reconstituted amoxicillin oral suspension must be discarded after **14 days** `[amoxil, Dosage and Administration]`. 

Refrigeration is preferable, but not required `[amoxil, Dosage and Administration]`.

*gemini-3.8-flash, 1 search(es), 2647 tokens, 24.68 s*

- search `Amoxil reconstituted suspension storage days` → [amoxil, Dosage and Administration], [amoxil, How Supplied], [augmentin, Dosage and Administration], [amoxil, Dosage and Administration], [amoxil, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Amoxil reconstituted suspension storage days`

```text
[amoxil, Dosage and Administration] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Dosage and Administration: Any unused portion of the reconstituted suspension must be discarded after 14 days. Refrigeration is preferable, but not required.

[amoxil, How Supplied] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), How Supplied: Amoxicillin for Oral Suspension, USP:Each 5 mL of reconstituted fruity-flavored suspension contains 125, 200, 250, or 400 mg Amoxicillin as the trihydrate. Amoxicillin for Oral Suspension, USP 125 mg/5ml 80-mL bottle 100-mL bottle 150-mL bottle Amoxicillin for Oral Suspension, USP 200 mg/5mL 50-mL bottle 75-mL bottle 100-mL bottle Amoxicillin for Oral Suspension, USP 250 mg/5mL 80-mL bottle 100-mL bottle 150-mL bottle Amoxicillin for Oral Suspension, USP 400 mg/5mL 50-mL bottle 75-mL bottle 100-mL bottle Store at 20° to 25°C (68° to 77°F ) [See USP Controlled Room Temperature] Dispense in a tight, light-resistant container as defined in the USP using a child-resistant closure.

[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: Table 5: Amount of Water for Mixing AUGMENTIN for Oral Suspension Strength of AUGMENTIN Oral Suspension Bottle Size Amount of Water for Reconstitution Contents of Each Teaspoonful (5 mL) 125 mg/31.25 mg per 5 mL 75 mL 100 mL 150 mL 67 mL 90 mL 134 mL 125 mg of amoxicillin and 31.25 mg of clavulanic acid as the potassium salt 250 mg/62.5 mg per 5 mL 75 mL 100 mL 150 mL 65 mL 87 mL 130 mL 250 mg of amoxicillin and 62.5 mg of clavulanic acid as the potassium salt Shake oral suspension well before using. Reconstituted suspension must be stored under refrigeration and discarded after 10 days. Some color change is normal during dosing period.

[amoxil, Dosage and Administration] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Dosage and Administration: Amount of Water for Mixing Oral Suspension Strength Bottle Size Amount of Water Required for Reconstitution Oral Suspension 125 mg /5 mL 80 mL 66 mL 100 mL 83 mL 150 mL 125 mL Oral Suspension 200 mg /5 mL 50 mL 39 mL 75 mL 59 mL 100 mL 78 mL Oral Suspension 250 mg /5 mL 80 mL 59 mL 100 mL 73 ml 150 mL 110 mL Oral Suspension 400 mg /5 mL 50 mL 34 mL 75 mL 51 mL 100 mL 68 mL After reconstitution, the required amount of suspension should be placed directly on the child's tongue for swallowing. Alternate means of administration are to add the required amount of suspension to formula, milk, fruit juice, water, ginger ale, or cold drinks. These preparations should then be taken immediately. NOTE: SHAKE ORAL SUSPENSION WELL BEFORE USING. Keep bottle tightly closed.

[amoxil, Dosage and Administration] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Dosage and Administration: Patients with a glomerular filtration rate of 10 to 30 mL/min should receive 500 mg or 250 mg every 12 hours, depending on the severity of the infection. Patients with a glomerular filtration rate less than 10 mL/min should receive 500 mg or 250 mg every 24 hours, depending on severity of the infection. Hemodialysis patients should receive 500 mg or 250 mg every 24 hours, depending on severity of the infection. They should receive an additional dose both during and at the end of dialysis. 2.5 Directions for Mixing Oral Suspension Tap bottle until all powder flows freely. Add approximately 1/3 of the total amount of water for reconstitution (see Table 2) and shake vigorously to wet powder. Add remainder of the water and again shake vigorously. Table 2.
```

</details>

## q07 (single)

**Question:** Why shouldn't amoxicillin be given to a patient with mononucleosis?

**Reference:** A high percentage of patients with mononucleosis who receive amoxicillin develop an erythematous skin rash, so it should not be given to them.

**Agent answer:**

Amoxicillin should not be administered to patients with mononucleosis because a high percentage of patients with mononucleosis who receive amoxicillin develop an erythematous skin rash [amoxil, Warnings and Precautions] [augmentin, Warnings and Precautions].

*gemini-3.8-flash, 1 search(es), 2528 tokens, 18.65 s*

- search `amoxicillin mononucleosis` → [amoxil, Warnings and Precautions], [augmentin, Warnings and Precautions], [amoxil, Indications and Usage], [amoxil, Contraindications], [amoxil, Adverse Reactions]

<details><summary>Retrieved passages</summary>

**search:** `amoxicillin mononucleosis`

```text
[amoxil, Warnings and Precautions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Warnings and Precautions: Prescribing Amoxicillin either in the absence of a proven or strongly suspected bacterial infection is unlikely to provide benefit to the patient, and increases the risk of the development of drug-resistant bacteria. 5.4 Use in Patients With Mononucleosis A high percentage of patients with mononucleosis who receive Amoxicillin develop an erythematous skin rash. Thus Amoxicillin should not be administered to patients with mononucleosis. 5.5 Phenylketonurics The oral suspensions of Amoxicillin do not contain phenylalanine and can be used by phenylketonurics.

[augmentin, Warnings and Precautions] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Warnings and Precautions: C. difficile produces toxins A and B which contribute to the development of CDAD. Hypertoxin-producing strains of C. difficile cause increased morbidity and mortality, as these infections can be refractory to antimicrobial therapy and may require colectomy. CDAD must be considered in all patients who present with diarrhea following antibacterial use. Careful medical history is necessary since CDAD has been reported to occur over 2 months after the administration of antibacterial agents. If CDAD is suspected or confirmed, ongoing antibacterial use not directed against C. difficile may need to be discontinued. Appropriate fluid and electrolyte management, protein supplementation, antibacterial treatment of C. difficile , and surgical evaluation should be instituted as clinically indicated. 5.6 Skin Rash in Patients with Mononucleosis A high percentage of patients with mononucleosis who receive amoxicillin develop an erythematous skin rash. Thus, AUGMENTIN should not be administered to patients with mononucleosis.

[amoxil, Indications and Usage] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Indications and Usage: 1.3 Infections of the skin and skin structure - due to Streptococcus spp. (α- and β-hemolytic isolates only), Staphylococcus spp., or E. coli. 1.4 Infections of the lower respiratory tract - due to Streptococcus spp. (α- and β-hemolytic isolates only), S. pneumoniae, Staphylococcus spp., or H. influenzae. 1.5 Gonorrhea, acute uncomplicated (ano-genital and urethral infections in males and females) - due to Neisseria gonorrhoeae. Because of high rates of Amoxicillin resistance, Amoxicillin for Oral Suspension is not recommended for empiric treatment of gonorrhea. Amoxicillin for Oral Suspension use should be limited to situations where N. gonorrhoeae isolates are known to be susceptible to Amoxicillin. 1.6 Triple therapy for Helicobacter pylori with clarithromycin and lansoprazole: Amoxicillin for Oral Suspension in combination with clarithromycin plus lansoprazole as triple therapy, is indicated for the treatment of patients with H.

[amoxil, Contraindications] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Contraindications: Amoxicillin is contraindicated in patients who have experienced a serious hypersensitivity reaction (e.g., anaphylaxis or Stevens-Johnson syndrome) to Amoxicillin or to other β-lactam antibiotics (e.g., penicillins and cephalosporins).

[amoxil, Adverse Reactions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Adverse Reactions: Liver: A moderate rise in AST and/or ALT has been noted, but the significance of this finding is unknown. Hepatic dysfunction including cholestatic jaundice, hepatic cholestasis and acute cytolytic hepatitis have been reported. Renal: Crystalluria has been reported [see Overdosage (10)]. Hemic and Lymphatic Systems: Anemia, including hemolytic anemia, thrombocytopenia, thrombocytopenic purpura, eosinophilia, leukopenia, and agranulocytosis have been reported. These reactions are usually reversible on discontinuation of therapy and are believed to be hypersensitivity phenomena. Central Nervous System: Reversible hyperactivity, agitation, anxiety, insomnia, confusion, convulsions, behavioral changes, and/or dizziness have been reported. Miscellaneous: Tooth discoloration (brown, yellow, or gray staining) has been reported. Most reports occurred in pediatric patients. Discoloration was reduced or eliminated with brushing or dental cleaning in most cases.
```

</details>

## q08 (single)

**Question:** Can amoxicillin make birth control pills less effective?

**Reference:** Yes. The label says amoxicillin may affect gut flora, reducing estrogen reabsorption and the effectiveness of combined oral estrogen/progesterone contraceptives.

**Agent answer:**

Yes. According to the FDA drug label, amoxicillin may affect gut flora, leading to lower estrogen reabsorption and reduced efficacy of combined oral estrogen/progesterone contraceptives [amoxil, Drug Interactions] [augmentin, Drug Interactions].

*gemini-3.8-flash, 1 search(es), 2702 tokens, 15.8 s*

- search `amoxicillin oral contraceptives birth control` → [amoxil, Drug Interactions], [augmentin, Drug Interactions], [amoxil, Drug Interactions], [amoxil, Use in Specific Populations], [augmentin, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `amoxicillin oral contraceptives birth control`

```text
[amoxil, Drug Interactions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Drug Interactions: 7.1 Probenecid Probenecid decreases the renal tubular secretion of Amoxicillin. Concurrent use of Amoxicillin and probenecid may result in increased and prolonged blood levels of Amoxicillin. 7.2 Oral Anticoagulants Abnormal prolongation of prothrombin time (increased international normalized ratio [INR]) has been reported in patients receiving Amoxicillin and oral anticoagulants. Appropriate monitoring should be undertaken when anticoagulants are prescribed concurrently. Adjustments in the dose of oral anticoagulants may be necessary to maintain the desired level of anticoagulation. 7.3 Allopurinol The concurrent administration of allopurinol and Amoxicillin increases the incidence of rashes in patients receiving both drugs as compared to patients receiving Amoxicillin alone. It is not known whether this potentiation of Amoxicillin rashes is due to allopurinol or the hyperuricemia present in these patients. 7.4 Oral Contraceptives Amoxicillin may affect the gut flora, leading to lower estrogen reabsorption and reduced efficacy of combined oral estrogen/progesterone contraceptives.

[augmentin, Drug Interactions] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Drug Interactions: 7.3 Allopurinol The concurrent administration of allopurinol and amoxicillin increases the incidence of rashes in patients receiving both drugs as compared to patients receiving amoxicillin alone. It is not known whether this potentiation of amoxicillin rashes is due to allopurinol or the hyperuricemia present in these patients. 7.4 Oral Contraceptives AUGMENTIN may affect intestinal flora, leading to lower estrogen reabsorption and reduced efficacy of combined oral estrogen/progesterone contraceptives.

[amoxil, Drug Interactions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Drug Interactions: 7.5 Other Antibacterials Chloramphenicol, macrolides, sulfonamides, and tetracyclines may interfere with the bactericidal effects of penicillin. This has been demonstrated in vitro; however, the clinical significance of this interaction is not well documented. 7.6 Effects on Laboratory Tests High urine concentrations of ampicillin may result in false-positive reactions when testing for the presence of glucose in urine using CLINITEST® (manufactured by Miles, Inc.), Benedict's Solution, or Fehling's Solution. Since this effect may also occur with Amoxicillin, it is recommended that glucose tests based on enzymatic glucose oxidase reactions [such as CLINISTIX® (manufactured by Bayer Corporation)] be used. Following administration of ampicillin or Amoxicillin to pregnant women, a transient decrease in plasma concentration of total conjugated estriol, estriol-glucuronide, conjugated estrone, and estradiol has been noted.

[amoxil, Use in Specific Populations] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Use in Specific Populations: 8.1 Pregnancy Teratogenic Effects: Pregnancy Category B. Reproduction studies have been performed in mice and rats at doses up to 2000 mg/kg (3 and 6 times the 3 g human dose, based on body surface area). There was no evidence of harm to the fetus due to Amoxicillin. There are, however, no adequate and well-controlled studies in pregnant women. Because animal reproduction studies are not always predictive of human response, Amoxicillin should be used during pregnancy only if clearly needed. 8.2 Labor and Delivery Oral ampicillin is poorly absorbed during labor. It is not known whether use of Amoxicillin in humans during labor or delivery has immediate or delayed adverse effects on the fetus, prolongs the duration of labor, or increases the likelihood of the necessity for an obstetrical intervention. 8.3 Nursing Mothers Penicillins have been shown to be excreted in human milk.

[augmentin, Drug Interactions] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Drug Interactions: 7 DRUG INTERACTIONS Co-administration with probenecid is not recommended. ( 7.1 ) Concomitant use of AUGMENTIN and oral anticoagulants may increase the prolongation of prothrombin time.( 7.2 ) Co-administration with allopurinol increases the risk of rash. ( 7.3 ) AUGMENTIN may reduce efficacy of oral contraceptives. ( 7.4 ) 7.1 Probenecid Probenecid decreases the renal tubular secretion of amoxicillin but does not delay renal excretion of clavulanic acid. Concurrent use with AUGMENTIN may result in increased and prolonged blood concentrations of amoxicillin. Co-administration of probenecid is not recommended. 7.2 Oral Anticoagulants Abnormal prolongation of prothrombin time (increased international normalized ratio [INR]) has been reported in patients receiving amoxicillin and oral anticoagulants. Appropriate monitoring should be undertaken when anticoagulants are prescribed concurrently with AUGMENTIN. Adjustments in the dose of oral anticoagulants may be necessary to maintain the desired level of anticoagulation.
```

</details>

## q09 (single)

**Question:** Can a customer use two Augmentin 250 mg tablets instead of one 500 mg tablet?

**Reference:** No. Both tablets contain the same 125 mg clavulanic acid, so two 250 mg tablets are not equivalent to one 500 mg tablet.

**Agent answer:**

**No**, a customer should not substitute two 250 mg/125 mg Augmentin tablets for one 500 mg/125 mg Augmentin tablet [augmentin, Dosage and Administration]. 

Both the 250 mg and 500 mg tablets contain the same amount of clavulanic acid (125 mg as the potassium salt). Because taking two 250 mg tablets would provide twice the amount of clavulanic acid (250 mg) compared to a single 500 mg tablet (125 mg), the two regimens are not equivalent [augmentin, Dosage and Administration].

*gemini-3.8-flash, 1 search(es), 3037 tokens, 13.16 s*

- search `Augmentin 250 mg 500 mg substitute equivalent` → [augmentin, Dosage and Administration], [augmentin, Dosage and Administration], [augmentin, Dosage and Administration], [augmentin, Warnings and Precautions], [augmentin, Description]

<details><summary>Retrieved passages</summary>

**search:** `Augmentin 250 mg 500 mg substitute equivalent`

```text
[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: Two AUGMENTIN 250 mg/125 mg Tablets are NOT Substitutable with One 500 mg/125 mg AUGMENTIN Tablet Two 250 mg/125 mg tablets of AUGMENTIN should NOT be substituted for one 500 mg/125 mg tablet of AUGMENTIN. Since both the 250 mg and 500 mg tablets of AUGMNTIN contain the same amount of clavulanic acid (125 mg, as the potassium salt), two 250 mg tablets of AUGMENTIN are not equivalent to one 500 mg tablet of AUGMENTIN.

[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: 2.6 Switching between Dosage Forms and between Strengths AUGMENTIN 250 mg/125 mg Tablet is NOT Substitutable with AUGMENTIN 250 mg/62.5 mg Chewable Tablet The 250 mg/125 mg tablet of AUGMENTIN and the 250 mg/62.5 mg chewable tablet of AUGMENTIN should NOT be substituted for each other and the 250 mg/125 mg tablet of AUGMENTIN should NOT be used in pediatric patients weighing less than 40 kg [see Dosage and Administration ( 2.3 )] . The 250 mg tablet of AUGMENTIN and the 250 mg chewable tablet of AUGMENTIN do not contain the same amount of clavulanic acid. The 250 mg tablet of AUGMENTIN contains 125 mg of clavulanic acid whereas the 250 mg chewable tablet of AUGMENTIN contains 62.5 mg of clavulanic acid.

[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: 2.2 Adult Patients See dosing regimens of AUGMENTIN (based on the amoxicillin component) provided in Table 1 below. Table 1. Dosing Regimens of AUGMENTIN in Adult Patients TYPE OF INFECTION DOSING REGIMEN OF Amoxicillin and Clavulanate Potassium Severe infections and infections of the respiratory tract one 875 mg tablet a of AUGMENTIN every 12 hours or one 500 mg tablet b,c of AUGMENTIN every 8 hours Less severe infections one 500 mg tablet b,c of AUGMENTIN every 12 hours or one 250 mg tablet d of AUGMENTIN every 8 hours a Adults who have difficulty swallowing may be given the AUGMENTIN 200 mg/28.5 mg per 5 mL suspension or the AUGMENTIN 400 mg/57 mg per 5 mL suspension may be used in place of the 875 mg/125 mg tablet.

[augmentin, Warnings and Precautions] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Warnings and Precautions: 5.7 Potential for Microbial Overgrowth The possibility of superinfections with fungal or bacterial pathogens should be considered during therapy. If superinfection occurs, amoxicillin and clavulanate potassium should be discontinued and appropriate therapy instituted. 5.8 Phenylketonurics AUGMENTIN Chewable tablets and AUGMENTIN for Oral Suspension contain aspartame which contains phenylalanine. Each 200 mg chewable tablet of AUGMENTIN contains 2.1 mg phenylalanine; each 400 mg chewable tablet contains 4.2 mg phenylalanine; each 5 mL of either the 200 mg/5 mL or 400 mg/5 mL oral suspension contains 7 mg phenylalanine. The other formulations of AUGMENTIN do not contain phenylalanine. 5.9 Development of Drug-Resistant Bacteria Prescribing AUGMENTIN in the absence of a proven or strongly suspected bacterial infection or a prophylactic indication is unlikely to provide benefit to the patient and increases the risk of the development of drug-resistant bacteria.

[augmentin, Description] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Description: 11 DESCRIPTION AUGMENTIN is an oral antibacterial combination consisting of amoxicillin and the beta-lactamase inhibitor, clavulanate potassium (the potassium salt of clavulanic acid). Amoxicillin is an analog of ampicillin, derived from the basic penicillin nucleus, 6-aminopenicillanic acid. The amoxicillin molecular formula is C 16 H 19 N 3 O 5 S-3H 2 O, and the molecular weight is 419.46. Chemically, amoxicillin is (2 S ,5 R ,6 R )-6-[( R )-(-)-2-Amino-2-( p -hydroxyphenyl)acetamido]-3,3-dimethyl-7-oxo-4-thia-1-azabicyclo[3.2.0]heptane-2-carboxylic acid trihydrate and may be represented structurally as: Clavulanic acid is produced by the fermentation of Streptomyces clavuligerus . It is a beta-lactam structurally related to the penicillins and possesses the ability to inactivate some beta-lactamases by blocking the active sites of these enzymes. The clavulanate potassium molecular formula is C 8 H 8 KNO 5 , and the molecular weight is 237.25.
```

</details>

## q10 (single)

**Question:** Should Augmentin be taken with food?

**Reference:** It can be taken regardless of meals, but taking it at the start of a meal improves clavulanate absorption and reduces stomach upset.

**Agent answer:**

Augmentin may be taken without regard to meals; however, it is recommended to take it with food for two reasons:

* **Minimizing gastrointestinal intolerance:** Augmentin should be taken at the start of a meal—or with a meal or snack—to reduce the potential for gastrointestinal upset/intolerance [augmentin, Dosage and Administration], [augmentin, Other Information].
* **Enhancing absorption:** Absorption of the clavulanate potassium component is enhanced when Augmentin is administered at the start of a meal [augmentin, Dosage and Administration].

*gemini-3.8-flash, 1 search(es), 2972 tokens, 8.17 s*

- search `Augmentin food administration dosing` → [augmentin, Dosage and Administration], [augmentin, Other Information], [augmentin, Dosage and Administration], [augmentin, Dosage and Administration], [augmentin, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Augmentin food administration dosing`

```text
[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: 2 DOSAGE AND ADMINISTRATION Adults and Pediatric Patients greater than 40 kg: 500 or 875 mg every 12 hours or 250 or 500 mg every 8 hours, based on the amoxicillin component. ( 2.2 , 2.3 ) Pediatric patients aged 12 weeks (3 months) and older: 25 to 45 mg/kg/day every 12 hours or 20 to 40 mg/kg/day every 8 hours, up to the adult dose. ( 2.3 ) Neonates and infants less than 12 weeks of age: 30 mg/kg/day divided every 12 hours, based on the amoxicillin component. Use of the 125 mg/5 mL oral suspension is recommended. ( 2.3 ) 2.1 Important Administration Instructions AUGMENTIN may be taken without regard to meals; however, absorption of clavulanate potassium is enhanced when AUGMENTIN is administered at the start of a meal. To minimize the potential for gastrointestinal intolerance, AUGMENTIN should be taken at the start of a meal.

[augmentin, Other Information] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Other Information: 17 PATIENT COUNSELING INFORMATION Administration Instructions Inform patients that AUGMENTIN may be taken every 8 hours or every 12 hours, depending on the dose prescribed. Each dose should be taken with a meal or snack to reduce the possibility of gastrointestinal upset. Allergic Reactions Counsel patients that AUGMENTIN contains a penicillin class drug product that can cause allergic reactions in some individuals. Severe Cutaneous Adverse Reactions (SCAR ) Advise patients about the signs and symptoms of serious skin manifestations. Instruct patients to stop taking AUGMENTIN immediately and promptly report the first signs or symptoms of skin rash, mucosal lesions, or any other sign of hypersensitivity [see Warnings and Precautions ( 5.2 )] . Diarrhea Counsel patients that diarrhea is a common problem caused by antibacterials, and it usually ends when the antibacterial is discontinued.

[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: Dosing Regimens of AUGMENTIN in Patients with Severe Renal Impairment Patients with Renal Impairment Dosing Regimen GFR 10 mL/min to 30 mL/min 500 mg or 250 mg every 12 hours, depending on the severity of the infection GFR less than 10 mL/min 500 mg or 250 mg every 24 hours, depending on severity of the infection Hemodialysis 500 mg or 250 mg every 24 hours, depending on severity of the infection Administer an additional dose both during and at the end of dialysis 2.5 Directions for Mixing Amoxicillin and Clavulanate Potassium for Oral Suspension Prepare AUGMENTIN for oral suspension at time of dispensing as follows: Tap bottle until all powder flows freely. Measure a total (see Table 5 below for total amount of water for reconstitution) OF WATER. Add approximately 2/3 of the water to the powder. Replace cap and shake VIGOROUSLY. Add remaining water. Replace cap and shake VIGOROUSLY.

[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: 2.2 Adult Patients See dosing regimens of AUGMENTIN (based on the amoxicillin component) provided in Table 1 below. Table 1. Dosing Regimens of AUGMENTIN in Adult Patients TYPE OF INFECTION DOSING REGIMEN OF Amoxicillin and Clavulanate Potassium Severe infections and infections of the respiratory tract one 875 mg tablet a of AUGMENTIN every 12 hours or one 500 mg tablet b,c of AUGMENTIN every 8 hours Less severe infections one 500 mg tablet b,c of AUGMENTIN every 12 hours or one 250 mg tablet d of AUGMENTIN every 8 hours a Adults who have difficulty swallowing may be given the AUGMENTIN 200 mg/28.5 mg per 5 mL suspension or the AUGMENTIN 400 mg/57 mg per 5 mL suspension may be used in place of the 875 mg/125 mg tablet.

[augmentin, Dosage and Administration] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Dosage and Administration: The Amoxicillin and Clavulanate Potassium 200 mg/28.5 mg per 5 mL and Amoxicillin and Clavulanate Potassium 400 mg/57 mg per 5 mL) for oral suspension and Amoxicillin and Clavulanate Potassium 200 mg/28.5 mg and Amoxicillin and Clavulanate Potassium 400 mg/57 mg chewable tablets contain aspartame and should not be used by phenylketonurics. [see Warnings and Precautions ( 5.8)]. Table 3: Dosing in Patients Aged 12 Weeks (3 Months) and Older and Weighing Less than 40 kg Table Patients Weighing 40 kg or More : Pediatric patients weighing 40 kg or more should be dosed according to adult recommendations. The 250 mg/125 mg tablet of AUGMENTIN should NOT be used until the child weighs at least 40 kg, due to the different amoxicillin to clavulanic acid ratios in the 250 mg/125 mg tablet of AUGMENTIN versus the 250 mg/62.5 mg chewable tablet of AUGMENTIN.
```

</details>

## q11 (single)

**Question:** What is the usual adult Bactrim dose for a urinary tract infection?

**Reference:** 1 Bactrim DS tablet (or 2 regular tablets) every 12 hours for 10 to 14 days.

**Agent answer:**

The usual adult dosage of Bactrim for the treatment of urinary tract infections is:

* **1 Bactrim DS (double strength) tablet** or **2 Bactrim tablets** every 12 hours for 10 to 14 days `[bactrim, Dosage and Administration]`.

*(Note: Dosage adjustments are required for patients with renal impairment: use 1/2 the usual regimen for creatinine clearance 15–30 mL/min, and use is not recommended for creatinine clearance below 15 mL/min `[bactrim, Dosage and Administration]`.)*

*gemini-3.8-flash, 1 search(es), 2935 tokens, 26.62 s*

- search `Bactrim urinary tract infection adult dosage` → [bactrim, Dosage and Administration], [bactrim, Dosage and Administration], [bactrim, Dosage and Administration], [bactrim, Dosage and Administration], [bactrim, Indications and Usage]

<details><summary>Retrieved passages</summary>

**search:** `Bactrim urinary tract infection adult dosage`

```text
[bactrim, Dosage and Administration] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Dosage and Administration: DOSAGE AND ADMINISTRATION BACTRIM is contraindicated in pediatric patients less than 2 months of age. Urinary Tract Infections and Shigellosis in Adults and Pediatric Patients, and Acute Otitis Media in Children Adults: The usual adult dosage in the treatment of urinary tract infections is 1 BACTRIM DS (double strength) tablet or 2 BACTRIM tablets every 12 hours for 10 to 14 days. An identical daily dosage is used for 5 days in the treatment of shigellosis. Children: The recommended dose for children with urinary tract infections or acute otitis media is 40 mg/kg sulfamethoxazole and 8 mg/kg trimethoprim per 24 hours, given in two divided doses every 12 hours for 10 days. An identical daily dosage is used for 5 days in the treatment of shigellosis.

[bactrim, Dosage and Administration] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Dosage and Administration: Pneumocystis jirovecii Pneumonia Treatment Adults and Children: The recommended dosage for treatment of patients with documented Pneumocystis jirovecii pneumonia is 75 to 100 mg/kg sulfamethoxazole and 15 to 20 mg/kg trimethoprim per 24 hours given in equally divided doses every 6 hours for 14 to 21 days. 12 The following table is a guideline for the upper limit of this dosage: Weight Dose-every 6 hours lb kg Tablets 18 8 - 35 16 1 53 24 1½ 70 32 2 or 1 DS tablet 88 40 2½ 106 48 3 or 1½ DS tablets 141 64 4 or 2 DS tablets 176 80 5 or 2½ DS tablets For the lower limit dose (75 mg/kg sulfamethoxazole and 15 mg/kg trimethoprim per 24 hours) administer 75% of the dose in the above table. Prophylaxis Adults: The recommended dosage for prophylaxis in adults is 1 BACTRIM DS (double strength) tablet daily.

[bactrim, Dosage and Administration] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Dosage and Administration: The following table is a guideline for the attainment of this dosage: Children 2 months of age or older: Weight Dose-every 12 hours lb kg Tablets 22 10 - 44 20 1 66 30 1½ 88 40 2 or 1 DS tablet For Patients with Impaired Renal Function When renal function is impaired, a reduced dosage should be employed using the following table: Creatinine Clearance (mL/min) Recommended Dosage Regimen Above 30 Usual standard regimen 15-30 ½ the usual regimen Below 15 Use not recommended Acute Exacerbations of Chronic Bronchitis in Adults The usual adult dosage in the treatment of acute exacerbations of chronic bronchitis is 1 BACTRIM DS (double strength) tablet or 2 BACTRIM tablets every 12 hours for 14 days.

[bactrim, Dosage and Administration] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Dosage and Administration: 13 Children: For children, the recommended dose is 750 mg/m 2 /day sulfamethoxazole with 150 mg/m 2 /day trimethoprim given orally in equally divided doses twice a day, on 3 consecutive days per week. The total daily dose should not exceed 1600 mg sulfamethoxazole and 320 mg trimethoprim. 14 The following table is a guideline for the attainment of this dosage in children: Body Surface Area Dose-every 12 hours (m 2 ) Tablets 0.26 - 0.53 ½ 1.06 1 Traveler's Diarrhea in Adults For the treatment of traveler's diarrhea, the usual adult dosage is 1 BACTRIM DS (double strength) tablet or 2 BACTRIM tablets every 12 hours for 5 days.

[bactrim, Indications and Usage] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Indications and Usage: INDICATIONS AND USAGE To reduce the development of drug-resistant bacteria and maintain the effectiveness of BACTRIM (sulfamethoxazole and trimethoprim) tablets and other antibacterial drugs, BACTRIM (sulfamethoxazole and trimethoprim) tablets should be used only to treat or prevent infections that are proven or strongly suspected to be caused by susceptible bacteria. When culture and susceptibility information are available, they should be considered in selecting or modifying antibacterial therapy. In the absence of such data, local epidemiology and susceptibility patterns may contribute to empiric selection of therapy. Urinary Tract Infections For the treatment of urinary tract infections due to susceptible strains of the following organisms: Escherichia coli , Klebsiella species, Enterobacter species, Morganella morganii , Proteus mirabilis and Proteus vulgaris . It is recommended that initial episodes of uncomplicated urinary tract infections be treated with a single effective antibacterial agent rather than the combination.
```

</details>

## q12 (single)

**Question:** Who should not take Bactrim?

**Reference:** People allergic to trimethoprim or sulfonamides; history of drug-induced immune thrombocytopenia from these drugs; megaloblastic anemia from folate deficiency; infants under 2 months; marked liver damage; severe kidney insufficiency when renal function can't be monitored; and anyone taking dofetilide.

**Agent answer:**

According to the Bactrim FDA label, Bactrim is contraindicated in the following individuals and situations:

* **Known hypersensitivity** to trimethoprim or sulfonamides `[bactrim, Contraindications]`.
* **History of drug-induced immune thrombocytopenia** with the use of trimethoprim and/or sulfonamides `[bactrim, Contraindications]`.
* **Documented megaloblastic anemia** due to folate deficiency `[bactrim, Contraindications]`.
* **Pediatric patients less than 2 months of age** `[bactrim, Contraindications]`.
* **Marked hepatic damage** `[bactrim, Contraindications]`.
* **Severe renal insufficiency** when renal function status cannot be monitored `[bactrim, Contraindications]`.
* **Concomitant administration with dofetilide** `[bactrim, Contraindications]`.

### Additional Populations Where Use Should Be Avoided:
The label also notes that use of Bactrim should be avoided in:
* Patients with **porphyria or thyroid dysfunction** `[bactrim, Precautions]`.
* Patients with **impaired renal or hepatic function**, those with **possible folate deficiency** (e.g., the elderly, chronic alcoholics, patients receiving anticonvulsant therapy, patients with malabsorption syndrome, or those in malnutrition states), and those with **severe allergies or bronchial asthma** `[bactrim, Precautions]`.

*gemini-3.8-flash, 1 search(es), 2840 tokens, 10.01 s*

- search `Bactrim contraindications` → [bactrim, Contraindications], [bactrim, Precautions], [bactrim, Precautions], [bactrim, Warnings], [bactrim, Nonteratogenic Effects]

<details><summary>Retrieved passages</summary>

**search:** `Bactrim contraindications`

```text
[bactrim, Contraindications] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Contraindications: CONTRAINDICATIONS BACTRIM is contraindicated in the following situations: a known hypersensitivity to trimethoprim or sulfonamides history of drug-induced immune thrombocytopenia with use of trimethoprim and/or sulfonamides documented megaloblastic anemia due to folate deficiency pediatric patients less than 2 months of age marked hepatic damage severe renal insufficiency when renal function status cannot be monitored concomitant administration with dofetilide (see PRECAUTIONS ).

[bactrim, Precautions] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Precautions: PRECAUTIONS Development of Drug Resistant Bacteria Prescribing BACTRIM (sulfamethoxazole and trimethoprim) tablets in the absence of a proven or strongly suspected bacterial infection or a prophylactic indication is unlikely to provide benefit to the patient and increases the risk of the development of drug-resistant bacteria. Folate Deficiency Avoid use of BACTRIM in patients with impaired renal or hepatic function, in those with possible folate deficiency (e.g., the elderly, chronic alcoholics, patients receiving anticonvulsant therapy, patients with malabsorption syndrome, and patients in malnutrition states) and in those with severe allergies or bronchial asthma. Hematological changes indicative of folic acid deficiency may occur in elderly patients or in patients with preexisting folic acid deficiency or kidney failure. These effects are reversible by folinic acid therapy (see PRECAUTIONS, Geriatric Use ). Hemolysis In glucose-6-phosphate dehydrogenase deficient individuals, hemolysis may occur. This reaction is frequently dose-related.

[bactrim, Precautions] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Precautions: Hypoglycemia Cases of hypoglycemia in non-diabetic patients treated with BACTRIM are seen rarely, usually occurring after a few days of therapy. Patients with renal dysfunction, liver disease, malnutrition or those receiving high doses of BACTRIM are particularly at risk. Impaired Phenylalanine Metabolism The trimethoprim component of BACTRIM has been noted to impair phenylalanine metabolism, but this is of no significance in phenylketonuric patients on appropriate dietary restriction. Porphyria and Hypothyroidism Like other drugs containing sulfonamides, BACTRIM can precipitate porphyria crisis and hypothyroidism. Avoid use of BACTRIM in patients with porphyria or thyroid dysfunction. Potential Risk in the Treatment of Pneumocystis jirovecii Pneumonia in Patients with Acquired Immunodeficiency Syndrome (AIDS) AIDS patients may not tolerate or respond to BACTRIM in the same manner as non-AIDS patients.

[bactrim, Warnings] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Warnings: WARNINGS Embryofetal Toxicity Some epidemiologic studies suggest that exposure to BACTRIM during pregnancy may be associated with an increased risk of congenital malformations, particularly neural tube defects, cardiovascular malformations, urinary tract defects, oral clefts, and club foot. If BACTRIM is used during pregnancy, or if the patient becomes pregnant while taking this drug, the patient should be advised of the potential hazards to the fetus (see PRECAUTIONS ). Hypersensitivity and Other Serious or Fatal Reactions Fatalities and serious adverse reactions including severe cutaneous adverse reactions (SCARs) including Stevens-Johnson syndrome, toxic epidermal necrolysis, drug reaction with eosinophilia and systemic symptoms (DRESS), acute febrile neutrophilic dermatosis (AFND), acute generalized erythematous pustulosis (AGEP); fulminant hepatic necrosis; agranulocytosis, aplastic anemia and other blood dyscrasias; acute and delayed lung injury; anaphylaxis and circulatory shock have occurred with the administration of sulfamethoxazole and trimethoprim products, including BACTRIM (see ADVERSE REACTIONS ).

[bactrim, Nonteratogenic Effects] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Nonteratogenic Effects: Nonteratogenic Effects See CONTRAINDICATIONS section.
```

</details>

## q13 (single)

**Question:** How should the Bactrim dose change for a patient with a creatinine clearance of 20 mL/min?

**Reference:** For CrCl 15-30 mL/min, use half the usual regimen. Below 15 mL/min it is not recommended.

**Agent answer:**

For a patient with impaired renal function and a creatinine clearance of 20 mL/min (which falls within the 15–30 mL/min range), the recommended Bactrim dose is **½ the usual regimen** [bactrim, Dosage and Administration]. 

According to the dosing guidelines for impaired renal function:
* **Above 30 mL/min:** Usual standard regimen [bactrim, Dosage and Administration]
* **15–30 mL/min:** ½ the usual regimen [bactrim, Dosage and Administration]
* **Below 15 mL/min:** Use not recommended [bactrim, Dosage and Administration]

*gemini-3.8-flash, 1 search(es), 3083 tokens, 13.06 s*

- search `Bactrim creatinine clearance renal impairment dosage` → [bactrim, Dosage and Administration], [bactrim, References], [bactrim, Dosage and Administration], [bactrim, Dosage and Administration], [bactrim, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `Bactrim creatinine clearance renal impairment dosage`

```text
[bactrim, Dosage and Administration] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Dosage and Administration: The following table is a guideline for the attainment of this dosage: Children 2 months of age or older: Weight Dose-every 12 hours lb kg Tablets 22 10 - 44 20 1 66 30 1½ 88 40 2 or 1 DS tablet For Patients with Impaired Renal Function When renal function is impaired, a reduced dosage should be employed using the following table: Creatinine Clearance (mL/min) Recommended Dosage Regimen Above 30 Usual standard regimen 15-30 ½ the usual regimen Below 15 Use not recommended Acute Exacerbations of Chronic Bronchitis in Adults The usual adult dosage in the treatment of acute exacerbations of chronic bronchitis is 1 BACTRIM DS (double strength) tablet or 2 BACTRIM tablets every 12 hours for 14 days.

[bactrim, References] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), References: REFERENCES Kremers P, Duvivier J, Heusghem C. Pharmacokinetic Studies of Co-Trimoxazole in Man after Single and Repeated Doses. J Clin Pharmacol . Feb-Mar 1974; 14:112-117. Kaplan SA, et al. Pharmacokinetic Profile of Trimethoprim-Sulfamethoxazole in Man. J Infect Dis . Nov 1973; 128 (Suppl): S547-S555. Varoquaux O, et al. Pharmacokinetics of the trimethoprim-sulfamethoxazole combination in the elderly. Br J Clin Pharmacol . 1985; 20:575-581. Safrin S, Lee BL, Sande MA. Adjunctive folinic acid with trimethoprim-sulfamethoxazole for Pneumocystis carinii pneumonia in AIDS patients is associated with an increased risk of therapeutic failure and death. J Infect Dis . 1994 Oct;170(4):912-7. Marinella Mark A. 1999. Trimethoprim-induced hyperkalemia: An analysis of reported cases. Gerontol . 45:209-212. Margassery, S. and B. Bastani. 2002. Life threatening hyperkalemia and acidosis secondary to trimethoprim-sulfamethoxazole treatment. J. Nephrol . 14:410-414. Moh R, et al.

[bactrim, Dosage and Administration] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Dosage and Administration: Pneumocystis jirovecii Pneumonia Treatment Adults and Children: The recommended dosage for treatment of patients with documented Pneumocystis jirovecii pneumonia is 75 to 100 mg/kg sulfamethoxazole and 15 to 20 mg/kg trimethoprim per 24 hours given in equally divided doses every 6 hours for 14 to 21 days. 12 The following table is a guideline for the upper limit of this dosage: Weight Dose-every 6 hours lb kg Tablets 18 8 - 35 16 1 53 24 1½ 70 32 2 or 1 DS tablet 88 40 2½ 106 48 3 or 1½ DS tablets 141 64 4 or 2 DS tablets 176 80 5 or 2½ DS tablets For the lower limit dose (75 mg/kg sulfamethoxazole and 15 mg/kg trimethoprim per 24 hours) administer 75% of the dose in the above table. Prophylaxis Adults: The recommended dosage for prophylaxis in adults is 1 BACTRIM DS (double strength) tablet daily.

[bactrim, Dosage and Administration] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Dosage and Administration: DOSAGE AND ADMINISTRATION BACTRIM is contraindicated in pediatric patients less than 2 months of age. Urinary Tract Infections and Shigellosis in Adults and Pediatric Patients, and Acute Otitis Media in Children Adults: The usual adult dosage in the treatment of urinary tract infections is 1 BACTRIM DS (double strength) tablet or 2 BACTRIM tablets every 12 hours for 10 to 14 days. An identical daily dosage is used for 5 days in the treatment of shigellosis. Children: The recommended dose for children with urinary tract infections or acute otitis media is 40 mg/kg sulfamethoxazole and 8 mg/kg trimethoprim per 24 hours, given in two divided doses every 12 hours for 10 days. An identical daily dosage is used for 5 days in the treatment of shigellosis.

[bactrim, Drug Interactions] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Drug Interactions: BACTRIM, given at a common clinical dosage, increased the phenytoin half-life by 39% and decreased the phenytoin metabolic clearance rate by 27%. When administering these drugs concurrently, one should be alert for possible excessive phenytoin effect. Methotrexate Avoid concurrent use Sulfonamides can also displace methotrexate from plasma protein binding sites and can compete with the renal transport of methotrexate, thus increasing free methotrexate concentrations. Cyclosporine Avoid concurrent use There have been reports of marked but reversible nephrotoxicity with coadministration of BACTRIM and cyclosporine in renal transplant recipients. Digoxin Monitor serum digoxin levels Increased digoxin blood levels can occur with concomitant BACTRIM therapy, especially in elderly patients. Indomethacin Avoid concurrent use Increased sulfamethoxazole blood levels may occur in patients who are also receiving indomethacin.
```

</details>

## q14 (single)

**Question:** Can a customer take Cipro with a glass of milk?

**Reference:** Not with dairy (milk, yogurt) or calcium-fortified juice alone, because absorption can drop. It can be taken with a meal that contains these products.

**Agent answer:**

**No**, a customer should not take Cipro with a glass of milk alone [cipro, Dosage and Administration], [cipro, Patient Counseling Information]. 

According to the FDA label:
* Concomitant administration of Cipro with dairy products (such as milk or yogurt) or calcium-fortified juices alone should be avoided because the absorption of ciprofloxacin may be significantly reduced [cipro, Dosage and Administration], [cipro, Patient Counseling Information].
* However, Cipro may be taken with a meal that contains these products [cipro, Dosage and Administration], [cipro, Patient Counseling Information].

*gemini-3.8-flash, 1 search(es), 2699 tokens, 39.16 s*

- search `Cipro milk dairy administration food` → [cipro, Dosage and Administration], [cipro, Patient Counseling Information], [cipro, Use in Specific Populations], [cipro, Use in Specific Populations], [cipro, Pregnancy Risks]

<details><summary>Retrieved passages</summary>

**search:** `Cipro milk dairy administration food`

```text
[cipro, Dosage and Administration] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Dosage and Administration: No information is available on dosing adjustments necessary for pediatric patients with moderate to severe renal insufficiency (that is, creatinine clearance of < 50 mL/min/1.73m 2 ). 2.4 Important Administration Instructions With Multivalent Cations Administer CIPRO at least 2 hours before or 6 hours after magnesium/aluminum antacids; polymeric phosphate binders (for example, sevelamer, lanthanum carbonate) or sucralfate; Videx ® (didanosine) chewable/buffered tablets or pediatric powder for oral solution; other highly buffered drugs; or other products containing calcium, iron or zinc. With Dairy Products Concomitant administration of CIPRO with dairy products (like milk or yogurt) or calcium-fortified juices alone should be avoided since decreased absorption is possible; however, CIPRO may be taken with a meal that contains these products. Hydration of Patients Receiving CIPRO Assure adequate hydration of patients receiving CIPRO to prevent the formation of highly concentrated urine. Crystalluria has been reported with quinolones.

[cipro, Patient Counseling Information] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Patient Counseling Information: - After treatment has been completed, CIPRO Oral Suspension should not be reused. Inform patients that CIPRO may be taken with or without food. Inform patients to drink fluids liberally while taking CIPRO to avoid formation of highly concentrated urine and crystal formation in the urine. Inform patients that antacids containing magnesium, or aluminum, as well as sucralfate, metal cations such as iron, and multivitamin preparations with zinc or didanosine should be taken at least two hours before or six hours after CIPRO administration. CIPRO should not be taken with dairy products (like milk or yogurt) or calcium-fortified juices alone since absorption of ciprofloxacin may be significantly reduced; however, CIPRO may be taken with a meal that contains these products. Advise patients that if a dose is missed, it should be taken anytime but not later than 6 hours prior to the next scheduled dose.

[cipro, Use in Specific Populations] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Use in Specific Populations: Because of the potential risk of serious adverse reactions in breastfed infants, including arthropathy shown in juvenile animal studies [see Use in Specific Populations (8.4), (Clinical Considerations)], for most indications a lactating woman may consider pumping and discarding breast milk during treatment with CIPRO and an additional two days (five half-lives) after the last dose. Alternatively, advise a woman that breastfeeding is not recommended during treatment with CIPRO and for an additional two days (five half-lives) after the last dose. However, for inhalation anthrax (post exposure), during an incident resulting in exposure to anthrax, the risk-benefit assessment of continuing breastfeeding while the mother (and potentially the infant) is (are) on CIPRO may be acceptable [see Dosage and Administration ( 2.2 ), Pediatric Use ( 8.4 ), and Clinical Studies ( 14.2 )].

[cipro, Use in Specific Populations] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Use in Specific Populations: 8 USE IN SPECIFIC POPULATIONS Lactation: Breastfeeding is not recommended during treatment, but a lactating woman may pump and discard breastmilk during treatment and an additional 2 days after the last dose. In patients treated for inhalational anthrax (post exposure), consider the risks and benefits of continuing breastfeeding. ( 8.2 ) See full prescribing information for use in pediatric and geriatric patients ( 8.4 , 8.5 ) 8.2 Lactation Risk Summary Published literature reports that ciprofloxacin is present in human milk following intravenous and oral administration . There is no information regarding effects of CIPRO on milk production or the breastfed infant.

[cipro, Pregnancy Risks] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Pregnancy Risks: general population, the estimated background risks of major birth defects and miscarriage in clinically recognized pregnancies is 2 to 4% and 15 to 20%, respectively. Risk Summary Published literature reports that ciprofloxacin is present in human milk following intravenous and oral administration . There is no information regarding effects of CIPRO on milk production or the breastfed infant. Because of the potential risk of serious adverse reactions in breastfed infants, including arthropathy shown in juvenile animal studies [see Use in Specific Populations (8.4), (Clinical Considerations)], for most indications a lactating woman may consider pumping and discarding breast milk during treatment with CIPRO and an additional two days (five half-lives) after the last dose. Alternatively, advise a woman that breastfeeding is not recommended during treatment with CIPRO and for an additional two days (five half-lives) after the last dose.
```

</details>

## q15 (single)

**Question:** How far apart should Cipro and a magnesium/aluminum antacid be taken?

**Reference:** Take Cipro at least 2 hours before or 6 hours after antacids or other products with multivalent cations (calcium, iron, zinc, sucralfate, etc.).

**Agent answer:**

Cipro should be administered at least **2 hours before** or **6 hours after** taking magnesium/aluminum antacids `[cipro, Dosage and Administration]`, `[cipro, Drug Interactions]`. 

Concomitant administration can decrease Cipro absorption, resulting in lower serum and urine drug levels `[cipro, Drug Interactions]`.

*gemini-3.8-flash, 1 search(es), 2654 tokens, 19.04 s*

- search `Cipro antacid magnesium aluminum spacing administration` → [cipro, Drug Interactions], [cipro, Drug Interactions], [cipro, Patient Counseling Information], [cipro, Dosage and Administration], [cipro, Overdosage]

<details><summary>Retrieved passages</summary>

**search:** `Cipro antacid magnesium aluminum spacing administration`

```text
[cipro, Drug Interactions] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Drug Interactions: Duloxetine Avoid Use Five-fold increase in duloxetine exposure If unavoidable, monitor for duloxetine toxicity Caffeine/Xanthine Derivatives Use with caution Reduced clearance resulting in elevated levels and prolongation of serum half-life CIPRO inhibits the formation of paraxanthine after caffeine administration (or pentoxifylline containing products). Monitor for xanthine toxicity and adjust dose as necessary. Zolpidem Avoid Use Co-administration with ciprofloxacin may increase blood levels of zolpidem, concurrent use is not recommended Drug(s) Affecting Pharmacokinetics of CIPRO Antacids, Sucralfate, Multivitamins and Other Products Containing Multivalent Cations (magnesium/aluminum antacids; polymeric phosphate binders (for example, sevelamer, lanthanum carbonate); sucralfate; Videx ® (didanosine) chewable/buffered tablets or pediatric powder; other highly buffered drugs; or products containing calcium, iron, or zinc and dairy products) CIPRO should be taken at least two hours before or six hours after Multivalent cation-containing products administration [see Dosage and Administration ( 2.4 )].

[cipro, Drug Interactions] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Drug Interactions: Decrease CIPRO absorption, resulting in lower serum and urine levels Probenecid Use with caution (interferes with renal tubular secretion of CIPRO and increases CIPRO serum levels) Potentiation of CIPRO toxicity may occur. Interacting Drug Interaction Theophylline Serious and fatal reactions. Avoid concomitant use. Monitor serum level ( 7 ) Warfarin Anticoagulant effect enhanced. Monitor prothrombin time, INR, and bleeding ( 7 ) Antidiabetic agents Hypoglycemia including fatal outcomes have been reported. Monitor blood glucose ( 7 ) Phenytoin Monitor phenytoin level ( 7 ) Methotrexate Monitor for methotrexate toxicity ( 7 ) Cyclosporine May increase serum creatinine. Monitor serum creatinine ( 7 ) Multivalent cation-containing products including antacids, metal cations or didanosine Decreased CIPRO absorption. Take CIPRO 2 hours before or 6 hours after administration of multivalent cation containing drugs ( 7 )

[cipro, Patient Counseling Information] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Patient Counseling Information: - After treatment has been completed, CIPRO Oral Suspension should not be reused. Inform patients that CIPRO may be taken with or without food. Inform patients to drink fluids liberally while taking CIPRO to avoid formation of highly concentrated urine and crystal formation in the urine. Inform patients that antacids containing magnesium, or aluminum, as well as sucralfate, metal cations such as iron, and multivitamin preparations with zinc or didanosine should be taken at least two hours before or six hours after CIPRO administration. CIPRO should not be taken with dairy products (like milk or yogurt) or calcium-fortified juices alone since absorption of ciprofloxacin may be significantly reduced; however, CIPRO may be taken with a meal that contains these products. Advise patients that if a dose is missed, it should be taken anytime but not later than 6 hours prior to the next scheduled dose.

[cipro, Dosage and Administration] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Dosage and Administration: No information is available on dosing adjustments necessary for pediatric patients with moderate to severe renal insufficiency (that is, creatinine clearance of < 50 mL/min/1.73m 2 ). 2.4 Important Administration Instructions With Multivalent Cations Administer CIPRO at least 2 hours before or 6 hours after magnesium/aluminum antacids; polymeric phosphate binders (for example, sevelamer, lanthanum carbonate) or sucralfate; Videx ® (didanosine) chewable/buffered tablets or pediatric powder for oral solution; other highly buffered drugs; or other products containing calcium, iron or zinc. With Dairy Products Concomitant administration of CIPRO with dairy products (like milk or yogurt) or calcium-fortified juices alone should be avoided since decreased absorption is possible; however, CIPRO may be taken with a meal that contains these products. Hydration of Patients Receiving CIPRO Assure adequate hydration of patients receiving CIPRO to prevent the formation of highly concentrated urine. Crystalluria has been reported with quinolones.

[cipro, Overdosage] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Overdosage: 10 OVERDOSAGE In the event of acute overdosage, reversible renal toxicity has been reported in some cases. Empty the stomach by inducing vomiting or by gastric lavage. Observe the patient carefully and give supportive treatment, including monitoring of renal function, urinary pH and acidify, if required, to prevent crystalluria and administration of magnesium, aluminum, or calcium containing antacids which can reduce the absorption of ciprofloxacin. Adequate hydration must be maintained. Only a small amount of ciprofloxacin (less than 10%) is removed from the body after hemodialysis or peritoneal dialysis.
```

</details>

## q16 (single)

**Question:** What serious side effects does the Cipro boxed warning describe?

**Reference:** Tendinitis and tendon rupture, peripheral neuropathy, CNS effects, and worsening of myasthenia gravis. Stop Cipro right away if these happen, and avoid it in patients with a history of myasthenia gravis.

**Agent answer:**

According to the Cipro **Boxed Warning**, the serious adverse reactions described are:

* **Disabling and potentially irreversible serious adverse reactions** that have occurred together, including:
  * **Tendinitis and tendon rupture** `[cipro, Boxed Warning]`
  * **Peripheral neuropathy** `[cipro, Boxed Warning]`
  * **Central nervous system effects** `[cipro, Boxed Warning]`
* **Exacerbation of myasthenia gravis:** Fluoroquinolones, including Cipro, may exacerbate muscle weakness in patients with myasthenia gravis; therefore, Cipro should be avoided in patients with a known history of myasthenia gravis `[cipro, Boxed Warning]`.

*gemini-3.8-flash, 1 search(es), 2930 tokens, 15.34 s*

- search `Cipro boxed warning serious side effects` → [cipro, Boxed Warning], [cipro, Boxed Warning], [cipro, Boxed Warning], [cipro, Warnings and Precautions], [cipro, Patient Counseling Information]

<details><summary>Retrieved passages</summary>

**search:** `Cipro boxed warning serious side effects`

```text
[cipro, Boxed Warning] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Boxed Warning: WARNING: SERIOUS ADVERSE REACTIONS INCLUDING TENDINITIS, TENDON RUPTURE, PERIPHERAL NEUROPATHY, CENTRAL NERVOUS SYSTEM EFFECTS AND EXACERBATION OF MYASTHENIA GRAVIS - Fluoroquinolones, including CIPRO ® , have been associated with disabling and potentially irreversible serious adverse reactions that have occurred together [see Warnings and Precautions ( 5.1 )], including: - Tendinitis and tendon rupture [see Warnings and Precautions ( 5.2 )]. - Peripheral neuropathy [see Warnings and Precautions ( 5.3 )]. - Central nervous system effects [see Warnings and Precautions ( 5.4 )]. Discontinue CIPRO immediately and avoid the use of fluoroquinolones, including CIPRO, in patients who experience any of these serious adverse reactions [see Warnings and Precautions ( 5.1 )] . - Fluoroquinolones, including CIPRO, may exacerbate muscle weakness in patients with myasthenia gravis. Avoid CIPRO in patients with known history of myasthenia gravis . [see Warnings and Precautions ( 5.5 )].

[cipro, Boxed Warning] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Boxed Warning: - Fluoroquinolones, including CIPRO ® , have been associated with disabling and potentially irreversible serious adverse reactions that have occurred together ( 5.1 ), including: - Tendinitis and tendon rupture ( 5.2 ) - Peripheral neuropathy ( 5.3 ) - Central nervous system effects ( 5.4 ) Discontinue CIPRO immediately and avoid the use of fluoroquinolones, including CIPRO, in patients who experience any of these serious adverse reactions ( 5.1 ) - Fluoroquinolones, including CIPRO, may exacerbate muscle weakness in patients with myasthenia gravis. Avoid CIPRO in patients with known history of myasthenia gravis. ( 5.5 ) - Because fluoroquinolones, including CIPRO, have been associated with serious adverse reactions ( 5.1-5.16 ), reserve CIPRO for use in patients who have no alternative treatment options for the following indications: - Acute exacerbation of chronic bronchitis ( 1.10 ) - Acute uncomplicated cystitis ( 1.11 ) Acute sinusitis ( 1.12 )

[cipro, Boxed Warning] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Boxed Warning: - Because fluoroquinolones, including CIPRO, have been associated with serious adverse reactions [see Warnings and Precautions ( 5.1-5.16 )] , reserve CIPRO for use in patients who have no alternative treatment options for the following indications: - Acute exacerbation of chronic bronchitis [see Indications and Usage ( 1.10 )]. - Acute uncomplicated cystitis [see Indications and Usage ( 1.11 )]. - Acute sinusitis [see Indications and Usage ( 1.12 )]. WARNING: SERIOUS ADVERSE REACTIONS INCLUDING TENDINITIS, TENDON RUPTURE, PERIPHERAL NEUROPATHY, CENTRAL NERVOUS SYSTEM EFFECTS AND EXACERBATION OF MYASTHENIA GRAVIS See full prescribing information for complete boxed warning.

[cipro, Warnings and Precautions] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Warnings and Precautions: ( 5.12 , 7 , 8.5 ) 5.1 Disabling and Potentially Irreversible Serious Adverse Reactions Including Tendinitis and Tendon Rupture, Peripheral Neuropathy, and Central Nervous System Effects Fluoroquinolones, including CIPRO, have been associated with disabling and potentially irreversible serious adverse reactions from different body systems that can occur together in the same patient. Commonly seen adverse reactions include tendinitis, tendon rupture, arthralgia, myalgia, peripheral neuropathy, and central nervous system effects (hallucinations, anxiety, depression, insomnia, severe headaches, and confusion). These reactions can occur within hours to weeks after starting CIPRO. Patients of any age or without pre-existing risk factors have experienced these adverse reactions [see Warnings and Precautions ( 5.2 , 5.3 , 5.4 )] . Discontinue CIPRO immediately at the first signs or symptoms of any serious adverse reaction.

[cipro, Patient Counseling Information] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Patient Counseling Information: - Tendinitis and tendon rupture: Instruct patients to contact their healthcare provider if they experience pain, swelling, or inflammation of a tendon, or weakness or inability to use one of their joints; rest and refrain from exercise; and discontinue CIPRO treatment. Symptoms may be irreversible. The risk of severe tendon disorder with fluoroquinolones is higher in older patients usually over 60 years of age, in patients taking corticosteroid drugs, and in patients with kidney, heart or lung transplants. - Peripheral Neuropathies: Inform patients that peripheral neuropathies have been associated with ciprofloxacin use, symptoms may occur soon after initiation of therapy and may be irreversible. If symptoms of peripheral neuropathy including pain, burning, tingling, numbness and/or weakness develop, immediately discontinue CIPRO and tell them to contact their physician.
```

</details>

## q17 (single)

**Question:** Can a patient on tizanidine be given Cipro?

**Reference:** No. The combination is contraindicated because Cipro increases tizanidine's blood-pressure-lowering and sedative effects.

**Agent answer:**

**No, a patient taking tizanidine should not be given Cipro.** 

Concomitant administration of Cipro with tizanidine is **contraindicated** `[cipro, Contraindications]`. 

* **Mechanism and Risk:** Ciprofloxacin is an inhibitor of human cytochrome P450 1A2 (CYP1A2) metabolism. Co-administration is contraindicated because it leads to the potentiation of the hypotensive and sedative effects of tizanidine `[cipro, Drug Interactions]`.
* **Counseling:** Patients must be instructed not to take ciprofloxacin if they are already taking tizanidine, as Cipro increases the effects of tizanidine `[cipro, Patient Counseling Information]`.

*gemini-3.8-flash, 1 search(es), 2816 tokens, 505.3 s*

- search `Cipro tizanidine` → [cipro, Drug Interactions], [cipro, Contraindications], [cipro, Patient Counseling Information], [cipro, Indications and Usage], [cipro, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `Cipro tizanidine`

```text
[cipro, Drug Interactions] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Drug Interactions: 7 DRUG INTERACTIONS Ciprofloxacin is an inhibitor of human cytochrome P450 1A2 (CYP1A2) mediated metabolism. Co-administration of CIPRO with other drugs primarily metabolized by CYP1A2 results in increased plasma concentrations of these drugs and could lead to clinically significant adverse events of the co-administered drug. Table 11: Drugs That are Affected by and Affecting CIPRO Drugs That are Affected by CIPRO Drug(s) Recommendation Comments Tizanidine Contraindicated Concomitant administration of tizanidine and CIPRO is contraindicated due to the potentiation of hypotensive and sedative effects of tizanidine [ see Contraindications ( 4.2 ) ] Theophylline Avoid Use (Plasma Exposure Likely to be Increased and Prolonged) Concurrent administration of CIPRO with theophylline may result in increased risk of a patient developing central nervous system (CNS) or other adverse reactions. If concomitant use cannot be avoided, monitor serum levels of theophylline and adjust dosage as appropriate [see Warnings and Precautions ( 5.10 )].

[cipro, Contraindications] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Contraindications: 4 CONTRAINDICATIONS - Known hypersensitivity to CIPRO or other quinolones ( 4.1 , 5.6 , 5.7) - Concomitant administration with tizanidine ( 4.2 ) 4.1 Hypersensitivity CIPRO is contraindicated in persons with a history of hypersensitivity to ciprofloxacin, any member of the quinolone class of antibacterials, or any of the product components [see Warnings and Precautions ( 5.7 )]. 4.2 Tizanidine Concomitant administration with tizanidine is contraindicated [see Drug Interactions ( 7 )].

[cipro, Patient Counseling Information] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Patient Counseling Information: Instruct patients to notify their physician if they have any symptoms of prolongation of the QT interval, including prolonged heart palpitations or a loss of consciousness. - Musculoskeletal Disorders in Pediatric Patients: Instruct parents to inform their child's physician if the child has a history of joint-related problems before taking this drug. Inform parents of pediatric patients to notify their child's physician of any joint-related problems that occur during or following ciprofloxacin therapy [see Warnings and Precautions ( 5.13 ) and Use in Specific Populations ( 8.4 )]. - Tizanidine: Instruct patients not to use ciprofloxacin if they are already taking tizanidine. CIPRO increases the effects of tizanidine (Zanaflex ® ). - Theophylline: Inform patients that ciprofloxacin CIPRO may increase the effects of theophylline. Life-threatening CNS effects and arrhythmias can occur. Advise the patients to immediately seek medical help if they experience seizures, palpitations, or difficulty breathing.

[cipro, Indications and Usage] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Indications and Usage: 1 INDICATIONS AND USAGE CIPRO is a fluoroquinolone antibacterial indicated in adults (18 years of age and older) with the following infections caused by designated, susceptible bacteria and in pediatric patients where indicated: - Skin and Skin Structure Infections ( 1.1 ) - Bone and Joint Infections ( 1.2 ) - Complicated Intra-Abdominal Infections ( 1.3 ) - Infectious Diarrhea ( 1.4 ) - Typhoid Fever (Enteric Fever) ( 1.5 ) - Uncomplicated Cervical and Urethral Gonorrhea ( 1.6 ) - Inhalational Anthrax post-exposure in adult and pediatric patients ( 1.7) - Plague in adult and pediatric patients ( 1.8 ) - Chronic Bacterial Prostatitis ( 1.9 ) - Lower Respiratory Tract Infections ( 1.10 ) - Acute Exacerbation of Chronic Bronchitis - Urinary Tract Infections ( 1.11 ) - Urinary Tract Infections (UTI) - Acute Uncomplicated Cystitis - Complicated UTI and Pyelonephritis in Pediatric Patients - Acute Sinusitis (

[cipro, Drug Interactions] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Drug Interactions: Duloxetine Avoid Use Five-fold increase in duloxetine exposure If unavoidable, monitor for duloxetine toxicity Caffeine/Xanthine Derivatives Use with caution Reduced clearance resulting in elevated levels and prolongation of serum half-life CIPRO inhibits the formation of paraxanthine after caffeine administration (or pentoxifylline containing products). Monitor for xanthine toxicity and adjust dose as necessary. Zolpidem Avoid Use Co-administration with ciprofloxacin may increase blood levels of zolpidem, concurrent use is not recommended Drug(s) Affecting Pharmacokinetics of CIPRO Antacids, Sucralfate, Multivitamins and Other Products Containing Multivalent Cations (magnesium/aluminum antacids; polymeric phosphate binders (for example, sevelamer, lanthanum carbonate); sucralfate; Videx ® (didanosine) chewable/buffered tablets or pediatric powder; other highly buffered drugs; or products containing calcium, iron, or zinc and dairy products) CIPRO should be taken at least two hours before or six hours after Multivalent cation-containing products administration [see Dosage and Administration ( 2.4 )].
```

</details>

## q18 (single)

**Question:** What is the adult Zithromax dose for non-gonococcal urethritis and cervicitis?

**Reference:** A single 1 gram dose.

**Agent answer:**

The recommended adult dosage of Zithromax for non-gonococcal urethritis and cervicitis is a single 1 gram dose [zithromax, Dosage and Administration].

*gemini-3.8-flash, 1 search(es), 2654 tokens, 464.82 s*

- search `Zithromax non-gonococcal urethritis cervicitis dose adult` → [zithromax, Dosage and Administration], [zithromax, Dosage and Administration], [zithromax, Indications and Usage], [zithromax, Indications and Usage], [zithromax, Warnings and Precautions]

<details><summary>Retrieved passages</summary>

**search:** `Zithromax non-gonococcal urethritis cervicitis dose adult`

```text
[zithromax, Dosage and Administration] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Dosage and Administration: 2 DOSAGE AND ADMINISTRATION Recommended Dosage for Adult Patients ( 2.1 ) Infection Recommended Dose/Duration of Therapy Community-acquired pneumonia (mild severity) Pharyngitis/tonsillitis (second-line therapy) Skin/skin structure (uncomplicated) 500 mg as a single dose on Day 1, followed by 250 mg once daily on Days 2 through 5. Acute bacterial exacerbations of chronic bronchitis (mild to moderate) 500 mg as a single dose on Day 1, followed by 250 mg once daily on Days 2 through 5 or 500 mg once daily for 3 days. Acute bacterial sinusitis 500 mg once daily for 3 days. Genital ulcer disease (chancroid) Non-gonococcal urethritis and cervicitis One single 1 gram dose. Gonococcal urethritis and cervicitis One single 2 gram dose.

[zithromax, Dosage and Administration] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Dosage and Administration: Recommended Dose/Duration of Therapy Community-acquired pneumonia Pharyngitis/tonsillitis (second-line therapy) Skin/skin structure (uncomplicated) 500 mg as a single dose on Day 1, followed by 250 mg once daily on Days 2 through 5 Acute bacterial exacerbations of chronic obstructive pulmonary disease 500 mg once daily for 3 days OR 500 mg as a single dose on Day 1, followed by 250 mg once daily on Days 2 through 5 Acute bacterial sinusitis 500 mg once daily for 3 days Genital ulcer disease (chancroid) One single 1 gram dose Non-gonococcal urethritis and cervicitis One single 1 gram dose Gonococcal urethritis and cervicitis One single 2 gram dose 2.2 Recommended Dosage for Pediatric Patients Recommended dosages and durations of therapy in pediatric patient populations vary by indications [see Indications and Usage (1.2) and Clinical Pharmacology (12.3) ] . ZITHROMAX for oral suspension can be taken with or without food. Table 2.

[zithromax, Indications and Usage] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Indications and Usage: 1 INDICATIONS AND USAGE ZITHROMAX is a macrolide antibacterial drug indicated for treatment of patients with mild to moderate infections caused by susceptible strains of the designated microorganisms in the specific conditions listed below: - Acute bacterial exacerbations of chronic bronchitis in adults ( 1.1 ) - Acute bacterial sinusitis in adults ( 1.1 ) - Uncomplicated skin and skin structure infections in adults ( 1.1 ) - Urethritis and cervicitis in adults ( 1.1 ) - Genital ulcer disease in men ( 1.1 ) - Acute otitis media in pediatric patients (6 months of age and older) ( 1.2 ) - Community-acquired pneumonia in adults and pediatric patients (6 months of age and older) ( 1.1 , 1.2 ) - Pharyngitis/tonsillitis in adults and pediatric patients (2 years of age and older) ( 1.1 , 1.2 ) Limitation of Use: ZITHROMAX is not recommended in patients with pneumonia who

[zithromax, Indications and Usage] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Indications and Usage: - Community-acquired pneumonia due to Chlamydophila pneumoniae , Haemophilus influenzae , Mycoplasma pneumoniae , or Streptococcus pneumoniae in patients appropriate for oral therapy. - Pharyngitis/tonsillitis caused by Streptococcus pyogenes as an alternative to first-line therapy in individuals who cannot use first-line therapy. - Uncomplicated skin and skin structure infections due to Staphylococcus aureus , Streptococcus pyogenes , or Streptococcus agalactiae . - Urethritis and cervicitis due to Chlamydia trachomatis or Neisseria gonorrhoeae . - Genital ulcer disease in men due to Haemophilus ducreyi (chancroid). Due to the small number of women included in clinical trials, the efficacy of azithromycin in the treatment of chancroid in women has not been established.

[zithromax, Warnings and Precautions] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Warnings and Precautions: Appropriate fluid and electrolyte management, protein supplementation, antibiotic treatment of C. difficile , and surgical evaluation should be instituted as clinically indicated. 5.7 Exacerbation of Myasthenia Gravis Exacerbation of symptoms of myasthenia gravis and new onset of myasthenic syndrome have been reported in patients receiving azithromycin therapy. 5.8 Risk of Antibacterial Resistance in Sexually Transmitted Infections ZITHROMAX, at the recommended dose, should not be relied upon to treat syphilis. Antibacterial agents used to treat non-gonococcal urethritis may mask or delay the symptoms of incubating syphilis. All patients with sexually transmitted urethritis or cervicitis should have a serologic test for syphilis and appropriate testing for gonorrhea performed at the time of diagnosis. Appropriate antibacterial therapy and follow-up tests for these diseases should be initiated if infection is confirmed.
```

</details>

## q19 (single)

**Question:** Does Zithromax need to be taken with food?

**Reference:** No. Zithromax tablets and oral suspension can be taken with or without food.

**Agent answer:**

No, Zithromax does not need to be taken with food. 

According to the FDA label, Zithromax tablets and Zithromax for oral suspension can be taken **with or without food** [zithromax, Dosage and Administration], [zithromax, Patient Counseling Information], [zithromax, Patient Information].

*gemini-3.8-flash, 1 search(es), 2648 tokens, 890.89 s*

- search `Zithromax food administration` → [zithromax, Dosage and Administration], [zithromax, Dosage and Administration], [zithromax, Patient Counseling Information], [zithromax, Indications and Usage], [zithromax, Patient Information]

<details><summary>Retrieved passages</summary>

**search:** `Zithromax food administration`

```text
[zithromax, Dosage and Administration] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Dosage and Administration: Recommended Dose/Duration of Therapy Community-acquired pneumonia Pharyngitis/tonsillitis (second-line therapy) Skin/skin structure (uncomplicated) 500 mg as a single dose on Day 1, followed by 250 mg once daily on Days 2 through 5 Acute bacterial exacerbations of chronic obstructive pulmonary disease 500 mg once daily for 3 days OR 500 mg as a single dose on Day 1, followed by 250 mg once daily on Days 2 through 5 Acute bacterial sinusitis 500 mg once daily for 3 days Genital ulcer disease (chancroid) One single 1 gram dose Non-gonococcal urethritis and cervicitis One single 1 gram dose Gonococcal urethritis and cervicitis One single 2 gram dose 2.2 Recommended Dosage for Pediatric Patients Recommended dosages and durations of therapy in pediatric patient populations vary by indications [see Indications and Usage (1.2) and Clinical Pharmacology (12.3) ] . ZITHROMAX for oral suspension can be taken with or without food. Table 2.

[zithromax, Dosage and Administration] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Dosage and Administration: ZITHROMAX tablets and ZITHROMAX for oral suspension can be taken with or without food. Table 1. Recommended dosage for Adult Patients by Indication Infection Due to the indicated microorganisms [see Indications and Usage (1.1) ].

[zithromax, Patient Counseling Information] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Patient Counseling Information: 17 PATIENT COUNSELING INFORMATION Advise the patient to read the FDA-approved patient labeling (Patient Information). Important Administration Instructions ZITHROMAX tablets and oral suspension can be taken with or without food. Concomitant Administration with Aluminum and Magnesium Containing Antacids Advise patients not to take aluminum and magnesium containing antacids and azithromycin simultaneously. Allergic Reactions Direct patients to discontinue azithromycin immediately and contact a physician if any signs of an allergic reaction occur [see warnings and Precautions (5.1) ] . Vomiting, Irritability, Diarrhea or Rash with Feeding in Infants Direct parents or caregivers to contact their physician if vomiting, irritability, diarrhea or rash with feeding occurs in the infant [see Warnings and Precautions (5.3) and Use in Specific Population (8.2) ] . Antibacterial Resistance Patients should be counseled that antibacterial drugs including ZITHROMAX should only be used to treat bacterial infections. They do not treat viral infections (e.g., the common cold).

[zithromax, Indications and Usage] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Indications and Usage: 1 INDICATIONS AND USAGE ZITHROMAX is a macrolide antibacterial drug indicated for treatment of patients with mild to moderate infections caused by susceptible strains of the designated microorganisms in the specific conditions listed below: - Acute bacterial exacerbations of chronic bronchitis in adults ( 1.1 ) - Acute bacterial sinusitis in adults ( 1.1 ) - Uncomplicated skin and skin structure infections in adults ( 1.1 ) - Urethritis and cervicitis in adults ( 1.1 ) - Genital ulcer disease in men ( 1.1 ) - Acute otitis media in pediatric patients (6 months of age and older) ( 1.2 ) - Community-acquired pneumonia in adults and pediatric patients (6 months of age and older) ( 1.1 , 1.2 ) - Pharyngitis/tonsillitis in adults and pediatric patients (2 years of age and older) ( 1.1 , 1.2 ) Limitation of Use: ZITHROMAX is not recommended in patients with pneumonia who

[zithromax, Patient Information] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Patient Information: Tell your healthcare provider about all the medicines you take, including prescription and over-the-counter medicines, vitamins, and herbal supplements. ZITHROMAX and other medicines may affect each other causing side effects. ZITHROMAX may affect the way other medicines work, and other medicines may affect how ZITHROMAX works. Especially tell your healthcare provider if you take: - nelfinavir - a blood thinner (warfarin) - digoxin - colchicine - phenytoin - an antacid that contains aluminum or magnesium Know the medicines you take. Keep a list of your medicines and show it to your healthcare provider and pharmacist when you get a new medicine. How should I take ZITHROMAX? - Take ZITHROMAX exactly as your healthcare provider tells you to take it. - ZITHROMAX can be taken with or without food. - If you take ZITHROMAX oral suspension, shake the bottle well just before you take it.
```

</details>

## q20 (single)

**Question:** Which patients need extra caution with Zithromax because of heart rhythm risk?

**Reference:** Patients with known QT prolongation or a history of torsades de pointes, proarrhythmic conditions, or other QT-prolonging drugs, because QT prolongation and torsades (which can be fatal) have been reported.

**Agent answer:**

According to the Zithromax label, healthcare providers should consider the fatal risk of QT prolongation and torsades de pointes when weighing risks and benefits for the following at-risk patient groups:

* **Patients with preexisting cardiac conditions:**
  * Known prolongation of the QT interval `[zithromax, Warnings and Precautions]` (or a family history of prolonged QT interval `[zithromax, Patient Information]`)
  * History of torsades de pointes `[zithromax, Warnings and Precautions]`
  * Congenital long QT syndrome `[zithromax, Warnings and Precautions]`
  * Bradyarrhythmias or clinically significant bradycardia `[zithromax, Warnings and Precautions]`
  * Uncompensated heart failure `[zithromax, Warnings and Precautions]`

* **Patients with electrolyte imbalances / proarrhythmic conditions:**
  * Uncorrected hypokalemia (low blood potassium) or uncorrected hypomagnesemia `[zithromax, Warnings and Precautions]`, `[zithromax, Patient Information]`

* **Patients taking certain interacting medications:**
  * Drugs known to prolong the QT interval `[zithromax, Warnings and Precautions]`
  * Class IA antiarrhythmic agents (e.g., quinidine, procainamide) `[zithromax, Warnings and Precautions]`
  * Class III antiarrhythmic agents (e.g., dofetilide, amiodarone, sotalol) `[zithromax, Warnings and Precautions]`

* **Elderly patients:**
  * Older individuals may be more susceptible to drug-associated effects on the QT interval and the development of torsades de pointes arrhythmias `[zithromax, Warnings and Precautions]`, `[zithromax, Geriatric Use]`.

*gemini-3.8-flash, 2 search(es), 6430 tokens, 637.06 s*

- search `Zithromax heart rhythm QT prolongation risk` → [zithromax, Warnings and Precautions], [zithromax, Patient Information], [zithromax, Warnings and Precautions], [zithromax, Adverse Reactions], [zithromax, Warnings and Precautions]
- search `Zithromax Geriatric Use QT interval` → [zithromax, Geriatric Use], [zithromax, Warnings and Precautions], [zithromax, Warnings and Precautions], [zithromax, Use in Specific Populations], [zithromax, Patient Information]

<details><summary>Retrieved passages</summary>

**search:** `Zithromax heart rhythm QT prolongation risk`

```text
[zithromax, Warnings and Precautions] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Warnings and Precautions: Direct parents and caregivers to contact their physician if vomiting or irritability with feeding occurs. 5.4 QT Prolongation Prolonged cardiac repolarization and QT interval, imparting a risk of developing cardiac arrhythmia and torsades de pointes, have been seen with treatment with macrolides, including azithromycin. Cases of torsades de pointes have been spontaneously reported during postmarketing surveillance in patients receiving azithromycin. Providers should consider the risk of QT prolongation which can be fatal when weighing the risks and benefits of azithromycin for at-risk groups including: - patients with known prolongation of the QT interval, a history of torsades de pointes, congenital long QT syndrome, bradyarrhythmias or uncompensated heart failure - patients on drugs known to prolong the QT interval - patients with ongoing proarrhythmic conditions such as uncorrected hypokalemia or hypomagnesemia, clinically significant bradycardia, and in patients receiving Class IA (quinidine, procainamide) or Class III (dofetilide, amiodarone, sotalol) antiarrhythmic agents.

[zithromax, Patient Information] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Patient Information: Tell your healthcare provider right away if you or your child feel a fast or irregular heartbeat, get dizzy or faint. ZITHROMAX may cause a rare heart problem known as prolongation of the QT interval. This condition can cause an abnormal heartbeat and can be very dangerous. The chances of this happening are higher in people: o who are elderly o with a family history of prolonged QT interval o with low blood potassium o who take certain medicines to control heart rhythm (antiarrhythmics) - Diarrhea. Tell your healthcare provider right away if you have watery diarrhea, diarrhea that does not go away, or bloody stools. You may experience cramping and a fever. This could happen as late as 2 or more months after you have finished your treatment with ZITHROMAX. - Worsening of myasthenia gravis (a problem that causes muscle weakness).

[zithromax, Warnings and Precautions] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Warnings and Precautions: Elderly patients may be more susceptible to drug-associated effects on the QT interval. 5.5 Cardiovascular Death Some observational studies have shown an approximately two-fold increased short-term potential risk of acute cardiovascular death in adults exposed to azithromycin relative to other antibacterial drugs, including amoxicillin. The five-day cardiovascular mortality observed in these studies ranged from 20 to 400 per million azithromycin treatment courses. This potential risk was noted to be greater during the first five days of azithromycin use and does not appear to be limited to those patients with preexisting cardiovascular diseases. The data in these observational studies are insufficient to establish or exclude a causal relationship between acute cardiovascular death and azithromycin use. Consider balancing this potential risk with treatment benefits when prescribing ZITHROMAX.

[zithromax, Adverse Reactions] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Adverse Reactions: 6.2 Postmarketing Experience The following adverse reactions have been identified during post-approval use of azithromycin. Because these reactions are reported voluntarily from a population of uncertain size, it is not always possible to reliably estimate their frequency or establish a causal relationship to drug exposure. Adverse reactions reported with azithromycin during the postmarketing period in adult and/or pediatric patients for which a causal relationship may not be established include: Allergic: Arthralgia, edema, urticaria, and angioedema. Cardiovascular: Arrhythmias including ventricular tachycardia and hypotension. There have been reports of QT prolongation, torsades de pointes, and cardiovascular death. Gastrointestinal: Anorexia, constipation, dyspepsia, flatulence, vomiting/diarrhea, pseudomembranous colitis, pancreatitis, oral candidiasis, pyloric stenosis, and reports of tongue discoloration. General: Asthenia, paresthesia, fatigue, malaise, and anaphylaxis. Genitourinary: Interstitial nephritis and acute renal failure and vaginitis. Hematopoietic: Thrombocytopenia. Liver/Biliary: Abnormal liver function, hepatitis, cholestatic jaundice, hepatic necrosis, and hepatic failure.

[zithromax, Warnings and Precautions] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Warnings and Precautions: 5 WARNINGS AND PRECAUTIONS - Serious (including fatal) allergic and skin reactions: Discontinue ZITHROMAX if reaction occurs. ( 5.1 ) - Hepatotoxicity: Severe, and sometimes fatal, hepatotoxicity has been reported. Discontinue ZITHROMAX immediately if signs and symptoms of hepatitis occur. ( 5.2 ) - Infantile Hypertrophic Pyloric Stenosis (IHPS): Following the use of azithromycin in neonates (treatment up to 42 days of life), IHPS has been reported. Direct parents and caregivers to contact their physician if vomiting or irritability with feeding occurs. ( 5.3 ) - Prolongation of QT interval and cases of torsades de pointes have been reported. This risk which can be fatal should be considered in patients with certain cardiovascular disorders including known QT prolongation or history torsades de pointes, those with proarrhythmic conditions, and with other drugs that prolong the QT interval.
```

**search:** `Zithromax Geriatric Use QT interval`

```text
[zithromax, Geriatric Use] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Geriatric Use: 8.5 Geriatric Use In multiple-dose clinical trials of oral azithromycin, 9% of patients were at least 65 years of age (458/4949) and 3% of patients (144/4949) were at least 75 years of age. No overall differences in safety or effectiveness were observed between these subjects and younger subjects, and other reported clinical experience has not identified differences in response between the elderly and younger patients, but greater sensitivity of some older individuals cannot be ruled out. Elderly patients may be more susceptible to development of torsades de pointes arrhythmias than younger patients. [see Warnings and Precautions (5.4) ]

[zithromax, Warnings and Precautions] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Warnings and Precautions: Elderly patients may be more susceptible to drug-associated effects on the QT interval. 5.5 Cardiovascular Death Some observational studies have shown an approximately two-fold increased short-term potential risk of acute cardiovascular death in adults exposed to azithromycin relative to other antibacterial drugs, including amoxicillin. The five-day cardiovascular mortality observed in these studies ranged from 20 to 400 per million azithromycin treatment courses. This potential risk was noted to be greater during the first five days of azithromycin use and does not appear to be limited to those patients with preexisting cardiovascular diseases. The data in these observational studies are insufficient to establish or exclude a causal relationship between acute cardiovascular death and azithromycin use. Consider balancing this potential risk with treatment benefits when prescribing ZITHROMAX.

[zithromax, Warnings and Precautions] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Warnings and Precautions: Direct parents and caregivers to contact their physician if vomiting or irritability with feeding occurs. 5.4 QT Prolongation Prolonged cardiac repolarization and QT interval, imparting a risk of developing cardiac arrhythmia and torsades de pointes, have been seen with treatment with macrolides, including azithromycin. Cases of torsades de pointes have been spontaneously reported during postmarketing surveillance in patients receiving azithromycin. Providers should consider the risk of QT prolongation which can be fatal when weighing the risks and benefits of azithromycin for at-risk groups including: - patients with known prolongation of the QT interval, a history of torsades de pointes, congenital long QT syndrome, bradyarrhythmias or uncompensated heart failure - patients on drugs known to prolong the QT interval - patients with ongoing proarrhythmic conditions such as uncorrected hypokalemia or hypomagnesemia, clinically significant bradycardia, and in patients receiving Class IA (quinidine, procainamide) or Class III (dofetilide, amiodarone, sotalol) antiarrhythmic agents.

[zithromax, Use in Specific Populations] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Use in Specific Populations: 8 USE IN SPECIFIC POPULATIONS Geriatric use: Elderly patients may be more susceptible to development of torsades de pointes arrhythmias. ( 8.5 ) 8.2 Lactation Risk Summary Azithromycin is present in human milk (see Data ) . Non-serious adverse reactions have been reported in breastfed infants after maternal administration of azithromycin (see Clinical Considerations ) . There are no available data on the effects of azithromycin on milk production. The developmental and health benefits of breastfeeding should be considered along with the mother's clinical need for ZITHROMAX and any potential adverse effects on the breastfed infant from ZITHROMAX or from the underlying maternal condition. Clinical Considerations Advise women to monitor the breastfed infant for diarrhea, vomiting, or rash. Data Azithromycin breastmilk concentrations were measured in 20 women after receiving a single 2 g oral dose of azithromycin during labor.

[zithromax, Patient Information] Zithromax (azithromycin dihydrate)
Zithromax (azithromycin dihydrate), Patient Information: Tell your healthcare provider right away if you or your child feel a fast or irregular heartbeat, get dizzy or faint. ZITHROMAX may cause a rare heart problem known as prolongation of the QT interval. This condition can cause an abnormal heartbeat and can be very dangerous. The chances of this happening are higher in people: o who are elderly o with a family history of prolonged QT interval o with low blood potassium o who take certain medicines to control heart rhythm (antiarrhythmics) - Diarrhea. Tell your healthcare provider right away if you have watery diarrhea, diarrhea that does not go away, or bloody stools. You may experience cramping and a fever. This could happen as late as 2 or more months after you have finished your treatment with ZITHROMAX. - Worsening of myasthenia gravis (a problem that causes muscle weakness).
```

</details>

## q21 (single)

**Question:** What is the Plavix loading dose for acute coronary syndrome?

**Reference:** A single 300 mg oral loading dose, then 75 mg once daily. Without the loading dose, the antiplatelet effect takes several days to develop.

**Agent answer:**

For acute coronary syndrome (ACS), Plavix is initiated with a single **300 mg oral loading dose**, followed by 75 mg once daily [plavix, Dosage and Administration]. 

Initiating Plavix without a loading dose will delay the establishment of an antiplatelet effect by several days [plavix, Dosage and Administration]. Plavix should also be administered in conjunction with aspirin for ACS [plavix, Indications and Usage].

*gemini-3.8-flash, 1 search(es), 2527 tokens, 283.44 s*

- search `Plavix loading dose acute coronary syndrome` → [plavix, Dosage and Administration], [plavix, Indications and Usage], [plavix, Dosage and Administration], [plavix, Indications and Usage], [plavix, Description]

<details><summary>Retrieved passages</summary>

**search:** `Plavix loading dose acute coronary syndrome`

```text
[plavix, Dosage and Administration] Plavix (clopidogrel)
Plavix (clopidogrel), Dosage and Administration: 2 DOSAGE AND ADMINISTRATION Acute coronary syndrome ( 2.1 ) - Initiate Plavix with a single 300 mg oral loading dose and then continue at 75 mg once daily. - Initiating Plavix without a loading dose will delay establishment of an antiplatelet effect by several days. Recent MI, recent stroke, or established peripheral arterial disease: 75 mg once daily orally without a loading dose. ( 2.2 ) 2.1 Acute Coronary Syndrome In patients who need an antiplatelet effect within hours, initiate Plavix with a single 300 mg oral loading dose and then continue at 75 mg once daily. Initiating Plavix without a loading dose will delay establishment of an antiplatelet effect by several days [see Clinical Pharmacology (12.3) and Clinical Studies (14.1) ] .

[plavix, Indications and Usage] Plavix (clopidogrel)
Plavix (clopidogrel), Indications and Usage: 1 INDICATIONS AND USAGE Plavix is a P2Y 12 platelet inhibitor indicated for: Acute coronary syndrome - For patients with non-ST-segment elevation ACS (unstable angina [UA]/non-ST-elevation myocardial infarction [NSTEMI]), Plavix has been shown to reduce the rate of myocardial infarction (MI) and stroke. ( 1.1 ) - For patients with ST-elevation myocardial infarction (STEMI), Plavix has been shown to reduce the rate of MI and stroke. ( 1.1 ) Recent MI, recent stroke, or established peripheral arterial disease. Plavix has been shown to reduce the rate of MI and stroke. ( 1.2 ) 1.1 Acute Coronary Syndrome (ACS) Plavix is indicated to reduce the rate of myocardial infarction (MI) and stroke in patients with non-ST-segment elevation ACS (unstable angina [UA]/non-ST-elevation myocardial infarction [NSTEMI]), including patients who are to be managed medically and those who are to be managed with coronary revascularization. Plavix should be administered in conjunction with aspirin.

[plavix, Dosage and Administration] Plavix (clopidogrel)
Plavix (clopidogrel), Dosage and Administration: 2.2 Recent MI, Recent Stroke, or Established Peripheral Arterial Disease 75 mg once daily orally without a loading dose [see Clinical Pharmacology (12.3) and Clinical Studies (14.2) ] .

[plavix, Indications and Usage] Plavix (clopidogrel)
Plavix (clopidogrel), Indications and Usage: Plavix is indicated to reduce the rate of myocardial infarction and stroke in patients with acute ST-elevation myocardial infarction (STEMI) who are to be managed medically. Plavix should be administered in conjunction with aspirin. 1.2 Recent MI, Recent Stroke, or Established Peripheral Arterial Disease In patients with established peripheral arterial disease or with a history of recent myocardial infarction (MI) or recent stroke Plavix is indicated to reduce the rate of MI and stroke.

[plavix, Description] Plavix (clopidogrel)
Plavix (clopidogrel), Description: Plavix for oral administration is provided as either pink, round, biconvex, debossed, film-coated tablets containing 97.875 mg of clopidogrel bisulfate which is the molar equivalent of 75 mg of clopidogrel base or pink, oblong, debossed, film-coated tablets containing 391.5 mg of clopidogrel bisulfate which is the molar equivalent of 300 mg of clopidogrel base. Each tablet contains hydrogenated castor oil, hydroxypropyl cellulose, mannitol, microcrystalline cellulose, and polyethylene glycol 6000 as inactive ingredients. The pink film coating contains ferric oxide, hypromellose 2910, lactose monohydrate, titanium dioxide, and triacetin. The tablets are polished with Carnauba wax. Chemical Structure
```

</details>

## q22 (single)

**Question:** What does the Plavix boxed warning say about CYP2C19 poor metabolizers?

**Reference:** Plavix forms less active metabolite in CYP2C19 poor metabolizers (two loss-of-function alleles), so it has less antiplatelet effect. Testing is available; consider another P2Y12 inhibitor for these patients.

**Agent answer:**

According to the Plavix **Boxed Warning** ("Diminished Antiplatelet Effect in Patients with Two Loss-of-Function Alleles of the CYP2C19 Gene"):

* **Mechanism and reduced effect:** The effectiveness of Plavix depends on its antiplatelet activity, which requires conversion to an active metabolite by the cytochrome P450 (CYP) system, principally CYP2C19 `[plavix, Boxed Warning]`. At recommended doses, Plavix forms less of the active metabolite and has a reduced effect on platelet activity in patients who are homozygous for nonfunctional alleles of the CYP2C19 gene (termed "CYP2C19 poor metabolizers") `[plavix, Boxed Warning]`.
* **Testing:** Tests are available to identify patients who are CYP2C19 poor metabolizers `[plavix, Boxed Warning]`.
* **Management recommendation:** Consider the use of another platelet $\text{P2Y}_{12}$ inhibitor in patients identified as CYP2C19 poor metabolizers `[plavix, Boxed Warning]`.

*gemini-3.8-flash, 1 search(es), 3227 tokens, 217.18 s*

- search `Plavix boxed warning CYP2C19 poor metabolizers` → [plavix, Boxed Warning], [plavix, Boxed Warning], [plavix, Warnings and Precautions], [plavix, Warnings and Precautions], [plavix, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `Plavix boxed warning CYP2C19 poor metabolizers`

```text
[plavix, Boxed Warning] Plavix (clopidogrel)
Plavix (clopidogrel), Boxed Warning: Plavix at recommended doses forms less of the active metabolite and so has a reduced effect on platelet activity in patients who are homozygous for nonfunctional alleles of the CYP2C19 gene, (termed "CYP2C19 poor metabolizers"). Tests are available to identify patients who are CYP2C19 poor metabolizers [see Clinical Pharmacology (12.5) ] . Consider use of another platelet P2Y 12 inhibitor in patients identified as CYP2C19 poor metabolizers.

[plavix, Boxed Warning] Plavix (clopidogrel)
Plavix (clopidogrel), Boxed Warning: WARNING: DIMINISHED ANTIPLATELET EFFECT IN PATIENTS WITH TWO LOSS-OF-FUNCTION ALLELES OF THE CYP2C19 GENE WARNING: DIMINISHED ANTIPLATELET EFFECT IN PATIENTS WITH TWO LOSS-OF-FUNCTION ALLELES OF THE CYP2C19 GENE See full prescribing information for complete boxed warning. Effectiveness of Plavix depends on conversion to an active metabolite by the cytochrome P450 (CYP) system, principally CYP2C19. ( 5.1 , 12.3 ) Tests are available to identify patients who are CYP2C19 poor metabolizers. ( 12.5 ) Consider use of another platelet P2Y 12 inhibitor in patients identified as CYP2C19 poor metabolizers. ( 5.1 ) The effectiveness of Plavix results from its antiplatelet activity, which is dependent on its conversion to an active metabolite by the cytochrome P450 (CYP) system, principally CYP2C19 [see Warnings and Precautions (5.1) , Clinical Pharmacology (12.3) ] .

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: 5 WARNINGS AND PRECAUTIONS CYP2C19 inhibitors: Avoid concomitant use of omeprazole or esomeprazole. ( 5.1 ) Bleeding: Plavix increases risk of bleeding. ( 5.2 ) Discontinuation: Premature discontinuation increases risk of cardiovascular events. Discontinue 5 days prior to elective surgery that has a major risk of bleeding. ( 5.3 ) Thrombotic thrombocytopenic purpura (TTP) has been reported. ( 5.4 ) Cross-reactivity among thienopyridines has been reported. ( 5.5 ) 5.1 Diminished Antiplatelet Activity in Patients with Impaired CYP2C19 Function Clopidogrel is a prodrug. Inhibition of platelet aggregation by clopidogrel is achieved through an active metabolite. The metabolism of clopidogrel to its active metabolite can be impaired by genetic variations in CYP2C19 [see Boxed Warning ] . The metabolism of clopidogrel can also be impaired by drugs that inhibit CYP2C19, such as omeprazole or esomeprazole.

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: Avoid concomitant use of Plavix with omeprazole or esomeprazole because both significantly reduce the antiplatelet activity of Plavix [see Drug Interactions (7.1) ] . 5.2 General Risk of Bleeding P2Y12 inhibitors (thienopyridines), including Plavix, increase the risk of bleeding. P2Y12 inhibitors (thienopyridines), inhibit platelet aggregation for the lifetime of the platelet (7-10 days). Because the half-life of clopidogrel's active metabolite is short, it may be possible to restore hemostasis by administering exogenous platelets; however, platelet transfusions within 4 hours of the loading dose or 2 hours of the maintenance dose may be less effective. Use of drugs that induce the activity of CYP2C19 would be expected to result in increased drug levels of the active metabolite of clopidogrel and might potentiate the bleeding risk. As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Drug Interactions (7.1) and Clinical Pharmacology (12.3) ] .

[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] . 7.2 CYP2C19 Inhibitors Clopidogrel is metabolized to its active metabolite in part by CYP2C19. Concomitant use of drugs that inhibit the activity of this enzyme results in reduced plasma concentrations of the active metabolite of clopidogrel and a reduction in platelet inhibition [see Warnings and Precautions (5.1) ] . Omeprazole or Esomeprazole Avoid concomitant use of Plavix with omeprazole or esomeprazole. In clinical studies, omeprazole was shown to reduce significantly the antiplatelet activity of Plavix when given concomitantly or 12 hours apart. A similar reduction in antiplatelet activity was observed with esomeprazole when given concomitantly with Plavix. Dexlansoprazole, lansoprazole, and pantoprazole had less effect on the antiplatelet activity of Plavix than did omeprazole or esomeprazole [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] .
```

</details>

## q23 (single)

**Question:** What is the target INR for a patient on Jantoven for a DVT or PE?

**Reference:** A target INR of 2.5 (range 2.0-3.0).

**Agent answer:**

For patients on Jantoven for venous thromboembolism (including deep venous thrombosis [DVT] and pulmonary embolism [PE]), the recommended target INR is **2.5**, with an INR range of **2.0 to 3.0** for all treatment durations `[jantoven, Dosage and Administration]`.

*gemini-3.5-flash, 1 search(es), 2974 tokens, 10.47 s*

- search `Jantoven target INR DVT PE` → [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Jantoven target INR DVT PE`

```text
[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: 2.2 Recommended Target INR Ranges and Durations for Individual Indications An INR of greater than 4.0 appears to provide no additional therapeutic benefit in most patients and is associated with a higher risk of bleeding. Venous Thromboembolism (including deep venous thrombosis [DVT] and PE) Adjust the warfarin dose to maintain a target INR of 2.5 (INR range, 2.0 to 3.0) for all treatment durations. The duration of treatment is based on the indication as follows: For patients with a DVT or PE secondary to a transient (reversible) risk factor, treatment with warfarin for 3 months is recommended. For patients with an unprovoked DVT or PE, treatment with warfarin is recommended for at least 3 months. After 3 months of therapy, evaluate the risk-benefit ratio of long-term treatment for the individual patient. For patients with two episodes of unprovoked DVT or PE, long-term treatment with warfarin is recommended.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: For a patient receiving long-term anticoagulant treatment, periodically reassess the risk-benefit ratio of continuing such treatment in the individual patient. Atrial Fibrillation In patients with non-valvular AF, anticoagulate with warfarin to target INR of 2.5 (range, 2.0 to 3.0). In patients with non-valvular AF that is persistent or paroxysmal and at high risk of stroke (i.e., having any of the following features: prior ischemic stroke, transient ischemic attack, or systemic embolism, or 2 of the following risk factors: age greater than 75 years, moderately or severely impaired left ventricular systolic function and/or heart failure, history of hypertension, or diabetes mellitus), long-term anticoagulation with warfarin is recommended.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: For patients with tilting disk valves and bileaflet mechanical valves in the mitral position, therapy with warfarin to a target INR of 3.0 (range, 2.5 to 3.5) is recommended. For patients with caged ball or caged disk valves, therapy with warfarin to a target INR of 3.0 (range, 2.5 to 3.5) is recommended. For patients with a bioprosthetic valve in the mitral position, therapy with warfarin to a target INR of 2.5 (range, 2.0 to 3.0) for the first 3 months after valve insertion is recommended. If additional risk factors for thromboembolism are present (AF, previous thromboembolism, left ventricular dysfunction), a target INR of 2.5 (range, 2.0 to 3.0) is recommended.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: Table 1: Three Ranges of Expected Maintenance JANTOVEN Daily Doses Based on CYP2C9 and VKORC1 Genotypes Ranges are derived from multiple published clinical studies. VKORC1-1639G>A (rs9923231) variant is used in this table. Other co-inherited VKORC1 variants may also be important determinants of warfarin dose. VKORC1 CYP2C9 *1/*1 *1/*2 *1/*3 *2/*2 *2/*3 *3/*3 GG 5-7 mg 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg AG 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg AA 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 2.4 Monitoring to Achieve Optimal Anticoagulation JANTOVEN has a narrow therapeutic range (index), and its action may be affected by factors such as other drugs and dietary vitamin K. Therefore, anticoagulation must be carefully monitored during JANTOVEN therapy. Determine the INR daily after the administration of the initial dose until INR results stabilize in the therapeutic range.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: Post-Myocardial Infarction For high-risk patients with MI (e.g., those with a large anterior MI, those with significant heart failure, those with intracardiac thrombus visible on transthoracic echocardiography, those with AF, and those with a history of a thromboembolic event), therapy with combined moderate-intensity (INR, 2.0 to 3.0) warfarin plus low-dose aspirin (≤100 mg/day) for at least 3 months after the MI is recommended. Recurrent Systemic Embolism and Other Indications Oral anticoagulation therapy with warfarin has not been fully evaluated by clinical trials in patients with valvular disease associated with AF, patients with mitral stenosis, and patients with recurrent systemic embolism of unknown etiology. However, a moderate dose regimen (INR 2.0 to 3.0) may be used for these patients. 2.3 Initial and Maintenance Dosing The appropriate initial dosing of JANTOVEN varies widely for different patients.
```

</details>

## q24 (single)

**Question:** How often should INR be checked after starting Jantoven?

**Reference:** Daily from the start until stable in the therapeutic range, then every 1 to 4 weeks.

**Agent answer:**

Upon initiating Jantoven therapy, INR monitoring should follow these frequency guidelines:

* **Upon Initiation:** Obtain **daily** INR determinations after the initial dose until INR results stabilize within the therapeutic range [jantoven, Dosage and Administration].
* **After Stabilization:** Once stable, obtain subsequent INR determinations every **1 to 4 weeks**, based on the clinical situation [jantoven, Dosage and Administration].

**Additional Monitoring Considerations:**
* Perform additional INR tests whenever other medications are initiated, discontinued, or taken irregularly, or when interchanging Jantoven with other warfarin products [jantoven, Dosage and Administration].
* Monitor INR more frequently in patients with compromised renal function [jantoven, Dosage and Administration].

*gemini-3.5-flash, 1 search(es), 3206 tokens, 39.54 s*

- search `Jantoven INR frequency checking monitoring` → [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Jantoven INR frequency checking monitoring`

```text
[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: After stabilization, maintain dosing within the therapeutic range by performing periodic INRs. The frequency of performing INR should be based on the clinical situation but generally acceptable intervals for INR determinations are 1 to 4 weeks. Perform additional INR tests when other warfarin products are interchanged with JANTOVEN, as well as whenever other medications are initiated, discontinued, or taken irregularly. Heparin, a common concomitant drug, increases the INR [see Dosage and Administration (2.8) and Drug Interactions (7) ]. Determinations of whole blood clotting and bleeding times are not effective measures for monitoring of JANTOVEN therapy. 2.5 Renal Impairment No dosage adjustment is necessary for patients with renal failure. Monitor INR more frequently in patients with compromised renal function to maintain INR within the therapeutic range [see Warnings and Precautions (5.4) and Use in Specific Populations (8.6) ]. 2.6 Missed Dose The anticoagulant effect of JANTOVEN persists beyond 24 hours.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: 2 DOSAGE AND ADMINISTRATION Individualize dosing regimen for each patient, and adjust based on INR response. ( 2.1 , 2.2 ) Knowledge of genotype can inform initial dose selection. ( 2.3 ) Monitoring: Obtain daily INR determinations upon initiation until stable in the therapeutic range. Obtain subsequent INR determinations every 1 to 4 weeks. ( 2.4 ) Review conversion instructions from other anticoagulants. ( 2.8 ) 2.1 Individualized Dosing The dosage and administration of JANTOVEN must be individualized for each patient according to the patient's International Normalized Ratio (INR) response to the drug. Adjust the dose based on the patient's INR and the condition being treated. Consult the latest evidence-based clinical practice guidelines regarding the duration and intensity of anticoagulation for the indicated conditions.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: Table 1: Three Ranges of Expected Maintenance JANTOVEN Daily Doses Based on CYP2C9 and VKORC1 Genotypes Ranges are derived from multiple published clinical studies. VKORC1-1639G>A (rs9923231) variant is used in this table. Other co-inherited VKORC1 variants may also be important determinants of warfarin dose. VKORC1 CYP2C9 *1/*1 *1/*2 *1/*3 *2/*2 *2/*3 *3/*3 GG 5-7 mg 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg AG 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg AA 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 2.4 Monitoring to Achieve Optimal Anticoagulation JANTOVEN has a narrow therapeutic range (index), and its action may be affected by factors such as other drugs and dietary vitamin K. Therefore, anticoagulation must be carefully monitored during JANTOVEN therapy. Determine the INR daily after the administration of the initial dose until INR results stabilize in the therapeutic range.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: For a patient receiving long-term anticoagulant treatment, periodically reassess the risk-benefit ratio of continuing such treatment in the individual patient. Atrial Fibrillation In patients with non-valvular AF, anticoagulate with warfarin to target INR of 2.5 (range, 2.0 to 3.0). In patients with non-valvular AF that is persistent or paroxysmal and at high risk of stroke (i.e., having any of the following features: prior ischemic stroke, transient ischemic attack, or systemic embolism, or 2 of the following risk factors: age greater than 75 years, moderately or severely impaired left ventricular systolic function and/or heart failure, history of hypertension, or diabetes mellitus), long-term anticoagulation with warfarin is recommended.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: Dosing Recommendations without Consideration of Genotype If the patient's CYP2C9 and VKORC1 genotypes are not known, the initial dose of JANTOVEN is usually 2 to 5 mg once daily. Determine each patient's dosing needs by close monitoring of the INR response and consideration of the indication being treated. Typical maintenance doses are 2 to 10 mg once daily. Dosing Recommendations with Consideration of Genotype Table 1 displays three ranges of expected maintenance JANTOVEN doses observed in subgroups of patients having different combinations of CYP2C9 and VKORC1 gene variants [see Clinical Pharmacology (12.5) ]. If the patient's CYP2C9 and/or VKORC1 genotype are known, consider these ranges in choosing the initial dose. Patients with CYP2C9 *1/*3, *2/*2, *2/*3, and *3/*3 may require more prolonged time (>2 to 4 weeks) to achieve maximum INR effect for a given dosage regimen than patients without these CYP variants.
```

</details>

## q25 (single)

**Question:** What dietary advice should a patient on Jantoven get?

**Reference:** Eat a normal, balanced diet with a consistent vitamin K intake, and avoid drastic changes such as eating large amounts of leafy green vegetables.

**Agent answer:**

Based on the FDA label for Jantoven, patients should receive the following dietary advice:

* **Vitamin K Intake and Diet Consistency:**
  * Eat a normal, balanced diet to maintain a consistent intake/amount of vitamin K, as the amount of vitamin K in food can affect Jantoven therapy `[jantoven, Drug Interactions]`, `[jantoven, Patient Counseling Information]`.
  * Avoid drastic changes in dietary habits, such as eating large amounts of leafy, green vegetables `[jantoven, Drug Interactions]`, `[jantoven, Patient Counseling Information]`.

* **Botanical (Herbal) Products, Foods, and Juices:**
  * Be aware that certain foods and botanicals (e.g., grapefruit juice, echinacea, ginkgo, goldenseal, St. John's wort) can interact with Jantoven through CYP450 interactions `[jantoven, Drug Interactions]`.
  * Some botanicals may cause bleeding events or have additive anticoagulant/antiplatelet/fibrinolytic effects (e.g., garlic, *Ginkgo biloba*), while others may decrease Jantoven's effects (e.g., co-enzyme Q10, St. John's wort, ginseng) `[jantoven, Drug Interactions]`.
  * Perform more frequent INR monitoring when starting or stopping botanicals `[jantoven, Drug Interactions]`.

* **Pediatric Nutrition Considerations:**
  * Infants receiving vitamin K-supplemented nutrition (including infant formulas) may be resistant to Jantoven therapy, whereas human milk-fed infants may be sensitive to Jantoven therapy `[jantoven, Pediatric Use]`.

*gemini-3.5-flash, 1 search(es), 3607 tokens, 20.64 s*

- search `Jantoven dietary food vitamin K diet` → [jantoven, Drug Interactions], [jantoven, Patient Counseling Information], [jantoven, Drug Interactions], [jantoven, Dosage and Administration], [jantoven, Pediatric Use]

<details><summary>Retrieved passages</summary>

**search:** `Jantoven dietary food vitamin K diet`

```text
[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: The amount of vitamin K in food may affect therapy with JANTOVEN. Advise patients taking JANTOVEN to eat a normal, balanced diet maintaining a consistent amount of vitamin K. Patients taking JANTOVEN should avoid drastic changes in dietary habits, such as eating large amounts of green leafy vegetables.

[jantoven, Patient Counseling Information] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Patient Counseling Information: And to tell their physician if they fall often as this may increase their risk for complications. Eat a normal, balanced diet to maintain a consistent intake of vitamin K. Avoid drastic changes in dietary habits, such as eating large amounts of leafy, green vegetables [see Drug Interactions (7.5) ]. Contact their physician to report any serious illness, such as severe diarrhea, infection, or fever [see Warnings and Precautions (5) and Adverse Reactions (6) ]. Immediately contact their physician when experiencing pain and discoloration of the skin (a purple bruise like rash) mostly on areas of the body with a high fat content, such as breasts, thighs, buttocks, hips and abdomen [see Warnings and Precautions (5.2) ]. Immediately contact their physician when experiencing any unusual symptom or pain since JANTOVEN may cause small cholesterol or athero emboli.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7.5 Botanical (Herbal) Products and Foods More frequent INR monitoring should be performed when starting or stopping botanicals. Few adequate, well-controlled studies evaluating the potential for metabolic and/or pharmacologic interactions between botanicals and JANTOVEN exist. Due to a lack of manufacturing standardization with botanical medicinal preparations, the amount of active ingredients may vary. This could further confound the ability to assess potential interactions and effects on anticoagulation. Some botanicals may cause bleeding events when taken alone (e.g., garlic and Ginkgo biloba) and may have anticoagulant, antiplatelet, and/or fibrinolytic properties. These effects would be expected to be additive to the anticoagulant effects of JANTOVEN. Conversely, some botanicals may decrease the effects of JANTOVEN (e.g., co-enzyme Q 10 , St. John's wort, ginseng). Some botanicals and foods can interact with JANTOVEN through CYP450 interactions (e.g., echinacea, grapefruit juice, ginkgo, goldenseal, St. John's wort).

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: Table 1: Three Ranges of Expected Maintenance JANTOVEN Daily Doses Based on CYP2C9 and VKORC1 Genotypes Ranges are derived from multiple published clinical studies. VKORC1-1639G>A (rs9923231) variant is used in this table. Other co-inherited VKORC1 variants may also be important determinants of warfarin dose. VKORC1 CYP2C9 *1/*1 *1/*2 *1/*3 *2/*2 *2/*3 *3/*3 GG 5-7 mg 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg AG 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg AA 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 2.4 Monitoring to Achieve Optimal Anticoagulation JANTOVEN has a narrow therapeutic range (index), and its action may be affected by factors such as other drugs and dietary vitamin K. Therefore, anticoagulation must be carefully monitored during JANTOVEN therapy. Determine the INR daily after the administration of the initial dose until INR results stabilize in the therapeutic range.

[jantoven, Pediatric Use] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Pediatric Use: Because of changing warfarin requirements due to age, concomitant medications, diet, and existing medical condition, target INR ranges may be difficult to achieve and maintain in pediatric patients, and more frequent INR determinations are recommended. Bleeding rates varied by patient population and clinical care center in pediatric observational studies and patient registries. Infants and children receiving vitamin K-supplemented nutrition, including infant formulas, may be resistant to warfarin therapy, while human milk-fed infants may be sensitive to warfarin therapy.
```

</details>

## q26 (single)

**Question:** Can a pregnant woman take Jantoven?

**Reference:** It is contraindicated in pregnancy except in pregnant women with mechanical heart valves at high risk of thromboembolism, because it can cause birth defects, fatal fetal bleeding and miscarriage.

**Agent answer:**

Jantoven is **contraindicated** in pregnant women, except in those with mechanical heart valves who are at high risk of thromboembolism and for whom the potential benefits may outweigh the risks `[jantoven, Contraindications]`, `[jantoven, Pregnancy]`.

Key considerations from the FDA label include:

* **Risks to the Fetus:** Jantoven can cause fetal harm when administered to a pregnant woman. Exposure during pregnancy causes a recognized pattern of major congenital malformations (warfarin embryopathy and fetotoxicity), fatal fetal hemorrhage, and an increased risk of spontaneous abortion and fetal mortality `[jantoven, Warnings and Precautions]`, `[jantoven, Contraindications]`. Warfarin embryopathy can occur from first-trimester exposure, and central nervous system/eye abnormalities or other adverse pregnancy outcomes have been reported following exposure during the second and third trimesters `[jantoven, Pregnancy]`.
* **Mechanical Heart Valve Exception:** In the specific situation of a pregnant woman with a mechanical heart valve at high risk of thromboembolism, the decision to initiate or continue Jantoven should be thoroughly reviewed with the patient, weighing the specific risks and benefits alongside current medical guidelines `[jantoven, Warnings and Precautions]`.
* **Patient Appraisal:** If Jantoven is used during pregnancy or if a patient becomes pregnant while taking Jantoven, the patient must be apprised of the potential hazards to the fetus `[jantoven, Contraindications]`.

*gemini-3.5-flash, 1 search(es), 3204 tokens, 45.32 s*

- search `Jantoven pregnancy` → [jantoven, Warnings and Precautions], [jantoven, Pregnancy], [jantoven, Pregnancy], [jantoven, Contraindications], [jantoven, Pregnancy]

<details><summary>Retrieved passages</summary>

**search:** `Jantoven pregnancy`

```text
[jantoven, Warnings and Precautions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Warnings and Precautions: 5.7 Use in Pregnant Women with Mechanical Heart Valves JANTOVEN can cause fetal harm when administered to a pregnant woman. While JANTOVEN is contraindicated during pregnancy, the potential benefits of using JANTOVEN may outweigh the risks for pregnant women with mechanical heart valves at high risk of thromboembolism. In those individual situations, the decision to initiate or continue JANTOVEN should be reviewed with the patient, taking into consideration the specific risks and benefits pertaining to the individual patient's medical situation, as well as the most current medical guidelines. JANTOVEN exposure during pregnancy causes a recognized pattern of major congenital malformations (warfarin embryopathy and fetotoxicity), fatal fetal hemorrhage, and an increased risk of spontaneous abortion and fetal mortality.

[jantoven, Pregnancy] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Pregnancy: 8.1 Pregnancy Risk Summary JANTOVEN is contraindicated in women who are pregnant except in pregnant women with mechanical heart valves, who are at high risk of thromboembolism, and for whom the benefits of JANTOVEN may outweigh the risks [see Warnings and Precautions (5.7) ]. JANTOVEN can cause fetal harm. Exposure to warfarin during the first trimester of pregnancy caused a pattern of congenital malformations in about 5% of exposed offspring. Because these data were not collected in adequate and well-controlled studies, this incidence of major birth defects is not an adequate basis for comparison to the estimated incidences in the control group or the U.S. general population and may not reflect the incidences observed in practice. Consider the benefits and risks of JANTOVEN and possible risks to the fetus when prescribing JANTOVEN to a pregnant woman.

[jantoven, Pregnancy] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Pregnancy: Adverse outcomes in pregnancy occur regardless of the health of the mother or the use of medications. The estimated background risk of major birth defects and miscarriage for the indicated population is unknown. In the U.S. general population, the estimated background risk of major birth defects and miscarriage in clinically recognized pregnancies is 2% to 4% and 15% to 20%, respectively. Clinical Considerations Fetal/Neonatal Adverse Reactions In humans, warfarin crosses the placenta, and concentrations in fetal plasma approach the maternal values. Exposure to warfarin during the first trimester of pregnancy caused a pattern of congenital malformations in about 5% of exposed offspring. Warfarin embryopathy is characterized by nasal hypoplasia with or without stippled epiphyses (chondrodysplasia punctata) and growth retardation (including low birth weight).

[jantoven, Contraindications] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Contraindications: 4 CONTRAINDICATIONS JANTOVEN is contraindicated in: Pregnancy JANTOVEN is contraindicated in women who are pregnant except in pregnant women with mechanical heart valves, who are at high risk of thromboembolism [see Warnings and Precautions (5.7) and Use in Specific Populations (8.1) ]. JANTOVEN can cause fetal harm when administered to a pregnant woman. JANTOVEN exposure during pregnancy causes a recognized pattern of major congenital malformations (warfarin embryopathy and fetotoxicity), fatal fetal hemorrhage, and an increased risk of spontaneous abortion and fetal mortality. If JANTOVEN is used during pregnancy or if the patient becomes pregnant while taking this drug, the patient should be apprised of the potential hazard to a fetus [see Use in Specific Populations (8.1) ].

[jantoven, Pregnancy] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Pregnancy: Central nervous system and eye abnormalities have also been reported, including dorsal midline dysplasia characterized by agenesis of the corpus callosum, Dandy-Walker malformation, midline cerebellar atrophy, and ventral midline dysplasia characterized by optic atrophy. Mental retardation, blindness, schizencephaly, microcephaly, hydrocephalus, and other adverse pregnancy outcomes have been reported following warfarin exposure during the second and third trimesters of pregnancy [see Contraindications (4) ].
```

</details>

## q27 (single)

**Question:** When should Prilosec be taken relative to meals?

**Reference:** Before meals. Antacids can be used at the same time.

**Agent answer:**

Prilosec should be taken **before meals** [prilosec, Dosage and Administration], [prilosec, Patient Counseling Information].

*gemini-3.5-flash, 2 search(es), 6205 tokens, 60.33 s*

- search `Prilosec taken relative to meals administration timing` → [prilosec, Dosage and Administration], [prilosec, Dosage and Administration], [prilosec, Dosage and Administration], [prilosec, Patient Counseling Information], [prilosec, Dosage and Administration]
- search `Prilosec "before meals" 30 60 minutes` → [prilosec, Dosage and Administration], [prilosec, Patient Counseling Information], [prilosec, Dosage and Administration], [prilosec, Dosage and Administration], [prilosec, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Prilosec taken relative to meals administration timing`

```text
[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: pylori Eradication to Reduce the Risk of Duodenal Ulcer Recurrence Triple Therapy: PRILOSEC Amoxicillin Clarithromycin 20 mg 1000 mg 500 mg Each drug twice daily for 10 days ( 2.1 )* Dual Therapy: PRILOSEC Clarithromycin 40 mg once daily for 14 days** 500 mg three times daily for 14 days ( 2.1 ) Active Benign Gastric Ulcer 40 mg once daily for 4 to 8 weeks ( 2.1 ) Symptomatic GERD 20 mg once daily for up to 4 weeks ( 2.1 ) See full prescribing information for weight based dosing in pediatric patients 1 year of age and older ( 2.2 ) EE due to Acid-Mediated GERD 20 mg once daily for 4 to 8 weeks ( 2.1 )*** See full prescribing information for weight based dosing in pediatric patients 1 month of age and older ( 2.2 ) Maintenance of Healing of EE due to Acid-Mediated GERD 20

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: 10 to less than 20 kg: 10 mg 20 kg and greater: 20 mg 1 month to less than 1 year 3 to less than 5 kg: 2.5 mg Once daily up to 6 weeks 5 to less than 10 kg: 5 mg 10 kg and greater: 10 mg Maintenance of Healing of EE due to Acid-Mediated GERD 1 to 16 years 5 to less than 10 kg: 5 mg Once daily. Controlled studies do not extend beyond 12 months 10 to less than 20 kg: 10 mg 20 kg and greater: 20 mg 2.3 Administration Instructions - PRILOSEC is intended to be prepared in water and administered orally or via a nasogastric (NG) or gastric tube. - Take PRILOSEC before meals. - Antacids may be used concomitantly with PRILOSEC. - Missed doses: If a dose is missed, administer as soon as possible.

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: Table 1: Recommended Dosage Regimen of PRILOSEC in Adults by Indication Indication Dosage of PRILOSEC Treatment Duration Treatment of Active Duodenal Ulcer 20 mg once daily 4 weeks Most patients heal within 4 weeks; some patients may require an additional 4 weeks of therapy to achieve healing Helicobacter pylori Eradication to Reduce the Risk of Duodenal Ulcer Recurrence Triple Therapy PRILOSEC 20 mg Amoxicillin 1000 mg Clarithromycin 500 mg Take all three drugs twice daily 10 days In patients with an ulcer present at the time of initiation of therapy, continue PRILOSEC 20 mg once daily for an additional 18 days for ulcer healing and symptom relief.

[prilosec, Patient Counseling Information] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Patient Counseling Information: Hypomagnesemia and Mineral Metabolism Advise the patient or caregiver to report any clinical symptoms that may be associated with hypomagnesemia, hypocalcemia, and/or hypokalemia to the patient's healthcare provider, if they have been receiving PRILOSEC for at least 3 months [see Warnings and Precautions ( 5.9 )] . Drug Interactions Advise patients to report to their healthcare provider if they start treatment with rilpivirine-containing products, clopidogrel, St. John's Wort or rifampin; or, if they take high-dose methotrexate [see Contraindications ( 4 ), Warnings and Precautions ( 5.7 , 5.10 , 5.12 )] . Administration - PRILOSEC is intended to be prepared in water and administered orally or via a nasogastric (NG) or gastric tube, as described in the Medication Guide. - Take PRILOSEC before meals. - Antacids may be used concomitantly with PRILOSEC. - Missed doses: If a dose is missed, administer as soon as possible.

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: Dual Therapy PRILOSEC 40 mg once daily Clarithromycin 500 mg three times daily 14 days In patients with an ulcer present at the time of initiation of therapy, an additional 14 days of PRILOSEC 20 mg once daily is recommended for ulcer healing and symptom relief. Active Benign Gastric Ulcer 40 mg once daily 4 to 8 weeks Treatment of Symptomatic GERD 20 mg once daily Up to 4 weeks Treatment of EE due to Acid-Mediated GERD 20 mg once daily 4 to 8 weeks The efficacy of PRILOSEC used for longer than 8 weeks in patients with EE has not been established. If a patient does not respond to 8 weeks of treatment, an additional 4 weeks of treatment may be given. If there is recurrence of EE or GERD symptoms (e.g., heartburn), additional 4 to 8 week courses of PRILOSEC may be considered.
```

**search:** `Prilosec "before meals" 30 60 minutes`

```text
[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: 10 to less than 20 kg: 10 mg 20 kg and greater: 20 mg 1 month to less than 1 year 3 to less than 5 kg: 2.5 mg Once daily up to 6 weeks 5 to less than 10 kg: 5 mg 10 kg and greater: 10 mg Maintenance of Healing of EE due to Acid-Mediated GERD 1 to 16 years 5 to less than 10 kg: 5 mg Once daily. Controlled studies do not extend beyond 12 months 10 to less than 20 kg: 10 mg 20 kg and greater: 20 mg 2.3 Administration Instructions - PRILOSEC is intended to be prepared in water and administered orally or via a nasogastric (NG) or gastric tube. - Take PRILOSEC before meals. - Antacids may be used concomitantly with PRILOSEC. - Missed doses: If a dose is missed, administer as soon as possible.

[prilosec, Patient Counseling Information] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Patient Counseling Information: Hypomagnesemia and Mineral Metabolism Advise the patient or caregiver to report any clinical symptoms that may be associated with hypomagnesemia, hypocalcemia, and/or hypokalemia to the patient's healthcare provider, if they have been receiving PRILOSEC for at least 3 months [see Warnings and Precautions ( 5.9 )] . Drug Interactions Advise patients to report to their healthcare provider if they start treatment with rilpivirine-containing products, clopidogrel, St. John's Wort or rifampin; or, if they take high-dose methotrexate [see Contraindications ( 4 ), Warnings and Precautions ( 5.7 , 5.10 , 5.12 )] . Administration - PRILOSEC is intended to be prepared in water and administered orally or via a nasogastric (NG) or gastric tube, as described in the Medication Guide. - Take PRILOSEC before meals. - Antacids may be used concomitantly with PRILOSEC. - Missed doses: If a dose is missed, administer as soon as possible.

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: pylori Eradication to Reduce the Risk of Duodenal Ulcer Recurrence Triple Therapy: PRILOSEC Amoxicillin Clarithromycin 20 mg 1000 mg 500 mg Each drug twice daily for 10 days ( 2.1 )* Dual Therapy: PRILOSEC Clarithromycin 40 mg once daily for 14 days** 500 mg three times daily for 14 days ( 2.1 ) Active Benign Gastric Ulcer 40 mg once daily for 4 to 8 weeks ( 2.1 ) Symptomatic GERD 20 mg once daily for up to 4 weeks ( 2.1 ) See full prescribing information for weight based dosing in pediatric patients 1 year of age and older ( 2.2 ) EE due to Acid-Mediated GERD 20 mg once daily for 4 to 8 weeks ( 2.1 )*** See full prescribing information for weight based dosing in pediatric patients 1 month of age and older ( 2.2 ) Maintenance of Healing of EE due to Acid-Mediated GERD 20

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: Table 1: Recommended Dosage Regimen of PRILOSEC in Adults by Indication Indication Dosage of PRILOSEC Treatment Duration Treatment of Active Duodenal Ulcer 20 mg once daily 4 weeks Most patients heal within 4 weeks; some patients may require an additional 4 weeks of therapy to achieve healing Helicobacter pylori Eradication to Reduce the Risk of Duodenal Ulcer Recurrence Triple Therapy PRILOSEC 20 mg Amoxicillin 1000 mg Clarithromycin 500 mg Take all three drugs twice daily 10 days In patients with an ulcer present at the time of initiation of therapy, continue PRILOSEC 20 mg once daily for an additional 18 days for ulcer healing and symptom relief.

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: Dual Therapy PRILOSEC 40 mg once daily Clarithromycin 500 mg three times daily 14 days In patients with an ulcer present at the time of initiation of therapy, an additional 14 days of PRILOSEC 20 mg once daily is recommended for ulcer healing and symptom relief. Active Benign Gastric Ulcer 40 mg once daily 4 to 8 weeks Treatment of Symptomatic GERD 20 mg once daily Up to 4 weeks Treatment of EE due to Acid-Mediated GERD 20 mg once daily 4 to 8 weeks The efficacy of PRILOSEC used for longer than 8 weeks in patients with EE has not been established. If a patient does not respond to 8 weeks of treatment, an additional 4 weeks of treatment may be given. If there is recurrence of EE or GERD symptoms (e.g., heartburn), additional 4 to 8 week courses of PRILOSEC may be considered.
```

</details>

## q28 (single)

**Question:** Which patients should get a reduced Prilosec dose?

**Reference:** Patients with hepatic impairment (Child-Pugh A, B or C) and Asian patients: reduce to 10 mg once daily.

**Agent answer:**

Based on the Prilosec drug label, a reduced dosage (10 mg once daily instead of 20 mg once daily) is recommended for:

* **Patients with hepatic impairment (Child-Pugh Class A, B, or C)** `[prilosec, Dosage and Administration]`, `[prilosec, Use in Specific Populations]`
* **Asian patients** `[prilosec, Dosage and Administration]`, `[prilosec, Use in Specific Populations]`

**Indication context:**
This dosage reduction to 10 mg once daily is specifically recommended when Prilosec is used for the **maintenance of healing of erosive esophagitis (EE) due to acid-mediated GERD** `[prilosec, Dosage and Administration]`, `[prilosec, Use in Specific Populations]`.

*gemini-3.5-flash, 1 search(es), 3245 tokens, 25.98 s*

- search `Prilosec reduced dose dosage special populations hepatic` → [prilosec, Dosage and Administration], [prilosec, Use in Specific Populations], [prilosec, Dosage and Administration], [prilosec, Use in Specific Populations], [prilosec, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Prilosec reduced dose dosage special populations hepatic`

```text
[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: Reduce the dosage to 10 mg once daily for patients with hepatic impairment (Child-Pugh Class A, B, or C) and Asian patients ( 8.6 , 8.7 ) 2.1 Recommended Adult Dosage Regimen by Indication Table 1 shows the recommended dosage of PRILOSEC in adult patients by indication.

[prilosec, Use in Specific Populations] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Use in Specific Populations: 8 USE IN SPECIFIC POPULATIONS 8.2 Lactation Risk Summary Limited data suggest omeprazole may be present in human milk. There are no clinical data on the effects of omeprazole on the breastfed infant or on milk production. The developmental and health benefits of breastfeeding should be considered along with the mother's clinical need for PRILOSEC and any potential adverse effects on the breastfed infant from PRILOSEC or from the underlying maternal condition. 8.6 Hepatic Impairment In patients with hepatic impairment (Child-Pugh Class A, B, or C) exposure to omeprazole substantially increased compared to healthy subjects. Dosage reduction of PRILOSEC to 10 mg once daily is recommended for patients with hepatic impairment for maintenance of healing of EE [see Dosage and Administration ( 2.1 ), Clinical Pharmacology ( 12.3 )] . 8.7 Asian Population In studies of healthy subjects, Asians had approximately a four-fold higher exposure than Caucasians.

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: Maintenance of Healing of EE due to Acid-Mediated GERD 20 mg once daily Dosage reduction to 10 mg once daily is recommended for patients with hepatic impairment (Child-Pugh Class A, B or C) and Asian patients when used for the maintenance of healing of EE [see Use in Specific Populations ( 8.6 , 8.7 ) and Clinical Pharmacology ( 12.3 , 12.5 )]. Controlled studies do not extend beyond 12 months. Pathological Hypersecretory Conditions Starting dose is 60 mg once daily; adjust to patient needs Daily dosages of greater than 80 mg should be administered in divided doses. Dosages up to 120 mg three times daily have been administered. As long as clinically indicated. Some patients with Zollinger-Ellison syndrome have been treated continuously for more than 5 years. 2.2 Recommended Pediatric Dosage Regimen by Indication Table 2 shows the recommended dosage of PRILOSEC in pediatric patients by indication.

[prilosec, Use in Specific Populations] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Use in Specific Populations: Dosage reduction of PRILOSEC to 10 mg once daily is recommended for Asian patients for maintenance of healing of EE [see Dosage and Administration ( 2.1 ), Clinical Pharmacology ( 12.5 )] .

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: pylori Eradication to Reduce the Risk of Duodenal Ulcer Recurrence Triple Therapy: PRILOSEC Amoxicillin Clarithromycin 20 mg 1000 mg 500 mg Each drug twice daily for 10 days ( 2.1 )* Dual Therapy: PRILOSEC Clarithromycin 40 mg once daily for 14 days** 500 mg three times daily for 14 days ( 2.1 ) Active Benign Gastric Ulcer 40 mg once daily for 4 to 8 weeks ( 2.1 ) Symptomatic GERD 20 mg once daily for up to 4 weeks ( 2.1 ) See full prescribing information for weight based dosing in pediatric patients 1 year of age and older ( 2.2 ) EE due to Acid-Mediated GERD 20 mg once daily for 4 to 8 weeks ( 2.1 )*** See full prescribing information for weight based dosing in pediatric patients 1 month of age and older ( 2.2 ) Maintenance of Healing of EE due to Acid-Mediated GERD 20
```

</details>

## q29 (single)

**Question:** What is the naproxen dose for an acute gout attack?

**Reference:** 750 mg to start, then 250 mg every 8 hours until the attack subsides.

**Agent answer:**

For an acute gout attack, the recommended naproxen tablet dosing is as follows:

* **Starting dose:** 750 mg [naproxen, Dosage and Administration]
* **Subsequent dosing:** 250 mg every 8 hours until the attack has subsided [naproxen, Dosage and Administration]
* **Maximum dose:** The total daily dose should not exceed 1,250 mg of naproxen [naproxen, Dosage and Administration]

*gemini-3.5-flash, 1 search(es), 2857 tokens, 49.74 s*

- search `naproxen acute gout attack dose` → [naproxen, Dosage and Administration], [naproxen, Dosage and Administration], [naproxen, Dosage and Administration], [naproxen, Indications and Usage], [naproxen, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `naproxen acute gout attack dose`

```text
[naproxen, Dosage and Administration] Naproxen (naproxen)
Naproxen (naproxen), Dosage and Administration: Acute Gout Recommended starting dose 750 mg of naproxen tablets followed by 250 mg every 8 hours until the attack has subsided. 2.1 General Dosing Instructions Carefully consider the potential benefits and risks of naproxen tablets and other treatment options before deciding to use Naproxen tablets. Use the lowest effective dose for the shortest duration consistent with individual patient treatment goals [ see Warnings and Precautions (5) ] . After observing the response to initial therapy with Naproxen tablets or the dose and frequency should be adjusted to suit an individual patient's needs. Naproxen-containing products such as naproxen tablets and other naproxen products should not be used concomitantly since they all circulate in the plasma as the naproxen anion. 2.2 Rheumatoid Arthritis, Osteoarthritis and Ankylosing Spondylitis The recommended dosages of naproxen tablets are shown in Table 1.

[naproxen, Dosage and Administration] Naproxen (naproxen)
Naproxen (naproxen), Dosage and Administration: The total daily dose should not exceed 1,250 mg of naproxen. 2.5 Acute Gout The recommended starting dose is 750 mg of naproxen tablets followed by 250 mg every 8 hours until the attack has subsided. 2.6 Non-Interchangeability with Other Formulations of Naproxen Different dose strengths and formulations (e.g., tablets, suspension) of naproxen are not interchangeable. This difference should be taken into consideration when changing strengths or formulations.

[naproxen, Dosage and Administration] Naproxen (naproxen)
Naproxen (naproxen), Dosage and Administration: 2.3 Polyarticular Juvenile Idiopathic Arthritis Naproxen solid-oral dosage forms may not allow for the flexible dose titration needed in pediatric patients with polyarticular juvenile idiopathic arthritis. A liquid formulation may be more appropriate for weight-based dosing and due to the need for dose flexibility in children. In pediatric patients, doses of 5 mg/kg/day produced plasma levels of naproxen similar to those seen in adults taking 500 mg of naproxen [ see Clinical Pharmacology (12) ] . The recommended total daily dose of naproxen is approximately 10 mg/kg given in 2 divided doses. Dosing with naproxen tablets are not appropriate for children weighing less than 50 kilograms. 2.4 Management of Pain, Primary Dysmenorrhea, and Acute Tendonitis and Bursitis Naproxen Tablets may also be used. The recommended starting dose of naproxen tablets is 500 mg followed by 250 mg every 6 to 8 hours as required.

[naproxen, Indications and Usage] Naproxen (naproxen)
Naproxen (naproxen), Indications and Usage: 1 INDICATIONS AND USAGE Naproxen tablets are indicated for: the relief of the signs and symptoms of: - rheumatoid arthritis - osteoarthritis - ankylosing spondylitis - Polyarticular Juvenile Idiopathic Arthritis Naproxen tablets are also indicated for: the relief of signs and symptoms of: - tendonitis - bursitis - acute gout the management of: - pain - primary dysmenorrhea Naproxen tablets are a non-steroidal anti-inflammatory drugs indicated for: the relief of the signs and symptoms of: - rheumatoid arthritis - osteoarthritis - ankylosing spondylitis - polyarticular juvenile idiopathic arthritis Naproxen Tablets are also indicated for: the relief of signs and symptoms of: - tendonitis - bursitis - acute gout the management of: - pain - primary dysmenorrhea

[naproxen, Dosage and Administration] Naproxen (naproxen)
Naproxen (naproxen), Dosage and Administration: 2 DOSAGE AND ADMINISTRATION Use the lowest effective dosage for shortest duration consistent with individual patient treatment goals. ( 2.1 ) Rheumatoid Arthritis, Osteoarthritis, and Ankylosing Spondylitis Naproxen Tablets 250 mg or 375 mg or 500 mg twice daily twice daily twice daily The dose may be adjusted up or down depending on the clinical response of the patient. In patients who tolerate lower doses well, the dose may be increased to naproxen 1500 mg/day for up to 6 months. Polyarticular Juvenile Idiopathic Arthritis Naproxen Tablets may not allow for the flexible dose titration needed in pediatric patients with polyarticular juvenile idiopathic arthritis. A liquid formulation may be more appropriate. Recommended total daily dose of naproxen is approximately 10 mg/kg given in 2 divided doses. Dosing with Naproxen Tablets is not appropriate for children weighing less than 50 kilograms.
```

</details>

## q30 (single)

**Question:** Can a patient on prescription naproxen tablets also take Aleve?

**Reference:** No. Naproxen-containing products should not be used together because they all circulate in the plasma as the naproxen anion.

**Agent answer:**

**No**, a patient taking prescription naproxen tablets should **not** also take Aleve.

### Reasons based on the FDA drug labels:
* **Concomitant NSAID Use Not Recommended:** The prescription naproxen label explicitly states that the concomitant use of naproxen with other nonsteroidal anti-inflammatory drugs (NSAIDs) or salicylates is not recommended `[naproxen, Drug Interactions]`.
* **Duplicate NSAID / Active Ingredient:** Aleve contains naproxen sodium, which is an NSAID `[aleve, Warnings]`. 
* **Increased Risk of Stomach Bleeding:** The Aleve label warns that taking it with other drugs containing prescription or nonprescription NSAIDs (such as aspirin, ibuprofen, naproxen, or others) increases the chance of severe stomach bleeding `[aleve, Warnings]`.

*gemini-3.5-flash, 2 search(es), 5307 tokens, 134.97 s*

- search `naproxen Aleve concurrent use active ingredient warnings` → [aleve, Warnings], [aleve, Ask a Doctor or Pharmacist Before Use], [aleve, Do Not Use], [aleve, Ask a Doctor Before Use], [naproxen, Warnings and Precautions]
- search `naproxen taking other drugs containing prescription nonprescription NSAIDs` → [naproxen, Drug Interactions], [naproxen, Drug Interactions], [naproxen, Other Information], [naproxen, Drug Interactions], [naproxen, Other Information]

<details><summary>Retrieved passages</summary>

**search:** `naproxen Aleve concurrent use active ingredient warnings`

```text
[aleve, Warnings] Aleve (naproxen sodium)
Aleve (naproxen sodium), Warnings: Stomach bleeding warning This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you: are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs (aspirin, ibuprofen, naproxen, or others) have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal. The risk is higher if you use more than directed or for longer than directed. Allergy alert Naproxen sodium may cause a severe allergic reaction, especially in people allergic to aspirin.

[aleve, Ask a Doctor or Pharmacist Before Use] Aleve (naproxen sodium)
Aleve (naproxen sodium), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are under a doctor's care for any serious condition taking aspirin for heart attack or stroke, because naproxen may decrease this benefit of aspirin taking any other drug

[aleve, Do Not Use] Aleve (naproxen sodium)
Aleve (naproxen sodium), Do Not Use: Do not use if you have ever had an allergic reaction to any other pain reliever/fever reducer right before or after heart surgery

[aleve, Ask a Doctor Before Use] Aleve (naproxen sodium)
Aleve (naproxen sodium), Ask a Doctor Before Use: Ask a doctor before use if the stomach bleeding warning applies to you you have a history of stomach problems, such as heartburn you have high blood pressure, heart disease, liver cirrhosis, kidney disease, asthma, or had a stroke you are taking a diuretic you have problems or serious side effects from taking pain relievers or fever reducers

[naproxen, Warnings and Precautions] Naproxen (naproxen)
Naproxen (naproxen), Warnings and Precautions: The increase in CV thrombotic risk has been observed most consistently at higher doses. To minimize the potential risk for an adverse CV event in NSAID-treated patients, use the lowest effective dose for the shortest duration possible. Physicians and patients should remain alert for the development of such events, throughout the entire treatment course, even in the absence of previous CV symptoms. Patients should be informed about the symptoms of serious CV events and the steps to take if they occur. There is no consistent evidence that concurrent use of aspirin mitigates the increased risk of serious CV thrombotic events associated with NSAID use. The concurrent use of aspirin and an NSAID, such as naproxen, increases the risk of serious gastrointestinal (GI) events [ see Warnings and Precautions (5.2) ] .
```

**search:** `naproxen taking other drugs containing prescription nonprescription NSAIDs`

```text
[naproxen, Drug Interactions] Naproxen (naproxen)
Naproxen (naproxen), Drug Interactions: Intervention: The concomitant use of naproxen with other NSAIDs or salicylates is not recommended. Pemetrexed Clinical Impact: Concomitant use of naproxen tablets and pemetrexed may increase the risk of pemetrexed-associated myelosuppression, renal, and GI toxicity (see the pemetrexed prescribing information). Intervention: During concomitant use of naproxen tablets and pemetrexed, in patients with renal impairment whose creatinine clearance ranges from 45 to 79 mL/min, monitor for myelosuppression, renal and GI toxicity. NSAIDs with short elimination half-lives (e.g., diclofenac, indomethacin) should be avoided for a period of two days before, the day of, and two days following administration of pemetrexed. In the absence of data regarding potential interaction between pemetrexed and NSAIDs with longer half-lives (e.g., meloxicam, nabumetone), patients taking these NSAIDs should interrupt dosing for at least five days before, the day of, and two days following pemetrexed administration.

[naproxen, Drug Interactions] Naproxen (naproxen)
Naproxen (naproxen), Drug Interactions: Aspirin Clinical Impact: A pharmacodynamic (PD) study has demonstrated an interaction in which lower dose naproxen (220mg/day or 220mg twice daily) interfered with the antiplatelet effect of low-dose immediate-release aspirin, with the interaction most marked during the washout period of naproxen [ see Pharmacodynamics 12.2 ) ]. There is reason to expect that the interaction would be present with prescription doses of naproxen or with enteric-coated low-dose aspirin; however, the peak interference with aspirin function may be later than observed in the PD study due to the longer washout period. Controlled clinical studies showed that the concomitant use of NSAIDs and analgesic doses of aspirin does not produce any greater therapeutic effect than the use of NSAIDs alone.

[naproxen, Other Information] Naproxen (naproxen)
Naproxen (naproxen), Other Information: NSAIDs are used to treat pain and redness, swelling, and heat (inflammation) from medical conditions such as different types of arthritis, menstrual cramps, and other types of short-term pain. Who should not take NSAIDs? Do not take NSAIDs: - if you have had an asthma attack, hives, or other allergic reaction with aspirin or any other NSAIDs. - right before or after heart bypass surgery. Before taking NSAIDS, tell your healthcare provider about all of your medical conditions, including if you: - have liver or kidney problems - have high blood pressure - have asthma - are pregnant or plan to become pregnant. Taking NSAIDs at about 20 weeks of pregnancy or later may harm your unborn baby.

[naproxen, Drug Interactions] Naproxen (naproxen)
Naproxen (naproxen), Drug Interactions: Antacids and Sucralfate Clinical Impact: Concomitant administration of some antacids (magnesium oxide or aluminum hydroxide) and sucralfate can delay the absorption of naproxen. Intervention: Concomitant administration of antacids such as magnesium oxide or aluminum hydroxide, and sucralfate with naproxen tablets are not recommended. Cholestyramine Clinical Impact: Concomitant administration of cholestyramine can delay the absorption of naproxen. Intervention: Concomitant administration of cholestyramine with naproxen tablets are not recommended. Probenecid Clinical Impact: Probenecid given concurrently increases naproxen anion plasma levels and extends its plasma half-life significantly. Intervention: Patients simultaneously receiving naproxen tablets and probenecid should be observed for adjustment of dose if required. Other albumin-bound drugs Clinical Impact: Naproxen is highly bound to plasma albumin; it thus has a theoretical potential for interaction with other albumin-bound drugs such as coumarin-type anticoagulants, sulphonylureas, hydantoins, other NSAIDs, and aspirin .

[naproxen, Other Information] Naproxen (naproxen)
Naproxen (naproxen), Other Information: - Increased risk of bleeding, ulcers, and tears (perforation) of the esophagus (tube leading from the mouth to the stomach), stomach and intestines: o anytime during use o without warning symptoms o that may cause death The risk of getting an ulcer or bleeding increases with: o past history of stomach ulcers, or stomach or intestinal bleeding with use of NSAIDs o taking medicines called "corticosteroids", "anticoagulants", "SSRIs", or "SNRIs" o increasing doses of NSAIDs o older age o longer use of NSAIDs o poor health o smoking o advanced liver disease o drinking alcohol o bleeding problems NSAIDs should only be used: o exactly as prescribed o at the lowest dose possible for your treatment o for the shortest time needed What are NSAIDs?
```

</details>

## q31 (single)

**Question:** A child with juvenile arthritis can't swallow Celebrex capsules. What are the options?

**Reference:** The capsule contents can be emptied onto a level teaspoon of cool or room-temperature applesauce and taken immediately with water; the mixture is stable up to 6 hours refrigerated.

**Agent answer:**

For patients who have difficulty swallowing capsules, the contents of a Celebrex capsule can be administered with applesauce [celebrex, Dosage and Administration]:

* **Preparation & Administration:** Carefully empty the entire contents of the capsule onto a level teaspoon of cool or room temperature applesauce, and ingest immediately with water [celebrex, Dosage and Administration].
* **Storage/Stability:** The sprinkled capsule contents on applesauce are stable for up to 6 hours when stored under refrigerated conditions (2°C to 8°C / 35°F to 45°F) [celebrex, Dosage and Administration].

*gemini-3.5-flash, 1 search(es), 3373 tokens, 146.22 s*

- search `Celebrex juvenile arthritis swallow capsule administration` → [celebrex, Dosage and Administration], [celebrex, Pediatric Use], [celebrex, Indications and Usage], [celebrex, Adverse Reactions], [celebrex, Pediatric Use]

<details><summary>Retrieved passages</summary>

**search:** `Celebrex juvenile arthritis swallow capsule administration`

```text
[celebrex, Dosage and Administration] CELEBREX (celecoxib)
CELEBREX (celecoxib), Dosage and Administration: 2.3 Rheumatoid Arthritis For RA, the dosage is 100 mg to 200 mg twice daily. 2.4 Juvenile Rheumatoid Arthritis For JRA, the dosage for pediatric patients (age 2 years and older) is based on weight. For patients ≥10 kg to ≤25 kg the recommended dose is 50 mg twice daily. For patients >25 kg the recommended dose is 100 mg twice daily. For patients who have difficulty swallowing capsules, the contents of a CELEBREX capsule can be added to applesauce. The entire capsule contents are carefully emptied onto a level teaspoon of cool or room temperature applesauce and ingested immediately with water. The sprinkled capsule contents on applesauce are stable for up to 6 hours under refrigerated conditions (2°C to 8°C/35°F to 45°F). 2.5 Ankylosing Spondylitis For AS, the dosage of CELEBREX is 200 mg daily in single (once per day) or divided (twice per day) doses.

[celebrex, Pediatric Use] CELEBREX (celecoxib)
CELEBREX (celecoxib), Pediatric Use: 8.4 Pediatric Use CELEBREX is approved for relief of the signs and symptoms of Juvenile Rheumatoid Arthritis in patients 2 years and older. Safety and efficacy have not been studied beyond six months in children. The long-term cardiovascular toxicity in children exposed to CELEBREX has not been evaluated and it is unknown if long-term risks may be similar to that seen in adults exposed to CELEBREX or other COX-2 selective and non-selective NSAIDs [see Boxed Warning , Warnings and Precautions (5.5) , and Clinical Studies (14.3) ] . The use of celecoxib in patients 2 years to 17 years of age with pauciarticular, polyarticular course JRA or in patients with systemic onset JRA was studied in a 12-week, double-blind, active controlled, pharmacokinetic, safety and efficacy study, with a 12-week open-label extension.

[celebrex, Indications and Usage] CELEBREX (celecoxib)
CELEBREX (celecoxib), Indications and Usage: 1 INDICATIONS AND USAGE CELEBREX is indicated CELEBREX is a nonsteroidal anti-inflammatory drug indicated for: - Osteoarthritis (OA) ( 1.1 ) - Rheumatoid Arthritis (RA) ( 1.2 ) - Juvenile Rheumatoid Arthritis (JRA) in patients 2 years and older ( 1.3 ) - Ankylosing Spondylitis (AS) ( 1.4 ) - Acute Pain (AP) ( 1.5 ) - Primary Dysmenorrhea (PD) ( 1.6 ) 1.1 Osteoarthritis (OA) For the management of the signs and symptoms of OA [see Clinical Studies (14.1) ] . 1.2 Rheumatoid Arthritis (RA) For the management of the signs and symptoms of RA [see Clinical Studies (14.2) ] . 1.3 Juvenile Rheumatoid Arthritis (JRA) For the management of the signs and symptoms of JRA in patients 2 years and older [see Clinical Studies (14.3) ] . 1.4 Ankylosing Spondylitis (AS) For the management of the signs and symptoms of AS [see Clinical Studies (14.4) ] .

[celebrex, Adverse Reactions] CELEBREX (celecoxib)
CELEBREX (celecoxib), Adverse Reactions: Juvenile Rheumatoid Arthritis Study In a 12-week, double-blind, active-controlled study, 242 JRA patients 2 years to 17 years of age were treated with celecoxib or naproxen; 77 JRA patients were treated with celecoxib 3 mg/kg twice daily, 82 patients were treated with celecoxib 6 mg/kg twice daily, and 83 patients were treated with naproxen 7.5 mg/kg twice daily. The most commonly occurring (≥5%) adverse events in celecoxib treated patients were headache, fever (pyrexia), upper abdominal pain, cough, nasopharyngitis, abdominal pain, nausea, arthralgia, diarrhea, and vomiting. The most commonly occurring (≥5%) adverse experiences for naproxen-treated patients were headache, nausea, vomiting, fever, upper abdominal pain, diarrhea, cough, abdominal pain, and dizziness (Table 2). Compared with naproxen, celecoxib at doses of 3 and 6 mg/kg twice daily had no observable deleterious effect on growth and development during the course of the 12-week double-blind study.

[celebrex, Pediatric Use] CELEBREX (celecoxib)
CELEBREX (celecoxib), Pediatric Use: Celecoxib has not been studied in patients under the age of 2 years, in patients with body weight less than 10 kg (22 lbs), and in patients with active systemic features. Patients with systemic onset JRA (without active systemic features) appear to be at risk for the development of abnormal coagulation laboratory tests. In some patients with systemic onset JRA, both celecoxib and naproxen were associated with mild prolongation of activated partial thromboplastin time (APTT) but not prothrombin time (PT). When NSAIDs including celecoxib are used in patients with systemic onset JRA, monitor patients for signs and symptoms of abnormal clotting or bleeding, due to the risk of disseminated intravascular coagulation. Patients with systemic onset JRA should be monitored for the development of abnormal coagulation tests [see Dosage and Administration (2.4) , Warnings and Precautions (5.15) , Adverse Reactions (6.1) , Animal Toxicology (13.2) , Clinical Studies (14.3) ] .
```

</details>

## q32 (multi)

**Question:** A patient on Plavix asks to buy omeprazole for heartburn. Is that OK?

**Reference:** No. Both labels say to avoid the combination: omeprazole (a CYP2C19 inhibitor) reduces clopidogrel's active metabolite and its antiplatelet effect. The Plavix label notes dexlansoprazole, lansoprazole and pantoprazole had less effect.

**Agent answer:**

**No, it is not recommended.** Concomitant use of Plavix (clopidogrel) and omeprazole should be avoided `[plavix, Drug Interactions]` `[prilosec, Drug Interactions]`.

### Key Reasons & Clinical Details:
* **Mechanism:** Clopidogrel is metabolized to its active metabolite in part by the enzyme CYP2C19 `[plavix, Drug Interactions]`. Omeprazole inhibits CYP2C19 activity, impairing this metabolism `[plavix, Warnings and Precautions]` `[prilosec, Warnings and Precautions]`.
* **Reduced Antiplatelet Activity:** Concomitant use reduces plasma concentrations of clopidogrel's active metabolite and significantly reduces the antiplatelet activity of Plavix `[plavix, Drug Interactions]` `[prilosec, Drug Interactions]`.
* **Dosing Separation Does Not Help:** This significant reduction in antiplatelet activity occurs even when omeprazole and Plavix are administered 12 hours apart `[plavix, Drug Interactions]` `[prilosec, Warnings and Precautions]`.
* **Alternatives:** Other proton pump inhibitors, such as dexlansoprazole, lansoprazole, and pantoprazole, have been shown to have less effect on the antiplatelet activity of Plavix compared to omeprazole or esomeprazole `[plavix, Drug Interactions]` `[plavix, Patient Counseling Information]`. Alternatively, the Prilosec label notes considering alternative anti-platelet therapy if omeprazole is required `[prilosec, Warnings and Precautions]`.

*gemini-3.5-flash, 2 search(es), 6636 tokens, 48.52 s*

- search `Plavix omeprazole` → [plavix, Drug Interactions], [plavix, Warnings and Precautions], [plavix, Warnings and Precautions], [plavix, Drug Interactions], [plavix, Patient Counseling Information]
- search `Prilosec clopidogrel Plavix` → [plavix, Drug Interactions], [plavix, Patient Counseling Information], [plavix, Drug Interactions], [prilosec, Drug Interactions], [prilosec, Warnings and Precautions]

<details><summary>Retrieved passages</summary>

**search:** `Plavix omeprazole`

```text
[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] . 7.2 CYP2C19 Inhibitors Clopidogrel is metabolized to its active metabolite in part by CYP2C19. Concomitant use of drugs that inhibit the activity of this enzyme results in reduced plasma concentrations of the active metabolite of clopidogrel and a reduction in platelet inhibition [see Warnings and Precautions (5.1) ] . Omeprazole or Esomeprazole Avoid concomitant use of Plavix with omeprazole or esomeprazole. In clinical studies, omeprazole was shown to reduce significantly the antiplatelet activity of Plavix when given concomitantly or 12 hours apart. A similar reduction in antiplatelet activity was observed with esomeprazole when given concomitantly with Plavix. Dexlansoprazole, lansoprazole, and pantoprazole had less effect on the antiplatelet activity of Plavix than did omeprazole or esomeprazole [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] .

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: Avoid concomitant use of Plavix with omeprazole or esomeprazole because both significantly reduce the antiplatelet activity of Plavix [see Drug Interactions (7.1) ] . 5.2 General Risk of Bleeding P2Y12 inhibitors (thienopyridines), including Plavix, increase the risk of bleeding. P2Y12 inhibitors (thienopyridines), inhibit platelet aggregation for the lifetime of the platelet (7-10 days). Because the half-life of clopidogrel's active metabolite is short, it may be possible to restore hemostasis by administering exogenous platelets; however, platelet transfusions within 4 hours of the loading dose or 2 hours of the maintenance dose may be less effective. Use of drugs that induce the activity of CYP2C19 would be expected to result in increased drug levels of the active metabolite of clopidogrel and might potentiate the bleeding risk. As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Drug Interactions (7.1) and Clinical Pharmacology (12.3) ] .

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: 5 WARNINGS AND PRECAUTIONS CYP2C19 inhibitors: Avoid concomitant use of omeprazole or esomeprazole. ( 5.1 ) Bleeding: Plavix increases risk of bleeding. ( 5.2 ) Discontinuation: Premature discontinuation increases risk of cardiovascular events. Discontinue 5 days prior to elective surgery that has a major risk of bleeding. ( 5.3 ) Thrombotic thrombocytopenic purpura (TTP) has been reported. ( 5.4 ) Cross-reactivity among thienopyridines has been reported. ( 5.5 ) 5.1 Diminished Antiplatelet Activity in Patients with Impaired CYP2C19 Function Clopidogrel is a prodrug. Inhibition of platelet aggregation by clopidogrel is achieved through an active metabolite. The metabolism of clopidogrel to its active metabolite can be impaired by genetic variations in CYP2C19 [see Boxed Warning ] . The metabolism of clopidogrel can also be impaired by drugs that inhibit CYP2C19, such as omeprazole or esomeprazole.

[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: 7 DRUG INTERACTIONS CYP2C19 inducers: Increases levels of clopidogrel active metabolite and increases platelet inhibition. ( 7.1 ) Opioids: Decreased exposure to clopidogrel. Consider use of parenteral antiplatelet agent. ( 7.3 ) Nonsteroidal anti-inflammatory drugs (NSAIDs), warfarin, selective serotonin and serotonin norepinephrine reuptake inhibitors (SSRIs, SNRIs): Increases risk of bleeding. ( 7.4 , 7.5 , 7.6 ) Other Antiplatelet Agents: Increases the risk of bleeding due to an additive effect. ( 7.7 ) Repaglinide (CYP2C8 substrates): Increases substrate plasma concentrations. ( 7.8 ) 7.1 CYP2C19 Inducers Since clopidogrel is metabolized to its active metabolite partly by CYP2C19, use of drugs that induce the activity of this enzyme would be expected to result in increased drug levels of the active metabolite of clopidogrel. Rifampin strongly induces CYP2C19 resulting to both an increase level of clopidogrel active metabolite and platelet inhibition, which in particular might potentiate the risk of bleeding.

[plavix, Patient Counseling Information] Plavix (clopidogrel)
Plavix (clopidogrel), Patient Counseling Information: Dexlansoprazole, lansoprazole, and pantoprazole had less pronounced effects on the antiplatelet activity of Plavix than did omeprazole or esomeprazole [see Drug Interactions (7.1) ] .
```

**search:** `Prilosec clopidogrel Plavix`

```text
[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] . 7.2 CYP2C19 Inhibitors Clopidogrel is metabolized to its active metabolite in part by CYP2C19. Concomitant use of drugs that inhibit the activity of this enzyme results in reduced plasma concentrations of the active metabolite of clopidogrel and a reduction in platelet inhibition [see Warnings and Precautions (5.1) ] . Omeprazole or Esomeprazole Avoid concomitant use of Plavix with omeprazole or esomeprazole. In clinical studies, omeprazole was shown to reduce significantly the antiplatelet activity of Plavix when given concomitantly or 12 hours apart. A similar reduction in antiplatelet activity was observed with esomeprazole when given concomitantly with Plavix. Dexlansoprazole, lansoprazole, and pantoprazole had less effect on the antiplatelet activity of Plavix than did omeprazole or esomeprazole [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] .

[plavix, Patient Counseling Information] Plavix (clopidogrel)
Plavix (clopidogrel), Patient Counseling Information: Dexlansoprazole, lansoprazole, and pantoprazole had less pronounced effects on the antiplatelet activity of Plavix than did omeprazole or esomeprazole [see Drug Interactions (7.1) ] .

[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: 7 DRUG INTERACTIONS CYP2C19 inducers: Increases levels of clopidogrel active metabolite and increases platelet inhibition. ( 7.1 ) Opioids: Decreased exposure to clopidogrel. Consider use of parenteral antiplatelet agent. ( 7.3 ) Nonsteroidal anti-inflammatory drugs (NSAIDs), warfarin, selective serotonin and serotonin norepinephrine reuptake inhibitors (SSRIs, SNRIs): Increases risk of bleeding. ( 7.4 , 7.5 , 7.6 ) Other Antiplatelet Agents: Increases the risk of bleeding due to an additive effect. ( 7.7 ) Repaglinide (CYP2C8 substrates): Increases substrate plasma concentrations. ( 7.8 ) 7.1 CYP2C19 Inducers Since clopidogrel is metabolized to its active metabolite partly by CYP2C19, use of drugs that induce the activity of this enzyme would be expected to result in increased drug levels of the active metabolite of clopidogrel. Rifampin strongly induces CYP2C19 resulting to both an increase level of clopidogrel active metabolite and platelet inhibition, which in particular might potentiate the risk of bleeding.

[prilosec, Drug Interactions] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Drug Interactions: Methotrexate Clinical Impact: Concomitant use of omeprazole with methotrexate (primarily at high dose) may elevate and prolong serum concentrations of methotrexate and/or its metabolite hydroxymethotrexate, possibly leading to methotrexate toxicities. No formal drug interaction studies of high-dose methotrexate with PPIs have been conducted [see Warnings and Precautions ( 5.11 )]. Intervention: A temporary withdrawal of PRILOSEC may be considered in some patients receiving high-dose methotrexate. CYP2C19 Substrates (e.g., clopidogrel, citalopram, cilostazol, phenytoin, diazepam) Clopidogrel Clinical Impact: Concomitant use of omeprazole 80 mg results in reduced plasma concentrations of the active metabolite of clopidogrel and a reduction in platelet inhibition [see Clinical Pharmacology ( 12.3 )]. There are no adequate combination studies of a lower dose of omeprazole or a higher dose of clopidogrel in comparison with the approved dose of clopidogrel. Intervention: Avoid concomitant use with PRILOSEC.

[prilosec, Warnings and Precautions] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Warnings and Precautions: The metabolism of clopidogrel to its active metabolite can be impaired by use with concomitant medications, such as omeprazole, that inhibit CYP2C19 activity. Concomitant use of clopidogrel with 80 mg omeprazole reduces the pharmacological activity of clopidogrel, even when administered 12 hours apart. When using PRILOSEC, consider alternative anti-platelet therapy [see Drug Interactions ( 7 ) and Clinical Pharmacology ( 12.3 )] . 5.8 Cyanocobalamin (Vitamin B-12) Deficiency Daily treatment with any acid-suppressing medications over a long period of time (e.g., longer than 3 years) may lead to malabsorption of cyanocobalamin (vitamin B-12) caused by hypo- or achlorhydria. Rare reports of cyanocobalamin deficiency occurring with acid-suppressing therapy have been reported in the literature. This diagnosis should be considered if clinical symptoms consistent with cyanocobalamin deficiency are observed in patients treated with PRILOSEC.
```

</details>

## q33 (multi)

**Question:** A customer with a sulfa allergy has prescriptions for Bactrim and Celebrex. What should the pharmacist flag?

**Reference:** Both are contraindicated: Bactrim with known sulfonamide hypersensitivity, and Celebrex in patients who have had allergic-type reactions to sulfonamides. Refer back to the prescriber.

**Agent answer:**

Based on the drug labels:

* **Bactrim** is contraindicated in patients with a known hypersensitivity to sulfonamides [bactrim, Contraindications].
* **Celebrex** is contraindicated in patients who have demonstrated allergic-type reactions to sulfonamides, and in patients with a known hypersensitivity to sulfonamides [celebrex, Contraindications]. 

The pharmacist should flag that both Bactrim and Celebrex contain sulfonamide components and are contraindicated in a patient with a sulfa allergy [bactrim, Contraindications, celebrex, Contraindications]. Please consult the supervising pharmacist before proceeding.

*gemini-3.5-flash-lite, 2 search(es), 3904 tokens, 2.59 s*

- search `Bactrim allergy contraindication sulfa` → [bactrim, Contraindications], [bactrim, Precautions], [bactrim, Warnings], [bactrim, Precautions], [bactrim, Warnings]
- search `Celebrex allergy contraindication sulfa sulfisoxazole` → [celebrex, Contraindications], [celebrex, Warnings and Precautions], [celebrex, Warnings and Precautions], [celebrex, Adverse Reactions], [celebrex, Warnings and Precautions]

<details><summary>Retrieved passages</summary>

**search:** `Bactrim allergy contraindication sulfa`

```text
[bactrim, Contraindications] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Contraindications: CONTRAINDICATIONS BACTRIM is contraindicated in the following situations: a known hypersensitivity to trimethoprim or sulfonamides history of drug-induced immune thrombocytopenia with use of trimethoprim and/or sulfonamides documented megaloblastic anemia due to folate deficiency pediatric patients less than 2 months of age marked hepatic damage severe renal insufficiency when renal function status cannot be monitored concomitant administration with dofetilide (see PRECAUTIONS ).

[bactrim, Precautions] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Precautions: PRECAUTIONS Development of Drug Resistant Bacteria Prescribing BACTRIM (sulfamethoxazole and trimethoprim) tablets in the absence of a proven or strongly suspected bacterial infection or a prophylactic indication is unlikely to provide benefit to the patient and increases the risk of the development of drug-resistant bacteria. Folate Deficiency Avoid use of BACTRIM in patients with impaired renal or hepatic function, in those with possible folate deficiency (e.g., the elderly, chronic alcoholics, patients receiving anticonvulsant therapy, patients with malabsorption syndrome, and patients in malnutrition states) and in those with severe allergies or bronchial asthma. Hematological changes indicative of folic acid deficiency may occur in elderly patients or in patients with preexisting folic acid deficiency or kidney failure. These effects are reversible by folinic acid therapy (see PRECAUTIONS, Geriatric Use ). Hemolysis In glucose-6-phosphate dehydrogenase deficient individuals, hemolysis may occur. This reaction is frequently dose-related.

[bactrim, Warnings] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Warnings: Hypersensitivity Reactions of the Respiratory Tract Cough, shortness of breath and pulmonary infiltrates potentially representing hypersensitivity reactions of the respiratory tract have been reported in association with sulfamethoxazole and trimethoprim treatment. Respiratory Failure Other severe pulmonary adverse reactions occurring within days to week of BACTRIM initiation and resulting in prolonged respiratory failure requiring mechanical ventilation or extracorporeal membrane oxygenation (ECMO), lung transplantation or death have also been reported in patients and otherwise healthy individuals treated with sulfamethoxazole and trimethoprim products. Circulatory Shock Circulatory shock with fever, severe hypotension, and confusion requiring intravenous fluid resuscitation and vasopressors has occurred within minutes to hours of re-challenge with sulfamethoxazole and trimethoprim products, including BACTRIM, in patients with history of recent (days to weeks) exposure to sulfamethoxazole and trimethoprim. Management of Hypersensitivity Reactions BACTRIM should be discontinued at the first appearance of skin rash or any sign of a serious adverse reaction.

[bactrim, Precautions] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Precautions: Hypoglycemia Cases of hypoglycemia in non-diabetic patients treated with BACTRIM are seen rarely, usually occurring after a few days of therapy. Patients with renal dysfunction, liver disease, malnutrition or those receiving high doses of BACTRIM are particularly at risk. Impaired Phenylalanine Metabolism The trimethoprim component of BACTRIM has been noted to impair phenylalanine metabolism, but this is of no significance in phenylketonuric patients on appropriate dietary restriction. Porphyria and Hypothyroidism Like other drugs containing sulfonamides, BACTRIM can precipitate porphyria crisis and hypothyroidism. Avoid use of BACTRIM in patients with porphyria or thyroid dysfunction. Potential Risk in the Treatment of Pneumocystis jirovecii Pneumonia in Patients with Acquired Immunodeficiency Syndrome (AIDS) AIDS patients may not tolerate or respond to BACTRIM in the same manner as non-AIDS patients.

[bactrim, Warnings] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Warnings: WARNINGS Embryofetal Toxicity Some epidemiologic studies suggest that exposure to BACTRIM during pregnancy may be associated with an increased risk of congenital malformations, particularly neural tube defects, cardiovascular malformations, urinary tract defects, oral clefts, and club foot. If BACTRIM is used during pregnancy, or if the patient becomes pregnant while taking this drug, the patient should be advised of the potential hazards to the fetus (see PRECAUTIONS ). Hypersensitivity and Other Serious or Fatal Reactions Fatalities and serious adverse reactions including severe cutaneous adverse reactions (SCARs) including Stevens-Johnson syndrome, toxic epidermal necrolysis, drug reaction with eosinophilia and systemic symptoms (DRESS), acute febrile neutrophilic dermatosis (AFND), acute generalized erythematous pustulosis (AGEP); fulminant hepatic necrosis; agranulocytosis, aplastic anemia and other blood dyscrasias; acute and delayed lung injury; anaphylaxis and circulatory shock have occurred with the administration of sulfamethoxazole and trimethoprim products, including BACTRIM (see ADVERSE REACTIONS ).
```

**search:** `Celebrex allergy contraindication sulfa sulfisoxazole`

```text
[celebrex, Contraindications] CELEBREX (celecoxib)
CELEBREX (celecoxib), Contraindications: 4 CONTRAINDICATIONS CELEBREX is contraindicated in the following patients: - Known hypersensitivity (e.g., anaphylactic reactions and serious skin reactions) to celecoxib, any components of the drug product [see Warnings and Precautions (5.7 , 5.9) ] . - History of asthma, urticaria, or other allergic-type reactions after taking aspirin or other NSAIDs. Severe, sometimes fatal, anaphylactic reactions to NSAIDs, have been reported in such patients [see Warnings and Precautions (5.7 , 5.8) ] . - In the setting of CABG surgery [see Warnings and Precautions (5.1) ] . - In patients who have demonstrated allergic-type reactions to sulfonamides [see Warnings and Precautions (5.7) ] . - Known hypersensitivity to celecoxib, or any components of the drug product or sulfonamides. ( 4 ) - History of asthma, urticaria, or other allergic-type reactions after taking aspirin or other NSAIDs. ( 4 ) - In the setting of CABG surgery. ( 4 )

[celebrex, Warnings and Precautions] CELEBREX (celecoxib)
CELEBREX (celecoxib), Warnings and Precautions: Seek emergency help if any anaphylactic reaction occurs. 5.8 Exacerbation of Asthma Related to Aspirin Sensitivity A subpopulation of patients with asthma may have aspirin-sensitive asthma which may include chronic rhinosinusitis complicated by nasal polyps; severe, potentially fatal bronchospasm; and/or intolerance to aspirin and other NSAIDs. Because cross-reactivity between aspirin and other NSAIDs has been reported in such aspirin-sensitive patients, CELEBREX is contraindicated in patients with this form of aspirin sensitivity [see Contraindications (4) ] . When CELEBREX is used in patients with preexisting asthma (without known aspirin sensitivity), monitor patients for changes in the signs and symptoms of asthma.

[celebrex, Warnings and Precautions] CELEBREX (celecoxib)
CELEBREX (celecoxib), Warnings and Precautions: Avoid the use of CELEBREX in patients with advanced renal disease unless the benefits are expected to outweigh the risk of worsening renal function. If CELEBREX is used in patients with advanced renal disease, monitor patients for signs of worsening renal function. Hyperkalemia Increases in serum potassium concentration, including hyperkalemia, have been reported with use of NSAIDs, even in some patients without renal impairment. In patients with normal renal function, these effects have been attributed to a hyporeninemic-hypoaldosteronism state. 5.7 Anaphylactic Reactions Celecoxib has been associated with anaphylactic reactions in patients with and without known hypersensitivity to celecoxib and in patients with aspirin sensitive asthma. CELEBREX is a sulfonamide and both NSAIDs and sulfonamides may cause allergic type reactions including anaphylactic symptoms and life-threatening or less severe asthmatic episodes in certain susceptible people [see Contraindications (4) and Warnings and Precautions (5.8) ] .

[celebrex, Adverse Reactions] CELEBREX (celecoxib)
CELEBREX (celecoxib), Adverse Reactions: The following adverse reactions occurred in 0.1% to 1.9% of patients treated with CELEBREX (100 mg to 200 mg twice daily or 200 mg once daily): Gastrointestinal: Constipation, diverticulitis, dysphagia, eructation, esophagitis, gastritis, gastroenteritis, gastroesophageal reflux, hemorrhoids, hiatal hernia, melena, dry mouth, stomatitis, tenesmus, vomiting Cardiovascular: Aggravated hypertension, angina pectoris, coronary artery disorder, myocardial infarction General: Hypersensitivity, allergic reaction, chest pain, cyst NOS, edema generalized, face edema, fatigue, fever, hot flushes, influenza-like symptoms, pain, peripheral pain Central, peripheral nervous system: Leg cramps, hypertonia, hypoesthesia, migraine, paresthesia, vertigo Hearing and vestibular: Deafness, tinnitus Heart rate and rhythm: Palpitation, tachycardia Liver and biliary: Hepatic enzyme increased (including SGOT increased, SGPT increased) Metabolic and nutritional: blood urea nitrogen (BUN) increased, creatine phosphokinase (CPK) increased, hypercholesterolemia, hyperglycemia, hypokalemia, NPN increased, creatinine increased, alkaline phosphatase increased, weight increased Musculoskeletal: Arthralgia, arthrosis, myalgia, synovitis, tendinitis Platelets (bleeding or clotting): Ecchymosis, epistaxis, thrombocythemia Psychiatric: Anorexia, anxiety, appetite

[celebrex, Warnings and Precautions] CELEBREX (celecoxib)
CELEBREX (celecoxib), Warnings and Precautions: 5.9 Serious Skin Reactions Serious skin reactions have occurred following treatment with CELEBREX, including erythema multiforme, exfoliative dermatitis, Stevens-Johnson Syndrome (SJS), toxic epidermal necrolysis (TEN), drug reaction with eosinophilia and systemic symptoms (DRESS), acute generalized exanthematous pustulosis (AGEP), and fixed drug eruption (FDE) which may present as a more severe variant known as generalized bullous fixed drug eruption (GBFDE). These serious events may occur without warning and can be fatal. Inform patients about the signs and symptoms of serious skin reactions, and to discontinue the use of CELEBREX at the first appearance of skin rash or any other sign of hypersensitivity. CELEBREX is contraindicated in patients with previous serious skin reactions to NSAIDs [see Contraindications (4) ] . 5.10 Drug Reaction with Eosinophilia and Systemic Symptoms (DRESS) Drug Reaction with Eosinophilia and Systemic Symptoms (DRESS) has been reported in patients taking NSAIDs such as CELEBREX.
```

</details>

## q34 (multi)

**Question:** A customer on warfarin wants an OTC pain reliever. What do the Tylenol and Advil labels say?

**Reference:** Tylenol: ask a doctor or pharmacist before use if taking warfarin. Advil: the stomach bleeding warning says the risk is higher with a blood thinner (anticoagulant), so ask a doctor before use. Both need a pharmacist or doctor check.

**Agent answer:**

Based on the drug labels:

* **Tylenol (Acetaminophen):** The label states to "ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin" [tylenol, Ask a Doctor or Pharmacist Before Use].
* **Advil (Ibuprofen) / Warfarin:** The warfarin (Jantoven) label lists ibuprofen under nonsteroidal anti-inflammatory agents (NSAIDs) and states that because bleeding risk is increased when these drugs are used concomitantly with warfarin, patients receiving any such drug with warfarin should be closely monitored [jantoven, Drug Interactions]. 

*Please refer any specific patient recommendations to the supervising pharmacist.*

*gemini-3.5-flash-lite, 2 search(es), 3899 tokens, 4.2 s*

- search `warfarin Tylenol acetaminophen interactions` → [jantoven, Drug Interactions], [jantoven, Drug Interactions], [jantoven, Drug Interactions], [jantoven, Drug Interactions], [tylenol, Ask a Doctor or Pharmacist Before Use]
- search `warfarin Advil ibuprofen interactions` → [jantoven, Drug Interactions], [naproxen, Drug Interactions], [jantoven, Drug Interactions], [jantoven, Drug Interactions], [celebrex, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `warfarin Tylenol acetaminophen interactions`

```text
[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: Because bleeding risk is increased when these drugs are used concomitantly with warfarin, closely monitor patients receiving any such drug with warfarin. Table 3: Drugs that Can Increase the Risk of Bleeding Drug Class Specific Drugs Anticoagulants argatroban, dabigatran, bivalirudin, desirudin, heparin, lepirudin Antiplatelet Agents aspirin, cilostazol, clopidogrel, dipyridamole, prasugrel, ticlopidine Nonsteroidal Anti-Inflammatory Agents celecoxib, diclofenac, diflunisal, fenoprofen, ibuprofen, indomethacin, ketoprofen, ketorolac, mefenamic acid, naproxen, oxaprozin, piroxicam, sulindac Serotonin Reuptake Inhibitors citalopram, desvenlafaxine, duloxetine, escitalopram, fluoxetine, fluvoxamine, milnacipran, paroxetine, sertraline, venlafaxine, vilazodone 7.4 Antibiotics and Antifungals There have been reports of changes in INR in patients taking warfarin and antibiotics or antifungals, but clinical pharmacokinetic studies have not shown consistent effects of these agents on plasma concentrations of warfarin. Closely monitor INR when starting or stopping any antibiotic or antifungal in patients taking warfarin.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7 DRUG INTERACTIONS Concomitant use of drugs that increase bleeding risk, antibiotics, antifungals, botanical (herbal) products, and inhibitors and inducers of CYP2C9, 1A2, or 3A4. ( 7 ) Consult labeling of all concurrently used drugs for complete information about interactions with JANTOVEN or increased risks for bleeding. ( 7 ) 7.1 General Information Drugs may interact with JANTOVEN through pharmacodynamic or pharmacokinetic mechanisms. Pharmacodynamic mechanisms for drug interactions with JANTOVEN are synergism (impaired hemostasis, reduced clotting factor synthesis), competitive antagonism (vitamin K), and alteration of the physiologic control loop for vitamin K metabolism (hereditary resistance). Pharmacokinetic mechanisms for drug interactions with JANTOVEN are mainly enzyme induction, enzyme inhibition, and reduced plasma protein binding. It is important to note that some drugs may interact by more than one mechanism.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7.5 Botanical (Herbal) Products and Foods More frequent INR monitoring should be performed when starting or stopping botanicals. Few adequate, well-controlled studies evaluating the potential for metabolic and/or pharmacologic interactions between botanicals and JANTOVEN exist. Due to a lack of manufacturing standardization with botanical medicinal preparations, the amount of active ingredients may vary. This could further confound the ability to assess potential interactions and effects on anticoagulation. Some botanicals may cause bleeding events when taken alone (e.g., garlic and Ginkgo biloba) and may have anticoagulant, antiplatelet, and/or fibrinolytic properties. These effects would be expected to be additive to the anticoagulant effects of JANTOVEN. Conversely, some botanicals may decrease the effects of JANTOVEN (e.g., co-enzyme Q 10 , St. John's wort, ginseng). Some botanicals and foods can interact with JANTOVEN through CYP450 interactions (e.g., echinacea, grapefruit juice, ginkgo, goldenseal, St. John's wort).

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: More frequent INR monitoring should be performed when starting or stopping other drugs, including botanicals, or when changing dosages of other drugs, including drugs intended for short-term use (e.g., antibiotics, antifungals, corticosteroids) [see Boxed Warning ]. Consult the labeling of all concurrently used drugs to obtain further information about interactions with JANTOVEN or adverse reactions pertaining to bleeding. 7.2 CYP450 Interactions CYP450 isozymes involved in the metabolism of warfarin include CYP2C9, 2C19, 2C8, 2C18, 1A2, and 3A4. The more potent warfarin S -enantiomer is metabolized by CYP2C9 while the R -enantiomer is metabolized by CYP1A2 and 3A4. Inhibitors of CYP2C9, 1A2, and/or 3A4 have the potential to increase the effect (increase INR) of warfarin by increasing the exposure of warfarin. Inducers of CYP2C9, 1A2, and/or 3A4 have the potential to decrease the effect (decrease INR) of warfarin by decreasing the exposure of warfarin.

[tylenol, Ask a Doctor or Pharmacist Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin
```

**search:** `warfarin Advil ibuprofen interactions`

```text
[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: Because bleeding risk is increased when these drugs are used concomitantly with warfarin, closely monitor patients receiving any such drug with warfarin. Table 3: Drugs that Can Increase the Risk of Bleeding Drug Class Specific Drugs Anticoagulants argatroban, dabigatran, bivalirudin, desirudin, heparin, lepirudin Antiplatelet Agents aspirin, cilostazol, clopidogrel, dipyridamole, prasugrel, ticlopidine Nonsteroidal Anti-Inflammatory Agents celecoxib, diclofenac, diflunisal, fenoprofen, ibuprofen, indomethacin, ketoprofen, ketorolac, mefenamic acid, naproxen, oxaprozin, piroxicam, sulindac Serotonin Reuptake Inhibitors citalopram, desvenlafaxine, duloxetine, escitalopram, fluoxetine, fluvoxamine, milnacipran, paroxetine, sertraline, venlafaxine, vilazodone 7.4 Antibiotics and Antifungals There have been reports of changes in INR in patients taking warfarin and antibiotics or antifungals, but clinical pharmacokinetic studies have not shown consistent effects of these agents on plasma concentrations of warfarin. Closely monitor INR when starting or stopping any antibiotic or antifungal in patients taking warfarin.

[naproxen, Drug Interactions] Naproxen (naproxen)
Naproxen (naproxen), Drug Interactions: 7 DRUG INTERACTIONS See Table 1 for clinically significant drug interactions with naproxen. Table 1: Clinically Significant Drug Interactions with naproxen Drugs That Interfere with Hemostasis Clinical Impact: Naproxen and anticoagulants such as warfarin have a synergistic effect on bleeding. The concomitant use of naproxen and anticoagulants have an increased risk of serious bleeding compared to the use of either drug alone. Serotonin release by platelets plays an important role in hemostasis. Case-control and cohort epidemiological studies showed that concomitant use of drugs that interfere with serotonin reuptake and an NSAID may potentiate the risk of bleeding more than an NSAID alone. Intervention: Monitor patients with concomitant use of naproxen tablets with anticoagulants (e.g., warfarin), antiplatelet agents (e.g., aspirin), selective serotonin reuptake inhibitors (SSRIs), and serotonin norepinephrine reuptake inhibitors (SNRIs) for signs of bleeding [ see Warnings and Precautions (5.12) ].

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7 DRUG INTERACTIONS Concomitant use of drugs that increase bleeding risk, antibiotics, antifungals, botanical (herbal) products, and inhibitors and inducers of CYP2C9, 1A2, or 3A4. ( 7 ) Consult labeling of all concurrently used drugs for complete information about interactions with JANTOVEN or increased risks for bleeding. ( 7 ) 7.1 General Information Drugs may interact with JANTOVEN through pharmacodynamic or pharmacokinetic mechanisms. Pharmacodynamic mechanisms for drug interactions with JANTOVEN are synergism (impaired hemostasis, reduced clotting factor synthesis), competitive antagonism (vitamin K), and alteration of the physiologic control loop for vitamin K metabolism (hereditary resistance). Pharmacokinetic mechanisms for drug interactions with JANTOVEN are mainly enzyme induction, enzyme inhibition, and reduced plasma protein binding. It is important to note that some drugs may interact by more than one mechanism.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7.5 Botanical (Herbal) Products and Foods More frequent INR monitoring should be performed when starting or stopping botanicals. Few adequate, well-controlled studies evaluating the potential for metabolic and/or pharmacologic interactions between botanicals and JANTOVEN exist. Due to a lack of manufacturing standardization with botanical medicinal preparations, the amount of active ingredients may vary. This could further confound the ability to assess potential interactions and effects on anticoagulation. Some botanicals may cause bleeding events when taken alone (e.g., garlic and Ginkgo biloba) and may have anticoagulant, antiplatelet, and/or fibrinolytic properties. These effects would be expected to be additive to the anticoagulant effects of JANTOVEN. Conversely, some botanicals may decrease the effects of JANTOVEN (e.g., co-enzyme Q 10 , St. John's wort, ginseng). Some botanicals and foods can interact with JANTOVEN through CYP450 interactions (e.g., echinacea, grapefruit juice, ginkgo, goldenseal, St. John's wort).

[celebrex, Drug Interactions] CELEBREX (celecoxib)
CELEBREX (celecoxib), Drug Interactions: 7 DRUG INTERACTIONS See Table 3 for clinically significant drug interactions with celecoxib. Table 3: Clinically Significant Drug Interactions with Celecoxib Drugs that Interfere with Hemostasis Clinical Impact: - Celecoxib and anticoagulants such as warfarin have a synergistic effect on bleeding. The concomitant use of Celecoxib and anticoagulants have an increased risk of serious bleeding compared to the use of either drug alone. - Serotonin release by platelets plays an important role in hemostasis. Case-control and cohort epidemiological studies showed that concomitant use of drugs that interfere with serotonin reuptake and an NSAID may potentiate the risk of bleeding more than an NSAID alone. Intervention: Monitor patients with concomitant use of CELEBREX with anticoagulants (e.g., warfarin), antiplatelet drugs (e.g., aspirin), SSRIs, and SNRIs for signs of bleeding [see Warnings and Precautions (5.12) ] .
```

</details>

## q35 (multi)

**Question:** A patient on Jantoven was just prescribed Bactrim. What monitoring is needed?

**Reference:** Bactrim may prolong prothrombin time in patients on warfarin, so monitor PT/INR and reassess coagulation. The Jantoven label lists antibiotics among drugs that affect INR and says to consult the labels of all drugs used together.

**Agent answer:**

When a patient on Jantoven (warfarin) is prescribed Bactrim (sulfamethoxazole/trimethoprim):

* **Monitor prothrombin time and INR:** Bactrim may prolong the prothrombin time and increase the effect of warfarin (since sulfamethoxazole is a CYP2C9 inhibitor) [bactrim, Drug Interactions]. 
* **Frequency of monitoring:** More frequent INR monitoring should be performed when starting or stopping short-term drugs such as antibiotics [jantoven, Drug Interactions]. The coagulation time should be reassessed [bactrim, Drug Interactions], and patients should be closely monitored for an increased risk of bleeding.

*gemini-3.5-flash-lite, 1 search(es), 2680 tokens, 2.55 s*

- search `Jantoven warfarin Bactrim monitoring INR interactions` → [bactrim, Drug Interactions], [jantoven, Drug Interactions], [jantoven, Drug Interactions], [jantoven, Drug Interactions], [jantoven, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `Jantoven warfarin Bactrim monitoring INR interactions`

```text
[bactrim, Drug Interactions] Bactrim (sulfamethoxazole and trimethoprim)
Bactrim (sulfamethoxazole and trimethoprim), Drug Interactions: Drug Interactions Potential for BACTRIM to Affect Other Drugs Trimethoprim is an inhibitor of CYP2C8 as well as OCT2 transporter. Sulfamethoxazole is an inhibitor of CYP2C9. Avoid coadministration of BACTRIM with drugs that are substrates of CYP2C8 and 2C9 or OCT2. Table 1: Drug Interactions with BACTRIM Drug(s) Recommendation Comments Diuretics Avoid concurrent use In elderly patients concurrently receiving certain diuretics, primarily thiazides, an increased incidence of thrombocytopenia with purpura has been reported. Warfarin Monitor prothrombin time and INR It has been reported that BACTRIM may prolong the prothrombin time in patients who are receiving the anticoagulant warfarin (a CYP2C9 substrate). This interaction should be kept in mind when BACTRIM is given to patients already on anticoagulant therapy, and the coagulation time should be reassessed. Phenytoin Monitor serum phenytoin levels BACTRIM may inhibit the hepatic metabolism of phenytoin (a CYP2C9 substrate).

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7 DRUG INTERACTIONS Concomitant use of drugs that increase bleeding risk, antibiotics, antifungals, botanical (herbal) products, and inhibitors and inducers of CYP2C9, 1A2, or 3A4. ( 7 ) Consult labeling of all concurrently used drugs for complete information about interactions with JANTOVEN or increased risks for bleeding. ( 7 ) 7.1 General Information Drugs may interact with JANTOVEN through pharmacodynamic or pharmacokinetic mechanisms. Pharmacodynamic mechanisms for drug interactions with JANTOVEN are synergism (impaired hemostasis, reduced clotting factor synthesis), competitive antagonism (vitamin K), and alteration of the physiologic control loop for vitamin K metabolism (hereditary resistance). Pharmacokinetic mechanisms for drug interactions with JANTOVEN are mainly enzyme induction, enzyme inhibition, and reduced plasma protein binding. It is important to note that some drugs may interact by more than one mechanism.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: More frequent INR monitoring should be performed when starting or stopping other drugs, including botanicals, or when changing dosages of other drugs, including drugs intended for short-term use (e.g., antibiotics, antifungals, corticosteroids) [see Boxed Warning ]. Consult the labeling of all concurrently used drugs to obtain further information about interactions with JANTOVEN or adverse reactions pertaining to bleeding. 7.2 CYP450 Interactions CYP450 isozymes involved in the metabolism of warfarin include CYP2C9, 2C19, 2C8, 2C18, 1A2, and 3A4. The more potent warfarin S -enantiomer is metabolized by CYP2C9 while the R -enantiomer is metabolized by CYP1A2 and 3A4. Inhibitors of CYP2C9, 1A2, and/or 3A4 have the potential to increase the effect (increase INR) of warfarin by increasing the exposure of warfarin. Inducers of CYP2C9, 1A2, and/or 3A4 have the potential to decrease the effect (decrease INR) of warfarin by decreasing the exposure of warfarin.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: Because bleeding risk is increased when these drugs are used concomitantly with warfarin, closely monitor patients receiving any such drug with warfarin. Table 3: Drugs that Can Increase the Risk of Bleeding Drug Class Specific Drugs Anticoagulants argatroban, dabigatran, bivalirudin, desirudin, heparin, lepirudin Antiplatelet Agents aspirin, cilostazol, clopidogrel, dipyridamole, prasugrel, ticlopidine Nonsteroidal Anti-Inflammatory Agents celecoxib, diclofenac, diflunisal, fenoprofen, ibuprofen, indomethacin, ketoprofen, ketorolac, mefenamic acid, naproxen, oxaprozin, piroxicam, sulindac Serotonin Reuptake Inhibitors citalopram, desvenlafaxine, duloxetine, escitalopram, fluoxetine, fluvoxamine, milnacipran, paroxetine, sertraline, venlafaxine, vilazodone 7.4 Antibiotics and Antifungals There have been reports of changes in INR in patients taking warfarin and antibiotics or antifungals, but clinical pharmacokinetic studies have not shown consistent effects of these agents on plasma concentrations of warfarin. Closely monitor INR when starting or stopping any antibiotic or antifungal in patients taking warfarin.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: Examples of inhibitors and inducers of CYP2C9, 1A2, and 3A4 are below in Table 2; however, this list should not be considered all-inclusive. Consult the labeling of all concurrently used drugs to obtain further information about CYP450 interaction potential. The CYP450 inhibition and induction potential should be considered when starting, stopping, or changing dose of concomitant medications. Closely monitor INR if a concomitant drug is a CYP2C9, 1A2, and/or 3A4 inhibitor or inducer.
```

</details>

## q36 (multi)

**Question:** Which allows more pills per day: Advil Liqui-Gels or Aleve Liquid Gels?

**Reference:** Advil: up to 6 capsules (200 mg ibuprofen) in 24 hours, 1 every 4-6 hours. Aleve: up to 3 capsules (220 mg naproxen sodium) in 24 hours, 1 every 8-12 hours. Aleve needs fewer doses because each one lasts longer.

**Agent answer:**

Based on the product labeling:

* **Advil Liqui-Gels** allows a maximum of **6 capsules in 24 hours** for adults and children 12 years and older [advil, Dosage and Administration].
* **Aleve Liquid Gels** allows a maximum of **3 capsules in a 24-hour period** (and no more than 2 capsules in any 8- to 12-hour period) for adults and children 12 years and older [aleve, Dosage and Administration].

Therefore, **Advil Liqui-Gels** allows more pills per day.

*gemini-3.5-flash-lite, 2 search(es), 2549 tokens, 2.53 s*

- search `Advil Liqui-Gels dosing pills per day` → [advil, Active Ingredient], [advil, Dosage and Administration], [aleve, Dosage and Administration], [advil, Inactive Ingredients], [advil, Warnings]
- search `Aleve Liquid Gels dosing pills per day` → [aleve, Dosage and Administration], [aleve, Active Ingredient], [aleve, Indications and Usage], [aleve, Ask a Doctor or Pharmacist Before Use], [aleve, Warnings]

<details><summary>Retrieved passages</summary>

**search:** `Advil Liqui-Gels dosing pills per day`

```text
[advil, Active Ingredient] Advil (ibuprofen)
Advil (ibuprofen), Active Ingredient: Active ingredient (in each capsule) Solubilized ibuprofen equal to 200 mg ibuprofen (NSAID)* (present as the free acid and potassium salt) *nonsteroidal anti-inflammatory drug

[advil, Dosage and Administration] Advil (ibuprofen)
Advil (ibuprofen), Dosage and Administration: Directions do not take more than directed the smallest effective dose should be used adults and children 12 years and over: take 1 capsule every 4 to 6 hours while symptoms persist if pain or fever does not respond to 1 capsule, 2 capsules may be used do not exceed 6 capsules in 24 hours, unless directed by a doctor children under 12 years: ask a doctor

[aleve, Dosage and Administration] Aleve (naproxen sodium)
Aleve (naproxen sodium), Dosage and Administration: Directions - do not take more than directed - the smallest effective dose should be used - drink a full glass of water with each dose Adults and children 12 years and older - take 1 capsule every 8 to 12 hours while symptoms last - for the first dose you may take 2 capsules within the first hour - do not exceed 2 capsules in any 8- to 12-hour period - do not exceed 3 capsules in a 24-hour period Children under 12 years of age - ask a doctor

[advil, Inactive Ingredients] Advil (ibuprofen)
Advil (ibuprofen), Inactive Ingredients: Inactive ingredients Advil Liqui-Gels FD&C green no. 3, gelatin, lecithin (soybean), medium-chain triglycerides, pharmaceutical ink, polyethylene glycol, potassium hydroxide, purified water, sorbitol sorbitan solution Advil Liqui-Gels Minis FD&C green no. 3, gelatin, medium-chain triglycerides, pharmaceutical ink, polyethylene glycol, potassium hydroxide, purified water, sorbitol sorbitan solution

[advil, Warnings] Advil (ibuprofen)
Advil (ibuprofen), Warnings: The risk is higher if you use more than directed or for longer than directed.
```

**search:** `Aleve Liquid Gels dosing pills per day`

```text
[aleve, Dosage and Administration] Aleve (naproxen sodium)
Aleve (naproxen sodium), Dosage and Administration: Directions - do not take more than directed - the smallest effective dose should be used - drink a full glass of water with each dose Adults and children 12 years and older - take 1 capsule every 8 to 12 hours while symptoms last - for the first dose you may take 2 capsules within the first hour - do not exceed 2 capsules in any 8- to 12-hour period - do not exceed 3 capsules in a 24-hour period Children under 12 years of age - ask a doctor

[aleve, Active Ingredient] Aleve (naproxen sodium)
Aleve (naproxen sodium), Active Ingredient: Active ingredient (in each capsule) Naproxen sodium 220 mg (naproxen 200 mg) (NSAID) nonsteroidal anti-inflammatory drug

[aleve, Indications and Usage] Aleve (naproxen sodium)
Aleve (naproxen sodium), Indications and Usage: Uses temporarily relieves minor aches and pains due to: minor pain of arthritis muscular aches backache menstrual cramps headache toothache the common cold temporarily reduces fever

[aleve, Ask a Doctor or Pharmacist Before Use] Aleve (naproxen sodium)
Aleve (naproxen sodium), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are under a doctor's care for any serious condition taking aspirin for heart attack or stroke, because naproxen may decrease this benefit of aspirin taking any other drug

[aleve, Warnings] Aleve (naproxen sodium)
Aleve (naproxen sodium), Warnings: Stomach bleeding warning This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you: are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs (aspirin, ibuprofen, naproxen, or others) have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal. The risk is higher if you use more than directed or for longer than directed. Allergy alert Naproxen sodium may cause a severe allergic reaction, especially in people allergic to aspirin.
```

</details>

## q37 (multi)

**Question:** Aleve and Flanax are both naproxen sodium 220 mg. Do their labels give the same pregnancy warning?

**Reference:** No. Both say to ask a health professional, but Aleve says to avoid use in the last 3 months of pregnancy, while Flanax says to avoid it at 20 weeks or later, unless a doctor directs.

**Agent answer:**

No, their labels do not give the exact same pregnancy warning text. 

* The **Aleve** label states: "If pregnant or breast-feeding, ask a health professional before use. It is especially important not to use naproxen sodium during the last 3 months of pregnancy unless definitely directed to do so by a doctor because it may cause problems in the unborn child or complications during delivery" [aleve, Pregnancy or Breast-feeding].
* The **Flanax** label states: "If pregnant or breast-feeding, ask a health professional before use. It is especially important not to use naproxen sodium at 20 weeks or later in pregnancy unless definitely directed to do so by a doctor because it may cause problems in the unborn child or complications during delivery" [flanax, Pregnancy or Breast-feeding].

*gemini-3.5-flash-lite, 1 search(es), 2346 tokens, 2.82 s*

- search `Aleve pregnancy warning` → [aleve, Pregnancy or Breast-feeding], [aleve, Warnings], [naproxen, Pregnancy], [flanax, Pregnancy or Breast-feeding], [naproxen, Pregnancy]

<details><summary>Retrieved passages</summary>

**search:** `Aleve pregnancy warning`

```text
[aleve, Pregnancy or Breast-feeding] Aleve (naproxen sodium)
Aleve (naproxen sodium), Pregnancy or Breast-feeding: If pregnant or breast-feeding, ask a health professional before use. It is especially important not to use naproxen sodium during the last 3 months of pregnancy unless definitely directed to do so by a doctor because it may cause problems in the unborn child or complications during delivery.

[aleve, Warnings] Aleve (naproxen sodium)
Aleve (naproxen sodium), Warnings: Stomach bleeding warning This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you: are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs (aspirin, ibuprofen, naproxen, or others) have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal. The risk is higher if you use more than directed or for longer than directed. Allergy alert Naproxen sodium may cause a severe allergic reaction, especially in people allergic to aspirin.

[naproxen, Pregnancy] Naproxen (naproxen)
Naproxen (naproxen), Pregnancy: Premature Closure of Fetal Ductus Arteriosus: Published literature reports that the use of NSAIDs at about 30 weeks of gestation and later in pregnancy may cause premature closure of the fetal ductus arteriosus. Oligohydramnios/Neonatal Renal Impairment: Published studies and postmarketing reports describe maternal NSAID use at about 20 weeks gestation or later in pregnancy associated with fetal renal dysfunction leading to oligohydramnios, and in some cases, neonatal renal impairment. These adverse outcomes are seen, on average, after days to weeks of treatment, although oligohydramnios has been infrequently reported as soon as 48 hours after NSAID initiation. In many cases, but not all, the decrease in amniotic fluid was transient and reversible with cessation of the drug. There have been a limited number of case reports of maternal NSAID use and neonatal renal dysfunction without oligohydramnios, some of which were irreversible.

[flanax, Pregnancy or Breast-feeding] Flanax (naproxen sodium)
Flanax (naproxen sodium), Pregnancy or Breast-feeding: If pregnant or breast-feeding, ask a health professional before use. It is especially important not to use naproxen sodium at 20 weeks or later in pregnancy unless definitely directed to do so by a doctor because it may cause problems in the unborn child or complications during delivery.

[naproxen, Pregnancy] Naproxen (naproxen)
Naproxen (naproxen), Pregnancy: 8.1 Pregnancy Risk Summary Use of NSAIDs, including Naproxen tablets, can cause premature closure of the fetal ductus arteriosus and fetal renal dysfunction leading to oligohydramnios and, in some cases, neonatal renal impairment. Because of these risks, limit dose and duration of Naproxen Tablets, use between about 20 and 30 weeks of gestation, and avoid Naproxen Tablets, use at about 30 weeks of gestation and later in pregnancy (see Clinical Considerations, Data). Premature Closure of Fetal Ductus Arteriosus Use of NSAIDs, including naproxen tablets, at about 30 weeks gestation or later in pregnancy increases the risk of premature closure of the fetal ductus arteriosus. Oligohydramnios/Neonatal Renal Impairment Use of NSAIDs at about 20 weeks gestation or later in pregnancy has been associated with cases of fetal renal dysfunction leading to oligohydramnios, and in some cases, neonatal renal impairment.
```

</details>

## q38 (multi)

**Question:** A patient who had anaphylaxis to penicillin brings prescriptions for Amoxil and Augmentin. Can either be dispensed?

**Reference:** Neither. Both are contraindicated in patients with serious hypersensitivity (e.g., anaphylaxis or Stevens-Johnson syndrome) to amoxicillin or other beta-lactams such as penicillins and cephalosporins. Contact the prescriber.

**Agent answer:**

**No, neither Amoxil nor Augmentin can be dispensed.** 

According to their prescribing information:
* **Amoxil (amoxicillin):** Is contraindicated in patients who have experienced a serious hypersensitivity reaction (such as anaphylaxis) to amoxicillin or other $\beta$-lactam antibiotics (penicillins and cephalosporins) [amoxil, Contraindications].
* **Augmentin (amoxicillin and clavulanate potassium):** Is contraindicated in patients with a history of a serious hypersensitivity reaction (such as anaphylaxis) to Augmentin or other $\beta$-lactams (penicillins or cephalosporins) [augmentin, Contraindications].

*gemini-3.5-flash-lite, 2 search(es), 5302 tokens, 3.44 s*

- search `Amoxil Contraindications hypersensitivity anaphylaxis` → [amoxil, Contraindications], [amoxil, Warnings and Precautions], [amoxil, Warnings and Precautions], [amoxil, Adverse Reactions], [amoxil, Warnings and Precautions]
- search `Augmentin Contraindications hypersensitivity anaphylaxis` → [augmentin, Contraindications], [augmentin, Warnings and Precautions], [augmentin, Warnings and Precautions], [amoxil, Contraindications], [augmentin, Warnings and Precautions]

<details><summary>Retrieved passages</summary>

**search:** `Amoxil Contraindications hypersensitivity anaphylaxis`

```text
[amoxil, Contraindications] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Contraindications: Amoxicillin is contraindicated in patients who have experienced a serious hypersensitivity reaction (e.g., anaphylaxis or Stevens-Johnson syndrome) to Amoxicillin or to other β-lactam antibiotics (e.g., penicillins and cephalosporins).

[amoxil, Warnings and Precautions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Warnings and Precautions: 5.1 Anaphylactic Reactions Serious and occasionally fatal hypersensitivity (anaphylactic) reactions have been reported in patients on penicillin therapy including Amoxicillin. Although anaphylaxis is more frequent following parenteral therapy, it has occurred in patients on oral penicillins. These reactions are more likely to occur in individuals with a history of penicillin hypersensitivity and/or a history of sensitivity to multiple allergens. There have been reports of individuals with a history of penicillin hypersensitivity who have experienced severe reactions when treated with cephalosporins. Before initiating therapy with Amoxicillin, careful inquiry should be made regarding previous hypersensitivity reactions to penicillins, cephalosporins, or other allergens. 5.2 Clostridium difficile Associated Diarrhea Clostridium difficile associated diarrhea (CDAD) has been reported with use of nearly all antibacterial agents, including Amoxicillin, and may range in severity from mild diarrhea to fatal colitis. Treatment with antibacterial agents alters the normal flora of the colon leading to overgrowth of C. difficile.

[amoxil, Warnings and Precautions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Warnings and Precautions: Prescribing Amoxicillin either in the absence of a proven or strongly suspected bacterial infection is unlikely to provide benefit to the patient, and increases the risk of the development of drug-resistant bacteria. 5.4 Use in Patients With Mononucleosis A high percentage of patients with mononucleosis who receive Amoxicillin develop an erythematous skin rash. Thus Amoxicillin should not be administered to patients with mononucleosis. 5.5 Phenylketonurics The oral suspensions of Amoxicillin do not contain phenylalanine and can be used by phenylketonurics.

[amoxil, Adverse Reactions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Adverse Reactions: For more information on adverse reactions with clarithromycin or lansoprazole, refer to the Adverse Reactions section of their package inserts. 6.2 Postmarketing or Other Experience In addition to adverse events reported from clinical trials, the following events have been identified during postmarketing use of penicillins. Because they are reported voluntarily from a population of unknown size, estimates of frequency cannot be made. These events have been chosen for inclusion due to a combination of their seriousness, frequency of reporting, or potential causal connection to Amoxicillin. Infections and Infestations: Mucocutaneous candidiasis. Gastrointestinal: Black hairy tongue, and hemorrhagic/pseudomembranous colitis. Onset of pseudomembranous colitis symptoms may occur during or after antibacterial treatment [see Warnings and Precautions (5.2)]. Hypersensitivity Reactions: Anaphylaxis [see Warnings and Precautions (5.1)]. Serum sickness-like reactions, erythematous maculopapular rashes, erythema multiforme, Stevens-Johnson syndrome, exfoliative dermatitis, toxic epidermal necrolysis, acute generalized exanthematous pustulosis, hypersensitivity vasculitis, and urticaria have been reported.

[amoxil, Warnings and Precautions] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Warnings and Precautions: C. difficile produces toxins A and B which contribute to the development of CDAD. Hypertoxin-producing strains of C. difficile cause increased morbidity and mortality, as these infections can be refractory to antimicrobial therapy and may require colectomy. CDAD must be considered in all patients who present with diarrhea following antibacterial use. Careful medical history is necessary since CDAD has been reported to occur over 2 months after the administration of antibacterial agents. If CDAD is suspected or confirmed, ongoing antibiotic use not directed against C. difficile may need to be discontinued. Appropriate fluid and electrolyte management, protein supplementation, antibiotic treatment of C. difficile, and surgical evaluation should be instituted as clinically indicated. 5.3 Potential for Microbial Overgrowth or Bacterial Resistance The possibility of superinfections with fungal or bacterial pathogens should be considered during therapy. If superinfections occur, Amoxicillin should be discontinued and appropriate therapy instituted.
```

**search:** `Augmentin Contraindications hypersensitivity anaphylaxis`

```text
[augmentin, Contraindications] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Contraindications: 4 CONTRAINDICATIONS History of a serious hypersensitivity reaction (e.g., anaphylaxis or Stevens-Johnson syndrome) to AUGMENTIN or to other beta-lactams (e.g., penicillins or cephalosporins). ( 4.1 ) History of cholestatic jaundice/hepatic dysfunction associated with AUGMENTIN. ( 4.2 ) 4.1 Serious Hypersensitivity Reactions AUGMENTIN is contraindicated in patients with a history of serious hypersensitivity reactions (e.g., anaphylaxis or Stevens-Johnson syndrome) to amoxicillin, clavulanate or to other beta-lactam antibacterial drugs (e.g., penicillins and cephalosporins). 4.2 Cholestatic Jaundice/Hepatic Dysfunction AUGMENTIN is contraindicated in patients with a previous history of cholestatic jaundice/hepatic dysfunction associated with AUGMENTIN.

[augmentin, Warnings and Precautions] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Warnings and Precautions: These reactions are more likely to occur in individuals with a history of penicillin hypersensitivity and/or a history of sensitivity to multiple allergens. Before initiating therapy with AUGMENTIN, careful inquiry should be made regarding previous hypersensitivity reactions to penicillins, cephalosporins, or other allergens. If an allergic reaction occurs, AUGMENTIN should be discontinued, and appropriate therapy instituted. 5.2 Severe Cutaneous Adverse Reactions AUGMENTIN may cause severe cutaneous adverse reactions (SCAR), such as Stevens-Johnson syndrome (SJS), toxic epidermal necrolysis (TEN), drug reaction with eosinophilia and systemic symptoms (DRESS), and acute generalized exanthematous pustulosis (AGEP). If patients develop a skin rash, they should be monitored closely, and AUGMENTIN discontinued if lesions progress. 5.3 Drug-Induced Enterocolitis Syndrome (DIES) Drug-induced enterocolitis syndrome (DIES) has been reported with use of amoxicillin, a componet of AUGMENTIN [see Adverse Reactions (6.2)], with most cases occurring in pediatric patients < 18 years of age.

[augmentin, Warnings and Precautions] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Warnings and Precautions: 5 WARNINGS AND PRECAUTIONS Serious (including fatal) hypersensitivity reactions: Discontinue AUGMENTIN if a reaction occurs. ( 5.1 ) Severe Cutaneous Adverse Reactions (SCAR): Monitor closely. Discontinue if rash progresses. ( 5.2 ) Drug-induced enterocolitis syndrome (DIES) has been reported with use of Amoxicillin, A componet of Augmentin. If this occures, discontinue AUGMENIN and institute appropriate therapy ( 5.3 ) Hepatic dysfunction and cholestatic jaundice: Discontinue if signs/symptoms of hepatitis occur. Monitor liver function tests in patients with hepatic impairment. ( 5.4 ) Clostridioides difficile -associated diarrhea (CDAD): Evaluate patients if diarrhea occurs. ( 5.5 ) Patients with mononucleosis who receive AUGMENTIN develop skin rash. Avoid AUGMENTIN use in these patients. ( 5.6 Overgrowth: The possibility of superinfections with fungal or bacterial pathogens should be considered during therapy. ( 5.7 ) 5.1 Hypersensitivity Reactions Serious and occasionally fatal hypersensitivity (anaphylactic) reactions have been reported in patients receiving beta-lactam antibacterials, including AUGMENTIN.

[amoxil, Contraindications] Amoxil (amoxicillin oral susp)
Amoxil (amoxicillin oral susp), Contraindications: Amoxicillin is contraindicated in patients who have experienced a serious hypersensitivity reaction (e.g., anaphylaxis or Stevens-Johnson syndrome) to Amoxicillin or to other β-lactam antibiotics (e.g., penicillins and cephalosporins).

[augmentin, Warnings and Precautions] Augmentin (amoxicillin and clavulanate potassium)
Augmentin (amoxicillin and clavulanate potassium), Warnings and Precautions: C. difficile produces toxins A and B which contribute to the development of CDAD. Hypertoxin-producing strains of C. difficile cause increased morbidity and mortality, as these infections can be refractory to antimicrobial therapy and may require colectomy. CDAD must be considered in all patients who present with diarrhea following antibacterial use. Careful medical history is necessary since CDAD has been reported to occur over 2 months after the administration of antibacterial agents. If CDAD is suspected or confirmed, ongoing antibacterial use not directed against C. difficile may need to be discontinued. Appropriate fluid and electrolyte management, protein supplementation, antibacterial treatment of C. difficile , and surgical evaluation should be instituted as clinically indicated. 5.6 Skin Rash in Patients with Mononucleosis A high percentage of patients with mononucleosis who receive amoxicillin develop an erythematous skin rash. Thus, AUGMENTIN should not be administered to patients with mononucleosis.
```

</details>

## q39 (multi)

**Question:** A patient on Plavix wants to take Advil for back pain. What are the concerns?

**Reference:** Plavix and NSAIDs together increase the risk of GI bleeding. Advil's stomach bleeding warning says to ask a doctor first if that warning applies, and its heart attack and stroke warning also matters for cardiac patients. Refer to the pharmacist or doctor.

**Agent answer:**

The main concerns with taking Advil (ibuprofen) while on Plavix (clopidogrel) include:

* **Increased Bleeding Risk:** Coadministration of Plavix and nonsteroidal anti-inflammatory drugs (NSAIDs) like Advil increases the risk of gastrointestinal bleeding [plavix, Drug Interactions]. Furthermore, Plavix increases the general risk of bleeding [plavix, Warnings and Precautions], and Advil's stomach bleeding warning notes that the chance of severe stomach bleeding is higher if you are taking a blood-thinning drug [advil, Warnings]. 
* **Risk Factors:** The risk of bleeding is heightened by the chronic use of NSAIDs along with antiplatelet agents [plavix, Warnings and Precautions], and the chance of stomach bleeding with Advil is also higher in individuals who have had stomach ulcers or bleeding problems, or who take more or for a longer time than directed [advil, Warnings].

Please refer the patient to their supervising pharmacist or healthcare provider before they take Advil with Plavix.

*gemini-3.5-flash-lite, 2 search(es), 5441 tokens, 3.38 s*

- search `Plavix Advil interaction bleeding warning` → [plavix, Patient Counseling Information], [plavix, Warnings and Precautions], [plavix, Drug Interactions], [plavix, Warnings and Precautions], [plavix, Warnings and Precautions]
- search `Advil ibuprofen warnings bleeding gastrointestinal` → [advil, Warnings], [advil, Ask a Doctor Before Use], [advil, Stop Use and Ask a Doctor], [advil, Warnings], [advil, Ask a Doctor or Pharmacist Before Use]

<details><summary>Retrieved passages</summary>

**search:** `Plavix Advil interaction bleeding warning`

```text
[plavix, Patient Counseling Information] Plavix (clopidogrel)
Plavix (clopidogrel), Patient Counseling Information: 17 PATIENT COUNSELING INFORMATION Advise patients to read FDA approved patient labeling (Medication Guide). Discontinuation Advise patients not to discontinue Plavix without first discussing it with the healthcare provider who prescribed it [see Warnings and Precautions (5.3) ] . Bleeding Advise patients that they: will bruise and bleed more easily will take longer than usual to stop bleeding must report any unanticipated, prolonged, or excessive bleeding, or blood in their stool or urine [see Warnings and Precautions (5.2) ] Thrombotic Thrombocytopenic Purpura Instruct patients to get prompt medical attention if they experience symptoms of TTP that cannot otherwise be explained [see Warnings and Precautions (5.4) ] . Invasive Procedures Advise patients to inform physicians and dentists that they are taking Plavix before any surgery or dental procedure [see Warnings and Precautions (5.2 , 5.3) ] . Proton Pump Inhibitors Advise patients not to take omeprazole or esomeprazole while taking Plavix.

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: Risk factors for bleeding include concomitant use of other drugs that increase the risk of bleeding (e.g., anticoagulants, antiplatelet agents, and chronic use of NSAIDs) [see Drug Interactions (7.4 , 7.5 , 7.6 , 7.7) ]. 5.3 Discontinuation of Plavix Discontinuation of Plavix increases the risk of cardiovascular events. If Plavix must be temporarily discontinued (e.g., to treat bleeding or for surgery with a major risk of bleeding), restart it as soon as possible. When possible, interrupt therapy with Plavix for five days prior to such surgery. Resume Plavix as soon as hemostasis is achieved. 5.4 Thrombotic Thrombocytopenic Purpura (TTP) TTP, sometimes fatal, has been reported following use of Plavix, sometimes after a short exposure (<2 weeks). TTP is a serious condition that requires urgent treatment including plasmapheresis (plasma exchange).

[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: 7.3 Opioids As with other oral P2Y 12 inhibitors, coadministration of opioid agonists delay and reduce the absorption of clopidogrel, presumably because of slowed gastric emptying, resulting in reduced exposure to its metabolites [see Clinical Pharmacology (12.3) ] . Consider the use of a parenteral antiplatelet agent in acute coronary syndrome patients requiring coadministration of morphine or other opioid agonists. 7.4 Nonsteroidal Anti-inflammatory Drugs (NSAIDs) Coadministration of Plavix and NSAIDs increases the risk of gastrointestinal bleeding. 7.5 Warfarin (CYP2C9 Substrates) Although the administration of clopidogrel 75 mg per day did not modify the pharmacokinetics of S-warfarin (a CYP2C9 substrate) or INR in patients receiving long-term warfarin therapy, coadministration of Plavix with warfarin increases the risk of bleeding because of independent effects on hemostasis. However, at high concentrations in vitro , clopidogrel inhibits CYP2C9.

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: 5 WARNINGS AND PRECAUTIONS CYP2C19 inhibitors: Avoid concomitant use of omeprazole or esomeprazole. ( 5.1 ) Bleeding: Plavix increases risk of bleeding. ( 5.2 ) Discontinuation: Premature discontinuation increases risk of cardiovascular events. Discontinue 5 days prior to elective surgery that has a major risk of bleeding. ( 5.3 ) Thrombotic thrombocytopenic purpura (TTP) has been reported. ( 5.4 ) Cross-reactivity among thienopyridines has been reported. ( 5.5 ) 5.1 Diminished Antiplatelet Activity in Patients with Impaired CYP2C19 Function Clopidogrel is a prodrug. Inhibition of platelet aggregation by clopidogrel is achieved through an active metabolite. The metabolism of clopidogrel to its active metabolite can be impaired by genetic variations in CYP2C19 [see Boxed Warning ] . The metabolism of clopidogrel can also be impaired by drugs that inhibit CYP2C19, such as omeprazole or esomeprazole.

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: Avoid concomitant use of Plavix with omeprazole or esomeprazole because both significantly reduce the antiplatelet activity of Plavix [see Drug Interactions (7.1) ] . 5.2 General Risk of Bleeding P2Y12 inhibitors (thienopyridines), including Plavix, increase the risk of bleeding. P2Y12 inhibitors (thienopyridines), inhibit platelet aggregation for the lifetime of the platelet (7-10 days). Because the half-life of clopidogrel's active metabolite is short, it may be possible to restore hemostasis by administering exogenous platelets; however, platelet transfusions within 4 hours of the loading dose or 2 hours of the maintenance dose may be less effective. Use of drugs that induce the activity of CYP2C19 would be expected to result in increased drug levels of the active metabolite of clopidogrel and might potentiate the bleeding risk. As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Drug Interactions (7.1) and Clinical Pharmacology (12.3) ] .
```

**search:** `Advil ibuprofen warnings bleeding gastrointestinal`

```text
[advil, Warnings] Advil (ibuprofen)
Advil (ibuprofen), Warnings: Warnings Allergy alert: Ibuprofen may cause a severe allergic reaction, especially in people allergic to aspirin. Symptoms may include: hives facial swelling asthma (wheezing) shock skin reddening rash blisters If an allergic reaction occurs, stop use and seek medical help right away. Stomach bleeding warning: This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs [aspirin, ibuprofen, naproxen, or others] have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning: NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal.

[advil, Ask a Doctor Before Use] Advil (ibuprofen)
Advil (ibuprofen), Ask a Doctor Before Use: Ask a doctor before use if stomach bleeding warning applies to you you have problems or serious side effects from taking pain relievers or fever reducers you have a history of stomach problems, such as heartburn you have high blood pressure, heart disease, liver cirrhosis, kidney disease, asthma, or had a stroke you are taking a diuretic

[advil, Stop Use and Ask a Doctor] Advil (ibuprofen)
Advil (ibuprofen), Stop Use and Ask a Doctor: Stop use and ask a doctor if you experience any of the following signs of stomach bleeding: feel faint vomit blood have bloody or black stools have stomach pain that does not get better you have symptoms of heart problems or stroke: chest pain trouble breathing weakness in one part or side of body slurred speech leg swelling pain gets worse or lasts more than 10 days fever gets worse or lasts more than 3 days redness or swelling is present in the painful area any new symptoms appear

[advil, Warnings] Advil (ibuprofen)
Advil (ibuprofen), Warnings: The risk is higher if you use more than directed or for longer than directed.

[advil, Ask a Doctor or Pharmacist Before Use] Advil (ibuprofen)
Advil (ibuprofen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are under a doctor's care for any serious condition taking aspirin for heart attack or stroke, because ibuprofen may decrease this benefit of aspirin taking any other drug
```

</details>

## q40 (unanswerable)

**Question:** What is the usual Eliquis dose for atrial fibrillation?

**Reference:** The available labels don't cover Eliquis (apixaban). Don't guess a dose; check the full Eliquis prescribing information or ask the supervising pharmacist.

**Agent answer:**

The current FDA drug label corpus does not contain the information for Eliquis (apixaban). Therefore, I cannot provide the usual dose for atrial fibrillation from the available labels. Please consult your supervising pharmacist or refer to the official Eliquis prescribing information.

*gemini-3.5-flash-lite, 1 search(es), 2612 tokens, 11.08 s*

- search `Eliquis atrial fibrillation dose` → [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration], [jantoven, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Eliquis atrial fibrillation dose`

```text
[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: For a patient receiving long-term anticoagulant treatment, periodically reassess the risk-benefit ratio of continuing such treatment in the individual patient. Atrial Fibrillation In patients with non-valvular AF, anticoagulate with warfarin to target INR of 2.5 (range, 2.0 to 3.0). In patients with non-valvular AF that is persistent or paroxysmal and at high risk of stroke (i.e., having any of the following features: prior ischemic stroke, transient ischemic attack, or systemic embolism, or 2 of the following risk factors: age greater than 75 years, moderately or severely impaired left ventricular systolic function and/or heart failure, history of hypertension, or diabetes mellitus), long-term anticoagulation with warfarin is recommended.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: In patients with non-valvular AF that is persistent or paroxysmal and at an intermediate risk of ischemic stroke (i.e., having 1 of the following risk factors: age greater than 75 years, moderately or severely impaired left ventricular systolic function and/or heart failure, history of hypertension, or diabetes mellitus), long-term anticoagulation with warfarin is recommended. For patients with AF and mitral stenosis, long-term anticoagulation with warfarin is recommended. For patients with AF and prosthetic heart valves, long-term anticoagulation with warfarin is recommended; the target INR may be increased and aspirin added depending on valve type and position, and on patient factors. Mechanical and Bioprosthetic Heart Valves For patients with a bileaflet mechanical valve or a Medtronic Hall (Minneapolis, MN) tilting disk valve in the aortic position who are in sinus rhythm and without left atrial enlargement, therapy with warfarin to a target INR of 2.5 (range, 2.0 to 3.0) is recommended.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: Post-Myocardial Infarction For high-risk patients with MI (e.g., those with a large anterior MI, those with significant heart failure, those with intracardiac thrombus visible on transthoracic echocardiography, those with AF, and those with a history of a thromboembolic event), therapy with combined moderate-intensity (INR, 2.0 to 3.0) warfarin plus low-dose aspirin (≤100 mg/day) for at least 3 months after the MI is recommended. Recurrent Systemic Embolism and Other Indications Oral anticoagulation therapy with warfarin has not been fully evaluated by clinical trials in patients with valvular disease associated with AF, patients with mitral stenosis, and patients with recurrent systemic embolism of unknown etiology. However, a moderate dose regimen (INR 2.0 to 3.0) may be used for these patients. 2.3 Initial and Maintenance Dosing The appropriate initial dosing of JANTOVEN varies widely for different patients.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: 2.2 Recommended Target INR Ranges and Durations for Individual Indications An INR of greater than 4.0 appears to provide no additional therapeutic benefit in most patients and is associated with a higher risk of bleeding. Venous Thromboembolism (including deep venous thrombosis [DVT] and PE) Adjust the warfarin dose to maintain a target INR of 2.5 (INR range, 2.0 to 3.0) for all treatment durations. The duration of treatment is based on the indication as follows: For patients with a DVT or PE secondary to a transient (reversible) risk factor, treatment with warfarin for 3 months is recommended. For patients with an unprovoked DVT or PE, treatment with warfarin is recommended for at least 3 months. After 3 months of therapy, evaluate the risk-benefit ratio of long-term treatment for the individual patient. For patients with two episodes of unprovoked DVT or PE, long-term treatment with warfarin is recommended.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: Table 1: Three Ranges of Expected Maintenance JANTOVEN Daily Doses Based on CYP2C9 and VKORC1 Genotypes Ranges are derived from multiple published clinical studies. VKORC1-1639G>A (rs9923231) variant is used in this table. Other co-inherited VKORC1 variants may also be important determinants of warfarin dose. VKORC1 CYP2C9 *1/*1 *1/*2 *1/*3 *2/*2 *2/*3 *3/*3 GG 5-7 mg 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg AG 5-7 mg 3-4 mg 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg AA 3-4 mg 3-4 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 0.5-2 mg 2.4 Monitoring to Achieve Optimal Anticoagulation JANTOVEN has a narrow therapeutic range (index), and its action may be affected by factors such as other drugs and dietary vitamin K. Therefore, anticoagulation must be carefully monitored during JANTOVEN therapy. Determine the INR daily after the administration of the initial dose until INR results stabilize in the therapeutic range.
```

</details>

## q41 (unanswerable)

**Question:** What should a customer do if they miss an Eliquis dose?

**Reference:** The available labels don't include missed-dose instructions for Eliquis. Refer to the Eliquis label or the supervising pharmacist.

**Agent answer:**

The available FDA drug labels in our database do not contain information regarding Eliquis (apixaban) or instructions for a missed dose of Eliquis. 

Please consult the supervising pharmacist for guidance, as the search results only provide information for other medications (such as Jantoven, Prilosec, and Cipro).

*gemini-3.5-flash-lite, 1 search(es), 2328 tokens, 11.64 s*

- search `Eliquis missed dose` → [jantoven, Dosage and Administration], [jantoven, Patient Counseling Information], [prilosec, Patient Counseling Information], [cipro, Patient Counseling Information], [jantoven, Dosage and Administration]

<details><summary>Retrieved passages</summary>

**search:** `Eliquis missed dose`

```text
[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: If a patient misses a dose of JANTOVEN at the intended time of day, the patient should take the dose as soon as possible on the same day. The patient should not double the dose the next day to make up for a missed dose. 2.7 Treatment during Dentistry and Surgery Some dental or surgical procedures may necessitate the interruption or change in the dose of JANTOVEN therapy. Consider the benefits and risks when discontinuing JANTOVEN even for a short period of time. Determine the INR immediately prior to any dental or surgical procedure. In patients undergoing minimally invasive procedures who must be anticoagulated prior to, during, or immediately following these procedures, adjusting the dosage of JANTOVEN to maintain the INR at the low end of the therapeutic range may safely allow for continued anticoagulation.

[jantoven, Patient Counseling Information] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Patient Counseling Information: 17 PATIENT COUNSELING INFORMATION Advise the patient to read the FDA-approved patient labeling (Medication Guide). Instructions for Patients Advise patients to: Strictly adhere to the prescribed dosage schedule [see Dosage and Administration (2.1) ]. If the prescribed dose of JANTOVEN is missed, take the dose as soon as possible on the same day but do not take a double dose of JANTOVEN the next day to make up for missed doses [see Dosage and Administration (2.6) ]. Obtain prothrombin time tests and make regular visits to their physician or clinic to monitor therapy [see Dosage and Administration (2.1) ]. Be aware that if therapy with JANTOVEN is discontinued, the anticoagulant effects of JANTOVEN may persist for about 2 to 5 days [see Clinical Pharmacology (12.2) ]. Avoid any activity or sport that may result in traumatic injury [see Use in Specific Populations (8.4) ].

[prilosec, Patient Counseling Information] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Patient Counseling Information: However, if the next scheduled dose is due, do not take the missed dose, and take the next dose on time. Do not take two doses at one time to make up for a missed dose.

[cipro, Patient Counseling Information] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Patient Counseling Information: If less than 6 hours remain before the next dose, the missed dose should not be taken and treatment should be continued as prescribed with the next scheduled dose. Double doses should not be taken to compensate for a missed dose. Advise patients that CIPRO Tablets (250 mg and 500 mg) are scored and can be split into one-half at the scored line to provide a 125 mg or 250 mg strength, respectively. Drug Interactions Oral Antidiabetic Agents Inform patients that hypoglycemia has been reported when ciprofloxacin and oral antidiabetic agents were co-administered; if low blood sugar occurs with CIPRO, instruct them to consult their physician and that their antibacterial medicine may need to be changed. Anthrax and Plague Studies Inform patients given CIPRO for these conditions that efficacy studies could not be conducted in humans for feasibility reasons.

[jantoven, Dosage and Administration] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Dosage and Administration: After stabilization, maintain dosing within the therapeutic range by performing periodic INRs. The frequency of performing INR should be based on the clinical situation but generally acceptable intervals for INR determinations are 1 to 4 weeks. Perform additional INR tests when other warfarin products are interchanged with JANTOVEN, as well as whenever other medications are initiated, discontinued, or taken irregularly. Heparin, a common concomitant drug, increases the INR [see Dosage and Administration (2.8) and Drug Interactions (7) ]. Determinations of whole blood clotting and bleeding times are not effective measures for monitoring of JANTOVEN therapy. 2.5 Renal Impairment No dosage adjustment is necessary for patients with renal failure. Monitor INR more frequently in patients with compromised renal function to maintain INR within the therapeutic range [see Warnings and Precautions (5.4) and Use in Specific Populations (8.6) ]. 2.6 Missed Dose The anticoagulant effect of JANTOVEN persists beyond 24 hours.
```

</details>

## q42 (unanswerable)

**Question:** Can a customer drink alcohol while taking Cipro?

**Reference:** The Cipro label in the corpus doesn't address alcohol. Say this isn't covered and refer to the pharmacist; don't infer an answer.

**Agent answer:**

The provided Cipro (ciprofloxacin hydrochloride) label search results do not contain information regarding drinking alcohol while taking the medication. 

Please consult the supervising pharmacist or check alternative clinical resources to answer this question.

*gemini-3.5-flash-lite, 1 search(es), 2780 tokens, 1.74 s*

- search `Cipro alcohol` → [cipro, Description], [cipro, Drug Interactions], [cipro, Dosage and Administration], [cipro, How Supplied], [cipro, How Supplied]

<details><summary>Retrieved passages</summary>

**search:** `Cipro alcohol`

```text
[cipro, Description] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Description: Each CIPRO film-coated tablet contains 250 mg (equivalent to 291 mg ciprofloxacin hydrochloride monohydrate) or 500 mg of ciprofloxacin (equivalent to 582 mg ciprofloxacin hydrochloride monohydrate) CIPRO tablets are white to slightly yellowish. The inactive ingredients are cornstarch, crospovidone, hypromellose, magnesium stearate, microcrystalline cellulose, polyethylene glycol, silicon dioxide, and titanium dioxide. CIPRO Oral Suspension is available in 5% (5 g ciprofloxacin in 100 mL) and 10% (10 g ciprofloxacin in 100 mL) strengths. CIPRO Oral Suspension is a white to slightly yellowish suspension with strawberry flavor which may contain yellow-orange droplets. It is composed of ciprofloxacin microcapsules and diluent which are mixed prior to dispensing [see Dosage and Administration ( 2.5 )] . The components of the suspension have the following compositions: - Microcapsules-ciprofloxacin, hypromellose, magnesium stearate, methacrylic acid copolymer, Polysorbate 20 and povidone. - Diluent-medium-chain triglycerides, sucrose, soy-lecithin, water, and strawberry flavor.

[cipro, Drug Interactions] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Drug Interactions: 7 DRUG INTERACTIONS Ciprofloxacin is an inhibitor of human cytochrome P450 1A2 (CYP1A2) mediated metabolism. Co-administration of CIPRO with other drugs primarily metabolized by CYP1A2 results in increased plasma concentrations of these drugs and could lead to clinically significant adverse events of the co-administered drug. Table 11: Drugs That are Affected by and Affecting CIPRO Drugs That are Affected by CIPRO Drug(s) Recommendation Comments Tizanidine Contraindicated Concomitant administration of tizanidine and CIPRO is contraindicated due to the potentiation of hypotensive and sedative effects of tizanidine [ see Contraindications ( 4.2 ) ] Theophylline Avoid Use (Plasma Exposure Likely to be Increased and Prolonged) Concurrent administration of CIPRO with theophylline may result in increased risk of a patient developing central nervous system (CNS) or other adverse reactions. If concomitant use cannot be avoided, monitor serum levels of theophylline and adjust dosage as appropriate [see Warnings and Precautions ( 5.10 )].

[cipro, Dosage and Administration] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), Dosage and Administration: CIPRO oral suspension is composed of two components (microcapsules and diluent) that must be combined prior to dispensing. Table 5: Appropriate Dosing Volumes of the Reconstituted Oral Suspensions Dose 5% (250 mg/5 mL) 10% (500 mg/5 mL) 250 mg 5 mL 2.5 mL 500 mg 10 mL 5 mL 750 mg 15 mL 7.5 mL Preparation of the suspension: Step1 The small bottle contains the microcapsules, the large bottle contains the diluent. Step 2 Open both bottles. Child-proof cap: Press down according to instructions on the cap while turning to the left. Step 3 Pour the microcapsules completely into the larger bottle of diluent. Do not add water to the suspension. Step 4 Remove the top layer of the diluent bottle label (to reveal the CIPRO Oral Suspension label). Close the large bottle completely according to the directions on the cap and shake vigorously for about 15 seconds.

[cipro, How Supplied] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), How Supplied: The drug product is composed of two components (microcapsules containing the active ingredient and diluent) which must be mixed by the pharmacist [see Dosage and Administration ( 2.5 )]. Strengths Total volume after reconstitution Ciprofloxacin Concentration Ciprofloxacin contents per bottle NDC Code 5% 100 mL 250 mg/5 mL 5,000 mg 50419-777-01 10% 100 mL 500 mg/5 mL 10,000 mg 50419-773-01 Store microcapsules and diluent below 25°C (77°F); excursions are permitted from 15°C to 30°C (59°F to 86°F) [see USP Controlled Room Temperature]. Protect from freezing. The reconstituted product may be stored at 25°C (77°F) for 14 days; excursions are permitted from 15°C to 30°C (59°F to 86°F) [see USP Controlled Room Temperature]. Protect from freezing. A graduated teaspoon (5mL) with markings 1/2 (2.5 mL) and 1/1 (5 mL) is provided for the patient.

[cipro, How Supplied] Cipro (ciprofloxacin hydrochloride)
Cipro (ciprofloxacin hydrochloride), How Supplied: 16 HOW SUPPLIED/STORAGE AND HANDLING CIPRO (ciprofloxacin hydrochloride) Tablets are available as round, slightly yellowish film-coated tablets containing 250 mg ciprofloxacin. The 250 mg tablet is coded with the word "BAYER" on one side and functionally scored and engraved with "CIP 250" on the reverse side. CIPRO is also available as capsule shaped, slightly yellowish film-coated tablets containing 500 mg ciprofloxacin. The 500 mg tablet is coded with the word "BAYER" on one side and functionally scored and engraved with "CIP 500" on the reverse side. CIPRO 250 mg and 500 mg are available in bottles of 100. Strength NDC Code Tablet Identification Bottles of 100: 250 mg NDC 50419-758-01 CIPRO 250 500 mg NDC 50419-754-01 CIPRO 500 Store at 20° to 25°C (68° to 77°F); excursions permitted to 15° to 30°C (59° to 86°F) [see USP Controlled Room Temperature]. CIPRO Oral Suspension is supplied in 5% and 10% strengths.
```

</details>

## q43 (unanswerable)

**Question:** Can a patient on Plavix drink grapefruit juice?

**Reference:** The Plavix label in the corpus doesn't mention grapefruit. Say it isn't covered and refer to the pharmacist.

**Agent answer:**

The provided Plavix (clopidogrel) drug label does not contain information regarding the consumption of grapefruit juice or its interaction with Plavix. 

Please consult the supervising pharmacist for further guidance.

*gemini-3.5-flash-lite, 1 search(es), 2752 tokens, 2.45 s*

- search `Plavix grapefruit juice` → [plavix, Drug Interactions], [plavix, Patient Counseling Information], [plavix, Warnings and Precautions], [plavix, Warnings and Precautions], [plavix, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `Plavix grapefruit juice`

```text
[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] . 7.2 CYP2C19 Inhibitors Clopidogrel is metabolized to its active metabolite in part by CYP2C19. Concomitant use of drugs that inhibit the activity of this enzyme results in reduced plasma concentrations of the active metabolite of clopidogrel and a reduction in platelet inhibition [see Warnings and Precautions (5.1) ] . Omeprazole or Esomeprazole Avoid concomitant use of Plavix with omeprazole or esomeprazole. In clinical studies, omeprazole was shown to reduce significantly the antiplatelet activity of Plavix when given concomitantly or 12 hours apart. A similar reduction in antiplatelet activity was observed with esomeprazole when given concomitantly with Plavix. Dexlansoprazole, lansoprazole, and pantoprazole had less effect on the antiplatelet activity of Plavix than did omeprazole or esomeprazole [see Warnings and Precautions (5.1) and Clinical Pharmacology (12.3) ] .

[plavix, Patient Counseling Information] Plavix (clopidogrel)
Plavix (clopidogrel), Patient Counseling Information: 17 PATIENT COUNSELING INFORMATION Advise patients to read FDA approved patient labeling (Medication Guide). Discontinuation Advise patients not to discontinue Plavix without first discussing it with the healthcare provider who prescribed it [see Warnings and Precautions (5.3) ] . Bleeding Advise patients that they: will bruise and bleed more easily will take longer than usual to stop bleeding must report any unanticipated, prolonged, or excessive bleeding, or blood in their stool or urine [see Warnings and Precautions (5.2) ] Thrombotic Thrombocytopenic Purpura Instruct patients to get prompt medical attention if they experience symptoms of TTP that cannot otherwise be explained [see Warnings and Precautions (5.4) ] . Invasive Procedures Advise patients to inform physicians and dentists that they are taking Plavix before any surgery or dental procedure [see Warnings and Precautions (5.2 , 5.3) ] . Proton Pump Inhibitors Advise patients not to take omeprazole or esomeprazole while taking Plavix.

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: Avoid concomitant use of Plavix with omeprazole or esomeprazole because both significantly reduce the antiplatelet activity of Plavix [see Drug Interactions (7.1) ] . 5.2 General Risk of Bleeding P2Y12 inhibitors (thienopyridines), including Plavix, increase the risk of bleeding. P2Y12 inhibitors (thienopyridines), inhibit platelet aggregation for the lifetime of the platelet (7-10 days). Because the half-life of clopidogrel's active metabolite is short, it may be possible to restore hemostasis by administering exogenous platelets; however, platelet transfusions within 4 hours of the loading dose or 2 hours of the maintenance dose may be less effective. Use of drugs that induce the activity of CYP2C19 would be expected to result in increased drug levels of the active metabolite of clopidogrel and might potentiate the bleeding risk. As a precaution, avoid concomitant use of strong CYP2C19 inducers [see Drug Interactions (7.1) and Clinical Pharmacology (12.3) ] .

[plavix, Warnings and Precautions] Plavix (clopidogrel)
Plavix (clopidogrel), Warnings and Precautions: 5 WARNINGS AND PRECAUTIONS CYP2C19 inhibitors: Avoid concomitant use of omeprazole or esomeprazole. ( 5.1 ) Bleeding: Plavix increases risk of bleeding. ( 5.2 ) Discontinuation: Premature discontinuation increases risk of cardiovascular events. Discontinue 5 days prior to elective surgery that has a major risk of bleeding. ( 5.3 ) Thrombotic thrombocytopenic purpura (TTP) has been reported. ( 5.4 ) Cross-reactivity among thienopyridines has been reported. ( 5.5 ) 5.1 Diminished Antiplatelet Activity in Patients with Impaired CYP2C19 Function Clopidogrel is a prodrug. Inhibition of platelet aggregation by clopidogrel is achieved through an active metabolite. The metabolism of clopidogrel to its active metabolite can be impaired by genetic variations in CYP2C19 [see Boxed Warning ] . The metabolism of clopidogrel can also be impaired by drugs that inhibit CYP2C19, such as omeprazole or esomeprazole.

[plavix, Drug Interactions] Plavix (clopidogrel)
Plavix (clopidogrel), Drug Interactions: 7 DRUG INTERACTIONS CYP2C19 inducers: Increases levels of clopidogrel active metabolite and increases platelet inhibition. ( 7.1 ) Opioids: Decreased exposure to clopidogrel. Consider use of parenteral antiplatelet agent. ( 7.3 ) Nonsteroidal anti-inflammatory drugs (NSAIDs), warfarin, selective serotonin and serotonin norepinephrine reuptake inhibitors (SSRIs, SNRIs): Increases risk of bleeding. ( 7.4 , 7.5 , 7.6 ) Other Antiplatelet Agents: Increases the risk of bleeding due to an additive effect. ( 7.7 ) Repaglinide (CYP2C8 substrates): Increases substrate plasma concentrations. ( 7.8 ) 7.1 CYP2C19 Inducers Since clopidogrel is metabolized to its active metabolite partly by CYP2C19, use of drugs that induce the activity of this enzyme would be expected to result in increased drug levels of the active metabolite of clopidogrel. Rifampin strongly induces CYP2C19 resulting to both an increase level of clopidogrel active metabolite and platelet inhibition, which in particular might potentiate the risk of bleeding.
```

</details>

## q44 (unanswerable)

**Question:** Is it safe to alternate Advil and Tylenol for a fever?

**Reference:** Neither the Advil nor the Tylenol label addresses taking or alternating them together. Give each product's own dosing limits only and refer to the pharmacist or doctor about combining them.

**Agent answer:**

The provided product labels for Advil (ibuprofen) and Tylenol (acetaminophen) do not contain specific information or instructions regarding alternating between the two medications for a fever [advil, Dosage and Administration], [tylenol, Indications and Usage]. 

Because the provided label texts do not cover this practice, please consult your supervising pharmacist for guidance.

*gemini-3.5-flash-lite, 2 search(es), 3449 tokens, 2.87 s*

- search `Advil fever alternate Tylenol` → [advil, Indications and Usage], [advil, Active Ingredient], [advil, Warnings], [advil, Ask a Doctor or Pharmacist Before Use], [advil, Dosage and Administration]
- search `Tylenol fever alternate Advil ibuprofen acetaminophen` → [tylenol, Indications and Usage], [advil, Indications and Usage], [tylenol, Active Ingredient], [advil, Active Ingredient], [tylenol, Ask a Doctor or Pharmacist Before Use]

<details><summary>Retrieved passages</summary>

**search:** `Advil fever alternate Tylenol`

```text
[advil, Indications and Usage] Advil (ibuprofen)
Advil (ibuprofen), Indications and Usage: Uses temporarily relieves minor aches and pains due to: headache toothache backache menstrual cramps the common cold muscular aches minor pain of arthritis temporarily reduces fever

[advil, Active Ingredient] Advil (ibuprofen)
Advil (ibuprofen), Active Ingredient: Active ingredient (in each capsule) Solubilized ibuprofen equal to 200 mg ibuprofen (NSAID)* (present as the free acid and potassium salt) *nonsteroidal anti-inflammatory drug

[advil, Warnings] Advil (ibuprofen)
Advil (ibuprofen), Warnings: Warnings Allergy alert: Ibuprofen may cause a severe allergic reaction, especially in people allergic to aspirin. Symptoms may include: hives facial swelling asthma (wheezing) shock skin reddening rash blisters If an allergic reaction occurs, stop use and seek medical help right away. Stomach bleeding warning: This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs [aspirin, ibuprofen, naproxen, or others] have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning: NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal.

[advil, Ask a Doctor or Pharmacist Before Use] Advil (ibuprofen)
Advil (ibuprofen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are under a doctor's care for any serious condition taking aspirin for heart attack or stroke, because ibuprofen may decrease this benefit of aspirin taking any other drug

[advil, Dosage and Administration] Advil (ibuprofen)
Advil (ibuprofen), Dosage and Administration: Directions do not take more than directed the smallest effective dose should be used adults and children 12 years and over: take 1 capsule every 4 to 6 hours while symptoms persist if pain or fever does not respond to 1 capsule, 2 capsules may be used do not exceed 6 capsules in 24 hours, unless directed by a doctor children under 12 years: ask a doctor
```

**search:** `Tylenol fever alternate Advil ibuprofen acetaminophen`

```text
[tylenol, Indications and Usage] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Indications and Usage: Uses temporarily relieves minor aches and pains due to: - the common cold - headache - backache - minor pain of arthritis - toothache - muscular aches - premenstrual and menstrual cramps temporarily reduces fever

[advil, Indications and Usage] Advil (ibuprofen)
Advil (ibuprofen), Indications and Usage: Uses temporarily relieves minor aches and pains due to: headache toothache backache menstrual cramps the common cold muscular aches minor pain of arthritis temporarily reduces fever

[tylenol, Active Ingredient] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Active Ingredient: Active ingredient (in each caplet) Acetaminophen 500 mg

[advil, Active Ingredient] Advil (ibuprofen)
Advil (ibuprofen), Active Ingredient: Active ingredient (in each capsule) Solubilized ibuprofen equal to 200 mg ibuprofen (NSAID)* (present as the free acid and potassium salt) *nonsteroidal anti-inflammatory drug

[tylenol, Ask a Doctor or Pharmacist Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin
```

</details>

## q45 (unanswerable)

**Question:** Does Prilosec affect levothyroxine absorption?

**Reference:** The Prilosec label in the corpus doesn't list levothyroxine. Say it isn't covered and refer to the pharmacist or full drug-interaction resources.

**Agent answer:**

The provided Prilosec (omeprazole) drug label does not contain information regarding an interaction with levothyroxine or its absorption. 

Please consult the supervising pharmacist or refer to the levothyroxine prescribing information for guidance on this potential interaction.

*gemini-3.5-flash-lite, 1 search(es), 2665 tokens, 2.22 s*

- search `Prilosec levothyroxine absorption` → [prilosec, Drug Interactions], [prilosec, Warnings and Precautions], [prilosec, Drug Interactions], [prilosec, Dosage and Administration], [prilosec, Drug Interactions]

<details><summary>Retrieved passages</summary>

**search:** `Prilosec levothyroxine absorption`

```text
[prilosec, Drug Interactions] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Drug Interactions: Digoxin Clinical Impact: Potential for increased exposure of digoxin [see Clinical Pharmacology ( 12.3 )] . Intervention: Monitor digoxin concentrations. Dose adjustment may be needed to maintain therapeutic drug concentrations. See digoxin prescribing information. Drugs Dependent on Gastric pH for Absorption (e.g., iron salts, erlotinib, dasatinib, nilotinib, mycophenolate mofetil, ketoconazole/itraconazole) Clinical Impact: Omeprazole can reduce the absorption of other drugs due to its effect on reducing intragastric acidity. Intervention: Mycophenolate mofetil (MMF): Co-administration of omeprazole in healthy subjects and in transplant patients receiving MMF has been reported to reduce the exposure to the active metabolite, mycophenolic acid (MPA), possibly due to a decrease in MMF solubility at an increased gastric pH. The clinical relevance of reduced MPA exposure on organ rejection has not been established in transplant patients receiving PRILOSEC and MMF. Use PRILOSEC with caution in transplant patients receiving MMF [see Clinical Pharmacology ( 12.3 )] .

[prilosec, Warnings and Precautions] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Warnings and Precautions: The metabolism of clopidogrel to its active metabolite can be impaired by use with concomitant medications, such as omeprazole, that inhibit CYP2C19 activity. Concomitant use of clopidogrel with 80 mg omeprazole reduces the pharmacological activity of clopidogrel, even when administered 12 hours apart. When using PRILOSEC, consider alternative anti-platelet therapy [see Drug Interactions ( 7 ) and Clinical Pharmacology ( 12.3 )] . 5.8 Cyanocobalamin (Vitamin B-12) Deficiency Daily treatment with any acid-suppressing medications over a long period of time (e.g., longer than 3 years) may lead to malabsorption of cyanocobalamin (vitamin B-12) caused by hypo- or achlorhydria. Rare reports of cyanocobalamin deficiency occurring with acid-suppressing therapy have been reported in the literature. This diagnosis should be considered if clinical symptoms consistent with cyanocobalamin deficiency are observed in patients treated with PRILOSEC.

[prilosec, Drug Interactions] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Drug Interactions: See the prescribing information for other drugs dependent on gastric pH for absorption. Combination Therapy with Clarithromycin and Amoxicillin Clinical Impact: Concomitant administration of clarithromycin with other drugs can lead to serious adverse reactions, including potentially fatal arrhythmias, and are contraindicated. Amoxicillin also has drug interactions. Intervention: See Contraindications , Warnings and Precautions in prescribing information for clarithromycin. See Drug Interactions in prescribing information for amoxicillin. Tacrolimus Clinical Impact: Potential for increased exposure of tacrolimus, especially in transplant patients who are intermediate or poor metabolizers of CYP2C19. Intervention: Monitor tacrolimus whole blood concentrations. Dose adjustment may be needed to maintain therapeutic drug concentrations. See prescribing information for tacrolimus. Interactions with Investigations of Neuroendocrine Tumors Clinical Impact: Serum chromogranin A (CgA) levels increase secondary to PPI-induced decreases in gastric acidity.

[prilosec, Dosage and Administration] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Dosage and Administration: pylori Eradication to Reduce the Risk of Duodenal Ulcer Recurrence Triple Therapy: PRILOSEC Amoxicillin Clarithromycin 20 mg 1000 mg 500 mg Each drug twice daily for 10 days ( 2.1 )* Dual Therapy: PRILOSEC Clarithromycin 40 mg once daily for 14 days** 500 mg three times daily for 14 days ( 2.1 ) Active Benign Gastric Ulcer 40 mg once daily for 4 to 8 weeks ( 2.1 ) Symptomatic GERD 20 mg once daily for up to 4 weeks ( 2.1 ) See full prescribing information for weight based dosing in pediatric patients 1 year of age and older ( 2.2 ) EE due to Acid-Mediated GERD 20 mg once daily for 4 to 8 weeks ( 2.1 )*** See full prescribing information for weight based dosing in pediatric patients 1 month of age and older ( 2.2 ) Maintenance of Healing of EE due to Acid-Mediated GERD 20

[prilosec, Drug Interactions] Prilosec (omeprazole magnesium)
Prilosec (omeprazole magnesium), Drug Interactions: Methotrexate Clinical Impact: Concomitant use of omeprazole with methotrexate (primarily at high dose) may elevate and prolong serum concentrations of methotrexate and/or its metabolite hydroxymethotrexate, possibly leading to methotrexate toxicities. No formal drug interaction studies of high-dose methotrexate with PPIs have been conducted [see Warnings and Precautions ( 5.11 )]. Intervention: A temporary withdrawal of PRILOSEC may be considered in some patients receiving high-dose methotrexate. CYP2C19 Substrates (e.g., clopidogrel, citalopram, cilostazol, phenytoin, diazepam) Clopidogrel Clinical Impact: Concomitant use of omeprazole 80 mg results in reduced plasma concentrations of the active metabolite of clopidogrel and a reduction in platelet inhibition [see Clinical Pharmacology ( 12.3 )]. There are no adequate combination studies of a lower dose of omeprazole or a higher dose of clopidogrel in comparison with the approved dose of clopidogrel. Intervention: Avoid concomitant use with PRILOSEC.
```

</details>

## q46 (unanswerable)

**Question:** Can Aleve be taken together with sumatriptan for a migraine?

**Reference:** The corpus has no sumatriptan label and the Aleve label doesn't mention it. Say it isn't covered and refer to the pharmacist or prescriber.

**Agent answer:**

The provided drug labels for Aleve (naproxen sodium) and prescription naproxen do not contain information regarding the concurrent use of sumatriptan. 

Because the labels do not cover this question, please consult your supervising pharmacist before advising a patient on taking Aleve and sumatriptan together.

*gemini-3.5-flash-lite, 2 search(es), 4227 tokens, 3.42 s*

- search `Aleve sumatriptan` → [aleve, Active Ingredient], [aleve, Warnings], [aleve, Indications and Usage], [aleve, Inactive Ingredients], [aleve, Ask a Doctor Before Use]
- search `naproxen sumatriptan` → [naproxen, Boxed Warning], [naproxen, Indications and Usage], [naproxen, Drug Interactions], [naproxen, Description], [naproxen, Warnings and Precautions]

<details><summary>Retrieved passages</summary>

**search:** `Aleve sumatriptan`

```text
[aleve, Active Ingredient] Aleve (naproxen sodium)
Aleve (naproxen sodium), Active Ingredient: Active ingredient (in each capsule) Naproxen sodium 220 mg (naproxen 200 mg) (NSAID) nonsteroidal anti-inflammatory drug

[aleve, Warnings] Aleve (naproxen sodium)
Aleve (naproxen sodium), Warnings: Stomach bleeding warning This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you: are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs (aspirin, ibuprofen, naproxen, or others) have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal. The risk is higher if you use more than directed or for longer than directed. Allergy alert Naproxen sodium may cause a severe allergic reaction, especially in people allergic to aspirin.

[aleve, Indications and Usage] Aleve (naproxen sodium)
Aleve (naproxen sodium), Indications and Usage: Uses temporarily relieves minor aches and pains due to: minor pain of arthritis muscular aches backache menstrual cramps headache toothache the common cold temporarily reduces fever

[aleve, Inactive Ingredients] Aleve (naproxen sodium)
Aleve (naproxen sodium), Inactive Ingredients: Inactive ingredients FD&C blue #1, gelatin, glycerin, lactic acid, mannitol, pharmaceutical ink, polyethylene glycol, povidone, propylene glycol, purified water, sorbitan, sorbitol

[aleve, Ask a Doctor Before Use] Aleve (naproxen sodium)
Aleve (naproxen sodium), Ask a Doctor Before Use: Ask a doctor before use if the stomach bleeding warning applies to you you have a history of stomach problems, such as heartburn you have high blood pressure, heart disease, liver cirrhosis, kidney disease, asthma, or had a stroke you are taking a diuretic you have problems or serious side effects from taking pain relievers or fever reducers
```

**search:** `naproxen sumatriptan`

```text
[naproxen, Boxed Warning] Naproxen (naproxen)
Naproxen (naproxen), Boxed Warning: WARNING: RISK OF SERIOUS CARDIOVASCULAR AND GASTROINTESTINAL EVENTS Cardiovascular Thrombotic Events - Nonsteroidal anti-inflammatory drugs (NSAIDs) cause an increased risk of serious cardiovascular thrombotic events, including myocardial infarction and stroke, which can be fatal. This risk may occur early in treatment and may increase with duration of use [ see Warnings and Precautions (5.1) ]. - Naproxen Tablets are contraindicated in the setting of coronary artery bypass graft (CABG) surgery [ see Contraindications(4) , Warnings and Precautions (5.1) ] . Gastrointestinal Bleeding, Ulceration, and Perforation - NSAIDs cause an increased risk of serious gastrointestinal (GI) adverse events including bleeding, ulceration, and perforation of the stomach or intestines, which can be fatal. These events can occur at any time during use and without warning symptoms.

[naproxen, Indications and Usage] Naproxen (naproxen)
Naproxen (naproxen), Indications and Usage: 1 INDICATIONS AND USAGE Naproxen tablets are indicated for: the relief of the signs and symptoms of: - rheumatoid arthritis - osteoarthritis - ankylosing spondylitis - Polyarticular Juvenile Idiopathic Arthritis Naproxen tablets are also indicated for: the relief of signs and symptoms of: - tendonitis - bursitis - acute gout the management of: - pain - primary dysmenorrhea Naproxen tablets are a non-steroidal anti-inflammatory drugs indicated for: the relief of the signs and symptoms of: - rheumatoid arthritis - osteoarthritis - ankylosing spondylitis - polyarticular juvenile idiopathic arthritis Naproxen Tablets are also indicated for: the relief of signs and symptoms of: - tendonitis - bursitis - acute gout the management of: - pain - primary dysmenorrhea

[naproxen, Drug Interactions] Naproxen (naproxen)
Naproxen (naproxen), Drug Interactions: 7 DRUG INTERACTIONS See Table 1 for clinically significant drug interactions with naproxen. Table 1: Clinically Significant Drug Interactions with naproxen Drugs That Interfere with Hemostasis Clinical Impact: Naproxen and anticoagulants such as warfarin have a synergistic effect on bleeding. The concomitant use of naproxen and anticoagulants have an increased risk of serious bleeding compared to the use of either drug alone. Serotonin release by platelets plays an important role in hemostasis. Case-control and cohort epidemiological studies showed that concomitant use of drugs that interfere with serotonin reuptake and an NSAID may potentiate the risk of bleeding more than an NSAID alone. Intervention: Monitor patients with concomitant use of naproxen tablets with anticoagulants (e.g., warfarin), antiplatelet agents (e.g., aspirin), selective serotonin reuptake inhibitors (SSRIs), and serotonin norepinephrine reuptake inhibitors (SNRIs) for signs of bleeding [ see Warnings and Precautions (5.12) ].

[naproxen, Description] Naproxen (naproxen)
Naproxen (naproxen), Description: 11 DESCRIPTION Naproxen tablets are nonsteroidal anti-inflammatory drugs available as follows: Naproxen tablets are available as white to off-white tablets containing 250 mg, 375 mg and 500 mg of naproxen for oral administration. Naproxen is a propionic acid derivative related to the arylacetic acid group of nonsteroidal anti-inflammatory drugs. The chemical names for naproxen and naproxen sodium are (S)-6-methoxy-a-methyl-2-naphthaleneacetic acid and (S)-6­ methoxy-a-methyl-2-naphthaleneacetic acid, sodium salt, respectively. Naproxen has a molecular weight of 230.26 and a molecular formula of C 14 H 14 O 3 . Naproxen sodium has a molecular weight of 252.23 and a molecular formula of C 14 H 13 NaO 3 . Naproxen and naproxen sodium have the following structures, respectively: Naproxen is an odorless, white to off-white crystalline substance. It is lipid-soluble, practically insoluble in water at low pH and freely soluble in water at high pH.

[naproxen, Warnings and Precautions] Naproxen (naproxen)
Naproxen (naproxen), Warnings and Precautions: ( 5.12 , 7 ) 5.1 Cardiovascular Thrombotic Events Clinical trials of several COX-2 selective and nonselective NSAIDs of up to three years duration have shown an increased risk of serious cardiovascular (CV) thrombotic events, including myocardial infarction (MI) and stroke, which can be fatal. Based on available data, it is unclear that the risk for CV thrombotic events is similar for all NSAIDs. The relative increase in serious CV thrombotic events over baseline conferred by NSAID use appears to be similar in those with and without known CV disease or risk factors for CV disease. However, patients with known CV disease or risk factors had a higher absolute incidence of excess serious CV thrombotic events, due to their increased baseline rate. Some observational studies found that this increased risk of serious CV thrombotic events began as early as the first weeks of treatment.
```

</details>
