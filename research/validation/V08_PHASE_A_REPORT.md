# V0.8 PHASE A — CHANGELOG DELTA AUDIT

## Boundary Declaration

| Item | Value |
|---|---|
| **V0.7 release snapshot** | `CkIS7ST6` / 688 entries |
| **V0.8 observation** | `CMg3B3wG` / 730 entries |
| **Delta** | +42 unique entries vs V0.7 baseline |
| **Retrieved** | 2026-09-29 03:35 |
| **Bundle sha256** | `ff80df0b6d2b1841` |
| **Status** | PHASE A COMPLETE — classification finalized |

## Classification Summary

| Category | Count | Mechanics-Relevant? |
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

## Detailed Classification

### MECHANICS-RELEVANT (21)

| # | Entry ID | Time | Domain | Impact | Evidence |
|---|---|---|---|---|---|
| 1 | `class-gear-sets` | 07:01 | EQUIPMENT | Class-specific equipment loadout (Novice→First job keeps items) | Changelog only |
| 2 | `two-handed-x2` | 05:18 | EQUIPMENT | Two-handed weapons: stats ×2 (Staff, Quarterstaff, Dagger Pair, Hammer) | Changelog only |
| 3 | `two-handed-special-option` | 23:55 | EQUIPMENT | Two-handed special option ×1.5 multiplier | Changelog only |
| 4 | `bow-one-handed` | 23:11 | EQUIPMENT | Bow reclassified as one-handed + 1 card slot | Changelog only |
| 5 | `quiver-archer-only` | 00:28 | EQUIPMENT | Quiver restricted to Archer class | Changelog only |
| 6 | `quiver-rename` | 22:58 | EQUIPMENT | Feather Arrow → Quiver rename (display only) | Changelog only |
| 7 | `nekobaku-skill-rework` | 04:22 | SKILL | Fizz Flask AoE radius 1.5 tiles, Tar Flask CD 0.5s (was 3s) | Changelog only |
| 8 | `nekobaku-skill-effects` | 04:41 | SKILL | Nekobaku full skill effect overhaul (VFX + behavior) | Changelog only |
| 9 | `nekobaku-matk-basic` | 01:47 | SKILL | Normal attack uses MATK instead of ATK | Changelog only |
| 10 | `nekobaku-orb` | 01:30 | SKILL | Nekobaku can equip Orb (new weapon-class interaction) | Changelog only |
| 11 | `kensei-new-animations` | 01:45 | SKILL | Kensei animation overhaul (cosmetic, no formula change confirmed) | Changelog only |
| 12 | `divine-wings-1-in-100k` | 05:50 | DROP | Divine Wings drop rate 10x increased (Mystery Relic Box) | Changelog only |
| 13 | `boss-every-channel` | 06:02 | BOSS/SPAWN | Crowned boss spawns every channel, respawns after 1 hour | Changelog only |
| 14 | `monster-damage-accuracy` | 06:41 | COMBAT/MONSTER | Monster damage reduced by level, accuracy increased | Changelog only |
| 15 | `lock-allows-refine-market` | 04:04 | ECONOMY | Locked items can be refined and sold on market | Changelog only |
| 16 | `gold-exchange-closes-before-launch` | 03:13 | ECONOMY | Gold market closes before server maintenance | Changelog only |
| 17 | `launch-gold-carry` | 02:28 | ECONOMY | Gold carries over to new server launch | Changelog only |
| 18 | `bot-long-cooldown-first` | 06:05 | BOT | Bot prioritizes long-cooldown skills | Changelog only |
| 19 | `bot-instant-next-target` | 03:48 | BOT | Bot instantly switches to next target after kill | Changelog only |
| 20 | `bot-approach-skill-resend` | 03:33 | BOT | Bot approaches then immediately casts | Changelog only |
| 21 | `bot-auto-coat-fix` | 23:33 | BOT | Bot auto-element-coating fixed | Changelog only |

### NON-MECHANICS (24)

| # | Entry ID | Time | Domain | Reason |
|---|---|---|---|---|
| 1 | `aurelia-town-v2` | 05:39 | WORLD/VISUAL | Aurelia town redesign (cosmetic) |
| 2 | `aurelia-npc-spread` | 06:59 | WORLD/VISUAL | NPC redistribution (cosmetic) |
| 3 | `monster-walk-frames` | 05:14 | WORLD/VISUAL | Monster walk animations (cosmetic) |
| 4 | `monster-wander-emotes` | 04:32 | WORLD/VISUAL | Monster wander + emotes (cosmetic) |
| 5 | `screen-shake-setting` | 06:15 | UI/UX | Screen shake toggle (preference) |
| 6 | `keybinds-gamepad` | 06:33 | UI/UX | Keybind customization (preference) |
| 7 | `storage-rarity-tiles` | 06:29 | UI/UX | Storage rarity color frames (display) |
| 8 | `inspect-equipment-frame` | 05:57 | UI/UX | Inspect window redesign (display) |
| 9 | `status-cards` | 05:55 | UI/UX | Status window card layout (display) |
| 10 | `remove-spell-total` | 05:45 | UI/UX | Remove TOTAL label from spell damage (display) |
| 11 | `gear-marks-everywhere` | 00:10 | UI/UX | Gear refine marks on all windows (display) |
| 12 | `party-guild-chat-unread` | 06:56 | UI/UX | Party/guild chat unread counters (display) |
| 13 | `chat-kept-on-device` | 04:30 | UI/UX | Chat history persists locally (storage) |
| 14 | `party-finder-size` | 23:50 | UI/UX | Party finder shows member count (display) |
| 15 | `inspect-privacy` | 23:24 | UI/UX | Inspect privacy toggle (preference) |
| 16 | `inspect-privacy-on-equipment` | 01:48 | UI/UX | Privacy toggle moved to equipment page (display) |
| 17 | `fusion-picker-right` | 01:53 | UI/UX | Fusion picker moved to right side (display) |
| 18 | `fusion-picked-top` | 23:40 | UI/UX | Fusion selection highlight (display) |
| 19 | `google-link-confirm` | 04:55 | UI/UX | Google account link confirmation (auth flow) |
| 20 | `zoom-view-once` | 02:52 | BUG/FIX | Zoom disconnect bug fix |
| 21 | `socket-budget-no-kick` | 02:41 | BUG/FIX | Socket disconnect bug fix |
| 22 | `portal-depth-retry` | 03:13 | BUG/FIX | Portal bounce-back bug fix |
| 23 | `splash-kill-keeps-target` | 02:24 | BUG/FIX | Splash skill target loss bug fix |
| 24 | `bag-card-tab` | 22:38 | UI/UX | Bag card tab separation (display) |

