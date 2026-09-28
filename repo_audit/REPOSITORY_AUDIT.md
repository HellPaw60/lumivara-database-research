# Repository Audit — v0.2

**Tanggal:** 2026-09-28 | **Auditor:** automated integrity audit | **Target:** HellPaw60/lumivara-database-research

## 1. Repository State

- Local: `main` @ `33fb637` = `origin/main` (sinkron, clean worktree)
- Remote: https://github.com/HellPaw60/lumivara-database-research.git
- Tag: `v0.1-research-archive`
- 133 file tracked, 2.616 ignored (node_modules, Electron extract, logs)

## 2. Local vs Remote Diff

**Hasil: 0 LOCAL_ONLY, 0 REMOTE_ONLY, 133 BOTH.**

- 56 file identical-size, 77 file size-delta — **semuanya CRLF artifact** (git autocrlf; delta bytes == jumlah baris file; `git diff origin/main` kosong = konten identik). Bukan perubahan konten.

## 3. Broken References (FIXED)

| Referensi di | Path didokumentasikan | Status sebelum | Aksi |
|---|---|---|---|
| README.md | `provenance/PROVENANCE.json` | BROKEN (file di `forensics/provenance/`) | copy ke path terdokumentasi |
| PROJECT.md | `validation/VALIDATION_REPORT.md` | BROKEN (file di `forensics/validation/`) | copy ke path terdokumentasi |
| RECONSTRUCTION_REPORT.md | `diffs/DIFF_v1_v2.json` | BROKEN (file di `forensics/diffs/`) | copy ke path terdokumentasi |

Salinan di `forensics/` dipertahankan (tidak menghapus evidence).

## 4. Documentation Claims Audit

**10/10 klaim angka MATCH dengan dataset aktual:**

| Claim | README | Actual | Status |
|---|---|---|---|
| Classes | 10 | 10 | ✓ |
| Skills | 64 | 64 | ✓ |
| Items (consumable) | 80 | 80 | ✓ |
| Cards | 49 | 49 | ✓ |
| Status effects | 42 | 42 | ✓ |
| Maps | 19 | 19 | ✓ |
| Monsters | 40 | 40 | ✓ |
| Translations | 2,547 | 2,547 | ✓ |
| Changelog entries | 650 | 650 | ✓ |
| WS event types | 26 | 26 | ✓ |

## 5. Database Audit

- 22 JSON database: semua parse OK, record count konsisten
- SQLite: 11 tabel, 2.881 rows, `PRAGMA integrity_check` = ok (dua salinan identik)
- Istilah changelog: "650 entries" — BENAR (bukan "650 patches/releases")

## 6. Cross-Database Consistency

| Check | Hasil |
|---|---|
| skill.classId → classes | OK (semua valid) |
| map.portals.to → maps | OK (semua valid) |
| monster.drops → items | 2 item material tanpa entri ITEMS — expected (ITEMS hanya consumable; material drop = kategori terpisah) |
| mob_status_attacks → monsters | 1 orphan: "Crowned Prism Hopper" — name variant dari World Boss "Prism Hopper" (key `prism-hopper` ada di MONSTER_DB). Bukan data hilang. |
| CLASS_DB.skills_by_class vs GAME_DB.skills | 64 = 64 OK |

## 7. Changelog Audit

- 650 entries, **649 unique ID** — 1 duplikat ID di SUMBER: `2026-09-23-skill-rebalance` muncul 2× dengan judul berbeda (12:58). Ini fakta bundle asli, bukan error ekstraksi.
- 7 unique dates. Istilah dokumentasi sudah benar ("entries").

## 8. Confidence Audit (koreksi dilakukan)

| Claim | Sebelum | Sesudah | Alasan |
|---|---|---|---|
| Refine formula | "VERIFIED dari kode" | "VERIFIED dari kode KLIEN — server belum tentu identik" | kode = klien |
| Drop rates | "VERIFIED (client display)" | tetap + caveat di report | sudah jujur |
| Crit ratio 3.551x | OBSERVED | OBSERVED | sudah benar |
| Party bonus +2% | VERIFIED | VERIFIED (string UI + TRANSLATIONS, 2 sumber string) | dipertahankan dengan catatan sumber |

Header disclaimer ditambahkan di RECONSTRUCTION_REPORT.md.

## 9. Formula Confidence Matrix

| Formula | Confidence |
|---|---|
| Refine success | CODE_VERIFIED (klien) / server UNKNOWN |
| Crit ratio | OBSERVED (3.551x mean, distribusi lebar) |
| Miss rate | OBSERVED (0% pada sample farming) |
| Damage | UNKNOWN |
| Hit/Flee | UNKNOWN |
| ASPD | PARTIAL (potions table VERIFIED, interval formula UNKNOWN) |
| Drop rates | VERIFIED (display konstanta) / server UNKNOWN |
| EXP per monster | OBSERVED (event defeat) |
| EXP table level-up | UNKNOWN (z5 tidak terekstrak) |

## 10. Network Audit

- 26 event server→client: semua teramati langsung (VERIFIED)
- 140+ type string klien→server: VERIFIED sebagai string di bundle; penggunaan aktual = INFERRED untuk yang tak terkirim saat capture

## 11. Extraction Reproducibility

| Script | Status | Output match |
|---|---|---|
| normalize_changelog.py | OK | ✓ (650 entries) |
| build_sqlite.py | OK | ✓ (integrity ok) |
| validate.py | OK | ✓ |

## 12. Version Audit

- v1 → v2 → v3 terdokumentasi di LAPORAN.md / LAPORAN-V2.md / commit history
- **Catatan:** GAME_DB.json & MONSTER_DB.json di root = versi v2 (overwrite v1). Data v1 hanya terdokumentasi di LAPORAN.md, tidak disimpan sebagai file terpisah. Raw bundle v1 (`web/`) tetap ada — v1 dapat direkonstruksi ulang dari bundle.

## 13. Remaining Unknowns

1. Koordinat pintu 6 interior area
2. Formula damage/hit/flee server
3. Rate drop aktual server (vs display klien)
4. Quest/mall/pet server state (auth wall)
5. World Boss spawn schedule (nilai `zi`/`Ao` belum diekstrak numerik)
6. Gold/Premium pack pricing (zf tidak ditemukan)
7. z5 function (points per level)
8. Refine formula versi server

## 14. Recommended Corrections (SEMUA DILAKUKAN)

- [x] Copy PROVENANCE/VALIDATION/DIFF ke path terdokumentasi
- [x] Refine formula confidence diperhalus (klien vs server)
- [x] Header disclaimer confidence di RECONSTRUCTION_REPORT
- [x] Duplikat changelog ID terdokumentasi (fakta sumber)
- [x] CRLF artifact terdokumentasi (bukan konten diff)
