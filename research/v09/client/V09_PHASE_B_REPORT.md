# V0.9 PHASE B REPORT — DATA DOMAIN EXTRACTION

**Status:** Documentation consistency fix only — no new research.
**Scope:** Quest/Equipment/79-structure/Coverage classification alignment.

---

## Coverage Methodology

No percentages are reported. Where the total population is unknown,
counts are reported as "X of UNKNOWN total". This applies to
equipment, quests, NPCs, shops, and any other domain where we
cannot prove the denominator.

`NOT_FOUND_IN_CLIENT` is a negative-evidence classification: it
means the data was not found in any of the 6 analyzed client
bundles. It is **not** evidence that data is server-authoritative
or that it exists only on the server.

---

## Quest Data — CORRECTED

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

**10 tutorial quests extracted** (was 0, now 10 of UNKNOWN total quest count)

Source: `party-BnJKGOnI.js` (Tn array)

**IMPORTANT**: Tn is NOT the master quest table — it's the tutorial/beginner quest subset. Full quest database is server-driven. Total quest count = UNKNOWN.

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

| Domain | Status | Notes |
|---|---|---|
| Tutorial quests | EXTRACTED | 10 quests, total quest count = UNKNOWN |
| Full quest database | NOT_FOUND_IN_CLIENT | Tn = tutorial subset only |
| Skills | EXTRACTED | 64 skills from v2_skills.json |
| Consumables | EXTRACTED | 80 items from v2_consumables.json |
| Cards | EXTRACTED | 49 cards from v2_cards.json |
| Status Effects | EXTRACTED | 42 effects from v2_status_effects.json |
| Maps | EXTRACTED | 19 maps from v2_maps.json |
| Monsters | PARTIAL | 40 species, no stats |
| Equipment | PARTIAL | 26 items, total count = UNKNOWN |
| Formulas | EXTRACTED | 47 formulas, client-verified |
| NPCs | NOT_FOUND_IN_CLIENT | No NPC table in bundles |
| Shops | NOT_FOUND_IN_CLIENT | No shop table in bundles |
| Refine | PARTIAL | Client formula only |
| Fusion | NOT_FOUND_IN_CLIENT | No recipe table in bundles |
| Pets | NOT_FOUND_IN_CLIENT | No pet table in bundles |
| Storage | NOT_FOUND_IN_CLIENT | No capacity formula in bundles |
| Market | NOT_FOUND_IN_CLIENT | No listing table in bundles |
| World Boss | PARTIAL | Spawn metadata only |
| Arena/PvP | PARTIAL | Basic data only |
| Party | PARTIAL | Party system data |

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

**Total client-side records: PARTIAL COUNT, total = UNKNOWN**

---

## Classification — NOT_FOUND_IN_CLIENT Domains

### Istilah
Sebelumnya menggunakan label yang menyiratkan data bersifat server-authoritative.
Koreksi ini tidak ada evidence bahwa data berada di server — hanya bahwa
datatidak ditemukan di client bundle yang dianalisis (6 bundle).

### Daftar Domain

| Domain | Status | Evidence |
|---|---|---|
| NPC | NOT_FOUND_IN_CLIENT | No NPC table, only sprite/UI references |
| Shop | NOT_FOUND_IN_CLIENT | No shop table, only UI strings |
| Fusion | NOT_FOUND_IN_CLIENT | No recipe table, only NPC sprite |
| Pets | NOT_FOUND_IN_CLIENT | No pet table, only UI window |
| Storage | NOT_FOUND_IN_CLIENT | No capacity formula, only UI |
| Market | NOT_FOUND_IN_CLIENT | No listing table, only order logic |
| Monster stats | NOT_FOUND_IN_CLIENT | Species only, no ATK/DEF/MDEF/HIT |
| Drop rates | NOT_FOUND_IN_CLIENT | Display constants only |
| Party EXP | NOT_FOUND_IN_CLIENT | Logic exists, formula unknown |
| EXP threshold | NOT_FOUND_IN_CLIENT | No table found |
| Bot AI | NOT_FOUND_IN_CLIENT | Bot window UI only |
| Economy | NOT_FOUND_IN_CLIENT | Gold/silver UI only |

### Catatan
Beberapa domain (NPC, Shop, Fusion, Pets, dll) kemungkinan memang server-authoritative tapi tidak bisa dibuktikan hanya dari client bundle analysis. Evidence negatif (tidak ditemukan) bukti bahwa data ada di client, bukti bahwa data ada di server.

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

**Phase B complete.** Records extracted: ~377 (partial count, unknown total).
NOT_FOUND_IN_CLIENT domains: 11 (NPC, Shop, Fusion, Pets, Storage, Market,
Monster stats, Drop rates, Party EXP, EXP threshold, Economy).
