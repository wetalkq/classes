"""Все 60 обложек v2. Шахматка: (r+c) чётное → обложка с фото, нечётное → листок с зажимом."""
import os, sys, json, html, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import REELS
import v2_build as B

ROOT = B.ROOT
U = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13"
OUT = os.path.join(ROOT, "v2full"); PH = os.path.join(OUT, "ph")
os.makedirs(PH, exist_ok=True)

# 30 фото в порядке появления в ленте (чередуем олива / коричневый / нейтральный)
PHOTOS = ["a582ad4e", "f50a214e", "38779c67", "eb1025f3", "387e0534", "dbb02000", "ce64ee2f",
          "1cdd24a5", "3a12a672", "62180978", "103875d7", "779fd367", "ee305f34", "6998d97e",
          "ebe280e1", "61531651", "b5e6f2e0", "85387ce9", "93414a44", "636e13bc", "f87941ba",
          "60b88bb9", "00485080", "5629baa1", "7ad957ee", "9b22d97e", "3ed5d9fc", "11851dde",
          "3188b3cc", "b244f84d"]
BAGLIKE = {"38779c67", "ce64ee2f", "103875d7", "ebe280e1", "93414a44", "f87941ba", "7ad957ee", "11851dde", "b244f84d"}
TPL_SIZE = {"pola": (1088, 1220), "deck": (1132, 1476), "book": (1320, 1240)}

NOTE_CSS = """
.note{top:470px;width:600px;height:700px;background:#f6f3ec;
 background-image:linear-gradient(rgba(65,80,56,.10) 2px,transparent 2px),linear-gradient(90deg,rgba(65,80,56,.10) 2px,transparent 2px);
 background-size:40px 40px;background-position:-2px -2px}
.note .in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#415038;font-family:T}
.bar{width:420px;height:4px;background:rgba(65,80,56,.35);position:relative;margin-top:10px}
.bar b{position:absolute;left:0;top:0;height:4px;background:#415038}
.bar i{position:absolute;top:-9px;width:22px;height:22px;border-radius:50%;background:#415038}
.ctl{margin-top:54px;display:flex;gap:70px}
.lst{font-style:italic;font-size:46px;line-height:86px;text-align:left}
.lst span{display:inline-block;width:250px;border-bottom:2px solid rgba(65,80,56,.45);margin-left:16px;transform:translateY(-12px)}
.q{font-style:italic;font-size:150px;line-height:1;height:110px}
.qt{font-style:italic;font-size:54px;margin-top:40px}
"""
CTL = """<svg width="300" height="44" viewBox="0 0 300 44" fill="#415038">
<rect x="10" y="6" width="6" height="32"/><path d="M60 6 L20 22 L60 38Z"/>
<rect x="132" y="6" width="12" height="32"/><rect x="156" y="6" width="12" height="32"/>
<path d="M240 6 L280 22 L240 38Z"/><rect x="284" y="6" width="6" height="32"/></svg>"""


def texts(d):
    num = f"({d['num']})" if d.get("num") else ""
    if d["kind"] == "bag":
        return "bag", num, d.get("level") and "// " + d["level"] or "// by our student"
    if d["kind"] == "special" and "Отзыв" in d["title"][0]:
        return "feedback", num, "// Madina Alieva" if "Мадина" in d.get("quote", "") else "// our students"
    lvl = d.get("level") or d.get("place")
    return "podcast", num, "// " + lvl if lvl else "// English Podcast"


def head(theme):
    t = B.THEMES[theme]
    return "<!doctype html><html><head><meta charset='utf-8'><style>:root{%s}%s%s</style></head><body>" % (
        ";".join(f"--{k}:{v}" for k, v in t.items()), B.CSS, NOTE_CSS)


def tail(kind, num, level):
    title = {"podcast": ("Podcast", "by our student"), "bag": ("What’s in", "my bag?"),
             "feedback": ("Feedback", "by our student")}[kind]
    e = html.escape
    return (f'<div class="t num">{e(num)}</div><div class="t title">{e(title[0])}<br>{e(title[1])}</div>'
            f'<div class="t level">{e(level)}</div></body></html>')


items, pi = [], 0
for i, d in enumerate(REELS, 1):
    kind, num, level = texts(d)
    photo_slot = (d["r"] + d["c"]) % 2 == 0
    if photo_slot:
        pid = PHOTOS[pi]; pi += 1
        tpl = "book" if (kind == "bag" or pid in BAGLIKE) and kind != "feedback" else ("pola", "deck")[pi % 2]
        theme = "green" if tpl == "deck" else "beige"
        w, h = TPL_SIZE[tpl]
        dst = f"{PH}/{i:02d}_{pid}.jpg"
        if not os.path.exists(dst):
            subprocess.run([sys.executable, os.path.join(ROOT, "src", "v2_prep.py"), f"{U}/{pid}-image.jpg", dst, str(w), str(h), "0.4"], check=True)
        img = f'<img src="file://{dst}">'
        obj = {"pola": f'<div class="obj pola shadow">{img}</div>{B.CLIP}',
               "deck": f'<div class="obj deck shadow">{img}</div>{B.PCLIP}',
               "book": f'<div class="obj book shadow">{img}</div>{B.RINGS()}'}[tpl]
    else:
        tpl, pid = "note", None
        theme = "green" if kind == "podcast" else "beige"
        if kind == "podcast":
            p = 18 + ((d.get("num") or 7) * 37) % 60
            inner = (f'<div class="bar"><b style="width:{p}%"></b><i style="left:calc({p}% - 11px)"></i></div>'
                     f'<div class="ctl">{CTL}</div>')
        elif kind == "bag":
            inner = '<div class="lst">' + "".join(f"({k:02d})<span></span><br>" for k in range(1, 7)) + "</div>"
        else:
            inner = '<div class="q">“</div><div class="qt">Madina Alieva</div>'
        obj = f'<div class="obj note shadow"><div class="in">{inner}</div></div>' + B.CLIP.replace(
            'class="obj clip"', 'class="obj clip" style="top:400px"')
    name = f"{i:02d}_ряд{d['r']+1:02d}-{d['c']+1}_{kind}" + (f"-{d['num']:02d}" if d.get("num") else "")
    open(f"{OUT}/{name}.html", "w").write(head(theme) + '<div class="t brand">@WeTalk.Ru</div>' + obj + tail(kind, num, level))
    items.append(dict(name=name, r=d["r"], c=d["c"], tpl=tpl, photo=pid))

json.dump(items, open(f"{OUT}/items.json", "w"), ensure_ascii=False, indent=1)
print(len(items), "covers,", pi, "photos")
