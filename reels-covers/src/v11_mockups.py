"""v11 — 16 раскладок макетов, ТОЛЬКО наши тексты. Каждый текст — в своём боксе (flex-колонка с gap),
авто-уменьшение при переполнении + проверка наложений. 3:4, 1080×1440 → ×2."""
import os, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
F = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v11"); PH = os.path.join(OUT, "ph"); os.makedirs(PH, exist_ok=True)
U = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13"
G, B, C, O, K = "#415038", "#d2cec3", "#f5f2ea", "#da5200", "#1e1e1c"


def ph(pid, w, h, fy=0.45):
    d = f"{PH}/{pid}_{w}x{h}.jpg"
    if not os.path.exists(d):
        subprocess.run([sys.executable, os.path.join(ROOT, "src", "v2_prep.py"), f"{U}/{pid}-image.jpg", d, str(w * 2), str(h * 2), str(fy)], check=True)
    return d


CSS = f"""
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt.ttf);font-weight:400;font-style:normal}}
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt_inclined.ttf);font-weight:400;font-style:italic}}
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt_bold.ttf);font-weight:700;font-style:normal}}
@font-face{{font-family:T;src:url(file://{F}/timesnrcyrmt_boldinclined.ttf);font-weight:700;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;overflow:hidden;font-family:T;background:{B};color:{K}}}
.a{{position:absolute}} .f{{background-size:cover;background-position:center}} .dim{{filter:brightness(.7)}}
.card{{background:{C}}}
.box{{position:absolute;display:flex;flex-direction:column;overflow:hidden;--k:1}}
.box>div{{line-height:1.12;font-size:calc(var(--fs) * var(--k))}}
.shd{{text-shadow:0 1px 8px rgba(0,0,0,.4)}}
"""
FIT = """<script>
document.fonts.ready.then(()=>{document.querySelectorAll('.box').forEach(b=>{let k=1;
 while((b.scrollHeight>b.clientHeight+1||b.scrollWidth>b.clientWidth+1)&&k>0.4){k-=0.02;b.style.setProperty('--k',k);}
 b.querySelectorAll(':scope>div').forEach(d=>{if(d.scrollWidth>b.clientWidth+1){d.style.whiteSpace='normal'}});});
 document.body.dataset.ok=1;});
</script>"""


def T(text, fs, color=K, w=400, it=False, ls=0, up=False, extra=""):
    st = f"--fs:{fs}px;color:{color};font-weight:{w};font-style:{'italic' if it else 'normal'};letter-spacing:{ls}px;{'text-transform:uppercase;' if up else ''}{extra}"
    return f'<div style="{st}">{text}</div>'


def box(x, y, w, h, items, gap=24, align="center", valign="center", cls=""):
    ai = {"center": "center", "left": "flex-start", "right": "flex-end"}[align]
    jc = {"center": "center", "top": "flex-start", "bottom": "flex-end", "between": "space-between"}[valign]
    return (f'<div class="box {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;gap:{gap}px;'
            f'align-items:{ai};justify-content:{jc};text-align:{align}">' + "".join(items) + "</div>")


def page(body, bg=B): return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='background:{bg}'>{body}{FIT}</body></html>"
def img(pid, x, y, w, h, fy=.45, cls="", r=0): return f'<div class="a f {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;background-image:url(file://{ph(pid,w,h,fy)})"></div>'
def rect(x, y, w, h, col=C, r=0, border=""): return f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{col};border-radius:{r}px;{border}"></div>'
def logo(col, fs=56): return ''
def _old_logo(col, fs=56): return f'<div style="--fs:{fs}px;color:{col};letter-spacing:6px;border-top:1.5px solid {col};border-bottom:1.5px solid {col};padding:8px 20px 6px">WETALK</div>'


POD, BAG = "Podcast By Our Student", "What’s In My Bag?"
AT = "@WeTalk.Ru"
SCH = "WeTalk | English School"
L = {}

