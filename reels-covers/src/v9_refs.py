"""v9 — 1:1 по трём референсам: «Drank coffee outside», «Drinking coffee together» (марка), «The Brief Edit» (9 плиток).
Только Times New Roman. Цвета бренда. 3:4, 1080×1440, рендер ×2."""
import os, html, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
F = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v9"); os.makedirs(OUT, exist_ok=True)
PH = os.path.join(OUT, "ph"); os.makedirs(PH, exist_ok=True)
U = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13"
PAPER = os.path.join(ROOT, "v5", "paper.jpg")
GREEN, BEIGE, CREAM, ORANGE = "#415038", "#d2cec3", "#f6f2ea", "#da5200"


def photo(pid, w=2160, h=2880, fy=0.45):
    dst = f"{PH}/{pid}_{w}x{h}.jpg"
    if not os.path.exists(dst):
        subprocess.run([sys.executable, os.path.join(ROOT, "src", "v2_prep.py"), f"{U}/{pid}-image.jpg", dst, str(w), str(h), str(fy)], check=True)
    return dst


BASE = f"""
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt_bold.ttf);font-weight:700;font-style:normal}}
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt_boldinclined.ttf);font-weight:700;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;overflow:hidden;font-family:T}}
.a{{position:absolute}} .c{{left:0;right:0;text-align:center}}
.bg{{background-size:cover;background-position:center}} .fill{{inset:0}}
.grain{{position:absolute;inset:0;background:url(file://{PAPER}) center/900px;mix-blend-mode:multiply;opacity:.45}}
.sh{{box-shadow:0 2px 3px rgba(0,0,0,.22),0 16px 28px rgba(0,0,0,.22)}}
.lock{{display:flex;align-items:center;justify-content:center;gap:18px;white-space:nowrap}}
.lock .s{{font-size:var(--ss);letter-spacing:.12em}} .lock .i{{font-style:italic;font-size:var(--si);line-height:1}}
"""
def doc(css, body): return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{body}</body></html>"
def lock(a, b, c, ss, si, color): return f'<div class="lock" style="--ss:{ss}px;--si:{si}px;color:{color}"><span class="s">{a}</span><span class="i">{b}</span><span class="s">{c}</span></div>'
def mono(size, color): return f'<span style="font-style:italic;font-size:{size}px;color:{color};letter-spacing:-.06em;line-height:1">WT</span>'
STAR = "M50 3 61 37 97 37 68 58 79 93 50 72 21 93 32 58 3 37 39 37Z"
def star(x, y, s, col, rot=0): return f'<svg class="a" style="left:{x}px;top:{y}px;width:{s}px;transform:rotate({rot}deg)" viewBox="0 0 100 100"><path d="{STAR}" fill="{col}"/></svg>'


# ---------- «Drank coffee outside» ----------
def coffee_card():
    p = photo("38779c67", fy=0.5)
    stars = "".join(star(250 + i * 150, 820, 110, GREEN) for i in range(4)) + "".join(star(250 + i * 150, 960, 110, ORANGE) for i in range(4))
    css = f""".c1{{left:230px;top:300px;width:620px;height:400px;background:{GREEN}}}
.c2{{left:230px;top:730px;width:620px;height:430px;background:{BEIGE}}}
.t1{{left:230px;top:300px;width:620px;height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{CREAM};text-align:center}}
.t1 .i{{font-style:italic;font-size:120px;line-height:1}} .t1 .s{{font-size:34px;letter-spacing:6px;margin-top:18px}}
.t2{{left:250px;width:580px;top:1080px;color:{GREEN};font-size:30px;letter-spacing:2px;line-height:1.3;text-align:center}}
.sig{{right:70px;bottom:60px;color:{CREAM};font-style:italic;font-size:44px;text-shadow:0 1px 8px rgba(0,0,0,.4)}}"""
    return doc(css, f"""<div class="a fill bg" style="background-image:url(file://{p})"></div>
<div class="a c1 sh"><div class="grain" style="opacity:.3"></div></div><div class="a c2 sh"><div class="grain"></div></div>
<div class="a t1"><div class="i">What’s in<br>my bag?</div><div class="s">BY OUR STUDENT</div></div>
{stars}<div class="a t2">(47) · EVERYTHING INSIDE,<br>IN ENGLISH</div>
{star(80, 640, 110, ORANGE, -12)}{star(880, 560, 110, ORANGE, 10)}{star(900, 800, 100, ORANGE, -6)}{star(690, 1230, 110, ORANGE, 14)}
<div class="a sig">@WeTalk.Ru</div>""")


