# Quick grading sheet (20 answers)
For each: **correct** = matches the reference (u-questions: refuses without inventing). **supported** = every claim is in the retrieved passages (open the block to check). 1 = yes, 0 = no.
Write each line into `eval/human_labels.csv` as `id,correct,supported,notes`.

---
### q02 (single): How many SR-84 headshots does it take to eliminate a Heavy contestant?

| Reference | Agent's answer |
|---|---|
| 2 headshots (time to kill about 1.333 s); a Heavy has 325 HP and a headshot deals 244. | It takes 2 headshots (or alternatively, 1 headshot and 1 body shot) to eliminate a Heavy contestant with the SR-84 [SR-84 § Stats > Damage Profile] [SR-84 § Guide > Strengths]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [SR-84 § Stats]
covers: Stats / Stats > Damage Profile / Stats > Properties > Weapon (cite any of these sections of SR-84)
url: https://www.thefinals.wiki/wiki/SR-84
- Bullets are hitscan up until 40m, and then converted into projectiles afterwards.

[Stats > Damage Profile]
Head: Light (175 HP) Bullets to kill 1; Light (175 HP) Time to kill (s) 0.000; Medium (250 HP) Bullets to kill 2; Medium (250 HP) Time to kill (s) 1.333; Heavy (325 HP) Bullets to kill 2; Heavy (325 HP) Time to kill (s) 1.333
Body: Light (175 HP) Bullets to kill 2; Light (175 HP) Time to kill (s) 1.333; Medium (250 HP) Bullets to kill 3; Medium (250 HP) Time to kill (s) 2.667; Heavy (325 HP) Bullets to kill 3; Heavy (325 HP) Time to kill (s) 2.667
Values are approximate and determined by community testing ( 12.0.0 ).

[Stats > Properties > Weapon]
Ranged — Strikes targets by aiming and firing at them from a distance.
Single Fire — Fires once when the trigger is pulled. The trigger must be released before firing again.
Scope — Has the ability to scope in. This grants near-perfect accuracy, but produces a glint that reveals the user's location.
Full Reload — Replaces the entire magazine in one animation on reload.
Unstable Accuracy — Suffers a significant decrease in accuracy while moving and while airborne.

---

Result 2  cite as: [SR-84 § Guide > Strengths]
url: https://www.thefinals.wiki/wiki/SR-84
- The SR-84 is able to reliably hit targets from extremely long distances thanks to the lack of bullet dispersion when scoped in. For shots within 40m (after which the bullet becomes a projectile) bullet drop does not need to be accounted for, as with other hitscan weapons.
- The SR-84 has a very strong headshot multiplier, dealing double the damage of a body shot. A Light contestant can be eliminated with a single headshot. A Medium contestant can be eliminated with a headshot and a body shot. A Heavy contestant can be eliminated with a headshot and a body shot.
- Other Useful Combos A Light contestant can be eliminated with a body shot and a melee. A Medium contestant can be eliminated with two body shots and a melee. A Medium contestant can be eliminated with a headshot and a melee. A Heavy contestant can be eliminated with three body shots. A Heavy contestant can be eliminated with a headshot and three melee's. A Heavy contestant can be eliminated with two body shots and three melee.

---

Result 3  cite as: [SR-84 § Stats > Properties > Bullet]
url: https://www.thefinals.wiki/wiki/SR-84
Hitscan — Up to 40m — Travels in a straight line, meaning there is no bullet drop. The direction will deviate from the crosshairs depending on accuracy.
Projectile — After 40m — Gets affected by gravity and has a travel time.
Critical Hit — Critically hits on headshots, applying a damage multiplier.
High Range Falloff — Deals reduced damage when hitting targets at long distances (falloff starts beyond 30m). For the SR-84, this distance is extremely far, with the falloff starting beyond 80 meters.
Sound Cue — Can be heard firing from across the arena. Bullets that fly near a target produce a distinct whiSR-84ing noise.
Minor Structure Damage — Damages structures. Takes a very long time to break a concrete wall.

---

Result 4  cite as: [SR-84 § Overview]
covers: Overview / Usage (cite any of these sections of SR-84)
url: https://www.thefinals.wiki/wiki/SR-84
SR-84
Weapon Quote: “Bolt-action sniper rifle”
Profile
Build: L Light
Icon
Type: Marksman Rifle
Unlock: Free
Damage
Body: 122
Head: 244 (2×)
Environmental: 27
Damage Falloff
Min Range: 80m
Max Range: 100m
Multiplier: 0.75
Technical
RPM: 45
Magazine: 6
Empty Reload: 3.35
Tactical Reload: 1.95
The SR-84 is a Light class bolt-action Sniper Rifle designed to deal very high damage per shot and extreme headshot damage from a long distance.

[Usage]
The SR-84 can be selected as the Weapon of any Light build loadout.
It has a special type of sights, offering a scope. Enabling the scope will zoom in the screen and overlay it with a duplex reticle, and will slow down movement and sensitivity.
The trigger can be pulled to fire one bullet that damages an opponent, also dealing additional damage on headshots. The trigger must be released before firing again. Moving decreases accuracy, especially when going airborne. Firing while scoped in grants the SR-84 near-perfect accuracy, even while moving.
The weapon automatically reloads when its magazine is empty, or the user can do a tactical reload before this point. The user has unlimited spare ammunition.
The SR-84 fires hitscan bullets up to 40m. After 40m, the bullet becomes a projectile with travel time and bullet drop.
Equip SR-84: PC 1; PS △; XBox Y; Key Weapon
Fire shot (Tap): PS R2; XBox RT; Key Primary fire
Scope in (Hold): PS L2; XBox LT; Key Secondary fire
Tactical reload: PC R; PS ◻; XBox X; Key Reload

---

Result 5  cite as: [SR-84 § Guide > Weaknesses]
url: https://www.thefinals.wiki/wiki/SR-84
- The SR-84 is weak at close distances, 
```
</details>

`q02,?,?,`

---
### q04 (single): How much health does a Heavy teammate come back with after being revived by the Defibrillator?

| Reference | Agent's answer |
|---|---|
| 175 HP, half of the Heavy build's maximum; they also get brief invulnerability and 5 s of revive sickness. | A Heavy teammate comes back with 175 health (half of their build's maximum HP) after being revived by the Defibrillator [Defibrillator § Stats > Effects]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Defibrillator § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget / Stats > Properties > Zap (cite any of these sections of Defibrillator)
url: https://www.thefinals.wiki/wiki/Defibrillator
The Defibrillator, once deployed, must be prepared for a brief moment before activation. The contestant using the gadget is required to be both facing and within a short distance of either a teammate's Revive Statue or an opposing contestant.
When a Defibrillator is used on a Revive Statue , it starts an uninterruptible revival process that requires no further action from the user. A hologram appears at the statue's location and gradually re-materializes during the revival. Once the process is complete:
- The revived contestant returns with half of their Build's maximum HP. Light 75, Medium 125, Heavy 175.
- They gain brief invulnerability.
- They suffer temporary revive sickness, which prevents them from using their Specializations or Gadgets for 5 seconds after being revived.
Alternatively, the Defibrillator can be activated on an opposing contestant to instantly deal 50 damage to them.

[Stats > Properties > Gadget]
Targeted — Can be activated while targeting a Revive Statue to revive it (or alternatively, an opponent to damage them).
Single Charge — Can be used once, then recharges automatically over the cooldown time.

[Stats > Properties > Zap]
Damaging — Can be used on an opponent to deal some damage to them.
Not Interceptible — Can not be removed by the APS Turret .

---

Result 2  cite as: [Defibrillator § Overview]
covers: Overview / Usage (cite any of these sections of Defibrillator)
url: https://www.thefinals.wiki/wiki/Defibrillator
DEFIBRILLATOR
“When charged, can be used on fallen teammates' statues to revive them instantly”
Profile
Build: M Medium
Icon
Type: Utility
Unlock: Medic
Stats
Cooldown: 45s
Ammo: 1
Technical
Damage: 50
Duration: Revive Sickness - 5s
Healing: 50% HP on Revive
The Defibrillator is a Medium class gadget that can revive a downed teammate automatically instead of needing to do so manually.

[Usage]
The Defibrillator can be selected as one of three gadgets of any Medium build loadout, except when competing in the Terminal Attack and Team Deathmatch gamemodes.
Once equipped, holding the primary fire button will prepare an activation of the Defibrillator. Releasing the button will activate the gadget as long as a valid target is within range and the minimum charge duration of 1 second is met.
Equip Defibrillator: PC 2 3 4; PS L1; XBox LB; Key Gadget
Prepare defibrillation (Hold) Activate (Release): PS R2; XBox RT; Key Primary fire

---

Result 3  cite as: [Defibrillator § Guide > Tactics]
url: https://www.thefinals.wiki/wiki/Defibrillator
- It is the responsibility of the Defibrillator user to ensure that their teammate won't immediately die upon revival. Moving the teammate's Revive Statue away from enemies or providing cover with abilities such as Goo , the APS Turret , or the Guardian Turret can all but guarantee the odds of successful revives.
- The Defibrillator is best used for mid-fight Revives, such as if a teammate dies early into a fight.
- The Healing Beam makes an excellent pairing with the Defibrillator, as it can heal the revived contestant and make them battle-ready quicker.

---

Result 4  cite as: [Defibrillator § Stats > Properties > Effect]
covers: Stats > Properties > Effect / Guide > Strengths / Guide > Weaknesses (cite any of these sections of Defibrillator)
url: https://www.thefinals.wiki/wiki/Defibrillator
Support — Applies a positive effect to teammates.
Not Glitchable — Cannot be disabled by a Glitch Grenade or Glitch Barrel , meaning the revive in progress will not be interrupted.
Not Reshapeable — Cannot be reshaped by the Data Reshaper .

[Guide > Strengths]
- The Defibrillator can revive teammates faster and without needing to do so manually past the initial activation. This allows contestants to fight, defend or assist with objectives while the revive is in progress, instead of remaining still for multiple seconds to perform a full revive.

[Guide > Weaknesses]
- Contestants revived by the Defibrillator are left at a disadvantage, with 50% their maximum HP and being unable to use Specializations or Gadgets for 5 seconds.
- Opposing contestants can easily camp and kill a teammate being revived by the Defibrillator due to the obvious hologram, timing, and sound cues. The defibrillator revive also becomes a waste if both the user and their revived teammate die during and/or immediately after the revival. To prevent this, contestants who are reviving a teammate should try to remain in close proximity to them. This will allow the contestant performing the revive to try and protect them from enemy contestants. Alternatively, the Revive Statue can be moved to a safer location before using the Defibrillator.
- Using the Defibrillator as a weapon is highly impractical. Not only is it slower and deals slightly less damage than 
```
</details>

`q04,?,?,`

---
### q07 (single): Does using Evasive Dash interrupt drawing the Recurve Bow?

