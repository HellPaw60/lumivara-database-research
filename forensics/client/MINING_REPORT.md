# LUMIVARA CLIENT DEEP-MINING REPORT
## Bundle: web-v2/main-DEXZ0AP0.js (2.4MB) + web-v2/items-CvFgs761.js (197KB)

---

## 1. QUEST SYSTEM
- **Status**: VERIFIED
- **Entries**: Server-driven (client only tracks)
- **Events tracked**: changeClass, equip, buy, sell, learn, stat, potion, pickup, travel, kill, kill:mobName
- **questTick()**: `counters[c] = (counters[c] ?? 0) + S`
- **claimQuest()**: Sends to server or processes via kh()
- **claimHunt()**: Daily hunt quest
- **claimDaily()**: Daily quest claim
- **Display format**: `${hint} (${have}/${need})` or `ทำครบแล้ว · แตะเพื่อรับรางวัล`
- **No quest**: `เส้นทางของนักผจญภัย`

## 2. SHOP/MALL
- **Status**: VERIFIED (Starter Pack), INFERRED (Gold/Premium Packs)
- **Starter Pack**: 160 Gold, 17 Lumina equipment pieces
- **Pieces**: Circlet, Monocle, Scarf, Coat, Guard, Cape, Boots, Ring, Earring, Sword/Knife/Kunai/Katana/Hammer/Bow/Rod/Flask/Staff
- **NPC Shop items**: potion(10), blue_potion(50), concentration_potion(80), awakening_potion(240), berserk_potion(600), fly_wing(30), butterfly_wing(30)
- **Gold/Premium packs**: zf array imported from items.js (ot export), definition not found in analyzed files

## 3. EQUIPMENT GENERATOR
- **Status**: VERIFIED (template system)
- **Templates**: sword, knife, kunai, katana, hammer, bow, rod, flask, quarterstaff, dagger_pair, staff
- **Special template**: divine_wings (uses Ga check)
- **Bonuses structure**: Object with stat values (atk, def, matk, hp, str, agi, vit, int, dex, luk, hit, crit, flee)
- **Generation**: Appears server-side, client has template detection logic

## 4. REFINE
- **Status**: VERIFIED
- **Refine Stone drop**: 1% chance, level 70+ only
- **Refine formula**: Ca(level) = min(0.3, max(0, (level - 20) * 0.0025))
- **Success rate**: Ic(level, refine) = 1 - Ca(level) * (1 - min(100, refine) / 100)
- **Refine bonuses**: pierce(60), mpierce(60), atkPct(30), matkPct(30), lifesteal(8), freezeHit(15), resStun(80), resFreeze(80), moveSpeed(30), critDmg(60)
- **Break Protection**: Protection Stone prevents equipment/card breaking on failure

## 5. FUSION
- **Status**: VERIFIED
- **Fusion action**: `{type:'fuse', gearIds:[...], slot:slot, template:template}`
- **Fusion Master NPC**: fusion-master-v1 sprite
- **Forge effects**: hammer, anvil, success, broken
- **Result display**: fusion-result element

## 6. PET SYSTEM
- **Status**: VERIFIED
- **Pet types**: dew-bunny(water), thorn-pixie(poison), honey-moth(wind), bramble-hare(earth), frost-puff(ice), icicle-hare(ice), snow-owl(ice), aurora-fox(ice), dune-gecko(earth), scarab-sentinel(earth)
- **Pet bag**: Separate storage for pet loot
- **Pet loot filter**: Configurable (consumable, etc, card, equipment)
- **Pet withdraw**: Individual (gearId) or All (all:true)
- **Pet options**: pet-pickup toggle, pet-first (owner/pet)

## 7. EXP TABLE
- **Status**: VERIFIED (BA array), INFERRED (z5 function)
- **BA array**: [6,7,10,9,2,11,4,15,5,14,1,8,3,0,13,12] - class job level progression order
- **jobExp**: Stored as Number, capped at BA(jobLevel)-1
- **jobProgress**: Per-class tracking (jobProgress[classId].level, jobExp)
- **Points**: `this.points += z5(i)` on level up (z5 function not fully extracted)
- **Exp display**: `${exp} / ${nextExp}` percentage

