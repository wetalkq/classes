"""v7 — точный повтор референса (9 плиток), наши цвета/шрифт/тексты/фото. 3:4, 1080×1440, рендер ×2."""
import os, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v7"); os.makedirs(OUT, exist_ok=True)
A = os.path.join(OUT, "assets")
PH = os.path.join(ROOT, "v4", "ph"); PH3 = os.path.join(ROOT, "v3", "ph")
GREEN, ORANGE, BEIGE, WHITE = "#415038", "#da5200", "#d2cec3", "#f7f4ee"
PAPER = os.path.join(ROOT, "v5", "paper.jpg")
E = html.escape

BASE = f"""
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_bold.ttf);font-weight:700;font-style:normal}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;overflow:hidden;font-family:T}}
.a{{position:absolute}} .c{{left:0;right:0;text-align:center}}
.cap{{font-size:26px;letter-spacing:4px;text-transform:uppercase}}
.ph{{background-size:cover;background-position:center}}
.grain{{position:absolute;inset:0;background:url(file://{PAPER}) center/1000px;mix-blend-mode:multiply;opacity:.6}}
.body{{font-size:30px;line-height:1.35;text-align:justify}}
.sh{{box-shadow:0 2px 3px rgba(0,0,0,.25),0 18px 30px rgba(0,0,0,.22)}}
"""
def doc(css, body): return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{body}</body></html>"

# 1 — бежевая бумага, фото в белой рамке, записка с зажимом
def t1():
    css = f"""body{{background:{BEIGE}}} .fr{{left:70px;top:70px;width:640px;height:1050px;background:{WHITE}}}
.p{{left:96px;top:96px;width:588px;height:998px}}
.cn{{left:520px;top:560px;width:470px}}
.nt{{left:520px;width:470px;top:840px;text-align:center;color:{GREEN}}}
.nt .i{{font-style:italic;font-size:58px;line-height:1.1}} .nt .s{{font-size:24px;letter-spacing:3px;margin-top:22px}}
.lab{{left:70px;bottom:120px;color:{ORANGE}}}"""
    return doc(css, f"""<div class="grain"></div><div class="a fr sh"></div><div class="a p ph" style="background-image:url(file://{PH}/f50a214e.jpg)"></div>
<img class="a cn" src="file://{A}/clipnote.png" style="filter:drop-shadow(0 14px 22px rgba(0,0,0,.25))">
<div class="a nt"><div class="i">Podcast<br>by our student</div><div class="s">(37) · A2-B1 LEVEL</div></div>
<div class="a cap lab">@WeTalk.Ru</div>""")

# 2 — однотонный тёмный (наш зелёный), крупный жирный капс по центру, мелкий текст внизу
def t2():
    css = f"""body{{background:{GREEN}}} .top{{top:70px;color:{WHITE}}}
.big{{top:420px;color:{WHITE};font-weight:700;font-size:118px;line-height:1.08;letter-spacing:2px}}
.txt{{left:120px;right:120px;bottom:170px;color:{WHITE};font-size:32px;line-height:1.4;text-align:center}}"""
    return doc(css, f"""<div class="grain" style="opacity:.35"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a c big">WHAT’S IN<br>MY BAG?</div>
<div class="a txt"><i>by our student</i><br>(47)</div>""")

# 3 — обложка блокнота на спирали, бледный огромный курсив, капс и мелкий текст
def t3():
    css = f"""body{{background:{BEIGE}}} .bg{{inset:0}}
.top{{top:70px;color:{GREEN}}} .ghost{{top:200px;left:40px;right:-60px;text-align:center;color:{GREEN};opacity:.28;font-style:italic;font-size:270px;letter-spacing:-6px;white-space:nowrap}}
.mid{{top:690px;left:150px;right:60px;text-align:center;color:{GREEN}}}
.mid .t{{font-size:58px;letter-spacing:8px}} .mid .i{{font-style:italic;font-size:104px;line-height:1.05;margin-top:6px}} .mid .s{{font-size:34px;letter-spacing:4px;margin-top:48px}}
.bot{{bottom:90px;left:150px;right:60px;text-align:center;color:{GREEN}}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{A}/notebook.jpg)"></div>
<div class="a cap top" style="left:150px;right:60px;text-align:center">@WeTalk.Ru</div><div class="a ghost">Podcast</div>
<div class="a mid"><div class="t">PODCAST</div><div class="i">by our student</div><div class="s">(30) · B1-B2 LEVEL</div></div>
<div class="a cap bot">wetalk.ru</div>""".replace('<div class="a cap bot">wetalk.ru</div>', ''))

# 4 — наш зелёный фон, фото по центру, огромный курсив через фото
def t4():
    css = f"""body{{background:{GREEN}}} .top{{top:70px;color:{WHITE}}}
.p{{left:290px;top:300px;width:500px;height:660px}}
.big{{top:330px;left:-40px;right:-80px;text-align:center;color:{BEIGE};font-style:italic;font-size:230px;letter-spacing:-5px;white-space:nowrap;opacity:.95}}
.txt{{left:110px;right:110px;top:1010px;color:{WHITE};text-align:center;font-size:34px;line-height:1.45}}"""
    return doc(css, f"""<div class="grain" style="opacity:.35"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a p ph" style="background-image:url(file://{PH}/eb1025f3.jpg)"></div><div class="a big">Podcast</div>
<div class="a txt"><i>by our student</i><br>(30) · B1-B2 Level</div>""")

