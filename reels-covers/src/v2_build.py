"""Обложки v2: шаблоны в стиле референсов (полароид с зажимом, фото со скрепкой, блокнот на спирали).
Общая сетка текста на всех обложках. Холст 1080×1920 CSS → рендер ×2 = 2160×3840."""
import os, json, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v2")
os.makedirs(OUT, exist_ok=True)
BEIGE, GREEN, ORANGE = "#d2cec3", "#415038", "#da5200"

# ---- единая сетка (CSS px) ----
Y_BRAND = 330          # @WeTalk.Ru
PHOTO_TOP, PHOTO_BOT = 420, 1190   # зона фото-объекта
Y_NUM = 1236           # (37)
Y_TITLE = 1290         # 2 строки × 108
Y_LEVEL = 1530         # // A2-B1 Level

CSS = f"""
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_boldinclined.ttf);font-weight:700;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{background:var(--bg);color:var(--ink);font-family:T;position:relative}}
body:before{{content:"";position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;
 background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .45 0 0 0 0 .4 0 0 0 .5 0'/></filter><rect width='400' height='400' filter='url(%23n)'/></svg>")}}
.t{{position:absolute;left:0;width:100%;text-align:center;white-space:nowrap}}
.brand{{top:{Y_BRAND}px;font-style:italic;font-size:44px;color:var(--brand)}}
.num{{top:{Y_NUM}px;font-size:38px;color:var(--soft)}}
.title{{top:{Y_TITLE}px;font-style:italic;font-weight:700;font-size:104px;line-height:108px}}
.level{{top:{Y_LEVEL}px;font-style:italic;font-size:50px;color:var(--soft)}}
.obj{{position:absolute;left:50%;transform:translateX(-50%)}}
.shadow{{box-shadow:0 18px 40px rgba(0,0,0,.28),0 4px 10px rgba(0,0,0,.18)}}
/* полароид */
.pola{{top:{PHOTO_TOP+40}px;width:600px;height:730px;background:#f4f1ea;padding:28px 28px 92px}}
.pola img{{width:100%;height:100%;object-fit:cover;display:block}}
.clip{{top:{PHOTO_TOP-30}px;width:190px;height:150px;z-index:3}}
/* фото с рваным краем + скрепка */
.deck{{top:{PHOTO_TOP+10}px;width:610px;height:760px;background:#f1ede4;padding:22px;transform:translateX(-50%) rotate(-2.2deg)}}
.deck img{{width:100%;height:100%;object-fit:cover;display:block}}
.pclip{{top:{PHOTO_TOP-20}px;left:calc(50% + 150px);width:90px;height:230px;z-index:3;transform:rotate(8deg)}}
/* блокнот на спирали */
.book{{top:{PHOTO_TOP+40}px;width:740px;height:730px;background:#f4f1ea;padding:70px 40px 40px}}
.book img{{width:100%;height:100%;object-fit:cover;display:block}}
.rings{{top:{PHOTO_TOP+8}px;width:700px;height:70px;z-index:3}}
"""

CLIP = """<svg class="obj clip" viewBox="0 0 190 150"><defs>
<linearGradient id="m" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#e9e9e9"/><stop offset=".45" stop-color="#9a9a9a"/><stop offset=".7" stop-color="#d6d6d6"/><stop offset="1" stop-color="#6f6f6f"/></linearGradient>
<linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="#777"/><stop offset=".5" stop-color="#eee"/><stop offset="1" stop-color="#777"/></linearGradient></defs>
<path d="M60 70 C55 20 70 6 95 6 C120 6 135 20 130 70" fill="none" stroke="url(#w)" stroke-width="9" stroke-linecap="round"/>
<path d="M75 72 C72 36 82 26 95 26 C108 26 118 36 115 72" fill="none" stroke="url(#w)" stroke-width="7" stroke-linecap="round"/>
<path d="M22 72 H168 L182 138 H8 Z" fill="url(#m)" stroke="#5e5e5e" stroke-width="2"/>
<rect x="8" y="132" width="174" height="10" rx="3" fill="#4d4d4d"/></svg>"""

PCLIP = """<svg class="obj pclip" viewBox="0 0 90 230"><defs><linearGradient id="p" x1="0" x2="1"><stop offset="0" stop-color="#8d8d8d"/><stop offset=".5" stop-color="#f2f2f2"/><stop offset="1" stop-color="#8d8d8d"/></linearGradient></defs>
<path d="M30 200 V40 a22 22 0 0 1 44 0 V190 a30 30 0 0 1 -60 0 V60 a14 14 0 0 1 28 0 V170" fill="none" stroke="url(#p)" stroke-width="6" stroke-linecap="round"/></svg>"""

def RINGS():
    s = ['<svg class="obj rings" viewBox="0 0 700 70">',
         '<defs><linearGradient id="r" x1="0" x2="1"><stop offset="0" stop-color="#555"/><stop offset=".5" stop-color="#ddd"/><stop offset="1" stop-color="#444"/></linearGradient></defs>']
    for i in range(22):
        x = 20 + i * 31
        s.append(f'<circle cx="{x+6}" cy="52" r="7" fill="#2b2b2b" opacity=".75"/>'
                 f'<path d="M{x} 54 C{x} 6 {x+14} 6 {x+14} 30" fill="none" stroke="url(#r)" stroke-width="5" stroke-linecap="round"/>')
    return "".join(s) + "</svg>"

THEMES = {
    "beige": dict(bg=BEIGE, ink=GREEN, brand=ORANGE, soft="rgba(65,80,56,.85)"),
    "green": dict(bg=GREEN, ink=BEIGE, brand=BEIGE, soft="rgba(210,206,195,.85)"),
}

def page(kind, tpl, theme, photo, num, level):
    t = THEMES[theme]
    vars_ = ";".join(f"--{k}:{v}" for k, v in t.items())
    title = ("Podcast", "by our student") if kind == "podcast" else ("What’s in", "my bag?")
    img = f'<img src="file://{photo}">'
    obj = {"pola": f'<div class="obj pola shadow">{img}</div>{CLIP}',
           "deck": f'<div class="obj deck shadow">{img}</div>{PCLIP}',
           "book": f'<div class="obj book shadow">{img}</div>{RINGS()}'}[tpl]
    e = html.escape
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{{vars_}}}{CSS}</style></head><body>
<div class="t brand">@WeTalk.Ru</div>{obj}
<div class="t num">{e(num)}</div>
<div class="t title">{e(title[0])}<br>{e(title[1])}</div>
<div class="t level">{e(level)}</div></body></html>"""

if __name__ == "__main__":
    P = os.path.join(ROOT, "v2", "ph")
    samples = [
        ("s1_podcast_polaroid", "podcast", "pola", "beige", f"{P}/a.jpg", "(37)", "// A2-B1 Level"),
        ("s2_podcast_skrepka", "podcast", "deck", "green", f"{P}/b.jpg", "(30)", "// B1-B2 Level"),
        ("s3_bag_bloknot", "bag", "book", "beige", f"{P}/c.jpg", "(47)", "// by our student"),
    ]
    for name, *args in samples:
        open(os.path.join(OUT, name + ".html"), "w").write(page(*args))
    json.dump([{"name": s[0]} for s in samples], open(os.path.join(OUT, "items.json"), "w"))
    print("ok")
