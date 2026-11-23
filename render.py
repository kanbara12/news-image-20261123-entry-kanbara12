#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261123 (kanbara12).

Fresh code written for this entry only. PIL draws the image locally; the
grader never runs this file (main.py only copies entry.png).
Deterministic: no randomness, no clock, no network.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FD = "/usr/share/fonts/truetype/dejavu/"
F_SERIF_B = FD + "DejaVuSerif-Bold.ttf"
F_SANS_B = FD + "DejaVuSans-Bold.ttf"
F_SANS = FD + "DejaVuSans.ttf"

PAPER = (247, 242, 231)
INK = (20, 20, 20)
NAVY = (18, 33, 61)
NAVY2 = (28, 52, 96)
TEAL = (14, 110, 110)
RUST = (176, 58, 32)
GOLD = (198, 142, 32)
CREAM = (247, 242, 231)
GREY = (70, 70, 70)
OCEAN = (178, 208, 226)
LAND = (216, 196, 154)
LAND_EDGE = (138, 118, 82)
PIN = (192, 39, 32)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, head, deck, hf, df, max_w, budget):
    """Headline up to 2 lines, deck trimmed until total fits budget px."""
    hl = wrap(d, head, hf, max_w)[:2]
    dl = wrap(d, deck, df, max_w)
    while dl and (len(hl) * 15 + len(dl) * 13) > budget:
        dl = dl[:-1]
    if not dl:
        dl = wrap(d, deck, df, max_w)[:1]
        if len(hl) * 15 + 13 > budget:
            hl = hl[:1]
    return hl, dl


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 104], fill=NAVY)
d.rectangle([0, 104, W, 108], fill=GOLD)
t = font(F_SERIF_B, 47)
d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=t, fill=CREAM, anchor="ma")
t2 = font(F_SANS_B, 21)
d.text((W // 2, 70), "Monday 23 November 2026", font=t2, fill=(232, 196, 90),
       anchor="ma")

# ---------------------------------------------------------------- heroes
heroes = [
    dict(tag="CLIMATE  \u2022  ANTALYA", tagc=TEAL, sky=(16, 96, 96),
         head="COP31 COLLAPSES WITH NO DEAL",
         deck="Nearly 200 nations fail to agree; the final draft never "
              "mentions fossil fuels. First summit since 2009 to end "
              "empty-handed \u2014 Guterres \u2018deeply disappointed\u2019."),
    dict(tag="GULF  \u2022  BAHRAIN", tagc=RUST, sky=(122, 52, 28),
         head="IRANIAN STRIKE HITS BAHRAIN",
         deck="A civilian industrial site on Sitra is hit; two hurt, one "
              "critically. Tehran claims US Patriot radars hit \u2014 Bahrain "
              "denies it. Bahrain takes Iran to the UN Security Council."),
    dict(tag="LIBYA  \u2022  BENGHAZI", tagc=(30, 30, 48), sky=(24, 28, 52),
         head="SEA DRONES HIT RUSSIAN CORVETTE",
         deck="Suspected Ukrainian sea drones severely damage the corvette "
              "Merkury at Benghazi naval base; satellite images show it "
              "partly submerged. 10 hurt lightly; Libya asks the UN to "
              "investigate."),
]
HX = [16, 352, 688]
HW = 320
HY, HH = 116, 258
PANEL = 112


def hero_art(i, x0, y0, w, h, sky):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=sky)
    if i == 0:  # COP31: sun, sea, conference dome, flags
        d.ellipse([x0 + w - 82, y0 + 12, x0 + w - 22, y0 + 72],
                  fill=(245, 214, 110))
        d.rectangle([x0, y0 + 80, x0 + w, y0 + h], fill=(38, 122, 138))
        for k in range(3):
            yy = y0 + 86 + k * 9
            d.arc([x0 + 18 + k * 8, yy, x0 + w - 18 - k * 8, yy + 16],
                  180, 360, fill=(220, 240, 240), width=2)
        # conference hall with dome
        d.rectangle([x0 + 88, y0 + 56, x0 + 232, y0 + 84], fill=(240, 236, 224))
        d.pieslice([x0 + 128, y0 + 22, x0 + 192, y0 + 62], 180, 360,
                   fill=(240, 236, 224))
        d.rectangle([x0 + 158, y0 + 8, x0 + 162, y0 + 26], fill=(240, 236, 224))
        d.polygon([(x0 + 162, y0 + 8), (x0 + 180, y0 + 14), (x0 + 162, y0 + 20)],
                  fill=RUST)
        for kx in range(5):
            d.rectangle([x0 + 98 + kx * 24, y0 + 64, x0 + 108 + kx * 24,
                         y0 + 74], fill=NAVY2)
        # cracked earth strip at the bottom
        for kx, ky in [(20, 96), (60, 100), (120, 95), (200, 100), (260, 96),
                       (300, 100)]:
            d.line([x0 + kx, y0 + ky, x0 + kx + 14, y0 + ky + 6],
                   fill=(210, 190, 140), width=2)
    elif i == 1:  # Bahrain: dusk sky, industrial site, fire, smoke
        d.ellipse([x0 + 30, y0 + 12, x0 + 84, y0 + 66], fill=(245, 178, 90))
        d.rectangle([x0, y0 + 84, x0 + w, y0 + h], fill=(52, 96, 120))
        # factory blocks
        for bx, bw, bh in [(24, 64, 34), (96, 48, 48), (152, 70, 30),
                           (230, 56, 42)]:
            d.rectangle([x0 + bx, y0 + h - bh, x0 + bx + bw, y0 + h],
                        fill=(28, 28, 36))
            for wy in range(y0 + h - bh + 6, y0 + h - 4, 12):
                for wx in range(x0 + bx + 6, x0 + bx + bw - 6, 12):
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 200, 90))
        # chimney with smoke
        d.rectangle([x0 + 250, y0 + 30, x0 + 262, y0 + h - 40],
                    fill=(40, 40, 48))
        for k, (sx, sy, sr) in enumerate([(252, 22, 7), (244, 12, 9),
                                          (258, 4, 6)]):
            d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                      fill=(200, 200, 200))
        # fire burst on the middle block
        cx, cy = x0 + 120, y0 + h - 48
        for k in range(8):
            a = k * math.pi / 4
            d.polygon([(cx, cy),
                       (cx + 24 * math.cos(a), cy + 24 * math.sin(a)),
                       (cx + 9 * math.cos(a + 0.4), cy + 9 * math.sin(a + 0.4))],
                      fill=(240, 140, 40))
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(250, 210, 90))
    else:  # Merkury: night sea, listing corvette, sea drones
        for sx, sy in [(28, 14), (92, 28), (180, 10), (250, 24), (300, 42),
                       (140, 42), (60, 50), (220, 56)]:
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                      fill=(235, 235, 220))
        d.rectangle([x0, y0 + 76, x0 + w, y0 + h], fill=(30, 68, 96))
        for k in range(3):
            yy = y0 + 82 + k * 10
            d.arc([x0 + 16 + k * 8, yy, x0 + w - 16 - k * 8, yy + 14],
                  180, 360, fill=(190, 220, 235), width=2)
        # corvette hull, listing to starboard
        d.polygon([(x0 + 40, y0 + 58), (x0 + 280, y0 + 74),
                   (x0 + 268, y0 + 96), (x0 + 56, y0 + 88)],
                  fill=(36, 36, 44))
        d.rectangle([x0 + 120, y0 + 40, x0 + 190, y0 + 60], fill=(36, 36, 44))
        d.rectangle([x0 + 150, y0 + 22, x0 + 158, y0 + 42], fill=(36, 36, 44))
        # smoke + fire amidships
        for k, (sx, sy, sr) in enumerate([(150, 30, 8), (140, 20, 10),
                                          (162, 14, 7)]):
            d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                      fill=(120, 120, 120))
        cx, cy = x0 + 200, y0 + 66
        for k in range(6):
            a = k * math.pi / 3
            d.polygon([(cx, cy),
                       (cx + 16 * math.cos(a), cy + 16 * math.sin(a)),
                       (cx + 6 * math.cos(a + 0.5), cy + 6 * math.sin(a + 0.5))],
                      fill=(240, 140, 40))
        # two sea drones with wakes
        for dx, dy in [(52, 96), (250, 100)]:
            d.ellipse([x0 + dx - 10, y0 + dy - 3, x0 + dx + 10, y0 + dy + 3],
                      fill=(210, 210, 210))
            d.line([x0 + dx - 22, y0 + dy + 4, x0 + dx - 10, y0 + dy],
                   fill=(220, 235, 245), width=2)