| Reference | Agent's answer |
|---|---|
| No. Evasive Dash does not interrupt drawing the Recurve Bow, a Sword lunge or scoping in with the SR-84. | No, using Evasive Dash does not interrupt drawing the Recurve Bow [Evasive Dash § Stats > Effects]. It is possible to use Evasive Dash while the bow is drawn [Recurve Bow § Guide > Tactics]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Recurve Bow § Guide > Tactics]
url: https://www.thefinals.wiki/wiki/Recurve_Bow
- The Recurve Bow can be paired with the Evasive Dash or Grappling Hook , as it is possible to use either while the bow is drawn (despite the grappling hook visually lowering the bow, it's still fully charged and ready to fire if you release the fire button while the grappling animation is playing).
- Headshots are key to quick takedowns! If you see an opponent before they see you, especially if they're stationary, take the extra time to line up a headshot before they're alerted to your presence.

---

Result 2  cite as: [Recurve Bow § Usage]
covers: Usage / Stats (cite any of these sections of Recurve Bow)
url: https://www.thefinals.wiki/wiki/Recurve_Bow
The Recurve Bow can be selected as the Weapon of any Light build loadout.
The trigger can be held down to prepare an arrow and draw back the string, which charges up its power over time. The maximum power is reached after charging for 0.49 seconds, at which point the string can be held down for any duration. The user cannot sprint while drawing an arrow.
Once the Recurve Bow has been charged up for at least a short moment, the trigger can be released to fire one arrow that damages an opponent, dealing damage based on its charge time and also dealing additional damage on headshots.
The secondary trigger can be used to zoom in slightly, though this does not affect the Recurve Bow's accuracy. Its accuracy also remains stable while moving and going airborne.
The weapon has infinite ammunition and does not need to reload.
Equip Recurve Bow: PC 1; PS △; XBox Y; Key Weapon
Draw bow (Hold) Fire shot (Release): PS R2; XBox RT; Key Primary fire
Zoom (Hold): PS L2; XBox LT; Key Secondary fire

[Stats]
- Damage increases from 60 to 126 (continuously) based on how long the weapon was drawn.

---

Result 3  cite as: [Recurve Bow § Overview]
url: https://www.thefinals.wiki/wiki/Recurve_Bow
RECURVE BOW
Weapon Quote: “Shoots arrows in a curved arc; the arrows' effective range and damage will increase the further back the bowstring is drawn”
Profile
Build: L Light
Icon
Type: Marksman Rifle
Unlock: 500
Damage
Body: 60
Head: 90 (1.5×)
Alt-Fire Body: Max Draw - 126
Alt-Fire Head: Max Draw - 189 (1.5×)
Environmental: 12.125
Environmental Alt-Fire: Max Draw - 25
Technical
RPM: 78丨48
Magazine: ∞
Empty Reload: 0.75s
The Recurve Bow is a Light class Marksman Weapon with the unique ability to charge its shots, designed to either deal high damage per shot over a long distance, or to fire more quickly at a lower velocity.

---

Result 4  cite as: [Recurve Bow § Stats > Properties > Weapon]
covers: Stats > Properties > Weapon / Stats > Properties > Bullet (cite any of these sections of Recurve Bow)
url: https://www.thefinals.wiki/wiki/Recurve_Bow
Ranged — Strikes targets by aiming and firing at them from a distance.
Single Fire — Fires once when the trigger is pulled. The trigger must be released before firing again.
Stable Accuracy — Keeps a stable accuracy, even while moving and going airborne.
Infinite Ammo — Does not need to reload.
No Aiming Down Sights — Cannot use sights. Zooms in slightly instead, but doing so does not significantly affect accuracy.

[Stats > Properties > Bullet]
Projectile — Gets affected by gravity and has a travel time.
Critical Hit — Critically hits on headshots, applying a damage multiplier.
Minor Structure Damage — Damages structures. Takes a very long time to break a concrete wall.
Not Interceptible — Can not be removed by the APS Turret .
No Falloff — Does not deal reduced damage when hitting targets at long distances.

---

Result 5  cite as: [Evasive Dash § Overview]
covers: Overview / Usage / Stats > Effects (cite any of these sections of Evasive Dash)
url: https://www.thefinals.wiki/wiki/Evasive_Dash
EVASIVE DASH
“A few quick dashes to close distance or dodge out of harm's way”
Profile
Build: L Light
Icon
Type: Specialization
Unlock: Duelist
Stats
Cooldown: 5s
Ammo: 2
Evasive Dash is a Light class specialization that allows its user to perform a dash frequently, which rapidly moves them a small distance in any direction.

[Usage]
Evasive Dash can be selected as the Specialization gadget of any Light build loadout.
The specialization trigger can be used to perform a dash. The direction of the dash depends on the direction in which its user is attempting to move. For example, if the movement trigger is set to move to the left while activating Evasive Dash, it will perform a dash to the left.
The vertical direction of the dash depends on the looking direction of the user. If the user is looking upwards, the dash will move up. However, Evasive Dash is primarily a horizontal movement tool and cannot go straight up or down.
Dash (Tap): PC Q; PS R1; XBox RB; Key Specialization

[Stats > Effects]
Evasive Dash can be activated to dash a short distance, going in a direction based on the user's movement inputs and their looking direction. Uniquely, using this sp
```
</details>

`q07,?,?,`

---
### q10 (single): How much damage does the first hit of Charge 'N' Slam deal?

| Reference | Agent's answer |
|---|---|
| 100 damage on the initial hit, 40 on subsequent hits; the ground slam deals 50-200 in a 4 m radius. | The first hit of Charge 'N' Slam deals 100 damage (with subsequent hits dealing 40 damage) [Charge 'N' Slam § Overview]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Charge 'N' Slam § Overview]
covers: Overview / Usage (cite any of these sections of Charge 'N' Slam)
url: https://www.thefinals.wiki/wiki/Charge_'N'_Slam
CHARGE 'N' SLAM
“A charge to propel you forward to break through walls and obstacles, or to slam the ground if activated in the air. Deals damage to opponents.”
Profile
Build: H Heavy
Icon
Type: Specialization
Unlock: Demolisher
Stats
Cooldown: 12s
Technical
Damage: 100 Initial 40 Subsequent 50-200 Ground Slam
Damage Radius: 4m (Ground Slam)
Duration: 3s
Charge 'N' Slam is a Heavy class specialization that causes its user to rampage forwards, dealing high damage and pushing opponents, and destroying structures. It also has a ground pound functionality.

[Usage]
Charge 'N' Slam can be selected as the specialization gadget of any Heavy build loadout.
The primary trigger can be used to activate Charge 'N' Slam. If the user is grounded, they will start charging forwards. The movement direction can be controlled by changing the looking direction, but not the speed.
If the user is airborne upon activation, a slam will be executed. It is also possible to perform one or multiple slams during a charge by jumping.
Charge (Tap): PC Q; PS R1; XBox RB; Key Specialization
Ground pound: PC Space; PS ✖; XBox A; Key Jump

---

Result 2  cite as: [Charge 'N' Slam § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget / Stats > Properties > Charge (cite any of these sections of Charge 'N' Slam)
url: https://www.thefinals.wiki/wiki/Charge_'N'_Slam
The Charge 'N' Slam can be activated to start charging in a direction. The user will lose control of their ability to move but can still control which direction they are moving in. During this time, the user can run through walls without being slowed down, also causing the walls to be destroyed instantly. Any opponents the user collides with in this state will take damage (with increased damage on the first hit) and get knocked back.
If the specialization is activated while airborne, or if the user jumps while charging, a slam will be triggered, which can break through a floor and deals damage and knocks away opponents on impact. The damage is based on how high up in the air the user slammed.

[Stats > Properties > Gadget]
Self Targeted — Can be activated to apply an effect to the contestant that used it.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
Disarms User — Forces the user to stop using their other items for the duration of the charge.

[Stats > Properties > Charge]
Sound Cue — The user can be heard screaming (if dialogue sound is not disabled), alerting nearby contestants of the ability.
Movement — Provides a special mode of transport for contestants.
Damaging — Deals damage to contestants.
Major Structure Damage — Damages structures. Instantly destroys a concrete wall.

---

Result 3  cite as: [Charge 'N' Slam § Guide > Strengths]
covers: Guide > Strengths / Guide > Weaknesses / Guide > Tactics (cite any of these sections of Charge 'N' Slam)
url: https://www.thefinals.wiki/wiki/Charge_'N'_Slam
- Charge 'N' Slam can deal a lot of damage to a nearby target without them being able to retaliate as they are being knocked away.
- Charge 'N' Slam can be used to get away by running through one or multiple walls.
- Charge 'N' Slam is able to deal the most structure damage in the shortest time out of any item. For example, it is possible to take out most of the supporting walls of a single house in Monaco by running along the edges of its floor.

[Guide > Weaknesses]
- The Nullifier can stop a charge in its tracks.
- Attempting to reach a far-away target with the Charge 'N' Slam while they have opened fire on its user will often end up with the user taking a lot of damage or being taken down as they are a very easy target in this state. Therefore, Charge 'N' Slam should generally only be used offensively when the target is already somewhat close.

[Guide > Tactics]
- Charge 'N' Slam can be activated while out of combat if the opponents are still far away, as this provides a movement speed boost.
- If the user jumps (while grounded) just before the ability ends, they'll travel a bit farther than if they let the ability finish on its own.

---

Result 4  cite as: [Sledgehammer § Guide > Tactics]
covers: Guide > Tactics / Guide > Useful Damage Combinations (cite any of these sections of Sledgehammer)
url: https://www.thefinals.wiki/wiki/Sledgehammer
- The user can freely rotate while charging up the overhead swing if an opponent is trying to dodge it by moving around the user.
- The Goo Gun can be used to trap opponents, allowing the user to catch up with them and hit them with a hammer swing. The Sledgehammer will deal damage to the target even if there is a goo blob around them.
- The Winch Claw can be used to reel in an opponent, to subsequently hit them with an overhead swing.
- The overhead swing always outdamages the regular swing. The regular swing sh
```
</details>

`q10,?,?,`

---
### q13 (single): How fast does the Healing Emitter heal and over what radius?

| Reference | Agent's answer |
|---|---|
| 10 HP/s rising to 15 HP/s over 2 seconds, in a 4 m radius. | The Healing Emitter heals at a rate of 10 health per second, ramping up to 15 health per second over 2 seconds [Healing Emitter § Overview]. It has a radius of 4m [Healing Emitter § Overview] [Healing Emitter § Usage]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Healing Emitter § Overview]
url: https://www.thefinals.wiki/wiki/Healing_Emitter
Healing Emitter
“Deployable that heals you and nearby teammates. Can be picked up, carried and thrown.”
Profile
Build: H Heavy
Icon
Type: Utility
Unlock: Guardian
Stats
Cooldown: 30s
Ammo: 1
Technical
Radius: 4m
Health: 200
Healing: 10/s → 15/s (over 2s)
The Healing Emitter is a Heavy class placeable and carriable gadget that heals contestants and their teammates within small area around itself.

---

Result 2  cite as: [Healing Emitter § Stats > Properties > Emmiter]
url: https://www.thefinals.wiki/wiki/Healing_Emitter
Support — Provides healing to teammates around it.
Solid — Has its own collision, meaning it blocks bullets and contestants can stand on it.
Arming Time — After initiall deployment doesn't provide healing. Starts healing automatically after a wind-up time. Healing Emitter doesn't remain active when picked up and needs to go through wind-up process again after it is dropped.
Destructible — Can be destroyed if its health is fully depleted, such as through hits from bullets or explosions. Has a health bar and cannot take damage from the user's team.
Glitchable — Can be temporarily disabled by a Glitch Grenade or Glitch Barrel .
Reshapeable — Can be reshaped by the Data Reshaper into a another arena carriable by opponents.
Sound Cue — Remains silent while idling or healing, but produces sound during the wind-up and then goes silent, signaling that it's ready to heal contestants.
Permanent — Does not disappear by itself.
Damaging — Hitting an ememy contestant with the thrown emitter directly deals 50 damage.
Not Attached — Can be picked up and carried or thrown. Acts like any other carriable object .
No Structure Damage — Cannot be used to damage structures.
No Friendly Fire — Can damage neither the user nor their teammates.
Not Interceptible — Can not be removed by the APS Turret .

---

Result 3  cite as: [Healing Emitter § Stats > Properties > Gadget]
url: https://www.thefinals.wiki/wiki/Healing_Emitter
Placeable — Can be placed on a surface or in the air. An indicator shows the exact target placement. If placed in the air the gadget will fall on the ground.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
Retrievable — Can be picked up after being deployed. For the Healing Emitter, this does not restore a full charge, but refunds most of the cooldown instead.
Remote Controlled — Can be commanded to self-destruct by the user from any distance. This refunds half of the cooldown.
Deployment Limit — Can only be deployed if there is no existing Healing Emitter.

---

Result 4  cite as: [Healing Beam § Stats > Effects]
covers: Stats > Effects / Stats > Overheat / Stats > Properties > Gadget / Stats > Properties > Heal Beam (cite any of these sections of Healing Beam)
url: https://www.thefinals.wiki/wiki/Healing_Beam
The Healing Beam can be used by aiming it at another contestant on the user's team within its 13m range and sustaining fire on them. The teammate will be healed at a rate of 46 health per second. The Healing Beam will overheat after healing 253 HP without pause.

