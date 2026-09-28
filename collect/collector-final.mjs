// Collector v5: spawnReady + walk realistis + BFS portal + interior probe
import { WebSocket } from 'ws';
import fs from 'node:fs';

const OUT = 'D:/lumivara-re/collect';
const GDB = JSON.parse(fs.readFileSync('D:/lumivara-re/GAME_DB.json', 'utf8'));
const ADJ = JSON.parse(fs.readFileSync(OUT + '/adjacency.json', 'utf8'));
const sleep = ms => new Promise(r => setTimeout(r, ms));

let cookie = '', area = '', self = {}, ws, wsAlive = false, ready = false;
let collected = { areas: {}, events: [] };

// merge run sebelumnya
try {
  const prev = JSON.parse(fs.readFileSync(OUT + '/raw-snapshots.json', 'utf8'));
  for (const [a, A] of Object.entries(prev.areas ?? {})) {
    if (!collected.areas[a]) collected.areas[a] = { snapshots: 0, mobInfo: {}, mobTuples: {}, drops: {}, players: 0, self: null, events: [] };
    const T = collected.areas[a];
    T.snapshots += A.snapshots ?? 0;
    Object.assign(T.mobInfo, A.mobInfo ?? {});
    for (const [id, t] of Object.entries(A.mobTuples ?? {})) {
      const p = T.mobTuples[id];
      T.mobTuples[id] = p ? { ...p, hp: Math.max(p.hp, t.hp) } : t;
    }
    Object.assign(T.drops, A.drops ?? {});
    T.players = Math.max(T.players, A.players ?? 0);
    T.events.push(...(A.events ?? []));
  }
  collected.events.push(...(prev.events ?? []));
  console.log(`merged: ${Object.keys(collected.areas).length} areas`);
} catch { console.log('fresh'); }

function record(area, msg) {
  if (!area) area = 'unknown';
  if (!collected.areas[area]) collected.areas[area] = { snapshots: 0, mobInfo: {}, mobTuples: {}, drops: {}, players: 0, self: null, events: [] };
  const A = collected.areas[area];
  A.snapshots++;
  if (msg.self) {
    A.self = { ...(A.self ?? {}), ...msg.self };
    self = { ...self, ...msg.self };
    if (msg.self.area) { area = msg.self.area; }
  }
  for (const mi of (msg.mobInfo ?? [])) A.mobInfo[mi.id] = mi;
  for (const t of (msg.mobs ?? [])) {
    if (!Array.isArray(t) || t.length < 5) continue;
    const [id, x, y, hp, alive] = t;
    const prev = A.mobTuples[id];
    A.mobTuples[id] = { id, x, y, hp: Math.max(prev?.hp ?? 0, hp), alive: alive ?? prev?.alive };
  }
  for (const d of (msg.drops ?? [])) A.drops[d.id] = d;
  A.players = Math.max(A.players, (msg.players ?? []).length);
  for (const ev of (msg.events ?? [])) { A.events.push(ev); collected.events.push({ area, ev }); }
}

function connectOnce() {
  return new Promise((resolve, reject) => {
    ws = new WebSocket('wss://lumivaraonline.com/api/ws?v=5' + (area ? `&area=${encodeURIComponent(area)}` : ''), { headers: { cookie } });
    wsAlive = true; ready = false;
    const to = setTimeout(() => { try { ws.terminate(); } catch {} reject(new Error('timeout')); }, 15000);
    ws.on('open', () => { clearTimeout(to); resolve(); });
    ws.on('error', e => { wsAlive = false; clearTimeout(to); reject(e); });
    ws.on('close', () => { wsAlive = false; });
    ws.on('message', d => {
      try { const m = JSON.parse(d.toString()); } catch {}
      let m; try { m = JSON.parse(d.toString()); } catch { return; }
      if (m.type === 'pong') return;
      if (m.type === 'moved') { console.log(`  MOVED -> ${m.area}`); area = m.area; return; }
      if (m.type === 'snapshot') {
        record(m.self?.area ?? area, m);
        // spawnReady setelah snapshot pertama diterima (ala klien)
        if (!ready) { ready = true; try { ws.send(JSON.stringify({ type: 'spawnReady' })); } catch {} }
      }
    });
  });
}
async function connect() {
  for (let i = 0; i < 6; i++) {
    try { await connectOnce(); await sleep(2000); if (wsAlive) return; } catch (e) { console.log(`  retry ${i + 1}: ${e.message}`); }
    await sleep(2500 * (i + 1));
  }
  throw new Error('connect failed');
}
const send = o => { try { ws.send(JSON.stringify(o)); return true; } catch { return false; } };

async function walk(tx, ty, maxMs = 90000) {
  const t0 = Date.now();
  let lastSent = 0;
  while (Date.now() - t0 < maxMs) {
    if (!wsAlive) return false;
    const dx = tx - self.x, dy = ty - self.y;
    const dist = Math.hypot(dx, dy);
    if (dist < 20) return true;
    const now = Date.now();
    if (now - lastSent < 125) { await sleep(30); continue; }
    lastSent = now;
    const step = Math.min(dist, 80);
    send({ type: 'move', x: Math.round((self.x + dx / dist * step) / 16) * 16, y: Math.round((self.y + dy / dist * step) / 16) * 16 });
    await sleep(130);
  }
  return Math.hypot(tx - self.x, ty - self.y) < 40;
}