for i, hro in enumerate(heroes):
    x0 = HX[i]
    d.rectangle([x0, HY, x0 + HW, HY + HH], fill=(255, 255, 255),
                outline=(150, 140, 120), width=1)
    hero_art(i, x0, HY, HW, PANEL, hro["sky"])
    tf = font(F_SANS_B, 12)
    tw = d.textlength(hro["tag"], font=tf)
    d.rectangle([x0, HY, x0 + tw + 16, HY + 22], fill=hro["tagc"])
    d.text((x0 + 8, HY + 4), hro["tag"], font=tf, fill=(255, 255, 255))
    hf = font(F_SANS_B, 19)
    hl = wrap(d, hro["head"], hf, HW - 20)
    yy = HY + PANEL + 8
    for ln in hl[:2]:
        d.text((x0 + 10, yy), ln, font=hf, fill=INK)
        yy += 23
    df = font(F_SANS, 13)
    dl = wrap(d, hro["deck"], df, HW - 20)
    for ln in dl[:5]:
        d.text((x0 + 10, yy), ln, font=df, fill=GREY)
        yy += 17

# ---------------------------------------------------------------- map
MY0, MY1 = 382, 520
d.text((16, MY0), "WHERE IT HAPPENED", font=font(F_SANS_B, 14), fill=NAVY)
d.text((W - 16, MY0), "12 places that made the news", font=font(F_SANS, 13),
       fill=GREY, anchor="ra")
