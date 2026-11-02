"""Ракушка: стираем «Salt & Silk» с карточки и выдавливаем свою фразу (Times New Roman Italic, тиснение)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
S = os.path.join(ROOT, "shell")
PHRASE = sys.argv[1] if len(sys.argv) > 1 else "How do you see me?"
X0, Y0, X1, Y1 = 488, 818, 1028, 1102          # карточка
IN = 10                                         # отступ от края карточки

im = Image.open(os.path.join(S, "shell_cut.png")).convert("RGBA")
a = np.asarray(im).astype(np.float32)
x0, y0, x1, y1 = X0 + IN, Y0 + IN, X1 - IN, Y1 - IN
card = a[y0:y1, x0:x1, :3]
h, w = card.shape[:2]
# гладкая подложка: билинейная интерполяция по краевым полосам (без текста)
top, bot = card[:12].mean(0), card[-12:].mean(0)
left, right = card[:, :12].mean(1), card[:, -12:].mean(1)
yy = np.linspace(0, 1, h)[:, None, None]; xx = np.linspace(0, 1, w)[None, :, None]
v = top[None] * (1 - yy) + bot[None] * yy
hz = left[:, None] * (1 - xx) + right[:, None] * xx
base = (v + hz) / 2
base += np.random.default_rng(2).normal(0, 1.6, (h, w, 1))
a[y0:y1, x0:x1, :3] = base

# тиснение
fnt = ImageFont.truetype(os.path.join(ROOT, "fonts", "PinyonScript-Regular.ttf"), 64)
m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
d.text((w / 2, h / 2), PHRASE, font=fnt, fill=255, anchor="mm")
m = m.filter(ImageFilter.GaussianBlur(0.6))
M = np.asarray(m).astype(np.float32) / 255
hi = np.roll(np.roll(M, -2, 0), -2, 1); sh = np.roll(np.roll(M, 2, 0), 2, 1)
hi = np.asarray(Image.fromarray((hi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32) / 255
reg = a[y0:y1, x0:x1, :3]
reg = reg + (255 - reg) * (hi * 0.55)[..., None]      # свет сверху-слева
reg = reg * (1 - (sh * 0.22)[..., None])               # тень снизу-справа
reg = reg * (1 - M * 0.04)[..., None] + M[..., None] * 3
a[y0:y1, x0:x1, :3] = np.clip(reg, 0, 255)
out = Image.fromarray(a.astype(np.uint8), "RGBA")
out.save(os.path.join(S, "shell_final.png"))
bg = Image.new("RGBA", out.size, (210, 206, 195, 255)); bg.alpha_composite(out)
bg.crop((400, 720, 1100, 1180)).convert("RGB").save(os.path.join(S, "card_preview.jpg"), quality=92)
print("ok")
