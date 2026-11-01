"""Единая сетка обложек Reels We Talk. Все элементы на фиксированных координатах.
Холст 1080×1920 CSS px, рендер ×2 = 2160×3840 (4K).
Сетка профиля показывает центр 3:4 → y 240–1680: всё внутри.
"""
import json, os, html
from data import REELS, BEIGE, GREEN, ORANGE

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "build")
FONTS = os.path.join(ROOT, "fonts")
os.makedirs(OUT, exist_ok=True)

# ---- Сетка (одинаковая для всех обложек) ----
Y_BRAND = 470    # ( WeTalk.Ru )
Y_NUM   = 640    # (30)
Y_META  = 712    # ( WETALK / MOSCOW )
Y_TITLE = 800    # верх заголовка: всегда 2 строки по 150 px → низ 1100
Y_SUB   = 1150   # // B1-B2 Level
Y_RULE  = 1300   # тонкая линия
Y_HANDLE = 1420  # @WETALK.RU

CSS = f"""
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_bold.ttf);font-weight:700;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_boldinclined.ttf);font-weight:700;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{background:var(--bg);color:var(--ink);font-family:T;position:relative}}
.a{{position:absolute;left:0;width:100%;text-align:center;white-space:nowrap}}
.brand{{top:{Y_BRAND}px;font-style:italic;font-size:46px;line-height:1;color:var(--brand)}}
.num{{top:{Y_NUM}px;font-size:40px;line-height:1;color:var(--soft)}}
.meta{{top:{Y_META}px;font-size:30px;line-height:1;letter-spacing:7px;text-transform:uppercase;color:var(--soft)}}
.title{{top:{Y_TITLE}px;font-style:italic;font-weight:700;font-size:142px;line-height:150px;letter-spacing:-1px}}
.sub{{top:{Y_SUB}px;font-style:italic;font-size:56px;line-height:1.1;color:var(--soft)}}
.rule{{top:{Y_RULE}px;left:270px;width:540px;height:2px;background:var(--line)}}
.rule b{{position:absolute;left:0;top:0;height:2px;background:var(--accent)}}
.rule i{{position:absolute;top:-8px;width:18px;height:18px;border-radius:50%;background:var(--accent)}}
.handle{{top:{Y_HANDLE}px;font-size:28px;line-height:1;letter-spacing:6px;color:var(--soft)}}
"""

THEMES = {
    # на бежевом: текст зелёный, акцент оранжевый
    "beige": dict(bg=BEIGE, ink=GREEN, brand=ORANGE, accent=ORANGE,
                  soft="rgba(65,80,56,.82)", line="rgba(65,80,56,.30)"),
    # на зелёном: БЕЗ оранжевого, всё бежевым
    "green": dict(bg=GREEN, ink=BEIGE, brand=BEIGE, accent=BEIGE,
                  soft="rgba(210,206,195,.82)", line="rgba(210,206,195,.30)"),
}


def theme(r, c):
    return "green" if (r + c) % 2 == 0 else "beige"  # шахматный порядок в сетке


def parts(d):
    """→ num, meta, title(2 строки), sub, progress(None = линия без точки)"""
    num = f"({d['num']})" if d.get("num") else ""
    if d["kind"] == "podcast":
        meta = f"( WeTalk / {d['place']} )" if d.get("place") else "( WeTalk / Student )"
        sub = "// " + d["level"] if d.get("level") else "by our student"
        prog = 18 + ((d.get("num") or 7) * 37) % 60
        return num, meta, ["New", "Podcast"], sub, prog
    if d["kind"] == "bag":
        sub = "// " + d["level"] if d.get("level") else "by our student"
        return num, "( WeTalk / Series )", ["What’s in", "my bag?"], sub, None
    return num, "( WeTalk / Student )", d["title"], d["quote"], None


items = []
for i, d in enumerate(REELS, 1):
    th = theme(d["r"], d["c"])
    t = THEMES[th]
    vars_ = ";".join(f"--{k}:{v}" for k, v in t.items())
    num, meta, title, sub, prog = parts(d)
    e = html.escape
    rule = '<div class="a rule">' + (f'<b style="width:{prog}%"></b><i style="left:calc({prog}% - 9px)"></i>' if prog else "") + "</div>"
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{{vars_}}}{CSS}</style></head><body>
<div class="a brand">( WeTalk.Ru )</div>
<div class="a num">{e(num)}</div>
<div class="a meta">{e(meta)}</div>
<div class="a title">{e(title[0])}<br>{e(title[1])}</div>
<div class="a sub">{e(sub)}</div>
{rule}
<div class="a handle">@WETALK.RU</div>
</body></html>"""
    label = d["kind"] + (f"-{d['num']:02d}" if d.get("num") else "")
    name = f"{i:02d}_ряд{d['r']+1:02d}-{d['c']+1}_{label}"
    open(os.path.join(OUT, name + ".html"), "w").write(page)
    items.append(dict(name=name, theme=th, **d))

json.dump(items, open(os.path.join(OUT, "items.json"), "w"), ensure_ascii=False, indent=1)
print(len(items), "pages")
