# LUMIVARA ONLINE - DAMAGE MODEL

**Sumber kode**: `web-v2/items-CvFgs761.js` (fungsi `De`, `Ml`, `_l`, `Ic`, `$1`), `web-v2/main-DEXZ0AP0.js` (fungsi `damageMonster`, `skillStrike`)  
**Tanggal ekstraksi**: 2025-09-28  
**Confidence**: VERIFIED_FROM_CLIENT_CODE

---

## 1. DAMAGE PIPELINE (Physical Attack)

### Pseudocode (Player → Monster)

```
function damageMonster(mob, time, multiplier=1, powerType="atk", arg, silent=false, override):
    if not mob.alive: return 0
    
    // Step 1: Determine base damage
    if override exists:
        hit = { ...override, missed: false }
    elif multiplier == 1 and powerType == "atk":
        // Basic attack: y5 computes hit/miss/crit/damage
        hit = y5(player, random, mob.level, mobFlee(mob.level))
    else:
        // Skill attack
        hit = skillStrike(multiplier, powerType)
    
    // Step 2: Apply status effects on basic attack (burn/crush/etc.)
    if not override and multiplier == 1 and powerType == "atk" and not hit.missed:
        hit.damage = round(hit.damage * E5(statuses, time))  // status damage modifier
        b5(player, time)  // apply momentum stacks
    
    // Step 3: Apply pierce
    if not override and hit.damage > 0:
        playerStats = Zt(player)  // De(player) - get computed stats
        pierceValue = (powerType == "matk") ? playerStats.mpierce : playerStats.pierce
        hit.damage = max(1, round(hit.damage * T5(mob.level, pierceValue)))
    
    // Step 4: Apply damage
    mob.hp = max(0, mob.hp - hit.damage)
    mob.aggro = true
    
    return hit.damage
```

### Step 1a: Basic Attack (`y5` di main = `Ml` di items)

**Fungsi `Ml` di `items-CvFgs761.js` (offset ~121135):**
```javascript
function Ml(A, e=()=>Math.random(), t=J0(A.level, Z0(A))) {
    const n = De(A);                    // Compute player stats
    const r = e() < n.critical / 100;   // Roll critical
    const a = !r && e() >= qr(n.hit, t); // Roll miss
    return {
        critical: !a && r,
        missed: a,
        damage: a ? 0 : Math.round(n.atk * n.basicFactor * (r ? n.critMultiplier : 1))
    };
}
```

**Formula:**
- **Hit/Miss**: `miss = random() >= qr(player.HIT, mobFLEE)` 
  - `qr(hit, flee) = min(1, max(0.5, 0.9 + (hit - flee) * 0.005))`
- **Critical**: `crit = random() < critical / 100`
- **Damage**: `round(ATK * basicFactor * (crit ? critMultiplier : 1))`

### Step 1b: Skill Attack (`skillStrike` di main)

**Fungsi di `main-DEXZ0AP0.js` (offset ~2297200):**
```javascript
skillStrike(c, S) {
    const T = Zt(this);  // Player stats
    const w = Math.random() < (S === "atk" ? T.critical : T.spellCritical) / 100;
    return {
        damage: Math.round(T[S] * c * (w ? T.critMultiplier : 1)),
        critical: w,
        missed: false  // Skills don't miss by default (miss added elsewhere)
    };
}
```

**Formula:**
- **Skill Damage**: `round(ATK_or_MATK * skillMultiplier * (crit ? critMultiplier : 1))`
- **Crit Roll**: Uses `critical` for physical skills, `spellCritical` for magic skills

### Step 2: Status Damage Modifier (`E5` di main = `O1` di items)

**Fungsi `O1` di `items-CvFgs761.js` (offset ~76293):**
```javascript
const O1 = (A, e = Date.now()) => 1 + me.perStack * Fs(A, e);
```

**Formula:**
- **Status Damage Multiplier**: `1 + momentumStacks * perStackValue`
- Applied only on basic attacks when not missed

### Step 3: Pierce Modifier (`T5` di main = `Ic` di items)

**Fungsi `Ic` di `items-CvFgs761.js` (offset ~273):**
```javascript
const Ic = (A, e) => 1 - Ca(A) * (1 - clamp(e, 0, 100) / 100);
// Ca(A) = clamp((A - 20) * 0.0025, 0, 0.3)
```

