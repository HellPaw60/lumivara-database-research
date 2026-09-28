# z5 / F0 / It RECONSTRUCTION (V0.7 Phase 2 — RESOLVED)

## Source
`web-v2/items-CvFgs761.js` — export chain: `F0 → dY → z5`

## Recovered Functions

### F0 (= z5)
```
F0 = A => Math.floor(A/5) + 3
```
- **What it returns**: Job/stat **points awarded at a specific level**
- **Scope**: Per-level job points (not cumulative)
- **Evidence**: `const i = this.level - r + 1, s = z5(i); this.points += s` — at level-up, player gains `floor(newLevel/5) + 3` points

### $0
```
$0 = A => Math.floor((A-1)/10) + 2
```
- **What it returns**: **Stat points per level** (base stat allocation)
- Evidence: Used in `B0(A)` function computing `r = lA.reduce(...$0(l)...)` — stat points spent per stat level

### It
```
It = A => { let e=0; for(let t=2; t<=A; t++) e += F0(t); return e }
```
- **What it returns**: **Cumulative job points from level 2 to level A**
- **Purpose**: Total points available at level A (used to calculate `It(A.level) - (n.points + r)` = unspent points)

## Implications

1. **Level-up grants BOTH stat points AND job points**:
   - Stat points per level = `floor((Lv-1)/10) + 2`
   - Job points per level = `floor(Lv/5) + 3`

2. **EXP threshold (server-side)**:
   - The EXP table that determines how much EXP is needed per level remains **server-side** (not in client bundle)
   - Client only receives the level-up event and computes points
   - Evidence: `M5(this, p)` returns boolean (level-up triggered?), `JC(this, o)` returns how many levels to advance
   - Actual EXP required per level = **UNKNOWN** (server authoritative)

3. **Level cap check**: `this.level >= Ws ? 0 : o` where `Ws` is status damage function, not level cap — level cap not found in client

## Sample Predictions (VERIFIED_FROM_CLIENT_CODE)
| Level | Job Points (${F0(Lv)}) | Cumulative (${It(Lv)}) | Stat Points (${\$0(Lv)}) |
|---|---|---|---|
| 1 | floor(1/5)+3 = 3 | 0 | floor(0/10)+2 = 2 |
| 5 | floor(5/5)+3 = 4 | 3+3+3+4 = 13 | floor(4/10)+2 = 2 |
| 10 | floor(10/5)+3 = 5 | ... | floor(9/10)+2 = 2 |
| 50 | floor(50/5)+3 = 13 | Σ F0(2..50) | floor(49/10)+2 = 6 |
| 100 | floor(100/5)+3 = 23 | Σ F0(2..100) | floor(99/10)+2 = 11 |

## Confidence
- z5 function body: **VERIFIED_FROM_CLIENT_CODE** (exact match `F0=A=>Math.floor(A/5)+3`)
- z5 purpose: **VERIFIED_FROM_CLIENT_CODE** (job points per level — direct code evidence)
- EXP threshold table: **UNKNOWN** (server-side, not in client bundle)
- Level cap: **UNKNOWN**
