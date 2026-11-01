"""v6 — журнальная фирменная лента по референсу (Get Inspired / Getting Inspired / лист на фото / фото + мелкий текст).
3:4, 1080×1440, рендер ×2. Только Times New Roman. Цвета: зелёный, бежевый, белый; оранжевый только на светлом."""
import os, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v6"); os.makedirs(OUT, exist_ok=True)
GREEN, ORANGE, BEIGE, WHITE = "#415038", "#da5200", "#d2cec3", "#f7f4ee"
PAPER = os.path.join(ROOT, "v5", "paper.jpg")
E = html.escape

BASE = f"""
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;overflow:hidden;font-family:T}}
.a{{position:absolute}} .c{{left:0;right:0;text-align:center}}
.cap{{font-size:24px;letter-spacing:6px;text-transform:uppercase}}
.grain{{position:absolute;inset:0;background:url(file://{PAPER}) center/1100px;mix-blend-mode:multiply;opacity:.55}}
.photo{{background-size:cover;background-position:center}}
"""

def doc(css, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{body}</body></html>"

def L1(photo, title, sub, num, bg="green"):
    top = 520 if bg == "green" else 880
    """Однотонный фон, фото в центре, огромный курсив поверх фото (как «Get Inspired»)."""
    ink, lab = (WHITE, WHITE) if bg == "green" else (GREEN, ORANGE)
    css = f"""body{{background:{GREEN if bg=='green' else BEIGE}}}
.ph{{left:270px;top:300px;width:540px;height:720px}}
.big{{top:{top}px;color:{ink};font-style:italic;font-size:250px;line-height:1;letter-spacing:-6px;white-space:nowrap;opacity:.93}}
.t1{{top:110px;color:{lab}}} .t2{{top:{1095 if bg=='green' else 1140}px;color:{ink};font-style:italic;font-size:54px}}
.t3{{top:1185px;color:{ink};font-size:30px;letter-spacing:3px}} .t4{{bottom:90px;color:{ink};opacity:.85}}"""
    return doc(css, f"""<div class="grain"></div><div class="a cap c t1">@WeTalk.Ru</div>
<div class="a ph photo" style="background-image:url(file://{photo})"></div>
<div class="a c big">{E(title)}</div><div class="a c t2">{E(sub)}</div>
<div class="a cap c t4">{E(num)}</div>""")

def L2(photo, l1, l2, sub, num):
    """Белый лист на зелёном фоне, огромный курсив в две строки, маленькое фото между (как «Getting Inspired»)."""
    css = f"""body{{background:{GREEN}}}
.sheet{{left:90px;top:90px;right:90px;bottom:90px;background:url(file://{PAPER}) center/1100px;box-shadow:0 2px 3px rgba(0,0,0,.3),0 24px 40px rgba(0,0,0,.28)}}
.lab{{top:150px;color:{ORANGE}}}
.ph{{left:330px;top:700px;width:420px;height:420px}}
.w1{{top:250px;color:{GREEN};font-style:italic;font-size:210px;line-height:1;letter-spacing:-5px}}
.w2{{top:455px;color:{GREEN};font-style:italic;font-size:210px;line-height:1;letter-spacing:-5px}}
.sub{{top:1170px;color:{GREEN};font-size:30px;letter-spacing:5px;text-transform:uppercase}}
.num{{top:1220px;color:{GREEN};font-style:italic;font-size:40px}}
.bot{{bottom:150px;color:{GREEN};opacity:.8}}"""
    return doc(css, f"""<div class="a sheet"></div><div class="a cap c lab">@WeTalk.Ru</div>
<div class="a ph photo" style="background-image:url(file://{photo});box-shadow:0 1px 2px rgba(0,0,0,.25),0 10px 22px rgba(0,0,0,.18)"></div>
<div class="a c w1">{E(l1)}</div><div class="a c w2">{E(l2)}</div>
<div class="a c sub">{E(sub)}</div><div class="a c num">{E(num)}</div>""")

def L3(photo, title, sub, num):
    """Фото на весь кадр, по центру высокий белый лист с тонкой рамкой (как лист на ноутбуке)."""
    css = f"""body{{background:#222}} .bg{{inset:0}}
.sheet{{left:250px;top:250px;width:580px;height:940px;background:url(file://{PAPER}) center/1100px;transform:rotate(-1deg);
 box-shadow:0 2px 3px rgba(0,0,0,.35),0 28px 46px rgba(0,0,0,.35)}}
.sheet:after{{content:"";position:absolute;inset:22px;border:1.5px solid {GREEN};opacity:.6}}
.in{{position:absolute;inset:0;color:{GREEN};text-align:center}}
.lab{{position:absolute;left:0;right:0;top:80px;color:{ORANGE}}}
.mid{{position:absolute;left:0;right:0;top:330px}}
.mid .t{{font-size:58px;letter-spacing:8px;text-transform:uppercase}}
.mid .i{{font-style:italic;font-size:74px;line-height:1;margin-top:6px}}
.mid .s{{font-size:26px;letter-spacing:5px;text-transform:uppercase;margin-top:30px}}
.bot{{position:absolute;left:0;right:0;bottom:80px}}"""
    return doc(css, f"""<div class="a bg photo" style="background-image:url(file://{photo})"></div>
<div class="a sheet"><div class="in"><div class="cap lab">@WeTalk.Ru</div>
<div class="mid"><div class="t">{E(title)}</div><div class="i">{E(sub)}</div></div>
<div class="cap bot">{E(num)}</div></div></div>""")

def L4(photo, title, sub, num):
    """Фото на весь кадр, маленький текст по центру (как фото с сапогами)."""
    css = f"""body{{background:#222}} .bg{{inset:0}} .sh{{inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0,rgba(0,0,0,0) 16%,rgba(0,0,0,0) 84%,rgba(0,0,0,.45) 100%),radial-gradient(ellipse at center,rgba(0,0,0,.32),rgba(0,0,0,.05) 60%)}}
.t1{{top:84px;color:{WHITE}}} .mid{{top:610px;color:{WHITE}}}
.mid .t{{font-size:44px;letter-spacing:9px;text-transform:uppercase}} .mid .i{{font-style:italic;font-size:76px;margin-top:4px}}
.mid .s{{font-size:26px;letter-spacing:5px;text-transform:uppercase;margin-top:22px}} .t4{{bottom:84px;color:{WHITE}}}"""
    return doc(css, f"""<div class="a bg photo" style="background-image:url(file://{photo})"></div><div class="a sh"></div>
<div class="a cap c t1">@WeTalk.Ru</div><div class="a c mid"><div class="t">{E(title)}</div><div class="i">{E(sub)}</div></div>
<div class="a cap c t4">{E(num)}</div>""")

if __name__ == "__main__":
    P = os.path.join(ROOT, "v4", "ph"); P3 = os.path.join(ROOT, "v3", "ph")
    pages = {
        "f1_podcast_zelenyi": L1(f"{P}/eb1025f3.jpg", "Podcast", "by our student", "(30) · B1-B2 Level", "green"),
        "f2_bag_list": L2(f"{P}/ebe280e1.jpg", "What’s in", "my bag?", "by our student", "(47)"),
        "f3_podcast_list_na_foto": L3(f"{P}/636e13bc.jpg", "Podcast", "by our student", "(16) · B1-B2 Level"),
        "f4_podcast_foto": L4(f"{P3}/a.jpg", "Podcast", "by our student", "(37) · A2-B1 Level"),
        "f5_podcast_bezhevyi": L1(f"{P}/f50a214e.jpg", "Podcast", "by our student", "(9) · 0-A1 Level", "beige"),
    }
    for n, h in pages.items():
        open(os.path.join(OUT, n + ".html"), "w").write(h)
    print("ok")
