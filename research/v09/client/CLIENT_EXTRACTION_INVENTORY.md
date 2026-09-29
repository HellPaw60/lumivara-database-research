# V0.9 PHASE A — CLIENT EXTRACTION INVENTORY

## Summary

| Metric | Value |
|---|---|
| Bundles analyzed | 6 |
| Total data structures | 259 |
| Large structures (>1000 chars) | 79 |
| Total characters | ~1,500,000 |
| Bundle with most data | main-CFj0fJNd.js (157 structures) |

---

## Bundle Breakdown

### 1. main-CFj0fJNd.js (V0.8 main bundle)
- **157 data structures** (88 arrays, 69 objects)
- **79 large structures** requiring analysis

### 2. items-DqMVEwxd.js (V0.8 items bundle)
- **85 data structures** (47 arrays, 38 objects)

### 3. party-BnJKGOnI.js (party system)
- **15 data structures** (7 arrays, 8 objects)

### 4. language-Dz8VbPNM.js (localization)
- **1 data structure** (1 object, 73,694 chars)

### 5. rarity-D7SWm6O3.js (rarity system)
- **0 data structures** (logic only)

### 6. changelog-notice-BKeFrGHU.js (changelog)
- **1 data structure** (1 array)

---

## Large Data Structures (main-CFj0fJNd.js)

| Name | Type | Size | Domain | Status |
|---|---|---|---|---|
| `Kk` | array | 51,934 | Guild/UI | Not analyzed |
| `t` | array | 46,942 | Inventory/UI | Not analyzed |
| `w` | object | 44,617 | Ground items | Not analyzed |
| `t` | array | 37,270 | Animation | Not analyzed |
| `v7` | array | 32,368 | Direction/NPC | Not analyzed |
| `uT` | array | 30,508 | Effects UI | Not analyzed |
| `i` | array | 29,073 | Guest account | Not analyzed |
| `Bo` | array | 26,415 | Emotes | Not analyzed |
| `tr` | array | 23,901 | Chat tabs | Not analyzed |
| `r` | array | 23,006 | Animation | Not analyzed |
| `B7` | array | 21,368 | NPC dialogue | Not analyzed |
| `yG` | array | 20,687 | Window names | Not analyzed |
| `z7` | array | 18,515 | NPC dialogue | Not analyzed |
| `t` | array | 17,432 | UI graphics | Not analyzed |
| `J7` | array | 15,677 | NPC dialogue | Not analyzed |
| `Jg` | array | 14,277 | Player sprites | Not analyzed |
| `C` | array | 12,855 | Remote players | Not analyzed |
| `hb` | array | 12,583 | FPS settings | Not analyzed |
| `S` | object | 12,223 | Character state | Not analyzed |
| `b` | array | 11,931 | Remote players | Not analyzed |
| `M` | array | 11,514 | Direction | Not analyzed |
| `pb` | array | 11,259 | Display settings | Not analyzed |
| `c` | array | 10,643 | Mail UI | Not analyzed |
| `CP` | array | 10,432 | Status effects | Not analyzed |
| `s` | array | 10,213 | Direction | Not analyzed |
| `C` | object | 10,179 | Mob views | Not analyzed |
| `x` | array | 10,152 | Area list | Not analyzed |
| `Ek` | array | 9,791 | Market NPC | Not analyzed |
| `p` | array | 9,231 | Tree textures | Not analyzed |
| `c` | array | 9,150 | Asset loading | Not analyzed |
| `c` | object | 8,746 | Card bonuses | Not analyzed |
| `YA` | array | 8,525 | Gamepad buttons | Not analyzed |
| `Gh` | array | 7,201 | Chat font | Not analyzed |
| `x` | array | 7,128 | Gamepad axes | Not analyzed |
| `l` | array | 6,851 | Chat tabs | Not analyzed |
| `c` | array | 6,716 | Chat font | Not analyzed |
| `Hp` | array | 5,487 | Settings | Not analyzed |
| `x` | array | 5,406 | Area list | Not analyzed |
| `b` | array | 5,299 | Font size | Not analyzed |
| `T` | object | 5,029 | Skill window | Not analyzed |

---

## Domain Coverage Assessment (CORRECTED)

