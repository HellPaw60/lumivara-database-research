# V0.4 Full Validation

**10/10 PASS** | 0 FAIL

| Check | Status | Detail |
|---|---|---|
| sqlite_integrity | PASS | kedua database ok |
| foreign_key_check | PASS | 0 issues |
| json_parse | PASS | semua OK |
| sql_recreation | PASS | integrity=ok, tables match=True |
| csv_sqlite_parity | PASS | semua tabel parity |
| doc_consistency | PASS | MATCH: 21/39 |
| formula_classification | PASS | 18 formulas semua terklasifikasi |
| provenance_completeness | PASS | 12 entities lengkap |
| duplicate_detection | PASS | dups: {'2026-09-23-skill-rebalance': 2} (expected 1, documented) |
| orphan_detection | PASS | 1 known orphan (World Boss name variant) — documented |