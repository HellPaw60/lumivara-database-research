#!/usr/bin/env python
"""Archive changelog snapshot B6x3YIz5"""
import re, json, os, shutil, hashlib

raw = open(os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'bundle_B6x3YIz5.js'), encoding='utf-8').read()
print('sha256:', hashlib.sha256(raw.encode()).hexdigest()[:16], f'({len(raw):,} bytes)')

head_pat = re.compile(r'id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"((?:[^"\\]|\\.)*)"')
LINE_STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
BS = chr(92); DQ = chr(34)

entries = []
for m in head_pat.finditer(raw):
    eid, date, tm, title = m.groups()
    lines = []
    lm = re.match(r',lines:\[', raw[m.end():m.end()+10])
    if lm:
        start = m.end() + lm.end() - 1
        depth, i, in_str, esc, end = 0, start, False, False, None
        while i < len(raw):
            c = raw[i]
            if in_str:
                if esc: esc = False
                elif c == BS: esc = True
                elif c == DQ: in_str = False
            else:
                if c == DQ: in_str = True
                elif c == '[': depth += 1
                elif c == ']':
                    depth -= 1
                    if depth == 0: end = i; break
            i += 1
        if end: lines = LINE_STR.findall(raw[start+1:end])
    entries.append({'id': eid, 'date': date, 'time': tm, 'title': title, 'lines': lines})

prev = json.load(open('research/changelog/OFFICIAL_CHANGELOG_V3.json', encoding='utf-8'))['entries']
prev_ids = set(e['id'] for e in prev)
new_ids = set(e['id'] for e in entries) - prev_ids
print(f'total: {len(entries)} | delta vs V3: {len(new_ids)} baru')
for e in entries:
    if e['id'] in new_ids:
        print(f'  BARU: {e["id"]} | {e["date"]} {e["time"]} | {e["title"][:65]}')

shutil.copy(os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'bundle_B6x3YIz5.js'),
            'research/changelog/official_changelog_notice_bundle_v3b.js')
json.dump({'_meta': {'bundle': 'changelog-notice-B6x3YIz5.js',
                     'sha256': hashlib.sha256(raw.encode()).hexdigest(),
                     'retrieved_at': '2026-09-28T19:55', 'entries': len(entries)},
           'entries': entries},
          open('research/changelog/OFFICIAL_CHANGELOG_V3B.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('archived as OFFICIAL_CHANGELOG_V3B.json')
