#!/usr/bin/env python
"""Phase 0: inventory manifest — semua file workspace dengan hash & provenance"""
import os, hashlib, json, time

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

manifest = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', 'forensics')]
    for fn in files:
        fp = os.path.join(root, fn)
        p = fp.replace(os.sep, '/')
        try:
            sz = os.path.getsize(fp)
            mime = 'binary'
            if fn.endswith(('.js', '.mjs', '.json', '.md', '.txt', '.html', '.css', '.py')):
                mime = 'text/' + fn.rsplit('.', 1)[-1]
            if '/web/' in p or p.startswith('web/'):
                src = 'extraction-v1'
            elif 'web-v2' in p:
                src = 'extraction-v2'
            elif 'collect/' in p:
                src = 'collector'
            elif p.startswith(('app/', 'nsis-out/', 'asar-out/')):
                src = 'electron-extract'
            elif fn in ('GAME_DB.json', 'MONSTER_DB.json', 'DROP_DB.json', 'TRANSLATIONS.json'):
                src = 'database'
            elif fn.endswith('.md'):
                src = 'doc'
            else:
                src = 'misc'
            manifest.append({
                'path': p, 'size': sz,
                'sha256': sha256(fp) if sz < 50_000_000 else 'SKIPPED_LARGE',
                'mime': mime, 'source': src,
            })
        except Exception as e:
            manifest.append({'path': p, 'error': str(e)})

out = {'_meta': {'generated': time.strftime('%Y-%m-%dT%H:%M:%S'),
                 'workspace': 'D:/lumivara-re', 'file_count': len(manifest)},
       'files': manifest}
json.dump(out, open('forensics/inventory_manifest.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'manifest: {len(manifest)} files')
from collections import Counter
for k, v in Counter(m.get('source') for m in manifest).items():
    print(f'  {k}: {v}')
