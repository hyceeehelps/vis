# 🎭 STABLE CAST — stop re-inventing characters every episode

**The rule in one line:** a character that appears more than once is declared **once** in
`cast_defs.py` and drawn with `char()`; scenes may change only pose, expression, position and size.

Before this, "John Law" existed as a tuple of numbers copy-pasted into each scene function —
`person(d, 540, 1500, 190, (70,110,180), seed=4101, hat='wig')`. Miss the seed and he drifts.
Forget the hat and the engine silently draws a stranger (that is how Ep.19 shipped a **bald Newton**:
`hat='wig'` didn't exist yet, and unknown hats fell through every `if/elif`).

---

## Files

| File | What it is |
|---|---|
| `cast_defs.py` | **The cast.** One `define()` per character: body colour, skin, hat, silhouette seed, default face. Edit here to change someone forever. |
| `cast_engine.py` | `define()`, `char()`, `group()`, `POSE`, `cast_sheet()`. Enforces that identity can't be edited at the call site. |
| `cast_sheet.py` | `python3 cast_sheet.py` → `cast_sheet.png`, everyone in a neutral pose. Run after every cast edit. |
| `test_cast.py` | `python3 test_cast.py` → anti-drift checks (stable identity, free pose, no strangers, valid vocabulary). |
| `cast_demo/` | Proof: 8 beats of Ep.20 P1's narration, every figure from the cast, built by the real `build_TEMPLATE.py`. |

---

## Add a character (30 seconds)

```python
# cast_defs.py
define('newton', body=(92, 76, 60), hat='wig', hatcol=(214, 210, 200), seed=4103)
```

```bash
python3 cast_sheet.py     # eyeball the sheet — colours, hat, no face covered
python3 test_cast.py      # identity locks, vocab valid
```

Use it in a scene:

```python
char(d, 'newton', 540, 1500, 195, f=f, pose='write')
char(d, 'newton', 700, 1520, 195, f=f, pose='shrug', face='worried')
```

**Seed rule:** pick a stable number per character (4xxx range, one block per era) and never change it —
the seed drives the hand-drawn wobble, so re-rolling it re-rolls the face and the limb joints.

## What scenes may vary

| Allowed per call | Values |
|---|---|
| `pose` | `idle` `walk` `argue` `point` `fist` `shrug` `panic` `write` `guard` `cheer` `sit` |
| `face` | `smile` `open` `flat` `sad` `angry` `cool` `smug` `worried` |
| `arms` / `legs` / `lean` / `bob` | explicit override of the pose |
| `x`, `y`, `s` (size), `f` | position and scale |

Everything else — `body`, `skin`, `hat`, `hatcol`, `seed`, `trim` — is **locked** and raises
`CastError` if a scene tries to change it. That is the whole point: no silent drift, no strangers.

## Hat / face vocabulary (engine-enforced)

```
HATS  : tricorne shako fez furcap turban tophat wig bonnet cap
FACES : smile open flat sad angry cool smug worried
ARMS  : down up point hip fist musket
LEGS  : stand walk none
```
A typo now raises `ValueError` from `person()` instead of drawing nothing. If a story needs a new
hat (a stovepipe, a mitre, a helmet), add the branch to `clipart_engine.person()` **and** the name to
`HATS` in the same edit.

## Cast sheet = the QC gate

`cast_sheet.png` is committed. After any cast change, regenerate it and look at it: that image is
how you catch a hat that covers the eyes before it reaches 750 rendered frames.

## Current cast (Ep.19/20 era)

`law` `regent` `newton` `director` `clerk` `duchess` `sailor` `soldier` `merchant` `merchant2`
`emperor` `admiral` + extras `villager` `villager2` `crowd`.

Extras are for background rows (`group(d, ['villager','crowd','villager2'], 1560, f=f)`) and are
interchangeable; named cast members are not.
