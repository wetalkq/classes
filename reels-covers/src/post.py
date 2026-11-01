"""Зерно бумаги + финальные файлы + макет ленты."""
import json, os, numpy as np
from PIL import Image
B = os.path.join(os.path.dirname(__file__), "..", "build")
OUT = os.path.join(os.path.dirname(__file__), "..", "covers_4K")
os.makedirs(OUT, exist_ok=True)
items = json.load(open(os.path.join(B, "items.json")))
rng = np.random.default_rng(7)
for it in items:
    a = np.asarray(Image.open(os.path.join(B, it["name"] + ".png")).convert("RGB")).astype(np.float32)
    n = rng.normal(0, 4.5, a.shape[:2])[..., None]
    Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8)).save(os.path.join(OUT, it["name"] + ".png"), optimize=True)

# макет ленты: тайлы постов из скриншотов + новые обложки (центр 3:4)
UP = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13/"
shots = ['0d9eee8d','17a4169c','3405ac2f','1c6572ce','9447c025','5ef5a43b','2ea143f8','9364e765']
row_y = {s: [110,478,846,1214] for s in shots}
row_y['3405ac2f']=[112,480,848,1216]; row_y['0d9eee8d']=[110,478,846,1214]
for s in ['1c6572ce','9447c025']: row_y[s]=[115,483,851,1219]
for s in ['5ef5a43b','2ea143f8']: row_y[s]=[114,482,850,1218]
row_y['9364e765']=[155,523,891,1259]
cols = [(0,275),(277,552),(554,828)]
TW, TH, G = 360, 480, 4
reels = {(it["r"], it["c"]): it for it in items}
rows = 32
for part, (r0, r1) in enumerate([(0, 16), (16, 32)], 1):
    M = Image.new("RGB", (3*TW+2*G, (r1-r0)*(TH+G)-G), "white")
    for r in range(r0, r1):
        s = shots[r//4]; y = row_y[s][r % 4]
        for c in range(3):
            if (r, c) in reels:
                im = Image.open(os.path.join(OUT, reels[(r, c)]["name"] + ".png"))
                im = im.crop((0, 480, 2160, 3360))
            else:
                if r == 31 and c > 0: continue
                x0, x1 = cols[c]
                im = Image.open(UP + s + "-image.jpg").crop((x0, y, x1, y+366))
            M.paste(im.resize((TW, TH), Image.LANCZOS), (c*(TW+G), (r-r0)*(TH+G)))
    M.save(os.path.join(os.path.dirname(__file__), "..", f"feed_mockup_part{part}.jpg"), quality=90)
print("ok")
