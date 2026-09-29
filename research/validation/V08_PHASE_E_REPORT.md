# V0.8 PHASE E — DROP MECHANICS DEEP AUDIT

## Source
| Field | Value |
|---|---|
| Bundle (V0.8) | `main-CFj0fJNd.js` / `items-DqMVEwxd.js` |
| Baseline | `CkIS7ST6` / 688 |
| Observation | `CMg3B3wG` / 730 |

---

## 1. DIVINE WINGS DROP RATE — FINDING

### Changelog Claim
| Field | Value |
|---|---|
| Source | `2026-09-29-divine-wings-1-in-100k` |
| Claim | Divine Wings dari Mystery Relic Box, 1/100.000 (dari ~1/1.000.000) |

### Client Evidence
```
SEARCHED: Tg constants, drop tables, box reward functions, divine_wings references
FOUND:
  - relicBox: 0.1 (display rate, bukan actual drop rate)
  - divine_wings: slot "wings" (untuk equip, bukan drop)
  - Se(A): cek apakah item adalah wings
  - TIDAK ADA koneksi antara relic box dan divine wings di client
```

**Kesimpulan**: SERVER_SIDE_ONLY — Client tidak memiliki logika reward box.

---

## 2. EXISTING DROP MODEL — AUDIT

### Kategori yang Diidentifikasi

| Kategori | Status |
|---|---|
| CLIENT DISPLAY | `relicBox: 0.1` di items bundle |
| CLIENT LOOT TABLE | Tidak ada (server-side) |
| SERVER DROP RESULT | Server-side (client hanya menerima hasil) |
| WIKI/HISTORICAL | Repo lama punya `extraStat: .25`, `relicBox: .01` sebagai display constants |

### Display vs Actual
```
Client display constants (items-DqMVEwxd.js):
  extraStat: 0.25
  equipment: 0.0125
  card: 0.001
  bossCard:  0.01
  relicBox:  0.1    ← display rate, bukan actual drop rate
  refineStone: 0.01
  aspdAccessory: 0.3

Server actual rates: UNKNOWN (server authoritative)
```

---

## 3. DROP RATE VS DISPLAY RATE — FINDING

### GAP-003 Status
| Item | Status |
|---|---|
| Client constants | Display rates only |
| Server actual rates | UNKNOWN |
| Divine Wings 1/100K | Changelog claim, server-side |

**GAP-003 tetap OPEN** — Tidak ada evidence baru yang menyelesaikan gap.

---

## 4. MYSTERY RELIC BOX — IMPLEMENTATION

### Client Evidence
```
SEARCHED: box reward function, random roll, reward pool
FOUND: NONE
```

Client hanya memiliki:
- `relic_box` item definition (name, description, price)
- `relicBox: 0.1` display constant
- UI untuk buka box (`bulk: relic_box`)

Semua logic reward (random roll, pool, weight) ada di server.

---

## 5. DROP PIPELINE GLOBAL — FINDING

### Drop-related changes in CMg3B3wG
| Item | Status |
|---|---|
| Monster normal drop | Tidak ada perubahan di client |
| Equipment drop | Tidak ada perubahan di client |
| Card drop | Tidak ada perubahan di client |
| Material drop | Tidak ada perubahan di client |
| Boss drop | Tidak ada perubahan di client |
| Box/reward drop | Tidak ada perubahan di client |
| Class-specific drop | Tidak ada perubahan di client |
| World boss reward | Tidak ada perubahan di client |

**Semua drop mechanics tidak berubah di client.**

---

## 6. RUNTIME VALIDATION

Tidak dilakukan (memerlukan server-side testing yang tidak mungkin dari client).

---

## 7. HISTORICAL COMPARISON

| Version | Divine Wings Rate | Evidence |
|---|---|---|
| V0.7 (historical) | ~1/1.000.000 | Changelog lama |
| V0.8 observation | ~1/100.000 | Changelog baru |
| Client implementation | NONE | Server-side only |

---

## 8. FORMULA DATABASE — NO NEW FORMULAS

Tidak ada formula baru ditambahkan di Phase E.

**Formula count remains 47.**

---

## 9. GAP REGISTER

### GAP-003 — Server Drop Rates vs Client Display Constants
**Status**: OPEN (tidak berubah)

| Evidence | Finding |
|---|---|
| Client constants | Display rates only |
| Server actual rates | Unknown |
| Divine Wings 1/100K | Changelog claim, server-side |

---

## 10. SERVER-EQUIVALENCE STATUS

| Mechanic | Client | Runtime | Server Equivalence |
|---|---|---|---|
| Divine Wings drop rate | NONE | — | SERVER_SIDE_ONLY |
| Mystery Relic Box reward | NONE | — | SERVER_SIDE_ONLY |
| Monster drop rates | NONE | — | SERVER_SIDE_ONLY |
| Equipment drop rates | NONE | — | SERVER_SIDE_ONLY |
| Card drop rates | NONE | — | SERVER_SIDE_ONLY |
| Boss drop rates | NONE | — | SERVER_SIDE_ONLY |
| Display constants | ✓ (relicBox: 0.1) | — | DISPLAY_ONLY |

---

## 11. CONCLUSION

Phase E complete. Key findings:
1. **Divine Wings drop rate is SERVER_SIDE_ONLY**
2. **Mystery Relic Box reward logic is SERVER_SIDE_ONLY**
3. **No new formulas added** (count remains 47)
4. **GAP-003 remains OPEN** (server drop rates unknown)
5. **Client only has display constants**, not actual drop rates

**Phase E complete.** Siap untuk Phase F (Economy) kapan pun LO mau lanjut.
