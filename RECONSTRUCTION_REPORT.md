# RECONSTRUCTION_REPORT.md — Lumivara Database Forensics v3

> **Catatan confidence:** formula yang ditandai "dari kode" = kode KLIEN. Server bisa berbeda.
> Statistik berlabel OBSERVED bukan formula. Lihat repo_audit/AUDIT_DETAILS.json untuk audit lengkap.

## 1. Executive Summary

Rekonstruksi database Lumivara Online dari 4 kelas sumber: client bundle (2 versi),
observasi WebSocket pasif (~50K snapshot, 14 area), localization bundle, dan changelog.
Menghasilkan 10-class database, 64 skill, 80 item, 49 kartu, 40 monster, 19 map,
26 event protokol terdokumentasi, dan 14 domain mekanik tambahan hasil deep mining.
Semua data dapat ditelusuri ke sumber dengan hash (lihat PROVENANCE.json).

## 2. Client Architecture

- **Desktop**: NSIS installer → electron-builder → Electron 44.4.5/Chromium 152 shell.
  main.cjs 153 baris: loadURL ke situs, sandbox ketat, tanpa IPC custom.
  139MB dari 141MB asar = Phaser yang tidak dipakai shell (sisa package.json web).
- **Web**: Vite bundle. main (2.4MB) + items (197KB, semua tabel data) + party + language + changelog.
  Phaser 3.90, rendering canvas prosedural (bukan tilemap file), UI DOM overlay.

## 3. Network Architecture

- REST: 19 endpoint (`/api/*`) untuk auth/guest/shop/queue/announce.
- WS: `wss://host/api/ws?v=5&area=<hint>`, cookie auth, JSON per pesan.
- **Handshake wajib**: `{type:"spawnReady"}` setelah snapshot pertama — tanpa ini server mengabaikan semua input pergerakan.
- **Validasi server**: move max ~90px/120ms; travel hanya diterima dekat koordinat portal sah; close codes 4002 (tab lain), 4004 (idle), 4100 (pindah area), 4005 (login lain).
- **Broadcast area**: semua player menerima event defeat (baseExp/jobExp/guildExp + nama mob) dan pickup (item) milik player lain — sumber pasif EXP/drop table.

## 4. Server Data Model (rekonstruksi)

Dari snapshot.self union (lihat research/self-state-fields.json): ~50 field character state —
level/exp/points/stats/inventory(80 slot)/gear/equipped/skillLevels/skillCooldowns/jobProgress/
quest(counters+claimed)/petBag/gear loadouts/classStats/classUnlocks/silver/arenaKills/statuses/deadUntil.
Server memegang state penuh; klien hanya render + input.

## 5-10. Database Content

| Domain | Jumlah | Sumber |
|---|---|---|
| Classes | 10 (2 unlockable: kensei, nekobaku @120K silver + job 50 ganda) | items.js var z + WA |
| Skills | 64 (aktif + passive, semua class) | items.js var x |
| Items | 80 consumable + starter set + shop templates | items.js var Pc + main |
| Cards | 49 (basic stat + special option) | items.js var le |
| Monsters | 40 spesies (Lv1-280), 29 dengan EXP, 27 dengan drops | WS observation |
| Maps | 19 (528KB portal graph lengkap) | items.js var Y |

## 11. Monsters — highlight

- Boss endgame: Crowned Tempest Drake Lv.280 (11.16M HP), Crowned Grave Knight Lv.230 (5.8M HP)
- World Boss: Crowned Prism Hopper Lv.100 — drop Tier V 100% (dari TRANSLATIONS)
- Rebalance v1→v2: Vine Lynx ×10 HP, Bog Toad ×4, Pebble Golem ÷4

## 12-13. Maps & Quest

19 area terhubung via portal graph (BFS-able). 6 interior (inn/cove/grove/ruins/temple/arena)
pintunya via objek dunia prosedural — koordinat belum terekstrak (open question).
Quest harian: questTick counters + claimQuest; daily hunt (100 monster) → refine stone.

## 14. Combat (statistik observasi — bukan formula)

Lihat formulas/combat-analysis.json (3.282 hit event, full coverage):
- **Crit ratio rata-rata 3.551x** (crit mean 13.267 vs non-crit 3.736; crit rate 35.3% dari labeled)
- **Miss rate teramati 0%** (2.940 outgoing berlabel, semua `missed:false`) — hit/flee mungkin tidak berlaku untuk mob farming biasa
- **Multi-hit terverifikasi**: `damage == sum(hits[])` pada event double (399 event)
- 20 skill teramati; terpopuler: viperfang (471 cast), coldbolt (397), twinfang (259 — crit ratio 7.29 tapi stdev 22.289, distribusi lebar)
- `incoming` (mob→player): 342 event; `drainSp`/`drainHp`/`dot` juga teramati
- Formula server-side = UNKNOWN (butuh eksperimen terkontrol)

## 15. Drop System (dari client constants + TRANSLATIONS)

- Base rates (display): equipment 1.25% (dinnerf dari 2.5%), card 0.1%, bossCard 1%, consumable 15%, etc 30%
- Favored slot: 6x lebih sering
- Nama equipment: ±10 level monster
- Party modifier: +2%/member (max 12)
- Pipeline lengkap: MONSTER DEFEATED → category roll → item roll → slot roll (favored) → tier/rarity → random option → drop

## 16-18. Equipment / Refine / Fusion

