"""Подготовка фото: кадр под рамку, увеличение (Lanczos), резкость, лёгкая единая цветокоррекция, зерно.
usage: v2_prep.py src.jpg dst.jpg W H [focus_y]"""
import sys, numpy as np
from PIL import Image, ImageFilter

src, dst, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
fy = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
im = Image.open(src).convert("RGB")
r = W / H
if im.width / im.height > r:
    nw = round(im.height * r); x = (im.width - nw) // 2
    im = im.crop((x, 0, x + nw, im.height))
else:
    nh = round(im.width / r); y = int((im.height - nh) * fy)
    im = im.crop((0, y, im.width, y + nh))
# мягкое двухшаговое увеличение
mid = im.resize((im.width * 3 // 2, im.height * 3 // 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
im = mid.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2.0, 70, 3))
a = np.asarray(im).astype(np.float32) / 255
lum = (a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
a = lum + (a - lum) * 0.85                      # чуть приглушить
a = a * np.array([1.02, 1.0, 0.95], np.float32)  # тепло
a = 0.03 + a * 0.95                              # плёночные тени
a += np.random.default_rng(1).normal(0, 0.018, a.shape[:2])[..., None]  # зерно
Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(dst, quality=94)
