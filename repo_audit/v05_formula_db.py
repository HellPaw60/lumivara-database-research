#!/usr/bin/env python
"""Phase 11 v0.5: FORMULA_DATABASE_V05.json — dari hasil mining + analisis runtime"""
import json, hashlib

def src_items():
    return {'source_type': 'CLIENT_CODE', 'source_path': 'web-v2/items-CvFgs761.js',
            'source_sha256': hashlib.sha256(open('web-v2/items-CvFgs761.js', 'rb').read()).hexdigest()[:16]}
def src_main():
    return {'source_type': 'CLIENT_CODE', 'source_path': 'web-v2/main-DEXZ0AP0.js',
            'source_sha256': hashlib.sha256(open('web-v2/main-DEXZ0AP0.js', 'rb').read()).hexdigest()[:16]}

F = {}
def add(fid, name, scope, inputs, outputs, expression, src, conf, notes=''):
    F[fid] = {'formula_id': fid, 'name': name, 'scope': scope, 'inputs': inputs,
              'outputs': outputs, 'expression': expression, **src,
              'confidence': conf, 'validation_status': 'EXTRACTED' if 'CLIENT' in conf else 'OBSERVED',
              'notes': notes}

# ===== STAT SYSTEM (semua dari De() function) =====
add('maxhp', 'Max HP', 'GLOBAL', ['level', 'VIT', 'classHP', 'equipHP', 'maxHpPct'], ['maxHp'],
    '((100 + (Lv-1)*5 + VIT*10) * (1 + classHP) + equipHP) * (1 + maxHpPct)', src_items(),
    'VERIFIED_FROM_CLIENT_CODE', 'fungsi De() offset ~118174')
add('maxsp', 'Max SP', 'GLOBAL', ['level', 'INT', 'classSP', 'equipSP', 'maxSpPct'], ['maxSp'],
    '((20 + (Lv-1) + INT*5) * (1 + classSP) + equipSP) * (1 + maxSpPct)', src_items(),
    'VERIFIED_FROM_CLIENT_CODE', 'fungsi De()')
add('atk', 'Attack', 'GLOBAL', ['baseATK', 'equipATK', 'weaponMult', 'atkPct'], ['atk'],
    '(baseATK + equipATK * weaponMult) * (1 + atkPct/100)', src_items(), 'VERIFIED_FROM_CLIENT_CODE')
add('matk', 'Magic Attack', 'GLOBAL', ['baseMATK', 'equipMATK', 'skillMatkPct', 'matkPct'], ['matk'],
    '(baseMATK + equipMATK * (1+skillMatkPct)) * (1 + matkPct/100)', src_items(), 'VERIFIED_FROM_CLIENT_CODE')
add('def', 'Defense', 'GLOBAL', ['VIT', 'equipDEF', 'skillDEF'], ['def'],
    'VIT/5 + equipDEF + skillDEF', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'DEF dikurangkan dari incoming damage (bukan outgoing)')
add('mdef', 'Magic Defense', 'GLOBAL', ['INT', 'VIT', 'equipMDEF', 'skillMDEF'], ['mdef'],
    'INT + VIT/5 + equipMDEF + skillMDEF', src_items(), 'VERIFIED_FROM_CLIENT_CODE')
add('hit', 'Hit Rate', 'GLOBAL', ['level', 'DEX', 'LUK', 'equipHIT', 'hitPct'], ['hit'],
    '(100 + Lv + DEX*2 + LUK/3 + equipHIT) * (1 + hitPct)', src_items(), 'VERIFIED_FROM_CLIENT_CODE')
add('flee', 'Flee Rate', 'GLOBAL', ['level', 'AGI', 'LUK', 'equipFLEE', 'fleePct'], ['flee'],
    '(Lv + AGI*2 + LUK/5 + equipFLEE) * (1 + fleePct)', src_items(), 'VERIFIED_FROM_CLIENT_CODE')

# ===== CRIT =====
add('crit_physical', 'Physical Crit Chance', 'GLOBAL', ['LUK', 'level', 'equipCRIT', 'skillCRIT', 'statusCRIT', 'weaponType'], ['critical'],
    'min(100, (floor(LUK/3) + (Lv-1)*0.1 + equipCRIT + skillCRIT + statusCRIT) * (isDaggerOrKnife ? 2 : 1))',
    src_items(), 'VERIFIED_FROM_CLIENT_CODE', 'dagger/knife/kunai ×2 (fungsi wi)')
