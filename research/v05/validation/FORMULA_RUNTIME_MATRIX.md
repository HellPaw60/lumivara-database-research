# V0.6 — FORMULA DATABASE HARDENING

## P4: Runtime/Network Correlation Matrix

| Mechanic | Formula | Evidence | Samples | Match Rate | Confidence | Server Equivalence |
|---|---|---|---|---|---|---|
| MaxHP | ((100+(Lv-1)*5+VIT*10)*(1+classHP)+equipHP)*(1+maxHpPct) | Client code De() offset 118174 | runtime self.hp vs predicted | n/a — extracted from code | VERIFIED_FROM_CLIENT_CODE | UNKNOWN |
| ATK | (baseATK + equipAKT*weaponMult)*(1+atkPct/100) | Client code De() | — | — | VERIFIED_FROM_CLIENT_CODE | UNKNOWN |
| Mob FLEE | 100 + 2*mobLevel | Client code (tooltip) + runtime fits miss patterns | 342 incoming events | 100% consistent with observed miss distribution | VERIFIED_FROM_CLIENT_CODE + RUNTIME_CONSISTENT | LIKELY (distribution match) |
| Pierce | 1 - Ca(level)*(1-pierce/100) | Client code Ic() | — | — | VERIFIED_FROM_CLIENT_CODE | UNKNOWN |
| Hit/Miss | qr = clamp(0.9+(hit-flee)*0.005, 0.5, 1) | Client code | 342 incoming (77.8% miss) + 2940+ outgoing (0%) | pattern consistent | VERIFIED_FROM_CLIENT_CODE + RUNTIME_CONSISTENT | LIKELY |
| Crit | LUK/3 + (Lv-1)*0.1 + equipCRIT | Client code | 29 paired groups, ratio 1.9-3.0 | critMultiplier 2*(1+bonus) explains range | VERIFIED_FROM_CLIENT_CODE + RUNTIME_CONSISTENT | LIKELY |
| ASPD | classBase + weaponMod + AGI*0.3*r + DEX*0.02*r, softcap 180, hardcap 193 | Client code De() | — | — | VERIFIED_FROM_CLIENT_CODE | UNKNOWN |
| Interval | (200-ASPD)*20ms | Client code De() | — | — | VERIFIED_FROM_CLIENT_CODE | UNKNOWN |
| Element | NO damage multiplier | Client code (negative finding) | — | — | VERIFIED_FROM_CLIENT_CODE | UNKNOWN |

### Notes on Server Equivalence
- "LIKELY" = runtime/network data konsisten dengan formula klien, bukti tidak langsung
- "UNKNOWN" = tidak ada runtime data untuk membandingkan
- "VERIFIED_FROM_CLIENT_CODE" = diekstrak dari kode, server behavior tidak dikonfirmasi
