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
    """Как «The Brief Edit» (сумка на фото): фото на весь кадр, по центру зелёная плашка, текст строго посередине."""
    css = f""".bg{{inset:0}} .sq{{left:250px;top:430px;width:580px;height:580px;background:{GREEN}}}
.in{{left:250px;top:430px;width:580px;height:580px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{BEIGE}}}
.in .t{{font-size:44px;letter-spacing:8px}} .in .i{{font-style:italic;font-size:96px;line-height:1.02;margin-top:4px}} .in .s{{font-size:28px;letter-spacing:4px;margin-top:30px}}
.top{{top:70px;color:{WHITE}}} .sh3{{inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,0) 14%)}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{PH}/f50a214e.jpg)"></div><div class="a sh3"></div>
<div class="a cap c top">@WeTalk.Ru</div><div class="a sq sh"><div class="grain" style="opacity:.3"></div></div>
<div class="a in"><div class="t">PODCAST</div><div class="i">by our<br>student</div><div class="s">(37) · A2-B1 LEVEL</div></div>""")


# 2 — однотонный тёмный (наш зелёный), крупный жирный капс по центру, мелкий текст внизу
def t2():
    css = f"""body{{background:{GREEN}}} .top{{top:70px;color:{WHITE}}}
.big{{top:420px;color:{WHITE};font-weight:700;font-size:118px;line-height:1.08;letter-spacing:2px}}
.txt{{left:120px;right:120px;bottom:130px;color:{WHITE}}}"""
    return doc(css, f"""<div class="grain" style="opacity:.35"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a c big">WHAT’S IN<br>MY BAG?</div>
<div class="a txt"><div class="body">Every episode, one of our students opens their bag and tells us about everything inside, in English. Real words, real life, real progress.</div><div style="margin-top:26px;font-size:26px;letter-spacing:4px">(47) · BY OUR STUDENT</div></div>""")

# 3 — обложка блокнота на спирали, бледный огромный курсив, капс и мелкий текст
def t3():
    css = f"""body{{background:{BEIGE}}} .bg{{inset:0}}
.top{{top:70px;color:{GREEN}}} .ghost{{top:250px;left:40px;right:-60px;text-align:center;color:{GREEN};opacity:.28;font-style:italic;font-size:270px;letter-spacing:-6px;white-space:nowrap}}
.mid{{top:600px;left:190px;right:110px;text-align:center;color:{GREEN}}}
.mid .t{{font-size:38px;letter-spacing:4px}} .mid .i{{font-style:italic;font-size:58px;line-height:1}} .mid .s{{font-size:28px;letter-spacing:3px;margin-top:30px}}
.bot{{bottom:80px;left:150px;right:60px;text-align:center;color:{GREEN}}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{A}/notebook.jpg)"></div>
<div class="a cap top" style="left:150px;right:60px;text-align:center">@WeTalk.Ru</div><div class="a ghost">Podcast</div>
<div class="a mid"><div class="t">PODCAST</div><div class="i">by our student</div><div class="s">RECORDED IN ENGLISH</div><div class="body" style="margin-top:34px;font-size:27px">Short, honest conversations recorded by our students. Listen, repeat and learn the English people really speak every day.</div></div>\n<div class="a cap bot">(30) · B1-B2 LEVEL</div>""")

# 4 — наш зелёный фон, фото по центру, огромный курсив через фото
def t4():
    css = f"""body{{background:{GREEN}}} .top{{top:70px;color:{WHITE}}}
.p{{left:300px;top:330px;width:470px;height:720px}}
.big{{top:360px;left:-40px;right:-80px;text-align:center;color:{BEIGE};font-style:italic;font-size:230px;letter-spacing:-5px;white-space:nowrap;opacity:.95}}
.txt{{left:110px;right:110px;top:1110px;color:{WHITE};text-align:center}}"""
    return doc(css, f"""<div class="grain" style="opacity:.35"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a p ph" style="background-image:url(file://{PH}/eb1025f3.jpg)"></div><div class="a big">Podcast</div>
<div class="a txt"><div class="body">Our students talk about their lives, plans and favourite things in English. Each episode is a small step to speaking with confidence.</div><div style="margin-top:22px;font-size:26px;letter-spacing:4px">(30) · B1-B2 LEVEL</div></div>""")

