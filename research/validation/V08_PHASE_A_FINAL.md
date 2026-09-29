# V0.8 PHASE A — CHANGELOG DELTA AUDIT (COMPLETE)

## Bundle Evidence Verification

### Source
| Field | Value |
|---|---|
| Bundle | `main-CFj0fJNd.js` / `items-DqMVEwxd.js` |
| Retrieved | 2026-09-29 15:36 |
| Baseline | `CkIS7ST6` / 688 entries |
| Observation | `CMg3B3wG` / 730 entries |
| Delta | +42 unique entries |

### Evidence-Based Reclassification

| # | Entry | Initial Class | Final Class | Evidence | Confidence |
|---|---|---|---|---|---|
| 1 | `two-handed-x2` | EQUIPMENT ✓ | EQUIPMENT ✓ | `Ee()` detects two-handed, `Ar=2` multiplier | VERIFIED_FROM_CLIENT_CODE |
| 2 | `two-handed-special-option` | EQUIPMENT ✓ | EQUIPMENT ✓ | Refine system applies to two-handed | VERIFIED_FROM_CLIENT_CODE |
| 3 | `bow-one-handed` | EQUIPMENT ✓ | EQUIPMENT ✓ | Bow NOT in Ee() list (one-handed), card slot = 1 | VERIFIED_FROM_CLIENT_CODE |
| 4 | `quiver-archer-only` | EQUIPMENT ✓ | EQUIPMENT ✓ | `ra()` checks bow template, archer-only restriction | VERIFIED_FROM_CLIENT_CODE |
| 5 | `nekobaku-matk-basic` | SKILL ✓ | SKILL ✓ | `Z0()` branches flask→matk, main bundle `basicPower=="matk"` | VERIFIED_FROM_CLIENT_CODE |
| 6 | `nekobaku-orb` | SKILL ✓ | SKILL ✓ | Orb `jobs:["mage","nekobaku"]` | VERIFIED_FROM_CLIENT_CODE |
| 7 | `class-gear-sets` | EQUIPMENT ✓ | EQUIPMENT ✓ | `classEquipped` system exists | VERIFIED_FROM_CLIENT_CODE |
| 8 | `nekobaku-skill-rework` | SKILL ✓ | SKILL ✓ | Skill definitions in items bundle | OBSERVED (changelog describes specifics) |
| 9 | `nekobaku-skill-effects` | SKILL ✓ | WORLD/VISUAL | VFX only, no formula change | Reclassified: NON-MECHANICS |
| 10 | `divine-wings-1-in-100k` | DROP ✓ | DROP ✓ | `divine_wings` in items bundle (special slot) | INFERRED (rate server-side) |
| 11 | `boss-every-channel` | BOSS/SPAWN ✓ | BOSS/SPAWN ✓ | Not in client (server-side) | UNKNOWN |
| 12 | `monster-damage-accuracy` | COMBAT ✓ | COMBAT ✓ | Not in client (server-side) | UNKNOWN |
| 13 | `lock-allows-refine-market` | ECONOMY ✓ | ECONOMY ✓ | Lock + refine interaction exists | OBSERVED |
| 14 | `gold-exchange-closes-before-launch` | ECONOMY ✓ | UI/UX | Server maintenance, not game mechanic | Reclassified: NON-MECHANICS |
| 15 | `launch-gold-carry` | ECONOMY ✓ | UI/UX | Server migration, not game mechanic | Reclassified: NON-MECHANICS |
| 16 | `bot-long-cooldown-first` | BOT ✓ | BOT | Bot AI behavior | OBSERVED |
| 17 | `bot-instant-next-target` | BOT ✓ | BOT | Bot AI behavior | OBSERVED |
| 18 | `bot-approach-skill-resend` | BOT ✓ | BOT | Bot AI behavior | OBSERVED |
| 19 | `bot-auto-coat-fix` | BOT ✓ | BOT | Bot AI behavior | OBSERVED |
| 20 | `kensei-new-animations` | SKILL ✓ | WORLD/VISUAL | Cosmetic only | Reclassified: NON-MECHANICS |
| 21 | `quiver-rename` | EQUIPMENT ✓ | UI/UX | Rename only | Reclassified: NON-MECHANICS |

## Final Classification (42 entries total, not 45)

| Category | Count | Notes |
|---|---|---|
| EQUIPMENT | 5 | two-handed ×2, bow 1H+card, quiver restriction, class gear sets |
| SKILL | 3 | nekobaku MATK basic, orb, skill rework |
| BOT/BEHAVIOR | 4 | All AI logic |
| BOSS/SPAWN | 1 | boss every channel |
| COMBAT/MONSTER | 1 | monster dmg/accuracy |
| DROP | 1 | Divine Wings rate |
| ECONOMY | 1 | lock refine/market |
| **Total Mechanics-Relevant** | **16** | (down from 21) |
| UI/UX | 15 | |
| WORLD/VISUAL | 7 | |
| BUG/FIX | 4 | |
| **Total Non-Mechanics** | **26** | |
| **Grand Total** | **42** | |

