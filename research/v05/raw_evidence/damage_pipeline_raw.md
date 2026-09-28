# RAW EVIDENCE - Damage Pipeline & Stat Relationships

## 1. De Function (Stat Computation) - items-CvFgs761.js offset 118174

```javascript
function De(A){const e=W0(A.stats),t=sa(A),n=Ai[A.classId??"novice"]??{};for(const E of lA)t[E]+=n[E]??0;const r=js(A.statuses);for(const E of lA)t[E]+=r.stats[E]??0;const a=Object.fromEntries(lA.map(E=>[E,e[E]+t[E]])),o=Ee(A);a.dex+=o.dex,a.vit+=o.vit,a.int+=o.int,a.str+=o.str;for(const E of lA)r.statPercent[E]&&(a[E]=Math.floor(a[E]*(1+r.statPercent[E])));const s=A.level-1,c=ei(A.classId),i=A.gear?.find(E=>E.id===A.equipped?.sword&&E.slot==="sword"),l=(A0(i)?1+o.meleeAtkPct:i?.template==="bow"?1+o.bowAtkPct:i?.template==="kunai"?1+o.kunaiAtkPct:i?.template==="katana"?1+o.katanaAtkPct:1)*(1+o.atkPct),h=Math.floor((Math.floor((100+s*5+a.vit*10)*(1+c.hp))+t.hp)*(1+o.maxHpPct)),P=Math.floor((Math.floor((20+s+a.int*5)*(1+c.sp))+t.sp)*(1+o.maxSpPct)),v=Math.floor((100+A.level+a.dex*2+Math.floor(a.luk/3)+o.hit+t.hit)*(1+o.hitPct)),_=Math.floor(h*o.maxHpAtkPct+v*o.atkPerHit+a.dex*o.atkPerDex+a.agi*o.atkPerAgi),M=(10+(Ft(i?.template)?a.dex*2+Math.floor(a.str/5):a.str*2+Math.floor(a.dex/5))+Math.floor(a.luk/10)+s*.3)*l+_,k=1+o.matkPct,T=(5+a.int*3+a.dex+s*.3)*k+Math.floor(P*o.matkPerMaxSp+a.dex*o.matkPerDex+a.agi*o.matkPerAgi),d=Math.floor(a.vit/5),u=a.int+Math.floor(a.vit/5),m=Math.min(K0,Math.max(50,Math.round(Q0(q0(U0(A.classId,i?.template,ui(A)),a.agi,a.dex,r.aspdPercent+o.aspdPercent)+t.aspd+(r.stats.aspd??0))*10)/10)),g=Math.round((200-m)*20),D=1+Math.max(0,m-xn.from)*xn.perPoint,y={...t};y.dex+=o.dex,y.def+=o.def,y.mdef+=o.mdef,y.vit+=o.vit,y.int+=o.int,y.str+=o.str;for(const E of lA)y[E]=a[E]-e[E];const S=E=>Math.max(0,Math.min(ce[E],t[E])),qA=S("atkPct"),YA=S("matkPct");return{base:e,bonus:y,total:a,atkBase:M,atkPct:qA,atk:(M+t.atk*l)*(1+qA/100),matkBase:T,matkPct:YA,matk:(T+t.matk*k)*(1+YA/100),pierce:S("pierce"),mpierce:S("mpierce"),lifesteal:S("lifesteal"),freezeHit:S("freezeHit"),resStun:S("resStun"),resFreeze:S("resFreeze"),critDmg:S("critDmg"),stunHit:S("stunHit"),bleedHit:S("bleedHit"),crushHit:S("crushHit"),spDrain:S("spDrain"),spRegen:Math.max(0,Math.min(Na,t.spRegen)),moveSpeed:Math.max(0,Math.min(ce.moveSpeed,t.moveSpeed+o.moveSpeed)),defBase:d,def:d+t.def+o.def,mdefBase:u,mdef:u+t.mdef+o.mdef,hit:v,flee:Math.floor((A.level+a.agi*2+Math.floor(a.luk/5)+t.flee)*(1+o.fleePct)),gearFlee:Math.floor(t.flee*(1+o.fleePct)),perfectDodge:Math.min(15,a.luk*.1)+o.perfectDodge,critical:Math.min(100,(Math.floor(a.luk/3)+s*.1+t.crit+o.crit+(r.stats.crit??0))*(wi(i)?2:1)),spellCritical:Math.min(100,Math.floor(a.luk/3)+t.crit),critMultiplier:2*(1+o.critDamagePct+S("critDmg")/100),aspd:m,interval:g,basicFactor:D,maxHp:h,maxSp:P}}
```

## 2. Ml Function (Basic Attack Damage) - items-CvFgs761.js offset 121135

