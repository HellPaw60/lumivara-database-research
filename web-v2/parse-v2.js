
const fs = require('fs');
const src = fs.readFileSync('items-CvFgs761.js', 'utf8');
const body = src.replace(/export\{[\s\S]*$/, 'module.exports = {ac, ne, O, K, T, ee, te, De};');
const mod = {exports:{}};
new Function('module','exports', body)(mod, mod.exports);
const E = mod.exports;
for (const n of Object.keys(E)) {
  fs.writeFileSync(`v2_${n}.json`, JSON.stringify(E[n], null, 2));
  console.log(n, Object.keys(E[n]).length, 'entries');
}