# 1 фото, логотип, @, заголовок по центру, подпись внизу
L[1] = page(img("ee305f34", 0, 0, 1080, 1440, .3, "dim")
    + box(90, 70, 900, 120, [T(AT, 60, C, it=True)], cls="shd")
    + box(90, 760, 900, 380, [T("Podcast", 110, C, 700), T("By Our Student", 110, C, 700), T("(37) · A2–B1 Level", 46, C, ls=2)], gap=18, cls="shd")
    + box(90, 1160, 900, 150, [T("«Говори — даже если страшно»", 54, C, it=True, extra="white-space:nowrap")], valign="top", cls="shd"))

# 2 фото сверху, светлая плашка снизу, крупный заголовок слева
L[2] = page(img("b5e6f2e0", 0, 0, 1080, 840, .4) + rect(0, 840, 1080, 600, B)
    + box(70, 870, 940, 240, [T("What’s In", 96, K, 700), T("My Bag?", 96, K, 700)], gap=6, align="left")
    + box(70, 1130, 940, 60, [T("«Каждое слово — шаг вперёд»", 42, G, it=True, extra="white-space:nowrap")], align="left")
    + box(70, 1205, 940, 60, [T("(47) · By Our Student", 44, K)], align="left")
    + box(0, 1290, 1080, 80, [T(AT, 52, O, it=True)]))

# 3 бежевый фон, текст сверху с выделением, квадратное фото, подпись снизу
L[3] = page(box(0, 50, 1080, 80, [T(AT, 54, O, it=True)])
    + box(90, 150, 900, 220, [T("Новый Выпуск", 76, K), T("Podcast By Our Student", 64, O, it=True)], gap=16)
    + img("38779c67", 190, 400, 700, 700, .5)
    + box(90, 1135, 900, 180, [T("(30) · B1–B2 Level", 52, G), T("«Ошибки — это рост»", 52, K, it=True, extra="white-space:nowrap")], gap=18, valign="top"))

# 4 зелёный фон, верх, @, светлая карточка с заголовком, низ
L[4] = page(box(0, 150, 1080, 120, [T(AT, 64, B, it=True)])
    + rect(120, 340, 840, 760, C, 30)
    + box(170, 380, 740, 680, [T("Podcast", 120, G, 700), T("By Our Student", 96, G, 700), T("(30) · B1–B2 Level", 48, K, ls=2)], gap=26)
    + box(90, 1150, 900, 200, [T("«Начни с одной фразы»", 62, C, it=True, extra="white-space:nowrap")], gap=12, valign="top"), bg=G)

# 5 шапка, две страницы, крупный капс снизу
hdr = lambda col=K: ''
_old_hdr = lambda col=K: box(50, 50, 980, 60, [f'<div style="--fs:26px;width:100%;display:flex;justify-content:space-between;color:{col};letter-spacing:2px"><span>WETALK</span><span>@wetalk.ru</span><span>2026</span></div>'])
L[5] = page(hdr() + box(90, 140, 900, 120, [T(AT, 64, O, it=True)])
    + rect(90, 290, 440, 760)
    + box(130, 330, 360, 680, [T("What’s In", 84, G, 700), T("My Bag?", 84, G, 700), T("(47)", 80, O, it=True), T("By Our", 56, K), T("Student", 56, K)], gap=26)
    + img("103875d7", 550, 290, 440, 760, .4)
    + box(60, 1095, 960, 260, [T("WHAT’S IN MY BAG?", 76, K, 700), T("«Немного каждый день»", 56, G, it=True, extra="white-space:nowrap")], gap=22, valign="top"))

