"""v8 — раскладка 1:1 с референсом (9 плиток), цвета бренда (бордо/чёрный→зелёный, голубой→бежевый),
шрифты как в референсе: рукописный (Pinyon Script) + рубленый (Inter). 3:4, 1080×1440, рендер ×2."""
import os, html, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
F = os.path.join(ROOT, "fonts"); INTER = "/usr/share/fonts/opentype/inter"
OUT = os.path.join(ROOT, "v8"); os.makedirs(OUT, exist_ok=True)
PH = os.path.join(OUT, "ph"); os.makedirs(PH, exist_ok=True)
A = os.path.join(ROOT, "v7", "assets")
U = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13"
PAPER = os.path.join(ROOT, "v5", "paper.jpg")
GREEN, BEIGE, CREAM, ORANGE = "#415038", "#d2cec3", "#f4f1ea", "#da5200"
E = html.escape


def photo(pid, w, h, fy=0.45, bw=False):
    dst = f"{PH}/{pid}_{w}x{h}{'_bw' if bw else ''}.jpg"
    if not os.path.exists(dst):
        subprocess.run([sys.executable, os.path.join(ROOT, "src", "v2_prep.py"), f"{U}/{pid}-image.jpg", dst, str(w), str(h), str(fy)], check=True)
        if bw:
            from PIL import Image, ImageOps
            Image.open(dst).convert("L").convert("RGB").save(dst, quality=94)
    return dst


BASE = f"""
@font-face{{font-family:S;src:url(file://{F}/PinyonScript-Regular.ttf)}}
@font-face{{font-family:I;src:url(file://{INTER}/Inter-Regular.otf);font-weight:400}}
@font-face{{font-family:I;src:url(file://{INTER}/Inter-Medium.otf);font-weight:500}}
@font-face{{font-family:I;src:url(file://{INTER}/Inter-Bold.otf);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;overflow:hidden;font-family:I}}
.a{{position:absolute}} .c{{left:0;right:0;text-align:center}}
.lab{{font-size:24px;font-weight:500;letter-spacing:1px;text-transform:uppercase}}
.sc{{font-family:S;font-weight:400;text-transform:none;letter-spacing:0}}
.mid{{font-size:26px;font-weight:500;line-height:1.3;text-transform:uppercase;text-align:center}}
.mid .sc{{font-size:40px;line-height:.6}}
.p{{font-size:26px;line-height:1.38;text-align:justify}}
.bg{{inset:0;background-size:cover;background-position:center}}
.grain{{position:absolute;inset:0;background:url(file://{PAPER}) center/900px;mix-blend-mode:multiply;opacity:.5}}
.sh{{box-shadow:0 2px 3px rgba(0,0,0,.22),0 16px 28px rgba(0,0,0,.20)}}
"""
def doc(css, body): return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{body}</body></html>"

TXT_POD = "Short, honest conversations recorded by our students. Listen, repeat and learn the English people really speak every day, one episode at a time."
TXT_BAG = "Every episode, one of our students opens their bag and tells us about everything inside, in English. Real words, real life, real progress."


def t1():  # бежевая бумага, фото в белой рамке, бежевая записка с зажимом и рукописным текстом
    p = photo("779fd367", 1100, 2320, 0.55)
    css = f"""body{{background:{BEIGE}}}
.fr{{left:97px;top:118px;width:563px;height:1180px;background:#fbfaf6;padding:20px}} .fr div{{width:100%;height:100%}}
.nt{{left:518px;top:718px;width:487px;height:510px;background:#e9e5dc}} .nt:after{{content:"";position:absolute;inset:18px;border:1.5px solid {GREEN};opacity:.55}}
.clip{{left:675px;top:640px;width:175px;transform:rotate(-2deg);filter:drop-shadow(0 4px 5px rgba(0,0,0,.3))}}
.tx{{left:518px;width:487px;top:845px;color:{GREEN};font-family:S;font-size:66px;line-height:1.05;text-align:center}}"""
    return doc(css, f"""<div class="grain"></div><div class="a fr sh"><div class="bg" style="background-image:url(file://{p})"></div></div>
<div class="a nt sh"><div class="grain" style="opacity:.45"></div></div>
<img class="a clip" src="file://{A}/clip_only.png">
<div class="a tx">Podcast<br>by our student<br><span style="font-family:I;font-size:22px;letter-spacing:2px">(37) · A2-B1 LEVEL</span></div>""")


