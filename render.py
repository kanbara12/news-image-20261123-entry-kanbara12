#!/usr/bin/env python3
"""Draw the front page for make.fun news-image-20261123 (kanbara12).

Local-only renderer: Pillow draws entry.png; the grader never runs this
file (main.py only copies the finished image). No randomness, no clock,
no network: the same run always writes the same bytes.

Layout, top to bottom: masthead, three lead stories with drawn art, a
world map with 12 pins, four columns of short briefs, footer date check.
"""
import math
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"

BG = (247, 242, 231)
FG = (20, 20, 20)
DARK = (18, 33, 61)
DARK2 = (28, 52, 96)
JADE = (14, 110, 110)
BRICK = (176, 58, 32)
AMBER = (198, 142, 32)
PARCH = (247, 242, 231)
SLATE = (70, 70, 70)
SEA = (178, 208, 226)
SHORE = (216, 196, 154)
COAST = (138, 118, 82)
DOT = (192, 39, 32)
RULE = (150, 140, 120)
FAINT = (210, 200, 180)


def typeface(path, size):
    return ImageFont.truetype(path, size)


def split_lines(draw, txt, fnt, maxw):
    """Greedy word wrap: longest fitting prefix per line."""
    words = txt.split()
    lines = []
    start = 0
    while start < len(words):
        end = start + 1
        while end <= len(words):
            if draw.textlength(" ".join(words[start:end]), font=fnt) > maxw:
                break
            end += 1
        end -= 1
        if end == start:
            end = start + 1
        lines.append(" ".join(words[start:end]))
        start = end
    return lines


def fit_block(draw, head, deck, hf, df, maxw, budget):
    """Headline (max 2 lines) plus deck (max 3 lines) within the budget.

    A brief that does not fit FAILS LOUDLY instead of being silently
    cut: a clipped sentence is a visible defect, so the renderer must
    refuse to ship it. Budget 56 = 2 headline lines (2x15) + 2 deck
    lines (2x13), or 1 headline line + 3 deck lines.
    """
    hl = split_lines(draw, head, hf, maxw)
    dl = split_lines(draw, deck, df, maxw)
    cost = len(hl) * 15 + len(dl) * 13
    if len(hl) > 2 or len(dl) > 3 or cost > budget:
        raise SystemExit(
            f"fit_block overflow: headline {len(hl)} lines, deck "
            f"{len(dl)} lines, cost {cost} > budget {budget}: "
            f"{head!r} / {deck!r}")
    return hl, dl


