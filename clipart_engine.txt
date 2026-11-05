"""Clipart-style animation engine (Experiment #3): white bg, blob-body cartoon
figures with flat COLOR fills + thick black outlines, wobbly hand-drawn lines,
bottom-third captions with one keyword highlighted (amber). 1080x1920, 15fps.
All colors must be int tuples. Each scene fn receives (d, f, n, t) where
d=ImageDraw, f=frame idx, n=total frames, t=f/n fraction."""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
INK = (26, 26, 30)
DAY_BG = (252, 252, 250)
NIGHT_BG = (12, 16, 38)
GROUND = (228, 226, 220)
ACCENT = (255, 176, 0)          # caption keyword colour (ours = amber, theirs = green)
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
STOP = {'THE','AND','WITH','THAT','THIS','THEY','THEIR','WAS','ARE','FOR','YOU',
        'WERE','INTO','FROM','HAVE','BUT','NOT','ALL','ONE','HIS','HER','SHE','WHO'}

def _rng(f, seed): return random.Random(seed * 100003 + f * 9176)

def _jit(pts, wob, r):  # jitter list of (x,y)
    return [(x + r.uniform(-wob, wob), y + r.uniform(-wob, wob)) for x, y in pts]

def wline(d, p1, p2, col=INK, w=6, wob=1.6, seed=0, f=0, nseg=0):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    dist = math.hypot(x2 - x1, y2 - y1)
    n = max(2, nseg or int(dist / 42))
    pts = [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n) for i in range(n + 1)]
    d.line(_jit(pts, wob, _rng(f, seed)), fill=col, width=w, joint='curve')

def wpoly(d, pts, fill, outline=INK, w=6, wob=1.6, seed=0, f=0):
    p = _jit(pts, wob, _rng(f, seed))
    if fill is not None: d.polygon(p, fill=fill)
    if outline is not None and w > 0:
        d.line(p + [p[0]], fill=outline, width=w, joint='curve')

def disk(d, cx, cy, r, fill, outline=INK, w=6, wob=1.8, seed=0, f=0, ry=0):
    ry = ry or r
    pts = [(cx + math.cos(a) * r, cy + math.sin(a) * ry) for a in
           [2 * math.pi * i / 14 for i in range(14)]]
    wpoly(d, pts, fill, outline, w, wob, seed, f)

# ---------------------------------------------------------------- figures ----
_FACE = {'smile': 0, 'open': 1, 'flat': 2, 'sad': 3}
# Validated vocabularies: an unknown value raises instead of drawing nothing.
# ('wig' used to fall through every hat branch -> a bald "Newton" shipped in Ep.19.)
HATS = {None, 'tricorne', 'shako', 'fez', 'furcap', 'turban', 'tophat', 'wig', 'bonnet', 'cap'}
FACES = {None, 'smile', 'open', 'flat', 'sad', 'angry', 'cool', 'smug', 'worried'}
ARMS = {None, 'down', 'up', 'point', 'hip', 'fist', 'musket'}
LEGS = {None, 'stand', 'walk', 'none'}

