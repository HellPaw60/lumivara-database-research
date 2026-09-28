# V0.3.1 Documentation Consistency Audit

**21/39 checks MATCH** | 2 mismatch | 16 not found

## Actual Dataset Values

| Key | Value |
|---|---|
| classes | 10 |
| skills | 64 |
| items_consumables | 80 |
| cards | 49 |
| statuses | 42 |
| maps | 19 |
| monsters | 40 |
| monster_status_attacks | 7 |
| translations | 2547 |
| changelog_entries | 650 |
| changelog_unique_ids | 649 |
| ws_events | 26 |
| formulas | 18 |
| sqlite_tables | 11 |
| sqlite_rows | 2881 |

## Checks

| Doc | Claim | Doc Value | Actual | Status |
|---|---|---|---|---|
| README.md | classes=10 | ['Classes | 10'] | 10 | MATCH |
| README.md | skills=64 | ['64 skill'] | 64 | MATCH |
| README.md | items=80 | [] | 80 | NOT_FOUND |
| README.md | cards=49 | [] | 49 | NOT_FOUND |
| README.md | monsters=40 | ['40 monster'] | 40 | MATCH |
| README.md | maps=19 | [] | 19 | NOT_FOUND |
| README.md | statuses=42 | [] | 42 | NOT_FOUND |
| README.md | translations=2547 | ['2,547'] | 2547 | MATCH |
| README.md | changelog=650 | ['650 entri', '650 changelog '] | 650 | MATCH |
| README.md | ws_events=26 | [] | 26 | NOT_FOUND |
| README.md | formulas=18 | ['18 formula'] | 18 | MATCH |
| README.md | sqlite_tables=12 | [] | 11 | NOT_FOUND |
| README.md | sqlite_rows=2891 | [] | 2881 | NOT_FOUND |
| RECONSTRUCTION_REPORT.md | classes=10 | ['Classes | 10'] | 10 | MATCH |
| RECONSTRUCTION_REPORT.md | skills=64 | ['64 skill'] | 64 | MATCH |
| RECONSTRUCTION_REPORT.md | items=80 | ['80 item', '80 consumable'] | 80 | MATCH |
| RECONSTRUCTION_REPORT.md | cards=49 | ['49 kartu'] | 49 | MATCH |
| RECONSTRUCTION_REPORT.md | monsters=40 | ['40 monster'] | 40 | MATCH |
| RECONSTRUCTION_REPORT.md | maps=19 | ['19 map'] | 19 | MATCH |
| RECONSTRUCTION_REPORT.md | statuses=42 | [] | 42 | NOT_FOUND |
| RECONSTRUCTION_REPORT.md | translations=2547 | [] | 2547 | NOT_FOUND |
| RECONSTRUCTION_REPORT.md | changelog=650 | ['650 changelog '] | 650 | MATCH |
| RECONSTRUCTION_REPORT.md | ws_events=26 | ['26 event'] | 26 | MATCH |
| RECONSTRUCTION_REPORT.md | formulas=18 | [] | 18 | NOT_FOUND |
| RECONSTRUCTION_REPORT.md | sqlite_tables=12 | [] | 11 | NOT_FOUND |
| RECONSTRUCTION_REPORT.md | sqlite_rows=2891 | [] | 2881 | NOT_FOUND |
| repo_audit/V03_AUDIT.md | classes=10 | [] | 10 | NOT_FOUND |
| repo_audit/V03_AUDIT.md | skills=64 | ['64 skill'] | 64 | MATCH |
| repo_audit/V03_AUDIT.md | items=80 | ['80 item'] | 80 | MATCH |
| repo_audit/V03_AUDIT.md | cards=49 | ['49 card'] | 49 | MATCH |
| repo_audit/V03_AUDIT.md | monsters=40 | ['40 monster'] | 40 | MATCH |
| repo_audit/V03_AUDIT.md | maps=19 | ['19 map'] | 19 | MATCH |
| repo_audit/V03_AUDIT.md | statuses=42 | ['42 status'] | 42 | MATCH |
| repo_audit/V03_AUDIT.md | translations=2547 | [] | 2547 | NOT_FOUND |
| repo_audit/V03_AUDIT.md | changelog=650 | [] | 650 | NOT_FOUND |
| repo_audit/V03_AUDIT.md | ws_events=26 | [] | 26 | NOT_FOUND |
| repo_audit/V03_AUDIT.md | formulas=18 | ['18 formula'] | 18 | MATCH |
| repo_audit/V03_AUDIT.md | sqlite_tables=12 | ['12 tabel', '12 tabel'] | 11 | MISMATCH |
| repo_audit/V03_AUDIT.md | sqlite_rows=2891 | ['2.891', '2.891'] | 2881 | MISMATCH |