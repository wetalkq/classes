"""v4 — фото на весь кадр + бумажная карточка по центру с фигурными краями (3:4, 1080×1440, рендер ×2)."""
import os, math, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v4"); os.makedirs(OUT, exist_ok=True)
GREEN, ORANGE, BEIGE, PAPER = "#415038", "#da5200", "#d2cec3", "#f7f4ee"
W, H = 1080, 1440
CW, CH = 640, 760                      # размер карточки
X0, Y0 = (W - CW) / 2, (H - CH) / 2    # ровно по центру

DEFS = f"""<defs>
<filter id="paper" x="-10%" y="-10%" width="120%" height="120%">
 <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="4" result="n"/>
 <feColorMatrix in="n" values="0 0 0 0 .35  0 0 0 0 .32  0 0 0 0 .28  0 0 0 .10 0" result="g"/>
 <feComposite in="g" in2="SourceAlpha" operator="in" result="gi"/>
 <feMerge result="m"><feMergeNode in="SourceGraphic"/><feMergeNode in="gi"/></feMerge>
 <feDropShadow in="m" dx="0" dy="16" stdDeviation="18" flood-color="#000" flood-opacity=".32"/>
</filter></defs>"""


def scallop_circles(x, y, w, h, r):
    c = []
    nx, ny = round(w / (2 * r)), round(h / (2 * r))
    sx, sy = w / nx, h / ny
    for i in range(nx + 1):
        c += [(x + i * sx, y), (x + i * sx, y + h)]
    for j in range(1, ny):
        c += [(x, y + j * sy), (x + w, y + j * sy)]
    return c, min(sx, sy) / 2


def shape(kind):
    x, y, w, h = X0, Y0, CW, CH
    if kind == "scallop":       # волнистый край
        pts, r = scallop_circles(x + 20, y + 20, w - 40, h - 40, 26)
        body = f'<rect x="{x+20}" y="{y+20}" width="{w-40}" height="{h-40}" fill="{PAPER}"/>' + "".join(
            f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r+1:.1f}" fill="{PAPER}"/>' for a, b in pts)
        inner = f'<rect x="{x+56}" y="{y+56}" width="{w-112}" height="{h-112}" fill="none" stroke="{GREEN}" stroke-opacity=".45" stroke-width="2"/>'
        return f'<g filter="url(#paper)">{body}</g>{inner}'
    if kind == "zigzag":        # край «зигзаг» (ножницы-зубчики)
        t, p = 18, []
        def edge(ax, ay, bx, by, n, ox, oy):
            for i in range(n):
                f0, f1 = i / n, (i + .5) / n
                p.append((ax + (bx - ax) * f0, ay + (by - ay) * f0))
                p.append((ax + (bx - ax) * f1 + ox, ay + (by - ay) * f1 + oy))
        edge(x, y, x + w, y, 32, 0, -t); edge(x + w, y, x + w, y + h, 38, t, 0)
        edge(x + w, y + h, x, y + h, 32, 0, t); edge(x, y + h, x, y, 38, -t, 0)
        d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in p) + " Z"
        return f'<path d="{d}" fill="{PAPER}" filter="url(#paper)"/>'
    if kind == "arch":          # арка как зеркало
        r = w / 2
        d = f"M{x} {y+h} V{y+r} A{r} {r} 0 0 1 {x+w} {y+r} V{y+h} Z"
        r2 = r - 26
        d2 = f"M{x+26} {y+h-26} V{y+r} A{r2} {r2} 0 0 1 {x+w-26} {y+r} V{y+h-26} Z"
        return (f'<path d="{d}" fill="{PAPER}" filter="url(#paper)"/>'
                f'<path d="{d2}" fill="none" stroke="{GREEN}" stroke-opacity=".5" stroke-width="2"/>')
    if kind == "lace":          # ажурная салфетка: волнистый край + дырочки
        pts, r = scallop_circles(x + 24, y + 24, w - 48, h - 48, 22)
        holes = "".join(f'<circle cx="{a + (0 if a in (x+24, x+w-24) else 0):.1f}" cy="{b:.1f}" r="5" fill="#000"/>' for a, b in pts)
        # дырочки чуть внутрь от края
        ring, _ = scallop_circles(x + 54, y + 54, w - 108, h - 108, 16)
        holes = "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="5.5" fill="#000"/>' for a, b in ring)
        body = f'<rect x="{x+24}" y="{y+24}" width="{w-48}" height="{h-48}" fill="#fff"/>' + "".join(
            f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r+1:.1f}" fill="#fff"/>' for a, b in pts)
        return (f'<mask id="lm">{body}{holes}</mask>'
                f'<g filter="url(#paper)"><rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}" mask="url(#lm)"/></g>'
                f'<rect x="{x+82}" y="{y+82}" width="{w-164}" height="{h-164}" fill="none" stroke="{GREEN}" stroke-opacity=".35" stroke-width="2"/>')
    if kind == "punched":       # лист с дырочками от дырокола и линовкой
        holes = "".join(f'<circle cx="{x+44}" cy="{y+70+i*62}" r="13" fill="#000"/>' for i in range(11))
        lines = "".join(f'<line x1="{x+90}" x2="{x+w-30}" y1="{y+110+i*46}" y2="{y+110+i*46}" stroke="{BEIGE}" stroke-width="2"/>' for i in range(14))
        return (f'<mask id="pm"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>{holes}</mask>'
                f'<g filter="url(#paper)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}" mask="url(#pm)"/></g>'
                f'<line x1="{x+84}" x2="{x+84}" y1="{y}" y2="{y+h}" stroke="{BEIGE}" stroke-width="3"/>{lines}')
    if kind == "stripes":       # паспарту в бежевую полоску + белая карточка
        st = "".join(f'<rect x="{x + i*32}" y="{y}" width="16" height="{h}" fill="{BEIGE}"/>' for i in range(int(w / 32) + 1))
        return (f'<clipPath id="sc"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
                f'<g filter="url(#paper)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/></g>'
                f'<g clip-path="url(#sc)">{st}</g>'
                f'<rect x="{x+58}" y="{y+70}" width="{w-116}" height="{h-140}" fill="{PAPER}" filter="url(#paper)"/>')
    raise ValueError(kind)


