#!/usr/bin/env python
"""V0.5 changelog check #1: bandingkan bundle terbaru vs snapshot 18:18"""
import hashlib, re, json, os, shutil

tmp = os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
new_raw = open(os.path.join(tmp, 'chk_bundle.js'), encoding='utf-8').read()
print('new bundle sha256:', hashlib.sha256(new_raw.encode()).hexdigest()[:16], f'({len(new_raw):,} bytes)')

BSLASH = chr(92)
DQUOTE = chr(34)

def parse(src):
    entries, errors = [], []
    head_pat = re.compile('id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"((?:[^"' + BSLASH + DQUOTE + BSLASH[:0] + r']|\\.)*)"')
    # simpler: reuse proven pattern from v042
    head_pat = re.compile(r'id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"((?:[^"\\]|\\.)*)"')
    LINE_STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
    for m in head_pat.finditer(src):
        eid, date, tm, title = m.groups()
        pos = m.end()
        lines = []
        lm = re.match(r',lines:\[', src[pos:pos+10])
        if lm:
            start = pos + lm.end() - 1
            depth, i, in_str, esc, end = 0, start, False, False, None
            while i < len(src):
                c = src[i]
                if in_str:
                    if esc: esc = False
                    elif c == BSLASH: esc = True
                    elif c == DQUOTE: in_str = False
                else:
                    if c == DQUOTE: in_str = True
                    elif c == '[': depth += 1
                    elif c == ']':
                        depth -= 1
                        if depth == 0: end = i; break
                i += 1
            if end: lines = LINE_STR.findall(src[start+1:end])
            else: errors.append(f'{eid}: unterminated')
        entries.append({'id': eid, 'date': date, 'time': tm, 'title': title, 'lines': lines})
    return entries, errors

new_entries, new_errors = parse(new_raw)
old_entries = json.load(open('research/changelog/CANONICAL_OFFICIAL_CHANGELOG.json', encoding='utf-8'))['entries']

print(f'new: {len(new_entries)} entries ({len(new_errors)} errors) | old snapshot: {len(old_entries)}')
old_ids = set(e['id'] for e in old_entries)
new_ids = set(e['id'] for e in new_entries)
fresh = new_ids - old_ids
gone = old_ids - new_ids
print(f'entries BARU: {len(fresh)} | hilang: {len(gone)}')
for e in new_entries:
    if e['id'] in fresh:
        print(f'  {e["id"]} | {e["date"]} {e["time"]} | {e["title"][:70]}')
for g in gone:
    print(f'  HILANG: {g}')

# arsip snapshot baru
shutil.copy(os.path.join(tmp, 'chk_changelog.html'), 'research/changelog/official_changelog_raw_v2.html')
shutil.copy(os.path.join(tmp, 'chk_bundle.js'), 'research/changelog/official_changelog_notice_bundle_v2.js')
json.dump({'_meta': {'bundle': 'changelog-notice-D0Wscyxj.js',
                     'sha256': hashlib.sha256(new_raw.encode()).hexdigest(),
                     'retrieved_at': '2026-09-28T19:08', 'entries': len(new_entries)},
           'entries': new_entries},
          open('research/changelog/OFFICIAL_CHANGELOG_V2.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('archived as OFFICIAL_CHANGELOG_V2.json')
