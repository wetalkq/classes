const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{const dir=path.join(__dirname,'..','v9');const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1440},deviceScaleFactor:2});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html'))){await p.goto('file://'+path.join(dir,f));await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:path.join(dir,f.replace('.html','.png'))});}await b.close();})();
