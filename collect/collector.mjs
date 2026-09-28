// Lumivara Online — collector v4: walk-to-portal + travel + dwell, merge antar run
import { WebSocket } from 'ws';
import fs from 'node:fs';

const OUT = 'D:/lumivara-re/collect';
const GDB = JSON.parse(fs.readFileSync('D:/lumivara-re/GAME_DB.json', 'utf8'));
const ADJ = JSON.parse(fs.readFileSync(OUT + '/adjacency.json', 'utf8'));
const sleep = ms => new Promise(r => setTimeout(r, ms));

let cookie = '', areaHint = '', ws = null, wsAlive = false, self = null;
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
  console.log(`merged: ${Object.keys(collected.areas).length} areas dari run sebelumnya`);
} catch { console.log('fresh start'); }

function record(area, msg) {
  if (!area) area = 'unknown';
  if (!collected.areas[area]) collected.areas[area] = { snapshots: 0, mobInfo: {}, mobTuples: {}, drops: {}, players: 0, self: null, events: [] };
  const A = collected.areas[area];
  A.snapshots++;
  if (msg.self) {
    A.self = { ...(A.self ?? {}), ...msg.self };
    self = { ...(self ?? {}), ...msg.self };
    if (msg.self.area) areaHint = msg.self.area;
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
    const url = 'wss://lumivaraonline.com/api/ws?v=5' + (areaHint ? `&area=${encodeURIComponent(areaHint)}` : '');
    ws = new WebSocket(url, { headers: { cookie } });
    wsAlive = true;
    const to = setTimeout(() => { try { ws.terminate(); } catch {} reject(new Error('connect timeout')); }, 15000);
    ws.on('open', () => { clearTimeout(to); resolve(); });
    ws.on('error', e => { wsAlive = false; clearTimeout(to); reject(e); });
    ws.on('close', (code) => { wsAlive = false; });
    ws.on('message', (data) => {
      let msg; try { msg = JSON.parse(data.toString()); } catch { return; }
      if (msg.type === 'pong') return;
      if (msg.type === 'moved') { console.log(`  moved -> ${msg.area}`); areaHint = msg.area; return; }
      if (msg.type === 'snapshot') record(msg.self?.area ?? areaHint, msg);
    });
  });
}
async function connect() {
  for (let i = 0; i < 6; i++) {
    try { await connectOnce(); await sleep(1500); if (wsAlive) return; } catch (e) { console.log(`  retry ${i + 1}: ${e.message}`); }
    await sleep(2500 * (i + 1));
  }
  throw new Error('connect failed');
}

function send(o) { try { ws.send(JSON.stringify(o)); return true; } catch { return false; } }

// jalan ke koordinat (interpolasi langkah kecil ala klien asli)
async function walkTo(tx, ty) {
  let x = self?.x ?? 0, y = self?.y ?? 0;
  if (!x && !y) return;
  const dist = Math.hypot(tx - x, ty - y);
  const steps = Math.min(40, Math.max(3, Math.ceil(dist / 48)));
  for (let i = 1; i <= steps; i++) {
    const nx = Math.round((x + (tx - x) * i / steps) / 16) * 16;
    const ny = Math.round((y + (ty - y) * i / steps) / 16) * 16;
    if (!send({ type: 'move', x: nx, y: ny })) return;
    await sleep(120);
  }
  // posisi terakhir = portal
  send({ type: 'move', x: Math.round(tx / 16) * 16, y: Math.round(ty / 16) * 16 });
  await sleep(400);
}

// BFS path di graf area
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
  while (areaHint !== target && stall < 10) {
    if (!wsAlive) { await connect(); }
    const path = pathTo(areaHint, target);
    if (!path || path.length < 2) { console.log(`  no path ${areaHint}->${target}`); return false; }
    const next = path[1];
    const portals = (GDB.maps[areaHint]?.portals ?? []).filter(p => p.to === next);
    if (!portals.length) { console.log(`  no portal def ${areaHint}->${next}`); return false; }
    const P = portals[0];
    console.log(`  walk ${areaHint} -> portal(${P.x},${P.y}) -> ${next}`);
    const before = areaHint;
    await walkTo(P.x, P.y);
    send({ type: 'travel', to: next });
    for (let i = 0; i < 60 && areaHint !== next; i++) await sleep(200);
    if (areaHint === next) { stall = 0; await sleep(1500); if (!wsAlive) await connect(); continue; }
    if (areaHint === before) stall++; else stall = 0;   // progress tetap dihitung
    console.log(`  hop gagal (${areaHint}), stall=${stall}`);
    await sleep(2000);
  }
  return areaHint === target;
}

async function main() {
  const r = await fetch('https://lumivaraonline.com/api/guest', { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
  cookie = (r.headers.getSetCookie?.() ?? []).map(c => c.split(';')[0]).join('; ');
  const acc = await r.json();
  console.log('guest:', acc.name);
  if (acc.needsName) {
    await fetch('https://lumivaraonline.com/api/character-name', {
      method: 'POST', headers: { 'content-type': 'application/json', cookie },
      body: JSON.stringify({ name: 'WanderDex' + (Math.floor(Math.random() * 9000) + 1000) })
    });
  }
  await connect();
  await sleep(4000);
  console.log('start area:', areaHint);

  const visited = new Set();
  const queue = [areaHint || 'rome'];
  while (queue.length) {
    const area = queue.shift();
    if (visited.has(area)) continue;
    visited.add(area);
    console.log(`\n=== DWELL ${area} (${visited.size}/${Object.keys(ADJ).length}) ===`);
    if (areaHint !== area) { const ok = await gotoArea(area); if (!ok) { console.log('  skip (unreachable)'); continue; } }
    if (!wsAlive) await connect();
    await sleep(10000); // dwell
    if (!wsAlive) { try { await connect(); await sleep(4000); } catch {} }
    fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected));
    console.log(`  saved: ${Object.entries(collected.areas).map(([a, A]) => a + ':' + Object.keys(A.mobInfo).length).join(' ')}`);
    for (const n of (ADJ[area] ?? [])) if (!visited.has(n)) queue.push(n);
  }

  console.log('\n=== SELESAI ===');
  fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected));
  try { ws.close(1000); } catch {}
  process.exit(0);
}

main().catch(e => { console.error('FATAL:', e.message); fs.writeFileSync(OUT + '/raw-snapshots.json', JSON.stringify(collected)); process.exit(1); });
