# SCHEMA_V03.md — Lumivara Logical Database Schema

## Entity Relationship Overview

```
CLASSES (10)
 ├── 1:N → SKILLS (class_id)
 ├── 1:N → CLASS_UNLOCKS (unlock_jobs → classes job 50)
 └── 1:N → STARTER_EQUIPMENT (jobs[])

SKILLS (64)
 ├── FK class_id → CLASSES
 ├── enum target: enemy|area|self|ally
 ├── enum effect: damage|buff|heal|passive
 └── opt buff_id → STATUSES

ITEMS (80, consumable)
 ├── enum kind: usable|cash
 └── N:M → MONSTERS via drops (DERIVED)

CARDS (49)
 ├── FK monster_key → MONSTERS (konvensi nama, INFERRED)
 └── bonuses: JSON stat map

MONSTERS (40)
 ├── areas[] → MAPS (N:M)
 ├── base_exp / job_exp / guild_exp (OBSERVED)
 ├── drops: JSON item→count (DERIVED)
 └── 1:N → MONSTER_STATUS_ATTACKS (by name, 7 rows)

MAPS (19)
 ├── portals[]: {x, y, to → MAPS, label, arrival}
 └── spawn: [x, y]

STATUSES (42)
 ├── enum kind: buff|debuff
 └── params: duration/dot/speedFactor/aspdPercent...

DROP_RATES (9) — kategori → rate (client display)

TRANSLATIONS (2547) — thai → english

CLIENT_MINING (14 domain) — quest/mall/refine/fusion/pet/world_boss/arena/npc/storage/market/feature_flags/death_revive/equipment_generator/exp_table
```

## Primary Keys

| Entity | PK | Note |
|---|---|---|
| CLASSES | class_id | string (novice, kensei...) |
| SKILLS | skill_id | string (bash, iaigiri...) |
| ITEMS | item_id | string (potion, megaphone...) |
| CARDS | card_id | string (hopper_card...) |
| MONSTERS | monster_key | string (dune-gecko...) |
| MAPS | map_id | string (field, rome...) |
| STATUSES | status_id | string (poison, meikyo...) |

## Foreign Keys (logical, bukan SQLite constraint)

| Dari | Field | Ke | Confidence |
|---|---|---|---|
| SKILLS | class_id | CLASSES | VERIFIED |
| SKILLS | buff_id | STATUSES | VERIFIED |
| MAPS | portals[].to | MAPS | VERIFIED |
| MONSTERS | areas[] | MAPS | VERIFIED |
| MONSTER_STATUS_ATTACKS | monster_name | MONSTERS.name | VERIFIED (1 variant orphan: World Boss) |
| CARDS | (name convention) | MONSTERS | INFERRED |
| MONSTERS | drops{} keys | ITEMS | PARTIAL (material drops di luar ITEMS) |

## Known Gaps

- Interior areas (inn/cove/grove/ruins/temple/arena) tidak punya entrance portal di MAPS
- Equipment drops (armor/sword/shoes...) tidak punya entity table — hanya category roll
- Quest rewards server-driven — tidak ada tabel statis
