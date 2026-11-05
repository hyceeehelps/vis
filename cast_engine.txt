"""cast_engine — STABLE, RECURRING CHARACTERS for the clipart factory.

THE PROBLEM THIS SOLVES
    `clipart_engine.person()` takes everything as raw arguments, so a recurring
    character only exists as a tuple of numbers copy-pasted into every scene:

        person(d, 540, 1500, 190, (70,110,180), f=f, seed=4101, hat='wig', ...)

    Miss the seed by one and the same character drifts. Forget the hat and it
    silently draws a stranger (that is how a bald "Newton" shipped in Ep.19).

THE RULE
    Identity is declared ONCE in `cast_defs.py`. Scenes may vary only
    pose / expression / position / size.

        from cast_engine import char
        char(d, 'law', 540, 1500, 190, f=f, pose='argue')

Guarantees
    * same name -> same colours, hat, head size, limb thickness, silhouette seed
    * the seed comes from the NAME, not from the call site, so the outline wobbles
      frame-to-frame exactly like the rest of the style but never re-rolls
      between scenes or episodes
    * a typo raises KeyError instead of putting a stranger in frame
    * `cast_sheet()` renders everyone side by side = the "no drift" QC image

CLI
    python3 cast_sheet.py                # writes cast_sheet.png at the repo root
"""
import os
import sys

sys.path.insert(0, os.environ.get('FACTORY_ROOT', os.path.dirname(os.path.abspath(__file__))))
import clipart_engine as ce

CAST = {}

# ---------------------------------------------------------------- poses ------
# Acting vocabulary. Keeps body language consistent across scenes/episodes too.
POSE = {
    'idle':  dict(arms=('down', 'down'),  lean=0.00, legs='stand'),
    'walk':  dict(arms=('down', 'down'),  lean=0.05, legs='walk'),
    'argue': dict(arms=('up', 'point'),   lean=0.08, legs='stand'),
    'point': dict(arms=('hip', 'point'),  lean=0.06, legs='stand'),
    'fist':  dict(arms=('fist', 'fist'),  lean=0.10, legs='stand'),
    'shrug': dict(arms=('up', 'up'),      lean=0.00, legs='stand'),
    'panic': dict(arms=('up', 'up'),      lean=-0.10, legs='walk'),
    'write': dict(arms=('point', 'hip'),  lean=0.12, legs='stand'),
    'guard': dict(arms=('musket', 'down'), lean=0.00, legs='stand'),
    'cheer': dict(arms=('up', 'up'),      lean=-0.05, legs='walk'),
    'sit':   dict(arms=('hip', 'hip'),    lean=0.04, legs='none'),
}

# Identity keys — locked after define(). Everything else is per-call acting.
IDENTITY = {'body', 'skin', 'hat', 'hatcol', 'seed', 'face', 'trim', 'size'}
ACTING = {'face', 'hat', 'arms', 'legs', 'lean', 'bob', 'trim', 'pose'}


class CastError(KeyError):
    pass


def define(name, **kw):
    """Register (or extend) a cast member. Runs `define()` once per character."""
    known = IDENTITY | {'arms', 'legs', 'lean', 'bob'}
    bad = set(kw) - known
    if bad:
        raise CastError(f"{name}: unknown identity key(s) {sorted(bad)} — "
                        f"allowed: {sorted(known)}")
    if 'seed' not in kw and name not in CAST:
        raise CastError(f"{name}: seed is required (it fixes the silhouette wobble)")
    if 'hat' in kw and kw['hat'] not in ce.HATS:
        raise CastError(f"{name}: unknown hat {kw['hat']!r} — known: {sorted(h for h in ce.HATS if h)}")
    if 'face' in kw and kw['face'] not in ce.FACES:
        raise CastError(f"{name}: unknown face {kw['face']!r} — known: {sorted(f for f in ce.FACES if f)}")
    CAST[name] = dict(CAST.get(name, {}), **kw)
    return CAST[name]


def char(d, name, x, y, s=None, f=0, **over):
    """Draw cast member `name` standing at (x, y = feet level).

    Only acting varies: pose/face/arms/legs/lean/bob plus position and size.
    Identity (body, skin, hat, seed, trim) is locked to cast_defs.py.
    """
    if not CAST:            # first call in a fresh process -> pull in cast_defs.py
        load_defs()
    if name not in CAST:
        raise CastError(f'"{name}" is not in the cast — define it once in cast_defs.py '
                        f'(known: {sorted(CAST)})')
    c = CAST[name]
    bad = set(over) - ACTING
    if bad:
        raise CastError(f'{name}: cannot vary {sorted(bad)} — identity is locked in '
                        f'cast_defs.py. Allowed per call: {sorted(ACTING)}')
    pose = POSE[over.pop('pose', 'idle')]
    face = over.pop('face', c.get('face'))
    if face not in ce.FACES:
        raise CastError(f'{name}: unknown face {face!r}')
    kw = dict(body=c.get('body', (250, 248, 244)),
              skin=c.get('skin', (255, 255, 255)),
              hat=over.pop('hat', c.get('hat')),
              hatcol=c.get('hatcol', (30, 32, 36)),
              trim=over.pop('trim', c.get('trim')),
              seed=c['seed'], f=f)
    # pose is the base; explicit overrides win
    for k, v in pose.items():
        kw[k] = v
    for k, v in over.items():
        if v is not None:
            kw[k] = v
    return ce.person(d, x, y, s or c.get('size', 160), face=face, **kw)


def group(d, names, y, f=0, spacing=None, s=None, poses=None):
    """Draw a row of cast members centred on the frame (crowd / delegation)."""
    spacing = spacing or (ce.W / (len(names) + 1))
    for i, n in enumerate(names):
        pose = (poses or {}).get(n, 'idle')
        char(d, n, spacing * (i + 1), y, s, f=f, pose=pose)


# ---------------------------------------------------------------- QC ---------
def load_defs(path=None):
    """Import the series cast file (safe to call repeatedly)."""
    import importlib.util
    path = path or os.path.join(os.environ.get('FACTORY_ROOT',
                                               os.path.dirname(os.path.abspath(__file__))),
                                'cast_defs.py')
    spec = importlib.util.spec_from_file_location('cast_defs', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cast_sheet(names=None, path='cast_sheet.png', per_row=4, cell=(320, 540)):
    """Render every cast member in a neutral pose — the one-image drift check."""
    from PIL import Image, ImageDraw, ImageFont
    if not CAST:
        load_defs()
    names = list(names or CAST)
    rows = (len(names) + per_row - 1) // per_row
    cols = min(per_row, len(names))
    img = Image.new('RGB', (cell[0] * cols, cell[1] * rows), ce.DAY_BG)
    font = ImageFont.truetype(ce.FONT_PATH, 26)
    for i, n in enumerate(names):
        tile = Image.new('RGB', cell, ce.DAY_BG)
        d = ImageDraw.Draw(tile)
        char(d, n, cell[0] // 2, cell[1] - 60, 175, f=0)
        ox, oy = (i % per_row) * cell[0], (i // per_row) * cell[1]
        img.paste(tile, (ox, oy))
        ImageDraw.Draw(img).text((ox + cell[0] // 2, oy + cell[1] - 22), n,
                                 font=font, fill=(28, 28, 30), anchor='mm')
    img.save(path)
    return path


if __name__ == '__main__':
    print(cast_sheet(path=sys.argv[1] if len(sys.argv) > 1 else 'cast_sheet.png'))
