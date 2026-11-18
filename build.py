#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261117 round 3.

Fresh design (v3): navy masthead, red ticker, 18 uniform illustrated
cards in a 3x6 grid, numbered world map + 30-item list below.
All illustrations are flat-vector shapes drawn in code with PIL.
No em-dash / en-dash anywhere in image text (hyphens only).
Deterministic: same input -> byte-identical PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
NAVY = (22, 35, 63)
NAVY_LT = (38, 56, 92)
RED = (164, 30, 34)
GOLD = (201, 162, 39)
INK = (24, 28, 36)
GREY = (90, 88, 80)
WHITE = (255, 255, 255)
CARD_BG = (255, 253, 247)
CARD_LINE = (205, 196, 172)
OCEAN = (207, 224, 232)
LAND = (222, 205, 150)
LAND_LINE = (120, 105, 70)

FD = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def fit_lines(draw, text, fnt_sizes, max_w, max_lines):
    """Pick the largest font size (from list, descending) that wraps
    the text into at most max_lines lines. Returns (font, lines)."""
    for size in fnt_sizes:
        fnt = SANS_B(size) if size >= 13 else SANS(size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = SANS_B(fnt_sizes[-1]) if fnt_sizes[-1] >= 13 else SANS(fnt_sizes[-1])
    return fnt, wrap(draw, text, fnt, max_w)

# ---------------------------------------------------------------- data
# (num, kicker, title, deck, illustration key, (lon, lat), label offset)
CARDS = [
    (1, "EUROPE - UKRAINE WAR",
     "Ukraine drops a Crimean Bridge road span into the sea",
     "Second strike in two days; Zelensky hails an 'unprecedented operation'; Moscow says it downed 1,441 drones.",
     "bridge", (33.5, 45.3), (14, -12)),
    (2, "MIDDLE EAST - IRAN WAR",
     "Iran fires drones at a US radar in Bahrain; US hits Qeshm",
     "Bahrain and the US say all were downed; US jets strike Qeshm; Iran says tankers hit mines in Hormuz.",
     "radar", (50.5, 26.2), (0, 0)),
    (3, "ASIA - DIPLOMACY",
     "Trump holds his first Quad summit, in Manila",
     "Four unveil critical-minerals deals; Trump heads to Shenzhen for Thursday talks with Xi and Putin.",
     "summit", (121.0, 14.6), (0, 0)),
    (4, "US - TECH",
     "Nvidia's quarterly sales double to $115.8bn",
     "First results since Huang quit; revenue up 103% on AI chip demand; board says it won't reinstate him.",
     "chip", (-121.9, 37.4), (-18, -2)),
    (5, "US - BANKING",
     "JPMorgan bug cuts off Zelle users for hours",
     "Software bug in on-premise hardware; delays at Chase and other banks; bank says not a cyberattack.",
     "bank", (-87.6, 41.8), (-14, -10)),
    (6, "US - MARKETS",
     "Wall Street slides: Dow falls 849 points",
     "Dow -1.6%, S&P 500 -1% as AI stocks lead losses.",
     "chart", (-74.0, 40.7), (14, -8)),
    (7, "AFRICA - HEALTH",
     "Ebola cases pass 11,000 in DR Congo",
     "Outbreak more than doubles in three months; 5,400 dead, WHO says.",
     "virus", (23.0, -2.0), (-14, 0)),
    (8, "ASIA - POLITICS",
     "Mongolia's president says he will resign",
     "Khurelsukh denies a $25m bribe claim; parliament must accept.",
     "ger", (106.9, 47.9), (0, 0)),
    (9, "ASIA - DEFENCE",
     "Japan scrambles jets at Russian incursion",
     "Two planes entered airspace near Okinoshima; Tokyo protests, first since 2024.",
     "jets", (130.5, 33.8), (0, 0)),
    (10, "EUROPE - MIGRATION",
     "Five EU states plan Rwanda asylum hub",
     "No deal signed yet; UN rights chief raises concerns.",
     "hub", (30.0, -2.0), (14, 0)),
    (11, "US - SPACE",
     "Vulcan rocket fails; 40 Amazon satellites lost",
     "ULA's first total failure; early data blames a weak first stage.",
     "rocket", (-80.6, 28.4), (10, 10)),
    (12, "GLOBAL - SPACE",
     "Voyager 1 nears one light-day from Earth",
     "First craft so far out; NASA asks the public to shine lights skyward Tuesday night.",
     "voyager", (-118.2, 34.2), (2, -18)),
    (13, "AMERICAS - HEALTH",
     "US, Mexico and Bolivia lose measles-free status",
     "PAHO cites a year of spread; US has 5,400+ cases in 2026.",
     "measles", (-100.0, 40.0), (-2, 14)),
    (14, "EUROPE - LABOUR",
     "French public-sector workers strike over pay",
     "146,000 march, ministry says; CGT claims 500,000.",
     "strike", (2.4, 48.9), (0, 0)),
    (15, "ASIA - LABOUR",
     "Bangladesh police tear-gas garment workers",
     "They want Tk 30,000 a month, up from 12,500; 37 factories shut.",
     "garment", (90.4, 23.8), (0, 0)),
    (16, "EUROPE - PRESS",
     "Turkey seizes opposition broadcaster Sozcu TV",
     "Police raid Istanbul offices; channel off air, trustee named.",
     "tv", (28.9, 41.0), (-16, 4)),
    (17, "GLOBAL - CLIMATE",
     "COP31 enters final days split on fossil fuels",
     "Antalya talks split on finance; Brazil says the draft falls short.",
     "climate", (30.7, 36.9), (-2, 16)),
    (18, "EUROPE - POLITICS",
     "Serbia's student-led majority takes its seats",
     "Student List holds 140 of 250; Vucic's party goes into opposition.",
     "ballot", (20.5, 44.8), (0, -14)),
]

# 19-48, one short line each (verified 17 Nov 2026 reporting)
BRIEFS = [
    "Gaza: UN warns winter crisis; 1.4m hungry",
    "Russian An-12 crash in Siberia kills all 19",
    "Cyclone Akvan grows; Odisha evacuates",
    "UK sanctions 8 firms over West Bank sites",
    "Eisenkot elected Knesset speaker, 66-52",
    "Pope Leo XIV back from South America tour",
    "WHO: superbugs could kill 39m by 2050",
    "US data centres emit like Denmark: study",
    "Ecuador fishermen sue US over boat strike",
    "Mexico: journalist found dead in Acapulco",
    "PNG defends closing Taiwan office",
    "Football: Canada beat Guatemala 4-1",
    "Poland: Tusk survives vote, 242-200",
    "Nepal: loss-and-damage first",
    "Moldova shuts airspace as drone nears",
    "Haiti: Aristide party fields no candidates",
    "Pentagon fails audit for ninth year",
    "NSA secret network down; no sign of hack",
    "Home Depot sales beat forecasts",
    "Brazil Senate delays fiscal vote",
    "Singapore seeks trusted AI-chip access",
    "World Court hears Myanmar case",
    "Bezos helped cast Pattinson as Bond",
    "Cyclone Xavier hits Cat 5, winds 220 km/h",
    "German ZEW jumps to 35.6, beats forecasts",
    "Depardieu drops appeal",
    "Seoul scrambles jets as Russian planes near",
    "Japan economy contracts",
    "UK PM tests EU reset before summit",
    "US-Thailand sign trade statement",
]

TICKER = ("DOW -849 (-1.6%)  |  NVIDIA $115.8BN  |  EBOLA 11,000+  |  "
          "VOYAGER 1 NEARS ONE LIGHT-DAY  |  KERCH BRIDGE HIT  |  "
          "TRUMP-XI-PUTIN THU")

# ---------------------------------------------------------------- map
NA = [(-168, 66), (-158, 71), (-140, 70), (-130, 71), (-125, 72), (-115, 73),
      (-105, 72), (-95, 80), (-88, 82), (-80, 78), (-75, 73), (-82, 66),
      (-85, 60), (-80, 57), (-88, 56), (-93, 59), (-94, 64), (-88, 68),
      (-80, 66), (-72, 60), (-65, 60), (-55, 52), (-60, 46), (-70, 42),
      (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20),
      (-115, 28), (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)]
SA = [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
      (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52),
      (-73, -50), (-73, -37), (-70, -20), (-77, -12), (-81, -5), (-80, 1)]
AFRICA = [(-17, 15), (-10, 31), (-5, 35), (10, 37), (20, 32), (32, 31),
          (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
          (32, -29), (26, -34), (19, -35), (15, -27), (12, -18), (9, 4),
          (4, 6), (-8, 5), (-13, 8), (-17, 12)]
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 58), (10, 59),
           (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68),
           (55, 69), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70),
           (170, 66), (178, 65), (170, 60), (162, 56), (158, 52), (150, 59),
           (142, 55), (140, 45), (135, 35), (130, 33), (127, 35), (122, 38),
           (120, 32), (110, 20), (108, 12), (105, 9), (100, 8), (98, 15),
           (95, 16), (92, 21), (88, 22), (85, 19), (80, 13), (77, 8),
           (74, 20), (70, 23), (66, 25), (62, 25), (58, 26), (56, 27),
           (52, 28), (50, 29), (48, 30), (44, 29), (40, 36), (36, 36),
           (30, 36), (26, 38), (23, 36), (20, 40), (18, 42), (14, 45),
           (12, 44), (8, 44), (3, 43), (-2, 44), (-2, 48), (-5, 48),
           (-10, 43), (-10, 37)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 53), (1, 51)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (140, 36), (141, 39),
         (141, 42), (143, 42), (141, 45), (140, 42), (139, 38), (136, 37),
         (133, 35), (131, 33)]