def t2():  # «ABOUT THE BRAND»: тёмный фон → зелёный
    css = f"""body{{background:{GREEN}}} .t{{top:110px;color:{CREAM}}}
.big{{top:470px;color:{CREAM};font-weight:700;font-size:104px;line-height:1.08;letter-spacing:-1px}}
.p{{left:110px;right:110px;top:1150px;color:{CREAM}}}"""
    return doc(css, f"""<div class="grain" style="opacity:.3"></div><div class="a lab c t">@WeTalk.Ru</div>
<div class="a c big">WHAT’S IN<br>MY<br>BAG?</div><div class="a p">{TXT_BAG}</div>""")


def t3():  # блокнот на спирали (голубой → бежевый)
    css = f""".t{{top:110px;left:150px;right:40px;color:{GREEN}}} .b{{top:1310px;left:150px;right:40px;color:{GREEN}}}
.gh{{top:250px;left:150px;right:-140px;text-align:center;color:{GREEN};opacity:.30;font-family:S;font-size:300px;line-height:1;white-space:nowrap}}
.m{{top:860px;left:190px;right:80px;color:{GREEN}}} .p{{left:280px;right:90px;top:1000px;color:{GREEN};font-size:22px}}"""
    return doc(css, f"""<div class="a bg" style="background-image:url(file://{A}/notebook.jpg)"></div>
<div class="a lab t" style="text-align:center">@WeTalk.Ru</div><div class="a gh">podcast</div>
<div class="a mid m">PODCAST <span class="sc">by our</span><br>STUDENT · RECORDED<br>IN ENGLISH.</div>
<div class="a p">{TXT_POD}</div><div class="a lab b" style="text-align:center">(30) · B1-B2 LEVEL</div>""")


def t4():  # «Get Inspired»: бордо → зелёный, фото по центру, рукописное слово поверх
    p = photo("387e0534", 940, 1500, 0.3)
    css = f"""body{{background:{GREEN}}} .t{{top:100px;color:{CREAM}}}
.ph{{left:300px;top:345px;width:470px;height:750px}}
.big{{top:340px;left:-80px;right:-120px;text-align:center;color:{BEIGE};font-family:S;font-size:230px;line-height:1;white-space:nowrap;opacity:.9}}
.p{{left:100px;right:100px;top:1165px;color:{CREAM}}}"""
    return doc(css, f"""<div class="grain" style="opacity:.3"></div><div class="a lab c t">@WeTalk.Ru</div>
<div class="a ph bg" style="background-image:url(file://{p})"></div><div class="a big">New Podcast</div>
<div class="a p">{TXT_POD}</div>""")


def t5():  # фото на весь кадр, маленький текст по центру
    p = photo("9b22d97e", 2160, 2880, 0.5)
    css = f""".t{{top:100px;color:{CREAM}}} .b{{top:1310px;color:{CREAM}}} .m{{top:640px;left:330px;right:330px;color:{CREAM}}}
.sh2{{inset:0;background:rgba(0,0,0,.12)}}"""
    return doc(css, f"""<div class="a bg" style="background-image:url(file://{p})"></div><div class="a sh2"></div>
<div class="a lab c t">@WeTalk.Ru</div><div class="a mid m">PODCAST <span class="sc">by our</span><br>STUDENT · A2-B1<br>LEVEL.</div>
<div class="a lab c b">(37) · ENGLISH PODCAST</div>""")


def t6():  # конверт с печатью
    css = f""".m{{top:1200px;left:300px;right:300px;color:{GREEN}}}"""
    return doc(css, f"""<div class="a bg" style="background-image:url(file://{A}/seal.jpg);background-position:center 30%"></div>
<div class="a mid m">WHAT’S IN <span class="sc">my bag?</span><br>BY OUR STUDENT · (44)<br>@WETALK.RU</div>""")


