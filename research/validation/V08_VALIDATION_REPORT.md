# V0.8 VALIDATION REPORT

## Remote Baseline
| Field | Value |
|---|---|
| main | `e036caf5140d44375de7c9c6f64b33f3750a1a4c` |
| v0.8-global-mechanics | `e036caf5140d44375de7c9c6f64b33f3750a1a4c` ✓ MATCH |
| v0.7-mechanics-validation | `f5ab9dd54965c583f6a35eb1d1bfb8770b9d5b06` ✓ preserved |

## Changelog Status
| Check | Bundle | Entries | Status |
|---|---|---|---| 
| V0.8 start | `CMg3B3wG` | 730 | — |
| V0.8 final | `CMg3B3wG` | 730 | **UNCHANGED** |

## Historical Progression
| Version | Bundle | Entries |
|---|---|---|
| V0.4.x | `Dk8pLLLq` | 669 |
| V0.5 | `D0Wscyxj` | 678 |
| V0.6 | `B6x3YIz5` | 685 |
| V0.7 | `CkIS7ST6` | 688 |
| V0.8 | `CMg3B3wG` | 730 |

## V0.8 Research Results

### Phase A — Changelog Delta Audit
- **42 delta entries** vs V0.7 baseline
- **16 mechanics-relevant**, 26 non-mechanics
- **3 reclassified** to non-mechanics (VFX, rename, server maintenance)
- **6 new formulas**

### Phase B — Equipment Mechanics
| Finding | Status |
|---|---|
| Two-handed detection (`Ee()`) | VERIFIED_FROM_CLIENT_CODE |
| Two-handed multiplier (`Ar=2`) | VERIFIED_FROM_CLIENT_CODE |
| Card slot count (`Dt()`) | VERIFIED_FROM_CLIENT_CODE |
| Bow = one-handed | VERIFIED_FROM_CLIENT_CODE |
| Class gear sets (`classEquipped`) | VERIFIED_FROM_CLIENT_CODE |

### Phase C — Skill/Class Mechanics
| Finding | Status |
|---|---|
| Nekobaku MATK basic (`Z0()`) | VERIFIED_FROM_CLIENT_CODE |
| MATK uses mpierce (not pierce) | VERIFIED_FROM_CLIENT_CODE |
| Nekobaku Orb equip | VERIFIED_FROM_CLIENT_CODE |
| Skill level scaling | VERIFIED_FROM_CLIENT_CODE |
| Cooldown-from-ASPD formula | VERIFIED_FROM_CLIENT_CODE |

### Phase D — Combat/Monster
| Finding | Status |
|---|---|
| Monster damage reduction | SERVER_SIDE_ONLY |
| Monster accuracy/FLEE | SERVER_SIDE_ONLY |
| Boss every channel | SERVER_SIDE_ONLY |

### Phase E — Drop
| Finding | Status |
|---|---|
| Divine Wings 1/100K | SERVER_SIDE_ONLY |
| Mystery Relic Box | SERVER_SIDE_ONLY |
| All drop mechanics | SERVER_SIDE_ONLY |

### Phase F — Economy
| Finding | Status |
|---|---|
| Locked item refine/market | SERVER_SIDE_ONLY |
| Gold market closure | SERVER_SIDE_ONLY |
| Gold carry-over | SERVER_SIDE_ONLY |
| All economy mechanics | SERVER_SIDE_ONLY |

### Phase G — Bot Behavior
| Finding | Status |
|---|---|
| Long-cooldown-first | NON-MECHANICS |
| Instant next target | NON-MECHANICS |
| Approach-skill-resend | NON-MECHANICS |
| Auto-coat fix | BUG/Fix |

## Formula Database
| Metric | V0.7 | V0.8 |
|---|---|---|
| Total | 38 | **47** |
| COMPUTED_FORMULA | 27 | **31** |
| CONDITIONAL_RULE | 3 | **7** |
| LOOKUP_TABLE | 3 | **4** |
| MECHANIC_DEFINITION | 5 | **5** |
| VERIFIED_FROM_CLIENT_CODE | 33 | **42** |

### New Formulas
| ID | Name | Type | Source |
|---|---|---|---|
| `isTwoHanded` | Two-Handed Detection | CONDITIONAL | `Ee()` items-DqMVEwxd.js |
| `twoHandedMultiplier` | Two-Handed Stat Multiplier | COMPUTED | `Ar=2` |
| `isBow` | Bow = One-Handed | CONDITIONAL | `Jn="bow"` |
| `cardSlotCount` | Card Slot Count | COMPUTED | `Dt()` |
| `basicAttackType` | Basic Attack Power Type | CONDITIONAL | `Z0()` main-CFj0fJNd.js |
| `orbEquipClasses` | Orb Equippable Classes | LOOKUP | `Orb.jobs` |
| `matkDamagePierce` | MATK Uses Magic Pierce | CONDITIONAL | `p?o.mpierce:o.pierce` |
| `nekobakuSkillMultiplier` | Nekobaku Damage Skill Scaling | COMPUTED | `R(skill,level)` |
| `cooldownFromAspd` | ASPD-Scaled Cooldown | COMPUTED | cooldownFromAspd branch |

## Gap Register
| ID | Subsystem | Status | Notes |
|---|---|---|---|
| GAP-001 | PROGRESSION | PARTIALLY_RESOLVED | z5 reconstructed |
| GAP-002 | PARTY | OPEN | Party EXP split |
| GAP-003 | DROP | OPEN | Server vs display rates |
| GAP-004 | REFINE | OPEN | Client formula verified |
| GAP-005 | DAMAGE | RESOLVED | No random multiplier |
| GAP-006 | MONSTER | OPEN | Mob stats server-side |
| GAP-007 | PvP | OPEN | No PvP data |
| GAP-008 | SKILL | OPEN | Cast time |
| GAP-009 | ASPD | OPEN | Skill cooldown |
| GAP-010 | STORAGE | OPEN | Bank capacity |
| GAP-011 | PROGRESSION | OPEN | EXP threshold |
| GAP-012 | EQUIPMENT | **RESOLVED** | Two-handed ×2 |
| GAP-013 | EQUIPMENT | **RESOLVED** | Bow 1H + card |
| GAP-014 | SKILL | **RESOLVED** | Nekobaku MATK basic |
| GAP-015 | COMBAT | OPEN | Server-side |
| GAP-016 | BOSS | OPEN | Server-side |
| **Total** | | **16** | **3 RESOLVED, 1 PARTIALLY, 12 OPEN** |

## Validation Checks (8/8 PASS)
| Check | Status |
|---|---|
| JSON validity | PASS |
| Formula schema & confidence | PASS |
| SQLite integrity | PASS |
| Changelog freshness | PASS |
| Changelog delta | PASS |
| Raw preservation | PASS |
| V0.8 artifact consistency | PASS |
| Gap ID uniqueness | PASS |

## Sample Counts
| Analysis | Samples |
|---|---|
| Controlled damage groups | 57 (≥10 hits each) |
| Outgoing damage events | 2,940+ |
| Incoming damage events | 342 |

## Worktree Status
**CLEAN** — no untracked or modified files.
