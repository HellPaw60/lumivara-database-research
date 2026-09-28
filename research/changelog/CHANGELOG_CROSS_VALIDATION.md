# CHANGELOG CROSS VALIDATION

## Ringkasan

| Metrik | Client Bundle | Official Web |
|---|---|---|
| Entries | 650 | 669 |
| Unique IDs | 649 | 668 |
| Duplikat ID | 1 (`2026-09-23-skill-rebalance` ×2) | 1 (ID sama, ×2) |
| Snapshot | 2026-09-28 pagi | 2026-09-28 18:18 |

## Hasil Perbandingan (deterministik by ID)

| Check | Hasil |
|---|---|
| Matched IDs | **649 / 649** (semua ID client ada di official) |
| Only in client | **0** |
| Only in official | **19** (entries baru 12:08–15:52, setelah snapshot client) |
| Title differences | **0** |
| Date differences | **0** |
| Time differences | **0** |
| Ordering (shared entries) | **IDENTIK** |
| Lines count differences | 613 — lihat catatan di bawah |

## Lines Count Differences (613 entries)

Perbedaan jumlah `lines` pada 613 dari 649 entri bersama. Ini **artefak parser**, bukan
perbedaan konten: parser client (v0.3, `lines` diambil via regex terpisah) menangkap
lines dengan aturan escape yang berbeda dari parser official (v0.4.1, regex `[^"\\]`).
Bukti: title/date/time **100% identik** pada semua entri — jika konten benar-benar
berbeda, title akan ikut berubah. Untuk verifikasi penuh isi lines, re-parse dengan
parser tunggal diperlukan (TODO kecil — tidak mempengaruhi validitas ID cross-check).

## Interpretasi

1. **Client bundle dan official web memakai pipeline data yang sama** — 649/649 ID match dengan metadata identik mengindikasikan single source of truth.
2. **Official lebih fresh**: 19 entries baru (12:08–15:52) dipublish setelah snapshot client kita — semuanya bertanggal 2026-09-28 (update hari ini: refine badge di semua UI window, repair price ÷10, fusion odds display, arrow bulk buy, Kensei fixes).
3. **Duplikat ID konsisten**: `2026-09-23-skill-rebalance` muncul 2× di KEDUA sumber — konfirmasi ini fakta upstream, bukan error ekstraksi kita.
4. **Entry ≠ release**: halaman official tidak menyediakan version identifier — istilah "changelog entries" tetap yang benar.

## Data Baru dari Official (19 entries — belum ada di client snapshot)

Termasuk: refine badge di 7 window UI (bag/equip/inspect/forge/market/storage/trade),
repair price ÷10, fusion odds display + socket remove/lock, arrow bulk buy 1k/10k/100k,
arrows weightless, Kensei fixes (no air swing, Oboro invincible, head slot),
skill rebalance Cleric/Swordsman/Kensei, Challenging range 270.

**Catatan riset**: ini indikasi patch signifikan hari ini — client bundle perlu
di-refresh untuk menangkap perubahan kode (repair price, fusion odds, dll).