def t7():  # тёмный фон → зелёный, конверт, карточка, фото в рамке
    p = photo("1cdd24a5", 700, 900, 0.5)
    css = f""".bgx{{left:0;top:-160px;width:1080px;height:1600px;background:url(file://{A}/envelope.jpg) center/cover}}
.t{{top:130px;color:{CREAM}}} .b{{top:1310px;color:{CREAM}}}
.cd{{left:335px;top:560px;width:650px;height:450px;background:{BEIGE}}}
.ct{{left:335px;width:650px;top:640px;text-align:center;color:{GREEN}}} .ct .s{{font-family:S;font-size:150px;line-height:1}} .ct .l{{font-size:26px;font-weight:500;letter-spacing:1px;margin-top:20px}}
.pf{{left:86px;top:680px;width:380px;height:500px;background:#fbfaf6;padding:16px;transform:rotate(-8deg)}} .pf div{{width:100%;height:100%}}"""
    return doc(css, f"""<div class="a bgx"></div><div class="a lab c t">@WeTalk.Ru</div>
<div class="a cd sh"><div class="grain" style="opacity:.45"></div></div>
<div class="a ct"><div class="s">Podcast</div><div class="l">BY OUR STUDENT</div></div>
<div class="a pf sh"><div class="bg" style="background-image:url(file://{p})"></div></div>
<div class="a lab c b">(16) · B1-B2 LEVEL</div>""")


def t8():  # фото сверху на весь кадр + белый лист с рамкой
    p = photo("11851dde", 2160, 2880, 0.5)
    css = f""".sheet{{left:250px;top:300px;width:580px;height:930px;background:url(file://{PAPER}) center/900px;transform:rotate(-1.2deg)}}
.sheet:after{{content:"";position:absolute;inset:22px;border:1.5px solid #222;opacity:.6}}
.in{{position:absolute;inset:0;color:#222}} .in .t{{position:absolute;left:0;right:0;top:80px;text-align:center}}
.in .m{{position:absolute;left:60px;right:60px;top:380px}} .in .b{{position:absolute;left:0;right:0;bottom:120px;text-align:center}}"""
    return doc(css, f"""<div class="a bg" style="background-image:url(file://{p})"></div>
<div class="a sheet sh"><div class="in"><div class="lab t">@WeTalk.Ru</div>
<div class="mid m" style="color:{GREEN}">PODCAST <span class="sc">by our</span><br>STUDENT · B1-B2<br>LEVEL.</div>
<div class="lab b" style="color:{GREEN}">LISTEN WITH US<br>TODAY · (17)</div></div></div>""")


def t9():  # «Getting Inspired»: бордо → зелёный, белый лист, чёрно-белое фото между строк
    p = photo("62180978", 520, 560, 0.4, bw=True)
    css = f"""body{{background:{GREEN}}} .sheet{{left:108px;top:144px;width:864px;height:1152px;background:url(file://{PAPER}) center/900px}}
.t{{top:235px;color:{GREEN}}} .ph{{left:430px;top:560px;width:260px;height:280px}}
.w{{left:108px;width:864px;text-align:center;color:{GREEN};font-family:S;font-size:200px;line-height:1;white-space:nowrap}}
.p{{left:250px;right:250px;top:1100px;color:#333;font-size:20px}}"""
    return doc(css, f"""<div class="grain" style="opacity:.3"></div><div class="a sheet sh"></div><div class="a lab c t">@WeTalk.Ru</div>
<div class="a ph bg" style="background-image:url(file://{p})"></div>
<div class="a w" style="top:430px">What’s in</div><div class="a w" style="top:690px">my bag?</div>
<div class="a p">{TXT_BAG}</div>""")


if __name__ == "__main__":
    for i, f in enumerate([t1, t2, t3, t4, t5, t6, t7, t8, t9], 1):
        open(os.path.join(OUT, f"h{i}.html"), "w").write(f())
    print("ok")
