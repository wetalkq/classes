"""Reels «Спроси свой AI, как он тебя видит»: ракушка, печатающийся промпт. 1080×1920, 30 fps, без звука."""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
S = os.path.join(ROOT, "box"); FR = os.path.join(S, "frames"); os.makedirs(FR, exist_ok=True)
F = os.path.join(ROOT, "fonts")
W, H, FPS = 1080, 1920, 30
G, O, K = (65, 80, 56), (218, 82, 0), (40, 40, 38)
REG, IT = "timesnrcyrmt.ttf", "timesnrcyrmt_inclined.ttf"
def font(n, s): return ImageFont.truetype(os.path.join(F, n), s)

# фон: бежевый с бумажной фактурой
paper = Image.open(os.path.join(ROOT, "v5", "paper.jpg")).convert("L").resize((W, H))
pn = (np.asarray(paper).astype(np.float32) / 255 - .93) * .6
BG = Image.fromarray(np.clip(np.array([210, 206, 195], np.float32)[None, None] * (1 + pn[..., None]), 0, 255).astype(np.uint8))

shell = Image.open(os.path.join(S, "box_cut.png")).convert("RGBA")
shell = shell.crop(shell.getbbox())
SW = 600; shell = shell.resize((SW, round(shell.height * SW / shell.width)), Image.LANCZOS)
al = shell.split()[3]
shad = Image.new("RGBA", (shell.width + 120, shell.height + 120), (0, 0, 0, 0))
sh = Image.new("RGBA", shell.size, (30, 22, 15, 0)); sh.putalpha(al.point(lambda v: int(v * .45)))
shad.paste(sh, (60, 60)); shad = shad.filter(ImageFilter.GaussianBlur(26))
SCX, SCY = W // 2, 960

TOP = [("@WeTalk.Ru", IT, 38, O, 355), ("Спроси Свой AI", IT, 66, G, 427), ("чем бы он заполнил эту коробку", IT, 40, G, 490)]
PROMPT = ["Промпт ждёт тебя", "в описании"]
P_Y, P_STEP, P_SIZE = 1420, 58, 46
END = [("А какая ты в его глазах?", REG, 52, G, 1392), ("Пиши в комментариях", IT, 36, G, 1452)]

def clamp(x): return max(0.0, min(1.0, x))
T_TYPE0, CPS = 1.9, 26
NCH = sum(len(l) for l in PROMPT)
T_TYPE1 = T_TYPE0 + NCH / CPS
T_POUT, T_END, DUR = 99, 99, 8.0

def txt(layer, items, a):
    d = ImageDraw.Draw(layer)
    for t, f, s, col, y in items: d.text((W // 2, y), t, font=font(f, s), fill=col + (int(255 * a),), anchor="mm")

def frame(t):
    im = BG.copy().convert("RGBA")
    a = clamp(t / 1.0); z = 1 + .02 * (t / DUR)
    s = shell.resize((int(shell.width * z), int(shell.height * z)), Image.LANCZOS)
    sd = shad.resize((int(shad.width * z), int(shad.height * z)), Image.LANCZOS)
    if a < 1:
        s.putalpha(s.split()[3].point(lambda v: int(v * a))); sd.putalpha(sd.split()[3].point(lambda v: int(v * a)))
    im.alpha_composite(sd, (SCX - sd.width // 2 + 14, SCY - sd.height // 2 + 30))
    im.alpha_composite(s, (SCX - s.width // 2, SCY - s.height // 2))
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    txt(L, TOP, clamp((t - .5) / .9))
    if t >= T_TYPE0:
        pa = 1.0
        if pa > 0:
            n = int((t - T_TYPE0) * CPS); d = ImageDraw.Draw(L); f = font(IT, P_SIZE); shown = []
            for line in PROMPT:
                k = max(0, min(len(line), n)); shown.append(line[:k]); n -= len(line)
            last = max(i for i, x in enumerate(shown + [""]) if i < len(shown) and (x or i == 0))
            for i, line in enumerate(shown):
                full_w = d.textlength(PROMPT[i], font=f)
                x = W / 2 - full_w / 2; y = P_Y + i * P_STEP
                d.text((x, y), line, font=f, fill=G + (int(255 * pa),), anchor="lm")
                if i == last and t < T_TYPE1 + .9 and int(t * 2.4) % 2 == 0:
                    cx = x + d.textlength(line, font=f) + 4
                    d.line([(cx, y - 20), (cx, y + 18)], fill=G + (int(200 * pa),), width=2)
    pass
    im.alpha_composite(L)
    return im.convert("RGB")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for t in map(float, sys.argv[1:]): frame(t).save(os.path.join(S, f"pv_{t:.1f}.jpg"), quality=90)
        print(DUR); raise SystemExit
    n = int(DUR * FPS)
    for k in range(n): frame(k / FPS).save(os.path.join(FR, f"{k:04d}.png"))
    out = os.path.join(S, "WeTalk_korobka_reels_v2.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FR, "%04d.png"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    print(out, n, round(DUR, 1))