def person(d, x, y, s, body=(250, 248, 244), skin=(255, 255, 255), f=0, seed=1,
           lean=0.0, face='smile', hat=None, hatcol=(30, 32, 36),
           arms=('down', 'down'), legs='stand', trim=None, bob=0.0):
    """Blob-body clipart figure. y = foot level. s = height scale (~150)."""
    if hat not in HATS:
        raise ValueError(f'person(): unknown hat {hat!r} — known: {sorted(h for h in HATS if h)}')
    if face not in FACES:
        raise ValueError(f'person(): unknown face {face!r} — known: {sorted(f for f in FACES if f)}')
    for a in arms:
        if a not in ARMS:
            raise ValueError(f'person(): unknown arm {a!r} — known: {sorted(a for a in ARMS if a)}')
    if legs not in LEGS:
        raise ValueError(f'person(): unknown legs {legs!r} — known: {sorted(l for l in LEGS if l)}')
    r = _rng(f, seed)
    y += bob * s * 0.03
    hip_y, sh_y = y - 0.44 * s, y - 0.98 * s
    head_c = (x + lean * 0.18 * s, y - (1.62 + lean * -0.02) * s)
    # legs
    if legs == 'none':
        feet = []
    elif legs == 'walk':
        sw = math.sin(f * 0.42 + seed) * 0.16 * s
        feet = [(x - 0.16 * s + sw, y), (x + 0.16 * s - sw, y)]
    else:
        feet = [(x - 0.15 * s, y), (x + 0.15 * s, y)]
    for (fx, fy) in feet:
        wline(d, (x, hip_y), (fx, fy), w=max(4, int(s * 0.05)), seed=seed + 3, f=f)
        disk(d, fx, fy - 2, s * 0.075, INK, w=0, seed=seed + 4, f=f)   # oval shoe
    # body blob (rounded coat): polygon between hips and shoulders
    bx = lean * 0.10 * s
    pts = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        ex = math.cos(a)
        ey = math.sin(a)
        px = x + bx * (0.5 - ey * 0.5) + ex * 0.40 * s
        py = (hip_y + sh_y) / 2 + ey * 0.34 * s
        pts.append((px, py))
    wpoly(d, pts, body, INK, max(5, int(s * 0.045)), 2.0, seed + 5, f)
    if trim is not None:  # diagonal sash
        wline(d, (x - 0.3 * s + bx, sh_y + 0.06 * s), (x + 0.28 * s + bx, hip_y - 0.05 * s),
              col=trim, w=max(5, int(s * 0.05)), wob=1.2, seed=seed + 6, f=f)
    # arms
    palm = s * 0.075
    def hand(mode, side):
        sx = x + bx + side * 0.33 * s
        hd = {'down': (side * 0.11 * s, 0.52 * s), 'up': (side * 0.4 * s, -0.62 * s),
              'point': (side * 0.55 * s, -0.05 * s), 'hip': (side * 0.2 * s, 0.42 * s),
              'fist': (side * 0.42 * s, -0.4 * s), 'musket': (side * 0.34 * s, -0.5 * s)}[mode]
        hx, hy = sx + hd[0], sh_y + hd[1]
        wline(d, (sx, sh_y), (hx, hy), w=max(4, int(s * 0.045)), seed=seed + 7 + side, f=f)
        disk(d, hx, hy, palm, INK, w=0, seed=seed + 8 + side, f=f)
        return hx, hy
    hxl, hyl = hand(arms[0], -1)
    hxr, hyr = hand(arms[1], 1)
    if 'musket' in arms:  # draw musket along the musket-hand
        hx, hy = (hxl, hyl) if arms[0] == 'musket' else (hxr, hyr)
        sgn = -1 if arms[0] == 'musket' else 1
        dx, dy = sgn * 0.5 * s, -0.55 * s
        nrm = math.hypot(dx, dy)
        wline(d, (x, sh_y), (x + dx, sh_y + dy), w=max(5, int(s * 0.05)),
              col=(88, 62, 40), seed=seed + 9, f=f)
        wline(d, (x + dx, sh_y + dy), (x + sgn * 0.62 * s, sh_y - 0.78 * s),
              w=max(3, int(s * 0.03)), col=(60, 60, 66), seed=seed + 10, f=f)
    # head
    disk(d, head_c[0], head_c[1], 0.335 * s, skin, INK, max(5, int(s * 0.05)), 2.2, seed + 11, f)
    ex, ey = head_c[0], head_c[1]
    eo = 0.115 * s
    if face == 'cool':
        for sgn in (-1, 1):
            d.rounded_rectangle([ex + sgn * eo - 0.062 * s, ey - 0.065 * s,
                                 ex + sgn * eo + 0.062 * s, ey + 0.005 * s],
                                radius=int(0.022 * s), fill=(36, 38, 42), outline=INK,
                                width=max(2, int(s * 0.014)))
        wline(d, (ex - 0.055 * s, ey - 0.030 * s), (ex + 0.055 * s, ey - 0.030 * s),
              w=max(2, int(s * 0.014)), wob=0.4, seed=seed + 12, f=f)   # bridge
    else:
        for sgn in (-1, 1):
            if face == 'sad':
                disk(d, ex + sgn * eo, ey - 0.03 * s, 0.032 * s, INK, w=0, seed=seed + 12, f=f)
            else:
                disk(d, ex + sgn * eo, ey - 0.03 * s, 0.05 * s, (255, 255, 255), INK,
                     max(2, int(s * 0.016)), 0.8, seed + 12 + sgn, f)
                disk(d, ex + sgn * eo, ey - 0.02 * s, 0.020 * s, INK, w=0, seed=seed + 14, f=f)
    if face == 'angry':
        for sgn in (-1, 1):
            wline(d, (ex + sgn * (eo - 0.05 * s), ey - 0.13 * s),
                  (ex + sgn * (eo + 0.05 * s), ey - 0.19 * s), w=max(3, int(s * 0.02)),
                  wob=0.8, seed=seed + 16 + sgn, f=f)
        disk(d, ex, ey + 0.13 * s, 0.07 * s, INK, w=0, wob=1.2, seed=seed + 18, f=f)
    elif face == 'open':
        disk(d, ex, ey + 0.13 * s, 0.075 * s, INK, w=0, wob=1.2, seed=seed + 18, f=f)
    elif face == 'flat':
        wline(d, (ex - 0.08 * s, ey + 0.13 * s), (ex + 0.08 * s, ey + 0.13 * s),
              w=max(3, int(s * 0.02)), wob=0.8, seed=seed + 18, f=f)
    elif face == 'sad':
        pts = [(ex - 0.09 * s, ey + 0.19 * s), (ex, ey + 0.11 * s), (ex + 0.09 * s, ey + 0.19 * s)]
        d.line(_jit(pts, 0.8, r), fill=INK, width=max(3, int(s * 0.02)), joint='curve')
    elif face == 'smug':      # one-sided smirk
        pts = [(ex - 0.08 * s, ey + 0.14 * s), (ex + 0.02 * s, ey + 0.18 * s),
               (ex + 0.10 * s, ey + 0.10 * s)]
        d.line(_jit(pts, 0.8, r), fill=INK, width=max(3, int(s * 0.02)), joint='curve')
        for sgn in (-1, 1):   # half-lidded eyes
            wline(d, (ex + sgn * eo - 0.05 * s, ey - 0.06 * s),
                  (ex + sgn * eo + 0.05 * s, ey - 0.04 * s),
                  w=max(3, int(s * 0.022)), wob=0.6, seed=seed + 19 + sgn, f=f)
    elif face == 'worried':
        pts = [(ex - 0.09 * s, ey + 0.18 * s), (ex, ey + 0.12 * s), (ex + 0.09 * s, ey + 0.18 * s)]
        d.line(_jit(pts, 0.8, r), fill=INK, width=max(3, int(s * 0.02)), joint='curve')
        for sgn in (-1, 1):   # raised inner brows
            wline(d, (ex + sgn * eo - sgn * 0.02 * s, ey - 0.16 * s),
                  (ex + sgn * eo + sgn * 0.07 * s, ey - 0.20 * s),
                  w=max(3, int(s * 0.02)), wob=0.8, seed=seed + 21 + sgn, f=f)
    else:  # smile
        pts = [(ex - 0.10 * s, ey + 0.10 * s), (ex, ey + 0.17 * s), (ex + 0.10 * s, ey + 0.10 * s)]
        d.line(_jit(pts, 0.8, r), fill=INK, width=max(3, int(s * 0.02)), joint='curve')
    # hats
    if hat == 'tricorne':
        disk(d, ex, ey - 0.30 * s, 0.30 * s, hatcol, INK, max(4, int(s * 0.04)), 1.6,
             seed + 20, f, ry=0.13 * s)
        disk(d, ex, ey - 0.31 * s, 0.10 * s, (250, 200, 60), w=max(2, int(s * 0.02)),
             wob=0.8, seed=seed + 21, f=f)
    elif hat == 'shako':
        pts = [(ex - 0.20 * s, ey - 0.30 * s), (ex + 0.20 * s, ey - 0.30 * s),
               (ex + 0.16 * s, ey - 0.78 * s), (ex - 0.16 * s, ey - 0.78 * s)]
        wpoly(d, pts, hatcol, INK, max(4, int(s * 0.04)), 1.6, seed + 22, f)
        disk(d, ex + 0.05 * s, ey - 0.86 * s, 0.09 * s, (220, 60, 60), w=max(2, int(s * 0.018)),
             wob=0.8, seed=seed + 23, f=f, ry=0.13 * s)
    elif hat == 'fez':
        pts = [(ex - 0.19 * s, ey - 0.30 * s), (ex + 0.19 * s, ey - 0.30 * s),
               (ex + 0.14 * s, ey - 0.62 * s), (ex - 0.14 * s, ey - 0.62 * s)]
        wpoly(d, pts, (178, 44, 48), INK, max(4, int(s * 0.04)), 1.6, seed + 24, f)
        wline(d, (ex + 0.14 * s, ey - 0.62 * s), (ex + 0.22 * s, ey - 0.44 * s),
              w=max(2, int(s * 0.02)), col=(240, 200, 80), wob=1.0, seed=seed + 25, f=f)
    elif hat == 'furcap':
        disk(d, ex, ey - 0.34 * s, 0.24 * s, (96, 84, 74), INK, max(4, int(s * 0.04)),
             1.4, seed + 26, f, ry=0.16 * s)
    elif hat == 'tophat':
        wpoly(d, [(ex - 0.26 * s, ey - 0.29 * s), (ex + 0.26 * s, ey - 0.29 * s),
                  (ex + 0.26 * s, ey - 0.36 * s), (ex - 0.26 * s, ey - 0.36 * s)],
              hatcol, INK, max(4, int(s * 0.04)), 1.4, seed + 30, f)          # brim
        wpoly(d, [(ex - 0.18 * s, ey - 0.36 * s), (ex + 0.18 * s, ey - 0.36 * s),
                  (ex + 0.16 * s, ey - 0.86 * s), (ex - 0.16 * s, ey - 0.86 * s)],
              hatcol, INK, max(4, int(s * 0.04)), 1.4, seed + 31, f)          # crown
        wline(d, (ex - 0.18 * s, ey - 0.50 * s), (ex + 0.18 * s, ey - 0.50 * s),
              w=max(4, int(s * 0.035)), col=(178, 44, 48), wob=0.8, seed=seed + 32, f=f)
    elif hat == 'wig':
        # full-bottomed wig: curls at the sides + a crown band that stays OFF the face
        for sgn in (-1, 1):
            for k in range(3):
                disk(d, ex + sgn * (0.35 + 0.035 * k) * s, ey + (0.02 + 0.16 * k) * s,
                     0.115 * s, hatcol, INK, max(3, int(s * 0.028)), 1.6,
                     seed + 34 + sgn * 3 + k, f)
            disk(d, ex + sgn * 0.31 * s, ey - 0.13 * s, 0.125 * s, hatcol, INK,
                 max(3, int(s * 0.028)), 1.6, seed + 38 + sgn, f)
        disk(d, ex, ey - 0.40 * s, 0.31 * s, hatcol, INK, max(4, int(s * 0.035)),
             1.8, seed + 40, f, ry=0.155 * s)                                  # crown
        wline(d, (ex - 0.19 * s, ey - 0.30 * s), (ex + 0.19 * s, ey - 0.30 * s),
              w=max(3, int(s * 0.024)), col=hatcol, wob=1.0, seed=seed + 41, f=f)
    elif hat == 'bonnet':
        disk(d, ex, ey - 0.36 * s, 0.34 * s, hatcol, INK, max(4, int(s * 0.04)),
             1.8, seed + 42, f, ry=0.22 * s)
        wline(d, (ex - 0.33 * s, ey - 0.235 * s), (ex + 0.33 * s, ey - 0.235 * s),
              w=max(3, int(s * 0.026)), col=(238, 232, 214), wob=1.0, seed=seed + 43, f=f)
        for sgn in (-1, 1):   # ribbons
            wline(d, (ex + sgn * 0.30 * s, ey - 0.20 * s),
                  (ex + sgn * 0.36 * s, ey + 0.06 * s),
                  w=max(2, int(s * 0.02)), col=(238, 232, 214), wob=0.8,
                  seed=seed + 44 + sgn, f=f)
        disk(d, ex + 0.26 * s, ey - 0.46 * s, 0.05 * s, (200, 60, 60), INK,
             max(2, int(s * 0.016)), 0.8, seed + 46, f)
    elif hat == 'cap':
        disk(d, ex, ey - 0.33 * s, 0.28 * s, hatcol, INK, max(4, int(s * 0.04)),
             1.6, seed + 45, f, ry=0.15 * s)
        wline(d, (ex - 0.24 * s, ey - 0.30 * s), (ex + 0.40 * s, ey - 0.27 * s),
              w=max(4, int(s * 0.034)), col=hatcol, wob=1.0, seed=seed + 46, f=f)  # peak
    elif hat == 'turban':
        disk(d, ex, ey - 0.32 * s, 0.27 * s, (242, 240, 234), INK, max(4, int(s * 0.04)),
             1.6, seed + 27, f, ry=0.16 * s)
        disk(d, ex, ey - 0.36 * s, 0.06 * s, (200, 60, 60), INK, max(2, int(s * 0.02)),
             0.8, seed + 28, f)
        wline(d, (ex - 0.2 * s, ey - 0.28 * s), (ex + 0.2 * s, ey - 0.28 * s),
              w=max(2, int(s * 0.02)), col=(220, 190, 90), wob=0.8, seed=seed + 29, f=f)