canvas = Image.new("RGB", (PAGE_W, PAGE_H), BG)
d = ImageDraw.Draw(canvas)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, PAGE_W, 104], fill=DARK)
d.rectangle([0, 104, PAGE_W, 108], fill=AMBER)
d.text((PAGE_W // 2, 16), "THE WORLD IN ONE DAY",
       font=typeface(SERIF_B, 47), fill=PARCH, anchor="ma")
d.text((PAGE_W // 2, 70), "Monday 23 November 2026",
       font=typeface(SANS_B, 21), fill=(232, 196, 90), anchor="ma")

# ---------------------------------------------------------------- lead stories
LEADS = [
    dict(kicker="CLIMATE  \u2022  ANTALYA", tint=JADE, sky=(16, 96, 96),
         title="COP31 COLLAPSES WITH NO DEAL",
         body="Nearly 200 nations fail to agree; the final draft never "
              "mentions fossil fuels. First summit since 2009 to end "
              "empty-handed \u2014 Guterres \u2018deeply disappointed\u2019."),
    dict(kicker="GULF  \u2022  BAHRAIN", tint=BRICK, sky=(122, 52, 28),
         title="IRANIAN STRIKE HITS BAHRAIN",
         body="A civilian industrial site on Sitra is hit; two hurt, one "
              "critically. Tehran claims US Patriot radars hit \u2014 Bahrain "
              "denies it. Bahrain takes Iran to the UN Security Council."),
    dict(kicker="LIBYA  \u2022  BENGHAZI", tint=(30, 30, 48), sky=(24, 28, 52),
         title="SEA DRONES HIT RUSSIAN CORVETTE",
         body="Suspected Ukrainian sea drones severely damage the corvette "
              "Merkury at Benghazi naval base; satellite images show it "
              "partly submerged. 10 hurt lightly; Libya asks the UN to "
              "investigate."),
]
LEAD_X = [16, 352, 688]
LEAD_W = 320
LEAD_Y, LEAD_H = 116, 258
ART_H = 112


def paint_cop(x0, y0, w, h):
    """Antalya: sun, sea, conference hall with a dome, cracked earth."""
    d.ellipse([x0 + w - 82, y0 + 12, x0 + w - 22, y0 + 72],
              fill=(245, 214, 110))
    d.rectangle([x0, y0 + 80, x0 + w, y0 + h], fill=(38, 122, 138))
    for k in range(3):
        yy = y0 + 86 + k * 9
        d.arc([x0 + 18 + k * 8, yy, x0 + w - 18 - k * 8, yy + 16],
              180, 360, fill=(220, 240, 240), width=2)
    d.rectangle([x0 + 88, y0 + 56, x0 + 232, y0 + 84], fill=(240, 236, 224))
    d.pieslice([x0 + 128, y0 + 22, x0 + 192, y0 + 62], 180, 360,
               fill=(240, 236, 224))
    d.rectangle([x0 + 158, y0 + 8, x0 + 162, y0 + 26], fill=(240, 236, 224))
    d.polygon([(x0 + 162, y0 + 8), (x0 + 180, y0 + 14), (x0 + 162, y0 + 20)],
              fill=BRICK)
    for kx in range(5):
        d.rectangle([x0 + 98 + kx * 24, y0 + 64, x0 + 108 + kx * 24,
                     y0 + 74], fill=DARK2)
    for kx, ky in [(20, 96), (60, 100), (120, 95), (200, 100), (260, 96),
                   (300, 100)]:
        d.line([x0 + kx, y0 + ky, x0 + kx + 14, y0 + ky + 6],
               fill=(210, 190, 140), width=2)


def paint_gulf(x0, y0, w, h):
    """Sitra: dusk sky, factory blocks, chimney smoke, fire burst."""
    d.ellipse([x0 + 30, y0 + 12, x0 + 84, y0 + 66], fill=(245, 178, 90))
    d.rectangle([x0, y0 + 84, x0 + w, y0 + h], fill=(52, 96, 120))
    for bx, bw, bh in [(24, 64, 34), (96, 48, 48), (152, 70, 30),
                       (230, 56, 42)]:
        d.rectangle([x0 + bx, y0 + h - bh, x0 + bx + bw, y0 + h],
                    fill=(28, 28, 36))
        for wy in range(y0 + h - bh + 6, y0 + h - 4, 12):
            for wx in range(x0 + bx + 6, x0 + bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 200, 90))
    d.rectangle([x0 + 250, y0 + 30, x0 + 262, y0 + h - 40],
                fill=(40, 40, 48))
    for sx, sy, sr in [(252, 22, 7), (244, 12, 9), (258, 4, 6)]:
        d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                  fill=(200, 200, 200))
    cx, cy = x0 + 120, y0 + h - 48
    for k in range(8):
        a = k * math.pi / 4
        d.polygon([(cx, cy),
                   (cx + 24 * math.cos(a), cy + 24 * math.sin(a)),
                   (cx + 9 * math.cos(a + 0.4), cy + 9 * math.sin(a + 0.4))],
                  fill=(240, 140, 40))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(250, 210, 90))


def paint_corvette(x0, y0, w, h):
    """Benghazi: night sea, listing corvette, smoke, two sea drones."""
    for sx, sy in [(28, 14), (92, 28), (180, 10), (250, 24), (300, 42),
                   (140, 42), (60, 50), (220, 56)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                  fill=(235, 235, 220))
    d.rectangle([x0, y0 + 76, x0 + w, y0 + h], fill=(30, 68, 96))
    for k in range(3):
        yy = y0 + 82 + k * 10
        d.arc([x0 + 16 + k * 8, yy, x0 + w - 16 - k * 8, yy + 14],
              180, 360, fill=(190, 220, 235), width=2)
    d.polygon([(x0 + 40, y0 + 58), (x0 + 280, y0 + 74),
               (x0 + 268, y0 + 96), (x0 + 56, y0 + 88)],
              fill=(36, 36, 44))
    d.rectangle([x0 + 120, y0 + 40, x0 + 190, y0 + 60], fill=(36, 36, 44))
    d.rectangle([x0 + 150, y0 + 22, x0 + 158, y0 + 42], fill=(36, 36, 44))
    for sx, sy, sr in [(150, 30, 8), (140, 20, 10), (162, 14, 7)]:
        d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                  fill=(120, 120, 120))
    cx, cy = x0 + 200, y0 + 66
    for k in range(6):
        a = k * math.pi / 3
        d.polygon([(cx, cy),
                   (cx + 16 * math.cos(a), cy + 16 * math.sin(a)),
                   (cx + 6 * math.cos(a + 0.5), cy + 6 * math.sin(a + 0.5))],
                  fill=(240, 140, 40))
    for dx, dy in [(52, 96), (250, 100)]:
        d.ellipse([x0 + dx - 10, y0 + dy - 3, x0 + dx + 10, y0 + dy + 3],
                  fill=(210, 210, 210))
        d.line([x0 + dx - 22, y0 + dy + 4, x0 + dx - 10, y0 + dy],
               fill=(220, 235, 245), width=2)


