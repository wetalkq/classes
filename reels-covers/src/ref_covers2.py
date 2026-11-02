"""v2 по 5 референсам: крупный текст строго по центру объекта (читается в сетке 3:4),
плотный интерлиньяж, без лишних подложек, без звёзд/сердечек. Цвета строго бренд, Times New Roman."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import ref_covers as R
from ref_covers import W, H, S, G, BE, DK, REG, IT, font, paper, load, place, shadow_of, lace, LACE_IN, letter_tex, polka

OUT = os.path.join(R.ROOT, "ref_covers2"); os.makedirs(OUT, exist_ok=True)
HY = 335                                    # @WeTalk.Ru — внутри 3:4 (y 240–1680)

def handle(im, fill, pill=False, shadow=False):
    R.text(im, (W / 2, HY), "@WeTalk.Ru", 46, IT, fill, shadow=shadow)
    if pill:
        d = ImageDraw.Draw(im); tw = d.textlength("@WeTalk.Ru", font=font(IT, 46)) / S
        d.rounded_rectangle(((W / 2 - tw / 2 - 30) * S, (HY - 36) * S, (W / 2 + tw / 2 + 30) * S, (HY + 36) * S),
                            radius=36 * S, outline=fill + (255,), width=int(2 * S))

def fit(t, f, size, maxw):
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    while size > 30 and d.textlength(t, font=font(f, size)) / S > maxw: size -= 2
    return size

def block(im, cx, cy, lines, maxw, fill, shadow=False, lead=1.02):
    """lines: [(text, font, size)] — размеры подгоняются под ширину, интерлиньяж плотный"""
    ls = [(t, f, fit(t, f, s, maxw)) for t, f, s in lines]
    hs = [s * lead for _, _, s in ls]; tot = sum(hs)
    y = cy - tot / 2
    for (t, f, s), h in zip(ls, hs):
        R.text(im, (cx, y + h / 2), t, s, f, fill, shadow=shadow); y += h

def save(im, name):
    im.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, name + ".jpg"), quality=95); print(name)

def dark_photo(path, w, h):
    """монохром бренда, приглушённые света — чтобы бежевый текст читался без подложки"""
    p = ImageOps.fit(Image.open(path).convert("RGB"), (int(w * S), int(h * S)), Image.LANCZOS, centering=(.5, .45))
    L = np.asarray(ImageOps.autocontrast(p.convert("L"), cutoff=1)).astype(np.float32) / 255
    d, b = np.array(DK, np.float32), np.array([150, 150, 136], np.float32)
    out = d[None, None] * (1 - L[..., None]) + b[None, None] * L[..., None]
    out += R.rng.normal(0, 4, out.shape[:2])[..., None]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8)).convert("RGBA")

def frame_photo(im, photo, col, width, cy):
    fr, k = lace(col, width)
    x0 = (W - width) / 2; y0 = cy - fr.height / S / 2
    ix0, iy0, ix1, iy1 = [v * k for v in LACE_IN]
    ph = dark_photo(os.path.join(R.A, photo), ix1 - ix0 + 24, iy1 - iy0 + 24)
    s, (dx, dy) = shadow_of(fr, blur=18, k=.5); im.alpha_composite(s, (int(x0 * S) + dx, int(y0 * S) + dy))
    im.alpha_composite(ph, (int((x0 + ix0 - 12) * S), int((y0 + iy0 - 12) * S)))
    im.alpha_composite(fr, (int(x0 * S), int(y0 * S)))
    return (x0 + ix0, y0 + iy0, x0 + ix1, y0 + iy1), (x0, y0, fr.width / S, fr.height / S)

# --- реф. «перчатка с карточкой»
def glove(lines, name):
    im = paper(BE, .03); handle(im, G, pill=True)
    k = .86; o = load("a_glove_g.png", k); x0 = (W - o.width / S) / 2; y0 = 1340 - 900 * k
    place(im, o, x0, y0, off=(10, 20), blur=24, k=.35)
    cx0, cy0, cx1, cy1 = x0 + 417 * k, y0 + 505 * k, x0 + 1183 * k, y0 + 895 * k
    block(im, (cx0 + cx1) / 2, (cy0 + cy1) / 2, lines, (cx1 - cx0) * .9, G)
    save(im, name)

# --- реф. «тиснёный овал»
def oval(lines, name):
    im = paper(G, .06)
    m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
    cx, cy, rx, ry = W / 2, 960, 300, 520
    for dr, wdt in ((0, 6), (-24, 3)):
        d.ellipse(((cx - rx - dr) * S, (cy - ry - dr) * S, (cx + rx + dr) * S, (cy + ry + dr) * S), outline=255, width=int(wdt * S))
    for side in (-1, 1):
        bx = cx + side * (rx + 56)
        for ang, ln, wd in ((0, 70, 15), (-34, 56, 13), (34, 56, 13), (-62, 44, 11), (62, 44, 11)):
            a = math.radians(ang); ux, uy = side * math.cos(a), math.sin(a)
            mx, my = bx + ux * (ln / 2 + 14), cy + uy * (ln / 2 + 14)
            L = Image.new("L", (int(ln * S), int(wd * S)), 0); ImageDraw.Draw(L).ellipse((0, 0, L.width - 1, L.height - 1), fill=255)
            L = L.rotate(-math.degrees(math.atan2(uy, ux)), expand=True, resample=Image.BICUBIC)
            m.paste(255, (int(mx * S - L.width / 2), int(my * S - L.height / 2)), L)
    m = m.filter(ImageFilter.GaussianBlur(1.5 * S)); M = np.asarray(m).astype(np.float32) / 255
    blur = lambda x: np.asarray(Image.fromarray((x * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2 * S))).astype(np.float32) / 255
    hi = blur(np.roll(np.roll(M, -3 * S, 0), -3 * S, 1)); lo = blur(np.roll(np.roll(M, 3 * S, 0), 3 * S, 1))
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    a = a * (1 - .45 * lo[..., None]) + (255 - a) * (.22 * hi[..., None]) - a * .08 * M[..., None]
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    handle(im, BE)
    block(im, cx, cy, lines, rx * 2 * .82, BE)
    save(im, name)

# --- реф. «кружевная рамка на бумаге»
def frame_paper(photo, lines, name):
    im = paper(G, .07); handle(im, BE)
    (wx0, wy0, wx1, wy1), _ = frame_photo(im, photo, BE, 920, 1015)
    block(im, (wx0 + wx1) / 2, (wy0 + wy1) / 2, lines, (wx1 - wx0) * .96, BE, shadow=True)
    save(im, name)

# --- реф. «горошек»
def frame_polka(photo, lines, name):
    im = polka(); handle(im, BE, shadow=True)
    (wx0, wy0, wx1, wy1), _ = frame_photo(im, photo, BE, 880, 1015)
    block(im, (wx0 + wx1) / 2, (wy0 + wy1) / 2, lines, (wx1 - wx0) * .96, BE, shadow=True)
    save(im, name)

# --- реф. «рукопись + кружево + табличка»
def frame_letter(photo, lines, plaque, name):
    im = letter_tex(W, H, 1.35, .38)
    clean = paper(BE, .035); yy = np.arange(H * S)[:, None] / S
    a = np.clip(1 - np.abs(yy - HY) / 80, 0, 1) ** .6 * 255
    clean.putalpha(Image.fromarray(np.repeat(a, W * S, 1).astype(np.uint8))); im.alpha_composite(clean)
    handle(im, G)
    (wx0, wy0, wx1, wy1), (x0, y0, fw, fh) = frame_photo(im, photo, G, 900, 1005)
    block(im, (wx0 + wx1) / 2, (wy0 + wy1) / 2, lines, (wx1 - wx0) * .96, BE, shadow=True)
    # табличка как на референсе: справа снизу на кромке рамки
    pw, ph = 380, 112; px, py = x0 + fw - pw + 10, y0 + fh - ph + 30
    pl = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
    d.rounded_rectangle((px * S, py * S, (px + pw) * S, (py + ph) * S), radius=12 * S, fill=BE + (255,))
    d.rounded_rectangle(((px + 9) * S, (py + 9) * S, (px + pw - 9) * S, (py + ph - 9) * S), radius=8 * S, outline=G + (255,), width=int(2 * S))
    s, (dx, dy) = shadow_of(pl, off=(6, 10), blur=10, k=.5); im.alpha_composite(s, (dx, dy)); im.alpha_composite(pl)
    R.text(im, (px + pw / 2, py + ph / 2), plaque, fit(plaque, IT, 48, pw - 50), IT, G)
    save(im, name)

if __name__ == "__main__":
    for f in os.listdir(OUT):
        if f.endswith(".jpg"): os.remove(os.path.join(OUT, f))
    glove([("Meet The New", REG, 84), ("Podcast", REG, 84), ("By Our Student", IT, 54)], "01_perchatka")
    oval([("New", REG, 104), ("Recording", REG, 104), ("By Our Student", IT, 60)], "02_oval")
    frame_paper("photo4.jpg", [("Let’s Talk", REG, 112), ("With Our Student", IT, 60)], "03_ramka_lets_talk")
    frame_polka("photo2.jpg", [("What’s In", REG, 112), ("My Bag?", REG, 112)], "04_goroshek_bag")
    frame_letter("photo5.jpg", [("Exchanging", REG, 104), ("Opinions", REG, 104), ("With Our Students", IT, 56)], "with love", "05_pismo_opinions")
    frame_paper("photo6.jpg", [("New", REG, 112), ("Recording", REG, 112), ("By Our Student", IT, 60)], "06_ramka_recording")
    frame_polka("photo7.jpg", [("Meet The New", REG, 104), ("Podcast", REG, 104), ("By Our Student", IT, 56)], "07_goroshek_podcast")
    frame_letter("photo3.jpg", [("Coffee Talk", REG, 112), ("With Our Student", IT, 60)], "new episode", "08_pismo_coffee")
    frame_paper("photo1.jpg", [("Real Stories", REG, 108), ("By Our Students", IT, 60)], "09_ramka_stories")
    im = Image.new("RGB", (280 * 5 - 10, 370 * 2), (255, 255, 255))
    fs = sorted(f for f in os.listdir(OUT) if f[0].isdigit())
    for i, f in enumerate(fs):
        t = Image.open(os.path.join(OUT, f)).crop((0, 240, W, 1680)).resize((270, 360), Image.LANCZOS)
        im.paste(t, ((i % 5) * 280, (i // 5) * 370))
    im.save(os.path.join(OUT, "setka_3x4_proverka.jpg"), quality=92)
