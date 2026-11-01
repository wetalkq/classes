"""9:16 версии всех 60 обложек: дизайн 3:4 по центру (y 240–1680 — то, что видно в сетке),
фото на весь кадр дотягивается до 1920, однотонный фон продолжается."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11_mockups as V
import v12_all as A

OUT = os.path.join(V.ROOT, "v12_916"); os.makedirs(OUT, exist_ok=True)
_img = V.img

def img916(pid, x, y, w, h, fy=.45, cls="", r=0):
    if y == 0 and h == 1440: y, h = -240, 1920
    elif y == 0 and x == 0 and w == 1080: y, h = -240, h + 240
    return _img(pid, x, y, w, h, fy, cls, r)

def page916(body, bg=V.B):
    css = V.CSS.replace("html,body{width:1080px;height:1440px;", "html,body{width:1080px;height:1920px;")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body style='background:{bg}'>"
            f"<div style='position:absolute;left:0;top:240px;width:1080px;height:1440px'>{body}</div>{V.FIT}</body></html>")

A.img, A.page = img916, page916

if __name__ == "__main__":
    A._pi = 0
    items = []
    for i, d in enumerate(A.REELS):
        t, meta = A.info_of(d)
        n = i % 16 + 1
        name = f"{i+1:02d}_ряд{d['r']+1:02d}-{d['c']+1}_{d['kind']}" + (f"-{d['num']:02d}" if d.get("num") else "")
        open(os.path.join(OUT, name + ".html"), "w").write(A.lay(n, t, meta, A.QUOTES[i % len(A.QUOTES)]))
        items.append(name)
    print(len(items))