add('crit_spell', 'Spell Crit Chance', 'GLOBAL', ['LUK', 'equipCRIT'], ['spellCritical'],
    'min(100, floor(LUK/3) + equipCRIT)', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'cocok changelog: crit เวท = LUK/3 + CRIT dari equipment')
add('crit_multiplier', 'Crit Damage Multiplier', 'GLOBAL', ['critDamagePct', 'equipCritDmg'], ['critMultiplier'],
    '2 * (1 + critDamagePct + equipCritDmg/100)', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'base 200%, max teoretis 3.8x dengan fatalsense+zanshin+equip')

# ===== HIT/MISS =====
add('hit_chance_p2m', 'Hit Chance Player→Mob', 'GLOBAL', ['playerHIT', 'mobFLEE'], ['hitChance'],
    'clamp(0.9 + (hit - flee) * 0.005, 0.5, 1.0)', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'fungsi qr(); mobFLEE = 100 + 2*mobLevel')
add('mob_flee', 'Mob FLEE', 'MONSTER_SPECIFIC', ['mobLevel'], ['mobFlee'],
    '100 + 2 * mobLevel', src_items(), 'VERIFIED_FROM_CLIENT_CODE', 'dari tooltip')
add('dodge_p', 'Player Dodge vs Mob', 'GLOBAL', ['flee', 'level', 'gearFlee', 'perfectDodge', 'mobHitBonus'], ['dodgeChance'],
    '(max(0, flee - level - gearFlee)*0.008 + min(0.2, gearFlee*0.008) + perfectDodge/100) / (1 + mobHitBonus), capped 0.95',
    src_items(), 'VERIFIED_FROM_CLIENT_CODE', 'fungsi _l(); dodgeCap 0.95 player / 0.87 mob')

# ===== DAMAGE =====
add('basic_damage', 'Basic Attack Damage', 'GLOBAL', ['atk', 'basicFactor', 'critMultiplier'], ['damage'],
    'round(ATK * basicFactor * (crit ? critMultiplier : 1))', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'fungsi Ml(); basicFactor = 1 + max(0, aspd-170)*0.015')
add('skill_damage', 'Skill Damage', 'GLOBAL', ['atkOrMatk', 'skillMultiplier', 'critMultiplier'], ['damage'],
    'round(ATK_or_MATK * multiplier * (crit ? critMultiplier : 1))', src_main(), 'VERIFIED_FROM_CLIENT_CODE',
    'fungsi skillStrike(); skill tidak miss by default')
add('skill_mult_scaling', 'Skill Multiplier per Level', 'SKILL_SPECIFIC', ['baseMultiplier', 'skillLevel'], ['multiplier'],
    '1 + (baseMulti - 1) * skillLevel / 10', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'level 10 = full multiplier; exceptions: hammerfall, arrowshower (linear)')
add('pierce', 'Pierce Modifier', 'GLOBAL', ['targetLevel', 'pierce'], ['damageFactor'],
    '1 - Ca(level) * (1 - clamp(pierce,0,100)/100) where Ca = min(0.3, max(0, (level-20)*0.0025))',
    src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'pierce = PERSENTASE bukan flat; efektivitas turun vs level tinggi')
add('incoming_damage', 'Mob→Player Damage', 'GLOBAL', ['mobDamage', 'shieldRefine', 'def', 'incomingFactor'], ['damage'],
    'max(1, round(mobDamage * (1 - shieldRefine/100)) - round(DEF * incomingFactor))',
    src_items(), 'VERIFIED_FROM_CLIENT_CODE', 'fungsi _l(); DEF dikurangi flat setelah shield')
add('status_dmg_mod', 'Momentum Status Modifier', 'GLOBAL', ['momentumStacks', 'perStack'], ['damageMultiplier'],
    '1 + momentumStacks * perStackValue', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'hanya basic attack, fungsi O1')