# 6 шапка, @, коллаж, оранжевая строка + текст
coll = [("ebe280e1", 230, 340, 330, 420), ("6998d97e", 70, 560, 400, 320), ("eb1025f3", 360, 300, 380, 640), ("a582ad4e", 700, 370, 300, 340), ("dbb02000", 720, 630, 280, 340)]
L[6] = page(hdr() + box(90, 130, 900, 140, [T("Podcast By Our Student", 72, K)])
    + "".join(img(p, x, y, w, h, .4) for p, x, y, w, h in coll)
    + box(90, 1005, 900, 330, [T("(37) · A2–B1 Level", 60, O, 700), T("«Начни сегодня»", 58, K, it=True, extra="white-space:nowrap"), T(AT, 56, O, it=True)], gap=22, valign="top"))

# 7 крупная строка, подпись, @, два фото со скруглением
L[7] = page(box(60, 60, 960, 420, [T("What’s In", 130, K), T("My Bag?", 130, K)], gap=4, align="left")
    + box(60, 470, 960, 160, [T("— (47) · By Our Student", 50, K), T("«Язык — это привычка»", 44, G, it=True, extra="white-space:nowrap")], gap=16, align="left", valign="top")
    + box(0, 640, 1080, 70, [T(AT, 56, O, it=True)])
    + img("dbb02000", 40, 720, 485, 660, .4, r=22) + img("11851dde", 555, 720, 485, 660, .4, r=22))

# 8 шапка, @, заголовок жирным курсивом, подзаголовок, фото снизу
L[8] = page(hdr() + box(90, 120, 900, 140, [T(AT, 84, O, it=True)])
    + box(90, 270, 900, 300, [T("Podcast", 96, K, 700, True), T("By Our Student", 96, K, 700, True)], gap=8)
    + box(90, 580, 900, 170, [T("(30) · B1–B2 Level", 52, G), T("«Слушай, повторяй, говори»", 44, K, it=True, extra="white-space:nowrap")], gap=16)
    + img("11851dde", 40, 790, 1000, 610, .5))

# 9 фото, верх, @, огромный капс, подзаголовок, низ
L[9] = page(img("85387ce9", 0, 0, 1080, 1440, .5, "dim")
    + box(0, 610, 1080, 90, [T(AT, 64, C, it=True)], cls="shd")
    + box(70, 720, 940, 480, [T("WHAT’S IN", 120, C, 700), T("MY BAG?", 120, C, 700), T("(47) · By Our Student", 54, C)], gap=18, align="left", valign="bottom", cls="shd")
    + box(70, 1225, 940, 80, [T("«Ты знаешь больше, чем думаешь»", 44, C, it=True, extra="white-space:nowrap")], align="left", valign="top", cls="shd"))

# 10 фото, верх, капс, светлая карточка, @, курсив снизу
L[10] = page(img("6998d97e", 0, 0, 1080, 1440, .4, "dim") + hdr(C)
    + box(60, 130, 960, 230, [T("PODCAST", 104, C, 700), T("BY OUR STUDENT", 84, C, 700)], gap=8, cls="shd")
    + rect(160, 420, 760, 560)
    + box(200, 460, 680, 480, [T("(30)", 90, G, it=True), T("B1–B2 Level", 66, K), T("«15 минут в день меняют всё»", 46, G, it=True, extra="white-space:nowrap")], gap=22)
    + box(90, 1020, 900, 100, [T(AT, 66, C, it=True)], valign="top", cls="shd")
    + box(90, 1130, 900, 120, [T("Новый выпуск — уже в Reels", 52, C, 700, True)], valign="top", cls="shd"))

# 11 зелёный, логотип, заголовок, @, три панели, низ
L[11] = page(box(90, 60, 900, 120, [logo(B, 52)])
    + box(90, 200, 900, 230, [T("Podcast", 96, C, 700), T("By Our Student", 80, C, 700)], gap=8)
    + box(90, 440, 900, 100, [T(AT, 60, B, it=True)])
    + img("387e0534", 0, 580, 330, 600, .3) + rect(375, 580, 330, 600) + rect(750, 580, 330, 600)
    + box(400, 610, 280, 540, [T("0–A1", 64, G, 700), T("A2–B1", 64, G, 700), T("B1–B2", 64, G, 700)], gap=40)
    + box(775, 610, 280, 540, [T("«Новый", 56, G, it=True), T("язык —", 56, G, it=True), T("новая", 56, G, it=True), T("версия", 56, G, it=True), T("тебя»", 56, G, it=True, extra="white-space:nowrap")], gap=16), bg=G)

