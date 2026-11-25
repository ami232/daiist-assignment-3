# Answers to grade by hand

For each one write a row in `eval/human_labels.csv`: `id,correct,supported,notes`.
- **correct** 1/0: agrees with the REFERENCE on everything that matters (or is a proper refusal for an unanswerable question).
- **supported** 1/0: every claim in the answer is in the RETRIEVED passages.
- **notes**: why, for every 0.

---
## q01 (single)

**Question:** What is the maximum altitude a small drone can fly under Part 107?

**Reference:** 400 feet above ground level, unless it flies within a 400-foot radius of a structure and no higher than 400 feet above the structure's uppermost limit.

**Agent answer:**

Under 14 CFR Part 107, the maximum altitude for a small unmanned aircraft is **400 feet above ground level (AGL)** [14 CFR Part 107, § 107.51(b)]. 

**Exception for flying near structures:**
A small unmanned aircraft may fly higher than 400 feet AGL if it:
1. Is flown within a 400-foot radius of a structure; and
2. Does not fly higher than 400 feet above the structure's immediate uppermost limit [14 CFR Part 107, § 107.51(b)(1)–(2)].

*Note: This information is for educational purposes. For specific flight operations or legal advice, please consult the FAA or a qualified aviation professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.51
§ 107.51 Operating limitations for small unmanned aircraft.
A remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system must comply with all of the following operating limitations when operating a small unmanned aircraft system:
(a) The groundspeed of the small unmanned aircraft may not exceed 87 knots (100 miles per hour).
(b) The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, unless the small unmanned aircraft:
(1) Is flown within a 400-foot radius of a structure; and
(2) Does not fly higher than 400 feet above the structure's immediate uppermost limit.
(c) The minimum flight visibility, as observed from the location of the control station must be no less than 3 statute miles. For purposes of this section, flight visibility means the average slant distance from the control station at which prominent unlighted objects may be seen and identified by day and prominent lighted objects may be seen and identified by night.
(d) The minimum distance of the small unmanned aircraft from clouds must be no less than:
(1) 500 feet below the cloud; and
(2) 2,000 feet horizontally from the cloud.

[2] 14 CFR Part 107 — § 107.39
§ 107.39 Operation over human beings.
No person may operate a small unmanned aircraft over a human being unless—
(a) That human being is directly participating in the operation of the small unmanned aircraft;
(b) That human being is located under a covered structure or inside a stationary vehicle that can provide reasonable protection from a falling small unmanned aircraft; or
(c) The operation meets the requirements of at least one of the operational categories specified in subpart D of this part.

[3] 14 CFR Part 91 Subpart B — § 91.119 (part 1/2)
§ 91.119 Minimum safe altitudes: General.
Except when necessary for takeoff or landing, no person may operate an aircraft below the following altitudes:
(a) Anywhere. An altitude allowing, if a power unit fails, an emergency landing without undue hazard to persons or property on the surface.
(b) Over congested areas. Over any congested area of a city, town, or settlement, or over any open air assembly of persons, an altitude of 1,000 feet above the highest obstacle within a horizontal radius of 2,000 feet of the aircraft.
(c) Over other than congested areas. An altitude of 500 feet above the surface, except over open water or sparsely populated areas. In those cases, the aircraft may not be operated closer than 500 feet to any person, vessel, vehicle, or structure.
(d) Helicopters, powered parachutes, and weight-shift-control aircraft. If the operation is conducted without hazard to persons or property on the surface—
(1) A helicopter may be operated at less than the minimums prescribed in paragraph (b) or (c) of this section, provided each person operating the helicopter complies with any routes or altitudes specifically prescribed for helicopters by the FAA; and

[4] 14 CFR Part 107 — § 107.31
§ 107.31 Visual line of sight aircraft operation.
(a) With vision that is unaided by any device other than corrective lenses, the remote pilot in command, the visual observer (if one is used), and the person manipulating the flight control of the small unmanned aircraft system must be able to see the unmanned aircraft throughout the entire flight in order to:
(1) Know the unmanned aircraft's location;
(2) Determine the unmanned aircraft's attitude, altitude, and direction of flight;
(3) Observe the airspace for other air traffic or hazards; and
(4) Determine that the unmanned aircraft does not endanger the life or property of another.
(b) Throughout the entire flight of the small unmanned aircraft, the ability described in paragraph (a) of this section must be exercised by either:
(1) The remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system; or
(2) A visual observer.

[5] 14 CFR Part 107 — § 107.41
§ 107.41 Operation in certain airspace.
No person may operate a small unmanned aircraft in Class B, Class C, or Class D airspace or within the lateral boundaries of the surface area of Class E airspace designated for an airport unless that person has prior authorization from Air Traffic Control (ATC).
```

---
## q02 (single)

**Question:** How often does a remote pilot have to refresh their aeronautical knowledge?

**Reference:** Within the previous 24 calendar months, by passing an initial knowledge test or completing recurrent training.

**Agent answer:**

To exercise the privileges of a remote pilot in command with a small UAS rating, a person must meet aeronautical knowledge recency requirements within the previous **24 calendar months** [14 CFR Part 107, § 107.65].

To satisfy this requirement, the pilot must have completed one of the following within that 24-calendar-month period:
* Passed an initial aeronautical knowledge test [14 CFR Part 107, § 107.65(a)];
* Completed recurrent training covering the specified knowledge areas [14 CFR Part 107, § 107.65(b)]; or
* If holding a Part 61 pilot certificate (other than a student pilot certificate) and meeting the flight review requirements of § 61.56, completed training covering the applicable small UAS knowledge areas [14 CFR Part 107, § 107.65(c)].

*This information reflects general regulatory requirements. For specific questions regarding your certification or operating privileges, please consult the FAA or a qualified aviation professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.65
§ 107.65 Aeronautical knowledge recency.
A person may not exercise the privileges of a remote pilot in command with small UAS rating unless that person has accomplished one of the following in a manner acceptable to the Administrator within the previous 24 calendar months:
(a) Passed an initial aeronautical knowledge test covering the areas of knowledge specified in § 107.73;
(b) Completed recurrent training covering the areas of knowledge specified in § 107.73; or
(c) If a person holds a pilot certificate (other than a student pilot certificate) issued under part 61 of this chapter and meets the flight review requirements specified in § 61.56, completed training covering the areas of knowledge specified in § 107.74.
(d) A person who has passed a recurrent aeronautical knowledge test in a manner acceptable to the Administrator or who has satisfied the training requirement of paragraph (c) of this section prior to April 6, 2021 within the previous 24 calendar months is considered to be in compliance with the requirement of paragraph (b) or (c) of this section, as applicable.

[2] 14 CFR Part 107 — § 107.73
§ 107.73 Knowledge and training.
An initial aeronautical knowledge test and recurrent training covers the following areas of knowledge:
(a) Applicable regulations relating to small unmanned aircraft system rating privileges, limitations, and flight operation;
(b) Airspace classification, operating requirements, and flight restrictions affecting small unmanned aircraft operation;
(c) Aviation weather sources and effects of weather on small unmanned aircraft performance;
(d) Small unmanned aircraft loading;
(e) Emergency procedures;
(f) Crew resource management;
(g) Radio communication procedures;
(h) Determining the performance of the small unmanned aircraft;
(i) Physiological effects of drugs and alcohol;
(j) Aeronautical decision-making and judgment;
(k) Airport operations;
(l) Maintenance and preflight inspection procedures; and
(m) Operation at night.

[3] 14 CFR Part 107 — § 107.74
§ 107.74 Small unmanned aircraft system training.
Training for pilots who hold a pilot certificate (other than a student pilot certificate) issued under part 61 of this chapter and meet the flight review requirements specified in § 61.56 covers the following areas of knowledge:
(a) Applicable regulations relating to small unmanned aircraft system rating privileges, limitations, and flight operation;
(b) Effects of weather on small unmanned aircraft performance;
(c) Small unmanned aircraft loading;
(d) Emergency procedures;
(e) Crew resource management;
(f) Determining the performance of the small unmanned aircraft;
(g) Maintenance and preflight inspection procedures; and
(h) Operation at night.

[4] 14 CFR Part 107 — § 107.61
§ 107.61 Eligibility.
Subject to the provisions of §§ 107.57 and 107.59, in order to be eligible for a remote pilot certificate with a small UAS rating under this subpart, a person must:
(a) Be at least 16 years of age;
(b) Be able to read, speak, write, and understand the English language. If the applicant is unable to meet one of these requirements due to medical reasons, the FAA may place such operating limitations on that applicant's certificate as are necessary for the safe operation of the small unmanned aircraft;
(c) Not know or have reason to know that he or she has a physical or mental condition that would interfere with the safe operation of a small unmanned aircraft system; and
(d) Demonstrate aeronautical knowledge by satisfying one of the following conditions, in a manner acceptable to the Administrator:
(1) Pass an initial aeronautical knowledge test covering the areas of knowledge specified in § 107.73; or
(2) If a person holds a pilot certificate (other than a student pilot certificate) issued under part 61 of this chapter and meets the flight review requirements specified in § 61.56, complete training covering the areas of knowledge specified in § 107.74.

[5] 14 CFR Part 107 — § 107.63 (part 1/2)
§ 107.63 Issuance of a remote pilot certificate with a small UAS rating.
An applicant for a remote pilot certificate with a small UAS rating under this subpart must make the application in a form and manner acceptable to the Administrator.
(a) The application must include either:
(1) Evidence showing that the applicant passed an initial aeronautical knowledge test. If applying using a paper application, this evidence must be an airman knowledge test report showing passage of the knowledge test; or
(2) If a person holds a pilot certificate (other than a student pilot certificate) issued under part 61 of this chapter and meets the flight review requirements specified in § 61.56, a certificate of completion of an initial training course under this part that covers the areas of knowledge specified in § 107.74.
(b) If the application is being made pursuant to paragraph (a)(2) of this section:
(1) The application must be submitted to the responsible Flight Standards of
```

---
## q03 (single)

**Question:** What lighting does my drone need to fly at night?

**Reference:** Lighted anti-collision lighting visible for at least 3 statute miles with a flash rate sufficient to avoid a collision (and the pilot must have completed the initial knowledge test or training after April 6, 2021).

**Agent answer:**

To operate a small unmanned aircraft (drone) at night under Part 107, the drone must be equipped with anti-collision lighting that meets the following requirements:

* **Visibility:** The lighted anti-collision lighting must be visible for at least 3 statute miles [14 CFR Part 107, § 107.29(a)(2)].
* **Flash rate:** It must have a flash rate sufficient to avoid a collision [14 CFR Part 107, § 107.29(a)(2)].
* **Intensity adjustment:** The remote pilot in command may reduce the intensity of the anti-collision lighting if operating conditions make it in the interest of safety to do so, but the lights may not be completely extinguished [14 CFR Part 107, § 107.29(a)(2)].

These same anti-collision lighting requirements also apply when operating during periods of civil twilight [14 CFR Part 107, § 107.29(b)]. Note that deviations from these lighting requirements require an FAA certificate of waiver [14 CFR Part 107, § 107.205(b)].

*This summary is for informational purposes. Please consult the FAA or a qualified aviation professional for official guidance on your specific operation.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.29 (part 1/2)
§ 107.29 Operation at night.
(a) Except as provided in paragraph (d) of this section, no person may operate a small unmanned aircraft system at night unless—
(1) The remote pilot in command of the small unmanned aircraft has completed an initial knowledge test or training, as applicable, under § 107.65 after April 6, 2021; and
(2) The small unmanned aircraft has lighted anti-collision lighting visible for at least 3 statute miles that has a flash rate sufficient to avoid a collision. The remote pilot in command may reduce the intensity of, but may not extinguish, the anti-collision lighting if he or she determines that, because of operating conditions, it would be in the interest of safety to do so.
(b) No person may operate a small unmanned aircraft system during periods of civil twilight unless the small unmanned aircraft has lighted anti-collision lighting visible for at least 3 statute miles that has a flash rate sufficient to avoid a collision. The remote pilot in command may reduce the intensity of, but may not extinguish, the anti-collision lighting if he or she determines that, because of operating conditions, it would be in the interest of safety to do so.

[2] 14 CFR Part 91 Subpart C — § 91.209
§ 91.209 Aircraft lights.
No person may:
(a) During the period from sunset to sunrise (or, in Alaska, during the period a prominent unlighted object cannot be seen from a distance of 3 statute miles or the sun is more than 6 degrees below the horizon)—
(1) Operate an aircraft unless it has lighted position lights;
(2) Park or move an aircraft in, or in dangerous proximity to, a night flight operations area of an airport unless the aircraft—
(i) Is clearly illuminated;
(ii) Has lighted position lights; or
(iii) is in an area that is marked by obstruction lights;
(3) Anchor an aircraft unless the aircraft—
(i) Has lighted anchor lights; or
(ii) Is in an area where anchor lights are not required on vessels; or
(b) Operate an aircraft that is equipped with an anticollision light system, unless it has lighted anticollision lights. However, the anticollision lights need not be lighted when the pilot-in-command determines that, because of operating conditions, it would be in the interest of safety to turn the lights off.

[3] 14 CFR Part 107 — § 107.205
§ 107.205 List of regulations subject to waiver.
A certificate of waiver issued pursuant to § 107.200 may authorize a deviation from the following regulations of this part:
(a) Section 107.25—Operation from a moving vehicle or aircraft. However, no waiver of this provision will be issued to allow the carriage of property of another by aircraft for compensation or hire.
(b) Section 107.29(a)(2) and (b)—Anti-collision light required for operations at night and during periods of civil twilight.
(c) Section 107.31—Visual line of sight aircraft operation. However, no waiver of this provision will be issued to allow the carriage of property of another by aircraft for compensation or hire.
(d) Section 107.33—Visual observer.
(e) Section 107.35—Operation of multiple small unmanned aircraft systems.
(f) Section 107.37(a)—Yielding the right of way.
(g) Section 107.39—Operation over people.
(h) Section 107.41—Operation in certain airspace.
(i) Section 107.51—Operating limitations for small unmanned aircraft.
(j) Section 107.145—Operations over moving vehicles.

[4] 14 CFR Part 101 — § 101.17
§ 101.17 Lighting and marking requirements.
(a) No person may operate a moored balloon or kite, between sunset and sunrise unless the balloon or kite, and its mooring lines, are lighted so as to give a visual warning equal to that required for obstructions to air navigation in the FAA publication “Obstruction Marking and Lighting”.
(b) No person may operate a moored balloon or kite between sunrise and sunset unless its mooring lines have colored pennants or streamers attached at not more than 50 foot intervals beginning at 150 feet above the surface of the earth and visible for at least one mile.

[5] 14 CFR Part 91 Subpart C — § 91.205 (part 4/7)
§ 91.205 Powered civil aircraft with standard U.S. airworthiness certificates: Instrument and equipment requirements.
(2) Approved position lights.
(3) An approved aviation red or aviation white anticollision light system on all U.S.-registered civil aircraft. Anticollision light systems initially installed after August 11, 1971, on aircraft for which a type certificate was issued or applied for before August 11, 1971, must at least meet the anticollision light standards of part 23, 25, 27, or 29 of this chapter, as applicable, that were in effect on August 10, 1971, except that the color may be either aviation red or aviation white. In the event of failure of any light of the anticollision light system, operations with the aircraft may be continued to a stop where repairs or replacement can be made.
(4) If the aircraft is operated for hire, one electric landing light.
(5) An adequate source of electric
```

---
## q04 (single)

**Question:** When is civil twilight for drone purposes, outside Alaska?

**Reference:** From 30 minutes before official sunrise until sunrise, and from official sunset until 30 minutes after official sunset.

**Agent answer:**

Outside Alaska, civil twilight for small unmanned aircraft system (drone) operations is defined as:

* **Morning civil twilight:** A period of time that begins 30 minutes before official sunrise and ends at official sunrise [14 CFR Part 107, § 107.29(c)(1)].
* **Evening civil twilight:** A period of time that begins at official sunset and ends 30 minutes after official sunset [14 CFR Part 107, § 107.29(c)(2)].

*Note: This response summarizes regulatory provisions and does not constitute legal advice. Please consult the FAA or a qualified aviation professional regarding your specific situation.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.29 (part 2/2)
§ 107.29 Operation at night.
(c) For purposes of paragraph (b) of this section, civil twilight refers to the following:
(1) Except for Alaska, a period of time that begins 30 minutes before official sunrise and ends at official sunrise;
(2) Except for Alaska, a period of time that begins at official sunset and ends 30 minutes after official sunset; and
(3) In Alaska, the period of civil twilight as defined in the Air Almanac.
(d) After May 17, 2021, no person may operate a small unmanned aircraft system at night in accordance with a certificate of waiver issued prior to April 21, 2021 under § 107.200. The certificates of waiver issued prior to March 16, 2021 under § 107.200 that authorize deviation from § 107.29 terminate on May 17, 2021.

[2] 14 CFR Part 107 — § 107.29 (part 1/2)
§ 107.29 Operation at night.
(a) Except as provided in paragraph (d) of this section, no person may operate a small unmanned aircraft system at night unless—
(1) The remote pilot in command of the small unmanned aircraft has completed an initial knowledge test or training, as applicable, under § 107.65 after April 6, 2021; and
(2) The small unmanned aircraft has lighted anti-collision lighting visible for at least 3 statute miles that has a flash rate sufficient to avoid a collision. The remote pilot in command may reduce the intensity of, but may not extinguish, the anti-collision lighting if he or she determines that, because of operating conditions, it would be in the interest of safety to do so.
(b) No person may operate a small unmanned aircraft system during periods of civil twilight unless the small unmanned aircraft has lighted anti-collision lighting visible for at least 3 statute miles that has a flash rate sufficient to avoid a collision. The remote pilot in command may reduce the intensity of, but may not extinguish, the anti-collision lighting if he or she determines that, because of operating conditions, it would be in the interest of safety to do so.

[3] 14 CFR Part 107 — § 107.51
§ 107.51 Operating limitations for small unmanned aircraft.
A remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system must comply with all of the following operating limitations when operating a small unmanned aircraft system:
(a) The groundspeed of the small unmanned aircraft may not exceed 87 knots (100 miles per hour).
(b) The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, unless the small unmanned aircraft:
(1) Is flown within a 400-foot radius of a structure; and
(2) Does not fly higher than 400 feet above the structure's immediate uppermost limit.
(c) The minimum flight visibility, as observed from the location of the control station must be no less than 3 statute miles. For purposes of this section, flight visibility means the average slant distance from the control station at which prominent unlighted objects may be seen and identified by day and prominent lighted objects may be seen and identified by night.
(d) The minimum distance of the small unmanned aircraft from clouds must be no less than:
(1) 500 feet below the cloud; and
(2) 2,000 feet horizontally from the cloud.

[4] 14 CFR Part 107 — § 107.11
§ 107.11 Applicability.
This subpart applies to the operation of all civil small unmanned aircraft systems subject to this part.

[5] 14 CFR Part 91 Subpart C — § 91.209
§ 91.209 Aircraft lights.
No person may:
(a) During the period from sunset to sunrise (or, in Alaska, during the period a prominent unlighted object cannot be seen from a distance of 3 statute miles or the sun is more than 6 degrees below the horizon)—
(1) Operate an aircraft unless it has lighted position lights;
(2) Park or move an aircraft in, or in dangerous proximity to, a night flight operations area of an airport unless the aircraft—
(i) Is clearly illuminated;
(ii) Has lighted position lights; or
(iii) is in an area that is marked by obstruction lights;
(3) Anchor an aircraft unless the aircraft—
(i) Has lighted anchor lights; or
(ii) Is in an area where anchor lights are not required on vessels; or
(b) Operate an aircraft that is equipped with an anticollision light system, unless it has lighted anticollision lights. However, the anticollision lights need not be lighted when the pilot-in-command determines that, because of operating conditions, it would be in the interest of safety to turn the lights off.
```