# 5 — фото на весь кадр, маленький текст по центру
def t5():
    css = f"""body{{background:#111}} .bg{{inset:0}} .sh2{{inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,0) 15%,rgba(0,0,0,.15) 50%,rgba(0,0,0,0) 85%,rgba(0,0,0,.5))}}
.top{{top:70px;color:{WHITE}}} .mid{{top:560px;color:{WHITE};text-shadow:0 2px 14px rgba(0,0,0,.55)}} .mid .t{{font-size:58px;letter-spacing:8px}}
.mid .i{{font-style:italic;font-size:104px;line-height:1.05;margin-top:6px}} .mid .s{{font-size:34px;letter-spacing:4px;margin-top:34px}} .bot{{bottom:70px;color:{WHITE}}}
.dk{{inset:0;background:radial-gradient(ellipse 55% 22% at 50% 47%,rgba(0,0,0,.50),rgba(0,0,0,0))}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{PH3}/a.jpg)"></div><div class="a sh2"></div><div class="a dk"></div>
<div class="a cap c top">@WeTalk.Ru</div><div class="a c mid"><div class="t">PODCAST</div><div class="i">by our student</div><div class="s">(37) · A2-B1 LEVEL</div></div>
<div class="a cap c bot">english podcast</div>""")

# 6 — конверт с сургучной печатью, текст под печатью
def t6():
    css = f""".bg{{inset:0}} .mid{{top:860px;color:{GREEN}}} .mid .t{{font-size:58px;letter-spacing:8px}}
.mid .i{{font-style:italic;font-size:112px;line-height:1.05;margin-top:6px}} .mid .s{{font-size:34px;letter-spacing:4px;margin-top:40px}} .top{{top:70px;color:{ORANGE}}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{A}/seal.jpg)"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a c mid"><div class="t">WHAT’S IN</div><div class="i">my bag?</div><div class="s">(44) · BY OUR STUDENT</div></div>""")

# 7 — тёмный (наш зелёный) фон: конверт, бежевая карточка, фото в белой рамке внахлёст
def t7():
    css = f""".bg{{inset:0}} .top{{top:70px;color:{WHITE}}} .bot{{bottom:70px;color:{WHITE}}}
.card{{left:330px;top:640px;width:620px;height:400px;background:{BEIGE};transform:rotate(0deg)}}
.ct{{left:330px;width:620px;top:730px;text-align:center;color:{GREEN}}} .ct .i{{font-style:italic;font-size:120px;line-height:1}} .ct .s{{font-size:26px;letter-spacing:4px;margin-top:26px;padding-left:120px}}
.pf{{left:110px;top:900px;width:300px;height:390px;background:{WHITE};padding:16px;transform:rotate(-6deg)}} .pf div{{width:100%;height:100%}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{A}/envelope.jpg)"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a card sh"><div class="grain" style="opacity:.5"></div></div>
<div class="a ct"><div class="i">Podcast</div><div class="s">BY OUR STUDENT · (16)</div></div>
<div class="a pf sh"><div class="ph" style="background-image:url(file://{PH}/636e13bc.jpg)"></div></div>
<div class="a cap c bot">B1-B2 level</div>""")

# 8 — фото на весь кадр, по центру белый лист с тонкой рамкой
def t8():
    css = f""".bg{{inset:0}} .sheet{{left:280px;top:330px;width:520px;height:760px;background:url(file://{PAPER}) center/900px;transform:rotate(-2deg)}}
.sheet:after{{content:"";position:absolute;inset:20px;border:1.5px solid {GREEN};opacity:.55}}
.in{{position:absolute;inset:0;text-align:center;color:{GREEN}}} .in .l1{{position:absolute;left:0;right:0;top:70px;color:{ORANGE}}}
.in .m{{position:absolute;left:0;right:0;top:290px}} .in .m .t{{font-size:34px;letter-spacing:4px}} .in .m .i{{font-style:italic;font-size:56px;line-height:1}}
.in .l2{{position:absolute;left:0;right:0;bottom:70px;font-size:26px;letter-spacing:3px}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{PH}/85387ce9.jpg)"></div>
<div class="a sheet sh"><div class="in"><div class="cap l1">@WeTalk.Ru</div><div class="m"><div class="t">WHAT’S IN</div><div class="i">my bag?</div></div>
<div class="l2">(45) · BY OUR STUDENT</div></div></div>""")

# 9 — наш зелёный фон, белый лист, огромный курсив в две строки, маленькое фото между
def t9():
    css = f"""body{{background:{GREEN}}} .sheet{{left:120px;top:120px;right:120px;bottom:120px;background:url(file://{PAPER}) center/1000px}}
.lab{{top:190px;color:{ORANGE}}} .p{{left:430px;top:560px;width:240px;height:260px}}
.w1{{top:330px;color:{GREEN};font-style:italic;font-size:200px;line-height:1;letter-spacing:-5px}}
.w2{{top:720px;color:{GREEN};font-style:italic;font-size:130px;line-height:1;letter-spacing:-3px}}
.txt{{left:200px;right:200px;bottom:200px;color:{GREEN};font-size:28px;text-align:center;letter-spacing:3px}}"""
    return doc(css, f"""<div class="grain" style="opacity:.35"></div><div class="a sheet sh"></div><div class="a cap c lab">@WeTalk.Ru</div>
<div class="a p ph" style="background-image:url(file://{PH}/62180978.jpg)"></div>
<div class="a c w1">Podcast</div><div class="a c w2">by our student</div><div class="a txt">(9) · 0-A1 LEVEL</div>""")

if __name__ == "__main__":
    for i, f in enumerate([t1, t2, t3, t4, t5, t6, t7, t8, t9], 1):
        open(os.path.join(OUT, f"g{i}.html"), "w").write(f())
    print("ok")
