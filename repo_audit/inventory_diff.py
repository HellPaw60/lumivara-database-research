#!/usr/bin/env python
"""Phase 1-3: local vs remote inventory + SHA diff"""
import subprocess, os, json, hashlib

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

# local inventory (git tracked + untracked + ignored)
tracked = set(subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.splitlines())
ignored = set()
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git',)]
    for fn in files:
        fp = os.path.join(root, fn).replace(os.sep, '/')
        if fp not in tracked:
            # cek ignored
            r = subprocess.run(['git', 'check-ignore', fp], capture_output=True, text=True)
            if r.returncode == 0:
                ignored.add(fp)

# remote inventory (git tree main)
remote = {}
out = subprocess.run(['git', 'ls-tree', '-r', '-l', 'origin/main'], capture_output=True, text=True).stdout
for line in out.splitlines():
    meta, path = line.split('\t', 1)
    parts = meta.split()
    sha = parts[2]
    size = int(parts[3].strip('-')) if len(parts) > 3 and parts[3] != '-' else 0
    remote[path] = {'git_sha': sha, 'size': size}

local = {}
for p in tracked:
    if os.path.exists(p):
        local[p] = {'size': os.path.getsize(p), 'sha256': sha256(p)}

# diff
diff = {'LOCAL_ONLY': [], 'REMOTE_ONLY': [], 'BOTH_IDENTICAL': [], 'CONTENT_DIFF': []}
for p in sorted(set(local) | set(remote)):
    if p in local and p in remote:
        if local[p]['size'] == remote[p]['size']:
            diff['BOTH_IDENTICAL'].append(p)
        else:
            diff['CONTENT_DIFF'].append({'path': p, 'local_size': local[p]['size'], 'remote_size': remote[p]['size']})
    elif p in local:
        diff['LOCAL_ONLY'].append(p)
    else:
        diff['REMOTE_ONLY'].append(p)

inv = {
    '_meta': {'local_tracked': len(tracked), 'local_ignored': len(ignored), 'remote_files': len(remote)},
    'local': {p: {'size': v['size'], 'sha256': v['sha256']} for p, v in local.items()},
    'remote': remote,
    'ignored': sorted(ignored),
}
json.dump(inv, open('repo_audit/local_inventory.json', 'w', encoding='utf-8'), indent=1)
json.dump(diff, open('repo_audit/LOCAL_REMOTE_DIFF.json', 'w', encoding='utf-8'), indent=1)

print(f"local tracked: {len(tracked)} | ignored: {len(ignored)} | remote: {len(remote)}")
print(f"IDENTICAL: {len(diff['BOTH_IDENTICAL'])} | LOCAL_ONLY: {len(diff['LOCAL_ONLY'])} | REMOTE_ONLY: {len(diff['REMOTE_ONLY'])} | CONTENT_DIFF: {len(diff['CONTENT_DIFF'])}")
for c in diff['CONTENT_DIFF'][:10]:
    print('  DIFF:', c)
for p in diff['LOCAL_ONLY'][:10]:
    print('  LOCAL_ONLY:', p)
for p in diff['REMOTE_ONLY'][:10]:
    print('  REMOTE_ONLY:', p)
