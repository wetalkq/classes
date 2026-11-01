"""v10 — 16 макетов пользователя 1:1 по раскладке. 3:4, 1080×1440 CSS → ×2 = 2160×2880.
Только Times New Roman. Основа бежевый, буквы зелёные/чёрные/оранжевые; на зелёном — бежевые."""
import os, html, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
F = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "v10"); PH = os.path.join(OUT, "ph"); os.makedirs(PH, exist_ok=True)
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
.a{{position:absolute}} .c{{left:0;right:0;text-align:center}}
.f{{background-size:cover;background-position:center}}
.dim{{filter:brightness(.72)}}
.at{{font-style:italic;color:{O}}}
.lab{{font-size:24px;letter-spacing:1.5px;text-transform:uppercase}}
.row{{left:50px;right:50px;top:66px;display:flex;justify-content:space-between}}
.logo{{display:inline-block;border-top:1.5px solid currentColor;border-bottom:1.5px solid currentColor;padding:6px 18px 4px;font-size:58px;letter-spacing:6px;line-height:1}}
.logo small{{display:block;font-size:14px;letter-spacing:3px;margin-top:4px}}
.card{{background:{C}}}
.shd{{text-shadow:0 1px 6px rgba(0,0,0,.35)}}
"""
def page(body, extra=""): return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra}</style></head><body>{body}</body></html>"
def logo(col, size=58): return f'<div class="logo" style="color:{col};font-size:{size}px">WETALK<small>ENGLISH SCHOOL</small></div>'
def labrow(l, col=K, m="@wetalk.ru", r="2026"):
    return f'<div class="a row lab" style="color:{col}"><span>{l}</span><span style="text-transform:none">{m}</span><span>{r}</span></div>'


L = {}

# 1 — фото на весь кадр, логотип сверху, @ курсивом, заголовок по центру, подпись внизу
L[1] = page(f"""<div class="a f dim" style="inset:0;background-image:url(file://{ph('ee305f34',1080,1440,.3)})"></div>
<div class="a c" style="top:96px">{logo(C)}</div>
<div class="a c shd" style="top:330px;font-size:64px;font-style:italic;color:#f5f2ea">@WeTalk.Ru</div>
<div class="a c shd" style="top:820px;color:{C};font-weight:700;font-size:92px;line-height:1.12">Podcast By<br>Our Student</div>
<div class="a c shd" style="top:1080px;color:{C};font-size:40px;letter-spacing:3px">(37) · A2–B1 LEVEL</div>
<div class="a c shd" style="bottom:110px;color:{C};font-size:40px">WETALK | English school</div>""")

# 2 — фото сверху, светлая плашка снизу с крупным заголовком (как ForbesWoman)
L[2] = page(f"""<div class="a f" style="left:0;top:0;width:1080px;height:860px;background-image:url(file://{ph('b5e6f2e0',1080,860,.4)})"></div>
<div class="a" style="left:0;top:860px;width:1080px;height:580px;background:{C}"></div>
<div class="a" style="left:60px;right:60px;top:930px;font-weight:700;font-size:80px;line-height:1.12">What’s In My Bag:<br>Что Носит С Собой<br>Наша Студентка</div>
<div class="a" style="left:60px;bottom:80px;display:flex;align-items:baseline;gap:22px"><span style="font-weight:700;font-size:58px">WeTalk</span><span class="at" style="font-size:52px">@WeTalk.Ru</span></div>""")

# 3 — бежевый фон, текст сверху с выделенной фразой, квадратное фото, подпись снизу (как AAA)
L[3] = page(f"""<div class="a at" style="left:70px;top:90px;font-size:56px">@WeTalk.Ru</div>
<div class="a c" style="top:190px;font-size:64px;line-height:1.2">Новый Выпуск,<br>Но <span style="color:{O}">Только На Английском</span>:</div>
<div class="a f" style="left:190px;top:420px;width:700px;height:740px;background-image:url(file://{ph('38779c67',700,740,.5)})"></div>
<div class="a c" style="top:1215px;font-size:50px;line-height:1.2;color:{G}">Podcast <i>by our student</i><br>(30) · B1–B2 Level</div>
<div class="a c" style="bottom:40px;font-weight:700;font-size:30px;letter-spacing:4px">WETALK × @WETALK.RU</div>""")

# 4 — зелёный фон, вопрос сверху, @, светлая карточка с крупным названием, призыв снизу
L[4] = page(f"""<body style="background:{G}"><div class="a c" style="top:150px;color:{C};font-size:62px;line-height:1.15;letter-spacing:1px">ПОСЛУШАЛИ ВЫПУСК?<br>А ЧТО ДАЛЬШЕ?</div>
<div class="a c" style="top:345px;color:{B};font-style:italic;font-size:64px">@WeTalk.Ru</div>
<div class="a card" style="left:120px;top:480px;width:840px;height:620px;border-radius:30px"></div>
<div class="a c" style="top:590px;color:{K};font-size:42px;line-height:1.3">Чтобы английский звучал живо,<br>слушайте наш подкаст</div>
<div class="a c" style="top:780px;color:{G};font-weight:700;font-size:88px;line-height:1.1">PODCAST<br>BY OUR STUDENT</div>
<div class="a c" style="top:1200px;color:{C};font-size:46px;line-height:1.3">Новые выпуски — <b>каждую неделю</b><br>в наших Reels</div>""")

# 5 — строка-шапка, оранжевый абзац, две страницы (книга), крупный капс снизу
L[5] = page(f"""{labrow('ПОДКАСТ НАШИХ СТУДЕНТОВ')}
<div class="a c" style="top:150px;color:{O};font-size:38px;line-height:1.3">Ты знаешь слова, но в разговоре неловко.<br>В голове нет фраз, которые звучат в жизни</div>
<div class="a c at" style="top:300px;font-size:56px">@WeTalk.Ru</div>
<div class="a card" style="left:100px;top:400px;width:420px;height:600px;padding:44px 36px">
 <div style="color:{G};font-weight:700;font-size:52px;line-height:1">What’s In<br>My Bag?</div>
 <div style="color:{O};font-style:italic;font-size:30px;margin-top:18px">Phrases Worth Stealing</div>
 <div style="border:1.5px solid {G};margin-top:26px;padding:20px 18px;font-size:27px;line-height:1.7">(01) lip balm<br>(02) a good book<br>(03) sunglasses<br>(04) a notebook<br>(05) earphones<br>(06) keys</div></div>
