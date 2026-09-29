# V0.8 PHASE G — BOT BEHAVIOR DEEP AUDIT

## Source
| Field | Value |
|---|---|
| Bundle (V0.8) | `main-CFj0fJNd.js` / `items-DqMVEwxd.js` |
| Baseline | `CkIS7ST6` / 688 |
| Observation | `CMg3B3wG` / 730 |

---

## 1. BOT BEHAVIOR ENTRIES IN CMg3B3wG

| Entry | Claim | Impact |
|---|---|---|
| `bot-long-cooldown-first` | Bot prioritizes long-cooldown skills when ready | AI logic |
| `bot-instant-next-target` | Bot instantly switches to next target after kill | AI logic |
| `bot-approach-skill-resend` | Bot approaches then immediately casts (reduced idle walking) | AI logic |
| `bot-auto-coat-fix` | Bot auto-element-coating fixed (reliability) | Bug fix |

---

## 2. CLIENT EVIDENCE

### Search Results
```
SEARCHED: bot, autoPlay, auto-play, bot AI
FOUND:
  - "bot-window" UI label (display only)
  - No AI logic changes found in client bundles
  - No skill priority logic found in client bundles
  - No target switching logic found in client bundles
```

### Analysis

All bot behavior changes in CMg3B3wG are **not in client bundles**. This is expected because:

1. **Bot behavior is server-authoritative** — The server controls bot AI decisions
2. **Client only renders bot state** — UI shows bot status but doesn't control logic
3. **Skill priority, target switching, approach-cast** — All server-side AI decisions

---

## 3. SERVER/CLIENT DISTINCTION

| Mechanic | Changelog | Client Evidence | Runtime | Server Status |
|---|---|---|---|---|
| Long-cooldown-first | ✓ | NONE | — | SERVER_SIDE_ONLY |
| Instant next target | ✓ | NONE | — | SERVER_SIDE_ONLY |
| Approach then cast | ✓ | NONE | — | SERVER_SIDE_ONLY |
| Auto-coat fix | ✓ | NONE | — | SERVER_SIDE_ONLY |

---

## 4. CLASSIFICATION

### Mechanics vs Non-Mechanics

| Entry | Initial Class | Final Class | Reason |
|---|---|---|---|
| `bot-long-cooldown-first` | BOT ✓ | BOT (non-mechanic) | AI behavior, not game rule |
| `bot-instant-next-target` | BOT ✓ | BOT (non-mechanic) | AI behavior, not game rule |
| `bot-approach-skill-resend` | BOT ✓ | BOT (non-mechanic) | AI behavior, not game rule |
| `bot-auto-coat-fix` | BOT ✓ | BUG/Fix | Reliability fix |

### Reasoning

Bot behavior changes **do not affect global game mechanics** because:
1. Bots follow the same game rules as players
2. AI priority logic doesn't change combat formulas
3. Target switching doesn't change damage calculations
4. Approach-cast behavior is efficiency optimization, not rule change

**All 4 bot entries are NON-MECHANICS** (AI behavior / bug fix).

---

## 5. FORMULA DATABASE — NO NEW FORMULAS

Tidak ada formula bot yang relevan dengan game mechanics.

**Formula count remains 47.**

---

## 6. GAP REGISTER — NO CHANGE

Tidak ada gap baru.

---

## 7. CONCLUSION

Phase G complete. Key findings:
1. **All bot behavior changes are server-side AI logic**
2. **None affect global game mechanics**
3. **All 4 entries reclassified as NON-MECHANICS** (AI behavior / bug fix)
4. **No new formulas or gaps**

---

## V0.8 PHASE A–G SUMMARY

| Phase | Topic | Findings | New Formulas |
|---|---|---|---|
| A | Changelog Delta | 42 entries, 16 mechanics-relevant | 6 |
| B | Equipment | Two-handed ×2, bow 1H, card slots, class gear | 0 |
| C | Skill/Class | Nekobaku MATK basic, Orb, skill scaling | 3 |
| D | Combat/Monster | All server-side | 0 |
| E | Drop | All server-side | 0 |
| F | Economy | All server-side | 0 |
| G | Bot | All server-side AI | 0 |

**Total formulas: 47**
**Total gaps: 16 (3 resolved, 13 open)**

---

**All phases complete.** Siap untuk Phase H (Gap Register) dan Phase I (Formula Database finalisasi).