## Evidence Assessment

### Has Client Implementation Evidence

| Entry | Evidence | Location |
|---|---|---|
| `nekobaku-matk-basic` | `basicPower=="matk"` branch exists | main-DEXZ0AP0.js @2336209 |
| `nekobaku-skill-rework` | `nekoflask` skill definition with `matk` damage type | items-CvFgs761.js @108345 |
| `bow-one-handed` | Bow in `slot:"sword"` (one-handed slot) | items-CvFgs761.js @149315 |
| `quiver-archer-only` | Quiver empty check + archer-only logic | main-DEXZ0AP0.js @2296936 |

### Changelog Claim Only (No Client Evidence Yet)

| Entry | Status |
|---|---|
| `two-handed-x2` | Server-side or new bundle (not in main-DEXZ0AP0.js) |
| `two-handed-special-option` | Server-side or new bundle |
| `class-gear-sets` | Server-side or new bundle |
| `divine-wings-1-in-100k` | Server-side or new bundle |
| `boss-every-channel` | Server-side or new bundle |
| `monster-damage-accuracy` | Server-side or new bundle |
| `lock-allows-refine-market` | Server-side or new bundle |
| `gold-exchange-closes-before-launch` | Server-side or new bundle |
| `launch-gold-carry` | Server-side or new bundle |
| `bot-*` (4 entries) | Bot behavior, likely server-side |

## Priority for Phase B-G

| Priority | Phase | Entries | Approach |
|---|---|---|---|
| **HIGH** | B (Equipment) | `two-handed-x2`, `two-handed-special-option`, `bow-one-handed`, `quiver-archer-only`, `class-gear-sets` | Search new bundle (main-CFj0fJNd.js) for weapon type detection + stat multiplier |
| **HIGH** | C (Skill/Class) | `nekobaku-matk-basic`, `nekobaku-skill-rework`, `nekobaku-orb`, `nekobaku-skill-effects` | Cross-reference skill definitions in items bundle + runtime experiment |
| **MEDIUM** | D (Combat/Monster) | `monster-damage-accuracy`, `boss-every-channel` | Compare with existing Mob FLEE formula + incoming damage pipeline |
| **MEDIUM** | E (Drop) | `divine-wings-1-in-100k` | Search for drop table constants in new bundle |
| **LOW** | F (Economy) | `lock-allows-refine-market`, `gold-exchange-closes-before-launch`, `launch-gold-carry` | Server-side authoritative, document as UNKNOWN |
| **LOW** | G (Bot) | `bot-long-cooldown-first`, `bot-instant-next-target`, `bot-approach-skill-resend`, `bot-auto-coat-fix` | Bot behavior, not game mechanic |

## Gap Status (Initial V0.8)

| ID | Status | V0.8 Impact |
|---|---|---|
| GAP-001 | PARTIALLY_RESOLVED | No change (z5 already reconstructed) |
| GAP-002 | OPEN | No new evidence from changelog |
| GAP-005 | RESOLVED | No change (damage variance confirmed) |
| GAP-011 | OPEN | **HIGH PRIORITY** — EXP threshold still UNKNOWN. Changelog does not reveal EXP table. |

## Action Items for V0.8

1. **Search new bundle** (main-CFj0fJNd.js) for two-handed weapon detection logic
2. **Extract skill multipliers** for Nekobaku rework from items bundle
3. **Run controlled experiments** for:
   - Two-handed weapon ATK calculation
   - Bow card slot interaction
   - Nekobaku MATK basic attack damage
4. **Document Divine Wings drop rate** as server-side UNKNOWN unless client constant found
5. **Update GAP-011** with empirical EXP measurement plan

## Conclusion

V0.7 release snapshot remains `CkIS7ST6` / 688. CMg3B3wG / 730 is post-freeze observation with 21 mechanics-relevant entries. 4 entries have partial client evidence (nekobaku skills, bow slot). 17 entries are changelog-only claims requiring further investigation in V0.8 Phase B-G.