AUS = [(113, -22), (114, -30), (115, -35), (124, -33), (132, -32),
       (137, -35), (140, -38), (147, -39), (150, -37), (153, -27),
       (146, -19), (142, -11), (136, -12), (132, -12), (126, -14),
       (122, -17), (118, -20)]
GREENLAND = [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-22, 70),
             (-25, 76), (-40, 80), (-55, 78), (-60, 74), (-58, 64)]
CONTINENTS = [NA, SA, AFRICA, EURASIA, UK, JAPAN, AUS, GREENLAND]

# ---------------------------------------------------------------- illustrations
def illu_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 92, 140))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(30, 70, 110))
    d.rectangle([x, y + 8, x + w, y + 14], fill=(220, 220, 210))
    d.rectangle([x, y + 8, x + 90, y + 14], fill=(220, 220, 210))
    for px in (x + 20, x + 60, x + 250, x + 290):
        d.line([px, y + 8, px, y], fill=(220, 220, 210), width=2)
    # broken span falling into the sea
    d.polygon([(x + 130, y + 14), (x + 190, y + 14), (x + 178, y + h - 10),
               (x + 142, y + h - 10)], fill=(200, 190, 170))
    d.ellipse([x + 150, y + 2, x + 168, y + 20], fill=(255, 190, 60))
    d.ellipse([x + 140, y + h - 14, x + 200, y + h - 4], fill=(255, 255, 255))

