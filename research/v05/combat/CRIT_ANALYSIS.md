# CRIT SYSTEM ANALYSIS V0.5

## Data: 29 Paired Groups (player × skill, ≥5 crit + ≥5 non-crit)

### Temuan Utama

**1. Crit ratio BUKAN konstanta global — bervariasi per player:**

| Skill | Player (nC/nN) | Ratio |
|---|---|---|
| coldbolt | 23/65 | 2.453 |
| coldbolt | 7/62 | 1.925 |
| coldbolt | 9/58 | 2.175 |
| viperfang | 42/6 | 2.356 |
| viperfang | 24/14 | 2.904 |
| iaigiri | 19/9 | 3.000 |
| doublestrafe | 12/30 | 2.500 |

Rentang ratio: **1.925 – 3.000** antar player (skill sama = coldbolt pun beda antar player: 1.9–2.5).

**2. Crit rate bervariasi ekstrem per player: 0.093 – 0.875**

- viperfang player A: 87.5% crit rate (heavy CRIT stat build)
- coldbolt player D: 9.3%

**3. Multi-hit crit roll = PER-CAST, bukan per-hit:**

399/399 double-hit events memiliki `crits[]` uniform (kedua hit crit atau kedua tidak).
Bukti: `damage=8874, hits=[4437, 4437], crits=[True, True]` — identik dan seragam.

**4. Variance dalam multi-hit:**

- 146/200 event: hits identik (ratio 1.0)
- Mean max/min ratio: 1.054
- Outlier hingga 4.059 — indikasi variance roll terpisah per hit pada sebagian skill, atau interaksi dengan DEF per hit

## Model Kandidat (HYPOTHESIS)

```
critChance = f(CRIT_stat, LUK, ...)          # per player — changelog: "crit เวท = LUK/3 + CRIT dari equipment"
critMultiplier = base × (1 + critDmg/100)     # critDmg dari equipment/card — cap 60 (client)
crit roll: sekali per CAST (multi-hit mewarisi hasil roll)
```

## Yang Belum Terjawab

- Nilai base multiplier (estimasi ~2x dari data, tapi variasi 1.9-3.0 mengindikasikan critDmg stat berpengaruh)
- Formula critChance eksak
- Apakah crit roll terjadi sebelum atau sesudah miss roll

## Confidence

- Crit ratio bervariasi per player: **OBSERVED** (29 paired groups)
- Per-cast crit roll: **OBSERVED** (399/399 uniform)
- Formula critChance/multiplier: **UNKNOWN** (menunggu hasil mining client code)
