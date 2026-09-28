# DB_COMPARE — Field-Level Comparison (v0.4 Phase 3)

**Method:** deterministic comparison (schema → columns → rows → values). Tanpa fuzzy matching.

## Hasil Utama

| Aspek | Hasil |
|---|---|
| Tabel hanya di final (database/) | `CLIENT_MINING` (14 rows) |
| Tabel hanya di initial (forensics/database/) | — tidak ada |
| Perubahan kolom | — tidak ada |
| Row delta pada 11 tabel bersama | **0** (semua identik) |
| Value diff pada 11 tabel bersama | **0** (added/removed/modified semua kosong) |

## Kesimpulan Terbukti

Klaim v0.3 "delta = CLIENT_MINING" **terverifikasi field-level**: kedua database identik
pada seluruh 11 tabel bersama (CLASSES, SKILLS, ITEMS, CARDS, STATUSES, MAPS,
MONSTER_STATUS_ATTACKS, DROP_RATES, MONSTERS, TRANSLATIONS, _prov). Final hanya
menambah tabel CLIENT_MINING berisi 14 domain mining.

## Bukti Per Tabel

Lihat `DB_COMPARE.json` untuk struktur lengkap:

- `schema_diff` — hanya `tables_only_in_final: [CLIENT_MINING]`, `column_changes: {}`
- `row_diff` — semua tabel `delta: 0`
- `value_diff` — semua tabel `added/removed/modified: []`

## Provenance Delta

| Delta | Source | Evidence | Confidence |
|---|---|---|---|
| +CLIENT_MINING (14 rows) | forensics/client/tables/*.json (subagent mining) | raw blob di forensics/client/raw/ + bundle web-v2 | VERIFIED (client code) |

## Implikasi untuk Merge

Tidak ada konflik merge — initial database adalah subset sempurna dari final.
Kedua database dapat dipertahankan sebagai evidence tanpa risiko inkonsistensi.
