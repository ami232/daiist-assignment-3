# Answers to grade

For each, write a row in `eval/human_labels.csv`: `id,correct,supported,notes` (1 or 0). Grade before looking at the judge's verdict in results.csv.
- **correct**: matches the reference answer (for unanswerable: refuses without inventing).
- **supported**: every claim is in the retrieved passages below.

---

## q01 (single)

**Question:** What is the cooldown of the Breach Charge, and how many charges does it have?

**Reference:** 20 seconds cooldown and 3 charges (ammo 3); it is a Light gadget.

**Agent answer:**

The Light build's Breach Charge has a cooldown of **20s** and an ammo capacity of **3** charges [Breach Charge § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Breach Charge § Stats > Effects]
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

Result 2  cite as: [Breach Charge § Overview]
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

Result 3  cite as: [Breach Charge § Stats > Properties > Charge]
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

Result 4  cite as: [Breach Drill § Overview]
covers: Overview / Usage / Usage > Properties > Gadget (cite any of these sections of Breach Drill)
url: https://www.thefinals.wiki/wiki/Breach_Drill
Breach Drill
“Deployable that drills through surfaces and flashes the other side before detonating.”
Profile
Build: M Medium
Icon
Type: Utility
Unlock: 500
Stats
Cooldown: 15s
Ammo: 1
Technical
Environment Dmg: Over 2000
The Breach Drill is a Medium class gadget that can be attached to a surface to flash the other side before detonating to breach it.

[Usage]
The Breach Drill can be selected as one of three Gadgets of any Medium build loadout.
Once attached to a surface, the Breach Drill will begin drilling through. When completed, a flash will blind opponents on the other side, followed by an explosion that destroys the targeted surface.
Fully blinding an opponent will display a yellow X on the crooshair, while partially blinding displays a white one.
Breach drill can be placed on top of Goo . The explosion breaks a single goo piece, but the flash doesn't blind any opponents.
Equip Breach Drill: PC 2 3 4; PS L1; XBox LB; Key Gadget
Place: PS R2; XBox RT
```
</details>

---

## q02 (single)

**Question:** How many SR-84 headshots does it take to eliminate a Heavy contestant?

**Reference:** 2 headshots (time to kill about 1.333 s); a Heavy has 325 HP and a headshot deals 244.

**Agent answer:**

It takes 2 headshots (or alternatively, 1 headshot and 1 body shot) to eliminate a Heavy contestant with the SR-84 [SR-84 § Stats > Damage Profile] [SR-84 § Guide > Strengths].

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
- The SR-84 is weak at close distances, due to its very high bullet dispersion when hipfiring, and difficulty scoping in on a close target.
- The SR-84 loses some of its damage at the absolute longest distances, meaning that hitting a target from across the arena is slightly less effective.
- The SR-84 does not have enough damage output to effectively break shields. Doing so also wastes a large part of the ammunition. However, it can be helpful to shoot the dome shield if your team is doing so as well. The SR-84, dealing 118 damage, takes off almost half of the dome shields HP of 250. That one shot can drastically reduce the time needed to shoot through a dome shield if done so in timing with your teammates attacks.
- It is not recommended to run cloak with this weapon, as the scope glint is still visible even while cloaked.
```
</details>

---

## q03 (single)

**Question:** How long does a surface stay dematerialized by the Dematerializer, and which build can use it?

**Reference:** 15 seconds; it is a Medium specialization.

**Agent answer:**

A surface stays dematerialized for **15 seconds** before it automatically rematerializes, though it can also be manually rematerialized sooner by toggling it [Dematerializer § Overview] [Dematerializer § Stats > Properties > Gadget]. 

The Dematerializer can be used by the **Medium** build [Dematerializer § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Dematerializer § Overview]
covers: Overview / Usage / Stats > Effects (cite any of these sections of Dematerializer)
url: https://www.thefinals.wiki/wiki/Dematerializer
DEMATERIALIZER
“A tool that temporarily dematerializes physical surfaces in the arena, allowing any contestant to see or pass through them. It can also make these surfaces rematerialize.”
Profile
Build: M Medium
Icon
Type: Specialization
Unlock: Hacker
Stats
Cooldown: 15s
Ammo: 3
Technical
Duration: 15s
The Dematerializer is a Medium class specialization that temporarily removes surfaces, allowing contestants to move and attack through them.

[Usage]
The Dematerializer can be selected as the specialization gadget of any Medium build loadout.
While the gadget is held, looking at a surface will show an indicator of a potential dematerialization as a blue hologram covering a part of the surface. The primary trigger can be used to activate the gadget and dematerialize the surface.
If a surface was already dematerialized by any contestant, the indicator will be red instead, and the secondary trigger can be used to rematerialize the surface.
Equip Dematerializer: PC Q; PS R1; XBox RB; Key Specialization
Dematerialize surface (Tap): PS R2; XBox RT; Key Primary fire
Rematerialize surface (Tap): PS L2; XBox LT; Key Secondary fire

[Stats > Effects]
The Dematerializer can be deployed by activating it on a targeted surface. This will cause the surface to turn into its dematerialized version. Contestants, attacks and other objects can look and phase through the wall freely. The Dematerializer will remove props attached to wall segments.
After a while, the surface rematerializes automatically, or it can be rematerialized manually.

---

Result 2  cite as: [Dematerializer § Stats > Properties > Gadget]
covers: Stats > Properties > Gadget / Stats > Properties > Dematerialized Surface / Guide > Strengths (cite any of these sections of Dematerializer)
url: https://www.thefinals.wiki/wiki/Dematerializer
Targeted — Can be activated while targeting a structure piece or solid object.
Toggle — Can be enabled and disabled by reactivating. Specifically, a dematerialized surface will rematerialize if it is reactivated.
Multiple Charges — Can be used 2 times. When a charge is used, it automatically recharges over the cooldown time.
No Deployment Limit — Any number of walls can be dematerialized at a time.

[Stats > Properties > Dematerialized Surface]
Attached — Attached to a structure piece or solid object.
Sound Cue — Produces a sound to alert nearby contestants when used. A dematerialized surface also hums softly.
Usable by Opponents — Can be used by opponents to their advantage. Opponents can see, shoot and move through the gaps.
Not Permanent — Disappears by itself after enough time has passed.
Not Damaging — Does not inflict damage.
No Structure Damage — Instantly removes a surface of any structure. However, this does not affect the structural integrity of the surrounding structure, and the removal is reversed after some time, or upon reactivation.

[Guide > Strengths]
- The Dematerializer can be used to create unexpected angles and opportunities while also being able to close the hole to deny opponents the possibility of retaliation.

---

Result 3  cite as: [Dematerializer § Guide > Weaknesses]
url: https://www.thefinals.wiki/wiki/Dematerializer
- If the surfaces around an objective are already breached in several places such as by Explosive Canisters , a Dematerializer user will not get as much benefit from the gadget, as opponents can easily follow them.
- It can be difficult to see well through a dematerialized surface to fire through it, due to the glitchy animation overlay, especially if opponents are far away from the surface.
- When the user is playing in an uncoordinated team, the Dematerializer may only benefit its user, whereas the other Medium Specializations would also benefit the team. However, with proper communication, the Dematerializer can be used strategically by the entire team. Additionally, capturing objectives using the Dematerializer also benefits the team regardless.

---

Result 4  cite as: [Dematerializer § Guide > Tactics]
url: https://www.thefinals.wiki/wiki/Dematerializer
- It is possible to defend an objective from an adjacent room, besides or above the room the station is in, by opening a hole whenever the sound cue plays and taking down the opponent while they are attempting to steal.
- To escape from a sticky situation, the user can dematerialize the floor under them or a wall besides them and rematerialize immediately after going through. However, it should be noted that there can sometimes be additional obstacles in unpredictable locations that block the way through, such as a cabinet behind a wall or a pipeline on a ceiling which may require an additional dematerialization. This happens particularly often on Las Vegas and Horizon .
- The Dematerializer can be used to take the Cashout Station down a floor and immediately rematerialize the opened ceiling, allowing for a quick steal. Alternatively, if the station is placed against a wall, dematerializing a cell in the wall may allow for an unexpected steal from behind while the rest of the wall and the station itself provides cover for the stealer. These strategies also apply to encrypting or decrypting Terminal Attack 's terminal.

---

Result 5  cite as: [Specializations § Overview]
covers: Overview / Removed specializations (cite any of these sections of Specializations)
url: https://www.thefinals.wiki/wiki/Specializations
Specializations are abilities that are available in a contestant's Loadout , and each Build has different specializations available to them. This allows contestants to customize their Build to complement their preferred playstyle.
Specializations are themed around the Build that they belong to:
- Light Builds have specializations that allow for high mobility, flanking and awareness.
- Medium Builds have utility-base
```
</details>

---

## q04 (single)

**Question:** How much health does a Heavy teammate come back with after being revived by the Defibrillator?

**Reference:** 175 HP, half of the Heavy build's maximum; they also get brief invulnerability and 5 s of revive sickness.

**Agent answer:**

A Heavy teammate comes back with 175 health (half of their build's maximum HP) after being revived by the Defibrillator [Defibrillator § Stats > Effects].

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
- Using the Defibrillator as a weapon is highly impractical. Not only is it slower and deals slightly less damage than a melee attack, the Defibrillator's cooldown is incurred once it damages an enemy, effectively wasting it.

---

Result 5  cite as: [Healing Emitter § Overview]
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
```
</details>

---

## q05 (single)

**Question:** In which game modes can the Defibrillator not be equipped?

**Reference:** Terminal Attack and Team Deathmatch.

**Agent answer:**

The Defibrillator cannot be equipped in the Terminal Attack and Team Deathmatch game modes [Defibrillator § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Defibrillator § Overview]
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

Result 2  cite as: [Defibrillator § Guide > Tactics]
url: https://www.thefinals.wiki/wiki/Defibrillator
- It is the responsibility of the Defibrillator user to ensure that their teammate won't immediately die upon revival. Moving the teammate's Revive Statue away from enemies or providing cover with abilities such as Goo , the APS Turret , or the Guardian Turret can all but guarantee the odds of successful revives.
- The Defibrillator is best used for mid-fight Revives, such as if a teammate dies early into a fight.
- The Healing Beam makes an excellent pairing with the Defibrillator, as it can heal the revived contestant and make them battle-ready quicker.

---

Result 3  cite as: [Defibrillator § Stats > Effects]
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
- Using the Defibrillator as a weapon is highly impractical. Not only is it slower and deals slightly less damage than a melee attack, the Defibrillator's cooldown is incurred once it damages an enemy, effectively wasting it.

---

Result 5  cite as: [Skyway Stadium § Supported Gamemodes]
covers: Supported Gamemodes / Supported Gamemodes > Limited Time Modes (cite any of these sections of Skyway Stadium)
url: https://www.thefinals.wiki/wiki/Skyway_Stadium
Skyway Stadium supports the following Gamemodes :
- Cashout
- Power Shift
- Quick Cash
- Ranked Cashout
- Team Deathmatch

