"""Анализ ленты: вырезаем 90 плиток, считаем цвет/яркость/фактуру, ищем гармоничный порядок."""
import os, json, numpy as np
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lenta")
COLS = [(0, 275), (277, 552), (554, 828)]
START = {1: 1, 2: 5, 3: 9, 4: 13, 5: 17, 6: 21, 7: 25, 8: 27}
tiles = {}; where = {}
for k in range(1, 9):
    im = Image.open(os.path.join(D, f"ss{k}.png")).convert("RGB")
    a = np.asarray(im.convert("L")).astype(int)
    rf = (a > 238).mean(1); seps = [y for y in range(96, 1626) if rf[y] > .97] + [1626]
    edges = []
    for y in seps:
        if not edges or y - edges[-1] > 3: edges.append(y)
    tops = [e + 2 for i, e in enumerate(edges[:-1]) if edges[i + 1] - e > 360]
    for ri, top in enumerate(tops):
        for ci, (x0, x1) in enumerate(COLS):
            n = (START[k] + ri - 1) * 3 + ci + 1
            where.setdefault(n, []).append((k, x0, top))
            if n not in tiles: tiles[n] = im.crop((x0, top, x1, top + 366))
os.makedirs(os.path.join(D, "tiles"), exist_ok=True)
for n, t in tiles.items(): t.save(os.path.join(D, "tiles", f"{n:02d}.png"))
json.dump(where, open(os.path.join(D, "where.json"), "w"))
print(len(tiles))
