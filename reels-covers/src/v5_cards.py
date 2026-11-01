"""v5 — крупная реалистичная бумажная карточка по центру на фото (3:4, 1080×1440, рендер ×2)."""
import os, html, subprocess, sys, urllib.parse
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v5"); os.makedirs(OUT, exist_ok=True)
GREEN, ORANGE, BEIGE = "#415038", "#da5200", "#d2cec3"
W, H = 1080, 1440
CW, CH = 830, 1030
PAPER = os.path.join(OUT, "paper.jpg")
if not os.path.exists(PAPER):
    subprocess.run([sys.executable, os.path.join(ROOT, "src", "paper_texture.py"), PAPER, "2400"], check=True)


def scallop(w, h, r, inset):
    x, y, ww, hh = inset, inset, w - 2 * inset, h - 2 * inset
    nx, ny = round(ww / (2 * r)), round(hh / (2 * r)); sx, sy = ww / nx, hh / ny; rr = min(sx, sy) / 2 + 1
    c = [(x + i * sx, y) for i in range(nx + 1)] + [(x + i * sx, y + hh) for i in range(nx + 1)]
    c += [(x, y + j * sy) for j in range(1, ny)] + [(x + ww, y + j * sy) for j in range(1, ny)]
    return f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" fill="#fff"/>' + "".join(
        f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{rr:.1f}" fill="#fff"/>' for a, b in c), c


def mask(kind):
    w, h = CW, CH
    if kind == "scallop":
        body, _ = scallop(w, h, 30, 32)
    elif kind == "lace":
        body, _ = scallop(w, h, 24, 28)
        ring = scallop(w, h, 18, 64)[1]
        body += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="6" fill="#000"/>' for a, b in ring)
    elif kind == "arch":
        r = w / 2
        body = f'<path d="M0 {h} V{r} A{r} {r} 0 0 1 {w} {r} V{h} Z" fill="#fff"/>'
    elif kind == "punched":
        body = f'<rect width="{w}" height="{h}" fill="#fff"/>' + "".join(
            f'<circle cx="50" cy="{86 + i * 78}" r="16" fill="#000"/>' for i in range(13))
    else:
        body = f'<rect width="{w}" height="{h}" fill="#fff"/>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs><mask id="k" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">{body}</mask></defs>'
           f'<rect width="{w}" height="{h}" fill="#fff" mask="url(#k)"/></svg>')
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def deco(kind):
    w, h = CW, CH
    if kind == "scallop":
        return f'<div class="ln" style="inset:78px"></div>'
    if kind == "lace":
        return f'<div class="ln" style="inset:104px"></div>'
    if kind == "arch":
        r = w / 2 - 34
        return (f'<svg class="dv" viewBox="0 0 {w} {h}"><path d="M34 {h-34} V{w/2} A{r} {r} 0 0 1 {w-34} {w/2} V{h-34} Z" '
                f'fill="none" stroke="{GREEN}" stroke-opacity=".45" stroke-width="2"/></svg>')
    if kind == "punched":
        ls = "".join(f'<line x1="120" x2="{w-40}" y1="{150+i*58}" y2="{150+i*58}"/>' for i in range(16))
        return (f'<svg class="dv" viewBox="0 0 {w} {h}"><g stroke="{BEIGE}" stroke-width="2.4">{ls}</g>'
                f'<line x1="112" x2="112" y1="0" y2="{h}" stroke="{BEIGE}" stroke-width="3.5"/></svg>')
    if kind == "stripes":
        return f'<div class="stp"></div><div class="inner"></div>'
    return ""


CSS = f"""
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:T;background:#222}}
.ph{{position:absolute;inset:0;background-size:cover;background-position:center}}
.wrap{{position:absolute;left:{(W-CW)/2}px;top:{(H-CH)/2}px;width:{CW}px;height:{CH}px;
 filter:drop-shadow(0 2px 2px rgba(0,0,0,.35)) drop-shadow(0 26px 34px rgba(0,0,0,.30))}}
.card{{position:absolute;inset:0;background:url(file://{PAPER}) center/1200px;-webkit-mask:var(--m) center/100% 100% no-repeat;mask:var(--m) center/100% 100% no-repeat}}
.card:after{{content:"";position:absolute;inset:0;background:linear-gradient(125deg,rgba(255,255,255,.18),rgba(255,255,255,0) 40%,rgba(0,0,0,.05) 100%)}}
.ln{{position:absolute;border:2px solid {GREEN};opacity:.42}}
.dv{{position:absolute;inset:0;width:100%;height:100%}}
.stp{{position:absolute;inset:0;background:repeating-linear-gradient(90deg,{BEIGE} 0 22px,transparent 22px 44px);opacity:.95}}
.inner{{position:absolute;inset:86px 76px;background:url(file://{PAPER}) 30% 40%/1200px;box-shadow:0 1px 2px rgba(0,0,0,.25),0 10px 22px rgba(0,0,0,.18)}}
.tx{{mix-blend-mode:multiply;position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{GREEN}}}
.b{{color:{ORANGE};font-style:italic;font-size:46px}}
.t{{font-size:108px;letter-spacing:7px;line-height:1;margin-top:44px}}
.i{{font-style:italic;font-size:84px;line-height:1.05;margin-top:10px}}
.p{{font-size:40px;letter-spacing:2px;margin-top:46px}}
"""


def page(photo, kind, rubric, num, level, rot, dx=0, dy=0):
    t = ('<div class="t">PODCAST</div><div class="i">by our student</div>' if rubric == "podcast"
         else '<div class="i" style="font-size:112px;margin-top:40px">What’s in<br>my bag?</div>')
    e = html.escape
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="ph" style="background-image:url(file://{photo})"></div>
<div class="wrap" style="transform:rotate({rot}deg)"><div class="card" style="--m:url('{mask(kind)}')">{deco(kind)}</div>
<div class="tx" style="transform:translate({dx}px,{dy}px)"><div class="b">@WeTalk.Ru</div>{t}<div class="p">{e(num)} &nbsp;·&nbsp; {e(level)}</div></div></div>
</body></html>"""


if __name__ == "__main__":
    U = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13"
    P = os.path.join(ROOT, "v4", "ph")
    S = [("d1_volna", "scallop", "f50a214e", "podcast", "(37)", "A2-B1 Level", -1.2, 0, 0),
         ("d2_arka", "arch", "ebe280e1", "bag", "(47)", "by our student", 0.8, 0, 90),
         ("d3_azhur", "lace", "636e13bc", "podcast", "(16)", "B1-B2 Level", 1.0, 0, 0),
         ("d4_tetrad", "punched", "85387ce9", "bag", "(44)", "by our student", -1.0, 40, 0),
         ("d5_poloska", "stripes", "1cdd24a5", "podcast", "(9)", "0-A1 Level", 0.6, 0, 0)]
    for name, kind, pid, rub, num, lvl, rot, dx, dy in S:
        open(f"{OUT}/{name}.html", "w").write(page(f"{P}/{pid}.jpg", kind, rub, num, lvl, rot, dx, dy))
    print("ok")
