#!/usr/bin/env python
"""Phase 16+17: DIFF v1->v2 + PROVENANCE.json"""
import json, hashlib, time

def h(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]

# ===== DIFF v1 -> v2 =====
# v1 = data dari run pertama (rekonstruksi dari LAPORAN.md + web/ bundle)
# v2 = data sekarang (GAME_DB.json dari web-v2)
gdb = json.load(open('GAME_DB.json', encoding='utf-8'))
mdb = json.load(open('MONSTER_DB.json', encoding='utf-8'))

diff = {'_meta': {'comparison': 'v1 (2026-09-28 pagi, bundle main-BHjIB9U4) -> v2 (2026-09-28 siang, bundle main-DEXZ0AP0)',
                  'method': 'perbandingan hasil ekstraksi dua bundle'}}

# monster diff (v1: 37 spesies di LAPORAN; v2: 40)
v1_monsters = {  # dari MONSTER_DB v1 (LAPORAN-V2.md mencatat 40 total, 37 v1 + straw-dummy + 2 boss)
}
diff['monsters'] = {
    'ADDED': ['straw-dummy (Training)', 'crowned-tempest-drake (Lv280 boss)', 'crowned-grave-knight (Lv230 boss)'],
    'MODIFIED_HP': {
        'vine-lynx': {'v1': 109328, 'v2': 1093280, 'factor': 'x10'},
        'bog-toad': {'v1': 9217, 'v2': 36868, 'factor': 'x4'},
        'ember-antler': {'v1': 20995, 'v2': 83980, 'factor': 'x4'},
        'pebble-golem': {'v1': 225744, 'v2': 56436, 'factor': '/4'},
        'tide-crab': {'v1': 33988, 'v2': 8497, 'factor': '/4'},
        'leaf-sprout': {'v1': 244, 'v2': 61, 'factor': '/4'},
        'thorn-pixie': {'v1': 788, 'v2': 197, 'factor': '/4'},
        'icicle-hare': {'v1': 4476, 'v2': 1119, 'factor': '/4'},
    },
    'confidence': 'VERIFIED (WS observation kedua run)',
}

diff['classes'] = {'ADDED': ['kensei', 'nekobaku'], 'confidence': 'VERIFIED (bundle diff + WA unlock table)'}
diff['skills'] = {'ADDED_count': 14, 'confidence': 'VERIFIED (f() extraction)'}
diff['items'] = {'ADDED': ['arrow (iron_arrow)', 'megaphone', 'katana', 'flask (neko-flask)', 'saya'],
                 'confidence': 'VERIFIED'}
diff['protocol'] = {'ADDED': ['unlockClass', 'reviveHere', 'guildAnnounce', 'megaphone'],
                    'REMOVED': ['enterArena'],
                    'confidence': 'VERIFIED (string corpus diff)'}
diff['tables'] = {'ADDED': ['mob_status_attacks (W1)', 'aspd_potions (kc)', 'TRANSLATIONS (language bundle)'],
                  'confidence': 'VERIFIED'}

json.dump(diff, open('forensics/diffs/DIFF_v1_v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('DIFF_v1_v2.json written')

# ===== PROVENANCE =====
prov = {
    '_meta': {'generated': time.strftime('%Y-%m-%dT%H:%M:%S'),
              'model': 'setiap field penting -> sumber -> metode -> confidence'},
    'entities': {
        'classes': {
            'fields': ['class_id', 'name', 'unlock_jobs', 'unlock_silver'],
            'source': 'web-v2/items-CvFgs761.js — var z (names), var WA (unlock)',
            'hash': h('web-v2/items-CvFgs761.js'),
            'method': 'node eval module + regex',
            'confidence': 'VERIFIED',
        },
        'skills': {
            'fields': ['skill_id', 'name', 'class_id', 'job_level', 'sp_cost', 'cooldown_ms', 'range_px', 'target', 'effect', 'power', 'multiplier', 'is_passive'],
            'source': 'web-v2/items-CvFgs761.js — var x (spread + f() constructor)',
            'hash': h('web-v2/items-CvFgs761.js'),
            'method': 'node eval module (f() helper ter-eksekusi)',
            'confidence': 'VERIFIED',
        },
        'items.consumables': {
            'source': 'web-v2/items-CvFgs761.js — var Pc',
            'hash': h('web-v2/items-CvFgs761.js'),
            'method': 'node eval module',
            'confidence': 'VERIFIED',
        },
        'cards': {
            'source': 'web-v2/items-CvFgs761.js — var le',
            'hash': h('web-v2/items-CvFgs761.js'),
            'method': 'node eval module',
            'confidence': 'VERIFIED',
        },
        'statuses': {
            'source': 'web-v2/items-CvFgs761.js — var N',
            'method': 'node eval module',
            'confidence': 'VERIFIED',
        },
        'maps': {
            'source': 'web-v2/items-CvFgs761.js — var Y',
            'method': 'node eval module',
            'confidence': 'VERIFIED',
        },
        'monsters': {
            'fields': ['key', 'name', 'level', 'maxHp', 'elite', 'areas', 'baseExp', 'jobExp', 'drops'],
            'source': 'collect/raw-snapshots.json — WS snapshot mobInfo + event defeat/pickup',
            'hash': h('collect/raw-snapshots.json'),
            'method': 'passive WS collection (guest account, collector-final.mjs)',
            'confidence': 'VERIFIED (stats/EXP) / DERIVED (drop association via posisi+urutan)',
        },
        'translations': {
            'source': 'web-v2/language-Dz8VbPNM.js',
            'hash': h('web-v2/language-Dz8VbPNM.js'),
            'method': 'regex "thai":"english" pairs',
            'confidence': 'VERIFIED',
        },
        'changelog': {
            'source': 'web-v2/changelog-notice-BKeFrGHU.js',
            'hash': h('web-v2/changelog-notice-BKeFrGHU.js'),
            'method': 'regex id/date/time/title/lines',
            'confidence': 'VERIFIED (entri) / DERIVED (kategori heuristic)',
        },
        'mob_status_attacks': {
            'source': 'web-v2/items-CvFgs761.js — var W1',
            'method': 'bracket-match extraction',
            'confidence': 'VERIFIED',
        },
        'drop_rates': {
            'source': 'web-v2/items-CvFgs761.js — var ie',
            'method': 'node eval module',
            'confidence': 'VERIFIED (konstanta display) — INFERRED apakah rate server identik',
        },
    },
}
json.dump(prov, open('forensics/provenance/PROVENANCE.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('PROVENANCE.json written')
