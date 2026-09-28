# HIT/FLEE Analysis (v0.4 Phase 8)

## Temuan Kunci — KOREKSI observasi v0.3

Observasi v0.3: "miss rate 0% dari 2.940 outgoing labeled events". 

**Temuan baru v0.4: sistem miss AKTIF, tapi arahnya berbeda:**

| Arah | Events | Missed | Miss Rate |
|---|---|---|---|
| Player → Mob (outgoing) | 2.940+ | 0 | **0%** |
| Mob → Player (incoming) | 342 | 266 | **77.8%** |

## Interpretasi (HYPOTHESIS — belum konklusi final)

1. **Outgoing 0% miss**: sample bias — semua event outgoing berasal dari player farming mob dengan level sesuai/lebih rendah. HIT stat player cukup vs FLEE mob.
2. **Incoming 77.8% miss**: mob menyerang player yang jauh lebih tinggi levelnya (farming spot) — FLEE player tinggi vs HIT mob rendah. ATAU: banyak event incoming adalah mob mati sebelum serangan mendarat (damage 0 + missed flag).
3. **Schema**: event missed menggunakan schema sama (`type, missed, area, x, damage, incoming, y, mob, player`) — tidak ada schema terpisah untuk miss.

## Yang BELUM bisa disimpulkan

- Apakah HIT/FLEE dipakai di PVP? (tidak ada data arena combat)
- Apakah formula miss beda untuk melee/ranged/magic? (perlu cross-tab skill type × missed)
- Apakah level difference mempengaruhi miss? (level player tidak ada di event — hanya level mob via mobInfo)

## Next Experiment Design

Untuk mengisolasi: butuh observasi player level rendah di area tinggi (mis. guest Lv1 di desert) —
outgoing hit rate harusnya turun jika HIT/FLEE berlaku dua arah. Dapat dilakukan dengan collector
yang mengirim attack ke mob level tinggi dari guest baru.

## Confidence

- Miss system AKTIF untuk mob→player: **OBSERVED** (266/342 events)
- Miss rate player→mob pada level sesuai: **OBSERVED** 0% (sample farming bias)
- Formula miss: **UNKNOWN**