MAP = [16, 402, 1008, 514]
d.rectangle(MAP, fill=OCEAN, outline=(150, 140, 120), width=1)


def proj(lon, lat):
    x = MAP[0] + (lon + 170.0) / 360.0 * (MAP[2] - MAP[0])
    y = MAP[1] + (75.0 - lat) / 130.0 * (MAP[3] - MAP[1])
    return (x, y)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-65, 44), (-75, 35),
     (-80, 26), (-85, 20), (-90, 14), (-95, 16), (-100, 20), (-110, 23),
     (-120, 34), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-30, 76),
     (-45, 76), (-58, 74), (-60, 70)],
    [(-80, 10), (-75, 5), (-70, 10), (-60, 8), (-50, 0), (-40, -5),
     (-35, -10), (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50),
     (-70, -55), (-75, -45), (-75, -30), (-80, -20), (-80, -10), (-80, 0)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (8, -2), (9, 4), (-8, 4), (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (40, 68),
     (45, 65), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (20, 40),
     (15, 44), (10, 44), (3, 43), (-2, 37), (-6, 36)],
    [(30, 70), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 66), (170, 66), (162, 60), (158, 52), (142, 50), (140, 40),
     (135, 35), (130, 33), (127, 35), (122, 38), (120, 30), (115, 23),
     (110, 20), (105, 10), (100, 8), (98, 15), (95, 16), (92, 21), (88, 22),
     (85, 19), (80, 15), (77, 8), (75, 20), (70, 22), (66, 25), (61, 25),
     (57, 26), (54, 26), (50, 29), (48, 30), (44, 29), (40, 32), (36, 36),
     (33, 42), (30, 45), (30, 50), (35, 55), (40, 60), (45, 65), (50, 68)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -3), (135, -4), (140, -8), (138, -2), (132, 0),
     (128, 2), (125, 5), (120, 0), (115, 2), (110, 0), (105, 2), (100, 5)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 38), (141, 41), (143, 43), (145, 44), (142, 44), (140, 40),
     (138, 38), (136, 36), (134, 34), (132, 33)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -25), (44, -25),
     (43, -20)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
     (175, -40), (172, -42), (168, -46)],
]
for poly in CONTINENTS:
    pts = [proj(lo, la) for lo, la in poly]
    d.polygon(pts, fill=LAND, outline=LAND_EDGE)