CSS = f"""
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:T}}
.ph{{position:absolute;inset:0;background-size:cover;background-position:center}}
svg{{position:absolute;inset:0}}
.tx{{position:absolute;left:0;right:0;top:{Y0}px;height:{CH}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{GREEN}}}
.b{{color:{ORANGE};font-style:italic;font-size:36px}}
.t{{font-size:80px;letter-spacing:5px;line-height:1;margin-top:34px}}
.i{{font-style:italic;font-size:64px;line-height:1.05;margin-top:8px}}
.p{{font-size:32px;letter-spacing:2px;margin-top:34px}}
"""


def page(photo, kind, rubric, num, level, dy=0):
    if rubric == "podcast":
        t = '<div class="t">PODCAST</div><div class="i">by our student</div>'
    else:
        t = '<div class="i" style="font-size:84px;margin-top:30px">What’s in<br>my bag?</div>'
    e = html.escape
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="ph" style="background-image:url(file://{photo})"></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{shape(kind)}</svg>
<div class="tx" style="transform:translate({ 30 if kind=='punched' else 0}px,{dy}px)"><div class="b">@WeTalk.Ru</div>{t}<div class="p">{e(num)} &nbsp;·&nbsp; {e(level)}</div></div>
</body></html>"""


if __name__ == "__main__":
    U = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13"
    P = os.path.join(OUT, "ph"); os.makedirs(P, exist_ok=True)
    S = [("c1_volna", "scallop", "f50a214e", "podcast", "(37)", "A2-B1 Level", 0),
         ("c2_zigzag", "zigzag", "eb1025f3", "podcast", "(30)", "B1-B2 Level", 0),
         ("c3_arka_zerkalo", "arch", "ebe280e1", "bag", "(47)", "by our student", 60),
         ("c4_azhur", "lace", "636e13bc", "podcast", "(16)", "B1-B2 Level", 0),
         ("c5_dyrokol", "punched", "85387ce9", "bag", "(44)", "by our student", 0),
         ("c6_poloska", "stripes", "1cdd24a5", "podcast", "(9)", "0-A1 Level", 0)]
    import subprocess, sys
    for name, kind, pid, rub, num, lvl, dy in S:
        ph = f"{P}/{pid}.jpg"
        if not os.path.exists(ph):
            subprocess.run([sys.executable, os.path.join(ROOT, "src", "v2_prep.py"), f"{U}/{pid}-image.jpg", ph, "2160", "2880", "0.4"], check=True)
        open(f"{OUT}/{name}.html", "w").write(page(ph, kind, rub, num, lvl, dy))
    print("ok")
