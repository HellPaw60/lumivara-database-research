#!/usr/bin/env python
"""Phase 15: changelog normalization — 650 entri -> CHANGELOG_NORMALIZED.json"""
import re, json

src = open('web-v2/changelog-notice-BKeFrGHU.js', encoding='utf-8').read()

# entri: id:"...",date:"...",time:"...",title:"...",lines:[...]
entries = []
for m in re.finditer(r'id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"([^"]+)"(?:,lines:\[(.*?)\])?\}', src, re.S):
    eid, date, tm, title, lines_raw = m.groups()
    lines = re.findall(r'"((?:[^"\\]|\\.)*)"', lines_raw or '')
    # klasifikasi kategori dari id + title
    kat = 'UNKNOWN'
    blob = (eid + ' ' + title).lower()
    for kw, label in [
        ('kensei', 'CLASS'), ('nekobaku', 'CLASS'), ('mamushi', 'CLASS'), ('class', 'CLASS'),
        ('skill', 'SKILL'), ('passive', 'PASSIVE'),
        ('item', 'ITEM'), ('card', 'CARD'), ('megaphone', 'ITEM'), ('arrow', 'ITEM'),
        ('monster', 'MONSTER'), ('mob', 'MONSTER'), ('boss', 'MONSTER'),
        ('drop', 'DROP'), ('loot', 'DROP'),
        ('combat', 'COMBAT'), ('damage', 'COMBAT'), ('crit', 'COMBAT'), ('aspd', 'COMBAT'),
        ('silver', 'ECONOMY'), ('gold', 'ECONOMY'), ('market', 'ECONOMY'), ('shop', 'ECONOMY'), ('price', 'ECONOMY'), ('refund', 'ECONOMY'), ('premium', 'ECONOMY'),
        ('quest', 'QUEST'), ('daily', 'QUEST'), ('hunt', 'QUEST'),
        ('map', 'MAP'), ('rome', 'MAP'), ('glacier', 'MAP'), ('arena', 'MAP'),
        ('network', 'NETWORK'), ('disconnect', 'NETWORK'), ('lag', 'NETWORK'), ('reconnect', 'NETWORK'),
        ('ui', 'UI'), ('window', 'UI'), ('bag', 'UI'), ('hud', 'UI'), ('button', 'UI'), ('menu', 'UI'), ('display', 'UI'), ('แสดง', 'UI'),
        ('fix', 'BUGFIX'), ('แก้', 'BUGFIX'),
        ('guild', 'GUILD'), ('party', 'PARTY'), ('pet', 'PET'),
        ('refine', 'REFINE'), ('fusion', 'FUSION'),
        ('auto', 'AUTOPLAY'), ('bot', 'AUTOPLAY'),
    ]:
        if kw in blob:
            kat = label
            break
    entries.append({
        'id': eid, 'date': date, 'time': tm, 'title': title,
        'lines': lines, 'category': kat,
        'confidence': 'VERIFIED',
    })

# parse angka dari title (old->new value hints)
for e in entries:
    nums = re.findall(r'(\d[\d,.]*)\s*(?:%|→|->)\s*(\d[\d,.]*)', e['title'] + ' ' + ' '.join(e['lines']))
    if nums:
        e['value_changes'] = [{'from': a, 'to': b} for a, b in nums]

out = {
    '_meta': {
        'source': 'web-v2/changelog-notice-BKeFrGHU.js',
        'method': 'regex extraction dari bundle changelog',
        'note': 'kategori diklasifikasi via keyword id+title (heuristic = DERIVED); entri = VERIFIED',
        'entry_count': len(entries),
    },
    'entries': entries,
}
json.dump(out, open('forensics/CHANGELOG_NORMALIZED.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'entries: {len(entries)}')
from collections import Counter
for k, v in Counter(e['category'] for e in entries).most_common():
    print(f'  {k}: {v}')
print('value_changes terdeteksi:', sum(1 for e in entries if e.get("value_changes")))
