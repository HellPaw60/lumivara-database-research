# OFFICIAL CHANGELOG SOURCE

## Sumber Resmi

**URL:** https://lumivaraonline.com/changelog/
**Retrieved:** 2026-09-28T18:18 (WIB)

## Struktur Teknis

Halaman `/changelog/` adalah SPA shell (4.503 bytes HTML):
- Konten dimuat oleh `/assets/changelog-DuuixMbX.js` (4.641 bytes, UI renderer)
- Data entri dari `/assets/changelog-notice-Dk8pLLLq.js` (895.812 bytes)
- **Bundle data official BERBEDA dari bundle game client** (`changelog-notice-BKeFrGHU.js`, 878.174 bytes) — snapshot official lebih baru

## Provenance

| Field | Value |
|---|---|
| source_type | OFFICIAL_WEB |
| url | https://lumivaraonline.com/changelog/ |
| data_bundle | https://lumivaraonline.com/assets/changelog-notice-Dk8pLLLq.js |
| retrieved_at | 2026-09-28T18:18 |
| html_sha256 | b90f6f9f7d5190802f6608228855fcf65ba6b0e817cbf02ceee9ee84ff687763 |
| bundle_sha256 | 77346c43266383a6... (full di CHANGELOG_CROSS_VALIDATION.json) |
| method | HTTP retrieval + module import trace + regex parse |
| confidence | VERIFIED_SOURCE |

## File Arsip

- `official_changelog_raw.html` — SPA shell asli
- `official_changelog_bundle.js` — renderer JS
- `official_changelog_notice_bundle.js` — bundle data entri (895 KB)
- `OFFICIAL_CHANGELOG.json` — 669 entries terparse

## Terminologi

Halaman official menyebut dirinya "บันทึกการอัปเดต / Patch Notes" dan setiap entri
diberi label "อัปเดต" (update). UI counter menampilkan "N updates". Setiap entri
punya `id` unik (slug) + date + time. **Namun tidak ada konsep "release version"**
yang eksplisit — jadi istilah yang benar tetap **"changelog entries"**, bukan releases.