# ----------------------------------------------------------------- props -----
def barrel(d, x, y, s, f=0, seed=30, brown=(150, 96, 58)):
    pts = [(x - 0.5 * s, y - 0.62 * s), (x + 0.5 * s, y - 0.62 * s),
           (x + 0.58 * s, y - 0.2 * s), (x + 0.5 * s, y + 0.2 * s), (x - 0.5 * s, y + 0.2 * s),
           (x - 0.58 * s, y - 0.2 * s)]
    wpoly(d, pts, brown, INK, max(4, int(s * 0.05)), 1.6, seed, f)
    disk(d, x, y - 0.6 * s, 0.5 * s, (176, 122, 80), INK, max(4, int(s * 0.05)), 1.4,
         seed + 1, f, ry=0.13 * s)
    for yy in (-0.42, -0.05):
        wline(d, (x - 0.46 * s, y + yy * s), (x + 0.46 * s, y + yy * s),
              col=(74, 74, 80), w=max(3, int(s * 0.045)), wob=1.2, seed=seed + 2, f=f)

def tent(d, x, y, s, f=0, seed=40, cloth=(238, 232, 216)):
    wpoly(d, [(x - 0.75 * s, y), (x + 0.05 * s, y - 0.95 * s), (x + 0.75 * s, y)],
          cloth, INK, max(4, int(s * 0.05)), 2.2, seed, f)
    wline(d, (x + 0.05 * s, y - 0.95 * s), (x + 0.05 * s, y), w=max(3, int(s * 0.04)),
          wob=1.2, seed=seed + 1, f=f)