def illu_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 164, 110))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(150, 115, 70))
    d.ellipse([x + 30, y + 4, x + 90, y + 30], fill=(240, 240, 230))
    d.line([x + 60, y + 18, x + 60, y + h - 8], fill=(90, 80, 60), width=3)
    d.line([x + 30, y + h - 8, x + 90, y + h - 8], fill=(90, 80, 60), width=3)
    d.ellipse([x + 200, y + 6, x + 260, y + 30], fill=(120, 60, 50))
    d.ellipse([x + 216, y + 12, x + 244, y + 24], fill=(200, 90, 70))
    for px, py in ((150, 8), (180, 4), (120, 14)):
        d.polygon([(px, py), (px + 12, py + 3), (px, py + 6)], fill=(40, 40, 40))

def illu_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 90, 120))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 80, 50))
    d.rectangle([x + 90, y + 18, x + 235, y + 26], fill=(150, 110, 70))
    for i, col in enumerate([(178, 34, 34), (255, 255, 255), (0, 60, 120), (255, 153, 51)]):
        fx = x + 110 + i * 30
        d.line([fx, y + 2, fx, y + 18], fill=(230, 230, 220), width=2)
        d.rectangle([fx, y + 2, fx + 18, y + 12], fill=col)
    for cx in (130, 165, 200):
        d.ellipse([cx, y + 14, cx + 12, y + 26], fill=(240, 210, 170))
        d.rectangle([cx, y + 26, cx + 12, y + 28], fill=(40, 40, 40))