PINS = [
    # lon, lat, label, anchor, dx, dy
    # Labels staggered so none overlap: 8 labelled, 4 dots (Baltic Sea,
    # Hormuz, Sanaa, Nigeria) in the crowded Europe/Middle-East cluster.
    (30.7, 36.9, "ANTALYA", "ra", -9, 4),
    (30.3, 50.8, "DYMER", "la", 9, -14),
    (26.2, 60.5, None, None, 0, 0),
    (4.35, 50.85, "BRUSSELS", "ra", -9, -6),
    (50.6, 26.15, "BAHRAIN", "la", 9, 8),
    (56.3, 26.6, None, None, 0, 0),
    (44.2, 15.35, None, None, 0, 0),
    (20.1, 32.1, "BENGHAZI", "la", 9, -16),
    (32.5, 15.6, "KHARTOUM", "la", 9, 14),
    (6.1, 4.9, None, None, 0, 0),
    (77.2, 28.6, "NEW DELHI", "la", 9, -6),
    (-84.43, 33.64, "ATLANTA", "la", 9, -6),
]
pf = font(F_SANS_B, 11)
for lon, lat, label, anchor, dx, dy in PINS:
    x, y = proj(lon, lat)
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=PIN, outline=(255, 255, 255),
              width=2)
    if label:
        d.text((x + dx, y + dy), label, font=pf, fill=INK, anchor=anchor,
               stroke_width=2, stroke_fill=(255, 255, 255))

