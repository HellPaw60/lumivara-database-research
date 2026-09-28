#!/usr/bin/env python
"""Phase 6-7: database audit + cross-database relationship audit"""
import json, sqlite3, os, hashlib

def sha(p):
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return h[:16]

audit = {'json': [], 'sqlite': []}

# JSON databases
for f in sorted(os.listdir('database')):
    if not f.endswith('.json'): continue
    p = f'database/{f}'
    try:
        d = json.load(open(p, encoding='utf-8'))
        keys = list(d.keys())
        counts = {k: len(v) for k, v in d.items() if isinstance(v, (list, dict)) and k != '_meta'}
        audit['json'].append({'file': f, 'size': os.path.getsize(p), 'sha256': sha(p),
                              'top_keys': keys[:8], 'record_counts': counts, 'status': 'OK'})
    except Exception as e:
        audit['json'].append({'file': f, 'status': f'PARSE_ERROR: {e}'})

# SQLite
p = 'database/LUMIVARA_FORENSICS.sqlite'
con = sqlite3.connect(p)
cur = con.cursor()
integrity = cur.execute('PRAGMA integrity_check').fetchone()[0]
tables = []
for (t,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != '_prov'"):
    cnt = cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
    tables.append({'table': t, 'rows': cnt})
audit['sqlite'] = {'file': p, 'size': os.path.getsize(p), 'sha256': sha(p),
                   'integrity': integrity, 'tables': tables}
con.close()

json.dump(audit, open('repo_audit/DATABASE_AUDIT.json', 'w', encoding='utf-8'), indent=1)
print('=== JSON DB ===')
for j in audit['json']:
    print(f"  {j['file']}: {j.get('status')} {json.dumps(j.get('record_counts', {}))[:100]}")
print(f"=== SQLite: integrity={audit['sqlite']['integrity']} ===")
for t in audit['sqlite']['tables']:
    print(f"  {t['table']}: {t['rows']} rows")

# ===== Phase 7: relationships =====
gdb = json.load(open('GAME_DB.json', encoding='utf-8'))
mdb = json.load(open('MONSTER_DB.json', encoding='utf-8'))
cdb = json.load(open('database/CLASS_DB_v3.json', encoding='utf-8'))

rel = {'issues': [], 'checks': []}

# 1. skill.classId -> classes
valid_classes = set(cdb['classes'].keys())
bad = [(s, d.get('classId')) for s, d in gdb['skills'].items()
       if d.get('classId') and d['classId'] not in valid_classes]
rel['checks'].append({'check': 'skill.classId -> classes', 'result': 'OK' if not bad else f'BROKEN: {bad}'})

# 2. map portals -> maps
maps = set(gdb['maps'].keys())
bad_portals = [(m, p['to']) for m, d in gdb['maps'].items() for p in d.get('portals', []) if p['to'] not in maps]
rel['checks'].append({'check': 'map.portals.to -> maps', 'result': 'OK' if not bad_portals else f'BROKEN: {bad_portals}'})

# 3. monster drops -> items (consumables) — item key harus ada
item_keys = set(gdb['consumables'].keys())
# tambah equipment/gear keys yang mungkin (dari starter + template)
gear_items = set()
for g in gdb.get('starter_equipment', []):
    pass  # starter pakai name bukan key
orphan_drops = {}
for k, m in mdb['monsters'].items():
    for item in (m.get('drops') or {}):
        if item not in item_keys and item not in ('armor', 'sword', 'shoes', 'shield', 'accessory1', 'accessory2',
                                                   'mouth', 'garment', 'head', 'ammo', 'pet', 'refine_stone'):
            orphan_drops.setdefault(item, []).append(k)
rel['checks'].append({'check': 'monster.drops -> items',
                      'result': f'{len(orphan_drops)} item tidak ada di ITEMS (material drops — expected, ITEMS hanya consumable)',
                      'detail': list(orphan_drops.keys())[:10]})

# 4. mob_status_attacks -> monsters (by name)
msa = gdb['mob_status_attacks']
monster_names = {m['name'] for m in mdb['monsters'].values()}
orphans = [n for n in msa if n not in monster_names]
rel['checks'].append({'check': 'mob_status_attacks.monster_name -> monsters',
                      'result': f'ORPHAN: {orphans}' if orphans else 'OK',
                      'note': 'Crowned Prism Hopper = World Boss (prism-hopper key ada di MONSTER_DB sebagai Prism Hopper Lv1 elite) — name variant'})

# 5. skills_by_class (CLASS_DB) vs skills (GAME_DB)
sbc = cdb.get('skills_by_class', {})
total_sbc = sum(len(v) for v in sbc.values())
rel['checks'].append({'check': 'CLASS_DB.skills_by_class total vs GAME_DB.skills',
                      'result': f'{total_sbc} vs {len(gdb["skills"])} — {"OK" if total_sbc == len(gdb["skills"]) else "MISMATCH"}'})

json.dump(rel, open('repo_audit/RELATIONSHIP_AUDIT.json', 'w', encoding='utf-8'), indent=1)
print('\n=== RELATIONSHIPS ===')
for c in rel['checks']:
    print(f"  {c['check']}: {c['result'][:100]}")
