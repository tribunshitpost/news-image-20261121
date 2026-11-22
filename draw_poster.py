#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news poster: one 1024x1024 PNG.

A newspaper front page on a deep midnight-blue ground. The lead story is
the double-tap missile strike on Kryvyi Rih; below it, the capture of
"El Chapo Isidro" in Mexico and the COP31 talks running into overtime;
then the AI market rout, BepiColombo reaching Mercury, and the Peru quake.
Every fact on the poster was reported on Saturday 21 November 2026.

Deterministic: no clock, no randomness, no network. Drawing the poster
twice produces byte-identical output.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
REG = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731

# Palette: midnight ground, cream paper, one red lead accent, gold numbers.
INK = (13, 27, 46)
INK_SOFT = (21, 41, 66)
PAPER = (247, 242, 231)
PAPER_DIM = (233, 227, 211)
RED = (176, 32, 32)
RED_SOFT = (214, 74, 74)
GOLD = (203, 164, 42)
GOLD_SOFT = (232, 196, 96)
TEAL = (13, 110, 102)
GREEN = (46, 110, 58)
PURPLE = (86, 58, 148)
AMBER = (172, 104, 8)
BLUE = (29, 78, 137)
DARK = (24, 32, 44)
MUTED = (96, 102, 114)
CREAM = (247, 242, 231)
FAINT = (168, 178, 192)
SAND = (222, 205, 164)
SEA = (64, 110, 148)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def card(draw, x, y, w, h, accent):
    """A cream story card with a coloured top bar and a soft edge."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PAPER)
    draw.rounded_rectangle([x, y, x + w, y + 9], radius=4, fill=accent)
    draw.rectangle([x, y + 5, x + w, y + 9], fill=accent)


def tagline(draw, x, y, text, color):
    draw.text((x, y), text, font=BOLD(14), fill=color)
    return y + 22


def headline(draw, x, y, text, max_w, size=21, leading=26):
    fnt = BOLD(size)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=DARK)
        y += leading
    return y


def body(draw, x, y, text, max_w, size=15, leading=21):
    return para(draw, x, y, text, REG(size), DARK, max_w, leading)


def star(draw, cx, cy, r, color):
    """A five-point star centred on (cx, cy)."""
    import math

    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)


def draw_header(draw):
    draw.text((28, 34), "THE WORLD IN ONE DAY", font=BOLD(42), fill=CREAM)
    draw.text((28, 88), "ONE DAY  ·  ONE IMAGE  ·  WORLD NEWS",
              font=BOLD(14), fill=GOLD_SOFT)
    draw.text((1024 - 28, 30), "SATURDAY", font=BOLD(22), fill=GOLD,
              anchor="ra")
    draw.text((1024 - 28, 58), "21 NOVEMBER 2026", font=BOLD(26),
              fill=CREAM, anchor="ra")
    draw.text((1024 - 28, 92), "FRONT PAGE", font=BOLD(13), fill=FAINT,
              anchor="ra")
    draw.line([(28, 128), (996, 128)], fill=GOLD, width=3)


def draw_map(draw, x, y, w, h):
    """Stylised map of Ukraine and its neighbours inside a panel."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=INK_SOFT)
    # Neighbour strips: Poland to the west, Russia to the east.
    draw.rectangle([x, y + 30, x + 34, y + h - 46], fill=(52, 68, 92))
    draw.rectangle([x + w - 40, y + 24, x + w, y + h - 52], fill=(92, 58, 58))
    draw.text((x + 30, y + h - 40), "POLAND", font=BOLD(10),
              fill=(196, 204, 216), anchor="ma")
    draw.text((x + w - 48, y + h - 40), "RUSSIA", font=BOLD(10),
              fill=(232, 196, 196), anchor="ma")
    # Ukraine landmass, drawn as a simplified polygon.
    land = [
        (x + 58, y + 62), (x + 96, y + 34), (x + 150, y + 26),
        (x + 205, y + 30), (x + 248, y + 48), (x + 262, y + 78),
        (x + 252, y + 112), (x + 232, y + 132), (x + 226, y + 158),
        (x + 196, y + 176), (x + 160, y + 186), (x + 128, y + 178),
        (x + 96, y + 158), (x + 66, y + 132), (x + 52, y + 96),
    ]
    draw.polygon(land, fill=SAND)
    # Black Sea along the southern edge.
    sea = [
        (x + 128, y + 186), (x + 168, y + 196), (x + 214, y + 190),
        (x + 252, y + 204), (x + 258, y + h - 14), (x + 120, y + h - 14),
        (x + 118, y + 206),
    ]
    draw.polygon(sea, fill=SEA)
    draw.text((x + 190, y + h - 34), "BLACK SEA", font=BOLD(10),
              fill=(214, 228, 240), anchor="ma")
    # Dnipro river running down to the sea.
    draw.line([(x + 168, y + 40), (x + 172, y + 96), (x + 160, y + 150),
               (x + 168, y + 196)], fill=(120, 150, 180), width=3)
    # Missile arcs sweeping in from the east.
    for (ax, ay, bx, by) in [
        (x + w - 6, y + 44, x + 168, y + 132),
        (x + w - 6, y + 78, x + 182, y + 150),
        (x + w - 6, y + 112, x + 158, y + 118),
    ]:
        mx, my = (ax + bx) // 2, min(ay, by) - 34
        pts = []
        for t in range(21):
            u = t / 20
            px = (1 - u) ** 2 * ax + 2 * (1 - u) * u * mx + u * u * bx
            py = (1 - u) ** 2 * ay + 2 * (1 - u) * u * my + u * u * by
            pts.append((px, py))
        draw.line(pts, fill=RED_SOFT, width=2)
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=RED)
    # Kyiv in the north, Kryvyi Rih starred in the south-centre.
    draw.ellipse([x + 148 - 4, y + 58 - 4, x + 148 + 4, y + 58 + 4],
                 fill=DARK)
    draw.text((x + 148, y + 40), "KYIV", font=BOLD(11), fill=CREAM,
              anchor="ma")
    star(draw, x + 172, y + 142, 13, GOLD)
    draw.text((x + 172, y + 162), "KRYVYI RIH", font=BOLD(11), fill=CREAM,
              anchor="ma")
    draw.text((x + 12, y + 8), "STYLISED MAP — UKRAINE", font=BOLD(10),
              fill=FAINT)