[Stats > Overheat]
When not overheated, pausing for 0.5 seconds will gradually restore total energy at a rate of 40 health points per second.
The Healing Beam has a maximum overheat time of 5.5 seconds. This means that if you continuously heal a teammate (who isn't at full health), the beam will overheat after 5.5 seconds of use, regardless of the healing rate.After overheating, it takes 7.5 seconds to be usable again.

[Stats > Properties > Gadget]
Targeted — Can be activated while targeting a teammate. The teammate needs to remain within line of sight to continue healing them.
Battery Charge — Uses up charge while used. Recharges over time. The Healing Beam can overheat if used to its limit, causing it to go on a cooldown.
Disarms User — Forces the user to stop using their other items for an extended time to be able to use the gadget effectively.
No Self Targeted — Cannot be used to heal the user.

[Stats > Properties > Heal Beam]
Support — Applies a positive effect to teammates.
Not Interceptible — Can not be removed by the APS Turret .
Not Damaging — Hitting a contestant directly with the projectile does not deal damage.

---

Result 5  cite as: [Healing Emitter § Usage]
url: https://www.thefinals.wiki/wiki/Healing_Emitter
The Healing Emitter can be selected as one of three gadgets in any Heavy build loadout.
When placed, it activates after a short wind‑up and heals it's team contestants within a 4 m radius if there's no obstacles. Healing Emitter acts like any arena carriable , so any contestant can pick it up, regardless of the team they're on. Once a Healing Emitter has been picked up, it is no longer providing its effects until it is either placed again or thrown on the ground.
While the Healing Emitter is deployed, the gadget will not start restoring its next charge. If emitter is d
```
</details>

`q13,?,?,`

---
### q17 (single): How much environmental (structure) damage does one KS-23 slug deal?

| Reference | Agent's answer |
|---|---|
| 1000 environmental damage per slug (100 body damage). | One KS-23 slug deals 1000 environmental structure damage [KS-23 § Overview]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [KS-23 § Segmented Reload > Properties > Bullet]
url: https://www.thefinals.wiki/wiki/KS-23
Hitscan — Up to 25m — Travels in a straight line, meaning there is no bullet drop. The direction will deviate from the crosshairs depending on accuracy.
Projectile — After 25m — Gets affected by gravity and has a travel time.
Mid Range Falloff — Deals reduced damage when hitting targets at a moderate distance (falloff starts at less than 30m).
Moderate Structure Damage — Damages structures. Takes a few seconds or multiple charges to break a concrete wall.
No Critical Hit — Does not critically hit for increased damage, even if the target was struck on the head.
Not Interceptible — Can not be removed by the APS Turret .

---

Result 2  cite as: [KS-23 § Overview]
covers: Overview / Usage (cite any of these sections of KS-23)
url: https://www.thefinals.wiki/wiki/KS-23
KS-23
Weapon Quote: “Pump-action shotgun that fires slugs that deal high arena damage”
Profile
Build: H Heavy
Icon
Type: Shotgun
Unlock: Strategist
Damage
Body: 100
Environmental: 1000
Damage Falloff
Min Range: 12m
Max Range: 22m
Multiplier: 0.58
Technical
RPM: 78
Magazine: 6
Empty Reload: 4.36s
Tactical Reload: Segmented
The KS-23 ( K arabin S petsialniy 23 mm) is a Heavy class slug shotgun designed to deal high damage per slug at close to moderate distances, also dealing significant damage to structures.

[Usage]
The KS-23 can be selected as the weapon of any Heavy build loadout.
The trigger can be pulled to fire one projectile that damages an opponent. The weapon does not deal additional damage on headshots but deals significant structure damage. The trigger must be released before firing again. Zooming in with the secondary trigger slightly increases the KS-23's accuracy. Moving decreases accuracy.
The KS-23 reloads by inserting one round at a time, making its reload extremely slow. However, the reload can be interrupted before the magazine is full to reload less rounds.
The weapon automatically reloads when its magazine is empty, or the user can do a tactical reload before this point. The user has unlimited spare ammunition.
Equip KS-23: PC 1; PS △; XBox Y; Key Weapon
Fire slug (Tap): PS R2; XBox RT; Key Primary fire
Zoom (Hold): PS L2; XBox LT; Key Secondary fire
Tactical reload: PC R; PS ◻; XBox X; Key Reload

---

Result 3  cite as: [KS-23 § Guide > Tactics]
url: https://www.thefinals.wiki/wiki/KS-23
- A quick-melee kick can widen the gap between the user and enemy contestants to force them out of extreme close quarters, if for just a moment, slightly helping with the weapon's downside of being weaker in direct fights.
- A concrete wall and ceilings take two shots to breach, sometimes three if there's additional objects in the way. You can fire slugs until you're one shot away from breaking your obstacle, reload to full then fire the last shot to enter the area with 5/6 shots in your weapon.
- Walls and floors can be prematurely shot with the KS-23 to make them easily breakable later on. This can, for example, be utilized to shoot the ground near the Cashout Station during defense preparation, to later quickly drop it by shooting the floor when necessary, potentially stalling a steal and preserve charges of explosive Gadgets if the user has any or somewhat substitute them.
- A KS-23 user may need to lead their target at longer distances, i.e. firing at the location where they will be when the projectile arrives. This is because the KS-23's attack uses a projectile instead of a hitscan beyond 25m.
- A full reload has a long wind-up time, but then reloads much more quickly. For this reason, the full reload should preferably not be interrupted by firing, but the tactical reload can be interrupted.

---

Result 4  cite as: [KS-23 § Stats > Damage Profile]
covers: Stats > Damage Profile / Segmented Reload / Segmented Reload > Properties > Weapon (cite any of these sections of KS-23)
url: https://www.thefinals.wiki/wiki/KS-23
Body: Light (175 HP) Shells to kill 2; Light (175 HP) Time to kill (s) 0.769; Medium (250 HP) Shells to kill 3; Medium (250 HP) Time to kill (s) 1.538; Heavy (325 HP) Shells to kill 4; Heavy (325 HP) Time to kill (s) 2.308
Values are approximate and determined by community testing ( 12.0.0 ).

[Segmented Reload]
Reload time can be expressed as 1 + 0.75 x , where x = missing ammo − 1 , if x ≤ 5 .
1: 1s
2: 1.75s
3: 2.5s
4: 3.25s
5: 4s
6: 4.36s

[Segmented Reload > Properties > Weapon]
Ranged — Strikes targets by aiming and firing at them from a distance.
Single Fire — Fires once when the trigger is pulled. The trigger must be released before firing again.
Round Reload — Inserts a single round on reload. The next round(s) will also start reloading automatically until the magazine is full.
No Multi-Shot — Releases a single slug projectile with each shot.
No Aiming Down Sights — Cannot use sights. Zooms in slightly instead, but doing so does not significantly affect accuracy.
Unstable Accuracy — Suffers a significant d
```
</details>

`q17,?,?,`

---
### q19 (single): What is Double Jeopardy in Cashout?

| Reference | Agent's answer |
|---|---|
| An anti-griefing rule since Season 9: it triggers when a team inserts a second Cash Box into an already active Cashout Station; if that team fails to secure the station, it loses 50% of its current cash. | Double Jeopardy is an anti-griefing mechanic in Cashout designed to discourage strategic griefing, such as deliberately targeting a specific squad or manipulating which teams advance [Cashout § Gameplay].   * **Trigger:** It is triggered when a team inserts a second Cash Box into an already active Cashout Station [Cashout § Rules > Objective > Cashout Station].  * **Penalty:** If that team fails to secure and own the Cashout Station when the timer expires, they instantly lose 50% of their current total cash [Cashout § Gameplay] [Cashout § Rules > Objective > Cashout Station]. * **Indicators:** When triggered, the team is highlighted in red on the scoreboard, their team name is shown on screen, and a dedicated callout plays from commentators Scotty and June [Cashout § Gameplay]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Cashout § Gameplay]
url: https://www.thefinals.wiki/wiki/Cashout
Double Jeopardy is designed to discourage strategic griefing, such as deliberately targeting a specific squad to eliminate them from contention or manipulating which teams advance to the next round. When a team triggers Double Jeopardy by inserting the second Cash Box, they will be highlighted in red on the scoreboard and the name of their team will be shown on screen—alongside a dedicated callout from Scotty and June . If that team fails to secure the Cashout Station before it completes, they lose 50% of their current cash.
Objectives
Vault Cash Box Cashout Station
Main page: Vault
VAULT
Type: Arena object
Effect: Holds a Cash Box
Windup Time: 15s
opening time: 20s
SFX 1: Vault opening https://www.thefinals.wiki/wiki/File:Vault_open.mp3
Vaults are stationary arena objects that spawns at any arena's predetermined locations.
They serve as the main source of objectives in Cashout Gamemodes . When unlocked by contestants, a Vault ejects its contents and then disappears granting $1,000.
Once opened, a Vault ejects a single
Cash Box
, which can then be transported to a
Cashout Station
to initiate a cashout. Vaults themselves cannot be reused and will vanish after they eject their contents.
Open: PC E; PS △; XBox Y; Key Interact
Final round | 1 | 3
Knockout rounds | 2 | 6
Main page: Cash Box
CASH BOX
Type: Arena Carriable
Effect: Used to transport cash from a Vault to a Cashout Station
Damage: 50
Value: $10,000 - $25,000

---

Result 2  cite as: [Ranked Cashout § Gameplay]
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
Double Jeopardy is designed to discourage strategic griefing, such as deliberately targeting a specific squad to eliminate them from contention or manipulating which teams advance to the next round. When a team triggers Double Jeopardy by inserting the second Cash Box, they will be highlighted in red on the scoreboard and the name of their team will be shown on screen—alongside a dedicated callout from Scotty and June . If that team fails to secure the Cashout Station before it completes, they lose 50% of their current cash.
Objectives
Vault Cash Box Cashout Station
Main page: Vault
VAULT
Type: Arena object
Effect: Holds a Cash Box
Windup Time: 15s
opening time: 20s
SFX 1: Vault opening https://www.thefinals.wiki/wiki/File:Vault_open.mp3
Vaults are stationary arena objects that spawns at any arena's predetermined locations.
They serve as the main source of objectives in Cashout Gamemodes . When unlocked by contestants, a Vault ejects its contents and then disappears granting $1,000.
Once opened, a Vault ejects a single
Cash Box
, which can then be transported to a
Cashout Station
to initiate a cashout. Vaults themselves cannot be reused and will vanish after they eject their contents.
Open: PC E; PS △; XBox Y; Key Interact
Final round | 1 | 3
Knockout rounds | 2 | 6
Main page: Cash Box
CASH BOX
Type: Arena Carriable
Effect: Used to transport cash from a Vault to a Cashout Station
Damage: 50
Value: $10,000 - $25,000

---

Result 3  cite as: [Cashout § Rules > Objective > Cashout Station]
url: https://www.thefinals.wiki/wiki/Cashout
- Two Cashout Stations spawn at the start of the game, with a new one appearing after each completed deposit.
- Only two Cashout Stations can be active at a time.
- Multiple Cash Boxes can be deposited into the same Cashout Station to increase the total cash value. The contestant that inserted a second Cash Box triggers Double Jeopardy for their team. If their team is not the owner of the Cashout Station when the timer expires, they instantly lose 50% of their total cash.
- Stealing an active Cashout Station takes 7 seconds and grants $1,000 during Qualifying Rounds.
- Stealing an active Cashout Station takes 6 seconds and grants $0 during the Final Round.
- Inactive Cashout Stations will despawn when overtime starts.
Deposit Process
- To start a deposit, place the Cash Box into a Cashout Station .
- When a Cash Box is deposited, 20% of its value is instantly awarded to the team, while the remaining 80% is stored in the Cashout Station .
- The deposit process takes 2 minutes to complete in regular time.
- If enough time remains in the round, the deposit lasts the full duration; otherwise, up to 1 minute of overtime is added.

---

Result 4  cite as: [Ranked Cashout § Rules > Objective > Cashout Station]
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
- Two Cashout Stations spawn at the start of the game, with a new one appearing after each completed deposit.
- Only two Cashout Stations can be active at a time.
- Multiple Cash Boxes can be deposited into the same Cashout Station to increase the total cash value. The contestant that inserted a second Cash Box triggers Double Jeopardy for their team. If their team is not the owner of the Cashout Station when the timer expires, they instantly lose 50% of their total cash.
- Stealing an active Cashout Station takes 7 seconds and grant
```
</details>

`q19,?,?,`

---
### q23 (single): Why was the Las Vegas arena removed from the game?

| Reference | Agent's answer |
|---|---|
| With the PRIME TIME season it was removed because of the difficulty of maintaining both Las Vegas and the reworked Las Vegas Stadium. | Las Vegas was entirely removed from the game with the release of the PRIME TIME season due to the difficulties of maintaining both the original map and its reworked version, Las Vegas Stadium, at the same time [Las Vegas § Overview]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Las Vegas § Overview]
covers: Overview / Arena Variants > Standard Issue / Arena Variants > Sandstorm (cite any of these sections of Las Vegas)
url: https://www.thefinals.wiki/wiki/Las_Vegas
Las Vegas has been removed from the game, and may return in the future!
Las Vegas
Introduced: Season 1
Sponsor(s): OSPUZE
Arena Variant(s): Sandstorm Standard Issue Tripwires & Turrets
Las Vegas 2032 was introduced with the launch of the game and Season 1 , and was the fourth Arena to be added. It is based on the real-life city of Las Vegas in the United States and features various casinos and attractions.
In Season 6 , Las Vegas was replaced by the reworked version Las Vegas Stadium . It later returned in the same season as a part of World Tour arena rotation, then later was added to the pull of gamemodes .
With the release of PRIME TIME season Las Vegas was entirely removed from the game due to difficulties of maintaining both versions of Las Vegas at the same time.

Map of Las Vegas Arena by Atsuhiro
Las Vegas is a moderately sized arena with open streets and building roofs that are dangerously open to traverse and tight insides of the buildings that offer a lot of cover.

[Arena Variants > Standard Issue]
“A standard arena, ready for destruction.”

[Arena Variants > Sandstorm]
“Don’t get lost in stinging sands! Seek shelter and glory in this Las Vegas map variant.”
Swirling sand clouds drastically reduce visibility.

---

Result 2  cite as: [Cashout § Arenas > Temporary Unavailable]
url: https://www.thefinals.wiki/wiki/Cashout
Las Vegas: Sandstorm • Standard Issue

---

Result 3  cite as: [Las Vegas Stadium § Overview]
covers: Overview / Arena Variants > Standard Issue / Arena Variants > Sandstorm (cite any of these sections of Las Vegas Stadium)
url: https://www.thefinals.wiki/wiki/Las_Vegas_Stadium
This article is a Stub . It needs some work! You can help us out by expanding it .
Information in this article is outdated . It no longer reflects the latest state of THE FINALS. You can help us out by updating it . Reason: Arena was reworked with the release of PRIME TIME season
Las Vegas Stadium
Introduced: Season 6
Sponsor(s): ALFA ACTA , OSPUZE , ENGIMO
Arena Variant(s): Sandstorm Standard Issue
Supported Gamemode(s): Cashout Point Break Power Shift Quick Cash Ranked Cashout Team Deathmatch
Las Vegas Stadium was introduced with Season 6 and was the ninth arena to be added. It is a reworked version of Las Vegas that transforms the original into a championship stadium, with a focus on improved movement, cleaner sightlines, and smoother combat flow. Season 6 sponsors OSPUZE , ALFA ACTA , and ENGIMO took over the casinos and branded them to fit their own architectural aesthetics.

Map of Las Vegas Stadium Arena.
Las Vegas is a moderately sized arena with open streets and building roofs that are dangerously open to traverse and tight insides of the buildings that offer a lot of cover.

[Arena Variants > Standard Issue]
“A standard arena, ready for destruction.”

[Arena Variants > Sandstorm]
“Don’t get lost in stinging sands! Seek shelter and glory in this Las Vegas map variant.”
Swirling sand clouds drastically reduce visibility.

---

Result 4  cite as: [Quick Cash § Arenas]
covers: Arenas / Arenas > Temporary Unavailable (cite any of these sections of Quick Cash)
url: https://www.thefinals.wiki/wiki/Quick_Cash
Bernal: Standard Issue • Suspended Structures
Fangwai City: Standard Issue
Fortune Stadium: Standard Issue
Galaxy Estates: Standard Issue
Kyoto: Moving Platforms • Standard Issue • Suspended Structures
Las Vegas Stadium: Sandstorm • Standard Issue
Monaco: File:Icon ArenaVariant Duck and Cover.png Duck and Cover • Standard Issue • Suspended Structures
NOZOMI/CITADEL: Standard Issue
Seoul: Moving Platforms • Standard Issue • Under Construction
Skyway Stadium: High Rise • Standard Issue • Up Down Left Right
SYS$HORIZON: Standard Issue

[Arenas > Temporary Unavailable]
Las Vegas: Sandstorm • Standard Issue

---

Result 5  cite as: [Las Vegas § Arena Variants > Sandstorm > Tripwires & Turrets]
covers: Arena Variants > Sandstorm > Tripwires & Turrets / Locations / Supported Gamemodes / Supported Gamemodes > Limited Time Modes (cite any of these sections of Las Vegas)
url: https://www.thefinals.wiki/wiki/Las_Vegas
“The environment can work for or against you. Traverse Vegas but watch your step, around every corner could be a trap.”
Notes: This modifier is only available in the Steal The Spotlight LTM .

[Locations]
This article is a Stub . It needs some work! You can help us out by expanding it .
Argon Casino: ***
Casino Eastwood: ***
Glamora: ***
Zaraby: ***
Parking Lot: ***
Stage: ***
Fremont Street: ***

[Supported Gamemodes]
Las Vegas supports the following Gamemodes :

[Supported Gamemodes > Limited Time Modes]
- Bank It
- Head2Head
- Steal The Spotlight
```
</details>