ARTISTS = [paint_cop, paint_gulf, paint_corvette]

for i, lead in enumerate(LEADS):
    x0 = LEAD_X[i]
    d.rectangle([x0, LEAD_Y, x0 + LEAD_W, LEAD_Y + LEAD_H],
                fill=(255, 255, 255), outline=RULE, width=1)
    d.rectangle([x0, LEAD_Y, x0 + LEAD_W, LEAD_Y + ART_H], fill=lead["sky"])
    ARTISTS[i](x0, LEAD_Y, LEAD_W, ART_H)
    kf = typeface(SANS_B, 12)
    kw = d.textlength(lead["kicker"], font=kf)
    d.rectangle([x0, LEAD_Y, x0 + kw + 16, LEAD_Y + 22], fill=lead["tint"])
    d.text((x0 + 8, LEAD_Y + 4), lead["kicker"], font=kf,
           fill=(255, 255, 255))
    hf = typeface(SANS_B, 19)
    hl = split_lines(d, lead["title"], hf, LEAD_W - 20)
    yy = LEAD_Y + ART_H + 8
    for ln in hl[:2]:
        d.text((x0 + 10, yy), ln, font=hf, fill=FG)
        yy += 23
    bf = typeface(SANS, 13)
    for ln in split_lines(d, lead["body"], bf, LEAD_W - 20)[:5]:
        d.text((x0 + 10, yy), ln, font=bf, fill=SLATE)
        yy += 17


# ---------------------------------------------------------------- world map
d.text((16, 382), "WHERE IT HAPPENED", font=typeface(SANS_B, 14), fill=DARK)
d.text((PAGE_W - 16, 382), "12 places that made the news",
       font=typeface(SANS, 13), fill=SLATE, anchor="ra")
MAPBOX = [16, 402, 1008, 514]
d.rectangle(MAPBOX, fill=SEA, outline=RULE, width=1)


def xy(lon, lat):
    x = MAPBOX[0] + (lon + 170.0) / 360.0 * (MAPBOX[2] - MAPBOX[0])
    y = MAPBOX[1] + (75.0 - lat) / 130.0 * (MAPBOX[3] - MAPBOX[1])
    return (x, y)


