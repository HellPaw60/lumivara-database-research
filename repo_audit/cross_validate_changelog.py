#!/usr/bin/env python
"""Cross-validation: client bundle changelog (650) vs official web changelog (669)"""
import json, hashlib, time

client = json.load(open('research/changelog/CHANGELOG_NORMALIZED.json', encoding='utf-8'))['entries']
official = json.load(open('research/changelog/OFFICIAL_CHANGELOG.json', encoding='utf-8'))

cmap = {e['id']: e for e in client}
omap = {e['id']: e for e in official}

both = set(cmap) & set(omap)
only_client = set(cmap) - set(omap)
only_official = set(omap) - set(cmap)

# detail differences pada entri bersama
title_diffs, date_diffs, time_diffs, lines_diffs = [], [], [], []
for eid in both:
    c, o = cmap[eid], omap[eid]
    if c['title'] != o['title']: title_diffs.append({'id': eid, 'client': c['title'], 'official': o['title']})
    if c['date'] != o['date']: date_diffs.append(eid)
    if c['time'] != o['time']: time_diffs.append({'id': eid, 'client': c['time'], 'official': o['time']})
    if len(c.get('lines', [])) != len(o.get('lines', [])):
        lines_diffs.append({'id': eid, 'client_lines': len(c.get('lines', [])), 'official_lines': len(o.get('lines', []))})

# duplikat di masing-masing
from collections import Counter
c_dups = {k: v for k, v in Counter(e['id'] for e in client).items() if v > 1}
o_dups = {k: v for k, v in Counter(e['id'] for e in official).items() if v > 1}

# ordering: apakah urutan sama untuk entri bersama?
c_order = [e['id'] for e in client if e['id'] in both]
o_order = [e['id'] for e in official if e['id'] in both]
order_same = c_order == o_order

html = open('research/changelog/official_changelog_raw.html', encoding='utf-8').read()
notice = open('research/changelog/official_changelog_notice_bundle.js', encoding='utf-8').read()

result = {
    '_meta': {
        'client_source': 'web-v2/changelog-notice-BKeFrGHU.js (dari game client main bundle)',
        'client_hash': hashlib.sha256(open('web-v2/changelog-notice-BKeFrGHU.js', 'rb').read()).hexdigest(),
        'official_source': 'https://lumivaraonline.com/changelog/ (SPA) -> assets/changelog-notice-Dk8pLLLq.js',
        'official_hash': hashlib.sha256(notice.encode()).hexdigest(),
        'official_html_hash': hashlib.sha256(html.encode()).hexdigest(),
        'retrieved_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'method': 'HTTP retrieval + module import trace + regex parse',
        'note': 'Halaman /changelog/ adalah SPA shell; konten dimuat dari changelog-notice-Dk8pLLLq.js — bundle BERBEDA dari yang dipakai game client (BKeFrGHU). Ini snapshot lebih baru.',
    },
    'counts': {
        'client_entries': len(client), 'official_entries': len(official),
        'client_unique_ids': len(cmap), 'official_unique_ids': len(omap),
        'matched': len(both), 'only_in_client': len(only_client), 'only_in_official': len(only_official),
    },
    'differences': {
        'title_diffs': title_diffs, 'date_diffs': date_diffs, 'time_diffs': time_diffs,
        'lines_count_diffs': lines_diffs,
        'ordering_same_for_shared': order_same,
        'client_duplicates': c_dups, 'official_duplicates': o_dups,
        'only_in_client_ids': sorted(only_client),
        'only_in_official_ids': sorted(only_official)[:30],
        'only_in_official_count': len(only_official),
    },
}
json.dump(result, open('research/changelog/CHANGELOG_CROSS_VALIDATION.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

print(f"client: {len(client)} ({len(cmap)} unique) | official: {len(official)} ({len(omap)} unique)")
print(f"matched: {len(both)} | only client: {len(only_client)} | only official: {len(only_official)}")
print(f"title diffs: {len(title_diffs)} | date diffs: {len(date_diffs)} | time diffs: {len(time_diffs)} | lines diffs: {len(lines_diffs)}")
print(f"ordering same: {order_same}")
print(f"client dups: {c_dups} | official dups: {o_dups}")
print(f"\nonly in official ({len(only_official)}):")
for eid in sorted(only_official)[:20]:
    print(f'  {eid} | {omap[eid]["date"]} {omap[eid]["time"]} | {omap[eid]["title"][:55]}')
if only_client:
    print(f"\nonly in client ({len(only_client)}):")
    for eid in sorted(only_client):
        print(f'  {eid} | {cmap[eid]["title"][:55]}')