**Formula:**
- **Level Scaling**: `Ca(level) = min(max(0, (level - 20) * 0.0025), 0.3)`
- **Pierce Factor**: `1 - Ca(level) * (1 - pierce/100)`
- **Interpretation**: Pierce effectiveness scales with target level. At level 20+: Ca=0 (full pierce). At level 80+: Ca=0.3 (70% of pierce effective).  
  Example: 60 pierce vs level 50 mob: Ca(50)=0.075, factor = 1 - 0.075*(1-0.6) = 1 - 0.03 = 0.97 → 97% damage goes through 3% reduction ignored

**Usage in code:**
```javascript
hit.damage = max(1, round(hit.damage * T5(mob.level, pierce)))
```

### Step 4: DEF Reduction

**DEF is NOT subtracted from damage in the main damage pipeline.** Instead:
- DEF reduces damage through the pierce mechanism
- Pierce stat on equipment determines how much DEF is ignored
- Physical DEF: `def = VIT/5 + equipDEF + skillDEF`
- Magic MDEF: `MDEF = INT + VIT/5 + equipMDEF + skillMDEF`

**Note**: The `_l` function (aliased as `D5`) handles **player taking damage** (mob → player), where DEF is subtracted.

---

## 2. DAMAGE PIPELINE (Mob → Player)

### Fungsi `_l` di `items-CvFgs761.js` (offset ~121346):

```javascript
function _l(A, e, t, n=()=>Math.random(), r, a=0) {
    const o = De(A);  // Player stats
    const s = Math.max(0, Math.min(o.gearFlee, o.flee - A.level));
    const c = (Math.max(0, o.flee - A.level - s) * 0.008 + 
               Math.min(0.2, s * 0.008) + 
               o.perfectDodge / 100) / (1 + r?.hitBonus);
    const i = r?.hit === undefined ? c : 1 - qr(r.hit, o.flee) + o.perfectDodge / 100;
    const l = t ? 0 : Math.min(r?.dodgeCap, i);
    const h = l > 0 && n() < l;  // Dodge roll
    
    const P = 1 - clamp(a, 0, 100) / 100;  // Incoming damage factor from statuses
    const v = Si(A) * P;  // Shield refine bonus
    const _ = round(e * (1 - v / 100));  // Damage after shield
    
    return {
        missed: h,
        damage: h ? 0 : max(1, _ - round((t ? o.mdef : o.def) * P))
    };
}
```

**Formula:**
- **Mob Flee Check**: `mobFlee = 100 + 2 * mobLevel` (from tooltip: "FLEE ของมอน = 100 + 2 × เลเวล")
- **Dodge Chance**: Based on FLEE vs mob HIT, capped by dodgeCap (0.95 for player, 0.87 for mob)
- **Mob Damage**: `round(mobDamage * (1 - shieldRefine/100))`
- **Final Damage**: `max(1, mobDamage - DEF * incomingFactor)` (or MDEF for magic)

---

## 3. CRIT CHANCE

### Physical Critical (melee/ranged)

```javascript
critical = min(100, (floor(LUK/3) + (Lv-1)*0.1 + equipCRIT + skillCRIT + statusCRIT) * (isDaggerOrKnife ? 2 : 1))
```

**Formula:**
- Base: `LUK/3 + 0.1% per level`
- Additive: Equipment CRIT + Skill CRIT (katanamastery) + Status CRIT (meikyo)
- Multiplicative: ×2 if weapon is knife/dagger_pair/kunai (via `wi(i)` function)
- Cap: 100%

### Spell Critical (magic)

```javascript
spellCritical = min(100, floor(LUK/3) + equipCRIT)
```

**Formula:**
- Base: `LUK/3`  
- Additive: Equipment CRIT only  
- No level bonus, no weapon doubling, no skill bonus  
- Matches changenote: *"crit เวท = LUK/3 + CRIT dari equipment"*

### Crit Damage Multiplier

```javascript
critMultiplier = 2 * (1 + critDamagePct + equipCritDmg/100)
```

**Formula:**
- Base: 200% (2× damage)
- Additive: Skill crit damage% (fatalsense, zanshin) + Equipment crit damage%
- At max: 2 × (1 + 0.30 + 0.60) = 3.8× (with fatalsense + zanshin + equip critDmg)

---

## 4. ASPD (Attack Speed)

### Base ASPD per Class

```javascript
Ln = {
    novice: 148, swordman: 150, mage: 145, archer: 147,
    acolyte: 150, merchant: 148, thief: 152, mamushi: 152,
    nekobaku: 150, kensei: 152
}
```

