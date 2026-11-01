"""v12 — обложки для ВСЕХ Reels ленты (data.REELS) на 16 одобренных раскладках v11.
Рубрика/номер/уровень — из ленты; фото — все 30 по кругу; у каждой обложки своя цитата."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11_mockups as V
from v11_mockups import T, box, page, img, rect, G, B, C, O, K, AT
from data import REELS

OUT = os.path.join(V.ROOT, "v12"); os.makedirs(OUT, exist_ok=True)

PHOTOS = ["ee305f34", "b5e6f2e0", "38779c67", "dbb02000", "103875d7", "ebe280e1", "6998d97e", "eb1025f3", "a582ad4e",
          "11851dde", "85387ce9", "387e0534", "5629baa1", "61531651", "ce64ee2f", "1cdd24a5", "3a12a672", "f50a214e",
          "1ae65af8", "3ed5d9fc", "60b88bb9", "636e13bc", "f87941ba", "7ad957ee", "9b22d97e", "93414a44", "00485080",
          "3188b3cc", "b244f84d", "62180978"]
QUOTES = ["Говори — даже если страшно", "Каждое слово — шаг вперёд", "Ошибки — это рост", "Начни с одной фразы",
          "Немного каждый день", "Начни сегодня", "Язык — это привычка", "Слушай, повторяй, говори",
          "Ты знаешь больше, чем думаешь", "15 минут в день меняют всё", "Новый язык — новая версия тебя",
          "Уверенность — в практике", "Говори больше", "Говори о том, что любишь", "Шаг за шагом", "Просто начни говорить",
          "Практика сильнее страха", "Слова оживают в речи", "Твой темп — правильный", "Английский — это свобода",
          "Пробуй снова и снова", "Каждый день — новый шанс", "Говори, а не заучивай", "Мир станет ближе",
          "Ты уже на пути", "Смелость — первый урок", "Учись с удовольствием", "Маленький шаг — большой путь",
          "Говори как живёшь", "Верь в свой голос"]

_pi = 0
def nextp(n=1):
    global _pi
    r = [PHOTOS[(_pi + k) % len(PHOTOS)] for k in range(n)]; _pi += n
    return r if n > 1 else r[0]

def cap(s): return " ".join(w[:1].upper() + w[1:] for w in s.split())

def info_of(d):
    lvl = (d.get("level") or "").replace("-", "–")
    if d["kind"] == "bag":
        t = ("What’s In", "My Bag?")
        meta = " · ".join(x for x in [f"({d['num']})" if d.get("num") else "", lvl or "By Our Student"] if x)
    elif d["kind"] == "podcast":
        t = ("Podcast", "By Our Student")
        meta = " · ".join(x for x in [f"({d['num']})" if d.get("num") else "", lvl or d.get("place") or ""] if x) or "English Podcast"
    else:
        tl = d["title"]
        t = (cap(tl[0]), cap(tl[1]) if len(tl) > 1 else "")
        meta = d.get("quote", "")
    return t, meta

def q(text, fs, col): return T(f"«{text}»", fs, col, it=True, extra="white-space:nowrap")


def lay(n, t, meta, quote):
    t1, t2 = t; full = f"{t1} {t2}".strip()
    if n == 1:
        return page(img(nextp(), 0, 0, 1080, 1440, .3, "dim") + box(90, 70, 900, 120, [T(AT, 60, C, it=True)], cls="shd")
            + box(90, 760, 900, 380, [T(t1, 110, C, 700), T(t2, 110, C, 700), T(meta, 46, C, ls=2)], gap=18, cls="shd")
            + box(90, 1160, 900, 150, [q(quote, 54, C)], valign="top", cls="shd"))
    if n == 2:
        return page(img(nextp(), 0, 0, 1080, 840, .4) + rect(0, 840, 1080, 600, B)
            + box(70, 870, 940, 240, [T(t1, 96, K, 700), T(t2, 96, K, 700)], gap=6, align="left")
            + box(70, 1130, 940, 60, [q(quote, 42, G)], align="left") + box(70, 1205, 940, 60, [T(meta, 44, K)], align="left")
            + box(0, 1290, 1080, 80, [T(AT, 52, O, it=True)]))
    if n == 3:
        return page(box(0, 50, 1080, 80, [T(AT, 54, O, it=True)]) + box(90, 150, 900, 220, [T("Новый Выпуск", 76, K), T(full, 64, O, it=True)], gap=16)
            + img(nextp(), 190, 400, 700, 700, .5) + box(90, 1135, 900, 180, [T(meta, 52, G), q(quote, 52, K)], gap=18, valign="top"))
    if n == 4:
        return page(box(0, 150, 1080, 120, [T(AT, 64, B, it=True)]) + rect(120, 340, 840, 760, C, 30)
            + box(170, 380, 740, 680, [T(t1, 120, G, 700), T(t2, 96, G, 700), T(meta, 48, K, ls=2)], gap=26)
            + box(90, 1150, 900, 200, [q(quote, 62, C)], valign="top"), bg=G)
    if n == 5:
        return page(box(90, 140, 900, 120, [T(AT, 64, O, it=True)]) + rect(90, 290, 440, 760)
            + box(130, 330, 360, 680, [T(t1, 84, G, 700), T(t2, 84, G, 700), T(meta, 50, O, it=True)], gap=30)
            + img(nextp(), 550, 290, 440, 760, .4)
            + box(60, 1095, 960, 260, [T(full.upper(), 76, K, 700), q(quote, 56, G)], gap=22, valign="top"))
    if n == 6:
        ps = nextp(5)
        coll = [(230, 340, 330, 420), (70, 560, 400, 320), (360, 300, 380, 640), (700, 370, 300, 340), (720, 630, 280, 340)]
        return page(box(90, 130, 900, 140, [T(full, 72, K)]) + "".join(img(p, *g, .4) for p, g in zip(ps, coll))
            + box(90, 1005, 900, 330, [T(meta, 60, O, 700), q(quote, 58, K), T(AT, 56, O, it=True)], gap=22, valign="top"))
    if n == 7:
        a, b = nextp(2)
        return page(box(60, 60, 960, 420, [T(t1, 130, K), T(t2, 130, K)], gap=4, align="left")
            + box(60, 470, 960, 160, [T("— " + meta, 50, K), q(quote, 44, G)], gap=16, align="left", valign="top")
            + box(0, 640, 1080, 70, [T(AT, 56, O, it=True)]) + img(a, 40, 720, 485, 660, .4, r=22) + img(b, 555, 720, 485, 660, .4, r=22))
    if n == 8:
        return page(box(90, 120, 900, 140, [T(AT, 84, O, it=True)]) + box(90, 270, 900, 300, [T(t1, 96, K, 700, True), T(t2, 96, K, 700, True)], gap=8)
            + box(90, 580, 900, 170, [T(meta, 52, G), q(quote, 44, K)], gap=16) + img(nextp(), 40, 790, 1000, 610, .5))
    if n == 9:
        return page(img(nextp(), 0, 0, 1080, 1440, .5, "dim") + box(0, 610, 1080, 90, [T(AT, 64, C, it=True)], cls="shd")
            + box(70, 720, 940, 480, [T(t1.upper(), 120, C, 700), T(t2.upper(), 120, C, 700), T(meta, 54, C)], gap=18, align="left", valign="bottom", cls="shd")
            + box(70, 1225, 940, 80, [q(quote, 44, C)], align="left", valign="top", cls="shd"))
    if n == 10:
        return page(img(nextp(), 0, 0, 1080, 1440, .4, "dim") + box(60, 130, 960, 230, [T(t1.upper(), 104, C, 700), T(t2.upper(), 84, C, 700)], gap=8, cls="shd")
            + rect(160, 420, 760, 560) + box(200, 460, 680, 480, [T(meta, 66, K), q(quote, 46, G)], gap=30)
            + box(90, 1020, 900, 100, [T(AT, 66, C, it=True)], valign="top", cls="shd"))
    if n == 11:
        w = quote.split()
        return page(box(90, 200, 900, 230, [T(t1, 96, C, 700), T(t2, 80, C, 700)], gap=8) + box(90, 440, 900, 100, [T(AT, 60, B, it=True)])
            + img(nextp(), 0, 580, 330, 600, .3) + rect(375, 580, 330, 600) + rect(750, 580, 330, 600)
            + box(400, 610, 280, 540, [T(x, 60, G, 700) for x in meta.split(" · ")], gap=34)
            + box(775, 610, 280, 540, [T(("«" if i == 0 else "") + x + ("»" if i == len(w) - 1 else ""), 54, G, it=True) for i, x in enumerate(w)], gap=14), bg=G)
    if n == 12:
        return page(img(nextp(), 0, 0, 1080, 1440, .4) + rect(170, 150, 740, 840)
            + box(210, 190, 660, 760, ([T("The", 130, K, it=True)] if t1 == "Podcast" else []) + [T(t1, 104, K), T(t2, 84, K), T(meta, 44, G, it=True)], gap=22)
            + box(90, 1030, 900, 100, [T(AT, 72, C, it=True)], valign="top", cls="shd")
            + box(90, 1135, 900, 150, [q(quote, 54, C)], valign="top", cls="shd"))
    if n in (13, 15):
        return page(img(nextp(), 40, 40, 1000, 540, .4) + box(90, 610, 900, 250, [T(t1, 90, G, it=True), T(t2, 90, G, it=True)], gap=4)
            + box(90, 870, 900, 80, [T(meta, 46, K, 700, True)]) + rect(170, 980, 740, 210, "transparent", 24, f"border:2px solid {G};")
            + box(200, 1000, 680, 170, [q(quote, 60, K)]) + box(90, 1220, 900, 170, [T("Новый выпуск", 60, K, it=True), T(AT, 54, O, it=True)], gap=14, valign="top"))
    if n == 14:
        return page(img(nextp(), 0, 0, 1080, 1440, .5, "dim") + box(90, 90, 900, 300, [T(t1, 116, C, it=True), T(t2, 116, C, it=True)], gap=4, cls="shd")
            + box(90, 400, 900, 100, [T(AT, 64, C, it=True)], cls="shd") + rect(170, 540, 740, 480)
            + box(210, 580, 660, 400, [T(meta, 64, K), q(quote, 46, G)], gap=30))
    if n == 16:
        return page(img(nextp(), 0, 0, 1080, 1440, .3) + box(90, 380, 900, 110, [T(AT, 72, C, it=True)], cls="shd") + rect(140, 520, 800, 520)
            + box(180, 560, 720, 440, [T(t1, 110, K, it=True), T(t2, 90, K, it=True), T(meta, 46, G)], gap=24)
            + box(90, 1085, 900, 150, [q(quote, 52, C)], valign="top", cls="shd"))


if __name__ == "__main__":
    items = []
    for i, d in enumerate(REELS):
        t, meta = info_of(d)
        n = i % 16 + 1
        name = f"{i+1:02d}_ряд{d['r']+1:02d}-{d['c']+1}_{d['kind']}" + (f"-{d['num']:02d}" if d.get("num") else "")
        open(os.path.join(OUT, name + ".html"), "w").write(lay(n, t, meta, QUOTES[i % len(QUOTES)]))
        items.append(dict(name=name, r=d["r"], c=d["c"], layout=n))
    json.dump(items, open(os.path.join(OUT, "items.json"), "w"), ensure_ascii=False)
    print(len(items))
