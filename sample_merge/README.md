# 🧪 Merge Sample — Farm Survival × Video Factory

This folder is the **working proof** that the two pipelines can be one: the factory's formatting,
workflow and delivery shell, wrapped around the survival avatar and its first-person POV.

**Watch:** `Farm_Survival_Day2_Part1.mp4` — 22.37 s · 1080×1920 · 30 fps · H.264 CRF18 + AAC 44.1k stereo
**Or look:** `preview_strip.png` — 8 frames from the render (badge → title → panels → dusk fire → closer)

| | Original Day 2 (your zip) | This sample (merged) |
|---|---|---|
| Canvas / fps | 720×1280 · 24 fps | **1080×1920 · 30 fps** (house spec) |
| Audio | AAC **mono** 44.1k | **AAC stereo** 44.1k |
| Shell | none | **PART 1 amber badge + title card + fades + brown-noise ambience** |
| Captions | 5 burned cues, char-count estimate (up to ~0.9 s drift) | **per-beat captions, 2-word chunks, amber keyword** |
| Motion | 94.8 % frozen frames (6 crossfades) | **63.6 % frozen** (rain, splashes, clouds, grass, flame flicker, 5 % push, per-beat reframe) |
| Structure | 5 sentences, one panel each | **6 beats → part 1 of N**, cliffhanger-shaped |

---

## What's in here

| File | What it is |
|---|---|
| `Farm_Survival_Day2_Part1.mp4` | the rendered sample |
| `preview_strip.png` | contact strip of that render |
| `anim_part.py` | **the part definition** — the whole merge contract: `BEATS` (one line of POV narration per beat), `PANELS` (pose/prop/weather/look/env per beat), `SCENES`/`PANEL_FN` adapters |
| `build_p1.py` | the factory builder (`build_TEMPLATE.py`) with **only the CONFIG block edited** |
| `vo/1/vo1.mp3 … vo/6/vo6.mp3` | one narration clip per beat, cut from the supplied Day 2 voiceover at its real sentence pauses |

Art + avatar come from `../survival/` (`rig.py`, `assets/`). Formatting + assembler come from the
repo root (`build_TEMPLATE.py`, `clipart_engine.py`, `align_vo.py`).

---

## Rebuild it

```bash
cd sample_merge
FACTORY_ROOT=/home/user/vis SURVIVAL_ASSETS=/home/user/vis/survival/assets \
  python build_p1.py
```

Needs: `imageio-ffmpeg`, `pillow`, `numpy`, `opencv-python-headless` (see `../survival/README.md`).
Output: `Farm_Survival_Day2_Part1.mp4` ≈ 22.4 s. Frames/segs are scratch and are deleted by the builder.

To do a **full-length house part** (≈49 s), write 8 beats of ~5.5 s narration each into
`vo/N/voN.mp3`, extend `BEATS` + `PANELS` to 8 entries, set `N = 8` and
`GAPS = [0.2]*7 + [1.2]` in `build_p1.py`. Everything else — badge, title, recap on part 2+,
end card on the finale, caption sync, squeeze-to-≤49.9 s, ambience, QC — is already handled.

## Why it's 22 s and not 49 s

The supplied voiceover is 20.25 s of speech (25.31 s original at 1.25×). The factory format wants
8 beats ≈ 44 s of narration, so this sample re-cuts the existing audio into 6 beats and runs at
rate 1.000. **No new narration was generated** — the voice gate in this sandbox is closed
(no house TTS tool, and edge-tts `speech.platform.bing.com` is unreachable). Give it 8 fresh VO
clips and the same builder produces a real 48–50 s part.

## The merge in one paragraph

A factory part is `8 beats + a scene function per beat + payload builder`. A survival panel is
`one pose/prop/weather/camera config`. So a survival beat is just a factory beat whose scene
function is "render the E panel for this config" — `rig.scene_panel(d, f, n, t)` — and the factory
keeps doing what it already does well: cadence, badges, captions, recap funnel, QC, upload metadata.
See `../MERGE_PLAN.md` for the full friction list (POV scope, native 1080p rig, one-subtitle rule,
voice gate, repo weight).
