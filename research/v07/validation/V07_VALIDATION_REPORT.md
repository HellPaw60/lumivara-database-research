# V07 VALIDATION REPORT

## Remote Baseline
| Field | Value |
|---|---|
| main | `e45b23da100bd6338e1f9b39a066f12c1971704f` |
| v0.7-global-mechanics | `e45b23da100bd6338e1f9b39a066f12c1971704f` |
| v0.6-mechanics-validation | `82fde9aef4a131d4b2a84b01081fb0d9fca5d4df` |
| v0.5-global-mechanics | `6131965787a638fe2da0d6c2e1c7c4606fd43730` |

## Changelog Snapshot (V0.7 Release)
| Field | Value |
|---|---|
| Bundle | `CkIS7ST6` |
| Entries | 688 |
| Status | V0.7 release snapshot — frozen |
| html sha256 | `ef8cecea4feef885` |

### Post-V0.7 Changelog Observation (NOT part of V0.7 release)
| Bundle | `CMg3B3wG` |
| Entries | 730 |
| Delta vs V0.7 snapshot | +45 entries |
| Status | POST_FREEZE_OBSERVATION |
| Retrieved | 2026-09-29 03:35 |
| Bundle sha256 | `ff80df0b6d2b1841` |

### Post-V0.7 Observations (45 entries, not part of V0.7 release data)
| Category | Count | Examples |
|---|---|---|
| Equipment/Balance | 6 | Two-handed ×2 stats, bow one-handed + card slot, class-locked quiver |
| Skills/Balance | 5 | Nekobaku skill effects/rework, MATK basic, Kensei animations |
| Bot/Automation | 4 | Bot instant next target, approach skill resend |
| Economy | 3 | Locked item trade/refine, gold market, gold carry |
| Boss/Spawn | 1 | Boss every channel |
| Combat/Monster | 1 | Monster damage ↓ / accuracy ↑ |
| Drop | 1 | Divine Wings 10x rate increase |
| UI/UX | 16 | Storage rarity tiles, screen shake, zoom, keybinds, inspect privacy |
| World/Visual | 4 | Aurelia town redesign, NPC redistribution, walk frames, emotes |
| Bug/Fix | 4 | Portal depth, socket disconnect, splash kill, zoom disconnect |

## Historical Progression
| Version | Bundle | Entries |
|---|---|---|
| V0.4.x | `Dk8pLLLq` | 669 |
| V0.5 | `D0Wscyxj` | 678 |
| V0.6 | `B6x3YIz5` | 685 |
| V0.7 | `CkIS7ST6` | 688 |

## V0.7 Research Results

### 1. z5 Reconstruction (GAP-001: PARTIALLY_RESOLVED)
| Item | Value |
|---|---|
| Function | `F0 = A => Math.floor(A/5) + 3` |
| Purpose | **Job Points per Level** (NOT EXP table) |
| Chain | `F0 → dY → z5` |
| Source | `web-v2/items-CvFgs761.js` offset 116487 |
| Confidence | **VERIFIED_FROM_CLIENT_CODE** (exact match) |
| Related | `$0 = floor((Lv-1)/10)+2` (stat points), `It = Σ F0(2..Lv)` (cumulative) |

### 2. EXP Threshold Table (GAP-011: OPEN)
| Item | Value |
|---|---|
| Status | **UNKNOWN** — server-side only |
| Evidence | Client bundles contain no EXP table. z5 is points, not EXP. |
| Method needed | Server disassembly or empirical measurement (track EXP/level-ups) |

### 3. Damage Variance (GAP-005: RESOLVED)
| Finding | Evidence |
|---|---|
| No random multiplier detected | 57 controlled groups, CV < 0.16 for single-mob non-crit |
| Crit is dominant variance source | Ratio = 2.0x exactly (crit vs non-crit) |
| DEF-driven cross-mob variance | 2-3x difference across areas |
| Rounding artifact | Minor within-mob spread |
| **Conclusion** | Formula is **deterministic apart from crit** (OBSERVED). No random roll in damage pipeline (INFERRED from distribution). |

### 4. Server Equivalence
| Mechanic | Client | Runtime | Server Equivalence |
|---|---|---|---|
| Mob FLEE | 100+2×Lv | ✓ | LIKELY |
| Hit/Miss | qr(HIT,FLEE) | ✓ | LIKELY |
| Crit | LUK/3+... | ✓ | LIKELY |
| Damage | ATK×factor−DEF | ✓ | LIKELY |
| Pierce | %(1-Ca×(1-p/100)) | — | UNKNOWN |
| z5 (job points) | floor(Lv/5)+3 | ✓ | N/A (client-only) |

## Formula Database
| Metric | Value |
|---|---|
| Total formulas | **38** |
| COMPUTED_FORMULA | 27 |
| LOOKUP_TABLE | 3 |
| CONDITIONAL_RULE | 3 |
| MECHANIC_DEFINITION | 5 |
| VERIFIED_FROM_CLIENT_CODE | 33 |
| OBSERVED | 4 |
| INFERRED | 1 |
| V0.7 changes | z5 verified (was UNKNOWN), +2 formulas ($0, It) |

## Gap Register
| ID | Subsystem | Status |
|---|---|---|
| GAP-001 | PROGRESSION | PARTIALLY_RESOLVED |
| GAP-002 | PARTY | OPEN |
| GAP-003 | DROP | OPEN |
| GAP-004 | REFINE | OPEN |
| GAP-005 | DAMAGE | **RESOLVED** |
| GAP-006 | MONSTER | OPEN |
| GAP-007 | PvP | OPEN |
| GAP-008 | SKILL | OPEN |
| GAP-009 | ASPD | OPEN |
| GAP-010 | STORAGE | OPEN |
| GAP-011 | PROGRESSION | OPEN |
| **Total unique** | **11** |
| Resolved | 1 |
| Partially resolved | 1 |
| Open | 9 |

## Validation Checks (8/8 PASS)
| Check | Status |
|---|---|
| JSON validity | PASS |
| Formula schema & confidence | PASS |
| SQLite integrity | PASS |
| Changelog freshness | PASS |
| Raw preservation | PASS |
| V0.5/V0.6/V0.7 artifact consistency | PASS |
| Gap ID uniqueness | PASS |
| Documentation cross-reference | PASS |

## Sample Counts
| Analysis | Samples |
|---|---|
| Controlled damage groups | 57 groups (≥10 hits each) |
| Paired crit/non-crit | 29 groups |
| Outgoing damage events | 2,940+ |
| Incoming damage events | 342 |

## Worktree Status
**CLEAN** — no untracked or modified files.

## Scope
GLOBAL mechanics only. Thief used as test vector for controlled experiments.