[Supported Gamemodes > Limited Time Modes]
- Bank It
- Head2Head
```
</details>

---

## q06 (single)

**Question:** What is the maximum range of the Grappling Hook?

**Reference:** 25 m (cooldown 4 s minimum, 7.5 s maximum).

**Agent answer:**

The maximum range of the Light build's Grappling Hook is **25m** [Grappling Hook § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Grappling Hook § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget / Stats > Properties > Projectile / Stats > Properties > Effect / Guide > Strengths (cite any of these sections of Grappling Hook)
url: https://www.thefinals.wiki/wiki/Grappling_Hook
The Grappling Hook can be activated to throw out a hook which, if it hits a surface, will drag the user towards it over time. During this time, the user can control their movements, It is also possible to use weapons and other items while flying.

[Stats > Properties > Gadget]
Ranged — Can be used by aiming and firing at a structure.
Stable Accuracy — Keeps a stable accuracy, even while moving and going airborne.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
No Disarm — Does not stop the user from using their other items while the gadget is active. The user can act while swinging.

[Stats > Properties > Projectile]
Projectile — Travels in a straight line with no bullet drop, but has travel time. The direction will deviate from the crosshairs depending on accuracy.
Trigger on Impact — Triggers when the hook hits a surface within effective range. The hook flies through contestants.
Not Interceptible — Can not be removed by the APS Turret .
Not Damaging — The projectile does not deal damage.

[Stats > Properties > Effect]
Movement — Provides a special mode of transport for contestants.

[Guide > Strengths]
- The user can still fire their weapon while grappling somewhere.
- When compared to the Evasive Dash , the Grappling hook offers more vertical movement.

---

Result 2  cite as: [Grappling Hook § Overview]
covers: Overview / Usage (cite any of these sections of Grappling Hook)
url: https://www.thefinals.wiki/wiki/Grappling_Hook
GRAPPLING HOOK
“A cord with a hook that you launch to scale structures and swing past walls. Also handy for quick escapes during combat”
Profile
Build: L Light
Icon
Type: Specialization
Unlock: Free
Stats
Cooldown: Minimum 4s Maximum 7.5s
Ammo: 1
Technical
Max Range: 25m
The Grappling Hook is a Light class specialization that allows its user to quickly move a long distance through the air by swinging from structures.

[Usage]
The Grappling Hook can be selected as the specialization gadget of any Light build loadout.
The primary trigger can be used to activate the gadget. If the hook hits a surface, the user will fly towards it. The movement triggers can be used to control this flight. Moving sideways will cause the user to sway to that side, whereas moving forwards or backwards will affect the height at which the user will be dropped off. The exact effects of each movement input depends on where the hook was placed relatively to its user. The user can also press the jump button to do a small midair hop off the grappling hook, or press the primary trigger again to end the grapple early without this hop.
Fire (Tap): PC Q; PS R1; XBox RB; Key Specialization

---

Result 3  cite as: [Winch Claw § Stats > Properties > Projectile]
covers: Stats > Properties > Projectile / Guide > Strengths / Guide > Weaknesses (cite any of these sections of Winch Claw)
url: https://www.thefinals.wiki/wiki/Winch_Claw
Projectile — Travels in a straight line without being affected by gravity.
Trigger on Impact — Applies its effects if an opponent or object is struck. Does not apply effects when hitting shields.
Damaging — The projectile deals damage if it hits a contestant.
Movement — Causes the affected opponent or object to move towards the user.
Immobilizing — Stops affected contestants from moving.
Not Interceptible — Can not be removed by the APS Turret .
No Structure Damage — Cannot be used to damage structures.
No Friendly Fire — Can not be used to grab teammates.

[Guide > Strengths]
- The Winch Claw can be used to grab objects from a distance that could not be reached otherwise.
- Some objects that cannot be grabbed normally, such as a cashout station , can be dragged with the Winch Claw.

[Guide > Weaknesses]
- If the target being pulled gets stuck on a wall, the pull will be cancelled after a second.
- The Winch Claw is blocked by shields, like the Mesh Shield and Dome Shield . It cannot latch onto opponents or targets behind these surfaces.
- Pulling in a melee weapon or shotgun user when the user is not using a melee weapon can lead to an unfavorable fight.

---

Result 4  cite as: [Grappling Hook § Guide > Weaknesses]
covers: Guide > Weaknesses / Guide > Tactics (cite any of these sections of Grappling Hook)
url: https://www.thefinals.wiki/wiki/Grappling_Hook
- The user is exposed while flying through the air and clearly visible to any onlookers.
- Compared to other Light Specializations , the Grappling Hook mostly offers out-of-combat value for transportation, whereas the other specializations offer mid-combat or stealth value. A Grappling Hook user should make sure to get the maximum value of their greatly enhanced out-of-combat movement, such as by bringing the Cash Box to the objective faster than anyone can follow them.

[Guide > Tactics]
- The Grappling Hook can be combined with a marksman weapon to travel from one high-up sniper position to the next.
- You can make a single high-speed combat escape if you don't use it to engage. It allows for some powerful curving around doorways, windows, and other obstacles, plus you can maintain speed afterwards with a slide.

---

Result 5  cite as: [Winch Claw § Overview]
covers: Overview / Usage / Stats > Effects / Stats > Properties > Gadget (cite any of these sections of Winch Claw)
url: https://www.thefinals.wiki/wiki/Winch_Claw
WINCH CLAW
“Launches a chain claw that latches on to objects or contestants, pulling them in closer to you”
Profile
Build: H Heavy
Icon
Type: Specialization
Unlock: Enforcer
Stats
Cooldown: Miss - 10s Low-value Target - 14s High-value Target - 18s
Technical
Damage: 5
Max Range: 12m
Duration: Stun: 3m or less - 0.1s Max range - 0.5s
The Winch Claw is a Heavy class specializatio
```
</details>

---

## q07 (single)

**Question:** Does using Evasive Dash interrupt drawing the Recurve Bow?

**Reference:** No. Evasive Dash does not interrupt drawing the Recurve Bow, a Sword lunge or scoping in with the SR-84.

**Agent answer:**

No, using Evasive Dash does not interrupt drawing the Recurve Bow [Evasive Dash § Stats > Effects]. It is possible to use Evasive Dash while the bow is drawn [Recurve Bow § Guide > Tactics].

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
Evasive Dash can be activated to dash a short distance, going in a direction based on the user's movement inputs and their looking direction. Uniquely, using this specialization does not interrupt actions such as drawing the Recurve Bow , holding a Sword lunge or scoping in with the SR-84 .
```
</details>

---

## q08 (single)

**Question:** Can True Sight reveal an opponent who is using the Cloaking Device?

**Reference:** Yes. Opponents are fully visible with True Sight even under the Cloaking Device or Vanishing Bomb; it also sees through smoke and dust.

**Agent answer:**

Yes, True Sight can reveal opponents who are using the Cloaking Device or Vanishing Bomb [True Sight § Stats > Effects]. Opponents under these cloaking effects are fully visible to the user when True Sight is active [True Sight § Stats > Effects].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [True Sight § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Specialization / Stats > Properties > Effect / Guide > Strengths (cite any of these sections of True Sight)
url: https://www.thefinals.wiki/wiki/True_Sight
True Sight can be activated to grant its user temporary increased clarity. Most of the screen will be a blue color, whereas significant objects are highlighted in their respective team colors. These objects include contestants, deployables, cash boxes , cashout stations and a few others.
It also allows its user to see past vision-obstructing objects, such as smoke clouds , but also general dust and debris caused by destruction and explosions, making for a clearer view of the area.
Opponents are fully visible even if they are under the effects of the Cloaking Device or Vanishing Bomb .

[Stats > Properties > Specialization]
Self Targeted — Can be activated to apply an effect to the contestant that used it.
Toggle — Can be enabled and disabled by reactivating.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
No Disarm — Does not stop the user from using their other items while the specialization is active.

[Stats > Properties > Effect]
Visibility — Affects the line of sight of the user and/or opponents. Changes the user's viewing mode to True Sight vision.
Not Permanent — Disappears by itself after enough time has passed.

[Guide > Strengths]
- True Sight is an effective counter to contestants using the Cloaking Device or Vanishing Bomb , as it reveals them to the True Sight user.
- In confined areas with lots of explosions, dust clouds and other vision-obstructing particles, True Sight often provides the most value.

---

Result 2  cite as: [True Sight § Overview]
covers: Overview / Usage (cite any of these sections of True Sight)
url: https://www.thefinals.wiki/wiki/True_Sight
This article is a Stub . It needs some work! You can help us out by expanding it .
This article is under construction . A work in progress is underway and article slowly being improved. Please bear with us while we make improvements.
TRUE SIGHT
“Reveals opponents through smoke and other visual obstructions, including cloaked and mimicked Contestants”
Profile
Build: L Light
Icon
Type: Utility
Unlock: Infiltrator
Stats
Cooldown: ???
Ammo: 25
Technical
Duration: ???
True Sight is a Light Build specialization that temporarily alters the user's vision, highlighting contestants and deployables in their team colors and allowing the user to see through smoke and dust.

[Usage]
True Sight can be selected as one of four specializations of any Light Build loadout.
The specialization key can be used to toggle True Sight on. It remains active for up to ?? seconds, after which it is automatically disabled to recharge. It can also be disabled early by toggling it again.
Toggle on (Tap) Toggle off (Tap): PC Q; PS R1; XBox RB; Key Specialization

---

Result 3  cite as: [True Sight § Guide > Weaknesses]
covers: Guide > Weaknesses / Guide > Tactics (cite any of these sections of True Sight)
url: https://www.thefinals.wiki/wiki/True_Sight
- True Sight cannot see gas , which can potentially cause the user to walk into a damaging area unintentionally.
- True Sight has limited range and will not highlight far-away opponents.
- Even if True Sight is highlighting an obscured enemy, they cannot be targeted by melee weapon lunges.

[Guide > Tactics]
- True Sight can be combined with the Smoke Grenade , as it is able to see through the smoke.

---

Result 4  cite as: [Cloaking Device § Stats > Energy-Based Cooldown]
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

Result 5  cite as: [Cloaking Device § Overview]
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
The specialization trigger can be used to toggle on the gadget. It will remain active for up to 12 seconds, after which it is automatically disabled to recharge. It can also be disabled before this point by toggling it again. Attacking or using an
```
</details>

---

## q09 (single)

**Question:** How far can a Guardian Turret detect opponents and how wide is its vision cone?

**Reference:** About 20 m, in a 150 degree vision cone; it arms after 3 seconds.

**Agent answer:**

The Guardian Turret has a limited detection range of about 20m [Guardian Turret § Stats > Effects] (with a Max Range of 20m) [Guardian Turret § Overview]. It scans a total vision cone of 150° while rotating left and right repeatedly [Guardian Turret § Stats > Effects].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Guardian Turret § Stats > Effects]
url: https://www.thefinals.wiki/wiki/Guardian_Turret
The Guardian Turret can be deployed by placing it down on any nearby surface. It arms itself over 3 seconds, after which it starts rotating left and right repeatedly, scanning a total vision cone of 150° (close to half of a circle). The middle of this vision cone is at the orientation of its placement. The vision of the turret has a limited range of about 20m.
Whenever an opponent enters the vision range of the Guardian Turret, it starts firing an unending stream of bullets at them and tracks their movements in the process. Additionally, if an opponent attacks the Guardian Turret, it will turn around to attack them even if they are outside of its vision cone.
The gadget can be damaged only by opponents. Picking up the gadget and placing it again is the only way to restore its health. When the gadget is picked up, a 3s cooldown begins before the turret can be placed again. The gadget has its own visible health bar. Uniquely, the next charge of the gadget will not begin charging until the previous turret is removed.

---