<div class="a f" style="left:560px;top:400px;width:420px;height:600px;background-image:url(file://{ph('103875d7',420,600,.4)})"></div>
<div class="a card" style="left:590px;top:760px;width:360px;padding:18px 20px;font-size:26px;line-height:1.5;color:{K}"><b>How it sounds:</b><br>I always carry…<br>I can’t live without…</div>
<div class="a c" style="top:1080px;left:30px;right:30px;font-weight:700;font-size:50px;line-height:1.15">НАШ ПОДКАСТ НЕ ПРО ПРАВИЛА.<br>ОН ПРО ЖИВОЙ АНГЛИЙСКИЙ<br>БЕЗ СТРАХА</div>""")

# 6 — шапка, кавычки, цитата, коллаж из 5 фото, оранжевая строка + текст
coll = [("ebe280e1", 230, 470, 330, 420), ("6998d97e", 70, 680, 400, 320), ("eb1025f3", 360, 410, 380, 640), ("a582ad4e", 700, 480, 300, 340), ("dbb02000", 720, 740, 280, 340)]
L[6] = page(f"""{labrow('ПОДКАСТ НАШИХ СТУДЕНТОВ')}
<div class="a" style="left:50px;top:110px;color:{O};font-weight:700;font-size:170px;line-height:1">“</div>
<div class="a c" style="top:180px;left:120px;right:120px;font-size:42px;line-height:1.3">Я долго учила английский по учебникам<br>и поняла: говорить проще, когда<br>слышишь живую речь каждый день.</div>
<div class="a at" style="left:740px;top:385px;font-size:50px">@WeTalk.Ru</div>
{''.join(f'<div class="a f" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background-image:url(file://{ph(p,w,h,.4)})"></div>' for p,x,y,w,h in coll)}
<div class="a c" style="top:1110px;color:{O};font-weight:700;font-size:44px">Так появился наш подкаст:</div>
<div class="a c" style="top:1170px;font-weight:700;font-size:42px;line-height:1.3">студенты рассказывают о своей жизни<br>на английском — просто и честно.</div>
<div class="a" style="right:90px;top:1300px;color:{O};font-weight:700;font-size:200px;line-height:.6">”</div>""")

# 7 — цитата крупно, подпись, @, два фото со скруглёнными углами (как твит)
L[7] = page(f"""<div class="a" style="left:60px;right:60px;top:80px;font-size:56px;line-height:1.3">“Every episode, one of our students opens their bag and tells us what’s inside — in English. Real words, real life, real progress.”</div>
<div class="a" style="left:60px;top:560px;font-size:50px">— What’s In My Bag, (47)</div>
<div class="a at" style="left:60px;top:660px;font-size:64px">@WeTalk.Ru</div>
<div class="a f" style="left:40px;top:780px;width:485px;height:600px;border-radius:22px;background-image:url(file://{ph('dbb02000',485,600,.4)})"></div>
<div class="a f" style="left:555px;top:780px;width:485px;height:600px;border-radius:22px;background-image:url(file://{ph('11851dde',485,600,.4)})"></div>""")

# 8 — шапка, @ крупно, жирный курсив-заголовок, абзацы, фото снизу
L[8] = page(f"""{labrow('ПОДКАСТ В WETALK')}
<div class="a c at" style="top:130px;font-size:80px">@WeTalk.Ru</div>
<div class="a c" style="top:250px;font-weight:700;font-style:italic;font-size:60px;line-height:1.15">Потом Начинается Час<br>Живого Английского</div>
<div class="a c" style="top:420px;left:70px;right:70px;font-size:42px;line-height:1.35">Студент говорит много, на любимые темы.<br>Ведущий не перебивает на каждой ошибке.<br><br>Сначала ты заканчиваешь мысль, а потом<br>вместе разбираете, что звучало не совсем так.</div>
<div class="a f" style="left:40px;top:830px;width:1000px;height:560px;background-image:url(file://{ph('11851dde',1000,560,.5)})"></div>""")

# 9 — фото на весь кадр, шапка, @, огромный капс, подзаголовок, низ
L[9] = page(f"""<div class="a f dim" style="inset:0;background-image:url(file://{ph('85387ce9',1080,1440,.5)})"></div>
<div class="a" style="left:80px;top:96px;color:{C};font-weight:700;font-size:44px;letter-spacing:4px">WT</div>
<div class="a lab" style="right:80px;top:106px;color:{C};font-size:26px">WETALK / ENGLISH SCHOOL</div>
<div class="a shd" style="left:80px;top:740px;font-size:62px;font-style:italic;color:#f5f2ea">@WeTalk.Ru</div>
<div class="a shd" style="left:80px;top:850px;color:{C};font-weight:700;font-size:100px;line-height:1.02">WHAT’S IN<br>MY BAG?</div>
<div class="a shd" style="left:80px;top:1080px;color:{C};font-size:56px;line-height:1.15">рассказывает наша студентка:<br>(47) · by our student</div>
<div class="a lab shd" style="left:80px;bottom:80px;color:{C};font-size:26px">ШКОЛА ЖИВОГО АНГЛИЙСКОГО</div>
<div class="a shd" style="right:80px;bottom:66px">{logo(C,34)}</div>""")

# 10 — фото на весь кадр, шапка, крупный капс, светлая карточка-список, @, курсив снизу
L[10] = page(f"""<div class="a f dim" style="inset:0;background-image:url(file://{ph('6998d97e',1080,1440,.4)})"></div>
{labrow('PODCAST BY OUR STUDENT', C)}
<div class="a c shd" style="top:135px;left:30px;right:30px;color:{C};font-weight:700;font-size:58px;line-height:1.1">ЧТОБЫ ПОДКАСТ<br>ДЕЙСТВИТЕЛЬНО ПОМОГАЛ<br>АНГЛИЙСКОМУ:</div>
<div class="a card" style="left:140px;top:430px;width:800px;height:560px"></div>
<div class="a c" style="top:475px;font-size:42px;line-height:1.3;color:{K}">— слушайте по одному выпуску в день<br><br>— повторяйте фразы вслух<br><br>— выписывайте только полезные слова<br><br>— переслушайте выпуск через неделю</div>
<div class="a c shd" style="top:1060px;font-size:62px;font-style:italic;color:#f5f2ea">@WeTalk.Ru</div>
<div class="a c shd" style="top:1200px;color:{C};font-weight:700;font-style:italic;font-size:46px;line-height:1.3">Слушать проще своего уровня — не «сдаться»,<br>а дать себе шанс заговорить</div>""")

# 11 — зелёный фон, логотип, заголовок, курсив, @, три «страницы», призыв капсом
L[11] = page(f"""<body style="background:{G}"><div class="a c" style="top:80px">{logo(B,52)}</div>
<div class="a c" style="top:230px;color:{C};font-weight:700;font-size:66px;line-height:1.15">Не Уверены, Какой У Вас Уровень<br>И Что Слушать Дальше?</div>
<div class="a c" style="top:420px;color:{B};font-style:italic;font-size:42px;line-height:1.3">Начните с нашего подкаста<br>«Podcast by our student»</div>
<div class="a c" style="top:545px;color:{B};font-style:italic;font-size:58px">@WeTalk.Ru</div>
<div class="a f" style="left:0;top:650px;width:330px;height:540px;background-image:url(file://{ph('387e0534',330,540,.3)})"></div>
<div class="a" style="left:20px;top:1090px;color:{C};font-weight:700;font-size:34px">PODCAST</div>
<div class="a card" style="left:375px;top:650px;width:330px;height:540px;padding:34px 26px;color:{K}"><div style="font-weight:700;font-size:38px;line-height:1.1;color:{G}">КАК СЛУШАТЬ<br>ВЫПУСКИ</div><div style="font-size:26px;line-height:2;margin-top:26px">Уровень 0–A1 ........ 3<br>Уровень A2–B1 ...... 5<br>Уровень B1–B2 ...... 9</div></div>
<div class="a card" style="left:750px;top:650px;width:330px;height:540px;padding:34px 26px;color:{K}"><div style="font-weight:700;font-size:38px;line-height:1.1;color:{G}">ЧТО МЕНЯЕТСЯ<br>НА УРОВНЕ</div><div style="border-left:3px solid {G};padding-left:16px;font-size:24px;line-height:1.5;margin-top:26px"><b>A1</b> — базовые фразы<br><b>A2</b> — повседневная речь<br><b>B1</b> — связные рассказы<br><b>B2</b> — свобода и аргументы</div></div>
<div class="a c" style="top:1270px;color:{C};font-weight:700;font-size:46px;line-height:1.2">НОВЫЙ ВЫПУСК — УЖЕ В REELS</div>""")

# 12 — фото на весь кадр, светлая карточка по центру с названием, @ ниже, логотип внизу
L[12] = page(f"""<div class="a f" style="inset:0;background-image:url(file://{ph('5629baa1',1080,1440,.4)})"></div>
<div class="a card" style="left:170px;top:180px;width:740px;height:820px"></div>
<div class="a c" style="top:250px;font-size:40px;color:{K}">WETALK | English school</div>
<div class="a c" style="top:400px;font-style:italic;font-size:130px;line-height:1;color:{K}">The</div>
<div class="a c" style="top:520px;font-size:92px;line-height:1.05;color:{K}">Podcast<br>By Our Student</div>
<div class="a c" style="top:765px;color:{G};font-style:italic;font-size:40px;line-height:1.25">живой английский<br>от наших студентов</div>
<div class="a c" style="top:915px;font-style:italic;font-size:40px;color:{K}">(30) • B1–B2 Level</div>
<div class="a c shd" style="top:1060px;font-size:70px;font-style:italic;color:#f5f2ea">@WeTalk.Ru</div>
<div class="a c shd" style="bottom:90px">{logo(C,52)}</div>""")

# 13 — фото сверху, курсив-заголовок, зелёный курсив, жирный курсив, рамка со списком, крупный курсив
def info(pid, title, sub, lead, items, tail, fy=.4, two=False):
    sy, ly, by, ty = (790, 900, 960, 1260) if two else (720, 835, 895, 1210)
    return page(f"""<div class="a f" style="left:40px;top:40px;width:1000px;height:560px;background-image:url(file://{ph(pid,1000,560,fy)})"></div>
