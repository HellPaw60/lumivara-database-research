#!/usr/bin/env python
"""Agregator v2: raw-snapshots.json -> MONSTER_DB.json (stats+EXP+drops)"""
import json
from collections import defaultdict

RAW = 'D:/lumivara-re/collect/raw-snapshots.json'
raw = json.load(open(RAW, encoding='utf-8'))

monsters = {}          # key -> stat
exp_by_name = defaultdict(list)     # name -> [baseExp...]
drops_by_area = defaultdict(lambda: defaultdict(int))
mob_item = defaultdict(lambda: defaultdict(int))  # (area, mobname) -> item -> count

# 1. stats dari mobInfo
for area, A in raw['areas'].items():
    for mi in A['mobInfo'].values():
        k = mi['key']
        e = monsters.setdefault(k, {'name': mi['name'], 'level': mi.get('level'),
                                    'maxHp': 0, 'elite': False, 'areas': set(), 'baseExp': None, 'jobExp': None, 'guildExp': None, 'drops': defaultdict(int)})
        e['maxHp'] = max(e['maxHp'], mi.get('maxHp') or 0)
        e['elite'] = e['elite'] or bool(mi.get('elite'))
        e['areas'].add(area)

# 2. EXP + drops dari events
for rec in raw.get('events', []):
    ev = rec.get('ev', {})
    area = rec.get('area', 'unknown')
    t = ev.get('type')
    if t == 'defeat':
        nm = ev.get('name')
        if nm:
            exp_by_name[nm].append((ev.get('baseExp'), ev.get('jobExp'), ev.get('guildExp')))
    elif t == 'pickup':
        item = ev.get('item')
        if item:
            drops_by_area[area][item] += 1
            # asosiasi: mob terdekat di area pada posisi event
            best, bd = None, 9e9
            for mt in raw['areas'].get(area, {}).get('mobTuples', {}).values():
                dx, dy = mt['x'] - ev.get('x', 0), mt['y'] - ev.get('y', 0)
                d = dx*dx + dy*dy
                if d < bd: bd, best = d, mt
            if best and bd < 160*160:
                mi = raw['areas'].get(area, {}).get('mobInfo', {}).get(best['id'])
                if mi: mob_item[(area, mi['name'])][item] += 1

# 3. gabungkan
for k, e in monsters.items():
    nm = e['name']
    if nm in exp_by_name:
        rows = exp_by_name[nm]
        be = [r[0] for r in rows if r[0] is not None]
        je = [r[1] for r in rows if r[1] is not None]
        ge = [r[2] for r in rows if r[2] is not None]
        if be: e['baseExp'] = max(be)  # base tertinggi (tanpa penalty party)
        if je: e['jobExp'] = max(je)
        if ge: e['guildExp'] = max(ge)
        e['expSamples'] = len(rows)
    # drops: dari semua area tempat mob ini hidup
    for (area, mname), items in mob_item.items():
        if mname == nm:
            for it, c in items.items(): e['drops'][it] += c
    e['areas'] = sorted(e['areas'])
    e['drops'] = dict(e['drops'])

out = {'_meta': {'source': 'passive WS collection (guest), event defeat/pickup mining',
                 'note': 'maxHp=max teramati; baseExp=base tertinggi teramati (party share menurunkan); drops=observasi empiris'},
       'monsters': {k: v for k, v in sorted(monsters.items(), key=lambda x: -(x[1]['level'] or 0))}}
json.dump(out, open('D:/lumivara-re/MONSTER_DB.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# ringkasan
with_exp = sum(1 for v in monsters.values() if v['baseExp'])
with_drops = sum(1 for v in monsters.values() if v['drops'])
print(f'total: {len(monsters)} spesies | dengan EXP: {with_exp} | dengan drops: {with_drops}')
print(f"{'Lv':>4} {'Nama':<30} {'HP':>8} {'ELITE':<6} {'baseExp':>8} {'jobExp':>7} {'drops'}")
for k, v in out['monsters'].items():
    dr = ','.join(v['drops']) if v['drops'] else '-'
    print(f"{v['level']:>4} {v['name']:<30} {v['maxHp']:>8} {'★' if v['elite'] else '':<6} {str(v['baseExp'] or '-'):>8} {str(v['jobExp'] or '-'):>7} {dr[:60]}")
