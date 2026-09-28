#!/usr/bin/env python
"""Clean duplicate GAP-011 and fix GAP-001 in GAP_REGISTER.json"""
import json

path = 'research/v05/validation/GAP_REGISTER.json'

with open(path, encoding='utf-8') as f:
    data = json.load(f)

# Remove duplicate GAP-011 (keep only the first occurrence)
seen_ids = set()
unique_gaps = []
for gap in data['gaps']:
    if gap['id'] in seen_ids:
        print(f"REMOVING duplicate: {gap['id']}")
        continue
    seen_ids.add(gap['id'])
    unique_gaps.append(gap)

data['gaps'] = unique_gaps
data['_meta']['version'] = 'v0.7'
data['_meta']['generated'] = '2026-09-28'
data['_meta']['note'] = 'Post-V0.7 cleanup: duplicates removed, GAP-001 updated'

# Fix GAP-001: no longer blocked by "need to locate z5"
for gap in data['gaps']:
    if gap['id'] == 'GAP-001':
        gap['blocking_dependency'] = None  # z5 already found
        gap['next_verification_method'] = 'N/A — z5 reconstructed. Use GAP-011 for remaining EXP threshold research.'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print(f"\nCLEANED: {len(data['gaps'])} unique gaps")
for g in data['gaps']:
    print(f"  {g['id']}: {g['status']}")
