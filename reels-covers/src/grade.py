"""Единая цветокоррекция фото под бренд: приглушённо, тепло, тени в зелёный, лёгкое зерно.
raw/<id>.jpg → graded/<id>.jpg  (2160×3840)"""
import os, sys, numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "photos")
os.makedirs(os.path.join(ROOT, "graded"), exist_ok=True)
W, H = 2160, 3840
SHADOW = np.array([0x1E, 0x25, 0x1A], np.float32)   # глубокий зелёный
LIGHT = np.array([0xE6, 0xDF, 0xD0], np.float32)    # тёплый бежевый


def grade(src, dst, focus_y=0.5):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = int((im.height - H) * focus_y)
    a = np.asarray(im.crop((x, y, x + W, y + H))).astype(np.float32) / 255
    lum = (a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    # 1) приглушить насыщенность
    a = lum + (a - lum) * 0.62
    # 2) сплит-тон к палитре бренда (30 %)
    tone = (SHADOW + (LIGHT - SHADOW) * lum) / 255
    a = a * 0.70 + tone * 0.30
    # 3) мягкий контраст + приподнятые тени (плёнка)
    a = 0.04 + a * 0.92
    # 4) затемнение под текст: общее + к центру/краям
    yy = np.linspace(-1, 1, H)[:, None, None]
    xx = np.linspace(-1, 1, W)[None, :, None]
    vign = 1 - 0.28 * np.clip(xx ** 2 * 0.6 + yy ** 2 * 0.5, 0, 1)
    a = a * 0.72 * vign
    # 5) зерно
    a += np.random.default_rng(3).normal(0, 0.012, a.shape[:2])[..., None]
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    out.save(dst, quality=92)


if __name__ == "__main__":
    for f in sorted(os.listdir(os.path.join(ROOT, "raw"))):
        grade(os.path.join(ROOT, "raw", f), os.path.join(ROOT, "graded", f))
    print("graded", len(os.listdir(os.path.join(ROOT, "graded"))))