function pathTo(from, to) {
  const q = [[from]], seen = new Set([from]);
  while (q.length) {
    const p = q.shift(); const last = p[p.length - 1];
    if (last === to) return p;
    for (const n of (ADJ[last] ?? [])) if (!seen.has(n)) { seen.add(n); q.push([...p, n]); }
  }
  return null;
}

async function gotoArea(target) {
  let stall = 0;
  while (area !== target && stall < 8) {
    if (!wsAlive) await connect();
    const path = pathTo(area, target);
    if (!path || path.length < 2) return false;
    const next = path[1];
    const P = (GDB.maps[area]?.portals ?? []).find(p => p.to === next);
    if (!P) return false;
    console.log(`  walk ${area} -> portal(${P.x},${P.y}) -> ${next}`);
    const before = area;
    await walk(P.x, P.y);
    send({ type: 'travel', to: next });
    for (let i = 0; i < 70 && area !== next; i++) await sleep(200);
    if (area === next) { stall = 0; await sleep(2000); if (!wsAlive) await connect(); continue; }
    if (area === before) stall++; else stall = 0;
    await sleep(2000);
  }
  return area === target;
}

// kandidat pintu interior: arrival portal balik di area sumber
const INTERIOR = {
  inn: { from: 'field', door: [640, 2336] },
  training: { from: 'field', door: [1470, 290] },
  cove: { from: 'field', door: [640, 2336] },
  grove: { from: 'field', door: [2688, 1120] },
  ruins: { from: 'snow', door: [150, 640] },
  temple: { from: 'grove', door: [110, 512] },
  arena: { from: 'rome', door: null },  // enterArena message
};

async function main() {
  const r = await fetch('https://lumivaraonline.com/api/guest', { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
  cookie = (r.headers.getSetCookie?.() ?? []).map(c => c.split(';')[0]).join('; ');
  const acc = await r.json();
  if (acc.needsName) {
    await fetch('https://lumivaraonline.com/api/character-name', {
      method: 'POST', headers: { 'content-type': 'application/json', cookie },
      body: JSON.stringify({ name: 'Cartograph' + (Math.floor(Math.random() * 9000) + 1000) })
    });
  }
  await connect();
  await sleep(4000);
  if (!area) area = self?.area || 'rome';   // pastikan area terisi dari snapshot
  console.log('start:', area, self.x, self.y);

  // 1. BFS area normal dulu
  const visited = new Set();
  const queue = [area || 'rome'];
  while (queue.length) {
    const a = queue.shift();
    if (visited.has(a)) continue;
    visited.add(a);
    if (area !== a) { const ok = await gotoArea(a); if (!ok) continue; }
    console.log(`DWELL ${a} (${visited.size}/19)`);
    if (!wsAlive) await connect();
    await sleep(9000);
    fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected));
    for (const n of (ADJ[a] ?? [])) if (!visited.has(n)) queue.push(n);
  }

  // 2. interior: arena via enterArena
  if (area !== 'arena') { await gotoArea('rome'); await sleep(1000); }
  send({ type: 'enterArena' });
  await sleep(4000);
  console.log('arena attempt ->', area);
  if (area === 'arena') {
    console.log('DWELL arena');
    await sleep(8000);
    fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected));
    // keluar arena
    const ap = GDB.maps.arena.portals[0];
    await walk(ap.x, ap.y); send({ type: 'travel', to: 'rome' }); await sleep(3000);
  }

  // 3. interior: inn & training & cove & grove via pintu di field
  for (const [name, cfg] of Object.entries(INTERIOR)) {
    if (name === 'arena' || collected.areas[name]?.mobInfo && Object.keys(collected.areas[name].mobInfo).length > 0) continue;
    if (collected.areas[name]?.snapshots > 3) continue;
    console.log(`\n=== INTERIOR ${name} ===`);
    if (cfg.door) {
      if (area !== cfg.from) { const ok = await gotoArea(cfg.from); if (!ok) { console.log('  gagal ke', cfg.from); continue; } }
      await sleep(1500);
      const ok = await walk(cfg.door[0], cfg.door[1]);
      console.log(`  at door(${cfg.door}): ${ok} pos=(${self.x},${self.y})`);
      send({ type: 'travel', to: name });
      await sleep(3500);
      console.log('  ->', area);
      if (area === name) {
        await sleep(8000); // dwell
        fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected));
        // keluar via portal balik
        const back = GDB.maps[name]?.portals?.[0];
        if (back) { await walk(back.x, back.y); send({ type: 'travel', to: back.to }); await sleep(3000); }
      }
    }
  }

  console.log('\n=== FINAL ===');
  for (const [a, A] of Object.entries(collected.areas)) console.log(`${a}: snaps=${A.snapshots} mobInfo=${Object.keys(A.mobInfo).length}`);
  fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected));
  try { ws.close(1000); } catch {}
  process.exit(0);
}
main().catch(e => { console.error('FATAL', e.message); fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected)); process.exit(1); });