# ===== ASPD =====
add('aspd', 'Attack Speed', 'GLOBAL', ['classBase', 'weaponMod', 'shield', 'AGI', 'DEX', 'equipAspd', 'aspdPercent'], ['aspd'],
    'softcap(clamp(base + (AGI*0.3 + DEX*0.02)*r + equipAspd, 50, 193)) where r = 1-(base-144)/50; softcap: >180 half effective',
    src_items(), 'VERIFIED_FROM_CLIENT_CODE', 'base per class 145-152; weapon mod -10..+2')
add('attack_interval', 'Attack Interval', 'GLOBAL', ['aspd'], ['intervalMs'],
    'round((200 - ASPD) * 20)', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'ASPD 148=1040ms, 193=140ms')
add('basic_factor', 'Basic Attack Scaling (high ASPD)', 'GLOBAL', ['aspd'], ['basicFactor'],
    '1 + max(0, aspd - 170) * 0.015', src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'ASPD 193 = 1.345x basic damage')

# ===== STAT BOUNDS =====
add('stat_bounds', 'Stat Min/Max', 'GLOBAL', [], ['minStat', 'maxStat'],
    'min=1, max=99 (base stats)', src_items(), 'VERIFIED_FROM_CLIENT_CODE', 'fungsi W0')

# ===== OBSERVED (runtime) =====
add('crit_ratio_observed', 'Crit Ratio Observed', 'GLOBAL', [], [],
    'mean 3.551x overall; per-player 1.925-3.000 (29 paired groups)', 
    {'source_type': 'RUNTIME', 'source_path': 'collect/raw-snapshots.json'}, 'OBSERVED',
    'bukan formula — distribusi; konsisten dengan critMultiplier 2*(1+bonus)')
add('crit_roll_percast', 'Crit Roll Per Cast', 'GLOBAL', [], [],
    'crit roll sekali per cast (multi-hit mewarisi)',
    {'source_type': 'RUNTIME', 'source_path': 'collect/raw-snapshots.json'}, 'OBSERVED',
    '399/399 double-hit events uniform crits')
add('jobexp_ratio', 'Job EXP Ratio', 'GLOBAL', [], [],
    'jobExp ≈ 50% baseExp (observed pattern)',
    {'source_type': 'RUNTIME', 'source_path': 'collect/raw-snapshots.json'}, 'OBSERVED')
add('miss_outgoing_zero', 'Outgoing Miss Rate (farming)', 'GLOBAL', [], [],
    '0% pada 2940+ outgoing (farming bias)',
    {'source_type': 'RUNTIME', 'source_path': 'collect/raw-snapshots.json'}, 'OBSERVED',
    'konsisten dengan formula qr: HIT player >> mobFLEE saat farming sesuai level')

# ===== UNKNOWN =====
add('z5_exptable', 'EXP Table per Level', 'GLOBAL', [], [], 'UNKNOWN — z5 function tidak terekstrak',
    {}, 'UNKNOWN')
add('party_share', 'Party EXP Share', 'GLOBAL', [], [], 'split merata (string UI) + 2%/member — formula eksak UNKNOWN',
    {'source_type': 'UI_STRING'}, 'INFERRED')
add('element_damage', 'Element Damage Multiplier', 'GLOBAL', [], [],
    'TIDAK ADA — element hanya menentukan status effect (burn/freeze/slow)',
    src_items(), 'VERIFIED_FROM_CLIENT_CODE',
    'negative finding: tidak ditemukan elementDamage/weakness multiplier di pipeline damage')

out = {'_meta': {'version': 'v0.5', 'formula_count': len(F),
                 'confidence_legend': ['VERIFIED_FROM_CLIENT_CODE', 'OBSERVED', 'INFERRED', 'UNKNOWN'],
                 'scope_legend': ['GLOBAL', 'CLASS_SPECIFIC', 'SKILL_SPECIFIC', 'MONSTER_SPECIFIC']},
       'formulas': F}
json.dump(out, open('formulas/FORMULA_DATABASE_V05.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'FORMULA_DATABASE_V05.json: {len(F)} formulas')
from collections import Counter
print('by confidence:', dict(Counter(v['confidence'] for v in F.values())))
print('by scope:', dict(Counter(v['scope'] for v in F.values())))
