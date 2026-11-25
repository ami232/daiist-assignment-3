# Grading sheet

Grade each answer **before** opening eval/results.csv or eval/verdicts.jsonl (they hold the judge's verdicts).
Write your grades in eval/human_labels.csv: `id,correct,supported,notes`.

- **correct** = 1 if the answer matches the reference (or, for an unanswerable question, it properly refuses).
- **supported** = 1 if every claim is in the retrieved passages shown below.
- **notes**: why, for every 0.


---

## q01 (single)

**Question:** What temperature do I have to keep hot food at on the line or while it waits for a delivery driver?

**Reference answer:** At 57°C (135°F) or above; roasts cooked as in 3-401.11(B) may be held at 54°C (130°F) or above.

**Expected source:** food_code_2026 3-501.16

**Agent's answer:**

Time/temperature control for safety food must be maintained at 57°C (135°F) or above, except for roasts cooked and held under specific conditions which may be held at 54°C (130°F) or above [Food Code 2026 §3-501.16].

**Passages the answer cites:**

> **[Food Code 2026 §3-501.16]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.16 (p. 72). Time/Temperature Control for Safety Food, Hot and Cold Holding
> (A) Except during preparation, cooking, or cooling, or when time is used as the public health control as specified under § 3-501.19, and except as specified under ¶ (B) and in ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be maintained: (1) At 57°C (135°F) or above, except roasts cooked to a temperature and for a time specified in ¶ 3-401.11(B) or reheated as specified in ¶ 3-403.11(E) may be held at a temperature of 54°C (130°F) or above; or (2) At 5°C (41°F) or less. (B) EGGS that have not been treated to destroy all viable Salmonellae shall be stored in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (C) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD in a homogenous liquid form may be maintained outside of the temperature control requirements, as specified under ¶ (A) of this section, while contained within specially designed EQUIPMENT that complies with the design and construction requirements as specified under ¶ 4-204.13(E). On-premises preparation Prepare and hold cold

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-401.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.13 (p. 66). Plant Food Cooking for Hot Holding
> Plant FOODS that are cooked for hot holding shall be cooked to a temperature of 57°C (135°F) or as specified under § 3-401.15.

> **[Food Code 2026 §3-202.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-202.11 (pp. 48-49). Temperature
> (A) Except as specified in ¶ (B) of this section, refrigerated, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be at a temperature of 5°C (41°F) or below when received. (B) If a temperature other than 5°C (41°F) for a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD is specified in LAW governing its distribution, such as LAWS governing milk and MOLLUSCAN SHELLFISH, the FOOD may be received at the specified temperature. (C) Raw EGGS shall be received in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (D) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked to a temperature and for a time specified under §§ 3-401.11 – 3-401.13 and received hot shall be at a temperature of 57°C (135°F) or above. (E) A FOOD that is labeled frozen and shipped frozen by a FOOD PROCESSING PLANT shall be received frozen. (F) Upon receipt, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be free of evidence of previous temperature abuse.

> **[Food Code 2026 §3-403.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-403.11 (pp. 68-69). Reheating for Hot Holding
> (A) Except as specified under ¶¶ (B) and (C) and in ¶ (E) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked, cooled, and reheated for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) for 15 seconds. (B) Except as specified under ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD reheated in a microwave oven for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) and the FOOD is rotated or stirred, covered, and allowed to stand covered for two minutes after reheating. (C) READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that has been commercially processed and PACKAGED in a FOOD PROCESSING PLANT that is inspected by the REGULATORY AUTHORITY that has jurisdiction over the plant, shall be heated to a temperature of at least 57°C (135°F) when being reheated for hot holding. (D) Reheating for hot holding as specified under ¶¶ (A) - (C) of this section shall be done rapidly and the time the FOOD is between 5°C (41°F) and the temperatures specified under ¶¶ (A) - (C) of this section may not exceed two hours. (E) Remaining unsliced portions of MEAT roasts that are cooked as specified under ¶ 3-401.11(B) may be reheated for hot holding using the oven parameters and minimum time and temperature conditions specified under ¶ 3-401.11(B).

> **[Food Code 2026 §4-204.111]** Source: FDA Food Code 2026, Chapters 1-6, §4-204.111 (pp. 94-95). Vending Machines, Automatic Shutoff
> (A) A machine vending TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall have an automatic control that prevents the machine from vending FOOD: (1) If there is a power failure, mechanical failure, or other condition that results in an internal machine temperature that cannot maintain FOOD temperatures as specified under Chapter 3; and (2) If a condition specified under Subparagraph (A)(1) of this section occurs, until the machine is serviced and restocked with FOOD that has been maintained at temperatures specified under Chapter 3. (B) When the automatic shutoff within a machine vending TIME/TEMPERATURE CONTROL FOR SAFETY FOOD is activated: (1) In a refrigerated VENDING MACHINE, the ambient air temperature may not exceed 5°C (41°F) for more than 30 minutes immediately after the machine is filled, serviced, or restocked; or (2) In a hot holding VENDING MACHINE, the ambient air temperature may not be less than 57°C (135°F) for more than 120 minutes immediately after the machine is filled, serviced, or restocked.

</details>


---

## q02 (single)

**Question:** What temperature should our walk-in fridge keep prepared food at?

**Reference answer:** At 5°C (41°F) or less.

**Expected source:** food_code_2026 3-501.16

**Agent's answer:**

Prepared time/temperature control for safety (TCS) food must be maintained at 5°C (41°F) or less [Food Code 2026 §3-501.16].

**Passages the answer cites:**

> **[Food Code 2026 §3-501.16]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.16 (p. 72). Time/Temperature Control for Safety Food, Hot and Cold Holding
> (A) Except during preparation, cooking, or cooling, or when time is used as the public health control as specified under § 3-501.19, and except as specified under ¶ (B) and in ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be maintained: (1) At 57°C (135°F) or above, except roasts cooked to a temperature and for a time specified in ¶ 3-401.11(B) or reheated as specified in ¶ 3-403.11(E) may be held at a temperature of 54°C (130°F) or above; or (2) At 5°C (41°F) or less. (B) EGGS that have not been treated to destroy all viable Salmonellae shall be stored in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (C) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD in a homogenous liquid form may be maintained outside of the temperature control requirements, as specified under ¶ (A) of this section, while contained within specially designed EQUIPMENT that complies with the design and construction requirements as specified under ¶ 4-204.13(E). On-premises preparation Prepare and hold cold

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-202.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-202.11 (pp. 48-49). Temperature
> (A) Except as specified in ¶ (B) of this section, refrigerated, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be at a temperature of 5°C (41°F) or below when received. (B) If a temperature other than 5°C (41°F) for a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD is specified in LAW governing its distribution, such as LAWS governing milk and MOLLUSCAN SHELLFISH, the FOOD may be received at the specified temperature. (C) Raw EGGS shall be received in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (D) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked to a temperature and for a time specified under §§ 3-401.11 – 3-401.13 and received hot shall be at a temperature of 57°C (135°F) or above. (E) A FOOD that is labeled frozen and shipped frozen by a FOOD PROCESSING PLANT shall be received frozen. (F) Upon receipt, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be free of evidence of previous temperature abuse.

> **[Food Code 2026 §3-501.14]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.14 (pp. 70-71). Cooling
> (A) Cooked TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled: (1) Within two hours from 57°C (135°F) to 21°C (70°F); and (2) Within a total of six hours from 57°C (135°F) to 5°C (41°F) or less. (B) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled within four hours to 5°C (41°F) or less if prepared from ingredients at ambient temperature, such as reconstituted FOODS and canned tuna. (C) Except as specified under ¶ (D) of this section, a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD received in compliance with LAWS allowing a temperature above 5°C (41°F) during shipment from the supplier as specified in ¶ 3-202.11(B), shall be cooled within four hours to 5°C (41°F) or less. (D) Raw EGGS shall be received as specified under ¶ 3-202.11(C) and immediately placed in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less.

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 2)
> 2. Followed by a 4-hour window where foods must be cooled to 41°F or less (21°C to 5°C) This means that within two hours, the food must be cooled from cooking temperature (135°F) to 70°F in order to eliminate risk of pathogen growth. Over the next 4 hours the food must be cooled from 70°F to 41°F or less. Note: If 70°F is reached before 2 hours, you have the remaining time to reach 41°F or less. Keep food out of the danger zone to avoid risk of foodborne illness! Cooling Methods in the FDA

> **[Food Code 2026 §3-403.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-403.11 (pp. 68-69). Reheating for Hot Holding
> (A) Except as specified under ¶¶ (B) and (C) and in ¶ (E) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked, cooled, and reheated for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) for 15 seconds. (B) Except as specified under ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD reheated in a microwave oven for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) and the FOOD is rotated or stirred, covered, and allowed to stand covered for two minutes after reheating. (C) READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that has been commercially processed and PACKAGED in a FOOD PROCESSING PLANT that is inspected by the REGULATORY AUTHORITY that has jurisdiction over the plant, shall be heated to a temperature of at least 57°C (135°F) when being reheated for hot holding. (D) Reheating for hot holding as specified under ¶¶ (A) - (C) of this section shall be done rapidly and the time the FOOD is between 5°C (41°F) and the temperatures specified under ¶¶ (A) - (C) of this section may not exceed two hours. (E) Remaining unsliced portions of MEAT roasts that are cooked as specified under ¶ 3-401.11(B) may be reheated for hot holding using the oven parameters and minimum time and temperature conditions specified under ¶ 3-401.11(B).

</details>


---

## q03 (single)

**Question:** What internal temperature does chicken need to reach when we cook it?

**Reference answer:** 74°C (165°F) or above for less than 1 second (instantaneous).

**Expected source:** food_code_2026 3-401.11

**Agent's answer:**

Poultry, including chicken, must be cooked to reach an internal temperature of 74°C (165°F) or above for less than 1 second (instantaneous) [Food Code 2026 §3-401.11]. If cooked in a microwave oven, it must be heated to at least 74°C (165°F) in all parts and allowed to stand covered for two minutes after cooking [Food Code 2026 §3-401.12]. Are we allowed to serve this? The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (p. 63). Raw Animal Foods (part 1)
> (A) Except as specified under ¶ (B) and in ¶¶ (C) and (D) of this section, raw animal FOODS such as EGGS, FISH, MEAT, POULTRY, and FOODS containing these raw animal FOODS, shall be cooked to heat all parts of the FOOD to a temperature and for a time that complies with one of the following methods based on the FOOD that is being cooked: (1) 63°C (145°F) or above for 15 seconds for: (a) Raw EGGS that are broken and prepared in response to a CONSUMER'S order and for immediate service, and (b) Except as specified under Subparagraphs (A)(2) and (A)(3) and ¶ (B), and in ¶ (C) of this section, FISH and INTACT MEAT including GAME ANIMALS commercially raised for FOOD as specified under Subparagraph 3-201.17(A)(1) and GAME ANIMALS under a voluntary inspection program as specified under Subparagraph 3-201.17(A)(2); (2) 68°C (155°F) for 17 seconds or the temperature specified in the following chart that corresponds to the holding time for RATITES, and nonINTACT MEATS; the following if they are COMMINUTED: FISH and GAME ANIMALS commercially raised for FOOD as specified under Subparagraph 3-201.17(A)(1), and GAME ANIMALS under a voluntary inspection program as specified under Subparagraph 3-201.17(A)(2); and raw EGGS that are not prepared as specified under Subparagraph (A)(1)(a) of this section; or: Minimum Temperature °C (°F) Minimum Time 63 (145) 3 minutes 66 (150) 1 minute 70 (158) < 1 second (instantaneous) (3) 74°C (165°F) or above for < 1 second (instantaneous) for POULTRY, BALUTS, wild GAME animals as specified under Subparagraphs 3-201.17(A)(3) and (4), stuffed FISH, stuffed MEAT, stuffed pasta, stuffed POULTRY, stuffed RATITES, or stuffing containing FISH, MEAT, POULTRY, or RATITES. (B) Whole MEAT roasts including beef, corned beef, lamb, pork, and cured pork roasts such as ham shall be cooked:

> **[Food Code 2026 §3-401.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.12 (pp. 65-66). Microwave Cooking
> Raw animal FOODS cooked in a microwave oven shall be: (A) Rotated or stirred throughout or midway during cooking to compensate for uneven distribution of heat; (B) Covered to retain surface moisture; (C) Heated to a temperature of at least 74°C (165°F) in all parts of the FOOD; and (D) Allowed to stand covered for two minutes after cooking to obtain temperature equilibrium.

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (pp. 63-65). Raw Animal Foods (part 2)
> (1) As specified in the following chart, to heat all parts of the FOOD to a temperature and for the holding time that corresponds to that temperature: and Temperature °C (°F) Time1 in Minutes 54.4 (130) 112 55.0 (131) 89 56.1 (133) 56 57.2 (135) 36 57.8 (136) 28 58.9 (138) 18 60.0 (140) 12 61.1 (142) 8 62.2 (144) 5 62.8 (145) 4 63.9 (147) 134 65.0 (149) 85 66.1 (151) 54 67.2 (153) 34 68.3 (155) 22 69.4 (157) 14 70.0 (158) 0 1 Holding time may include post-oven heat rise. (2) If cooked in an oven, use an oven that is preheated to the temperature specified for the roast's weight in the following chart and that is held at that temperature: Oven Temperature Based on Roast Weight Oven Type Less than 4.5 kg (10 lbs.) 4.5 kg (10 lbs.) or More Still Dry 177°C (350°F) or more 121°C (250°F) or more Convection 163°C (325°F) or more 121°C (250°F) or more High Humidity 1 121°C (250°F) or less 121°C (250°F) or less 1 Relative humidity greater than 90% for at least 1 hour as measured in the cooking chamber or exit of the oven; or in a moisture-impermeable bag that provides 100% humidity. (C) A raw or undercooked WHOLE-MUSCLE, INTACT BEEF steak may be served or offered for sale in a READY-TO-EAT form if: (1) The FOOD ESTABLISHMENT serves a population that is not a HIGHLY SUSCEPTIBLE POPULATION, (2) The steak is prepared so that it remains intact, and (3) The steak is cooked on both the top and bottom to a surface temperature of 63°C (145°F) or above and a cooked color change is achieved on all external surfaces.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-401.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.13 (p. 66). Plant Food Cooking for Hot Holding
> Plant FOODS that are cooked for hot holding shall be cooked to a temperature of 57°C (135°F) or as specified under § 3-401.15.

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 2)
> 2. Followed by a 4-hour window where foods must be cooled to 41°F or less (21°C to 5°C) This means that within two hours, the food must be cooled from cooking temperature (135°F) to 70°F in order to eliminate risk of pathogen growth. Over the next 4 hours the food must be cooled from 70°F to 41°F or less. Note: If 70°F is reached before 2 hours, you have the remaining time to reach 41°F or less. Keep food out of the danger zone to avoid risk of foodborne illness! Cooling Methods in the FDA

</details>


---

## q04 (single)

**Question:** What temperature do burgers made from ground beef have to be cooked to?

**Reference answer:** 68°C (155°F) for 17 seconds, or an equivalent from the chart: 63°C (145°F) for 3 minutes, 66°C (150°F) for 1 minute, 70°C (158°F) instantaneous.

**Expected source:** food_code_2026 3-401.11

**Agent's answer:**

Ground beef is comminuted (ground) meat and must be cooked to 68°C (155°F) for 17 seconds, or by using one of the following alternative time and temperature combinations: 63°C (145°F) for 3 minutes, 66°C (150°F) for 1 minute, or 70°C (158°F) for less than 1 second (instantaneous) [Food Code 2026 §3-401.11].

**Passages the answer cites:**

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (p. 63). Raw Animal Foods (part 1)
> (A) Except as specified under ¶ (B) and in ¶¶ (C) and (D) of this section, raw animal FOODS such as EGGS, FISH, MEAT, POULTRY, and FOODS containing these raw animal FOODS, shall be cooked to heat all parts of the FOOD to a temperature and for a time that complies with one of the following methods based on the FOOD that is being cooked: (1) 63°C (145°F) or above for 15 seconds for: (a) Raw EGGS that are broken and prepared in response to a CONSUMER'S order and for immediate service, and (b) Except as specified under Subparagraphs (A)(2) and (A)(3) and ¶ (B), and in ¶ (C) of this section, FISH and INTACT MEAT including GAME ANIMALS commercially raised for FOOD as specified under Subparagraph 3-201.17(A)(1) and GAME ANIMALS under a voluntary inspection program as specified under Subparagraph 3-201.17(A)(2); (2) 68°C (155°F) for 17 seconds or the temperature specified in the following chart that corresponds to the holding time for RATITES, and nonINTACT MEATS; the following if they are COMMINUTED: FISH and GAME ANIMALS commercially raised for FOOD as specified under Subparagraph 3-201.17(A)(1), and GAME ANIMALS under a voluntary inspection program as specified under Subparagraph 3-201.17(A)(2); and raw EGGS that are not prepared as specified under Subparagraph (A)(1)(a) of this section; or: Minimum Temperature °C (°F) Minimum Time 63 (145) 3 minutes 66 (150) 1 minute 70 (158) < 1 second (instantaneous) (3) 74°C (165°F) or above for < 1 second (instantaneous) for POULTRY, BALUTS, wild GAME animals as specified under Subparagraphs 3-201.17(A)(3) and (4), stuffed FISH, stuffed MEAT, stuffed pasta, stuffed POULTRY, stuffed RATITES, or stuffing containing FISH, MEAT, POULTRY, or RATITES. (B) Whole MEAT roasts including beef, corned beef, lamb, pork, and cured pork roasts such as ham shall be cooked:

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (pp. 63-65). Raw Animal Foods (part 2)
> (1) As specified in the following chart, to heat all parts of the FOOD to a temperature and for the holding time that corresponds to that temperature: and Temperature °C (°F) Time1 in Minutes 54.4 (130) 112 55.0 (131) 89 56.1 (133) 56 57.2 (135) 36 57.8 (136) 28 58.9 (138) 18 60.0 (140) 12 61.1 (142) 8 62.2 (144) 5 62.8 (145) 4 63.9 (147) 134 65.0 (149) 85 66.1 (151) 54 67.2 (153) 34 68.3 (155) 22 69.4 (157) 14 70.0 (158) 0 1 Holding time may include post-oven heat rise. (2) If cooked in an oven, use an oven that is preheated to the temperature specified for the roast's weight in the following chart and that is held at that temperature: Oven Temperature Based on Roast Weight Oven Type Less than 4.5 kg (10 lbs.) 4.5 kg (10 lbs.) or More Still Dry 177°C (350°F) or more 121°C (250°F) or more Convection 163°C (325°F) or more 121°C (250°F) or more High Humidity 1 121°C (250°F) or less 121°C (250°F) or less 1 Relative humidity greater than 90% for at least 1 hour as measured in the cooking chamber or exit of the oven; or in a moisture-impermeable bag that provides 100% humidity. (C) A raw or undercooked WHOLE-MUSCLE, INTACT BEEF steak may be served or offered for sale in a READY-TO-EAT form if: (1) The FOOD ESTABLISHMENT serves a population that is not a HIGHLY SUSCEPTIBLE POPULATION, (2) The steak is prepared so that it remains intact, and (3) The steak is cooked on both the top and bottom to a surface temperature of 63°C (145°F) or above and a cooked color change is achieved on all external surfaces.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-401.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.12 (pp. 65-66). Microwave Cooking
> Raw animal FOODS cooked in a microwave oven shall be: (A) Rotated or stirred throughout or midway during cooking to compensate for uneven distribution of heat; (B) Covered to retain surface moisture; (C) Heated to a temperature of at least 74°C (165°F) in all parts of the FOOD; and (D) Allowed to stand covered for two minutes after cooking to obtain temperature equilibrium.

> **[Food Code 2026 §3-401.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.13 (p. 66). Plant Food Cooking for Hot Holding
> Plant FOODS that are cooked for hot holding shall be cooked to a temperature of 57°C (135°F) or as specified under § 3-401.15.

> **[Food Code 2026 §3-202.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-202.11 (pp. 48-49). Temperature
> (A) Except as specified in ¶ (B) of this section, refrigerated, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be at a temperature of 5°C (41°F) or below when received. (B) If a temperature other than 5°C (41°F) for a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD is specified in LAW governing its distribution, such as LAWS governing milk and MOLLUSCAN SHELLFISH, the FOOD may be received at the specified temperature. (C) Raw EGGS shall be received in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (D) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked to a temperature and for a time specified under §§ 3-401.11 – 3-401.13 and received hot shall be at a temperature of 57°C (135°F) or above. (E) A FOOD that is labeled frozen and shipped frozen by a FOOD PROCESSING PLANT shall be received frozen. (F) Upon receipt, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be free of evidence of previous temperature abuse.

</details>


---

## q05 (single)

**Question:** We made chili yesterday and cooled it. What temperature do we have to reheat it to before putting it back in the hot-holding unit?

**Reference answer:** All parts to at least 74°C (165°F) for 15 seconds, done rapidly: no more than 2 hours between 5°C (41°F) and 74°C. In a microwave: 74°C, rotated or stirred, covered, and left to stand covered 2 minutes.

**Expected source:** food_code_2026 3-403.11

**Agent's answer:**

Time/temperature control for safety food that is cooked, cooled, and reheated for hot holding must be reheated so that all parts of the food reach at least 74°C (165°F) for 15 seconds [Food Code 2026 §3-403.11]. This reheating must be done rapidly, and the time the food is between 5°C (41°F) and 74°C (165°F) may not exceed two hours [Food Code 2026 §3-403.11]. 

The version of the Food Code adopted by your state or local jurisdiction is what applies to your establishment.

**Passages the answer cites:**

> **[Food Code 2026 §3-403.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-403.11 (pp. 68-69). Reheating for Hot Holding
> (A) Except as specified under ¶¶ (B) and (C) and in ¶ (E) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked, cooled, and reheated for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) for 15 seconds. (B) Except as specified under ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD reheated in a microwave oven for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) and the FOOD is rotated or stirred, covered, and allowed to stand covered for two minutes after reheating. (C) READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that has been commercially processed and PACKAGED in a FOOD PROCESSING PLANT that is inspected by the REGULATORY AUTHORITY that has jurisdiction over the plant, shall be heated to a temperature of at least 57°C (135°F) when being reheated for hot holding. (D) Reheating for hot holding as specified under ¶¶ (A) - (C) of this section shall be done rapidly and the time the FOOD is between 5°C (41°F) and the temperatures specified under ¶¶ (A) - (C) of this section may not exceed two hours. (E) Remaining unsliced portions of MEAT roasts that are cooked as specified under ¶ 3-401.11(B) may be reheated for hot holding using the oven parameters and minimum time and temperature conditions specified under ¶ 3-401.11(B).

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-401.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.13 (p. 66). Plant Food Cooking for Hot Holding
> Plant FOODS that are cooked for hot holding shall be cooked to a temperature of 57°C (135°F) or as specified under § 3-401.15.

> **[Food Code 2026 §3-501.16]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.16 (p. 72). Time/Temperature Control for Safety Food, Hot and Cold Holding
> (A) Except during preparation, cooking, or cooling, or when time is used as the public health control as specified under § 3-501.19, and except as specified under ¶ (B) and in ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be maintained: (1) At 57°C (135°F) or above, except roasts cooked to a temperature and for a time specified in ¶ 3-401.11(B) or reheated as specified in ¶ 3-403.11(E) may be held at a temperature of 54°C (130°F) or above; or (2) At 5°C (41°F) or less. (B) EGGS that have not been treated to destroy all viable Salmonellae shall be stored in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (C) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD in a homogenous liquid form may be maintained outside of the temperature control requirements, as specified under ¶ (A) of this section, while contained within specially designed EQUIPMENT that complies with the design and construction requirements as specified under ¶ 4-204.13(E). On-premises preparation Prepare and hold cold

> **[Food Code 2026 §3-202.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-202.11 (pp. 48-49). Temperature
> (A) Except as specified in ¶ (B) of this section, refrigerated, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be at a temperature of 5°C (41°F) or below when received. (B) If a temperature other than 5°C (41°F) for a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD is specified in LAW governing its distribution, such as LAWS governing milk and MOLLUSCAN SHELLFISH, the FOOD may be received at the specified temperature. (C) Raw EGGS shall be received in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (D) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked to a temperature and for a time specified under §§ 3-401.11 – 3-401.13 and received hot shall be at a temperature of 57°C (135°F) or above. (E) A FOOD that is labeled frozen and shipped frozen by a FOOD PROCESSING PLANT shall be received frozen. (F) Upon receipt, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be free of evidence of previous temperature abuse.

> **[Food Code 2026 §3-501.14]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.14 (pp. 70-71). Cooling
> (A) Cooked TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled: (1) Within two hours from 57°C (135°F) to 21°C (70°F); and (2) Within a total of six hours from 57°C (135°F) to 5°C (41°F) or less. (B) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled within four hours to 5°C (41°F) or less if prepared from ingredients at ambient temperature, such as reconstituted FOODS and canned tuna. (C) Except as specified under ¶ (D) of this section, a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD received in compliance with LAWS allowing a temperature above 5°C (41°F) during shipment from the supplier as specified in ¶ 3-202.11(B), shall be cooled within four hours to 5°C (41°F) or less. (D) Raw EGGS shall be received as specified under ¶ 3-202.11(C) and immediately placed in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less.

</details>


---

## q06 (single)

**Question:** How many days can we keep a soup or sauce we made in the fridge before we have to throw it out?

**Reference answer:** At most 7 days at 5°C (41°F) or less, counting the day of preparation as Day 1; it must be date-marked if kept more than 24 hours.

**Expected source:** food_code_2026 3-501.17

**Agent's answer:**

Refrigerated, ready-to-eat time/temperature control for safety food prepared and held for more than 24 hours must be clearly marked to be consumed, sold, or discarded within a maximum of seven days when held at a temperature of 5°C (41°F) or less, with the day of preparation counted as Day 1 [Food Code 2026 §3-501.17]. Are you allowed to keep it longer if frozen? The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §3-501.17]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.17 (pp. 72-73). Ready-to-Eat, Time/Temperature Control for Safety Food, Date Marking (part 1)
> (A) Except when PACKAGING FOOD using a REDUCED OXYGEN PACKAGING method as specified under § 3-502.12, and except as specified in ¶¶ (E) and (F) of this section, refrigerated, READY-TO-EAT, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD prepared and held in a FOOD ESTABLISHMENT for more than 24 hours shall be clearly marked to indicate the date or day by which the FOOD shall be consumed on the PREMISES, sold, or discarded when held at a temperature of 5°C (41°F) or less for a maximum of seven days. The day of preparation shall be counted as Day 1. Commercially processed food Open and hold cold (B) Except as specified in ¶¶ (E) - (G) of this section, refrigerated, READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD prepared and PACKAGED by a FOOD PROCESSING PLANT shall be clearly marked, at the time the original container is opened in a FOOD ESTABLISHMENT and if the FOOD is held for more than 24 hours, to indicate the date or day by which the FOOD shall be consumed on the PREMISES, sold, or discarded, based on the temperature and time combinations specified in ¶ (A) of this section and: (1) The day the original container is opened in the FOOD ESTABLISHMENT shall be counted as Day 1; and (2) The day or date marked by the FOOD ESTABLISHMENT may not exceed a manufacturer’s use-by date if the manufacturer determined the use-by date based on FOOD safety. (C) A refrigerated, READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD ingredient or a portion of a refrigerated, READY-TO-EAT, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is subsequently combined with additional ingredients or portions of FOOD shall retain the date marking of the earliest-prepared or first-prepared ingredient.

> **[Food Code 2026 §3-501.17]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.17 (p. 73). Ready-to-Eat, Time/Temperature Control for Safety Food, Date Marking (part 2)
> (D) A date marking system that meets the criteria stated in ¶¶ (A) and (B) of this section may include: (1) Using a method APPROVED by the REGULATORY AUTHORITY for refrigerated, READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is frequently rewrapped, such as lunchmeat or a roast, or for which date marking is impractical, such as soft serve mix or milk in a dispensing machine; (2) Marking the date or day of preparation, with a procedure to discard the FOOD on or before the last date or day by which the FOOD must be consumed on the PREMISES, sold, or discarded as specified under ¶ (A) of this section; (3) Marking the date or day the original container is opened in a FOOD ESTABLISHMENT, with a procedure to discard the FOOD on or before the last date or day by which the FOOD must be consumed on the PREMISES, sold, or discarded as specified under ¶ (B) of this section; or (4) Using calendar dates, days of the week, color-coded marks, or other effective marking methods, provided that the marking system is disclosed to the REGULATORY AUTHORITY upon request. (E) Paragraphs (A) and (B) of this section do not apply to individual meal portions served or rePACKAGED for sale from a bulk container upon a CONSUMER’S request. (F) Paragraphs (A) and (B) of this section do not apply to SHELLSTOCK (G) Paragraph (B) of this section does not apply to the following FOODS prepared and PACKAGED by a FOOD PROCESSING PLANT inspected by a REGULATORY AUTHORITY: (1) Deli salads, such as ham salad, seafood salad, chicken salad, EGG salad, pasta salad, potato salad, and macaroni salad, manufactured in accordance with 21 CFR 117 Current good manufacturing practice in manufacturing, packing, or holding human FOOD;

> **[Food Code 2026 §3-501.17]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.17 (p. 74). Ready-to-Eat, Time/Temperature Control for Safety Food, Date Marking (part 3)
> (2) Hard cheeses containing not more than 39% moisture as defined in 21 CFR 133 Cheeses and related cheese products, such as cheddar, gruyere, parmesan and reggiano, and romano; (3) Semi-soft cheeses containing more than 39% moisture, but not more than 50% moisture, as defined in 21 CFR 133 Cheeses and related cheese products, such as blue, edam, gorgonzola, gouda, and monterey jack; (4) Cultured dairy products as defined in 21 CFR 131 Milk and cream, such as yogurt, sour cream, and buttermilk; (5) Preserved FISH products, such as pickled herring and dried or salted cod, and other acidified FISH products defined in 21 CFR 114 Acidified FOODS; (6) Shelf stable, dry fermented sausages, such as pepperoni and Genoa; and (7) Shelf stable salt-cured products such as prosciutto and Parma (ham).

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-501.18]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.18 (p. 74). Ready-to-Eat, Time/Temperature Control for Safety Food, Disposition
> (A) A FOOD specified in ¶ 3-501.17(A) or (B) shall be discarded if it: (1) Exceeds the temperature and time combination specified in ¶ 3-501.17(A), except time that the product is frozen; (2) Is in a container or PACKAGE that does not bear a date or day; or (3) Is inappropriately marked with a date or day that exceeds a temperature and time combination as specified in ¶ 3-501.17(A). (B) Refrigerated, READY-TO-EAT, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD prepared in a FOOD ESTABLISHMENT and dispensed through a VENDING MACHINE with an automatic shutoff control shall be discarded if it exceeds a temperature and time combination as specified in ¶ 3-501.17(A).

