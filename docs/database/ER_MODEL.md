# ER_MODEL.md — Lumivara Entity Relationship

```mermaid
erDiagram
    CLASSES ||--o{ SKILLS : "class_id"
    CLASSES ||--o{ CLASS_UNLOCKS : "unlock chain"
    SKILLS }o--|| STATUSES : "buff_id (opt)"
    MONSTERS }o--o{ MAPS : "spawn areas"
    MAPS ||--o{ MAP_PORTALS : "portals[]"
    MAP_PORTALS }o--|| MAPS : "to"
    MONSTERS ||--o{ MONSTER_STATUS_ATTACKS : "by name"
    MONSTERS ||--o{ MONSTER_DROPS : "drops (DERIVED)"
    MONSTER_DROPS }o--|| ITEMS : "item_id (partial)"
    CARDS }o--|| MONSTERS : "source (INFERRED)"
    MONSTERS ||--o| MONSTER_EXP : "base/job/guild"

    CLASSES {
        string class_id PK
        string name
        json unlock_jobs
        int unlock_silver
    }
    SKILLS {
        string skill_id PK
        string class_id FK
        string name
        int job_level
        int sp_cost
        int cooldown_ms
        int range_px
        string target
        string effect
        bool is_passive
    }
    ITEMS {
        string item_id PK
        string name
        string kind
        int weight
        int sell_price
        int buy_price
    }
    CARDS {
        string card_id PK
        string name
        json bonuses
        int price
    }
    MONSTERS {
        string monster_key PK
        string name
        int level
        int max_hp
        bool elite
        json areas
        int base_exp
        int job_exp
        json drops
    }
    MAPS {
        string map_id PK
        string name
        int width
        int height
        json portals
    }
    STATUSES {
        string status_id PK
        string name
        string kind
        int duration_ms
        json params
    }
    MONSTER_STATUS_ATTACKS {
        string monster_name FK
        string status_id
        float chance
    }
    DROP_RATES {
        string category PK
        float rate
    }
```

## Catatan

- Relasi MONSTERS→ITEMS via drops bersifat DERIVED (asosiasi posisi event, bukan FK server)
- CARDS→MONSTERS via konvensi penamaan (hopper_card → prism-hopper) — INFERRED
- Tidak ada FK constraint fisik di SQLite (logical model only)
