#!/usr/bin/env python
"""Official changelog parser — dari bundle changelog-notice-Dk8pLLLq.js"""
import re, json, hashlib

src = open('research/changelog/official_changelog_notice_bundle.js', encoding='utf-8').read()
print('sha256:', hashlib.sha256(src.encode()).hexdigest()[:16])

pat = re.compile(r'id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"([^"]+)"')
lines_pat = re.compile(r'"((?:[^"\\]|\\.)*)"')

entries = []
for m in pat.finditer(src):
    eid, date, tm, title = m.groups()
    # cari lines array setelah title
    tail = src[m.end():m.end()+300]
    lm = re.match(r',lines:\[(.*?)\]\}', tail, re.S)
    lines = lines_pat.findall(lm.group(1)) if lm else []
    entries.append({'id': eid, 'date': date, 'time': tm, 'title': title, 'lines': lines})

print(f'official entries: {len(entries)}')
print(f'unique IDs: {len(set(e["id"] for e in entries))}')
from collections import Counter
dates = Counter(e['date'] for e in entries)
print('dates:', dict(sorted(dates.items())))
print('\n5 terbaru:')
for e in entries[:5]:
    print(f'  {e["id"]} | {e["date"]} {e["time"]} | {e["title"][:60]}')
print('\n5 tertua:')
for e in entries[-5:]:
    print(f'  {e["id"]} | {e["date"]} {e["time"]} | {e["title"][:60]}')

json.dump(entries, open('research/changelog/OFFICIAL_CHANGELOG.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
