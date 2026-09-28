# Lumivara Database Research

**Lumivara Online client, network, runtime data and database reverse-engineering research archive.**

## Overview

Repositori ini berisi hasil penelitian dan rekonstruksi database serta game mechanics
**Lumivara Online** (MMORPG pixel browser-based, https://lumivaraonline.com/) dari:

- Client web bundles (2 versi bundle, diff-able)
- Observasi network WebSocket (passive collection via guest account)
- Runtime snapshot state (~50K snapshot, 14 area)
- Localization bundle (TH→EN, 2.5K pasang)
- Changelog in-game (650 entri, 7 hari)
- Hasil extraction bertahap (v1 → v2)

## Research Scope

| Domain | Cakupan |
|---|---|
| Client | Bundle JS mining, tabel data tertanam, formula |
| Network | Protokol WS JSON, event schema, handshake |
| Runtime | Character state, monster state, combat events |
| Database | Rekonstruksi logical data model server |
| Formulas | Combat, drop, refine, equipment generator |
| Content | Class, skill, item, card, monster, map, quest, ekonomi |
| History | Changelog normalization, version diff |

## Repository Structure

```
database/      — SQLite master + JSON database per-domain
protocol/      — Rekonstruksi protokol client-server
formulas/      — Formula combat/drop/equipment (research)
research/      — Catatan riset per-domain
diffs/         — Version diff antar bundle
provenance/    — Lineage setiap field ke sumbernya
validation/    — Laporan validasi integritas
extraction/    — Script reproducible (inventory, parser, collector, aggregator)
raw/           — Raw evidence (bundle, snapshot, log collector)
docs/          — Laporan & dokumentasi arsitektur
```

## Current Dataset

| Entity | Jumlah | Confidence |
|---|---|---|
| Classes | 10 | VERIFIED |
| Skills (aktif + passive) | 64 | VERIFIED |
| Items (consumable) | 80 | VERIFIED |
| Cards | 49 | VERIFIED |
| Status effects | 42 | VERIFIED |
| Maps | 19 | VERIFIED |
| Monsters | 40 | VERIFIED (stat/EXP), DERIVED (drops) |
| Monster status attacks | 7 | VERIFIED |
| Drop rate categories | 9 | VERIFIED (client display) |
| Translations TH→EN | 2,547 | VERIFIED |
| Changelog entries | Client snapshot: 650 entries / 649 unique IDs · Official snapshot: 669 entries / 668 unique IDs · Cross-validated: 649/649 ID + full content match | VERIFIED |
| WS event types teramati | lihat protocol/ | VERIFIED |

## Confidence Model

- **VERIFIED** — langsung teramati di source (bundle code / WS payload), dapat direproduksi
- **DERIVED** — hasil agregasi/transformasi dari data VERIFIED (mis. drop association via posisi)
- **INFERRED** — hipotesis dari pola, belum ada bukti langsung
- **UNKNOWN** — field/relasi yang ada tapi maknanya belum diketahui

## Data Provenance

Setiap entity dapat ditelusuri via `provenance/PROVENANCE.json`:
`database field → normalized record → raw record → source file → sha256 → extraction method → confidence`

## Version History

- **v1** — 2026-09-28 pagi: pembongkaran pertama (exe → NSIS → asar → Electron shell → web bundle). 37 monster, 50 skill.
- **v2** — 2026-09-28 siang: bundle update (Kensei/Nekobaku/Mamushi class, rebalancing). 40 monster, 64 skill, TRANSLATIONS.
- **v3** — forensik lengkap: SQLite master, protokol, changelog, provenance, repo GitHub.
- **v0.2** — integrity audit: 10/10 klaim match, 3 broken path fixed, confidence refined.
- **v0.3** — full database dump: SQL/CSV/JSON archive ketiga format, reproducibility PASS, schema + ER model, 18 formula terklasifikasi.

## Research Status

| Fitur/Data | Status |
|---|---|
| Class & unlock requirements | CONFIRMED |
| Skill table (semua class) | CONFIRMED |
| Item/card/status tables | CONFIRMED |
| Monster stats + EXP | CONFIRMED (40 spesies) |
| Monster drop table | PARTIALLY RECONSTRUCTED (17-27 spesies, asosiasi posisi) |
| Protokol WS (event schema) | CONFIRMED (lihat protocol/) |
| Combat formula server | UNKNOWN (hanya statistik observasi) |
| Interior areas (inn/cove/grove/ruins/temple/arena) | UNKNOWN (pintu tidak di data portal) |
| Quest/mall/pet/refine tables | lihat forensics/client/tables/ (hasil mining) |

## Known Limitations

- Combat damage formula: UNKNOWN (hanya statistik observasi)
- Actual server drop rate: UNKNOWN (konstanta klien = display only)
- Interior area coordinates (inn/cove/grove/ruins/temple/arena): UNKNOWN
- Quest server reward schema: UNKNOWN (server-driven)
- Refine formula: VERIFIED dari kode KLIEN — versi server belum tentu identik
- Monster drop table: asosiasi posisi (DERIVED), bukan tabel server
- maxHp: nilai maksimum teramati (variance elite/normal bisa tercampur)

## Important Findings (VERIFIED)

1. **Class unlock chain**: Kensei = Swordsman 50 + Thief 50 + 120K Silver; Nekobaku = Merchant 50 + Mamushi 50 + 120K Silver
2. **mob_status_attacks table** (terlewat di v1): Crowned Prism Hopper crush 30%, Moss Mushroom poison 18%, dst.
3. **Equipment drop rebalance**: 2.5% → 1.25% per kill; favored slot 6x; nama ±10 level monster
4. **World Boss**: Crowned Prism Hopper Lv.100 drop Tier V equipment 100%
5. **Party rules**: EXP/Drop +2%/member (max 12, ±10 level)
6. **Monster rebalancing v1→v2**: Vine Lynx HP ×10, Bog Toad ×4, Pebble Golem ÷4
7. **Boss endgame baru**: Crowned Tempest Drake Lv.280 (11.16M HP), Crowned Grave Knight Lv.230
8. **Protokol**: handshake `spawnReady` wajib sebelum input diterima; travel divalidasi posisi portal; move max ~90px/120ms
9. **Guest system**: endpoint `POST /api/guest` dengan body kosong teramati (tanpa CAPTCHA di client flow). Selama riset, ±15 guest account dibuat via endpoint publik ini tanpa hambatan yang terlihat. Catatan: ini observasi eksperimen terbatas — bukan security audit server, rate-limit server-side tidak diuji.
10. **650 changelog entries terekstrak dari bundle klien** yang mencakup periode 7 hari; 649 unique ID teramati, 1 duplikat ID ada di source bundle. Entry ≠ release — jumlah patch/release aktual tidak diketahui.

## Legal Note

Penelitian ini bersifat read-only/passive terhadap server publik. Tidak ada eksploitasi,
modifikasi data, atau akses tidak sah. Semua data dari endpoint publik yang dapat diakses
guest account normal.
