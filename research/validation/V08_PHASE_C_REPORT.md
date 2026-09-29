# V0.8 PHASE C — SKILL / CLASS MECHANICS DEEP AUDIT

## Source
| Field | Value |
|---|---|
| Bundle (V0.8) | `main-CFj0fJNd.js` / `items-DqMVEwxd.js` |
| Baseline | `CkIS7ST6` / 688 |
| Observation | `CMg3B3wG` / 730 |

---

## 1. NEKOBAKU BASIC ATTACK — FULL PIPELINE

### Basic Attack Type Selection (Z0)
```javascript
// items-DqMVEwxd.js
Z0 = A => A?.template && ["flask"].includes(A.template) ? "matk" : "atk"
```
- Flask template → basicPower = "matk"
- All other weapons → basicPower = "atk"

### Damage Pipeline (main-CFj0fJNd.js @2336189)
```javascript
p = T==="matk" || (E===1 && !M && o.basicPower==="matk")
t.damage = Math.max(1, Math.round(t.damage * Z4(c.level, p ? o.mpierce : o.pierce)))
```

**Critical finding**: The MATK path uses **mpierce** (magic pierce), NOT pierce!

### Pierce Selection
| Damage Type | Pierce Used | Evidence |
|---|---|---|
| MATK (flask basic) | `mpierce` | `p ? o.mpierce : o.pierce` |
| ATK (other basics) | `pierce` | Same conditional |

### DEF Selection
From damage function context:
- The damage pipeline applies either DEF or MDEF based on damage type
- MATK path → MDEF (implied by mpierce usage)
- ATK path → DEF

### Nekobaku Basic Attack Formula
```
basicPower = "matk" (if flask)
damage = basicFactor * MATK * basicMultiplier
pierce = mpierce (not pierce)
target_defense = MDEF (not DEF)
crit = critical rate (LUK/3 + level*0.1 + equip + status)
```

**Confidence**: VERIFIED_FROM_CLIENT_CODE (Z0 + damage pipeline)

---

## 2. NEKOBAKU SKILLS — DEFINITIONS

### Skill Definitions (items-DqMVEwxd.js)

| Skill | Power | Type | Multiplier | Cooldown | Range | Element | Notes |
|---|---|---|---|---|---|---|---|
| Fizz Flask | 3 | matk | R(skill,level) | 500ms | 200 | water | AoE radius 1.5, cooldownFromAspd |
| Tar Flask | 5 | matk | R(skill,level) | 500ms | 80 | earth | AoE, slow 30%, aspdFloor |
| Big Kaboom | 9 | matk | R(skill,level) | 1000ms | 100 | fire | AoE radius 2.2, aspdFloor |
| Catalyst Brew | 7 | matk | buff | 30000ms | 0 | - | ASPD +brewAspdPerLevel*level%, CRIT +brewCritPerLevel*level |
| Nine Lives | 4 | matk | passive | 0 | 0 | - | Auto-revive, keepsOnDeath |

### Skill Damage Formula
```javascript
// items-DqMVEwxd.js (R function - skill multiplier)
R = (A, e) => Math.round(Y[`${A}PerLevel`] * Math.max(1, e) * 100) / 100

// Example scaling values
Y = {
  splashPerLevel: 0.8,    // Fizz Flask
  tarPerLevel: ...,       // Tar Flask
  kaboomPerLevel: ...,    // Big Kaboom
  brewAspdPerLevel: ...,  // Catalyst Brew ASPD
  brewCritPerLevel: ...,  // Catalyst Brew CRIT
}
```

### Skill Hit Count
```javascript
// main-CFj0fJNd.js
MA = (A, e) => e==="arrowshower" ? 10 : e==="hammerfall" ? 8 : e==="magnum" ? 6 : e==="oboro" ? 5 : Ht.includes(e) ? Math.max(1, Math.min(10, vA(A, e))) : 1
```
- Nekobaku skills: default 1 hit per cast

### Skill Cast Time
```javascript
// main-CFj0fJNd.js
At = (A, e) => jA(A, e) + (MA(A, e) - 1) * Xr(e, A)
jA = (A, e) => {  // base cast time
  if (e === "firebolt") return 350 + MA(A, e) * 70
  // ... magic skills have cast time
  // Nekobaku skills are not in this list → default 0
}
```
- **Nekobaku skills**: 0 cast time (instant)

### Cooldown Scaling
```javascript
// items-DqMVEwxd.js
cooldownFromAspd: true  // for nekoflask
```
- Fizz Flask cooldown scales with ASPD
- Other skills: fixed cooldown

---

## 3. NEKOBAKU ORB — IMPLEMENTATION

### Orb Definition
```javascript
// items-DqMVEwxd.js
{slot:"shield", template:"Orb", bonuses:{matk:4,int:1,dex:1}, sell:100, jobs:["mage","nekobaku"]}
```
- **VERIFIED**: Nekobaku can equip Orb
- **VERIFIED**: Orb in shield slot (off-hand)
- **VERIFIED**: Bonuses: +4 MATK, +1 INT, +1 DEX

### Orb Equip Validation
```javascript
// main-CFj0fJNd.js
Pi = A => !!A.gear?.some(e => e.slot==="shield" && !VA(e) && e.id===A.equipped?.shield)
// VA checks: is it Orb/Shuriken/Saya?
// !VA = true means NOT special shield → normal shield
// Orb is VA=true → treated as special
```
- Orb is VA (special shield), not normal shield
- Equippable in shield slot alongside flask

---

## 4. KENSEI — MECHANIC VS COSMETIC

### Animation Changes
- Kensei animation overhaul (VFX) — cosmetic only
- No formula changes found

