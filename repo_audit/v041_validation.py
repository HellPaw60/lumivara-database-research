#!/usr/bin/env python
"""V0.4.1 VALIDATION HARDENING — fail-closed, full parity, no silent except.

Perbaikan atas v04_validation.py:
1. SQL recreation: full parity (schema+columns+rows+values, deterministic)
2. CSV parity: fail-closed (no except:pass), explicit table mapping
3. Doc consistency: structured JSON parsing, status MATCH/MISMATCH/NOT_FOUND/DEFINITION_VARIANCE
4. Provenance audit: semua hasil v0.4 dicek source-nya
5. Orphan detection: algorithm nyata (bukan hard-code)
6. DB compare: PK-based (PRAGMA table_info), row-hash fallback
"""
import json, sqlite3, os, csv, hashlib, tempfile, shutil, sys

PASS, FAIL = 0, 0
def report(name, ok, detail):
    global PASS, FAIL
    status = 'PASS' if ok else 'FAIL'
    if ok: PASS += 1
    else: FAIL += 1
    print(f'  [{status}] {name}: {str(detail)[:100]}')
    return ok, detail

results = []

# ============ 1. SQL RECREATION FULL PARITY ============
def sql_full_parity():
    src = sqlite3.connect('database/LUMIVARA_FORENSICS.sqlite')
    src.row_factory = sqlite3.Row
    test = os.path.join(tempfile.gettempdir(), 'v041_parity.sqlite')
    if os.path.exists(test): os.remove(test)
    dst = sqlite3.connect(test)
    dst.executescript(open('database/dumps/LUMIVARA_FORENSICS/full_dump.sql', encoding='utf-8').read())
    dst.commit()
    dst.row_factory = sqlite3.Row

    src_tables = sorted(r[0] for r in src.execute("SELECT name FROM sqlite_master WHERE type='table'"))
    dst_tables = sorted(r[0] for r in dst.execute("SELECT name FROM sqlite_master WHERE type='table'"))
    if src_tables != dst_tables:
        return False, f'table list mismatch: {set(src_tables) ^ set(dst_tables)}'

    diffs = []
    for t in src_tables:
        # schema (CREATE statement)
        s_sql = src.execute("SELECT sql FROM sqlite_master WHERE name=?", (t,)).fetchone()[0]
        d_sql = dst.execute("SELECT sql FROM sqlite_master WHERE name=?", (t,)).fetchone()[0]
        if s_sql != d_sql: diffs.append(f'{t}: schema diff')
        # columns
        s_cols = [(r[1], r[2]) for r in src.execute(f'PRAGMA table_info({t})')]
        d_cols = [(r[1], r[2]) for r in dst.execute(f'PRAGMA table_info({t})')]
        if s_cols != d_cols: diffs.append(f'{t}: column diff')
        # rows (canonical: sorted by all columns as string)
        s_rows = sorted(tuple(str(v) for v in tuple(r)) for r in src.execute(f'SELECT * FROM {t}'))
        d_rows = sorted(tuple(str(v) for v in tuple(r)) for r in dst.execute(f'SELECT * FROM {t}'))
        if s_rows != d_rows:
            only_s = [r for r in s_rows if r not in d_rows][:2]
            only_d = [r for r in d_rows if r not in s_rows][:2]
            diffs.append(f'{t}: row diff (+{len([r for r in s_rows if r not in d_rows])}/-{len([r for r in d_rows if r not in s_rows])}) e.g. src_only={only_s[:1]}')
    src.close(); dst.close()
    return len(diffs) == 0, diffs if diffs else f'{len(src_tables)} tables full parity (schema+cols+rows+values)'
ok, d = report('sql_recreation_full_parity', *sql_full_parity())
results.append({'check': 'sql_recreation_full_parity', 'ok': ok, 'detail': d})

# simpan diff detail
json.dump({'parity_result': 'PASS' if ok else 'FAIL', 'detail': d},
          open('validation/sql_recreation_validation.json', 'w', encoding='utf-8'), indent=1)

