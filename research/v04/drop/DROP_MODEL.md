# DROP MODEL (v0.4 Phase 9)

## Tiga Lapisan Data Drop (PISAHKAN!)

### 1. Client Display Probability (CLIENT_CONSTANT)

Dari `items-CvFgs761.js var ie`:

| Kategori | Rate | Catatan |
|---|---|---|
| etc | 30% | material |
| consumable | 15% | potion dll |
| equipment | **1.25%** | dinnerf dari 2.5% (per TRANSLATIONS) |
| card | 0.1% | |
| bossCard | 1% | dari boss |
| relicBox | 1% | |
| refineStone | 1% | Lv70+ only |
| extraStat | 25% | |
| aspdAccessory | 30% | |

**Label: CLIENT_CONSTANT — bukan server rate.** Server rate UNKNOWN.

### 2. Observed Drop Events (OBSERVED_RUNTIME)

- 312 drop entri di snapshot.drops (14 area)
- 198+ pickup events
- 48 item unik teramati

### 3. Reconstructed Monster Association (DERIVED)

Asosiasi via posisi event defeat→pickup (radius 100px, window 40 event). 44/48 item terasosiasi.
MONSTER_DB drops = DERIVED, bukan tabel server.

## Orphan Resolution (v0.4 re-analysis)

| Item | Pickup | Snapshot Drops | Posisi | Asosiasi Baru (INFERRED dari posisi) |
|---|---|---|---|---|
| aurora_tail | 0 | 25 | snow (952,584) dll | **Aurora Fox** (snow area, Lv45) — posisi konsisten |
| garment | 1 | 0 | desert (1431,1263) | mob desert terdekat: Scarab/Cobra/Gecko — **slot garment drop generik** (bukan material) |
| honey_wing_dust | 0 | 3 | field (1106,2463) dll | **Honey Moth** (field, Lv15) — nama match + posisi |
| magma_scale | 1 | 0 | caldera (514,853) | **Magma Salamander** (caldera) — sudah ada di MONSTER_DB drops via asosiasi lama |

**Status: INFERRED** (asosiasi posisional + penamaan) — bukan VERIFIED kecuali magma_scale yang sudah terasosiasi.

## Drop Pipeline (dari client evidence)

```
MONSTER DEFEATED
↓ [category roll — CLIENT_CONSTANT rates, server UNKNOWN]
CATEGORY (etc/consumable/equipment/card/...)
↓ [item roll — dalam kategori]
ITEM
↓ [slot roll — equipment only: favored slot 6x (TRANSLATIONS)]
SLOT
↓ [tier/rarity + random option — server-side, UNKNOWN]
FINAL DROP
```

## Party Modifier

+2% per member (max 12, ±10 level) — dari string UI + TRANSLATIONS (CLIENT_CONSTANT, 2 sumber string).

## Open Questions

1. Apakah client rate == server rate? (UNKNOWN — butuh observasi statistik jangka panjang)
2. Favored slot mechanics detail (slot apa yang favored per mob?)
3. Tier assignment formula
4. World boss drop table (Tier V 100% dari TRANSLATIONS — VERIFIED as claim, values UNKNOWN)