Result 2  cite as: [Guardian Turret § Overview]
url: https://www.thefinals.wiki/wiki/Guardian_Turret
GUARDIAN TURRET
“Deployable AI-controlled assault rifle”
Profile
Build: M Medium
Icon
Type: Specialization
Unlock: Engineer
Stats
Cooldown: Destroyed - 35s Picked up manually - 3s Picked up remotely - 10s
Technical
Damage: 6
Max Range: 20m
Health: 300
rpm: 400
The Guardian Turret is a Medium class specialization that places a turret which protects an area by rapidly firing at opponents it detects.

---

Result 3  cite as: [Guardian Turret § Guide > Weaknesses]
covers: Guide > Weaknesses / Guide > Tactics (cite any of these sections of Guardian Turret)
url: https://www.thefinals.wiki/wiki/Guardian_Turret
- The Guardian Turret can be disabled by a nearby Glitch Grenade or Glitch Barrel triggering, or reshaped by the Data Reshaper .
- The Guardian Turret can be stopped from detecting contestants by disrupting its direct line of sight. Deploying Goo , setting up Barricades , or using Smoke Grenades and Powder Canisters are effective ways to block its vision.

[Guide > Tactics]
- Placing the Guardian Turret on the ceiling is often a better idea than on the ground, as it won't be harmed by damage from sources such as the Frag Grenade , and melee weapon users will have a hard time dealing with it. Meanwhile, being on the ceiling has little downsides for the Guardian Turret.

---

Result 4  cite as: [Guardian Turret § Stats > Properties > Gadget]
covers: Stats > Properties > Gadget / Stats > Properties > Bullet (cite any of these sections of Guardian Turret)
url: https://www.thefinals.wiki/wiki/Guardian_Turret
Placeable — Can be placed attached to a surface. An indicator shows the exact target placement.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
Retrievable — Can be picked up after being deployed. For the Guardian Turret, this does not restore a full charge, but refunds most of the cooldown instead.
Remote Controlled — Can be commanded to self-destruct by the user from any distance. This refunds half of the cooldown.
Deployment Limit — Can only be deployed if there is no existing Guardian Turret.

[Stats > Properties > Bullet]
Hitscan — Travels in a straight line, meaning there is no bullet drop. The direction will deviate from the crosshairs depending on accuracy.
Damaging — The projectile deals damage if it hits a contestant.
No Critical Hit — Does not critically hit for increased damage, even if the target was struck on the head.
Not Interceptible — Can not be removed by the APS Turret .
No Falloff — Does not deal reduced damage when hitting targets at long distances.

---

Result 5  cite as: [Guardian Turret § Stats > Properties > Turret]
covers: Stats > Properties > Turret / Guide > Strengths (cite any of these sections of Guardian Turret)
url: https://www.thefinals.wiki/wiki/Guardian_Turret
Attached — Attaches to a surface upon deployment. Sticks to the surface even if it moves. Weighs down any carriable object it is attached to.
Solid — Has its own collision, meaning it blocks bullets and contestants can stand on it.
Arming Time — Disarmed when initially deployed. Does not detect enemies while disarmed. Arms automatically after a wind-up time. Uniquely, the Guardian Turret remains armed when picked up as an attachment.
Destructible — Can be destroyed if its health is fully depleted, such as through hits from bullets or explosions. Has a health bar and cannot take damage from the user's team.
Glitchable — Can be temporarily disabled by a Glitch Grenade or Glitch Barrel .
Reshapeable — Can be reshaped by the Data Reshaper into a piece of decor by opponents.
Sound Cue — Remains silent while idling, but produces a loud sound on startup and when it locks onto a target, alerting nearby contestants.
Permanent — Does not disappear by itself.
No Structure Damage — Cannot be used to damage structures.
No Friendly Fire — Can damage neither the user nor their teammates.

[Guide > Strengths]
- The Guardian Turret can be used to lock down an area. If an opponent enters its line of sight, it will make the team aware an opponent is there thanks to its sound cue.
```
</details>

---

## q10 (single)

**Question:** How much damage does the first hit of Charge 'N' Slam deal?

**Reference:** 100 damage on the initial hit, 40 on subsequent hits; the ground slam deals 50-200 in a 4 m radius.

**Agent answer:**

The first hit of Charge 'N' Slam deals 100 damage (with subsequent hits dealing 40 damage) [Charge 'N' Slam § Overview].

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
- The overhead swing always outdamages the regular swing. The regular swing should be used to finish off opponents at lower health or to damage opponents that the user can not catch in their overhead swing.

[Guide > Useful Damage Combinations]
Light: Attack Combo Alt Fire; Damage 200; Time to kill (s) 1.05
Medium: Attack Combo Alt Fire → Primary Fire; Damage 200 + 120 = 320; Time to kill (s) 1.99
Medium: Attack Combo Primary Fire → Primary Fire → Quick Melee; Damage 120 + 120 + 25 = 265; Time to kill (s) 1.64
Heavy: Attack Combo Alt Fire → Alt Fire; Damage 200 + 200 = 400; Time to kill (s) 2.46
Heavy: Attack Combo Primary Fire → Primary Fire → Primary Fire; Damage 120 + 120 + 120 = 360; Time to kill (s) 2.26
Heavy: Attack Combo Alt Fire → Primary Fire → Quick Melee; Damage 200 + 120 + 25 = 345; Time to kill (s) 2.24

---

Result 5  cite as: [KS-23 § Guide > Tactics]
url: https://www.thefinals.wiki/wiki/KS-23
- Dealing an immediate 100 damage within effective range, it's important for the user to be aware of certain breakpoints in combination with Gadgets , Spec
```
</details>

---

## q11 (single)

**Question:** What happens when a Goo Gun blob hits an opponent?

**Reference:** The opponent is momentarily slowed and any action they are doing is interrupted, including reviving or stealing a cashout; then the goo destroys itself.

**Agent answer:**

When a Goo Gun blob hits an opponent, it does not deal any damage [Goo Gun § Stats > Properties > Projectile], but it momentarily slows them and interrupts any action they are currently performing (such as reviving a teammate or stealing a cashout) before the goo destroys itself [Goo Gun § Stats > Effects]. It can also briefly incapacitate or trap them .

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Goo Gun § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget (cite any of these sections of Goo Gun)
url: https://www.thefinals.wiki/wiki/Goo_Gun
The Goo Gun can be used to create blobs of goo . The goo will stick to the first entity it hits; besides surfaces, this can be another piece of goo, an arena carriable or a contestant.
The goo can be damaged by opponents and teammates to destroy it. The created goo is also highly flammable; a nearby fire will quickly spread to any connected pieces of goo and destroy it after a few seconds.
If a goo piece is fired at a contestant, they will be momentarily slowed before the goo destroys itself. This also interrupts any action the contestant is currently performing, including reviving or stealing cashouts.

[Stats > Properties > Gadget]
Ranged — Strikes targets by aiming and firing at them from a distance.
Stable Accuracy — Keeps a stable accuracy, even while moving and going airborne.
Full Reload — Replaces the entire magazine in one animation on reload.
No Deployment Limit — Can be deployed any number of times.

---

Result 2  cite as: [Goo Gun § Stats > Properties > Projectile]
covers: Stats > Properties > Projectile / Stats > Properties > Goo (cite any of these sections of Goo Gun)
url: https://www.thefinals.wiki/wiki/Goo_Gun
Projectile — Gets affected by gravity and has a travel time. Once attached, the gadget is no longer a projectile.
Trigger on Impact — Can fly for any amount of time and triggers when the projectile collides with a surface or contestant, creating a Placed Goo.
Interceptible — Can be removed by the APS Turret , nullifying its effects. This causes the turret to lose some health.
Not Damaging — Hitting a contestant directly with the projectile does not deal damage.
Not Destructible — Cannot be destroyed by receiving damage such as from bullets or explosions.

[Stats > Properties > Goo]
Attached — Attaches to a surface upon deployment. Sticks to the surface even if it moves. Weighs down any carriable object it is attached to.
Solid — Has its own collision, meaning it blocks bullets and contestants can stand on it.
Destructible — Can be destroyed if its health is fully depleted, such as through hits from bullets or explosions. Teammates can also destroy it.
Immobilizing — Can trap contestants, making them unable to move until the goo destroys itself a moment later.
Not Reshapeable — Cannot be reshaped by the Data Reshaper .
Not Permanent — Disappears by itself after enough time has passed.

---

Result 3  cite as: [Goo Gun § Overview]
covers: Overview / Usage (cite any of these sections of Goo Gun)
url: https://www.thefinals.wiki/wiki/Goo_Gun
GOO GUN
“Shoots blobs of goo that solidify on impact; useful for creating defenses”
Profile
Build: H Heavy
Icon
Type: Specialization
Unlock: Strategist
Stats
Cooldown: Reload - 2.4s
Ammo: 20
Technical
Health: 240 per Goo Blob
rpm: 230
The Goo Gun is a Heavy class specialization that shoots blobs of goo.

[Usage]
The Goo Gun can be selected as the specialization gadget of any Heavy build loadout.
The Goo Gun is very versatile, Its prime uses are for creating defenses, blocking turrets, mines and grenades, and being used as a movement tool.
Additionally it has more obscure uses such as: Temporarily trapping enemies to close gaps or run away, Quickly destroying APS turrets, Interrupting steals and revives, Moving cashout stations, and more.
The Goo Gun rewards out of the box thinking and fast reactions, every use has a time and place.
Equip Goo Gun: PC Q; PS R1; XBox RB; Key Specialization
Fire goo (Tap): PS R2; XBox RT; Key Primary fire
Tactical reload: PC R; PS ◻; XBox X; Key Reload

---

Result 4  cite as: [Goo Gun § Guide > Strengths]
covers: Guide > Strengths / Guide > Weaknesses / Guide > Tactics (cite any of these sections of Goo Gun)
url: https://www.thefinals.wiki/wiki/Goo_Gun
- The Goo Gun can block off potential all the entry points of an area, such as windows.
- The Goo Gun can be used to briefly incapacitate players by trapping them in a blob of goo.
- Goo placed by the Goo Gun can be used to access inaccessible areas, or open up alternative entry points.

[Guide > Weaknesses]
- Fire can get rid of constructions made by the Goo Gun.

[Guide > Tactics]
- The Goo Gun can be used to surround an objective in a wall of goo, often called a "cocoon." Paired with an Anti-Gravity Cube , they can be attached to walls or ceilings, making them much harder to bypass.
- The Goo Gun can quickly destroy an APS Turret by firing multiple shots near it, as each blob is intercepted and damages the turret.

---

