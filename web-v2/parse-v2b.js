
const fs = require('fs');
const src = fs.readFileSync('items-CvFgs761.js', 'utf8');
const body = src.replace(/export\{[\s\S]*$/, 'module.exports = {Kn, le, N, Y, x, ie, W1};');
const mod = {exports:{}};
new Function('module','exports', body)(mod, mod.exports);
const E = mod.exports;
const map = {Kn:'consumables', le:'cards', N:'status_effects', Y:'maps', x:'skills', ie:'drop_rates', W1:'mob_status_attacks'};
for (const [n, label] of Object.entries(map)) {
  if (E[n]) { fs.writeFileSync(`v2_${label}.json`, JSON.stringify(E[n], null, 2)); console.log(label, Object.keys(E[n]).length); }
  else console.log(n, 'MISSING');
}
