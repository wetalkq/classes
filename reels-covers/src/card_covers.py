"""Обложки по рефам «игральная карта на шкуре» и «конверт из шерсти».
Шерсть — наша (тёмно-зелёная основа, узор #415038), карта/листок — бежевый #d2cec3, текст Times New Roman.
@WeTalk.Ru — первой строкой центрального блока; всё важное в видимой зоне сетки."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import ref_covers as R, ref_covers2 as R2
from ref_covers import W, H, S, G, BE, REG, IT, font, paper, shadow_of
from fur_brand import otsu, BASE

OUT = os.path.join(R.ROOT, "card_covers"); os.makedirs(OUT, exist_ok=True)
FUR = os.path.join(R.ROOT, "box", "fur")
SYM = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"     # только масти (в Times их нет)

def fur_bg(name):
    return Image.open(os.path.join(FUR, f"fon2_{name}.jpg")).convert("RGB").resize((W * S, H * S), Image.LANCZOS).convert("RGBA")

def suit(d, xy, ch, size, rot=False):
    from PIL import ImageFont
    f = ImageFont.truetype(SYM, int(size * S))
    d.text((xy[0] * S, xy[1] * S), ch, font=f, fill=G + (255,), anchor="mm")

def card(name, bg, photo, ch, lines):
    im = fur_bg(bg)
    cw, chh, cy = 740, 1040, 1090
    x0, y0 = (W - cw) / 2, cy - chh / 2
    C = Image.new("RGBA", (cw * S, chh * S), (0, 0, 0, 0))
    m = Image.new("L", C.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, C.width - 1, C.height - 1), radius=28 * S, fill=255)
    tex = paper(BE, .03).crop((0, 0, C.width, C.height)); C.paste(tex, (0, 0), m)
    # фото во внутренней рамке
    ix0, iy0, ix1, iy1 = 112, 120, cw - 112, chh - 120
    ph = R2.dark_photo(os.path.join(R.A, photo), ix1 - ix0, iy1 - iy0)
    C.alpha_composite(ph, (ix0 * S, iy0 * S))
    d = ImageDraw.Draw(C)
    d.rectangle((ix0 * S, iy0 * S, ix1 * S, iy1 * S), outline=G + (255,), width=int(2.5 * S))
    # индексы карты: «A» + масть, нижний — перевёрнут
    d.text((58 * S, 78 * S), "A", font=font(REG, 66), fill=G + (255,), anchor="mm")
    suit(d, (58, 140), ch, 50)
    corner = Image.new("RGBA", (120 * S, 200 * S), (0, 0, 0, 0)); dc = ImageDraw.Draw(corner)
    dc.text((60 * S, 50 * S), "A", font=font(REG, 66), fill=G + (255,), anchor="mm"); suit(dc, (60, 112), ch, 50)
    corner = corner.rotate(180)
    C.alpha_composite(corner, ((cw - 118) * S, (chh - 222) * S))
    s, (dx, dy) = shadow_of(C, off=(10, 22), blur=26, k=.55); im.alpha_composite(s, (int(x0 * S) + dx, int(y0 * S) + dy))
    im.alpha_composite(C, (int(x0 * S), int(y0 * S)))
    R2.block(im, W / 2, y0 + (iy0 + iy1) / 2, lines, (ix1 - ix0) * .8, BE, shadow=True)
    R2.save.__globals__["OUT"] = OUT; R2.save(im, name)

def envelope(name, lines):
    im = paper(BE, .03)
    e = np.asarray(Image.open(os.path.join(R.A, "a_env_fur.png")).convert("RGBA")).astype(np.float32)
    rgb, al = e[..., :3], e[..., 3]
    L = rgb.mean(-1); cardm = (al > 200) & (L > 170)
    fur = (al > 10) & ~cardm
    Lf = L / 255
    p5, pd, pl, p97 = np.percentile(Lf[fur], [3, 30, 75, 99.5])
    stops = np.array([[8, 9, 3], [16, 17, 5], BASE, G, [92, 108, 80], [110, 126, 96]], np.float32)
    col = np.stack([np.interp(Lf, [0, p5, pd, pl, p97, 1], stops[:, c]) for c in range(3)], -1)
    cardc = np.array(BE, np.float32)[None, None] * (L / np.median(L[cardm]))[..., None]
    out = np.where(cardm[..., None], cardc, np.where(fur[..., None], col, rgb))
    env = Image.fromarray(np.dstack([out.clip(0, 255), al]).astype(np.uint8), "RGBA")
    k = .8; env = env.resize((int(env.width * k * S), int(env.height * k * S)), Image.LANCZOS)
    x0 = (W - env.width / S) / 2; y0 = 1080 - (331 + 1302) / 2 * k
    s, (dx, dy) = shadow_of(env, off=(10, 24), blur=24, k=.45); im.alpha_composite(s, (int(x0 * S) + dx, int(y0 * S) + dy))
    im.alpha_composite(env, (int(x0 * S), int(y0 * S)))
    cx0, cx1, ctop, cbot = x0 + 328 * k, x0 + 1264 * k, y0 + 940 * k, y0 + 1160 * k
    R2.block(im, (cx0 + cx1) / 2, (ctop + cbot) / 2, lines, (cx1 - cx0) * .8, G, lead=.98)
    R2.save.__globals__["OUT"] = OUT; R2.save(im, name)

if __name__ == "__main__":
    envelope("01_konvert_lets_talk", [("Let’s Talk", REG, 90), ("With Our Student", IT, 48)])
    envelope("02_konvert_opinions", [("Exchanging", REG, 74), ("Opinions", REG, 74), ("With Our Students", IT, 44)])
    card("03_karta_bag", "lzebra", "photo2.jpg", "♠", [("What’s In", REG, 100), ("My Bag?", REG, 100)])
    card("04_karta_podcast", "lgiraffe", "photo7.jpg", "♣", [("Meet The", REG, 100), ("New Podcast", REG, 100), ("By Our Student", IT, 54)])
    card("05_karta_recording", "lleopard", "photo4.jpg", "♠", [("New", REG, 104), ("Recording", REG, 104), ("By Our Student", IT, 54)])
    card("06_karta_stories", "ltiger", "photo1.jpg", "♣", [("Real Stories", REG, 100), ("By Our Students", IT, 54)])
    fs = sorted(f for f in os.listdir(OUT) if f[0].isdigit())
    sh = Image.new("RGB", (280 * len(fs) - 10, 370 * 2), (255, 255, 255))
    for i, f in enumerate(fs):
        a = Image.open(os.path.join(OUT, f))
        sh.paste(a.crop((0, 240, W, 1680)).resize((270, 360)), (i * 280, 0))
        sh.paste(a.crop((44, 560, 1036, 1920)).resize((270, 360)), (i * 280, 370))
    sh.save(os.path.join(OUT, "setka_proverka.jpg"), quality=92)