---
## q05 (single)

**Question:** Under what conditions can I fly a drone over people?

**Reference:** Only if the person is directly participating in the operation, is under a covered structure or inside a stationary vehicle that gives reasonable protection, or the operation meets one of the operational categories in subpart D of Part 107.

**Agent answer:**

Under 14 CFR Part 107, a remote pilot may operate a small unmanned aircraft over a human being only under the following conditions:

1. **Direct Participants:** The human being is directly participating in the operation of the small unmanned aircraft [14 CFR Part 107, § 107.39(a)].
2. **Protected Location:** The human being is located under a covered structure or inside a stationary vehicle capable of providing reasonable protection from a falling small unmanned aircraft [14 CFR Part 107, § 107.39(b)].
3. **Subpart D Operational Categories:** The operation meets the requirements of one of four specific categories [14 CFR Part 107, § 107.39(c)], [14 CFR Part 107, § 107.105]:
   - **Category 1:** The small unmanned aircraft weighs 0.55 pounds or less (including everything on board or attached) and has no exposed rotating parts that would lacerate human skin upon impact [14 CFR Part 107, § 107.110(a)]. Sustained flight over open-air assemblies of human beings is prohibited unless Remote ID requirements under § 89.110 or § 89.115(a) are met [14 CFR Part 107, § 107.110(b)].
   - **Category 2:** The aircraft is eligible, listed on an FAA-accepted declaration of compliance, and labeled for Category 2 [14 CFR Part 107, § 107.115(a)]. Sustained flight over open-air assemblies requires compliance with Remote ID requirements under § 89.110 or § 89.115(a) [14 CFR Part 107, § 107.115(b)].
   - **Category 3:** The aircraft is eligible, listed on an FAA-accepted declaration of compliance, and labeled for Category 3 [14 CFR Part 107, § 107.125(a)]. Operations cannot be conducted over open-air assemblies of human beings [14 CFR Part 107, § 107.125(b)], and must either:
     - Take place within or over a closed- or restricted-access site where all individuals are on notice that a small unmanned aircraft may fly over them [14 CFR Part 107, § 107.125(c)(1)]; or
     - Not maintain sustained flight over any human being unless that person is directly participating or protected inside a covered structure or stationary vehicle [14 CFR Part 107, § 107.125(c)(2)].
   - **Category 4:** The aircraft has an airworthiness certificate under Part 21, is operated under operating limitations that do not prohibit operations over human beings, and meets maintenance requirements [14 CFR Part 107, § 107.140(a)(1), (b)]. Sustained flight over open-air assemblies requires compliance with Remote ID requirements under § 89.110 or § 89.115(a) [14 CFR Part 107, § 107.140(a)(2)].

*Disclaimer: This information reflects federal regulations and is not legal advice. For specific operational situations or determinations, please consult the FAA or a qualified aviation legal professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.39
§ 107.39 Operation over human beings.
No person may operate a small unmanned aircraft over a human being unless—
(a) That human being is directly participating in the operation of the small unmanned aircraft;
(b) That human being is located under a covered structure or inside a stationary vehicle that can provide reasonable protection from a falling small unmanned aircraft; or
(c) The operation meets the requirements of at least one of the operational categories specified in subpart D of this part.

[2] 14 CFR Part 107 — § 107.105
§ 107.105 Limitations on operations over human beings.
Except as provided in §§ 107.39(a) and (b) and 107.145, a remote pilot in command may conduct operations over human beings only in accordance with the following, as applicable: § 107.110 for Category 1 operations; §§ 107.115 and 107.120 for Category 2 operations; §§ 107.125 and 107.130 for Category 3 operations; or § 107.140 for Category 4 operations.

[3] 14 CFR Part 107 — § 107.140 (part 1/4)
§ 107.140 Category 4 operations.
(a) Remote pilot in command requirements. To conduct Category 4 operations—
(1) A remote pilot in command—
(i) Must use a small unmanned aircraft that is eligible for Category 4 operations pursuant to paragraph (b) of this section; and
(ii) Must operate the small unmanned aircraft in accordance with all operating limitations that apply to the small unmanned aircraft, as specified by the Administrator.
(2) No remote pilot in command may operate a small unmanned aircraft in sustained flight over open-air assemblies of human beings unless the operation meets the requirements of either § 89.110 or § 89.115(a) of this chapter.
(b) Small unmanned aircraft requirements for Category 4. To be eligible to operate over human beings under this section, the small unmanned aircraft must—
(1) Have an airworthiness certificate issued under part 21 of this chapter.
(2) Be operated in accordance with the operating limitations specified in the approved Flight Manual or as otherwise specified by the Administrator. The operating limitations must not prohibit operations over human beings.
(3) Have maintenance, preventive maintenance, alterations, or inspections performed in accordance with paragraph (c)(1) of this section.

[4] 14 CFR Part 107 — § 107.125
§ 107.125 Category 3 operations: Operating requirements.
To conduct Category 3 operations, a remote pilot in command—
(a) Must use a small unmanned aircraft that—
(1) Is eligible for Category 3 operations pursuant to § 107.130(a);
(2) Is listed on an FAA-accepted declaration of compliance as eligible for Category 3 operations in accordance with § 107.160; and
(3) Is labeled as eligible for Category 3 operations in accordance with § 107.130(b)(1);
(b) Must not operate the small unmanned aircraft over open-air assemblies of human beings; and
(c) May only operate the small unmanned aircraft above any human being if operation meets one of the following conditions:
(1) The operation is within or over a closed- or restricted-access site and all human beings located within the closed- or restricted-access site must be on notice that a small unmanned aircraft may fly over them; or
(2) The small unmanned aircraft does not maintain sustained flight over any human being unless that human being is—
(i) Directly participating in the operation of the small unmanned aircraft; or
(ii) Located under a covered structure or inside a stationary vehicle that can provide reasonable protection from a falling small unmanned aircraft.

[5] 14 CFR Part 107 — § 107.145
§ 107.145 Operations over moving vehicles.
No person may operate a small unmanned aircraft over a human being located inside a moving vehicle unless the following conditions are met:
(a) The operation occurs in accordance with § 107.110 for Category 1 operations; § 107.115 for Category 2 operations; § 107.125 for Category 3 operations; or § 107.140 for Category 4 operations.
(b) For an operation under Category 1, Category 2, or Category 3, the small unmanned aircraft, throughout the operation—
(1) Must remain within or over a closed- or restricted-access site, and all human beings located inside a moving vehicle within the closed- or restricted-access site must be on notice that a small unmanned aircraft may fly over them; or
(2) Must not maintain sustained flight over moving vehicles.
(c) For a Category 4 operation, the small unmanned aircraft must—
(1) Have an airworthiness certificate issued under part 21 of this chapter.
(2) Be operated in accordance with the operating limitations specified in the approved Flight Manual or as otherwise specified by the Administrator. The operating limitations must not prohibit operations over human beings located inside moving vehicles.

[1] 14 CFR Part 107 — § 107.105
§ 107.105 Limitations on operations over human beings.
Except as provided in §§ 107.39(a) and (b) and 107.145, a remote pilot in command may conduct operations over human beings only in accordance with t
```

---
## q06 (single)

**Question:** Who has to be able to see the drone during a flight?

**Reference:** Unaided by anything other than corrective lenses, the remote pilot in command and the person manipulating the controls, or a visual observer, must be able to see the drone throughout the flight.

**Agent answer:**

Under 14 CFR Part 107, the following people must be able to see the drone (unmanned aircraft) throughout the entire flight with vision unaided by any device other than corrective lenses [14 CFR Part 107, § 107.31(a)]:

* **The remote pilot in command**
* **The person manipulating the flight controls** of the small unmanned aircraft system
* **The visual observer** (if one is used)

Throughout the entire flight, the visual line of sight capability must be exercised by either:
1. The remote pilot in command and the person manipulating the flight controls; **or**
2. A visual observer [14 CFR Part 107, § 107.31(b)].

If a visual observer is used, the remote pilot in command must ensure that the visual observer is able to see the drone as required by § 107.31 [14 CFR Part 107, § 107.33(b)].

*Note: This summary reflects federal regulatory requirements. For specific operational cases or waivers, consult the FAA or a qualified aviation legal professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.31
§ 107.31 Visual line of sight aircraft operation.
(a) With vision that is unaided by any device other than corrective lenses, the remote pilot in command, the visual observer (if one is used), and the person manipulating the flight control of the small unmanned aircraft system must be able to see the unmanned aircraft throughout the entire flight in order to:
(1) Know the unmanned aircraft's location;
(2) Determine the unmanned aircraft's attitude, altitude, and direction of flight;
(3) Observe the airspace for other air traffic or hazards; and
(4) Determine that the unmanned aircraft does not endanger the life or property of another.
(b) Throughout the entire flight of the small unmanned aircraft, the ability described in paragraph (a) of this section must be exercised by either:
(1) The remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system; or
(2) A visual observer.

[2] 14 CFR Part 107 — § 107.33
§ 107.33 Visual observer.
If a visual observer is used during the aircraft operation, all of the following requirements must be met:
(a) The remote pilot in command, the person manipulating the flight controls of the small unmanned aircraft system, and the visual observer must maintain effective communication with each other at all times.
(b) The remote pilot in command must ensure that the visual observer is able to see the unmanned aircraft in the manner specified in § 107.31.
(c) The remote pilot in command, the person manipulating the flight controls of the small unmanned aircraft system, and the visual observer must coordinate to do the following:
(1) Scan the airspace where the small unmanned aircraft is operating for any potential collision hazard; and
(2) Maintain awareness of the position of the small unmanned aircraft through direct visual observation.

[3] 14 CFR Part 107 — § 107.3 (part 2/2)
§ 107.3 Definitions.
Visual observer means a person who is designated by the remote pilot in command to assist the remote pilot in command and the person manipulating the flight controls of the small UAS to see and avoid other air traffic or objects aloft or on the ground.

[4] 14 CFR Part 107 — § 107.51
§ 107.51 Operating limitations for small unmanned aircraft.
A remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system must comply with all of the following operating limitations when operating a small unmanned aircraft system:
(a) The groundspeed of the small unmanned aircraft may not exceed 87 knots (100 miles per hour).
(b) The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, unless the small unmanned aircraft:
(1) Is flown within a 400-foot radius of a structure; and
(2) Does not fly higher than 400 feet above the structure's immediate uppermost limit.
(c) The minimum flight visibility, as observed from the location of the control station must be no less than 3 statute miles. For purposes of this section, flight visibility means the average slant distance from the control station at which prominent unlighted objects may be seen and identified by day and prominent lighted objects may be seen and identified by night.
(d) The minimum distance of the small unmanned aircraft from clouds must be no less than:
(1) 500 feet below the cloud; and
(2) 2,000 feet horizontally from the cloud.

[5] 14 CFR Part 89 — § 89.115 (part 3/3)
§ 89.115 Alternative remote identification.
(1) The unmanned aircraft and the person manipulating the flight controls of the unmanned aircraft system remain within the boundaries of an FAA-recognized identification area throughout the operation; and
(2) The person manipulating the flight controls of the unmanned aircraft system must be able to see the unmanned aircraft at all times throughout the operation.
```

---
## q07 (single)

**Question:** How long is a drone registration valid and when can I renew it?

**Reference:** A Certificate of Aircraft Registration expires 3 years after issue; the renewal verification can be done within the six months before the month it expires.

**Agent answer:**

Under 14 CFR Part 48, drone registration validity and renewal terms are as follows:

* **Validity Period:** A Certificate of Aircraft Registration expires **3 years** after its date of issue unless it is renewed [14 CFR Part 48, § 48.100(c)] [14 CFR Part 48, § 48.105(c)]. When renewed, the new certificate expires 3 years from the expiration date of the previous certificate [14 CFR Part 48, § 48.100(c)(2)] [14 CFR Part 48, § 48.105(c)(2)].
* **When You Can Renew:** You can renew your certificate at any time **within the 6 months preceding the month in which the certificate expires** [14 CFR Part 48, § 48.100(c)(1)] [14 CFR Part 48, § 48.105(c)(1)].
* **Renewal Process:** Renewal requires verifying in a form and manner prescribed by the FAA that your registration information is accurate, or providing updated information if it has changed [14 CFR Part 48, § 48.100(c)(1)] [14 CFR Part 48, § 48.105(c)(1)].

These rules apply to small unmanned aircraft registered for both limited recreational operations and commercial/other operations [14 CFR Part 48, § 48.100] [14 CFR Part 48, § 48.105].

*Note: This response provides regulatory details only and does not constitute legal advice. Please consult the FAA or a qualified professional regarding your specific situation.*

**Retrieved passages:**

```
[1] 14 CFR Part 48 — § 48.105 (part 1/2)
§ 48.105 Registration: Small unmanned aircraft intended exclusively for limited recreational operations.
(a) Certificate of Aircraft Registration. A Certificate of Aircraft Registration issued in accordance with § 48.110 for small unmanned aircraft to be operated exclusively in compliance with 49 U.S.C. 44809 constitutes registration for all the small unmanned aircraft used exclusively for operations in compliance with 49 U.S.C. 44809 owned by the individual identified on the application.
(b) Effective date of registration. An aircraft is registered when the applicant receives a Certificate of Aircraft Registration. The effective date of registration is shown by the date of issue on the Certificate of Aircraft Registration issued under this part.
(c) Registration renewal. A Certificate of Aircraft registration issued under this part expires 3 years after the date of issue unless it is renewed.
(1) The holder of a Certificate of Aircraft Registration must renew the Certificate by verifying, in a form and manner prescribed by the Administrator, that the information provided in accordance with § 48.110 is accurate and if it is not, provide updated information. The verification may take place at any time within the six months preceding the month in which the Certificate of Aircraft registration expires.

[2] 14 CFR Part 48 — § 48.100 (part 1/3)
§ 48.100 Registration: Small unmanned aircraft operated for any purpose other than exclusively limited recreational operations.
(a) Certificate of Aircraft Registration. A Certificate of Aircraft Registration issued in accordance with § 48.110 to a small unmanned aircraft used for any purpose other than operating exclusively in compliance with 49 U.S.C. 44809 constitutes registration for the small unmanned aircraft identified on the application.
(b) Effective date of registration. An aircraft is registered when the applicant receives a Certificate of Aircraft Registration for the specific aircraft. The effective date of registration is shown by the date of issue on the Certificate of Aircraft Registration issued for the aircraft.
(c) Registration renewal. A Certificate of Aircraft registration issued under this part expires 3 years after the date of issue unless it is renewed.
(1) The holder of a Certificate of Aircraft Registration must renew the Certificate by verifying, in a form and manner prescribed by the Administrator, that the information provided in accordance with § 48.110 is accurate and if it is not, provide updated information. The verification may take place at any time within the six months preceding the month in which the Certificate of Aircraft registration expires.
(2) A certificate issued under this paragraph expires three years from the expiration date of the previous certificate.

[3] 14 CFR Part 48 — § 48.105 (part 2/2)
§ 48.105 Registration: Small unmanned aircraft intended exclusively for limited recreational operations.
(2) A certificate issued under this paragraph expires three years from the expiration date of the previous certificate.
(d) Other events affecting effectiveness of Certificate. Each Certificate of Aircraft Registration issued by the FAA under this part is effective, unless registration has ended by reason of having been revoked, canceled or expired, or until the date upon which one of the following events occurs:
(1) The holder of the Certificate of Aircraft Registration loses U.S. citizenship.
(2) Thirty days have elapsed since the death of the holder of the Certificate of Aircraft Registration.
(3) The owner, if an individual who is not a citizen of the United States, loses status as a resident alien, unless that person becomes a citizen of the United States at the same time.

[4] 14 CFR Part 48 — § 48.115
§ 48.115 Requirement to maintain current information.
(a) The holder of a Certificate of Aircraft Registration must ensure that the information provided under § 48.110 remains accurate.
(b) The holder of a Certificate of Aircraft Registration must update the information using the web-based small unmanned aircraft registration system within 14 calendar days of the following:
(1) A change in the information provided under § 48.110.
(2) When aircraft registration requires cancellation for any reason including sale or transfer, destruction, or export.

[5] 14 CFR Part 48 — § 48.100 (part 2/3)
§ 48.100 Registration: Small unmanned aircraft operated for any purpose other than exclusively limited recreational operations.
(d) Other events affecting effectiveness of Certificate. Each Certificate of Aircraft Registration issued by the FAA under this subpart is effective, unless registration has ended by reason of having been revoked, canceled, expired, or the ownership is transferred, until the date upon which one of the following events occurs:
(1) Subject to the Convention on the International Recognition of Rights in Aircraft when applicable, the aircraft is registered under the laws of a fore
```