```javascript
function Ml(A,e=()=>Math.random(),t=J0(A.level,Z0(A))){const n=De(A),r=e()<n.critical/100,a=!r&&e()>=qr(n.hit,t);return{critical:!a&&r,missed:a,damage:a?0:Math.round(n.atk*n.basicFactor*(r?n.critMultiplier:1))}}
```

## 3. _l Function (Mob → Player Damage) - items-CvFgs761.js offset 121346

```javascript
function _l(A,e,t,n=()=>Math.random(),r,a=0){const o=De(A),s=Math.max(0,Math.min(o.gearFlee,o.flee-A.level)),c=(Math.max(0,o.flee-A.level-s)*.008+Math.min(qn,s*.008)+o.perfectDodge/100)/(1+r?.hitBonus),i=r?.hit===void 0?c:1-qr(r.hit,o.flee)+o.perfectDodge/100,l=t?0:Math.min(r?.dodgeCap,i),h=l>0&&n()<l,P=1-Math.max(0,Math.min(100,a))/100,v=Si(A)*P,_=Math.round(e*(1-v/100));return{missed:h,damage:h?0:Math.max(1,_-Math.round((t?o.mdef:o.def)*P))}}
```

## 4. Ic Function (Pierce Damage Modifier) - items-CvFgs761.js offset ~27

```javascript
const Ic=(A,e)=>1-Ca(A)*(1-Math.max(0,Math.min(100,e))/100)
// Ca(A)=Math.max(0,Math.min(.3,(A-20)*.0025))
// Usage: T5(c.level, w==="matk" ? o.mpierce : o.pierce)
// T5 in main = Ic in items (alias: dA as T5)
```

## 5. O1 Function (Status Damage Modifier) - items-CvFgs761.js offset ~76293

```javascript
const O1=(A,e=Date.now())=>1+me.perStack*Fs(A,e)
// Usage: t.damage=Math.round(t.damage*E5(this.statuses,S))
// E5 in main = O1 in items (alias: dy as E5)
```

## 6. $1 Function (Incoming Damage Factor) - items-CvFgs761.js offset ~77721

```javascript
const $1=(A,e)=>A.incomingFactor*(e?A.magicFactor:A.physicalFactor)
// Usage: B5(status, isMagic)
// B5 in main = $1 in items (alias: dR as B5)
```

## 7. skillStrike Function - main-DEXZ0AP0.js offset ~2297200

```javascript
skillStrike(c,S){const T=Zt(this),w=Math.random()<(S==="atk"?T.critical:T.spellCritical)/100;return{damage:Math.round(T[S]*c*(w?T.critMultiplier:1)),critical:w,missed:!1}}
```

## 8. damageMonster Function (core pipeline) - main-DEXZ0AP0.js offset ~2297267

```javascript
damageMonster(c,S,T=1,w="atk",A,u=!1,y){if(!c.alive)return 0;const t=y?{...y,missed:!1}:T===1&&w==="atk"?y5(this,Math.random,x5(c.level,S5(this))):this.skillStrike(T,w);if(this.lastHitCritical=t.critical,t.missed||this.art[this.mobs.indexOf(c)+1]?.act("hurt",this.player.x,this.player.y),!y&&T===1&&w==="atk"&&!t.missed&&(t.damage=Math.round(t.damage*E5(this.statuses,S)),b5(this,S)),!y&&t.damage>0){const o=Zt(this);t.damage=Math.max(1,Math.round(t.damage*T5(c.level,w==="matk"?o.mpierce:o.pierce)))}if(A&&w==="matk"&&mx(this,`${this.area}:self`,c.x,c.y,t.damage),c.key===G0?og(t.damage,t.missed,t.critical):(c.hp=Math.max(0,c.hp-t.damage),c.aggro=!0),...
```

## 9. qr Function (Hit Chance) - items-CvFgs761.js

```javascript
const ee={even:.9,perPoint:.005,min:.5,max:1}
const qr=(A,e)=>Math.min(ee.max,Math.max(ee.min,ee.even+(A-e)*ee.perPoint))
```

## 10. q0 Function (ASPD Calculation) - items-CvFgs761.js offset ~118048

```javascript
function q0(A,e,t,n=0){const r=1-(A-144)/50,a=(Math.max(0,e)*X0+Math.max(0,t)*V0)*r;return 200-(200-(A+a))*(1-n)}
// X0=.3, V0=.02
// Usage: q0(U0(class,weapon,shield), AGI, DEX, statusAspdPercent)
```

## 11. U0 Function (Base ASPD) - items-CvFgs761.js

```javascript
function U0(A,e,t){return(Ln[A??"novice"]??Ln.novice)+(e?Xr[e]??0:0)-(t?Vr:0)}
// Ln = class base ASPD, Xr = weapon modifier, Vr = shield penalty (8)
```

## 12. Q0 Function (ASPD Soft Cap) - items-CvFgs761.js

```javascript
const Q0=A=>A<=Ye?A:Ye+(A-Ye)*Y0
// Ye=180, Y0=.5
```