def illu_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 90, 60))
    for i in range(5):
        d.line([x + 20 + i * 60, y + 4, x + 20 + i * 60, y + h - 4],
               fill=(60, 160, 110), width=2)
    d.rectangle([x + 130, y + 6, x + 195, y + 30], fill=(30, 30, 30))
    d.rectangle([x + 140, y + 11, x + 185, y + 25], fill=(201, 162, 39))
    d.rectangle([x + 152, y + 14, x + 173, y + 22], fill=(24, 90, 60))
    d.line([x + 220, y + 28, x + 250, y + 18, x + 275, y + 22, x + 305, y + 6],
           fill=(255, 220, 80), width=3)
    d.polygon([(x + 305, y + 6), (x + 296, y + 6), (x + 305, y + 14)], fill=(255, 220, 80))

def illu_bank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 90, 130))
    d.polygon([(x + 30, y + 4), (x + 110, y + 4), (x + 70, y + 14)], fill=(220, 210, 190))
    for cx in (40, 60, 80, 95):
        d.rectangle([cx, y + 16, cx + 7, y + 32], fill=(230, 225, 210))
    d.rectangle([x + 30, y + 32, x + 112, y + 36], fill=(230, 225, 210))
    d.rectangle([x + 230, y + 4, x + 292, y + 36], fill=(30, 30, 34))
    d.rectangle([x + 236, y + 9, x + 286, y + 30], fill=(120, 200, 230))
    d.line([x + 250, y + 30, x + 272, y + 9], fill=(255, 60, 40), width=3)
    d.line([x + 272, y + 30, x + 250, y + 9], fill=(255, 60, 40), width=3)

def illu_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 225))
    for i, (bx, bh) in enumerate(((40, 22), (90, 16), (140, 24), (190, 12), (240, 18))):
        col = (164, 30, 34) if i in (2, 4) else (40, 120, 70)
        d.rectangle([x + bx, y + h - 6 - bh, x + bx + 22, y + h - 6], fill=col)
    d.line([x + 20, y + 6, x + 90, y + 14, x + 170, y + 10, x + 250, y + 26,
            x + 305, y + 30], fill=(164, 30, 34), width=3)
    d.polygon([(x + 305, y + 30), (x + 292, y + 24), (x + 298, y + 32)],
              fill=(164, 30, 34))

def illu_virus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 30, 30))
    cx, cy = x + 160, y + 18
    for ang in range(0, 360, 30):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([cx + dx * 10, cy + dy * 10, cx + dx * 17, cy + dy * 17],
               fill=(90, 200, 120), width=2)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(60, 160, 90))
    d.ellipse([cx - 5, cy - 5, cx + 2, cy + 2], fill=(30, 110, 60))
    for px, py, r in ((60, 8, 4), (90, 26, 3), (260, 10, 4), (280, 24, 3)):
        d.ellipse([x + px - r, y + py - r, x + px + r, y + py + r],
                  fill=(255, 220, 100))