def fire(d, x, y, s, f=0, seed=50):
    grow = 1 + 0.16 * math.sin(f * 0.7)
    wline(d, (x - 0.3 * s, y), (x + 0.3 * s, y - 0.06 * s), col=(96, 66, 40),
          w=max(4, int(s * 0.09)), wob=1.4, seed=seed, f=f)
    pts = [(x - 0.26 * s, y), (x - 0.08 * s, y - 0.5 * s * grow),
           (x, y - 0.34 * s * grow), (x + 0.10 * s, y - 0.62 * s * grow),
           (x + 0.28 * s, y)]
    wpoly(d, pts, (240, 120, 40), INK, max(3, int(s * 0.045)), 2.4, seed + 1, f)
    pts2 = [(p[0] * 0.6 + x * 0.4, y - (y - p[1]) * 0.55) for p in pts]
    wpoly(d, pts2, (250, 210, 90), None, 0, 1.6, seed + 2, f)

def bottle(d, x, y, s, f=0, seed=60, tilt=0):
    pts = [(x - 0.10 * s, y), (x + 0.10 * s, y), (x + 0.10 * s, y - 0.36 * s),
           (x + 0.035 * s, y - 0.42 * s), (x + 0.035 * s, y - 0.58 * s),
           (x - 0.035 * s, y - 0.58 * s), (x - 0.035 * s, y - 0.42 * s),
           (x - 0.10 * s, y - 0.36 * s)]
    wpoly(d, pts, (60, 130, 70), INK, max(3, int(s * 0.05)), 1.0, seed, f)

