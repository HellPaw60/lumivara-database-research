# PROJECT.md — Lumivara Database Research

## Project Goals

1. Membangun representasi database Lumivara Online sedetail mungkin dari seluruh sumber yang tersedia
2. Mendokumentasikan protokol client-server yang teramati
3. Me-rekonstruksi formula dan mekanik game (combat, drop, equipment)
4. Menyimpan raw evidence agar penelitian dapat direproduksi
5. Melacak evolusi game via version diff

## Research Methodology

**DATA DULU, PROSE BELAKANGAN.**

1. **Static extraction** — bundle JS di-parse (node eval untuk object literal, regex + bracket-match untuk konstruksi dinamis). Tidak ada nama field yang dikarang: field semantic hanya diberi nama jika ada bukti penggunaan di kode.
2. **Passive network observation** — guest account resmi via endpoint publik, WebSocket logging tanpa modifikasi traffic. Semua input mengikuti pola klien asli (move 90px/120ms, spawnReady handshake).
3. **Event mining** — event broadcast area (defeat/pickup) dimanfaatkan untuk EXP & drop table player lain (pasif, tanpa interaksi).
4. **Cross-referencing** — setiap claim dicek minimal dari satu sumber; dua sumber = VERIFIED kuat.
5. **Version diff** — dua snapshot bundle dibandingkan per-entity untuk deteksi perubahan.

## Data Sources

| Sumber | Versi | Hash (sha256, 16 char) |
|---|---|---|
| Desktop exe (NSIS) | 0.1.0 | 003862eec2c8c3dc (verified vs GitHub release) |
| Web bundle v1 | main-BHjIB9U4.js | lihat inventory_manifest.json |
| Web bundle v2 | main-DEXZ0AP0.js | lihat inventory_manifest.json |
| WS snapshots | ~50K, 14 area | collect/raw-snapshots.json |
| Localization | language-Dz8VbPNM.js | 2.547 pasang |
| Changelog | 650 entri | changelog-notice-BKeFrGHU.js |

## Extraction Methodology

- `extraction/scripts/inventory.py` — manifest + hashing
- `extraction/scripts/normalize_changelog.py` — changelog → normalized JSON
- `extraction/scripts/build_sqlite.py` — master SQLite dari semua sumber
- `extraction/scripts/validate.py` — integritas + referential check
- `extraction/scripts/diff_provenance.py` — version diff + lineage
- `collect/collector-final.mjs` — WS collector (spawnReady + BFS portal + walk realistis)
- `collect/aggregate.py` — agregasi monster/EXP/drop dari snapshot

## Validation Methodology

1. JSON parse test semua database file
2. SQLite `PRAGMA integrity_check`
3. Duplicate ID detection
4. Referential check (skill→class, portal→map, status→monster)
5. Impossible value check (HP<=0, level<1)
6. Hash manifest verification

Hasil: `validation/VALIDATION_REPORT.md`

## Known Limitations

1. **Drop table** — asosiasi mob→item via posisi event defeat/pickup (radius 100px, window 40 event). Akurat untuk farming spot statis, bisa salah untuk area padat.
2. **Combat formula** — server-side; hanya statistik observasi (OBSERVED), bukan formula (VERIFIED).
3. **Interior areas** (inn/cove/grove/ruins/temple/arena) — pintu masuk via objek dunia prosedural, koordinat belum terekstrak.
4. **maxHp** — nilai maksimum teramati; variance elite vs normal bisa tercampur antar run.
5. **Changelog kategori** — heuristic keyword (DERIVED), bukan kategori resmi developer.

## Open Research Questions

1. Koordinat pintu 6 interior area (perlu deminifikasi scene builder)
2. Formula damage server (perlu eksperimen terkontrol — di luar lingkup pasif)
3. Rate drop aktual server vs konstanta display klien
4. Struktur quest/mall/pet server-side (endpoint butuh login Google)
5. Mekanik World Boss spawn (Crowned Prism Hopper belum teramati live)

## Milestones

- [x] **v0.1 Research Archive** — raw evidence + database v1/v2 + laporan
- [x] **v0.2 Client Reconstruction** — seluruh tabel client terekstrak
- [x] **v0.3 Network Reconstruction** — protokol event terdokumentasi
- [~] **v0.4 Database Reconstruction** — SQLite master (interior area masih bolong)
- [ ] **v0.5 Formula Reconstruction** — butuh eksperimen terkontrol

Tag: `v0.1-research-archive`