| Domain | Status | Evidence |
|---|---|---|
| Skills | ✓ EXTRACTED | 64 skills from v2_skills.json |
| Consumables | ✓ EXTRACTED | 80 items from v2_consumables.json |
| Cards | ✓ EXTRACTED | 49 cards from v2_cards.json |
| Status effects | ✓ EXTRACTED | 42 effects from v2_status_effects.json |
| Maps/areas | ✓ EXTRACTED | 19 maps from v2_maps.json |
| Formulas | ✓ EXTRACTED | 47 formulas, client-verified |
| Tutorial quests | ✓ EXTRACTED | 10 quests from party-BnJKGOnI.js (Tn array) |
| Equipment | ⚠️ PARTIAL | ~26 items from TA array |
| Monsters (species) | ⚠️ PARTIAL | 40 species, no stats |
| Drops | ⚠️ PARTIAL | 9 display rates |
| Refine | ⚠️ PARTIAL | Client formula only |
| World Boss | ⚠️ PARTIAL | Spawn metadata only |
| Arena/PvP | ⚠️ PARTIAL | Basic data only |
| Party | ⚠️ PARTIAL | Party system data |
| Full quest database | NOT_FOUND_IN_CLIENT | Tn = tutorial subset only |
| NPCs | NOT_FOUND_IN_CLIENT | No NPC table in bundles |
| Shops | NOT_FOUND_IN_CLIENT | No shop table in bundles |
| Fusion/Craft | NOT_FOUND_IN_CLIENT | No recipe table in bundles |
| Pets | NOT_FOUND_IN_CLIENT | No pet table in bundles |
| Storage | NOT_FOUND_IN_CLIENT | No capacity formula in bundles |
| Market | NOT_FOUND_IN_CLIENT | No listing table in bundles |
| Monster stats | NOT_FOUND_IN_CLIENT | Species only, no ATK/DEF/MDEF/HIT |
| Drop rates | NOT_FOUND_IN_CLIENT | Display constants only |
| Party EXP | NOT_FOUND_IN_CLIENT | Logic exists, formula unknown |
| EXP threshold | NOT_FOUND_IN_CLIENT | No table found |
| Bot AI | NOT_FOUND_IN_CLIENT | Bot window UI only |
| Economy | NOT_FOUND_IN_CLIENT | Gold/silver UI only |

---

## Extraction Priority for V0.9

| Priority | Domain | Location | Status |
|---|---|---|---|
| HIGH | Quests | main-CFj0fJNd.js (`tr`, `t`) | Not extracted |
| HIGH | Monsters | main-CFj0fJNd.js (`Jg`, `Kk`) | Partial |
| HIGH | NPCs | items-DqMVEwxd.js (`n`) | Not extracted |
| HIGH | Equipment stats | items-DqMVEwxd.js (`r`) | Partial |
| MEDIUM | Shops | main-CFj0fJNd.js | Not extracted |
| MEDIUM | Refine | items-DqMVEwxd.js (`Hr`) | Partial |
| MEDIUM | Fusion/Craft | main-CFj0fJNd.js | Not extracted |
| MEDIUM | Pets | main-CFj0fJNd.js | Not extracted |
| MEDIUM | Storage | main-CFj0fJNd.js | Not extracted |
| LOW | World Boss | main-CFj0fJNd.js | Partial |
| LOW | Arena/PvP | items-DqMVEwxd.js (`a`) | Partial |
| LOW | Party | party-BnJKGOnI.js | Partial |
| LOW | Market | main-CFj0fJNd.js | Not extracted |

---

## Coverage Calculation (Preliminary)

| Category | Known | Unknown | Total | Coverage |
|---|---|---|---|---|
| Skills | 64 | 0 | 64 | 100% |
| Items | 80 | ? | ? | ~50%? |
| Cards | 49 | 0 | 49 | 100% |
| Status effects | 42 | 0 | 42 | 100% |
| Maps | 19 | 0 | 19 | 100% |
| Monsters | 40 | ? | ? | ~30%? |
| Equipment | ~30 | ? | ? | ~20%? |
| Formulas | 47 | 0 | 47 | 100% |
| Quests | 0 | ? | ? | 0% |
| NPCs | 0 | ? | ? | 0% |
| Shops | 0 | ? | ? | 0% |
| Refine | 1 | ? | ? | 10% |
| Fusion | 0 | ? | ? | 0% |
| Pets | 0 | ? | ? | 0% |
| Storage | 0 | ? | ? | 0% |
| World Boss | 1 | ? | ? | 20% |
| Arena | 1 | ? | ? | 20% |
| Party | 1 | ? | ? | 30% |
| Market | 0 | ? | ? | 0% |

**Overall estimated client coverage: ~40-50%**

This is LOWER than the previous 60-70% estimate because the denominator is now clearer.

---

## Next Steps

1. **Extract all large data structures** from main bundle
2. **Identify domain** for each structure
3. **Parse and normalize** into JSON
4. **Cross-reference** with existing database
5. **Calculate final coverage** based on actual data

---

## Files Generated

- research/v09/client/CLIENT_EXTRACTION_INVENTORY.md (this file)
- research/v09/client/bundle_analysis/ (per-bundle analysis)
