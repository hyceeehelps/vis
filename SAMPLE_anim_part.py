"""Ep.12 Part 1/3: The 335 Years' War -- declaration scenes (1651), clipart mode."""
import sys, math
sys.path.insert(0, '/home/user')
from PIL import ImageFont
from clipart_engine import (W, H, INK, person, barrel, tent, fire, bottle, flag,
                            river, moon, stars, burst, groundline, wline, disk,
                            wpoly, horse, cannon, sea, ship, island, gull)

TXTF = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
DUTCH = ((216, 62, 62), (250, 250, 248), (72, 92, 170))
MERCH = (160, 128, 88)
ROY = (92, 68, 52)

def text(d, x, y, txt, size, col=INK, stroke=(255, 255, 255)):
    fnt = ImageFont.truetype(TXTF, size)
    d.text((x, y), txt, font=fnt, fill=col, anchor='mm', stroke_width=4,
           stroke_fill=stroke)

# S1 - 1651: the islands ----------------------------------------------------------------
def s1(d, f, n, t):
    sea(d, 1620, 320, f, 701)
    island(d, 950, 1500, 250, f, 702)
    ship(d, 400, 1500, 160, f, 703, bands=DUTCH)
    ship(d, 780, 1530, 100, f, 704, hull=ROY, sailcol=(238, 234, 224), masts=1)

# S2 - royalist fleet flees to Scilly ----------------------------------------------------
def s2(d, f, n, t):
    disk(d, 220, 420, 130, (226, 226, 230), INK, 5, 2.6, 710, f, ry=60)
    disk(d, 700, 360, 100, (232, 232, 236), INK, 5, 2.2, 711, f, ry=48)
    sea(d, 1600, 300, f, 712)
    island(d, 1060, 1520, 200, f, 713)
    for i, (x, y, s) in enumerate(((230, 1510, 95), (480, 1540, 110), (700, 1480, 85))):
        ship(d, x + f * 1.2 % 60 - 30, y, s, f, 714 + i, hull=ROY, masts=1)

# S3 - right in the shipping lanes --------------------------------------------------------
def s3(d, f, n, t):
    sea(d, 1560, 340, f, 720)
    island(d, 150, 1470, 160, f, 721)
    for yy in (1685, 1765):
        for xx in range(120, W, 150):
            d.line([(xx, yy), (xx + 66, yy)], fill=(242, 248, 252), width=5)
    ship(d, 430, 1450, 105, f, 722, hull=MERCH)
    ship(d, 660, 1525, 88, f, 723, hull=MERCH, masts=1)
    ship(d, 870, 1485, 98, f, 724, hull=MERCH, masts=1)

# S4 - the raids ---------------------------------------------------------------------------
def s4(d, f, n, t):
    sea(d, 1600, 320, f, 730)
    ship(d, 390 + int(f * 0.8), 1500, 135, f, 731, hull=(96, 70, 52))
    ship(d, 800 + int(f * 1.1), 1480, 118, f, 732, hull=MERCH, masts=1)
    disk(d, 620, 1685 + 4 * math.sin(f * 0.4), 46, (150, 96, 58), INK, 5, 1.6, 733, f, ry=34)
    text(d, 850, 950, '!', 95)

# S5 - demand and refusal -------------------------------------------------------------------
def s5(d, f, n, t):
    sea(d, 1700, 260, f, 740)
    wpoly(d, [(520, 1490), (W, 1460), (W, H), (520, H)], (116, 152, 94), INK, 5, 2.2, 741, f)
    person(d, 580, 1500, 185, (74, 62, 54), f=f, seed=742, hat='tricorne',
           arms=('point', 'down'), trim=(240, 196, 60), face='flat')
    sx, sy = 580 + 0.88 * 185, 1500 - 0.98 * 185 - 0.05 * 185
    d.rectangle([sx, sy - 42, sx + 62, sy + 22], fill=(250, 248, 240), outline=INK, width=4)
    for k in range(3):
        d.line([(sx + 8, sy - 30 + k * 16), (sx + 54, sy - 30 + k * 16)],
               fill=(150, 148, 144), width=3)
    person(d, 880, 1510, 175, (146, 114, 80), f=f, seed=743, hat='furcap',
           arms=('hip', 'down'), face='flat')
    text(d, 880, 1010, 'NO', 115)

# S6 - Tromp arrives -------------------------------------------------------------------------
def s6(d, f, n, t):
    sea(d, 1600, 340, f, 750)
    ship(d, 150, 1445, 108, f, 751, hull=(110, 82, 56), sailcol=(236, 234, 226))
    ship(d, 470, 1500, 185, f, 752, bands=DUTCH)
    ship(d, 900, 1435, 108, f, 753, hull=(110, 82, 56), sailcol=(236, 234, 226))
    person(d, 470, 1399, 60, (58, 58, 64), f=f, seed=754, hat='tricorne',
           arms=('point', 'down'), face='flat')

# S7 - braced for a fight --------------------------------------------------------------------
def s7(d, f, n, t):
    sea(d, 1620, 320, f, 760)
    ship(d, 190, 1470, 118, f, 761, hull=(110, 82, 56))
    ship(d, 450, 1510, 138, f, 762, hull=(96, 70, 52), bands=DUTCH)
    disk(d, 860, 1590, 210, (158, 158, 162), INK, 6, 2.4, 763, f, ry=120)
    for i, ex in enumerate((820, 910)):
        cy = 1478 - i * 14
        disk(d, ex, cy, 34, (255, 255, 255), INK, 5, 1.6, 764 + i, f)
        disk(d, ex - 8, cy, 5, INK, w=0, seed=766 + i, f=f)
        disk(d, ex + 8, cy, 5, INK, w=0, seed=768 + i, f=f)

# S8 - ...nothing ------------------------------------------------------------------------------
def s8(d, f, n, t):
    sea(d, 1620, 320, f, 770)
    ship(d, 190, 1470, 118, f, 771, hull=(110, 82, 56))
    ship(d, 450, 1510, 138, f, 772, hull=(96, 70, 52), bands=DUTCH)
    disk(d, 860, 1590, 210, (158, 158, 162), INK, 6, 2.4, 773, f, ry=120)
    for i in range(3):
        gx = (80 + f * 4 + i * 330) % (W + 80) - 40
        gull(d, gx, 540 + i * 120 + 10 * math.sin(f * 0.3 + i), 24, f, 774 + i)

SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
NIGHT = [False] * 8
BEATS = [
    'In 1651, the Netherlands declared war on a tiny group of islands near England. The war would last 335 years, without a single shot fired.'.split(),
    'It all started during the English Civil War, when the defeated Royalist navy was chased out of England, and fled to the Isles of Scilly.'.split(),
    'Now, these were tiny islands. But they sat right in the middle of the busiest shipping lanes in Europe.'.split(),
    'The Dutch had supported the other side. So Royalist ships sailing from Scilly started attacking Dutch cargo ships, in revenge.'.split(),
    'The Netherlands demanded the islanders pay for the damage. The islanders flat out refused, and the insults escalated.'.split(),
    'So a Dutch admiral, Maarten Tromp, sailed to the islands with his fleet of warships, and officially declared war.'.split(),
    'His men braced for a long, bloody fight over those tiny islands. But then something happened that nobody expected.'.split(),
    'Nothing happened. Absolutely nothing. And that nothing would continue, quite literally, for centuries.'.split(),
]
