# 🎭 Cast Demo — the same characters, 8 beats, zero re-invention

Proof that the factory now holds a **stable cast**. Every figure in this video comes from
`../cast_defs.py` via `char()`; not one scene invents a colour, a hat or a seed.

**Watch:** `Cast_Demo_Mississippi.mp4` — 38.6 s · 1080×1920 · 30 fps · H.264 + AAC
**Or look:** `preview_strip.png` — one frame per beat

| Beat | Who | Pose | What it shows |
|---|---|---|---|
| 1 | `law` | walk | the gambler arrives (same figure as beats 2, 5, 8) |
| 2 | `law` + `regent` | argue / point | two declared characters interacting |
| 3 | `clerk` | write | a minor role, still consistent |
| 4 | `villager`, `crowd`, `villager2` | panic / shrug / argue | `group()` for backgrounds |
| 5 | `merchant` + `law` | point / cheer | the "millionaire" burst |
| 6 | `duchess` + `sailor` | argue / shrug | |
| 7 | `newton` + `director` | write / point | the wig you recognise from Ep.19 — now with a face |
| 8 | `soldier` + `law` + `emperor` | guard / panic / point | cliffhanger trio |

Narration text is Ep.20 P1's real script so the badges and captions are house output. The demo
runs without voiceover (silent beats) on purpose — it isolates the cast, not the audio.

## Rebuild

```bash
cd cast_demo
python3 -c "import subprocess,sys"   # (no VO needed — silent beats)
# make 8 silent voN.mp3 clips, then:
FACTORY_ROOT=/home/user/vis python3 build_p1.py
```

## Where the characters live

- **`../cast_defs.py`** — one `define()` per character (body, skin, hat, hatcol, seed, default face)
- **`../cast_engine.py`** — `char()`, `group()`, `POSE`, and the locks that stop drift
- **`../cast_sheet.png`** — every cast member in a neutral pose (the drift check)
- **`../test_cast.py`** — automated anti-drift tests (`all checks passed` = safe to build)
- **`../CAST_GUIDE.md`** — how to add someone, what scenes may vary, the hat/face vocabulary

This file is the kit's `build_TEMPLATE.py` with only the CONFIG block edited — proof that adopting
the cast needs no change to the build pipeline at all.
