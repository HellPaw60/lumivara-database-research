#!/usr/bin/env python
"""Phase 18: VALIDATION_REPORT.md — duplikat, orphan, kontradiksi"""
import json, sqlite3, os

report = ['# Validation Report — Lumivara Forensics v3', '']
issues = []
stats = {}

# 1. JSON parse test
for f in ['GAME_DB.json', 'MONSTER_DB.json', 'TRANSLATIONS.json', 'DROP_DB.json',
          'forensics/CHANGELOG_NORMALIZED.json', 'forensics/inventory_manifest.json']:
    try:
        json.load(open(f, encoding='utf-8'))
        stats[f] = 'OK'
    except Exception as e:
        stats[f] = f'PARSE ERROR: {e}'
        issues.append(f'JSON parse gagal: {f}: {e}')

# 2. SQLite integrity
con = sqlite3.connect('forensics/database/LUMIVARA_FORENSICS.sqlite')
cur = con.cursor()
integrity = cur.execute('PRAGMA integrity_check').fetchone()[0]
stats['sqlite_integrity'] = integrity
if integrity != 'ok':
    issues.append(f'SQLite integrity: {integrity}')

# 3. Duplicate check
gdb = json.load(open('GAME_DB.json', encoding='utf-8'))
mdb = json.load(open('MONSTER_DB.json', encoding='utf-8'))

# skill duplikat nama
skill_names = {}
for sid, s in gdb['skills'].items():
    nm = s.get('name')
    if nm:
        skill_names.setdefault(nm, []).append(sid)
dups = {k: v for k, v in skill_names.items() if len(v) > 1}
if dups:
    issues.append(f'Skill nama duplikat (bisa shared antar class — valid): {json.dumps(dups)}')
stats['skill_name_dupes'] = len(dups)

# monster key vs name konsisten
monster_keys = set(mdb['monsters'].keys())
mob_status_names = set(gdb['mob_status_attacks'].keys())
orphan_status = mob_status_names - {m['name'] for m in mdb['monsters'].values()}
if orphan_status:
    issues.append(f'mob_status_attacks menunjuk monster yang tidak ada di MONSTER_DB: {orphan_status}')
stats['orphan_status_refs'] = len(orphan_status)

# card source check: kartu menyebut monster (hopper_card -> Prism Hopper)
card_monster_orphans = []
for cid in gdb['cards']:
    base = cid.replace('_card', '')
    # cek apakah ada monster dengan key semacam itu
    if base not in monster_keys and base + 's' not in monster_keys:
        card_monster_orphans.append(cid)
stats['cards_without_confirmed_monster'] = len(card_monster_orphans)
# catatan: bukan error — mapping nama kartu ke monster via konvensi penamaan

# 4. Impossible values
bad_hp = [(k, m['maxHp']) for k, m in mdb['monsters'].items() if m['maxHp'] <= 0]
if bad_hp:
    issues.append(f'Monster HP <= 0: {bad_hp}')
bad_level = [(k, m['level']) for k, m in mdb['monsters'].items() if not m['level'] or m['level'] < 1]
if bad_level:
    issues.append(f'Monster level invalid: {bad_level}')
stats['invalid_monster_values'] = len(bad_hp) + len(bad_level)

# 5. Referential: skill class_id valid?
valid_classes = {'novice', 'swordman', 'mage', 'archer', 'acolyte', 'merchant', 'thief', 'mamushi', 'nekobaku', 'kensei'}
bad_class = [sid for sid, s in gdb['skills'].items() if s.get('classId') and s['classId'] not in valid_classes]
if bad_class:
    issues.append(f'Skill dengan classId tidak dikenal: {bad_class}')
stats['skills_with_invalid_class'] = len(bad_class)

# 6. Map adjacency sanity
maps = gdb['maps']
for mid, m in maps.items():
    for p in m.get('portals', []):
        if p['to'] not in maps:
            issues.append(f'Portal {mid}->{p["to"]} menunjuk map tidak dikenal')
stats['map_count'] = len(maps)

# 7. TRANSLATIONS dupes
tr = json.load(open('TRANSLATIONS.json', encoding='utf-8'))
stats['translation_entries'] = len(tr)

con.close()

report.append('## Hasil Test')
report.append('| Item | Status |')
report.append('|---|---|')
for k, v in stats.items():
    report.append(f'| {k} | {v} |')
report.append('')
if issues:
    report.append('## Temuan / Isu')
    for i in issues:
        report.append(f'- {i}')
else:
    report.append('## Temuan / Isu')
    report.append('- Tidak ada isu struktural kritis.')
report.append('')
report.append('## Catatan')
report.append('- Skill dengan nama sama antar class (mis. shared passive) BUKAN duplikat error.')
report.append('- Kartu tanpa monster terkonfirmasi: mapping kartu->monster via konvensi nama, belum diverifikasi biner (INFERRED).')
report.append(f'- Total isu: {len(issues)}')

open('forensics/validation/VALIDATION_REPORT.md', 'w', encoding='utf-8').write('\n'.join(report))
print('\n'.join(report))
