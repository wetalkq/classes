"""Полосатые тканевые фоны в фирменных цветах + те же 6 обложек (текст 1:1 из v13_916).
A — узкие бежевые пин-полосы на зелёном #415038, текст бежевый #d2cec3 прямо на ткани.
B — широкие полосы зелёный/бежевый с тонкими оранжевыми #da5200 (только по бежевому), сверху бежевая
    тканевая карточка #d2cec3 с зелёным текстом, как на референсе."""
import os, subprocess
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "v13_916"); OUT = os.path.join(ROOT, "stripe_covers"); TMP = os.path.join(OUT, "tmp")
os.makedirs(TMP, exist_ok=True)
G = np.array([65, 80, 56], np.float32); BE = np.array([210, 206, 195], np.float32); O = np.array([218, 82, 0], np.float32)
W, H, S = 1080, 1920, 2
rng = np.random.default_rng(7)

def weave(h, w, amp=.06):
    """фактура ткани: нити по x и y + шум по нитям + мелкое зерно (среднее = 1)"""
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    t = .5 * np.sin(x * 2 * np.pi / 5.0) * np.sin(y * 2 * np.pi / 5.0)
    rows = rng.normal(0, 1, (h, 1)).astype(np.float32); cols = rng.normal(0, 1, (1, w)).astype(np.float32)
    rows = (rows + np.roll(rows, 1, 0) + np.roll(rows, -1, 0)) / 3
    grain = rng.normal(0, 1, (h, w)).astype(np.float32)
    # меланж: короткие вертикальные волокна
    fib = rng.normal(0, 1, (h // 6 + 1, w)).astype(np.float32); fib = np.repeat(fib, 6, 0)[:h]
    grain = .6 * grain + .8 * fib
    f = 1 + amp * (t + .35 * rows + .35 * cols + .5 * grain)
    return f / f.mean()

def stripes(unit, h, w):
    seq = np.concatenate([np.repeat(np.array(c, np.float32)[None], n * S, 0) for c, n in unit])
    reps = int(np.ceil(w / len(seq))) + 1
    row = np.tile(seq, (reps, 1))
    off = (len(row) - w) // 2
    return np.repeat(row[off:off + w][None], h, 0)

def fabric(unit, name):
    h, w = H * S, W * S
    img = stripes(unit, h, w)
    # мягкие края нитей между полосами
    img = np.asarray(Image.fromarray(img.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)
    img *= weave(h, w, .17)[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    im.save(os.path.join(TMP, name + ".png"))
    return im

A_UNIT = [(G, 64), (BE, 3), (G, 7), (BE, 3), (G, 7), (BE, 3)]                       # пин-полоса
B_UNIT = [(G, 150), (BE, 26), (O, 9), (BE, 12), (O, 9), (BE, 26), (BE, 110), (BE, 0)]  # широкие + тонкие оранжевые по бежевому

JOBS = [("59_ряд31-2_bag-49", "A", "1_bag49"), ("16_ряд11-1_special", "B", "2_otzyvy"),
        ("12_ряд07-3_podcast", "A", "3_podcast_uverennost"), ("54_ряд29-2_bag-45", "B", "4_bag45"),
        ("48_ряд27-2_podcast-03", "A", "5_podcast3"), ("44_ряд26-1_podcast-05", "B", "6_podcast5")]

def render_text():
    for src, kind, name in JOBS:
        h = open(os.path.join(SRC, src + ".html"), encoding="utf-8").read()
        h = h.replace("background:#d2cec3", "background:transparent")
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

if __name__ == "__main__" and "--cd" not in __import__("sys").argv:
    fa = fabric(A_UNIT, "fabric_A"); fb = fabric(B_UNIT, "fabric_B")
    fa.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "fon_polosy_A.jpg"), quality=96)
    fb.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "fon_polosy_B.jpg"), quality=96)
    render_text()
    card_tex = weave(H * S, W * S, .05)
    for src, kind, name in JOBS:
        txt = Image.open(os.path.join(TMP, name + ".png")).convert("RGBA")
        base = (fa if kind == "A" else fb).copy().convert("RGBA")
        al = txt.split()[3]
        if False:
            g = Image.new("RGBA", base.size, (8, 10, 4, 0)); g.putalpha(al.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * .85)))
            base.alpha_composite(g)
        else:  # тканевая карточка как на референсе
            x0, y0, x1, y1 = al.point(lambda v: 255 if v > 20 else 0).getbbox()
            X0, Y0, X1, Y1 = 120 * S, y0 - 150 * S // 2 * 2, (W - 120) * S, y1 + 150 * S // 2 * 2
            sh = Image.new("RGBA", base.size, (10, 10, 6, 0)); m = Image.new("L", base.size, 0)
            m.paste(255, (X0 + 14, Y0 + 30, X1 + 14, Y1 + 30)); sh.putalpha(m.point(lambda v: int(v * .55)))
            base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(40)))
            card = (BE[None, None] * card_tex[Y0:Y1, X0:X1, None])
            base.paste(Image.fromarray(np.clip(card, 0, 255).astype(np.uint8)).convert("RGBA"), (X0, Y0))
        base.alpha_composite(txt)
        base.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, f"{name}_polosy.jpg"), quality=95)
        print(name, kind)