def illu_ger(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 190, 220))
    d.rectangle([x, y + 24, x + w, y + h], fill=(120, 170, 90))
    d.polygon([(x + 120, y + 6), (x + 200, y + 6), (x + 215, y + 24),
               (x + 105, y + 24)], fill=(200, 90, 60))
    d.rectangle([x + 110, y + 24, x + 210, y + 36], fill=(245, 235, 210))
    d.rectangle([x + 152, y + 24, x + 168, y + 36], fill=(120, 70, 40))
    d.line([x + 260, y + 4, x + 260, y + 24], fill=(90, 80, 60), width=2)
    d.rectangle([x + 260, y + 4, x + 284, y + 12], fill=(0, 80, 160))
    d.rectangle([x + 260, y + 12, x + 284, y + 20], fill=(200, 40, 40))

def illu_jets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 180, 220))
    d.ellipse([x + 20, y + 4, x + 70, y + 14], fill=(255, 255, 255))
    d.ellipse([x + 250, y + 8, x + 300, y + 18], fill=(255, 255, 255))
    for jx, jy, col in ((90, 12, (60, 60, 70)), (200, 20, (140, 30, 30))):
        d.polygon([(x + jx, y + jy), (x + jx + 34, y + jy + 5),
                   (x + jx, y + jy + 10)], fill=col)
        d.polygon([(x + jx + 8, y + jy - 6), (x + jx + 16, y + jy + 5),
                   (x + jx + 8, y + jy + 5)], fill=col)
    d.line([x + 130, y + 30, x + 240, y + 30], fill=(164, 30, 34), width=2)

def illu_hub(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 170, 120))
    d.rectangle([x + 110, y + 10, x + 215, y + 36], fill=(245, 240, 225))
    d.polygon([(x + 100, y + 10), (x + 162, y + 0), (x + 225, y + 10)],
              fill=(164, 30, 34))
    d.rectangle([x + 152, y + 20, x + 172, y + 36], fill=(90, 60, 40))
    for i, sx in enumerate((30, 60, 90, 250, 280)):
        d.polygon([(x + sx, y + 4), (x + sx + 3, y + 11), (x + sx + 10, y + 11),
                   (x + sx + 5, y + 15), (x + sx + 7, y + 22), (x + sx, y + 18),
                   (x + sx - 7, y + 22), (x + sx - 5, y + 15),
                   (x + sx - 10, y + 11), (x + sx - 3, y + 11)],
                  fill=(201, 162, 39))

def illu_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 60))
    for sx, sy in ((30, 6), (90, 3), (250, 5), (290, 10), (200, 3)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.polygon([(x + 148, y + 2), (x + 158, y + 2), (x + 162, y + 18),
               (x + 156, y + 30), (x + 150, y + 30), (x + 144, y + 18)],
              fill=(230, 230, 225))
    d.ellipse([x + 149, y + 8, x + 157, y + 16], fill=(120, 200, 230))
    d.polygon([(x + 148, y + 30), (x + 158, y + 30), (x + 160, y + 36),
               (x + 146, y + 36)], fill=(255, 150, 40))
    d.ellipse([x + 60, y + 8, x + 110, y + 30], fill=(200, 120, 60))
    d.ellipse([x + 70, y + 14, x + 100, y + 26], fill=(230, 160, 90))
    for px, py in ((230, 10), (260, 22), (280, 8)):
        d.rectangle([x + px, y + py, x + px + 12, y + py + 4], fill=(120, 200, 230))

def illu_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
    for sx, sy in ((20, 5), (60, 12), (110, 4), (200, 8), (260, 4), (300, 14),
                   (40, 26), (240, 28), (290, 26)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.ellipse([x + 8, y + 8, x + 26, y + 26], fill=(255, 220, 100))
    d.line([x + 120, y + 18, x + 210, y + 18], fill=(180, 180, 180), width=2)
    d.ellipse([x + 210, y + 8, x + 240, y + 28], fill=(201, 162, 39))
    d.line([x + 225, y + 8, x + 225, y + 28], fill=(150, 120, 40), width=2)
    d.rectangle([x + 120, y + 12, x + 150, y + 24], fill=(200, 200, 190))
    d.line([x + 250, y + 18, x + 300, y + 18], fill=(255, 220, 100), width=2)

def illu_measles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 225, 210))
    d.ellipse([x + 120, y + 2, x + 205, y + 34], fill=(230, 120, 100))
    for px, py, r in ((140, 10, 4), (165, 20, 5), (185, 8, 3), (150, 28, 3),
                      (180, 28, 4)):
        d.ellipse([x + px - r, y + py - r, x + px + r, y + py + r],
                  fill=(164, 30, 34))
    d.polygon([(x + 250, y + 4), (x + 268, y + 10), (x + 262, y + 30),
               (x + 244, y + 30), (x + 238, y + 10)], fill=(60, 120, 180))
    d.line([x + 244, y + 12, x + 262, y + 24], fill=(255, 255, 255), width=3)
    d.line([x + 262, y + 12, x + 244, y + 24], fill=(255, 255, 255), width=3)
    for px, py in ((40, 10), (70, 24), (95, 8), (290, 12)):
        d.ellipse([x + px - 3, y + py - 3, x + px + 3, y + py + 3],
                  fill=(164, 30, 34))

