#!/usr/bin/env python
"""V0.4.2 Phase 2-4: full content comparison + canonical dataset"""
import json, hashlib
from collections import Counter

client = json.load(open('research/changelog/CANONICAL_CLIENT_CHANGELOG.json', encoding='utf-8'))['entries']
official = json.load(open('research/changelog/CANONICAL_OFFICIAL_CHANGELOG.json', encoding='utf-8'))['entries']

# grup by ID (menangani duplikat upstream)
def group(entries):
    g = {}
    for e in entries:
        g.setdefault(e['id'], []).append(e)
    return g

cg, og = group(client), group(official)

classification = {}  # id -> {status, detail}
canonical = []       # dataset gabungan

all_ids = sorted(set(cg) | set(og))
for eid in all_ids:
    in_c, in_o = eid in cg, eid in og
    if in_c and in_o:
        c_list, o_list = cg[eid], og[eid]
        # bandingkan seluruh instance (duplikat upstream: kedua sumber punya 2 instance?)
        c_sigs = [json.dumps(e, sort_keys=True, ensure_ascii=False) for e in c_list]
        o_sigs = [json.dumps(e, sort_keys=True, ensure_ascii=False) for e in o_list]
        if c_sigs == o_sigs:
            status = 'EXACT_MATCH' if len(c_list) == 1 else 'DUPLICATE_UPSTREAM'
            detail = f'{len(c_list)} instance(s) identical across sources'
        else:
            # metadata sama, lines beda?
            c0, o0 = c_list[0], o_list[0]
            meta_same = (c0['date'], c0['time'], c0['title']) == (o0['date'], o0['time'], o0['title'])
            lines_same = all(c['lines'] == o['lines'] for c, o in zip(c_list, o_list)) and len(c_list) == len(o_list)
            if meta_same and not lines_same:
                status = 'METADATA_MATCH_CONTENT_DIFF'
                detail = f'lines differ: client={c0["lines"][:1]} official={o0["lines"][:1]}'
            else:
                # cari field mana yang beda
                diffs = []
                if c0['date'] != o0['date']: diffs.append('date')
                if c0['time'] != o0['time']: diffs.append('time')
                if c0['title'] != o0['title']: diffs.append('title')
                if c0['lines'] != o0['lines']: diffs.append('lines')
                status = 'METADATA_MATCH_CONTENT_DIFF' if not diffs[:3] else 'CONTENT_DIFF'
                detail = f'fields differ: {diffs}'
        # canonical: pakai official (freshest)
        for o in o_list:
            canonical.append({**o, 'sources': ['CLIENT_BUNDLE', 'OFFICIAL_WEB'],
                              'source_status': status,
                              'confidence': 'VERIFIED_BOTH_SOURCES' if status in ('EXACT_MATCH', 'DUPLICATE_UPSTREAM') else 'VERIFIED_OFFICIAL'})
    elif in_c:
        status, detail = 'CLIENT_ONLY', 'hanya di client snapshot'
        for c in c_list:
            canonical.append({**c, 'sources': ['CLIENT_BUNDLE'], 'source_status': status, 'confidence': 'VERIFIED_CLIENT'})
    else:
        status, detail = 'OFFICIAL_ONLY', 'update baru setelah snapshot client'
        for o in o_list:
            canonical.append({**o, 'sources': ['OFFICIAL_WEB'], 'source_status': status, 'confidence': 'VERIFIED_OFFICIAL'})

    classification[eid] = {'status': status, 'detail': detail}

# ordering comparison (shared IDs, first occurrence order)
c_order = [e['id'] for e in client]
o_order = [e['id'] for e in official]
shared_c = [i for i in c_order if i in og]
shared_o = [i for i in o_order if i in cg]
ordering_identical = shared_c == shared_o

# summary
counts = Counter(v['status'] for v in classification.values())
full_content_match = sum(1 for eid, v in classification.items()
                         if v['status'] in ('EXACT_MATCH', 'DUPLICATE_UPSTREAM')
                         and cg[eid][0]['lines'] == og[eid][0]['lines'] and len(cg[eid][0]['lines']) > 0)

result = {
    '_meta': {
        'parser': 'canonical v1 (bracket-match) — sama untuk kedua sumber',
        'previous_613_lines_diff_resolution': 'PARSER_ERROR pada parser official lama (regex lazy gagal); raw source identik — terbukti via raw slice comparison',
    },
    'counts': {
        'client_entries': len(client), 'official_entries': len(official),
        'unique_ids_total': len(all_ids),
        **dict(counts),
    },
    'full_content_matches': full_content_match,
    'ordering_identical_for_shared': ordering_identical,
    'duplicate_ids': {k: {'client': len(v), 'official': len(og[k])}
                       for k, v in cg.items() if len(v) > 1},
    'classification': classification,
}
json.dump(result, open('research/changelog/FULL_CHANGELOG_COMPARISON.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# canonical dataset (Phase 4)
canon_out = {
    '_meta': {
        'definition': 'OFFICIAL_WEB = freshest public source; CLIENT_BUNDLE = historical snapshot (dipertahankan, tidak dioverwrite)',
        'total_entries': len(canonical),
        'source_status_counts': dict(Counter(e['source_status'] for e in canonical)),
    },
    'entries': canonical,
}
json.dump(canon_out, open('research/changelog/CHANGELOG_CANONICAL.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
# juga ke database/json
json.dump(canon_out, open('database/json/CHANGELOG_CANONICAL.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

print('=== KLASIFIKASI ===')
for k, v in counts.items():
    print(f'  {k}: {v}')
print(f'full content matches (lines identik, non-empty): {full_content_match}')
print(f'ordering identical: {ordering_identical}')
print(f'duplicates: {result["duplicate_ids"]}')
print(f'canonical entries: {len(canonical)}')
