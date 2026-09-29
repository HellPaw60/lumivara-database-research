# V0.9 PHASE B REPORT — DATA DOMAIN EXTRACTION

## Quest Data — EXTRACTED

| ID | Title | Goal | Reward |
|---|---|---|---|
| first-steps | ก้าวแรกของนักผจญภัย | Kill 1 Prism Hopper | 50 silver |
| field-loot | เก็บของในสนามรบ | Pickup 3 items | 5 potions |
| basic-power | พลังพื้นฐาน | Allocate 1 stat point | 100 silver |
| first-gear | เกราะชิ้นแรก | Equip 1 gear | starter sword |
| life-force | พลังชีวิต | Use 1 potion | 10 potions |
| first-skill | เลือกเส้นทาง | Learn 1 skill | 200 silver + fly wing |
| true-class | สู่อาชีพที่แท้จริง | Complete class quest | class unlock |
| border-economy | เศรษฐกิจชายขอบ | Sell 1 item | 150 silver |
| wider-world | โลกกว้างกว่าที่คิด | Travel to new map | 400 silver |
| true-conqueror | ผู้พิชิตตัวจริง | Reach Base Level 10 | 1000 silver + potions |

**Total: 10 quests extracted** (was 0, now 100%)

Source: `party-BnJKGOnI.js` (Tn array)

---

## Items — COUNT UPDATE

Previously counted ~30 items. Now counting from v2 JSON files:

| Source | Count | Status |
|---|---|---|
| v2_consumables.json | 80 | ✓ Already extracted |
| v2_cards.json | 49 | ✓ Already extracted |
| items-DqMVEwxd.js (weapons/armor) | ~26 | ✓ Partially extracted |

**Total items in client: ~155** (80 consumables + 49 cards + 26 equipment)

---

## Domain Classification Summary

| Domain | Status | Coverage |
|---|---|---|
| Quests | ✓ EXTRACTED | 100% |
| Skills | ✓ EXTRACTED | 100% |
| Consumables | ✓ EXTRACTED | 100% |
| Cards | ✓ EXTRACTED | 100% |
| Status Effects | ✓ EXTRACTED | 100% |
| Maps | ✓ EXTRACTED | 100% |
| Monsters | ⚠️ PARTIAL | Species only, no stats |
| Equipment | ⚠️ PARTIAL | ~26 items extracted |
| Formulas | ✓ EXTRACTED | 100% |
| NPCs | ❌ NOT FOUND | Server-side |
| Shops | ❌ NOT FOUND | Server-side |
| Refine | ⚠️ PARTIAL | Client formula only |
| Fusion | ❌ NOT FOUND | Server-side |
| Pets | ❌ NOT FOUND | Server-side |
| Storage | ❌ NOT FOUND | Server-side |
| Market | ❌ NOT FOUND | Server-side |
| World Boss | ⚠️ PARTIAL | Spawn metadata |
| Arena/PvP | ⚠️ PARTIAL | Basic data |

---

## Client Coverage (Measurable)

| Category | Count | Source |
|---|---|---|
| Quests | 10 | party-BnJKGOnI.js |
| Skills | 64 | v2_skills.json |
| Consumables | 80 | v2_consumables.json |
| Cards | 49 | v2_cards.json |
| Status Effects | 42 | v2_status_effects.json |
| Maps | 19 | v2_maps.json |
| Monsters (species) | 40 | MONSTER_DB.json |
| Equipment | ~26 | items-DqMVEwxd.js |
| Formulas | 47 | FORMULA_DATABASE |

**Total client-side records: ~377**

---

## Server-Side Only (Confirmed NOT in client)

| Domain | Evidence |
|---|---|
| NPC data | No NPC table found in bundles |
| Shop data | No shop table found in bundles |
| Refine success rates | Client formula only, server rate unknown |
| Fusion recipes | No recipe table found in bundles |
| Pet definitions | No pet table found in bundles |
| Storage capacity | No capacity formula found in bundles |
| Market listings | No market table found in bundles |
| Monster stats (ATK/DEF/MDEF/HIT) | Server authoritative |
| Drop rates (actual) | Server authoritative |
| Party EXP split | Server authoritative |
| EXP threshold | Server authoritative |
| Bot AI behavior | Server authoritative |
| Economy (gold market, etc.) | Server authoritative |

---

## Phase B Output

| File | Content |
|---|---|
| research/v09/client/quests.json | 10 quest records |
| research/v09/client/items.json | 26 equipment records |
| research/v09/client/CLIENT_EXTRACTION_INVENTORY.md | 259 structures documented |

---

## Next Steps (Phase C-F)

1. **Phase C**: Formula Audit — verify all 47 formulas against source
2. **Phase D**: GAP Resolution — attack open gaps with new evidence
3. **Phase E**: Runtime/Network Validation — passive observation
4. **Phase F**: Coverage + Final Validation

---

**Phase B complete.** Records extracted: ~377. Server-side confirmed: 12+ domains.
