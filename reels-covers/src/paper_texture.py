"""Реалистичная текстура хлопковой бумаги (волокна, неровность, крапинки). out.png size"""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
out, S = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2400
rng = np.random.default_rng(11)

def blurred(sigma, w):
    n = Image.fromarray((rng.random((S, S)) * 255).astype(np.uint8))
    return (np.asarray(n.filter(ImageFilter.GaussianBlur(sigma))).astype(np.float32) / 255 - .5) * w

lum = blurred(0.6, 0.10) + blurred(2.5, 0.35) + blurred(14, 0.9) + blurred(70, 1.6)
lum = lum / (np.abs(lum).max() + 1e-6) * 0.035          # ±3.5 % неровности
# волокна
fib = Image.new("L", (S, S), 0); d = ImageDraw.Draw(fib)
for _ in range(S * 3):
    x, y = rng.random(2) * S; a = rng.random() * np.pi; L = 6 + rng.random() * 26
    d.line([(x, y), (x + np.cos(a) * L, y + np.sin(a) * L)], fill=int(40 + rng.random() * 60), width=1)
fib = np.asarray(fib.filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255
# крапинки
sp = (rng.random((S, S)) > 0.99985).astype(np.float32)
sp = np.asarray(Image.fromarray((sp * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1))).astype(np.float32) / 255
base = np.array([246, 242, 233], np.float32) / 255
img = base[None, None, :] * (1 + lum[..., None]) - fib[..., None] * 0.035 - sp[..., None] * 0.25 * np.array([.6, .7, .8])
Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save(out, quality=95)