> **[Food Code 2026 §3-501.19]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.19 (pp. 75-76). Time as a Public Health Control (part 3)
> (3) The FOOD shall be marked or otherwise identified to indicate: (a) The time when the FOOD is removed from 5°C (41°F) or less cold holding temperature control, and (b) The time that is six hours past the point in time when the FOOD is removed from cold holding temperature control; (4) The FOOD shall be: (a) Discarded if the temperature of the FOOD exceeds 21°C (70°F), or (b) Cooked and served, served at any temperature if READY-TO-EAT, or discarded within a maximum of six hours from the point in time when the FOOD is removed from 5°C (41°F) or less cold holding temperature control; and (5) The FOOD in unmarked containers or PACKAGES, or marked with a time that exceeds the six-hour limit shall be discarded. (D) A FOOD ESTABLISHMENT that serves a HIGHLY SUSCEPTIBLE POPULATION may not use time as specified under ¶¶ (A), (B), or (C) of this section as the public health control for raw EGGS.

</details>


---

## q07 (single)

**Question:** One of our cooks wants to make desserts at home and bring them in to sell at the restaurant. Is that allowed?

**Reference answer:** No. Food prepared in a private home may not be used or offered for human consumption in a food establishment.

**Expected source:** food_code_2026 3-201.11

**Agent's answer:**

No, food prepared in a private home may not be used or offered for human consumption in a food establishment [Food Code 2026 §3-201.11]. Additionally, a private home may not be used for conducting food establishment operations [Food Code 2026 §6-202.111]. The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §6-202.111]** Source: FDA Food Code 2026, Chapters 1-6, §6-202.111 (p. 137). Private Homes and Living or Sleeping Quarters, Use Prohibition
> A private home, a room used as living or sleeping quarters, or an area directly opening into a room used as living or sleeping quarters may not be used for conducting FOOD ESTABLISHMENT operations.

> **[Food Code 2026 §3-201.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-201.11 (pp. 45-46). Compliance with Food Law (part 1)
> (A) FOOD shall be obtained from sources that comply with LAW. (B) FOOD prepared in a private home may not be used or offered for human consumption in a FOOD ESTABLISHMENT. (C) PACKAGED FOOD shall be labeled as specified in LAW, including 21 CFR 101 FOOD Labeling, 9 CFR 317 Labeling, Marking Devices, and Containers, and 9 CFR 381 Subpart N Labeling and Containers, and as specified under § 3-202.18. (D) FISH, other than those specified in ¶ 3-402.11(B), that are intended for consumption in raw or undercooked form and allowed as specified in ¶ 3-401.11(D), may be offered for sale or service if they are obtained from a supplier that freezes the FISH, as specified under § 3-402.11; or if they are frozen on the PREMISES as specified under § 3-402.11 and records are retained as specified under § 3-402.12. (E) WHOLE-MUSCLE, INTACT BEEF steaks that are intended for consumption in an undercooked form without a CONSUMER advisory as specified in ¶ 3-401.11(C) shall be: (1) Obtained from a FOOD PROCESSING PLANT that does not MECHANICALLY TENDERIZE, vacuum tumble with solutions, reconstruct, cube or pound these WHOLE-MUSCLE, INTACT BEEF steaks; or (2) Deemed acceptable by the REGULATORY AUTHORITY based on other evidence, such as written buyer specifications or invoices, that indicates that the steaks meet the definition of WHOLE-MUSCLE, INTACT BEEF; and (3) If individually cut in a FOOD ESTABLISHMENT: (a) Cut from WHOLE-MUSCLE, INTACT BEEF that is received from a FOOD PROCESSING PLANT as specified in Subparagraph (E)(1) of this section or identified as specified in Subparagraph (E)(2) of this section; and (b) Prepared so they remain intact.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 8-9). Statement of Application and Listing of Terms (part 9)
> (3) "Food establishment" does not include: (a) An establishment that offers only pre-PACKAGED FOODS that are not TIME/TEMPERATURE CONTROL FOR SAFETY FOODS; (b) A produce stand that only offers whole, uncut fresh fruits and vegetables; (c) A FOOD PROCESSING PLANT; including those that are located on the PREMISES of a FOOD ESTABLISHMENT; (d) A kitchen in a private home if only FOOD that is not TIME/TEMPERATURE CONTROL FOR SAFETY FOOD, is prepared for sale or service at a function such as a religious or charitable organization’s bake sale if allowed by LAW and if the CONSUMER is informed by a clearly visible placard at the sales or service location that the FOOD is prepared in a kitchen that is not subject to regulation and inspection by the REGULATORY AUTHORITY; (e) An area where FOOD that is prepared as specified in Subparagraph (3)(d) of this definition is sold or offered for human consumption; (f) A kitchen in a private home, such as a small family day-care provider; or a bed-and-breakfast operation that prepares and offers FOOD to guests if the home is owner occupied, the number of available guest bedrooms does not exceed 6, breakfast is the only meal offered, the number of guests served does not exceed 18, and the CONSUMER is informed by statements contained in published advertisements, mailed brochures, and placards posted at the registration area that the FOOD is prepared in a kitchen that is not regulated and inspected by the REGULATORY AUTHORITY; or (g) A private home that receives catered or home-delivered FOOD. Food Processing Plant. (1) "Food processing plant" means a commercial operation that manufactures, PACKAGES, labels, or stores FOOD for human consumption, and provides FOOD for sale or distribution to other business entities such as FOOD PROCESSING PLANTS or FOOD ESTABLISHMENTS.

> **[Food Code 2026 §3-201.16]** Source: FDA Food Code 2026, Chapters 1-6, §3-201.16 (p. 47). Wild Mushrooms
> (A) Except as specified in ¶ (B) of this section, mushroom species picked in the wild shall not be offered for sale or service by a FOOD ESTABLISHMENT unless the FOOD ESTABLISHMENT has been APPROVED to do so. (B) This section does not apply to: (1) Cultivated wild mushroom species that are grown, harvested, and processed in an operation that is regulated by the FOOD REGULATORY AGENCY that has jurisdiction over the operation; or (2) Wild mushroom species if they are in PACKAGED form and are the product of a FOOD PROCESSING PLANT that is regulated by the FOOD REGULATORY AGENCY that has jurisdiction over the plant.

> **[Food Code 2026 §3-403.10]** Source: FDA Food Code 2026, Chapters 1-6, §3-403.10 (p. 68). Preparation for Immediate Service
> Cooked and refrigerated FOOD that is prepared for immediate service in response to an individual CONSUMER order, such as a roast beef sandwich au jus, may be served at any temperature.

</details>


---

## q08 (single)

**Question:** How long do staff need to wash their hands for?

**Reference answer:** At least 20 seconds in total, rubbing vigorously with soap for at least 10 to 15 seconds, then rinsing under clean, running warm water and drying.

**Expected source:** food_code_2026 2-301.12

**Agent's answer:**

Staff must clean their hands and exposed portions of their arms for at least 20 seconds [Food Code 2026 §2-301.12]. This includes rubbing together vigorously with soap for at least 10 to 15 seconds [Food Code 2026 §2-301.12].

**Passages the answer cites:**

> **[Food Code 2026 §2-301.12]** Source: FDA Food Code 2026, Chapters 1-6, §2-301.12 (pp. 39-40). Cleaning Procedure
> (A) Except as specified in ¶ (D) of this section, FOOD EMPLOYEES shall clean their hands and exposed portions of their arms, including surrogate prosthetic devices for hands or arms for at least 20 seconds, using a cleaning compound in a HANDWASHING SINK that is equipped as specified under § 5-202.12 and Subpart 6-301. (B) FOOD EMPLOYEES shall use the following cleaning procedure in the order stated to clean their hands and exposed portions of their arms, including surrogate prosthetic devices for hands and arms: (1) Rinse under clean, running warm water; (2) Apply an amount of cleaning compound recommended by the cleaning compound manufacturer; (3) Rub together vigorously for at least 10 to 15 seconds while: (a) Paying particular attention to removing soil from underneath the fingernails during the cleaning procedure, and (b) Creating friction on the surfaces of the hands and arms or surrogate prosthetic devices for hands and arms, fingertips, and areas between the fingers; (4) Thoroughly rinse under clean, running warm water; and (5) Immediately follow the cleaning procedure with thorough drying using a method as specified under § 6-301.12. (C) To avoid re-contaminating their hands or surrogate prosthetic devices, FOOD EMPLOYEES may use disposable paper towels or similar clean barriers when touching surfaces such as manually operated faucet handles on a HANDWASHING SINK or the handle of a restroom door. (D) If APPROVED and capable of removing the types of soils encountered in the FOOD operations involved, an automatic handwashing facility may be used by FOOD EMPLOYEES to clean their hands or surrogate prosthetic devices.

<details><summary>Other retrieved passages</summary>

> **[Employee Health Handbook p. 14]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), pp. 14-15. What handwashing steps do food employees need to follow?
> Clean hands and exposed portions of arms, including surrogate prosthetic devices for hands and arms, for at least 20 seconds by the following method: 1. Rinse under clean, warm running water; 2. Apply soap and rub all surfaces of the hands and fingers together vigorously with friction for at least 10 to 15 seconds, giving particular attention to the area under the fingernails, between the fingers/fingertips, and surfaces of the hands, arms, and surrogate prosthetic devices; 3. Rinse thoroughly with clean, warm running water; and Personal Hygiene 4. Thoroughly dry the hands and exposed portions of arms with single-use paper toweling, a heated-air hand-drying device, or a clean, unused towel from a continuous towel system that supplies the user with a clean towel. Avoid recontamination of hands and arms by using a clean barrier, such as a paper towel, when turning off hand sink faucets or touching the handle of a restroom door. It is important to follow these steps to remove germs from hands and ensure hands are as clean as possible. Thorough handwashing with warm water, the recommended amount of soap as indicated by the manufacturer, and proper hand drying are essential to reduce the possibility of hands transferring microorganisms to food.

> **[Employee Health Handbook p. 15]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 15. How important is the temperature of water used for handwashing?
> Warm water is generally more comfortable than cold water and encourages handwashing for the recommended duration. The water temperature used in handwashing can also affect the solubility or emulsification of some soils. Warm water is more effective than cold water in removing fatty soils. An adequate flow of warm water will cause soap to lather and aid in flushing soil quickly from the hands. The 2017 FDA Food Code specifies that a handwashing sink shall be equipped to provide water at a temperature of at least 38°C (100°F) through a mixing valve or combination faucet.

> **[Employee Health Handbook p. 14]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 14. What is effective handwashing?
> It is the act of cleansing hands by applying soap and water, rubbing them together vigorously, rinsing them with clean water, and thoroughly drying them. This process gets rid of dirt and germs. Every handwashing stage is important and effectively contributes to soil removal and reduction of microorganisms that can cause illness.

> **[Food Code 2026 §5-202.12]** Source: FDA Food Code 2026, Chapters 1-6, §5-202.12 (pp. 121-122). Handwashing Sink, Installation
> (A) A HANDWASHING SINK shall be equipped to provide water at a temperature of at least 29.4°C (85°F) through a mixing valve or combination faucet (B) A steam, mixing valve may not be used at a HANDWASHING SINK. (C) A self-closing, slow-closing, or metering faucet shall provide a flow of water for at least 15 seconds without the need to reactivate the faucet. (D) An automatic handwashing facility shall be installed in accordance with manufacturer’s instructions.

</details>


---

## q09 (single)

**Question:** Can our cooks wear a wedding ring while preparing food?

**Reference answer:** Yes. Jewelry on the arms and hands is not allowed while preparing food, except a plain ring such as a wedding band (and a medically necessary device for someone covered by the ADA).

**Expected source:** food_code_2026 2-303.11

**Agent's answer:**

Yes, a food employee may wear a plain ring, such as a wedding band, while preparing food [Food Code 2026 §2-303.11]. The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §2-303.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-303.11 (p. 42). Prohibition
> (A) Except as specified in ¶¶ (B) and (C) of this section, FOOD EMPLOYEES may not wear jewelry on their arms and hands while preparing FOOD. (B) A plain ring, such as a wedding band, may be worn. (C) An individual with a disability covered under the Americans with Disabilities Act may be allowed to wear a medically necessary device that can be kept clean and worn in a manner that prevents potential contamination.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §2-302.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-302.11 (pp. 41-42). Maintenance
> (A) FOOD EMPLOYEES shall keep their fingernails trimmed, filed, and maintained so the edges and surfaces are cleanable and not rough. (B) Unless wearing intact gloves in good repair, a FOOD EMPLOYEE may not wear fingernail polish or artificial fingernails when working with exposed FOOD.

> **[Food Code 2026 §3-305.14]** Source: FDA Food Code 2026, Chapters 1-6, §3-305.14 (p. 61). Food Preparation
> During preparation, unPACKAGED FOOD shall be protected from environmental sources of contamination.

> **[Employee Health Handbook p. 17]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 17. Should food employees with one hand or those with a surrogate prosthetic device for hands and arms follow these handwashing procedures? (part 2)
> • Wear disposable gloves over artificial nails, nail polish, or uncleanable orthopedic support devices. The 2017 FDA Food Code allows bare hand contact with RTE food only when the regulatory authority has granted prior approval for an alternative procedure. The alternative procedure must address the management of food employees and related food handling activities to prevent food contamination, including the enforcement of thorough handwashing practices after toilet use. No Bare Hand Contact with Ready-to-Eat Foods

> **[Food Code 2026 §4-204.15]** Source: FDA Food Code 2026, Chapters 1-6, §4-204.15 (p. 93). Bearings and Gear Boxes, Leakproof
> EQUIPMENT containing bearings and gears that require lubricants shall be designed and constructed so that the lubricant cannot leak, drip, or be forced into FOOD or onto FOOD-CONTACT SURFACES.

</details>


---

## q10 (single)

**Question:** Can staff plate salads or make sandwiches with their bare hands?

**Reference answer:** No. Exposed ready-to-eat food may not be touched with bare hands; use utensils such as deli tissue, spatulas, tongs, single-use gloves or dispensing equipment. Exceptions: when it is added to food that will be cooked, or with prior approval and written procedures (not when serving a highly susceptible population).

**Expected source:** food_code_2026 3-301.11

**Agent's answer:**

Except when washing fruits and vegetables or under specific approved alternative procedures, food employees may not contact exposed, ready-to-eat food (such as salads and sandwiches) with their bare hands [Food Code 2026 §3-301.11]. Staff must use suitable utensils such as deli tissue, spatulas, tongs, single-use gloves, or dispensing equipment [Food Code 2026 §3-301.11]. 

The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §3-301.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-301.11 (pp. 52-53). Preventing Contamination from Hands (part 1)
> (A) FOOD EMPLOYEES shall wash their hands as specified under § 2-301.12. (B) Except when washing fruits and vegetables as specified under § 3-302.15 or as specified in ¶¶ (D) and (E) of this section, FOOD EMPLOYEES may not contact exposed, READY-TO-EAT FOOD with their bare hands and shall use suitable UTENSILS such as deli tissue, spatulas, tongs, single-use gloves, or dispensing EQUIPMENT. (C) FOOD EMPLOYEES shall minimize bare hand and arm contact with exposed FOOD that is not in a ready-to-eat form. (D) Paragraph (B) of this section does not apply to a FOOD EMPLOYEE that contacts exposed, READY-TO-EAT FOOD with bare hands at the time the READY-TO-EAT FOOD is being added as an ingredient to a FOOD that: (1) Contains a raw animal FOOD and is to be cooked in the FOOD ESTABLISHMENT to heat all parts of the FOOD to the minimum temperatures specified in ¶¶ 3-401.11(A)-(B) or § 3-401.12; or (2) Does not contain a raw animal FOOD but is to be cooked in the FOOD ESTABLISHMENT to heat all parts of the food to a temperature of at least 63°C (145°F). (E) FOOD EMPLOYEES not serving a HIGHLY SUSCEPTIBLE POPULATION may contact exposed, READY-TO-EAT FOOD with their bare hands if: (1) The PERMIT HOLDER obtains prior APPROVAL from the REGULATORY AUTHORITY. (2) Written procedures are maintained in the FOOD ESTABLISHMENT and made available to the REGULATORY AUTHORITY upon request that include: (a) For each bare hand contact procedure, a listing of the specific READY-TO-EAT FOODs that are touched by bare hands; (b) Diagrams and other information showing that handwashing facilities, installed, located, equipped, and maintained as specified under §§ 5-

> **[Food Code 2026 §3-301.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-301.11 (p. 54). Preventing Contamination from Hands (part 3)
> (6) Documentation that FOOD EMPLOYEES contacting READY-TO-EAT FOOD with bare hands use two or more of the following control measures to provide additional safeguards to HAZARDS associated with bare hand contact: (a) Double handwashing; (b) Nail brushes; (c) A hand antiseptic after handwashing as specified under § 2-301.16; (d) Incentive programs such as paid sick leave that assist or encourage FOOD EMPLOYEES not to work when they are ill, or (e) Other control measures APPROVED by the REGULATORY AUTHORITY; and (7) Documentation that corrective action is taken when Subparagraphs (E)(1) - (6) of this section are not followed.

<details><summary>Other retrieved passages</summary>

> **[Employee Health Handbook p. 17]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 17. Should food employees with one hand or those with a surrogate prosthetic device for hands and arms follow these handwashing procedures? (part 2)
> • Wear disposable gloves over artificial nails, nail polish, or uncleanable orthopedic support devices. The 2017 FDA Food Code allows bare hand contact with RTE food only when the regulatory authority has granted prior approval for an alternative procedure. The alternative procedure must address the management of food employees and related food handling activities to prevent food contamination, including the enforcement of thorough handwashing practices after toilet use. No Bare Hand Contact with Ready-to-Eat Foods

> **[Employee Health Handbook p. 16]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), pp. 16-17. Should food employees with one hand or those with a surrogate prosthetic device for hands and arms follow these handwashing procedures? (part 1)
> Yes, this requirement for thorough handwashing is achievable through reasonable accommodation in accordance with the ADA. In order to achieve the intent of this requirement, devices are available that are attachable to a lavatory. These devices enable a one-handed food employee to generate the necessary friction to achieve the intent of this requirement. When hands are heavily contaminated, effective handwashing practices may not be enough to prevent the transmission of transient pathogens from the hands to RTE foods. The 2017 FDA Food Code discourages bare hand contact with RTE food (i.e., food that is eaten without further washing or cooking) and requires the use of suitable utensils such as scoops, spoons, forks, spatulas, tongs, deli tissue, single-use gloves, or dispensing equipment when handling these food items. Bare hand contact with an RTE food, such as sandwiches and salads, can result in contamination of food and contribute to foodborne illness outbreaks. Therefore, food employees should always use suitable utensils such as spatulas, tongs, single-use gloves, or dispensing equipment when handling RTE foods. Single-use gloves used along with handwashing can be an effective barrier to decrease the transfer of microorganisms from the hand to food. However, gloves are not total barriers to microbial transmission, and will not be an effective barrier alone for food employee without education on proper glove use and handwashing requirements. Follow these instructions for the use of single-use gloves: • Always wash hands before donning gloves. • Change disposable gloves between handling raw products and RTE products. • Do not wash or reuse disposable gloves. • Discard torn or damaged disposable gloves. • Cover an infected lesion (cut, burn, or boil) with pus with a waterproof covering and disposable glove.

> **[Employee Health Handbook p. 2]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 2. Introduction (part 5)
> “No Bare Hand Contact” is the practice of preventing direct contact with bare hands while handling RTE foods. This practice provides a secondary protection against the contamination of foods that do not require further cooking with microbial pathogens from the hands of ill food employees. The 2017 FDA Food Code recognizes the increased risks of foodborne illness in highly susceptible populations (HSPs) such as the very young, older adults, and those with compromised immune systems. Food establishments in health care; assisted living, child or adult day care, hospitals, nursing homes, nursery schools, and senior citizen centers are required to take additional precautions to prevent the transmission of foodborne illness. For additional information about food safety, employee health and hygiene, and prevention of foodborne illness, go to the FDA/Center for Food Safety and Applied Nutrition’s (CFSAN’s) Retail Food Protection web page at: http:/ /www.fda.gov/RetailFoodProtection. Source: Adapted from the 2017 FDA Food Code, U.S. Department of Health and Human Services, Public Health Service, Food and Drug Administration https://www.fda.gov/downloads/Food/GuidanceRegulation/RetailFoodProtection/FoodCode/ UCM595140.pdf (FDA 2017 Food Code) Acknowledgements: • FDA National Retail Food Team • FDA CFSAN Retail Food Protection Staff

</details>


---

## q11 (single)

**Question:** What are the approved ways to thaw frozen chicken?

**Reference answer:** Under refrigeration that keeps it at 5°C (41°F) or less; completely submerged under running water at 21°C (70°F) or below (with time limits); as part of cooking; or in a microwave and immediately moved to conventional cooking.

**Expected source:** food_code_2026 3-501.13

**Agent's answer:**

Frozen chicken may be thawed under refrigeration that maintains a temperature of 5°C (41°F) or less [Food Code 2026 §3-501.13]. 

It can also be thawed completely submerged under running water at a water temperature of 21°C (70°F) or below, with sufficient water velocity to agitate and float off loose particles, provided the temperature of the raw animal food does not rise above 5°C (41°F) for more than four hours [Food Code 2026 §3-501.13]. 

Additionally, it may be thawed as part of a cooking process or by thawing in a microwave oven and immediately transferring it to conventional cooking equipment with no interruption [Food Code 2026 §3-501.13].

**Passages the answer cites:**