---
## q08 (single)

**Question:** How quickly must I update my drone registration after my information changes?

**Reference:** Within 14 calendar days of the change, or of the registration needing cancellation (sale, transfer, destruction or export), using the web-based registration system.

**Agent answer:**

You must update your **drone registration** information using the web-based small unmanned aircraft registration system within **14 calendar days** of [14 CFR Part 48, § 48.115(b)]:

* A change in the information provided for registration [14 CFR Part 48, § 48.115(b)(1)].
* An event requiring registration cancellation (including sale, transfer, destruction, or export) [14 CFR Part 48, § 48.115(b)(2)].

*(Note: If you hold a Remote Pilot Certificate under Part 107 and change your permanent mailing address, you must notify the FAA within **30 days** of the change to continue exercising the privileges of your certificate [14 CFR Part 107, § 107.77(c)].)*

*This information is for regulatory reference. Please consult the FAA or a qualified aviation professional regarding your specific situation.*

**Retrieved passages:**

```
[1] 14 CFR Part 48 — § 48.115
§ 48.115 Requirement to maintain current information.
(a) The holder of a Certificate of Aircraft Registration must ensure that the information provided under § 48.110 remains accurate.
(b) The holder of a Certificate of Aircraft Registration must update the information using the web-based small unmanned aircraft registration system within 14 calendar days of the following:
(1) A change in the information provided under § 48.110.
(2) When aircraft registration requires cancellation for any reason including sale or transfer, destruction, or export.

[2] 14 CFR Part 107 — § 107.77
§ 107.77 Change of name or address.
(a) Change of name. An application to change the name on a certificate issued under this subpart must be accompanied by the applicant's:
(1) Remote pilot certificate with small UAS rating; and
(2) A copy of the marriage license, court order, or other document verifying the name change.
(b) The documents in paragraph (a) of this section will be returned to the applicant after inspection.
(c) Change of address. The holder of a remote pilot certificate with small UAS rating issued under this subpart who has made a change in permanent mailing address may not, after 30 days from that date, exercise the privileges of the certificate unless the holder has notified the FAA of the change in address using one of the following methods:
(1) By letter to the FAA Airman Certification Branch, P.O. Box 25082, Oklahoma City, OK 73125 providing the new permanent mailing address, or if the permanent mailing address includes a post office box number, then the holder's current residential address; or
(2) By using the FAA Web site portal at www.faa.gov providing the new permanent mailing address, or if the permanent mailing address includes a post office box number, then the holder's current residential address.

[3] 14 CFR Part 48 — § 48.105 (part 1/2)
§ 48.105 Registration: Small unmanned aircraft intended exclusively for limited recreational operations.
(a) Certificate of Aircraft Registration. A Certificate of Aircraft Registration issued in accordance with § 48.110 for small unmanned aircraft to be operated exclusively in compliance with 49 U.S.C. 44809 constitutes registration for all the small unmanned aircraft used exclusively for operations in compliance with 49 U.S.C. 44809 owned by the individual identified on the application.
(b) Effective date of registration. An aircraft is registered when the applicant receives a Certificate of Aircraft Registration. The effective date of registration is shown by the date of issue on the Certificate of Aircraft Registration issued under this part.
(c) Registration renewal. A Certificate of Aircraft registration issued under this part expires 3 years after the date of issue unless it is renewed.
(1) The holder of a Certificate of Aircraft Registration must renew the Certificate by verifying, in a form and manner prescribed by the Administrator, that the information provided in accordance with § 48.110 is accurate and if it is not, provide updated information. The verification may take place at any time within the six months preceding the month in which the Certificate of Aircraft registration expires.

[4] 14 CFR Part 48 — § 48.100 (part 1/3)
§ 48.100 Registration: Small unmanned aircraft operated for any purpose other than exclusively limited recreational operations.
(a) Certificate of Aircraft Registration. A Certificate of Aircraft Registration issued in accordance with § 48.110 to a small unmanned aircraft used for any purpose other than operating exclusively in compliance with 49 U.S.C. 44809 constitutes registration for the small unmanned aircraft identified on the application.
(b) Effective date of registration. An aircraft is registered when the applicant receives a Certificate of Aircraft Registration for the specific aircraft. The effective date of registration is shown by the date of issue on the Certificate of Aircraft Registration issued for the aircraft.
(c) Registration renewal. A Certificate of Aircraft registration issued under this part expires 3 years after the date of issue unless it is renewed.
(1) The holder of a Certificate of Aircraft Registration must renew the Certificate by verifying, in a form and manner prescribed by the Administrator, that the information provided in accordance with § 48.110 is accurate and if it is not, provide updated information. The verification may take place at any time within the six months preceding the month in which the Certificate of Aircraft registration expires.
(2) A certificate issued under this paragraph expires three years from the expiration date of the previous certificate.

[5] 14 CFR Part 48 — § 48.100 (part 2/3)
§ 48.100 Registration: Small unmanned aircraft operated for any purpose other than exclusively limited recreational operations.
(d) Other events affecting effectiveness of Certificate. Each Certificate of Aircraft Registration issued by the FAA under this subpart is 
```

---
## q09 (single)

**Question:** Is Remote ID required for drones and since when?

**Reference:** After September 16, 2023 no person may operate an unmanned aircraft in US airspace unless the operation meets the standard (§ 89.110) or alternative (§ 89.115) remote identification requirements, except as authorized by the Administrator.

**Agent answer:**

Yes, Remote ID is required for drone operations in the United States, subject to specific rules and applicability:

* **Compliance Date:** After **September 16, 2023**, no person may operate an unmanned aircraft within the airspace of the United States unless the operation meets the remote identification requirements of § 89.110 or § 89.115, except as otherwise authorized by the Administrator or provided in § 89.120 [14 CFR Part 89, § 89.105].
* **Applicability:** The operational Remote ID requirement applies to persons operating unmanned aircraft registered or required to be registered under 14 CFR Part 47 or Part 48, as well as persons operating foreign civil unmanned aircraft in the U.S. [14 CFR Part 89, § 89.101(a)].
* **Exception:** It does not apply to unmanned aircraft operations under Part 91 that are transmitting ADS-B Out pursuant to § 91.225 [14 CFR Part 89, § 89.101(b)].

*Disclaimer: This response summarizes regulatory requirements and is not legal advice. For specific cases or operations, please consult the FAA or a qualified aviation professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 89 — § 89.105
§ 89.105 Remote identification requirement.
Except as otherwise authorized by the Administrator or as provided in § 89.120, after September 16, 2023, no person may operate an unmanned aircraft within the airspace of the United States unless the operation meets the requirements of § 89.110 or § 89.115.

[2] 14 CFR Part 89 — § 89.125
§ 89.125 Automatic Dependent Surveillance-Broadcast (ADS-B) Out prohibition.
Automatic Dependent Surveillance-Broadcast (ADS-B) Out equipment cannot be used to comply with the remote identification requirements of this part.

[3] 14 CFR Part 89 — § 89.301
§ 89.301 Applicability.
This subpart prescribes the minimum message element set and minimum performance requirements for standard remote identification unmanned aircraft and remote identification broadcast modules.

[4] 14 CFR Part 89 — § 89.315
§ 89.315 Minimum message elements broadcast by remote identification broadcast modules.
Remote identification broadcast modules must be capable of broadcasting the following remote identification message elements:
(a) The identity of the unmanned aircraft, consisting of the serial number assigned to the remote identification broadcast module by the person responsible for the production of the remote identification broadcast module.
(b) An indication of the latitude and longitude of the unmanned aircraft.
(c) An indication of the geometric altitude of the unmanned aircraft.
(d) An indication of the velocity of the unmanned aircraft.
(e) An indication of the latitude and longitude of the take-off location of the unmanned aircraft.
(f) An indication of the geometric altitude of the take-off location of the unmanned aircraft.
(g) A time mark identifying the Coordinated Universal Time (UTC) time of applicability of a position source output.

[5] 14 CFR Part 89 — § 89.320 (part 2/3)
§ 89.320 Minimum performance requirements for remote identification broadcast modules.
(f) Interference considerations. The remote identification broadcast module must not interfere with other systems or equipment installed on compatible unmanned aircraft, and other systems or equipment installed on compatible unmanned aircraft must not interfere with the remote identification equipment.
(g) Message broadcast. (1) The remote identification broadcast module must be capable of broadcasting the message elements in § 89.315 using a non-proprietary broadcast specification and using radio frequency spectrum compatible with personal wireless devices in accordance with 47 CFR part 15, where operations may occur without an FCC individual license.
(2) The remote identification broadcast module must be designed to maximize the range at which the broadcast can be received, while complying with 47 CFR part 15 and any other applicable laws in effect as of the date the declaration of compliance is submitted to the FAA for acceptance.
(h) Message elements performance requirements. (1) The reported geometric position of the unmanned aircraft must be accurate to within 100 feet of the true position, with 95 percent probability.
(2) The reported geometric altitude of the unmanned aircraft must be accurate to within 150 feet of the true geometric altitude, with 95 percent probability.

[1] 14 CFR Part 89 — § 89.101
§ 89.101 Applicability.
(a) Except as provided in paragraph (b) of this section, this subpart applies to the following:
(1) Persons operating unmanned aircraft registered or required to be registered under part 47 or 48 of this chapter.
(2) Persons operating foreign civil unmanned aircraft in the United States.
(b) This subpart does not apply to unmanned aircraft operations under part 91 of this chapter that are transmitting ADS-B Out pursuant to § 91.225.

[2] 14 CFR Part 89 — § 89.201
§ 89.201 Applicability.
This subpart prescribes procedural requirements to establish an FAA-recognized identification area.

[3] 14 CFR Part 89 — § 89.301
§ 89.301 Applicability.
This subpart prescribes the minimum message element set and minimum performance requirements for standard remote identification unmanned aircraft and remote identification broadcast modules.

[4] 14 CFR Part 89 — § 89.501
§ 89.501 Applicability.
(a) This subpart prescribes—
(1) Requirements for the design and production of unmanned aircraft with remote identification produced for operation in the airspace of the United States.
(2) Requirements for the design and production of remote identification broadcast modules.
(3) Procedural requirements for the submission, acceptance, and rescission of declarations of compliance.
(4) Rules governing persons submitting declarations of compliance for FAA acceptance under this part.
(b) Except as provided in paragraph (c) of this section, this subpart applies to the design and production of all unmanned aircraft operated in the airspace of the United States.
(c) Except for unmanned aircraft designed and produced to be standard remote identification unmanned aircraft, this subpart does not apply to t
```

---
## q10 (single)

**Question:** Does Remote ID apply to a drone operation that is transmitting ADS-B Out?

**Reference:** No. The subpart does not apply to unmanned aircraft operations under part 91 that are transmitting ADS-B Out under § 91.225.

**Agent answer:**

No, Remote Identification operating rules **do not apply** to unmanned aircraft operations under 14 CFR Part 91 that are transmitting ADS-B Out pursuant to 14 CFR § 91.225 [14 CFR Part 89, § 89.101(b)].

However, the regulations specify the following conditions regarding ADS-B Out and Remote ID:

* **ADS-B Out cannot be used to satisfy Remote ID:** ADS-B Out equipment cannot be used to comply with Remote ID requirements [14 CFR Part 89, § 89.125].
* **Part 107 Operations:** Operating a small unmanned aircraft system under Part 107 with ADS-B Out equipment in transmit mode is prohibited unless otherwise authorized by the Administrator [14 CFR Part 107, § 107.53].
* **Part 91 Operations:** No person may operate an unmanned aircraft under Part 91 with ADS-B Out in transmit mode unless the operation is conducted under a flight plan with two-way ATC communication maintained, or is otherwise authorized by the Administrator [14 CFR Part 91, § 91.225(i)(2)].

*This answer summarizes the regulations and is not legal advice. For specific operations, verify requirements with the FAA or a qualified aviation professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 89 — § 89.125
§ 89.125 Automatic Dependent Surveillance-Broadcast (ADS-B) Out prohibition.
Automatic Dependent Surveillance-Broadcast (ADS-B) Out equipment cannot be used to comply with the remote identification requirements of this part.

[2] 14 CFR Part 91 Subpart C — § 91.225 (part 5/8)
§ 91.225 Automatic Dependent Surveillance-Broadcast (ADS-B) Out equipment and use.
(i) That aircraft has equipment installed that meets the performance requirements in TSO-C166b (including Section 2 of RTCA DO-260B, as referenced in TSO-C166b), TSO-C166c (including Section 2 of RTCA DO-260C as modified by DO-260C—Change 1, as referenced in TSO-C166c), TSO-C154c (including Section 2 of RTCA DO-282B, as referenced in TSO-C154c), or TSO-C154d (including Section 2 of RTCA DO-282C, as referenced in TSO-C154d); and
(ii) The equipment meets the requirements of § 91.227.
(2) No person may operate an unmanned aircraft under this part with Automatic Dependent Surveillance-Broadcast Out equipment in transmit mode unless:
(i) The operation is conducted under a flight plan and the person operating that unmanned aircraft maintains two-way communication with ATC; or
(ii) The use of ADS-B Out is otherwise authorized by the Administrator.

[3] 14 CFR Part 107 — § 107.53
§ 107.53 Automatic Dependent Surveillance-Broadcast (ADS-B) Out prohibition.
Unless otherwise authorized by the Administrator, no person may operate a small unmanned aircraft system under this part with ADS-B Out equipment in transmit mode.

[4] 14 CFR Part 89 — § 89.305
§ 89.305 Minimum message elements broadcast by standard remote identification unmanned aircraft.
A standard remote identification unmanned aircraft must be capable of broadcasting the following remote identification message elements:
(a) The identity of the unmanned aircraft, consisting of:
(1) A serial number assigned to the unmanned aircraft by the person responsible for the production of the standard remote identification unmanned aircraft; or
(2) A session ID.
(b) An indication of the latitude and longitude of the control station.
(c) An indication of the geometric altitude of the control station.
(d) An indication of the latitude and longitude of the unmanned aircraft.
(e) An indication of the geometric altitude of the unmanned aircraft.
(f) An indication of the velocity of the unmanned aircraft.
(g) A time mark identifying the Coordinated Universal Time (UTC) time of applicability of a position source output.
(h) An indication of the emergency status of the unmanned aircraft.

[5] 14 CFR Part 89 — § 89.315
§ 89.315 Minimum message elements broadcast by remote identification broadcast modules.
Remote identification broadcast modules must be capable of broadcasting the following remote identification message elements:
(a) The identity of the unmanned aircraft, consisting of the serial number assigned to the remote identification broadcast module by the person responsible for the production of the remote identification broadcast module.
(b) An indication of the latitude and longitude of the unmanned aircraft.
(c) An indication of the geometric altitude of the unmanned aircraft.
(d) An indication of the velocity of the unmanned aircraft.
(e) An indication of the latitude and longitude of the take-off location of the unmanned aircraft.
(f) An indication of the geometric altitude of the take-off location of the unmanned aircraft.
(g) A time mark identifying the Coordinated Universal Time (UTC) time of applicability of a position source output.

[1] 14 CFR Part 89 — § 89.201
§ 89.201 Applicability.
This subpart prescribes procedural requirements to establish an FAA-recognized identification area.

[2] 14 CFR Part 89 — § 89.301
§ 89.301 Applicability.
This subpart prescribes the minimum message element set and minimum performance requirements for standard remote identification unmanned aircraft and remote identification broadcast modules.

[3] 14 CFR Part 89 — § 89.101
§ 89.101 Applicability.
(a) Except as provided in paragraph (b) of this section, this subpart applies to the following:
(1) Persons operating unmanned aircraft registered or required to be registered under part 47 or 48 of this chapter.
(2) Persons operating foreign civil unmanned aircraft in the United States.
(b) This subpart does not apply to unmanned aircraft operations under part 91 of this chapter that are transmitting ADS-B Out pursuant to § 91.225.

[4] 14 CFR Part 89 — § 89.105
§ 89.105 Remote identification requirement.
Except as otherwise authorized by the Administrator or as provided in § 89.120, after September 16, 2023, no person may operate an unmanned aircraft within the airspace of the United States unless the operation meets the requirements of § 89.110 or § 89.115.

[5] 14 CFR Part 89 — § 89.401
§ 89.401 Applicability.
This subpart prescribes—
(a) Requirements for means of compliance with subpart D of this part.
(b) Procedural requirements for the submission and acceptance of means of compliance used in the d
```

