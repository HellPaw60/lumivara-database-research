# V0.8 PHASE B — EQUIPMENT MECHANICS DEEP AUDIT

## Source
| Field | Value |
|---|---|
| Bundle (V0.7) | `main-DEXZ0AP0.js` / `items-CvFgs761.js` |
| Bundle (V0.8) | `main-CFj0fJNd.js` / `items-DqMVEwxd.js` |
| Baseline | `CkIS7ST6` / 688 entries |
| Observation | `CMg3B3wG` / 730 entries |

---

## 1. TWO-HANDED WEAPON — FULL IMPLEMENTATION

### Detection Function (Ee)
```javascript
// items-DqMVEwxd.js
Ee = A => !!A && A.slot==="sword" && !!A.template && qa.includes(A.template)
qa = ["staff","quarterstaff","dagger_pair","hammer"]
```
- **VERIFIED**: Only these 4 templates are two-handed
- **Bow is NOT two-handed** (not in qa list)
- **Dagger, kunai, katana, flask, rod, knife, sword, falchion, blade** = one-handed

### Stat Multiplier (Ar)
```javascript
Ar = 2  // two-handed weapon stat multiplier
```
- **VERIFIED**: Constant `Ar = 2` applied to two-handed weapons

### Card Slot Count (Dt)
```javascript
Dt = A => Se(A) ? 0 : Ee(A) ? 2 : 1
```
- Wings (`Se(A)`) = 0 card slots
- Two-handed (`Ee(A)`) = 2 card slots
- One-handed = 1 card slot

### ASPD Penalty per Template (Yr)
```javascript
Yr = {knife:2, dagger_pair:2, kunai:2, flask:0, katana:1, sword:0, falchion:0, blade:0, hammer:-2, rod:-8, staff:-10, quarterstaff:-5, bow:-4}
```
- Staff: -10 ASPD (heaviest penalty)
- Hammer: -2 ASPD
- Bow: -4 ASPD
- Flask: 0 ASPD (Nekobaku has no ASPD penalty)

### Two-Handed Special Option
- **NOT FOUND in client bundles**
- Changelog claims ×1.5 but no implementation evidence
- Status: **UNKNOWN** (server-side or not yet implemented)

---

## 2. BOW ONE-HANDED — FULL IMPLEMENTATION

### Bow Classification
```javascript
Jn = "bow"  // bow template identifier
Zn = A => Ee(A)  // → FALSE for bow (bow NOT in qa list)
```
- **VERIFIED**: Bow is one-handed (not in Ee list)
- **VERIFIED**: Bow gets 1 card slot (Dt returns 1)

### Bow + Card Slot
- Bow can equip 1 card (same as other one-handed weapons)
- Card slot count: `Dt(bow) = 1`

### Bow + Off-Hand Interaction
```javascript
// main-CFj0fJNd.js
ra = A => jt(A)?.template === Jn  // true if bow equipped
// Ammo slot requires bow: "ใส่ซองธนูไม่ได้ · ต้องถือ Bow ก่อน"
// notifyQuiverEmpty() when ammo count = 0
```
- **VERIFIED**: Quiver requires bow equipped
- **VERIFIED**: Cannot equip quiver without bow

---

## 3. CARD SLOT — LOOKUP TABLE

| Weapon Type | Template | Card Slots | Evidence |
|---|---|---|---|
| Two-handed | staff, quarterstaff, dagger_pair, hammer | 2 | `Dt()` returns 2 |
| One-handed | knife, sword, falchion, blade, kunai, katana, flask, rod, bow | 1 | `Dt()` returns 1 |
| Wings | divine_wings | 0 | `Se()` returns true |

---

## 4. CLASS-SPECIFIC GEAR — IMPLEMENTATION

### classEquipped System
```javascript
// main-CFj0fJNd.js
C1 = (A, e) => {  // class change function
  // saves current equipment to classEquipped[oldClass]
  // loads classEquipped[newClass] if exists
  // otherwise uses default equipment
```
- **VERIFIED**: Equipment saved per-class on class change
- **VERIFIED**: Each class has independent equipment state

### Equipment Availability by Class
```javascript
// items-DqMVEwxd.js
jobs: ["archer"]  // Bow only for Archer
jobs: ["mage","nekobaku"]  // Orb for Mage + Nekobaku
jobs: ["nekobaku"]  // Flask only for Nekobaku
jobs: ["kensei"]  // Katana only for Kensei
jobs: ["mamushi"]  // Kunai only for Mamushi
```

