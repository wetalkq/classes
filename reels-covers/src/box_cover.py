"""Обложка 9:16 для Reels с коробкой: бархат во весь кадр, коробка по центру, весь текст бежевый (Times New Roman)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
B = os.path.join(ROOT, "box"); F = os.path.join(ROOT, "fonts")
W, H, S = 1080, 1920, 2
BE = (210, 206, 195)
REG, IT = "timesnrcyrmt.ttf", "timesnrcyrmt_inclined.ttf"
def font(n, s): return ImageFont.truetype(os.path.join(F, n), s * S)

# фон: бархат на весь кадр, лёгкая виньетка
BGF = sys.argv[1] if len(sys.argv) > 1 else "velvet_bg.png"
OUTN = sys.argv[2] if len(sys.argv) > 2 else "WeTalk_korobka_oblozhka_v2.jpg"
bg = Image.open(os.path.join(B, BGF)).convert("RGB").resize((W * S, H * S), Image.LANCZOS)
# подгоняем средний цвет под бархат
ref = np.asarray(Image.open(os.path.join(B, "velvet_bg.png")).convert("RGB").resize((270, 480))).reshape(-1, 3).mean(0)
RAW = BGF.startswith("fur/fon2_")           # готовая шкура: цвет и виньетка уже применены
if not RAW:
    ba = np.asarray(bg).astype(np.float32); ba *= (ref / ba.reshape(-1, 3).mean(0))[None, None]
    bg = Image.fromarray(np.clip(ba, 0, 255).astype(np.uint8))
yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
r = np.sqrt(((xx - W * S / 2) / (W * S * .75)) ** 2 + ((yy - H * S / 2) / (H * S * .75)) ** 2)
vig = np.ones_like(r) if RAW else np.clip(1.08 - .45 * r ** 2, .55, 1.08)
im = Image.fromarray(np.clip(np.asarray(bg).astype(np.float32) * vig[..., None], 0, 255).astype(np.uint8)).convert("RGBA")

# коробка
box = Image.open(os.path.join(B, "box_cut.png")).convert("RGBA")
BW = 820; k = BW / box.width
b = box.resize((BW * S, round(box.height * k * S)), Image.LANCZOS)
CY = 1010; top = CY - b.height // (2 * S)
sh = Image.new("RGBA", (b.width + 240 * S, b.height + 240 * S), (0, 0, 0, 0))
m = Image.new("RGBA", b.size, (5, 6, 2, 0)); m.putalpha(b.split()[3].point(lambda v: int(v * .75)))
sh.paste(m, (120 * S, 120 * S)); sh = sh.filter(ImageFilter.GaussianBlur(28 * S))
im.alpha_composite(sh, ((W * S - sh.width) // 2 + 14 * S, top * S - 120 * S + 34 * S))
im.alpha_composite(b, ((W * S - b.width) // 2, top * S))

def ys(y_box): return top + y_box * k          # координата из box_cut -> кадр
LID = (ys(50) + ys(630)) / 2                   # центр крышки (кружево)
BOT0, BOT1 = ys(740), ys(1420)                 # нижнее отделение (бархат)

# текст с мягкой тенью для читаемости
def block(items):
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for txt, f, s, y in items: d.text((W // 2 * S, y * S), txt, font=font(f, s), fill=(8, 10, 4, 235), anchor="mm")
    L = L.filter(ImageFilter.GaussianBlur(9 * S)); im.alpha_composite(L); im.alpha_composite(L)
    d = ImageDraw.Draw(im)
    for txt, f, s, y in items: d.text((W // 2 * S, y * S), txt, font=font(f, s), fill=BE + (255,), anchor="mm")

block([("@WeTalk.Ru", IT, 40, top - 52)])
block([("Спроси", IT, 118, LID - 62), ("Свой AI", IT, 118, LID + 62)])
bc = (BOT0 + BOT1) / 2
block([("Чем Бы Он Заполнил", IT, 60, bc - 78), ("Эту Коробку?", IT, 60, bc - 8),
       ("промпт ждёт тебя в описании", IT, 36, bc + 92)])

out = im.resize((W, H), Image.LANCZOS).convert("RGB")
p = os.path.join(B, OUTN); out.save(p, quality=95)
out.crop((0, 240, W, 1680)).resize((270, 360), Image.LANCZOS).save(os.path.join(B, "oblozhka_grid.jpg"), quality=92)
print(p, round(top), round(top + b.height / S), round(LID), round(BOT0), round(BOT1))
