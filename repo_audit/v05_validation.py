#!/usr/bin/env python
"""V0.5 Phase 16: FULL VALIDATION — fail-closed"""
import json, os, sys, hashlib

PASS, FAIL = 0, 0
def check(name, fn):
    global PASS, FAIL
    try:
        ok, detail = fn()
        PASS += 1 if ok else 0
        FAIL += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {str(detail)[:85]}")
    except Exception as e:
        FAIL += 1
        print(f"  [FAIL] {name}: ERROR {e}")

def jc1():
    d = json.load(open('research/changelog/OFFICIAL_CHANGELOG_V3.json', encoding='utf-8'))
    return d['_meta']['entries'] == 679, f"snapshot v2: {d['_meta']['entries']} entries, bundle {d['_meta']['bundle']}"
check('official_changelog_freshness', jc1)

def jc2():
    old = json.load(open('research/changelog/CANONICAL_OFFICIAL_CHANGELOG.json', encoding='utf-8'))['entries']
    new = json.load(open('research/changelog/OFFICIAL_CHANGELOG_V3.json', encoding='utf-8'))['entries']
    old_ids = set(e['id'] for e in old); new_ids = set(e['id'] for e in new)
    delta = new_ids - old_ids
    return len(delta) == 10, f'delta: {len(delta)} new entries (expected 10)'
check('changelog_delta_processed', jc2)

def jc3():
    # raw preservation: raw titles tidak diganti
    idx = json.load(open('research/v05/changelog/CHANGELOG_MECHANICS_INDEX.json', encoding='utf-8'))
    raw_ok = all(c.get('raw_title') for c in idx['correlations'])
    # tidak ada field translated yang menimpa raw
    no_override = all('translated_title' not in c or c['raw_title'] != c.get('translated_title') for c in idx['correlations'])
    return raw_ok and no_override, f"{len(idx['correlations'])} entries, raw preserved: {raw_ok}"
check('raw_source_preservation', jc3)

def jc4():
    files = ['research/v05/combat/CRIT_ANALYSIS.md', 'research/v05/combat/hit_flee_v05.md',
             'research/v05/combat/STATUS_ANALYSIS.md', 'research/v05/progression/EXP_ANALYSIS.md',
             'research/v05/changelog/CHANGELOG_MECHANICS_INDEX.json']
    missing = [f for f in files if not os.path.exists(f)]
    return len(missing) == 0, missing if missing else f'{len(files)} v0.5 artifacts exist'
check('v05_artifacts', jc4)

def jc5():
    # formula database v05: cek schema & confidence valid
    if not os.path.exists('formulas/FORMULA_DATABASE_V05.json'):
        return False, 'FORMULA_DATABASE_V05.json not yet created'
    d = json.load(open('formulas/FORMULA_DATABASE_V05.json', encoding='utf-8'))
    valid_conf = {'VERIFIED', 'VERIFIED_FROM_CLIENT_CODE', 'OBSERVED', 'DERIVED', 'INFERRED', 'UNKNOWN'}
    bad = [k for k, v in d.get('formulas', {}).items() if v.get('confidence') not in valid_conf]
    # unsupported VERIFIED detection: VERIFIED hanya boleh dengan source
    unverified = [k for k, v in d.get('formulas', {}).items()
                  if 'VERIFIED' in v.get('confidence', '') and not v.get('source_type')]
    return len(bad) == 0 and len(unverified) == 0, f"bad={bad} unsupported_verified={unverified}" if bad or unverified else f"{len(d.get('formulas', {}))} formulas valid"
check('formula_schema_confidence', jc5)

def jc6():
    # DB integrity masih ok
    import sqlite3
    con = sqlite3.connect('database/LUMIVARA_FORENSICS.sqlite')
    r = con.execute('PRAGMA integrity_check').fetchone()[0]
    con.close()
    return r == 'ok', 'sqlite integrity ok'
check('db_integrity', jc6)

def jc7():
    # JSON validity semua file v05
    errs = []
    for root, dirs, files in os.walk('research/v05'):
        for f in files:
            if f.endswith('.json'):
                try: json.load(open(os.path.join(root, f), encoding='utf-8'))
                except Exception as e: errs.append(f'{f}: {e}')
    return len(errs) == 0, errs if errs else 'all v05 JSON valid'
check('json_validity', jc7)

print(f'\nV0.5 VALIDATION: {PASS}/{PASS+FAIL} PASS, {FAIL} FAIL')
sys.exit(0 if FAIL == 0 else 1)
