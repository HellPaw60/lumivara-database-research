#!/usr/bin/env python
"""Phase 3: LUMIVARA_FORENSICS.sqlite — master database dari semua sumber"""
import json, sqlite3, os

DB = 'forensics/database/LUMIVARA_FORENSICS.sqlite'
os.makedirs('forensics/database', exist_ok=True)
if os.path.exists(DB): os.remove(DB)
con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute('CREATE TABLE _prov (tbl TEXT, source TEXT)')

def table(name, cols, rows, provenance):
    cur.execute(f'CREATE TABLE {name} ({", ".join(cols)})')
    if rows:
        cur.executemany(f'INSERT INTO {name} VALUES ({",".join("?"*len(cols))})', rows)
    cur.execute('INSERT INTO _prov VALUES (?,?)', (name, provenance))
    print(f'  {name}: {len(rows)} rows')

# ===== GAME_DB v2 (extraction-v2) =====
gdb = json.load(open('GAME_DB.json', encoding='utf-8'))

# CLASSES
class_names = {'novice': 'Novice', 'swordman': 'Swordsman', 'mage': 'Mage', 'archer': 'Archer',
               'acolyte': 'Cleric', 'merchant': 'Merchant', 'thief': 'Thief',
               'mamushi': 'Mamushi', 'nekobaku': 'Nekobaku', 'kensei': 'Kensei'}
unlock = {'kensei': {'jobs': {'swordman': 50, 'thief': 50}, 'silver': 120000},
          'nekobaku': {'jobs': {'merchant': 50, 'mamushi': 50}, 'silver': 120000}}
table('CLASSES', ['class_id', 'name', 'unlock_jobs', 'unlock_silver', 'confidence'],
      [(k, v, json.dumps(unlock.get(k, {}).get('jobs')), unlock.get(k, {}).get('silver'), 'VERIFIED')
       for k, v in class_names.items()],
      'items-CvFgs761.js var z (names) + WA (unlock)')

# SKILLS
skills = gdb['skills']
rows = []
for sid, s in skills.items():
    rows.append((sid, s.get('name'), s.get('classId'), s.get('job'), s.get('sp'),
                 s.get('cooldown'), s.get('range'), s.get('target'), s.get('effect'),
                 s.get('power'), s.get('multiplier'), bool(s.get('passive')),
                 bool(s.get('cooldownFromAspd')), s.get('buff'),
                 'VERIFIED' if s.get('name') else 'DERIVED'))
table('SKILLS', ['skill_id', 'name', 'class_id', 'job_level', 'sp_cost', 'cooldown_ms',
                 'range_px', 'target', 'effect', 'power', 'multiplier', 'is_passive',
                 'cd_from_aspd', 'buff_id', 'confidence'], rows,
      'items-CvFgs761.js var x (skill table)')

# ITEMS (consumables)
rows = []
for iid, it in gdb['consumables'].items():
    rows.append((iid, it.get('name'), 'consumable', it.get('kind'), it.get('weight'),
                 it.get('price'), it.get('buy'), it.get('description'), 'VERIFIED'))
table('ITEMS', ['item_id', 'name', 'category', 'kind', 'weight', 'sell_price', 'buy_price', 'description', 'confidence'],
      rows, 'items-CvFgs761.js var Pc')

# CARDS
rows = []
for cid, c in gdb['cards'].items():
    rows.append((cid, c.get('name'), json.dumps(c.get('bonuses')), c.get('price'),
                 c.get('description'), 'VERIFIED'))
table('CARDS', ['card_id', 'name', 'bonuses_json', 'price', 'description', 'confidence'],
      rows, 'items-CvFgs761.js var le')

# STATUS EFFECTS
rows = []
for sid, s in gdb['status_effects'].items():
    rows.append((sid, s.get('name'), s.get('kind'), s.get('icon'), s.get('duration'),
                 json.dumps({k: v for k, v in s.items() if k not in ('id', 'name', 'kind', 'icon', 'duration', 'image')}), 'VERIFIED'))
table('STATUSES', ['status_id', 'name', 'kind', 'icon', 'duration_ms', 'params_json', 'confidence'],
      rows, 'items-CvFgs761.js var N')

# MAPS
rows = []
for mid, m in gdb['maps'].items():
    rows.append((mid, m.get('name'), m.get('subtitle'), m.get('width'), m.get('height'),
                 json.dumps(m.get('spawn')), json.dumps(m.get('portals')), 'VERIFIED'))
table('MAPS', ['map_id', 'name', 'subtitle', 'width', 'height', 'spawn_json', 'portals_json', 'confidence'],
      rows, 'items-CvFgs761.js var Y')

# MOB STATUS ATTACKS
rows = []
for mname, sa in gdb['mob_status_attacks'].items():
    rows.append((mname, sa.get('status'), sa.get('chance'), 'VERIFIED'))
table('MONSTER_STATUS_ATTACKS', ['monster_name', 'status_id', 'chance', 'confidence'],
      rows, 'items-CvFgs761.js var W1')

# DROP RATES
rows = []
for cat, rate in gdb['drop_rates'].items():
    rows.append((cat, rate, 'VERIFIED'))
table('DROP_RATES', ['category', 'rate', 'confidence'], rows, 'items-CvFgs761.js var ie')

# ===== MONSTER_DB =====
mdb = json.load(open('MONSTER_DB.json', encoding='utf-8'))
rows = []
for key, m in mdb['monsters'].items():
    rows.append((key, m['name'], m['level'], m['maxHp'], bool(m['elite']),
                 json.dumps(m['areas']), m.get('baseExp'), m.get('jobExp'), m.get('guildExp'),
                 json.dumps(m.get('drops')), m.get('expSamples'),
                 'VERIFIED' if m['maxHp'] else 'DERIVED'))
table('MONSTERS', ['monster_key', 'name', 'level', 'max_hp', 'elite', 'areas_json',
                   'base_exp', 'job_exp', 'guild_exp', 'drops_json', 'exp_samples', 'confidence'],
      rows, 'collect/raw-snapshots.json (WS observation)')

# ===== TRANSLATIONS =====
tr = json.load(open('TRANSLATIONS.json', encoding='utf-8'))
rows = [(k, v) for k, v in tr.items()]
table('TRANSLATIONS', ['thai', 'english'], rows, 'web-v2/language-Dz8VbPNM.js')

con.commit()
# integrity check
ok = cur.execute('PRAGMA integrity_check').fetchone()[0]
print(f'\nintegrity: {ok}')
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != '_prov'")]
print(f'tables ({len(tables)}): {", ".join(tables)}')
con.close()
print(f'size: {os.path.getsize(DB):,} bytes')