def illu_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 225, 190))
    d.polygon([(x + 20, y + 36), (x + 35, y + 6), (x + 50, y + 36)],
              fill=(120, 110, 100))
    d.rectangle([x + 30, y + 2, x + 40, y + 8], fill=(120, 110, 100))
    for i, cx in enumerate((90, 120, 150, 180, 210, 240, 270)):
        d.ellipse([x + cx, y + 10, x + cx + 10, y + 20], fill=(60, 60, 70))
        d.rectangle([x + cx - 2, y + 20, x + cx + 12, y + 36],
                    fill=(164, 30, 34) if i % 2 == 0 else (22, 35, 63))
    d.rectangle([x + 100, y + 2, x + 150, y + 9], fill=(255, 255, 255))
    d.line([x + 125, y + 2, x + 125, y + 14], fill=(90, 80, 60), width=2)

def illu_garment(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
    d.rectangle([x + 20, y + 14, x + 140, y + 36], fill=(150, 120, 90))
    d.polygon([(x + 20, y + 14), (x + 50, y + 4), (x + 80, y + 14)],
              fill=(120, 90, 60))
    d.rectangle([x + 95, y + 2, x + 102, y + 14], fill=(90, 70, 50))
    d.ellipse([x + 170, y + 6, x + 210, y + 30], fill=(230, 230, 220))
    d.ellipse([x + 180, y + 12, x + 200, y + 24], fill=(180, 180, 170))
    d.polygon([(x + 240, y + 10), (x + 280, y + 10), (x + 300, y + 30),
               (x + 220, y + 30)], fill=(40, 120, 160))
    d.rectangle([x + 252, y + 10, x + 268, y + 30], fill=(255, 255, 255))

def illu_tv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 60, 80))
    d.rectangle([x + 90, y + 6, x + 235, y + 32], fill=(20, 20, 26))
    for i in range(6):
        d.line([x + 96, y + 9 + i * 4, x + 229, y + 9 + i * 4],
               fill=(120, 200, 220), width=1)
    d.line([x + 100, y + 32, x + 225, y + 6], fill=(164, 30, 34), width=4)
    d.line([x + 225, y + 32, x + 100, y + 6], fill=(164, 30, 34), width=4)
    d.line([x + 150, y + 32, x + 162, y + 36], fill=(40, 40, 50), width=3)
    d.ellipse([x + 260, y + 12, x + 300, y + 28], fill=(255, 220, 100))