> **[Food Code 2026 §3-501.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.13 (p. 70). Thawing
> Except as specified in ¶ (D) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be thawed: (A) Under refrigeration that maintains the FOOD temperature at 5°C (41°F) or less; or (B) Completely submerged under running water: (1) At a water temperature of 21°C (70°F) or below, (2) With sufficient water velocity to agitate and float off loose particles in an overflow, and (3) For a period that does not allow thawed portions of READY-TO-EAT FOOD to rise above 5°C (41°F), or (4) For a period that does not allow thawed portions of a raw animal FOOD requiring cooking as specified under ¶ 3-401.11(A) or (B) to be above 5°C (41°F), for more than four hours including: (a) The time the FOOD is exposed to the running water and the time needed for preparation for cooking, or (b) The time it takes under refrigeration to lower the FOOD temperature to 5°C (41°F); (C) As part of a cooking process if the FOOD that is frozen is: (1) Cooked as specified under ¶¶ 3-401.11(A) or (B), § 3-401.12, or § 3-401.15, or (2) Thawed in a microwave oven and immediately transferred to conventional cooking EQUIPMENT, with no interruption in the process; or (D) Using any procedure if a portion of frozen READY-TO-EAT FOOD is thawed and prepared for immediate service in response to an individual CONSUMER's order. (E) REDUCED OXYGEN PACKAGED FISH that bears a label indicating that it is to be kept frozen until time of use shall be removed from the reduced oxygen environment: (1) Prior to its thawing under refrigeration as specified in ¶ (A) of this section; PF or (2) Prior to, or Immediately upon completion of, its thawing using procedures specified in ¶ (B) of this section.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-501.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.12 (pp. 69-70). Time/Temperature Control for Safety Food, Slacking
> Frozen TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is SLACKED to moderate the temperature shall be held: (A) Under refrigeration that maintains the FOOD temperature at 5°C (41°F) or less; or (B) At any temperature if the FOOD remains frozen.

> **[Food Code 2026 §3-401.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.12 (pp. 65-66). Microwave Cooking
> Raw animal FOODS cooked in a microwave oven shall be: (A) Rotated or stirred throughout or midway during cooking to compensate for uneven distribution of heat; (B) Covered to retain surface moisture; (C) Heated to a temperature of at least 74°C (165°F) in all parts of the FOOD; and (D) Allowed to stand covered for two minutes after cooking to obtain temperature equilibrium.

> **[Food Code 2026 §3-402.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-402.11 (p. 67). Parasite Destruction
> (A) Except as specified in ¶ (B) of this section, before service or sale in READY-TO-EAT form, raw, raw-marinated, partially cooked, or marinated-partially cooked FISH shall be: (1) Frozen and stored at a temperature of -20°C (-4°F) or below for a minimum of 168 hours (7 days) in a freezer; (2) Frozen at -35°C (-31°F) or below until solid and stored at -35°C (-31°F) or below for a minimum of 15 hours; or (3) Frozen at -35°C (-31°F) or below until solid and stored at -20°C (-4°F) or below for a minimum of 24 hours. (B) Paragraph (A) of this section does not apply to: (1) MOLLUSCAN SHELLFISH; (2) A scallop product consisting only of the shucked adductor muscle; (3) Tuna of the species Thunnus alalunga, Thunnus albacores (Yellowfin tuna), Thunnus atlanticus, Thunnus maccoyii (Bluefin tuna, Southern), Thunnus obesus (Bigeye tuna), or Thunnus thynnus (Bluefin tuna, Northern); or (4) Aquacultured FISH, such as salmon, that: (a) If raised in open water, are raised in net-pens, or (b) Are raised in land-based operations such as ponds or tanks, and (c) Are fed formulated feed, such as pellets, that contains no live parasites infective to the aquacultured FISH. (5) FISH eggs that have been removed from the skein and rinsed.

> **[Food Code 2026 §3-303.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-303.12 (p. 57). Storage or Display of Food in Contact with Water or Ice
> (A) PACKAGED FOOD may not be stored in direct contact with ice or water if the FOOD is subject to the entry of water because of the nature of its packaging, wrapping, or container or its positioning in the ice or water. (B) Except as specified in ¶¶ (C) and (D) of this section, unPACKAGED FOOD may not be stored in direct contact with undrained ice. (C) Whole, raw fruits or vegetables; cut, raw vegetables such as celery or carrot sticks or cut potatoes; and tofu may be immersed in ice or water. (D) Raw POULTRY and raw FISH that are received immersed in ice in shipping containers may remain in that condition while in storage awaiting preparation, display, service, or sale.

</details>


---

## q12 (single)

**Question:** Which ingredients count as major food allergens?

**Reference answer:** Milk, egg, fish, crustacean shellfish, tree nuts, wheat, peanuts, soybeans and sesame, and food ingredients containing protein from them (not highly refined oils made from them).

**Expected source:** food_code_2026 1-201.10

**Agent's answer:**

Major food allergens include milk, egg, fish (such as bass, flounder, or cod), crustacean shellfish (such as crab, lobster, or shrimp), tree nuts (such as almonds, pecans, or walnuts), wheat, peanuts, soybeans, and sesame [Food Code 2026 §1-201.10]. They also include any food ingredient that contains protein derived from one of these foods [Food Code 2026 §1-201.10]. Highly refined oils derived from these foods and ingredients derived from such oils are excluded [Food Code 2026 §1-201.10].

**Passages the answer cites:**

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 10-11). Statement of Application and Listing of Terms (part 12)
> (1) "Juice" means the aqueous liquid expressed or extracted from one or more fruits or vegetables, purées of the edible portions of one or more fruits or vegetables, or any concentrates of such liquid or purée. (2) "Juice" does not include, for purposes of HACCP, liquids, purées, or concentrates that are not used as BEVERAGES or ingredients of BEVERAGES. "Kitchenware" means FOOD preparation and storage UTENSILS. "Law" means applicable local, state, and federal statutes, regulations, and ordinances. "Linens" means fabric items such as cloth hampers, cloth napkins, tablecloths, wiping cloths, and work garments including cloth gloves. Major Food Allergen. (1) "Major food allergen" means: (a) Milk, EGG, FISH (such as bass, flounder, cod, and including crustacean shellfish such as crab, lobster, or shrimp), tree nuts (such as almonds, pecans, or walnuts), wheat, peanuts, soybeans, and sesame; or (b) A FOOD ingredient that contains protein derived from a FOOD, as specified in Subparagraph (1)(a) of this definition. (2) "Major food allergen" does not include: (a) Any highly refined oil derived from a FOOD specified in Subparagraph (1)(a) of this definition and any ingredient derived from such highly refined oil; or (b) Any ingredient that is exempt under the petition or notification process specified in the Food Allergen Labeling and Consumer Protection Act of 2004 (Public Law 108-282). "Meat" means the flesh of animals used as FOOD including the dressed flesh of cattle, swine, sheep, or goats and other edible animals, except FISH, POULTRY, and wild GAME ANIMALS as specified under Subparagraphs 3-201.17(A)(3) and (4). "Mechanically Tenderized" means manipulating MEAT by piercing with a set of needles, pins, blades or any mechanical device, which breaks up muscle fiber and tough connective tissue, to increase tenderness. This includes INJECTION, scoring, and processes which may be referred to as “blade tenderizing,”

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-602.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.11 (pp. 80-81). Food Labels (part 1)
> (A) FOOD PACKAGED in a FOOD ESTABLISHMENT, shall be labeled as specified in LAW, including 21 CFR 101 - Food labeling, and 9 CFR 317 Labeling, marking devices, and containers. (B) Label information shall include: (1) The common name of the FOOD, or absent a common name, an adequately descriptive identity statement; (2) If made from two or more ingredients, a list of ingredients and sub-ingredients in descending order of predominance by weight, including a declaration of artificial colors, artificial flavors and chemical preservatives, if contained in the FOOD; (3) An accurate declaration of the net quantity of contents; (4) The name and place of business of the manufacturer, packer, or distributor; and (5) The name of the FOOD source for each MAJOR FOOD ALLERGEN contained in the FOOD unless the FOOD source is already part of the common or usual name of the respective ingredient. (6) Except as exempted in the Federal Food, Drug, and Cosmetic Act § 403(q)(3) - (5), nutrition labeling as specified in 21 CFR 101 - Food Labeling and 9 CFR 317 Subpart B Nutrition Labeling. (7) For any salmonid containing canthaxanthin or astaxanthin as a COLOR ADDITIVE, the labeling of the bulk FISH container, including a list of ingredients, displayed on the retail container or by other written means, such as a counter card, that discloses the use of canthaxanthin or astaxanthin. (C) Bulk FOOD that is available for CONSUMER self-dispensing shall be prominently labeled with the following information in plain view of the CONSUMER: (1) The manufacturer's or processor's label that was provided with the FOOD; or (2) A card, sign, or other method of notification that includes the information specified under Subparagraphs (B)(1), (2), (5), and (6) of this section.

> **[Food Code 2026 §3-602.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.12 (pp. 81-82). Other Forms of Information
> (A) If required by LAW, CONSUMER warnings shall be provided. (B) FOOD ESTABLISHMENT or manufacturers' dating information on FOODS may not be concealed or altered. (C) The PERMIT HOLDER shall notify CONSUMERS by written notification of the presence of MAJOR FOOD ALLERGENS as an ingredient in unPACKAGED FOOD items that are served or sold to the CONSUMER.

> **[Food Code 2026 §3-302.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-302.13 (p. 56). Pasteurized Eggs, Substitute for Raw Eggs for Certain Recipes
> Pasteurized EGGS or EGG PRODUCTS shall be substituted for raw EGGS in the preparation of FOODS such as Caesar salad, hollandaise or Béarnaise sauce, mayonnaise, meringue, eggnog, ice cream, and EGG-fortified BEVERAGES that are not: (A) Cooked as specified under Subparagraphs 3-401.11(A)(1) or (2); or (B) Included in ¶ 3-401.11(D).

> **[Food Code 2026 §3-202.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-202.12 (p. 49). Additives
> FOOD may not contain unAPPROVED FOOD ADDITIVES or ADDITIVES that exceed amounts specified in 21 CFR 170-180 relating to FOOD ADDITIVES, generally recognized as safe or prior sanctioned substances that exceed amounts specified in 21 CFR 181-186, substances that exceed amounts specified in 9 CFR Subpart C Section 424.21(b) FOOD ingredients and sources of radiation, or pesticide residues that exceed provisions specified in 40 CFR 180 Tolerances for pesticides chemicals in FOOD, and exceptions.

</details>


---

## q13 (single)

**Question:** We serve burgers cooked to order, including rare. Do we have to warn customers?

**Reference answer:** Yes, with a consumer advisory: a disclosure (describe the item or asterisk it to a footnote) and a reminder footnote such as 'Consuming raw or undercooked meats, poultry, seafood, shellfish, or eggs may increase your risk of foodborne illness', on the menu, placards, labels or other written means.

**Expected source:** food_code_2026 3-603.11

**Agent's answer:**

Yes. If an animal food such as beef is served raw, undercooked, or without being processed to eliminate pathogens, the permit holder must inform consumers of the significantly increased risk by way of a disclosure and a reminder using brochures, menu advisories, table tents, placards, or other effective written means [Food Code 2026 §3-603.11]. 

The disclosure must either describe the animal-derived foods (such as "hamburgers (can be cooked to order)") or use an asterisk linking them to a footnote stating the items are served raw or undercooked [Food Code 2026 §3-603.11]. 

The reminder must use an asterisk linking the items to a footnote stating that consuming raw or undercooked meats may increase your risk of foodborne illness, or that it may increase your risk especially if you have certain medical conditions, or stating that written information is available upon request [Food Code 2026 §3-603.11]. 

Additionally, if the burgers contain comminuted (ground) meat, they cannot be offered on a children's menu if served undercooked [Food Code 2026 §3-401.11]. 

The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §3-603.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-603.11 (p. 82). Consumption of Animal Foods that are Raw, Undercooked, or Not Otherwise Processed to Eliminate Pathogens
> (A) Except as specified in ¶ 3-401.11(C) and Subparagraph 3-401.11(D)(4) and under ¶ 3-801.11(C), if an animal FOOD such as beef, EGGS, FISH, lamb, milk, pork, POULTRY, or shellfish is served or sold raw, undercooked, or without otherwise being processed to eliminate pathogens, either in READY-TO-EAT form or as an ingredient in another READY-TO-EAT FOOD, the PERMIT HOLDER shall inform CONSUMERS of the significantly increased RISK of consuming such FOODS by way of a DISCLOSURE and REMINDER, as specified in ¶¶ (B) and (C) of this section using brochures, deli case or menu advisories, label statements, table tents, placards, or other effective written means. (B) DISCLOSURE shall include: (1) A description of the animal-derived FOODS, such as “oysters on the half shell (raw oysters) ,” “raw-EGG Caesar salad,” and “hamburgers (can be cooked to order)”; or (2) Identification of the animal-derived FOODS by asterisking them to a footnote that states that the items are served raw or undercooked, or contain (or may contain) raw or undercooked ingredients. (C) REMINDER shall include asterisking the animal-derived FOODS requiring DISCLOSURE to a footnote that states: (1) Regarding the safety of these items, written information is available upon request; (2) Consuming raw or undercooked MEATS, POULTRY, seafood, shellfish, or EGGS may increase your RISK of foodborne illness; or (3) Consuming raw or undercooked MEATS, POULTRY, seafood, shellfish, or EGGS may increase your RISK of foodborne illness, especially if you have certain medical conditions.

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (p. 65). Raw Animal Foods (part 3)
> (D) A raw animal FOOD such as raw EGG, raw FISH, raw-marinated FISH, raw MOLLUSCAN SHELLFISH, or steak tartare; or a partially cooked FOOD such as lightly cooked FISH, soft cooked EGGS, or rare MEAT other than WHOLE-MUSCLE, INTACT BEEF steaks as specified in ¶ (C) of this section, may be served or offered for sale upon CONSUMER request or selection in a READY-TO-EAT form if: (1) As specified under Subparagraphs 3-801.11(C)(1) and (2), the FOOD ESTABLISHMENT serves a population that is not a HIGHLY SUSCEPTIBLE POPULATION; (2) The FOOD, if served or offered for service by CONSUMER selection from a children’s menu, does not contain COMMINUTED MEAT; and (3) The CONSUMER is informed as specified under § 3-603.11 that to ensure its safety, the FOOD should be cooked as specified under ¶ (A) or (B) of this section; or (4) The REGULATORY AUTHORITY grants a VARIANCE from ¶ (A) or (B) of this section as specified in § 8-103.10 based on a HACCP PLAN that: (a) Is submitted by the PERMIT HOLDER and APPROVED as specified under § 8-103.11, (b) Documents scientific data or other information showing that a lesser time and temperature regimen results in a safe FOOD, and (c) Verifies that EQUIPMENT and procedures for FOOD preparation and training of FOOD EMPLOYEES at the FOOD ESTABLISHMENT meet the conditions of the VARIANCE.

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (pp. 63-65). Raw Animal Foods (part 2)
> (1) As specified in the following chart, to heat all parts of the FOOD to a temperature and for the holding time that corresponds to that temperature: and Temperature °C (°F) Time1 in Minutes 54.4 (130) 112 55.0 (131) 89 56.1 (133) 56 57.2 (135) 36 57.8 (136) 28 58.9 (138) 18 60.0 (140) 12 61.1 (142) 8 62.2 (144) 5 62.8 (145) 4 63.9 (147) 134 65.0 (149) 85 66.1 (151) 54 67.2 (153) 34 68.3 (155) 22 69.4 (157) 14 70.0 (158) 0 1 Holding time may include post-oven heat rise. (2) If cooked in an oven, use an oven that is preheated to the temperature specified for the roast's weight in the following chart and that is held at that temperature: Oven Temperature Based on Roast Weight Oven Type Less than 4.5 kg (10 lbs.) 4.5 kg (10 lbs.) or More Still Dry 177°C (350°F) or more 121°C (250°F) or more Convection 163°C (325°F) or more 121°C (250°F) or more High Humidity 1 121°C (250°F) or less 121°C (250°F) or less 1 Relative humidity greater than 90% for at least 1 hour as measured in the cooking chamber or exit of the oven; or in a moisture-impermeable bag that provides 100% humidity. (C) A raw or undercooked WHOLE-MUSCLE, INTACT BEEF steak may be served or offered for sale in a READY-TO-EAT form if: (1) The FOOD ESTABLISHMENT serves a population that is not a HIGHLY SUSCEPTIBLE POPULATION, (2) The steak is prepared so that it remains intact, and (3) The steak is cooked on both the top and bottom to a surface temperature of 63°C (145°F) or above and a cooked color change is achieved on all external surfaces.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-602.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.12 (pp. 81-82). Other Forms of Information
> (A) If required by LAW, CONSUMER warnings shall be provided. (B) FOOD ESTABLISHMENT or manufacturers' dating information on FOODS may not be concealed or altered. (C) The PERMIT HOLDER shall notify CONSUMERS by written notification of the presence of MAJOR FOOD ALLERGENS as an ingredient in unPACKAGED FOOD items that are served or sold to the CONSUMER.

> **[Food Code 2026 §3-306.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-306.13 (p. 62). Consumer Self-Service Operations
> (A) Raw, unPACKAGED animal FOOD, such as beef, lamb, pork, POULTRY, and FISH may not be offered for CONSUMER self-service. This paragraph does not apply to: (1) CONSUMER self-service of READY-TO-EAT FOODS at buffets or salad bars that serve FOODS such as sushi or raw shellfish; (2) Ready-to-cook individual portions for immediate cooking and consumption on the PREMISES such as CONSUMER-cooked MEATS or CONSUMER-selected ingredients for Mongolian barbecue; or (3) RAW, frozen, shell-on shrimp, or lobster. (B) CONSUMER self-service operations for READY-TO-EAT FOODS shall be provided with suitable UTENSILS or effective dispensing methods that protect the FOOD from contamination. (C) CONSUMER self-service operations such as buffets and salad bar shall be monitored by FOOD EMPLOYEES trained in safe operating procedures.

</details>


---

## q14 (single)

**Question:** We package grab-and-go salads to sell. What has to be on the label?

**Reference answer:** The common name; the ingredients in descending order by weight (including artificial colors, flavors and chemical preservatives); net quantity; name and place of business of the manufacturer, packer or distributor; the food source of each major food allergen; and nutrition labeling unless exempt.

**Expected source:** food_code_2026 3-602.11

**Agent's answer:**

Food packaged in a food establishment must be labeled as specified in law, including:
* The common name of the food, or an adequately descriptive identity statement [Food Code 2026 §3-602.11].
* A list of ingredients and sub-ingredients in descending order of predominance by weight, including artificial colors, flavors, and chemical preservatives, if the food is made from two or more ingredients [Food Code 2026 §3-602.11].
* An accurate declaration of the net quantity of contents [Food Code 2026 §3-602.11].
* The name and place of business of the manufacturer, packer, or distributor [Food Code 2026 §3-602.11].
* The name of the food source for each major food allergen contained in the food, unless already part of the ingredient's common name [Food Code 2026 §3-602.11].
* Nutrition labeling, except as exempted in the Federal Food, Drug, and Cosmetic Act [Food Code 2026 §3-602.11].

**Passages the answer cites:**

> **[Food Code 2026 §3-602.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.11 (pp. 80-81). Food Labels (part 1)
> (A) FOOD PACKAGED in a FOOD ESTABLISHMENT, shall be labeled as specified in LAW, including 21 CFR 101 - Food labeling, and 9 CFR 317 Labeling, marking devices, and containers. (B) Label information shall include: (1) The common name of the FOOD, or absent a common name, an adequately descriptive identity statement; (2) If made from two or more ingredients, a list of ingredients and sub-ingredients in descending order of predominance by weight, including a declaration of artificial colors, artificial flavors and chemical preservatives, if contained in the FOOD; (3) An accurate declaration of the net quantity of contents; (4) The name and place of business of the manufacturer, packer, or distributor; and (5) The name of the FOOD source for each MAJOR FOOD ALLERGEN contained in the FOOD unless the FOOD source is already part of the common or usual name of the respective ingredient. (6) Except as exempted in the Federal Food, Drug, and Cosmetic Act § 403(q)(3) - (5), nutrition labeling as specified in 21 CFR 101 - Food Labeling and 9 CFR 317 Subpart B Nutrition Labeling. (7) For any salmonid containing canthaxanthin or astaxanthin as a COLOR ADDITIVE, the labeling of the bulk FISH container, including a list of ingredients, displayed on the retail container or by other written means, such as a counter card, that discloses the use of canthaxanthin or astaxanthin. (C) Bulk FOOD that is available for CONSUMER self-dispensing shall be prominently labeled with the following information in plain view of the CONSUMER: (1) The manufacturer's or processor's label that was provided with the FOOD; or (2) A card, sign, or other method of notification that includes the information specified under Subparagraphs (B)(1), (2), (5), and (6) of this section.

> **[Food Code 2026 §3-602.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.11 (p. 81). Food Labels (part 2)
> (D) Bulk, unPACKAGED FOODS such as bakery products and unPACKAGED FOODS that are portioned to CONSUMER specification need not be labeled if: . (1) A health, nutrient content, or other claim is not made; (2) There are no state or local LAWS requiring labeling; and (3) The FOOD is manufactured or prepared on the PREMISES of the FOOD ESTABLISHMENT or at another FOOD ESTABLISHMENT or a FOOD PROCESSING PLANT that is owned by the same PERSON and is regulated by the FOOD regulatory agency that has jurisdiction.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-302.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-302.12 (p. 56). Food Storage Containers, Identified with Common Name of Food
> Except for containers holding FOOD that can be readily and unmistakably recognized such as dry pasta, working containers holding FOOD or FOOD ingredients that are removed from their original packages for use in the FOOD ESTABLISHMENT, such as cooking oils, flour, herbs, potato flakes, salt, spices, and sugar shall be identified with the common name of the FOOD.

> **[Food Code 2026 §3-201.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-201.11 (p. 46). Compliance with Food Law (part 2)
> (F) MEAT and POULTRY that is not a READY-TO-EAT FOOD and is in a PACKAGED form when it is offered for sale or otherwise offered for consumption, shall be labeled to include safe handling instructions as specified in LAW, including 9 CFR 317.2(l) and 9 CFR 381.125(b). (G) EGGS that have not been specifically treated to destroy all viable Salmonellae shall be labeled to include safe handling instructions as specified in LAW, including 21 CFR 101.17(h).

> **[Food Code 2026 §3-601.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-601.11 (p. 80). Standards of Identity
> PACKAGED FOOD shall comply with standard of identity requirements in 21 CFR 131-169 and 9 CFR 319 Definitions and standards of identity or composition, and the general requirements in 21 CFR 130 – Food Standards: General and 9 CFR 319 Subpart A – General.

</details>


---

## q15 (single)

**Question:** Does our manager on duty need a food safety certification?

**Reference answer:** Yes. The person in charge must be a certified food protection manager who passed a test from an accredited program, unless the regulatory authority considers the establishment minimal risk.

**Expected source:** food_code_2026 2-102.12

**Agent's answer:**

Yes, the person in charge must be a certified food protection manager who has shown proficiency through passing a test that is part of an accredited program, unless the regulatory authority deems that your establishment poses a minimal risk of causing foodborne illness based on its operation and food preparation [Food Code 2026 §2-102.12]. 

The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §2-102.12]** Source: FDA Food Code 2026, Chapters 1-6, §2-102.12 (pp. 25-26). Certified Food Protection Manager
> (A) The PERSON IN CHARGE shall be a certified FOOD protection manager who has shown proficiency of required information through passing a test that is part of an ACCREDITED PROGRAM. (B) This section does not apply to certain types of FOOD ESTABLISHMENTS deemed by the REGULATORY AUTHORITY to pose minimal RISK of causing, or contributing to, foodborne illness based on the nature of the operation and extent of FOOD preparation.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §2-102.20]** Source: FDA Food Code 2026, Chapters 1-6, §2-102.20 (p. 26). Food Protection Manager Certification
> (A) A PERSON IN CHARGE who demonstrates knowledge by being a FOOD protection manager that is certified by a FOOD protection manager certification program that is evaluated and listed by a Conference for FOOD Protection-recognized accrediting agency as conforming to the Conference for Food Protection Standard for Accreditation of Food Protection Manager Certification Programs is deemed to comply with ¶ 2-102.11(B). (B) A FOOD ESTABLISHMENT that has a PERSON IN CHARGE that is certified by a FOOD protection manager certification program that is evaluated and listed by a Conference for Food Protection-recognized accrediting agency as conforming to the Conference for Food Protection Standard for Accreditation of Food Protection Manager Certification Programs is deemed to comply with § 2-102.12.

> **[Food Code 2026 §2-103.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-103.11 (pp. 26-27). Person in Charge (part 1)
> The PERSON IN CHARGE shall maintain ACTIVE MANAGERIAL CONTROL of foodborne illness RISK factors by ensuring that: (A) FOOD ESTABLISHMENT operations are not conducted in a private home or in a room used as living or sleeping quarters as specified under § 6-202.111; (B) PERSONS unnecessary to the FOOD ESTABLISHMENT operation are not allowed in the FOOD preparation, FOOD storage, or WAREWASHING areas, except that brief visits and tours may be authorized by the PERSON IN CHARGE if steps are taken to ensure that exposed FOOD; clean EQUIPMENT, UTENSILS, and LINENS; and unwrapped SINGLE-SERVICE and SINGLE-USE ARTICLES are protected from contamination; (C) EMPLOYEES and other PERSONS such as delivery and maintenance PERSONS and pesticide applicators entering the FOOD preparation, FOOD storage, and WAREWASHING areas comply with this Code; (D) EMPLOYEES are effectively cleaning their hands, by routinely monitoring the EMPLOYEES' handwashing; (E) EMPLOYEES are visibly observing FOODS as they are received to determine that they are from APPROVED sources, delivered at the required temperatures, protected from contamination, unADULTERATED, and accurately presented, by routinely monitoring the EMPLOYEES’ observations and periodically evaluating FOODS upon their receipt; (F) EMPLOYEES are verifying that FOODS delivered to the FOOD ESTABLISHMENT during non-operating hours are from APPROVED sources and are placed into appropriate storage locations such that they are maintained at the required temperatures, protected from contamination, unADULTERATED, and accurately presented; (G) EMPLOYEES are properly cooking TIME/TEMPERATURE CONTROL FOR SAFETY FOOD, being particularly careful in cooking those FOODS known to cause severe foodborne illness and death, such as EGGS and COMMINUTED MEATS, through daily oversight of the EMPLOYEES' routine monitoring of the cooking temperatures using appropriate TEMPERATURE MEASURING DEVICES properly scaled and calibrated as specified under § 4-203.11 and ¶ 4-502.11(B);

> **[Food Code 2026 §2-101.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-101.11 (p. 23). Assignment
> (A) Except as specified in ¶¶ (B) and (C) of this section, the PERMIT HOLDER shall be the PERSON IN CHARGE or shall designate a PERSON IN CHARGE and shall ensure that a PERSON IN CHARGE is present at the FOOD ESTABLISHMENT during all hours of operation. (B) In a FOOD ESTABLISHMENT with two or more separately PERMITTED departments that are the legal responsibility of the same PERMIT HOLDER and that are located on the same PREMISES, the PERMIT HOLDER may, during specific time periods when FOOD is not being prepared, PACKAGED, or served, designate a single PERSON IN CHARGE who is present on the PREMISES during all hours of operation, and who is responsible for each separately PERMITTED FOOD ESTABLISHMENT on the PREMISES. (C) This section does not apply to certain types of FOOD ESTABLISHMENTs deemed by the REGULATORY AUTHORITY to pose minimal RISK of causing, or contributing to, foodborne illness based on the nature of the operation and extent of the FOOD preparation.

> **[Food Code 2026 §2-102.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-102.11 (pp. 23-24). Demonstration (part 1)
> Based on the RISKS inherent to the FOOD operation, during inspections and upon request the PERSON IN CHARGE shall demonstrate to the REGULATORY AUTHORITY knowledge of foodborne disease prevention, application of the HAZARD analysis and CRITICAL CONTROL POINT principles, and the requirements of this Code. The PERSON IN CHARGE shall demonstrate this knowledge by: (A) Complying with this Code by having no violations of PRIORITY ITEMS during the current inspection; (B) Being a certified FOOD protection manager who has shown proficiency of required information through passing a test that is part of an ACCREDITED PROGRAM; or (C) Responding correctly to the inspector's questions as they relate to the specific FOOD operation. The areas of knowledge include: (1) Describing the relationship between the prevention of foodborne disease and the personal hygiene of a FOOD EMPLOYEE; (2) Explaining the responsibility of the PERSON IN CHARGE for preventing the transmission of foodborne disease by a FOOD EMPLOYEE who has a disease or medical condition that may cause foodborne disease; (3) Describing the symptoms associated with the diseases that are transmissible through FOOD; (4) Explaining the significance of the relationship between maintaining the time and temperature of TIME/TEMPERATURE CONTROL FOR SAFETY FOOD and the prevention of foodborne illness; (5) Explaining the HAZARDS involved in the consumption of raw or undercooked MEAT, POULTRY, EGGS, and FISH; (6) Stating the required FOOD temperatures and times for safe cooking of TIME/TEMPERATURE CONTROL FOR SAFETY FOOD including MEAT, POULTRY, EGGS, and FISH; (7) Stating the required temperatures and times for the safe refrigerated storage, hot holding, cooling, and reheating of TIME/TEMPERATURE CONTROL FOR SAFETY FOOD;

</details>


---

## q16 (single)

**Question:** Can the owner's dog stay in the kitchen while we prep food?

**Reference answer:** No. Live animals may not be allowed on the premises of a food establishment; the exceptions (such as service animals in customer areas not used for food preparation) do not cover a pet in the kitchen.

**Expected source:** food_code_2026 6-501.115

**Agent's answer:**

No, live animals may not be allowed on the premises of a food establishment, except for specific situations like patrol dogs, service animals in customer areas, or fish in aquariums [Food Code 2026 §6-501.115]. The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §6-501.115]** Source: FDA Food Code 2026, Chapters 1-6, §6-501.115 (p. 143). Prohibiting Animals (part 2)
> (C) Live or dead FISH bait may be stored if contamination of FOOD; clean EQUIPMENT, UTENSILS, and LINENS; and unwrapped SINGLE-SERVICE AND SINGLE-USE ARTICLES cannot result. (D) If APPROVED by the REGULATORY AUTHORITY, FOOD ESTABLISHMENTS may allow pet dogs in outdoor dining areas

> **[Food Code 2026 §6-501.115]** Source: FDA Food Code 2026, Chapters 1-6, §6-501.115 (pp. 142-143). Prohibiting Animals (part 1)
> (A) Except as specified in ¶¶ (B), (C) and (D) of this section, live animals may not be allowed on the PREMISES of a FOOD ESTABLISHMENT. (B) Live animals may be allowed in the following situations if the contamination of FOOD; clean EQUIPMENT, UTENSILS, and LINENS; and unwrapped SINGLE-SERVICE and SINGLE-USE ARTICLES cannot result: (1) Edible FISH or decorative FISH in aquariums, shellfish or crustacea on ice or under refrigeration, and shellfish and crustacea in display tank systems; (2) Patrol dogs accompanying police or security officers in offices and dining, sales, and storage areas, and sentry dogs running loose in outside fenced areas; (3) In areas that are not used for FOOD preparation and that are usually open for customers, such as dining and sales areas, SERVICE ANIMALS that are controlled by the disabled EMPLOYEE or PERSON, if a health or safety HAZARD will not result from the presence or activities of the SERVICE ANIMAL; (4) Pets in the common dining areas of institutional care facilities such as nursing homes, assisted living facilities, group homes, or residential care facilities at times other than during meals if: (a) Effective partitioning and self-closing doors separate the common dining areas from FOOD storage or FOOD preparation areas, (b) Condiments, EQUIPMENT, and UTENSILS are stored in enclosed cabinets or removed from the common dining areas when pets are present, and (c) Dining areas including tables, countertops, and similar surfaces are effectively cleaned before the next meal service; and (5) In areas that are not used for FOOD preparation, storage, sales, display, or dining, in which there are caged animals or animals that are similarly confined, such as in a variety store that sells pets or a tourist park that displays animals.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §2-403.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-403.11 (p. 43). Handling Prohibition
> (A) Except as specified in ¶ (B) of this section, FOOD EMPLOYEES may not care for or handle animals that may be present such as patrol dogs, SERVICE ANIMALS, or pets that are allowed as specified in Subparagraphs 6-501.115(B)(2) - (5) and (D). (B) FOOD EMPLOYEES with SERVICE ANIMALS may handle or care for their SERVICE ANIMALS and FOOD EMPLOYEES may handle or care for FISH in aquariums or MOLLUSCAN SHELLFISH or crustacea in display tanks if they wash their hands as specified under § 2-301.12 and ¶ 2-301.14(C).

> **[Food Code 2026 §2-303.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-303.11 (p. 42). Prohibition
> (A) Except as specified in ¶¶ (B) and (C) of this section, FOOD EMPLOYEES may not wear jewelry on their arms and hands while preparing FOOD. (B) A plain ring, such as a wedding band, may be worn. (C) An individual with a disability covered under the Americans with Disabilities Act may be allowed to wear a medically necessary device that can be kept clean and worn in a manner that prevents potential contamination.

> **[Food Code 2026 §3-304.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-304.12 (pp. 57-58). In-Use Utensils, Between-Use Storage
> During pauses in FOOD preparation or dispensing, FOOD preparation and dispensing UTENSILS shall be stored: (A) Except as specified under ¶ (B) of this section, in the FOOD with their handles above the top of the FOOD and the container; (B) In FOOD that is not TIME/TEMPERATURE CONTROL FOR SAFETY FOOD with their handles above the top of the FOOD within containers or EQUIPMENT that can be closed, such as bins of sugar, flour, or cinnamon; (C) On a clean portion of the FOOD preparation table or cooking EQUIPMENT only if the in-use UTENSIL and the FOOD-CONTACT SURFACE of the FOOD preparation table or cooking EQUIPMENT are cleaned and SANITIZED at a frequency specified under §§ 4-602.11 and 4-702.11; (D) In running water of sufficient velocity to flush particulates to the drain, if used with moist FOOD such as ice cream or mashed potatoes; (E) In a clean, protected location if the UTENSILS, such as ice scoops, are used only with a FOOD that is not TIME/TEMPERATURE CONTROL FOR SAFETY FOOD; or (F) In a container of water if the water is maintained at a temperature of at least 57°C (135°F) and the container is cleaned at a frequency specified under Subparagraph 4-602.11(D)(7).

</details>


---

## q17 (single)

**Question:** How accurate do our food thermometers have to be?

**Reference answer:** Accurate to ±1°C if scaled in Celsius or in both Celsius and Fahrenheit, or to ±2°F if scaled only in Fahrenheit.

**Expected source:** food_code_2026 4-203.11

**Agent's answer:**

Food temperature measuring devices scaled only in Celsius or dually scaled in Celsius and Fahrenheit must be accurate to ±1°C in the intended range of use [Food Code 2026 §4-203.11]. Food temperature measuring devices scaled only in Fahrenheit must be accurate to ±2°F in the intended range of use [Food Code 2026 §4-203.11].

**Passages the answer cites:**

> **[Food Code 2026 §4-203.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-203.11 (p. 91). Temperature Measuring Devices, Food
> (A) FOOD TEMPERATURE MEASURING DEVICES that are scaled only in Celsius or dually scaled in Celsius and Fahrenheit shall be accurate to ±1°C in the intended range of use. (B) FOOD TEMPERATURE MEASURING DEVICES that are scaled only in Fahrenheit shall be accurate to ±2°F in the intended range of use.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §4-203.12]** Source: FDA Food Code 2026, Chapters 1-6, §4-203.12 (p. 91). Temperature Measuring Devices, Ambient Air and Water
> (A) Ambient air and water TEMPERATURE MEASURING DEVICES that are scaled in Celsius or dually scaled in Celsius and Fahrenheit shall be designed to be easily readable and accurate to ±1.5°C in the intended range of use. (B) Ambient air and water TEMPERATURE MEASURING DEVICES that are scaled only in Fahrenheit shall be accurate to ±3°F in the intended range of use.

> **[Food Code 2026 §4-201.12]** Source: FDA Food Code 2026, Chapters 1-6, §4-201.12 (p. 90). Food Temperature Measuring Devices
> FOOD TEMPERATURE MEASURING DEVICES may not have sensors or stems constructed of glass, except that thermometers with glass sensors or stems that are encased in a shatterproof coating such as candy thermometers may be used.

> **[Food Code 2026 §4-302.12]** Source: FDA Food Code 2026, Chapters 1-6, §4-302.12 (p. 100). Food Temperature Measuring Devices
> (A) FOOD TEMPERATURE MEASURING DEVICES shall be provided and readily accessible for use in ensuring attainment and maintenance of FOOD temperatures as specified under Chapter 3. (B) A TEMPERATURE MEASURING DEVICE with a suitable small-diameter probe that is designed to measure the temperature of thin masses shall be provided and readily accessible to accurately measure the temperature in thin FOODS such as MEAT patties and FISH filets.

> **[Food Code 2026 §4-204.112]** Source: FDA Food Code 2026, Chapters 1-6, §4-204.112 (p. 95). Temperature Measuring Devices
> (A) In a mechanically refrigerated or hot FOOD storage unit, the sensor of a TEMPERATURE MEASURING DEVICE shall be located to measure the air temperature or a simulated product temperature in the warmest part of a mechanically refrigerated unit and in the coolest part of a hot FOOD storage unit. (B) Except as specified in ¶ (C) of this section, cold or hot holding EQUIPMENT used for TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be designed to include and shall be equipped with at least one integral or permanently affixed TEMPERATURE MEASURING DEVICE that is located to allow easy viewing of the device's temperature display. (C) Paragraph (B) of this section does not apply to EQUIPMENT for which the placement of a TEMPERATURE MEASURING DEVICE is not a practical means for measuring the ambient air surrounding the FOOD because of the design, type, and use of the EQUIPMENT, such as calrod units, heat lamps, cold plates, bain-maries, steam tables, insulated FOOD transport containers, and salad bars. (D) TEMPERATURE MEASURING DEVICES shall be designed to be easily readable. (E) FOOD TEMPERATURE MEASURING DEVICES and water TEMPERATURE MEASURING DEVICES on WAREWASHING machines shall have a numerical scale, printed record, or digital readout in increments no greater than 1°C or 2°F in the intended range of use.

</details>


---

## q18 (single)

**Question:** When we sanitize pans in the sink with hot water, how long do they need to stay in the water?

**Reference answer:** At least 30 seconds of immersion (hot water manual operations).

**Expected source:** food_code_2026 4-703.11

**Agent's answer:**

When sanitizing in hot water using manual operations, pans must be immersed for at least 30 seconds [Food Code 2026 §4-703.11]. The water temperature must be maintained at 77°C (171°F) or above [Food Code 2026 §4-501.111].

**Passages the answer cites:**

> **[Food Code 2026 §4-501.111]** Source: FDA Food Code 2026, Chapters 1-6, §4-501.111 (p. 104). Manual Warewashing Equipment, Hot Water Sanitization Temperatures
> If immersion in hot water is used for SANITIZING in a manual operation, the temperature of the water shall be maintained at 77°C (171°F) or above.

> **[Food Code 2026 §4-703.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-703.11 (p. 112). Hot Water and Chemical
> After being cleaned, EQUIPMENT FOOD-CONTACT SURFACES and UTENSILS shall be SANITIZED in: (A) Hot water manual operations by immersion for at least 30 seconds and as specified under § 4-501.111; (B) Hot water mechanical operations by being cycled through EQUIPMENT that is set up as specified under §§ 4-501.15, 4-501.112, and 4-501.113 and achieving a UTENSIL surface temperature of 71°C (160°F) as measured by an irreversible registering temperature indicator; or (C) Chemical manual or mechanical operations, including the application of SANITIZING chemicals by immersion, manual swabbing, brushing, or pressure spraying methods, using a solution as specified under § 4-501.114. Contact times shall be consistent with those on EPA-registered label use instructions by providing: (1) Except as specified under Subparagraph (C)(2) of this section, a contact time of at least 10 seconds for a chlorine solution specified under ¶ 4-501.114(A), (2) A contact time of at least seven seconds for a chlorine solution of 50 “MG/L” that has a PH of 10 or less and a temperature of at least 38°C (100°F) or a PH of 8 or less and a temperature of at least 24°C (75°F), (3) A contact time of at least 30 seconds for other chemical SANITIZING solutions, or (4) A contact time used in relationship with a combination of temperature, concentration, and PH that, when evaluated for efficacy, yields SANITIZATION as defined in ¶ 1-201.10(B).

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §4-204.116]** Source: FDA Food Code 2026, Chapters 1-6, §4-204.116 (p. 96). Manual Warewashing Equipment, Heaters and Baskets
> If hot water is used for SANITIZATION in manual WAREWASHING operations, the SANITIZING compartment of the sink shall be: (A) Designed with an integral heating device that can maintain water at a temperature not less than 77°C (171°F); and (B) Provided with a rack or basket to allow complete immersion of EQUIPMENT and UTENSILS into the hot water.

> **[Food Code 2026 §4-501.112]** Source: FDA Food Code 2026, Chapters 1-6, §4-501.112 (p. 104). Mechanical Warewashing Equipment, Hot Water Sanitization Temperatures
> (A) Except as specified in ¶ (B) of this section, in a mechanical operation, the temperature of the fresh hot water SANITIZING rinse as it enters the manifold may not be more than 90°C (194°F), or less than: (1) For a stationary rack, single temperature machine, 74°C (165°F); or (2) For all other machines, 82°C (180°F). (B) The maximum temperature specified under ¶ (A) of this section, does not apply to the high pressure and temperature systems with wand-type, hand-held, spraying devices used for the in-place cleaning and SANITIZING of EQUIPMENT such as MEAT saws.

> **[Food Code 2026 §4-501.110]** Source: FDA Food Code 2026, Chapters 1-6, §4-501.110 (p. 104). Mechanical Warewashing Equipment, Wash Solution Temperature
> (A) The temperature of the wash solution in spray-type warewashers that use hot water to SANITIZE may not be less than: (1) For a stationary rack, single temperature machine, 74°C (165°F); (2) For a stationary rack, dual temperature machine, 66°C (150°F); (3) For a single tank, conveyor, dual temperature machine, 71°C (160°F); or (4) For a multi-tank, conveyor, multitemperature machine, 66°C (150°F). (B) The temperature of the wash solution in spray-type warewashers that use chemicals to SANITIZE may not be less than 49°C (120°F).

</details>


---

## q19 (single)

**Question:** Can a cook use the same gloves to cut raw chicken and then make a salad?

**Reference answer:** No. Single-use gloves are used for only one task, such as working with raw animal food or with ready-to-eat food, and for no other purpose; they are discarded when damaged, soiled or when the work is interrupted.

**Expected source:** food_code_2026 3-304.15

**Agent's answer:**

No, a cook cannot use the same single-use gloves to cut raw chicken and then make a salad [Food Code 2026 §3-304.15]. Single-use gloves must be used for only one task, such as working with raw animal food or with ready-to-eat food, and used for no other purpose [Food Code 2026 §3-304.15]. Gloves must also be discarded if they are damaged, soiled, or contaminated when interruptions occur [Food Code 2026 §3-304.15]. The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §3-304.15]** Source: FDA Food Code 2026, Chapters 1-6, §3-304.15 (p. 59). Gloves, Use Limitation (part 2)
> (F) Cloth gloves may not be used in direct contact with FOOD unless the FOOD is subsequently cooked as required under Part 3-4 such as frozen FOOD or a PRIMAL CUT of MEAT.

> **[Food Code 2026 §3-304.15]** Source: FDA Food Code 2026, Chapters 1-6, §3-304.15 (pp. 58-59). Gloves, Use Limitation (part 1)
> (A) Except as specified in ¶ (B) of this section, if used, single-use gloves shall be used for only one task such as working with READY-TO-EAT FOOD or with raw animal FOOD and used for no other purpose. (B) If APPROVED, FOOD EMPLOYEES may continue to use an interior single-use glove, provided the single-use interior glove is protected from contamination through the use of a task-specific loose-fitting exterior glove, if: (1) The method of removal of the exterior glove prevents contamination of the hands and the interior glove, and ensures that the hands and interior glove are not exposed to contamination during removal and discard, and (2) The exterior glove is sufficiently loose to allow removal by gravity, without contacting the interior glove and without requiring the exterior glove to be peeled off, and (3) If the exterior glove is single use only, it shall be immediately discarded in an appropriate waste container after use. (4) After exterior glove removal, the interior single-use glove remained intact with no tears or punctures, and free of contamination. (C) When in use, single-use gloves shall be discarded when damaged or soiled, or contaminated when interruptions occur in the operation. (D) Except as specified in ¶ (E) of this section, slash-resistant gloves that are used to protect the hands during operations requiring cutting shall be used in direct contact only with FOOD that is subsequently cooked as specified under Part 3-4 such as frozen FOOD or a PRIMAL CUT of MEAT. (E) Slash-resistant gloves may be used with READY-TO-EAT FOOD that will not be subsequently cooked if the slash-resistant gloves have a SMOOTH, durable, and nonabsorbent outer surface; or if the slash-resistant gloves are covered with a SMOOTH, durable, nonabsorbent glove, or a single-use glove.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-306.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-306.13 (p. 62). Consumer Self-Service Operations
> (A) Raw, unPACKAGED animal FOOD, such as beef, lamb, pork, POULTRY, and FISH may not be offered for CONSUMER self-service. This paragraph does not apply to: (1) CONSUMER self-service of READY-TO-EAT FOODS at buffets or salad bars that serve FOODS such as sushi or raw shellfish; (2) Ready-to-cook individual portions for immediate cooking and consumption on the PREMISES such as CONSUMER-cooked MEATS or CONSUMER-selected ingredients for Mongolian barbecue; or (3) RAW, frozen, shell-on shrimp, or lobster. (B) CONSUMER self-service operations for READY-TO-EAT FOODS shall be provided with suitable UTENSILS or effective dispensing methods that protect the FOOD from contamination. (C) CONSUMER self-service operations such as buffets and salad bar shall be monitored by FOOD EMPLOYEES trained in safe operating procedures.

> **[Food Code 2026 §3-301.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-301.11 (pp. 52-53). Preventing Contamination from Hands (part 1)
> (A) FOOD EMPLOYEES shall wash their hands as specified under § 2-301.12. (B) Except when washing fruits and vegetables as specified under § 3-302.15 or as specified in ¶¶ (D) and (E) of this section, FOOD EMPLOYEES may not contact exposed, READY-TO-EAT FOOD with their bare hands and shall use suitable UTENSILS such as deli tissue, spatulas, tongs, single-use gloves, or dispensing EQUIPMENT. (C) FOOD EMPLOYEES shall minimize bare hand and arm contact with exposed FOOD that is not in a ready-to-eat form. (D) Paragraph (B) of this section does not apply to a FOOD EMPLOYEE that contacts exposed, READY-TO-EAT FOOD with bare hands at the time the READY-TO-EAT FOOD is being added as an ingredient to a FOOD that: (1) Contains a raw animal FOOD and is to be cooked in the FOOD ESTABLISHMENT to heat all parts of the FOOD to the minimum temperatures specified in ¶¶ 3-401.11(A)-(B) or § 3-401.12; or (2) Does not contain a raw animal FOOD but is to be cooked in the FOOD ESTABLISHMENT to heat all parts of the food to a temperature of at least 63°C (145°F). (E) FOOD EMPLOYEES not serving a HIGHLY SUSCEPTIBLE POPULATION may contact exposed, READY-TO-EAT FOOD with their bare hands if: (1) The PERMIT HOLDER obtains prior APPROVAL from the REGULATORY AUTHORITY. (2) Written procedures are maintained in the FOOD ESTABLISHMENT and made available to the REGULATORY AUTHORITY upon request that include: (a) For each bare hand contact procedure, a listing of the specific READY-TO-EAT FOODs that are touched by bare hands; (b) Diagrams and other information showing that handwashing facilities, installed, located, equipped, and maintained as specified under §§ 5-

> **[Employee Health Handbook p. 17]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 17. Should food employees with one hand or those with a surrogate prosthetic device for hands and arms follow these handwashing procedures? (part 2)
> • Wear disposable gloves over artificial nails, nail polish, or uncleanable orthopedic support devices. The 2017 FDA Food Code allows bare hand contact with RTE food only when the regulatory authority has granted prior approval for an alternative procedure. The alternative procedure must address the management of food employees and related food handling activities to prevent food contamination, including the enforcement of thorough handwashing practices after toilet use. No Bare Hand Contact with Ready-to-Eat Foods

</details>


---

## q20 (single)

**Question:** A cook threw up this morning before her shift. When can she come back to work?

**Reference answer:** Not until at least 24 hours have passed after the vomiting (and any diarrhea) ended; she should phone the manager rather than come in.

**Expected source:** employee_health_handbook_2020 p. 4

**Agent's answer:**

The cook must not report to work and must remain excluded until at least 24 hours have passed since the vomiting and diarrhea symptoms ended, or until she provides medical documentation [Employee Health Handbook p. 29]. 

Are we allowed to let her return after 24 hours? The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Employee Health Handbook p. 29]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 29. 2-201.12 Table 1a Summary of Requirements for Symptomatic Food Employees
> Food employees and conditional employees shall report symptoms immediately to the person in charge The person in charge shall prohibit a conditional employee who reports a listed symptom from becoming a food employee until meeting the criteria listed in section 2-201.13 of the Food Code, for reinstatement of a symptomatic food employee. Symptom Exclusion or Restriction (Facilities Serving an HSP) Exclusion or Restriction (Facilities Not Serving an HSP) Removing Symptomatic Food Employees from Exclusion or Restriction RA Approval Required to Return to Work? Vomiting Exclude 2-201.12(A)(1) Exclude 2-201.12(A)(1) When the excluded food employee has been asymptomatic for at least 24 hours or provides medical documentation 2-201.13(A)(1). Exceptions: If diagnosed with Norovirus, Shigella spp., STEC, HAV, or typhoid fever (S. Typhi) (see Tables 1b and 2). No, if not diagnosed Diarrhea Exclude 2-201.12(A)(1) Exclude 2-201.12(A)(1) When the excluded food employee has been asymptomatic for at least 24 hours or provides medical documentation 2-201.13(A). Exceptions: If Diagnosed with Norovirus, STEC, HAV, or S. Typhi (see Tables 1b and 2). No, if not diagnosed Jaundice Exclude 2-201.12(B)(1) if the onset occurred within the last 7 days Exclude 2-201.12(B)(1) if the onset occurred within the last 7 days When approval is obtained from the RA 2-201.13(B), and: • Food employee has been jaundiced for more than 7 calendar days 2-201.13(B)(1), or • Food employee provides medical documentation 2-201.13(B)(3). Yes Sore Throat with Fever Exclude 2-201.12(G)(1) Restrict 2-201.12(G)(2) When food employee provides written medical documentation 2-201.13(G) (1)-(3). No Infected Wound or Pustular Boil Restrict 2-201.12(I) Restrict 2-201.12(I) When the infected wound or boil is properly covered 2-201.13(I)(1)-(3). No Key: Table 1a RA = Regulatory Authority STEC = Shiga toxin-producing Escherichia coli HAV = Hepatitis A virus HSP = Highly Susceptible Population

<details><summary>Other retrieved passages</summary>

> **[Employee Health Handbook p. 5]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 5. What should a manager do when a food employee reports symptoms of vomiting or diarrhea? (See Decision Tree 1 and Table 1a (and Table 1b if diagnosed))
> Ask the food employee to stop work immediately and leave the food establishment. Permit a return to work no sooner than 24 hours after vomiting and diarrhea have ended. Employee Health Management Responsibilities

> **[Employee Health Handbook p. 4]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 4. What should food employees do when they have symptoms of vomiting or diarrhea?
> If at work: • Stop work immediately; • Report to management; and • Go home and return after at least 24 hours have passed since the vomiting and diarrhea symptoms ended. If the symptoms occur before the employee arrives to work, he or she should: • Notify the manager by telephone; and • Do not report to work until at least 24 hours have passed after the diarrhea and vomiting symptoms have ended.

> **[Employee Health Handbook p. 30]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 30. 2-201.12 Table 1b Summary of Requirements for Diagnosed, Symptomatic Food Employees (part 1)
> Food employees and conditional employees shall report a listed diagnosis with symptoms immediately to the person in charge • The person in charge shall notify the RA when a food employee is jaundiced or reports a listed diagnosis. • The person in charge shall prohibit a conditional employee who reports a listed diagnosis with symptoms from becoming a food employee until meeting the criteria listed in section 2 201.13 of the Food Code, for reinstatement of a diagnosed, symptomatic food employee. Diagnosis Exclusion (Facilities Serving an HSP or Not Serving an HSP) Removing Diagnosed, Symptomatic Food Employees from Exclusion RA Approval Required to Return to Work? Hepatitis A Virus Exclude if within 14 days of any symptom, or within 7 days of jaundice 2-201.12(B)(2) When approval is obtained from the RA 2-201.13(B), and: • The food employee has been jaundiced for more than 7 calendar days 2-201.13(B)(1), or • The anicteric food employee has had symptoms for more than 14 days 2-201.13(B)(2), or • The food employee provides medical documentation 2-201.13(B)(3) (also see Table 2). Yes Typhoid Fever (S. Typhi) Exclude 2-201.12(C) When approval is obtained from the RA 2-201.13(C)(1), and: • Food employee provides medical documentation, that states the food employee is free of a S. Typhi infection 2-201.13(C)(2) (also see Table 2). Yes Nontyphoidal Salmonella Exclude Based on vomiting or diarrhea symptoms, under 2-201.12(A)(2) When approval is obtained from the RA 2-201.13(G), and: • Food employee provides medical documentation, that states the food employee is free of a nontyphoidal Salmonella infection 2-201.13)(G)(1) or • Food employee symptoms of vomiting or diarrhea resolved and >30 days have passed since the food employee became asymptomatic (2-201.13(G)(2)). Yes STEC Exclude Based on vomiting or diarrhea symptoms, under 2-201.12(A)(2)

> **[Employee Health Handbook p. 30]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), pp. 30-31. 2-201.12 Table 1b Summary of Requirements for Diagnosed, Symptomatic Food Employees (part 2)
> 1. Serving a non-HSP facility: 2-201.13(A)(4)(a): Shall only work on a restricted basis 24 hours after symptoms resolve and remains restricted until meeting the requirements listed in No. 3. 2. Serving an HSP facility: 2-201.13(A)(4)(b): Remains excluded until meeting the requirements listed in No. 3. 3. Restriction or Exclusion remains until: • Approval is obtained from RA 2-201.13(F), and • Medically cleared 2-201.13(F)(1), or • More than 7 calendar days have passed since the food employee became asymptomatic 2-201.13(F)(2) (also see Table 2). Yes to return to an HSP or to return unrestricted; not required to work on a restricted basis in a non-HSP facility Key: Table 1b RA = Regulatory Authority STEC = Shiga toxin-producing Escherichia coli HAV = Hepatitis A virus NTS = Nontyphoidal Salmonella Diagnosis Exclusion (Facilities Serving an HSP or Not Serving an HSP) Removing Diagnosed, Symptomatic Food Employees from Exclusion RA Approval Required to Return to Work? STEC Exclude Based on vomiting or diarrhea symptoms, under 2-201.12(A)(2) 1. Serving a non-HSP facility: 2-201.13(A)(4)(a): Shall only work on a restricted basis 24 hours after symptoms resolve and remains restricted until meeting the requirements listed in No. 3. 2. Serving an HSP facility: 2-201.13(A)(4)(b): Remains excluded until meeting the requirements listed in No. 3. 3. Restriction or Exclusion remains until: • Approval is obtained from RA 2-201.13(F), and • Medically cleared 2-201.13(F)(1), or • More than 7 calendar days have passed since the food employee became asymptomatic 2-201.13(F)(2) (also see Table 2). Yes to return to an HSP or to return unrestricted; not required to work on a restricted basis in a non-HSP facility Norovirus Exclude Based on vomiting or diarrhea symptoms, under 2-201.12(A)(2)

</details>


---

## q21 (single)

**Question:** Can staff use hand sanitizer instead of washing their hands?

**Reference answer:** No. Hand antiseptics may only be used in addition to proper handwashing.

**Expected source:** employee_health_handbook_2020 p. 15

**Agent's answer:**

No, hand sanitizers cannot be used in place of adequate handwashing, and should only be used in addition to proper handwashing [Employee Health Handbook p. 15]. 

The version of the Food Code adopted by your state or city is what applies here.

**Passages the answer cites:**

> **[Employee Health Handbook p. 15]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 15. Can hand antiseptics (hand sanitizers) be used in place of adequate handwashing in food establishments?
> No. Hand antiseptics should be used only in addition to proper handwashing.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §2-301.15]** Source: FDA Food Code 2026, Chapters 1-6, §2-301.15 (p. 40). Where to Wash
> FOOD EMPLOYEES shall clean their hands in a HANDWASHING SINK or APPROVED automatic handwashing facility and may not clean their hands in a sink used for FOOD preparation or WAREWASHING, or in a service sink or a curbed cleaning facility used for the disposal of mop water and similar liquid waste.

> **[Employee Health Handbook p. 14]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 14. Why is handwashing important?
> Handwashing reduces the spread of pathogenic microorganisms that are transmitted through food. The hands of food employees can be colonized with microorganisms such as Staphylococcus aureus or contaminated with organisms from human fecal material, such as Norovirus, Shigella spp., hepatitis A virus, E. coli O157:H7, or Salmonella Typhi, or contaminated from raw animal foods, with E. coli O157:H7 and Salmonella spp. These and other pathogenic microorganisms can get on the hands from a number of sources and then move from hands to food during preparation and service. An infected food employee and/or food employees with unclean hands, and exposed portions of arms or fingernails, can contaminate food. If a consumer eats contaminated food, foodborne illness may result.

> **[Employee Health Handbook p. 14]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), pp. 14-15. What handwashing steps do food employees need to follow?
> Clean hands and exposed portions of arms, including surrogate prosthetic devices for hands and arms, for at least 20 seconds by the following method: 1. Rinse under clean, warm running water; 2. Apply soap and rub all surfaces of the hands and fingers together vigorously with friction for at least 10 to 15 seconds, giving particular attention to the area under the fingernails, between the fingers/fingertips, and surfaces of the hands, arms, and surrogate prosthetic devices; 3. Rinse thoroughly with clean, warm running water; and Personal Hygiene 4. Thoroughly dry the hands and exposed portions of arms with single-use paper toweling, a heated-air hand-drying device, or a clean, unused towel from a continuous towel system that supplies the user with a clean towel. Avoid recontamination of hands and arms by using a clean barrier, such as a paper towel, when turning off hand sink faucets or touching the handle of a restroom door. It is important to follow these steps to remove germs from hands and ensure hands are as clean as possible. Thorough handwashing with warm water, the recommended amount of soap as indicated by the manufacturer, and proper hand drying are essential to reduce the possibility of hands transferring microorganisms to food.

> **[Food Code 2026 §2-301.16]** Source: FDA Food Code 2026, Chapters 1-6, §2-301.16 (p. 41). Hand Antiseptics (part 2)
> (1) Followed by thorough hand rinsing in clean water beforehand contact with FOOD or using gloves; or (2) Limited to situations that involve no direct contact with FOOD by the bare hands. (C) A hand antiseptic solution used as a hand dip shall be maintained clean and at a strength equivalent to at least 100 “MG/L” chlorine.

</details>


---

## q22 (single)

**Question:** What is the 'temperature danger zone'?

**Reference answer:** The range where pathogens grow fastest on TCS foods, usually between 41°F and 135°F (5°C and 57°C).

**Expected source:** cooling_guide_2024 p. 1

**Agent's answer:**

The "Temperature Danger Zone" is the range where food is most susceptible to pathogen growth, usually between 41°F and 135°F (5°C and 57°C) [Cooling Guide p. 1]. 

Pathogens can grow rapidly on Time/Temperature Control for Safety (TCS) foods when they are not cooled, held, or prepared properly [Cooling Guide p. 1]. The amount of time food spends in this range must be minimized [Cooling Guide p. 1].

**Passages the answer cites:**

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 1)
> One of the top contributors to foodborne illness is improper cooling of Time/Temperature Control for Safety (TCS) foods. Following the FDA Food Code cooling guidelines prevents this problem. Cooling to Avoid the Temperature Danger Zone Bacteria or other pathogens that cause foodborne illness can grow rapidly on TCS foods when they are not cooled properly. The “Temperature Danger Zone” is when food is most susceptible to pathogen growth— usually between 41°F and 135°F (5°C and 57°C). • The amount of time food spends in this range needs to be minimized by proper cooling. Cooling typically occurs when: • Leftovers are put into the refrigerator to be stored. • After preparing hot foods, but before you intend to serve them. • After preparing foods from room temperature that are not getting used immediately. • After milk and molluscan shellfish are delivered and placed under refrigeration. Cooling Cooked Time/Temperature Control for Safety Foods and the FDA Food Code: for Food Employees STEP 1 135°F 57°C 2 Hours 4 Hours “Rapid Cool” Stage 135°F - 70°F (57°C - 21°C) Cool Down Window 70°F - 41°F or less (21°C - 5°C) 70°F 21°C 41°F 5°C STEP 2 The FDA Food Code requires a two-step cooling process for cooked TCS Food: 1. A two-hour “rapid cool” from 135°F to 70°F (57°C to 21°C)

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 2)
> 2. Followed by a 4-hour window where foods must be cooled to 41°F or less (21°C to 5°C) This means that within two hours, the food must be cooled from cooking temperature (135°F) to 70°F in order to eliminate risk of pathogen growth. Over the next 4 hours the food must be cooled from 70°F to 41°F or less. Note: If 70°F is reached before 2 hours, you have the remaining time to reach 41°F or less. Keep food out of the danger zone to avoid risk of foodborne illness! Cooling Methods in the FDA

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-202.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-202.11 (pp. 48-49). Temperature
> (A) Except as specified in ¶ (B) of this section, refrigerated, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be at a temperature of 5°C (41°F) or below when received. (B) If a temperature other than 5°C (41°F) for a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD is specified in LAW governing its distribution, such as LAWS governing milk and MOLLUSCAN SHELLFISH, the FOOD may be received at the specified temperature. (C) Raw EGGS shall be received in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (D) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked to a temperature and for a time specified under §§ 3-401.11 – 3-401.13 and received hot shall be at a temperature of 57°C (135°F) or above. (E) A FOOD that is labeled frozen and shipped frozen by a FOOD PROCESSING PLANT shall be received frozen. (F) Upon receipt, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be free of evidence of previous temperature abuse.

> **[Food Code 2026 §3-501.14]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.14 (pp. 70-71). Cooling
> (A) Cooked TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled: (1) Within two hours from 57°C (135°F) to 21°C (70°F); and (2) Within a total of six hours from 57°C (135°F) to 5°C (41°F) or less. (B) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled within four hours to 5°C (41°F) or less if prepared from ingredients at ambient temperature, such as reconstituted FOODS and canned tuna. (C) Except as specified under ¶ (D) of this section, a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD received in compliance with LAWS allowing a temperature above 5°C (41°F) during shipment from the supplier as specified in ¶ 3-202.11(B), shall be cooled within four hours to 5°C (41°F) or less. (D) Raw EGGS shall be received as specified under ¶ 3-202.11(C) and immediately placed in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less.

> **[Food Code 2026 §3-501.16]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.16 (p. 72). Time/Temperature Control for Safety Food, Hot and Cold Holding
> (A) Except during preparation, cooking, or cooling, or when time is used as the public health control as specified under § 3-501.19, and except as specified under ¶ (B) and in ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be maintained: (1) At 57°C (135°F) or above, except roasts cooked to a temperature and for a time specified in ¶ 3-401.11(B) or reheated as specified in ¶ 3-403.11(E) may be held at a temperature of 54°C (130°F) or above; or (2) At 5°C (41°F) or less. (B) EGGS that have not been treated to destroy all viable Salmonellae shall be stored in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (C) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD in a homogenous liquid form may be maintained outside of the temperature control requirements, as specified under ¶ (A) of this section, while contained within specially designed EQUIPMENT that complies with the design and construction requirements as specified under ¶ 4-204.13(E). On-premises preparation Prepare and hold cold

</details>


---

## q23 (single)

**Question:** Do our cooks have to wear hairnets?

**Reference answer:** They must wear hair restraints such as hats, hair coverings or nets, beard restraints, and clothing that covers body hair, so hair cannot touch exposed food or clean equipment; not required for counter staff serving only drinks or wrapped food, hosts and wait staff with minimal risk.

**Expected source:** food_code_2026 2-402.11

**Agent's answer:**

Food employees must wear hair restraints such as hats, hair coverings or nets, beard restraints, and clothing that covers body hair, designed and worn to effectively keep their hair from contacting exposed food, clean equipment, utensils, linens, and unwrapped single-service and single-use articles [Food Code 2026 §2-402.11]. This requirement does not apply to food employees such as counter staff who only serve beverages and wrapped or packaged foods, hostesses, and wait staff if they present a minimal risk of contaminating exposed food, clean equipment, linens, and unwrapped single-service and single-use articles [Food Code 2026 §2-402.11]. 

The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §2-402.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-402.11 (p. 43). Effectiveness
> (A) Except as provided in ¶ (B) of this section, FOOD EMPLOYEES shall wear hair restraints such as hats, hair coverings or nets, beard restraints, and clothing that covers body hair, that are designed and worn to effectively keep their hair from contacting exposed FOOD; clean EQUIPMENT, UTENSILS, and LINENS; and unwrapped SINGLE-SERVICE and SINGLE-USE ARTICLES. (B) This section does not apply to FOOD EMPLOYEES such as counter staff who only serve BEVERAGES and wrapped or PACKAGED FOODS, hostesses, and wait staff if they present a minimal RISK of contaminating exposed FOOD; clean EQUIPMENT, LINENS; and unwrapped SINGLE-SERVICE and SINGLE-USE ARTICLES.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §2-302.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-302.11 (pp. 41-42). Maintenance
> (A) FOOD EMPLOYEES shall keep their fingernails trimmed, filed, and maintained so the edges and surfaces are cleanable and not rough. (B) Unless wearing intact gloves in good repair, a FOOD EMPLOYEE may not wear fingernail polish or artificial fingernails when working with exposed FOOD.

> **[Food Code 2026 §2-401.12]** Source: FDA Food Code 2026, Chapters 1-6, §2-401.12 (pp. 42-43). Discharges from the Eyes, Nose, and Mouth
> FOOD EMPLOYEES experiencing persistent sneezing, coughing, or a runny nose that causes discharges from the eyes, nose, or mouth may not work with exposed FOOD; clean EQUIPMENT, UTENSILS, and LINENS; or unwrapped SINGLE-SERVICE or SINGLE-USE ARTICLES.

> **[Food Code 2026 §2-304.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-304.11 (p. 42). Clean Condition
> FOOD EMPLOYEES shall wear clean outer clothing to prevent contamination of FOOD, EQUIPMENT, UTENSILS, LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES.

> **[Employee Health Handbook p. 7]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 7. If an infected wound, cut, or burn is covered, can employees continue working?
> Yes, food employees can continue working as long as the wound, cut, or burn is properly covered with a waterproof cover like a finger cot and a disposable glove.

</details>


---

## q24 (multi)

**Question:** Our soup cooled to 70°F after one hour. How much longer do we have to get it down to fridge temperature?

**Reference answer:** Cooked TCS food must be cooled from 57°C (135°F) to 21°C (70°F) within 2 hours and to 5°C (41°F) or less within a total of 6 hours. Since it reached 70°F after 1 hour, 5 hours remain to reach 41°F (the guide: if 70°F is reached before 2 hours, you keep the remaining time).

**Expected source:** food_code_2026;cooling_guide_2024 3-501.14;p. 1

**Agent's answer:**

You have a total of six hours from 57°C (135°F) to 5°C (41°F) or less to cool the food [Food Code 2026 §3-501.14]. Because you reached 70°F before two hours, you have the remaining time to reach 41°F (5°C) or less [Cooling Guide p. 1].

**Passages the answer cites:**

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 2)
> 2. Followed by a 4-hour window where foods must be cooled to 41°F or less (21°C to 5°C) This means that within two hours, the food must be cooled from cooking temperature (135°F) to 70°F in order to eliminate risk of pathogen growth. Over the next 4 hours the food must be cooled from 70°F to 41°F or less. Note: If 70°F is reached before 2 hours, you have the remaining time to reach 41°F or less. Keep food out of the danger zone to avoid risk of foodborne illness! Cooling Methods in the FDA

> **[Food Code 2026 §3-501.14]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.14 (pp. 70-71). Cooling
> (A) Cooked TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled: (1) Within two hours from 57°C (135°F) to 21°C (70°F); and (2) Within a total of six hours from 57°C (135°F) to 5°C (41°F) or less. (B) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled within four hours to 5°C (41°F) or less if prepared from ingredients at ambient temperature, such as reconstituted FOODS and canned tuna. (C) Except as specified under ¶ (D) of this section, a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD received in compliance with LAWS allowing a temperature above 5°C (41°F) during shipment from the supplier as specified in ¶ 3-202.11(B), shall be cooled within four hours to 5°C (41°F) or less. (D) Raw EGGS shall be received as specified under ¶ 3-202.11(C) and immediately placed in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less.

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 1)
> One of the top contributors to foodborne illness is improper cooling of Time/Temperature Control for Safety (TCS) foods. Following the FDA Food Code cooling guidelines prevents this problem. Cooling to Avoid the Temperature Danger Zone Bacteria or other pathogens that cause foodborne illness can grow rapidly on TCS foods when they are not cooled properly. The “Temperature Danger Zone” is when food is most susceptible to pathogen growth— usually between 41°F and 135°F (5°C and 57°C). • The amount of time food spends in this range needs to be minimized by proper cooling. Cooling typically occurs when: • Leftovers are put into the refrigerator to be stored. • After preparing hot foods, but before you intend to serve them. • After preparing foods from room temperature that are not getting used immediately. • After milk and molluscan shellfish are delivered and placed under refrigeration. Cooling Cooked Time/Temperature Control for Safety Foods and the FDA Food Code: for Food Employees STEP 1 135°F 57°C 2 Hours 4 Hours “Rapid Cool” Stage 135°F - 70°F (57°C - 21°C) Cool Down Window 70°F - 41°F or less (21°C - 5°C) 70°F 21°C 41°F 5°C STEP 2 The FDA Food Code requires a two-step cooling process for cooked TCS Food: 1. A two-hour “rapid cool” from 135°F to 70°F (57°C to 21°C)

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-501.15]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.15 (pp. 71-72). Cooling Methods
> (A) Except as specified in ¶ (C), cooling shall be accomplished in accordance with the time and temperature criteria specified under § 3-501.14 by using one or more of the following methods based on the type of FOOD being cooled: (1) Placing the FOOD in shallow pans; (2) Separating the FOOD into smaller or thinner portions; (3) Using rapid cooling EQUIPMENT; (4) Stirring the FOOD in a container placed in an ice water bath; (5) Using containers that facilitate heat transfer; (6) Adding ice as an ingredient; or (7) Placing the FOOD at a depth of no more than 2 inches; or (8) Other effective methods. (B) When placed in cooling or cold holding EQUIPMENT, FOOD containers in which FOOD is being cooled shall be: (1) Arranged in the EQUIPMENT to provide maximum heat transfer through the container walls; and (2) Loosely covered, or uncovered if protected from overhead contamination as specified under Subparagraph 3-305.11(A)(2), during the cooling period to facilitate heat transfer from the surface of the FOOD. (C) Except for FOOD cooled under ¶ 3-401.14(B), Subparagraph 3-502.12 (D)(2)(e), or § 3-501.19, a FOOD ESTABLISHMENT may cool cooked, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD, if APPROVED and: (1) Filled no more than two inches deep, (2) Held uncovered, and (3) Held in a refrigeration unit that: (a) Maintains ambient temperature of 5°C (41°F) or less, and (b) Is equipped with an electronic system that continuously monitors time and ambient air temperature.

> **[Food Code 2026 §3-501.19]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.19 (pp. 75-76). Time as a Public Health Control (part 3)
> (3) The FOOD shall be marked or otherwise identified to indicate: (a) The time when the FOOD is removed from 5°C (41°F) or less cold holding temperature control, and (b) The time that is six hours past the point in time when the FOOD is removed from cold holding temperature control; (4) The FOOD shall be: (a) Discarded if the temperature of the FOOD exceeds 21°C (70°F), or (b) Cooked and served, served at any temperature if READY-TO-EAT, or discarded within a maximum of six hours from the point in time when the FOOD is removed from 5°C (41°F) or less cold holding temperature control; and (5) The FOOD in unmarked containers or PACKAGES, or marked with a time that exceeds the six-hour limit shall be discarded. (D) A FOOD ESTABLISHMENT that serves a HIGHLY SUSCEPTIBLE POPULATION may not use time as specified under ¶¶ (A), (B), or (C) of this section as the public health control for raw EGGS.

</details>


---

## q25 (multi)

**Question:** We cook a big batch of rice every morning. How fast must it be cooled, and what methods can we use?

**Reference answer:** From 57°C (135°F) to 21°C (70°F) within 2 hours and to 5°C (41°F) within a total of 6 hours. Methods: shallow pans, smaller or thinner portions, rapid cooling equipment, stirring in an ice water bath, containers that transfer heat, adding ice as an ingredient, a depth of no more than 2 inches; containers arranged for heat transfer and loosely covered.

**Expected source:** food_code_2026 3-501.14;3-501.15

**Agent's answer:**

Cooked rice must be cooled within two hours from 57°C (135°F) to 21°C (70°F), and within a total of six hours from 57°C (135°F) to 5°C (41°F) or less [Food Code 2026 §3-501.14]. 

Permitted cooling methods include placing the food in shallow pans (or at a depth of no more than 2 inches), separating it into smaller or thinner portions, using rapid cooling equipment, stirring in an ice water bath, using containers that facilitate heat transfer, or adding ice as an ingredient [Food Code 2026 §3-501.15]. Containers should be arranged to provide maximum heat transfer and left loosely covered or uncovered (if protected from overhead contamination) during cooling [Food Code 2026 §3-501.15]. 

The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §3-501.14]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.14 (pp. 70-71). Cooling
> (A) Cooked TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled: (1) Within two hours from 57°C (135°F) to 21°C (70°F); and (2) Within a total of six hours from 57°C (135°F) to 5°C (41°F) or less. (B) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled within four hours to 5°C (41°F) or less if prepared from ingredients at ambient temperature, such as reconstituted FOODS and canned tuna. (C) Except as specified under ¶ (D) of this section, a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD received in compliance with LAWS allowing a temperature above 5°C (41°F) during shipment from the supplier as specified in ¶ 3-202.11(B), shall be cooled within four hours to 5°C (41°F) or less. (D) Raw EGGS shall be received as specified under ¶ 3-202.11(C) and immediately placed in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less.

> **[Food Code 2026 §3-501.15]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.15 (pp. 71-72). Cooling Methods
> (A) Except as specified in ¶ (C), cooling shall be accomplished in accordance with the time and temperature criteria specified under § 3-501.14 by using one or more of the following methods based on the type of FOOD being cooled: (1) Placing the FOOD in shallow pans; (2) Separating the FOOD into smaller or thinner portions; (3) Using rapid cooling EQUIPMENT; (4) Stirring the FOOD in a container placed in an ice water bath; (5) Using containers that facilitate heat transfer; (6) Adding ice as an ingredient; or (7) Placing the FOOD at a depth of no more than 2 inches; or (8) Other effective methods. (B) When placed in cooling or cold holding EQUIPMENT, FOOD containers in which FOOD is being cooled shall be: (1) Arranged in the EQUIPMENT to provide maximum heat transfer through the container walls; and (2) Loosely covered, or uncovered if protected from overhead contamination as specified under Subparagraph 3-305.11(A)(2), during the cooling period to facilitate heat transfer from the surface of the FOOD. (C) Except for FOOD cooled under ¶ 3-401.14(B), Subparagraph 3-502.12 (D)(2)(e), or § 3-501.19, a FOOD ESTABLISHMENT may cool cooked, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD, if APPROVED and: (1) Filled no more than two inches deep, (2) Held uncovered, and (3) Held in a refrigeration unit that: (a) Maintains ambient temperature of 5°C (41°F) or less, and (b) Is equipped with an electronic system that continuously monitors time and ambient air temperature.

<details><summary>Other retrieved passages</summary>

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 2)
> 2. Followed by a 4-hour window where foods must be cooled to 41°F or less (21°C to 5°C) This means that within two hours, the food must be cooled from cooking temperature (135°F) to 70°F in order to eliminate risk of pathogen growth. Over the next 4 hours the food must be cooled from 70°F to 41°F or less. Note: If 70°F is reached before 2 hours, you have the remaining time to reach 41°F or less. Keep food out of the danger zone to avoid risk of foodborne illness! Cooling Methods in the FDA

> **[Cooling Guide p. 2]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 2. Page 2
> Cooling Cooked Time/Temperature Control for Safety Foods and the FDA Food Code: for Food Employees (continued) 2 Food Code: Section 3-501.15 of the Food Code recommends using one or more of following methods be employed to assist with the cooling of TCS Food: Placing the food in shallow pans Separating the food into smaller or thinner portions Using rapid cooling equipment Stirring the food in a container placed in an ice water bath Using containers that facilitate heat transfer Adding ice as an ingredient, or other effective methods When placed in cooling or cold holding equipment, food containers in which food is being cooled shall be: • Arranged in the equipment to provide maximum heat transfer through the container walls, and • Loosely covered, or uncovered if protected from overhead contamination, during the cooling period to facilitate heat transfer from the surface of the food. For more information: • FDA, Poster: Why It’s Important to Cool Food Properly. Multiple translations available. • FDA, Retail Food Protection Industry Educational Materials (See Section “Proper Cooling of Time-Temperature Control for Safety Foods”) https://www.fda.gov/food/retail-food-industryregulatory-assistance-training/retail-food-protection-industry-educational-materials • CDC, Food Cooling Practice Improvements: https://www.cdc.gov/restaurant-food-safety/php/practices/ food-cooling.html • FDA Food Code: https://www.fda.gov/food/fda-food-code/food-code-2022 • FDA Job Aid: Time and Temperature Control for Safety Foods: https://www.fda.gov/files/food/ published/Job-Aid--Time-and-Temperature-Control-for-Safety-Foods.pdf

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 1)
> One of the top contributors to foodborne illness is improper cooling of Time/Temperature Control for Safety (TCS) foods. Following the FDA Food Code cooling guidelines prevents this problem. Cooling to Avoid the Temperature Danger Zone Bacteria or other pathogens that cause foodborne illness can grow rapidly on TCS foods when they are not cooled properly. The “Temperature Danger Zone” is when food is most susceptible to pathogen growth— usually between 41°F and 135°F (5°C and 57°C). • The amount of time food spends in this range needs to be minimized by proper cooling. Cooling typically occurs when: • Leftovers are put into the refrigerator to be stored. • After preparing hot foods, but before you intend to serve them. • After preparing foods from room temperature that are not getting used immediately. • After milk and molluscan shellfish are delivered and placed under refrigeration. Cooling Cooked Time/Temperature Control for Safety Foods and the FDA Food Code: for Food Employees STEP 1 135°F 57°C 2 Hours 4 Hours “Rapid Cool” Stage 135°F - 70°F (57°C - 21°C) Cool Down Window 70°F - 41°F or less (21°C - 5°C) 70°F 21°C 41°F 5°C STEP 2 The FDA Food Code requires a two-step cooling process for cooked TCS Food: 1. A two-hour “rapid cool” from 135°F to 70°F (57°C to 21°C)

</details>


---

## q26 (multi)

**Question:** We're thinking of opening a delivery-only kitchen. Does that count as a food establishment, and could we sell food that someone prepared at home?

**Reference answer:** Yes, it is a food establishment: the definition covers operations that hand food to consumers directly or through a delivery service such as takeout orders, and includes commissaries. Food prepared in a private home may not be used or offered in a food establishment.

**Expected source:** food_code_2026 1-201.10;3-201.11

**Agent's answer:**

Yes, a delivery-only kitchen counts as a food establishment because it prepares, packages, and provides food directly or indirectly to the consumer through a delivery service [Food Code 2026 §1-201.10]. 

A private home may not be used for conducting food establishment operations [Food Code 2026 §6-202.111], and a home kitchen is only excluded from the definition of a food establishment under very narrow conditions, such as preparing non-time/temperature control for safety foods for a bake sale, or specific small-scale bed-and-breakfast operations [Food Code 2026 §1-201.10]. 

Are we allowed to sell food that someone prepared at home? No, commercial food establishments generally cannot sell or serve food prepared in a private home kitchen [Food Code 2026 §6-202.111]. 

The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 8-9). Statement of Application and Listing of Terms (part 9)
> (3) "Food establishment" does not include: (a) An establishment that offers only pre-PACKAGED FOODS that are not TIME/TEMPERATURE CONTROL FOR SAFETY FOODS; (b) A produce stand that only offers whole, uncut fresh fruits and vegetables; (c) A FOOD PROCESSING PLANT; including those that are located on the PREMISES of a FOOD ESTABLISHMENT; (d) A kitchen in a private home if only FOOD that is not TIME/TEMPERATURE CONTROL FOR SAFETY FOOD, is prepared for sale or service at a function such as a religious or charitable organization’s bake sale if allowed by LAW and if the CONSUMER is informed by a clearly visible placard at the sales or service location that the FOOD is prepared in a kitchen that is not subject to regulation and inspection by the REGULATORY AUTHORITY; (e) An area where FOOD that is prepared as specified in Subparagraph (3)(d) of this definition is sold or offered for human consumption; (f) A kitchen in a private home, such as a small family day-care provider; or a bed-and-breakfast operation that prepares and offers FOOD to guests if the home is owner occupied, the number of available guest bedrooms does not exceed 6, breakfast is the only meal offered, the number of guests served does not exceed 18, and the CONSUMER is informed by statements contained in published advertisements, mailed brochures, and placards posted at the registration area that the FOOD is prepared in a kitchen that is not regulated and inspected by the REGULATORY AUTHORITY; or (g) A private home that receives catered or home-delivered FOOD. Food Processing Plant. (1) "Food processing plant" means a commercial operation that manufactures, PACKAGES, labels, or stores FOOD for human consumption, and provides FOOD for sale or distribution to other business entities such as FOOD PROCESSING PLANTS or FOOD ESTABLISHMENTS.

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 7-8). Statement of Application and Listing of Terms (part 8)
> (1) A surface of EQUIPMENT or a UTENSIL with which FOOD normally comes into contact; or (2) A surface of EQUIPMENT or a UTENSIL from which FOOD may drain, drip, or splash: (a) Into a FOOD, or (b) Onto a surface normally in contact with FOOD. "Food defense" is the effort to protect FOOD from acts of intentional ADULTERATION or tampering. "Food employee" means an individual working with unPACKAGED FOOD, FOOD EQUIPMENT or UTENSILS, or FOOD-CONTACT SURFACES. Food Establishment. (1) "Food establishment" means an operation that: (a) Stores, prepares, PACKAGES, serves, vends FOOD directly to the CONSUMER, or otherwise provides FOOD for human consumption such as a restaurant; satellite or catered feeding location; commissary, catering operation if the operation provides FOOD directly to a CONSUMER or to a conveyance used to transport people; market; vending location; conveyance used to transport people; institution; or FOOD bank; and (b) Relinquishes possession of FOOD to a CONSUMER directly, or indirectly through a delivery service such as home delivery of grocery orders or restaurant takeout orders, or delivery service that is provided by common carriers. (2) "Food establishment" includes: (a) An element of the operation such as a transportation vehicle or a central preparation facility that supplies a vending location or satellite feeding location unless the vending or feeding location is PERMITTED by the REGULATORY AUTHORITY; and (b) An operation that is conducted in a mobile, stationary, temporary, or permanent facility or location; where consumption is on or off the PREMISES; and regardless of whether there is a charge for the FOOD.

