# Lumivara Online — Laporan Pembongkaran Klien & Arsitektur Keamanan

**Target:** `Lumivara.Online-0.1.0-win-x64-portable.exe` (102.6 MB)
**SHA-256:** `003862eec2c8c3dcd12f9e742980af0d1a52582cdb3ce7a6c9118df25239afb7` — cocok dengan digest resmi di GitHub `Gamezxz/lumivara-online-downloads` v0.1.0 (provenance terverifikasi, bukan repack)
**Tanggal analisis:** 2026-09-28
**Metode:** Statis murni (NSIS → 7z → asar → JS bundle). Tidak ada eksekusi sample.

---

## 1. Struktur Kemasan (CONFIRMED)

```
portable.exe (102.6 MB)
└─ NSIS-3 (electron-builder)
   └─ app-64.7z (LZMA2+BCJ2)
      ├─ Lumivara Online.exe — Electron 44.4.5 / Chromium 152.0.7977.130
      ├─ resources/app.asar (141 MB)
      │  ├─ desktop/main.cjs (4 KB) — satu-satunya kode desktop
      │  └─ node_modules/phaser (139 MB — tidak dipakai main.cjs)
      └─ resources/elevate.exe — helper standar electron-builder (bersih)
```

**Fakta kunci:** exe ini hanya shell browser. `main.cjs` memuat `https://lumivaraonline.com/` — seluruh logika game berjalan dari web bundle. Env var `LUMIVARA_GAME_URL` bisa mengarahkan shell ke origin lain.

**Hardening shell (CONFIRMED, dibaca penuh dari main.cjs):**
- `contextIsolation:true`, `nodeIntegration:false`, `sandbox:true`
- Permission handler menolak SEMUA permission request
- Navigasi dibatasi whitelist: origin game + `accounts.google.com`; sisanya dibuka via `shell.openExternal` dengan validasi protokol (http/https/mailto saja)
- Tidak ada preload script, tidak ada IPC custom
- Session persist: `partition: 'persist:lumivara'`
- Single-instance lock aktif

## 2. Klien Web (CONFIRMED)

| Bundle | Ukuran | Isi |
|---|---|---|
| `main-BHjIB9U4.js` | 2.3 MB | Seluruh game (Phaser 3.90 + engine) |
| `items-CgoiYVa1.js` | 185 KB | Konstanta mekanik: drop rate display, formula refine, cap stat |
| `party-DtA8am7a.js` | 602 KB | Party + locale dinamis |
| `changelog-notice-C0oHFSuO.js` | 541 KB | Riwayat patch |
| `legal-D2W54pbO.js` | 40 KB | ToS |

- Genre: klon Ragnarok Online (pierce/flee/ASPD/MDEF/refine/card slot), MMORPG pixel Thailand, F2P.
- Transport realtime: `wss://lumivaraonline.com/api/ws?v=<ver>&area=<hint>`, auth cookie session, JSON per pesan, ping/pong built-in.
- **Snapshot di-decode via protobufjs (`T.decode(A)`)** — skema protobuf tertanam di bundle, dapat direkonstruksi.
- Locale: th (default), en, zh-CN, zh-TW, id, fil, pt-BR.
- `/api/boot-report` = crash reporter (sendBeacon: `at, message, error, diag, ua, href`), dipanggil saat boot >8 dtk atau error fatal. **Bukan anti-cheat.**

## 3. Permukaan REST (CONFIRMED dari korpus string)

```
/api/announce  /api/boot-report  /api/character-name  /api/donation
/api/exp-event /api/guest  /api/guest/delete  /api/login-queue
/api/logout   /api/me  /api/referral  /api/referral/bind
/api/shop  /api/shop/checkout  /api/shop/confirm
/api/shop/purchases  /api/shop/refund  /api/version  /api/ws
```

## 4. Protokol WS

**Klien→server (CONFIRMED):** `move, stop, attack, skill, pickup, drop, equip, unequip, use, potion, refine, fuse, deposit, withdraw, travel, revive, repair, inspect, emote, sit, donate, skin, channel, text, view, stat, lock, destroy`

**Server→klien top-level (CONFIRMED):** `pong`, `moved` (area baru → close 4100 → reconnect), `snapshot` (state utama + events), `chatline`, `attributes`

**Event dalam snapshot (CONFIRMED):** `hit, bossCast, bossSkill, buy, casting, daily, defeat, donate, eat, emote, exchange, friend, fusion, gold, hunt, inspect, market, mobSkill, party, pet, pickup, potion, premium, pvp, quest, reaction, refine, rename, repair, resetSkills, resetStats, reveal, sale, skill, skillError, status, storage, trade, use, bagFull`