def illu_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 225))
    d.ellipse([x + 20, y + 4, x + 52, y + 36], fill=(255, 220, 100))
    d.ellipse([x + 120, y + 6, x + 160, y + 30], fill=(60, 140, 90))
    d.ellipse([x + 128, y + 10, x + 140, y + 18], fill=(40, 110, 70))
    d.ellipse([x + 144, y + 16, x + 152, y + 24], fill=(40, 110, 70))
    d.line([x + 200, y + 30, x + 200, y + 6], fill=(164, 30, 34), width=3)
    d.ellipse([x + 194, y + 26, x + 206, y + 36], fill=(164, 30, 34))
    d.line([x + 200, y + 12, x + 216, y + 18], fill=(164, 30, 34), width=2)
    d.line([x + 240, y + 30, x + 280, y + 10, x + 300, y + 16],
           fill=(22, 35, 63), width=3)

def illu_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 225, 205))
    d.rectangle([x + 110, y + 14, x + 215, y + 36], fill=(22, 35, 63))
    d.rectangle([x + 140, y + 10, x + 185, y + 14], fill=(255, 255, 255))
    d.polygon([(x + 160, y + 2), (x + 165, y + 8), (x + 175, y + 8),
               (x + 167, y + 12), (x + 170, y + 18), (x + 160, y + 14),
               (x + 150, y + 18), (x + 153, y + 12), (x + 145, y + 8),
               (x + 155, y + 8)], fill=(201, 162, 39))
    for i, cx in enumerate((40, 70, 260, 290)):
        d.ellipse([x + cx, y + 12, x + cx + 10, y + 22], fill=(240, 210, 170))
        d.rectangle([x + cx - 2, y + 22, x + cx + 12, y + 36],
                    fill=(164, 30, 34) if i % 2 else (60, 120, 70))

ILLU = {"bridge": illu_bridge, "radar": illu_radar, "summit": illu_summit,
        "chip": illu_chip, "bank": illu_bank, "chart": illu_chart,
        "virus": illu_virus, "ger": illu_ger, "jets": illu_jets,
        "hub": illu_hub, "rocket": illu_rocket, "voyager": illu_voyager,
        "measles": illu_measles, "strike": illu_strike,
        "garment": illu_garment, "tv": illu_tv, "climate": illu_climate,
        "ballot": illu_ballot}