## 8. MARKET/EXCHANGE
- **Status**: VERIFIED
- **Sell order**: `{type:'marketCreateOrder', side:'sell', item:item, price:price, quantity:qty}`
- **Buy order**: `{type:'marketCreateOrder', side:'buy', item:item, price:price, quantity:qty}`
- **Gold order**: `{type:'goldOrder', side:side, price:price, quantity:qty}`
- **List gear**: `{type:'marketListGear', gearId:id, price:price}`
- **Cancel order**: cancelOrder function
- **Gold market**: Server-provided (w.goldMarket)

## 9. STORAGE/BANK
- **Status**: VERIFIED
- **Open**: `{type:'storageOpen'}`
- **Deposit**: `{type:'deposit', gearId:id}` or `{type:'deposit', item:item, quantity:qty}`
- **Premium access**: Can access from menu anywhere
- **Banker NPC**: banker-v2 sprite

## 10. WORLD BOSS
- **Status**: VERIFIED
- **Crowned Prism Hopper**: HP=30000, Damage=180, Reward=9000
- **Status attack**: crush with 30% chance
- **Boss card**: Crowned Prism Hopper Card (atk:10, luk:3, atkPct:5, matkPct:5, price:3000)
- **King mechanic**: king flag affects loot ownership

## 11. ARENA/PVP
- **Status**: VERIFIED
- **Arena**: Aurelia Arena (PVP free-for-all, party members can't attack each other)
- **Training**: Training Grounds (dummy testing, no EXP/items)
- **Challenge**: `{type:'pvpChallenge', target:playerId}`
- **Duel**: 3 minutes, no penalty for losing
- **Respond**: `{type:'pvpRespond', from:playerId, accept:bool}`
- **Auto-settings**: localStorage.pixelrpg.auto-settings

## 12. DEATH/REVIVE
- **Status**: VERIFIED
- **deadUntil**: Timestamp, 0 when alive
- **Revive here**: Costs silver (L1(area)), full HP
- **Revive at town**: Free, full HP, nextAttack=now+500ms
- **Death cause**: String describing killer
- **Death timer**: Math.max(0, deadUntil - time.now) in seconds

## 13. FEATURE FLAGS
- **Status**: NOT FOUND (as explicit flags)
- **experimental**: Only in WebGL context
- **disabled**: 214 matches (UI states, not feature flags)
- **hidden**: 570 matches (UI visibility, not feature flags)
- **comingSoon/notImplemented/workInProgress**: Not found

## 14. NPC TABLE
- **Status**: VERIFIED
- **NPCs found**:
  - blacksmith: `/npc/blacksmith-v1/npc.png` - Repair equipment
  - merchant: `/npc/merchant-v2/player.png` - Buy/sell items
  - broker: `/npc/merchant-v1/npc.png` - Market (นายหน้าตลาด)
  - banker: `/jobs/banker-v2/player.png` - Storage (เจ้าหน้าที่คลัง)
  - stat-master: `/jobs/stat-master-v1/player.png` - Stat allocation
  - fusion-master: `/npc/fusion-master-v1/player.png` - Equipment fusion

---

## OUTPUT FILES
- Raw blobs: D:/lumivara-re/forensics/client/raw/ (14 files)
- Parsed tables: D:/lumivara-re/forensics/client/tables/ (14 files)

## NOTES
- Quest data is SERVER-DRIVEN. Client only tracks counters and displays progress.
- Gold/Premium mall packs (zf array) imported from items.js but definition not found in analyzed files.
- z5 function (points per level) found but not fully extracted.
- Equipment generation appears SERVER-SIDE. Client has template detection logic only.
- No explicit feature flags found. 'disabled' and 'hidden' are UI element states.
- All NPCs located in Aurelia Forum (rome map).