---
## q11 (single)

**Question:** What are the weather limits for launching an unmanned free balloon?

**Reference:** Not at any altitude with clouds or obscuring phenomena of more than five-tenths coverage, and not below 60,000 feet where horizontal visibility is under five miles (plus other limits such as airport surface areas below 2,000 feet and over congested areas in the first 1,000 feet of ascent).

**Agent answer:**

Under Federal Aviation Regulations, the weather and operating limitations for launching and operating an unmanned free balloon include the following:

* **Cloud Coverage:** Cannot be operated at any altitude where clouds or obscuring phenomena exceed five-tenths (5/10) coverage `[14 CFR Part 101, § 101.33(b)]`.
* **Visibility:** Cannot be operated at any altitude below 60,000 feet standard pressure altitude where horizontal visibility is less than 5 miles `[14 CFR Part 101, § 101.33(c)]`.
* **Airspace Limitations:** Cannot be operated below 2,000 feet above the surface within the lateral boundaries of Class B, Class C, Class D, or Class E surface areas designated for an airport, unless authorized by ATC `[14 CFR Part 101, § 101.33(a)]`.

*Note: This information is for general educational purposes. Please consult with the FAA or a qualified aviation professional for official guidance regarding your specific operation.*

**Retrieved passages:**

```
[1] 14 CFR Part 101 — § 101.33
§ 101.33 Operating limitations.
No person may operate an unmanned free balloon—
(a) Unless otherwise authorized by ATC, below 2,000 feet above the surface within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport;
(b) At any altitude where there are clouds or obscuring phenomena of more than five-tenths coverage;
(c) At any altitude below 60,000 feet standard pressure altitude where the horizontal visibility is less than five miles;
(d) During the first 1,000 feet of ascent, over a congested area of a city, town, or settlement or an open-air assembly of persons not associated with the operation; or
(e) In such a manner that impact of the balloon, or part thereof including its payload, with the surface creates a hazard to persons or property not associated with the operation.

[2] 14 CFR Part 101 — § 101.13
§ 101.13 Operating limitations.
(a) Except as provided in paragraph (b) of this section, no person may operate a moored balloon or kite—
(1) Less than 500 feet from the base of any cloud;
(2) More than 500 feet above the surface of the earth;
(3) From an area where the ground visibility is less than three miles; or
(4) Within five miles of the boundary of any airport.
(b) Paragraph (a) of this section does not apply to the operation of a balloon or kite below the top of any structure and within 250 feet of it, if that shielded operation does not obscure any lighting on the structure.

[3] 14 CFR Part 107 — § 107.51
§ 107.51 Operating limitations for small unmanned aircraft.
A remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system must comply with all of the following operating limitations when operating a small unmanned aircraft system:
(a) The groundspeed of the small unmanned aircraft may not exceed 87 knots (100 miles per hour).
(b) The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, unless the small unmanned aircraft:
(1) Is flown within a 400-foot radius of a structure; and
(2) Does not fly higher than 400 feet above the structure's immediate uppermost limit.
(c) The minimum flight visibility, as observed from the location of the control station must be no less than 3 statute miles. For purposes of this section, flight visibility means the average slant distance from the control station at which prominent unlighted objects may be seen and identified by day and prominent lighted objects may be seen and identified by night.
(d) The minimum distance of the small unmanned aircraft from clouds must be no less than:
(1) 500 feet below the cloud; and
(2) 2,000 feet horizontally from the cloud.

[4] 14 CFR Part 101 — § 101.25
§ 101.25 Operating limitations for Class 2-High Power Rockets and Class 3-Advanced High Power Rockets.
When operating Class 2-High Power Rockets or Class 3-Advanced High Power Rockets, you must comply with the General Operating Limitations of § 101.23. In addition, you must not operate Class 2-High Power Rockets or Class 3-Advanced High Power Rockets—
(a) At any altitude where clouds or obscuring phenomena of more than five-tenths coverage prevails;
(b) At any altitude where the horizontal visibility is less than five miles;
(c) Into any cloud;
(d) Between sunset and sunrise without prior authorization from the FAA;
(e) Within 9.26 kilometers (5 nautical miles) of any airport boundary without prior authorization from the FAA;
(f) In controlled airspace without prior authorization from the FAA;
(g) Unless you observe the greater of the following separation distances from any person or property that is not associated with the operations:
(1) Not less than one-quarter the maximum expected altitude;
(2) 457 meters (1,500 ft.);
(h) Unless a person at least eighteen years old is present, is charged with ensuring the safety of the operation, and has final approval authority for initiating high-power rocket flight; and
(i) Unless reasonable precautions are provided to report and control a fire caused by rocket activities.

[5] 14 CFR Part 101 — § 101.37 (part 1/2)
§ 101.37 Notice requirements.
(a) Prelaunch notice: Except as provided in paragraph (b) of this section, no person may operate an unmanned free balloon unless, within 6 to 24 hours before beginning the operation, he gives the following information to the FAA ATC facility that is nearest to the place of intended operation:
(1) The balloon identification.
(2) The estimated date and time of launching, amended as necessary to remain within plus or minus 30 minutes.
(3) The location of the launching site.
(4) The cruising altitude.
(5) The forecast trajectory and estimated time to cruising altitude or 60,000 feet standard pressure altitude, whichever is lower.
(6) The length and diameter of the balloon, length of the suspension device, weight of the payload, and length of the trailing antenna.
(7) The duration of flight.
(8) The forecast time an
```

---
## q12 (single)

**Question:** What general limits apply to launching an amateur rocket?

**Reference:** It must be launched on a suborbital trajectory, must not cross into a foreign country without an agreement, must be unmanned, and must not create a hazard to persons, property or other aircraft.

**Agent answer:**

Under 14 CFR Part 101, an amateur rocket must be operated according to the following general limitations:

* **Suborbital Trajectory:** It must be launched on a suborbital trajectory [14 CFR Part 101, § 101.23(a)(1)].
* **Foreign Territory:** When launched, it must not cross into the territory of a foreign country unless an agreement is in place between the United States and that country [14 CFR Part 101, § 101.23(a)(2)].
* **Unmanned:** It must be unmanned [14 CFR Part 101, § 101.23(a)(3)].
* **No Hazards:** It must not create a hazard to persons, property, or other aircraft [14 CFR Part 101, § 101.23(a)(4)]. Additionally, no object may be dropped from an amateur rocket if doing so creates a hazard to other persons or their property [14 CFR Part 101, § 101.7(b)].
* **FAA Additional Limitations:** The FAA may specify additional operating limitations necessary to ensure air traffic is not adversely affected and public safety is not jeopardized [14 CFR Part 101, § 101.23(b)].

*(Note: Class 2—High-Power Rockets and Class 3—Advanced High-Power Rockets must comply with these general limitations as well as specific additional operational restrictions under [14 CFR Part 101, § 101.25].)*

*This information is provided for regulatory reference only and does not constitute legal advice. Please consult the FAA or a qualified aviation professional regarding your specific operation.*

**Retrieved passages:**

```
[1] 14 CFR Part 101 — § 101.23
§ 101.23 General operating limitations.
(a) You must operate an amateur rocket in such a manner that it:
(1) Is launched on a suborbital trajectory;
(2) When launched, must not cross into the territory of a foreign country unless an agreement is in place between the United States and the country of concern;
(3) Is unmanned; and
(4) Does not create a hazard to persons, property, or other aircraft.
(b) The FAA may specify additional operating limitations necessary to ensure that air traffic is not adversely affected, and public safety is not jeopardized.

[2] 14 CFR Part 101 — § 101.25
§ 101.25 Operating limitations for Class 2-High Power Rockets and Class 3-Advanced High Power Rockets.
When operating Class 2-High Power Rockets or Class 3-Advanced High Power Rockets, you must comply with the General Operating Limitations of § 101.23. In addition, you must not operate Class 2-High Power Rockets or Class 3-Advanced High Power Rockets—
(a) At any altitude where clouds or obscuring phenomena of more than five-tenths coverage prevails;
(b) At any altitude where the horizontal visibility is less than five miles;
(c) Into any cloud;
(d) Between sunset and sunrise without prior authorization from the FAA;
(e) Within 9.26 kilometers (5 nautical miles) of any airport boundary without prior authorization from the FAA;
(f) In controlled airspace without prior authorization from the FAA;
(g) Unless you observe the greater of the following separation distances from any person or property that is not associated with the operations:
(1) Not less than one-quarter the maximum expected altitude;
(2) 457 meters (1,500 ft.);
(h) Unless a person at least eighteen years old is present, is charged with ensuring the safety of the operation, and has final approval authority for initiating high-power rocket flight; and
(i) Unless reasonable precautions are provided to report and control a fire caused by rocket activities.

[3] 14 CFR Part 101 — § 101.7
§ 101.7 Hazardous operations.
(a) No person may operate any moored balloon, kite, amateur rocket, or unmanned free balloon in a manner that creates a hazard to other persons, or their property.
(b) No person operating any moored balloon, kite, amateur rocket, or unmanned free balloon may allow an object to be dropped therefrom, if such action creates a hazard to other persons or their property.

[4] 14 CFR Part 101 — § 101.21
§ 101.21 Applicability.
(a) This subpart applies to operating unmanned rockets. However, a person operating an unmanned rocket within a restricted area must comply with § 101.25(g)(2)) and with any additional limitations imposed by the using or controlling agency.
(b) A person operating an unmanned rocket other than an amateur rocket as defined in § 1.1 of this chapter must comply with 14 CFR Chapter III.

[5] 14 CFR Part 101 — § 101.22
§ 101.22 Definitions.
The following definitions apply to this subpart:
(a) Class 1—Model Rocket means an amateur rocket that:
(1) Uses no more than 125 grams (4.4 ounces) of propellant;
(2) Uses a slow-burning propellant;
(3) Is made of paper, wood, or breakable plastic;
(4) Contains no substantial metal parts; and
(5) Weighs no more than 1,500 grams (53 ounces), including the propellant.
(b) Class 2—High-Power Rocket means an amateur rocket other than a model rocket that is propelled by a motor or motors having a combined total impulse of 40,960 Newton-seconds (9,208 pound-seconds) or less.
(c) Class 3—Advanced High-Power Rocket means an amateur rocket other than a model rocket or high-power rocket.
```

---
## q13 (single)

**Question:** What near-vision standard does a first-class medical certificate require?

**Reference:** Near vision of 20/40 or better at 16 inches in each eye separately; if age 50 or older, 20/40 or better at both 16 and 32 inches.

**Agent answer:**

For a first-class airman medical certificate, the near-vision standards are:

* **General standard:** Near vision of 20/40 or better, Snellen equivalent, at 16 inches in each eye separately, with or without corrective lenses [14 CFR Part 67, § 67.103(b)].
* **Age 50 or older:** Near vision of 20/40 or better, Snellen equivalent, at both 16 inches and 32 inches in each eye separately, with or without corrective lenses [14 CFR Part 67, § 67.103(b)].

*This response summarizes regulatory standards and does not constitute legal or medical advice. Please consult the FAA or an Aviation Medical Examiner (AME) regarding your specific situation.*

**Retrieved passages:**

```
[1] 14 CFR Part 67 — § 67.103 (part 1/2)
§ 67.103 Eye.
Eye standards for a first-class airman medical certificate are:
(a) Distant visual acuity of 20/20 or better in each eye separately, with or without corrective lenses. If corrective lenses (spectacles or contact lenses) are necessary for 20/20 vision, the person may be eligible only on the condition that corrective lenses are worn while exercising the privileges of an airman certificate.
(b) Near vision of 20/40 or better, Snellen equivalent, at 16 inches in each eye separately, with or without corrective lenses. If age 50 or older, near vision of 20/40 or better, Snellen equivalent, at both 16 inches and 32 inches in each eye separately, with or without corrective lenses.
(c) Ability to perceive those colors necessary for the safe performance of airman duties.
(d) Normal fields of vision.
(e) No acute or chronic pathological condition of either eye or adnexa that interferes with the proper function of an eye, that may reasonably be expected to progress to that degree, or that may reasonably be expected to be aggravated by flying.

[2] 14 CFR Part 67 — § 67.203 (part 1/2)
§ 67.203 Eye.
Eye standards for a second-class airman medical certificate are:
(a) Distant visual acuity of 20/20 or better in each eye separately, with or without corrective lenses. If corrective lenses (spectacles or contact lenses) are necessary for 20/20 vision, the person may be eligible only on the condition that corrective lenses are worn while exercising the privileges of an airman certificate.
(b) Near vision of 20/40 or better, Snellen equivalent, at 16 inches in each eye separately, with or without corrective lenses. If age 50 or older, near vision of 20/40 or better, Snellen equivalent, at both 16 inches and 32 inches in each eye separately, with or without corrective lenses.
(c) Ability to perceive those colors necessary for the safe performance of airman duties.
(d) Normal fields of vision.
(e) No acute or chronic pathological condition of either eye or adnexa that interferes with the proper function of an eye, that may reasonably be expected to progress to that degree, or that may reasonably be expected to be aggravated by flying.

[3] 14 CFR Part 67 — § 67.303
§ 67.303 Eye.
Eye standards for a third-class airman medical certificate are:
(a) Distant visual acuity of 20/40 or better in each eye separately, with or without corrective lenses. If corrective lenses (spectacles or contact lenses) are necessary for 20/40 vision, the person may be eligible only on the condition that corrective lenses are worn while exercising the privileges of an airman certificate.
(b) Near vision of 20/40 or better, Snellen equivalent, at 16 inches in each eye separately, with or without corrective lenses.
(c) Ability to perceive those colors necessary for the safe performance of airman duties.
(d) No acute or chronic pathological condition of either eye or adnexa that interferes with the proper function of an eye, that may reasonably be expected to progress to that degree, or that may reasonably be expected to be aggravated by flying.

[4] 14 CFR Part 67 — § 67.103 (part 2/2)
§ 67.103 Eye.
(f) Bifoveal fixation and vergence-phoria relationship sufficient to prevent a break in fusion under conditions that may reasonably be expected to occur in performing airman duties. Tests for the factors named in this paragraph are not required except for persons found to have more than 1 prism diopter of hyperphoria, 6 prism diopters of esophoria, or 6 prism diopters of exophoria. If any of these values are exceeded, the Federal Air Surgeon may require the person to be examined by a qualified eye specialist to determine if there is bifoveal fixation and an adequate vergence-phoria relationship. However, if otherwise eligible, the person is issued a medical certificate pending the results of the examination.

[5] 14 CFR Part 67 — § 67.113 (part 1/2)
§ 67.113 General medical condition.
The general medical standards for a first-class airman medical certificate are:
(a) No established medical history or clinical diagnosis of diabetes mellitus that requires insulin or any other hypoglycemic drug for control.
(b) No other organic, functional, or structural disease, defect, or limitation that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the condition involved, finds—
(1) Makes the person unable to safely perform the duties or exercise the privileges of the airman certificate applied for or held; or
(2) May reasonably be expected, for the maximum duration of the airman medical certificate applied for or held, to make the person unable to perform those duties or exercise those privileges.
(c) No medication or other treatment that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the medication or other treatment involved, finds—
(1) Makes the person unable to safely perform the duties or exercise t
```

---
## q14 (single)

**Question:** Can someone who needs insulin for diabetes hold a first-class medical certificate?

**Reference:** No. The standard requires no established history or diagnosis of diabetes mellitus that requires insulin or another hypoglycemic drug for control.

**Agent answer:**

Under standard medical rules, the general medical standards for a first-class airman medical certificate state that an applicant must have no established medical history or clinical diagnosis of diabetes mellitus that requires insulin or any other hypoglycemic drug for control [14 CFR Part 67, § 67.113(a)].

However, an individual who does not meet this medical standard may apply for discretionary issuance of a medical certificate [14 CFR Part 67, § 67.115]. At the discretion of the Federal Air Surgeon, an Authorization for Special Issuance of a Medical Certificate may be granted if the applicant demonstrates to the satisfaction of the Federal Air Surgeon that the duties authorized by the class of medical certificate applied for can be performed without endangering public safety [14 CFR Part 67, § 67.401(a)].

*This answer is for informational purposes only and does not constitute medical or legal advice. Please consult an Aviation Medical Examiner (AME) or the FAA regarding eligibility for a specific medical condition.*

**Retrieved passages:**