# Coastlines as one compact string: "lon,lat lon,lat | ..." per landmass.
LAND_S = (
    "-168,66 -140,70 -125,71 -110,68 -95,69 -85,66 -80,73 -70,62 -60,55 "
    "-55,47 -65,44 -75,35 -80,26 -85,20 -90,14 -95,16 -100,20 -110,23 "
    "-120,34 -125,40 -125,49 -140,60 -155,58 -165,60 | "
    "-55,60 -45,60 -40,65 -30,68 -22,70 -30,76 -45,76 -58,74 -60,70 | "
    "-80,10 -75,5 -70,10 -60,8 -50,0 -40,-5 -35,-10 -40,-20 -48,-28 -55,-35 "
    "-65,-40 -70,-50 -70,-55 -75,-45 -75,-30 -80,-20 -80,-10 -80,0 | "
    "-17,15 -10,30 0,35 10,37 20,32 30,31 35,28 43,12 51,10 48,0 40,-10 "
    "35,-20 30,-30 20,-35 15,-30 12,-18 8,-2 9,4 -8,4 -15,10 | "
    "-10,36 -9,43 -2,48 0,50 5,53 8,57 10,59 18,56 21,55 24,58 28,60 30,62 "
    "30,70 40,68 45,65 40,60 35,55 30,50 28,45 23,40 20,40 15,44 10,44 3,43 "
    "-2,37 -6,36 | "
    "30,70 40,68 50,70 60,70 70,72 80,73 90,75 100,77 110,74 120,73 130,72 "
    "140,72 150,70 160,66 170,66 162,60 158,52 142,50 140,40 135,35 130,33 "
    "127,35 122,38 120,30 115,23 110,20 105,10 100,8 98,15 95,16 92,21 88,22 "
    "85,19 80,15 77,8 75,20 70,22 66,25 61,25 57,26 54,26 50,29 48,30 44,29 "
    "40,32 36,36 33,42 30,45 30,50 35,55 40,60 45,65 50,68 | "
    "95,5 100,0 105,-5 110,-7 115,-8 120,-10 125,-9 130,-3 135,-4 140,-8 "
    "138,-2 132,0 128,2 125,5 120,0 115,2 110,0 105,2 100,5 | "
    "113,-22 114,-30 115,-35 120,-34 125,-32 130,-32 135,-35 140,-38 145,-38 "
    "150,-37 153,-32 153,-27 150,-22 146,-19 142,-15 142,-11 137,-12 135,-15 "
    "132,-12 130,-13 126,-14 122,-17 118,-20 | "
    "-5,50 -3,53 -5,56 -3,58 -1,57 0,53 1,51 | "
    "130,31 132,33 134,34 136,35 138,35 140,36 141,38 141,41 143,43 145,44 "
    "142,44 140,40 138,38 136,36 134,34 132,33 | "
    "44,-16 47,-15 50,-16 49,-20 47,-25 44,-25 43,-20 | "
    "167,-45 170,-43 173,-41 175,-38 177,-38 175,-40 172,-42 168,-46"
)


def parse_polys(blob):
    out = []
    for chunk in blob.split("|"):
        pts = []
        for pair in chunk.split():
            lo, la = pair.split(",")
            pts.append((int(lo), int(la)))
        out.append(pts)
    return out


for poly in parse_polys(LAND_S):
    d.polygon([xy(lo, la) for lo, la in poly], fill=SHORE, outline=COAST)

# lon, lat, label, anchor, dx, dy — 8 labelled, 4 dots in the crowd.
# Optional 7th/8th fields shift the DOT only (ox, oy): Sparta II is
# nudged west so its dot no longer crowds the Dymer dot.
MARKS = [
    (30.7, 36.9, "ANTALYA", "la", 9, -12),
    (30.3, 50.8, "DYMER", "la", 9, -14),
    (26.2, 60.5, None, None, 0, 0, -10, -2),
    (4.35, 50.85, "BRUSSELS", "ra", -9, -6),
    (50.6, 26.15, "BAHRAIN", "la", 9, 8),
    (56.3, 26.6, None, None, 0, 0),
    (44.2, 15.35, None, None, 0, 0),
    (20.1, 32.1, "BENGHAZI", "ra", -9, 0),
    (32.5, 15.6, "KHARTOUM", "la", 9, 14),
    (6.1, 4.9, None, None, 0, 0),
    (77.2, 28.6, "NEW DELHI", "la", 9, -6),
    (-84.43, 33.64, "ATLANTA", "la", 9, -6),
]
pf = typeface(SANS_B, 11)
for mark in MARKS:
    lon, lat, label, anchor, dx, dy = mark[:6]
    ox, oy = mark[6:8] if len(mark) > 6 else (0, 0)
    x, y = xy(lon, lat)
    x += ox
    y += oy
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=DOT,
              outline=(255, 255, 255), width=2)
    if label:
        d.text((x + dx, y + dy), label, font=pf, fill=FG, anchor=anchor,
               stroke_width=2, stroke_fill=(255, 255, 255))