Result 5  cite as: [Goo Grenade § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget / Stats > Properties > Projectile (cite any of these sections of Goo Grenade)
url: https://www.thefinals.wiki/wiki/Goo_Grenade
The Goo Grenade can be deployed by throwing it. The moment it impacts on a surface or contestant, it releases goo that instantly expands into a wall. The direction that the wall expands into depends on where it was thrown (see Mechanics ).
The goo can be damaged by opponents and teammates to destroy it. The created goo is also highly flammable. A nearby fire will quickly spread to all of the goo and destroy it after a few seconds.

[Stats > Properties > Gadget]
Grenade — Can be thrown like a grenade, meaning overhand or underhand. The trajectory and impact point are shown as an indicator.
Multiple Charges — Can be used 2 times. When a charge is used, it automatically recharges over the cooldown time.

[Stats > Properties > Projectile]
Projectile — Gets affected by gravity and has a travel time.
Trigger on Impact — Can fly for any amount of time and triggers when the projectile collides with a surface or contestant. Contestants are treated like walls.
Interceptible — Can be removed by the APS Turret , nullifying its effects. This causes the turret to lose some health.
Reshapeable — Can be reshaped by the Data Reshaper into a p
```
</details>

---

## q12 (single)

**Question:** What is the Winch Claw's cooldown after pulling a high-value target?

**Reference:** 18 seconds (10 s on a miss, 14 s on a low-value target).

**Agent answer:**

The wiki contains conflicting information regarding the Winch Claw's cooldowns:

* The Overview section lists the cooldown for a high-value target as **18s** (along with 10s for a miss and 14s for a low-value target) [Winch Claw § Overview].
* The Guide > Pull section lists the cooldown as **14s** for a high-value target (and 7s for a low-value target or a miss) [Winch Claw § Guide > Tactics].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Winch Claw § Guide > Tactics]
covers: Guide > Tactics / Guide > Pull (cite any of these sections of Winch Claw)
url: https://www.thefinals.wiki/wiki/Winch_Claw
- The Winch Claw can be combined well with the Sledgehammer , Spear , Flamethrower and SA1216 as the Winch Claw will pull an opponent into its effective range.
- The Winch Claw can be used to drag a cashout station to a more optimal position for attack and defense or to deny a steal.

[Guide > Pull]
- Contestants and carriable objects, such as barrels , revive statues and cash boxes will be pulled in such a way that they are placed neatly in front of the user.
- Heavier objects such as a piece of structure debris or the cashout station will be forced in the direction of the user instead.
- The Winch Claw can be used on the following objects, separated into "low-value" and "high-value" targets. The cooldown of the Winch Claw depends on what object is grabbed: 7s for a low-value target (or miss), and 14s for a high-value target.
Arena objects , including ally Revive Statues and cash boxes: Enemy contestants
Debris from fallen structures: Cashout Stations or Terminals
- Objects that can not be pulled include: a Revive Statue of a team other than the user's, a Coin , and a piece of structure that is attached to an existing structure. Any other object can be pulled.
- If the user is eliminated before the pull, the pull is cancelled.

---

Result 2  cite as: [Winch Claw § Overview]
covers: Overview / Usage / Stats > Effects / Stats > Properties > Gadget (cite any of these sections of Winch Claw)
url: https://www.thefinals.wiki/wiki/Winch_Claw
WINCH CLAW
“Launches a chain claw that latches on to objects or contestants, pulling them in closer to you”
Profile
Build: H Heavy
Icon
Type: Specialization
Unlock: Enforcer
Stats
Cooldown: Miss - 10s Low-value Target - 14s High-value Target - 18s
Technical
Damage: 5
Max Range: 12m
Duration: Stun: 3m or less - 0.1s Max range - 0.5s
The Winch Claw is a Heavy class specialization that fires a claw which, upon impact with an opponent or almost any type of object, forcibly brings them to the user.

[Usage]
The Winch Claw can be selected as the specialization gadget of any Heavy build loadout.
The specialization trigger can be used to cast out the Winch Claw. It is possible to move while reeling in an object to change the location it is dragged to.
Fire (Tap): PC Q; PS R1; XBox RB; Key Specialization

[Stats > Effects]
The Winch Claw can be activated to throw out a claw in a straight line ahead. The first thing it catches, if not an immovable structure, will be pulled towards the user.

[Stats > Properties > Gadget]
Ranged — Can be used by aiming and firing at a contestant or object.
Stable Accuracy — Keeps a stable accuracy, even while moving and going airborne.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
Disarms User — Forces the user to stop using their other items for a short time while using the gadget.

---

Result 3  cite as: [Winch Claw § Stats > Properties > Projectile]
covers: Stats > Properties > Projectile / Guide > Strengths / Guide > Weaknesses (cite any of these sections of Winch Claw)
url: https://www.thefinals.wiki/wiki/Winch_Claw
Projectile — Travels in a straight line without being affected by gravity.
Trigger on Impact — Applies its effects if an opponent or object is struck. Does not apply effects when hitting shields.
Damaging — The projectile deals damage if it hits a contestant.
Movement — Causes the affected opponent or object to move towards the user.
Immobilizing — Stops affected contestants from moving.
Not Interceptible — Can not be removed by the APS Turret .
No Structure Damage — Cannot be used to damage structures.
No Friendly Fire — Can not be used to grab teammates.

[Guide > Strengths]
- The Winch Claw can be used to grab objects from a distance that could not be reached otherwise.
- Some objects that cannot be grabbed normally, such as a cashout station , can be dragged with the Winch Claw.

[Guide > Weaknesses]
- If the target being pulled gets stuck on a wall, the pull will be cancelled after a second.
- The Winch Claw is blocked by shields, like the Mesh Shield and Dome Shield . It cannot latch onto opponents or targets behind these surfaces.
- Pulling in a melee weapon or shotgun user when the user is not using a melee weapon can lead to an unfavorable fight.

---

Result 4  cite as: [Grappling Hook § Overview]
covers: Overview / Usage (cite any of these sections of Grappling Hook)
url: https://www.thefinals.wiki/wiki/Grappling_Hook
GRAPPLING HOOK
“A cord with a hook that you launch to scale structures and swing past walls. Also handy for quick escapes during combat”
Profile
Build: L Light
Icon
Type: Specialization
Unlock: Free
Stats
Cooldown: Minimum 4s Maximum 7.5s
Ammo: 1
Technical
Max Range: 25m
The Grappling Hook is a Light class specialization that allows its user to quickly move a long distance through the air by swinging from structures.

[Usage]
The Grappling Hook can be selected as the specialization gadget of any Light build loadout.
The primary trigger can be used to activate the gadget. If the hook hits a surface, the user will fly towards it. The movement triggers can be used to control this flight. Moving sideways will cause the user to sway to that side, whereas moving forwards or backwards will affect the height at which the user will be dropped off. The exact effects of each movement input depends on where the hook was placed relatively to its user. The user can also press the jump button to do a small midair hop off the grappling hook, or press the primary trigger again to end the grapple early without this hop.
Fire (Tap): PC Q; PS R1; XBox RB; Key Specialization

---

Result 5  cite as: [Glitch Trap § Overview]
covers: Overview / Usage (cite any of these sections of Glitch Trap)
url: https://www.thefinals.wiki/wiki/Glitch_Trap
GLITCH TRAP
“Deployable that sticks to a surface; when 
```
</details>

---

## q13 (single)

**Question:** How fast does the Healing Emitter heal and over what radius?

**Reference:** 10 HP/s rising to 15 HP/s over 2 seconds, in a 4 m radius.

**Agent answer:**

The Healing Emitter heals at a rate of 10 health per second, ramping up to 15 health per second over 2 seconds [Healing Emitter § Overview]. It has a radius of 4m [Healing Emitter § Overview] [Healing Emitter § Usage].

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
While the Healing Emitter is deployed, the gadget will not start restoring its next charge. If emitter is destroyed, the full cooldown is applied. The gadget can be retrieved manually to restore most of its cooldown by interacting with it for a few seconds while standing close. Alternatively, it can be retrieved remotely to restore half of its charge by holding the secondary trigger on the gadget while a Healing Emitter is deployed.
Equip Healing Emitter: PC 2 3 4; PS L1; XBox LB; Key Gadget
Throw: PS R2; XBox RT; Key Primary fire
Drop Remove deployed Emitter (Hold): PS L2; XBox LT; Key Secondary fire
Retrieve (Hold): PC E; PS △; XBox Y; Key Interact
Pick up: PC F; PS ◻; XBox X; Key Pick up
```
</details>

---

## q14 (single)

**Question:** How much damage does an RPG-7 rocket deal and what is its blast radius?

**Reference:** 110 damage, with an inner radius of 1.5 m and an outer radius of 5.5 m; cooldown 45 s.

**Agent answer:**

The Heavy's RPG-7 deals **110** damage [RPG-7 § Overview]. Its damage radius features an **inner radius of 1.5m** and an **outer radius of 5.5m** [RPG-7 § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [RPG-7 § Overview]
covers: Overview / Usage / Stats > Effects (cite any of these sections of RPG-7)
url: https://www.thefinals.wiki/wiki/RPG-7
RPG-7
“Fires long-range, high-explosive missiles that detonate on impact”
Profile
Build: H Heavy
Icon
Type: Offensive
Unlock: Demolisher
Stats
Cooldown: 45s Reload - 2.15s
Ammo: 1
Technical
Damage: 110
Environment Dmg: Over 2000
Damage Radius: Inner - 1.5m Outer - 5.5m
The RPG-7 is a Heavy class gadget that fires a rocket propelled grenade which deals high damage in an area and destroys structures.

[Usage]
The RPG-7 can be selected as one of three gadgets of any Heavy build loadout.
The gadget can be held and fired like a weapon. Aiming down sights increases the accuracy of the projectile. Moving decreases accuracy.
The trigger can be pulled to fire a projectile that explodes upon impact.
When a new charge of the RPG-7 is ready, it needs to be reloaded like a weapon, unlike most gadgets. The reloading animation is automatically started once a charge is ready and the gadget is held.
Equip RPG-7: PC 2 3 4; PS L1; XBox LB; Key Gadget
Fire shot (Tap): PS R2; XBox RT; Key Primary fire
Aim down sights (Hold): PS L2; XBox LT; Key Secondary fire

[Stats > Effects]
The RPG-7 can be deployed by firing it. When the rocket collides with a surface or contestant, it explodes, dealing high damage in an area and major damage to structures. The user will take an even higher amount of damage if they are too close.
The rocket can reach nearby targets very quickly, but will take a long time to travel longer distances.

---

Result 2  cite as: [RPG-7 § Stats > Properties > Gadget]
covers: Stats > Properties > Gadget / Stats > Properties > Projectile / Stats > Properties > Explosion (cite any of these sections of RPG-7)
url: https://www.thefinals.wiki/wiki/RPG-7
Ranged — Strikes targets by aiming and firing at them from a distance.
Aim Down Sights — Has iron sights that significantly increase accuracy when used.
Single Charge — Can be used once, then recharges automatically over the cooldown time.
Gadget Reload — Automatically goes into a reloading animation once the gadget is used and a new charge is ready to be loaded.
Unstable Accuracy — Suffers a significant decrease in accuracy while moving and while airborne.

[Stats > Properties > Projectile]
Projectile — Has a travel time but has a straight trajectory.
Trigger on Impact — Can fly for any amount of time and triggers when the projectile collides with a surface or contestant.
Interceptible — Can be removed by the APS Turret , nullifying its effects. This causes the turret to lose some health.
Reshapeable — Can be reshaped by the Data Reshaper into a piece of decor by opponents.
Not Damaging — Hitting a contestant directly with the projectile does not deal damage.
Not Destructible — Cannot be destroyed by receiving damage such as from bullets or explosions.

[Stats > Properties > Explosion]
Explosive — Deals damage in an area of effect that can be intercepted by structures and shields.
Damaging — Deals damage to contestants.
Major Structure Damage — Damages structures. Instantly destroys a concrete wall.
No Friendly Fire — Can damage the user, but not their teammates.

---

Result 3  cite as: [RPG-7 § Guide > Strengths]
covers: Guide > Strengths / Guide > Weaknesses / Guide > Tactics (cite any of these sections of RPG-7)
url: https://www.thefinals.wiki/wiki/RPG-7
- The RPG-7 is very effective at taking down contestants at low health, as it is very easy and quick to hit.
- The gadget has a high inner damage radius, meaning it will deal maximum damage even if the target is 1.5 meters away.
- Compared to most other projectiles/launchers, the RPG-7 has no projectile drop, allowing it to be destructive at any range.

[Guide > Weaknesses]
- If the RPG-7 explodes near its user, it will cause them additional damage compared to the damage dealt to their opponent (1.8x), discouraging a deployment of the RPG-7 very close to the user.
- The APS Turret counters the RPG-7. A Medium build contestant facing a potential RPG-7 usage can quickly place an APS Turret near themselves to intercept it.

[Guide > Tactics]
- The RPG-7 can reach a high ceiling to breach it unlike the C4 , such as to bring down the cashout station .

---

Result 4  cite as: [KS-23 § Segmented Reload > Properties > Bullet]
url: https://www.thefinals.wiki/wiki/KS-23
Hitscan — Up to 25m — Travels in a straight line, meaning there is no bullet drop. The direction will deviate from the crosshairs depending on accuracy.
Projectile — After 25m — Gets affected by gravity and has a travel time.
Mid Range Falloff — Deals reduced damage when hitting targets at a moderate distance (falloff starts at less than 30m).
Moderate Structure Damage — Damages structures. Takes a few seconds or multiple charges to break a concrete wall.
No Critical Hit — Does not critically hit for increased damage, even if the target was struck on the head.
Not Interceptible — Can not be removed by the APS Turret .

---

Result 5  cite as: [MGL32 § Stats > Properties > Projectile]
covers: Stats > Properties > Projectile / Stats > Properties > Explosion (cite any of these sections of MGL32)
url: https://www.thefinals.wiki/wiki/MGL32
Projectile — Gets affected by gravity and has a travel time.
Bounce — Bounces away when the projectile collides with a surface or contestant. For the MGL32, this happens exactly once per projectile.
Trigger on Impact — Triggers when the projectile collides with a surface or contestant. For the MGL32, this happens only on the second impact.
Trigger on Time — Triggers after a fixed amount of time if the projectile does not strike a surface or contestant.
Interceptible — Can be removed by the APS Turret , nullifying its effects. This causes the turret to lose some health.
No Critical Hit — Does not critically hit for increased damage, even if the target was struck on the head.
No Falloff — Does not deal reduced damage when hitting targets at long dista
```
</details>

---

## q15 (single)

**Question:** How many Barricade panels can a Heavy have deployed at once, and how much health does each have?

**Reference:** Up to 4 deployed, 800 health per panel (environmental).

**Agent answer:**

A Heavy can have a maximum of **4** Barricades deployed at a time [Barricade § Stats > Properties > Gadget]. Each individual panel has **800** health [Barricade § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Barricade § Overview]
covers: Overview / Usage (cite any of these sections of Barricade)
url: https://www.thefinals.wiki/wiki/Barricade
BARRICADE
“Highly durable shields that are perfect for fortifying an area”
Profile
Build: H Heavy
Icon
Type: Defensive
Unlock: Strategist
Stats
Cooldown: 30s
Ammo: 2
Technical
Max Deployed: 4
Health: 800 per panel (environmental)
The Barricade is a Heavy class placeable gadget that creates a strong wall to take cover behind.

[Usage]
The Barricade can be selected as one of three gadgets of any Heavy build loadout.
While the gadget is held, an indicator will show a potential placement of the Barricade as a blue hologram in front of the user. If the hologram is red, the gadget will not fit in the target location. The secondary trigger can be used to rotate the placement hologram. Using the primary trigger, the placement can be confirmed to deploy the gadget. It can be only deployed on floors, not walls or ceilings.
The gadget can also be retrieved to restore a charge, by interacting with it for a few moments while looking at it from up close.
Equip Barricade: PC 2 3 4; PS L1; XBox LB; Key Gadget
Confirm placement (Tap): PS R2; XBox RT; Key Primary fire
Rotate placement (Tap): PS L2; XBox LT; Key Secondary fire
Retrieve deployed Barricade (Hold): PC E; PS △; XBox Y; Key Interact

---

Result 2  cite as: [Barricade § Stats > Effects]
covers: Stats > Effects / Stats > Properties > Gadget / Stats > Properties > Barricade (cite any of these sections of Barricade)
url: https://www.thefinals.wiki/wiki/Barricade
The Barricade can be deployed by placing it down on a nearby floor. It will absorb damage like a regular structure. Opponents can destroy it by attacking it. Items that deal high structure damage will have an easier time removing a Barricade.
The Barricade is made up of 5 panels placed in a horizontal line, with each panel having the same amount of health.

[Stats > Properties > Gadget]
Placeable — Can be placed attached to a surface. An indicator shows the exact target placement.
Multiple Charges — Can be used 2 times. When a charge is used, it automatically recharges over the cooldown time.
Retrievable — Can be picked up after being deployed to restore a charge.
Deployment Limit — 4 Barricades can be deployed at a time. An excess deployment causes the oldest Barricade to disappear.

[Stats > Properties > Barricade]
Attached — Attaches to a surface upon deployment. Sticks to the surface even if it moves. Weighs down any carriable object it is attached to.
Solid — Has its own collision, meaning it blocks bullets and contestants can stand on it.
Destructible — Can be destroyed if its health is fully depleted, such as through hits from bullets or explosions. Teammates can also destroy it.
Reshapeable — Can be reshaped by the Data Reshaper into a piece of decor by opponents.
Permanent — Does not disappear by itself.
Usable by Opponents — Can be used by opponents to their advantage.

---

Result 3  cite as: [Barricade § Guide > Strengths]
covers: Guide > Strengths / Guide > Weaknesses / Guide > Tactics (cite any of these sections of Barricade)
url: https://www.thefinals.wiki/wiki/Barricade
- The Barricade has the highest amount of health out of any gadget per segment, let alone when adding up the health of every segment.
- A relatively high amount of Barricades can be placed compared to other gadgets, making it strong on Power Shift .
- The Barricade places itself nearly instantly. Besides offering fast cover, with good reflexes and prediction abilities, it can be used to "parry" projectiles, such as an RPG-7 's rocket or the Lockbolt 's projectile.

[Guide > Weaknesses]
- The Pyro Grenade can be thrown at a Barricade, making it unusable as a proper barrier as anyone hiding behind it will burn.
- Explosions with high structure damage such as the RPG-7 can immediately breach a Barricade.
- A Data Reshaper can simply reshape Barricades into Arena Carriables .
- The KS-23 's slugs or Sledgehammer 's overhead swings high enviromental damage apply to the Barricade and its panels, allowing those weapons to easily take them down.

[Guide > Tactics]
- The Barricade can be combined with the MGL32 . After placing a Barricade, the user can fire their grenades at the ceiling while the target cannot retaliate as the user is taking cover behind the Barricade.
- The Barricade can be pre-selected during a Charge 'N' Slam , allowing the user to place it when they finish charging and provide near instant cover.

---

Result 4  cite as: [Builds § Heavy Build]
url: https://www.thefinals.wiki/wiki/Builds
“High survivability. Low movement speed. Specializes in demolition and fortifications.”
The Heavy Build is a powerhouse: Though slow-moving, it is the most durable Build, designed for taking and holding ground. With the highest health pool, Heavies thrive in direct combat and controlling objectives but struggle with mobility.
Heavies bring devastating equipment to the battlefield, like the Charge 'N' Slam and RPG-7 , capable of damaging enemies and obliterating structures. They also possess a wide array of defensive utility, like the Barricade , Dome Shield , and Mesh Shield , all of which allow them to defend objectives and their teammates. Additionally, gadgets like the Lockbolt and Anti-Gravity Cube let them manipulate enemy movement and disrupt objectives.
Heavy contestants favor close to mid-range weapons, from more traditional options like the M60 and Lewis Gun to wildcards like the MGL32 . They can also be seen with strong melee weapons, from the heavy-hitting Sledgehammer and swift Spear , or even a Flamethrower for close-range pyrotechnics.
Due to their size, Heavies cannot crouch or slide through vents, but they can vault onto elevated areas more easily and throw objects farther using the Gravity Glove .
Boasting an impressive 325 HP , Heavies are the toughest build to bring down—but this comes at the cost of the slowest movement speed and largest hit
```
</details>

---

## q16 (single)

**Question:** What are the AKM's magazine size and rate of fire?

**Reference:** 36 rounds per magazine, 600 RPM.

**Agent answer:**

The Medium class AKM has a magazine size of 36 and a rate of fire of 600 RPM [AKM § Overview].

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
- Immediately, the closest contestant, structure, object or shield intersecting the hitscan will be tagged as being struck. First, a bullet tracer animation quickly travels from the weapon to the hit location, then its effects are applied. This means it is possible for targets to be struck a few frames after they appear to take cover, as the hit is confirmed the moment the weapon is fired.

---

Result 5  cite as: [FCAR § Stats > Properties > Bullet]
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
- The FCAR's damage begins to fall off at moderate distances, and falls off
```
</details>

---

## q17 (single)

**Question:** How much environmental (structure) damage does one KS-23 slug deal?

**Reference:** 1000 environmental damage per slug (100 body damage).

**Agent answer:**

One KS-23 slug deals 1000 environmental structure damage [KS-23 § Overview].

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
Unstable Accuracy — Suffers a significant decrease in accuracy while moving and while airborne.

---

Result 5  cite as: [KS-23 § Guide > Strengths]
url: https://www.thefinals.wiki/wiki/KS-23
- The KS-23 can break through any breakable surface with its slugs, giving the user a way to destroy the enviroment in a few shots without having to rely on charges of explosive Gadgets like the C4 and RPG-7 or Charge 'N' Slam .
- Dealing up to a 100 damage per shot makes the KS-23 great at dealing quick bursts of high damage while not being reliant on hitting heads, as this weapon has no headshot multiplier.
- Because of it's single-shot nature, the KS-23 is great at dealing poke damage, even at range if the user can predict enemy movement from afar.
- In Terminal Attack , the maximum health Light contestants can regenerate to is 100 health. This is exactly the damage of the KS-23, giving the weapon a slight advantage against that build in the game mode.
```
</details>

---

## q18 (single)

**Question:** How much cash does a team need to win Quick Cash, and how many teams play?

**Reference:** $20,000; three teams of three (3v3v3).

**Agent answer:**

To win a Quick Cash match, a team must be the first to reach **$20,000** [Quick Cash § Overview]. 

The mode is played with **three teams of three** (3v3v3) [Quick Cash § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Quick Cash § Overview]
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

Result 2  cite as: [Quick Cash § Gameplay]
url: https://www.thefinals.wiki/wiki/Quick_Cash
Teams earn cash by depositing Cash Boxes into Cashout Stations . Contestants must first locate an available Vault and open it, triggering a twenty second timer. When this timer expires, the Vault will eject a Cash Box which contestants can carry to a Cashout Station . Once picked up, Cash Boxes can be thrown, allowing contestants to defend themselves if attacked, pass the Cash Box to a teammate, or insert it from distance.
After a Cash Box is deposited into a Cashout Station , a timer will begin. The team must defend the active Cashout and prevent opponents from stealing it. All other contestants will be alerted to the active Cashout and may attempt to steal it. If the team successfully defends the station until the timer ends, the cash will be added to their total, and a new Vault will spawn in the arena.
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

---

Result 3  cite as: [Quick Cash § Gameplay]
covers: Gameplay / Rules / Rules > Win Conditions / Rules > Objective > Vaults (cite any of these sections of Quick Cash)
url: https://www.thefinals.wiki/wiki/Quick_Cash
Once the cashout is completed, the team that currently controls the Cashout Station is awarded the full value of the Cash Box .
While a cashout is active, it is owned by a single team. If that team remains the owner when the cashout completes, they are awarded the full cash value. Contestants from opposing teams can attempt to steal the cashout by interacting with the Cashout Station for a short duration.
Steal Cashout (Hold): PC E; PS △; XBox Y; Key Interact
Cashout durations are fixed, provided there is sufficient time remaining in the round. If there is not enough time left to complete a full cashout, up to one minute of overtime is added to allow it to finish.
- Cashout Duration - 2:00

[Rules]
UNLOCK THE VAULT Unlock a vault and grab the Cash Box
Deposit a Cashbox Insert the Cash Box into a Cashout Station
Defend the Cashout The team that controls the Cashout Station when the timer ends gets the money

[Rules > Win Conditions]
- The first team to reach $20,000 cash wins.

[Rules > Objective > Vaults]
- A $10,000 Vault spawns at the start of the game and after each completed deposit.
- Only one Vault can be active at a time.
- After spawning, the Vault has a 15-second wind-up before it can be interacted with.
- Once interacted with, it takes 20 seconds for the Cash Boxes to pop out and become available for deposit.

---

Result 4  cite as: [Cashout § Rules > Tournament Structure]
covers: Rules > Tournament Structure / Rules > Ways to Gain Cash (cite any of these sections of Cashout)
url: https://www.thefinals.wiki/wiki/Cashout
The Tournament features 8 teams (24 contestants total) competing in a knockout bracket. The top 2 teams qualify for the next round, while the bottom 2 teams are eliminated.
- Knockout Round 1: 8 teams split into two matches (4 teams per match).
- Knockout Round 2: 4 remaining teams compete in one match.
- Final Round: The last 2 teams face off under rules similar to Head2Head , with Vaults worth $25,000. The first team to reach $50,000 wins the tournament.

[Rules > Ways to Gain Cash]
- $500 – Eliminating a contestant.
- $1,000 – Eliminating a contestant during Death Match .
- $1,000 – Opening a Vault.
- $1,000 – Stealing an active Cashout Station .
- $2,000 – Depositing Cash Boxes from Vaults 1 & 2
- $3,000 – Depositing Cash Boxes from Vaults 3 & 4
- $4,000 – Depositing Cash Boxes from Vaults 5 & 6
- All Cash in the Cashout Station – Completing a Deposit

---

Result 5  cite as: [Ranked Cashout § Rules > Tournament Structure]
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
```
</details>

---

## q19 (single)

**Question:** What is Double Jeopardy in Cashout?

**Reference:** An anti-griefing rule since Season 9: it triggers when a team inserts a second Cash Box into an already active Cashout Station; if that team fails to secure the station, it loses 50% of its current cash.

**Agent answer:**

Double Jeopardy is an anti-griefing mechanic in Cashout designed to discourage strategic griefing, such as deliberately targeting a specific squad or manipulating which teams advance [Cashout § Gameplay]. 

* **Trigger:** It is triggered when a team inserts a second Cash Box into an already active Cashout Station [Cashout § Rules > Objective > Cashout Station]. 
* **Penalty:** If that team fails to secure and own the Cashout Station when the timer expires, they instantly lose 50% of their current total cash [Cashout § Gameplay] [Cashout § Rules > Objective > Cashout Station].
* **Indicators:** When triggered, the team is highlighted in red on the scoreboard, their team name is shown on screen, and a dedicated callout plays from commentators Scotty and June [Cashout § Gameplay].

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
- Stealing an active Cashout Station takes 7 seconds and grants $1,000 during Qualifying Rounds.
- Stealing an active Cashout Station takes 6 seconds and grants $0 during the Final Round.
- Inactive Cashout Stations will despawn when overtime starts.
Deposit Process
- To start a deposit, place the Cash Box into a Cashout Station .
- When a Cash Box is deposited, 20% of its value is instantly awarded to the team, while the remaining 80% is stored in the Cashout Station .
- The deposit process takes 2 minutes to complete in regular time.
- If enough time remains in the round, the deposit lasts the full duration; otherwise, up to 1 minute of overtime is added.

---

Result 5  cite as: [Cashout § Gameplay]
url: https://www.thefinals.wiki/wiki/Cashout
Teams earn cash by depositing Cash Boxes into Cashout Stations . Contestants must first locate an available Vault and open it, triggering a twenty second timer. When this timer expires, the Vault will eject a Cash Box which contestants can carry to a Cashout Station . Once picked up, Cash Boxes can be th
```
</details>

---

## q20 (single)

**Question:** How much cash does a team earn per elimination in Team Deathmatch, and how much do they need to win a round?

**Reference:** $100 per elimination; a round is won by reaching $3,000 first (or having the most money when the 5-minute timer ends).

**Agent answer:**

In Team Deathmatch, a team earns **$100** per enemy elimination [Team Deathmatch § Elimination Rules]. To win a round, a team must be the first to reach **$3,000**, or have the highest score when the 5-minute timer expires [Team Deathmatch § Contestants and Respawns].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Team Deathmatch § Overview]
covers: Overview / Objective / Elimination Rules / Maps (cite any of these sections of Team Deathmatch)
url: https://www.thefinals.wiki/wiki/Team_Deathmatch
Team Deathmatch
Overview
Short description: Eliminate opponents to earn cash
Length: Three Rounds (BO3)
Format: 5v5
Features: Unlimited respawn credits
Progression: World Tour
Eliminate Opponents Get more eliminations than the opponent team
First to $3,000 wins First team to win 2 rounds wins the game
Team Deathmatch (TDM) is a fast-paced Gamemode where two teams of five contestants compete to achieve the most eliminations in a best-of-three format. It was introduced as a Limited-Time Mode during Season 5 and later added permanently as a Quickplay mode with the release of Season 6 .

[Objective]
The objective of TDM is for a team to reach the goal amount of $3,000 by eliminating opponents, or have the highest score when the 5-minute timer ends.

[Elimination Rules]
- Eliminations : Each enemy that is eliminated by a contestant will award their team with $100.
- Other : Self-eliminations or friendly-fire eliminations will award the opposite team with $25.

[Maps]
- Arena Selection : When contestants load into a TDM match, a random arena will be chosen from the map pool. This arena will be played for the entire match.
- Individual Rounds : Each round takes place in an enclosed part of the chosen arena, surrounded by ‘out of bounds’ walls. Each round is played in a different section of the chosen arena.

---

Result 2  cite as: [Team Deathmatch § Contestants and Respawns]
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
NOZOMI/CITADEL: Standard Issue
P.E.A.C.E. Center: Standard Issue
Seoul: Under Construction
Skyway Stadium: High Rise • Up Down Left Right
Starlight Hollow: Standard Issue
SYS$HORIZON: Standard Issue

---

Result 3  cite as: [Quick Cash § Overview]
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
The gamemode was introduced in Season 3 . Prior to Season 9 , the gamemode was referred as World Tour and was a prime mode for casual play where weekly events that altered gameplay through special rules or modifiers took place. Before that change, the name "Cashout" refereed to a group of gamemodes with similar set of rules.

---

Result 5  cite as: [Cashout § Rules > Tournament Structure]
covers: Rules > Tournament Structure / Rules > Ways to Gain Cash (cite any of these sections of Cashout)
url: https://www.thefinals.wiki/wiki/Cashout
The Tournament features 8 teams (24 contestants total) competing in a knockout bracket. The top 2 teams qualify for the next round, while the bottom 2 teams are eliminated.
- Knockout Round 1: 8 teams split into two matches (4 teams per match).
- Knockout Round 2: 4 remaining teams compete in one match.
- Final Round: The last 2 teams face off under rules similar to Head2Head , with Vaults worth $25,000. The first team to reach $50,000 wins the tournament.

[Rules > Ways to Gain Cash]
- $500 – Eliminating a contestant.
- $1,000 – Eliminating a contestant during Death Match .
- $1,000 – Opening a Vault.
- $1,000 – Stealing an active Cashout Station .
- $2,000 – Depositing Cash Boxes from Vaults 1 & 2
- $3,000 – Depositing Cash Boxes from Vaults 3 & 4
- $4,000 – Depositing Cash Boxes from Vaults 5 & 6
- All Cash in the Cashout Station – Completing a Deposit
```
</details>

---

## q21 (single)

**Question:** In Power Shift, how many contestants need to stand on the platform for it to move at maximum speed?

**Reference:** Three or more (1 = slow, 2 = moderate, 3+ = maximum).

**Agent answer:**

In Power Shift, 3 or more contestants need to stand on the platform for it to move at maximum speed [Power Shift § Platform Mechanics] [Power Shift § Overview]. 

The speed scales as follows:
* **1 Contestant:** Slow [Power Shift § Platform Mechanics]
* **2 Contestants:** Moderate [Power Shift § Platform Mechanics]
* **3+ Contestants:** Maximum [Power Shift § Platform Mechanics]

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Power Shift § Platform Mechanics]
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

