"""Обложка 9:16 для Reels с коробкой: бежевая бумага, арка из зелёного бархата, коробка, текст Times New Roman."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
B = os.path.join(ROOT, "box"); F = os.path.join(ROOT, "fonts")
W, H = 1080, 1920
G, O = (65, 80, 56), (218, 82, 0)
REG, IT, BD, BI = "timesnrcyrmt.ttf", "timesnrcyrmt_inclined.ttf", "timesnrcyrmt_bold.ttf", "timesnrcyrmt_boldinclined.ttf"
def font(n, s): return ImageFont.truetype(os.path.join(F, n), s)
S = 2  # суперсэмплинг

def paper():
    p = Image.open(os.path.join(ROOT, "v5", "paper.jpg")).convert("L").resize((W * S, H * S))
    pn = (np.asarray(p).astype(np.float32) / 255 - .93) * .6
    return Image.fromarray(np.clip(np.array([210, 206, 195], np.float32)[None, None] * (1 + pn[..., None]), 0, 255).astype(np.uint8)).convert("RGBA")

box = Image.open(os.path.join(B, "box_cut.png")).convert("RGBA")
velvet = box.crop((170, 860, 990, 1290)).convert("RGB")

# арка
AX0, AX1, AY0, AY1 = 150, 930, 560, 1470
aw, ah = (AX1 - AX0) * S, (AY1 - AY0) * S
v = velvet.resize((round(velvet.width * ah / velvet.height), ah), Image.LANCZOS)
v = v.crop(((v.width - aw) // 2, 0, (v.width - aw) // 2 + aw, ah)) if v.width >= aw else velvet.resize((aw, ah), Image.LANCZOS)
v = Image.fromarray(np.clip(np.asarray(v).astype(np.float32) * 1.08 + 4, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
mask = Image.new("L", (aw, ah), 0); md = ImageDraw.Draw(mask)
r = aw // 2
md.ellipse((0, 0, aw, 2 * r), fill=255); md.rectangle((0, r, aw, ah), fill=255)

im = paper()
sh = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
sm = Image.new("L", (W * S, H * S), 0); sm.paste(mask, (AX0 * S + 10 * S, AY0 * S + 18 * S))
sh.putalpha(sm.point(lambda x: int(x * .28))); sh = sh.filter(ImageFilter.GaussianBlur(22 * S))
im.alpha_composite(sh)
va = v.convert("RGBA"); va.putalpha(mask); im.alpha_composite(va, (AX0 * S, AY0 * S))
# тонкая бежевая линия-кант внутри арки
d = ImageDraw.Draw(im); ins = 18 * S; lw = 2 * S
x0, y0, x1, y1 = AX0 * S + ins, AY0 * S + ins, AX1 * S - ins, AY1 * S - ins
rr = (x1 - x0) // 2
d.arc((x0, y0, x1, y0 + 2 * rr), 180, 360, fill=(210, 206, 195, 170), width=lw)
d.line((x0, y0 + rr, x0, y1), fill=(210, 206, 195, 170), width=lw)
d.line((x1, y0 + rr, x1, y1), fill=(210, 206, 195, 170), width=lw)
d.line((x0, y1, x1, y1), fill=(210, 206, 195, 170), width=lw)

# коробка
BW = 560
b = box.resize((BW * S, round(box.height * BW * S / box.width)), Image.LANCZOS)
cx, cy = W // 2 * S, 1060 * S
bs = Image.new("RGBA", (b.width + 160 * S, b.height + 160 * S), (0, 0, 0, 0))
k = Image.new("RGBA", b.size, (15, 12, 8, 0)); k.putalpha(b.split()[3].point(lambda x: int(x * .55)))
bs.paste(k, (80 * S, 80 * S)); bs = bs.filter(ImageFilter.GaussianBlur(20 * S))
im.alpha_composite(bs, (cx - bs.width // 2 + 12 * S, cy - bs.height // 2 + 26 * S))
im.alpha_composite(b, (cx - b.width // 2, cy - b.height // 2))

def t(txt, f, s, col, y):
    d.text((W // 2 * S, y * S), txt, font=font(f, s * S), fill=col, anchor="mm")
d = ImageDraw.Draw(im)
t("@WeTalk.Ru", IT, 38, O, 320)
t("Чем AI Заполнит", REG, 74, G, 410)
t("Твою Коробку?", IT, 74, G, 492)
t("Промпт ждёт тебя в описании", IT, 40, G, 1560)

out = im.resize((W, H), Image.LANCZOS).convert("RGB")
p = os.path.join(B, "WeTalk_korobka_oblozhka.jpg"); out.save(p, quality=95)
g = out.crop((0, 240, W, 1680)).resize((270, 360), Image.LANCZOS); g.save(os.path.join(B, "oblozhka_grid.jpg"), quality=92)
print(p)