```
[1] 14 CFR Part 67 — § 67.113 (part 1/2)
§ 67.113 General medical condition.
The general medical standards for a first-class airman medical certificate are:
(a) No established medical history or clinical diagnosis of diabetes mellitus that requires insulin or any other hypoglycemic drug for control.
(b) No other organic, functional, or structural disease, defect, or limitation that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the condition involved, finds—
(1) Makes the person unable to safely perform the duties or exercise the privileges of the airman certificate applied for or held; or
(2) May reasonably be expected, for the maximum duration of the airman medical certificate applied for or held, to make the person unable to perform those duties or exercise those privileges.
(c) No medication or other treatment that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the medication or other treatment involved, finds—
(1) Makes the person unable to safely perform the duties or exercise the privileges of the airman certificate applied for or held; or

[2] 14 CFR Part 67 — § 67.313 (part 1/2)
§ 67.313 General medical condition.
The general medical standards for a third-class airman medical certificate are:
(a) No established medical history or clinical diagnosis of diabetes mellitus that requires insulin or any other hypoglycemic drug for control.
(b) No other organic, functional, or structural disease, defect, or limitation that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the condition involved, finds—
(1) Makes the person unable to safely perform the duties or exercise the privileges of the airman certificate applied for or held; or
(2) May reasonably be expected, for the maximum duration of the airman medical certificate applied for or held, to make the person unable to perform those duties or exercise those privileges.
(c) No medication or other treatment that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the medication or other treatment involved, finds—
(1) Makes the person unable to safely perform the duties or exercise the privileges of the airman certificate applied for or held; or

[3] 14 CFR Part 67 — § 67.213 (part 1/2)
§ 67.213 General medical condition.
The general medical standards for a second-class airman medical certificate are:
(a) No established medical history or clinical diagnosis of diabetes mellitus that requires insulin or any other hypoglycemic drug for control.
(b) No other organic, functional, or structural disease, defect, or limitation that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the condition involved, finds—
(1) Makes the person unable to safely perform the duties or exercise the privileges of the airman certificate applied for or held; or
(2) May reasonably be expected, for the maximum duration of the airman medical certificate applied for or held, to make the person unable to perform those duties or exercise those privileges.
(c) No medication or other treatment that the Federal Air Surgeon, based on the case history and appropriate, qualified medical judgment relating to the medication or other treatment involved, finds—
(1) Makes the person unable to safely perform the duties or exercise the privileges of the airman certificate applied for or held; or

[4] 14 CFR Part 67 — § 67.111
§ 67.111 Cardiovascular.
Cardiovascular standards for a first-class airman medical certificate are:
(a) No established medical history or clinical diagnosis of any of the following:
(1) Myocardial infarction;
(2) Angina pectoris;
(3) Coronary heart disease that has required treatment or, if untreated, that has been symptomatic or clinically significant;
(4) Cardiac valve replacement;
(5) Permanent cardiac pacemaker implantation; or
(6) Heart replacement;
(b) A person applying for first-class medical certification must demonstrate an absence of myocardial infarction and other clinically significant abnormality on electrocardiographic examination:
(1) At the first application after reaching the 35th birthday; and
(2) On an annual basis after reaching the 40th birthday.
(c) An electrocardiogram will satisfy a requirement of paragraph (b) of this section if it is dated no earlier than 60 days before the date of the application it is to accompany and was performed and transmitted according to acceptable standards and techniques.

[5] 14 CFR Part 67 — § 67.101
§ 67.101 Eligibility.
To be eligible for a first-class airman medical certificate, and to remain eligible for a first-class airman medical certificate, a person must meet the requirements of this subpart.

[1] 14 CFR Part 67 — § 67.401 (part 1/6)
§ 67.401 Special issuance of medical certificates.
(a) At the discretion of the Federal Air Surgeon
```

---
## q15 (single)

**Question:** How long after drinking alcohol can I act as a crew member, and what is the alcohol limit?

**Reference:** Not within 8 hours after consuming any alcoholic beverage, and not with an alcohol concentration of 0.04 or greater (nor while under the influence).

**Agent answer:**

Under US Federal Aviation Regulations, no person may act or attempt to act as a crewmember of a civil aircraft:

* **Time limit:** Within **8 hours** after consuming any alcoholic beverage [14 CFR Part 91 Subpart A, § 91.17(a)(1)].
* **Alcohol concentration limit:** While having an alcohol concentration of **0.04 or greater** in a blood or breath specimen (defined as grams of alcohol per deciliter of blood or grams of alcohol per 210 liters of breath) [14 CFR Part 91 Subpart A, § 91.17(a)(4)].
* **Under the influence:** While under the influence of alcohol [14 CFR Part 91 Subpart A, § 91.17(a)(2)].

These requirements also apply to small unmanned aircraft system (sUAS) operations under Part 107, including remote pilots in command, visual observers, and individuals manipulating the flight controls [14 CFR Part 107, § 107.27].

*Disclaimer: This information is provided for regulatory reference only and does not constitute legal advice. Please consult the FAA or a qualified legal professional regarding specific situations.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart A — § 91.17 (part 1/3)
§ 91.17 Alcohol or drugs.
(a) No person may act or attempt to act as a crewmember of a civil aircraft—
(1) Within 8 hours after the consumption of any alcoholic beverage;
(2) While under the influence of alcohol;
(3) While using any drug that affects the person's faculties in any way contrary to safety; or
(4) While having an alcohol concentration of 0.04 or greater in a blood or breath specimen. Alcohol concentration means grams of alcohol per deciliter of blood or grams of alcohol per 210 liters of breath.
(b) Except in an emergency, no pilot of a civil aircraft may allow a person who appears to be intoxicated or who demonstrates by manner or physical indications that the individual is under the influence of drugs (except a medical patient under proper care) to be carried in that aircraft.
(c) A crewmember shall do the following:
(1) On request of a law enforcement officer, submit to a test to indicate the alcohol concentration in the blood or breath, when—
(i) The law enforcement officer is authorized under State or local law to conduct the test or to have the test conducted; and

[2] 14 CFR Part 91 Subpart A — § 91.17 (part 2/3)
§ 91.17 Alcohol or drugs.
(ii) The law enforcement officer is requesting submission to the test to investigate a suspected violation of State or local law governing the same or substantially similar conduct prohibited by paragraph (a)(1), (a)(2), or (a)(4) of this section.
(2) Whenever the FAA has a reasonable basis to believe that a person may have violated paragraph (a)(1), (a)(2), or (a)(4) of this section, on request of the FAA, that person must furnish to the FAA the results, or authorize any clinic, hospital, or doctor, or other person to release to the FAA, the results of each test taken within 4 hours after acting or attempting to act as a crewmember that indicates an alcohol concentration in the blood or breath specimen.
(d) Whenever the Administrator has a reasonable basis to believe that a person may have violated paragraph (a)(3) of this section, that person shall, upon request by the Administrator, furnish the Administrator, or authorize any clinic, hospital, doctor, or other person to release to the Administrator, the results of each test taken within 4 hours after acting or attempting to act as a crewmember that indicates the presence of any drugs in the body.

[3] 14 CFR Part 107 — § 107.27
§ 107.27 Alcohol or drugs.
A person manipulating the flight controls of a small unmanned aircraft system or acting as a remote pilot in command or visual observer must comply with the provisions of §§ 91.17 and 91.19 of this chapter.

[4] 14 CFR Part 107 — § 107.59
§ 107.59 Refusal to submit to an alcohol test or to furnish test results.
A refusal to submit to a test to indicate the percentage by weight of alcohol in the blood, when requested by a law enforcement officer in accordance with § 91.17(c) of this chapter, or a refusal to furnish or authorize the release of the test results requested by the Administrator in accordance with § 91.17(c) or (d) of this chapter, is grounds for:
(a) Denial of an application for a remote pilot certificate with a small UAS rating for a period of up to 1 year after the date of that refusal; or
(b) Suspension or revocation of a remote pilot certificate with a small UAS rating.

[5] 14 CFR Part 107 — § 107.57
§ 107.57 Offenses involving alcohol or drugs.
(a) A conviction for the violation of any Federal or State statute relating to the growing, processing, manufacture, sale, disposition, possession, transportation, or importation of narcotic drugs, marijuana, or depressant or stimulant drugs or substances is grounds for:
(1) Denial of an application for a remote pilot certificate with a small UAS rating for a period of up to 1 year after the date of final conviction; or
(2) Suspension or revocation of a remote pilot certificate with a small UAS rating.
(b) Committing an act prohibited by § 91.17(a) or § 91.19(a) of this chapter is grounds for:
(1) Denial of an application for a remote pilot certificate with a small UAS rating for a period of up to 1 year after the date of that act; or
(2) Suspension or revocation of a remote pilot certificate with a small UAS rating.
```

---
## q16 (single)

**Question:** What is the minimum altitude when flying over a congested area?

**Reference:** 1,000 feet above the highest obstacle within a horizontal radius of 2,000 feet of the aircraft, except when necessary for takeoff or landing.

**Agent answer:**

Except when necessary for takeoff or landing, when flying over any congested area of a city, town, or settlement, or over any open-air assembly of persons, the minimum altitude is **1,000 feet above the highest obstacle within a horizontal radius of 2,000 feet of the aircraft** [14 CFR Part 91 Subpart B, § 91.119(b)].

**Exceptions:**
* A helicopter, powered parachute, or weight-shift-control aircraft may be operated at less than these minimums if the operation is conducted without hazard to persons or property on the surface, provided a helicopter pilot complies with any routes or altitudes specifically prescribed for helicopters by the FAA [14 CFR Part 91 Subpart B, § 91.119(d)].

*This response provides regulatory information and does not constitute formal legal advice. For specific flight operations or interpretations, please consult the FAA or a qualified aviation legal professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart B — § 91.119 (part 1/2)
§ 91.119 Minimum safe altitudes: General.
Except when necessary for takeoff or landing, no person may operate an aircraft below the following altitudes:
(a) Anywhere. An altitude allowing, if a power unit fails, an emergency landing without undue hazard to persons or property on the surface.
(b) Over congested areas. Over any congested area of a city, town, or settlement, or over any open air assembly of persons, an altitude of 1,000 feet above the highest obstacle within a horizontal radius of 2,000 feet of the aircraft.
(c) Over other than congested areas. An altitude of 500 feet above the surface, except over open water or sparsely populated areas. In those cases, the aircraft may not be operated closer than 500 feet to any person, vessel, vehicle, or structure.
(d) Helicopters, powered parachutes, and weight-shift-control aircraft. If the operation is conducted without hazard to persons or property on the surface—
(1) A helicopter may be operated at less than the minimums prescribed in paragraph (b) or (c) of this section, provided each person operating the helicopter complies with any routes or altitudes specifically prescribed for helicopters by the FAA; and

[2] 14 CFR Part 91 Subpart D — § 91.303
§ 91.303 Aerobatic flight.
No person may operate an aircraft in aerobatic flight—
(a) Over any congested area of a city, town, or settlement;
(b) Over an open air assembly of persons;
(c) Within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport;
(d) Within 4 nautical miles of the center line of any Federal airway;
(e) Below an altitude of 1,500 feet above the surface; or
(f) When flight visibility is less than 3 statute miles.

[3] 14 CFR Part 101 — § 101.33
§ 101.33 Operating limitations.
No person may operate an unmanned free balloon—
(a) Unless otherwise authorized by ATC, below 2,000 feet above the surface within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport;
(b) At any altitude where there are clouds or obscuring phenomena of more than five-tenths coverage;
(c) At any altitude below 60,000 feet standard pressure altitude where the horizontal visibility is less than five miles;
(d) During the first 1,000 feet of ascent, over a congested area of a city, town, or settlement or an open-air assembly of persons not associated with the operation; or
(e) In such a manner that impact of the balloon, or part thereof including its payload, with the surface creates a hazard to persons or property not associated with the operation.

[4] 14 CFR Part 91 Subpart B — § 91.159
§ 91.159 VFR cruising altitude or flight level.
Except while holding in a holding pattern of 2 minutes or less, or while turning, each person operating an aircraft under VFR in level cruising flight more than 3,000 feet above the surface shall maintain the appropriate altitude or flight level prescribed below, unless otherwise authorized by ATC:
(a) When operating below 18,000 feet MSL and—
(1) On a magnetic course of zero degrees through 179 degrees, any odd thousand foot MSL altitude + 500 feet (such as 3,500, 5,500, or 7,500); or
(2) On a magnetic course of 180 degrees through 359 degrees, any even thousand foot MSL altitude + 500 feet (such as 4,500, 6,500, or 8,500).
(b) When operating above 18,000 feet MSL, maintain the altitude or flight level assigned by ATC.

[5] 14 CFR Part 91 Subpart B — § 91.129 (part 3/5)
§ 91.129 Operations in Class D airspace.
(e) Minimum altitudes when operating to an airport in Class D airspace. (1) Unless required by the applicable distance-from-cloud criteria, each pilot operating a large or turbine-powered airplane must enter the traffic pattern at an altitude of at least 1,500 feet above the elevation of the airport and maintain at least 1,500 feet until further descent is required for a safe landing.
(2) Each pilot operating a large or turbine-powered airplane approaching to land on a runway served by an instrument approach procedure with vertical guidance, if the airplane is so equipped, must:
(i) Operate that airplane at an altitude at or above the glide path between the published final approach fix and the decision altitude (DA), or decision height (DH), as applicable; or
(ii) If compliance with the applicable distance-from-cloud criteria requires glide path interception closer in, operate that airplane at or above the glide path, between the point of interception of glide path and the DA or the DH.
(3) Each pilot operating an airplane approaching to land on a runway served by a visual approach slope indicator must maintain an altitude at or above the glide path until a lower altitude is necessary for a safe landing.
```

---
## q17 (single)

**Question:** What is the speed limit for aircraft below 10,000 feet MSL?

**Reference:** No more than 250 knots (288 mph) indicated airspeed, unless authorized by the Administrator.

**Agent answer:**

Unless otherwise authorized by the Administrator, no person may operate an aircraft below 10,000 feet MSL at an indicated airspeed of more than **250 knots (288 mph)** [14 CFR Part 91 Subpart B, § 91.117(a)].

### Additional Speed Limitations and Exceptions Below 10,000 Feet MSL:
* **Class C or Class D Airspace:** At or below 2,500 feet above the surface within 4 nautical miles of the primary airport of a Class C or Class D airspace area, the maximum indicated airspeed is **200 knots (230 mph)**, unless otherwise authorized or required by ATC. (This specific limit does not apply to operations within Class B airspace) [14 CFR Part 91 Subpart B, § 91.117(b)].
* **Underlying Class B Airspace / VFR Corridors:** In the airspace underlying a Class B airspace area designated for an airport, or in a VFR corridor designated through Class B airspace, the maximum indicated airspeed is **200 knots (230 mph)** [14 CFR Part 91 Subpart B, § 91.117(c)].
* **Minimum Safe Airspeed Exception:** If the minimum safe airspeed for a particular operation is greater than the prescribed maximum speed, the aircraft may be operated at that minimum safe speed [14 CFR Part 91 Subpart B, § 91.117(d)].

*Note: This response is for informational purposes only. Please consult the FAA or a qualified aviation legal professional regarding specific flight operations.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart B — § 91.117
§ 91.117 Aircraft speed.
(a) Unless otherwise authorized by the Administrator, no person may operate an aircraft below 10,000 feet MSL at an indicated airspeed of more than 250 knots (288 m.p.h.).
(b) Unless otherwise authorized or required by ATC, no person may operate an aircraft at or below 2,500 feet above the surface within 4 nautical miles of the primary airport of a Class C or Class D airspace area at an indicated airspeed of more than 200 knots (230 mph.). This paragraph (b) does not apply to any operations within a Class B airspace area. Such operations shall comply with paragraph (a) of this section.
(c) No person may operate an aircraft in the airspace underlying a Class B airspace area designated for an airport or in a VFR corridor designated through such a Class B airspace area, at an indicated airspeed of more than 200 knots (230 mph).
(d) If the minimum safe airspeed for any particular operation is greater than the maximum speed prescribed in this section, the aircraft may be operated at that minimum speed.

[2] 14 CFR Part 91 Subpart B — § 91.119 (part 1/2)
§ 91.119 Minimum safe altitudes: General.
Except when necessary for takeoff or landing, no person may operate an aircraft below the following altitudes:
(a) Anywhere. An altitude allowing, if a power unit fails, an emergency landing without undue hazard to persons or property on the surface.
(b) Over congested areas. Over any congested area of a city, town, or settlement, or over any open air assembly of persons, an altitude of 1,000 feet above the highest obstacle within a horizontal radius of 2,000 feet of the aircraft.
(c) Over other than congested areas. An altitude of 500 feet above the surface, except over open water or sparsely populated areas. In those cases, the aircraft may not be operated closer than 500 feet to any person, vessel, vehicle, or structure.
(d) Helicopters, powered parachutes, and weight-shift-control aircraft. If the operation is conducted without hazard to persons or property on the surface—
(1) A helicopter may be operated at less than the minimums prescribed in paragraph (b) or (c) of this section, provided each person operating the helicopter complies with any routes or altitudes specifically prescribed for helicopters by the FAA; and

[3] 14 CFR Part 91 Subpart D — § 91.303
§ 91.303 Aerobatic flight.
No person may operate an aircraft in aerobatic flight—
(a) Over any congested area of a city, town, or settlement;
(b) Over an open air assembly of persons;
(c) Within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport;
(d) Within 4 nautical miles of the center line of any Federal airway;
(e) Below an altitude of 1,500 feet above the surface; or
(f) When flight visibility is less than 3 statute miles.

