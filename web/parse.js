
const fs = require('fs');
for (const n of ['ac','ne','O','K','T']) {
  try {
    const blob = fs.readFileSync(`table_${n}.js`, 'utf8');
    const obj = eval('(' + blob + ')');
    fs.writeFileSync(`db_${n}.json`, JSON.stringify(obj, null, 2));
    console.log(n, Object.keys(obj).length, 'entries');
  } catch(e) { console.log(n, 'ERR', e.message.slice(0,80)); }
}
