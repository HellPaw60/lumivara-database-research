# STATUS / DOT / DRAIN ANALYSIS V0.5

## Data: 1.570 status events + 111 dot + 120 drain

### Status Teramati (by frequency)

| Status | Events | Arah | Source |
|---|---|---|---|
| spawnguard | 551 | player buff | spawn protection (mekanik, bukan combat) |
| venom | 442 | player→mob | Mamushi Viper Fang/Dokugiri |
| freeze | 265 | player→mob | Mage Frost Area / freezeHit stat |
| stun | 95 | player→mob | stunHit stat |
| burn | 12 | player→mob | Flame Burst / fire coat |
| holyguard | 11 | player buff | Cleric skill |
| remedy | 10 | player buff | status cure |
| poison | 9 | mob→player | Moss Mushroom (18% chance per client table) |
| blind | 8 | player→mob | Cleric Holy Light |
| vanish | 7 | player buff | Thief |
| endure | 7 | player buff | Swordsman Iron Will |
| dokunuri | 6 | player buff | Mamushi |
| crush | 5 | player→mob | crushHit stat |
| spirit/blessing/overthrust/slow/weaken | 1-3 | campur | berbagai skill |

### Drain Events (120)

Contoh: `{"type":"hit", "damage":701, "critical":true, "drainSp":4}` — drainSp menyertai event hit.
- **drainSp/drainHp = field pada event hit** (bukan event terpisah) — OBSERVED
- Client constant: lifesteal cap 10% maxHP/hit, spDrain cap 2% maxSP/hit (VERIFIED_FROM_CLIENT_CODE)

### DoT Events (111)

DoT menyertai status: poison (1.5% maxHP per 2s per STATUS_DB), venom, burn.
Duration dari STATUS_DB: poison 12s, venom 8s (client), dst.

### Status Chance (mob attacks)

Dari mob_status_attacks (CLIENT table): Moss Mushroom poison 18%, Bog Toad 15%, Cave Bat slow 18%, dst.
Runtime: 9 poison events dari Moss Mushroom attacks teramati — konsisten dengan chance < 100% (OBSERVED, sample kecil).

### Status Resistance

resStun/resFreeze cap 80 (client constant) — mekanisme resist teramati di stat caps tapi formula resist UNKNOWN.

## Confidence

- Daftar status + arah: **OBSERVED** (1.570 events)
- Drain sebagai field hit event: **OBSERVED**
- DoT params (duration/dot%/interval): **VERIFIED_FROM_CLIENT_CODE** (STATUS_DB)
- Status chance table (mob): **VERIFIED_FROM_CLIENT_CODE** (W1)
- Formula resist/statusChance player-side: **UNKNOWN**
