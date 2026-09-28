// Probe interior areas: walk realistis (80px/130ms) ke kandidat lokasi objek, lalu travel
import { WebSocket } from 'ws';
import fs from 'node:fs';

const gdb = JSON.parse(fs.readFileSync('D:/lumivara-re/GAME_DB.json', 'utf8'));
const sleep = ms => new Promise(r => setTimeout(r, ms));
let cookie = '', area = '', self = {}, ws, wsAlive = false;

function connect() {
  return new Promise((resolve, reject) => {
    ws = new WebSocket('wss://lumivaraonline.com/api/ws?v=5' + (area ? `&area=${area}` : ''), { headers: { cookie } });
    wsAlive = true;
    const to = setTimeout(() => { try { ws.terminate(); } catch {} reject(new Error('timeout')); }, 15000);
    ws.on('open', () => { clearTimeout(to); resolve(); });
    ws.on('error', e => { wsAlive = false; clearTimeout(to); reject(e); });
    ws.on('close', () => { wsAlive = false; });
    ws.on('message', d => {
      try { const m = JSON.parse(d.toString());
        if (m.type === 'snapshot') { self = { ...self, ...m.self }; if (m.self?.area) area = m.self.area; }
        if (m.type === 'moved') { area = m.area; console.log('  MOVED ->', m.area); }
      } catch {}
    });
  });
}
const send = o => { try { ws.send(JSON.stringify(o)); } catch {} };

// walk dengan langkah kecil ala klien asli (max 90px per 120ms)
async function walk(tx, ty, maxMs = 60000) {
  const t0 = Date.now();
  while (Date.now() - t0 < maxMs) {
    if (!wsAlive) return false;
    const dx = tx - self.x, dy = ty - self.y;
    const dist = Math.hypot(dx, dy);
    if (dist < 24) return true;
    const step = Math.min(dist, 80);
    send({ type: 'move', x: Math.round((self.x + dx / dist * step) / 16) * 16, y: Math.round((self.y + dy / dist * step) / 16) * 16 });
    await sleep(130);
  }
  return false;
}

async function main() {
  const r = await fetch('https://lumivaraonline.com/api/guest', { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
  cookie = (r.headers.getSetCookie?.() ?? []).map(c => c.split(';')[0]).join('; ');
  const acc = await r.json();
  if (acc.needsName) {
    await fetch('https://lumivaraonline.com/api/character-name', {
      method: 'POST', headers: { 'content-type': 'application/json', cookie },
      body: JSON.stringify({ name: 'DoorSeek' + (Math.floor(Math.random() * 9000) + 1000) })
    });
  }
  await connect();
  await sleep(4000);
  console.log('start:', area, self.x, self.y);

  // target: pintu inn di field — arrival inn->field = [640, 2336]
  const pf = gdb.maps.rome.portals.find(p => p.to === 'field');
  await walk(pf.x, pf.y);
  send({ type: 'travel', to: 'field' });
  await sleep(4000);
  console.log('in field:', area, self.x, self.y);

  // jalan ke kandidat pintu inn (640,2336)
  const ok = await walk(640, 2336);
  console.log('walk to inn-door:', ok, 'pos:', self.x, self.y);
  send({ type: 'travel', to: 'inn' });
  await sleep(3000);
  console.log('after inn travel:', area);
  if (area === 'inn') { console.log('*** INN ENTERED ***'); fs.appendFileSync('D:/lumivara-re/collect/interior-findings.txt', `inn via field(640,2336)\n`); }

  // sweep halus di sekitar (640,2336) radius 128 — mungkin offset pintu
  if (area !== 'inn') {
    for (const [ox, oy] of [[-128,0],[128,0],[0,-128],[0,128],[-64,-64],[64,64]]) {
      await walk(640 + ox, 2336 + oy);
      send({ type: 'travel', to: 'inn' });
      await sleep(2500);
      if (area === 'inn') { console.log(`*** INN via field(${640+ox},${2336+oy}) ***`); fs.appendFileSync('D:/lumivara-re/collect/interior-findings.txt', `inn via field(${640+ox},${2336+oy})\n`); break; }
    }
  }
  console.log('final area:', area);
  process.exit(0);
}
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