- Generator: template-based (11 template senjata), random stat +1–3 (75% 1 stat, 25% 2 stat) — bukti klien yang tersedia mengindikasikan equipment generation diselesaikan server-side (klien hanya berisi template detection/rendering logic, tidak ada formula generation authoritative yang ditemukan)
- **Refine formula (VERIFIED dari kode KLIEN — server belum tentu identik)**: `failFactor(level) = min(0.3, max(0, (level-20) × 0.0025))`; `successRate(level, refine) = 1 − failFactor × (1 − min(100, refine)/100)` — makin tinggi level & refine stat, makin tinggi success; cap 30% fail factor. Refine stone 1% drop Lv70+ atau daily hunt. 10 bonus stat refine dengan cap masing-masing (pierce 60, atkPct 30, lifesteal 8, moveSpeed 30, dst.)
- Fusion: `fuse gearIds[] + slot + template` via Fusion Master NPC → forge effects (4 jenis)
- **Pet system (VERIFIED)**: 10+ pet dengan elemen — dew-bunny(water), thorn-pixie(poison), honey-moth(wind), bramble-hare(earth), frost-puff(ice) — petBag terpisah dari inventory, petLoot dengan filter (consumable/etc/card/equipment), petWithdraw all
- **World Boss (VERIFIED dari kode klien)**: Crowned Prism Hopper — `hp:30000, damage:180, reward:9000` (VERIFIED_FROM_CLIENT_CODE). Ada respawn timer (`respawn:zi`) dan home area (`home:Ao`) — keberadaan field VERIFIED, **nilai numerik timer & koordinat home masih UNKNOWN** (variabel minified belum diekstrak).

## 19-20. Party & Economy

- Party: EXP split merata + bonus +2%/member; max 12; ±10 level
- Ekonomi: Silver (game) + Gold (premium); Gold Exchange (market order book: goldOrder/goldWatch);
  market gear (marketCreateOrder/GetDepth); mall (starter pack 5 item, premium packs)
- Anti-RMT: megaphone bound, trade restrictions (lihat TRANSLATIONS)

## 21. Network Events (26 terdokumentasi)

buy, casting, defeat, fusion, gold, guild, hit, mail, market, mobSkill, party, pet, pickup,
potion, reaction, refine, repair, resetStats, reveal, revive, sale, skill, skillError, status,
storage, use — schema lengkap di protocol/NETWORK_PROTOCOL_v3.json

**Temuan protokol tambahan:**
- Envelope konsisten `{area, ev}`; event `market` teramati dengan outer area `unknown` — indikasi **broadcast lintas area**
- `castId` format `<playerId>:<tsMs>:<skillId>` — korelasi event `skill` → `hit`
- Field reuse: `potion.damage` = HP healed, `sale.damage` = silver
- 265 player teramati (184 google vs 81 guest, rasio 2.27); area teraktif: dunes (1.762 event/46 player)
- 62 field path character state (44 top-level + nested) — rekonstruksi model data server terlengkap

## 22-23. Changelog & Version Diff

**Dua sumber changelog, cross-validated:**
- CLIENT_BUNDLE_CHANGELOG: 650 entries (changelog-notice-BKeFrGHU.js, snapshot 2026-09-28 pagi)
- OFFICIAL_WEB_CHANGELOG: 669 entries (https://lumivaraonline.com/changelog/ → changelog-notice-Dk8pLLLq.js, retrieved 2026-09-28 18:18)
- **Cross-validation: 649/649 ID match, 0 title/date/time diff, ordering identik.** 19 entries hanya di official = update baru (12:08–15:52) setelah snapshot client. Duplikat ID `2026-09-23-skill-rebalance` konsisten di kedua sumber (fakta upstream).
- Lihat research/changelog/CHANGELOG_CROSS_VALIDATION.{json,md}

Diff v1→v2: +2 class, +14 skill, +5 item, +4 pesan protokol,
−1 (enterArena), rebalancing 8 monster. Lihat diffs/DIFF_v1_v2.json.

**Drop orphans**: 4 item teramati sebagai drop tapi belum terasosiasi ke mob di MONSTER_DB —
`aurora_tail`, `garment`, `honey_wing_dust`, `magma_scale` (kandidat drop mob yang belum terdata / drop world boss).

## 24. Unknowns

1. Koordinat pintu 6 interior area
2. Formula damage/flee/hit server
3. Rate drop aktual server (vs display klien)
4. Quest/mall/pet server state (endpoint butuh login Google)
5. World Boss spawn schedule
6. Gold/Premium pack pricing (zf array di-import tapi definisi tidak ditemukan di bundle yang dianalisis)
7. z5 function — RECONSTRUCTED (V0.7): `floor(level/5)+3` = job points per level. EXP threshold table remains UNKNOWN (GAP-011).
8. Quest harian sepenuhnya server-driven — struktur reward tidak terlihat dari klien

## 25. Confidence Matrix

| Data | Confidence |
|---|---|
| Class/skill/item/card/map/status tables | VERIFIED |
| Monster stats + EXP | VERIFIED |
| Monster drops | DERIVED (asosiasi posisi) |
| Drop rates | VERIFIED (display) / INFERRED (server) |
| Combat formula | OBSERVED (statistik saja) |
| Protokol event schema | VERIFIED |
| Changelog kategori | DERIVED (heuristic) |
| Interior area entrances | UNKNOWN |