[4] 14 CFR Part 91 Subpart B — § 91.177 (part 2/2)
§ 91.177 Minimum altitudes for IFR operations.
(ii) In any other case, an altitude of 1,000 feet above the highest obstacle within a horizontal distance of 4 nautical miles from the course to be flown.
(b) Climb. Climb to a higher minimum IFR altitude shall begin immediately after passing the point beyond which that minimum altitude applies, except that when ground obstructions intervene, the point beyond which that higher minimum altitude applies shall be crossed at or above the applicable MCA.

[5] 14 CFR Part 91 Subpart B — § 91.157 (part 1/2)
§ 91.157 Special VFR weather minimums.
(a) Except as provided in appendix D, section 3, of this part, special VFR operations may be conducted under the weather minimums and requirements of this section, instead of those contained in § 91.155, below 10,000 feet MSL within the airspace contained by the upward extension of the lateral boundaries of the controlled airspace designated to the surface for an airport.
(b) Special VFR operations may only be conducted—
(1) With an ATC clearance;
(2) Clear of clouds;
(3) Except for helicopters, when flight visibility is at least 1 statute mile; and
(4) Except for helicopters, between sunrise and sunset (or in Alaska, when the sun is 6 degrees or less below the horizon) unless—
(i) The person being granted the ATC clearance meets the applicable requirements for instrument flight under part 61 of this chapter; and
(ii) The aircraft is equipped as required in § 91.205(d).
(c) No person may take off or land an aircraft (other than a helicopter) under special VFR—
(1) Unless ground visibility is at least 1 statute mile; or
```

---
## q18 (single)

**Question:** What are the basic VFR weather minimums in Class E airspace below 10,000 feet MSL?

**Reference:** 3 statute miles flight visibility and distance from clouds of 500 feet below, 1,000 feet above and 2,000 feet horizontal.

**Agent answer:**

The corpus does not cover the complete table of general VFR flight visibility and cloud clearance minimums under 14 CFR § 91.155(a). 

The returned passages from 14 CFR § 91.155 do, however, cover the following VFR weather rules regarding Class E airspace:

* **Surface area ground/flight visibility:** Within the lateral boundaries of the surface area of Class E airspace designated for an airport, taking off, landing, or entering the traffic pattern under VFR requires a ground visibility of at least 3 statute miles (or flight visibility of at least 3 statute miles if ground visibility is not reported) [14 CFR Part 91 Subpart B, § 91.155(d)].
* **Ceiling minimum for surface areas:** Within the lateral boundaries of controlled airspace designated to the surface for an airport, operating an aircraft beneath the ceiling under VFR is prohibited when the ceiling is less than 1,000 feet [14 CFR Part 91 Subpart B, § 91.155(c)].
* **Base altitude:** An aircraft operating at the base altitude of a Class E airspace area is considered to be within the airspace directly below that area [14 CFR Part 91 Subpart B, § 91.155(e)].

For the complete visual weather minimums table (flight visibility and distance from clouds), please consult the official FAA text of 14 CFR § 91.155 or contact the FAA or a qualified aviation professional for your specific operating situation.

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart B — § 91.155 (part 2/2)
§ 91.155 Basic VFR weather minimums.
(c) Except as provided in § 91.157, no person may operate an aircraft beneath the ceiling under VFR within the lateral boundaries of controlled airspace designated to the surface for an airport when the ceiling is less than 1,000 feet.
(d) Except as provided in § 91.157 of this part, no person may take off or land an aircraft, or enter the traffic pattern of an airport, under VFR, within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport—
(1) Unless ground visibility at that airport is at least 3 statute miles; or
(2) If ground visibility is not reported at that airport, unless flight visibility during landing or takeoff, or while operating in the traffic pattern is at least 3 statute miles.
(e) For the purpose of this section, an aircraft operating at the base altitude of a Class E airspace area is considered to be within the airspace directly below that area.

[2] 14 CFR Part 91 Subpart B — § 91.155 (part 1/2)
§ 91.155 Basic VFR weather minimums.
(a) Except as provided in paragraph (b) of this section and § 91.157, no person may operate an aircraft under VFR when the flight visibility is less, or at a distance from clouds that is less, than that prescribed for the corresponding altitude and class of airspace in the following table:
(b) Class G Airspace. Notwithstanding the provisions of paragraph (a) of this section, the following operations may be conducted in Class G airspace below 1,200 feet above the surface:
(1) Helicopter. A helicopter may be operated clear of clouds in an airport traffic pattern within 1/2 mile of the runway or helipad of intended landing if the flight visibility is not less than 1/2 statute mile.
(2) Airplane, powered parachute, or weight-shift-control aircraft. If the visibility is less than 3 statute miles but not less than 1 statute mile during night hours and you are operating in an airport traffic pattern within 1/2 mile of the runway, you may operate an airplane, powered parachute, or weight-shift-control aircraft clear of clouds.

[3] 14 CFR Part 91 Subpart B — § 91.157 (part 1/2)
§ 91.157 Special VFR weather minimums.
(a) Except as provided in appendix D, section 3, of this part, special VFR operations may be conducted under the weather minimums and requirements of this section, instead of those contained in § 91.155, below 10,000 feet MSL within the airspace contained by the upward extension of the lateral boundaries of the controlled airspace designated to the surface for an airport.
(b) Special VFR operations may only be conducted—
(1) With an ATC clearance;
(2) Clear of clouds;
(3) Except for helicopters, when flight visibility is at least 1 statute mile; and
(4) Except for helicopters, between sunrise and sunset (or in Alaska, when the sun is 6 degrees or less below the horizon) unless—
(i) The person being granted the ATC clearance meets the applicable requirements for instrument flight under part 61 of this chapter; and
(ii) The aircraft is equipped as required in § 91.205(d).
(c) No person may take off or land an aircraft (other than a helicopter) under special VFR—
(1) Unless ground visibility is at least 1 statute mile; or

[4] 14 CFR Part 101 — § 101.33
§ 101.33 Operating limitations.
No person may operate an unmanned free balloon—
(a) Unless otherwise authorized by ATC, below 2,000 feet above the surface within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport;
(b) At any altitude where there are clouds or obscuring phenomena of more than five-tenths coverage;
(c) At any altitude below 60,000 feet standard pressure altitude where the horizontal visibility is less than five miles;
(d) During the first 1,000 feet of ascent, over a congested area of a city, town, or settlement or an open-air assembly of persons not associated with the operation; or
(e) In such a manner that impact of the balloon, or part thereof including its payload, with the surface creates a hazard to persons or property not associated with the operation.

[5] 14 CFR Part 107 — § 107.51
§ 107.51 Operating limitations for small unmanned aircraft.
A remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system must comply with all of the following operating limitations when operating a small unmanned aircraft system:
(a) The groundspeed of the small unmanned aircraft may not exceed 87 knots (100 miles per hour).
(b) The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, unless the small unmanned aircraft:
(1) Is flown within a 400-foot radius of a structure; and
(2) Does not fly higher than 400 feet above the structure's immediate uppermost limit.
(c) The minimum flight visibility, as observed from the location of the control station must be no less than 3 statute miles. For purposes of 
```

---
## q19 (single)

**Question:** How much fuel reserve is needed for a daytime VFR flight in an airplane?

**Reference:** Enough to fly to the first point of intended landing and then at least 30 minutes at normal cruising speed (45 minutes at night).

**Agent answer:**

For a daytime flight under VFR conditions in an airplane, you must carry enough fuel—considering wind and forecast weather conditions—to fly to the first point of intended landing and, assuming normal cruising speed, to fly beyond that point for at least **30 minutes** [14 CFR Part 91, § 91.151(a)(1)].

*Note: This response summarizes regulatory requirements and does not constitute official legal advice or flight planning guidance. Always confirm requirements with the FAA or a qualified aviation professional for your specific situation.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart B — § 91.151
§ 91.151 Fuel requirements for flight in VFR conditions.
(a) No person may begin a flight in an airplane under VFR conditions unless (considering wind and forecast weather conditions) there is enough fuel to fly to the first point of intended landing and, assuming normal cruising speed—
(1) During the day, to fly after that for at least 30 minutes; or
(2) At night, to fly after that for at least 45 minutes.
(b) No person may begin a flight in a rotorcraft under VFR conditions unless (considering wind and forecast weather conditions) there is enough fuel to fly to the first point of intended landing and, assuming normal cruising speed, to fly after that for at least 20 minutes.

[2] 14 CFR Part 91 Subpart B — § 91.153
§ 91.153 VFR flight plan: Information required.
(a) Information required. Unless otherwise authorized by ATC, each person filing a VFR flight plan shall include in it the following information:
(1) The aircraft identification number and, if necessary, its radio call sign.
(2) The type of the aircraft or, in the case of a formation flight, the type of each aircraft and the number of aircraft in the formation.
(3) The full name and address of the pilot in command or, in the case of a formation flight, the formation commander.
(4) The point and proposed time of departure.
(5) The proposed route, cruising altitude (or flight level), and true airspeed at that altitude.
(6) The point of first intended landing and the estimated elapsed time until over that point.
(7) The amount of fuel on board (in hours).
(8) The number of persons in the aircraft, except where that information is otherwise readily available to the FAA.
(9) Any other information the pilot in command or ATC believes is necessary for ATC purposes.
(b) Cancellation. When a flight plan has been activated, the pilot in command, upon canceling or completing the flight under the flight plan, shall notify an FAA Flight Service Station or ATC facility.

[3] 14 CFR Part 91 Subpart B — § 91.167 (part 1/2)
§ 91.167 Fuel requirements for flight in IFR conditions.
(a) No person may operate a civil aircraft in IFR conditions unless it carries enough fuel (considering weather reports and forecasts and weather conditions) to—
(1) Complete the flight to the first airport of intended landing;
(2) Except as provided in paragraph (b) of this section, fly from that airport to the alternate airport; and
(3) Fly after that for 45 minutes at normal cruising speed or, for helicopters, fly after that for 30 minutes at normal cruising speed.
(b) Paragraph (a)(2) of this section does not apply if:
(1) Part 97 of this chapter prescribes a standard instrument approach procedure to, or a special instrument approach procedure has been issued by the Administrator to the operator for, the first airport of intended landing; and
(2) Appropriate weather reports or weather forecasts, or a combination of them, indicate the following:
(i) For aircraft other than helicopters. For at least 1 hour before and for 1 hour after the estimated time of arrival, the ceiling will be at least 2,000 feet above the airport elevation and the visibility will be at least 3 statute miles.

[4] 14 CFR Part 91 Subpart C — § 91.205 (part 1/7)
§ 91.205 Powered civil aircraft with standard U.S. airworthiness certificates: Instrument and equipment requirements.
(a) General. Except as provided in paragraphs (c)(3) and (e) of this section, no person may operate a powered civil aircraft with a standard U.S. airworthiness certificate in any operation described in paragraphs (b) through (f) of this section unless that aircraft contains the instruments and equipment specified in those paragraphs (or FAA-approved equivalents) for that type of operation, and those instruments and items of equipment are in operable condition.
(b) Visual-flight rules (day). For VFR flight during the day, the following instruments and equipment are required:
(1) Airspeed indicator.
(2) Altimeter.
(3) Magnetic direction indicator.
(4) Tachometer for each engine.
(5) Oil pressure gauge for each engine using pressure system.
(6) Temperature gauge for each liquid-cooled engine.
(7) Oil temperature gauge for each air-cooled engine.
(8) Manifold pressure gauge for each altitude engine.
(9) Fuel gauge indicating the quantity of fuel in each tank.
(10) Landing gear position indicator, if the aircraft has a retractable landing gear.

[5] 14 CFR Part 91 Subpart B — § 91.167 (part 2/2)
§ 91.167 Fuel requirements for flight in IFR conditions.
(ii) For helicopters. At the estimated time of arrival and for 1 hour after the estimated time of arrival, the ceiling will be at least 1,000 feet above the airport elevation, or at least 400 feet above the lowest applicable approach minima, whichever is higher, and the visibility will be at least 2 statute miles.
```

---
## q20 (single)

**Question:** When do I need supplemental oxygen for the crew?

**Reference:** Above 12,500 feet up to 14,000 feet MSL for flight of more than 30 minutes at those altitudes; above 14,000 feet during the entire time at those altitudes; and above 15,000 feet every occupant must be provided with oxygen.

**Agent answer:**

Under 14 CFR Part 91, the requirements for supplemental oxygen for the required minimum flight crew depend on cabin pressure altitude and aircraft pressurization:

### General Requirements (Unpressurized Cabin / Cabin Pressure Altitude)
* **Above 12,500 feet (MSL) up to and including 14,000 feet (MSL):** The minimum required flight crew must be provided with and use supplemental oxygen for any portion of the flight at those altitudes that lasts longer than 30 minutes [14 CFR Part 91 Subpart C, § 91.211(a)(1)].
* **Above 14,000 feet (MSL):** The minimum required flight crew must be provided with and use supplemental oxygen during the entire flight time at those altitudes [14 CFR Part 91 Subpart C, § 91.211(a)(2)].
*(Note: Above 15,000 feet MSL, each occupant of the aircraft must also be provided with supplemental oxygen [14 CFR Part 91 Subpart C, § 91.211(a)(3)].)*

### Pressurized Cabin Aircraft
* **Above Flight Level (FL) 250:** At least a 10-minute supply of supplemental oxygen must be available for each occupant in the event a descent is required due to loss of pressurization [14 CFR Part 91 Subpart C, § 91.211(b)(1)(i)].
* **Above FL 350:** One pilot at the controls must continuously wear and use a sealed oxygen mask that supplies oxygen (or automatically supplies oxygen if cabin pressure altitude exceeds 14,000 feet MSL) [14 CFR Part 91 Subpart C, § 91.211(b)(1)(ii)].
  * *Exception:* The pilot does not need to wear the mask at or below FL 410 if two pilots are at the controls and each has a quick-donning type oxygen mask reachable with one hand from the ready position within 5 seconds [14 CFR Part 91 Subpart C, § 91.211(b)(1)(ii)].
  * *If one pilot leaves:* Above FL 350, if one pilot leaves the controls for any reason, the remaining pilot must put on and use an oxygen mask until the other returns [14 CFR Part 91 Subpart C, § 91.211(b)(2)].

*This information is provided for regulatory reference only and does not constitute legal advice. Please consult the FAA or a qualified aviation legal professional regarding your specific operational situation.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart C — § 91.211 (part 1/2)
§ 91.211 Supplemental oxygen.
(a) General. No person may operate a civil aircraft of U.S. registry—
(1) At cabin pressure altitudes above 12,500 feet (MSL) up to and including 14,000 feet (MSL) unless the required minimum flight crew is provided with and uses supplemental oxygen for that part of the flight at those altitudes that is of more than 30 minutes duration;
(2) At cabin pressure altitudes above 14,000 feet (MSL) unless the required minimum flight crew is provided with and uses supplemental oxygen during the entire flight time at those altitudes; and
(3) At cabin pressure altitudes above 15,000 feet (MSL) unless each occupant of the aircraft is provided with supplemental oxygen.
(b) Pressurized cabin aircraft. (1) No person may operate a civil aircraft of U.S. registry with a pressurized cabin—
(i) At flight altitudes above flight level 250 unless at least a 10-minute supply of supplemental oxygen, in addition to any oxygen required to satisfy paragraph (a) of this section, is available for each occupant of the aircraft for use in the event that a descent is necessitated by loss of cabin pressurization; and

[2] 14 CFR Part 91 Subpart C — § 91.211 (part 2/2)
§ 91.211 Supplemental oxygen.
(ii) At flight altitudes above flight level 350 unless one pilot at the controls of the airplane is wearing and using an oxygen mask that is secured and sealed and that either supplies oxygen at all times or automatically supplies oxygen whenever the cabin pressure altitude of the airplane exceeds 14,000 feet (MSL), except that the one pilot need not wear and use an oxygen mask while at or below flight level 410 if there are two pilots at the controls and each pilot has a quick-donning type of oxygen mask that can be placed on the face with one hand from the ready position within 5 seconds, supplying oxygen and properly secured and sealed.
(2) Notwithstanding paragraph (b)(1)(ii) of this section, if for any reason at any time it is necessary for one pilot to leave the controls of the aircraft when operating at flight altitudes above flight level 350, the remaining pilot at the controls shall put on and use an oxygen mask until the other pilot has returned to that crewmember's station.

[3] 14 CFR Part 91 Subpart C — § 91.219 (part 2/3)
§ 91.219 Altitude alerting system or device: Turbojet-powered civil airplanes.
(5) Accept necessary barometric pressure settings if the system or device operates on barometric pressure. However, for operation below 3,000 feet AGL, the system or device need only provide one signal, either visual or aural, to comply with this paragraph. A radio altimeter may be included to provide the signal if the operator has an approved procedure for its use to determine DA/DH or MDA, as appropriate.
(c) Each operator to which this section applies must establish and assign procedures for the use of the altitude alerting system or device and each flight crewmember must comply with those procedures assigned to him.
(d) Paragraph (a) of this section does not apply to any operation of an airplane that has an experimental certificate or to the operation of any airplane for the following purposes:
(1) Ferrying a newly acquired airplane from the place where possession of it was taken to a place where the altitude alerting system or device is to be installed.
(2) Continuing a flight as originally planned, if the altitude alerting system or device becomes inoperative after the airplane has taken off; however, the flight may not depart from a place where repair or replacement can be made.

[4] 14 CFR Part 91 Subpart B — § 91.121
§ 91.121 Altimeter settings.
(a) Each person operating an aircraft shall maintain the cruising altitude or flight level of that aircraft, as the case may be, by reference to an altimeter that is set, when operating—
(1) Below 18,000 feet MSL, to—
(i) The current reported altimeter setting of a station along the route and within 100 nautical miles of the aircraft;
(ii) If there is no station within the area prescribed in paragraph (a)(1)(i) of this section, the current reported altimeter setting of an appropriate available station; or
(iii) In the case of an aircraft not equipped with a radio, the elevation of the departure airport or an appropriate altimeter setting available before departure; or
(2) At or above 18,000 feet MSL, to 29.92″ Hg.
(b) The lowest usable flight level is determined by the atmospheric pressure in the area of operation as shown in the following table:
(c) To convert minimum altitude prescribed under §§ 91.119 and 91.177 to the minimum flight level, the pilot shall take the flight level equivalent of the minimum altitude in feet and add the appropriate number of feet specified below, according to the current reported altimeter setting:

[5] 14 CFR Part 91 Subpart C — § 91.205 (part 6/7)
§ 91.205 Powered civil aircraft with standard U.S. airworthiness certificates: Instrument and equipment requirements.
(e) Flight
```

