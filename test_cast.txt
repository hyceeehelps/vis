"""test_cast.py — the anti-drift checks for the recurring cast.

Run:  python3 test_cast.py
All four must pass before an episode build. They are deliberately dumb and fast:
no episode code, no ffmpeg, no frames on disk.

  1. IDENTITY IS STABLE   same name + same pose + same frame -> byte-identical pixels
  2. POSE IS FREE         same name, different pose -> different pixels (it really moved)
  3. NO STRANGERS         an undefined name or an identity override raises
  4. VOCAB IS VALID       an unknown hat/face raises instead of drawing nothing
"""
import io
import sys
import hashlib

import cast_engine
from cast_engine import char, CAST, CastError
from PIL import Image, ImageDraw
import clipart_engine as ce

cast_engine.load_defs()
FAILS = []


def render(name, pose, f=0, size=300):
    img = Image.new('RGB', (ce.W, ce.H), ce.DAY_BG)
    char(ImageDraw.Draw(img), name, ce.W // 2, 1500, size, f=f, pose=pose)
    return img


def h(img):
    return hashlib.md5(img.tobytes()).hexdigest()


def check(label, ok, detail=''):
    print(f"{'PASS' if ok else 'FAIL'}  {label}" + (f'  ({detail})' if detail else ''))
    if not ok:
        FAILS.append(label)


# 1 — identity is stable: the same call twice is pixel-identical
for name in CAST:
    check(f'1 identity stable: {name}', h(render(name, 'idle')) == h(render(name, 'idle')))

# 2 — pose actually changes the drawing
check('2 pose varies the figure', h(render('law', 'idle')) != h(render('law', 'argue')))

# 3 — no strangers, no identity edits at the call site
for bad in ('not_a_character', 'Law'):
    try:
        render(bad, 'idle')
        check(f'3 unknown name rejected: {bad}', False)
    except CastError:
        check(f'3 unknown name rejected: {bad}', True)
try:
    render('law', 'idle')
    img = Image.new('RGB', (ce.W, ce.H), ce.DAY_BG)
    char(ImageDraw.Draw(img), 'law', 500, 1500, 300, body=(255, 0, 0))
    check('3 identity override rejected', False, 'body= was accepted')
except CastError:
    check('3 identity override rejected', True)

# 4 — validated vocabularies in the engine
for bad_hat in ('wiglet', 'bowler'):
    try:
        ce.person(ImageDraw.Draw(Image.new('RGB', (10, 10))), 5, 5, 100, hat=bad_hat)
        check(f'4 unknown hat rejected: {bad_hat}', False)
    except ValueError:
        check(f'4 unknown hat rejected: {bad_hat}', True)

print()
if FAILS:
    print(f'{len(FAILS)} FAILED: {FAILS}')
    sys.exit(1)
print(f'all checks passed — {len(CAST)} cast members locked')
