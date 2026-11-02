"""Трендовый Reels: «Попроси свой AI наполнить поднос». 1080×1920, 30 fps, ~12 c, без звука."""
import os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
A = os.path.join(ROOT, "tray", "a"); OUT = os.path.join(ROOT, "tray"); FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
F = os.path.join(ROOT, "fonts")
W, H, FPS = 1080, 1920, 30
G, O = (65, 80, 56), (218, 82, 0)

def font(n, s): return ImageFont.truetype(os.path.join(F, n), s)
REG, IT, BOLD = "timesnrcyrmt.ttf", "timesnrcyrmt_inclined.ttf", "timesnrcyrmt_bold.ttf"

BG = Image.open(os.path.join(A, "bg.png")).convert("RGB").resize((W, H), Image.LANCZOS)

# предмет: файл, ширина, центр, поворот (порядок появления)
ITEMS = [("book", 250, (420, 880), -9), ("notebook", 205, (650, 990), 11), ("candle", 230, (365, 1075), 0),
         ("bag", 255, (620, 830), 5), ("pearls", 320, (500, 1010), -6), ("phones", 240, (735, 1090), -14),
         ("cup", 195, (300, 870), 0), ("perfume", 165, (790, 860), 18), ("figs", 175, (540, 1160), 8)]

def prep(name, w, rot):
    im = Image.open(os.path.join(A, name + ".png")).convert("RGBA")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).rotate(rot, expand=True, resample=Image.BICUBIC)
    a = im.split()[3]
    sh = Image.new("RGBA", im.size, (40, 25, 15, 0)); sh.putalpha(a.point(lambda v: int(v * .38)))
    pad = 40
    shc = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); shc.paste(sh, (pad, pad))
    return im, shc.filter(ImageFilter.GaussianBlur(14))
OBJ = [(prep(n, w, r), c) for n, w, c, r in ITEMS]

def text_layer(lines, alpha):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for t, f, s, col, y in lines:
        d.text((W // 2, y), t, font=font(f, s), fill=col + (int(255 * alpha),), anchor="mm")
    return L

TOP = [("@WeTalk.Ru", IT, 46, O, 150), ("Попроси Свой AI", REG, 84, G, 255),
       ("наполнить этот поднос тем,", IT, 50, G, 345), ("что напоминает ему о тебе", IT, 50, G, 405)]
PROMPT = [("«Наполни поднос вещами,", IT, 44, G, 1500), ("которые ассоциируются у тебя со мной,", IT, 44, G, 1560),
          ("и объясни выбор одной строкой»", IT, 44, G, 1620)]
END = [("А что на твоём подносе?", REG, 70, G, 1520), ("Пиши в комментариях", IT, 50, G, 1610)]

def ease_out(t): return 1 - (1 - t) ** 3
def clamp(x): return max(0.0, min(1.0, x))

T_IN, STEP, DROP = 1.6, 0.55, 0.45
T_FULL = T_IN + STEP * len(OBJ) + 1.3
T_OUT_STEP = 0.18
T_EMPTY = T_FULL + T_OUT_STEP * len(OBJ) + 0.35
DUR = T_EMPTY + 2.4

def frame(t):
    im = BG.copy().convert("RGBA")
    im.alpha_composite(text_layer(TOP, clamp(t / 0.8)))
    for i, ((obj, sh), (cx, cy)) in enumerate(OBJ):
        t0 = T_IN + i * STEP
        t1 = T_FULL + (len(OBJ) - 1 - i) * T_OUT_STEP
        if t < t0: continue
        if t < t0 + DROP:
            p = ease_out((t - t0) / DROP); sc = 1.25 - .25 * p; a = p; dy = -60 * (1 - p); shs = .4 + .6 * p
        elif t < t1: sc, a, dy, shs = 1, 1, 0, 1
        elif t < t1 + .3:
            p = (t - t1) / .3; sc = 1 - .15 * p; a = 1 - p; dy = 0; shs = 1 - p
        else: continue
        o = obj.resize((max(1, int(obj.width * sc)), max(1, int(obj.height * sc))), Image.LANCZOS)
        s = sh.resize((max(1, int(sh.width * sc)), max(1, int(sh.height * sc))), Image.LANCZOS)
        if a < 1:
            o.putalpha(o.split()[3].point(lambda v, a=a: int(v * a)))
        s.putalpha(s.split()[3].point(lambda v, k=a * shs: int(v * k)))
        lift = (1 - shs) * 30
        im.alpha_composite(s, (int(cx - s.width / 2 + 10 + lift), int(cy - s.height / 2 + 16 + lift)))
        im.alpha_composite(o, (int(cx - o.width / 2), int(cy - o.height / 2 + dy)))
    pa = clamp((t - T_IN + .3) / .6) * (1 - clamp((t - T_FULL) / .5))
    if pa > 0: im.alpha_composite(text_layer(PROMPT, pa))
    ea = clamp((t - T_EMPTY) / .7)
    if ea > 0: im.alpha_composite(text_layer(END, ea))
    return im.convert("RGB")

if __name__ == "__main__":
    n = int(DUR * FPS)
    for k in range(n):
        frame(k / FPS).save(os.path.join(FR, f"{k:04d}.png"))
    out = os.path.join(OUT, "WeTalk_podnos_reels.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FR, "%04d.png"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    print(out, n, round(DUR, 1))