Result 5  cite as: [Cashout § Rules > Tournament Structure]
covers: Rules > Tournament Structure / Rules > Ways to Gain Cash (cite any of these sections of Cashout)
url: https://www.thefinals.wiki/wiki/Cashout
The Tournament features 8 teams (24 contestants total) competing in a knockout bracket. The top 2 teams qualify for the next round, while the bottom 2 teams are eliminated.
- Knockout Round 1: 8 teams split into two matches (4 teams per match).
- Knockout Round 2: 4 remaining teams compete in one match.
- Final Round: The last 2 teams face off under rules similar to Head2Head , with Vaults worth $25,000. The first team to reach $50,000 wins the tournament.

[Rules > Ways to Gain Cash]
- $500 – Eliminating a con
```
</details>

---

## q22 (single)

**Question:** Which sponsor is Kyoto associated with, and when was the arena introduced?

**Reference:** DISSUN; Kyoto was introduced in Season 3.

**Agent answer:**

Kyoto is associated with the sponsor **DISSUN** and was introduced in **Season 3** [Kyoto § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Kyoto § Overview]
covers: Overview / Arena Variants > Standard Issue / Arena Variants > Moving Platforms / Arena Variants > Suspended Structures (cite any of these sections of Kyoto)
url: https://www.thefinals.wiki/wiki/Kyoto
Kyoto
Introduced: Season 3
Sponsor(s): DISSUN
Arena Variant(s): Moving Platforms Standard Issue Suspended Structures
Supported Gamemode(s): Cashout Cashout (Bots) Power Shift Quick Cash Ranked Cashout Team Deathmatch
Kyoto 1568 was introduced with Season 3 and was the sixth arena to be added. It is based on the real-life city of Kyoto during the historic feudal period of Japan. The arena is set on a steep mountainside in the lush Kyoto Valley and features a network of 16th-century temples, gardens and dense bamboo forests.
Kyoto changes with each real-life season. During Fall, the leaves on trees in the arena become orange and golden brown. During Winter, the environment is covered in snow and the lakes freeze over. During Spring, cherry trees bloom.

Map of Kyoto Arena by Embark Studios
Kyoto is a large arena with a lot of open areas. Despite that there is a place for close quarter combat inside of the many buildings. Arena rewards movement speed and long range engagements with an ability to prepare for the defence before the attackers reach you. It features 3 arena variants, each introducing new obstacles and challenges to overcome to outplay the opponents.

[Arena Variants > Standard Issue]
“A standard arena, ready for destruction.”

[Arena Variants > Moving Platforms]
“Vaults or cashout stations could be found on platforms moving around the arena.”

[Arena Variants > Suspended Structures]
“Cashout stations are suspended high above the arena.”
This variant raises the arena with a network of high platforms.

---

Result 2  cite as: [Kyoto § Locations]
covers: Locations / Supported Gamemodes / Supported Gamemodes > Limited Time Modes (cite any of these sections of Kyoto)
url: https://www.thefinals.wiki/wiki/Kyoto
This article is a Stub . It needs some work! You can help us out by expanding it .
Bamboo Forest: An elevated bamboo forest, with disrupted sightlines and a small house.
Tower: Towering over the arena, this building offers a vantage point, it is accessed by a circular Jump Pad at the base if the structure.

[Supported Gamemodes]
Kyoto supports the following Gamemodes :
- Cashout
- Cashout (Bots)
- Power Shift
- Quick Cash
- Ranked Cashout
- Team Deathmatch

[Supported Gamemodes > Limited Time Modes]
- Bank It
- Head2Head

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

Result 4  cite as: [Fortune Stadium § Overview]
covers: Overview / Arena Variants > Standard Issue (cite any of these sections of Fortune Stadium)
url: https://www.thefinals.wiki/wiki/Fortune_Stadium
Fortune Stadium
Introduced: Season 4
Sponsor(s): HOLTOW , ENGIMO , ISEUL-T
Arena Variant(s): Standard Issue
Supported Gamemode(s): Cashout Quick Cash Ranked Cashout Team Deathmatch
Fortune Stadium was introduced with Season 4 and was the seventh arena to be added. The arena is comprised of sectors designated to the Season 4 sponsors: HOLTOW (sectors 1 and 3), ENGIMO (sector 2) and ISEUL-T (sectors 4, 5, and 6).

Map of Fortune Stadium Arena by Embark Studios
Fortune Stadium is a medium sized arena that is split into several sectors separated by the void, making the traversal between them dangerous. Every sector features a building that forces contestants to go close quarters inside and rarely offers a clear sigh line. Arena rewards adaptability to traversal speed and methods as your opponents will try their best to gun you down as you are trying to reach their sector. It features a single Standard Issue variant with two time-of-day modifiers.

[Arena Variants > Standard Issue]
“A standard arena, ready for destruction.”

---

Result 5  cite as: [NOZOMI/CITADEL § Overview]
covers: Overview / Arena Variants > Standard Issue / Supported Gamemodes (cite any of these sections of NOZOMI/CITADEL)
url: https://www.thefinals.wiki/wiki/NOZOMI/CITADEL
NOZOMI/CITADEL
Introduced: Season 7
Sponsor(s): CNS VAIIYA
Arena Variant(s): Standard Issue
Supported Gamemode(s): Cashout Point Break Power Shift Quick Cash Ranked Cashout Solo Showdown Team Deathmatch
NOZOMI/CITADEL was introduced with Season 7 and was the twelfth Arena to be added. The location of this arena is heavily inspired by Japan, especially Tokyo. The arena is split into two parts: Nozomi, the CNS district feel
```
</details>