# ---------- «Drinking coffee together» (марка) ----------
def stamp_mask(w, h, r=13):
    import urllib.parse
    n, m = round(w / (2.6 * r)), round(h / (2.6 * r))
    holes = "".join(f'<circle cx="{w*(i+.5)/n:.1f}" cy="0" r="{r}"/><circle cx="{w*(i+.5)/n:.1f}" cy="{h}" r="{r}"/>' for i in range(n))
    holes += "".join(f'<circle cx="0" cy="{h*(j+.5)/m:.1f}" r="{r}"/><circle cx="{w}" cy="{h*(j+.5)/m:.1f}" r="{r}"/>' for j in range(m))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><defs><mask id="k"><rect width="{w}" height="{h}" fill="#fff"/>'
           f'<g fill="#000">{holes}</g></mask></defs><rect width="{w}" height="{h}" fill="#fff" mask="url(#k)"/></svg>')
    return "url('data:image/svg+xml;utf8," + urllib.parse.quote(svg) + "')"

def stamp():
    p1 = photo("11851dde", 1000, 640, 0.35); p2 = photo("ce64ee2f", 2160, 1700, 0.5)
    m = stamp_mask(500, 320)
    css = f"""body{{background:url(file://{PAPER}) center/1000px}}
.st{{left:290px;width:500px;height:320px;-webkit-mask:{m} center/100% 100%;mask:{m} center/100% 100%}}
.row{{left:40px;right:40px;top:560px;display:flex;justify-content:space-between;color:{GREEN};font-size:58px}}
.low{{left:0;right:0;top:640px;height:800px}}
.tx{{left:290px;width:500px;top:960px;height:320px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{GREEN};text-align:center}}
.tx .s{{font-size:34px;letter-spacing:5px}} .tx .o{{color:{ORANGE};font-style:italic;font-size:40px;margin-top:16px}}"""
    return doc(css, f"""<div class="a st bg" style="top:130px;background-image:url(file://{p1})"></div>
<div class="a row"><span>Podcast</span><span><i>by our</i></span><span>student</span></div>
<div class="a low bg" style="background-image:url(file://{p2})"></div>
<div class="a st" style="top:960px;background:url(file://{PAPER}) center/900px"></div>
<div class="a tx"><div class="s">(30) · B1-B2 LEVEL</div><div class="o">@WeTalk.Ru</div></div>""")


# ---------- «The Brief Edit» ----------
WORDS = ["Speak", "English", "with", "confidence."]

def b1():  # фото + квадратная плашка (как сумка) с логотипом
    p = photo("dbb02000", fy=0.5)
    css = f""".sq{{left:240px;top:420px;width:600px;height:600px;background:{GREEN}}} .in{{left:240px;top:420px;width:600px;height:600px;display:flex;align-items:center;justify-content:center;text-align:center;color:{CREAM}}}"""
    return doc(css, f"""<div class="a fill bg" style="background-image:url(file://{p})"></div><div class="a sq sh"><div class="grain" style="opacity:.25"></div></div>
<div class="a in"><div><div style="font-size:46px;letter-spacing:10px">WHAT’S IN</div><div style="font-style:italic;font-size:130px;line-height:1">my bag?</div><div style="font-size:30px;letter-spacing:5px;margin-top:28px">(47) · @WETALK.RU</div></div></div>""")

def b2():  # однотонный (голубой→бежевый), монограмма по центру, слова в одну строку
    css = f"""body{{background:{BEIGE}}} .row{{left:40px;right:40px;top:620px;height:200px;display:flex;align-items:center;justify-content:space-between;color:{GREEN};font-size:50px}}"""
    return doc(css, f"""<div class="grain"></div><div class="a row"><span>{WORDS[0]}</span><span>{WORDS[1]}</span>{mono(210, GREEN)}<span>{WORDS[2]}</span><span>{WORDS[3]}</span></div>
<div class="a c" style="bottom:90px;color:{GREEN};font-size:34px;letter-spacing:6px">@WETALK.RU</div>""")

