#!/usr/bin/env python
"""Phase 4-5 v0.4: CLIENT_MINING normalization -> domain model terhubung"""
import json, os

os.makedirs('research/v04/database_merge', exist_ok=True)

# baca hasil mining per domain
domains = {}
for f in os.listdir('database'):
    if f.endswith('.json') and f[0].islower():
        domains[f[:-5]] = json.load(open(f'database/{f}', encoding='utf-8'))

model = {}
def dom(name, source, symbols, observed, normalized, relations, confidence, unknowns):
    model[name] = {
        'domain': name, 'source_file': source, 'source_symbols': symbols,
        'observed_fields': observed, 'normalized_fields': normalized,
        'relations': relations, 'confidence': confidence, 'unknowns': unknowns,
    }

dom('quest', 'web-v2/main-DEXZ0AP0.js', 'questTick(), FC(), claimQuest/claimHunt/claimDaily',
    ['quest.counters{}', 'quest.claimed[]', 'questTick events (11 jenis)'],
    ['counters: map<event_id, count>', 'claimed: list<quest_id>'],
    {'MONSTERS': 'questTick kill counter → monster defeat events',
     'ITEMS': 'reward presumably item — UNKNOWN'},
    'OBSERVED_MODEL (protocol) / UNKNOWN_MODEL (rewards)',
    ['reward structure server-side', 'quest definitions server-side', 'daily reset schedule'])

dom('mall', 'web-v2/items-CvFgs761.js + main', 'Ae (starter pack), zf (gold packs, not found), premiumBuy',
    ['starter_pack: {id, gold:160, pieces:[5 slot items]}', 'npc_shop_items: 7', 'premiumBuy protocol'],
    ['MALL_ITEMS: 5 starter pieces VERIFIED', 'gold_packs: INFERRED (zf imported, def not found)'],
    {'ITEMS': 'starter pieces = Lumina set (starter_equipment)',
     'ECONOMY': 'gold pricing'},
    'CLIENT_MODEL (starter) / INFERRED_MODEL (gold packs)',
    ['zf array definition location', 'premium pack contents', 'gold pricing table'])

dom('equipment_generator', 'web-v2/main-DEXZ0AP0.js', 'Ga (sword-slot templates), Pe (template check), Wa (divine_wings)',
    ['templates: bow staff quarterstaff dagger_pair hammer + sword knife kunai hammer bow rod quarterstaff katana flask',
     'divine_wings special template'],
    ['EQUIPMENT_TEMPLATES: 11 weapon templates + divine_wings'],
    {'CLASSES': 'templates bound to class jobs[] (katana→kensei, flask→nekobaku)',
     'ITEMS': 'starter equipment uses templates'},
    'CLIENT_MODEL (template list) / UNKNOWN_MODEL (generation formula)',
    ['actual generation roll server-side', 'stat ranges per tier', 'tier assignment'])

dom('exp_table', 'web-v2/items-CvFgs761.js', 'BA (16-entry array), z5 function (not extracted), of(level)',
    ['BA=[6,7,10,9,2,11,4,15,5,14,1,8,3,0,13,12]', 'z5 = base exp function, ditemukan tidak terekstrak'],
    ['EXP_TABLE: UNKNOWN — z5 belum diekstrak; BA = job progression order (interpretasi INFERRED)'],
    {'MONSTERS': 'baseExp observed per monster', 'CLASSES': 'jobProgress per class'},
    'UNKNOWN_MODEL',
    ['z5 function body', 'level cap', 'job exp curve'])

dom('refine', 'web-v2/items-CvFgs761.js', 'Ce (fail factor), pc/Ic (success calc), ce (stat caps), ie.refineStone',
    ['startLevel:20, perLevel:0.0025, max:0.3', '10 stat caps', 'refineStone rate 0.01, level>=70'],
    ['REFINE_RULES: failFactor(level), successRate(level, refine), stat_caps[10]'],
    {'ITEMS': 'refine_stone item', 'MONSTERS': 'drop Lv70+'},
    'CLIENT_MODEL (formula display) / UNKNOWN_MODEL (server behavior)',
    ['server refine formula', 'break behavior', 'break_protection_stone mechanics'])

dom('fusion', 'web-v2/main-DEXZ0AP0.js', 'Iy({type:"fuse",...}), fusion-master NPC',
    ['fuse protocol: gearIds[] + slot + template', 'forge_effects: 4'],
    ['FUSION_RULES: protocol VERIFIED, forge effect values UNKNOWN'],
    {'EQUIPMENT_TEMPLATES': 'template param', 'NPCS': 'fusion-master'},
    'OBSERVED_MODEL (protocol) / UNKNOWN_MODEL (rules)',
    ['forge effect definitions', 'fusion success rate', 'material requirements'])