> **[Food Code 2026 §6-202.111]** Source: FDA Food Code 2026, Chapters 1-6, §6-202.111 (p. 137). Private Homes and Living or Sleeping Quarters, Use Prohibition
> A private home, a room used as living or sleeping quarters, or an area directly opening into a room used as living or sleeping quarters may not be used for conducting FOOD ESTABLISHMENT operations.

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 6-7). Statement of Application and Listing of Terms (part 7)
> "Employee" means the PERMIT HOLDER, PERSON IN CHARGE, FOOD EMPLOYEE, PERSON having supervisory or management duties, PERSON on the payroll, family member, volunteer, PERSON performing work under contractual agreement, or other PERSON working in a FOOD ESTABLISHMENT. "EPA" means the U.S. Environmental Protection Agency. Equipment. (1) "Equipment" means an article that is used in the operation of a FOOD ESTABLISHMENT such as a freezer, grinder, hood, ice maker, MEAT block, mixer, oven, reach-in refrigerator, scale, sink, slicer, stove, table, TEMPERATURE MEASURING DEVICE for ambient air, VENDING MACHINE, or WAREWASHING machine. (2) "Equipment" does not include apparatuses used for handling or storing large quantities of PACKAGED FOODS that are received from a supplier in a cased or overwrapped lot, such as hand trucks, forklifts, dollies, pallets, racks, and skids. "Exclude" means to prevent a PERSON from working as an EMPLOYEE in a FOOD ESTABLISHMENT or entering a FOOD ESTABLISHMENT as an EMPLOYEE. "FDA" means the U.S. Food and Drug Administration. Fish. (1) "Fish" means fresh or saltwater finfish, crustaceans and other forms of aquatic life (including alligator, frog, aquatic turtle, jellyfish, sea cucumber, and sea urchin and the roe of such animals) other than birds or mammals, and all mollusks, if such animal life is intended for human consumption. (2) "Fish" includes an edible human FOOD product derived in whole or in part from FISH, including FISH that have been processed in any manner. "Food" means a raw, cooked, or processed edible substance, ice, BEVERAGE, or ingredient used or intended for use or for sale in whole or in part for human consumption, or chewing gum. "Foodborne disease outbreak" means the occurrence of two or more cases of a similar illness resulting from the ingestion of a common FOOD. "Food-contact surface" means:

<details><summary>Other retrieved passages</summary>

> **[Employee Health Handbook p. 8]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 8. What is “exclusion”?
> Exclusion means a food employee is not permitted to work in or enter a food establishment as a food employee. This requirement applies to areas where food is received, prepared, stored, packaged, served, vended, transported, or purchased.

</details>


---

## q27 (multi)

**Question:** We cook chicken thighs and keep them warm for takeout orders. What temperature do we cook them to, and what temperature do we hold them at?

**Reference answer:** Cook to 74°C (165°F) or above (instantaneous); then hold at 57°C (135°F) or above.

**Expected source:** food_code_2026 3-401.11;3-501.16

**Agent's answer:**

Poultry must be cooked to a temperature of 74°C (165°F) or above for < 1 second (instantaneous) [Food Code 2026 §3-401.11]. 

For hot holding, time/temperature control for safety food must be maintained at 57°C (135°F) or above [Food Code 2026 §3-501.16].

Are we allowed to... depends on the version of the Food Code adopted by your state or local health jurisdiction.

**Passages the answer cites:**

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (p. 63). Raw Animal Foods (part 1)
> (A) Except as specified under ¶ (B) and in ¶¶ (C) and (D) of this section, raw animal FOODS such as EGGS, FISH, MEAT, POULTRY, and FOODS containing these raw animal FOODS, shall be cooked to heat all parts of the FOOD to a temperature and for a time that complies with one of the following methods based on the FOOD that is being cooked: (1) 63°C (145°F) or above for 15 seconds for: (a) Raw EGGS that are broken and prepared in response to a CONSUMER'S order and for immediate service, and (b) Except as specified under Subparagraphs (A)(2) and (A)(3) and ¶ (B), and in ¶ (C) of this section, FISH and INTACT MEAT including GAME ANIMALS commercially raised for FOOD as specified under Subparagraph 3-201.17(A)(1) and GAME ANIMALS under a voluntary inspection program as specified under Subparagraph 3-201.17(A)(2); (2) 68°C (155°F) for 17 seconds or the temperature specified in the following chart that corresponds to the holding time for RATITES, and nonINTACT MEATS; the following if they are COMMINUTED: FISH and GAME ANIMALS commercially raised for FOOD as specified under Subparagraph 3-201.17(A)(1), and GAME ANIMALS under a voluntary inspection program as specified under Subparagraph 3-201.17(A)(2); and raw EGGS that are not prepared as specified under Subparagraph (A)(1)(a) of this section; or: Minimum Temperature °C (°F) Minimum Time 63 (145) 3 minutes 66 (150) 1 minute 70 (158) < 1 second (instantaneous) (3) 74°C (165°F) or above for < 1 second (instantaneous) for POULTRY, BALUTS, wild GAME animals as specified under Subparagraphs 3-201.17(A)(3) and (4), stuffed FISH, stuffed MEAT, stuffed pasta, stuffed POULTRY, stuffed RATITES, or stuffing containing FISH, MEAT, POULTRY, or RATITES. (B) Whole MEAT roasts including beef, corned beef, lamb, pork, and cured pork roasts such as ham shall be cooked:

> **[Food Code 2026 §3-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.11 (pp. 63-65). Raw Animal Foods (part 2)
> (1) As specified in the following chart, to heat all parts of the FOOD to a temperature and for the holding time that corresponds to that temperature: and Temperature °C (°F) Time1 in Minutes 54.4 (130) 112 55.0 (131) 89 56.1 (133) 56 57.2 (135) 36 57.8 (136) 28 58.9 (138) 18 60.0 (140) 12 61.1 (142) 8 62.2 (144) 5 62.8 (145) 4 63.9 (147) 134 65.0 (149) 85 66.1 (151) 54 67.2 (153) 34 68.3 (155) 22 69.4 (157) 14 70.0 (158) 0 1 Holding time may include post-oven heat rise. (2) If cooked in an oven, use an oven that is preheated to the temperature specified for the roast's weight in the following chart and that is held at that temperature: Oven Temperature Based on Roast Weight Oven Type Less than 4.5 kg (10 lbs.) 4.5 kg (10 lbs.) or More Still Dry 177°C (350°F) or more 121°C (250°F) or more Convection 163°C (325°F) or more 121°C (250°F) or more High Humidity 1 121°C (250°F) or less 121°C (250°F) or less 1 Relative humidity greater than 90% for at least 1 hour as measured in the cooking chamber or exit of the oven; or in a moisture-impermeable bag that provides 100% humidity. (C) A raw or undercooked WHOLE-MUSCLE, INTACT BEEF steak may be served or offered for sale in a READY-TO-EAT form if: (1) The FOOD ESTABLISHMENT serves a population that is not a HIGHLY SUSCEPTIBLE POPULATION, (2) The steak is prepared so that it remains intact, and (3) The steak is cooked on both the top and bottom to a surface temperature of 63°C (145°F) or above and a cooked color change is achieved on all external surfaces.

> **[Food Code 2026 §3-501.16]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.16 (p. 72). Time/Temperature Control for Safety Food, Hot and Cold Holding
> (A) Except during preparation, cooking, or cooling, or when time is used as the public health control as specified under § 3-501.19, and except as specified under ¶ (B) and in ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be maintained: (1) At 57°C (135°F) or above, except roasts cooked to a temperature and for a time specified in ¶ 3-401.11(B) or reheated as specified in ¶ 3-403.11(E) may be held at a temperature of 54°C (130°F) or above; or (2) At 5°C (41°F) or less. (B) EGGS that have not been treated to destroy all viable Salmonellae shall be stored in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (C) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD in a homogenous liquid form may be maintained outside of the temperature control requirements, as specified under ¶ (A) of this section, while contained within specially designed EQUIPMENT that complies with the design and construction requirements as specified under ¶ 4-204.13(E). On-premises preparation Prepare and hold cold

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-401.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.12 (pp. 65-66). Microwave Cooking
> Raw animal FOODS cooked in a microwave oven shall be: (A) Rotated or stirred throughout or midway during cooking to compensate for uneven distribution of heat; (B) Covered to retain surface moisture; (C) Heated to a temperature of at least 74°C (165°F) in all parts of the FOOD; and (D) Allowed to stand covered for two minutes after cooking to obtain temperature equilibrium.

> **[Food Code 2026 §3-501.14]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.14 (pp. 70-71). Cooling
> (A) Cooked TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled: (1) Within two hours from 57°C (135°F) to 21°C (70°F); and (2) Within a total of six hours from 57°C (135°F) to 5°C (41°F) or less. (B) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be cooled within four hours to 5°C (41°F) or less if prepared from ingredients at ambient temperature, such as reconstituted FOODS and canned tuna. (C) Except as specified under ¶ (D) of this section, a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD received in compliance with LAWS allowing a temperature above 5°C (41°F) during shipment from the supplier as specified in ¶ 3-202.11(B), shall be cooled within four hours to 5°C (41°F) or less. (D) Raw EGGS shall be received as specified under ¶ 3-202.11(C) and immediately placed in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less.

> **[Cooling Guide p. 1]** Source: FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024), p. 1. Page 1 (part 2)
> 2. Followed by a 4-hour window where foods must be cooled to 41°F or less (21°C to 5°C) This means that within two hours, the food must be cooled from cooking temperature (135°F) to 70°F in order to eliminate risk of pathogen growth. Over the next 4 hours the food must be cooled from 70°F to 41°F or less. Note: If 70°F is reached before 2 hours, you have the remaining time to reach 41°F or less. Keep food out of the danger zone to avoid risk of foodborne illness! Cooling Methods in the FDA

> **[Food Code 2026 §3-403.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-403.11 (pp. 68-69). Reheating for Hot Holding
> (A) Except as specified under ¶¶ (B) and (C) and in ¶ (E) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked, cooled, and reheated for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) for 15 seconds. (B) Except as specified under ¶ (C) of this section, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD reheated in a microwave oven for hot holding shall be reheated so that all parts of the FOOD reach a temperature of at least 74°C (165°F) and the FOOD is rotated or stirred, covered, and allowed to stand covered for two minutes after reheating. (C) READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that has been commercially processed and PACKAGED in a FOOD PROCESSING PLANT that is inspected by the REGULATORY AUTHORITY that has jurisdiction over the plant, shall be heated to a temperature of at least 57°C (135°F) when being reheated for hot holding. (D) Reheating for hot holding as specified under ¶¶ (A) - (C) of this section shall be done rapidly and the time the FOOD is between 5°C (41°F) and the temperatures specified under ¶¶ (A) - (C) of this section may not exceed two hours. (E) Remaining unsliced portions of MEAT roasts that are cooked as specified under ¶ 3-401.11(B) may be reheated for hot holding using the oven parameters and minimum time and temperature conditions specified under ¶ 3-401.11(B).

> **[Food Code 2026 §3-401.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-401.13 (p. 66). Plant Food Cooking for Hot Holding
> Plant FOODS that are cooked for hot holding shall be cooked to a temperature of 57°C (135°F) or as specified under § 3-401.15.

> **[Food Code 2026 §3-202.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-202.11 (pp. 48-49). Temperature
> (A) Except as specified in ¶ (B) of this section, refrigerated, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be at a temperature of 5°C (41°F) or below when received. (B) If a temperature other than 5°C (41°F) for a TIME/TEMPERATURE CONTROL FOR SAFETY FOOD is specified in LAW governing its distribution, such as LAWS governing milk and MOLLUSCAN SHELLFISH, the FOOD may be received at the specified temperature. (C) Raw EGGS shall be received in refrigerated EQUIPMENT that maintains an ambient air temperature of 7°C (45°F) or less. (D) TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is cooked to a temperature and for a time specified under §§ 3-401.11 – 3-401.13 and received hot shall be at a temperature of 57°C (135°F) or above. (E) A FOOD that is labeled frozen and shipped frozen by a FOOD PROCESSING PLANT shall be received frozen. (F) Upon receipt, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD shall be free of evidence of previous temperature abuse.

> **[Food Code 2026 §4-301.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-301.11 (p. 98). Cooling, Heating, and Holding Capacities
> EQUIPMENT for cooling and heating FOOD, and holding cold and hot FOOD, shall be sufficient in number and capacity to provide FOOD temperatures as specified under Chapter 3.

</details>


---

## q28 (multi)

**Question:** How warm does the water at our handwashing sink have to be?

**Reference answer:** The Food Code 2026 requires at least 29.4°C (85°F) through a mixing valve or combination faucet. The Handbook quotes the 2017 Food Code's 38°C (100°F), which is outdated.

**Expected source:** food_code_2026;employee_health_handbook_2020 5-202.12;p. 15

**Agent's answer:**

A handwashing sink must be equipped to provide water at a temperature of at least 29.4°C (85°F) through a mixing valve or combination faucet [Food Code 2026 §5-202.12]. (Note that the Employee Health Handbook cites an older Food Code specification of 38°C (100°F) [Employee Health Handbook p. 15], but the Food Code 2026 is the newest edition.)

**Passages the answer cites:**

> **[Employee Health Handbook p. 15]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 15. How important is the temperature of water used for handwashing?
> Warm water is generally more comfortable than cold water and encourages handwashing for the recommended duration. The water temperature used in handwashing can also affect the solubility or emulsification of some soils. Warm water is more effective than cold water in removing fatty soils. An adequate flow of warm water will cause soap to lather and aid in flushing soil quickly from the hands. The 2017 FDA Food Code specifies that a handwashing sink shall be equipped to provide water at a temperature of at least 38°C (100°F) through a mixing valve or combination faucet.

> **[Food Code 2026 §5-202.12]** Source: FDA Food Code 2026, Chapters 1-6, §5-202.12 (pp. 121-122). Handwashing Sink, Installation
> (A) A HANDWASHING SINK shall be equipped to provide water at a temperature of at least 29.4°C (85°F) through a mixing valve or combination faucet (B) A steam, mixing valve may not be used at a HANDWASHING SINK. (C) A self-closing, slow-closing, or metering faucet shall provide a flow of water for at least 15 seconds without the need to reactivate the faucet. (D) An automatic handwashing facility shall be installed in accordance with manufacturer’s instructions.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §4-501.19]** Source: FDA Food Code 2026, Chapters 1-6, §4-501.19 (p. 104). Manual Warewashing Equipment, Wash Solution Temperature
> The temperature of the wash solution in manual WAREWASHING EQUIPMENT shall be maintained at not less than 43°C (110°F) or the temperature specified on the cleaning agent manufacturer's label instructions.

> **[Food Code 2026 §4-204.116]** Source: FDA Food Code 2026, Chapters 1-6, §4-204.116 (p. 96). Manual Warewashing Equipment, Heaters and Baskets
> If hot water is used for SANITIZATION in manual WAREWASHING operations, the SANITIZING compartment of the sink shall be: (A) Designed with an integral heating device that can maintain water at a temperature not less than 77°C (171°F); and (B) Provided with a rack or basket to allow complete immersion of EQUIPMENT and UTENSILS into the hot water.

> **[Food Code 2026 §4-501.111]** Source: FDA Food Code 2026, Chapters 1-6, §4-501.111 (p. 104). Manual Warewashing Equipment, Hot Water Sanitization Temperatures
> If immersion in hot water is used for SANITIZING in a manual operation, the temperature of the water shall be maintained at 77°C (171°F) or above.

</details>


---

## q29 (multi)

**Question:** A cook tells me his eyes have turned yellow. Do I have to send him home, and do I need to tell anyone?

**Reference answer:** Exclude him if the jaundice started within the last 7 days, unless a health practitioner documents it is not caused by hepatitis A or another fecal-orally transmitted infection. Report the jaundice to the regulatory authority, whose approval is needed before he returns.

**Expected source:** food_code_2026;employee_health_handbook_2020 2-201.12;p. 6

**Agent's answer:**

Yes, you must have the food employee stop work immediately and leave the food establishment if he or she has had jaundice for less than 7 days [Employee Health Handbook p. 6]. You must also report cases of jaundice to the regulatory authority [Employee Health Handbook p. 6]. The employee needs regulatory authority approval to return to work [Employee Health Handbook p. 6].

**Passages the answer cites:**

> **[Employee Health Handbook p. 6]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 6. What should a manager do when a food employee reports symptoms of jaundice?
> (See Decision Tree 1 and Table 1a) • Have the food employee stop work immediately. • Inquire about how long the employee has been experiencing jaundice or associated symptoms of jaundice. • Have the food employee leave the food establishment if he or she has had jaundice or has been experiencing symptoms of jaundice for less than 7 days. • Report cases of jaundice to the regulatory authority and have the food employee’s return to work approved by a regulatory authority.

<details><summary>Other retrieved passages</summary>

> **[Employee Health Handbook p. 4]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 4. What should food employees do if they are not feeling well and their skin or eyes turn yellow?
> Report the symptoms to their manager or person in charge (PIC) immediately and seek medical attention. The employee should not return to work until after receiving clearance from a health practitioner. If the employee is jaundiced for more than 7 days, clearance from the local health department is required.

> **[Employee Health Handbook p. 29]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 29. 2-201.12 Table 1a Summary of Requirements for Symptomatic Food Employees
> Food employees and conditional employees shall report symptoms immediately to the person in charge The person in charge shall prohibit a conditional employee who reports a listed symptom from becoming a food employee until meeting the criteria listed in section 2-201.13 of the Food Code, for reinstatement of a symptomatic food employee. Symptom Exclusion or Restriction (Facilities Serving an HSP) Exclusion or Restriction (Facilities Not Serving an HSP) Removing Symptomatic Food Employees from Exclusion or Restriction RA Approval Required to Return to Work? Vomiting Exclude 2-201.12(A)(1) Exclude 2-201.12(A)(1) When the excluded food employee has been asymptomatic for at least 24 hours or provides medical documentation 2-201.13(A)(1). Exceptions: If diagnosed with Norovirus, Shigella spp., STEC, HAV, or typhoid fever (S. Typhi) (see Tables 1b and 2). No, if not diagnosed Diarrhea Exclude 2-201.12(A)(1) Exclude 2-201.12(A)(1) When the excluded food employee has been asymptomatic for at least 24 hours or provides medical documentation 2-201.13(A). Exceptions: If Diagnosed with Norovirus, STEC, HAV, or S. Typhi (see Tables 1b and 2). No, if not diagnosed Jaundice Exclude 2-201.12(B)(1) if the onset occurred within the last 7 days Exclude 2-201.12(B)(1) if the onset occurred within the last 7 days When approval is obtained from the RA 2-201.13(B), and: • Food employee has been jaundiced for more than 7 calendar days 2-201.13(B)(1), or • Food employee provides medical documentation 2-201.13(B)(3). Yes Sore Throat with Fever Exclude 2-201.12(G)(1) Restrict 2-201.12(G)(2) When food employee provides written medical documentation 2-201.13(G) (1)-(3). No Infected Wound or Pustular Boil Restrict 2-201.12(I) Restrict 2-201.12(I) When the infected wound or boil is properly covered 2-201.13(I)(1)-(3). No Key: Table 1a RA = Regulatory Authority STEC = Shiga toxin-producing Escherichia coli HAV = Hepatitis A virus HSP = Highly Susceptible Population

> **[Employee Health Handbook p. 30]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 30. 2-201.12 Table 1b Summary of Requirements for Diagnosed, Symptomatic Food Employees (part 1)
> Food employees and conditional employees shall report a listed diagnosis with symptoms immediately to the person in charge • The person in charge shall notify the RA when a food employee is jaundiced or reports a listed diagnosis. • The person in charge shall prohibit a conditional employee who reports a listed diagnosis with symptoms from becoming a food employee until meeting the criteria listed in section 2 201.13 of the Food Code, for reinstatement of a diagnosed, symptomatic food employee. Diagnosis Exclusion (Facilities Serving an HSP or Not Serving an HSP) Removing Diagnosed, Symptomatic Food Employees from Exclusion RA Approval Required to Return to Work? Hepatitis A Virus Exclude if within 14 days of any symptom, or within 7 days of jaundice 2-201.12(B)(2) When approval is obtained from the RA 2-201.13(B), and: • The food employee has been jaundiced for more than 7 calendar days 2-201.13(B)(1), or • The anicteric food employee has had symptoms for more than 14 days 2-201.13(B)(2), or • The food employee provides medical documentation 2-201.13(B)(3) (also see Table 2). Yes Typhoid Fever (S. Typhi) Exclude 2-201.12(C) When approval is obtained from the RA 2-201.13(C)(1), and: • Food employee provides medical documentation, that states the food employee is free of a S. Typhi infection 2-201.13(C)(2) (also see Table 2). Yes Nontyphoidal Salmonella Exclude Based on vomiting or diarrhea symptoms, under 2-201.12(A)(2) When approval is obtained from the RA 2-201.13(G), and: • Food employee provides medical documentation, that states the food employee is free of a nontyphoidal Salmonella infection 2-201.13)(G)(1) or • Food employee symptoms of vomiting or diarrhea resolved and >30 days have passed since the food employee became asymptomatic (2-201.13(G)(2)). Yes STEC Exclude Based on vomiting or diarrhea symptoms, under 2-201.12(A)(2)

> **[Employee Health Handbook p. 3]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), pp. 3-4. What is a common symptom of the hepatitis A virus?
> Jaundice, a common symptom of the hepatitis A virus, often results in a yellowing of the skin, mucous membranes, and white portion of the eyes. Foodborne Illness Employee Health and the Food Establishment

</details>


---

## q30 (multi)

**Question:** We made potato salad on Monday and keep it at 41°F. What is the last day we can serve it, and what if someone forgot to put a date on it?

**Reference answer:** Monday counts as Day 1 and it may be kept at most 7 days, so through Sunday. Food that must be date-marked but whose container bears no date must be discarded.

**Expected source:** food_code_2026 3-501.17;3-501.18

**Agent's answer:**

If prepared on Monday, the potato salad must be consumed, sold, or discarded by the end of Sunday (a maximum of seven days, counting Monday as Day 1) when held at 41°F or less [Food Code 2026 §3-501.17]. If someone forgot to put a date on it, the potato salad must be discarded [Food Code 2026 §3-501.18].

**Passages the answer cites:**

> **[Food Code 2026 §3-501.17]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.17 (pp. 72-73). Ready-to-Eat, Time/Temperature Control for Safety Food, Date Marking (part 1)
> (A) Except when PACKAGING FOOD using a REDUCED OXYGEN PACKAGING method as specified under § 3-502.12, and except as specified in ¶¶ (E) and (F) of this section, refrigerated, READY-TO-EAT, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD prepared and held in a FOOD ESTABLISHMENT for more than 24 hours shall be clearly marked to indicate the date or day by which the FOOD shall be consumed on the PREMISES, sold, or discarded when held at a temperature of 5°C (41°F) or less for a maximum of seven days. The day of preparation shall be counted as Day 1. Commercially processed food Open and hold cold (B) Except as specified in ¶¶ (E) - (G) of this section, refrigerated, READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD prepared and PACKAGED by a FOOD PROCESSING PLANT shall be clearly marked, at the time the original container is opened in a FOOD ESTABLISHMENT and if the FOOD is held for more than 24 hours, to indicate the date or day by which the FOOD shall be consumed on the PREMISES, sold, or discarded, based on the temperature and time combinations specified in ¶ (A) of this section and: (1) The day the original container is opened in the FOOD ESTABLISHMENT shall be counted as Day 1; and (2) The day or date marked by the FOOD ESTABLISHMENT may not exceed a manufacturer’s use-by date if the manufacturer determined the use-by date based on FOOD safety. (C) A refrigerated, READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD ingredient or a portion of a refrigerated, READY-TO-EAT, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is subsequently combined with additional ingredients or portions of FOOD shall retain the date marking of the earliest-prepared or first-prepared ingredient.