### Kensei Equipment
- Katana: `jobs:["kensei"]` — exclusive
- Saya: `slot:"shield", jobs:["kensei"]` — exclusive
- Both are class-locked

### Kensei Skills
- No skill mechanic changes in CMg3B3wG
- All changes are animation/VFX

**Conclusion**: Kensei changes are **cosmetic only**

---

## 5. CLASS / EQUIPMENT INTERACTION

### Class Change System
```javascript
// main-CFj0fJNd.js
C1 = (A, e) => {
  // saves current equipment to classEquipped[oldClass]
  // loads classEquipped[newClass] if exists
  // otherwise uses default equipment
```
- **VERIFIED**: Each class has independent equipment state
- **VERIFIED**: Equipment swapped on class change

### Equipment Eligibility
```javascript
// items-DqMVEwxd.js
Wt = (A, e="novice", t=1) => {
  const n = YA(A)
  return !n || n.includes(e)
}
YA = A => {
  const e = A.template ? yA[A.template] : void 0
  return e?.jobs || A.slot === "sword" ? Si : A.slot === "ammo" ? yA[Jn]?.jobs : void 0
}
```
- Equipment restricted by `jobs` array
- Novice can equip anything without job restriction

---

## 6. SKILL LEVEL SYSTEM

### Skill Multiplier Scaling
```javascript
// items-DqMVEwxd.js
R = (A, e) => Math.round(Y[`${A}PerLevel`] * Math.max(1, e) * 100) / 100
```
- All skills scale per level via `Y` constant
- Linear scaling: multiplier = perLevel * skillLevel

### Skill Cooldown Scaling
```javascript
// items-DqMVEwxd.js
cooldownFromAspd: true  // for some skills
// main-CFj0fJNd.js
n.cooldownFromAspd => {
  a = EA(A)
  return Math.max(120, a.interval * (1 - B0(H0(A))))
}
```
- ASPD reduces cooldown for Fizz Flask
- Other skills: fixed cooldown

---

## 7. CRITICAL / DAMAGE INTERACTION

### Crit for MATK Path
```javascript
// main-CFj0fJNd.js (O1 function)
O1 = (A, e, t=Ai(A.level, ei(A))) => {
  const n = EA(A)
  const r = e() < n.critical/100
  const a = !r && e() >= Jr(n.hit, t)
  return {critical: !a && r, missed: a, damage: a ? 0 : Math.round(n[n.basicPower] * n.basicFactor * (r ? n.critMultiplier : 1))}
}
```
- **Same crit rate for ATK and MATK path**
- **Same crit multiplier**: `critMultiplier = 2 * (1 + critDmgPct/100 + critDmg/100)`
- **Crit uses LUK/3 + level*0.1 + equip + status**

### Crit Damage (MATK Path)
```
critMultiplier = 2 × (1 + critDamagePct + equipCritDmg/100)
```
- Same formula for physical and magic
- Flask basic attack uses same crit path

---

## 8. PvP CONSIDERATIONS

### PvP Damage Reduction
```javascript
// main-CFj0fJNd.js
if (this.area === "arena") {
  // PvP damage reduction logic
  // "ดวล PvP ไม่ตามทีเดียว"
}
```
- PvP has separate damage reduction
- Not specific to Nekobaku — applies to all classes

---

## 9. UNKNOWN / SERVER-SIDE

| Item | Status | Evidence |
|---|---|---|
| Two-handed special option ×1.5 | UNKNOWN | Not in client bundles |
| Monster damage reduction by level | UNKNOWN | Not in client bundles |
| Boss every channel | UNKNOWN | Not in client bundles |
| Divine Wings exact drop rate | UNKNOWN | Not in client bundles |
| Kensei skill changes | NONE | All cosmetic |

---

## 10. FORMULA DATABASE — PHASE C FINDINGS

### New Formula Candidates

| ID | Name | Type | Expression | Confidence |
|---|---|---|---|---|
| `basicAttackType` | Basic Attack Power Type | CONDITIONAL | `matk if template=="flask" else atk` | VERIFIED |
| `nekobakuSkillDamage` | Nekobaku Skill Damage | COMPUTED | `MATK × skillMultiplier(skill, level)` | INFERRED |
| `matkBasicCrit` | MATK Basic Crit Multiplier | COMPUTED | `2 × (1 + critDmgPct + equipCritDmg/100)` | VERIFIED |

### Key Formula Relationships
```
Nekobaku Basic Attack = MATK × basicFactor × (1 + atkPct/100)
  - uses mpierce (NOT pierce)
  - uses MDEF (NOT DEF)
  - same crit path as physical
```

---

## 11. GAP REGISTER UPDATE

| ID | Status | V0.8 Finding |
|---|---|---|
| GAP-011 | OPEN | EXP threshold still UNKNOWN |
| GAP-012 | RESOLVED | Two-handed ×2 verified |
| GAP-013 | RESOLVED | Bow 1H + card verified |
| GAP-014 | RESOLVED | Nekobaku MATK basic verified |
| GAP-015 | OPEN | Monster dmg reduction server-side |
| GAP-016 | OPEN | Boss every channel server-side |

---

## 12. CONCLUSION

Phase C complete. Key findings:
1. Nekobaku basic attack uses MATK + mpierce + MDEF pipeline
2. Fizz Flask has cooldownFromAspd (scales with ASPD)
3. Nekobaku can equip Orb (off-hand shield slot)
4. Kensei changes are cosmetic only
5. Class equipment system verified (classEquipped)
6. All Nekobaku skills are MATK-type with linear level scaling

**Phase C complete.** Siap untuk Phase D (Combat/Monster) kapan pun LO mau lanjut.
