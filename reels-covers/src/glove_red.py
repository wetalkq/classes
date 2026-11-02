"""Рука в тёмно-красной кружевной перчатке с карточкой — несколько надписей."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ref_covers2 as R2
from ref_covers import W, S, G, BE, REG, IT, paper, load, place
OUT = os.path.join(R2.R.ROOT, "glove_red"); os.makedirs(OUT, exist_ok=True)

def make(lines, name, bg=BE):
    im = paper(bg, .03)
    k = .86; o = load("a_glove_red.png", k); x0 = (W - o.width / S) / 2; y0 = 1290 - 900 * k
    place(im, o, x0, y0, off=(10, 20), blur=24, k=.35)
    cx0, cy0, cx1, cy1 = x0 + 417 * k, y0 + 505 * k, x0 + 1183 * k, y0 + 895 * k
    R2.block(im, (cx0 + cx1) / 2, (cy0 + cy1) / 2, lines, (cx1 - cx0) * .8, G)
    R2.save.__globals__["OUT"] = OUT; R2.save(im, name)

make([("Podcast", REG, 90), ("By Our Students", IT, 54)], "01_podcast_by_our_students")
make([("Meet The New", REG, 84), ("Podcast", REG, 84), ("By Our Student", IT, 52)], "02_meet_new_podcast")
make([("Let’s Talk", REG, 90), ("With Our Student", IT, 52)], "03_lets_talk")
make([("New", REG, 88), ("Recording", REG, 88), ("By Our Student", IT, 52)], "04_new_recording")
make([("Podcast", REG, 90), ("By Our Students", IT, 54)], "05_podcast_zelenyi_fon", bg=G)
