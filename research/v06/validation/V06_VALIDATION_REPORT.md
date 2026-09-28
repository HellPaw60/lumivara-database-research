# V0.6 Validation Report

## Baseline
| Field | Value |
|---|---|
| Commit | `c2eac65` (FINAL V0.6 release state) |
| Tag | `v0.6-mechanics-validation` |
| Previous | `1bd5fd6` (initial V0.6) → `d797ee1` (first cleanup) → `371bf84` (changelog V3B archive) → `c15274d` (provenance correction) → `6baeede` (freeze attempt #1) → `c2eac65` (FINAL V0.6 release state) |
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
| V0.6 (release) | `B6x3YIz5` | 685 |

### Post-Freeze Observation (informational, not part of V0.6 release)
After V0.6 freeze (commit c2eac65), the official changelog bundle changed:
- From: `B6x3YIz5` (685 entries, archived as V0.6 snapshot)
- To: `CkIS7ST6` (688 entries)
- Delta: 3 new UI/UX entries (Quiver rename, bag card tab, bot coat fix)
- Archived as: `OFFICIAL_CHANGELOG_POSTV06.json` (observational, not V0.6 release data)

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

## Validation Checks (7/7 PASS)
| Check | Status |
|---|---|
| JSON validity | PASS |
| Formula schema/confidence | PASS |
| SQLite integrity | PASS |
| Changelog freshness | PASS (B6x3YIz5 confirmed at final check) |
| Changelog delta | PASS |
| Raw preservation | PASS |
| V0.5/V0.6 artifact consistency | PASS |

## Server-Equivalence Status
- **LIKELY**: Mob FLEE, Hit/Miss, Crit (distributional fit to client formula)
- **UNKNOWN**: MaxHP, ATK, Pierce, ASPD, Interval, Damage pipeline

## Cleanup Actions Performed
1. Added `formula_type` field to all 36 formulas (semantic classification)
2. Crit runtime matrix updated with weapon-type ×2 modifier
3. Gap register confidence labels normalized to {UNKNOWN, INFERRED}
4. Final changelog check: B6x3YIz5 unchanged from the immediately preceding V0.6 final-check retrieval

## Remaining Work
10 gaps remain unresolved — see GAP_REGISTER.json for details.
