"""Генерирует HTML для каждой обложки. Рендер — render.js (Playwright), потом post.py."""
import json, os, html
from data import REELS, BEIGE, GREEN, ORANGE

OUT = os.path.join(os.path.dirname(__file__), "..", "build")
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FONT_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

CSS = """
@font-face{font-family:TNR;src:url(file://%s);font-style:italic}
@font-face{font-family:TNRr;src:url(file://%s)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px}
body{background:var(--bg);color:var(--ink);font-family:TNR,serif;font-style:italic;
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;position:relative}
/* сетка профиля показывает центр 3:4 (y 240–1680) — всё держим в нём */
.brand{position:absolute;top:470px;width:100%%;font-size:46px;color:#DA5200;letter-spacing:.5px}
.handle{position:absolute;top:1440px;width:100%%;font-family:TNRr;font-style:normal;font-size:30px;letter-spacing:6px;color:var(--soft)}
.num{font-family:TNRr;font-style:normal;font-size:44px;color:var(--soft);margin-bottom:34px}
.meta{font-family:TNRr;font-style:normal;font-size:34px;letter-spacing:7px;text-transform:uppercase;color:var(--soft);margin-bottom:38px}
h1{font-weight:400;font-size:150px;line-height:1.02;letter-spacing:-2px}
.sub{font-size:62px;margin-top:40px;color:var(--soft)}
.bar{width:560px;height:3px;background:var(--line);margin-top:70px;position:relative}
.bar i{position:absolute;left:0;top:-9px;width:21px;height:21px;border-radius:50%%;background:#DA5200}
.bar b{position:absolute;left:0;top:0;height:3px;width:var(--p);background:#DA5200}
.q{text-wrap:balance;font-size:60px;margin-top:44px;max-width:860px;line-height:1.25;color:var(--soft)}
""" % (FONT, FONT_R)


def theme(r, c):
    # шахматный порядок по позиции в сетке
    return "green" if (r + c) % 2 == 0 else "beige"


def body(d):
    e = html.escape
    num = f'<div class="num">({d["num"]})</div>' if d.get("num") else ""
    if d["kind"] == "podcast":
        meta = f'<div class="meta">( WeTalk / {e(d["place"])} )</div>' if d.get("place") and d.get("level") else \
               f'<div class="meta">( {e(d.get("top","by our student"))} )</div>'
        sub_txt = []
        if d.get("level"):
            sub_txt.append("// " + d["level"])
        elif d.get("place"):
            sub_txt.append(d["place"])
        sub = f'<div class="sub">{e(sub_txt[0])}</div>' if sub_txt else ""
        p = 18 + ((d.get("num") or 7) * 37) % 60
        return f'{num}{meta}<h1>New Podcast</h1>{sub}<div class="bar" style="--p:{p}%"><b></b><i style="left:calc({p}% - 10px)"></i></div>'
    if d["kind"] == "bag":
        sub = f'<div class="sub">// {e(d["level"])}</div>' if d.get("level") else '<div class="sub">by our student</div>'
        return f'{num}<div class="meta">( WeTalk / Series )</div><h1>What’s in<br>my bag?</h1>{sub}'
    # special
    t = "<br>".join(e(x) for x in d["title"])
    return f'<div class="meta">( WeTalk / Student )</div><h1>{t}</h1><div class="q">{e(d["quote"])}</div>'


items = []
for i, d in enumerate(REELS, 1):
    th = theme(d["r"], d["c"])
    if th == "green":
        vars_ = f"--bg:{GREEN};--ink:{BEIGE};--soft:rgba(217,211,199,.78);--line:rgba(217,211,199,.45)"
    else:
        vars_ = f"--bg:{BEIGE};--ink:{GREEN};--soft:rgba(67,82,59,.8);--line:rgba(67,82,59,.35)"
    label = d["kind"] + (f"-{d['num']:02d}" if d.get("num") else "")
    name = f"{i:02d}_r{d['r']+1:02d}c{d['c']+1}_{label}"
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{{vars_}}}{CSS}</style></head>
<body><div class="brand">( WeTalk.Ru )</div>{body(d)}<div class="handle">@WETALK.RU</div></body></html>"""
    with open(os.path.join(OUT, name + ".html"), "w") as f:
        f.write(page)
    items.append(dict(name=name, theme=th, **d))

json.dump(items, open(os.path.join(OUT, "items.json"), "w"), ensure_ascii=False, indent=1)
print(len(items), "pages")
