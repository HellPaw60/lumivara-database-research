# EXP / PROGRESSION ANALYSIS V0.5

## Data: baseExp per Monster Level (dari 800+ defeat events)

| Lv | n | min | max | mean |
|---|---|---|---|---|
| 8 | 3 | 59 | 118 | 79 |
| 20 | 7 | 183 | 2,196 | 484 |
| 50 | 27 | 753 | 4,518 | 1,241 |
| 70 | 33 | 471 | 15,984 | 3,345 |
| 90 | 153 | 271 | 4,310 | 709 |
| 125 | 166 | 611 | 15,008 | 1,709 |
| 170 | 34 | 140 | 39,786 | 9,585 |
| 200 | 31 | 4,681 | 28,086 | 10,796 |
| 250 | 57 | 1,904 | 42,070 | 6,471 |

## Temuan

1. **Rentang min-max SANGAT lebar per level** (mis. Lv90: 271–4.310) — ini bukan variance random, melainkan **party share & modifier**: event defeat milik player lain dengan party size berbeda. `baseExp` di event = EXP final yang diterima, bukan base monster murni.
2. **MAX per level naik konsisten dengan level** — max(Lv50)=4.518, max(Lv250)=42.070 — pola ~level² terlihat tapi sample terkontaminasi party.
3. **Mean menurun di beberapa level** (Lv90 mean 709 < Lv70 mean 3.345) — dominasi party besar di area populer (Mire Jelly farming spot).

## jobExp

jobExp teramati ≈ baseExp/2 untuk sebagian besar mob (mis. 271→135, 4.310→2.155) — konsisten rasio 50% (OBSERVED, bukan formula confirmed).

## guildExp

guildExp muncul pada sebagian event (~1/4 dari defeat) — hanya player yang punya guild. Nilai ≈ baseExp/8 (OBSERVED).

## Yang Tidak Terjawab

- **z5 function** (base EXP per level player) — tidak terekstrak dari client
- Level cap — tidak ada evidence
- Formula party share eksak (split merata? +2%/member terlihat di string tapi implementasi UNKNOWN)
- EXP penalty level difference (ada di banyak MMORPG — tidak ada evidence di Lumivara)

## Confidence

- baseExp = EXP final diterima (bukan base murni): **OBSERVED**
- jobExp ≈ 50% baseExp: **OBSERVED** (pola konsisten di 20+ monster)
- guildExp ≈ 12.5% baseExp: **OBSERVED** (sample kecil)
- z5 / level table / party formula: **UNKNOWN**
