# COMBAT EXPERIMENT PLAN (v0.4 Phase 7)

## Data Terkendali yang Sudah Ada

395 grup (player × skill × mob × area) — **144 grup dengan ≥5 sampel** = kandidat analisis variabel terkontrol.

## Variabel yang Dapat Diisolasi dari Data Eksisting

| Variabel | Cara Isolasi | Status |
|---|---|---|
| Crit vs non-crit (same player/skill/mob) | Bandingkan damage dalam grup sama | BISA — data ada |
| Multi-hit (double) | event dengan hits[] | BISA — 399 event |
| Skill berbeda (same player/mob) | Cross-grup per player+mob | BISA |
| Mob berbeda (same player/skill) | Cross-grup per player+skill | BISA |
| Level difference | TIDAK BISA — level player tidak ada di event | BUTUH collector baru |

## OBSERVED FACTS (dari data, bukan hipotesis)

1. `damage == sum(hits[])` pada multi-hit — 399 event konsisten
2. Crit damage > non-crit damage konsisten di semua skill teramati
3. Miss hanya teramati pada arah mob→player (266/342 incoming)
4. skillError menyertakan alasan teks (cooldown, range, ammo habis)

## HYPOTHESES (belum diverifikasi — JANGAN diperlakukan sebagai formula)

- H1: Crit multiplier ~2x-4x tergantung skill (distribusi lebar — twinfang 7.29x mean tapi stdev 22.289)
- H2: Damage punya variance random ±X% per hit (perlu uji distribusi dalam grup terkontrol)
- H3: Mob defense mengurangi damage flat atau persentase (perlu mob berbeda, same player+skill)
- H4: Miss formula = f(playerHIT, mobFLEE, levelDiff) — tidak dapat diverifikasi dari data eksisting

## Eksperimen yang Diperlukan (butuh collector aktif)

| Eksperimen | Desain | Variabel Terisolasi |
|---|---|---|
| E1: Guest Lv1 attack mob Lv50 | guest baru → field/desert → attack | level diff effect pada miss/damage |
| E2: Same skill, mob berbeda | attack Scarab vs Cobra dengan skill sama | defense per mob |
| E3: Crit rate per skill | hitung crit frequency per skill dalam grup ≥30 | crit stat effect |
| E4: Potion effect | damage before/after potion | buff effect |

**CATATAN ETIKA RISET**: eksperimen pasif terbatas — mengamati player lain + guest sendiri farming normal. Tidak ada load testing atau spam.

## Formula Candidates: BELUM ADA

Tidak ada formula damage yang dapat diajukan dengan confidence > INFERRED dari data eksisting. Eksperimen E1-E4 diperlukan sebelum fitting formula apa pun.
