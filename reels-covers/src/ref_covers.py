"""12 обложек 9:16 по 10 референсам (перчатки, конверт, тиснение, силуэты, кружевные рамки).
Цвета строго бренд: G #415038, BE #d2cec3, O #da5200 (оранжевый только по бежевому). Шрифт Times New Roman.
@WeTalk.Ru один раз, строго по центру."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
A = os.path.join(ROOT, "refs2"); OUT = os.path.join(ROOT, "ref_covers"); os.makedirs(OUT, exist_ok=True)
F = os.path.join(ROOT, "fonts")
W, H, S = 1080, 1920, 2
G, BE, O = (65, 80, 56), (210, 206, 195), (218, 82, 0)
DK = (24, 28, 18)
REG, IT = "timesnrcyrmt.ttf", "timesnrcyrmt_inclined.ttf"
rng = np.random.default_rng(3)
HANDLE_Y = 400          # 3:4-сетка ленты = y 240–1680, всё важное внутри с запасом

def font(n, s): return ImageFont.truetype(os.path.join(F, n), int(s * S))

def paper(col, amp=.05, fib=True):
    h, w = H * S, W * S
    n = rng.normal(0, 1, (h // 2, w // 2)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 30) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32) / 128 - 1
    big = rng.normal(0, 1, (h // 64, w // 64)).astype(np.float32)
    big = np.asarray(Image.fromarray(((big * 40) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 128 - 1
    f = 1 + amp * n + amp * .8 * big
    if fib:  # редкие волокна
        sp = rng.random((h, w)) > .9992
        fl = Image.fromarray((sp * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
        f = f - .06 * np.asarray(fl).astype(np.float32) / 255
    img = np.array(col, np.float32)[None, None] * f[..., None]
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")

def text(im, xy, s, size, f=IT, fill=G, anchor="mm", shadow=False):
    if shadow:
        L = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(L).text((xy[0] * S, xy[1] * S), s, font=font(f, size), fill=(8, 10, 4, 220), anchor=anchor)
        L = L.filter(ImageFilter.GaussianBlur(10 * S)); im.alpha_composite(L); im.alpha_composite(L)
    ImageDraw.Draw(im).text((xy[0] * S, xy[1] * S), s, font=font(f, size), fill=fill + (255,), anchor=anchor)

def handle(im, fill, pill=False, shadow=False):
    text(im, (W / 2, HANDLE_Y), "@WeTalk.Ru", 38, IT, fill, shadow=shadow)
    if pill:
        d = ImageDraw.Draw(im); tw = d.textlength("@WeTalk.Ru", font=font(IT, 38)) / S
        d.rounded_rectangle(((W / 2 - tw / 2 - 26) * S, (HANDLE_Y - 30) * S, (W / 2 + tw / 2 + 26) * S, (HANDLE_Y + 30) * S),
                            radius=30 * S, outline=fill + (255,), width=int(1.6 * S))

def shadow_of(rgba, off=(14, 26), blur=26, k=.45, col=(10, 10, 6)):
    a = rgba.split()[3].point(lambda v: int(v * k))
    sh = Image.new("RGBA", rgba.size, col + (0,)); sh.putalpha(a)
    return sh.filter(ImageFilter.GaussianBlur(blur * S)), (off[0] * S, off[1] * S)

def place(im, obj, x, y, sh=True, **kw):
    """obj — RGBA в масштабе S; x,y — левый верх в пикселях кадра"""
    if sh:
        s, (dx, dy) = shadow_of(obj, **kw); im.alpha_composite(s, (int(x * S) + dx, int(y * S) + dy))
    im.alpha_composite(obj, (int(x * S), int(y * S)))

def load(name, scale):
    o = Image.open(os.path.join(A, name)).convert("RGBA")
    return o.resize((int(o.width * scale * S), int(o.height * scale * S)), Image.LANCZOS)

def duotone(path, w, h):
    """фото в тёплый монохром бренда (тени DK -> света BE), обрезка cover"""
    p = ImageOps.fit(Image.open(path).convert("RGB"), (w * S, h * S), Image.LANCZOS, centering=(.5, .45))
    L = np.asarray(ImageOps.autocontrast(p.convert("L"), cutoff=1)).astype(np.float32) / 255
    L = L ** .9
    d, b = np.array(DK, np.float32), np.array([228, 224, 214], np.float32)
    out = d[None, None] * (1 - L[..., None]) + b[None, None] * L[..., None]
    g = rng.normal(0, 5, out.shape[:2])[..., None]
    return Image.fromarray((out + g).clip(0, 255).astype(np.uint8)).convert("RGBA")

def headline(im, lines, y0, step, fill, shadow=False):
    for i, (s, f, size) in enumerate(lines): text(im, (W / 2, y0 + i * step), s, size, f, fill, shadow=shadow)

def save(im, name):
    im.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, name + ".jpg"), quality=95); print(name)

# ---------- ассеты
lace_src = Image.open(os.path.join(A, "a_lace.png")).convert("L")
LACE_IN = (390, 467, 1217, 1550)                         # внутреннее окно рамки в исходнике
def lace(col, width):
    k = width / lace_src.width
    a = ImageOps.autocontrast(lace_src, cutoff=.5).point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 1.4)))
    a = a.resize((int(lace_src.width * k * S), int(lace_src.height * k * S)), Image.LANCZOS)
    tone = np.asarray(lace_src.resize(a.size, Image.LANCZOS)).astype(np.float32) / 255
    c = np.array(col, np.float32)[None, None] * (.82 + .18 * tone[..., None])
    im = Image.fromarray(c.clip(0, 255).astype(np.uint8)).convert("RGBA"); im.putalpha(a)
    return im, k

def framed(im, photo, col, width, cy):
    fr, k = lace(col, width)
    x0 = (W - width) / 2; y0 = cy - fr.height / S / 2
    ix0, iy0, ix1, iy1 = [v * k for v in LACE_IN]
    pw, ph = int(ix1 - ix0 + 24), int(iy1 - iy0 + 24)
    ph_im = duotone(os.path.join(A, photo), pw, ph)
    s, (dx, dy) = shadow_of(fr, blur=18, k=.5); im.alpha_composite(s, (int(x0 * S) + dx, int(y0 * S) + dy))
    im.alpha_composite(ph_im, (int((x0 + ix0 - 12) * S), int((y0 + iy0 - 12) * S)))
    im.alpha_composite(fr, (int(x0 * S), int(y0 * S)))
    im._win = (x0 + ix0, y0 + iy0, x0 + ix1, y0 + iy1)
    return x0, y0, fr.width / S, fr.height / S

def in_frame(im, lines, step=60):
    wx0, wy0, wx1, wy1 = im._win; cx, cy = (wx0 + wx1) / 2, (wy0 + wy1) / 2
    v = Image.new("RGBA", im.size, (14, 16, 10, 0)); m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rectangle((int(wx0 * S), int(wy0 * S), int(wx1 * S), int(wy1 * S)), fill=95)
    v.putalpha(m); im.alpha_composite(v)
    y0 = cy - step * (len(lines) - 1) / 2
    for i, (t, f, size) in enumerate(lines): text(im, (cx, y0 + i * step), t, size, f, BE, shadow=True)

def star(im, cx, cy, r, col, rot=0):
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = []
    for i in range(10):
        a = math.radians(rot - 90 + i * 36); rr = r if i % 2 == 0 else r * .45
        pts.append(((cx + rr * math.cos(a)) * S, (cy + rr * math.sin(a)) * S))
    d.polygon(pts, fill=col + (255,))
    s, (dx, dy) = shadow_of(L, off=(3, 5), blur=4, k=.5); im.alpha_composite(s, (dx, dy)); im.alpha_composite(L)

# письмо: чернила зелёные, бумага бежевая
_let = np.asarray(Image.open(os.path.join(A, "a_letter.png")).convert("L")).astype(np.float32)
_let = _let[60:-60, 60:-60]
_bgL = np.asarray(Image.fromarray(_let.astype(np.uint8)).filter(ImageFilter.MedianFilter(21))).astype(np.float32)
INK = np.clip((_bgL - _let - 18) / 60, 0, 1)
def letter_tex(w, h, zoom=1.0, ink_k=1.0, ink=G, base=BE):
    m = Image.fromarray((INK * 255).astype(np.uint8))
    m = m.resize((int(m.width * zoom), int(m.height * zoom)), Image.LANCZOS)
    m = ImageOps.fit(m, (w * S, h * S), Image.LANCZOS)
    mi = np.asarray(m).astype(np.float32)[..., None] / 255 * ink_k
    base_im = np.asarray(paper(base, .035).crop((0, 0, w * S, h * S)).convert("RGB")).astype(np.float32)
    out = base_im * (1 - mi) + np.array(ink, np.float32)[None, None] * mi
    return Image.fromarray(out.clip(0, 255).astype(np.uint8)).convert("RGBA")

_sil = Image.open(os.path.join(A, "a_silhouette.png")).convert("L")
SIL = _sil.point(lambda v: 255 if v < 110 else 0).crop(_sil.point(lambda v: 255 if v < 110 else 0).getbbox())
def silhouette(height, zoom=1.6, flip=False):
    k = height / SIL.height
    m = SIL.resize((int(SIL.width * k * S), int(height * S)), Image.LANCZOS)
    if flip: m = ImageOps.mirror(m)
    # лёгкая «вырезанная ножницами» кромка
    m = m.filter(ImageFilter.GaussianBlur(2 * S)).point(lambda v: 255 if v > 128 else 0)
    t = letter_tex(m.width // S + 1, m.height // S + 1, zoom)
    t = t.crop((0, 0, m.width, m.height)); t.putalpha(m)
    return t

# ---------- макеты
def L1():  # реф.1: зелёная кружевная перчатка с тиснёной карточкой
    im = paper(BE, .03); handle(im, G, pill=True)
    k = .8; o = load("a_glove_g.png", k); x0 = (W - o.width / S) / 2; y0 = H - o.height / S + 150
    place(im, o, x0, y0, off=(10, 20), blur=24, k=.35)
    ix0, iy0, ix1, iy1 = [x0 + 417 * k, y0 + 500 * k, x0 + 1183 * k, y0 + 900 * k]
    cy = (iy0 + iy1) / 2
    headline(im, [("Meet The New", REG, 54), ("Podcast", REG, 54), ("By Our Student", IT, 38)], cy - 70, 62, G)
    save(im, "01_perchatka_zelenaya")

def L2():  # реф.4: бежевая кружевная перчатка, карточка под наклоном
    im = paper(G, .04); handle(im, BE, pill=True)
    k = .78; o = load("a_glove_b.png", k); x0 = (W - o.width / S) / 2 + 20; y0 = H - o.height / S
    place(im, o, x0, y0, off=(12, 22), blur=26, k=.55)
    cx, cy, ang = x0 + 833 * k, y0 + 783 * k, -18
    L = Image.new("RGBA", (int(900 * S), int(420 * S)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i, (s, f, size) in enumerate([("Exchanging", REG, 54), ("Opinions", REG, 54), ("With Our Students", IT, 38)]):
        d.text((450 * S, (130 + i * 64) * S), s, font=font(f, size), fill=G + (255,), anchor="mm")
    L = L.rotate(-ang, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(L, (int(cx * S - L.width / 2), int(cy * S - L.height / 2)))
    save(im, "02_perchatka_bezhevaya")

def L3():  # реф.2: кружевной конверт с листком, светлые дуги на фоне
    im = paper(BE, .03)
    d = ImageDraw.Draw(im)
    lc = tuple(min(255, c + 14) for c in BE) + (255,)
    d.ellipse((-260 * S, 520 * S, 1500 * S, 1700 * S), outline=lc, width=int(16 * S))
    d.ellipse((380 * S, 300 * S, 2100 * S, 1500 * S), outline=lc, width=int(14 * S))
    im = im.filter(ImageFilter.GaussianBlur(1.2 * S)); handle(im, G)
    k = .7; o = load("a_envelope.png", k); x0 = (W - o.width / S) / 2; y0 = 1000 - (266 + 1641) / 2 * k
    place(im, o, x0, y0, off=(10, 22), blur=22, k=.4)
    cx = x0 + (487 + 1237) / 2 * k; cy = y0 + (418 + 1000) / 2 * k
    for i, (s, f, size) in enumerate([("Let’s Talk", REG, 52), ("With Our Student", IT, 34)]):
        text(im, (cx, cy - 26 + i * 56), s, size, f, G)
    save(im, "03_konvert")

def L4():  # реф.3: тиснёная овальная рамка на зелёной бумаге
    im = paper(G, .06); handle(im, BE)
    m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
    cx, cy, rx, ry = W / 2, 1000, 190, 380
    for dr, wdt in ((0, 5), (-20, 3)):
        d.ellipse(((cx - rx - dr) * S, (cy - ry - dr) * S, (cx + rx + dr) * S, (cy + ry + dr) * S), outline=255, width=int(wdt * S))
    for side in (-1, 1):  # веточки по бокам: лепестки веером от точки у овала
        bx = cx + side * (rx + 50)
        for ang, ln, wd in ((0, 62, 14), (-34, 50, 12), (34, 50, 12), (-62, 40, 10), (62, 40, 10)):
            a = math.radians(ang); ux, uy = side * math.cos(a), math.sin(a)
            mx, my = bx + ux * (ln / 2 + 14), cy + uy * (ln / 2 + 14)
            L = Image.new("L", (int(ln * S), int(wd * S)), 0); ImageDraw.Draw(L).ellipse((0, 0, L.width - 1, L.height - 1), fill=255)
            L = L.rotate(-math.degrees(math.atan2(uy, ux)), expand=True, resample=Image.BICUBIC)
            m.paste(255, (int(mx * S - L.width / 2), int(my * S - L.height / 2)), L)
    m = m.filter(ImageFilter.GaussianBlur(1.5 * S))
    M = np.asarray(m).astype(np.float32) / 255
    hi = np.roll(np.roll(M, -3 * S, 0), -3 * S, 1); lo = np.roll(np.roll(M, 3 * S, 0), 3 * S, 1)
    hi = np.asarray(Image.fromarray((hi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2 * S))).astype(np.float32) / 255
    lo = np.asarray(Image.fromarray((lo * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2 * S))).astype(np.float32) / 255
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    a = a * (1 - .45 * lo[..., None]) + (255 - a) * (.22 * hi[..., None]) - a * .08 * M[..., None]
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA"); handle(im, BE)
    headline(im, [("New", REG, 58), ("Recording", REG, 58), ("By Our Student", IT, 34)], cy - 70, 66, BE)
    save(im, "04_tisnenie_oval")

def L5():  # реф.5: силуэт из рукописи на однотонном фоне с «полом»
    im = paper(G, .04)
    floor = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(floor).rectangle((0, 1700 * S, W * S, H * S), fill=(0, 0, 0, 40))
    im.alpha_composite(floor.filter(ImageFilter.GaussianBlur(6 * S)))
    handle(im, BE)
    headline(im, [("Real Stories", REG, 60), ("By Our Students", IT, 40)], 440, 66, BE)
    s = silhouette(1180, 2.0); x = (W - s.width / S) / 2; y = 1760 - s.height / S
    place(im, s, x, y, off=(8, 12), blur=10, k=.45)
    save(im, "05_siluet")

def L_sil_photo(photo, lines, name, flip):  # реф.6/7: силуэт поверх фото
    im = ImageOps.fit(Image.open(os.path.join(A, photo)).convert("RGB"), (W * S, H * S), Image.LANCZOS).convert("RGBA")
    a = np.asarray(im.convert("RGB")).astype(np.float32) * .78                      # приглушаем фото
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    grad = np.linspace(1, 0, 900 * S)[:, None] ** 1.4 * 170
    gl = Image.new("RGBA", (W * S, 900 * S), (12, 14, 8, 0)); gl.putalpha(Image.fromarray(np.repeat(grad, W * S, 1).astype(np.uint8)))
    im.alpha_composite(gl)
    handle(im, BE, shadow=True)
    yy = np.arange(H * S)[:, None] / S
    band = (np.clip(1 - np.abs(yy - 960) / 260, 0, 1) ** 1.5 * 120).astype(np.uint8)
    bl = Image.new("RGBA", im.size, (12, 14, 8, 0)); bl.putalpha(Image.fromarray(np.repeat(band, W * S, 1))); im.alpha_composite(bl)
    headline(im, lines, 927, 66, BE, shadow=True)
    save(im, name)

def L_frame_paper(photo, l1, l2, name, stars):  # реф.8: зелёная бумага, бежевое кружево, звёзды, подпись справа внизу
    im = paper(G, .07); handle(im, BE)
    x0, y0, fw, fh = framed(im, photo, BE, 680, 950)
    for (sx, sy, r, rot) in stars: star(im, sx, sy, r, BE, rot)
    in_frame(im, [(t, REG, 48) for t in l1.split('|')] + [(t, IT, 32) for t in l2.split('|')], 56)
    save(im, name)

def L_frame_letter(photo, plaque, heart, name):  # реф.9: рукопись на фоне, оранжевое кружево, сердце и табличка
    im = letter_tex(W, H, 1.35, .38)
    clean = paper(BE, .035)                                   # чистая полоса бумаги под @WeTalk.Ru
    yy = np.arange(H * S)[:, None] / S
    a = np.clip(1 - np.abs(yy - HANDLE_Y) / 70, 0, 1) ** .6 * 255
    clean.putalpha(Image.fromarray(np.repeat(a, W * S, 1).astype(np.uint8))); im.alpha_composite(clean)
    handle(im, G)
    x0, y0, fw, fh = framed(im, photo, G, 720, 990)
    # сердце-наклейка (оранжевое по бежевому) слева сверху
    hL = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(hL)
    hx, hy, r = x0 + 20, y0 + 40, 70
    d.ellipse(((hx - r) * S, (hy - r * .6) * S, hx * S + 6, (hy + r * .55) * S), fill=G + (255,))
    d.ellipse((hx * S - 6, (hy - r * .6) * S, (hx + r) * S, (hy + r * .55) * S), fill=G + (255,))
    d.polygon([((hx - r * .97) * S, (hy + .05 * r) * S), ((hx + r * .97) * S, (hy + .05 * r) * S), (hx * S, (hy + r * 1.15) * S)], fill=G + (255,))
    hL = hL.rotate(12, center=(hx * S, hy * S), resample=Image.BICUBIC)
    s, (dx, dy) = shadow_of(hL, off=(4, 7), blur=6, k=.45); im.alpha_composite(s, (dx, dy)); im.alpha_composite(hL)
    text(im, (hx, hy + 6), heart, 30, IT, BE)
    # табличка справа снизу: зелёная с бежевой каймой
    pw, ph = 330, 110; wx0, wy0, wx1, wy1 = im._win; px, py = (wx0 + wx1) / 2 - pw / 2, (wy0 + wy1) / 2 - ph / 2
    pl = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
    d.rounded_rectangle((px * S, py * S, (px + pw) * S, (py + ph) * S), radius=14 * S, fill=BE + (255,))
    d.rounded_rectangle(((px + 10) * S, (py + 10) * S, (px + pw - 10) * S, (py + ph - 10) * S), radius=9 * S, outline=G + (255,), width=int(1.6 * S))
    s, (dx, dy) = shadow_of(pl, off=(6, 10), blur=10, k=.5); im.alpha_composite(s, (dx, dy)); im.alpha_composite(pl)
    text(im, (px + pw / 2, py + ph / 2), plaque, 40, IT, G)
    save(im, name)

def polka():
    im = paper(G, .09)
    d = ImageDraw.Draw(im); r = 72
    for j, y in enumerate(range(-60, H + 200, 330)):
        for x in range(-100 + (j % 2) * 230, W + 200, 460):
            d.ellipse(((x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S), fill=BE + (255,))
    # переплетение льна поверх горошка
    y, x = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
    t = 1 + .07 * np.sin(x * 2 * np.pi / 7) * np.sin(y * 2 * np.pi / 7) + rng.normal(0, .04, (H * S, W * S))
    a = np.asarray(im.convert("RGB")).astype(np.float32) * t[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def L_frame_polka(photo, words, name):  # реф.10: горошек, кружево, слова вокруг рамки, звёздочка
    im = polka()
    # подложка под @WeTalk.Ru не нужна: ставим текст бежевым с тенью
    handle(im, BE, shadow=True)
    x0, y0, fw, fh = framed(im, photo, BE, 620, 990)
    (w1, w2, w3) = words
    in_frame(im, [(w1, REG, 50), (w2, REG, 50), (w3, REG, 50)], 60)
    save(im, name)

if __name__ == "__main__":
    L1(); L2(); L3(); L4()
    L_sil_photo("photo1.jpg", [("A Day In English", REG, 60), ("With Our Student", IT, 40)], "06_foto_1", False)
    L_sil_photo("photo3.jpg", [("Coffee Talk", REG, 60), ("With Our Student", IT, 40)], "07_foto_2", True)
    L_frame_paper("photo4.jpg", "Speaking|Without Fear", "With Our Student", "08_ramka_bumaga_1",
                  [(255, 610, 34, 10), (445, 545, 30, -8), (848, 700, 32, 20), (240, 1100, 30, 0), (590, 1230, 32, 14), (830, 1370, 30, -12), (220, 1440, 34, 6)])
    L_frame_letter("photo5.jpg", "New Recording", "new", "09_ramka_pismo")
    L_frame_polka("photo2.jpg", ("What’s", "In My", "Bag?"), "10_ramka_goroshek_1")
    L_frame_paper("photo6.jpg", "Morning|Routine", "With Our Student", "11_ramka_bumaga_2",
                  [(260, 640, 32, -6), (820, 560, 30, 12), (870, 1000, 34, -14), (215, 1250, 30, 8), (610, 1400, 32, 0)])
    L_frame_polka("photo7.jpg", ("Meet", "The New", "Podcast"), "12_ramka_goroshek_2")