> **[Food Code 2026 §3-501.17]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.17 (p. 73). Ready-to-Eat, Time/Temperature Control for Safety Food, Date Marking (part 2)
> (D) A date marking system that meets the criteria stated in ¶¶ (A) and (B) of this section may include: (1) Using a method APPROVED by the REGULATORY AUTHORITY for refrigerated, READY-TO-EAT TIME/TEMPERATURE CONTROL FOR SAFETY FOOD that is frequently rewrapped, such as lunchmeat or a roast, or for which date marking is impractical, such as soft serve mix or milk in a dispensing machine; (2) Marking the date or day of preparation, with a procedure to discard the FOOD on or before the last date or day by which the FOOD must be consumed on the PREMISES, sold, or discarded as specified under ¶ (A) of this section; (3) Marking the date or day the original container is opened in a FOOD ESTABLISHMENT, with a procedure to discard the FOOD on or before the last date or day by which the FOOD must be consumed on the PREMISES, sold, or discarded as specified under ¶ (B) of this section; or (4) Using calendar dates, days of the week, color-coded marks, or other effective marking methods, provided that the marking system is disclosed to the REGULATORY AUTHORITY upon request. (E) Paragraphs (A) and (B) of this section do not apply to individual meal portions served or rePACKAGED for sale from a bulk container upon a CONSUMER’S request. (F) Paragraphs (A) and (B) of this section do not apply to SHELLSTOCK (G) Paragraph (B) of this section does not apply to the following FOODS prepared and PACKAGED by a FOOD PROCESSING PLANT inspected by a REGULATORY AUTHORITY: (1) Deli salads, such as ham salad, seafood salad, chicken salad, EGG salad, pasta salad, potato salad, and macaroni salad, manufactured in accordance with 21 CFR 117 Current good manufacturing practice in manufacturing, packing, or holding human FOOD;

> **[Food Code 2026 §3-501.18]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.18 (p. 74). Ready-to-Eat, Time/Temperature Control for Safety Food, Disposition
> (A) A FOOD specified in ¶ 3-501.17(A) or (B) shall be discarded if it: (1) Exceeds the temperature and time combination specified in ¶ 3-501.17(A), except time that the product is frozen; (2) Is in a container or PACKAGE that does not bear a date or day; or (3) Is inappropriately marked with a date or day that exceeds a temperature and time combination as specified in ¶ 3-501.17(A). (B) Refrigerated, READY-TO-EAT, TIME/TEMPERATURE CONTROL FOR SAFETY FOOD prepared in a FOOD ESTABLISHMENT and dispensed through a VENDING MACHINE with an automatic shutoff control shall be discarded if it exceeds a temperature and time combination as specified in ¶ 3-501.17(A).

> **[Food Code 2026 §3-501.17]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.17 (p. 74). Ready-to-Eat, Time/Temperature Control for Safety Food, Date Marking (part 3)
> (2) Hard cheeses containing not more than 39% moisture as defined in 21 CFR 133 Cheeses and related cheese products, such as cheddar, gruyere, parmesan and reggiano, and romano; (3) Semi-soft cheeses containing more than 39% moisture, but not more than 50% moisture, as defined in 21 CFR 133 Cheeses and related cheese products, such as blue, edam, gorgonzola, gouda, and monterey jack; (4) Cultured dairy products as defined in 21 CFR 131 Milk and cream, such as yogurt, sour cream, and buttermilk; (5) Preserved FISH products, such as pickled herring and dried or salted cod, and other acidified FISH products defined in 21 CFR 114 Acidified FOODS; (6) Shelf stable, dry fermented sausages, such as pepperoni and Genoa; and (7) Shelf stable salt-cured products such as prosciutto and Parma (ham).

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-501.19]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.19 (pp. 75-76). Time as a Public Health Control (part 3)
> (3) The FOOD shall be marked or otherwise identified to indicate: (a) The time when the FOOD is removed from 5°C (41°F) or less cold holding temperature control, and (b) The time that is six hours past the point in time when the FOOD is removed from cold holding temperature control; (4) The FOOD shall be: (a) Discarded if the temperature of the FOOD exceeds 21°C (70°F), or (b) Cooked and served, served at any temperature if READY-TO-EAT, or discarded within a maximum of six hours from the point in time when the FOOD is removed from 5°C (41°F) or less cold holding temperature control; and (5) The FOOD in unmarked containers or PACKAGES, or marked with a time that exceeds the six-hour limit shall be discarded. (D) A FOOD ESTABLISHMENT that serves a HIGHLY SUSCEPTIBLE POPULATION may not use time as specified under ¶¶ (A), (B), or (C) of this section as the public health control for raw EGGS.

</details>


---

## q31 (multi)

**Question:** A cook switches from cutting raw chicken to making salads. Is changing gloves enough?

**Reference answer:** No. The gloves must be changed because single-use gloves are for one task only, and the cook must also wash hands when switching between raw food and ready-to-eat food and before putting on new gloves.

**Expected source:** food_code_2026 3-304.15;2-301.14

**Agent's answer:**

No, changing gloves is not enough. Food employees must clean their hands and exposed portions of their arms when switching between working with raw food and working with ready-to-eat food, and before donning gloves to initiate a task [Food Code 2026 §2-301.14]. The cook must remove the gloves, wash their hands, and then put on a new pair of clean single-use gloves before making salads. 

The version of the Food Code adopted by your state or local jurisdiction is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §2-301.14]** Source: FDA Food Code 2026, Chapters 1-6, §2-301.14 (p. 40). When to Wash
> FOOD EMPLOYEES shall clean their hands and exposed portions of their arms as SPECIFIED under § 2-301.12 immediately before engaging in FOOD preparation including working with exposed FOOD, clean EQUIPMENT and UTENSILS, and unwrapped SINGLE-SERVICE and SINGLE-USE ARTICLES and: (A) After touching bare human body parts other than clean hands and clean, exposed portions of arms; (B) After using the toilet room; (C) After caring for or handling SERVICE ANIMALS or aquatic animals as specified in ¶ 2-403.11(B); (D) Except as specified in ¶ 2-401.11(B), after coughing, sneezing, using a handkerchief or disposable tissue, using TOBACCO PRODUCTS, eating, or drinking; (E) After handling soiled EQUIPMENT or UTENSILS; (F) During FOOD preparation, as often as necessary to remove soil and contamination and to prevent cross contamination when changing tasks; (G) When switching between working with raw FOOD and working with READY-TO-EAT FOOD; (H) Before donning gloves to initiate a task that involves working with FOOD; and (I) After engaging in other activities that contaminate the hands.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-304.15]** Source: FDA Food Code 2026, Chapters 1-6, §3-304.15 (pp. 58-59). Gloves, Use Limitation (part 1)
> (A) Except as specified in ¶ (B) of this section, if used, single-use gloves shall be used for only one task such as working with READY-TO-EAT FOOD or with raw animal FOOD and used for no other purpose. (B) If APPROVED, FOOD EMPLOYEES may continue to use an interior single-use glove, provided the single-use interior glove is protected from contamination through the use of a task-specific loose-fitting exterior glove, if: (1) The method of removal of the exterior glove prevents contamination of the hands and the interior glove, and ensures that the hands and interior glove are not exposed to contamination during removal and discard, and (2) The exterior glove is sufficiently loose to allow removal by gravity, without contacting the interior glove and without requiring the exterior glove to be peeled off, and (3) If the exterior glove is single use only, it shall be immediately discarded in an appropriate waste container after use. (4) After exterior glove removal, the interior single-use glove remained intact with no tears or punctures, and free of contamination. (C) When in use, single-use gloves shall be discarded when damaged or soiled, or contaminated when interruptions occur in the operation. (D) Except as specified in ¶ (E) of this section, slash-resistant gloves that are used to protect the hands during operations requiring cutting shall be used in direct contact only with FOOD that is subsequently cooked as specified under Part 3-4 such as frozen FOOD or a PRIMAL CUT of MEAT. (E) Slash-resistant gloves may be used with READY-TO-EAT FOOD that will not be subsequently cooked if the slash-resistant gloves have a SMOOTH, durable, and nonabsorbent outer surface; or if the slash-resistant gloves are covered with a SMOOTH, durable, nonabsorbent glove, or a single-use glove.