def b3():  # только фото
    p = photo("a582ad4e", fy=0.4)
    return doc("", f'<div class="a fill bg" style="background-image:url(file://{p})"></div>')

def b4():  # фото + монограмма и слова поверх
    p = photo("11851dde", fy=0.5)
    css = f""".sh2{{inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15),rgba(0,0,0,.55) 40%,rgba(0,0,0,.55) 58%,rgba(0,0,0,.15))}} .row{{left:50px;right:50px;top:560px;height:200px;display:flex;align-items:center;justify-content:space-between;color:{CREAM};font-size:50px;text-shadow:0 2px 12px rgba(0,0,0,.6)}}"""
    return doc(css, f"""<div class="a fill bg" style="background-image:url(file://{p})"></div><div class="a sh2"></div>
<div class="a row"><span>{WORDS[0]}</span><span>{WORDS[1]}</span>{mono(200, CREAM)}<span>{WORDS[2]}</span><span>{WORDS[3]}</span></div>""")

def b5():  # кремовый, большой логотип по центру
    css = f"""body{{background:{CREAM}}} .in{{left:0;right:0;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}"""
    return doc(css, f"""<div class="grain"></div><div class="a in">{lock('PODCAST','by our','STUDENT',46,170,GREEN)}
<div style="color:{GREEN};font-size:34px;letter-spacing:6px;margin-top:40px">(30) · B1-B2 LEVEL</div><div style="color:{ORANGE};font-style:italic;font-size:42px;margin-top:22px">@WeTalk.Ru</div></div>""")

def b6():  # полоски (голубые→бежевые) + круглая наклейка
    css = f"""body{{background:repeating-linear-gradient(90deg,{BEIGE} 0 90px,{CREAM} 90px 180px)}}
.dot{{left:290px;top:470px;width:500px;height:500px;border-radius:50%;background:{GREEN};display:flex;flex-direction:column;align-items:center;justify-content:center;color:{CREAM}}}"""
    return doc(css, f"""<div class="grain" style="opacity:.35"></div><div class="a dot sh">{mono(210, CREAM)}<div style="font-size:30px;letter-spacing:6px;margin-top:10px">@WETALK.RU</div></div>""")

def b7():  # узор из монограмм на зелёном
    cells = ""
    for r in range(4):
        xs = [90, 420, 750] if r % 2 == 0 else [255, 585]
        for k, x in enumerate(xs):
            y = 110 + r * 330
            cells += f'<div class="a" style="left:{x}px;top:{y}px">{mono(150, CREAM)}</div>'
            cells += f'<div class="a" style="left:{x+40}px;top:{y+190}px;color:{CREAM};font-size:34px;transform:rotate(-25deg);opacity:.9">{WORDS[(r+k)%4]}</div>'
    return doc(f"body{{background:{GREEN}}}", f'<div class="grain" style="opacity:.3"></div>{cells}')

def b8():  # только фото
    p = photo("636e13bc", fy=0.5)
    return doc("", f'<div class="a fill bg" style="background-image:url(file://{p})"></div>')

def b9():  # фото + логотип и вертикальные слова справа
    p = photo("ebe280e1", fy=0.5)
    css = f""".sh2{{inset:0;background:rgba(0,0,0,.30)}} .lg{{left:0;right:0;top:640px}}
.v{{right:120px;color:{CREAM};font-size:46px;writing-mode:vertical-rl;text-shadow:0 1px 8px rgba(0,0,0,.5)}}"""
    v = "".join(f'<div class="a v" style="top:{90 + i*330}px">{w}</div>' for i, w in enumerate(WORDS))
    return doc(css, f"""<div class="a fill bg" style="background-image:url(file://{p})"></div><div class="a sh2"></div>
<div class="a lg" style="text-shadow:0 2px 12px rgba(0,0,0,.45)">{lock('WE','Talk','.RU',46,170,CREAM)}</div>{v}""")


if __name__ == "__main__":
    pages = {"k1_coffee_card": coffee_card(), "k2_marka": stamp()}
    for i, f in enumerate([b1, b2, b3, b4, b5, b6, b7, b8, b9], 1):
        pages[f"b{i}"] = f()
    for n, h in pages.items():
        open(os.path.join(OUT, n + ".html"), "w").write(h)
    print("ok", len(pages))
