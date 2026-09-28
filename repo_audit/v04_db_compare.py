#!/usr/bin/env python
"""Phase 3 v0.4: DB_COMPARE — field-level comparison dua SQLite"""
import sqlite3, json, os

os.makedirs('research/v04/database_merge', exist_ok=True)

def load(db):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    tables = {}
    for (t,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
        cols = [(r[1], r[2]) for r in cur.execute(f'PRAGMA table_info({t})').fetchall()]
        rows = [dict(r) for r in cur.execute(f'SELECT * FROM {t}').fetchall()]
        tables[t] = {'columns': cols, 'rows': rows}
    con.close()
    return tables

A = load('database/LUMIVARA_FORENSICS.sqlite')          # final
B = load('forensics/database/LUMIVARA_FORENSICS.sqlite')  # initial

schema_diff = {'tables_only_in_final': [], 'tables_only_in_initial': [],
               'column_changes': {}, 'common_tables': []}
row_diff = {}
value_diff = {}

all_tables = sorted(set(A) | set(B))
for t in all_tables:
    if t in A and t in B:
        schema_diff['common_tables'].append(t)
        # column diff
        ca = [c for c, _ in A[t]['columns']]
        cb = [c for c, _ in B[t]['columns']]
        if ca != cb:
            schema_diff['column_changes'][t] = {'final': ca, 'initial': cb}
        # row diff (deterministic: by row index + full compare)
        ra, rb = A[t]['rows'], B[t]['rows']
        row_diff[t] = {'final_rows': len(ra), 'initial_rows': len(rb),
                       'delta': len(ra) - len(rb)}
        # value diff untuk tabel dengan PK jelas
        if len(ra) > 0 and len(rb) > 0:
            # pakai kolom pertama sebagai key
            key_col = ca[0]
            mapA = {str(r[key_col]): r for r in ra}
            mapB = {str(r[key_col]): r for r in rb}
            added = [k for k in mapA if k not in mapB]
            removed = [k for k in mapB if k not in mapA]
            modified = []
            for k in mapA:
                if k in mapB and dict(mapA[k]) != dict(mapB[k]):
                    changed_fields = [c for c in ca if mapA[k][c] != mapB[k].get(c)]
                    modified.append({'key': k, 'changed_fields': changed_fields})
            value_diff[t] = {'added': added, 'removed': removed, 'modified': modified}
    elif t in A:
        schema_diff['tables_only_in_final'].append(t)
    else:
        schema_diff['tables_only_in_initial'].append(t)

out = {
    '_meta': {'final': 'database/LUMIVARA_FORENSICS.sqlite',
              'initial': 'forensics/database/LUMIVARA_FORENSICS.sqlite',
              'method': 'deterministic column+row+value comparison'},
    'schema_diff': schema_diff,
    'row_diff': row_diff,
    'value_diff': value_diff,
}
json.dump(out, open('research/v04/database_merge/DB_COMPARE.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# ringkas
print('=== SCHEMA ===')
print('only in final:', schema_diff['tables_only_in_final'])
print('only in initial:', schema_diff['tables_only_in_initial'])
print('column changes:', list(schema_diff['column_changes'].keys()))
print('\n=== ROW DELTA ===')
for t, d in row_diff.items():
    if d['delta'] != 0:
        print(f"  {t}: {d['initial_rows']} -> {d['final_rows']} ({d['delta']:+d})")
print('\n=== VALUE DIFF (tabel berubah) ===')
for t, d in value_diff.items():
    if d['added'] or d['removed'] or d['modified']:
        print(f"  {t}: +{len(d['added'])} -{len(d['removed'])} ~{len(d['modified'])}")
        for m in d['modified'][:3]:
            print(f"    modified {m['key']}: fields {m['changed_fields']}")
