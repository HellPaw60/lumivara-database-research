#!/usr/bin/env python
"""Phase 10+12 v0.3: FORMULA_DATABASE_V03.json + PROVENANCE_V03.json"""
import json, hashlib, time

def h(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

formulas = {
    '_meta': {'version': 'v0.3', 'classification': ['CLIENT_CODE', 'OBSERVED_RUNTIME', 'DERIVED', 'UNKNOWN']},
    'formulas': {
        'refine_success': {
            'formula': 'failFactor(level) = min(0.3, max(0, (level-20) * 0.0025)); successRate(level, refine) = 1 - failFactor * (1 - min(100, refine)/100)',
            'class': 'CLIENT_CODE',
            'source': 'web-v2/items-CvFgs761.js — Ce={startLevel:20,perLevel:.0025,max:.3} + fungsi pc/Ic',
            'source_hash': h('web-v2/items-CvFgs761.js'),
            'note': 'Formula display klien; versi server UNKNOWN',
        },
        'refine_stat_caps': {
            'table': {'pierce': 60, 'mpierce': 60, 'atkPct': 30, 'matkPct': 30, 'lifesteal': 8,
                      'freezeHit': 15, 'resStun': 80, 'resFreeze': 80, 'moveSpeed': 30,
                      'critDmg': 60, 'stunHit': 15, 'bleedHit': 15, 'crushHit': 15, 'spDrain': 5},
            'class': 'CLIENT_CODE', 'source': 'items var ce (stat caps)',
        },
        'lifesteal_cap': {'value': 0.10, 'class': 'CLIENT_CODE', 'source': 'ga=.1 (10% maxHP per hit)'},
        'sp_drain_cap': {'value': 0.02, 'class': 'CLIENT_CODE', 'source': 'ba=.02 (2% maxSP per hit)'},
        'flee_cap': {'value': 0.20, 'class': 'CLIENT_CODE', 'source': 'Bn=.2 (20% equipment+card flee stack)'},
        'drop_rates_display': {
            'table': {'etc': 0.30, 'consumable': 0.15, 'equipment': 0.0125, 'card': 0.001,
                      'bossCard': 0.01, 'relicBox': 0.01, 'refineStone': 0.01, 'extraStat': 0.25, 'aspdAccessory': 0.30},
            'class': 'CLIENT_CODE',
            'note': 'Display klien; server UNKNOWN. Equipment 1.25% (dinnerf dari 2.5% per TRANSLATIONS)',
        },
        'party_bonus': {'value': '+2% EXP/Drop per member, max 12, ±10 level', 'class': 'CLIENT_CODE',
                        'source': 'string UI + TRANSLATIONS (2 sumber string)'},
        'crit_ratio': {'value': 'mean 3.551x', 'class': 'OBSERVED_RUNTIME',
                       'source': 'combat-analysis.json (3.282 hit events)'},
        'miss_rate': {'value': '0% pada 2.940 outgoing labeled', 'class': 'OBSERVED_RUNTIME',
                      'note': 'sample bias: mob farming level sesuai'},
        'exp_per_monster': {'class': 'OBSERVED_RUNTIME', 'source': 'event defeat baseExp/jobExp/guildExp'},
        'multi_hit': {'rule': 'damage == sum(hits[])', 'class': 'OBSERVED_RUNTIME',
                      'source': '399 event double terverifikasi'},
        'aspd_potions': {'table': {'concentration': {'level': 1, 'aspd': 3}, 'awakening': {'level': 40, 'aspd': 4}, 'berserk': {'level': 85, 'aspd': 5}},
                         'class': 'CLIENT_CODE', 'source': 'items var kc'},
        'damage_formula': {'class': 'UNKNOWN'},
        'hit_flee_formula': {'class': 'UNKNOWN'},
        'atk_def_mdef_formula': {'class': 'UNKNOWN'},
        'exp_level_table': {'class': 'UNKNOWN', 'note': 'z5 function tidak terekstrak'},
        'equipment_stat_roll': {'value': '+1-3 per stat, 75% 1 stat / 25% 2 stat', 'class': 'CLIENT_CODE',
                                'source': 'TRANSLATIONS (deskripsi item)'},
        'world_boss_stats': {'hp': 30000, 'damage': 180, 'reward': 9000, 'class': 'CLIENT_CODE',
                             'source': 'main-DEXZ0AP0.js {key:"prism-hopper",hp:3e4,damage:180,reward:9e3}'},
    },
}
json.dump(formulas, open('formulas/FORMULA_DATABASE_V03.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'FORMULA_DATABASE_V03.json: {len(formulas["formulas"])} formulas')

prov = {
    '_meta': {'version': 'v0.3', 'generated': time.strftime('%Y-%m-%dT%H:%M:%S')},
    'entities': {
        'classes': {'source': 'web-v2/items-CvFgs761.js', 'source_sha256': h('web-v2/items-CvFgs761.js'),
                    'method': 'node eval (var z + WA)', 'confidence': 'VERIFIED'},
        'skills': {'source': 'web-v2/items-CvFgs761.js', 'source_sha256': h('web-v2/items-CvFgs761.js'),
                   'method': 'node eval (var x)', 'confidence': 'VERIFIED'},
        'items': {'source': 'web-v2/items-CvFgs761.js', 'source_sha256': h('web-v2/items-CvFgs761.js'),
                  'method': 'node eval (var Pc)', 'confidence': 'VERIFIED'},
        'cards': {'source': 'web-v2/items-CvFgs761.js', 'source_sha256': h('web-v2/items-CvFgs761.js'),
                  'method': 'node eval (var le)', 'confidence': 'VERIFIED'},
        'statuses': {'source': 'web-v2/items-CvFgs761.js', 'source_sha256': h('web-v2/items-CvFgs761.js'),
                     'method': 'node eval (var N)', 'confidence': 'VERIFIED'},
        'maps': {'source': 'web-v2/items-CvFgs761.js', 'source_sha256': h('web-v2/items-CvFgs761.js'),
                 'method': 'node eval (var Y)', 'confidence': 'VERIFIED'},
        'monsters': {'source': 'collect/raw-snapshots.json', 'source_sha256': h('collect/raw-snapshots.json'),
                     'method': 'passive WS collection (collector-final.mjs)', 'confidence': 'VERIFIED stats/EXP, DERIVED drops'},
        'translations': {'source': 'web-v2/language-Dz8VbPNM.js', 'source_sha256': h('web-v2/language-Dz8VbPNM.js'),
                         'method': 'regex pairs', 'confidence': 'VERIFIED'},
        'changelog': {'source': 'web-v2/changelog-notice-BKeFrGHU.js', 'source_sha256': h('web-v2/changelog-notice-BKeFrGHU.js'),
                      'method': 'regex extraction', 'confidence': 'VERIFIED entries, DERIVED categories'},
        'network_protocol': {'source': 'collect/raw-snapshots.json', 'source_sha256': h('collect/raw-snapshots.json'),
                             'method': 'event union analysis', 'confidence': 'VERIFIED (26 event types)'},
        'combat_stats': {'source': 'collect/raw-snapshots.json', 'source_sha256': h('collect/raw-snapshots.json'),
                         'method': 'descriptive statistics', 'confidence': 'OBSERVED'},
        'sql_dump': {'source': 'database/LUMIVARA_FORENSICS.sqlite',
                     'source_sha256': h('database/LUMIVARA_FORENSICS.sqlite'),
                     'method': 'python sqlite3 iterdump-style', 'confidence': 'VERIFIED + reproducibility PASS'},
    },
}
json.dump(prov, open('provenance/PROVENANCE_V03.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('PROVENANCE_V03.json written')
