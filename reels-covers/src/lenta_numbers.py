"""Нумерация постов на скриншотах ленты: аккуратный бежевый кружок с зелёным номером в левом верхнем углу плитки."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lenta")
F = os.path.join(D, "..", "fonts", "timesnrcyrmt.ttf")
G, BE = (65, 80, 56), (210, 206, 195)
COLS = [(0, 275), (277, 552), (554, 828)]
START = {1: 1, 2: 5, 3: 9, 4: 13, 5: 17, 6: 21, 7: 25, 8: 27}   # номер первого полного ряда
S = 3
for k in range(1, 9):
    im = Image.open(os.path.join(D, f"ss{k}.png")).convert("RGB")
    a = np.asarray(im.convert("L")).astype(int)
    rf = (a > 238).mean(1); seps = [y for y in range(96, 1626) if rf[y] > .97] + [1626]
    # верхние края полных рядов
    edges = []
    for y in seps:
        if not edges or y - edges[-1] > 3: edges.append(y)
    tops = [e + 2 for e in edges[:-1] if edges[edges.index(e) + 1] - e > 360]
    big = im.resize((im.width * S, im.height * S), Image.LANCZOS).convert("RGBA")
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    lay = Image.new("RGBA", big.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    r = 21
    for ri, top in enumerate(tops):
        row = START[k] + ri
        for ci, (x0, x1) in enumerate(COLS):
            n = (row - 1) * 3 + ci + 1
            cx, cy = x0 + 14 + r, top + 14 + r
            box = ((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S)
            ds.ellipse(((cx - r + 1) * S, (cy - r + 3) * S, (cx + r + 1) * S, (cy + r + 3) * S), fill=(0, 0, 0, 90))
            d.ellipse(box, fill=BE + (250,), outline=G + (255,), width=int(1.6 * S))
            f = ImageFont.truetype(F, int((22 if n < 100 else 18) * S))
            d.text((cx * S, (cy + 1) * S), str(n), font=f, fill=G + (255,), anchor="mm")
    big.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3 * S))); big.alpha_composite(lay)
    big.resize(im.size, Image.LANCZOS).convert("RGB").save(os.path.join(D, f"lenta_{k}.jpg"), quality=95)
    print(k, len(tops), "rows from post", (START[k] - 1) * 3 + 1, "to", (START[k] - 1 + len(tops)) * 3)