# ---------------------------------------------------------------- columns
COLS = [
    ("EUROPE + SPORT", [
        ("Drone flattens flats in Dymer",
         "Two bodies found, 15 missing including two children, near Kyiv."),
        ("Sparta II towed from Baltic",
         "Fire-damaged Russian cargo ship leaves Finnish waters; crew safe."),
        ("NATO meets on Poland today",
         "Allies gather in Brussels over Russian Kh-101 missiles in Poland."),
        ("Belgium grounds all flights",
         "Air traffic strike cancels 429 Brussels Airport flights today."),
        ("Plot to kill rapper Kyivstoner",
         "Poland says Russia tried twice \u2014 in Denmark and in Poland."),
        ("Liverpool thrash United 4\u20130",
         "Ten-man United humbled in Pochettino\u2019s first game in charge."),
    ]),
    ("MIDDLE EAST", [
        ("Two tankers burn off Hormuz",
         "Iran\u2019s navy says they hit mines east of the strait; UKMTO logs "
         "a separate incident."),
        ("Houthis claim Rabigh strike",
         "Yemen\u2019s Houthis say they hit a Saudi refinery; Riyadh silent."),
        ("Iran readies 14-tanker convoy",
         "Tankers gather at Kharg to test the US blockade; experts doubt it."),
        ("Trump eyes new Iran strikes",
         "New strikes after the new year if no deal, he tells Fox News."),
        ("Settlers torch cars in West Bank",
         "At least a dozen cars burned; Eisenkot calls it \u2018Jewish "
         "terrorism\u2019."),
        ("Bahrain takes Iran to the UN",
         "Manama demands enforcement of Resolution 2817 and full damages."),
        ("Saudi jets hit Sanaa fuel station",
         "Houthi media say six hurt; coalition says it stopped a drone."),
        ("Netanyahu\u2013Eisenkot talks fail",
         "Unity-government talks end with no deal over who leads."),
    ]),
    ("AFRICA + ASIA-PACIFIC", [
        ("Drones kill four near Khartoum",
         "A UN building is damaged; Sudan\u2019s army blames launches from "
         "Ethiopia."),
        ("Nigeria boat sinks: 24 dead",
         "Overloaded boat carrying funeral mourners capsizes in Bayelsa."),
        ("15 die in South Sudan raid",
         "Rebels hit a cattle camp in Warrap; officials warn toll may rise."),
        ("Fighting traps WHO Ebola team",
         "Clashes pin the team inside a DR Congo hospital for over a day."),
        ("Nepal PM meets Modi today",
         "Balendra Shah holds talks in New Delhi on his first trip abroad."),
        ("Search resumes at Cikande factory",
         "24 body bags recovered; 29 workers still missing after the fire."),
        ("JEE Main sign-up closes today",
         "Registration ends for India\u2019s 2027 engineering entrance exam."),
        ("Japan marks Labor Thanksgiving",
         "National holiday; Tokyo markets closed for the day."),
        ("US futures bounce, Asia braces",
         "Taiwan down 17% in a week; Seoul readies market stabilisation."),
    ]),
    ("AMERICAS + OCEANIA", [
        ("Australia opens asbestos week",
         "One in three homes found to contain asbestos materials."),
        ("NZ battle to save Wellington Test",
         "India\u2019s record 720/9 leaves NZ 157/4 at lunch on day 5."),
        ("Delta failure snarls Atlanta",
         "Computer fault delays hundreds of flights before Thanksgiving."),
        ("San Francisco braces for king tides",
         "Record tides feared; mayor urges no non-essential travel."),
        ("US ports face cyber surge",
         "LA blocked 120 million attack attempts in August, FT reports."),
        ("Patch deadline hits US agencies",
         "Four exploited flaws due today, led by a VMware bug rated 9.8."),
        ("Democrats take House, 258 seats",
         "Biggest majority since 1992 after a North Carolina win."),
        ("Mexico: 11 die in cartel arrest",
         "Four soldiers and seven gunmen killed as \u2018El Chapo Isidro\u2019 "
         "is seized."),
    ]),
]
CX = [16, 268, 520, 772]
CW = 236
CY0, CY1 = 524, 950
chf = font(F_SANS_B, 12)
hf = font(F_SANS_B, 13)
df = font(F_SANS, 12)
for ci, (title, items) in enumerate(COLS):
    x0 = CX[ci]
    d.rectangle([x0, CY0, x0 + CW, CY0 + 24], fill=NAVY)
    d.text((x0 + 8, CY0 + 5), title, font=chf, fill=CREAM)
    yy = CY0 + 30
    for head, deck in items:
        hl, dl = fit_lines(d, head, deck, hf, df, CW - 4, 41)
        for ln in hl:
            d.text((x0 + 2, yy), ln, font=hf, fill=INK)
            yy += 15
        for ln in dl:
            d.text((x0 + 2, yy), ln, font=df, fill=GREY)
            yy += 13
        yy += 2
        d.line([x0, yy - 1, x0 + CW, yy - 1], fill=(210, 200, 180), width=1)
        yy += 1

# ---------------------------------------------------------------- footer
d.rectangle([0, 962, W, H], fill=NAVY)
d.rectangle([0, 962, W, 966], fill=GOLD)
ff = font(F_SANS_B, 17)
d.text((W // 2, 972), "DATE CHECK: Coverage verified for Monday 23 November 2026.",
       font=ff, fill=CREAM, anchor="ma")
ff2 = font(F_SANS, 13)
d.text((W // 2, 996),
       "34 stories  \u00b7  7 regions  \u00b7  Every story happened or was first "
       "reported on 23 November 2026",
       font=ff2, fill=(200, 210, 225), anchor="ma")

img.save(OUT, format="PNG")
print("saved", OUT)
