#!/usr/bin/env python
"""Archive new changelog snapshot B6x3YIz5"""
import re, json, os, shutil, hashlib

raw = open(os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'finalv06.html'), encoding='utf-8').read()
bundle_url = re.search(r'changelog-notice-([\w-]+)\.js', raw).group(1)
bundle_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', f'bundle_{bundle_url}.js')
print('fetching bundle:', bundle_url)

import urllib.request
req = urllib.request.Request(f'https://lumivaraonline.com/assets/changelog-notice-{bundle_url}.js',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
urllib.request.urlretrieve(req, bundle_path)
raw_bundle = open(bundle_path, encoding='utf-8').read()
print('sha256:', hashlib.sha256(raw_bundle.encode()).hexdigest()[:16], f'({len(raw_bundle):,} bytes)')

BS = chr(92); DQ = chr(34)

def parse(src):
    entries = []
    head_pat = re.compile(r'id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"((?:[^"\\]|\\.)*)"')
    LINE_STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
    for m in head_pat.finditer(src):
        eid, date, tm, title = m.groups()
        lines = []
        lm = re.match(r',lines:\[', src[m.end():m.end()+10])
        if lm:
            start = m.end() + lm.end() - 1
            depth, i, in_str, esc, end = 0, start, False, False, None
            while i < len(src):
                c = src[i]
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
            if end: lines = LINE_STR.findall(src[start+1:end])
        entries.append({'id': eid, 'date': date, 'time': tm, 'title': title, 'lines': lines})
    return entries

entries = parse(raw_bundle)
prev = json.load(open('research/changelog/OFFICIAL_CHANGELOG_V3.json', encoding='utf-8'))['entries']
prev_ids = set(e['id'] for e in prev)
new_ids = set(e['id'] for e in entries) - prev_ids

print(f'total: {len(entries)} | delta vs V3: {len(new_ids)} baru')
for e in entries:
    if e['id'] in new_ids:
        print(f'  BARU: {e["id"]} | {e["date"]} {e["time"]} | {e["title"][:65]}')

# arsip
shutil.copy(os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'finalv06.html'), 'research/changelog/official_changelog_raw_v3b.html')
shutil.copy(bundle_path, f'research/changelog/official_changelog_notice_bundle_v3b_{bundle_url}.js')
json.dump({'_meta': {'bundle': f'changelog-notice-{bundle_url}.js',
                     'sha256': hashlib.sha256(raw_bundle.encode()).hexdigest(),
                     'retrieved_at': '2026-09-28T19:55', 'entries': len(entries)},
           'entries': entries},
          open('research/changelog/OFFICIAL_CHANGELOG_V3B.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('archived as OFFICIAL_CHANGELOG_V3B.json')