# 5 — фото на весь кадр, маленький текст по центру
def t5():
    css = f"""body{{background:#111}} .bg{{inset:0}} .sh2{{inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,0) 15%,rgba(0,0,0,.15) 50%,rgba(0,0,0,0) 85%,rgba(0,0,0,.5))}}
.top{{top:70px;color:{WHITE}}} .mid{{top:610px;color:{WHITE}}} .mid .t{{font-size:36px;letter-spacing:4px}}
.mid .i{{font-style:italic;font-size:60px;line-height:1}} .mid .s{{font-size:28px;letter-spacing:3px;margin-top:10px}} .bot{{bottom:70px;color:{WHITE}}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{PH3}/a.jpg)"></div><div class="a sh2"></div>
<div class="a cap c top">@WeTalk.Ru</div><div class="a c mid"><div class="t">PODCAST</div><div class="i">by our student</div><div class="s">(37) · A2-B1 LEVEL</div></div>
<div class="a cap c bot">english podcast</div>""")

# 6 — конверт с сургучной печатью, текст под печатью
def t6():
    css = f""".bg{{inset:0}} .mid{{top:880px;color:{GREEN}}} .mid .t{{font-size:36px;letter-spacing:4px}}
.mid .i{{font-style:italic;font-size:64px;line-height:1}} .mid .s{{font-size:28px;letter-spacing:3px;margin-top:12px}} .top{{top:70px;color:{ORANGE}}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{A}/seal.jpg)"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a c mid"><div class="t">WHAT’S IN</div><div class="i">my bag?</div><div class="s">(44) · BY OUR STUDENT</div></div>""")

# 7 — тёмный (наш зелёный) фон: конверт, бежевая карточка, фото в белой рамке внахлёст
def t7():
    """Конверт на зелёном, текст строго по центру конверта."""
    css = f""".bg{{inset:0}} .top{{top:70px;color:{WHITE}}} .bot{{bottom:70px;color:{WHITE}}}
.in{{left:0;right:0;top:545px;height:420px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{GREEN}}}
.in .t{{font-size:34px;letter-spacing:7px}} .in .i{{font-style:italic;font-size:78px;line-height:1;margin-top:4px}} .in .s{{font-size:24px;letter-spacing:4px;margin-top:20px}}"""
    return doc(css, f"""<div class="a bg ph" style="background-image:url(file://{A}/envelope.jpg)"></div><div class="a cap c top">@WeTalk.Ru</div>
<div class="a in"><div class="t">PODCAST</div><div class="i">by our student</div><div class="s">(16) · B1-B2 LEVEL</div></div>""")


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
.lab{{top:180px;color:{ORANGE}}} .p{{left:380px;top:420px;width:330px;height:380px}}
.w1{{top:300px;color:{GREEN};font-style:italic;font-size:210px;line-height:1;letter-spacing:-5px}}
.w2{{top:640px;color:{GREEN};font-style:italic;font-size:132px;line-height:1;letter-spacing:-3px}}
.txt{{left:200px;right:200px;bottom:180px;color:{GREEN};font-size:24px;text-align:center;letter-spacing:3px}}"""
    return doc(css, f"""<div class="grain" style="opacity:.35"></div><div class="a sheet sh"></div><div class="a cap c lab">@WeTalk.Ru</div>
<div class="a p ph" style="background-image:url(file://{PH}/62180978.jpg)"></div>
<div class="a c w1">Podcast</div><div class="a c w2">by our student</div><div class="a txt"><div class="body" style="letter-spacing:0;font-size:26px">Our students talk about their lives, plans and favourite things in English. Each episode is a small step to speaking with confidence.</div><div style="margin-top:20px">(9) · 0-A1 LEVEL</div></div>""")

if __name__ == "__main__":
    for i, f in enumerate([t1, t2, t3, t4, t5, t6, t7, t8, t9], 1):
        open(os.path.join(OUT, f"g{i}.html"), "w").write(f())
    print("ok")
