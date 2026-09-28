#!/usr/bin/env python
"""Phase 1-2 v0.3: SQLite forensics + full SQL/CSV/JSON dump untuk SETIAP database"""
import sqlite3, os, json, hashlib, shutil

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

os.makedirs('database/dumps', exist_ok=True)
dbs = ['database/LUMIVARA_FORENSICS.sqlite', 'forensics/database/LUMIVARA_FORENSICS.sqlite']

discovered = []
for db_path in dbs:
    info = {'path': db_path, 'size': os.path.getsize(db_path), 'sha256': sha(db_path)}
    con = sqlite3.connect(db_path)
    con.text_factory = bytes  # hindari decode error
    cur = con.cursor()

    # pragmas
    info['integrity'] = cur.execute('PRAGMA integrity_check').fetchone()[0].decode()
    info['page_size'] = cur.execute('PRAGMA page_size').fetchone()[0]
    info['page_count'] = cur.execute('PRAGMA page_count').fetchone()[0]
    info['journal_mode'] = cur.execute('PRAGMA journal_mode').fetchone()[0].decode()
    fk_issues = cur.execute('PRAGMA foreign_key_check').fetchall()
    info['fk_check_clean'] = len(fk_issues) == 0

    tables = []
    for (t,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
        t = t.decode()
        cols = [{'name': r[1].decode(), 'type': (r[2] or b'').decode()} for r in cur.execute(f'PRAGMA table_info({t})').fetchall()]
        cnt = cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
        tables.append({'table': t, 'columns': cols, 'rows': cnt})
    info['tables'] = tables
    con.close()
    discovered.append(info)
    print(f"{db_path}: integrity={info['integrity']}, {len(tables)} tables, {sum(t['rows'] for t in tables)} rows")

json.dump(discovered, open('database/discovered_databases.json', 'w', encoding='utf-8'), indent=1)

# ===== FULL DUMP dari database/ (versi final dengan CLIENT_MINING) =====
src = 'database/LUMIVARA_FORENSICS.sqlite'
name = 'LUMIVARA_FORENSICS'
outdir = f'database/dumps/{name}'
os.makedirs(f'{outdir}/tables', exist_ok=True)
os.makedirs(f'{outdir}/csv', exist_ok=True)
os.makedirs(f'{outdir}/json', exist_ok=True)

con = sqlite3.connect(src)
cur = con.cursor()

# schema.sql
schema = cur.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL").fetchall()
with open(f'{outdir}/schema.sql', 'w', encoding='utf-8') as f:
    for (s,) in schema:
        f.write(s + ';\n\n')
print(f'schema.sql: {len(schema)} objects')

# per-table: sql, csv, json
table_names = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
total_rows = 0
for t in table_names:
    cols = [r[1] for r in cur.execute(f'PRAGMA table_info({t})').fetchall()]
    rows = cur.execute(f'SELECT * FROM {t}').fetchall()
    total_rows += len(rows)
    # SQL insert
    with open(f'{outdir}/tables/{t}.sql', 'w', encoding='utf-8') as f:
        f.write(f'-- {t}: {len(rows)} rows\n')
        for row in rows:
            vals = ','.join('NULL' if v is None else (f"'{str(v).replace(chr(39), chr(39)*2)}'" if isinstance(v, str) else str(v)) for v in row)
            f.write(f'INSERT INTO {t} VALUES ({vals});\n')
    # CSV
    import csv
    with open(f'{outdir}/csv/{t}.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for row in rows:
            w.writerow([('' if v is None else str(v)) for v in row])
    # JSON
    recs = [dict(zip(cols, [v.decode() if isinstance(v, bytes) else v for v in row])) for row in rows]
    json.dump(recs, open(f'{outdir}/json/{t}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# full_dump.sql (schema + data, executable)
with open(f'{outdir}/full_dump.sql', 'w', encoding='utf-8') as f:
    f.write('-- LUMIVARA_FORENSICS full dump — recreate dengan: sqlite3 new.sqlite < full_dump.sql\n')
    f.write('BEGIN TRANSACTION;\n\n')
    for (s,) in schema:
        f.write(s + ';\n\n')
    for t in table_names:
        rows = cur.execute(f'SELECT * FROM {t}').fetchall()
        for row in rows:
            vals = ','.join('NULL' if v is None else (f"'{str(v).replace(chr(39), chr(39)*2)}'" if isinstance(v, str) else str(v)) for v in row)
            f.write(f'INSERT INTO {t} VALUES ({vals});\n')
        f.write('\n')
    f.write('COMMIT;\n')
con.close()

print(f'dump complete: {total_rows} total rows, {len(table_names)} tables')
import subprocess
sz = os.path.getsize(f'{outdir}/full_dump.sql')
print(f'full_dump.sql: {sz:,} bytes')
