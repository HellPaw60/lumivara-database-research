# V0.4.1 Failure Injection Tests

**7/7 negative tests detected correctly**

Validator terbukti fail-closed: setiap korupsi data menghasilkan FAIL.

| Test | Injected | Detected | Detail |
|---|---|---|---|
| A: single value modification | ✅ | ✅ | value change detected: True (modified vs dump differ) |
| B: single row deletion | ✅ | ✅ | row count 63 vs 64 — detected: True |
| C: single row addition | ✅ | ✅ | row count 41 vs 40 — detected: True |
| D: corrupted JSON | ✅ | ✅ | JSONDecodeError raised: Expecting value: line 1 column 12 (char 11) |
| E: CSV value modification | ✅ | ✅ | CSV value "CORRUPTED_NAME" not in SQL — detected: True |
| F: provenance source removal | ✅ | ✅ | missing source detected: ['skills'] |
| G: schema column change | ✅ | ✅ | column diff detected: ['class_id', 'name', 'unlock_jobs', 'unlock_silv |