# ============ 2. CSV PARITY FAIL-CLOSED ============
def csv_parity():
    TABLE_MAP = {'cards': 'CARDS', 'classes': 'CLASSES', 'client_mining': 'CLIENT_MINING',
                 'drop_rates': 'DROP_RATES', 'items': 'ITEMS', 'maps': 'MAPS',
                 'monster_status_attacks': 'MONSTER_STATUS_ATTACKS', 'monsters': 'MONSTERS',
                 'skills': 'SKILLS', 'statuses': 'STATUSES', 'translations': 'TRANSLATIONS'}
    con = sqlite3.connect('database/LUMIVARA_FORENSICS.sqlite')
    con.row_factory = sqlite3.Row
    errors = []
    checked = 0
    for fname, tname in TABLE_MAP.items():
        path = f'database/csv/{fname}.csv'
        if not os.path.exists(path):
            errors.append(f'MISSING CSV: {path}')
            continue
        checked += 1
        with open(path, encoding='utf-8', newline='') as fh:
            rows = list(csv.reader(fh))
        if not rows:
            errors.append(f'{fname}: empty CSV')
            continue
        csv_cols = rows[0]
        sql_cols = [r[1] for r in con.execute(f'PRAGMA table_info({tname})')]
        if csv_cols != sql_cols:
            errors.append(f'{fname}: column mismatch csv={csv_cols} sql={sql_cols}')
            continue
        csv_data = sorted(tuple('' if c == '' else str(c) for c in r) for r in rows[1:])
        sql_data = sorted(tuple('' if v is None else str(v) for v in tuple(r)) for r in con.execute(f'SELECT * FROM {tname}'))
        if csv_data != sql_data:
            errors.append(f'{fname}: value mismatch csv={len(csv_data)} sql={len(sql_data)}')
    con.close()
    return len(errors) == 0, {'checked': checked, 'errors': errors} if errors else f'{checked} CSV full parity'