def draw_lead(draw):
    x, y, w, h = 28, 146, 968, 322
    card(draw, x, y, w, h, RED)
    tx = x + 26
    ty = tagline(draw, tx, y + 24, "LEAD STORY  ·  UKRAINE", RED)
    ty = headline(draw, tx, ty + 2,
                  "DOUBLE-TAP STRIKE HITS ZELENSKYY'S HOMETOWN",
                  596, size=30, leading=36)
    ty = body(draw, tx, ty + 10,
              "Russian ballistic missiles hit Kryvyi Rih on Friday night — "
              "then more struck as rescuers arrived. A 7-year-old boy and a "
              "20-year-old paramedic were killed; 60 people were wounded, "
              "six of them children.", 596)
    ty = body(draw, tx, ty + 8,
              "About 25 apartment blocks, a hospital and schools were "
              "damaged. Overnight, Russia fired 3 missiles and 148 drones "
              "at Ukraine; air defences shot down 117 of them.", 596)
    draw.line([(tx, ty + 12), (tx + 596, ty + 12)], fill=(196, 188, 168),
              width=1)
    draw.text((tx, ty + 22), "HOURS AFTER THE WAR'S BIGGEST NOVEMBER "
              "BARRAGE SPILLED INTO POLAND", font=BOLD(12), fill=MUTED)
    draw_map(draw, x + 648, y + 22, 294, 278)


