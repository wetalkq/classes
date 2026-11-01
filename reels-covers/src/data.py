# Reels в ленте @wetalk.ru (сверху вниз), координаты: (row, col) в сетке профиля.
# kind: podcast | bag | special
REELS = [
    # --- скрин 1 (ряды 0–3)
    dict(r=0, c=0, kind="podcast", top="by our student", level="A1-A2 Level"),
    dict(r=0, c=1, kind="podcast", num=2, place="Belarus", level="0-A1 Level"),
    dict(r=0, c=2, kind="podcast", top="by our student", level="A1-A2 Level"),
    dict(r=1, c=1, kind="podcast", top="by our student", place="Edinburgh"),
    dict(r=2, c=2, kind="bag", level="A1-A2 Level"),
    dict(r=3, c=0, kind="podcast", top="by our student", place="Interstellar"),
    # --- скрин 2 (ряды 4–7)
    dict(r=4, c=0, kind="podcast", top="by our student", level="B1 Level"),
    dict(r=4, c=1, kind="bag", num=40),
    dict(r=4, c=2, kind="podcast", top="by our student", level="B1 Level"),
    dict(r=5, c=1, kind="podcast", top="by our student"),
    dict(r=5, c=2, kind="podcast", top="by our student", level="B1 Level"),
    dict(r=6, c=2, kind="podcast", top="by our student"),
    # --- скрин 3 (ряды 8–11)
    dict(r=8, c=0, kind="special", title=["Meet our", "student"], quote="w/ her new podcast"),
    dict(r=8, c=1, kind="podcast", top="by our student", level="0-A1 Level"),
    dict(r=8, c=2, kind="podcast", top="by our student", level="A1 Level"),
    dict(r=10, c=0, kind="special", title=["Отзывы", "& результаты"], quote="наших учениц", maybe=True),
    dict(r=10, c=1, kind="podcast", num=13, place="Jiddah", level="0-A1 Level"),
    dict(r=11, c=0, kind="podcast", num=30, place="Moscow", level="B1-B2 Level"),
    dict(r=11, c=1, kind="podcast", num=25, place="Russia", level="B1-B2 Level"),
    # --- скрин 4 (ряды 12–15)
    dict(r=12, c=0, kind="podcast", num=1, place="Ingushetia", level="0-A1 Level"),
    dict(r=13, c=0, kind="podcast", num=23, place="Russia", level="A2-B1 Level"),
    dict(r=14, c=0, kind="podcast", num=37, top="by our student", level="A2-B1 Level"),
    dict(r=14, c=1, kind="podcast", num=24, place="Russia", level="A1-A2 Level"),
    dict(r=15, c=0, kind="podcast", num=38, top="by our student", level="0-A1 Level"),
    dict(r=15, c=2, kind="podcast", num=6, place="Belarus", level="0-A1 Level"),
    # --- скрин 5 (ряды 16–19)
    dict(r=17, c=0, kind="bag", num=43),
    dict(r=18, c=0, kind="podcast", num=12, place="Jiddah", level="0-A1 Level"),
    dict(r=18, c=1, kind="bag", num=44),
    dict(r=19, c=1, kind="podcast", num=11, place="Chechnya", level="B1-B2 Level"),
    dict(r=19, c=2, kind="podcast", num=9, place="Grozny", level="0-A1 Level"),
    # --- скрин 6 (ряды 20–23)
    dict(r=20, c=0, kind="bag", num=47),
    dict(r=20, c=2, kind="podcast", num=15, place="Russia", level="A2-B1 Level"),
    dict(r=21, c=0, kind="podcast", num=18, place="Saudi Arabia", level="0-A1 Level"),
    dict(r=21, c=1, kind="podcast", num=21, place="Russia", level="B1-B2 Level"),
    dict(r=21, c=2, kind="bag", num=46, maybe=True),
    dict(r=22, c=0, kind="podcast", num=16, place="Moscow", level="B1-B2 Level"),
    dict(r=22, c=1, kind="podcast", num=14, place="Russia", level="B1-B2 Level"),
    dict(r=22, c=2, kind="podcast", num=17, place="Moscow", level="B1-B2 Level"),
    dict(r=23, c=0, kind="bag", num=53, maybe=True),
    dict(r=23, c=2, kind="podcast", num=19, place="Russia", level="B1-B2 Level", maybe=True),
    # --- скрин 7 (ряды 24–27)
    dict(r=24, c=0, kind="podcast", num=36, top="by our student", level="0-A1 Level"),
    dict(r=24, c=1, kind="podcast", num=20, place="Russia", level="B1-B2 Level"),
    dict(r=24, c=2, kind="podcast", num=8, place="Saudi Arabia", level="0-A1 Level"),
    dict(r=25, c=0, kind="podcast", num=5, place="Moscow", level="A2-B1 Level"),
    dict(r=25, c=1, kind="bag", num=52),
    dict(r=25, c=2, kind="bag", num=42),
    dict(r=26, c=0, kind="podcast", num=10, place="Magas", level="0-A1 Level"),
    dict(r=26, c=1, kind="podcast", num=3, place="Moscow", level="0-A1 Level"),
    dict(r=26, c=2, kind="podcast", num=29, place="Grozny", level="0-A1 Level"),
    dict(r=27, c=0, kind="bag", num=39),
    dict(r=27, c=1, kind="podcast", num=26, place="Saudi Arabia", level="0-A1 Level"),
    dict(r=27, c=2, kind="podcast", num=22, place="Russia", level="A2-B1 Level"),
    # --- скрин 8 (ряды 28–31)
    dict(r=28, c=0, kind="podcast", num=32, place="Grozny", level="0-A1 Level"),
    dict(r=28, c=1, kind="bag", num=45),
    dict(r=29, c=0, kind="bag", num=50, maybe=True),
    dict(r=29, c=1, kind="podcast", num=31, place="Chechnya", level="B1-B2 Level"),
    dict(r=29, c=2, kind="bag", num=48),
    dict(r=30, c=0, kind="podcast", num=28, place="England", level="B1-B2 Level"),
    dict(r=30, c=1, kind="bag", num=49, maybe=True),
    dict(r=31, c=0, kind="special", title=["Отзыв", "ученицы"], quote="Мадина Алиева"),
]

# Цвета бренда (заменить на точные коды, когда пришлёт)
BEIGE = "#D2CEC3"
GREEN = "#415038"
ORANGE = "#DA5200"
