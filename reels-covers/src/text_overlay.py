"""Прозрачный слой с текстом Times New Roman Cyr для страницы Canva 1080×1440 (рендер ×2).
usage: text_overlay.py out.png '<json list>'  — элементы: {t, f: r|i|bi, s, c, x, y}  (x,y = центр строки в px страницы)"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
FONT = {"r": "timesnrcyrmt.ttf", "i": "timesnrcyrmt_inclined.ttf", "bi": "timesnrcyrmt_boldinclined.ttf", "b": "timesnrcyrmt_bold.ttf"}
K = 2
out, items = sys.argv[1], json.loads(sys.argv[2])
im = Image.new("RGBA", (1080 * K, 1440 * K), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
for it in items:
    f = ImageFont.truetype(os.path.join(F, FONT[it["f"]]), int(it["s"] * K))
    d.text((it["x"] * K, it["y"] * K), it["t"], font=f, fill=it["c"], anchor="mm")
im.save(out)