---

## q23 (single)

**Question:** Why was the Las Vegas arena removed from the game?

**Reference:** With the PRIME TIME season it was removed because of the difficulty of maintaining both Las Vegas and the reworked Las Vegas Stadium.

**Agent answer:**

Las Vegas was entirely removed from the game with the release of the PRIME TIME season due to the difficulties of maintaining both the original map and its reworked version, Las Vegas Stadium, at the same time [Las Vegas § Overview].

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

---

## q24 (single)

**Question:** What is the team wipe penalty in a Ranked Cashout qualifying round?

**Reference:** A 27-second respawn and losing 15% of the team's total cash.

**Agent answer:**

In a Ranked Cashout qualifying round, the team wipe penalty is a 27-second respawn time and the loss of 15% of the team's total cash [Ranked Cashout § Overview].

<details><summary>Retrieved passages</summary>

```
Result 1  cite as: [Ranked Cashout § Overview]
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

Result 3  cite as: [Ranked Cashout § Rules > Objective > Cashout Station]
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
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
The gamemode was introduced in Season 3 . Prior to Season 9 , the gamemode was referred as World Tour and was a prime mode for casual play where weekly events that altered gameplay through special rules or modifiers took place. Before that change, the name "Cashout" refereed to a group of gamemodes with similar set of rules.

---

Result 5  cite as: [Ranked Cashout § Gameplay]
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
Teams earn cash by depositing Cash Boxes into Cashout Stations . Contestants must first locate an available Vault and open it, triggering a twenty second timer. When this timer expires, the Vault will eject a Cash Box which contestants can carry to a Cashout Station . Once picked up, Cash Boxes can be thrown, allowing contestants to defend themselves if attacked, pass the Cash Box to a teammate, or insert it from distance.
After a Cash Box is deposited into a Cashout Station , a timer will begin. The team must defend the active Cashout and prevent opponents from stealing it. All other contestants will be alerted to the active Cashout and may attempt to steal it. If the team successfully defends the station until the timer ends, the cash will be added to their total, and a new Vault will spawn in the arena.
Since Season 9 an anti-griefing mechanic known as Double Jeopardy was added to the gamemode. This system activates when a second Cash Box is inserted into an already active Cashout Station.
```
</details>