# 12 фото, светлая карточка по центру, @ ниже, логотип внизу
L[12] = page(img("5629baa1", 0, 0, 1080, 1440, .4) + rect(170, 150, 740, 840)
    + box(210, 190, 660, 760, [T("The", 130, K, it=True), T("Podcast", 104, K), T("By Our Student", 84, K), T("(30) • B1–B2 Level", 44, G, it=True)], gap=22)
    + box(90, 1030, 900, 100, [T(AT, 72, C, it=True)], valign="top", cls="shd")
    + box(90, 1135, 900, 150, [T("«Уверенность — в практике»", 54, C, it=True, extra="white-space:nowrap")], valign="top", cls="shd"))

# 13 / 15 фото сверху, курсив-заголовок, подзаголовок, рамка, курсив внизу
def info(pid, t1, t2, sub, frame, tail):
    return page(img(pid, 40, 40, 1000, 540, .4)
        + box(90, 610, 900, 250, [T(t1, 90, G, it=True), T(t2, 90, G, it=True)], gap=4)
        + box(90, 870, 900, 80, [T(sub, 46, K, 700, True)])
        + rect(170, 980, 740, 210, "transparent", 24, f"border:2px solid {G};")
        + box(200, 1000, 680, 170, frame, gap=14)
        + box(90, 1220, 900, 170, [T(tail, 60, K, it=True), T(AT, 54, O, it=True)], gap=14, valign="top"))
L[13] = info("61531651", "Podcast", "By Our Student", "(37) · A2–B1 Level", [T("«Говори больше»", 64, K, it=True, extra="white-space:nowrap")], "Новый выпуск")
L[15] = info("1cdd24a5", "What’s In", "My Bag?", "(44) · By Our Student", [T("«Шаг за шагом»", 64, K, it=True, extra="white-space:nowrap")], "Новый выпуск")

# 14 фото, курсив сверху, @, светлая карточка, текст снизу
L[14] = page(img("ce64ee2f", 0, 0, 1080, 1440, .5, "dim")
    + box(90, 90, 900, 300, [T("What’s In", 116, C, it=True), T("My Bag?", 116, C, it=True)], gap=4, cls="shd")
    + box(90, 400, 900, 100, [T(AT, 64, C, it=True)], cls="shd")
    + rect(170, 540, 740, 480)
    + box(210, 580, 660, 400, [T("(47)", 110, G, it=True), T("By Our Student", 64, K), T("«Говори о том, что любишь»", 44, G, it=True, extra="white-space:nowrap")], gap=26)
    + box(90, 1065, 900, 250, [T("Что внутри сумки —", 64, C, it=True), T("на английском", 64, C, it=True)], gap=10, valign="top", cls="shd"))

# 16 фото, подпись сверху, @, светлая карточка с курсивом, логотип внизу
L[16] = page(img("3a12a672", 0, 0, 1080, 1440, .3)
    + box(90, 380, 900, 110, [T(AT, 72, C, it=True)], cls="shd")
    + rect(140, 520, 800, 520)
    + box(180, 560, 720, 440, [T("Podcast", 110, K, it=True), T("By Our Student", 90, K, it=True), T("(9) · 0–A1 Level", 46, G)], gap=24)
    + box(90, 1085, 900, 150, [T("«Просто начни говорить»", 52, C, it=True, extra="white-space:nowrap")], valign="top", cls="shd"))

if __name__ == "__main__":
    for i, h in L.items():
        open(os.path.join(OUT, f"m{i:02d}.html"), "w").write(h)
    print(len(L))