## Key Client Implementation Evidence

### 1. Two-Handed Weapon Detection
```javascript
// items-DqMVEwxd.js
Ee = A => A.slot === "sword" && A.template && ["staff","quarterstaff","dagger_pair","hammer"].includes(A.template)
Ar = 2  // two-handed stat multiplier
Dt = A => Se(A) ? 0 : Ee(A) ? 2 : 1  // card slots: two-handed=2, one-handed=1
```

### 2. Bow = One-Handed
```javascript
Jn = "bow"
Zn = A => Ee(A)  // → FALSE for bow (bow NOT in Ee list)
// Therefore: bow is ONE-HANDED, gets 1 card slot, can equip shield/orb/quiver
```

### 3. Nekobaku Basic Attack Uses MATK
```javascript
// main-CFj0fJNd.js (Z0 function / basicPower branch)
Z0 = A => A?.template && ["flask"].includes(A.template) ? "matk" : "atk"
// In damage pipeline: p = (T==="matk" || E===1 && !M && o.basicPower==="matk")
```

### 4. Nekobaku Can Equip Orb
```javascript
// items-DqMVEwxd.js
{slot:"shield", template:"Orb", bonuses:{matk:4,int:1,dex:1}, jobs:["mage","nekobaku"]}
```

### 5. Class-Specific Equipment Sets
```javascript
// main-CFj0fJNd.js
C1 = (A, e) => {  // class change function
  // saves current equipment to classEquipped[oldClass]
  // loads classEquipped[newClass] if exists
  // otherwise uses default equipment
```

### 6. Quiver/Ammo Logic
```javascript
// main-CFj0fJNd.js
ra = A => jt(A)?.template === Jn  // true if bow equipped
// Ammo slot requires bow: "ใส่ซองธนูไม่ได้ · ต้องถือ Bow ก่อน"
// notifyQuiverEmpty() when ammo count = 0
```

### 7. Divine Wings Special Slot
```javascript
// items-DqMVEwxd.js
Ua = new Set(["divine_wings"])
Se = A => !!A?.template && Ua.has(A.template)
// Divine Wings in special "wings" slot, not standard equipment
```

## Formula Database Updates (V0.8 Phase A)

| Change | Count |
|---|---|
| Total formulas | 38 → **44** |
| COMPUTED_FORMULA | 27 → **29** |
| CONDITIONAL_RULE | 3 → **6** |
| LOOKUP_TABLE | 3 → **4** |
| MECHANIC_DEFINITION | 5 |
| **New formulas** | **6** |

### New Formulas

| ID | Name | Type | Expression | Source |
|---|---|---|---|---|
| `isTwoHanded` | Two-Handed Detection | CONDITIONAL | `item.slot=="sword" && ["staff","quarterstaff","dagger_pair","hammer"].includes(item.template)` | Ee() items-DqMVEwxd.js |
| `twoHandedMultiplier` | Two-Handed Stat Multiplier | COMPUTED | `2 if isTwoHanded else 1` | Ar=2 |
| `isBow` | Bow Classification (One-Handed) | CONDITIONAL | `item.slot=="sword" && item.template=="bow"` | Jn="bow" |
| `cardSlotCount` | Card Slot Count | COMPUTED | `0 if isWings else 2 if isTwoHanded else 1` | Dt() |
| `basicAttackType` | Basic Attack Power Type | CONDITIONAL | `"matk" if item.template=="flask" else "atk"` | Z0() main-CFj0fJNd.js |
| `orbEquipClasses` | Orb Equippable Classes | LOOKUP | `["mage", "nekobaku"]` | Orb.jobs |

| ID | Question | Current Status | Next Step |
|---|---|---|---|
| GAP-011 | EXP threshold per level | UNKNOWN | Runtime EMP measurement |
| GAP-012 | Two-handed ×2 exact formula | VERIFIED | Add to formula DB |
| GAP-013 | Bow one-handed + card slot | VERIFIED | Add to formula DB |
| GAP-014 | Nekobaku MATK basic formula | VERIFIED | Add to formula DB |
| GAP-015 | Monster damage reduction by level | INFERRED | Server-side or client? |
| GAP-016 | Crowned boss spawn every channel | INFERRED | Server-side |

## Conclusion

Phase A complete. 42 delta entries classified. 7 entries have VERIFIED client evidence. 3 entries reclassified from mechanics to non-mechanics (VFX, rename, server maintenance). 16 mechanics-relevant entries remain for Phase B-G investigation.
