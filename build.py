#!/usr/bin/env python3
"""Build the news-image-20261117 round-2 front page.

Draws a 1024x1024 illustrated front page for Tuesday 17 November 2026
with PIL, from a fresh design: masthead, 3 illustrated leads, a numbered
world map, 9 illustrated story cards, a 30-item numbered brief list and
an honesty footer. Deterministic: no network, no randomness, no clock.
Run:  python3 build.py   -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# ---- palette: dark red + cream identity, own composition ----
CREAM = (247, 240, 220)
PAPER = (252, 248, 236)
CARD = (255, 252, 244)
INK = (34, 30, 26)
RED = (139, 26, 26)
RED2 = (178, 34, 34)
GOLD = (176, 141, 60)
BLUE = (38, 84, 124)
TEAL = (42, 110, 110)
GREEN = (74, 120, 66)
OLIVE = (120, 118, 70)
SEA = (198, 220, 230)
LAND = (216, 198, 152)
LAND2 = (205, 190, 140)
GREY = (110, 104, 92)
WHITE = (255, 255, 255)
SKY = (186, 214, 232)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, f, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def fit_text(draw, s, f, max_w, max_lines):
    """Wrap text to at most max_lines; hard-fail loudly if it cannot fit."""
    lines = wrap(draw, s, f, max_w)
    assert len(lines) <= max_lines, "TEXT OVERFLOW %r -> %r" % (s, lines)
    return lines


def rrect(draw, box, rad, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)


# ---- simplified world map (equirectangular lon/lat polygons) ----
NA = [(-168, 65), (-155, 71), (-140, 70), (-130, 71), (-120, 70), (-110, 68),
      (-100, 68), (-90, 70), (-85, 66), (-80, 73), (-75, 72), (-70, 62),
      (-65, 60), (-60, 55), (-55, 47), (-60, 46), (-65, 44), (-70, 42),
      (-75, 35), (-80, 32), (-81, 26), (-85, 30), (-90, 21), (-95, 17),
      (-97, 16), (-100, 18), (-105, 20), (-110, 24), (-115, 28), (-120, 34),
      (-124, 40), (-124, 48), (-130, 55), (-140, 60), (-150, 60),
      (-160, 58), (-168, 65)]
SA = [(-78, 7), (-75, 10), (-72, 12), (-68, 11), (-64, 10), (-60, 8),
      (-55, 6), (-52, 5), (-50, 0), (-48, -3), (-44, -3), (-40, -5),
      (-37, -8), (-35, -9), (-35, -13), (-38, -17), (-40, -22), (-45, -24),
      (-48, -27), (-52, -32), (-55, -35), (-58, -38), (-62, -41), (-65, -45),
      (-68, -50), (-68, -54), (-70, -52), (-72, -47), (-73, -40), (-73, -33),
      (-71, -28), (-70, -22), (-72, -18), (-75, -15), (-78, -10), (-80, -6),
      (-81, -3), (-79, 1), (-78, 7)]
AF = [(-17, 15), (-15, 20), (-12, 25), (-9, 30), (-6, 33), (-1, 35), (3, 37),
      (8, 37), (11, 34), (15, 32), (20, 32), (25, 31), (30, 31), (32, 29),
      (34, 28), (36, 24), (38, 20), (39, 15), (41, 11), (44, 11), (48, 11),
      (51, 12), (50, 8), (46, 4), (42, 0), (40, -4), (39, -8), (37, -12),
      (36, -18), (33, -25), (30, -30), (26, -34), (20, -35), (17, -32),
      (14, -28), (13, -22), (12, -17), (12, -12), (9, -4), (9, 1), (6, 4),
      (0, 5), (-6, 5), (-10, 6), (-13, 8), (-16, 12), (-17, 15)]
EU = [(-9, 37), (-9, 43), (-5, 44), (-2, 44), (-1, 46), (-3, 48), (-1, 49),
      (2, 51), (4, 53), (7, 55), (8, 57), (10, 58), (12, 58), (10, 59),
      (7, 60), (5, 61), (5, 63), (8, 64), (12, 65), (15, 66), (18, 69),
      (22, 70), (26, 71), (30, 70), (32, 70), (35, 68), (38, 68), (40, 67),
      (43, 66), (45, 65), (44, 62), (42, 60), (40, 58), (38, 56), (36, 54),
      (35, 52), (33, 50), (32, 48), (30, 46), (28, 45), (26, 44), (23, 42),
      (22, 40), (20, 40), (18, 42), (16, 44), (13, 45), (10, 44), (8, 44),
      (6, 43), (3, 42), (1, 40), (-1, 38), (-3, 36), (-6, 36), (-9, 37)]
AS = [(28, 70), (35, 70), (42, 69), (50, 69), (58, 69), (66, 70), (74, 72),
      (82, 73), (90, 74), (98, 76), (106, 77), (114, 76), (122, 74),
      (130, 72), (138, 72), (146, 71), (154, 70), (160, 69), (162, 66),
      (160, 60), (156, 55), (152, 58), (148, 59), (143, 58), (141, 52),
      (140, 47), (138, 42), (136, 37), (134, 34), (131, 33), (129, 32),
      (127, 34), (126, 37), (124, 39), (122, 40), (120, 37), (118, 32),
      (116, 28), (113, 22), (110, 20), (108, 17), (106, 14), (104, 10),
      (103, 7), (100, 6), (98, 10), (97, 14), (94, 17), (92, 20), (89, 22),
      (86, 20), (83, 17), (80, 14), (78, 9), (76, 10), (74, 14), (72, 19),
      (70, 21), (67, 24), (64, 25), (61, 25), (58, 26), (56, 27), (54, 27),
      (52, 26), (50, 29), (48, 30), (47, 31), (45, 32), (43, 30), (41, 28),
      (39, 24), (37, 20), (36, 18), (35, 22), (34, 27), (33, 29), (32, 31),
      (31, 33), (30, 36), (30, 38), (29, 41), (28, 44), (28, 48), (28, 52),
      (28, 56), (28, 60), (28, 64), (28, 68), (28, 70)]
AU = [(113, -22), (114, -30), (115, -33), (118, -35), (122, -34), (124, -33),
      (126, -32), (129, -32), (132, -32), (134, -33), (136, -35), (138, -35),
      (140, -38), (142, -38), (145, -38), (147, -39), (150, -37), (150, -34),
      (152, -31), (153, -27), (153, -24), (150, -22), (147, -19), (144, -15),
      (142, -11), (141, -13), (139, -15), (136, -15), (135, -12), (133, -12),
      (131, -12), (129, -14), (127, -14), (125, -14), (123, -16), (121, -19),
      (119, -20), (117, -21), (115, -21), (113, -22)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-2, 50), (-5, 50)]
JP = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
      (141, 39), (141, 41), (141, 43), (142, 44), (143, 42), (141, 40),
      (140, 38), (139, 37), (137, 36), (135, 34), (133, 34), (131, 33),
      (130, 31)]
IDN = [(95, 5), (98, 3), (100, 0), (102, -3), (105, -5), (108, -7),
       (110, -7), (113, -7), (115, -8), (117, -8), (119, -9), (120, -10),
       (122, -9), (124, -10), (126, -9), (128, -8), (130, -7), (131, -3),
       (132, -1), (134, -2), (136, -3), (138, -4), (140, -5), (141, -6),
       (140, -8), (138, -8), (136, -7), (134, -5), (132, -4), (130, -3),
       (128, -2), (126, -1), (124, 0), (122, 1), (120, 1), (118, 0),
       (116, -1), (114, -3), (112, -4), (110, -6), (108, -7), (106, -6),
       (104, -5), (102, -4), (100, -2), (98, 0), (96, 3), (95, 5)]
NZ = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
      (175, -40), (173, -42), (170, -44), (167, -45)]

CONTINENTS = [AS, NA, SA, AF, EU, AU, UK, JP, IDN, NZ]

# pins: (number, lon, lat, nudge_dx, nudge_dy) on the map
PINS = [
    (1, 33.5, 45.2, 14, -16),   # Kerch Bridge
    (2, 51.5, 26.5, 0, -10),   # Gulf / Bahrain
    (3, 121.0, 14.6, 0, 0),    # Manila
    (4, 23.0, -2.0, 0, 0),     # DR Congo
    (5, 30.7, 36.9, -12, 14),  # Antalya
    (6, -100.0, 39.5, 0, 0),   # USA measles
    (7, -122.0, 37.4, 0, 0),   # Nvidia, California
    (8, 34.5, 31.4, 14, 12),   # Gaza
    (9, 106.0, 47.0, 0, 0),    # Mongolia
    (10, 20.5, 44.8, -26, -16),  # Serbia
    (11, 90.4, 23.8, 6, 6),    # Bangladesh
    (12, 87.0, 55.4, 0, -6),   # Kemerovo
]

# ---- flat-vector illustrations (all drawn here, original) ----
def _canvas(w, h, bg):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def _sun(d, x, y, r, col=(232, 178, 60)):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=(200, 140, 40), width=2)
    for a in range(0, 360, 45):
        import math
        x2 = x + (r + 8) * math.cos(math.radians(a))
        y2 = y + (r + 8) * math.sin(math.radians(a))
        x3 = x + (r + 14) * math.cos(math.radians(a))
        y3 = y + (r + 14) * math.sin(math.radians(a))
        d.line([x2, y2, x3, y3], fill=col, width=3)


def ill_kerch(w, h):
    img, d = _canvas(w, h, (233, 196, 140))
    d.rectangle([0, 0, w, int(h * 0.55)], fill=(243, 214, 160))
    d.rectangle([0, int(h * 0.55), w, h], fill=(52, 96, 128))
    for i in range(5):
        d.line([0, int(h * 0.60) + i * 7, w, int(h * 0.60) + i * 7],
               fill=(70, 118, 148), width=2)
    _sun(d, int(w * 0.84), int(h * 0.22), 13)
    # bridge deck, broken in the middle
    deck_y = int(h * 0.52)
    d.rectangle([0, deck_y, int(w * 0.42), deck_y + 8], fill=(90, 60, 50))
    d.rectangle([int(w * 0.58), deck_y, w, deck_y + 8], fill=(90, 60, 50))
    # falling middle span, tilted
    d.polygon([(int(w * 0.44), deck_y + 2), (int(w * 0.56), deck_y + 2),
               (int(w * 0.54), deck_y + 26), (int(w * 0.46), deck_y + 26)],
              fill=(120, 80, 64))
    # towers
    for tx in (int(w * 0.18), int(w * 0.78)):
        d.rectangle([tx - 3, int(h * 0.20), tx + 3, deck_y], fill=(70, 48, 42))
        d.line([tx, int(h * 0.20), int(w * 0.42), deck_y], fill=(70, 48, 42), width=2)
        d.line([tx, int(h * 0.20), 0, deck_y], fill=(70, 48, 42), width=2)
    # smoke + blast star at the break
    cx, cy = int(w * 0.50), int(h * 0.34)
    for ox, oy, r in ((-14, 6, 12), (0, -4, 15), (14, 6, 12)):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=(120, 118, 112))
    d.polygon([(cx, cy - 16), (cx + 5, cy - 5), (cx + 16, cy - 3), (cx + 6, cy + 4),
               (cx + 9, cy + 15), (cx, cy + 8), (cx - 9, cy + 15), (cx - 6, cy + 4),
               (cx - 16, cy - 3), (cx - 5, cy - 5)], fill=(232, 150, 40))
    # water line + small boat
    d.polygon([(int(w * 0.08), int(h * 0.82)), (int(w * 0.16), int(h * 0.82)),
               (int(w * 0.14), int(h * 0.88)), (int(w * 0.10), int(h * 0.88))],
              fill=(240, 230, 210))
    return img


def ill_gulf(w, h):
    img, d = _canvas(w, h, (168, 205, 210))
    d.rectangle([0, 0, w, int(h * 0.30)], fill=(238, 222, 180))
    d.polygon([(0, int(h * 0.30)), (w, int(h * 0.22)), (w, 0), (0, 0)],
              fill=(222, 200, 150))
    d.rectangle([0, int(h * 0.30), w, h], fill=(38, 110, 130))
    for i in range(4):
        d.line([0, int(h * 0.42) + i * 12, w, int(h * 0.42) + i * 12],
               fill=(60, 132, 150), width=2)
    _sun(d, int(w * 0.12), int(h * 0.18), 12)
    # tanker
    bx, by = int(w * 0.12), int(h * 0.62)
    d.polygon([(bx, by), (bx + 110, by), (bx + 98, by + 20), (bx + 10, by + 20)],
              fill=(139, 26, 26))
    for i, c in enumerate([(240, 200, 80), (60, 120, 90), (240, 240, 240)]):
        d.rectangle([bx + 12 + i * 34, by - 18, bx + 42 + i * 34, by - 2], fill=c,
                    outline=INK, width=1)
    d.rectangle([bx + 96, by - 26, bx + 108, by - 2], fill=(60, 60, 60))
    # island with radar dish (Bahrain)
    ix, iy = int(w * 0.74), int(h * 0.55)
    d.polygon([(ix - 42, iy + 26), (ix + 42, iy + 26), (ix + 26, iy),
               (ix - 26, iy)], fill=(222, 200, 150))
    d.line([ix, iy, ix, iy - 26], fill=INK, width=3)
    d.pieslice([ix - 20, iy - 46, ix + 20, iy - 6], 180, 360, fill=WHITE,
               outline=INK, width=1)
    # drone with dashed path
    dx, dy = int(w * 0.60), int(h * 0.28)
    for i in range(6):
        d.line([dx - 60 + i * 12, dy - 8 + (i % 2) * 4,
                dx - 52 + i * 12, dy - 8 + ((i + 1) % 2) * 4],
               fill=(60, 60, 60), width=2)
    d.ellipse([dx - 7, dy - 4, dx + 7, dy + 4], fill=(40, 40, 40))
    d.line([dx - 14, dy - 8, dx + 14, dy - 8], fill=(40, 40, 40), width=2)
    d.line([dx - 14, dy + 8, dx + 14, dy + 8], fill=(40, 40, 40), width=2)
    return img


def ill_quad(w, h):
    img, d = _canvas(w, h, (176, 206, 226))
    _sun(d, int(w * 0.86), int(h * 0.20), 12)
    # skyline silhouettes
    base = int(h * 0.86)
    towers = [(0.02, 0.42), (0.14, 0.62), (0.28, 0.50), (0.40, 0.72),
              (0.54, 0.55), (0.66, 0.80), (0.80, 0.60), (0.92, 0.45)]
    for fx, fh in towers:
        x0 = int(w * fx)
        d.rectangle([x0, base - int(h * fh), x0 + int(w * 0.11), base],
                    fill=(52, 78, 110))
    d.polygon([(int(w * 0.66), base - int(h * 0.80)), (int(w * 0.715), base - int(h * 0.80)),
               (int(w * 0.6875), base - int(h * 0.94))], fill=(52, 78, 110))
    d.rectangle([0, base, w, h], fill=(38, 84, 124))
    # four small flags on poles
    flags = [
        ([(232, 60, 60), (255, 255, 255), (232, 60, 60)], (38, 84, 150)),
        ([(255, 255, 255)], (200, 40, 40)),
        ([(232, 140, 40), (255, 255, 255), (40, 130, 70)], (30, 90, 160)),
        ([(30, 60, 140)], (232, 200, 60)),
    ]
    for i, (stripes, dot) in enumerate(flags):
        fx = int(w * (0.10 + i * 0.22))
        fy = int(h * 0.30)
        d.line([fx, fy, fx, fy + 34], fill=INK, width=2)
        fw, fh = 30, 18
        for j, c in enumerate(stripes):
            d.rectangle([fx, fy + j * fh // len(stripes), fx + fw,
                         fy + (j + 1) * fh // len(stripes)], fill=c)
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)
        d.ellipse([fx + fw // 2 - 3, fy + fh // 2 - 3, fx + fw // 2 + 3, fy + fh // 2 + 3],
                  fill=dot)
    # plane
    px, py = int(w * 0.62), int(h * 0.16)
    d.polygon([(px, py), (px + 46, py + 6), (px, py + 10), (px + 8, py + 5)],
              fill=(255, 255, 255))
    d.polygon([(px + 12, py + 2), (px + 22, py - 6), (px + 26, py + 2)],
              fill=(255, 255, 255))
    return img


def _virus(d, cx, cy, r, col):
    for a in range(0, 360, 30):
        import math
        x2 = cx + (r + 7) * math.cos(math.radians(a))
        y2 = cy + (r + 7) * math.sin(math.radians(a))
        d.line([cx, cy, x2, y2], fill=col, width=2)
        d.ellipse([x2 - 2, y2 - 2, x2 + 2, y2 + 2], fill=col)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
              outline=(90, 20, 20), width=2)
    d.ellipse([cx - r // 2, cy - r // 2, cx - r // 5, cy - r // 5],
              fill=(255, 255, 255))


def ill_ebola(w, h):
    img, d = _canvas(w, h, (214, 232, 204))
    d.rectangle([0, int(h * 0.72), w, h], fill=(140, 168, 110))
    # clinic building
    d.rectangle([int(w * 0.08), int(h * 0.34), int(w * 0.58), int(h * 0.74)],
                fill=(255, 255, 255), outline=INK, width=2)
    d.polygon([(int(w * 0.04), int(h * 0.34)), (int(w * 0.33), int(h * 0.16)),
               (int(w * 0.62), int(h * 0.34))], fill=(139, 26, 26))
    d.rectangle([int(w * 0.28), int(h * 0.55), int(w * 0.38), int(h * 0.74)],
                fill=(90, 120, 150), outline=INK, width=1)
    d.rectangle([int(w * 0.14), int(h * 0.42), int(w * 0.22), int(h * 0.50)],
                fill=(170, 205, 225), outline=INK, width=1)
    d.rectangle([int(w * 0.44), int(h * 0.42), int(w * 0.52), int(h * 0.50)],
                fill=(170, 205, 225), outline=INK, width=1)
    # red cross sign
    cx, cy = int(w * 0.33), int(h * 0.26)
    d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=RED2)
    d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=RED2)
    # tent
    tx = int(w * 0.66)
    d.polygon([(tx, int(h * 0.46)), (tx + 34, int(h * 0.74)), (tx - 34, int(h * 0.74))],
              fill=(232, 220, 180), outline=INK, width=2)
    d.line([tx, int(h * 0.46), tx, int(h * 0.74)], fill=INK, width=1)
    _virus(d, int(w * 0.80), int(h * 0.32), 11, (178, 60, 60))
    return img


def ill_cop31(w, h):
    img, d = _canvas(w, h, (186, 220, 228))
    _sun(d, int(w * 0.16), int(h * 0.20), 11)
    cx, cy, r = int(w * 0.50), int(h * 0.50), 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 130, 180),
              outline=(30, 80, 120), width=2)
    # land blobs
    d.polygon([(cx - 26, cy - 12), (cx - 8, cy - 22), (cx + 2, cy - 8),
               (cx - 12, cy + 2), (cx - 24, cy + 2)], fill=GREEN)
    d.polygon([(cx + 6, cy + 6), (cx + 24, cy + 2), (cx + 26, cy + 16),
               (cx + 10, cy + 22), (cx + 2, cy + 14)], fill=GREEN)
    d.ellipse([cx - 30, cy - 6, cx - 18, cy + 8], fill=GREEN)
    # latitude lines
    for dy in (-16, 0, 16):
        d.arc([cx - r, cy - r + dy, cx + r, cy + r + dy], 0, 360,
              fill=(120, 180, 210), width=1)
    # leaf
    lx, ly = int(w * 0.80), int(h * 0.74)
    d.polygon([(lx - 16, ly + 10), (lx + 2, ly - 14), (lx + 18, ly + 8),
               (lx + 2, ly + 14)], fill=(74, 140, 66), outline=(50, 100, 50))
    d.line([lx - 14, ly + 8, lx + 2, ly - 12], fill=(50, 100, 50), width=2)
    return img


def ill_measles(w, h):
    img, d = _canvas(w, h, (250, 240, 214))
    # three flags: US, Mexico, Bolivia
    def flag(x, stripes, dot=None):
        fy = int(h * 0.22)
        d.line([x, fy, x, fy + 40], fill=INK, width=2)
        fw, fh = 34, 20
        for j, c in enumerate(stripes):
            d.rectangle([x, fy + j * fh // len(stripes), x + fw,
                         fy + (j + 1) * fh // len(stripes)], fill=c)
        d.rectangle([x, fy, x + fw, fy + fh], outline=INK, width=1)
        if dot:
            d.ellipse([x + fw // 2 - 3, fy + fh // 2 - 3, x + fw // 2 + 3,
                       fy + fh // 2 + 3], fill=dot)
    flag(int(w * 0.06), [(200, 40, 40), (255, 255, 255), (200, 40, 40)],
         (38, 84, 150))
    flag(int(w * 0.38), [(40, 130, 70), (255, 255, 255), (200, 40, 40)],
         (140, 90, 40))
    flag(int(w * 0.70), [(200, 40, 40), (232, 200, 60), (40, 130, 70)])
    # big virus ball
    _virus(d, int(w * 0.52), int(h * 0.72), 15, (178, 60, 60))
    d.rectangle([0, int(h * 0.88), w, h], fill=(120, 140, 110))
    return img


def ill_nvidia(w, h):
    img, d = _canvas(w, h, (22, 34, 52))
    # chip
    cx, cy, s = int(w * 0.34), int(h * 0.52), 26
    for i in range(5):
        d.line([cx - s - 8, cy - s + 8 + i * 10, cx - s, cy - s + 8 + i * 10],
               fill=(232, 200, 60), width=2)
        d.line([cx + s, cy - s + 8 + i * 10, cx + s + 8, cy - s + 8 + i * 10],
               fill=(232, 200, 60), width=2)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(30, 90, 50),
                outline=(232, 200, 60), width=2)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(52, 140, 80), outline=(232, 200, 60), width=1)
    # rising chart
    pts = [(int(w * 0.52), int(h * 0.72)), (int(w * 0.62), int(h * 0.60)),
           (int(w * 0.70), int(h * 0.64)), (int(w * 0.80), int(h * 0.44)),
           (int(w * 0.90), int(h * 0.30))]
    d.line(pts, fill=(90, 220, 120), width=4, joint="curve")
    d.polygon([(int(w * 0.90), int(h * 0.30)), (int(w * 0.82), int(h * 0.30)),
               (int(w * 0.90), int(h * 0.20))], fill=(90, 220, 120))
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.rectangle([int(w * 0.08), int(h * 0.86), int(w * 0.20), int(h * 0.92)],
                fill=(90, 220, 120))
    return img


def ill_gaza(w, h):
    img, d = _canvas(w, h, (238, 224, 186))
    _sun(d, int(w * 0.82), int(h * 0.20), 11)
    d.rectangle([0, int(h * 0.68), w, h], fill=(206, 178, 130))
    # tents
    for tx, ts in ((int(w * 0.14), 1.0), (int(w * 0.52), 0.85)):
        tw, th = int(44 * ts), int(34 * ts)
        d.polygon([(tx, int(h * 0.68) - th), (tx + tw, int(h * 0.68)),
                   (tx - tw, int(h * 0.68))], fill=(232, 222, 190),
                  outline=(120, 100, 70), width=2)
        d.line([tx, int(h * 0.68) - th, tx, int(h * 0.68)], fill=(120, 100, 70),
               width=1)
    # aid boxes
    for bx in (int(w * 0.72), int(w * 0.84)):
        d.rectangle([bx, int(h * 0.72), bx + 20, int(h * 0.88)], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([bx + 8, int(h * 0.76), bx + 12, int(h * 0.84)], fill=RED2)
        d.rectangle([bx + 6, int(h * 0.78), bx + 14, int(h * 0.82)], fill=RED2)
    d.rectangle([int(w * 0.72), int(h * 0.60), int(w * 0.92), int(h * 0.72)],
                fill=(240, 240, 240), outline=INK, width=1)
    d.rectangle([int(w * 0.80), int(h * 0.63), int(w * 0.84), int(h * 0.69)],
                fill=RED2)
    return img


def ill_mongolia(w, h):
    img, d = _canvas(w, h, (178, 208, 232))
    _sun(d, int(w * 0.84), int(h * 0.18), 11)
    # mountains
    d.polygon([(0, int(h * 0.55)), (int(w * 0.22), int(h * 0.30)),
               (int(w * 0.44), int(h * 0.55))], fill=(130, 140, 150))
    d.polygon([(int(w * 0.30), int(h * 0.55)), (int(w * 0.55), int(h * 0.26)),
               (int(w * 0.80), int(h * 0.55))], fill=(110, 122, 132))
    d.polygon([(int(w * 0.62), int(h * 0.55)), (int(w * 0.82), int(h * 0.34)),
               (w, int(h * 0.55))], fill=(130, 140, 150))
    d.rectangle([0, int(h * 0.55), w, h], fill=(110, 160, 90))
    d.rectangle([0, int(h * 0.72), w, h], fill=(200, 170, 80))
    # ger (round tent)
    gx, gy = int(w * 0.34), int(h * 0.66)
    d.polygon([(gx - 34, gy), (gx, gy - 22), (gx + 34, gy)], fill=(232, 220, 200),
              outline=INK, width=2)
    d.rectangle([gx - 34, gy, gx + 34, gy + 22], fill=(250, 244, 228),
                outline=INK, width=2)
    d.rectangle([gx - 7, gy + 4, gx + 7, gy + 22], fill=(200, 120, 50),
                outline=INK, width=1)
    # flag pole
    fx = int(w * 0.80)
    d.line([fx, int(h * 0.30), fx, int(h * 0.78)], fill=INK, width=2)
    for j, c in enumerate([(200, 40, 40), (38, 84, 150), (200, 40, 40)]):
        d.rectangle([fx, int(h * 0.30) + j * 8, fx + 26, int(h * 0.30) + (j + 1) * 8],
                    fill=c)
    d.rectangle([fx, int(h * 0.30), fx + 26, int(h * 0.54)], outline=INK, width=1)
    d.ellipse([fx + 10, int(h * 0.36), fx + 16, int(h * 0.42)], fill=(232, 200, 60))
    return img


def ill_serbia(w, h):
    img, d = _canvas(w, h, (188, 210, 228))
    _sun(d, int(w * 0.86), int(h * 0.18), 10)
    # parliament: base + columns + dome
    bx0, by0, bx1, by1 = int(w * 0.16), int(h * 0.42), int(w * 0.84), int(h * 0.82)
    d.rectangle([bx0, by0, bx1, by1], fill=(240, 232, 210), outline=INK, width=2)
    d.polygon([(int(w * 0.38), by0), (int(w * 0.50), int(h * 0.22)),
               (int(w * 0.62), by0)], fill=(90, 130, 110), outline=INK)
    d.ellipse([int(w * 0.46), int(h * 0.24), int(w * 0.54), int(h * 0.34)],
              fill=(90, 130, 110), outline=INK)
    for i in range(5):
        cx = bx0 + 12 + i * 22
        d.rectangle([cx, by0 + 10, cx + 8, by1 - 8], fill=(200, 190, 160),
                    outline=INK, width=1)
    d.rectangle([bx0 + 8, by1 - 8, bx1 - 8, by1], fill=(120, 110, 90))
    # flag
    fx = int(w * 0.08)
    d.line([fx, int(h * 0.28), fx, int(h * 0.82)], fill=INK, width=2)
    for j, c in enumerate([(200, 40, 40), (38, 84, 150), (255, 255, 255)]):
        d.rectangle([fx, int(h * 0.28) + j * 7, fx + 22, int(h * 0.28) + (j + 1) * 7],
                    fill=c)
    d.rectangle([fx, int(h * 0.28), fx + 22, int(h * 0.49)], outline=INK, width=1)
    # crowd dots
    for i, c in enumerate([(178, 34, 34), (38, 84, 150), (74, 120, 66),
                           (232, 200, 60), (120, 60, 120)]):
        d.ellipse([int(w * 0.30) + i * 16 - 4, int(h * 0.88) - 4,
                   int(w * 0.30) + i * 16 + 4, int(h * 0.88) + 4], fill=c)
    return img


def ill_bangladesh(w, h):
    img, d = _canvas(w, h, (240, 232, 200))
    d.rectangle([0, int(h * 0.70), w, h], fill=(190, 180, 140))
    # factory with sawtooth roof
    d.rectangle([int(w * 0.06), int(h * 0.40), int(w * 0.62), int(h * 0.72)],
                fill=(200, 190, 170), outline=INK, width=2)
    for i in range(3):
        x0 = int(w * 0.06) + i * 30
        d.polygon([(x0, int(h * 0.40)), (x0 + 15, int(h * 0.30)),
                   (x0 + 30, int(h * 0.40))], fill=(150, 140, 120), outline=INK)
    d.rectangle([int(w * 0.66), int(h * 0.22), int(w * 0.74), int(h * 0.72)],
                fill=(170, 90, 70), outline=INK, width=2)
    d.ellipse([int(w * 0.68), int(h * 0.16), int(w * 0.76), int(h * 0.24)],
              fill=(200, 200, 200))
    d.ellipse([int(w * 0.70), int(h * 0.10), int(w * 0.78), int(h * 0.18)],
              fill=(200, 200, 200))
    for i in range(3):
        d.rectangle([int(w * 0.12) + i * 26, int(h * 0.50), int(w * 0.30) + i * 26,
                     int(h * 0.62)], fill=(170, 205, 225), outline=INK, width=1)
    # t-shirt on a line
    d.line([int(w * 0.68), int(h * 0.34), int(w * 0.96), int(h * 0.34)],
           fill=INK, width=2)
    for sx, c in ((int(w * 0.72), (38, 84, 150)), (int(w * 0.84), (178, 34, 34))):
        d.polygon([(sx, int(h * 0.34)), (sx + 6, int(h * 0.34)), (sx + 6, int(h * 0.40)),
                   (sx + 12, int(h * 0.40)), (sx + 12, int(h * 0.56)),
                   (sx - 12, int(h * 0.56)), (sx - 12, int(h * 0.40)),
                   (sx - 6, int(h * 0.40)), (sx - 6, int(h * 0.34))], fill=c,
                  outline=INK)
    # banknote
    d.rectangle([int(w * 0.06), int(h * 0.74), int(w * 0.60), int(h * 0.90)],
                fill=(240, 230, 190), outline=(140, 110, 40), width=2)
    d.text((int(w * 0.10), int(h * 0.77)), "Tk 30,000", font=font(SANS_B, 12),
           fill=(120, 30, 30))
    return img


def ill_crash(w, h):
    img, d = _canvas(w, h, (200, 208, 214))
    # mountains + snow
    d.polygon([(0, int(h * 0.62)), (int(w * 0.26), int(h * 0.30)),
               (int(w * 0.52), int(h * 0.62))], fill=(120, 128, 138))
    d.polygon([(int(w * 0.38), int(h * 0.62)), (int(w * 0.66), int(h * 0.26)),
               (int(w * 0.94), int(h * 0.62))], fill=(100, 110, 120))
    d.polygon([(int(w * 0.60), int(h * 0.34)), (int(w * 0.66), int(h * 0.26)),
               (int(w * 0.72), int(h * 0.34))], fill=(255, 255, 255))
    d.rectangle([0, int(h * 0.62), w, h], fill=(238, 240, 242))
    # tilted plane descending, white with a red tail
    px, py = int(w * 0.40), int(h * 0.36)
    d.polygon([(px - 34, py + 18), (px + 38, py - 14), (px + 44, py - 8),
               (px - 28, py + 24)], fill=(250, 250, 250), outline=INK)
    d.polygon([(px - 8, py + 4), (px + 6, py - 16), (px + 14, py - 12),
               (px + 2, py + 8)], fill=(250, 250, 250), outline=INK)
    d.polygon([(px - 30, py + 20), (px - 16, py + 4), (px - 8, py + 8),
               (px - 22, py + 24)], fill=(250, 250, 250), outline=INK)
    d.polygon([(px + 30, py - 11), (px + 40, py - 15), (px + 44, py - 8),
               (px + 34, py - 5)], fill=(178, 34, 34))
    # smoke column from crash site
    sx, sy = int(w * 0.70), int(h * 0.60)
    for ox, oy, r in ((-8, -12, 9), (0, -22, 11), (8, -32, 10)):
        d.ellipse([sx + ox - r, sy + oy - r, sx + ox + r, sy + oy + r],
                  fill=(140, 140, 138))
    d.polygon([(sx - 14, sy), (sx + 14, sy), (sx + 8, sy - 8), (sx - 8, sy - 8)],
              fill=(232, 150, 40))
    return img


ILLUSTRATIONS = [ill_kerch, ill_gulf, ill_quad, ill_ebola, ill_cop31,
                 ill_measles, ill_nvidia, ill_gaza, ill_mongolia,
                 ill_serbia, ill_bangladesh, ill_crash]

# ---- content: 42 stories, all verified 17 Nov 2026 ----
LEADS = [
    (1, "CRIMEA · UKRAINE WAR", "KERCH BRIDGE DOWN",
     "Second day of strikes closes the Crimea link. Kyiv claims the hit; "
     "Russia hits back at Kyiv's bridges.", ill_kerch),
    (2, "THE GULF · US-IRAN", "US STRIKES IRAN",
     "Qeshm hit in a third attack in five days. Tehran says it struck a "
     "US radar site in Bahrain.", ill_gulf),
    (3, "MANILA · QUAD SUMMIT", "QUAD MEETS, TRUMP FLIES ON",
     "Four leaders warn on export curbs and set patrol flights. Trump "
     "heads to Shenzhen for Xi and Putin.", ill_quad),
]

CARDS = [
    (4, "EBOLA PASSES 11,000 CASES",
     "DR Congo outbreak: 5,400 dead, WHO warns.", ill_ebola),
    (5, "COP31 DRAFT SPLITS TALKS",
     "Antalya: heat plan backed, $20m pledged.", ill_cop31),
    (6, "MEASLES-FREE STATUS LOST",
     "US, Mexico, Bolivia out; US cases pass 5,400.", ill_measles),
    (7, "NVIDIA: $115.8BN QUARTER",
     "Revenue doubles; Huang stays out; Dow -849.", ill_nvidia),
    (8, "GAZA: TENTS AND AID FLOW",
     "Allies urge crossings open; 93,000 tents in.", ill_gaza),
    (9, "MONGOLIA'S PRESIDENT QUITS",
     "The president resigns; Ulaanbaatar awaits a successor.", ill_mongolia),
    (10, "STUDENTS TAKE SERBIA'S HOUSE",
     "Student List sworn in, ending 14 years of Vucic rule.", ill_serbia),
    (11, "TK 30,000 OR NOTHING",
     "Garment workers clash with police in Gazipur.", ill_bangladesh),
    (12, "AN-12 DOWN: 19 KILLED",
     "Russian cargo plane crashes near Kemerovo.", ill_crash),
]

BRIEFS = [
    "Japan scrambles jets as Russian planes intrude",
    "Five EU states plan a Rwanda return hub",
    "Nepal first to tap UN loss-and-damage fund",
    "Mondlane trial opens in Maputo; 5 charges",
    "Sozcu TV seized in dawn raid; trustee in",
    "Tusk survives no-confidence vote, 242-200",
    "Houthis close on Aden; Saudi swaps commander",
    "Russian drone over Chisinau; airspace shut",
    "Haiti backs Bukele troops; 253,700 children at risk",
    "Pentagon fails ninth straight audit",
    "NSA's secret network goes down; no sign of hack",
    "US chip curbs sink SE Asia stocks",
    "Home Depot: $43.4bn sales; McPhail named CEO",
    "Nvidia ends H200 sales in China",
    "Brazil Senate delays fiscal vote to Wednesday",
    "Singapore seeks 'trusted access' to AI chips",
    "World Court to rule Thursday on Rohingya case",
    "Bezos helped cast Pattinson as Bond",
    "Cyclone Xavier hits Category 5; winds 220 km/h",
    "Woman, 72, killed near Jericho; accounts differ",
    "German ZEW jumps to 35.6, beating forecasts",
    "Depardieu drops appeal; sentence stands",
    "Canada-China widen tariff deal after Xi talks",
    "Modi floats Seafarers' Safety Initiative",
    "Cyclone Akvan forms in Bay of Bengal",
    "Seoul scrambles jets as Russian planes near",
    "Japan's economy contracts as spending fades",
    "UK PM sets tests for EU reset before summit",
    "US, Thailand conclude trade deal in Manila",
    "Quad sets first joint patrol flights for 2027",
]
assert len(BRIEFS) == 30


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([4, 4, W - 5, H - 5], outline=RED, width=3)
    d.rectangle([9, 9, W - 10, H - 10], outline=GOLD, width=1)

    # ---------- masthead ----------
    f_kick = font(SANS_B, 13)
    d.text((16, 20), "TUESDAY, 17 NOVEMBER 2026", font=f_kick, fill=RED)
    right = "42 STORIES · 6 CONTINENTS"
    d.text((W - 16 - d.textlength(right, font=f_kick), 20), right,
           font=f_kick, fill=RED)
    f_title = font(SERIF, 54)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 36), title,
           font=f_title, fill=RED)
    f_sub = font(SANS_B, 11)
    sub = "WAR · CLIMATE · MARKETS · POWER — EVERY STORY FROM A SINGLE DAY"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 98), sub,
           font=f_sub, fill=INK)
    d.line([16, 114, W - 16, 114], fill=RED, width=2)
    d.line([16, 118, W - 16, 118], fill=RED, width=1)

    # ---------- 3 illustrated leads ----------
    col_x = [16, 350, 684]
    for i, (num, kick, head, deck, ill) in enumerate(LEADS):
        x = col_x[i]
        art = ill(320, 146)
        img.paste(art, (x, 124))
        d.rectangle([x, 124, x + 319, 269], outline=INK, width=1)
        # number badge on the illustration
        d.rectangle([x + 4, 128, x + 26, 150], fill=RED)
        d.text((x + 15, 139), str(num), font=font(SANS_B, 13), fill=WHITE,
               anchor="mm")
        f_lk = font(SANS_B, 11)
        d.text((x, 278), kick, font=f_lk, fill=RED2)
        f_lh = font(SERIF, 19)
        lines = fit_text(d, head, f_lh, 320, 2)
        draw_lines(d, lines, x, 294, f_lh, INK, 22)
        f_ld = font(SANS, 12)
        lines = fit_text(d, deck, f_ld, 320, 3)
        draw_lines(d, lines, x, 340, f_ld, (60, 56, 50), 15)
    d.line([16, 398, W - 16, 398], fill=(190, 180, 160), width=1)

    # ---------- numbered world map ----------
    f_mh = font(SANS_B, 12)
    d.text((16, 406), "WHERE IT HAPPENED", font=f_mh, fill=RED)
    f_mr = font(SANS, 11)
    mr = "12 numbered stories — find each number on the map"
    d.text((W - 16 - d.textlength(mr, font=f_mr), 407), mr, font=f_mr,
           fill=GREY)
    mx0, my0, mx1, my1 = 16, 428, 1008, 536
    d.rectangle([mx0, my0, mx1, my1], fill=SEA, outline=INK, width=1)

    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                my0 + (78 - lat) / 136 * (my1 - my0))

    # graticule
    for lon in range(-180, 181, 60):
        x, _ = proj(lon, 78)
        d.line([x, my0, x, my1], fill=(170, 195, 205), width=1)
    for lat in range(-60, 79, 30):
        _, y = proj(-180, lat)
        d.line([mx0, y, mx1, y], fill=(170, 195, 205), width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(150, 132, 90))
    # continent labels
    f_lab = font(SANS_B, 8)
    for label, lon, lat in [
            ("NORTH AMERICA", -128, 60), ("SOUTH AMERICA", -58, -18),
            ("AFRICA", 8, -18), ("EUROPE", -8, 62), ("ASIA", 100, 62),
            ("AUSTRALIA", 134, -30), ("PACIFIC", -155, -12)]:
        lx, ly = proj(lon, lat)
        d.text((lx, ly), label, font=f_lab, fill=(96, 88, 66), anchor="mm")
    # pins
    f_pin = font(SANS_B, 11)
    for num, lon, lat, ndx, ndy in PINS:
        tx, ty = proj(lon, lat)
        cx, cy = tx + ndx, ty + ndy
        if ndx or ndy:
            d.line([tx, ty, cx, cy], fill=RED, width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=WHITE, width=1)
        d.text((cx, cy), str(num), font=f_pin, fill=WHITE, anchor="mm")

    # ---------- 9 illustrated cards ----------
    for i, (num, head, deck, ill) in enumerate(CARDS):
        row, col = divmod(i, 3)
        x = col_x[col]
        y = 544 + row * 99
        d.rectangle([x, y, x + 319, y + 91], fill=CARD,
                    outline=(200, 190, 170), width=1)
        art = ill(84, 92)
        img.paste(art, (x, y))
        d.line([x + 84, y, x + 84, y + 91], fill=(200, 190, 170), width=1)
        tx = x + 92
        # number badge
        d.ellipse([tx + 2, y + 8, tx + 18, y + 24], fill=RED)
        d.text((tx + 10, y + 16), str(num), font=font(SANS_B, 10),
               fill=WHITE, anchor="mm")
        f_ch = font(SANS_B, 13)
        lines = fit_text(d, head, f_ch, 196, 2)
        draw_lines(d, lines, tx + 24, y + 6, f_ch, INK, 16)
        f_cd = font(SANS, 11)
        lines = fit_text(d, deck, f_cd, 214, 2)
        draw_lines(d, lines, tx + 4, y + 46, f_cd, (70, 66, 58), 14)

    # ---------- numbered brief list 13-42 ----------
    d.text((16, 844), "ALSO ON TUESDAY 17 NOVEMBER", font=f_mh, fill=RED)
    f_lr = font(SANS, 11)
    lr = "30 more stories, one line each"
    d.text((W - 16 - d.textlength(lr, font=f_lr), 845), lr, font=f_lr,
           fill=GREY)
    d.line([16, 864, W - 16, 864], fill=RED, width=1)
    for i, text in enumerate(BRIEFS):
        col, row = divmod(i, 10)
        x = col_x[col]
        y = 872 + row * 11
        num = str(13 + i) + "."
        f_bn = font(SANS_B, 10)
        d.text((x, y), num, font=f_bn, fill=RED2)
        nx = x + d.textlength(num, font=f_bn) + 4
        f_bt = font(SANS, 10)
        # shrink only if the line would overflow the column
        if d.textlength(text, font=f_bt) > (x + 320 - nx):
            f_bt = font(SANS, 9)
        assert d.textlength(text, font=f_bt) <= (x + 320 - nx), \
            "BRIEF OVERFLOW %r" % text
        d.text((nx, y), text, font=f_bt, fill=INK)

    # ---------- honesty footer ----------
    d.line([16, 988, W - 16, 988], fill=RED, width=1)
    f_f1 = font(SANS, 10)
    f1 = ("Every story here happened or was first reported on Tuesday "
          "17 November 2026. Disputed claims are attributed to their source.")
    d.text(((W - d.textlength(f1, font=f_f1)) / 2, 994), f1, font=f_f1,
           fill=INK)
    f_f2 = font(SANS_B, 9)
    f2 = ("SOURCES: REUTERS · AP · AFP · BBC · AL JAZEERA · UN NEWS · WHO · "
          "IPC · ZEW · METSERVICE")
    d.text(((W - d.textlength(f2, font=f_f2)) / 2, 1007), f2, font=f_f2,
           fill=GREY)
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    assert img.size == (1024, 1024), img.size
    assert size <= 1048576, size
    print("wrote %s %d bytes" % (out, size))


if __name__ == "__main__":
    main()
