#!/usr/bin/env python
"""V0.4.2 Phase 7: validation checks untuk canonical changelog reconciliation"""
import json, os, sys

PASS, FAIL = 0, 0
def check(name, fn):
    global PASS, FAIL
    try:
        ok, detail = fn()
        PASS += 1 if ok else 0
        FAIL += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {str(detail)[:90]}")
        return ok
    except Exception as e:
        FAIL += 1
        print(f"  [FAIL] {name}: ERROR {e}")

def c1():
    d = json.load(open('research/changelog/CANONICAL_CLIENT_CHANGELOG.json', encoding='utf-8'))
    errs = d['_meta']['parser_errors']
    return len(errs) == 0 and d['_meta']['entry_count'] == 650, f"650 entries, {len(errs)} errors, {sum(len(e['lines']) for e in d['entries'])} lines"
check('canonical_client_parse', c1)

def c2():
    d = json.load(open('research/changelog/CANONICAL_OFFICIAL_CHANGELOG.json', encoding='utf-8'))
    errs = d['_meta']['parser_errors']
    return len(errs) == 0 and d['_meta']['entry_count'] == 669, f"669 entries, {len(errs)} errors, {sum(len(e['lines']) for e in d['entries'])} lines"
check('canonical_official_parse', c2)

def c3():
    d = json.load(open('research/changelog/FULL_CHANGELOG_COMPARISON.json', encoding='utf-8'))
    c = d['counts']
    expected = {'client_entries': 650, 'official_entries': 669, 'EXACT_MATCH': 648,
                'DUPLICATE_UPSTREAM': 1, 'OFFICIAL_ONLY': 19, 'CLIENT_ONLY': 0,
                'METADATA_MATCH_CONTENT_DIFF': 0, 'PARSER_ERROR': 0}
    mismatches = {k: (c.get(k, 0), v) for k, v in expected.items() if c.get(k, 0) != v}
    return len(mismatches) == 0, mismatches if mismatches else f'all counts match: {expected}'
check('full_content_comparison', c3)

def c4():
    d = json.load(open('research/changelog/FULL_CHANGELOG_COMPARISON.json', encoding='utf-8'))
    dup = d['duplicate_ids']
    ok = list(dup.keys()) == ['2026-09-23-skill-rebalance'] and dup['2026-09-23-skill-rebalance'] == {'client': 2, 'official': 2}
    return ok, f'upstream duplicate preserved: {dup}'
check('duplicate_consistency', c4)

def c5():
    d = json.load(open('research/changelog/FULL_CHANGELOG_COMPARISON.json', encoding='utf-8'))
    return d['ordering_identical_for_shared'] is True, 'ordering identical for all shared'
check('ordering_consistency', c5)

def c6():
    for f in ['research/changelog/CANONICAL_CLIENT_CHANGELOG.json',
              'research/changelog/CANONICAL_OFFICIAL_CHANGELOG.json']:
        m = json.load(open(f, encoding='utf-8'))['_meta']
        if not m.get('source') or not m.get('source_sha256'):
            return False, f'{f}: missing provenance'
    return True, 'both canonical files have source + sha256'
check('source_provenance', c6)

def c7():
    files = ['research/changelog/official_changelog_raw.html',
             'research/changelog/official_changelog_notice_bundle.js']
    return all(os.path.exists(f) and os.path.getsize(f) > 1000 for f in files), 'official raw evidence archived'
check('official_source_retrieval', c7)

def c8():
    d = json.load(open('research/changelog/CHANGELOG_CANONICAL.json', encoding='utf-8'))
    return d['_meta']['total_entries'] == 669, f"canonical: {d['_meta']['total_entries']} entries"
check('canonical_dataset', c8)

print(f'\nV0.4.2 VALIDATION: {PASS}/{PASS+FAIL} PASS, {FAIL} FAIL')
sys.exit(0 if FAIL == 0 else 1)
