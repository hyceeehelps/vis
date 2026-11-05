"""CAST DEMO — the same characters across 8 beats, zero re-invention.

Every figure below comes from cast_defs.py via char(). Nothing here invents a colour,
a hat or a seed: a scene only chooses WHO is on screen, WHERE, and WHAT they're doing.
Change Law's coat once in cast_defs.py and all 8 beats follow.

Beat text = Ep.20 P1's narration, so badges/captions are real house output.
This demo runs without voiceover (silent VO beats) to show the cast in isolation.
"""
import sys, os
sys.path.insert(0, os.environ.get('FACTORY_ROOT', '/home/user/vis'))
from PIL import ImageFont
from clipart_engine import (W, H, INK, groundline, disk, wpoly, wline, burst,
                            moon, stars, barrel, river)
from cast_engine import char, group

TXTF = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
CAP_CHUNK = 2


def label(d, x, y, txt, size=64, col=INK):
    fnt = ImageFont.truetype(TXTF, size)
    d.text((x, y), txt, font=fnt, fill=col, anchor='mm', stroke_width=5,
           stroke_fill=(255, 255, 255))


# 1 — Paris, 1715: bankrupt, a gambler walks in ------------------------------------------
def s1(d, f, n, t):
    groundline(d, 1560, f)
    label(d, 300, 980, 'BANKRUPT', 78)
    barrel(d, 880, 1560, 150, f, 501)
    char(d, 'law', 420 + f * 0.8 % 40, 1540, 195, f=f, pose='walk')


# 2 — the Regent lets him open a bank ----------------------------------------------------
def s2(d, f, n, t):
    groundline(d, 1560, f)
    label(d, 540, 700, 'BANQUE', 86)
    char(d, 'law', 360, 1540, 190, f=f, pose='argue')
    char(d, 'regent', 760, 1550, 185, f=f, pose='point')


# 3 — the press prints notes -------------------------------------------------------------
def s3(d, f, n, t):
    groundline(d, 1580, f)
    char(d, 'clerk', 300, 1550, 185, f=f, pose='write')
    for k in range(4):
        x = 520 + (k * 90 + f * 2) % 420
        d.rectangle([x, 900 + k * 40, x + 70, 940 + k * 40],
                    fill=(250, 246, 232), outline=INK, width=4)
        label(d, x + 35, 920 + k * 40, '$', 34)


# 4 — Paris queues for shares ------------------------------------------------------------
def s4(d, f, n, t):
    groundline(d, 1580, f)
    group(d, ['villager', 'crowd', 'villager2'], 1560, f=f, s=165,
          poses={'villager': 'argue', 'crowd': 'shrug', 'villager2': 'panic'})


# 5 — the word "millionaire" is born -----------------------------------------------------
def s5(d, f, n, t):
    groundline(d, 1580, f)
    char(d, 'merchant', 300, 1550, 190, f=f, pose='point')
    char(d, 'law', 700, 1550, 200, f=f, pose='cheer')
    burst(d, 700, 1080, 80, (255, 214, 90), f, 502)


# 6 — duchesses fight for shares ---------------------------------------------------------
def s6(d, f, n, t):
    groundline(d, 1580, f)
    char(d, 'duchess', 320, 1550, 195, f=f, pose='argue')
    char(d, 'sailor', 700, 1550, 185, f=f, pose='shrug')


# 7 — Newton cashes out, then dives back in ----------------------------------------------
def s7(d, f, n, t):
    groundline(d, 1580, f)
    char(d, 'newton', 340, 1550, 195, f=f, pose='write')
    char(d, 'director', 760, 1550, 190, f=f, pose='point')
    label(d, 540, 820, 'x2', 96)


# 8 — the wagons arrive: cliffhanger -----------------------------------------------------
def s8(d, f, n, t):
    groundline(d, 1580, f)
    char(d, 'soldier', 260, 1550, 185, f=f, pose='guard')
    char(d, 'law', 540, 1550, 190, f=f, pose='panic')
    char(d, 'emperor', 820, 1550, 185, f=f, pose='point')
    label(d, 540, 780, '. . .', 110)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
NIGHT = [False] * 8

BEATS = [
    ["Paris,", "1715.", "France", "is", "bankrupt", "from", "war."],
    ["A", "smooth", "talking", "Scottish", "gambler", "arrives", "with", "an", "idea."],
    ["His", "bank", "prints", "notes", "backed", "by", "confidence,", "not", "gold."],
    ["The", "street", "outside", "becomes", "a", "human", "casino."],
    ["Paris", "invents", "a", "brand", "new", "word,", "the", "millionaire."],
    ["Duchesses", "fight", "for", "shares", "and", "servants", "turn", "into", "lords."],
    ["Law", "becomes", "richer", "than", "the", "king.", "On", "paper."],
    ["Then", "a", "prince", "arrives", "demanding", "real", "gold."],
]