### Weapon ASPD Modifier

```javascript
Xr = {
    knife: 2, dagger_pair: 2, kunai: 2, flask: 0, katana: 1,
    sword: 0, falchion: 0, blade: 0, hammer: -2,
    rod: -8, staff: -10, quarterstaff: -5, bow: -4
}
```

### ASPD Formula (from `De` function)

```javascript
// Step 1: Base ASPD
baseAspd = classBaseAspd + weaponMod - (shieldEquipped ? 8 : 0)

// Step 2: AGI/DEX contribution (scaled by base)
r = 1 - (baseAspd - 144) / 50  // R-factor
agiDexBonus = (AGI * 0.3 + DEX * 0.02) * r
aspdWithStats = baseAspd + agiDexBonus

// Step 3: Apply ASPD% from buffs
aspdPercent = statusAspdPercent + skillAspdPercent
finalAspd = 200 - (200 - aspdWithStats) * (1 - aspdPercent)

// Step 4: Add flat ASPD from equipment
finalAspd += equipAspd + statusAspdFlat

// Step 5: Soft cap (>180)
if finalAspd > 180: finalAspd = 180 + (finalAspd - 180) * 0.5

// Step 6: Hard cap
aspd = clamp(finalAspd, 50, 193)
```

### Attack Interval

```javascript
interval = round((200 - aspd) * 20)  // milliseconds
```

| ASPD | Interval |
|------|----------|
| 50   | 3000ms   |
| 100  | 2000ms   |
| 148  | 1040ms   |
| 170  | 600ms    |
| 180  | 400ms    |
| 193  | 140ms    |

### Basic Attack Damage Scaling (above 170 ASPD)

```javascript
basicFactor = 1 + max(0, aspd - 170) * 0.015
```

| ASPD | basicFactor |
|------|-------------|
| 170  | 1.000       |
| 180  | 1.150       |
| 193  | 1.345       |

---

## 5. ELEMENT SYSTEM

### Monster Elements

```javascript
Cr = {
    "moss-mushroom": "poison", "amber-beetle": "earth", "cave-bat": "shadow",
    "tide-crab": "water", "leaf-sprout": "earth", "forest-wolf": "wind",
    "wild-boar": "earth", "lantern-wisp": "fire", "pebble-golem": "earth",
    // ... 60+ monsters mapped to: fire, water, ice, earth, wind, poison, shadow, light
}
```

### Element Hierarchy

```javascript
Ks = {
    fire: "fire", water: "water", ice: "water", earth: "earth",
    wind: "wind", poison: "earth", shadow: "dark", light: "light"
}
```

### Skill Elements

```javascript
Vs = {
    firebolt: "fire", magnum: "fire", coldbolt: "water",
    thunderstorm: "wind", tierra: "earth", holylight: "light",
    shadowburst: "dark", bigkaboom: "fire"
}
```

### Element Coating System

**Fungsi `_c` di `items-CvFgs761.js`:**
- Weapon coating: Makes basic attacks and non-element skills become that element
- Armor coating: Changes what element the player *receives* damage as
- Duration: `gA.duration` (30 minutes default)
- Max stack: `gA.max` (capped)

### Element Damage Modifier

**Tidak ditemukan element damage multiplier di kode klien.**  
Tidak ada `elementDamage`, `weaknessMultiplier`, atau `resistMultiplier` yang diterapkan di `damageMonster` atau `_l`.

**Kesimpulan**: Element di Lumivara Online hanya menentukan **status effect** yang diapplied (burn, freeze, slow, dll.), bukan damage multiplier. Damage formula tidak membandingkan elemen attacker vs defender.

---

## 6. SKILL MULTIPLIER SYSTEM

### Skill `multiplier` Field

```javascript
x.bash = { multiplier: 2.5 }       // Physical: ATK * 2.5
x.firebolt = { multiplier: ... }   // Magic: MATK * multiplier
```

### Multiplier Scaling by Level

**Fungsi `C` di `items-CvFgs761.js`:**
```javascript
function C(skillId, level) {
    const baseMultipliers = {
        tierra: p0, thunderstorm: h0, coldbolt: m0,
        holylight: f0, leapshot: g0, doublestrafe: b0,
        cartstrike: w0, oboro: uA.perLevel, venomknife: M0,
        tarflask: J.tarPerLevel, bigkaboom: J.kaboomPerLevel,
        hammerfall: fe.base + fe.perLevel * (level - 1),
        arrowshower: 0.35 + 0.12 * level
    };
    // Default: round((1 + (defaultMulti - 1) * level / 10) * 100) / 100
}
```

