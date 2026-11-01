"""Финальные PNG 2160×3840 + макет ленты (посты из скриншотов + новые обложки)."""
import json, os, shutil
from PIL import Image
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
B, OUT = os.path.join(ROOT, "build"), os.path.join(ROOT, "covers_4K")
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
items = json.load(open(os.path.join(B, "items.json")))
for it in items:
    shutil.copy(os.path.join(B, it["name"] + ".png"), os.path.join(OUT, it["name"] + ".png"))

UP = "/root/.claude/uploads/241421bf-6941-55f1-ad6e-5867ad3cca13/"
shots = ['0d9eee8d','17a4169c','3405ac2f','1c6572ce','9447c025','5ef5a43b','2ea143f8','9364e765']
row_y = {'0d9eee8d':110,'17a4169c':111,'3405ac2f':113,'1c6572ce':116,'9447c025':116,'5ef5a43b':115,'2ea143f8':115,'9364e765':156}
cols = [(0,275),(277,552),(554,828)]
TW, TH, G = 360, 480, 4
reels = {(it["r"], it["c"]): it for it in items}
for part, (r0, r1) in enumerate([(0, 16), (16, 32)], 1):
    M = Image.new("RGB", (3*TW+2*G, (r1-r0)*(TH+G)-G), "white")
    for r in range(r0, r1):
        s = shots[r//4]; y = row_y[s] + 368*(r % 4)
        for c in range(3):
            if (r, c) in reels:
                im = Image.open(os.path.join(OUT, reels[(r, c)]["name"] + ".png")).crop((0, 480, 2160, 3360))
            elif r == 31 and c > 0:
                continue
            else:
                x0, x1 = cols[c]
                im = Image.open(UP + s + "-image.jpg").crop((x0, y, x1, y+366))
            M.paste(im.convert("RGB").resize((TW, TH), Image.LANCZOS), (c*(TW+G), (r-r0)*(TH+G)))
    M.save(os.path.join(ROOT, f"feed_mockup_{part}.jpg"), quality=88)
print("ok", len(os.listdir(OUT)))