def flag(d, x, y, s, f=0, seed=70, bands=((40, 40, 44), (240, 196, 60))):
    wline(d, (x, y), (x, y - 1.5 * s), w=max(4, int(s * 0.05)), wob=1.2, seed=seed, f=f)
    n = 8
    top = [(x, y - 1.50 * s - 0.0 * s)]
    pts_top = [(x + 0.07 * i * s, y - 1.50 * s + math.sin(f * 0.35 + i * 0.9) * 0.06 * s)
                for i in range(n + 1)]
    pts_bot = [(px, py + 0.42 * s) for px, py in pts_top]
    for i, band in enumerate(bands):
        a, b = pts_top[::], pts_bot[::]
        ya = [(p[0], p[1] + i * 0.42 * s / len(bands)) for p in a]
        yb = [(p[0], p[1] + (i + 1) * 0.42 * s / len(bands)) for p in b]
        wpoly(d, ya + yb[::-1], band, None, 0, 0.8, seed + 2 + i, f)
    d.line(_jit(pts_top, 0.8, _rng(f, seed + 9)), fill=INK, width=max(3, int(s * 0.035)))
    d.line(_jit(pts_bot, 0.8, _rng(f, seed + 10)), fill=INK, width=max(3, int(s * 0.035)))
    wline(d, pts_top[-1], pts_bot[-1], w=max(3, int(s * 0.035)), wob=0.8, seed=seed + 11, f=f)

