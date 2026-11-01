"""v3 — журнальные обложки 3:4 (1080×1440, рендер ×2) по референсам: фото на весь кадр + типографика Times."""
import os, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v3"); os.makedirs(OUT, exist_ok=True)
GREEN, ORANGE, BEIGE, PAPER = "#415038", "#da5200", "#d2cec3", "#f6f3ec"

BASE = f"""
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_bold.ttf);font-weight:700;font-style:normal}}
@font-face{{font-family:T;src:url(file://{FONTS}/timesnrcyrmt_boldinclined.ttf);font-weight:700;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;overflow:hidden;font-family:T}}
.ph{{position:absolute;inset:0;background-size:cover;background-position:center}}
.sh{{position:absolute;inset:0}}
.a{{position:absolute}}
"""

def page(css, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{body}</body></html>"

def A(photo, num, level):  # «More time CREATING»: крупный курсив + капс по центру-слева, внизу подпись
    css = f"""
.sh{{background:linear-gradient(180deg,rgba(0,0,0,.05) 0%,rgba(0,0,0,.35) 35%,rgba(0,0,0,.45) 55%,rgba(0,0,0,.15) 80%,rgba(0,0,0,.35) 100%)}}
.k{{left:96px;top:470px;color:{PAPER}}}
.k .s{{font-style:italic;font-size:150px;line-height:1;letter-spacing:-2px}}
.k .c{{font-size:104px;line-height:1;letter-spacing:6px;margin-top:-6px}}
.k .p{{font-style:italic;font-size:40px;margin-top:34px;opacity:.92}}
.n{{right:96px;top:96px;color:{PAPER};font-size:40px}}
.f{{left:0;right:0;bottom:84px;text-align:center;color:{PAPER};font-size:28px;letter-spacing:8px}}
"""
    return page(css, f"""<div class="ph" style="background-image:url(file://{photo})"></div><div class="sh"></div>
<div class="a n">{html.escape(num)}</div>
<div class="a k"><div class="s">Podcast</div><div class="c">BY OUR STUDENT</div><div class="p">{html.escape(level)}</div></div>
<div class="a f">@WETALK.RU</div>""")

def B(photo, num, level):  # «Write here»: курсив-заголовок внизу слева + короткий текст
    css = f"""
.sh{{background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.55) 78%,rgba(0,0,0,.7) 100%)}}
.t{{left:84px;bottom:250px;color:{PAPER};font-style:italic;font-size:132px;line-height:1.0;letter-spacing:-2px}}
.p{{left:88px;bottom:170px;color:{PAPER};font-size:36px;font-style:italic;opacity:.92}}
.n{{left:88px;top:84px;color:{PAPER};font-size:40px}}
.f{{right:84px;top:90px;color:{PAPER};font-size:28px;letter-spacing:8px}}
"""
    return page(css, f"""<div class="ph" style="background-image:url(file://{photo})"></div><div class="sh"></div>
<div class="a n">{html.escape(num)}</div><div class="a f">@WETALK.RU</div>
<div class="a t">What’s in<br>my bag?</div><div class="a p">{html.escape(level)}</div>""")

def C(photo, num, level):  # «Talking point»: фото + белая карточка с рамкой
    css = f"""
.card{{left:96px;top:120px;width:620px;padding:46px 40px 44px;background:{PAPER};box-shadow:0 22px 50px rgba(0,0,0,.30),0 4px 10px rgba(0,0,0,.15);text-align:center}}
.card:after{{content:"";position:absolute;inset:16px;border:2px solid {GREEN};opacity:.55}}
.card .b{{color:{ORANGE};font-style:italic;font-size:34px}}
.card .t{{color:{GREEN};font-size:96px;letter-spacing:6px;line-height:1;margin-top:18px}}
.card .i{{color:{GREEN};font-style:italic;font-size:60px;margin-top:6px}}
.card .p{{color:{GREEN};font-size:32px;margin-top:22px;letter-spacing:2px}}
"""
    return page(css, f"""<div class="ph" style="background-image:url(file://{photo})"></div>
<div class="a card"><div class="b">@WeTalk.Ru</div><div class="t">PODCAST</div><div class="i">by our student</div>
<div class="p">{html.escape(num)} &nbsp;·&nbsp; {html.escape(level)}</div></div>""")

if __name__ == "__main__":
    P = os.path.join(OUT, "ph")
    for name, fn, ph, num, lvl in [("e1_podcast_zhurnal", A, "a", "(30)", "// B1-B2 Level"),
                                   ("e2_bag_zhurnal", B, "b", "(47)", "// by our student"),
                                   ("e3_podcast_kartochka", C, "c", "(37)", "A2-B1 Level")]:
        open(os.path.join(OUT, name + ".html"), "w").write(fn(f"{P}/{ph}.jpg", num, lvl))
    print("ok")