# ---------------------------------------------------------------- build
def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0-92) navy
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 92, W, 94], fill=GOLD)
    d.text((16, 10), "THE DAY IN WORLD NEWS", font=SANS_B(13), fill=GOLD)
    d.text((16, 30), "Tuesday 17 November 2026", font=SERIF_B(40), fill=WHITE)
    d.text((1008, 14), "48 STORIES", font=SANS_B(20), fill=GOLD, anchor="ra")
    d.text((1008, 42), "6 CONTINENTS - ONE DAY", font=SANS_B(15), fill=WHITE,
           anchor="ra")
    d.text((1008, 64), "ALL IN ONE IMAGE", font=SANS(11), fill=(180, 190, 210),
           anchor="ra")

    # ---- ticker (94-122) red, auto-fit
    d.rectangle([0, 94, W, 122], fill=RED)
    tsize = 17
    while tsize > 11:
        tf = SANS_B(tsize)
        if d.textlength(TICKER, font=tf) <= 992:
            break
        tsize -= 1
    d.text((512, 108), TICKER, font=SANS_B(tsize), fill=WHITE, anchor="mm")

    # ---- 18 uniform cards, 3 cols x 6 rows (y 124-788)
    cw, ch, gap = 325, 106, 5
    x0, y0 = 16, 124
    for idx, (num, kicker, title, deck, key, _pin, _off) in enumerate(CARDS):
        col, row = idx % 3, idx // 3
        cx = x0 + col * (cw + 8)
        cy = y0 + row * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD_BG,
                    outline=CARD_LINE, width=1)
        # illustration band 36px
        ILLU[key](d, cx + 1, cy + 1, cw - 2, 36)
        # number badge
        bx, by = cx + 14, cy + 19
        d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=NAVY,
                  outline=WHITE, width=2)
        d.text((bx, by), str(num), font=SANS_B(11), fill=WHITE, anchor="mm")
        # text block
        tx = cx + 8
        tw = cw - 16
        ty = cy + 38
        d.text((tx, ty), kicker, font=SANS_B(9), fill=RED)
        ty += 11
        tf, tlines = fit_lines(d, title, [14, 13], tw, 2)
        assert len(tlines) <= 2, f"card {num} title overflows: {tlines}"
        for ln in tlines:
            d.text((tx, ty), ln, font=tf, fill=INK)
            ty += 16
        ty += 1
        df, dlines = fit_lines(d, deck, [11, 10], tw, 2)
        assert len(dlines) <= 2, f"card {num} deck overflows: {dlines}"
        for ln in dlines:
            d.text((tx, ty), ln, font=df, fill=(70, 70, 66))
            ty += 12
        assert ty <= cy + ch + 1, f"card {num} text overflows bottom"

    # ---- bottom section (y 794-984)
    d.line([16, 790, 1008, 790], fill=NAVY, width=2)
    # map (left)
    d.text((16, 796), "WHERE IT HAPPENED", font=SANS_B(13), fill=NAVY)
    d.text((512, 798), "Pins 1-18 match the cards; 12 tracked from NASA JPL",
           font=SANS(10), fill=GREY, anchor="ra")
    mx0, my0, mx1, my1 = 16, 812, 512, 984
    d.rectangle([mx0, my0, mx1, my1], fill=OCEAN, outline=CARD_LINE, width=1)
    scale = min((mx1 - mx0 - 8) / 360.0, (my1 - my0 - 8) / 133.0)
    ox = mx0 + ((mx1 - mx0) - 360 * scale) / 2
    oy = my0 + ((my1 - my0) - 133 * scale) / 2

    def proj(lon, lat):
        return (ox + (lon + 180) * scale, oy + (78 - lat) * scale)

    for lon in range(-150, 181, 30):
        x = ox + (lon + 180) * scale
        d.line([x, my0, x, my1], fill=(190, 210, 218), width=1)
    for lat in (-30, 0, 30, 60):
        _x, y = proj(0, lat)
        d.line([mx0, y, mx1, y], fill=(190, 210, 218), width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # pins
    pin_xy = {}
    for (num, _k, _t, _dk, _key, (lon, lat), (dx, dy)) in CARDS:
        px, py = proj(lon, lat)
        pin_xy[num] = (px, py)
        lx, ly = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.line([px, py, lx, ly], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([lx - 7, ly - 7, lx + 7, ly + 7], fill=RED,
                  outline=WHITE, width=1)
        d.text((lx, ly), str(num), font=SANS_B(8), fill=WHITE, anchor="mm")

    # list 19-48 (right), two columns
    lx0 = 520
    d.text((lx0, 796), "ALSO ON TUESDAY 17 NOVEMBER", font=SANS_B(13),
           fill=NAVY)
    d.text((1008, 798), "19-48", font=SANS_B(11), fill=RED, anchor="ra")
    col_w = 244
    bf = SANS(10)
    ly = 816
    for i, item in enumerate(BRIEFS):
        col = i // 15
        row = i % 15
        bx = lx0 + col * col_w
        by = ly + row * 11
        text = f"{19 + i}  {item}"
        assert d.textlength(text, font=bf) <= col_w - 2, f"brief {19+i} too long"
        d.text((bx, by), f"{19 + i}", font=SANS_B(10), fill=RED)
        d.text((bx + 22, by), item, font=bf, fill=INK)
    d.text((lx0, 984), "", font=bf, fill=INK)

    # ---- footer (985-1024)
    d.line([16, 988, 1008, 988], fill=CARD_LINE, width=1)
    d.text((512, 997),
           "Every story here happened or was first reported on Tuesday 17 November 2026. Disputed claims are attributed.",
           font=SANS(10), fill=GREY, anchor="ma")
    d.text((512, 1012),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN News. Original drawings.",
           font=SANS(10), fill=GREY, anchor="ma")

    img.save(out_path, "PNG")
    return img

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print("wrote", out)