**Close codes (CONFIRMED):**
- `4100` — pindah area, reconnect
- `4002` — karakter terbuka di tab lain
- `4004` — idle timeout
- `F0` (variabel) — login dari tempat lain

## 5. Trust Boundary — Temuan Inti

### 5.1 Anti-cheat klien: NIHIL (CONFIRMED)
| Pencarian | Hasil |
|---|---|
| integrity, devtools, debugger, cheat, hack, tamper, verify, banned | 0 hit |

Tidak ada integrity check, devtools detection, atau anti-tampering apa pun di klien.

### 5.2 Pergerakan: klien kirim posisi langsung (CONFIRMED di klien)
```javascript
r={type:"move",x:o,y:p},i=JSON.stringify(r);
i!==this.networkCommand&&(J.send(r),this.networkCommand=i)
```
Koordinat dibulatkan ke grid 16px di klien lalu dikirim. Tidak ada kode koreksi/reconcile posisi dari server yang terlihat. **Validasi server opaque — ada atau tidaknya tidak bisa dikonfirmasi dari bundle klien** (HYPOTHESIS: kemungkinan ada validasi server-side, tapi tak terbukti).

### 5.3 Cooldown: semua klien-side (CONFIRMED)
- Chat: `chatReadyAt` + queue `flushChat()` dengan retry
- Potion: `se={potions:0,cooldown:0,...}`
- Skill: `skillCooldowns={}, skillReadyAt`
- Attack interval: `nextAttack=this.time.now+this.interval` (dari ASPD)

Semua timer bisa dimodifikasi via JS. `rateLimit/throttle/spam/flood`: 0 hit di korpus.

### 5.4 Fog of war: berbasis area (CONFIRMED)
Snapshot hanya memuat `mobInfo`, `drops`, `players` untuk area aktif. Pindah area → `this.mobs.clear()`. Tidak ada AOI radius, tidak ada data area tetangga. Konstanta drop-rate di `items.js` (`card:.001`, `bossCard:.01`, `equipment:.0125`) kemungkinan hanya untuk display UI — roll asli ada di server (HYPOTHESIS).

### 5.5 Auto Play resmi (CONFIRMED)
Game punya tombol "ตั้งค่าบอท" (pengaturan bot) bawaan — ToS eksplisit mengizinkan Auto Play internal, melarang bot eksternal/makro/modifikasi paket. State machine `setAuto()` klien-side penuh: targeting, `autoRotation` skill, auto-loot, `walkToward()` antar-map.

### 5.6 Guest: POST kosong, tanpa CAPTCHA (CONFIRMED mekanisme, HYPOTHESIS farmability)
```javascript
const f=await fetch("/api/guest",{method:"POST",
  headers:{"content-type":"application/json"},body:"{}"})
// → {needsName:true} → POST /api/character-name {name}
```
Tidak ada CAPTCHA atau rate-limit yang terlihat di klien. Guest bisa dihapus via `POST /api/guest/delete` `{confirmation:"DELETE"}`, bisa convert ke akun Google. Apakah endpoint-nya dibatasi server-side (IP throttle dsb.) tidak bisa dikonfirmasi statis.

## 6. Ringkasan Risiko

| Aspek | Status | Catatan |
|---|---|---|
| Anti-cheat klien | ❌ tidak ada | CONFIRMED |
| Integrity check | ❌ tidak ada | CONFIRMED |
| Validasi gerakan server | ⚠️ opaque | HYPOTHESIS — tak terlihat dari klien |
| Rate limiting | ❌ klien-only | CONFIRMED (di sisi klien) |
| Fog of war | ✅ per-area | CONFIRMED |
| Guest farming | ⚠️ proteksi minimal tampak | HYPOTHESIS |

## 7. Artefak

- `D:\lumivara-re\nsis-out\` — lapisan NSIS
- `D:\lumivara-re\app\` — aplikasi Electron terekstrak
- `D:\lumivara-re\asar-out\` — isi app.asar (main.cjs + node_modules)
- `D:\lumivara-re\web\` — bundle JS situs (main, items, party, legal, changelog)

## 8. Langkah Lanjut yang Terbuka

1. Rekonstruksi skema protobuf snapshot dari bundle (protobufjs `T.decode` → struktur field lengkap)
2. Deminifikasi main.js (webcrack/source-map probe) untuk baca engine Auto Play & combat secara utuh
3. Pengamatan pasif WS (proxy logging) untuk verifikasi empiris validasi server — **butuh akun & jalankan game, di luar lingkup statis**
4. Diff rilis berikutnya (repo GitHub releases) untuk melihat apakah server-side hardening berubah
5. Audit `/api/login-queue` dan `/api/exp-event` — endpoint yang belum dibedah
