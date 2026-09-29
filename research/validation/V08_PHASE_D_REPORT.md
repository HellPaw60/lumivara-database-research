# V0.8 PHASE D — COMBAT / MONSTER / BOSS MECHANICS DEEP AUDIT

## Source
| Field | Value |
|---|---|
| Bundle (V0.7) | `main-DEXZ0AP0.js` / `items-CvFgs761.js` |
| Bundle (V0.8) | `main-CFj0fJNd.js` / `items-DqMVEwxd.js` |
| Baseline | `CkIS7ST6` / 688 |
| Observation | `CMg3B3wG` / 730 |

---

## 1. MONSTER DAMAGE REDUCTION — FINDING

### Changelog Claim
- Monster damage reduced by level
- Lv100+: ~50% reduction
- Lv200+: ~35-40% reduction
- Early maps: 20-30% reduction
- Crowned boss damage ×2 species (was ×2.5)

### Client Evidence
```
SEARCHED: main-CFj0fJNd.js, main-DEXZ0AP0.js, items-DqMVEwxd.js, items-CvFgs761.js
FOUND: NONE
```

The `damageMonster` function exists in both bundles but contains **no level-based scaling**:
```javascript
damageMonster(c,x,E=1,T="atk",M,u=!1,y){
  // Basic attack calc → skill calc → pierce → damage
  // No monster level multiplier
}
```

**Conclusion**: SERVER_SIDE_ONLY — No client implementation found.

---

## 2. MONSTER ACCURACY / FLEE — FINDING

### Changelog Claim
- Normal mob max dodge ≈ 0.50
- Boss max dodge ≈ 0.40
- Monster accuracy increased

### Client Evidence
```
SEARCHED: Qn constant, Jr function
FOUND:
  Qn = 0.2 (FLEE cap from equipment + cards, not dodge cap)
  Jr(A,e) = min(re.max, max(re.min, re.even + (A-e) * re.perPoint))
```

The `Jr` function calculates **player dodge chance**, not monster accuracy. It uses:
- `re.even = 0.9` (base dodge at equal level)
- `re.perPoint = 0.005` (per level difference)
- `re.min = 0.5` (minimum dodge)
- `re.max = 1.0` (maximum dodge)

**No monster accuracy modifier found in client.**

**Conclusion**: SERVER_SIDE_ONLY — Monster accuracy/FLEE changes not in client.

---

## 3. HIT / MISS REGRESSION — FINDING

### Player Dodge vs Monster
```
EXISTING FORMULA (unchanged):
  Jr(A,e) = min(1.0, max(0.5, 0.9 + (playerLevel - mobLevel) * 0.005))
  
EXISTING CONSTANT (unchanged):
  Qn = 0.2 (FLEE equipment cap)
```

### Boss Dodge Cap
```
EXISTING FORMULA (unchanged):
  Boss dodge uses same Jr function
  No separate boss dodge cap in client code
```

**Conclusion**: CLIENT DOES NOT CONTAIN boss-specific dodge cap. Any caps are server-side.

---

## 4. CROWNED BOSS EVERY CHANNEL — FINDING

### Changelog Claim
- Every channel has 1 Crowned boss
- Respawns after 1 hour
- Random nest selection

### Client Evidence
```
SEARCHED: spawnTable, bossTable, channel logic
FOUND: NONE
```

No boss spawn table, no channel selection logic, no respawn timer found in client bundles.

The `crowned` key only appears in **drop tables** (boss_card rate), not spawn logic.

**Conclusion**: SERVER_SIDE_ONLY — Boss spawn logic entirely server-authoritative.

---

## 5. WORLD BOSS REGRESSION — FINDING

### Historical (V0.7)
- Max 5 bosses per map
- Channel 1 only (per changelog)
- Respawn variable `zi`
- Home area `Ao`

### Current (V0.8)
- Every channel has Crowned boss
- Respawn 1 hour
- Random nest

**Client contains NO spawn table.** Both old and new behaviors are server-side.

---

## 6. DAMAGE PIPELINE — FINDING

### Player → Monster (unchanged)
```
ATK/MATK → basic/skill → crit → pierce/mpierce → target DEF/MDEF → final damage
```

### Monster → Player (unchanged in client)
```
mobDamage → shield → DEF/MDEF → incoming factor → final damage
```

**No new level-based modifier found in client.**

---

## 7. GAP RESOLUTION

### GAP-015 — Monster Damage Reduction
**Status**: OPEN → **SERVER_SIDE_ONLY**

| Evidence | Finding |
|---|---|
| Client search | No level-based damage scaling |
| Changelog | Claims reduction by level |
| Runtime | Cannot verify from client |
| Conclusion | Server authoritative |

### GAP-016 — Boss Every Channel
**Status**: OPEN → **SERVER_SIDE_ONLY**

| Evidence | Finding |
|---|---|
| Client search | No spawn table / channel logic |
| Changelog | Claims every channel, 1hr respawn |
| Runtime | Cannot verify from client |
| Conclusion | Server authoritative |

---

## 8. FORMULA DATABASE — NO NEW FORMULAS

No new formulas added in Phase D. All combat/monster/boss changes from CMg3B3wG are **server-side only** with no client implementation.

**Formula count remains 47.**

---

## 9. SERVER-EQUIVALENCE STATUS

| Mechanic | Client | Runtime | Server Equivalence |
|---|---|---|---|
| Monster damage reduction | NONE | — | UNKNOWN |
| Monster accuracy increase | NONE | — | UNKNOWN |
| Boss every channel | NONE | — | UNKNOWN |
| Boss respawn 1hr | NONE | — | UNKNOWN |
| Random nest | NONE | — | UNKNOWN |
| Player dodge cap | Jr() | — | LIKELY |
| FLEE equipment cap | Qn=0.2 | — | LIKELY |

---

## 10. CONCLUSION

Phase D complete. Key findings:
1. **All monster/boss changes in CMg3B3wG are server-side only**
2. **No new formulas added** (count remains 47)
3. **GAP-015 and GAP-016 remain OPEN** (server-side)
4. **Client evidence is conclusive**: these mechanics are NOT in client bundles

**Phase D complete.** Siap untuk Phase E (Drop) kapan pun LO mau lanjut.
