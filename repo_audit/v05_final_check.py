#!/usr/bin/env python
"""Final changelog check v3: parse bundle DY1AbHUd"""
import re, json, os, hashlib, shutil

raw = open(os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'final_bundle.js'), encoding='utf-8').read()
print('bundle sha256:', hashlib.sha256(raw.encode()).hexdigest()[:16], f'({len(raw):,} bytes)')

head_pat = re.compile(r'id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"((?:[^"\\]|\\.)*)"')
LINE_STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
BS = chr(92)

entries = []
for m in head_pat.finditer(raw):
    eid, date, tm, title = m.groups()
    pos = m.end()
    lines = []
    lm = re.match(r',lines:\[', raw[pos:pos+10])
    if lm:
        start = pos + lm.end() - 1
        depth, i, in_str, esc, end = 0, start, False, False, None
        while i < len(raw):
            c = raw[i]
            if in_str:
                if esc: esc = False
                elif c == BS: esc = True
                elif c == '"': in_str = False
            else:
                if c == '"': in_str = True
                elif c == '[': depth += 1
                elif c == ']':
                    depth -= 1
                    if depth == 0: end = i; break
            i += 1
        if end: lines = LINE_STR.findall(raw[start+1:end])
    entries.append({'id': eid, 'date': date, 'time': tm, 'title': title, 'lines': lines})

prev = json.load(open('research/changelog/OFFICIAL_CHANGELOG_V2.json', encoding='utf-8'))['entries']
prev_ids = set(e['id'] for e in prev)
new_ids = set(e['id'] for e in entries) - prev_ids
print(f'total: {len(entries)} | delta vs v2: {len(new_ids)} baru')
for e in entries:
    if e['id'] in new_ids:
        print(f'  BARU: {e["id"]} | {e["time"]} | {e["title"][:65]}')

shutil.copy(os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'final_chk.html'), 'research/changelog/official_changelog_raw_v3.html')
shutil.copy(os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'final_bundle.js'), 'research/changelog/official_changelog_notice_bundle_v3.js')
json.dump({'_meta': {'bundle': 'changelog-notice-DY1AbHUd.js',
                     'sha256': hashlib.sha256(raw.encode()).hexdigest(),
                     'retrieved_at': '2026-09-28T19:40', 'entries': len(entries)},
           'entries': entries},
          open('research/changelog/OFFICIAL_CHANGELOG_V3.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('archived as OFFICIAL_CHANGELOG_V3.json')