`q23,?,?,`

---
### m01 (multi): Which items or effects can reveal an enemy who is using the Cloaking Device?

| Reference | Agent's answer |
|---|---|
| Thermal Vision, the Motion Sensor and the Sonar Grenade (Cloaking Device weaknesses), and True Sight, which shows cloaked opponents fully. | The items, specializations, and effects that can reveal or counter an enemy using the Cloaking Device include:  * **Thermal Vision:** Hard counters the Cloaking Device by revealing the heat signature of a cloaked player [Cloaking Device § Guide > Weaknesses]. * **True Sight:** A Light build specialization that highlights opponents and makes them fully visible even under the effects of the Cloaking Device [True Sight § Overview] [True Sight § Stats > Effects]. * **Motion Sensor and Sonar Grenade:** Detection sources that can reveal the location of a cloaked enemy [Cloaking Device § Guide > Weaknesses]. * **Taking Damage:** Dealing any damage to a cloaked player will cause them to instantly decloak [Cloaking Device § Guide > Weaknesses]. * **Visual & Audio Cues:** While moving, cloaked players display a glitchy visual effect and produce a distinct sound that can be heard by enemies up to 30m away (though they are nearly invisible and silent while completely motionless) [Cloaking Device § Stats > Effects] [Cloaking Device § Guide > Weaknesses] [Cloaking Device § Guide > Tactics]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Cloaking Device § Overview]
covers: Overview / Usage / Stats > Effects (cite any of these sections of Cloaking Device)
url: https://www.thefinals.wiki/wiki/Cloaking_Device
CLOAKING DEVICE
“A temporary cloak that makes you hard to see when moving, and invisible when motionless”
Profile
Build: L Light
Icon
Type: Specialization
Unlock: Assassin
Stats
Cooldown: Energy-Based
Technical
Duration: Min - 11s Max - 29s
Activation Costs: 33% of energy
The Cloaking Device is a Light class specialization that allows its user to enter invisibility for a limited duration.

[Usage]
The Cloaking Device can be selected as the specialization gadget of any Light build loadout.
The specialization trigger can be used to toggle on the gadget. It will remain active for up to 12 seconds, after which it is automatically disabled to recharge. It can also be disabled before this point by toggling it again. Attacking or using an item will forcibly end the effect.
Energy consumption is largely based on speed; crouching will lower energy consumption, sprinting will increase it.
Toggle on/off (Tap): PC Q; PS R1; XBox RB; Key Specialization

[Stats > Effects]
The Cloaking Device can be activated to grant its user temporary invisibility. Opponents will not be able to see the user well, although there are still indications that the user is present:
- A glitchy visual effect replaces the contestant's body. This effect is almost completely invisible while the user is standing still, but very noticeable if the user is moving.
- A glitchy sound is produced when you; activate cloak, move while cloaked, or the cloak is deactivated. This can be heard by enemies up to 30m away.

---

Result 2  cite as: [Cloaking Device § Guide > Weaknesses]
covers: Guide > Weaknesses / Guide > Tactics (cite any of these sections of Cloaking Device)
url: https://www.thefinals.wiki/wiki/Cloaking_Device
- Thermal Vision hard counters the Cloaking Device as it can also reveal the heat signature of a cloaked player.
- Detection sources such as the Motion Sensor and Sonar Grenade can still reveal the location of a cloaked enemy.
- When you activate or deactivate the Cloaking Device, it makes a distinct sound that can be heard from up to 30m away.
- Moving while cloaked makes a loud distinct sound which can also be heard from up to 30m away.
- Taking damage will cause a cloaked player to instantly decloak.
- Activating cloak consumes 33% of your overall meter, punishing repeated uses.

[Guide > Tactics]
- Remaining in a motionless state while cloaked will make it nearly impossible for enemies to see and hear you and consume less cloak meter.
- Activating Cloaking Device while cloaked from a Vanishing Bomb allows the contestant to seamlessly transition to the other invisibility, effectively extending it. There will be a subtle visual cue when activating the cloaking device this way.
- Mantling an object in a motionless state by tapping the forward and jump buttons at the same time will retain the motionless state properties, allowing you to move slightly while still being extremely difficult to see and hear and consuming the least amount of cloak meter.
- Utilize loud sound effects from the arena, or setup your own with Breach Charge , Gravity Vortex , or Thermal Bore to mask your cloak activation sound and/or movement sounds.

---

Result 3  cite as: [Cloaking Device § Stats > Energy-Based Cooldown]
covers: Stats > Energy-Based Cooldown / Stats > Properties > Gadget / Stats > Properties > Effect / Guide > Strengths (cite any of these sections of Cloaking Device)
url: https://www.thefinals.wiki/wiki/Cloaking_Device
The Cloaking Device consumes energy based on the user’s movement speed while cloaked, remaining motionless consumes the least amount of energy, enabling the user to stay cloaked for a maximum of 27 seconds in a single charge.
The Cloaking Device’s invisibility will not be disrupted by burning or poison damage.

[Stats > Properties > Gadget]
Self Targeted — Can be activated to apply an effect to the contestant that used it.
Toggle — Can be enabled and disabled by reactivating.
Battery Charge — Uses up charge while used. Recharges over time.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
Disarms User — Forces the user to stop using their other items, as doing so will cancel the Cloaking Device.

[Stats > Properties > Effect]
Sound Cue — Produces a glitched noise while moving, alerting nearby contestants of the user's presence.
Visibility — Affects the line of sight of the user and/or opponents. Opponents are unable to see the user well.

[Guide > Strengths]
- Standing still while cloaked will make the user nearly undetectable, even to opponents who are walking directly past the user. The user still has collision which could give them away if an opponent bumps into them.

---