def draw_middle(draw):
    y, h = 484, 216
    # Mexico: the cartel boss captured.
    x, w = 28, 478
    card(draw, x, y, w, h, TEAL)
    ty = tagline(draw, x + 24, y + 22, "MEXICO  ·  CARTELS", TEAL)
    ty = headline(draw, x + 24, ty + 2,
                  "FBI'S MOST-WANTED “EL CHAPO ISIDRO” CAPTURED",
                  w - 48, size=21, leading=26)
    body(draw, x + 24, ty + 8,
         "Fausto Isidro Meza Flores was seized in Sinaloa on Friday night "
         "with US intelligence help. Two other cartel leaders were taken "
         "too — and gunmen answered with flaming roadblocks.",
         w - 48)
    # COP31: the climate talks run over.
    x = 518
    card(draw, x, y, w, h, GREEN)
    ty = tagline(draw, x + 24, y + 22, "CLIMATE  ·  COP31", GREEN)
    ty = headline(draw, x + 24, ty + 2,
                  "CLIMATE TALKS RUN INTO OVERTIME — NO DEAL YET",
                  w - 48, size=21, leading=26)
    body(draw, x + 24, ty + 8,
         "Negotiators in Antalya blew past their Friday deadline. The draft "
         "drops any fossil-fuel phase-out and a $120bn adaptation fund. "
         "The EU warns: a good deal, or none at all.",
         w - 48)


def draw_bottom(draw):
    y, h, w, gap = 716, 192, 312, 16
    # Markets: the AI rout.
    x = 28
    card(draw, x, y, w, h, RED)
    ty = tagline(draw, x + 20, y + 20, "MARKETS  ·  AI ROUT", RED)
    ty = headline(draw, x + 20, ty + 2,
                  "STOCKS TUMBLE AS THE AI RALLY CRACKS",
                  w - 40, size=19, leading=24)
    body(draw, x + 20, ty + 8,
         "S&P 500 −3.7%, into correction. Nasdaq −5.28%, wiping out its "
         "2026 gains. Nikkei −5.06%. Chip shares −10.7%.",
         w - 40, size=14, leading=20)
    # Space: BepiColombo at Mercury.
    x = 28 + w + gap
    card(draw, x, y, w, h, PURPLE)
    ty = tagline(draw, x + 20, y + 20, "SPACE  ·  MERCURY", PURPLE)
    ty = headline(draw, x + 20, ty + 2,
                  "BEPICOLOMBO ARRIVES AT MERCURY",
                  w - 40, size=19, leading=24)
    body(draw, x + 20, ty + 8,
         "After an eight-year journey, ESA and JAXA's twin probes enter "
         "orbit — only the second mission ever to circle the innermost "
         "planet.",
         w - 40, size=14, leading=20)
    # Peru: the Andes quake.
    x = 28 + 2 * (w + gap)
    card(draw, x, y, w, h, AMBER)
    ty = tagline(draw, x + 20, y + 20, "EARTHQUAKE  ·  PERU", AMBER)
    ty = headline(draw, x + 20, ty + 2,
                  "M6.7 QUAKE SHAKES THE ANDES",
                  w - 40, size=19, leading=24)
    body(draw, x + 20, ty + 8,
         "A deep quake near Junín was felt in Lima on Friday night. No "
         "damage or casualties were reported.",
         w - 40, size=14, leading=20)


def draw_numbers(draw):
    y = 924
    draw.rounded_rectangle([28, y, 996, y + 44], radius=8, fill=INK_SOFT)
    label = "BY THE NUMBERS"
    draw.text((48, y + 12), label, font=BOLD(15), fill=GOLD)
    stats = "2 killed  ·  60 wounded  ·  148 drones  ·  S&P −3.7%  ·  " \
            "Nasdaq −5.28%  ·  M6.7  ·  8 yrs to Mercury"
    lx = 48 + draw.textlength(label, font=BOLD(15)) + 26
    draw.text((lx, y + 12), stats, font=BOLD(14), fill=CREAM)


def draw_footer(draw):
    draw.text((28, 982),
              "ALSO: Trump weighs new Iran strikes  ·  Russian cargo ship "
              "hit by drones in the Baltic  ·  Dengue cut 69% in Brazil  ·  "
              "UN talks on AI weapons",
              font=REG(12), fill=FAINT)
    draw.text((28, 1002),
              "Sources: AP · Reuters · CNN · Nature · ESA · USGS · NYT — All "
              "events happened, or were first reported, on Saturday "
              "21 November 2026.",
              font=REG(12), fill=FAINT)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "/output"
    os.makedirs(out_dir, exist_ok=True)
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_lead(draw)
    draw_middle(draw)
    draw_bottom(draw)
    draw_numbers(draw)
    draw_footer(draw)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")
    print("wrote", os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
