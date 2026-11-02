"""Фоны «шерсть животных» в фирменных цветах: основа строго #415038, узор строго #d2cec3.
Перекраска по яркости: тёмный класс -> зелёный, светлый -> бежевый, фактура шерсти сохраняется.
Плюс коробка с кружевом/бархатом, приведёнными к #415038."""
import os
import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = os.path.join(ROOT, "box", "fur")
G = np.array([65, 80, 56], np.float32); BE = np.array([210, 206, 195], np.float32)

def otsu(x):
    h, e = np.histogram(x, 256, (0, 1)); h = h.astype(np.float64); c = (e[:-1] + e[1:]) / 2
    w = np.cumsum(h); m = np.cumsum(h * c); mt = m[-1]
    s = (mt * w - m * (w[-1] - w)) ** 2 / np.maximum(w * (w[-1] - w), 1)   # межклассовая дисперсия
    s = (mt * w / w[-1] - m) ** 2 / np.maximum(w * (w[-1] - w), 1)
    return c[np.argmax(s)]

def brand(name):
    from PIL import ImageFilter
    a = np.asarray(Image.open(os.path.join(D, f"raw_{name}.png")).convert("RGB")).astype(np.float32) / 255
    L = a @ np.array([.299, .587, .114], np.float32)
    th = otsu(L.ravel()[::7])
    lo, hi = np.median(L[L < th]), np.median(L[L >= th])
    # мягкая маска узора: 0 = зелёный, 1 = бежевый (узкий переход, чтобы цвета были чистыми)
    m = 1 / (1 + np.exp(-(L - th) / ((hi - lo) * .07)))
    # фактура шерсти: мелкие детали яркости, со средним 0 в каждом классе
    blur = np.asarray(Image.fromarray((L * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    det = L - blur
    for cls in (L < th, L >= th): det[cls] -= det[cls].mean()
    det = np.clip(det / (det.std() + 1e-6), -2.5, 2.5)
    col = G[None, None] * (1 - m[..., None]) + BE[None, None] * m[..., None]
    out = col * (1 + .07 * det[..., None])
    out = np.clip(out, 0, 255).astype(np.uint8)
    im = Image.fromarray(out).resize((1080, 1920), Image.LANCZOS)
    im.save(os.path.join(D, f"fon_{name}.jpg"), quality=96)
    r = np.asarray(im).astype(np.float32).reshape(-1, 3); Lr = r @ np.array([.299, .587, .114], np.float32)
    print(name, "green", r[Lr < 120].mean(0).round(), "beige", r[Lr > 170].mean(0).round())

def box():
    b = Image.open(os.path.join(ROOT, "box", "box_cut.png")).convert("RGBA")
    a = np.asarray(b).astype(np.float32); rgb = a[..., :3]
    L = rgb @ np.array([.299, .587, .114], np.float32)
    chroma = rgb.max(-1) - rgb.min(-1)
    gmask = np.clip((chroma - 10) / 14, 0, 1) * (rgb[..., 2] < rgb[..., 1] - 6)   # зелёная ткань, не металл
    ratio = np.ones_like(L)
    for y0, y1 in ((0, 690), (690, L.shape[0])):          # крышка (кружево) и низ (бархат) отдельно
        sl = slice(y0, y1); med = np.median(L[sl][gmask[sl] > .5])
        ratio[sl] = (L[sl] / med) ** .75
    new = G[None, None] * ratio[..., None]
    rgb2 = rgb * (1 - gmask[..., None]) + new * gmask[..., None]
    a[..., :3] = np.clip(rgb2, 0, 255)
    Image.fromarray(a.astype(np.uint8), "RGBA").save(os.path.join(ROOT, "box", "box_cut_brand.png"))
    print("box fabric median ->", (G * 1).round())

if __name__ == "__main__":
    for n in ["zebra", "tiger", "giraffe", "panther", "cheetah"]: brand(n)
    box()
