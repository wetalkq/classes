const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, '..', 'v13'); const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 2 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
    await p.goto('file://' + path.join(dir, f)); await p.waitForFunction(() => document.body.dataset.ok);
    const rep = await p.evaluate(() => {
      const out = []; const boxes = [...document.querySelectorAll('.box')];
      boxes.forEach((b, i) => {
        const k = parseFloat(b.style.getPropertyValue('--k') || 1);
        if (b.scrollHeight > b.clientHeight + 1 || b.scrollWidth > b.clientWidth + 1) out.push(`box${i} overflow`);
        if (k < 0.8) out.push(`box${i} shrunk k=${k.toFixed(2)}`);
        const kids = [...b.children].map(c => c.getBoundingClientRect());
        for (let j = 1; j < kids.length; j++) if (kids[j].top < kids[j - 1].bottom - 2) out.push(`box${i} lines overlap`);
      });
      const r = boxes.map(b => { const ks = [...b.children].map(c => c.getBoundingClientRect()); return ks.length ? { t: Math.min(...ks.map(k => k.top)), b: Math.max(...ks.map(k => k.bottom)), l: Math.min(...ks.map(k => k.left)), r: Math.max(...ks.map(k => k.right)) } : null; });
      for (let i = 0; i < r.length; i++) for (let j = i + 1; j < r.length; j++) { const A = r[i], B = r[j]; if (A && B && A.l < B.r && B.l < A.r && A.t < B.b && B.t < A.b) out.push(`box${i}&box${j} overlap`); }
      return out;
    });
    console.log(f, rep.length ? rep.join('; ') : 'OK');
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')) });
  }
  await b.close();
})();