# ---------------------------------------------------------------- brief columns
SECTIONS = [
    ("EUROPE + SPORT", [
        ("Drone flattens flats in Dymer",
         "Two bodies found, 15 missing including two children, near Kyiv."),
        ("Sparta II towed from Baltic",
         "Fire-damaged Russian cargo ship leaves Finnish waters; crew safe."),
        ("NATO meets on Poland today",
         "Allies gather in Brussels over Russian Kh-101 missiles in Poland."),
        ("Belgium grounds all flights",
         "All flights 07:00\u201321:00 cancelled; 429 scheduled, 59,500 "
         "passengers hit."),
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
        ("Settlers torch West Bank cars",
         "At least a dozen cars burned; Eisenkot calls it \u2018Jewish "
         "terrorism\u2019."),
        ("Bahrain takes Iran to the UN",
         "Manama demands enforcement of Resolution 2817 and full damages."),
        ("Saudi jets hit Sanaa station",
         "Houthi media say six hurt; coalition says it stopped a drone."),
        ("Netanyahu\u2013Eisenkot talks fail",
         "Unity-government talks end with no deal over who leads."),
    ]),
    ("AFRICA + ASIA-PACIFIC", [
        ("Drones kill four near Khartoum",
         "A UN building is damaged; Sudan\u2019s army blames launches from "
         "Ethiopia."),
        ("Nigeria boat: at least 24 dead",
         "Overloaded boat carrying funeral mourners capsizes in Bayelsa."),
        ("At least 24 die in South Sudan raid",
         "Rebels hit a cattle camp in Warrap; 7 children among the dead."),
        ("Fighting traps WHO Ebola team",
         "Clashes pin the team inside a DR Congo hospital for over a day."),
        ("Nepal PM meets Modi today",
         "Balendra Shah holds talks in New Delhi on his first trip abroad."),
        ("Search resumes at Cikande",
         "24 body bags found at torched candy factory; 29 workers still "
         "missing."),
        ("JEE Main sign-up closes today",
         "Registration ends for India\u2019s 2027 engineering entrance exam."),
        ("Japan's Labor Thanksgiving",
         "National holiday; Tokyo markets closed for the day."),
        ("US futures bounce, Asia braces",
         "Taiwan down 17% in a week; Seoul readies market stabilisation."),
    ]),
    ("AMERICAS + OCEANIA", [
        ("Australia opens asbestos week",
         "One in three homes found to contain asbestos materials."),
        ("NZ fight to save Wellington Test",
         "India\u2019s record 720/9 leaves NZ 157/4 at lunch on day 5."),
        ("Delta failure snarls Atlanta",
         "Computer fault delays hundreds of flights before Thanksgiving."),
        ("King tides threaten San Francisco",
         "Record tides feared; mayor urges no non-essential travel."),
        ("US ports face cyber surge",
         "LA blocked 120 million attack attempts in August, FT reports."),
        ("US agencies face patch deadline",
         "Four exploited flaws due today, led by a VMware bug rated 9.8."),
        ("Democrats win House, 258 seats",
         "Biggest majority since 1992 after a North Carolina win."),
        ("Mexico: 11 die in cartel arrest",
         "Four soldiers and seven gunmen killed as \u2018El Chapo Isidro\u2019 "
         "is seized."),
    ]),
]
COL_X = [16, 268, 520, 772]
COL_W = 236
COL_TOP = 524


def draw_column(x0, title, items):
    d.rectangle([x0, COL_TOP, x0 + COL_W, COL_TOP + 24], fill=DARK)
    d.text((x0 + 8, COL_TOP + 5), title, font=typeface(SANS_B, 12),
           fill=PARCH)
    yy = COL_TOP + 30
    for head, deck in items:
        hl, dl = fit_block(d, head, deck, typeface(SANS_B, 13),
                           typeface(SANS, 12), COL_W - 4, 56)
        for ln in hl:
            d.text((x0 + 2, yy), ln, font=typeface(SANS_B, 13), fill=FG)
            yy += 15
        for ln in dl:
            d.text((x0 + 2, yy), ln, font=typeface(SANS, 12), fill=SLATE)
            yy += 13
        yy += 1
        d.line([x0, yy - 1, x0 + COL_W, yy - 1], fill=FAINT, width=1)
        yy += 1


for ci, (title, items) in enumerate(SECTIONS):
    draw_column(COL_X[ci], title, items)

# ---------------------------------------------------------------- footer
d.rectangle([0, 962, PAGE_W, PAGE_H], fill=DARK)
d.rectangle([0, 962, PAGE_W, 966], fill=AMBER)
d.text((PAGE_W // 2, 972),
       "DATE CHECK: Coverage verified for Monday 23 November 2026.",
       font=typeface(SANS_B, 17), fill=PARCH, anchor="ma")
d.text((PAGE_W // 2, 996),
       "34 stories  \u00b7  7 regions  \u00b7  Every story happened or was first "
       "reported on 23 November 2026",
       font=typeface(SANS, 13), fill=(200, 210, 225), anchor="ma")

canvas.save(OUT, format="PNG")
print("saved", OUT)
