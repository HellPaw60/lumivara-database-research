
const fs = require('fs');
const src = fs.readFileSync('items.js', 'utf8');
// bungkus: jalankan seluruh file sebagai module, tapi items.js adalah ESM (const...)
// trik: buat module context manual — replace export di akhir, jalankan via new Function
const body = src.replace(/export\{[\s\S]*$/, 'module.exports = {ac, ne, O, K, T, ee, te, De};');
const mod = {exports:{}};
new Function('module','exports', body)(mod, mod.exports);
const E = mod.exports;
for (const n of Object.keys(E)) {
  fs.writeFileSync(`db_${n}.json`, JSON.stringify(E[n], null, 2));
  const v = E[n];
  const cnt = typeof v === 'object' ? Object.keys(v).length : 'scalar';
  console.log(n, cnt, 'entries');
}