---
## q21 (single)

**Question:** Where and how low can I do aerobatic flight?

**Reference:** Not over congested areas or open-air assemblies, not within the surface areas of Class B, C, D or E airspace designated for an airport, not within 4 nautical miles of the center line of a Federal airway, not below 1,500 feet above the surface, and not when flight visibility is under 3 statute miles.

**Agent answer:**

Under federal aviation regulations, no person may operate an aircraft in aerobatic flight:

* **Minimum Altitude:** Below an altitude of **1,500 feet above the surface** [14 CFR Part 91 Subpart D, § 91.303(e)].
* **Location Restrictions:**
  * Over any congested area of a city, town, or settlement [14 CFR Part 91 Subpart D, § 91.303(a)];
  * Over an open air assembly of persons [14 CFR Part 91 Subpart D, § 91.303(b)];
  * Within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport [14 CFR Part 91 Subpart D, § 91.303(c)]; or
  * Within 4 nautical miles of the center line of any Federal airway [14 CFR Part 91 Subpart D, § 91.303(d)].
* **Visibility Requirement:** When flight visibility is less than 3 statute miles [14 CFR Part 91 Subpart D, § 91.303(f)].

*This answer provides standard regulatory requirements and is not formal legal advice. Check with the FAA or a qualified aviation professional for guidance regarding your specific flight operation or waiver requests.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart D — § 91.303
§ 91.303 Aerobatic flight.
No person may operate an aircraft in aerobatic flight—
(a) Over any congested area of a city, town, or settlement;
(b) Over an open air assembly of persons;
(c) Within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport;
(d) Within 4 nautical miles of the center line of any Federal airway;
(e) Below an altitude of 1,500 feet above the surface; or
(f) When flight visibility is less than 3 statute miles.

[2] 14 CFR Part 91 Subpart B — § 91.119 (part 1/2)
§ 91.119 Minimum safe altitudes: General.
Except when necessary for takeoff or landing, no person may operate an aircraft below the following altitudes:
(a) Anywhere. An altitude allowing, if a power unit fails, an emergency landing without undue hazard to persons or property on the surface.
(b) Over congested areas. Over any congested area of a city, town, or settlement, or over any open air assembly of persons, an altitude of 1,000 feet above the highest obstacle within a horizontal radius of 2,000 feet of the aircraft.
(c) Over other than congested areas. An altitude of 500 feet above the surface, except over open water or sparsely populated areas. In those cases, the aircraft may not be operated closer than 500 feet to any person, vessel, vehicle, or structure.
(d) Helicopters, powered parachutes, and weight-shift-control aircraft. If the operation is conducted without hazard to persons or property on the surface—
(1) A helicopter may be operated at less than the minimums prescribed in paragraph (b) or (c) of this section, provided each person operating the helicopter complies with any routes or altitudes specifically prescribed for helicopters by the FAA; and

[3] 14 CFR Part 91 Subpart B — § 91.145 (part 3/4)
§ 91.145 Management of aircraft operations in the vicinity of aerial demonstrations and major sporting events.
(1) Flight restricted airspace area for an aerial demonstration— The amount of airspace needed to protect persons and property on the surface or in the air, to maintain air safety and efficiency, or to prevent the unsafe congestion of aircraft will vary depending on the aerial demonstration and the factors listed in paragraph (b) of this section. The restricted airspace area will normally be limited to a 5 nautical mile radius from the center of the demonstration and an altitude 17000 mean sea level (for high performance aircraft) or 13000 feet above the surface (for certain parachute operations), but will be no greater than the minimum airspace necessary for the management of aircraft operations in the vicinity of the specified area.

[4] 14 CFR Part 101 — § 101.33
§ 101.33 Operating limitations.
No person may operate an unmanned free balloon—
(a) Unless otherwise authorized by ATC, below 2,000 feet above the surface within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport;
(b) At any altitude where there are clouds or obscuring phenomena of more than five-tenths coverage;
(c) At any altitude below 60,000 feet standard pressure altitude where the horizontal visibility is less than five miles;
(d) During the first 1,000 feet of ascent, over a congested area of a city, town, or settlement or an open-air assembly of persons not associated with the operation; or
(e) In such a manner that impact of the balloon, or part thereof including its payload, with the surface creates a hazard to persons or property not associated with the operation.

[5] 14 CFR Part 91 Subpart D — § 91.305
§ 91.305 Flight test areas.
No person may flight test an aircraft except over open water, or sparsely populated areas, having light air traffic.
```

---
## q22 (multi)

**Question:** I want to fly my registered small drone at night. What lighting do I need, and do I also need Remote ID?

**Reference:** Lighted anti-collision lighting visible for at least 3 statute miles; and yes, after September 16, 2023 the operation must meet the Remote ID requirements (standard or alternative) unless authorized otherwise.

**Agent answer:**

### Lighting Requirements (14 CFR Part 107)

To operate a small unmanned aircraft system (sUAS) at night under Part 107:

* **Anti-Collision Lighting:** The small unmanned aircraft must have lighted anti-collision lighting visible for at least 3 statute miles with a flash rate sufficient to avoid a collision [14 CFR Part 107, § 107.29(a)(2)].
* **Adjusting Intensity:** The remote pilot in command (PIC) may reduce the intensity of the anti-collision lighting if, due to operating conditions, doing so is in the interest of safety; however, the lighting may not be extinguished [14 CFR Part 107, § 107.29(a)(2)].
* **Pilot Training/Testing:** The remote PIC must have completed an initial knowledge test or training under § 107.65 after April 6, 2021 [14 CFR Part 107, § 107.29(a)(1)].

---

### Remote ID Requirement (14 CFR Part 89)

* **General Rule:** Yes. After September 16, 2023, no person may operate an unmanned aircraft within the airspace of the United States unless the operation meets FAA Remote Identification requirements [14 CFR Part 89, § 89.105].
* **Compliance Options:** You can comply by operating a standard remote identification unmanned aircraft that broadcasts from takeoff to shutdown [14 CFR Part 89, § 89.110], by equipping the drone with an FAA-accepted remote identification broadcast module [14 CFR Part 89, § 89.115(a)], or by operating within an FAA-recognized identification area (FRIA) [14 CFR Part 89, § 89.115(b)].

---

*Disclaimer: This response summarizes federal aviation regulations and is not legal advice. For specific cases or questions regarding your operations, consult the FAA or a qualified aviation professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.29 (part 1/2)
§ 107.29 Operation at night.
(a) Except as provided in paragraph (d) of this section, no person may operate a small unmanned aircraft system at night unless—
(1) The remote pilot in command of the small unmanned aircraft has completed an initial knowledge test or training, as applicable, under § 107.65 after April 6, 2021; and
(2) The small unmanned aircraft has lighted anti-collision lighting visible for at least 3 statute miles that has a flash rate sufficient to avoid a collision. The remote pilot in command may reduce the intensity of, but may not extinguish, the anti-collision lighting if he or she determines that, because of operating conditions, it would be in the interest of safety to do so.
(b) No person may operate a small unmanned aircraft system during periods of civil twilight unless the small unmanned aircraft has lighted anti-collision lighting visible for at least 3 statute miles that has a flash rate sufficient to avoid a collision. The remote pilot in command may reduce the intensity of, but may not extinguish, the anti-collision lighting if he or she determines that, because of operating conditions, it would be in the interest of safety to do so.

[2] 14 CFR Part 91 Subpart C — § 91.209
§ 91.209 Aircraft lights.
No person may:
(a) During the period from sunset to sunrise (or, in Alaska, during the period a prominent unlighted object cannot be seen from a distance of 3 statute miles or the sun is more than 6 degrees below the horizon)—
(1) Operate an aircraft unless it has lighted position lights;
(2) Park or move an aircraft in, or in dangerous proximity to, a night flight operations area of an airport unless the aircraft—
(i) Is clearly illuminated;
(ii) Has lighted position lights; or
(iii) is in an area that is marked by obstruction lights;
(3) Anchor an aircraft unless the aircraft—
(i) Has lighted anchor lights; or
(ii) Is in an area where anchor lights are not required on vessels; or
(b) Operate an aircraft that is equipped with an anticollision light system, unless it has lighted anticollision lights. However, the anticollision lights need not be lighted when the pilot-in-command determines that, because of operating conditions, it would be in the interest of safety to turn the lights off.

[3] 14 CFR Part 101 — § 101.17
§ 101.17 Lighting and marking requirements.
(a) No person may operate a moored balloon or kite, between sunset and sunrise unless the balloon or kite, and its mooring lines, are lighted so as to give a visual warning equal to that required for obstructions to air navigation in the FAA publication “Obstruction Marking and Lighting”.
(b) No person may operate a moored balloon or kite between sunrise and sunset unless its mooring lines have colored pennants or streamers attached at not more than 50 foot intervals beginning at 150 feet above the surface of the earth and visible for at least one mile.

[4] 14 CFR Part 107 — § 107.205
§ 107.205 List of regulations subject to waiver.
A certificate of waiver issued pursuant to § 107.200 may authorize a deviation from the following regulations of this part:
(a) Section 107.25—Operation from a moving vehicle or aircraft. However, no waiver of this provision will be issued to allow the carriage of property of another by aircraft for compensation or hire.
(b) Section 107.29(a)(2) and (b)—Anti-collision light required for operations at night and during periods of civil twilight.
(c) Section 107.31—Visual line of sight aircraft operation. However, no waiver of this provision will be issued to allow the carriage of property of another by aircraft for compensation or hire.
(d) Section 107.33—Visual observer.
(e) Section 107.35—Operation of multiple small unmanned aircraft systems.
(f) Section 107.37(a)—Yielding the right of way.
(g) Section 107.39—Operation over people.
(h) Section 107.41—Operation in certain airspace.
(i) Section 107.51—Operating limitations for small unmanned aircraft.
(j) Section 107.145—Operations over moving vehicles.

[5] 14 CFR Part 101 — § 101.35 (part 1/2)
§ 101.35 Equipment and marking requirements.
(a) No person may operate an unmanned free balloon unless—
(1) It is equipped with at least two payload cut-down systems or devices that operate independently of each other;
(2) At least two methods, systems, devices, or combinations thereof, that function independently of each other, are employed for terminating the flight of the balloon envelope; and
(3) The balloon envelope is equipped with a radar reflective device(s) or material that will present an echo to surface radar operating in the 200 MHz to 2700 MHz frequency range.
(b) No person may operate an unmanned free balloon below 60,000 feet standard pressure altitude between sunset and sunrise (as corrected to the altitude of operation) unless the balloon and its attachments and payload, whether or not they become separated during the operation, are equipped with lights that are visible for at least 5 miles and 
```

---
## q23 (multi)

**Question:** How long is a drone registration valid, and how often must a remote pilot refresh their knowledge?

**Reference:** Registration expires 3 years after issue unless renewed; the remote pilot must have passed the knowledge test or completed recurrent training within the previous 24 calendar months.

**Agent answer:**

**Drone Registration Validity**
A Certificate of Aircraft Registration for a small unmanned aircraft (whether operated for recreational or non-recreational purposes) expires **3 years** after the date of issue unless renewed [14 CFR Part 48, § 48.100(c)], [14 CFR Part 48, § 48.105(c)]. Renewal certificates are also valid for 3 years from the expiration date of the previous certificate [14 CFR Part 48, § 48.100(c)(2)], [14 CFR Part 48, § 48.105(c)(2)].

**Remote Pilot Knowledge Recency**
To exercise the privileges of a remote pilot in command, a person must refresh their aeronautical knowledge within the previous **24 calendar months** by completing one of the following [14 CFR Part 107, § 107.65]:
* Passing an initial aeronautical knowledge test [14 CFR Part 107, § 107.65(a)];
* Completing recurrent training [14 CFR Part 107, § 107.65(b)]; or
* Completing specified training if holding a Part 61 pilot certificate (other than student pilot) and meeting current flight review requirements [14 CFR Part 107, § 107.65(c)].

*Note: This response provides information based on federal regulations. For official guidance or questions regarding your specific situation, please consult the FAA or a qualified aviation professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.65
§ 107.65 Aeronautical knowledge recency.
A person may not exercise the privileges of a remote pilot in command with small UAS rating unless that person has accomplished one of the following in a manner acceptable to the Administrator within the previous 24 calendar months:
(a) Passed an initial aeronautical knowledge test covering the areas of knowledge specified in § 107.73;
(b) Completed recurrent training covering the areas of knowledge specified in § 107.73; or
(c) If a person holds a pilot certificate (other than a student pilot certificate) issued under part 61 of this chapter and meets the flight review requirements specified in § 61.56, completed training covering the areas of knowledge specified in § 107.74.
(d) A person who has passed a recurrent aeronautical knowledge test in a manner acceptable to the Administrator or who has satisfied the training requirement of paragraph (c) of this section prior to April 6, 2021 within the previous 24 calendar months is considered to be in compliance with the requirement of paragraph (b) or (c) of this section, as applicable.

[2] 14 CFR Part 48 — § 48.100 (part 1/3)
§ 48.100 Registration: Small unmanned aircraft operated for any purpose other than exclusively limited recreational operations.
(a) Certificate of Aircraft Registration. A Certificate of Aircraft Registration issued in accordance with § 48.110 to a small unmanned aircraft used for any purpose other than operating exclusively in compliance with 49 U.S.C. 44809 constitutes registration for the small unmanned aircraft identified on the application.
(b) Effective date of registration. An aircraft is registered when the applicant receives a Certificate of Aircraft Registration for the specific aircraft. The effective date of registration is shown by the date of issue on the Certificate of Aircraft Registration issued for the aircraft.
(c) Registration renewal. A Certificate of Aircraft registration issued under this part expires 3 years after the date of issue unless it is renewed.
(1) The holder of a Certificate of Aircraft Registration must renew the Certificate by verifying, in a form and manner prescribed by the Administrator, that the information provided in accordance with § 48.110 is accurate and if it is not, provide updated information. The verification may take place at any time within the six months preceding the month in which the Certificate of Aircraft registration expires.
(2) A certificate issued under this paragraph expires three years from the expiration date of the previous certificate.

[3] 14 CFR Part 48 — § 48.105 (part 1/2)
§ 48.105 Registration: Small unmanned aircraft intended exclusively for limited recreational operations.
(a) Certificate of Aircraft Registration. A Certificate of Aircraft Registration issued in accordance with § 48.110 for small unmanned aircraft to be operated exclusively in compliance with 49 U.S.C. 44809 constitutes registration for all the small unmanned aircraft used exclusively for operations in compliance with 49 U.S.C. 44809 owned by the individual identified on the application.
(b) Effective date of registration. An aircraft is registered when the applicant receives a Certificate of Aircraft Registration. The effective date of registration is shown by the date of issue on the Certificate of Aircraft Registration issued under this part.
(c) Registration renewal. A Certificate of Aircraft registration issued under this part expires 3 years after the date of issue unless it is renewed.
(1) The holder of a Certificate of Aircraft Registration must renew the Certificate by verifying, in a form and manner prescribed by the Administrator, that the information provided in accordance with § 48.110 is accurate and if it is not, provide updated information. The verification may take place at any time within the six months preceding the month in which the Certificate of Aircraft registration expires.

[4] 14 CFR Part 107 — § 107.73
§ 107.73 Knowledge and training.
An initial aeronautical knowledge test and recurrent training covers the following areas of knowledge:
(a) Applicable regulations relating to small unmanned aircraft system rating privileges, limitations, and flight operation;
(b) Airspace classification, operating requirements, and flight restrictions affecting small unmanned aircraft operation;
(c) Aviation weather sources and effects of weather on small unmanned aircraft performance;
(d) Small unmanned aircraft loading;
(e) Emergency procedures;
(f) Crew resource management;
(g) Radio communication procedures;
(h) Determining the performance of the small unmanned aircraft;
(i) Physiological effects of drugs and alcohol;
(j) Aeronautical decision-making and judgment;
(k) Airport operations;
(l) Maintenance and preflight inspection procedures; and
(m) Operation at night.

