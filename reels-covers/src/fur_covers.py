"""Шесть обложек 9:16 на фонах «шерсть» — текст и отступы 1:1 из v13_916, цвет текста строго #d2cec3,
под текстом плашка строго #415038, чтобы бежевый читался на любом узоре."""
import os, re, subprocess
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "v13_916"); FUR = os.path.join(ROOT, "box", "fur")
OUT = os.path.join(ROOT, "fur_covers"); TMP = os.path.join(OUT, "tmp"); os.makedirs(TMP, exist_ok=True)
G = (65, 80, 56); BE = "#d2cec3"

JOBS = [  # исходник v13 -> фон -> имя (порядок как прислала)
    ("59_ряд31-2_bag-49", "fon2_zebra", "1_bag49_zebra"),
    ("16_ряд11-1_special", "fon2_tiger", "2_otzyvy_tigr"),
    ("12_ряд07-3_podcast", "fon2_giraffe", "3_podcast_uverennost_zhiraf"),
    ("54_ряд29-2_bag-45", "fon2_panther", "4_bag45_pantera"),
    ("48_ряд27-2_podcast-03", "fon2_cheetah", "5_podcast3_gepard"),
    ("44_ряд26-1_podcast-05", "fon2_zebra", "6_podcast5_zebra"),
]
import sys
PANEL = "--panel" in sys.argv

for src, _, name in JOBS:
    h = open(os.path.join(SRC, src + ".html"), encoding="utf-8").read()
    h = h.replace("#415038", BE).replace("background:#d2cec3", "background:transparent")
    h = h.replace("<body style='background:transparent'>", "<body style='background:transparent'>")
    open(os.path.join(TMP, name + ".html"), "w", encoding="utf-8").write(h)

js = """const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{const dir=process.argv[2]; const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:2});
for (const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html')).sort()){
 await p.goto('file://'+path.join(dir,f)); await p.waitForFunction(()=>document.body.dataset.ok);
 await p.screenshot({path:path.join(dir,f.replace('.html','.png')),omitBackground:true});}
await b.close();})();"""
open(os.path.join(TMP, "r.js"), "w").write(js)
subprocess.run(["node", os.path.join(TMP, "r.js"), TMP], check=True)

for src, bg, name in JOBS:
    txt = Image.open(os.path.join(TMP, name + ".png")).convert("RGBA").resize((2160, 3840), Image.LANCZOS)
    fur = Image.open(os.path.join(FUR, bg + ".jpg")).convert("RGB").resize((2160, 3840), Image.LANCZOS).convert("RGBA")
    x0, y0, x1, y1 = txt.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox()
    px, py = 120, 130
    X0, Y0, X1, Y1 = 2 * 120, y0 - py, 2160 - 2 * 120, y1 + py     # одинаковая плашка на всех обложках
    if PANEL:
        sh = Image.new("RGBA", fur.size, (0, 0, 0, 0)); m = Image.new("L", fur.size, 0)
        m.paste(255, (X0 + 10, Y0 + 24, X1 + 10, Y1 + 24)); sh.putalpha(m.point(lambda v: int(v * .35)))
        fur.alpha_composite(sh.filter(ImageFilter.GaussianBlur(36)))
        fur.paste(G + (255,), (X0, Y0, X1, Y1))
    else:  # без плашки: лёгкая тёмная тень под буквами, как на обложке с коробкой
        al = txt.split()[3]
        g = Image.new("RGBA", fur.size, (8, 10, 4, 0)); g.putalpha(al.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * .92)))
        fur.alpha_composite(g); fur.alpha_composite(g)
    fur.alpha_composite(txt)
    out = fur.resize((1080, 1920), Image.LANCZOS).convert("RGB")
    out.save(os.path.join(OUT, name + ".jpg"), quality=95)
    print(name, (X0 // 2, Y0 // 2, X1 // 2, Y1 // 2))
