# DAMAGE VARIANCE ANALYSIS (V0.7)

## Key Finding: Damage is **Mostly Deterministic**

After analyzing 57 controlled groups (same player × skill × mob, ≥10 samples):

| Pattern | Ratio Range | CV Range | Interpretation |
|---|---|---|---|
| Single mob, non-crit | 1.0 – 1.55 | 0.00 – 0.16 | Deterministic formula with minor rounding |
| Single mob, mixed crit | up to 2.0 | up to 0.33 | Crit multiplier (2x base) |
| Cross-mob comparison | up to 3.5 | up to 0.29 | Different DEF values per mob |

## Evidence

1. **No random multiplier detected**: For a single mob with non-crit hits, damage ranges are tight (ratio 1.0-1.55, CV < 0.16). This is consistent with `damage = round(raw_damage) - DEF` with rounding artifacts.

2. **Crit is the dominant source of variance**: Ratio = 2.0x exactly for skills like doublestrafe when crit vs non-crit compared — matches `critMultiplier = 2 × (1 + bonus)`.

3. **Cross-mob variance is DEF-driven**: Different mobs have different DEF (e.g., Crystal Hollows mobs vs Desert mobs), causing 2-3x damage difference for identical player/skill.

4. **No hidden server roll**: If server applied a random multiplier (e.g., 0.9-1.1), we would see continuous distribution within a single mob — not observed. Damage clusters around discrete values.

## Conclusion

| Component | Status |
|---|---|
| Random multiplier | **NOT DETECTED** (no evidence) |
| Damage range | **NOT DETECTED** (no min/max roll) |
| DEF subtraction | **CONFIRMED** (primary source of inter-mob variance) |
| Crit roll | **CONFIRMED** (per-cast, 2x+ multiplier) |
| Pierce | **CONFIRMED** (DEF reduction percentage) |
| Rounding artifact | **CONFIRMED** (minor within-mob variance) |

## Confidence

- Damage formula is **deterministic apart from crit**: **OBSERVED** (57 controlled groups)
- No random roll in damage pipeline: **INFERRED** (distribution analysis)
- Variance sources identified (crit, DEF, pierce, rounding): **OBSERVED**
