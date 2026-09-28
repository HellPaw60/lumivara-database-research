# Lumivara Online — Laporan Pembongkaran v2 (Update 2026-09-28)

**Update sejak analisis pertama:** patch `2026-09-28-kensei-twin-strike` (11:47). Bundle baru: `main-DEXZ0AP0.js`, `items-CvFgs761.js`, + bundle BARU `language-Dz8VbPNM.js` (kamus TH→EN) & CSS terpisah. Protokol WS masih **v5** (kompatibel).

## Konten Baru (diff bundle lama → baru)

### 3 Class Baru (total 10 class)
| Class | Role | Senjata | Unlock |
|---|---|---|---|
| **Kensei** | Katana fighter | Katana + Saya (offhand) | Swordsman 50 + Thief 50 + 120,000 Silver |
| **Nekobaku** | Cat alchemist (bom) | Neko Flask | Merchant 50 + Mamushi 50 + 120,000 Silver |
| **Mamushi** | (sudah ada, kini base unlock chain) | Viper Kunai + Shuriken | base class |

Skill baru terekstrak (14): Kensei — Iaigiri, Oboro Ranbu, Issen, Meikyo Shisui, Katana Mastery, Shukuchi, Zanshin; Mamushi — Viper Fang, Dokugiri, Venom Rupture, Dokunuri, Venom Mastery, Numbing Toxin, Predator's Patience; Nekobaku — Fizz Flask, Tar Flask, Big Kaboom, Catalyst Brew, Alchemy Mastery, Nine Lives, Feline Reflex.

### Item Baru
- **Arrow** (ammo system kembali! 0.1 Silver/pcs, bow wajib ammo) + **Lumina Katana** (starter kensei)
- **Megaphone** — broadcast global 20 dtk, bound, dari Mystery Relic Box 1/1,000,000
- Buff baru: Meikyo Shisui, Catalyst Brew, Nine Lives (พักฟื้น), Dokunuri, Oil (debuff)

### Pesan protokol baru
`unlockClass` (ganti `enterArena` yang dihapus), `reviveHere` (revive di tempat — baru), `guildAnnounce`, `megaphone`.

## Temuan yang Terlewat di Analisis v1

1. **`mob_status_attacks` (W1)** — tabel status attack monster: Moss Mushroom poison 18%, Bog Toad poison 15%, Cave Bat slow 18%, Sunscale Cobra slow 15%, Amber Beetle crush 18%, Pebble Golem crush 15%, Crowned Prism Hopper crush 30%. Kemarin tidak terekstrak.
2. **`TRANSLATIONS.json` (2595 pasang TH→EN)** — dari bundle language baru. Membocorkan mekanik:
   - Equipment drop **dinetralkan 2.5% → 1.25%** per kill
   - Favored slot roll **6x lebih sering** dari slot lain
   - Nama equipment dibatasi **±10 level** dari monster
   - **World Boss Crowned Prism Hopper Lv.100 drop Tier V 100%**
   - Party bonus EXP/Drop **+2%/member** (max 12, ±10 level)
   - Refine stone: daily hunt (100 mob) atau 1% drop Lv.70+
3. **650 entri changelog** (7 hari, ~93 patch/hari) — sejarah lengkap termasuk nerf/buff: arrows pernah dihapus (09-22) lalu dikembalikan (09-28), rebalance skill rutin, glacier monster agresif.
4. **Unlock table (WA)** — syarat unlock class lengkap dengan biaya Silver.
5. **Boss baru teramati via WS**: **Crowned Tempest Drake Lv.280 (11.16M HP)** dan **Crowned Grave Knight Lv.230 (5.8M HP)** — endgame boss yang tidak muncul di run pertama.

## Monster Rebalancing (v1 → v2)

| Monster | HP lama | HP baru | Faktor |
|---|---|---|---|
| Vine Lynx | 109,328 | 1,093,280 | **×10** |
| Bog Toad | 9,217 | 36,868 | ×4 |
| Ember Antler | 20,995 | 83,980 | ×4 |
| Pebble Golem | 225,744 | 56,436 | ÷4 |
| Tide Crab | 33,988 | 8,497 | ÷4 |
| Leaf Sprout | 244 | 61 | ÷4 |
| Thorn Pixie | 788 | 197 | ÷4 |
| Icicle Hare | 4,476 | 1,119 | ÷4 |

(Catatan: sebagian bisa variance elite/non-elite antar run; ambil max HP teramati.)

## Database Final

| File | Isi |
|---|---|
| `GAME_DB.json` | 80 consumable, 49 kartu, 64 skill, 42 status effect, 19 map, drop rates, mob status attacks (BARU), aspd potions (BARU), starter equip 18 (Katana masuk) |
| `MONSTER_DB.json` | 40 spesies, 29 dengan EXP, 27 dengan drop table |
| `TRANSLATIONS.json` | 2595 pasang TH→EN (BARU) |
| `collect/raw-snapshots.json` | ~50K snapshot (14 area) |

## Yang Masih Tertutup

Sama seperti v1: interior `inn`, `cove`, `grove`, `ruins`, `temple`, `arena` (koordinat pintu di kode scene prosedural). `enterArena` kini DIHAPUS dari klien — arena dimasuki via UI dialog `arena-confirm` (perlu diselidiki jalur server-nya di run berikutnya).

## Catatan Riset

- Server masih menerima collector lama tanpa modifikasi (protokol v5 stabil).
- Event `defeat` masih membocorkan baseExp/jobExp/guildExp + nama mob ke seluruh area.
- Guest creation masih terbuka tanpa CAPTCHA/rate-limit yang terlihat.