# ---- вариант C/D по новым референсам: меланжевая ткань (заметное «соль-перец» зерно)
DK = np.array([29, 29, 8], np.float32)       # тёмный зелёный (как фон обложки с коробкой)
C_UNIT = [(BE, 62), (G, 6), (BE, 6), (G, 6), (BE, 6), (G, 6), (BE, 62)]              # бежевая основа + тройные зелёные полоски
D_UNIT = [(G, 70), (DK, 34), (G, 8), (BE, 6), (G, 8), (DK, 34), (G, 70), (BE, 6)]      # зелёная основа + широкие тёмные полосы и тонкие бежевые

def melange(unit, name, amp=.22):
    h, w = H * S, W * S
    img = stripes(unit, h, w)
    img = np.asarray(Image.fromarray(img.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)
    f = weave(h, w, amp)
    # цветные «искры» меланжа: отдельные светлые/тёмные волокна
    sp = rng.random((h, w)).astype(np.float32)
    f = f * np.where(sp > .985, 1.18, np.where(sp < .015, .82, 1.0))
    img *= f[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    return im

if __name__ == "__main__" and "--cd" in __import__("sys").argv:
    fc = melange(C_UNIT, "C"); fd = melange(D_UNIT, "D")
    fc.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "fon_polosy_C.jpg"), quality=96)
    fd.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "fon_polosy_D.jpg"), quality=96)
    card_tex = weave(H * S, W * S, .07)
    for i, (src, _, name) in enumerate(JOBS):
        txt = Image.open(os.path.join(TMP, name + ".png")).convert("RGBA")
        base = (fc if i % 2 == 0 else fd).copy().convert("RGBA")
        al = txt.split()[3]
        x0, y0, x1, y1 = al.point(lambda v: 255 if v > 20 else 0).getbbox()
        X0, Y0, X1, Y1 = 120 * S, y0 - 150 * S, (W - 120) * S, y1 + 150 * S
        sh = Image.new("RGBA", base.size, (10, 10, 6, 0)); m = Image.new("L", base.size, 0)
        m.paste(255, (X0 + 14, Y0 + 30, X1 + 14, Y1 + 30)); sh.putalpha(m.point(lambda v: int(v * .6)))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(40)))
        card = BE[None, None] * card_tex[Y0:Y1, X0:X1, None]
        base.paste(Image.fromarray(np.clip(card, 0, 255).astype(np.uint8)).convert("RGBA"), (X0, Y0))
        base.alpha_composite(txt)
        base.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, f"{name}_polosy_{'C' if i % 2 == 0 else 'D'}.jpg"), quality=95)
        print(name)