## 13. W0 Function (Stat Clamping) - items-CvFgs761.js

```javascript
function W0(A){return Object.fromEntries(lA.map(e=>[e,Number.isFinite(A[e])?Math.min(Ur,Math.max(Q,Math.floor(A[e]))):Q]))}
// Q=1, Ur=99
```

## 14. Class Bonuses (Ai) - items-CvFgs761.js

```javascript
Ai={novice:{},swordman:{str:3,vit:2},mage:{int:5},archer:{dex:5},acolyte:{int:3,vit:2},merchant:{str:2,vit:3},thief:{agi:3,luk:2},mamushi:{agi:2,dex:2,luk:1},nekobaku:{agi:2,int:3},kensei:{agi:2,str:2,de...}
```

## 15. Class Base ASPD (Ln) - items-CvFgs761.js

```javascript
Ln={novice:148,swordman:150,mage:145,archer:147,acolyte:150,merchant:148,thief:152,mamushi:152,nekobaku:150,kensei:152}
```

## 16. Weapon ASPD Modifiers (Xr) - items-CvFgs761.js

```javascript
Xr={knife:2,dagger_pair:2,kunai:2,flask:0,katana:1,sword:0,falchion:0,blade:0,hammer:-2,rod:-8,staff:-10,quarterstaff:-5,bow:-4}
```

## 17. ce Caps - items-CvFgs761.js

```javascript
ce={pierce:60,mpierce:60,atkPct:30,matkPct:30,lifesteal:8,freezeHit:15,resStun:80,resFreeze:80,moveSpeed:30,critDmg:60,stunHit:15,bleedHit:15,crushHit:15,spDrain:5}
```

## 18. xn (Basic Attack Scaling) - items-CvFgs761.js

```javascript
xn={from:170,perPoint:.015}
// basicFactor = 1 + max(0, aspd - 170) * 0.015
```

## 19. Element System - items-CvFgs761.js

```javascript
// Monster elements
Cr={"moss-mushroom":"poison","amber-beetle":"earth","cave-bat":"shadow","tide-crab":"water","leaf-sprout":"earth","forest-wolf":"wind","wild-boar":"earth","lantern-wisp":"fire","pebble-golem":"earth","rootling":"earth","prism-hopper":"light","dew-bunny":"water","thorn-pixie":"poison","honey-moth":"wind","bramble-hare":"earth","frost-puff":"ice","icicle-hare":"ice","snow-owl":"ice","aurora-fox":"ice","dune-gecko":"earth","scarab-sentinel":"earth","sunscale-cobra":"poison","cactus-imp":"earth","bog-toad":"poison","mud-newt":"water","mire-jelly":"water","reed-mantis":"wind","ember-antler":"fire","moon-owl":"shadow","vine-lynx":"earth","sand-drake":"fire","magma-salamander":"fire","ember-hound":"fire","basalt-tortoise":"earth","obsidian-scorpion":"shadow","shade-raven":"shadow","bone-hound":"shadow","bog-wraith":"poison","grave-knight":"shadow","quartz-crawler":"earth","geode-armadillo":"earth","prism-serpent":"light","amethyst-wyvern":"light","thunder-ram":"wind","storm-roc":"wind","cloud-serpent":"water","tempest-drake":"wind"}

// Element hierarchy (for coating/resist)
Ks={fire:"fire",water:"water",ice:"water",earth:"earth",wind:"wind",poison:"earth",shadow:"dark",light:"light"}

// Skill elements
Vs={firebolt:"fire",magnum:"fire",coldbolt:"water",thunderstorm:"wind",tierra:"earth",holylight:"light",shadowburst:"dark",bigkaboom:"fire"}
```

## 20. Status Effect Damage

```javascript
// From N object (status definitions) - poison example
// N.poison.dot = {percent: 0.015, interval: 2000}  // 1.5% maxHP every 2s
// Damage: Math.max(1, Math.floor(maxHp * dot.percent * stacks))
```

## 21. Double Attack (Double Strike passive)

```javascript
// In damageMonster context:
// g5(T) && S.alive && w>0 && random()*100 < ih(player).doubleAttack
// doubleAttack = skillLevel * 5 (from Ee function: e("doubleattack")*5)
```

## 22. Level Up Rewards (from damageMonster)

```javascript
// On kill:
// points += z5(level - r + 1)  // stat points gained
// hp = maxHp, sp = maxSp  // full heal
// Float text: "LEVEL UP! Lv" + level + " · +statPoints points · MaxHP +5 · MaxSP +1 · ATK/MATK +0.3 · CRIT +0.1% · Weight +50"
```

---

**Confidence level**: VERIFIED_FROM_CLIENT_CODE (all formulas extracted directly from minified source)  
**Source files**: items-CvFgs761.js (197KB), main-DEXZ0AP0.js (2.4MB)  
**Extraction method**: Python regex + bracket matching on minified JS