def river(d, yc, th=190, f=0, seed=80):
    d.rectangle([0, yc - th // 2, W, yc + th // 2], fill=(154, 196, 228))
    r = _rng(f, seed)
    for i in range(9):
        x = 60 + i * 122
        pts = [(x + j * 26, yc - th / 2 + 30 + (i * 37 % (th - 60)) +
                math.sin(f * 0.5 + j) * 5) for j in range(3)]
        d.line(_jit(pts, 1.2, r), fill=(110, 160, 200), width=5, joint='curve')

def moon(d, x, y, r, f=0, seed=90):
    disk(d, x, y, r, (250, 238, 170), INK, 5, 1.2, seed, f)
    disk(d, x + r * 0.55, y - r * 0.2, r * 0.8, NIGHT_BG, None, 0, 1.0, seed + 1, f)

def stars(d, n=55, f=0):
    r = _rng(f, 99)
    for i in range(n):
        x, y = r.uniform(20, W - 20), r.uniform(20, H * 0.5)
        rr = r.uniform(1.5, 3.4)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(240, 240, 250))

def burst(d, x, y, r, col=(255, 214, 90), f=0, seed=100, spikes=9):
    pts = []
    for i in range(spikes * 2):
        a = math.pi * i / spikes + f * 0.02
        rr = r if i % 2 == 0 else r * 0.38
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    wpoly(d, pts, col, INK, 5, 2.0, seed, f)

def groundline(d, y, f=0, col=GROUND):
    wline(d, (0, y), (W, y), col=col, w=8, wob=2.0, seed=777, f=f)

# --------------------------------------------------------------- captions ----
def _chunks(words, n=3):
    return [words[i:i + n] for i in range(0, len(words), n)]

def _keyword(chunk):
    best, bestlen = None, 4
    for wd in chunk:
        c = wd.strip('.,!?:;—').upper()
        if len(c) >= bestlen and c not in STOP:
            best, bestlen = wd, len(c)
    return best

def draw_caption(img, words, t, size=64, night=False, chunk_n=3, speech_frac=1.0,
                 schedule=None, y_frac=0.775, max_w=940, scale=1.0):
    if chunk_n == 1 and size < 76:
        size = 76             # karaoke single words read punchier
    elif chunk_n == 2 and size < 72:
        size = 72
    size = int(round(size * scale))
    if 0 < speech_frac < 1:
        t = min(t / speech_frac, 0.99999)   # caption clock covers SPEECH only, not the tail gap
    gs = _chunks(words, chunk_n)
    if schedule and len(schedule) == len(words):
        # TRUE SYNC (ASR): show the word actually being spoken right now
        cur = 0
        for wi, sf in enumerate(schedule):
            if t >= sf:
                cur = wi
            else:
                break
        gi = min(cur // chunk_n, len(gs) - 1)
        chunk = gs[gi]
        kw = words[cur]                       # exact spoken word goes amber
    else:
        # fallback estimate: weight every chunk by word length + punctuation pauses
        wts = []
        for ch in gs:
            w = 0.0
            for wd in ch:
                c = wd.rstrip('.,!?:;').upper()
                w += 0.8 + len(c)
                if wd[-1:] in '.!?':        w += 4.0    # sentence-final pause
                elif wd[-1:] in ',;':       w += 2.0    # comma breath
                elif wd[-1:] == ':':        w += 3.0
            wts.append(w)
        tot = sum(wts)
        cut = t * tot
        acc, gi = 0.0, len(gs) - 1
        for k, w in enumerate(wts):
            acc += w
            if cut < acc:
                gi = k
                break
        chunk = gs[gi]
        kw = _keyword(chunk)
    d = ImageDraw.Draw(img, 'RGBA')
    font = ImageFont.truetype(FONT_PATH, size)
    text = ' '.join(chunk).upper()
    while size > 34 and d.textlength(text, font=font) > max_w:
        size -= 2; font = ImageFont.truetype(FONT_PATH, size)
        text = ' '.join(chunk).upper()
    total = d.textlength(text, font=font)
    cx = (W - total) / 2
    y = H * y_frac
    for wd in chunk:
        wtxt = wd.upper() + ' '
        col = ACCENT if (wd == kw) else (252, 252, 252)
        d.text((cx, y), wtxt, font=font, fill=col,
               stroke_width=max(3, int(round(5 * scale))), stroke_fill=(18, 18, 22))
        cx += d.textlength(wtxt, font=font)

# ---------------------------------------------------------------- driver -----
def render_scene(scene_fn, nframes, outdir, caption_words, night=False, seed0=0,
                 extra=None, chunk_n=3, caption_frac=1.0, caption_schedule=None,
                 cap_kw=None, bg=None, size=None, panel=None, drift=0.0):
    os.makedirs(outdir, exist_ok=True)
    for fd in range(nframes):
        path = f'{outdir}/f{fd+1:04d}.png'
        if os.path.exists(path):
            continue
        img = Image.new('RGB', size or (W, H), bg if bg is not None else (NIGHT_BG if night else DAY_BG))
        d = ImageDraw.Draw(img)
        if panel is not None:          # full-canvas art (another engine draws the frame)
            p = panel(fd, nframes, fd / max(1, nframes - 1)).convert('RGB')
            if p.size != img.size:
                p = p.resize(img.size, Image.LANCZOS)
            if drift:                  # Ken-Burns style slow push (factory zoompan feel)
                z = 1.0 + drift * (fd / max(1, nframes - 1))
                w2, h2 = int(round(p.width * z)), int(round(p.height * z))
                p = p.resize((w2, h2), Image.LANCZOS)
                x0 = (w2 - img.width) // 2; y0 = (h2 - img.height) // 2
                p = p.crop((x0, y0, x0 + img.width, y0 + img.height))
            img.paste(p)
            d = ImageDraw.Draw(img)    # captions still land on top
        else:
            scene_fn(d, fd, nframes, fd / max(1, nframes - 1))
        if extra is not None:
            extra(img)
        if caption_words:
            draw_caption(img, caption_words, fd / max(1, nframes - 1),
                         night=night, chunk_n=chunk_n, speech_frac=caption_frac,
                         schedule=caption_schedule, **(cap_kw or {}))
        img.convert('RGB').save(path)

def horse(d, x, y, s, f=0, seed=300, col=(124, 96, 70)):
    cy = y - 0.95 * s
    disk(d, x, cy, 0.52 * s, col, INK, max(5, int(s * 0.045)), 2.0, seed, f, ry=0.30 * s)
    wline(d, (x + 0.38 * s, cy - 0.08 * s), (x + 0.66 * s, cy - 0.52 * s),
          col=col, w=max(6, int(0.16 * s)), wob=1.6, seed=seed + 1, f=f)
    disk(d, x + 0.74 * s, cy - 0.60 * s, 0.15 * s, col, INK, max(4, int(s * 0.04)),
         1.4, seed + 2, f, ry=0.21 * s)
    wline(d, (x - 0.48 * s, cy - 0.04 * s), (x - 0.80 * s, cy + 0.30 * s),
          col=col, w=max(4, int(0.09 * s)), wob=2.2, seed=seed + 3, f=f)
    tops = [(x + 0.36 * s, cy + 0.16 * s), (x + 0.26 * s, cy + 0.18 * s),
            (x - 0.28 * s, cy + 0.16 * s), (x - 0.38 * s, cy + 0.14 * s)]
    for li, (lx, ly) in enumerate(tops):
        dirn = 1 if li < 2 else -1
        sw = math.sin(f * 0.75 + li * 1.4) * 0.30 * s * dirn
        foot = (lx + dirn * 0.28 * s + sw, y)
        wline(d, (lx, ly), foot, col=col, w=max(4, int(s * 0.05)), wob=1.5,
              seed=seed + 4 + li, f=f)
        disk(d, foot[0], foot[1] - 2, 0.05 * s, INK, w=0, seed=seed + 8 + li, f=f)
    wline(d, (x + 0.70 * s, cy - 0.74 * s), (x + 0.75 * s, cy - 0.88 * s),
          col=INK, w=max(2, int(s * 0.022)), wob=0.8, seed=seed + 12, f=f)

def cannon(d, x, y, s, f=0, seed=400, col=(54, 58, 66)):
    bl, yb, ang = 0.95 * s, y - 0.5 * s, 0.30 * s
    pts = [(x, yb - 0.14 * s), (x - bl, yb - ang - 0.09 * s),
           (x - bl, yb - ang + 0.09 * s), (x, yb + 0.14 * s)]
    wpoly(d, pts, col, INK, max(4, int(s * 0.04)), 1.6, seed, f)
    wline(d, (x - 0.14 * s, y - 0.30 * s), (x + 0.32 * s, y - 0.30 * s),
          col=(120, 84, 52), w=max(4, int(s * 0.05)), wob=1.2, seed=seed + 1, f=f)
    disk(d, x - 0.14 * s, y - 0.28 * s, 0.28 * s, (132, 94, 56), INK,
         max(4, int(s * 0.04)), 1.8, seed + 2, f)
    disk(d, x + 0.32 * s, y - 0.24 * s, 0.24 * s, (132, 94, 56), INK,
         max(4, int(s * 0.04)), 1.8, seed + 3, f)
    disk(d, x - 0.14 * s, y - 0.28 * s, 0.06 * s, INK, w=0, wob=0.6, seed=seed + 4, f=f)
    disk(d, x + 0.32 * s, y - 0.24 * s, 0.05 * s, INK, w=0, wob=0.6, seed=seed + 5, f=f)
    return (x - bl, yb - ang)

def sea(d, yc, th=280, f=0, seed=700):
    d.rectangle([0, yc - th // 2, W, yc + th // 2], fill=(126, 174, 208))
    rr = _rng(f, seed)
    for row in range(4):
        yy = yc - th // 2 + 40 + row * 55
        col = (226, 238, 248) if row % 2 else (164, 200, 228)
        pts = []
        for xx in range(30, W, 110):
            yo = math.sin(f * 0.35 + xx * 0.013 + row * 1.9) * 7
            pts += [(xx, int(yy + yo)), (xx + 52, int(yy - 6 - yo))]
        d.line(pts, fill=col, width=6, joint='curve')

def ship(d, x, y, s, f=0, seed=650, hull=(120, 84, 52), sailcol=(246, 243, 232),
         masts=2, bands=()):
    hullpts = [(x - 1.0 * s, y - 0.52 * s), (x + 1.0 * s, y - 0.52 * s),
               (x + 0.86 * s, y - 0.18 * s), (x + 0.45 * s, y + 0.03 * s),
               (x - 0.45 * s, y + 0.03 * s), (x - 0.86 * s, y - 0.18 * s)]
    wpoly(d, hullpts, hull, INK, max(4, int(s * 0.04)), 1.8, seed, f)
    wline(d, (x - 0.95 * s, y - 0.55 * s), (x + 0.95 * s, y - 0.55 * s),
          col=(84, 58, 38), w=max(3, int(s * 0.03)), wob=1.0, seed=seed + 1, f=f)
    xs = [x - 0.42 * s, x + 0.32 * s] if masts == 2 else [x]
    for mi, mx in enumerate(xs):
        top = y - 2.05 * s
        wline(d, (mx, y - 0.55 * s), (mx, top), col=(88, 62, 40),
              w=max(3, int(s * 0.032)), wob=1.2, seed=seed + 2 + mi, f=f)
        bulge = math.sin(f * 0.45 + mi * 1.7) * 0.05 * s
        sail = [(mx - 0.34 * s, top + 0.12 * s), (mx + 0.34 * s, top + 0.12 * s),
                (mx + 0.50 * s + bulge, top + 0.62 * s), (mx + bulge, top + 0.98 * s),
                (mx - 0.50 * s + bulge, top + 0.62 * s)]
        wpoly(d, sail, sailcol, INK, max(3, int(s * 0.035)), 1.6, seed + 4 + mi, f)
    if bands:
        mx = xs[0]
        bh = 0.10 * s
        for bi, bc in enumerate(bands):
            wv = 3 * math.sin(f * 0.5 + bi * 2)
            wpoly(d, [(mx + 0.03 * s, y - 2.12 * s + bi * bh),
                      (mx + 0.36 * s, y - 2.12 * s + bi * bh + wv),
                      (mx + 0.36 * s, y - 2.12 * s + (bi + 1) * bh + wv),
                      (mx + 0.03 * s, y - 2.12 * s + (bi + 1) * bh)],
                  bc, None, 0, 0.8, seed + 8 + bi, f)

def island(d, x, y, s, f=0, seed=750, church=True):
    disk(d, x, y, 0.9 * s, (112, 152, 92), INK, 6, 2.2, seed, f, ry=0.34 * s)
    if church:
        d.rectangle([x - 0.13 * s, y - 0.60 * s, x + 0.13 * s, y - 0.12 * s],
                    fill=(240, 238, 230), outline=INK, width=4)
        wpoly(d, [(x - 0.17 * s, y - 0.60 * s), (x, y - 0.82 * s),
                  (x + 0.17 * s, y - 0.60 * s)], (150, 110, 90), INK, 4, 1.0, seed + 1, f)
        wline(d, (x, y - 0.82 * s), (x, y - 0.96 * s), col=INK, w=3, wob=0.6, seed=seed + 2, f=f)
        wline(d, (x - 0.045 * s, y - 0.90 * s), (x + 0.045 * s, y - 0.90 * s), col=INK,
              w=3, wob=0.6, seed=seed + 3, f=f)

def gull(d, x, y, s=26, f=0, seed=760):
    pts = [(x - s, y - 4 * math.sin(f * 0.5 + seed)), (x, y - s * 0.55), (x + s, y)]
    d.line(pts, fill=INK, width=4, joint='curve')
