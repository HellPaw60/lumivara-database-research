# POST-V0.7 FREEZE — CMg3B3wG IMPACT REGISTER

## Boundary Declaration

| Item | Value |
|---|---|
| **V0.7 release snapshot** | `CkIS7ST6` / 688 entries |
| **Post-freeze observation** | `CMg3B3wG` / 730 entries |
| **Delta** | +45 unique entries |
| **Retrieved** | 2026-09-29 03:35 |
| **Bundle sha256** | `ff80df0b6d2b1841` |
| **Status** | POST_FREEZE_OBSERVATION — not part of V0.7 release |

## Classification Summary (45 entries total)

| Domain | Count | Mechanics-relevant |
|---|---|---|
| EQUIPMENT | 6 | ✓ |
| SKILL / CLASS | 5 | ✓ |
| ECONOMY | 3 | ✓ |
| BOT / BEHAVIOR | 4 | ✓ |
| BOSS / SPAWN | 1 | ✓ |
| COMBAT / MONSTER | 1 | ✓ |
| DROP | 1 | ✓ |
| UI / UX | 16 | — |
| WORLD / VISUAL | 4 | — |
| BUG / FIX | 4 | — |
| **TOTAL** | **45** | **21 mechanics-relevant** |

## Detailed Impact Register

| # | Entry ID | Time | Domain | Mechanics Impact | Status |
|---|---|---|---|---|---|
| 1 | `class-gear-sets` | 07:01 | EQUIPMENT | Each class has dedicated gear sets (class-specific equipment availability) | POST_FREEZE_OBSERVATION |
| 2 | `two-handed-x2` | 05:18 | EQUIPMENT | Two-handed weapons receive ×2 stat scaling (fundamental ATK/DEF recalc) | POST_FREEZE_OBSERVATION |
| 3 | `two-handed-special-option` | 23:55 | EQUIPMENT | Two-handed special option ×1.5 multiplier added (affects refine/option bonuses) | POST_FREEZE_OBSERVATION |
| 4 | `bow-one-handed` | 23:11 | EQUIPMENT | Bow reclassified as one-handed + gains 1 card slot (equipment slot interaction changed) | POST_FREEZE_OBSERVATION |
| 5 | `quiver-archer-only` | 00:28 | EQUIPMENT | Quiver restricted to Archer class (class-equipment lock) | POST_FREEZE_OBSERVATION |
| 6 | `quiver-rename` | 22:58 | EQUIPMENT | Feather Arrow → Quiver rename (display/translation, no formula change) | POST_FREEZE_OBSERVATION |
| 7 | `nekobaku-skill-rework` | 04:22 | SKILL | Nekobaku AoE damage and frequency buffed (skill multipliers changed) | POST_FREEZE_OBSERVATION |
| 8 | `nekobaku-skill-effects` | 04:41 | SKILL | Nekobaku full skill effect overhaul (new VFX + behavior) | POST_FREEZE_OBSERVATION |
| 9 | `nekobaku-matk-basic` | 01:47 | SKILL | Nekobaku normal attack now uses MATK (formula: ATK → MATK for basic attacks) | POST_FREEZE_OBSERVATION |
| 10 | `nekobaku-orb` | 01:30 | SKILL | Nekobaku can equip Orb (new weapon-class interaction) | POST_FREEZE_OBSERVATION |
| 11 | `kensei-new-animations` | 01:45 | SKILL | Kensei animation overhaul (cosmetic, no formula change confirmed) | POST_FREEZE_OBSERVATION |
| 12 | `divine-wings-1-in-100k` | 05:50 | DROP | Divine Wings drop rate 10x increased (was ~1/1M, now ~1/100K) | POST_FREEZE_OBSERVATION |
| 13 | `boss-every-channel` | 06:02 | BOSS/SPAWN | Bosses now spawn on every channel (spawn frequency/availability changed) | POST_FREEZE_OBSERVATION |
| 14 | `monster-damage-accuracy` | 06:41 | COMBAT/MONSTER | Monster damage reduced but accuracy increased (ATK/STAT tradeoff) | POST_FREEZE_OBSERVATION |
| 15 | `lock-allows-refine-market` | 04:04 | ECONOMY | Locked items can now be refined and sold (economy flow change) | POST_FREEZE_OBSERVATION |
| 16 | `gold-exchange-closes-before-launch` | 03:13 | ECONOMY | Gold market closes before server maintenance launch | POST_FREEZE_OBSERVATION |
| 17 | `launch-gold-carry` | 02:28 | ECONOMY | Gold carries over to new server launch (currency persistence) | POST_FREEZE_OBSERVATION |
| 18 | `bot-long-cooldown-first` | 06:05 | BOT | Bot prioritizes long-cooldown skills (behavioral AI logic) | POST_FREEZE_OBSERVATION |
| 19 | `bot-instant-next-target` | 03:48 | BOT | Bot instantly switches to next target after kill | POST_FREEZE_OBSERVATION |
| 20 | `bot-approach-skill-resend` | 03:33 | BOT | Bot approaches then immediately casts (reduced idle walking) | POST_FREEZE_OBSERVATION |
| 21 | `bot-auto-coat-fix` | 23:33 | BOT | Bot auto-element-coating fixed (reliability improvement) | POST_FREEZE_OBSERVATION |

## Domains Affected (mechanics-relevant)

| Domain | Entries | Key Changes |
|---|---|---|
| EQUIPMENT | 6 | Two-handed ×2, bow→1H+card, class-locked quiver |
| SKILL | 5 | Nekobaku rework (MATK basic, AoE buff, Orb equip) |
| BOT | 4 | Target switching, skill priority, approach-cast logic |
| ECONOMY | 3 | Locked item trade/refine, gold market, gold carry |
| BOSS/SPAWN | 1 | Boss every channel (spawn density) |
| COMBAT/MONSTER | 1 | Monster damage ↓ / accuracy ↑ |
| DROP | 1 | Divine Wings 10x rate increase |

## Not Mechanics-Relevant (24 entries)

| Domain | Count | Examples |
|---|---|---|
| UI/UX | 16 | Storage rarity tiles, keybinds, chat persistence, inspect privacy, screen shake, gear marks, bag tabs |
| WORLD/VISUAL | 4 | Aurelia town redesign, NPC redistribution, monster walk frames, wander emotes |
| BUG/FIX | 4 | Portal depth, socket disconnect, splash kill, zoom disconnect |

## Action Required for V0.8

All 21 mechanics-relevant entries above are **observations only**. They require:
1. Static client bundle re-extraction to locate new constants/formulas
2. Runtime verification via controlled experiments
3. Cross-reference against existing formula database entries
4. Confidence classification per standard (VERIFIED/OBSERVED/INFERRED/UNKNOWN)

**Do NOT merge into V0.7 release data. Treat as V0.8 input queue.**
