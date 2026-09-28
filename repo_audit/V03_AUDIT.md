# V03 Audit — Full Database Dump & SQL Archive

## Local Inventory (Phase 0)

- **249 file** total workspace (149 tracked-candidate, 100 ignored)
- Bug inventory script v0.3 awal (false untracked) — diperbaiki: git status asli hanya 2 file baru
- **Dua SQLite ditemukan**: database/ (final, 12 tabel) + forensics/database/ (versi awal, 11 tabel)

## Database Forensics (Phase 1-2)

| Aspek | database/ | forensics/database/ |
|---|---|---|
| Tables | 12 | 11 |
| Rows | 2.891 | 2.877 |
| Integrity | ok | ok |
| FK check | clean | clean |
| Page size | 4.096 | 4.096 |

Delta = tabel CLIENT_MINING (14 domain mining hasil subagent).

## SQL Archive (Phase 7-9)

```
database/dumps/LUMIVARA_FORENSICS/
├── schema.sql          (12 objects)
├── full_dump.sql       (572 KB, executable)
├── tables/*.sql        (12 file)
├── csv/*.csv           (12 file)
└── json/*.json         (12 file)

database/sql/           (schema + full + 11 per-domain)
database/csv/           (11 tabel)
database/json/          (12 tabel)
database/raw/           (game_db_raw, monster_db_raw)
database/normalized/    (7 entity + _metadata)
```

## Reproducibility (Phase 18)

`sqlite3 new.db < full_dump.sql` → **PASS**: 12/12 tabel, semua row count identik, integrity ok.

## New in v0.3

1. Full SQL/CSV/JSON dump ketiga format
2. Raw vs Normalized dataset terpisah (database/raw/ + database/normalized/)
3. SCHEMA_V03.md + ER_MODEL.md (mermaid) — logical schema + relationship
4. FORMULA_DATABASE_V03.json — 18 formula terklasifikasi (CLIENT_CODE/OBSERVED/UNKNOWN)
5. PROVENANCE_V03.json — 12 entity dengan source hash
6. discovered_databases.json — forensik metadata SQLite lengkap

## Validation Summary

- JSON parse: semua OK
- SQLite integrity: ok (kedua database)
- Reproducibility: PASS
- Dataset counts: konsisten dengan v0.2 (10 class, 64 skill, 80 item, 49 card, 40 monster, 19 map, 42 status)

## Remaining Unknowns (tidak berubah dari v0.2)

Interior area coordinates, server damage formula, actual server drop rates, quest server rewards, world boss spawn schedule, gold pack pricing, z5 function, server refine formula.
