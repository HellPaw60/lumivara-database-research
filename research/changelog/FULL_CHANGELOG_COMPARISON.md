# FULL CHANGELOG COMPARISON (v0.4.2)

## Hasil Final — Parser Canonical

**Misteri 613 lines-diff: TERPECAHKAN — PARSER_ERROR pada parser official lama.**

### Bukti Langsung (Phase 3)

Raw slice entry `2026-09-28-kensei-twin-strike` dari kedua bundle **identik karakter-per-karakter** (termasuk `lines[]` lengkap dengan 2 baris teks Thai). Parser official lama memakai regex lazy `lines:\[(.*?)\]` yang gagal saat konten lines mengandung karakter `]` atau struktur kompleks — menyebabkan lines tidak terekstrak → 613 false diff. Parser client lama kebetulan memakai pola regex berbeda yang lebih toleran.

### Perbaikan

Parser canonical tunggal (bracket-matching dengan string-aware depth tracking, escape handling seragam) dipakai untuk KEDUA sumber. Hasil: **0 parser error, 650/650 client + 669/669 official entries memiliki lines lengkap** (1.593 vs 1.627 total lines).

## Klasifikasi Lengkap

| Status | Jumlah | Keterangan |
|---|---|---|
| **EXACT_MATCH** | 648 | id+date+time+title+lines identik di kedua sumber |
| **DUPLICATE_UPSTREAM** | 1 | `2026-09-23-skill-rebalance` ×2 di KEDUA sumber, instance identik lintas sumber — konfirmasi final fakta upstream |
| **OFFICIAL_ONLY** | 19 | update baru (2026-09-28 12:08–15:52) setelah snapshot client |
| **CLIENT_ONLY** | 0 | — |
| **METADATA_MATCH_CONTENT_DIFF** | 0 | — |
| **PARSER_ERROR** | 0 | — |

**Full-content matches (lines identik non-empty): 649/649 shared IDs**
**Ordering: identik untuk seluruh entri bersama**

## 19 Official-Only Entries

Update hari ini setelah snapshot client: refine badge di 7 window UI (bag/equip/inspect/forge/market/storage/trade), repair price ÷10, fusion odds display, fusion socket remove/lock, arrow bulk buy 1k/10k/100k, arrows weightless, broken gear indicator, Kensei fixes (no air swing, Oboro invincible, head slot), skill rebalance Cleric/Swordsman/Kensei, Challenging range 270, shard market memory fix.

## Canonical Dataset

`CHANGELOG_CANONICAL.json` — 669 entries, basis **OFFICIAL_WEB (freshest)**, dengan `sources[]` + `source_status` + `confidence` per entry. Historical client snapshot tetap utuh di `CANONICAL_CLIENT_CHANGELOG.json` (tidak dioverwrite).

## Kesimpulan

Kedua sumber changelog berasal dari **pipeline data identik** — 649/649 shared entries cocok penuh (metadata + konten + ordering). Perbedaan hanya usia snapshot. Dataset changelog sekarang **fully content-validated**.
