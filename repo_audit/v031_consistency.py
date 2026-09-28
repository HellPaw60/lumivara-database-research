#!/usr/bin/env python
"""Phase 2 v0.3.1: documentation consistency audit — semua angka dok vs dataset aktual"""
import json, sqlite3, re, os

gdb = json.load(open('GAME_DB.json', encoding='utf-8'))
mdb = json.load(open('MONSTER_DB.json', encoding='utf-8'))
tr = json.load(open('TRANSLATIONS.json', encoding='utf-8'))
chg = json.load(open('research/changelog/CHANGELOG_NORMALIZED.json', encoding='utf-8'))
proto = json.load(open('protocol/NETWORK_PROTOCOL_v3.json', encoding='utf-8'))
cdb = json.load(open('database/CLASS_DB_v3.json', encoding='utf-8'))
fml = json.load(open('formulas/FORMULA_DATABASE_V03.json', encoding='utf-8'))

con = sqlite3.connect('database/LUMIVARA_FORENSICS.sqlite')
cur = con.cursor()
sql_tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != '_prov'").fetchall()]
sql_rows = sum(cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t in sql_tables)
con.close()

actual = {
    'classes': len(cdb['classes']),
    'skills': len(gdb['skills']),
    'items_consumables': len(gdb['consumables']),
    'cards': len(gdb['cards']),
    'statuses': len(gdb['status_effects']),
    'maps': len(gdb['maps']),
    'monsters': len(mdb['monsters']),
    'monster_status_attacks': len(gdb['mob_status_attacks']),
    'translations': len(tr),
    'changelog_entries': len(chg['entries']),
    'changelog_unique_ids': len(set(e['id'] for e in chg['entries'])),
    'ws_events': len(proto.get('events', {})),
    'formulas': len(fml['formulas']),
    'sqlite_tables': len(sql_tables),
    'sqlite_rows': sql_rows,
}

# baca dokumen & cari angka
docs = {}
for f in ['README.md', 'RECONSTRUCTION_REPORT.md', 'repo_audit/V03_AUDIT.md']:
    docs[f] = open(f, encoding='utf-8').read()

checks = []
def check(doc, claim, pattern, key, expect_match=True):
    found = re.findall(pattern, docs[doc])
    val = actual[key]
    # ekstrak angka dari setiap frasa yang cocok
    doc_nums = []
    for phrase in found:
        nums = re.findall(r'\d[\d,.]*', phrase)
        doc_nums.extend(n.replace(',', '').replace('.', '') for n in nums)
    ok = (str(val) in doc_nums) if doc_nums else not expect_match
    checks.append({'doc': doc, 'claim': claim, 'doc_values': found, 'actual': val,
                   'status': 'MATCH' if ok else ('NOT_FOUND' if not found else 'MISMATCH')})

for doc in docs:
    check(doc, 'classes=10', r'\b10 classes|\bClasses \| 10\b|classes.*10', 'classes')
    check(doc, 'skills=64', r'\b64 skill', 'skills')
    check(doc, 'items=80', r'\b80 (?:item|consumable)', 'items_consumables')
    check(doc, 'cards=49', r'\b49 (?:card|kartu)', 'cards')
    check(doc, 'monsters=40', r'\b40 monster', 'monsters')
    check(doc, 'maps=19', r'\b19 map', 'maps')
    check(doc, 'statuses=42', r'\b42 status', 'statuses')
    check(doc, 'translations=2547', r'2[,.]?547', 'translations')
    check(doc, 'changelog=650', r'\b650 (?:changelog |entri|entries)', 'changelog_entries')
    check(doc, 'ws_events=26', r'\b26 (?:event|WS)', 'ws_events')
    check(doc, 'formulas=18', r'\b18 formula', 'formulas')
    check(doc, 'sqlite_tables=12', r'\b12 tabel|\b12 tables', 'sqlite_tables')
    check(doc, 'sqlite_rows=2891', r'2[,.]?891', 'sqlite_rows')

# summary
match = sum(1 for c in checks if c['status'] == 'MATCH')
mismatch = [c for c in checks if c['status'] == 'MISMATCH']
notfound = [c for c in checks if c['status'] == 'NOT_FOUND']

out = {
    '_meta': {'docs_checked': list(docs.keys()), 'total_checks': len(checks)},
    'actual_values': actual,
    'checks': checks,
    'summary': {'match': match, 'mismatch': len(mismatch), 'not_found': len(notfound)},
}
json.dump(out, open('repo_audit/V031_DOC_CONSISTENCY.json', 'w', encoding='utf-8'), indent=1)

md = ['# V0.3.1 Documentation Consistency Audit', '',
      f'**{match}/{len(checks)} checks MATCH** | {len(mismatch)} mismatch | {len(notfound)} not found', '',
      '## Actual Dataset Values', '', '| Key | Value |', '|---|---|']
for k, v in actual.items():
    md.append(f'| {k} | {v} |')
md += ['', '## Checks', '', '| Doc | Claim | Doc Value | Actual | Status |', '|---|---|---|---|---|']
for c in checks:
    md.append(f"| {c['doc']} | {c['claim']} | {c['doc_values'][:2]} | {c['actual']} | {c['status']} |")
open('repo_audit/V031_DOC_CONSISTENCY.md', 'w', encoding='utf-8').write('\n'.join(md))

print(f'MATCH: {match}/{len(checks)}')
for c in mismatch:
    print(f"  MISMATCH: {c['doc']} — {c['claim']}: doc={c['doc_values']} actual={c['actual']}")
for c in notfound[:5]:
    print(f"  NOT_FOUND: {c['doc']} — {c['claim']}")