[5] 14 CFR Part 48 — § 48.105 (part 2/2)
§ 48.105 Registration: Small unmanned aircraft intended exclusively for limited recreational operations.
(2)
```

---
## q24 (multi)

**Question:** Is the minimum visibility the same for a drone and for a VFR airplane in Class E below 10,000 feet?

**Reference:** Yes, both need at least 3 statute miles. Cloud distance differs: a drone needs 500 feet below and 2,000 feet horizontal; the airplane also needs 1,000 feet above.

**Agent answer:**

**Yes, under standard basic VFR rules, both require a minimum visibility of 3 statute miles, but Special VFR rules allow a lower visibility for VFR airplanes under certain conditions.**

Here are the specific requirements from the regulations:

* **Small Unmanned Aircraft (Drone):** Under Part 107, the minimum flight visibility—observed from the control station—must be **no less than 3 statute miles** [14 CFR Part 107, § 107.51(c)].
* **VFR Airplane (Basic VFR):** For takeoffs, landings, or operations within the surface area of Class E airspace designated for an airport, the ground visibility (or flight visibility if ground visibility is not reported) must be **at least 3 statute miles** [14 CFR Part 91 Subpart B, § 91.155(d)].
* **VFR Airplane (Special VFR):** Unlike drones, an airplane operating under VFR below 10,000 feet MSL within controlled airspace designated to the surface for an airport may be granted a Special VFR clearance by ATC to operate clear of clouds with a flight visibility of **at least 1 statute mile** [14 CFR Part 91 Subpart B, § 91.157(a), (b)(1)–(3)].

*This answer provides information from federal aviation regulations and does not constitute formal legal advice or an operational verdict. Consult the FAA or a qualified aviation professional regarding specific flight operations.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.51
§ 107.51 Operating limitations for small unmanned aircraft.
A remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system must comply with all of the following operating limitations when operating a small unmanned aircraft system:
(a) The groundspeed of the small unmanned aircraft may not exceed 87 knots (100 miles per hour).
(b) The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, unless the small unmanned aircraft:
(1) Is flown within a 400-foot radius of a structure; and
(2) Does not fly higher than 400 feet above the structure's immediate uppermost limit.
(c) The minimum flight visibility, as observed from the location of the control station must be no less than 3 statute miles. For purposes of this section, flight visibility means the average slant distance from the control station at which prominent unlighted objects may be seen and identified by day and prominent lighted objects may be seen and identified by night.
(d) The minimum distance of the small unmanned aircraft from clouds must be no less than:
(1) 500 feet below the cloud; and
(2) 2,000 feet horizontally from the cloud.

[2] 14 CFR Part 91 Subpart B — § 91.155 (part 1/2)
§ 91.155 Basic VFR weather minimums.
(a) Except as provided in paragraph (b) of this section and § 91.157, no person may operate an aircraft under VFR when the flight visibility is less, or at a distance from clouds that is less, than that prescribed for the corresponding altitude and class of airspace in the following table:
(b) Class G Airspace. Notwithstanding the provisions of paragraph (a) of this section, the following operations may be conducted in Class G airspace below 1,200 feet above the surface:
(1) Helicopter. A helicopter may be operated clear of clouds in an airport traffic pattern within 1/2 mile of the runway or helipad of intended landing if the flight visibility is not less than 1/2 statute mile.
(2) Airplane, powered parachute, or weight-shift-control aircraft. If the visibility is less than 3 statute miles but not less than 1 statute mile during night hours and you are operating in an airport traffic pattern within 1/2 mile of the runway, you may operate an airplane, powered parachute, or weight-shift-control aircraft clear of clouds.

[3] 14 CFR Part 107 — § 107.31
§ 107.31 Visual line of sight aircraft operation.
(a) With vision that is unaided by any device other than corrective lenses, the remote pilot in command, the visual observer (if one is used), and the person manipulating the flight control of the small unmanned aircraft system must be able to see the unmanned aircraft throughout the entire flight in order to:
(1) Know the unmanned aircraft's location;
(2) Determine the unmanned aircraft's attitude, altitude, and direction of flight;
(3) Observe the airspace for other air traffic or hazards; and
(4) Determine that the unmanned aircraft does not endanger the life or property of another.
(b) Throughout the entire flight of the small unmanned aircraft, the ability described in paragraph (a) of this section must be exercised by either:
(1) The remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system; or
(2) A visual observer.

[4] 14 CFR Part 91 Subpart B — § 91.155 (part 2/2)
§ 91.155 Basic VFR weather minimums.
(c) Except as provided in § 91.157, no person may operate an aircraft beneath the ceiling under VFR within the lateral boundaries of controlled airspace designated to the surface for an airport when the ceiling is less than 1,000 feet.
(d) Except as provided in § 91.157 of this part, no person may take off or land an aircraft, or enter the traffic pattern of an airport, under VFR, within the lateral boundaries of the surface areas of Class B, Class C, Class D, or Class E airspace designated for an airport—
(1) Unless ground visibility at that airport is at least 3 statute miles; or
(2) If ground visibility is not reported at that airport, unless flight visibility during landing or takeoff, or while operating in the traffic pattern is at least 3 statute miles.
(e) For the purpose of this section, an aircraft operating at the base altitude of a Class E airspace area is considered to be within the airspace directly below that area.

[5] 14 CFR Part 91 Subpart B — § 91.157 (part 1/2)
§ 91.157 Special VFR weather minimums.
(a) Except as provided in appendix D, section 3, of this part, special VFR operations may be conducted under the weather minimums and requirements of this section, instead of those contained in § 91.155, below 10,000 feet MSL within the airspace contained by the upward extension of the lateral boundaries of the controlled airspace designated to the surface for an airport.
(b) Special VFR operations may only be conducted—
(1) With an ATC clearance;
(2) Clear of clouds;
(3) Except for helicopters, when flight visibility is at least 1 statute mile; and
(
```

---
## q25 (multi)

**Question:** Is dropping objects restricted for both drones and manned aircraft?

**Reference:** Yes. A drone may not drop an object in a way that creates an undue hazard to persons or property; the pilot in command of a civil aircraft may not allow an object to be dropped that creates a hazard, though reasonable precautions to avoid injury or damage are allowed.

**Agent answer:**

Yes, dropping objects is restricted for both manned civil aircraft and drones:

* **Manned Civil Aircraft:** No pilot in command of a civil aircraft may allow any object to be dropped from that aircraft in flight that creates a hazard to persons or property. Dropping an object is permitted if reasonable precautions are taken to avoid injury or damage to persons or property [14 CFR Part 91 Subpart A, § 91.15].
* **Small Unmanned Aircraft (Drones):** No person may allow an object to be dropped from a small unmanned aircraft in a manner that creates an undue hazard to persons or property [14 CFR Part 107, § 107.23].
* **Balloons, Kites, and Rockets:** No person operating a moored balloon, kite, amateur rocket, or unmanned free balloon may allow an object to be dropped if doing so creates a hazard to other persons or their property [14 CFR Part 101, § 101.7].

*Note: This response provides regulatory text for informational purposes and does not constitute legal advice. Check with the FAA or a qualified aviation professional regarding specific operational scenarios.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart A — § 91.15
§ 91.15 Dropping objects.
No pilot in command of a civil aircraft may allow any object to be dropped from that aircraft in flight that creates a hazard to persons or property. However, this section does not prohibit the dropping of any object if reasonable precautions are taken to avoid injury or damage to persons or property.

[2] 14 CFR Part 107 — § 107.23
§ 107.23 Hazardous operation.
No person may:
(a) Operate a small unmanned aircraft system in a careless or reckless manner so as to endanger the life or property of another; or
(b) Allow an object to be dropped from a small unmanned aircraft in a manner that creates an undue hazard to persons or property.

[3] 14 CFR Part 101 — § 101.7
§ 101.7 Hazardous operations.
(a) No person may operate any moored balloon, kite, amateur rocket, or unmanned free balloon in a manner that creates a hazard to other persons, or their property.
(b) No person operating any moored balloon, kite, amateur rocket, or unmanned free balloon may allow an object to be dropped therefrom, if such action creates a hazard to other persons or their property.

[4] 14 CFR Part 91 Subpart B — § 91.108 (part 2/8)
§ 91.108 Use of supplemental restraint systems.
(2) Prior to releasing an FAA-approved safety belt and, if installed, shoulder harness during an operation with the doors opened or removed, an individual must be properly secured by a supplemental restraint system that is connected to an FAA-approved airframe attachment point. An individual cannot release their safety belt and, if installed, shoulder harness until the pilot in command authorizes them to do so.
(c) Supplemental restraint system design requirements. Each supplemental restraint system must:
(1) Have a harness that secures around the torso of the individual using the supplemental restraint system;
(2) Have a lanyard that connects the harness to an FAA-approved airframe attachment point or points inside the aircraft and that ensures the torso of the individual using the supplemental restraint system remains inside the aircraft at all times;
(3) Not impede egress from the aircraft in an emergency after being released; and
(4) Have a release mechanism that—
(i) Can be quickly operated by the individual using the supplemental restraint system with minimal difficulty;
(ii) Is attached to the front or side of the harness in a location easily accessible to and visible by the individual using the supplemental restraint system;
(iii) Prevents inadvertent release; and

[5] 14 CFR Part 107 — § 107.79
§ 107.79 Voluntary surrender of certificate.
(a) The holder of a certificate issued under this subpart may voluntarily surrender it for cancellation.
(b) Any request made under paragraph (a) of this section must include the following signed statement or its equivalent: “I voluntarily surrender my remote pilot certificate with a small UAS rating for cancellation. This request is made for my own reasons, with full knowledge that my certificate will not be reissued to me unless I again complete the requirements specified in §§ 107.61 and 107.63.”
```

---
## q26 (multi)

**Question:** Who has the final authority over a drone flight and over a manned aircraft flight?

**Reference:** For the drone, the remote pilot in command; for the manned aircraft, the pilot in command.

**Agent answer:**

- **Manned aircraft flight:** The **pilot in command** is directly responsible for, and is the final authority as to, the operation of the aircraft [14 CFR Part 91 Subpart A, § 91.3(a)].
- **Drone flight (small UAS):** The **remote pilot in command** is directly responsible for, and is the final authority as to, the operation of the small unmanned aircraft system [14 CFR Part 107, § 107.19(b)].

*Note: This information is for educational purposes. Please check with the FAA or a qualified aviation professional regarding specific operational scenarios.*

**Retrieved passages:**

```
[1] 14 CFR Part 91 Subpart A — § 91.3
§ 91.3 Responsibility and authority of the pilot in command.
(a) The pilot in command of an aircraft is directly responsible for, and is the final authority as to, the operation of that aircraft.
(b) In an in-flight emergency requiring immediate action, the pilot in command may deviate from any rule of this part to the extent required to meet that emergency.
(c) Each pilot in command who deviates from a rule under paragraph (b) of this section shall, upon the request of the Administrator, send a written report of that deviation to the Administrator.

[2] 14 CFR Part 107 — § 107.19
§ 107.19 Remote pilot in command.
(a) A remote pilot in command must be designated before or during the flight of the small unmanned aircraft.
(b) The remote pilot in command is directly responsible for and is the final authority as to the operation of the small unmanned aircraft system.
(c) The remote pilot in command must ensure that the small unmanned aircraft will pose no undue hazard to other people, other aircraft, or other property in the event of a loss of control of the small unmanned aircraft for any reason.
(d) The remote pilot in command must ensure that the small UAS operation complies with all applicable regulations of this chapter.
(e) The remote pilot in command must have the ability to direct the small unmanned aircraft to ensure compliance with the applicable provisions of this chapter.

[3] 14 CFR Part 91 Subpart A — § 91.5
§ 91.5 Pilot in command of aircraft requiring more than one required pilot.
No person may operate an aircraft that is type certificated for more than one required pilot flight crewmember unless the pilot in command meets the requirements of § 61.58 of this chapter.

[4] 14 CFR Part 107 — § 107.12
§ 107.12 Requirement for a remote pilot certificate with a small UAS rating.
(a) Except as provided in paragraph (c) of this section, no person may manipulate the flight controls of a small unmanned aircraft system unless:
(1) That person has a remote pilot certificate with a small UAS rating issued pursuant to subpart C of this part and satisfies the requirements of § 107.65; or
(2) That person is under the direct supervision of a remote pilot in command and the remote pilot in command has the ability to immediately take direct control of the flight of the small unmanned aircraft.
(b) Except as provided in paragraph (c) of this section, no person may act as a remote pilot in command unless that person has a remote pilot certificate with a small UAS rating issued pursuant to Subpart C of this part and satisfies the requirements of § 107.65.
(c) The Administrator may, consistent with international standards, authorize an airman to operate a civil foreign-registered small unmanned aircraft without an FAA-issued remote pilot certificate with a small UAS rating.

[5] 14 CFR Part 107 — § 107.35
§ 107.35 Operation of multiple small unmanned aircraft.
A person may not manipulate flight controls or act as a remote pilot in command or visual observer in the operation of more than one unmanned aircraft at the same time.
```

---
## q27 (multi)

**Question:** Can a visual observer replace the pilot's own line of sight, and what must the observer keep up with the pilot?

**Reference:** Yes, a visual observer can exercise the see-the-aircraft ability instead of the pilot and the person at the controls; the pilot, the person at the controls and the observer must maintain effective communication at all times.

**Agent answer:**

**Yes**, a visual observer can satisfy the visual line of sight requirement on behalf of the pilot. The visual line of sight capability required during flight may be exercised by either the remote pilot in command and the person manipulating the flight controls, or by a visual observer [14 CFR Part 107, § 107.31(b)].

When a visual observer is used, they must maintain the following with the pilot and the person manipulating the flight controls:

* **Effective communication:** The remote pilot in command, the person manipulating the flight controls, and the visual observer must maintain effective communication with each other at all times [14 CFR Part 107, § 107.33(a)].
* **Coordination:** They must coordinate to:
  1. Scan the airspace for potential collision hazards [14 CFR Part 107, § 107.33(c)(1)].
  2. Maintain awareness of the position of the small unmanned aircraft through direct visual observation [14 CFR Part 107, § 107.33(c)(2)].

*Note: This information is for general regulatory guidance and does not constitute legal advice. For specific flight operations or official interpretations, consult the FAA or a qualified aviation legal professional.*

**Retrieved passages:**

```
[1] 14 CFR Part 107 — § 107.33
§ 107.33 Visual observer.
If a visual observer is used during the aircraft operation, all of the following requirements must be met:
(a) The remote pilot in command, the person manipulating the flight controls of the small unmanned aircraft system, and the visual observer must maintain effective communication with each other at all times.
(b) The remote pilot in command must ensure that the visual observer is able to see the unmanned aircraft in the manner specified in § 107.31.
(c) The remote pilot in command, the person manipulating the flight controls of the small unmanned aircraft system, and the visual observer must coordinate to do the following:
(1) Scan the airspace where the small unmanned aircraft is operating for any potential collision hazard; and
(2) Maintain awareness of the position of the small unmanned aircraft through direct visual observation.

[2] 14 CFR Part 107 — § 107.31
§ 107.31 Visual line of sight aircraft operation.
(a) With vision that is unaided by any device other than corrective lenses, the remote pilot in command, the visual observer (if one is used), and the person manipulating the flight control of the small unmanned aircraft system must be able to see the unmanned aircraft throughout the entire flight in order to:
(1) Know the unmanned aircraft's location;
(2) Determine the unmanned aircraft's attitude, altitude, and direction of flight;
(3) Observe the airspace for other air traffic or hazards; and
(4) Determine that the unmanned aircraft does not endanger the life or property of another.
(b) Throughout the entire flight of the small unmanned aircraft, the ability described in paragraph (a) of this section must be exercised by either:
(1) The remote pilot in command and the person manipulating the flight controls of the small unmanned aircraft system; or
(2) A visual observer.

[3] 14 CFR Part 107 — § 107.3 (part 2/2)
§ 107.3 Definitions.
Visual observer means a person who is designated by the remote pilot in command to assist the remote pilot in command and the person manipulating the flight controls of the small UAS to see and avoid other air traffic or objects aloft or on the ground.

[4] 14 CFR Part 89 — § 89.115 (part 2/3)
§ 89.115 Alternative remote identification.
(2) Remote identification operating requirements. Unless otherwise authorized by the Administrator, a person may operate an unmanned aircraft under this paragraph (a) only if all of the following conditions are met:
(i) From takeoff to shutdown, the person operating the unmanned aircraft must ensure that the remote identification broadcast module broadcasts the remote identification message elements of § 89.315 directly from the unmanned aircraft.
(ii) The person manipulating the flight controls of the unmanned aircraft system must be able to see the unmanned aircraft at all times throughout the operation.
(3) Pre-flight requirement. Prior to takeoff, the person manipulating the flight controls of the unmanned aircraft system must ensure the remote identification broadcast module is functioning in accordance with this subpart.
(4) In-flight loss of remote identification broadcast. The person manipulating the flight controls of the unmanned aircraft system must land the unmanned aircraft as soon as practicable if the unmanned aircraft is no longer broadcasting the message elements of § 89.315.
(b) Operations at FAA-recognized identification areas. Unless otherwise authorized by the Administrator, a person may operate an unmanned aircraft without remote identification equipment only if all of the following conditions are met:

[5] 14 CFR Part 89 — § 89.115 (part 3/3)
§ 89.115 Alternative remote identification.
(1) The unmanned aircraft and the person manipulating the flight controls of the unmanned aircraft system remain within the boundaries of an FAA-recognized identification area throughout the operation; and
(2) The person manipulating the flight controls of the unmanned aircraft system must be able to see the unmanned aircraft at all times throughout the operation.
```