<div class="a shd" style="left:520px;top:520px;font-size:60px;font-style:italic;color:#f5f2ea">@WeTalk.Ru</div>
<div class="a c" style="top:625px;left:40px;right:40px;font-style:italic;font-size:76px;line-height:1.05;color:{G}">{title}</div>
<div class="a c" style="top:{sy}px;color:{G};font-style:italic;font-size:36px;line-height:1.3">{sub}</div>
<div class="a c" style="top:{ly}px;font-weight:700;font-style:italic;font-size:40px">{lead}</div>
<div class="a" style="left:170px;width:740px;top:{by}px;border:1.5px solid {G};border-radius:24px;padding:26px 20px;text-align:center;font-size:38px;line-height:1.45">{items}</div>
<div class="a c" style="top:{ty}px;font-style:italic;font-size:52px;line-height:1.1">{tail}</div>""")
L[13] = info("61531651", "Что Такое Podcast<br>By Our Student?", "Это короткие выпуски, где наши студенты<br>говорят о своей жизни на английском.",
             "В каждом выпуске вы услышите:", "— живую лексику и полезные фразы<br>— естественную грамматику<br>— истории о работе и путешествиях",
             "И всё это — в атмосфере<br>поддержки", two=True)

# 14 — фото на весь кадр, крупный курсив сверху, @, светлая карточка со списком, текст снизу
L[14] = page(f"""<div class="a f dim" style="inset:0;background-image:url(file://{ph('ce64ee2f',1080,1440,.5)})"></div>
<div class="a c shd" style="top:130px;color:{C};font-style:italic;font-size:92px;line-height:1.05">What’s In My Bag<br>Помогает:</div>
<div class="a c shd" style="top:380px;font-size:62px;font-style:italic;color:#f5f2ea">@WeTalk.Ru</div>
<div class="a card" style="left:120px;top:480px;width:840px;height:560px"></div>
<div class="a c" style="top:520px;left:150px;right:150px;font-size:40px;line-height:1.35;color:{K}">• учить слова на привычных вещах<br><br>• расширять запас современной лексикой<br><br>• начать <b><i>думать на английском</i></b><br><br>• говорить о себе легко и свободно</div>
<div class="a c shd" style="top:1120px;color:{C};font-weight:700;font-style:italic;font-size:40px">Потому что язык — это не только учебник.</div>
<div class="a c shd" style="top:1185px;color:{C};font-style:italic;font-size:62px;line-height:1.1">Это инструмент для жизни,<br>общения и идей.</div>""")

# 15 — как 13, «Формат»
L[15] = info("1cdd24a5", "Формат Подкаста", "Выпуски выходят в Reels<br>каждую неделю.",
             "Слушатели получают:", "— живые истории наших студентов<br>— современную лексику и фразы<br>— примеры речи на разных уровнях",
             "Каждый выпуск — всего<br>2–3 минуты в день.")

# 16 — фото на весь кадр, подпись сверху, @, светлая карточка с курсивом, логотип внизу
L[16] = page(f"""<div class="a f" style="inset:0;background-image:url(file://{ph('3a12a672',1080,1440,.3)})"></div>
<div class="a c shd" style="top:110px;color:{C};font-size:42px">WETALK | English school</div>
<div class="a c shd" style="top:400px;font-size:72px;font-style:italic;color:#f5f2ea">@WeTalk.Ru</div>
<div class="a card" style="left:120px;top:510px;width:840px;height:540px"></div>
<div class="a c" style="top:620px;font-style:italic;font-size:76px;line-height:1.12;color:{K}">Как Проходит Выпуск<br>Подкаста В WeTalk</div>
<div class="a c" style="top:880px;font-style:italic;font-size:42px;line-height:1.25;color:{G}">от первой секунды<br>до последней.</div>
<div class="a c shd" style="bottom:110px">{logo(C,52)}</div>""")

if __name__ == "__main__":
    for i, h in L.items():
        open(os.path.join(OUT, f"m{i:02d}.html"), "w").write(h)
    print(len(L))
