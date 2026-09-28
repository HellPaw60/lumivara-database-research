# V03 Database Validation

**Tanggal:** 2026-09-28 | **Scope:** full database dump + SQL archive

## SQLite Forensics

| Database | Size | Tables | Rows | Integrity | FK Check |
|---|---|---|---|---|---|
| database/LUMIVARA_FORENSICS.sqlite | 552,960 | 12 | 2,891 | ok | clean |
| forensics/database/LUMIVARA_FORENSICS.sqlite | 536,576 | 11 | 2,877 | ok | clean |

Delta: database/ versi memiliki +1 tabel (CLIENT_MINING, 14 rows) — versi final.

## SQL Dump Reproducibility

- `full_dump.sql` (572,004 bytes) → recreate ke database baru
- Hasil: **integrity=ok, 12/12 tables match, semua row count match — PASS**

## JSON Parse Test

- database/normalized/*.json: 8 file, semua OK
- database/raw/*.json: 2 file, OK
- database/json/*.json: 12 file (per-table export), OK
- formulas/FORMULA_DATABASE_V03.json: OK
- provenance/PROVENANCE_V03.json: OK

## Dataset Counts (normalized)

| Entity | Records | Match dengan v0.2 |
|---|---|---|
| classes | 10 | ✓ |
| skills | 64 | ✓ |
| items | 80 | ✓ |
| cards | 49 | ✓ |
| monsters | 40 | ✓ |
| maps | 19 | ✓ |
| statuses | 42 | ✓ |

## CSV Export

11 tabel → CSV (cards, classes, client_mining, drop_rates, items, maps, monster_status_attacks, monsters, skills, statuses, translations). Kolom asli dipertahankan.

## Known Issues

1. `forensics/database/` SQLite = versi lama (tanpa CLIENT_MINING) — dipertahankan sebagai evidence, database/ = versi final
2. Duplikat changelog ID `2026-09-23-skill-rebalance` (fakta sumber, terdokumentasi di v0.2 audit)
3. CRLF line-ending artifact pada file teks (terdokumentasi di v0.2 audit — konten identik)

## Kesimpulan

**LULUS** — seluruh database terinventaris, terdump, dapat direproduksi identik dari SQL.
