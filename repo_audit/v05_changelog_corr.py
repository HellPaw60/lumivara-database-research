#!/usr/bin/env python
"""Phase 12 v0.5: changelog → mechanics correlation index.
Raw text dipertahankan as-is; interpretasi EN/ID terpisah."""
import json, re

canon = json.load(open('research/changelog/CHANGELOG_CANONICAL.json', encoding='utf-8'))['entries']
tr = json.load(open('TRANSLATIONS.json', encoding='utf-8'))

# kamus terjemahan untuk judul umum (dari TRANSLATIONS bila ada, else heuristic ID/EN)
def translate(text):
    # cek kamus persis
    if text in tr:
        return tr[text]
    return None

# klasifikasi mechanic berdasarkan keyword di id+title (raw Thai tetap raw)
MECH_KEYS = [
    (r'crit|คริ', 'CRIT_SYSTEM'),
    (r'aspd|ASPD|ความเร็วโจมตี', 'ASPD'),
    (r'exp|EXP|เวล|ประสบการณ์', 'EXP_PROGRESSION'),
    (r'drop|ดรอป|ลดโอกาส|เพิ่มโอกาส', 'DROP_SYSTEM'),
    (r'damage|ดาเมจ|แรงขึ้น|เบาลง', 'DAMAGE'),
    (r'skill|สกิล', 'SKILL_MECHANICS'),
    (r'refine|ตีบวก', 'REFINE'),
    (r'fusion|หลอมรวม', 'FUSION'),
    (r'card|การ์ด', 'CARD_SYSTEM'),
    (r'monster|มอน|บอส|boss', 'MONSTER'),
    (r'party|ปาร์ตี้', 'PARTY'),
    (r'guild|กิล', 'GUILD'),
    (r'silver|โกลด์|gold|เงิน|ราคา|ซื้อ|ขาย', 'ECONOMY'),
    (r'pvp|ดวล|arena|สนาม', 'PVP'),
    (r'pet|สัตว์เลี้ยง', 'PET'),
    (r'stun|freeze|poison|สตัน|แข็ง|พิษ', 'STATUS'),
    (r'hit|flee|หลบ|miss', 'HIT_FLEE'),
    (r'arrow|ลูกธนู', 'AMMO'),
    (r'class|อาชีพ|kensei|nekobaku|mamushi|thief|merchant|cleric|sword|mage|archer', 'CLASS'),
    (r'equipment|อุปกรณ์|gear|เกราะ|อาวุธ', 'EQUIPMENT'),
]

correlations = []
for e in canon:
    blob = (e['id'] + ' ' + e['title']).lower()
    mechs = []
    for pat, mech in MECH_KEYS:
        if re.search(pat, blob, re.I):
            mechs.append(mech)
    if not mechs:
        mechs = ['UI_ONLY']
    # entri mechanics-relevant (bukan murni UI)
    is_mechanic = 'UI_ONLY' not in mechs
    correlations.append({
        'id': e['id'],
        'raw_title': e['title'],          # RAW - as-is
        'raw_lines': e['lines'],          # RAW - as-is
        'date': e['date'],
        'mechanics': mechs,
        'is_mechanic_relevant': is_mechanic,
        'confidence': 'DERIVED (keyword classification)',
    })

from collections import Counter
mech_counts = Counter(m for c in correlations for m in c['mechanics'])
print('=== MECHANICS DISTRIBUTION (669 canonical entries) ===')
for m, cnt in mech_counts.most_common(20):
    print(f'  {m}: {cnt}')

# simpan
out = {
    '_meta': {
        'source': 'CHANGELOG_CANONICAL.json (669 entries)',
        'method': 'keyword classification on id+title (raw Thai preserved as-is)',
        'note': 'raw_title/raw_lines = RAW SOURCE (Thai, unmodified). mechanics = DERIVED classification.',
    },
    'mechanics_distribution': dict(mech_counts),
    'correlations': correlations,
}
json.dump(out, open('research/v05/changelog/CHANGELOG_MECHANICS_INDEX.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# entri mechanics-relevant dengan dampak terbesar (multi-mechanic)
big = [c for c in correlations if len(c['mechanics']) >= 3 and c['is_mechanic_relevant']]
print(f'\n=== ENTRI MULTI-MECHANIC (>=3): {len(big)} ===')
for c in big[:10]:
    print(f"  {c['id']}: {c['mechanics']}")
    print(f"    raw: {c['raw_title'][:80]}")