Result 4  cite as: [Vanishing Bomb § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget (cite any of these secti
```
</details>

`m01,?,?,`

---
### m02 (multi): Which has the larger magazine, the AKM or the FCAR, and by how many rounds?

| Reference | Agent's answer |
|---|---|
| The AKM: 36 rounds vs 20 for the FCAR, 16 more. | The AKM has the larger magazine [AKM § Guide > Strengths] [FCAR § Guide > Strengths].   * **AKM Magazine:** 36 rounds [AKM § Overview] * **FCAR Magazine:** 20 rounds [FCAR § Overview]  The AKM has a larger magazine by **16 rounds**. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [AKM § Overview]
covers: Overview / Usage (cite any of these sections of AKM)
url: https://www.thefinals.wiki/wiki/AKM
AKM
Weapon Quote: “Fully automatic assault rifle”
Profile
Build: M Medium
Icon
Type: Assault Rifle
Unlock: Free
Damage
Body: 21
Head: 31.5 (1.5×)
Environmental: 10
Damage Falloff
Min Range: 30m
Max Range: 37.5m
Multiplier: 0.55
Technical
RPM: 600
Magazine: 36
Empty Reload: 2.35s
Tactical Reload: 2.35s
The AKM ( A vtomat K alashnikova M odernizirovanny) is an automatic assault rifle available to the Medium class. It is best suited for dealing sustained damage at medium range and is easy for new contestants to excel with.

[Usage]
The AKM can be selected as the weapon of any Medium build loadout.
The trigger can be held to continuously fire bullets that damage opponents, also dealing additional damage on headshots. Aiming down sights increases the AKM's accuracy. Moving decreases accuracy, especially when going airborne.
The weapon automatically reloads when its magazine is empty, or the user can do a tactical reload before this point. The user has unlimited spare ammunition.
Equip AKM: PC 1; PS △; XBox Y; Key Weapon
Fire shot (Tap) Continuous fire (Hold): PS R2; XBox RT; Key Primary fire
Aim down sights (Hold): PS L2; XBox LT; Key Secondary fire
Tactical reload: PC R; PS ◻; XBox X; Key Reload

---

Result 2  cite as: [AKM § Stats > Damage Profile]
covers: Stats > Damage Profile / Stats > Sights / Stats > Properties > Weapon (cite any of these sections of AKM)
url: https://www.thefinals.wiki/wiki/AKM
Head: Light (175 HP) Bullets to kill 6; Light (175 HP) Time to kill (s) 0.5; Medium (250 HP) Bullets to kill 8; Medium (250 HP) Time to kill (s) 0.7; Heavy (325 HP) Bullets to kill 11; Heavy (325 HP) Time to kill (s) 1.0
Body: Light (175 HP) Bullets to kill 9; Light (175 HP) Time to kill (s) 0.8; Medium (250 HP) Bullets to kill 12; Medium (250 HP) Time to kill (s) 1.1; Heavy (325 HP) Bullets to kill 16; Heavy (325 HP) Time to kill (s) 1.5
Values are approximate and determined by community testing ( 12.2.0 ).

[Stats > Sights]
Main page: Sights
IRON SIGHTS
ADDER REFLEX
COMPACT REFLECTOR
HOLOGRAPHIC
LOOKING GLASS

[Stats > Properties > Weapon]
Ranged — Strikes targets by aiming and firing at them from a distance.
Automatic Fire — Continues to fire automatically until the trigger is released.
Aim Down Sights — Has iron sights and optical sights that significantly increase accuracy when used.
Full Reload — Replaces the entire magazine in one animation on reload.
Unstable Accuracy — Suffers a significant decrease in accuracy while moving and while airborne.

---

Result 3  cite as: [AKM § Stats > Properties > Bullet]
covers: Stats > Properties > Bullet / Guide > Strengths / Guide > Weaknesses / Guide > Tactics (cite any of these sections of AKM)
url: https://www.thefinals.wiki/wiki/AKM
Hitscan — Travels in a straight line, meaning there is no bullet drop. The direction will deviate from the crosshairs depending on accuracy.
Critical Hit — Critically hits on headshots, applying a damage multiplier.
High Range Falloff — Deals reduced damage when hitting targets at long distances (falloff starts beyond 30m).
Minor Structure Damage — Damages structures. Takes a very long time to break a concrete wall.

[Guide > Strengths]
- The AKM has the second highest magazine size out of any Medium class ranged weapon, behind the P90 .
- The AKM is able to sustain fire for longer than the comparable FCAR without reloading. However, it has a lower immediate damage output and has a higher reload time.

[Guide > Weaknesses]
- The AKM's damage begins to fall off at moderate distances, and falls off severely at long distances. Additionally, due to bullet dispersion, it becomes more difficult to hit the target consistently.

[Guide > Tactics]
- Firing should always be done while aiming down sights, unless the target is extremely close. Doing so greatly increases the accuracy of the AKM.

---

Result 4  cite as: [AKM § Guide > Recoil]
url: https://www.thefinals.wiki/wiki/AKM
How to control:
- Pull down hard and slightly right during the first four bullets
- Pull down and left until the 10th bullet
- After the 10th bullet, pull down evenly until bullet 26.
- After the 26th bullet, pull directly to the right until the mag is empty
Hitscan
- When the weapon fires a shot, a target is scanned for using a hitscan. This is a detection mechanism that scans in a straight line, meaning there is no bullet drop. The direction of this line will be deviate randomly from the direction of the crosshairs, depending on the accuracy level at the time of firing.
- Immediately, the closest contestant, structure, object or shield intersecting the hitscan will be tagged as being struck. First, a bullet tracer animation quickly travels from the weapon to the hit location, then its effects are applied. This means it is possible for targets to be struck a few frames after they appear to take cover, as the hit is confirmed the momen
```
</details>

`m02,?,?,`

---
### m03 (multi): Which deals more environmental damage per shot, the KS-23 or the CL-40?

| Reference | Agent's answer |
|---|---|
| The KS-23: 1000 per slug vs 300 for the CL-40. | The KS-23 deals more environmental damage per shot than the CL-40 [KS-23 § Overview] [CL-40 § Overview].   * **KS-23 (Heavy):** Deals **1000** environmental damage per shot [KS-23 § Overview]. * **CL-40 (Medium):** Deals **300** environmental damage per shot [CL-40 § Overview]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [KS-23 § Overview]
covers: Overview / Usage (cite any of these sections of KS-23)
url: https://www.thefinals.wiki/wiki/KS-23
KS-23
Weapon Quote: “Pump-action shotgun that fires slugs that deal high arena damage”
Profile
Build: H Heavy
Icon
Type: Shotgun
Unlock: Strategist
Damage
Body: 100
Environmental: 1000
Damage Falloff
Min Range: 12m
Max Range: 22m
Multiplier: 0.58
Technical
RPM: 78
Magazine: 6
Empty Reload: 4.36s
Tactical Reload: Segmented
The KS-23 ( K arabin S petsialniy 23 mm) is a Heavy class slug shotgun designed to deal high damage per slug at close to moderate distances, also dealing significant damage to structures.

[Usage]
The KS-23 can be selected as the weapon of any Heavy build loadout.
The trigger can be pulled to fire one projectile that damages an opponent. The weapon does not deal additional damage on headshots but deals significant structure damage. The trigger must be released before firing again. Zooming in with the secondary trigger slightly increases the KS-23's accuracy. Moving decreases accuracy.
The KS-23 reloads by inserting one round at a time, making its reload extremely slow. However, the reload can be interrupted before the magazine is full to reload less rounds.
The weapon automatically reloads when its magazine is empty, or the user can do a tactical reload before this point. The user has unlimited spare ammunition.
Equip KS-23: PC 1; PS △; XBox Y; Key Weapon
Fire slug (Tap): PS R2; XBox RT; Key Primary fire
Zoom (Hold): PS L2; XBox LT; Key Secondary fire
Tactical reload: PC R; PS ◻; XBox X; Key Reload

---

Result 2  cite as: [KS-23 § Segmented Reload > Properties > Bullet]
url: https://www.thefinals.wiki/wiki/KS-23
Hitscan — Up to 25m — Travels in a straight line, meaning there is no bullet drop. The direction will deviate from the crosshairs depending on accuracy.
Projectile — After 25m — Gets affected by gravity and has a travel time.
Mid Range Falloff — Deals reduced damage when hitting targets at a moderate distance (falloff starts at less than 30m).
Moderate Structure Damage — Damages structures. Takes a few seconds or multiple charges to break a concrete wall.
No Critical Hit — Does not critically hit for increased damage, even if the target was struck on the head.
Not Interceptible — Can not be removed by the APS Turret .

---

Result 3  cite as: [KS-23 § Guide > Tactics]
url: https://www.thefinals.wiki/wiki/KS-23
- Due to the long downtime between firing, it is important for the KS-23 user to utilise cover through the enviroment or Gadgets in order to hide between shots and mitigate damage taken while the KS-23 cycles its next shot. With the damage starting to fall off at 12 meters, positioning is very important as the user should be trying to find an appropriate distance to their enemies where they can benefit from cover without losing out on too much damage. The Barricade and Dome Shield are great Gadgets to pair with the KS-23 to have very quick and durable cover available. The Goo Gun can quickly create a piller of two to three Goo blobs for similar effect, although less durable and less wide in size. The Goo Grenade creates big walls and is also useful for mobility around the map, but switching to and deploying it takes a decent amount of time and the wall that spawns might not form in a way the user wanted it to. Despite the downtime, the KS-23 is still very capable in direct close range encounters particularly against Lights and Heavies . The former can be eliminated in just two accurate shots and, when against the latter, the user can substitute the 4th shot with a Quick Melee attack.

---

Result 4  cite as: [KS-23 § Stats > Damage Profile]
covers: Stats > Damage Profile / Segmented Reload / Segmented Reload > Properties > Weapon (cite any of these sections of KS-23)
url: https://www.thefinals.wiki/wiki/KS-23
Body: Light (175 HP) Shells to kill 2; Light (175 HP) Time to kill (s) 0.769; Medium (250 HP) Shells to kill 3; Medium (250 HP) Time to kill (s) 1.538; Heavy (325 HP) Shells to kill 4; Heavy (325 HP) Time to kill (s) 2.308
Values are approximate and determined by community testing ( 12.0.0 ).

[Segmented Reload]
Reload time can be expressed as 1 + 0.75 x , where x = missing ammo − 1 , if x ≤ 5 .
1: 1s
2: 1.75s
3: 2.5s
4: 3.25s
5: 4s
6: 4.36s

[Segmented Reload > Properties > Weapon]
Ranged — Strikes targets by aiming and firing at them from a distance.
Single Fire — Fires once when the trigger is pulled. The trigger must be released before firing again.
Round Reload — Inserts a single round on reload. The next round(s) will also start reloading automatically until the magazine is full.
No Multi-Shot — Releases a single slug projectile with each shot.
No Aiming Down Sights — Cannot use sights. Zooms in slightly instead, but doing so does not significantly affect accuracy.
Unstable Accuracy — Suffers a significant decrease in accuracy while moving and while airborne.

---

Result 5  cite as: [KS-23 § Guide > Strengths]
url: https:
```
</details>

`m03,?,?,`

---
### m04 (multi): Which has the shorter cooldown, the Breach Charge or the Thermal Bore, and which build uses them?

| Reference | Agent's answer |
|---|---|
| The Breach Charge (20 s vs 25 s for the Thermal Bore); both are Light gadgets. | The **Breach Charge** has the shorter cooldown (20s) compared to the Thermal Bore (25s) [Breach Charge § Overview] [Thermal Bore § Overview]. Both gadgets are used by the **Light** build [Breach Charge § Overview] [Thermal Bore § Overview]. |

<details><summary>Retrieved passages</summary>

```
Error executing tool search

Error executing tool search

Result 1  cite as: [Breach Charge § Overview]
covers: Overview / Usage / Usage > Detonator (cite any of these sections of Breach Charge)
url: https://www.thefinals.wiki/wiki/Breach_Charge
BREACH CHARGE
“ Highly destructive deployable explosive that can be remotely detonated”
Profile
Build: L Light
Icon
Type: Utility
Unlock: Assassin
Stats
Cooldown: 20s
Ammo: 3
Technical
Damage: 80
Environment Dmg: Over 2000
Damage Radius: 2.5m
Priming Time: 1s
Max Deployed: 3
Health: 25
The Breach Charge is a Light class mounted gadget which, when remotely detonated, creates an explosion that breaches structures.

[Usage]
The Breach Charge can be selected as one of three gadgets of any Light build loadout.
The primary trigger can be used to toss the gadget a small distance. It will attach to the first surface it contacts.
Once the gadget is armed, the user can use the gadget's secondary trigger to detonate the explosive remotely, from any place at any time.
The gadget can also be retrieved to restore a charge, by interacting with it for a few moments while looking at it from up close.

[Usage > Detonator]
- When armed, the light on the detonator is blue.
- When disarmed, the light on the detonator is yellow.
- When no breach charges are deployed, the light is red.
Equip Breach Charge: PC 2 3 4; PS L1; XBox LB; Key Gadget
Toss (Tap): PS R2; XBox RT; Key Primary fire
Detonate (Tap): PS L2; XBox LT; Key Secondary fire
Retrieve deployed Breach Charge (Hold): PC E; PS △; XBox Y; Key Interact

---

Result 2  cite as: [Breach Charge § Stats > Properties > Charge]
covers: Stats > Properties > Charge / Stats > Properties > Explosion (cite any of these sections of Breach Charge)
url: https://www.thefinals.wiki/wiki/Breach_Charge
Attached — Attaches to a surface upon deployment. Sticks to the surface even if it moves. Weighs down any carriable object it is attached to.
Solid — Has its own collision, albeit of a very small size, that can be stood upon.
Arming Time — Disarmed when initially deployed or while picked up as an attachment. Arms automatically after a wind-up time.
Destructible — Can be destroyed if its health is fully depleted, such as through hits from bullets or explosions. This causes the Breach Charge to explode. Teammates can also destroy it.
Glitchable — Can be temporarily disabled by a Glitch Grenade or Glitch Barrel .
Reshapeable — Can be reshaped by the Data Reshaper into a piece of decor by opponents.
Sound Cue — Produces a constant beeping noise while it is armed, alerting nearby contestants of its presence.
Permanent — Does not disappear by itself.
Reversible — Can be used against the user's team, if an opponent triggers the explosion by destroying the gadget. Any damage and eliminations are attributed to the opponent.

[Stats > Properties > Explosion]
Explosive — Deals damage in an area of effect that can be intercepted by structures and shields.
Damaging — Deals damage to contestants.
Major Structure Damage — Damages structures. Instantly destroys a concrete wall.
No Friendly Fire — Can damage the user, but not their teammates (unless an opponent caused it to explode).

---

Result 3  cite as: [Breach Charge § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget / Stats > Properties > Projectile (cite any of these sections of Breach Charge)
url: https://www.thefinals.wiki/wiki/Breach_Charge
The Breach Charge can be deployed with a small throw to attach it to a nearby surface. The gadget will arm itself after a few moments. From this point on, it can be remotely detonated, causing it to explode. The explosion deals major damage to the surrounding structure, effectively creating a large hole, and also deals damage to opponents in a small area.
If an opponent destroys the gadget, they become the user instead, meaning any damage it deals is attributed to them.

[Stats > Properties > Gadget]
Tossed — Can be thrown out a short distance, after which it attaches to the first surface it hits.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
Retrievable — Can be picked up after being deployed to restore a charge.
Remote Controlled — Comes with a remote to trigger all deployed Breach Charges from any distance.
Deployment Limit — 3 Breach Charges can be deployed at a time. An excess deployment causes the oldest Breach Charge to disappear.

[Stats > Properties > Projectile]
Projectile — Gets affected by gravity and has a travel time. Once attached, the gadget is no longer a projectile.
Interceptible — While not attached, can be removed by the APS Turret , nullifying its effects. This causes the turret to lose some health.
No Trigger on Impact — Does not trigger when thrown at a contestant, instead flies through them.
Not Damaging — Hitting a contestant directly with the projectile does not deal damage.

---

Result 4  cite as: [Breach Drill § Overview]
covers: Overview / Usage / Usage > Properties > Gadget (cite
```
</details>

`m04,?,?,`

---
### m05 (multi): How do team sizes differ between Quick Cash and Power Shift?

| Reference | Agent's answer |
|---|---|
| Quick Cash is three teams of three (3v3v3); Power Shift is two teams of five (5v5). | Quick Cash features 3v3v3 team sizes (three teams of three players) [Quick Cash § Overview], whereas Power Shift features 5v5 team sizes (two teams of five players) [Power Shift § Overview]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Power Shift § Overview]
covers: Overview / Objective (cite any of these sections of Power Shift)
url: https://www.thefinals.wiki/wiki/Power_Shift
Power Shift
“A casual 5v5 game mode where two teams compete to escort a platform through the arena.”
Overview
Short description: Hold the platform
Length: Single match
Format: 5v5
Features: Unlimited respawn credits
Progression: World Tour
Capture Platform Eliminate opponents or force them out of the platform to take control
Defend Platform Fend off enemy attacks and keep your team alive
Advance Platform Have up to 3 teammates on the platform to move at max speed
Power Shift is a 5v5 Quickplay gamemode in which two teams compete to escort a massive, moving platform through the arena. Teams fight for control of the platform as it advances along a fixed route, with momentum shifting as players engage, regroup, and contest key positions.

[Objective]
The objective of Power Shift is to escort the central platform into the opposing team’s goal area. Teams gain control of the platform by positioning contestants on it while preventing the enemy team from doing the same.
The distance the platform has traveled is represented by the money value displayed on the scoreboard, up to a maximum of $40,000 when the platform reaches the finish.

---

Result 2  cite as: [Power Shift § Platform Mechanics]
covers: Platform Mechanics / Contestants and Respawns (cite any of these sections of Power Shift)
url: https://www.thefinals.wiki/wiki/Power_Shift
- Activation : The platform begins moving shortly after a contestant steps onto it.
- Contested State : If contestants from both teams are on the platform simultaneously, movement halts until only one team remains.
- Speed : The platform speed increases with each contestant simultaneously standing on the platform, up to a cap. 1 Contestant: Slow 2 Contestants: Moderate 3+ Contestants: Maximum
- Unstoppable : The platform cannot be damaged, destroyed, or otherwise stopped. However, it can be rocked by certain impulse forces, such as explosions, and will destroy any terrain in its path.
- Hazardous : Contestants caught beneath the platform will take continuous damage until they leave the area or are eliminated.

[Contestants and Respawns]
- Loadouts : While waiting to respawn, contestants can swap their loadout freely, including their Build. Respawning as a team or using a respawn coin will apply any loadout changes, but being revived will not.
- Wave Respawns : Contestants respawn in timed waves to encourage coordinated re-engagements.
- Unlimited Coins : Each individual contestant has unlimited respawn coins.
- Spawn Locations : At the start of the match, both teams spawn an equal distance from the platform. Following respawns are based on the platform's current position, ensuring contestants return to the arena near the platform and do not need to travel a long distance.

---

Result 3  cite as: [Power Shift § Win Conditions]
covers: Win Conditions / Overtime Rules / Arenas (cite any of these sections of Power Shift)
url: https://www.thefinals.wiki/wiki/Power_Shift
- Primary Victory : A team wins by successfully escorting the platform into the opposing team's goal area.
- Time Expiry : If the timer expires before either goal is reached, the team that has pushed the platform furthest wins. If the platform is currently being contested, overtime begins instead.

[Overtime Rules]
- Trigger and Duration : Overtime is triggered if time expires while the platform is being contested, and lasts for a maximum of 5 minutes.
- Victory in Overtime : The team currently controlling the platform must escort it fully onto the opposing team’s side of the arena. The platform must not be contested when it reaches the end zone.
- Stalemate : If the platform has never been controlled by either team during the match, and overtime ends without a winner, the game will randomly assign victory to one of the teams.

[Arenas]
Bernal: Standard Issue • Suspended Structures
Kyoto: Standard Issue • Suspended Structures
Las Vegas Stadium: Standard Issue
Monaco: Standard Issue
NOZOMI/CITADEL: Standard Issue
Seoul: Standard Issue
Skyway Stadium: Standard Issue
SYS$HORIZON: Standard Issue

---

Result 4  cite as: [Cashout § Overview]
url: https://www.thefinals.wiki/wiki/Cashout
Cashout
Overview
Length: 1-3 Rounds Qual. rounds - 9.5min Final round - 14min (max)
Format: Tournament (8 teams) Qual. rounds - 3v3v3v3 Final round - 3v3
Earn cash: Vault open / deposit Steal / complete Cashout Eliminate opponents
Team wipe penalty: Qual. round - 27s respawn Final round - 25s respawn
Respawn credits: 2 credits at start +1 credit per round
Win: Win the final round
Progression: World Tour Win Points
Cashout is the premier Gamemode in THE FINALS. It's a casual tournament mode where contestants compete in an eight-team bracket consisting of two qualifying rounds with four teams each, followed by a final round where the remaining two teams face off.
The gamemode was in
```
</details>

`m05,?,?,`

---
### m06 (multi): Which heals faster, the Healing Beam or the Healing Emitter?

| Reference | Agent's answer |
|---|---|
| The Healing Beam: 50 HP/s in its stats box (its Effects section says 46 HP/s) vs 10-15 HP/s for the Healing Emitter. | The Healing Beam heals significantly faster than the Healing Emitter [Healing Beam § Stats > Effects] [Healing Emitter § Overview].  * **Healing Beam** (Medium specialization) heals at a rate of 46 to 50 health per second [Healing Beam § Stats > Effects] [Healing Beam § Overview]. * **Healing Emitter** (Heavy gadget) heals at a rate of 10 to 15 health per second [Healing Emitter § Overview]. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Healing Beam § Stats > Effects]
covers: Stats > Effects / Stats > Overheat / Stats > Properties > Gadget / Stats > Properties > Heal Beam (cite any of these sections of Healing Beam)
url: https://www.thefinals.wiki/wiki/Healing_Beam
The Healing Beam can be used by aiming it at another contestant on the user's team within its 13m range and sustaining fire on them. The teammate will be healed at a rate of 46 health per second. The Healing Beam will overheat after healing 253 HP without pause.

[Stats > Overheat]
When not overheated, pausing for 0.5 seconds will gradually restore total energy at a rate of 40 health points per second.
The Healing Beam has a maximum overheat time of 5.5 seconds. This means that if you continuously heal a teammate (who isn't at full health), the beam will overheat after 5.5 seconds of use, regardless of the healing rate.After overheating, it takes 7.5 seconds to be usable again.

[Stats > Properties > Gadget]
Targeted — Can be activated while targeting a teammate. The teammate needs to remain within line of sight to continue healing them.
Battery Charge — Uses up charge while used. Recharges over time. The Healing Beam can overheat if used to its limit, causing it to go on a cooldown.
Disarms User — Forces the user to stop using their other items for an extended time to be able to use the gadget effectively.
No Self Targeted — Cannot be used to heal the user.

[Stats > Properties > Heal Beam]
Support — Applies a positive effect to teammates.
Not Interceptible — Can not be removed by the APS Turret .
Not Damaging — Hitting a contestant directly with the projectile does not deal damage.

---

Result 2  cite as: [Healing Emitter § Overview]
url: https://www.thefinals.wiki/wiki/Healing_Emitter
Healing Emitter
“Deployable that heals you and nearby teammates. Can be picked up, carried and thrown.”
Profile
Build: H Heavy
Icon
Type: Utility
Unlock: Guardian
Stats
Cooldown: 30s
Ammo: 1
Technical
Radius: 4m
Health: 200
Healing: 10/s → 15/s (over 2s)
The Healing Emitter is a Heavy class placeable and carriable gadget that heals contestants and their teammates within small area around itself.

---

Result 3  cite as: [Healing Emitter § Stats > Properties > Emmiter]
url: https://www.thefinals.wiki/wiki/Healing_Emitter
Support — Provides healing to teammates around it.
Solid — Has its own collision, meaning it blocks bullets and contestants can stand on it.
Arming Time — After initiall deployment doesn't provide healing. Starts healing automatically after a wind-up time. Healing Emitter doesn't remain active when picked up and needs to go through wind-up process again after it is dropped.
Destructible — Can be destroyed if its health is fully depleted, such as through hits from bullets or explosions. Has a health bar and cannot take damage from the user's team.
Glitchable — Can be temporarily disabled by a Glitch Grenade or Glitch Barrel .
Reshapeable — Can be reshaped by the Data Reshaper into a another arena carriable by opponents.
Sound Cue — Remains silent while idling or healing, but produces sound during the wind-up and then goes silent, signaling that it's ready to heal contestants.
Permanent — Does not disappear by itself.
Damaging — Hitting an ememy contestant with the thrown emitter directly deals 50 damage.
Not Attached — Can be picked up and carried or thrown. Acts like any other carriable object .
No Structure Damage — Cannot be used to damage structures.
No Friendly Fire — Can damage neither the user nor their teammates.
Not Interceptible — Can not be removed by the APS Turret .

---

Result 4  cite as: [Healing Beam § Guide > Strengths]
covers: Guide > Strengths / Guide > Weaknesses (cite any of these sections of Healing Beam)
url: https://www.thefinals.wiki/wiki/Healing_Beam
- The more health the user's teammates have, the more effective the Healing Beam will be. A team with at least one Heavy provides a lot of value for the Healing Beam.
- The Healing Beam is effective while defending objectives in the open, such as the platform on Power Shift .

[Guide > Weaknesses]
- The wielder is defenseless while using the Healing Beam and cannot retaliate. A way of countering strategies that involve the Healing Beam is to focus the Healing Beam user.

---

Result 5  cite as: [Healing Beam § Overview]
covers: Overview / Usage / Usage > Charge-Based Cooldown (cite any of these sections of Healing Beam)
url: https://www.thefinals.wiki/wiki/Healing_Beam
HEALING BEAM
“A beam that gives health directly to another teammate”
Profile
Build: M Medium
Icon
Type: Specialization
Unlock: Free
Stats
Cooldown: Charge-Based Cooldown No overheating - 0.5s → 40 charge per second Overheating - 7.5s
Technical
Max Range: 10m 13m while healing
Duration: 5.5s
Health: 275 charge
Healing: 50 per second
The Healing Beam is a Medium class specialization that restores health over time for any teammate it is fired at.

[Usage]
The Healing Beam can be selected as the specialization gadget of any Me
```
</details>

`m06,?,?,`

---
### u01 (unanswerable): How much does the battle pass cost in Multibucks?

| Reference | Agent's answer |
|---|---|
| Not in the wiki snapshot: prices and the battle pass were not indexed. | The wiki does not cover this. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Cashout § Overview]
url: https://www.thefinals.wiki/wiki/Cashout
Cashout
Overview
Length: 1-3 Rounds Qual. rounds - 9.5min Final round - 14min (max)
Format: Tournament (8 teams) Qual. rounds - 3v3v3v3 Final round - 3v3
Earn cash: Vault open / deposit Steal / complete Cashout Eliminate opponents
Team wipe penalty: Qual. round - 27s respawn Final round - 25s respawn
Respawn credits: 2 credits at start +1 credit per round
Win: Win the final round
Progression: World Tour Win Points
Cashout is the premier Gamemode in THE FINALS. It's a casual tournament mode where contestants compete in an eight-team bracket consisting of two qualifying rounds with four teams each, followed by a final round where the remaining two teams face off.
The gamemode was introduced in Season 3 . Prior to Season 9 , the gamemode was referred as World Tour and was a prime mode for casual play where weekly events that altered gameplay through special rules or modifiers took place. Before that change, the name "Cashout" refereed to a group of gamemodes with similar set of rules.

---

Result 2  cite as: [Quick Cash § Overview]
url: https://www.thefinals.wiki/wiki/Quick_Cash
Quick Cash
“Single match rush to a cash goal”
Overview
Length: Single Round 18 min (max)
Format: 3 v 3 v 3
Earn cash: Complete Cashout
Team wipe penalty: 7s - 30s respawn
Respawn credits: Unlimited
Win: First to reach $20,000
Features: Unlimited respawn credits
Progression: World Tour Win Points
Quick Cash is a fast-paced Quickplay Gamemode designed for casual play. Three teams of three compete to be the first to reach $20,000 by depositing Cash Boxes from Vaults in Cashout Stations .

---

Result 3  cite as: [Cashout § Gameplay]
url: https://www.thefinals.wiki/wiki/Cashout
Cash Boxes are Carriable Objects that appear in the arena once a Vault has been opened. Contestants are tasked with transporting the valuable Cash Box to a Cashout Station to start a cashout, which is the only method for teams to extract the cash value.
Cash Boxes are central objectives in Cashout Gamemodes and serve as the primary means for teams to earn large amounts of cash. They originate exclusively from Vaults which must be opened before they can be accessed. Once released, teams must transport the Cash Box to a Cashout Station to initiate a cashout.
Cash Boxes are worth no monetary value to any team until they are inserted into a Cashout Station .
Once released from a Vault, Cash Boxes can be picked up, carried, dropped, or thrown by contestants.
Throw: PS R2; XBox RT; Key Primary fire
Drop: PS L2; XBox LT; Key Secondary fire
Carry: PC F; PS ◻; XBox X; Key Pick up
- In the knockout rounds Cash Boxes increase in value on every second spawn. During these rounds, inserting a Cash Box into a Cashout Station awards the team responsible with 20% of its initial value, with the remaining value granted to the team that successfully completes the cashout.
Cash Box 1 & 2: $10,000
Cash Box 3 & 4
Main page: Cashout Station
CASHOUT STATION
Type: Arena object
Effect: Accepts the Cash Box
Cashout time: Min. 1m Max. 2m10s
Steal time: 6s - 7s
SFX 1: Cashout in progress https://www.thefinals.wiki/wiki/File:Cashout.mp3

---

Result 4  cite as: [Cashout § Gameplay]
url: https://www.thefinals.wiki/wiki/Cashout
Teams earn cash by depositing Cash Boxes into Cashout Stations . Contestants must first locate an available Vault and open it, triggering a twenty second timer. When this timer expires, the Vault will eject a Cash Box which contestants can carry to a Cashout Station . Once picked up, Cash Boxes can be thrown, allowing contestants to defend themselves if attacked, pass the Cash Box to a teammate, or insert it from distance.
After a Cash Box is deposited into a Cashout Station , a timer will begin. The team must defend the active Cashout and prevent opponents from stealing it. All other contestants will be alerted to the active Cashout and may attempt to steal it. If the team successfully defends the station until the timer ends, the cash will be added to their total, and a new Vault will spawn in the arena.
Since Season 9 an anti-griefing mechanic known as Double Jeopardy was added to the gamemode. This system activates when a second Cash Box is inserted into an already active Cashout Station.

---

Result 5  cite as: [Fortune Stadium § Overview]
covers: Overview / Arena Variants > Standard Issue (cite any of these sections of Fortune Stadium)
url: https://www.thefinals.wiki/wiki/Fortune_Stadium
Fortune Stadium
Introduced: Season 4
Sponsor(s): HOLTOW , ENGIMO , ISEUL-T
Arena Variant(s): Standard Issue
Supported Gamemode(s): Cashout Quick Cash Ranked Cashout Team Deathmatch
Fortune Stadium was introduced with Season 4 and was the seventh arena to be added. The arena is comprised of sectors designated to the Season 4 sponsors: HOLTOW (sectors 1 and 3), ENGIMO (sector 2) and ISEUL-T (sectors 4, 5, and 6).

Map of Fortune Stadium Arena by Embark Studios
Fortune Stadium is a medium sized arena th
```
</details>

`u01,?,?,`

---
### u02 (unanswerable): Which team won The Grand Major 2025?

| Reference | Agent's answer |
|---|---|
| Not in the wiki snapshot: esports results were not indexed. | The wiki does not cover this. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Cashout § Overview]
url: https://www.thefinals.wiki/wiki/Cashout
Cashout
Overview
Length: 1-3 Rounds Qual. rounds - 9.5min Final round - 14min (max)
Format: Tournament (8 teams) Qual. rounds - 3v3v3v3 Final round - 3v3
Earn cash: Vault open / deposit Steal / complete Cashout Eliminate opponents
Team wipe penalty: Qual. round - 27s respawn Final round - 25s respawn
Respawn credits: 2 credits at start +1 credit per round
Win: Win the final round
Progression: World Tour Win Points
Cashout is the premier Gamemode in THE FINALS. It's a casual tournament mode where contestants compete in an eight-team bracket consisting of two qualifying rounds with four teams each, followed by a final round where the remaining two teams face off.
The gamemode was introduced in Season 3 . Prior to Season 9 , the gamemode was referred as World Tour and was a prime mode for casual play where weekly events that altered gameplay through special rules or modifiers took place. Before that change, the name "Cashout" refereed to a group of gamemodes with similar set of rules.

---

Result 2  cite as: [Las Vegas Stadium § Overview]
covers: Overview / Arena Variants > Standard Issue / Arena Variants > Sandstorm (cite any of these sections of Las Vegas Stadium)
url: https://www.thefinals.wiki/wiki/Las_Vegas_Stadium
This article is a Stub . It needs some work! You can help us out by expanding it .
Information in this article is outdated . It no longer reflects the latest state of THE FINALS. You can help us out by updating it . Reason: Arena was reworked with the release of PRIME TIME season
Las Vegas Stadium
Introduced: Season 6
Sponsor(s): ALFA ACTA , OSPUZE , ENGIMO
Arena Variant(s): Sandstorm Standard Issue
Supported Gamemode(s): Cashout Point Break Power Shift Quick Cash Ranked Cashout Team Deathmatch
Las Vegas Stadium was introduced with Season 6 and was the ninth arena to be added. It is a reworked version of Las Vegas that transforms the original into a championship stadium, with a focus on improved movement, cleaner sightlines, and smoother combat flow. Season 6 sponsors OSPUZE , ALFA ACTA , and ENGIMO took over the casinos and branded them to fit their own architectural aesthetics.

Map of Las Vegas Stadium Arena.
Las Vegas is a moderately sized arena with open streets and building roofs that are dangerously open to traverse and tight insides of the buildings that offer a lot of cover.

[Arena Variants > Standard Issue]
“A standard arena, ready for destruction.”

[Arena Variants > Sandstorm]
“Don’t get lost in stinging sands! Seek shelter and glory in this Las Vegas map variant.”
Swirling sand clouds drastically reduce visibility.

---

Result 3  cite as: [Ranked Cashout § Overview]
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
Ranked Cashout
“Pinnacle of competitive gameplay”
Overview
Length: 1-3 Rounds Qual. rounds - 9.5 min Final round - 14min (max)
Format: Tournament (8 teams) Qual. rounds - 3v3v3v3 Final round - 3v3
Earn cash: Vault open / deposit Steal / complete Cashout Eliminate opponents
Team wipe penalty: Qual. round - 27s respawn & 15% of team's total cash Final round - 25s respawn
Respawn credits: 2 credits at start +1 credit per round
Win: Win the final round
Progression: Ranked Score World Tour Win Points
See also: Ranked Leagues
Ranked Cashout is the primary competitive mode of THE FINALS, where contestants play Cashout tournaments to earn Rank Score (RS) and climb through the Leagues . Matches follow eight-team tournament structure, with two qualifying rounds of four teams and a final round between the remaining two teams.

---

Result 4  cite as: [Ranked Cashout § Rules > Tournament Structure]
covers: Rules > Tournament Structure / Rules > Ways to Gain Cash (cite any of these sections of Ranked Cashout)
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
The Tournament features 8 teams (24 contestants total) competing in a knockout bracket. The top 2 teams qualify for the next round, while the bottom 2 teams are eliminated.
- Knockout Round 1: 8 teams split into two matches (4 teams per match).
- Knockout Round 2: 4 remaining teams compete in one match.
- Final Round: The last 2 teams face off under rules similar to Head2Head , with Vaults worth $25,000. The first team to reach $50,000 wins the tournament.

[Rules > Ways to Gain Cash]
- $500 – Eliminating a contestant.
- $1,000 – Opening a Vault.
- $1,000 – Stealing an active Cashout Station .
- $2,000 – Depositing Cash Boxes from Vaults 1 & 2
- $3,000 – Depositing Cash Boxes from Vaults 3 & 4
- $4,000 – Depositing Cash Boxes from Vaults 5 & 6
- All Cash in the Cashout Station – Completing a Deposit

---

Result 5  cite as: [Ranked Cashout § Gameplay]
covers: Gameplay / Rules (cite any of these sections of Ranked Cashout)
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
When a Cash Box comes into contact with one of the sliding panels on a Cashout Station, it's automatically absorbed and a cashout will begin. Contestants can either carr
```
</details>

`u02,?,?,`

---
### u03 (unanswerable): What PC graphics settings give the best FPS in THE FINALS?

| Reference | Agent's answer |
|---|---|
| Not in the wiki snapshot: no graphics-settings pages were indexed. | The wiki does not cover this. The community wiki focuses on weapons, gadgets, specializations, builds, and game modes rather than PC graphics optimization or hardware settings. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [FCAR § Stats > Properties > Bullet]
covers: Stats > Properties > Bullet / Guide > Strengths / Guide > Weaknesses / Guide > Tactics / Guide > Recoil (cite any of these sections of FCAR)
url: https://www.thefinals.wiki/wiki/FCAR
Hitscan — Travels in a straight line, meaning there is no bullet drop. The direction will deviate from the crosshairs depending on accuracy.
Critical Hit — Critically hits on headshots, applying a damage multiplier.
High Range Falloff — Deals reduced damage when hitting targets at long distances (falloff starts beyond 30m).
Minor Structure Damage — Damages structures. Takes a very long time to break a concrete wall.

[Guide > Strengths]
- The FCAR has a higher immediate damage output than the comparable AKM , though it has a smaller magazine size.

[Guide > Weaknesses]
- The FCAR's small magazine size means it often has moments of downtime.
- The FCAR's damage begins to fall off at moderate distances, and falls off severely at long distances. Additionally, due to bullet dispersion, it becomes more difficult to hit the target consistently.

[Guide > Tactics]
- Firing should always be done while aiming down sights, unless the target is extremely close. Doing so greatly increases the accuracy of the FCAR.

[Guide > Recoil]
How to control:
- Pull straight down on the first four bullets
- After the 4th bullet, pull hard down and to the left
- After the 7th bullet, pull straight down again
- Pull down and left slightly during the 11th to 19th bullet
- Pull down slightly until the mag is empty

---

Result 2  cite as: [Builds § Light Build]
url: https://www.thefinals.wiki/wiki/Builds
“Exceptionally fast, but low survivability. Executes hit-and-run tactics. Specializes in stealth and evasion.”
The Light Build is the smallest, fastest, and most mobile of the three builds, excelling in swift repositioning and flanking manoeuvrers. However, this agility comes at a cost: Light has the lowest health, making direct combat risky.
Lights wield a versatile arsenal, including close-range weapons with a high firing rate like the XP-54 and M11 , as well as potent long-range options like the LH1 and SR-84 . They also carry melee weapons that are devastating in the right hands, with the Dagger having the capability of eliminating a contestant with a single backstab and the Sword possessing a lunge attack that can close distances between targets. Lights also possess more unconventional low-tech options such as the Recurve Bow and Throwing Knives for contestants who prefer projectile options over hitscan.
Additionally, Light contestants can be seen with unique gadget options, like the Breach Charge to create new openings in surfaces and the Glitch Grenade to turn fights in their favor.
With only 175 HP , Light Builds rely on speed, smart positioning, and quick disengages. However, they also have the fastest health regeneration, activating after 8 seconds of avoiding damage.

---

Result 3  cite as: [R .357 § Overview]
covers: Overview / Usage (cite any of these sections of R .357)
url: https://www.thefinals.wiki/wiki/R_.357
R .357
Weapon Quote: “High-power revolver”
Profile
Build: M Medium
Icon
Type: Handgun
Unlock: Free
Damage
Body: 76
Head: 152 (2.0×)
Environmental: 25
Damage Falloff
Min Range: 27.5m
Max Range: 44m
Multiplier: 0.4
Technical
RPM: 140
Magazine: 6
Empty Reload: 2.50s
Tactical Reload: 2.20s
The R .357 (Taurus Raging Bull R evolver . 357 Magnum) is a Medium class revolver designed to deal high damage per shot and very high headshot damage at close to moderate distances.

[Usage]
The R .357 can be selected as the weapon of any Medium build loadout.
The trigger can be pulled to fire one bullet that damages an opponent, also dealing additional damage on headshots. The trigger must be released before firing again. Aiming down sights increases the R .357's accuracy. Moving decreases accuracy, especially when going airborne.
The weapon automatically reloads when its magazine is empty, or the user can do a tactical reload before this point. The user has unlimited spare ammunition.
Equip R .357: PC 1; PS △; XBox Y; Key Weapon
Fire shot (Tap): PS R2; XBox RT; Key Primary fire
Aim down sights (Hold): PS L2; XBox LT; Key Secondary fire
Tactical reload: PC R; PS ◻; XBox X; Key Reload

---

Result 4  cite as: [Flashbang § Overview]
covers: Overview / Usage (cite any of these sections of Flashbang)
url: https://www.thefinals.wiki/wiki/Flashbang
FLASHBANG
“Thrown projectile that disorients, blinds and deafens nearby players; can be thrown underhand or overhand”
Profile
Build: L M H All
Icon
Type: Offensive
Unlock: Free
Stats
Cooldown: 18s
Ammo: 2
Technical
Duration: Minimum 2s Maximum 5s
The Flashbang is a Light , Medium and Heavy class thrown gadget that creates a flash which temporarily blinds and deafens onlooking contestants.

[Usage]
The Flashbang can be selected as one of three gadgets of any Light , Medium or Heavy build loadout.
Holding the primary trigger will prepare a high-veloc
```
</details>

`u03,?,?,`

---
### u04 (unanswerable): In Point Break, what does the attacking team have to do to win?

| Reference | Agent's answer |
|---|---|
| Not in the indexed snapshot (the Point Break page is held out). After adding it: destroy all 9 Grand Vaults, 3 per phase over 3 phases. | The wiki does not cover this. (There are no game modes named "Point Break" in the current wiki snapshot; modes include Cashout, Ranked Cashout, Power Shift, and Team Deathmatch.) |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Power Shift § Win Conditions]
covers: Win Conditions / Overtime Rules / Arenas (cite any of these sections of Power Shift)
url: https://www.thefinals.wiki/wiki/Power_Shift
- Primary Victory : A team wins by successfully escorting the platform into the opposing team's goal area.
- Time Expiry : If the timer expires before either goal is reached, the team that has pushed the platform furthest wins. If the platform is currently being contested, overtime begins instead.

[Overtime Rules]
- Trigger and Duration : Overtime is triggered if time expires while the platform is being contested, and lasts for a maximum of 5 minutes.
- Victory in Overtime : The team currently controlling the platform must escort it fully onto the opposing team’s side of the arena. The platform must not be contested when it reaches the end zone.
- Stalemate : If the platform has never been controlled by either team during the match, and overtime ends without a winner, the game will randomly assign victory to one of the teams.

[Arenas]
Bernal: Standard Issue • Suspended Structures
Kyoto: Standard Issue • Suspended Structures
Las Vegas Stadium: Standard Issue
Monaco: Standard Issue
NOZOMI/CITADEL: Standard Issue
Seoul: Standard Issue
Skyway Stadium: Standard Issue
SYS$HORIZON: Standard Issue

---

Result 2  cite as: [Power Shift § Overview]
covers: Overview / Objective (cite any of these sections of Power Shift)
url: https://www.thefinals.wiki/wiki/Power_Shift
Power Shift
“A casual 5v5 game mode where two teams compete to escort a platform through the arena.”
Overview
Short description: Hold the platform
Length: Single match
Format: 5v5
Features: Unlimited respawn credits
Progression: World Tour
Capture Platform Eliminate opponents or force them out of the platform to take control
Defend Platform Fend off enemy attacks and keep your team alive
Advance Platform Have up to 3 teammates on the platform to move at max speed
Power Shift is a 5v5 Quickplay gamemode in which two teams compete to escort a massive, moving platform through the arena. Teams fight for control of the platform as it advances along a fixed route, with momentum shifting as players engage, regroup, and contest key positions.

[Objective]
The objective of Power Shift is to escort the central platform into the opposing team’s goal area. Teams gain control of the platform by positioning contestants on it while preventing the enemy team from doing the same.
The distance the platform has traveled is represented by the money value displayed on the scoreboard, up to a maximum of $40,000 when the platform reaches the finish.

---

Result 3  cite as: [Cashout § Gameplay]
covers: Gameplay / Rules (cite any of these sections of Cashout)
url: https://www.thefinals.wiki/wiki/Cashout
When a Cash Box comes into contact with one of the sliding panels on a Cashout Station, it's automatically absorbed and a cashout will begin. Contestants can either carry the Cash Box directly to the station or throw it in from a distance. The last team to hold the Cash Box before it is absorbed becomes the initial owner of the cashout.
Once the cashout is completed, the team that currently controls the Cashout Station is awarded the full value of the Cash Box .
While a cashout is active, it is owned by a single team. If that team remains the owner when the cashout completes, they are awarded the full cash value. Contestants from opposing teams can attempt to steal the cashout by interacting with the Cashout Station for a short duration.
Steal Cashout (Hold): PC E; PS △; XBox Y; Key Interact
Cashout durations are fixed, provided there is sufficient time remaining in the round. If there is not enough time left to complete a full cashout, up to one minute of overtime is added to allow it to finish.
- Cashout Duration in knockout rounds - 2:10
- Cashout Duration in the final round - 2:00

[Rules]
Classic Cashout Open Vaults, deposit Cash Boxes, and defend or steal Cashout Stations
Two Qualifier Rounds Finish as one of the 2 teams with the most cash to qualify for the next round
Final Round The two teams that reach the final round compete to be the tournament winner

---

Result 4  cite as: [Team Deathmatch § Contestants and Respawns]
covers: Contestants and Respawns / Win Conditions / Arenas (cite any of these sections of Team Deathmatch)
url: https://www.thefinals.wiki/wiki/Team_Deathmatch
- Loadouts : Players can switch contestants and equipment between respawns.
- Quick Respawns : Respawns are available only 5 seconds after a contestant is eliminated
- Unlimited Coins : The number of respawns per contestant is unlimited.

[Win Conditions]
- Round Win : Reach $3,000 first or Have the most money when the 5-minute timer expires.
- Match Win : Win 2 out of 3 rounds

[Arenas]
Bernal: Standard Issue
Fangwai City: Standard Issue
Fortune Stadium: Standard Issue
Galaxy Estates: Standard Issue
Kyoto: Suspended Structures
Las Vegas Stadium: Standard Issue
Monaco: Standard Issue
NOZOMI/CITADEL: Stan
```
</details>

`u04,?,?,`

---
### u05 (unanswerable): What are the minimum PC system requirements to run THE FINALS?

| Reference | Agent's answer |
|---|---|
| Not in the wiki snapshot. | The wiki does not cover this. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [M134 Minigun § Overview]
url: https://www.thefinals.wiki/wiki/M134_Minigun
M134 Minigun
Weapon Quote: “A heavily modified minigun with relentless firepower, perfect for sustained suppression.”
Profile
Build: H Heavy
Icon
Type: HMG
Unlock: Demolisher
Damage
Body: 11
Head: 14.63 (1.33×)
Environmental: 35
Damage Falloff
Min Range: 30m
Max Range: 50m
Multiplier: 0.40
Technical
RPM: 1500
Magazine: 300
Empty Reload: 5.25s
Tactical Reload: 5.00s
The M134 Minigun is a high-capacity weapon, classified as a heavy machine gun , available to the Heavy build. It is best suited for sustained suppression, structural destruction, and area denial within a close range of threat.

---

Result 2  cite as: [M134 Minigun § Usage]
url: https://www.thefinals.wiki/wiki/M134_Minigun
The M134 Minigun can be selected as the weapon for any Heavy build loadout.
The weapon must be spun up before it can be fired, which can be performed by holding Primary Fire . Alternatively, the user can hold Secondary Fire to begin spinning up the weapon early without firing. Once the weapon is sufficiently spun up, the trigger can be held to continuously fire bullets that damage opponents and deal additional damage on headshots.
Aiming down sights is unavailable, but holding Secondary Fire to manually spin up the weapon will zoom the camera slightly and improve hipfire accuracy. Due to its weight, users experience drastically reduced mobility while spinning or firing the weapon. Like all the weapons in THE FINALS, M134 Minigun has infinite spare ammunition.
Equip M134 Minigun: PC 1; PS △; XBox Y; Key Weapon
Fire shot (Tap) Continuous fire (Hold): PS R2; XBox RT; Key Primary fire
Spin up (Hold): PS L2; XBox LT; Key Secondary fire
Tactical reload: PC R; PS ◻; XBox X; Key Reload

---

Result 3  cite as: [SYS$HORIZON § Overview]
covers: Overview / Arena Variants > Standard Issue / Locations / Supported Gamemodes / Supported Gamemodes > Limited Time Modes (cite any of these sections of SYS$HORIZON)
url: https://www.thefinals.wiki/wiki/SYS$HORIZON
SYS$HORIZON
Introduced: Season 2
Sponsor(s): CNS
Arena Variant(s): Standard Issue
Supported Gamemode(s): Cashout Cashout (Bots) Point Break Power Shift Quick Cash Ranked Cashout Team Deathmatch
SYS$HORIZON , or simply Horizon was added at the launch of Season 2 and was the fifth Arena to be introduced. The arena enviroment is a glitchy, colorful cityscape glowing under a neon sun. It is only partially loaded and filled with floating geometric shapes, due to it being introduced by hacking collective CNS . Much of Horizon is tall buildings connected by zip lines, providing high ground attack points.

SYS$HORIZON is a medium sized arena with many multi-story buildings, that offer both tight and open spaces to fight in, and very open outdoor areas around them. Arena rewards ability to traverse the open environments and finding different angles to hit your opponents from. It features a single Standard Issue variant with several weather or time modifiers.
Map of SYS$HORIZON Arena by Embark Studios

[Arena Variants > Standard Issue]
A standard arena, ready for destruction.

[Locations]
This article is a Stub . It needs some work! You can help us out by expanding it .
Work Space: ***
Library: ***
Art Gallery: ***
Museum: ***
Campus: ***

[Supported Gamemodes]
SYS$HORIZON supports the following Gamemodes :
- Cashout
- Cashout (Bots)
- Point Break
- Power Shift
- Quick Cash
- Ranked Cashout
- Team Deathmatch

[Supported Gamemodes > Limited Time Modes]
- Bank It
- Head2Head

---

Result 4  cite as: [Builds § Light Build]
url: https://www.thefinals.wiki/wiki/Builds
“Exceptionally fast, but low survivability. Executes hit-and-run tactics. Specializes in stealth and evasion.”
The Light Build is the smallest, fastest, and most mobile of the three builds, excelling in swift repositioning and flanking manoeuvrers. However, this agility comes at a cost: Light has the lowest health, making direct combat risky.
Lights wield a versatile arsenal, including close-range weapons with a high firing rate like the XP-54 and M11 , as well as potent long-range options like the LH1 and SR-84 . They also carry melee weapons that are devastating in the right hands, with the Dagger having the capability of eliminating a contestant with a single backstab and the Sword possessing a lunge attack that can close distances between targets. Lights also possess more unconventional low-tech options such as the Recurve Bow and Throwing Knives for contestants who prefer projectile options over hitscan.
Additionally, Light contestants can be seen with unique gadget options, like the Breach Charge to create new openings in surfaces and the Glitch Grenade to turn fights in their favor.
With only 175 HP , Light Builds rely on speed, smart positioning, and quick disengages. However, they also have the fastest health regeneration, activating after 8 seconds of avoiding damage.

---

Result 5  cite as: [Recurve Bow § Usage]
covers: Usage / Stats 
```
</details>

`u05,?,?,`

---
### u06 (unanswerable): How much damage does the Plasma Cutter deal to Heavy contestants?

| Reference | Agent's answer |
|---|---|
| There is no Plasma Cutter in the wiki snapshot; the agent should not invent one. | The wiki does not cover this. There is no item named "Plasma Cutter" in THE FINALS Community Wiki. |

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Sledgehammer § Stats > Damage Profile]
url: https://www.thefinals.wiki/wiki/Sledgehammer
Precise (Alt-Fire): Light (175 HP) Hits to kill 1; Light (175 HP) Time to kill (s) 1.05; Medium (250 HP) Hits to kill 2; Medium (250 HP) Time to kill (s) 2.46; Heavy (325 HP) Hits to kill 2; Heavy (325 HP) Time to kill (s) 2.46
Glancing (Alt-Fire): Light (175 HP) Hits to kill 2; Light (175 HP) Time to kill (s) 2.46; Medium (250 HP) Hits to kill 2; Medium (250 HP) Time to kill (s) 2.46; Heavy (325 HP) Hits to kill 3; Heavy (325 HP) Time to kill (s) 3.87
Precise: Light (175 HP) Hits to kill 2; Light (175 HP) Time to kill (s) 1.39; Medium (250 HP) Hits to kill 3; Medium (250 HP) Time to kill (s) 2.26; Heavy (325 HP) Hits to kill 3; Heavy (325 HP) Time to kill (s) 2.26
Glancing: Light (175 HP) Hits to kill 2; Light (175 HP) Time to kill (s) 1.39; Medium (250 HP) Hits to kill 3; Medium (250 HP) Time to kill (s) 2.26; Heavy (325 HP) Hits to kill 4; Heavy (325 HP) Time to kill (s) 3.10
Values are approximate and determined by community testing ( 12.0.0 ).

---

Result 2  cite as: [Flamethrower § Stats > Damage Profile]
covers: Stats > Damage Profile / Stats > Properties > Weapon / Stats > Properties > Flames (cite any of these sections of Flamethrower)
url: https://www.thefinals.wiki/wiki/Flamethrower
Splash: Light (175 HP) Ammo to kill 6; Light (175 HP) Time to kill (s) 1.77; Medium (250 HP) Ammo to kill 9; Medium (250 HP) Time to kill (s) 2.82; Heavy (325 HP) Ammo to kill 11; Heavy (325 HP) Time to kill (s) 3.53
Values are approximate and determined by community testing ( 12.3.0 ).

[Stats > Properties > Weapon]
Ranged — Strikes targets by aiming and firing at them from a distance.
Automatic Fire — Continues to fire automatically until the trigger is released.
Stable Accuracy — Keeps a stable accuracy, even while moving and going airborne.
Full Reload — Replaces the entire magazine in one animation on reload.
No Aiming Down Sights — Cannot use sights. Zooms in slightly instead, but doing so does not significantly affect accuracy.

[Stats > Properties > Flames]
Projectile — Gets affected by gravity and has a travel time.
Incendiary — Creates fire, which can spread to nearby goo and foliage and burn them down. It can also light up contestants.
No Critical Hit — Does not critically hit for increased damage, even if the target was struck on the head.
Not Interceptible — Can not be removed by the APS Turret .
No Structure Damage — Cannot be used to damage structures.

---

Result 3  cite as: [Throwing Knives § Stats > Damage Profile]
url: https://www.thefinals.wiki/wiki/Throwing_Knives
Head (Alt-Fire): Light (175 HP) Shots to kill 1; Light (175 HP) Time to kill (s) 0.000; Medium (250 HP) Shots to kill 2; Medium (250 HP) Time to kill (s) 2.166; Heavy (325 HP) Shots to kill 2; Heavy (325 HP) Time to kill (s) 2.166
Body (Alt-Fire): Light (175 HP) Shots to kill 2; Light (175 HP) Time to kill (s) 2.166; Medium (250 HP) Shots to kill 2; Medium (250 HP) Time to kill (s) 2.166; Heavy (325 HP) Shots to kill 3; Heavy (325 HP) Time to kill (s) 4.332
Head: Light (175 HP) Shots to kill 2; Light (175 HP) Time to kill (s) 0.110; Medium (250 HP) Shots to kill 3; Medium (250 HP) Time to kill (s) 0.784; Heavy (325 HP) Shots to kill 4; Heavy (325 HP) Time to kill (s) 0.894
Body: Light (175 HP) Shots to kill 3; Light (175 HP) Time to kill (s) 0.784; Medium (250 HP) Shots to kill 5; Medium (250 HP) Time to kill (s) 1.568; Heavy (325 HP) Shots to kill 6; Heavy (325 HP) Time to kill (s) 1.678
Values are approximate and determined by community testing ( 12.0.0 ).
Note: A Light can be killed by 1 headshot and 1 body (60+90) and a quick melee for easier close quarter brawling

---

Result 4  cite as: [Dual Blades § Stats > Damage Profile]
url: https://www.thefinals.wiki/wiki/Dual_Blades
Precise (Alt-Fire): Light (175 HP) Hits to kill 2; Light (175 HP) Time to kill (s) 1.75; Medium (250 HP) Hits to kill 2; Medium (250 HP) Time to kill (s) 1.75; Heavy (325 HP) Hits to kill 3; Heavy (325 HP) Time to kill (s) 2.75
Glancing (Alt-Fire): Light (175 HP) Hits to kill 2; Light (175 HP) Time to kill (s) 1.75; Medium (250 HP) Hits to kill 3; Medium (250 HP) Time to kill (s) 2.75; Heavy (325 HP) Hits to kill 4; Heavy (325 HP) Time to kill (s) 3.75
Precise: Light (175 HP) Hits to kill 3; Light (175 HP) Time to kill (s) 1.29; Medium (250 HP) Hits to kill 5; Medium (250 HP) Time to kill (s) 2.11; Heavy (325 HP) Hits to kill 6; Heavy (325 HP) Time to kill (s) 2.37
Glancing: Light (175 HP) Hits to kill 5; Light (175 HP) Time to kill (s) 2.11; Medium (250 HP) Hits to kill 7; Medium (250 HP) Time to kill (s) 2.93; Heavy (325 HP) Hits to kill 9; Heavy (325 HP) Time to kill (s) 3.75
Values are approximate and determined by community testing ( 12.0.0 ).

---

Result 5  cite as: [Builds § Heavy Build]
url: https://www.thefinals.wiki/wiki/Builds
“High survivability. Low movement speed. Specializes in demolition and fortifications.”
The Heavy Build is a powerho
```
</details>

`u06,?,?,`