---

## m01 (multi)

**Question:** Which items or effects can reveal an enemy who is using the Cloaking Device?

**Reference:** Thermal Vision, the Motion Sensor and the Sonar Grenade (Cloaking Device weaknesses), and True Sight, which shows cloaked opponents fully.

**Agent answer:**

The items, specializations, and effects that can reveal or counter an enemy using the Cloaking Device include:

* **Thermal Vision:** Hard counters the Cloaking Device by revealing the heat signature of a cloaked player [Cloaking Device § Guide > Weaknesses].
* **True Sight:** A Light build specialization that highlights opponents and makes them fully visible even under the effects of the Cloaking Device [True Sight § Overview] [True Sight § Stats > Effects].
* **Motion Sensor and Sonar Grenade:** Detection sources that can reveal the location of a cloaked enemy [Cloaking Device § Guide > Weaknesses].
* **Taking Damage:** Dealing any damage to a cloaked player will cause them to instantly decloak [Cloaking Device § Guide > Weaknesses].
* **Visual & Audio Cues:** While moving, cloaked players display a glitchy visual effect and produce a distinct sound that can be heard by enemies up to 30m away (though they are nearly invisible and silent while completely motionless) [Cloaking Device § Stats > Effects] [Cloaking Device § Guide > Weaknesses] [Cloaking Device § Guide > Tactics].

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
covers: Stats > Effects / Stats > Properties > Gadget (cite any of these sections of Vanishing Bomb)
url: https://www.thefinals.wiki/wiki/Vanishing_Bomb
The Vanishing Bomb can be deployed by throwing it. The moment it impacts on a surface or contestant, it explodes into an area of effect. Any teammates (including the user) caught in the area will become invisible for a few seconds. The invisibility effect is similar to that of the Cloaking Device , although the sound cue of the Vanishing Bomb is more difficult for opponents to hear when moving near them, meaning it offers superior stealth.
It is possible to enable the Cloaking Device right before the effect of the Vanishing Bomb ends, which will transition from one invisibility to the next and bypass the sound cue that would normally play when activating the Cloaking Device.

[Stats > Properties > Gadget]
Grenade — Can be thrown like a grenade, meaning overhand or underhand. The trajectory and impact point are shown as an indicator.
Single Charge — Can be used once, then recharges automatically over the cooldown
```
</details>

---

## m02 (multi)

**Question:** Which has the larger magazine, the AKM or the FCAR, and by how many rounds?

**Reference:** The AKM: 36 rounds vs 20 for the FCAR, 16 more.

**Agent answer:**

The AKM has the larger magazine [AKM § Guide > Strengths] [FCAR § Guide > Strengths]. 

* **AKM Magazine:** 36 rounds [AKM § Overview]
* **FCAR Magazine:** 20 rounds [FCAR § Overview]

The AKM has a larger magazine by **16 rounds**.

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
- Immediately, the closest contestant, structure, object or shield intersecting the hitscan will be tagged as being struck. First, a bullet tracer animation quickly travels from the weapon to the hit location, then its effects are applied. This means it is possible for targets to be struck a few frames after they appear to take cover, as the hit is confirmed the moment the weapon is fired.

---

Result 5  cite as: [ShAK-50 § Guide > Weaknesses]
url: https://www.thefinals.wiki/wiki/ShAK-50
- Despite the shorter tactical and empty reload times, due to the low amount of bullets per magazine (being 20), the ShAk-50 sees more frequent downtime, especially in longer fights.
- While the individual shot deals considerably higher damage, the shot needs to hit the target in the first place. Missing multiple shots with the ShAk-50 can be very punishing, so it is crucial for the user to have good tracking to make each shot count.
- The distance between the two bullets shot by the ShAk-50 upon firing once increases with distance (see graphic on the right). Combined with it's short minimum and maximum range (compared to the M60 and Lewis Gun ), this significantly decreases its effectiveness at longer ranges, as one of the two bullets might not hit the target, halving the damage that this weapon could deal.

Result 1  cite as: [FCAR § Overview]
covers: Overview /
```
</details>

---

## m03 (multi)

**Question:** Which deals more environmental damage per shot, the KS-23 or the CL-40?

**Reference:** The KS-23: 1000 per slug vs 300 for the CL-40.

**Agent answer:**

The KS-23 deals more environmental damage per shot than the CL-40 [KS-23 § Overview] [CL-40 § Overview]. 

* **KS-23 (Heavy):** Deals **1000** environmental damage per shot [KS-23 § Overview].
* **CL-40 (Medium):** Deals **300** environmental damage per shot [CL-40 § Overview].

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
url: https://www.thefinals.wiki/wiki/KS-23
- The KS-23 can break through any breakable surface with its slugs, giving the user a way to destroy the enviroment in a few shots without having to rely on charges of explosive Gadgets like the C4 and RPG-7 or Charge 'N' Slam .
- Dealing up to a 100 damage per shot makes the KS-23 great at dealing quick bursts of high damage while not being reliant on hitting heads, as this weapon has no headshot multiplier.
- Because of it's single-shot nature, the KS-23 is great at dealing poke damage, even at range if the user can predict enemy movement from afar.
- In Terminal Attack , the maximum health Light contestants can regenerate to is 100 health. This is exactly the damage of the KS-23, giving the weapon a slight advantage against that build in the game mode.

