# HIT/FLEE ANALYSIS V0.5 (update dari v0.4)

## Data Baru: Miss Rate Incoming per Mob

Cross-tab 342 incoming (mob→player) events per target mob:

| Area | Mob ID | Total | Missed | Rate |
|---|---|---|---|---|
| dunes | #120 | 12 | 2 | 16.7% |
| desert | #109 | 10 | 6 | 60.0% |
| swamp | #74 | 9 | 6 | 66.7% |
| desert | #33 | 8 | 7 | 87.5% |
| desert | #25 | 7 | 7 | 100% |
| dunes | #2 | 7 | 7 | 100% |
| glacier | #62 | 6 | 6 | 100% |
| tempest | #121 | 5 | 5 | 100% |

## Interpretasi (HYPOTHESIS — bukan formula final)

1. **Miss rate incoming bervariasi per player target** (setiap mob-id menyerang player berbeda di event ini) — konsisten dengan `missChance = f(attackerHIT, targetFLEE)`.
2. Beberapa target 100% missed — player FLEE jauh melampaui mob HIT (farming spot, player over-leveled).
3. Outgoing 0% miss pada player farming mob level sesuai — HIT player >> FLEE mob.
4. **Formula tetap UNKNOWN** — level player tidak tersimpan di event, tidak bisa memisahkan HIT vs FLEE vs levelDiff.

## Eksperimen yang Masih Diperlukan

E1 (guest Lv1 attack mob Lv50+) tetap satu-satunya jalan mengisolasi level difference.

## Confidence

- Sistem miss aktif dua arah: **OBSERVED**
- missChance = f(HIT, FLEE, ...): **INFERRED** (konsisten dengan variasi per target, belum terisolasi)
- Formula eksak: **UNKNOWN**