dom('pet', 'web-v2/main-DEXZ0AP0.js', 'petBag, petLoot, petWithdraw',
    ['10 pet types elemental', 'petBag {inventory, gear}', 'loot filter: consumable/etc/card/equipment'],
    ['PET_TYPES: 10 (dew-bunny water, thorn-pixie poison, honey-moth wind, bramble-hare earth, frost-puff ice, ...)',
     'PET_ACTIONS: petLoot/petWithdraw protocol'],
    {'ITEMS': 'pet loot filter references item categories', 'MONSTERS': 'pet originates from monster family (INFERRED: dew-bunny ↔ Dew Bunny mob)'},
    'CLIENT_MODEL (types) / OBSERVED_MODEL (protocol)',
    ['pet acquisition', 'pet leveling', 'pet stats'])

dom('world_boss', 'web-v2/main-DEXZ0AP0.js', '{key:"prism-hopper",hp:3e4,damage:180,reward:9e3,respawn:zi,home:Ao}',
    ['hp:30000, damage:180, reward:9000 (VERIFIED)', 'respawn: zi (variable, UNKNOWN value)', 'home: Ao (UNKNOWN value)'],
    ['WORLD_BOSSES: 1 boss — stats VERIFIED, respawn/home UNKNOWN'],
    {'MONSTERS': 'prism-hopper = Prism Hopper Lv1 elite (30000 HP match!)',
     'CARDS': 'boss_card = Crowned Prism Hopper Card'},
    'CLIENT_MODEL (stats) / UNKNOWN_MODEL (schedule)',
    ['zi respawn value', 'Ao home coordinates', 'spawn announcement'])

dom('arena', 'web-v2/main-DEXZ0AP0.js', 'arena map, pvpChallenge, duel rules',
    ['arena map 1536x1216', 'pvp_actions: 3 (challenge/respond/concede)', 'duel: 3 minutes no penalty'],
    ['ARENAS: 1 arena map + PVP protocol'],
    {'MAPS': 'arena map entry', 'CLASSES': 'class change in arena'},
    'CLIENT_MODEL',
    ['arena channels server state', 'rating system (ada?)'])

dom('npc', 'web-v2/main-DEXZ0AP0.js', 'atlas loads: blacksmith merchant broker banker stat-master fusion-master',
    ['6 NPC dengan sprite + fungsi'],
    ['NPCS: 6 — blacksmith(refine), merchant(shop), broker(market), banker(storage), stat-master(reset), fusion-master(fusion)'],
    {'MAPS': 'semua di rome (Aurelia Forum)', 'REFINE/FUSION/STORAGE/MARKET': 'masing-masing NPC gateway'},
    'CLIENT_MODEL (VERIFIED sprite+fungsi)',
    ['posisi koordinat NPC di map'])

dom('storage', 'web-v2/main-DEXZ0AP0.js', 'storageOpen, deposit, withdraw protocol',
    ['3 actions', 'premium: buka dari menu di mana saja'],
    ['STORAGE_RULES: protocol VERIFIED, kapasitas UNKNOWN'],
    {'NPCS': 'banker', 'ECONOMY': 'premium feature'},
    'OBSERVED_MODEL (protocol)',
    ['kapasitas storage', 'premium multiplier'])

dom('market', 'web-v2/main-DEXZ0AP0.js', 'marketCreateOrder, goldOrder, marketGetDepth, marketListGear, w.goldMarket',
    ['5 actions', 'gold market: order book (asks/bids depth)', 'goldMarket = server-provided'],
    ['MARKET_RULES: order protocol VERIFIED, fee/tax UNKNOWN'],
    {'ITEMS': 'gear listing', 'ECONOMY': 'gold exchange'},
    'OBSERVED_MODEL (protocol) / UNKNOWN_MODEL (fees)',
    ['market fee/tax', 'min/max price', 'order expiry'])

dom('feature_flags', 'web-v2/main-DEXZ0AP0.js', 'disabled(214), hidden(570) — UI states only',
    ['tidak ada feature flag eksplisit', 'comingSoon/notImplemented: tidak ditemukan'],
    ['FEATURE_FLAGS: NONE — semua disabled/hidden = UI state'],
    {},
    'VERIFIED (negative finding)',
    [])

dom('death_revive', 'web-v2/main-DEXZ0AP0.js', 'deadUntil, reviveHere, reviveAtTown, L1(area)',
    ['reviveHere: silver cost varies by area (L1)', 'reviveAtTown: free + full HP + 500ms attack delay'],
    ['DEATH_REVIVE_RULES: 2 mode — cost table L1(area) UNKNOWN values'],
    {'MAPS': 'cost per area', 'ECONOMY': 'silver sink'},
    'CLIENT_MODEL (mechanism) / UNKNOWN_MODEL (cost values)',
    ['L1 cost table per area', 'EXP penalty (ada?)'])

json.dump({'_meta': {'version': 'v0.4', 'domains': len(model),
                     'classification_legend': ['OBSERVED_MODEL', 'CLIENT_MODEL', 'INFERRED_MODEL', 'UNKNOWN_MODEL']},
           'domains': model},
          open('research/v04/database_merge/CLIENT_MINING_NORMALIZED.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

print(f'domains normalized: {len(model)}')
for name, d in model.items():
    print(f"  {name}: {d['confidence'][:60]}")