Result 1  cite as: [CL-40 § Overview]
url: https://www.thefinals.wiki/wiki/CL-40
CL-40
Weapon Quote: “Pump-action grenade launcher”
Profile
Build: M Medium
Icon
Type: Grenade Launcher
Unlock: Free
Dama
```
</details>

---

## m04 (multi)

**Question:** Which has the shorter cooldown, the Breach Charge or the Thermal Bore, and which build uses them?

**Reference:** The Breach Charge (20 s vs 25 s for the Thermal Bore); both are Light gadgets.

**Agent answer:**

The **Breach Charge** has the shorter cooldown (20s) compared to the Thermal Bore (25s) [Breach Charge § Overview] [Thermal Bore § Overview]. Both gadgets are used by the **Light** build [Breach Charge § Overview] [Thermal Bore § Overview].

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
covers: Overview / Usage / Usage > Properties > Gadget (cite any of these sections of Breach Drill)
url: https://www.thefinals.wiki/wiki/Breach_Drill
Breach Drill
“Deployable that drills through surfaces and flashes the other side before detonating.”
Profile
Build: M Medium
Icon
Type: Utility
Unlock: 500
Stats
Cooldown: 15s
Ammo: 1
Technical
Environment Dmg: Over 2000
The Breach Drill is a Medium class gadget that can be attached to a surface to flash the other side before detonating to breach it.

[Usage]
The Breach Drill can be selected as one of three Gadgets of any Medium build loadout.
Once attached to a surface, the Breach Drill will begin drilling through. When completed, a flash will blind opponents on the other side, followed by an explosion that destroys the targeted surface.
Fully blinding an opponent will display a yellow X on the crooshair, while partially blinding displays a white one.
Breach drill can be placed on top of Goo . The explosion breaks a single goo piece, but the flash doesn't blind any opponents.
Equip Breach Drill: 
```
</details>

---

## m05 (multi)

**Question:** How do team sizes differ between Quick Cash and Power Shift?

**Reference:** Quick Cash is three teams of three (3v3v3); Power Shift is two teams of five (5v5).

**Agent answer:**

Quick Cash features 3v3v3 team sizes (three teams of three players) [Quick Cash § Overview], whereas Power Shift features 5v5 team sizes (two teams of five players) [Power Shift § Overview].

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
The gamemode was introduced in Season 3 . Prior to Season 9 , the gamemode was referred as World Tour and was a prime mode for casual play where weekly events that altered gameplay through special rules or modifiers took place. Before that change, the name "Cashout" refereed to a group of gamemodes with similar set of rules.

---

Result 5  cite as: [Ranked Cashout § Rules > Tournament Structure]
covers: Rules > Tournament Structure / Rules > Ways to Gain Cash (cite any of these sections of Ranked Cashout)
url: https://www.thefinals.wiki/wiki/Ranked_Cashout
The Tournament features 8 teams (24 contestants total) competing in a knockout bracket. The top 2 teams qualify for the next round, while the bottom 2 teams are eliminated.
- Knockout Round 1: 8 teams split into two matches (4 teams per match).
- Knockout Round 2: 4 remaining teams compete in one match.
- Final Round: The last 2 teams face off under rules similar to Head2Head , with Vaults worth $25,000. The first team to reach $50,000 wins the tourna
```
</details>

---

## m06 (multi)

**Question:** Which heals faster, the Healing Beam or the Healing Emitter?

**Reference:** The Healing Beam: 50 HP/s in its stats box (its Effects section says 46 HP/s) vs 10-15 HP/s for the Healing Emitter.

**Agent answer:**

The Healing Beam heals significantly faster than the Healing Emitter [Healing Beam § Stats > Effects] [Healing Emitter § Overview].

* **Healing Beam** (Medium specialization) heals at a rate of 46 to 50 health per second [Healing Beam § Stats > Effects] [Healing Beam § Overview].
* **Healing Emitter** (Heavy gadget) heals at a rate of 10 to 15 health per second [Healing Emitter § Overview].

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
The Healing Beam can be selected as the specialization gadget of any Medium build loadout. The gadget (together with the Defibrillator ) is specifically unavailable in Terminal Attack matches.
The gadget can be held like a weapon. To activate it, the user must be aiming at a teammate. Holding the primary trigger will heal them over time. If the opponent leaves gadget's range or the user's line of sight (such as by going behind a wall) for too long, the Healing Beam disconnects from them.

[Usage > Charge-Based Cooldown]
The Healing Beam has a battery charge indicated on the gadget as a cross shape that fills up as it is used. While the Healing Beam is not active, this charge reduces over time. If the display fills up completely, the gadget malfunctions and needs to cool down before healing again.
Equip Healing Beam: PC Q; PS R1; XBox RB; Key Specialization
Continuous healing (Hold): PS R2; XBox RT; Key Primary fire
```
</details>

---

## u01 (unanswerable)

**Question:** How much does the battle pass cost in Multibucks?

**Reference:** Not in the wiki snapshot: prices and the battle pass were not indexed.

**Agent answer:**

The wiki does not cover this.

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
Fortune Stadium is a medium sized arena that is split into several sectors separated by the void, making the traversal between them dangerous. Every sector features a building that forces contestants to go close quarters inside and rarely offers a clear sigh line. Arena rewards adaptability to traversal speed and methods as your opponents will try their best to gun you down as you are trying to reach their sector. It features a single Standard Issue variant with two time-of-day modifiers.

[Arena Variants > Standard Issue]
“A standard arena, ready for destruction.”

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
P
```
</details>

---

## u02 (unanswerable)

**Question:** Which team won The Grand Major 2025?

**Reference:** Not in the wiki snapshot: esports results were not indexed.

**Agent answer:**

The wiki does not cover this.

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
When a Cash Box comes into contact with one of the sliding panels on a Cashout Station, it's automatically absorbed and a cashout will begin. Contestants can either carry the Cash Box directly to the station or throw it in from a distance. The last team to hold the Cash Box before it is absorbed becomes the initial owner of the cashout.
Once the cashout is completed, the team that currently controls the Cashout Station is awarded the full value of the Cash Box .
While a cashout is active, it is owned by a single team. If that team remains the owner when the cashout completes, they are awarded the full cash value. Contestants from opposing teams can attempt to steal the cashout by interacting with the Cashout Station for a short duration.
Steal Cashout (Hold): PC E; PS △; XBox Y; Key Interact
Cashout durations are fixed, provided there is sufficient time remaining in the round. If there is not enough time left to complete a full cashout, up to one minute of overtime is added to allow it to finish.
- Cashout Duration in knockout rounds - 2:10
- Cashout Duration in the final round - 2:00

[Rules]
Classic Cashout Open Vaults, deposit Cash Boxes, and defen
```
</details>

---

## u03 (unanswerable)

**Question:** What PC graphics settings give the best FPS in THE FINALS?

**Reference:** Not in the wiki snapshot: no graphics-settings pages were indexed.

**Agent answer:**

The wiki does not cover this. The community wiki focuses on weapons, gadgets, specializations, builds, and game modes rather than PC graphics optimization or hardware settings.

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
Holding the primary trigger will prepare a high-velocity overhand throw. Holding the secondary trigger will prepare a low-velocity underhand throw. While preparing a throw, the gadget's trajectory is indicated up to the point where it bounces off a surface (or up to its mid-air detonation point). Swapping to a different item will cancel the throw. Releasing the trigger throws the gadget.
Equip Flashbang: PC 2 3 4; PS L1; XBox LB; Key Gadget
Prepare overhand throw (Hold) Overhand Throw (Release): PS R2; XBox RT; Key Primary fire
Prepare underhand throw (Hold) Underhand Throw (Release): PS L2; XBox LT; Key Secondary fire

---

Result 5  cite as: [Frag Grenade § Overview]
covers: Overview / Usage / Stats > Effects (cite any of these sections of Frag Grenade)
url: https://www.thefinals.wiki/wiki/Frag_Grenade
FRAG GRENADE
“Thrown projectile that explodes shortly after release; can be thrown underhand or overhand”
Profile
Build: L M H All
Icon
Type: Offensive
Unlock: Free
Stats
Cooldown: 20s
Ammo: 1
Technical
Damage: 165
Environment Dmg: 900
D
```
</details>

---

## u04 (unanswerable)

**Question:** In Point Break, what does the attacking team have to do to win?

**Reference:** Not in the indexed snapshot (the Point Break page is held out). After adding it: destroy all 9 Grand Vaults, 3 per phase over 3 phases.

**Agent answer:**

The wiki does not cover this. (There are no game modes named "Point Break" in the current wiki snapshot; modes include Cashout, Ranked Cashout, Power Shift, and Team Deathmatch.)

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
NOZOMI/CITADEL: Standard Issue
P.E.A.C.E. Center: Standard Issue
Seoul: Under Construction
Skyway Stadium: High Rise • Up Down Left Right
Starlight Hollow: Standard Issue
SYS$HORIZON: Standard Issue

---

Result 5  cite as: [Team Deathmatch § Overview]
covers: Overview / Objective / Elimination Rules / Maps (cite any of these sections of Team Deathmatch)
url: https://www.thefinals.wiki/wiki/Team_Deathmatch
Team Deathmatch
Overview
Short description: Eliminate opponents to earn cash
Length: Three Rounds (BO3)
Format: 5v5
Features: Unlimited respawn credits
Progression: World Tour
Eliminate Opponents Get more eliminations than the opponent team
First to $3,000 wins First team to win 2 rounds wins the game
Team Deathmatch (TDM) is a fast-paced Gamemode where two teams of five contestants compete to achieve the most eliminations in a best-of-three format. It was introduced as a Limited-Time Mode during Season 5 and later added permanently as a Quickplay mode with the release of Season 6 .

[Objective]
The obj
```
</details>

---

## u05 (unanswerable)

**Question:** What are the minimum PC system requirements to run THE FINALS?

**Reference:** Not in the wiki snapshot.

**Agent answer:**

The wiki does not cover this.

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
covers: Usage / Stats (cite any of these sections of Recurve Bow)
url: https://www.thefinals.wiki/wiki/Recurve_Bow
The Recurve Bow can be selected as the Weapon of any Light build loadout.
The trigger can be held down to prepare an arrow and draw back the string, which charges up its power over time. The maximum power is reached after charging for 0.49 seconds, at which point the string can be held down for any duration. The user cannot sprint while drawing an arrow.
Once the Recurve Bow has been charged up for at least a short moment, the trigger can be released to fire one arrow that damages an opponent, dealing damage based on its charge time and also dealing additional damage on headshots.
The secondary trigger can be used to zoom in slightly, though this does not affect the Recurve Bow's accuracy. Its accuracy also remains stable while moving and going airborne.
The weapon has infinite ammunition and does not need to reload.
Equip Recurve Bow: PC 1; PS △; XBox Y; Key Weapon
Draw bow (Hold) Fire shot (R
```
</details>

---

## u06 (unanswerable)

**Question:** How much damage does the Plasma Cutter deal to Heavy contestants?

**Reference:** There is no Plasma Cutter in the wiki snapshot; the agent should not invent one.

**Agent answer:**

The wiki does not cover this. There is no item named "Plasma Cutter" in THE FINALS Community Wiki.

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
The Heavy Build is a powerhouse: Though slow-moving, it is the most durable Build, designed for taking and holding ground. With the highest health pool, Heavies thrive in direct combat and controlling objectives but struggle with mobility.
Heavies bring devastating equipment to the battlefield, like the Charge 'N' Slam and RPG-7 , capable of damaging enemies and obliterating structures. They also possess a wide array of defensive utility, like the Barricade , Dome Shield , and Mesh Shield , all of which allow them to defend objectives and their teammates. Additionally, gadgets like the Lockbolt and Anti-Gravity Cube let them manipulate enemy movement and disrupt objectives.
Heavy contestants favor close to mid-range weapons, from more traditional options like the M60 and Lewis Gun to wildcards like the MGL32 . They can also be seen with strong melee weapons, from the heavy-hitting Sledgehammer and swift Spear , or even a Flamethrower for close-range pyrotechnics.
Due to their size, Heavies cannot crouch or slide 
```
</details>
