"""Гармоничная раскладка ленты: тёмные плитки по диагонали (по одной в ряд), одинаковые дизайны не рядом,
порядок по возможности близок к хронологии. Итог: новые номера позиций на скриншотах + превью."""
import os, json, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lenta")
F = os.path.join(D, "..", "fonts", "timesnrcyrmt.ttf"); FI = os.path.join(D, "..", "fonts", "timesnrcyrmt_inclined.ttf")
G, BE = (65, 80, 56), (210, 206, 195)
N = 90; ROWS = 30
DARK = [7, 23, 25, 3, 14, 31, 52, 80, 43, 21, 34, 18, 19, 86, 61, 39, 46, 69, 2, 35, 78, 59, 13, 45, 36, 87, 56, 72, 4, 15]
GROUPS = {"zebra": [3, 7, 23, 25], "oval": [18, 19, 34], "chair": [31, 52], "olive": [61, 86, 43],
          "clip": [4, 9, 15], "stripe": [1, 2, 6, 10, 20, 22, 30, 37], "plainpod": [41, 48, 68, 75, 77, 79],
          "plainbag": [16, 82, 84, 88, 90], "shag": [28, 42, 70, 73, 81], "legs": [53, 57], "newrel": [64, 67, 71],
          "card": [56, 58, 69, 76, 78, 87], "glove": [5, 12], "twophoto": [60, 66, 85, 63, 62, 65, 74, 32],
          "promo": [8, 17, 24, 26, 27, 29, 33, 38, 40, 44, 47, 49, 51, 54, 55, 83, 89, 11, 21, 35, 39, 45, 46, 59, 14, 36]}
grp = {}
for g, ms in GROUPS.items():
    for m in ms: grp.setdefault(m, g)
LIGHT = [n for n in range(1, N + 1) if n not in DARK]
dslots = [r * 3 + (r % 3) for r in range(ROWS)]                 # диагональ
lslots = [p for p in range(N) if p not in dslots]

def cost(order):                                                # order[p] = пост на позиции p
    c = 0
    for p, n in enumerate(order):
        c += abs(p - (n - 1)) * .04                               # близость к хронологии
        r, col = divmod(p, 3)
        for dr, dc, w in ((0, 1, 1.0), (1, 0, 1.0), (1, 1, .5), (1, -1, .5), (2, 0, .25), (0, 2, .3)):
            rr, cc = r + dr, col + dc
            if 0 <= cc < 3 and rr < ROWS:
                m = order[rr * 3 + cc]
                if grp.get(n) and grp.get(n) == grp.get(m):
                    c += (4 if grp[n] == "promo" else 12) * w
    return c

def build(d, l):
    o = [0] * N
    for s, n in zip(dslots, d): o[s] = n
    for s, n in zip(lslots, l): o[s] = n
    return o

random.seed(4)
d, l = sorted(DARK), sorted(LIGHT); cur = build(d, l); cc = cost(cur); T = 6.0
best, bc = cur[:], cc
for it in range(120000):
    nd, nl = d[:], l[:]
    if random.random() < .35:
        i, j = random.sample(range(len(nd)), 2); nd[i], nd[j] = nd[j], nd[i]
    else:
        i, j = random.sample(range(len(nl)), 2); nl[i], nl[j] = nl[j], nl[i]
    o = build(nd, nl); c = cost(o)
    if c < cc or random.random() < math.exp((cc - c) / T):
        d, l, cur, cc = nd, nl, o, c
        if c < bc: best, bc = o[:], c
    T = max(.02, T * .99995)
print("cost", round(bc, 2))
newpos = {n: p + 1 for p, n in enumerate(best)}
json.dump({"order": best, "newpos": newpos}, open(os.path.join(D, "plan.json"), "w"))
moved = sum(1 for n, p in newpos.items() if n != p); print("moved", moved)

# --- превью новой ленты (3 картинки по 10 рядов)
tw, th, gap = 260, 346, 4
fnt = ImageFont.truetype(F, 30); small = ImageFont.truetype(FI, 20)
for part in range(3):
    W_ = 3 * tw + 2 * gap; H_ = 10 * th + 9 * gap
    s = Image.new("RGB", (W_, H_), (255, 255, 255))
    for p in range(part * 30, part * 30 + 30):
        n = best[p]; r, c = divmod(p - part * 30, 3)
        t = Image.open(os.path.join(D, "tiles", f"{n:02d}.png")).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = c * (tw + gap), r * (th + gap); s.paste(t, (x, y))
        dd = ImageDraw.Draw(s)
        dd.ellipse((x + 10, y + 10, x + 56, y + 56), fill=BE, outline=G, width=2)
        dd.text((x + 33, y + 34), str(p + 1), font=fnt, fill=G, anchor="mm")
    s.save(os.path.join(D, f"novaya_lenta_{part + 1}.jpg"), quality=93)

# --- скриншоты: на каждом посте номер его НОВОЙ позиции
where = json.load(open(os.path.join(D, "where.json")))
COLW = 275; S = 3; r0 = 23
for k in range(1, 9):
    im = Image.open(os.path.join(D, f"ss{k}.png")).convert("RGB")
    big = im.resize((im.width * S, im.height * S), Image.LANCZOS).convert("RGBA")
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    lay = Image.new("RGBA", big.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for n, locs in where.items():
        for (kk, x0, top) in locs:
            if kk != k: continue
            np_ = newpos[int(n)]
            cx, cy = x0 + 14 + r0, top + 14 + r0
            ds.ellipse(((cx - r0 + 1) * S, (cy - r0 + 3) * S, (cx + r0 + 1) * S, (cy + r0 + 3) * S), fill=(0, 0, 0, 90))
            dl.ellipse(((cx - r0) * S, (cy - r0) * S, (cx + r0) * S, (cy + r0) * S), fill=BE + (250,), outline=G + (255,), width=int(1.6 * S))
            dl.text((cx * S, (cy + 1) * S), str(np_), font=ImageFont.truetype(F, 22 * S), fill=G + (255,), anchor="mm")
    big.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3 * S))); big.alpha_composite(lay)
    big.resize(im.size, Image.LANCZOS).convert("RGB").save(os.path.join(D, f"perestanovka_{k}.jpg"), quality=95)