> **[Food Code 2026 §4-802.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-802.11 (p. 113). Specifications
> (A) LINENS that do not come in direct contact with FOOD shall be laundered between operations if they become wet, sticky, or visibly soiled. (B) Cloth gloves used as specified in 3-304.15(F) shall be laundered before being used with a different type of raw animal FOOD such as beef, FISH, lamb, pork or POULTRY. (C) LINENS that are used as specified under § 3-304.13 and cloth napkins shall be laundered between each use. (D) Wet wiping cloths shall be laundered daily. (E) Dry wiping cloths shall be laundered as necessary to prevent contamination of FOOD and clean serving UTENSILS.

> **[Employee Health Handbook p. 14]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 14. When should food employees wash their hands?
> They should do this immediately after engaging in activities that contaminate the hands and: • When entering a food preparation area; • Before putting on clean, single-use gloves for working with food and between glove changes; • Before engaging in food preparation; • Before handling clean equipment and serving utensils; • When changing tasks and switching between handling raw foods and working with RTE foods; • After handling soiled dishes, equipment, or utensils; • After touching bare human body parts, for example, parts other than clean hands and clean, exposed portions of arms; • After using the toilet; • After coughing, sneezing, blowing the nose, using tobacco, eating, or drinking; and • After caring for or handling services animals or aquatic animals such as molluscan shellfish or crustacea in display tanks.

> **[Food Code 2026 §3-304.15]** Source: FDA Food Code 2026, Chapters 1-6, §3-304.15 (p. 59). Gloves, Use Limitation (part 2)
> (F) Cloth gloves may not be used in direct contact with FOOD unless the FOOD is subsequently cooked as required under Part 3-4 such as frozen FOOD or a PRIMAL CUT of MEAT.

</details>


---

## q32 (unanswerable)

**Question:** Can we store bleach and other cleaning chemicals on a shelf above the prep table?

**Reference answer:** The FDA documents I have do not cover this.

**Expected source:** - 

**Agent's answer:**

The FDA documents I have do not cover this. (I searched several times without finding a passage that answers it.)

**Passages the answer cites:**

> (the answer cites no passage)

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §4-401.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-401.11 (p. 101). Equipment, Clothes Washers and Dryers, and Storage Cabinets, Contamination Prevention
> (A) Except as specified in ¶ (B) of this section, EQUIPMENT, a cabinet used for the storage of FOOD, or a cabinet that is used to store cleaned and SANITIZED EQUIPMENT, UTENSILS, laundered LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES may not be located: (1) In locker rooms; (2) In toilet rooms; (3) In garbage rooms; (4) In mechanical rooms; (5) Under sewer lines that are not shielded to intercept potential drips; (6) Under leaking or where water is condensed on pipes, tubes, or hoses, including plumbing, heating, air conditioning and WATER-BASED FIRE PROTECTION SYSTEMS; (7) Under open stairwells; or (8) Under other sources of contamination. (B) A storage cabinet used for LINENS or SINGLE-SERVICE or SINGLE-USE ARTICLES may be stored in a locker room. (C) If a mechanical clothes washer or dryer is provided, it shall be located so that the washer or dryer is protected from contamination and only where there is no exposed FOOD; clean EQUIPMENT, UTENSILS, and LINENS; and unwrapped SINGLE-SERVICE and SINGLE-USE ARTICLES.

> **[Food Code 2026 §4-903.12]** Source: FDA Food Code 2026, Chapters 1-6, §4-903.12 (p. 115). Prohibitions
> (A) Except as specified in ¶ (B) of this section, cleaned and SANITIZED EQUIPMENT, UTENSILS, laundered LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES may not be stored: (1) In locker rooms; (2) In toilet rooms; (3) In garbage rooms; (4) In mechanical rooms; (5) Under sewer lines that are not shielded to intercept potential drips; (6) Under leaking or where water is condensed on pipes, tubes, or hoses, including plumbing, heating, air conditioning and WATER-BASED FIRE PROTECTION SYSTEMS; (7) Under open stairwells; or (8) Under other sources of contamination. (B) Laundered LINENS and SINGLE-SERVICE and SINGLE-USE ARTICLES that are PACKAGED or in a facility such as a cabinet may be stored in a locker room.

> **[Food Code 2026 §4-903.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-903.11 (pp. 114-115). Equipment, Utensils, Linens, and Single-Service and Single-Use Articles
> (A) Except as specified in ¶ (D) of this section, cleaned EQUIPMENT and UTENSILS, laundered LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES shall be stored: (1) In a clean, dry location; (2) Where they are not exposed to splash, dust, or other contamination; and (3) At least 15 cm (6 inches) above the floor. (B) Clean EQUIPMENT and UTENSILS shall be stored as specified under ¶ (A) of this section and shall be stored: (1) In a self-draining position that allows air drying; and (2) Covered or inverted. (C) SINGLE-SERVICE and SINGLE-USE ARTICLES shall be stored as specified under ¶ (A) of this section and shall be kept in the original protective PACKAGE or stored by using other means that afford protection from contamination until used. (D) Items that are kept in closed PACKAGES may be stored less than 15 cm (6 inches) above the floor on dollies, pallets, racks, and skids that are designed as specified under § 4-204.122.

> **[Food Code 2026 §6-501.113]** Source: FDA Food Code 2026, Chapters 1-6, §6-501.113 (p. 142). Storing Maintenance Tools
> Maintenance tools such as brooms, mops, vacuum cleaners, and similar items shall be: (A) Stored so they do not contaminate FOOD, EQUIPMENT, UTENSILS, LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES; and (B) Stored in an orderly manner that facilitates cleaning the area used for storing the maintenance tools.

> **[Food Code 2026 §6-501.15]** Source: FDA Food Code 2026, Chapters 1-6, §6-501.15 (p. 141). Cleaning Maintenance Tools, Preventing Contamination
> FOOD preparation sinks, HANDWASHING SINKS, and WAREWASHING EQUIPMENT may not be used for the cleaning of maintenance tools, the preparation or holding of maintenance materials, or the disposal of mop water and similar liquid wastes.

> **[Food Code 2026 §4-204.18]** Source: FDA Food Code 2026, Chapters 1-6, §4-204.18 (p. 94). Condenser Unit, Separation
> If a condenser unit is an integral component of EQUIPMENT, the condenser unit shall be separated from the FOOD and FOOD storage space by a dustproof barrier.

> **[Food Code 2026 §3-302.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-302.11 (pp. 54-55). Packaged and Unpackaged Food - Separation, Packaging, and Segregation (part 1)
> (A) FOOD shall be protected from cross contamination by: (1) Except as specified in (1)(d) below or when combined as ingredients, separating raw animal FOODS during storage, preparation, holding, and display from: (a) Raw READY-TO-EAT FOOD including other raw animal FOOD such as FISH for sushi or MOLLUSCAN SHELLFISH, or other raw READY-TO-EAT FOOD such as fruits and vegetables; (b) Cooked READY-TO-EAT FOOD; and (c) Fruits and vegetables before they are washed; (d) Frozen, commercially processed and PACKAGED raw animal FOOD may be stored or displayed with or above frozen, commercially processed and PACKAGED, READY-TO-EAT FOOD. (2) Except when combined as ingredients, separating types of raw animal FOODS from each other such as beef, FISH, lamb, pork, and POULTRY during storage, preparation, holding, and display by: (a) Using separate EQUIPMENT for each type; or (b) Arranging each type of FOOD in EQUIPMENT so that cross contamination of one type with another is prevented; and (c) Preparing each type of FOOD at different times or in separate areas; (3) Cleaning EQUIPMENT and UTENSILS as specified under ¶ 4-602.11(A) and SANITIZING as specified under § 4-703.11; (4) Except as specified under Subparagraph 3-501.15(B)(2) and in ¶ (B) of this section, storing the FOOD in PACKAGES, covered containers, or wrappings; (5) Cleaning HERMETICALLY SEALED CONTAINERS of FOOD of visible soil before opening; (6) Protecting FOOD containers that are received PACKAGED together in a case or overwrap from cuts when the case or overwrap is opened; (7) Storing damaged, spoiled, or recalled FOOD being held in the FOOD ESTABLISHMENT as specified under § 6-404.11; and (8) Separating fruits and vegetables, before they are washed as specified under § 3-302.15 from READY-TO-EAT FOOD. (B) Subparagraph (A)(4) of this section does not apply to:

> **[Food Code 2026 §4-402.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-402.11 (pp. 101-102). Fixed Equipment, Spacing or Sealing
> (A) EQUIPMENT that is fixed because it is not EASILY MOVABLE shall be installed so that it is: (1) Spaced to allow access for cleaning along the sides, behind, and above the EQUIPMENT; (2) Spaced from adjoining EQUIPMENT, walls, and ceilings not more than one millimeter or one thirty-second inch; or (3) SEALED to adjoining EQUIPMENT or walls if the EQUIPMENT is exposed to spillage or seepage. (B) COUNTER-MOUNTED EQUIPMENT that is not EASILY MOVABLE shall be installed to allow cleaning of the EQUIPMENT and areas underneath and around the EQUIPMENT by being: (1) SEALED; or (2) Elevated on legs as specified under ¶ 4-402.12(D).

> **[Food Code 2026 §6-404.11]** Source: FDA Food Code 2026, Chapters 1-6, §6-404.11 (p. 140). Segregation and Location
> Products that are held by the PERMIT HOLDER for credit, redemption, or return to the distributor, such as damaged, spoiled, or recalled products, shall be segregated and held in designated areas that are separated from FOOD, EQUIPMENT, UTENSILS, LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES.

> **[Food Code 2026 §3-305.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-305.11 (p. 60). Food Storage
> (A) Except as specified in ¶¶ (B) and (C) of this section, FOOD shall be protected from contamination by storing the FOOD: (1) In a clean, dry location; (2) Where it is not exposed to splash, dust, or other contamination; and (3) At least 15 cm (6 inches) above the floor. (B) FOOD in packages and working containers may be stored less than 15 cm (6 inches) above the floor on case lot handling EQUIPMENT as specified under § 4-204.122. (C) Pressurized BEVERAGE containers, cased FOOD in waterproof containers such as bottles or cans, and milk containers in plastic crates may be stored on a floor that is clean and not exposed to floor moisture.

> **[Food Code 2026 §5-501.19]** Source: FDA Food Code 2026, Chapters 1-6, §5-501.19 (pp. 130-131). Storage Areas, Redeeming Machines, Receptacles and Waste Handling Units, Location
> (A) An area designated for REFUSE, recyclables, returnables, and, except as specified in ¶ (B) of this section, a redeeming machine for recyclables or returnables shall be located so that it is separate from FOOD, EQUIPMENT, UTENSILS, LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES and a public health HAZARD or nuisance is not created. (B) A redeeming machine may be in the PACKAGED FOOD storage area or CONSUMER area of a FOOD ESTABLISHMENT if FOOD, EQUIPMENT, UTENSILS, LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES are not subject to contamination from the machines and a public health HAZARD or nuisance is not created. (C) The location of receptacles and waste handling units for REFUSE, recyclables, and returnables may not create a public health HAZARD or nuisance or interfere with the cleaning of adjacent space. Operation and maintenance

> **[Food Code 2026 §5-501.110]** Source: FDA Food Code 2026, Chapters 1-6, §5-501.110 (p. 131). Storing Refuse, Recyclables, and Returnables
> REFUSE, recyclables, and returnables shall be stored in receptacles or waste handling units so that they are inaccessible to insects and rodents.

> **[Food Code 2026 §3-302.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-302.11 (p. 55). Packaged and Unpackaged Food - Separation, Packaging, and Segregation (part 2)
> (1) Whole, uncut, raw fruits and vegetables and nuts in the shell, that require peeling or hulling before consumption; (2) PRIMAL CUTS, quarters, or sides of raw MEAT or slab bacon that are hung on clean, SANITIZED hooks or placed on clean, SANITIZED racks; (3) Whole, uncut, processed MEATS such as country hams, and smoked or cured sausages that are placed on clean, SANITIZED racks; (4) FOOD being cooled as specified under Subparagraph 3-501.15(B)(2); or (5) SHELLSTOCK.

> **[Food Code 2026 §6-202.112]** Source: FDA Food Code 2026, Chapters 1-6, §6-202.112 (p. 137). Living or Sleeping Quarters, Separation
> Living or sleeping quarters located on the PREMISES of a FOOD ESTABLISHMENT such as those provided for lodging registration clerks or resident managers shall be separated from rooms and areas used for FOOD ESTABLISHMENT operations by complete partitioning and solid self-closing doors.

> **[Food Code 2026 §3-305.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-305.12 (pp. 60-61). Food Storage, Prohibited Areas
> FOOD may not be stored: (A) In locker rooms; (B) In toilet rooms; (C) In dressing rooms; (D) In garbage rooms; (E) In mechanical rooms; (F) Under sewer lines that are not shielded to intercept potential drips; (G) Under leaking or where water is condensed on pipes, tubes, or hoses, including plumbing, heating, air conditioning and WATER-BASED FIRE PROTECTION SYSTEMS: (H) Under open stairwells; or (I) Under other sources of contamination.

> **[Food Code 2026 §6-403.11]** Source: FDA Food Code 2026, Chapters 1-6, §6-403.11 (p. 140). Designated Areas
> (A) Areas designated for EMPLOYEES to eat, drink, and use TOBACCO PRODUCTS shall be located so that FOOD, EQUIPMENT, LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES are protected from contamination. (B) Lockers or other suitable facilities shall be in a designated room or area where contamination of FOOD, EQUIPMENT, UTENSILS, LINENS, and SINGLE-SERVICE and SINGLE-USE ARTICLES cannot occur.

</details>


---

## q33 (unanswerable)

**Question:** How often will the health inspector come to inspect our restaurant?

**Reference answer:** The FDA documents I have do not cover this.

**Expected source:** - 

**Agent's answer:**

The FDA documents I have do not cover this. You can check your local health department or inspector to find out how often inspections occur.

**Passages the answer cites:**

> (the answer cites no passage)

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §5-502.11]** Source: FDA Food Code 2026, Chapters 1-6, §5-502.11 (p. 132). Frequency
> REFUSE, recyclables, and returnables shall be removed from the PREMISES at a frequency that will minimize the development of objectionable odors and other conditions that attract or harbor insects and rodents.

> **[Food Code 2026 §6-501.12]** Source: FDA Food Code 2026, Chapters 1-6, §6-501.12 (pp. 140-141). Cleaning, Frequency and Restrictions
> (A) PHYSICAL FACILITIES shall be cleaned as often as necessary to keep them clean. (B) Except for cleaning that is necessary due to a spill or other accident, cleaning shall be done during periods when the least amount of FOOD is exposed such as after closing.

> **[Food Code 2026 §5-205.13]** Source: FDA Food Code 2026, Chapters 1-6, §5-205.13 (p. 124). Scheduling Inspection and Service for a Water System Device
> A device such as a water treatment device or backflow preventer shall be scheduled for inspection and service, in accordance with manufacturer's instructions and as necessary to prevent device failure based on local water conditions, and records demonstrating inspection and service shall be maintained by the PERSON IN CHARGE.

> **[Food Code 2026 §4-501.14]** Source: FDA Food Code 2026, Chapters 1-6, §4-501.14 (p. 103). Warewashing Equipment, Cleaning Frequency
> A WAREWASHING machine; the compartments of sinks, basins, or other receptacles used for washing and rinsing EQUIPMENT, UTENSILS, or raw FOODS, or laundering wiping cloths; and drainboards or other EQUIPMENT used to substitute for drainboards as specified under § 4-301.13 shall be cleaned: (A) Before use; (B) Throughout the day at a frequency necessary to prevent recontamination of EQUIPMENT and UTENSILS and to ensure that the EQUIPMENT performs its intended function; and (C) If used, at least every 24 hours.

> **[Food Code 2026 §4-602.12]** Source: FDA Food Code 2026, Chapters 1-6, §4-602.12 (p. 109). Cooking and Baking Equipment
> (A) The FOOD-CONTACT SURFACES of cooking and baking EQUIPMENT shall be cleaned at least every 24 hours. This section does not apply to hot oil cooking and filtering EQUIPMENT if it is cleaned as specified in Subparagraph 4-602.11(D)(6). (B) The cavities and door seals of microwave ovens shall be cleaned at least every 24 hours by using the manufacturer's recommended cleaning procedure.

</details>


---

## q34 (unanswerable)

**Question:** How much does a food establishment permit cost?

**Reference answer:** The FDA documents I have do not cover this.

**Expected source:** - 

**Agent's answer:**

The FDA documents I have do not cover this. You could check your local health department instead.

**Passages the answer cites:**

> (the answer cites no passage)

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §1-103.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-103.10 (p. 1). Statement
> This Code establishes definitions; sets standards for management and personnel, FOOD operations, and EQUIPMENT and facilities; and provides for FOOD ESTABLISHMENT plan review, PERMIT issuance, inspection, EMPLOYEE RESTRICTION, and PERMIT suspension.

> **[Food Code 2026 §2-101.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-101.11 (p. 23). Assignment
> (A) Except as specified in ¶¶ (B) and (C) of this section, the PERMIT HOLDER shall be the PERSON IN CHARGE or shall designate a PERSON IN CHARGE and shall ensure that a PERSON IN CHARGE is present at the FOOD ESTABLISHMENT during all hours of operation. (B) In a FOOD ESTABLISHMENT with two or more separately PERMITTED departments that are the legal responsibility of the same PERMIT HOLDER and that are located on the same PREMISES, the PERMIT HOLDER may, during specific time periods when FOOD is not being prepared, PACKAGED, or served, designate a single PERSON IN CHARGE who is present on the PREMISES during all hours of operation, and who is responsible for each separately PERMITTED FOOD ESTABLISHMENT on the PREMISES. (C) This section does not apply to certain types of FOOD ESTABLISHMENTs deemed by the REGULATORY AUTHORITY to pose minimal RISK of causing, or contributing to, foodborne illness based on the nature of the operation and extent of the FOOD preparation.

> **[Food Code 2026 §2-102.12]** Source: FDA Food Code 2026, Chapters 1-6, §2-102.12 (pp. 25-26). Certified Food Protection Manager
> (A) The PERSON IN CHARGE shall be a certified FOOD protection manager who has shown proficiency of required information through passing a test that is part of an ACCREDITED PROGRAM. (B) This section does not apply to certain types of FOOD ESTABLISHMENTS deemed by the REGULATORY AUTHORITY to pose minimal RISK of causing, or contributing to, foodborne illness based on the nature of the operation and extent of FOOD preparation.

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 8-9). Statement of Application and Listing of Terms (part 9)
> (3) "Food establishment" does not include: (a) An establishment that offers only pre-PACKAGED FOODS that are not TIME/TEMPERATURE CONTROL FOR SAFETY FOODS; (b) A produce stand that only offers whole, uncut fresh fruits and vegetables; (c) A FOOD PROCESSING PLANT; including those that are located on the PREMISES of a FOOD ESTABLISHMENT; (d) A kitchen in a private home if only FOOD that is not TIME/TEMPERATURE CONTROL FOR SAFETY FOOD, is prepared for sale or service at a function such as a religious or charitable organization’s bake sale if allowed by LAW and if the CONSUMER is informed by a clearly visible placard at the sales or service location that the FOOD is prepared in a kitchen that is not subject to regulation and inspection by the REGULATORY AUTHORITY; (e) An area where FOOD that is prepared as specified in Subparagraph (3)(d) of this definition is sold or offered for human consumption; (f) A kitchen in a private home, such as a small family day-care provider; or a bed-and-breakfast operation that prepares and offers FOOD to guests if the home is owner occupied, the number of available guest bedrooms does not exceed 6, breakfast is the only meal offered, the number of guests served does not exceed 18, and the CONSUMER is informed by statements contained in published advertisements, mailed brochures, and placards posted at the registration area that the FOOD is prepared in a kitchen that is not regulated and inspected by the REGULATORY AUTHORITY; or (g) A private home that receives catered or home-delivered FOOD. Food Processing Plant. (1) "Food processing plant" means a commercial operation that manufactures, PACKAGES, labels, or stores FOOD for human consumption, and provides FOOD for sale or distribution to other business entities such as FOOD PROCESSING PLANTS or FOOD ESTABLISHMENTS.

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 7-8). Statement of Application and Listing of Terms (part 8)
> (1) A surface of EQUIPMENT or a UTENSIL with which FOOD normally comes into contact; or (2) A surface of EQUIPMENT or a UTENSIL from which FOOD may drain, drip, or splash: (a) Into a FOOD, or (b) Onto a surface normally in contact with FOOD. "Food defense" is the effort to protect FOOD from acts of intentional ADULTERATION or tampering. "Food employee" means an individual working with unPACKAGED FOOD, FOOD EQUIPMENT or UTENSILS, or FOOD-CONTACT SURFACES. Food Establishment. (1) "Food establishment" means an operation that: (a) Stores, prepares, PACKAGES, serves, vends FOOD directly to the CONSUMER, or otherwise provides FOOD for human consumption such as a restaurant; satellite or catered feeding location; commissary, catering operation if the operation provides FOOD directly to a CONSUMER or to a conveyance used to transport people; market; vending location; conveyance used to transport people; institution; or FOOD bank; and (b) Relinquishes possession of FOOD to a CONSUMER directly, or indirectly through a delivery service such as home delivery of grocery orders or restaurant takeout orders, or delivery service that is provided by common carriers. (2) "Food establishment" includes: (a) An element of the operation such as a transportation vehicle or a central preparation facility that supplies a vending location or satellite feeding location unless the vending or feeding location is PERMITTED by the REGULATORY AUTHORITY; and (b) An operation that is conducted in a mobile, stationary, temporary, or permanent facility or location; where consumption is on or off the PREMISES; and regardless of whether there is a charge for the FOOD.

</details>


---

## q35 (unanswerable)

**Question:** Do our servers need a food handler card in California?

**Reference answer:** The FDA documents I have do not cover this.

**Expected source:** - 

**Agent's answer:**

The FDA documents I have do not cover this. You could check with your local health department, the food safety inspector, or the full Food Code instead.

**Passages the answer cites:**

> (the answer cites no passage)

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §2-102.12]** Source: FDA Food Code 2026, Chapters 1-6, §2-102.12 (pp. 25-26). Certified Food Protection Manager
> (A) The PERSON IN CHARGE shall be a certified FOOD protection manager who has shown proficiency of required information through passing a test that is part of an ACCREDITED PROGRAM. (B) This section does not apply to certain types of FOOD ESTABLISHMENTS deemed by the REGULATORY AUTHORITY to pose minimal RISK of causing, or contributing to, foodborne illness based on the nature of the operation and extent of FOOD preparation.

> **[Food Code 2026 §2-102.20]** Source: FDA Food Code 2026, Chapters 1-6, §2-102.20 (p. 26). Food Protection Manager Certification
> (A) A PERSON IN CHARGE who demonstrates knowledge by being a FOOD protection manager that is certified by a FOOD protection manager certification program that is evaluated and listed by a Conference for FOOD Protection-recognized accrediting agency as conforming to the Conference for Food Protection Standard for Accreditation of Food Protection Manager Certification Programs is deemed to comply with ¶ 2-102.11(B). (B) A FOOD ESTABLISHMENT that has a PERSON IN CHARGE that is certified by a FOOD protection manager certification program that is evaluated and listed by a Conference for Food Protection-recognized accrediting agency as conforming to the Conference for Food Protection Standard for Accreditation of Food Protection Manager Certification Programs is deemed to comply with § 2-102.12.

> **[Employee Health Handbook p. 25]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 25. Form 1-C Conditional Employee or Food Employee Medical Referral (part 1)
> Preventing Transmission of Diseases through Food by Infected Food Employees with Emphasis on Illness due to Norovirus, Typhoid Fever (Salmonella Typhi), Shigellosis (Shigella spp.), Escherichia coli O157:H7 or other Shiga Toxin-producing Escherichia coli (STEC), nontyphoidal Salmonella and Hepatitis A Virus. The Food Code specifies, under Part 2-2 Employee Health Subpart 2-201 Disease or Medical Condition, that Conditional Employees and Food Employees obtain medical clearance from a health practitioner licensed to practice medicine, unless the Food Employees have complied with the provisions specified as an alternative to providing medical documentation, whenever the individual: 1. Is chronically suffering from a symptom such as diarrhea; or 2. Has a current illness involving Norovirus, typhoid fever (Salmonella Typhi), shigellosis (Shigella spp.), E. coli O157:H7 infection (or other STEC), nontyphoidal Salmonella or hepatitis A virus (hepatitis A), or 3. Reports past illness involving typhoid fever (S. Typhi) within the past three months (while salmonellosis is fairly common in the U.S., typhoid fever, caused by infection with S. Typhi, is rare). Conditional employee being referred: (Name, please print) Food Employee being referred: (Name, please print)

> **[Employee Health Handbook p. 7]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 7. Can food employees work if their symptoms are from a non-infectious condition?
> Yes, food employees can work as long as they can provide medical documentation indicating that the symptoms are from a non-infectious condition. Some non-infectious conditions include Crohn’s disease (an ongoing disorder that causes inflammation of the gastrointestinal system), irritable bowel syndrome, some liver diseases, and symptoms commonly experienced during stages of pregnancy.

> **[Employee Health Handbook p. 4]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 4. What should food employees do if they have a sore throat with fever?
> Report the illness to the manager and, if possible, continue working while remaining aware that the manager could consider reassignment to a position that does not include the handling of food, food-contact equipment, utensils, or single-service articles. If the employee works in a food establishment serving an HSP , such as a hospital, nursing home, assisted living facility, or a day care center, the employee must stop working and go home until obtaining a clearance from a health practitioner and presenting it to the manager.

</details>


---

## q36 (unanswerable)

**Question:** How many days of sick pay do we have to give a cook we send home with vomiting?

**Reference answer:** The FDA documents I have do not cover this.

**Expected source:** - 

**Agent's answer:**

The FDA documents I have do not cover this. You can check your local labor department or human resources guidelines for rules on sick pay.

**Passages the answer cites:**

> (the answer cites no passage)

<details><summary>Other retrieved passages</summary>

> **[Employee Health Handbook p. 4]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 4. What should food employees do when they have symptoms of vomiting or diarrhea?
> If at work: • Stop work immediately; • Report to management; and • Go home and return after at least 24 hours have passed since the vomiting and diarrhea symptoms ended. If the symptoms occur before the employee arrives to work, he or she should: • Notify the manager by telephone; and • Do not report to work until at least 24 hours have passed after the diarrhea and vomiting symptoms have ended.

> **[Employee Health Handbook p. 5]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 5. What should a manager do when a food employee reports symptoms of vomiting or diarrhea? (See Decision Tree 1 and Table 1a (and Table 1b if diagnosed))
> Ask the food employee to stop work immediately and leave the food establishment. Permit a return to work no sooner than 24 hours after vomiting and diarrhea have ended. Employee Health Management Responsibilities

> **[Employee Health Handbook p. 29]** Source: FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020), p. 29. 2-201.12 Table 1a Summary of Requirements for Symptomatic Food Employees
> Food employees and conditional employees shall report symptoms immediately to the person in charge The person in charge shall prohibit a conditional employee who reports a listed symptom from becoming a food employee until meeting the criteria listed in section 2-201.13 of the Food Code, for reinstatement of a symptomatic food employee. Symptom Exclusion or Restriction (Facilities Serving an HSP) Exclusion or Restriction (Facilities Not Serving an HSP) Removing Symptomatic Food Employees from Exclusion or Restriction RA Approval Required to Return to Work? Vomiting Exclude 2-201.12(A)(1) Exclude 2-201.12(A)(1) When the excluded food employee has been asymptomatic for at least 24 hours or provides medical documentation 2-201.13(A)(1). Exceptions: If diagnosed with Norovirus, Shigella spp., STEC, HAV, or typhoid fever (S. Typhi) (see Tables 1b and 2). No, if not diagnosed Diarrhea Exclude 2-201.12(A)(1) Exclude 2-201.12(A)(1) When the excluded food employee has been asymptomatic for at least 24 hours or provides medical documentation 2-201.13(A). Exceptions: If Diagnosed with Norovirus, STEC, HAV, or S. Typhi (see Tables 1b and 2). No, if not diagnosed Jaundice Exclude 2-201.12(B)(1) if the onset occurred within the last 7 days Exclude 2-201.12(B)(1) if the onset occurred within the last 7 days When approval is obtained from the RA 2-201.13(B), and: • Food employee has been jaundiced for more than 7 calendar days 2-201.13(B)(1), or • Food employee provides medical documentation 2-201.13(B)(3). Yes Sore Throat with Fever Exclude 2-201.12(G)(1) Restrict 2-201.12(G)(2) When food employee provides written medical documentation 2-201.13(G) (1)-(3). No Infected Wound or Pustular Boil Restrict 2-201.12(I) Restrict 2-201.12(I) When the infected wound or boil is properly covered 2-201.13(I)(1)-(3). No Key: Table 1a RA = Regulatory Authority STEC = Shiga toxin-producing Escherichia coli HAV = Hepatitis A virus HSP = Highly Susceptible Population

> **[Food Code 2026 §2-501.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-501.11 (pp. 43-44). Employee Illness Policy Documentation
> (A) The PERMIT HOLDER shall provide a written EMPLOYEE Illness Policy, available upon request; and (B) The EMPLOYEE Illness Policy shall include the following procedures addressing reporting and compliance requirements for FOOD EMPLOYEES, CONDITIONAL EMPLOYEES, the PERSON-IN-CHARGE, and required reporting to the REGULATORY AUTHORITY: (1) Illness symptoms of diarrhea, vomiting, sore throat with fever, jaundice or infected wounds or cuts; (2) Illness disease diagnosis due to norovirus, hepatitis A virus, Shigella spp., Typhoid fever, non-typhoidal Salmonella, or SHIGA TOXIN-PRODUCING ESCHERICHIA COLI; and (3) Illness EXCLUSION and/or RESTRICTION and reinstatement after illness symptom or disease resolution.

> **[Food Code 2026 §2-502.11]** Source: FDA Food Code 2026, Chapters 1-6, §2-502.11 (p. 44). Clean-up of Vomiting and Diarrheal Events
> A FOOD ESTABLISHMENT shall have written procedures for EMPLOYEES to follow when responding to vomiting or diarrheal events that involve the discharge of vomitus or fecal matter onto surfaces in the FOOD ESTABLISHMENT. The procedures shall address the specific actions EMPLOYEES must take to minimize the spread of contamination and the exposure of EMPLOYEES, CONSUMERS, FOOD and surfaces to vomitus or fecal matter.

</details>


---

## q37 (unanswerable)

**Question:** Do we have to show calorie counts on our menu?

**Reference answer:** The FDA documents I have do not cover this.

**Expected source:** - 

**Agent's answer:**

Food packaged in a food establishment requires nutrition labeling as specified in 21 CFR 101 and 9 CFR 317 Subpart B, except as exempted in the Federal Food, Drug, and Cosmetic Act § 403(q)(3) – (5) [Food Code 2026 §3-602.11].

**Passages the answer cites:**

> **[Food Code 2026 §3-602.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.11 (pp. 80-81). Food Labels (part 1)
> (A) FOOD PACKAGED in a FOOD ESTABLISHMENT, shall be labeled as specified in LAW, including 21 CFR 101 - Food labeling, and 9 CFR 317 Labeling, marking devices, and containers. (B) Label information shall include: (1) The common name of the FOOD, or absent a common name, an adequately descriptive identity statement; (2) If made from two or more ingredients, a list of ingredients and sub-ingredients in descending order of predominance by weight, including a declaration of artificial colors, artificial flavors and chemical preservatives, if contained in the FOOD; (3) An accurate declaration of the net quantity of contents; (4) The name and place of business of the manufacturer, packer, or distributor; and (5) The name of the FOOD source for each MAJOR FOOD ALLERGEN contained in the FOOD unless the FOOD source is already part of the common or usual name of the respective ingredient. (6) Except as exempted in the Federal Food, Drug, and Cosmetic Act § 403(q)(3) - (5), nutrition labeling as specified in 21 CFR 101 - Food Labeling and 9 CFR 317 Subpart B Nutrition Labeling. (7) For any salmonid containing canthaxanthin or astaxanthin as a COLOR ADDITIVE, the labeling of the bulk FISH container, including a list of ingredients, displayed on the retail container or by other written means, such as a counter card, that discloses the use of canthaxanthin or astaxanthin. (C) Bulk FOOD that is available for CONSUMER self-dispensing shall be prominently labeled with the following information in plain view of the CONSUMER: (1) The manufacturer's or processor's label that was provided with the FOOD; or (2) A card, sign, or other method of notification that includes the information specified under Subparagraphs (B)(1), (2), (5), and (6) of this section.

> **[Food Code 2026 §3-602.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.11 (p. 81). Food Labels (part 2)
> (D) Bulk, unPACKAGED FOODS such as bakery products and unPACKAGED FOODS that are portioned to CONSUMER specification need not be labeled if: . (1) A health, nutrient content, or other claim is not made; (2) There are no state or local LAWS requiring labeling; and (3) The FOOD is manufactured or prepared on the PREMISES of the FOOD ESTABLISHMENT or at another FOOD ESTABLISHMENT or a FOOD PROCESSING PLANT that is owned by the same PERSON and is regulated by the FOOD regulatory agency that has jurisdiction.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §4-502.11]** Source: FDA Food Code 2026, Chapters 1-6, §4-502.11 (p. 106). Good Repair and Calibration
> (A) UTENSILS shall be maintained in a state of repair or condition that complies with the requirements specified under Parts 4-1 and 4-2 or shall be discarded. (B) FOOD TEMPERATURE MEASURING DEVICES shall be calibrated in accordance with manufacturer's specifications as necessary to ensure their accuracy. (C) Ambient air temperature, water pressure, and water TEMPERATURE MEASURING DEVICES shall be maintained in good repair and be accurate within the intended range of use.

> **[Food Code 2026 §3-501.17]** Source: FDA Food Code 2026, Chapters 1-6, §3-501.17 (p. 74). Ready-to-Eat, Time/Temperature Control for Safety Food, Date Marking (part 3)
> (2) Hard cheeses containing not more than 39% moisture as defined in 21 CFR 133 Cheeses and related cheese products, such as cheddar, gruyere, parmesan and reggiano, and romano; (3) Semi-soft cheeses containing more than 39% moisture, but not more than 50% moisture, as defined in 21 CFR 133 Cheeses and related cheese products, such as blue, edam, gorgonzola, gouda, and monterey jack; (4) Cultured dairy products as defined in 21 CFR 131 Milk and cream, such as yogurt, sour cream, and buttermilk; (5) Preserved FISH products, such as pickled herring and dried or salted cod, and other acidified FISH products defined in 21 CFR 114 Acidified FOODS; (6) Shelf stable, dry fermented sausages, such as pepperoni and Genoa; and (7) Shelf stable salt-cured products such as prosciutto and Parma (ham).

> **[Food Code 2026 §3-302.13]** Source: FDA Food Code 2026, Chapters 1-6, §3-302.13 (p. 56). Pasteurized Eggs, Substitute for Raw Eggs for Certain Recipes
> Pasteurized EGGS or EGG PRODUCTS shall be substituted for raw EGGS in the preparation of FOODS such as Caesar salad, hollandaise or Béarnaise sauce, mayonnaise, meringue, eggnog, ice cream, and EGG-fortified BEVERAGES that are not: (A) Cooked as specified under Subparagraphs 3-401.11(A)(1) or (2); or (B) Included in ¶ 3-401.11(D).

> **[Food Code 2026 §3-603.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-603.11 (p. 82). Consumption of Animal Foods that are Raw, Undercooked, or Not Otherwise Processed to Eliminate Pathogens
> (A) Except as specified in ¶ 3-401.11(C) and Subparagraph 3-401.11(D)(4) and under ¶ 3-801.11(C), if an animal FOOD such as beef, EGGS, FISH, lamb, milk, pork, POULTRY, or shellfish is served or sold raw, undercooked, or without otherwise being processed to eliminate pathogens, either in READY-TO-EAT form or as an ingredient in another READY-TO-EAT FOOD, the PERMIT HOLDER shall inform CONSUMERS of the significantly increased RISK of consuming such FOODS by way of a DISCLOSURE and REMINDER, as specified in ¶¶ (B) and (C) of this section using brochures, deli case or menu advisories, label statements, table tents, placards, or other effective written means. (B) DISCLOSURE shall include: (1) A description of the animal-derived FOODS, such as “oysters on the half shell (raw oysters) ,” “raw-EGG Caesar salad,” and “hamburgers (can be cooked to order)”; or (2) Identification of the animal-derived FOODS by asterisking them to a footnote that states that the items are served raw or undercooked, or contain (or may contain) raw or undercooked ingredients. (C) REMINDER shall include asterisking the animal-derived FOODS requiring DISCLOSURE to a footnote that states: (1) Regarding the safety of these items, written information is available upon request; (2) Consuming raw or undercooked MEATS, POULTRY, seafood, shellfish, or EGGS may increase your RISK of foodborne illness; or (3) Consuming raw or undercooked MEATS, POULTRY, seafood, shellfish, or EGGS may increase your RISK of foodborne illness, especially if you have certain medical conditions.

> **[Food Code 2026 §3-602.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-602.12 (pp. 81-82). Other Forms of Information
> (A) If required by LAW, CONSUMER warnings shall be provided. (B) FOOD ESTABLISHMENT or manufacturers' dating information on FOODS may not be concealed or altered. (C) The PERMIT HOLDER shall notify CONSUMERS by written notification of the presence of MAJOR FOOD ALLERGENS as an ingredient in unPACKAGED FOOD items that are served or sold to the CONSUMER.

> **[Food Code 2026 §3-201.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-201.11 (p. 46). Compliance with Food Law (part 2)
> (F) MEAT and POULTRY that is not a READY-TO-EAT FOOD and is in a PACKAGED form when it is offered for sale or otherwise offered for consumption, shall be labeled to include safe handling instructions as specified in LAW, including 9 CFR 317.2(l) and 9 CFR 381.125(b). (G) EGGS that have not been specifically treated to destroy all viable Salmonellae shall be labeled to include safe handling instructions as specified in LAW, including 21 CFR 101.17(h).

> **[Food Code 2026 §3-601.12]** Source: FDA Food Code 2026, Chapters 1-6, §3-601.12 (p. 80). Honestly Presented
> (A) FOOD shall be offered for human consumption in a way that does not mislead or misinform the CONSUMER. (B) FOOD or COLOR ADDITIVES, colored overwraps, or lights may not be used to misrepresent the true appearance, color, or quality of a FOOD.

</details>


---

## q38 (unanswerable)

**Question:** Can I sell meals I cook in my home kitchen under my state's cottage food law?

**Reference answer:** The FDA documents I have do not cover this.

**Expected source:** - 

**Agent's answer:**

A private home may not be used for conducting food establishment operations [Food Code 2026 §6-202.111], and food prepared in a private home may not be used or offered for human consumption in a food establishment [Food Code 2026 §3-201.11]. However, a kitchen in a private home is not considered a food establishment if only non-TCS (Time/Temperature Control for Safety) food is prepared for sale at specific events like a bake sale, or under certain limited conditions for bed-and-breakfasts or day-care providers [Food Code 2026 §1-201.10]. 

The version of the Food Code adopted by your state or city is what applies.

**Passages the answer cites:**

> **[Food Code 2026 §6-202.111]** Source: FDA Food Code 2026, Chapters 1-6, §6-202.111 (p. 137). Private Homes and Living or Sleeping Quarters, Use Prohibition
> A private home, a room used as living or sleeping quarters, or an area directly opening into a room used as living or sleeping quarters may not be used for conducting FOOD ESTABLISHMENT operations.

> **[Food Code 2026 §1-201.10]** Source: FDA Food Code 2026, Chapters 1-6, §1-201.10 (pp. 8-9). Statement of Application and Listing of Terms (part 9)
> (3) "Food establishment" does not include: (a) An establishment that offers only pre-PACKAGED FOODS that are not TIME/TEMPERATURE CONTROL FOR SAFETY FOODS; (b) A produce stand that only offers whole, uncut fresh fruits and vegetables; (c) A FOOD PROCESSING PLANT; including those that are located on the PREMISES of a FOOD ESTABLISHMENT; (d) A kitchen in a private home if only FOOD that is not TIME/TEMPERATURE CONTROL FOR SAFETY FOOD, is prepared for sale or service at a function such as a religious or charitable organization’s bake sale if allowed by LAW and if the CONSUMER is informed by a clearly visible placard at the sales or service location that the FOOD is prepared in a kitchen that is not subject to regulation and inspection by the REGULATORY AUTHORITY; (e) An area where FOOD that is prepared as specified in Subparagraph (3)(d) of this definition is sold or offered for human consumption; (f) A kitchen in a private home, such as a small family day-care provider; or a bed-and-breakfast operation that prepares and offers FOOD to guests if the home is owner occupied, the number of available guest bedrooms does not exceed 6, breakfast is the only meal offered, the number of guests served does not exceed 18, and the CONSUMER is informed by statements contained in published advertisements, mailed brochures, and placards posted at the registration area that the FOOD is prepared in a kitchen that is not regulated and inspected by the REGULATORY AUTHORITY; or (g) A private home that receives catered or home-delivered FOOD. Food Processing Plant. (1) "Food processing plant" means a commercial operation that manufactures, PACKAGES, labels, or stores FOOD for human consumption, and provides FOOD for sale or distribution to other business entities such as FOOD PROCESSING PLANTS or FOOD ESTABLISHMENTS.

> **[Food Code 2026 §3-201.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-201.11 (pp. 45-46). Compliance with Food Law (part 1)
> (A) FOOD shall be obtained from sources that comply with LAW. (B) FOOD prepared in a private home may not be used or offered for human consumption in a FOOD ESTABLISHMENT. (C) PACKAGED FOOD shall be labeled as specified in LAW, including 21 CFR 101 FOOD Labeling, 9 CFR 317 Labeling, Marking Devices, and Containers, and 9 CFR 381 Subpart N Labeling and Containers, and as specified under § 3-202.18. (D) FISH, other than those specified in ¶ 3-402.11(B), that are intended for consumption in raw or undercooked form and allowed as specified in ¶ 3-401.11(D), may be offered for sale or service if they are obtained from a supplier that freezes the FISH, as specified under § 3-402.11; or if they are frozen on the PREMISES as specified under § 3-402.11 and records are retained as specified under § 3-402.12. (E) WHOLE-MUSCLE, INTACT BEEF steaks that are intended for consumption in an undercooked form without a CONSUMER advisory as specified in ¶ 3-401.11(C) shall be: (1) Obtained from a FOOD PROCESSING PLANT that does not MECHANICALLY TENDERIZE, vacuum tumble with solutions, reconstruct, cube or pound these WHOLE-MUSCLE, INTACT BEEF steaks; or (2) Deemed acceptable by the REGULATORY AUTHORITY based on other evidence, such as written buyer specifications or invoices, that indicates that the steaks meet the definition of WHOLE-MUSCLE, INTACT BEEF; and (3) If individually cut in a FOOD ESTABLISHMENT: (a) Cut from WHOLE-MUSCLE, INTACT BEEF that is received from a FOOD PROCESSING PLANT as specified in Subparagraph (E)(1) of this section or identified as specified in Subparagraph (E)(2) of this section; and (b) Prepared so they remain intact.

<details><summary>Other retrieved passages</summary>

> **[Food Code 2026 §3-305.11]** Source: FDA Food Code 2026, Chapters 1-6, §3-305.11 (p. 60). Food Storage
> (A) Except as specified in ¶¶ (B) and (C) of this section, FOOD shall be protected from contamination by storing the FOOD: (1) In a clean, dry location; (2) Where it is not exposed to splash, dust, or other contamination; and (3) At least 15 cm (6 inches) above the floor. (B) FOOD in packages and working containers may be stored less than 15 cm (6 inches) above the floor on case lot handling EQUIPMENT as specified under § 4-204.122. (C) Pressurized BEVERAGE containers, cased FOOD in waterproof containers such as bottles or cans, and milk containers in plastic crates may be stored on a floor that is clean and not exposed to floor moisture.

> **[Food Code 2026 §6-202.112]** Source: FDA Food Code 2026, Chapters 1-6, §6-202.112 (p. 137). Living or Sleeping Quarters, Separation
> Living or sleeping quarters located on the PREMISES of a FOOD ESTABLISHMENT such as those provided for lodging registration clerks or resident managers shall be separated from rooms and areas used for FOOD ESTABLISHMENT operations by complete partitioning and solid self-closing doors.

</details>
