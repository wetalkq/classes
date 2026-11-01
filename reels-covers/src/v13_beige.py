"""v13 — по одной обложке в каждом ряду ленты: просто бежевый фон, весь текст той же обложки — зелёным, по центру.
Пишет обе версии: 3:4 (v13/) и 9:16 (v13_916/). Имена файлов — как в v12."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11_mockups as V
import v12_all as A
from v11_mockups import T, box, G, B, AT

O34 = os.path.join(V.ROOT, "v13"); O916 = os.path.join(V.ROOT, "v13_916")
for d in (O34, O916): os.makedirs(d, exist_ok=True)


def body(t, meta, quote):
    t1, t2 = t
    return box(90, 0, 900, 1440, [
        T(AT, 58, G, it=True),
        f'<div style="--fs:40px;height:40px"></div>',
        T(t1, 120, G), T(t2, 104, G) if t2 else "",
        f'<div style="--fs:20px;height:20px"></div>',
        T(meta, 48, G, ls=2),
        T(f"«{quote}»", 54, G, it=True, extra="white-space:nowrap"),
    ], gap=26)


def doc(inner, h):
    css = V.CSS.replace("height:1440px;", f"height:{h}px;")
    top = (h - 1440) // 2
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body style='background:{B}'>"
            f"<div style='position:absolute;left:0;top:{top}px;width:1080px;height:1440px'>{inner}</div>{V.FIT}</body></html>")


if __name__ == "__main__":
    rows = {}
    for i, d in enumerate(A.REELS): rows.setdefault(d["r"], []).append((i, d))
    picked, prev = [], None
    for r in sorted(rows):
        cand = rows[r]
        order = sorted(cand, key=lambda x: (x[1]["c"] == prev, x[1]["c"] != 1))
        i, d = order[0]; prev = d["c"]
        t, meta = A.info_of(d)
        name = f"{i+1:02d}_ряд{d['r']+1:02d}-{d['c']+1}_{d['kind']}" + (f"-{d['num']:02d}" if d.get("num") else "")
        inner = body(t, meta, A.QUOTES[i % len(A.QUOTES)])
        open(os.path.join(O34, name + ".html"), "w").write(doc(inner, 1440))
        open(os.path.join(O916, name + ".html"), "w").write(doc(inner, 1920))
        picked.append(name)
    json.dump(picked, open(os.path.join(O34, "picked.json"), "w"), ensure_ascii=False)
    print(len(picked))
