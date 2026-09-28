# Validation Report — Lumivara Forensics v3

## Hasil Test
| Item | Status |
|---|---|
| GAME_DB.json | OK |
| MONSTER_DB.json | OK |
| TRANSLATIONS.json | OK |
| DROP_DB.json | OK |
| forensics/CHANGELOG_NORMALIZED.json | OK |
| forensics/inventory_manifest.json | OK |
| sqlite_integrity | ok |
| skill_name_dupes | 0 |
| orphan_status_refs | 1 |
| cards_without_confirmed_monster | 48 |
| invalid_monster_values | 0 |
| skills_with_invalid_class | 0 |
| map_count | 19 |
| translation_entries | 2547 |

## Temuan / Isu
- mob_status_attacks menunjuk monster yang tidak ada di MONSTER_DB: {'Crowned Prism Hopper'}

## Catatan
- Skill dengan nama sama antar class (mis. shared passive) BUKAN duplikat error.
- Kartu tanpa monster terkonfirmasi: mapping kartu->monster via konvensi nama, belum diverifikasi biner (INFERRED).
- Total isu: 1