**Formula:**
- Most skills: `multiplier = 1 + (baseMulti - 1) * skillLevel / 10`
- At level 10: full base multiplier
- At level 1: `1 + (baseMulti - 1) * 0.1`

---

## 7. HIT / MISS SYSTEM

### Player → Monster

```javascript
// qr function
qr(hit, flee) = clamp(0.9 + (hit - flee) * 0.005, 0.5, 1.0)

// Hit chance
hitChance = qr(player.HIT, mobFLEE)
miss = random() >= hitChance
```

**Mob FLEE**: `100 + 2 * mobLevel` (from tooltip)

### Mob → Player

```javascript
// Dodge calculation
gearFlee = min(equipFlee, totalFlee - level)
dodgeFromGear = gearFlee * 0.008 (capped at 0.2)
dodgeFromBase = max(0, totalFlee - level - gearFlee) * 0.008
perfectDodge = perfectDodge / 100
totalDodge = (dodgeFromBase + dodgeFromGear + perfectDodge) / (1 + mob.hitBonus)
dodgeCap = mob.dodgeCap (0.95 for player, 0.87 for mob)
finalDodge = min(dodgeCap, totalDodge)
```

---

## 8. STATUS EFFECTS ON DAMAGE

### Incoming Factor (`$1` di items = `B5` di main)

```javascript
const $1 = (A, e) => A.incomingFactor * (e ? A.magicFactor : A.physicalFactor);
```

- `incomingFactor`: From buffs like endure, holyguard (damage reduction)
- `physicalFactor`: Physical-only damage reduction
- `magicFactor`: Magic-only damage reduction

### Status Damage Modifier (`O1` di items = `E5` di main)

```javascript
const O1 = (A, e = Date.now()) => 1 + me.perStack * Fs(A, e);
```

- `momentumStacks`: Stacks from consecutive attacks
- `me.perLevel`: Damage increase per stack

---

## 9. SUMMARY TABLE

| Stat | Formula | Source |
|------|---------|--------|
| MaxHP | `((100 + (Lv-1)*5 + VIT*10) * (1 + classHP) + equipHP) * (1 + maxHpPct)` | De() |
| MaxSP | `((20 + (Lv-1) + INT*5) * (1 + classSP) + equipSP) * (1 + maxSpPct)` | De() |
| ATK | `(baseATK + equipATK * weaponMult) * (1 + atkPct/100)` | De() |
| MATK | `(baseMATK + equipMATK * (1+skillMatkPct)) * (1 + matkPct/100)` | De() |
| DEF | `VIT/5 + equipDEF + skillDEF` | De() |
| MDEF | `INT + VIT/5 + equipMDEF + skillMDEF` | De() |
| HIT | `(100 + Lv + DEX*2 + LUK/3 + equipHIT) * (1 + hitPct)` | De() |
| FLEE | `(Lv + AGI*2 + LUK/5 + equipFLEE) * (1 + fleePct)` | De() |
| CRIT | `min(100, (LUK/3 + (Lv-1)*0.1 + equipCRIT) * (2 if dagger else 1))` | De() |
| ASPD | `clamp(softCap(base + AGI*0.3*r + DEX*0.02*r + equipAspd), 50, 193)` | De() |
| Basic Dmg | `ATK * basicFactor * (crit ? critMultiplier : 1)` | Ml() |
| Skill Dmg | `ATK/MATK * multiplier * (crit ? critMultiplier : 1)` | skillStrike() |
| Pierce | `damage * (1 - Ca(level) * (1 - pierce/100))` | Ic() |
| Interval | `(200 - ASPD) * 20` ms | De() |

---

## 10. CATATAN PENTING

1. **Tidak ada element damage multiplier** - Element hanya menentukan status effect
2. **DEF tidak langsung dikurangi dari damage** - DEF dikabaikan oleh pierce
3. **Pierce adalah persentase** - Bukan flat. 60 pierce = ignore 60% DEF (scaled by level)
4. **ASPD soft cap di 180** - Setiap poin di atas 180 hanya setengah efektif
5. **Basic attack scaling** - Di atas 170 ASPD, damage meningkat 1.5% per poin
6. **Spell crit berbeda** - Tidak ada bonus dari level, hanya LUK/3 + equip CRIT
7. **Weapon type matters** - Dagger/knife mendapat ×2 CRIT multiplier
