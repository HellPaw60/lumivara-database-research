#!/usr/bin/env python
"""Phase 0 v0.3: FULL workspace inventory — termasuk yang ter-ignore"""
import os, json, hashlib, subprocess

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

tracked = set(subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.splitlines())

DATA_EXT = {'.sqlite', '.db', '.sqlite3', '.json', '.csv', '.sql', '.ndjson', '.txt', '.log', '.js', '.map'}
files = []
for root, dirs, fnames in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
    for fn in fnames:
        fp = os.path.join(root, fn)
        rel = fp.replace(os.sep, '/')
        ext = os.path.splitext(fn)[1].lower()
        sz = os.path.getsize(fp)
        # status git
        if rel in tracked:
            gstat = 'tracked'
        else:
            r = subprocess.run(['git', 'check-ignore', rel], capture_output=True, text=True)
            gstat = 'ignored' if r.returncode == 0 else 'untracked'
        # source group
        if rel.startswith(('app/', 'nsis-out/', 'asar-out/')):
            grp = 'electron-extract'
        elif 'web-v2' in rel:
            grp = 'bundle-v2'
        elif rel.startswith('web/'):
            grp = 'bundle-v1'
        elif 'collect/' in rel:
            grp = 'collector'
        elif rel.startswith('database/'):
            grp = 'database'
        elif rel.startswith('forensics/'):
            grp = 'forensics'
        elif rel.startswith(('repo_audit/', 'extraction/', 'protocol/', 'formulas/', 'research/', 'diffs/', 'provenance/', 'validation/', 'docs/')):
            grp = 'repo'
        elif fn.endswith('.md'):
            grp = 'doc'
        elif fn.endswith('_DB.json') or fn == 'GAME_DB.json' or fn == 'TRANSLATIONS.json':
            grp = 'database'
        else:
            grp = 'misc'
        # likely data
        likely = ext in DATA_EXT
        files.append({
            'path': rel, 'size': sz, 'sha256': sha256(fp) if sz < 60_000_000 else 'LARGE',
            'extension': ext, 'git_status': gstat, 'source_group': grp,
            'likely_data': likely,
        })

json.dump({'_meta': {'total': len(files), 'generated': '2026-09-28 v0.3 audit'},
           'files': files}, open('repo_audit/v03_full_inventory.json', 'w', encoding='utf-8'), indent=0)

# ringkasan
from collections import Counter
print(f'total files scanned: {len(files)}')
print('by git status:', dict(Counter(f['git_status'] for f in files)))
print('by group:', dict(Counter(f['source_group'] for f in files)))
print('\n=== DATABASE FILES (sqlite/db) ===')
for f in files:
    if f['extension'] in ('.sqlite', '.db', '.sqlite3'):
        print(f"  {f['size']:>10,}  {f['git_status']:<9} {f['path']}")
print('\n=== UNTRACKED DATA FILES (belum di repo) ===')
for f in files:
    if f['likely_data'] and f['git_status'] == 'untracked':
        print(f"  {f['size']:>10,}  {f['path']}")