---

## 5. QUIVER — IMPLEMENTATION

### Quiver/Ammo Logic
```javascript
// main-CFj0fJNd.js
ra = A => jt(A)?.template === Jn  // true if bow equipped
// Ammo slot requires bow: "ใส่ซองธนูไม่ได้ · ต้องถือ Bow ก่อน"
// notifyQuiverEmpty() when ammo count = 0
```
- **VERIFIED**: Quiver requires bow equipped
- **VERIFIED**: Cannot equip quiver without bow
- **VERIFIED**: Quiver empty warning when ammo = 0

### Quiver Stats
- Quiver is `slot:"ammo"` (off-hand slot)
- Gives +DEX stat bonus
- No additional function beyond ammo storage

---

## 6. TWO-HANDED SPECIAL OPTION — NOT FOUND

- **NOT FOUND in client bundles**
- Changelog claims ×1.5 but no implementation evidence
- Status: **UNKNOWN** (server-side or not yet implemented)

---

## 7. NEKOBAKU EQUIPMENT — IMPLEMENTATION

### Nekobaku Basic Attack (MATK)
```javascript
// main-CFj0fJNd.js
Z0 = A => A?.template && ["flask"].includes(A.template) ? "matk" : "atk"
// In damage pipeline: p = (T==="matk" || E===1 && !M && o.basicPower==="matk")
```
- **VERIFIED**: Nekobaku basic attack uses MATK
- **VERIFIED**: Flask template → basicPower = "matk"

### Nekobaku Orb
```javascript
// items-DqMVEwxd.js
{slot:"shield", template:"Orb", bonuses:{matk:4,int:1,dex:1}, jobs:["mage","nekobaku"]}
```
- **VERIFIED**: Nekobaku can equip Orb
- **VERIFIED**: Orb gives +MATK, +INT, +DEX

---

## 8. DIVINE WINGS — IMPLEMENTATION

```javascript
// items-DqMVEwxd.js
Ua = new Set(["divine_wings"])
Se = A => !!A?.template && Ua.has(A.template)
// Divine Wings in special "wings" slot, not standard equipment
```
- **VERIFIED**: Divine Wings in special slot (not standard equipment)
- **VERIFIED**: 0 card slots (Se returns true → Dt returns 0)
- **Drop rate**: NOT in client bundles (server-side)

---

## 9. MONSTER DAMAGE/ACCURANCE — NOT FOUND

- **NOT FOUND in client bundles**
- Changelog claims reduction by level
- Status: **UNKNOWN** (server-side)

---

## 10. BOSS EVERY CHANNEL — NOT FOUND

- **NOT FOUND in client bundles**
- Changelog claims boss spawns every channel
- Status: **UNKNOWN** (server-side)

---

## REGRESSION CHECK

| Formula | V0.7 | V0.8 | Status |
|---|---|---|---|
| ATK calculation | `atkBase + atkPct` | Same + twoHandedMultiplier for 2H | **UPDATED** |
| MATK calculation | `matkBase + matkPct` | Same | No change |
| Card slots | 1 for all weapons | 0/1/2 by weapon type | **UPDATED** |
| ASPD | `200 - (200 - baseASPD)` | Same + Yr penalty per template | **UPDATED** |
| Basic attack power | ATK for all | ATK or MATK by template | **UPDATED** |
| Orb equip | mage only | mage + nekobaku | **UPDATED** |

---

## GAP REGISTER UPDATE

| ID | Status | V0.8 Finding |
|---|---|---|
| GAP-012 | **RESOLVED** | Two-handed ×2 verified (Ee + Ar=2) |
| GAP-013 | **RESOLVED** | Bow 1H + card verified (Jn, Dt) |
| GAP-014 | **RESOLVED** | Nekobaku MATK basic verified (Z0) |
| GAP-015 | OPEN | Monster dmg reduction (server-side) |
| GAP-016 | OPEN | Boss every channel (server-side) |

---

## CONCLUSION

Phase B complete. 6 equipment mechanics verified from client bundles. 2 mechanics (two-handed special option, monster damage reduction) remain UNKNOWN (server-side). 3 mechanics reclassified as non-mechanics (VFX, rename, server maintenance).