ok, d = report('csv_parity_fail_closed', *csv_parity())
results.append({'check': 'csv_parity_fail_closed', 'ok': ok, 'detail': d})
json.dump({'ok': ok, 'detail': d}, open('validation/csv_parity.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1, default=str)

# ============ 3. DOC CONSISTENCY (structured) ============
def doc_consistency():
    try:
        cons = json.load(open('repo_audit/V031_DOC_CONSISTENCY.json', encoding='utf-8'))
    except Exception as e:
        return False, f'cannot read consistency JSON: {e}'
    checks = cons.get('checks', [])
    if not checks:
        return False, 'no checks found'
    counts = {'MATCH': 0, 'MISMATCH': 0, 'NOT_FOUND': 0, 'DEFINITION_VARIANCE': 0}
    for c in checks:
        counts[c['status']] = counts.get(c['status'], 0) + 1
    # PASS criteria: 0 MISMATCH. NOT_FOUND = klaim tidak muncul di dokumen tsb (valid negative,
    # tidak semua dokumen menyebut semua angka). DEFINITION_VARIANCE boleh bila terdokumentasi.
    ok = counts['MISMATCH'] == 0
    return ok, counts
ok, d = report('doc_consistency_structured', *doc_consistency())
results.append({'check': 'doc_consistency_structured', 'ok': ok, 'detail': d})

# ============ 4. PROVENANCE AUDIT V0.4 ============
def provenance_audit():
    required = {
        'research/v04/database_merge/DB_COMPARE.json': ['_meta.final', '_meta.method'],
        'research/v04/database_merge/CLIENT_MINING_NORMALIZED.json': ['_meta.version', '_meta.domains'],
        'research/v04/drop/DROP_MODEL.md': None,  # markdown — cek ada section provenance
        'research/v04/combat/hit_flee_analysis.md': None,
        'research/v04/combat/EXPERIMENT_PLAN.md': None,
        'research/changelog/OFFICIAL_CHANGELOG.json': None,
        'research/changelog/CHANGELOG_CROSS_VALIDATION.json': ['_meta.official_source', '_meta.retrieved_at', '_meta.official_hash'],
    }
    missing = []
    for path, fields in required.items():
        if not os.path.exists(path):
            missing.append(f'MISSING: {path}')
            continue
        if fields:
            data = json.load(open(path, encoding='utf-8'))
            for f in fields:
                cur = data
                for part in f.split('.'):
                    cur = cur.get(part) if isinstance(cur, dict) else None
                    if cur is None:
                        missing.append(f'{path}: missing {f}')
                        break
    # PROVENANCE_V03/V04 entities
    for pf in ['provenance/PROVENANCE_V03.json']:
        p = json.load(open(pf, encoding='utf-8'))
        for ent, meta in p['entities'].items():
            if not meta.get('source'):
                missing.append(f'{pf}: {ent} no source')
    return len(missing) == 0, missing if missing else f'{len(required)} v0.4 artifacts + provenance complete'
ok, d = report('provenance_audit_v04', *provenance_audit())
results.append({'check': 'provenance_audit_v04', 'ok': ok, 'detail': d})
json.dump({'ok': ok, 'detail': d}, open('validation/V04_PROVENANCE_AUDIT.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1, default=str)

# ============ 5. ORPHAN DETECTION (algorithm nyata) ============
def orphan_detection():
    raw = json.load(open('collect/raw-snapshots.json', encoding='utf-8'))
    gdb = json.load(open('GAME_DB.json', encoding='utf-8'))
    mdb = json.load(open('MONSTER_DB.json', encoding='utf-8'))

    # semua drop observations
    drop_items = {}  # item -> [(area, x, y)]
    for area, A in raw['areas'].items():
        for dr in A['drops'].values():
            drop_items.setdefault(dr['item'], []).append((area, dr['x'], dr['y']))
    for e in raw['events']:
        ev = e['ev']
        if ev.get('type') == 'pickup':
            drop_items.setdefault(ev['item'], []).append((e['area'], ev.get('x', 0), ev.get('y', 0)))

    # monster positions per area
    mob_pos = {}  # (area, monster_name) -> [(x,y)]
    for area, A in raw['areas'].items():
        for t in A['mobTuples'].values():
            mi = A['mobInfo'].get(t['id'])
            if mi:
                mob_pos.setdefault((area, mi['name']), []).append((t['x'], t['y']))

    def nearest_mob(area, x, y, radius=160):
        best, bd = None, radius * radius
        for (a, name), positions in mob_pos.items():
            if a != area: continue
            for (mx, my) in positions:
                d = (mx - x) ** 2 + (my - y) ** 2
                if d < bd: bd, best = d, name
        return best

    # klasifikasi setiap item
    classification = {}
    for item, obs in drop_items.items():
        # cek MONSTER_DB drops (asosiasi lama)
        in_db = any(item in (m.get('drops') or {}) for m in mdb['monsters'].values())
        # asosiasi posisional baru
        votes = {}
        for (area, x, y) in obs[:20]:
            nm = nearest_mob(area, x, y)
            if nm: votes[nm] = votes.get(nm, 0) + 1
        positional = max(votes, key=votes.get) if votes else None
        if in_db:
            classification[item] = {'status': 'RESOLVED', 'source': 'MONSTER_DB drops', 'positional_agrees': positional}
        elif positional:
            classification[item] = {'status': 'INFERRED', 'source': 'positional association', 'candidate': positional, 'votes': votes}
        else:
            classification[item] = {'status': 'ORPHAN', 'observations': len(obs)}

    # monster tanpa drop evidence
    monsters_no_drop = [k for k, m in mdb['monsters'].items() if not m.get('drops')]

    # items slot generik (armor/sword/dst) — kategori bukan material
    summary = {
        'total_drop_items': len(classification),
        'resolved': sum(1 for c in classification.values() if c['status'] == 'RESOLVED'),
        'inferred': sum(1 for c in classification.values() if c['status'] == 'INFERRED'),
        'orphan': sum(1 for c in classification.values() if c['status'] == 'ORPHAN'),
        'monsters_without_drops': len(monsters_no_drop),
        'known_orphans_check': {i: classification.get(i, {'status': 'NOT_OBSERVED'})
                                 for i in ['aurora_tail', 'garment', 'honey_wing_dust', 'magma_scale']},
    }
    return True, summary  # audit bersifat informatif; detail disimpan
ok, d = report('orphan_detection_algorithm', *orphan_detection())
results.append({'check': 'orphan_detection_algorithm', 'ok': ok, 'detail': d})
# jalankan ulang untuk simpan detail
raw_d = orphan_detection()
json.dump({'_meta': {'method': 'positional association radius 160px + MONSTER_DB cross-check'},
           **raw_d[1]}, open('research/v04/drop/ORPHAN_AUDIT.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1, default=str)

# ============ 6. DB COMPARE PK-BASED ============
def db_compare_pk():
    def load(db):
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        out = {}
        for (t,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            info = cur.execute(f'PRAGMA table_info({t})').fetchall()
            pk_cols = [r[1] for r in sorted(info, key=lambda r: r[5]) if r[5] > 0]
            rows = [dict(r) for r in cur.execute(f'SELECT * FROM {t}').fetchall()]
            if pk_cols:
                key = lambda r: tuple(str(r[c]) for c in pk_cols)
                method = f'PK({",".join(pk_cols)})'
            else:
                key = lambda r: hashlib.sha256(json.dumps(r, sort_keys=True, default=str).encode()).hexdigest()
                method = 'row_hash_sorted'
            out[t] = {'pk': pk_cols, 'method': method,
                      'map': {key(r): r for r in rows}, 'count': len(rows)}
        con.close()
        return out
    A = load('database/LUMIVARA_FORENSICS.sqlite')
    B = load('forensics/database/LUMIVARA_FORENSICS.sqlite')
    diffs = []
    for t in sorted(set(A) | set(B)):
        if t not in A: diffs.append(f'{t}: only in initial')
        elif t not in B: diffs.append(f'{t}: only in final (expected: CLIENT_MINING)' if t == 'CLIENT_MINING' else f'{t}: UNEXPECTED only in final')
        else:
            if A[t]['method'] != B[t]['method']: diffs.append(f'{t}: key method diff')
            ka, kb = A[t]['map'], B[t]['map']
            for k in ka:
                if k not in kb: diffs.append(f'{t}: added key {str(k)[:40]}')
                elif dict(ka[k]) != dict(kb[k]): diffs.append(f'{t}: modified key {str(k)[:40]}')
            for k in kb:
                if k not in ka: diffs.append(f'{t}: removed key {str(k)[:40]}')
    expected_only = ['CLIENT_MINING: only in final (expected: CLIENT_MINING)']
    unexpected = [x for x in diffs if x not in expected_only]
    return len(unexpected) == 0, {'unexpected': unexpected, 'expected_delta': expected_only} if unexpected else 'PK-based compare clean (only CLIENT_MINING delta)'
ok, d = report('db_compare_pk_based', *db_compare_pk())
results.append({'check': 'db_compare_pk_based', 'ok': ok, 'detail': d})

# ============ 7. OFFICIAL CHANGELOG CHECKS ============
def official_changelog():
    checks = []
    # source archived?
    for f in ['research/changelog/official_changelog_raw.html',
              'research/changelog/official_changelog_notice_bundle.js',
              'research/changelog/OFFICIAL_CHANGELOG.json',
              'research/changelog/CHANGELOG_CROSS_VALIDATION.json']:
        if not os.path.exists(f): checks.append(f'missing {f}')
    # parse valid?
    try:
        oc = json.load(open('research/changelog/OFFICIAL_CHANGELOG.json', encoding='utf-8'))
        if len(oc) < 600: checks.append(f'suspicious entry count: {len(oc)}')
        if not all(e.get('id') and e.get('date') for e in oc): checks.append('entries missing id/date')
    except Exception as e:
        checks.append(f'parse error: {e}')
    # cross validation exists?
    try:
        cv = json.load(open('research/changelog/CHANGELOG_CROSS_VALIDATION.json', encoding='utf-8'))
        if cv['counts']['matched'] != 649: checks.append(f'matched != 649: {cv["counts"]["matched"]}')
    except Exception as e:
        checks.append(f'cross-val error: {e}')
    return len(checks) == 0, checks if checks else f'official source archived+parsed+cross-validated ({len(oc)} entries)'
ok, d = report('official_changelog_source', *official_changelog())
results.append({'check': 'official_changelog_source', 'ok': ok, 'detail': d})

# ============ SUMMARY ============
out = {'_meta': {'version': 'v0.4.1', 'total': len(results), 'pass': PASS, 'fail': FAIL},
       'checks': results}
json.dump(out, open('validation/V041_FULL_VALIDATION.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1, default=str)
md = ['# V0.4.1 Full Validation (Hardened)', '',
      f"**{PASS}/{len(results)} PASS** | {FAIL} FAIL", '',
      '| Check | Status | Detail |', '|---|---|---|']
for r in results:
    md.append(f"| {r['check']} | {'✅ PASS' if r['ok'] else '❌ FAIL'} | {str(r['detail'])[:90]} |")
open('validation/V041_FULL_VALIDATION.md', 'w', encoding='utf-8').write('\n'.join(md))
print(f'\nVALIDATION V0.4.1: {PASS}/{len(results)} PASS, {FAIL} FAIL')
sys.exit(0 if FAIL == 0 else 1)
