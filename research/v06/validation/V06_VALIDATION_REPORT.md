# V0.6 Validation Report

## Baseline
| Field | Value |
|---|---|
| Commit | `d797ee1` (final V0.6 cleanup) |
| Tag | `v0.6-mechanics-validation` |
| Previous | `1bd5fd6` (initial V0.6) → `d797ee1` (final) |
| v0.5 baseline | `6131965` |

## Changelog Snapshot
| Field | Value |
|---|---|
| Bundle | `B6x3YIz5` |
| Entries | 685 |
| Status | 6 new entries since V0.6 initial — all UI/UX, no mechanics impact |
| Check time | 2026-09-28T19:55 |

### Historical Progression
| Version | Bundle | Entries |
|---|---|---|
| V0.4.x | `Dk8pLLLq` | 669 |
| V0.5 | `D0Wscyxj` | 678 |
| V0.6 | `B6x3YIz5` | 685 |

## Files Changed (this cleanup)
| File | Change |
|---|---|
| `formulas/FORMULA_DATABASE_V05.json` | +formula_type classification (COMPUTED/LOOKUP/CONDITIONAL/MECHANIC) |
| `research/v05/validation/FORMULA_RUNTIME_MATRIX.md` | Crit formula: +weapon modifier term |
| `research/v05/validation/GAP_REGISTER.json` | confidence normalized |

## Formula Database
| Metric | Value |
|---|---|
| Total formulas | 36 |
| COMPUTED_FORMULA | 24 |
| LOOKUP_TABLE | 3 |
| CONDITIONAL_RULE | 3 |
| MECHANIC_DEFINITION | 6 |

## Gap Register
| Priority | Count |
|---|---|
| HIGH | 2 (z5 EXP table, party split) |
| MEDIUM | 5 (drop rates, refine server, damage variance, monster stats, PvP) |
| LOW | 3 (cast time, ASPD-skill, storage) |

## Validation Checks
| Check | Status |
|---|---|
| JSON validity | PASS |
| Formula schema/confidence | PASS |
| SQLite integrity | PASS |
| Changelog freshness | PASS (unchanged) |
| Changelog delta | PASS |
| Raw preservation | PASS |
| V0.5/V0.6 artifact consistency | PASS |
| Documentation/path consistency | PASS |

## Server-Equivalence Status
- **LIKELY**: Mob FLEE, Hit/Miss, Crit (distributional fit to client formula)
- **UNKNOWN**: MaxHP, ATK, Pierce, ASPD, Interval, Damage pipeline

## Cleanup Actions Performed
1. Added `formula_type` field to all 36 formulas (semantic classification)
2. Crit runtime matrix updated with weapon-type ×2 modifier
3. Gap register confidence labels normalized to {UNKNOWN, INFERRED}
4. Final changelog check: unchanged

## Remaining Work
10 gaps remain unresolved — see GAP_REGISTER.json for details.
