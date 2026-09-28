#!/usr/bin/env python
"""Phase 4-5: documentation claims audit + path reference audit"""
import json, os, re

# ===== Phase 4: claims =====
gdb = json.load(open('GAME_DB.json', encoding='utf-8'))
mdb = json.load(open('MONSTER_DB.json', encoding='utf-8'))
tr = json.load(open('TRANSLATIONS.json', encoding='utf-8'))
chg = json.load(open('research/changelog/CHANGELOG_NORMALIZED.json', encoding='utf-8'))
proto = json.load(open('protocol/NETWORK_PROTOCOL_v3.json', encoding='utf-8'))

actual = {
    'classes': len(gdb.get('skills', {})) and 10,  # dari CLASS_DB
    'skills': len(gdb['skills']),
    'items_consumables': len(gdb['consumables']),
    'cards': len(gdb['cards']),
    'statuses': len(gdb['status_effects']),
    'maps': len(gdb['maps']),
    'monsters': len(mdb['monsters']),
    'translations': len(tr),
    'changelog_entries': len(chg['entries']),
    'ws_events': len(proto.get('events', {})),
}

# cek CLASS_DB
cdb = json.load(open('database/CLASS_DB_v3.json', encoding='utf-8'))
actual['classes'] = len(cdb['classes'])

# cek starter_equipment
actual['starter_equipment'] = len(gdb.get('starter_equipment', []))

claims = [
    # (document, claim_text, claimed_value, actual_key)
    ('README.md', 'Classes = 10', 10, 'classes'),
    ('README.md', 'Skills = 64', 64, 'skills'),
    ('README.md', 'Items (consumable) = 80', 80, 'items_consumables'),
    ('README.md', 'Cards = 49', 49, 'cards'),
    ('README.md', 'Status effects = 42', 42, 'statuses'),
    ('README.md', 'Maps = 19', 19, 'maps'),
    ('README.md', 'Monsters = 40', 40, 'monsters'),
    ('README.md', 'Translations = 2,547', 2547, 'translations'),
    ('README.md', 'Changelog entries = 650', 650, 'changelog_entries'),
    ('README.md', 'WS event types = 26', 26, 'ws_events'),
]

results = []
for doc, claim, claimed, key in claims:
    act = actual[key]
    status = 'MATCH' if claimed == act else ('INCONSISTENT' if abs(claimed - act) > 0 else 'MATCH')
    results.append({
        'document': doc, 'claim': claim, 'claimed_value': claimed,
        'actual_value': act, 'source': f'database/{key} count',
        'confidence': 'VERIFIED', 'status': status,
    })

json.dump({'_meta': {'method': 'count langsung dari file database final'}, 'claims': results},
          open('repo_audit/DOCUMENTATION_CLAIMS.json', 'w', encoding='utf-8'), indent=1)
print('=== CLAIMS ===')
for r in results:
    flag = '✓' if r['status'] == 'MATCH' else '✗'
    print(f"  {flag} {r['claim']}: actual={r['actual_value']}")

# ===== Phase 5: path references =====
md_files = ['README.md', 'PROJECT.md', 'RECONSTRUCTION_REPORT.md']
all_paths = set()
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', 'app', 'nsis-out', 'asar-out')]
    for fn in files:
        all_paths.add(os.path.join(root, fn).replace(os.sep, '.').lstrip('.').replace('.', '/'))

path_refs = []
for md in md_files:
    src = open(md, encoding='utf-8').read()
    # cari path references: folder/file.json, .md, .sqlite, .py, .mjs
    for m in re.finditer(r'`?((?:database|protocol|formulas|research|diffs|provenance|validation|extraction|raw|docs|forensics|collect|web)[/\w.-]+\.(?:json|md|sqlite|py|mjs|js|txt))`?', src):
        ref = m.group(1)
        exists = os.path.exists(ref)
        path_refs.append({'document': md, 'referenced_path': ref, 'exists': exists,
                          'status': 'VALID' if exists else 'BROKEN_REFERENCE'})

json.dump(path_refs, open('repo_audit/PATH_AUDIT.json', 'w', encoding='utf-8'), indent=1)
print(f'\n=== PATH REFS ({len(path_refs)}) ===')
broken = [p for p in path_refs if not p['exists']]
for b in broken:
    print(f"  ✗ BROKEN: {b['document']} -> {b['referenced_path']}")
if not broken:
    print('  semua valid')
