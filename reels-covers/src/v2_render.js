const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, '..', 'v2');
  const only = process.argv[2];
  const items = JSON.parse(fs.readFileSync(path.join(dir, 'items.json')));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  for (const it of items) {
    if (only && !it.name.includes(only)) continue;
    await p.goto('file://' + path.join(dir, it.name + '.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(dir, it.name + '.png') });
  }
  await b.close();
})();
