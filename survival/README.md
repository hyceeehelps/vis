# 🍅 Farm Survival — E avatar series on the Video Factory pipeline

The **survival** half of the merge: the E red-pepper avatar rig, the hand-drawn farm panel, and the
first-person survival-journal POV. The **formatting/workflow** half (part structure, badges, title
cards, recap, captions, ambience, QC, upload metadata, retention) comes from the factory kit one
level up: `build_TEMPLATE.py`, `clipart_engine.py`, `align_vo.py`, `PROCESS_STEPS.md`.

Design notes, friction list and the demo verdict: **`../MERGE_PLAN.md`**.

## Files

| Path | What it is |
|---|---|
| `rig.py` | The Day 2 renderer, art half only: `make_character()`, `background_portrait()`, `scene_frame_day2_portrait()`, the factory hook `scene_panel(d, f, n, t)`, camera reframes (`camera_look`), and motion layers (`env_overlay`: rain + splashes, wind, embers). |
| `assets/` | E rig PNGs (1280×832 canvas: limbs, body, stem, faces, mouths), the barn doodle, and the Day 2 narration. |
| `day2_demo/anim_part.py` | The merge contract: a normal factory `anim_part.py` (`SCENES / NIGHT / BEATS / CAP_CHUNK`) whose art comes from `rig.py` via a `PANELS` table. |
| `day2_demo/build_p1.py` | A `build_TEMPLATE.py` copy with only the CONFIG block edited. |
| `day2_demo/Farm_Survival_Day2_Part1.mp4` | Proof build: 22.37 s, 1080×1920 @30fps, H.264 CRF18 + AAC stereo, house badge + captions. |

## Build a part

```bash
# 1. one panel config per beat in anim_part.py:
#    dict(pose=COLD, prop='broken', weather='dawn', look='down', env={'rain':True,'wind':True})
# 2. vo/1/vo1.mp3 … vo/8/vo8.mp3  (one clip per beat — same as the factory)
# 3. copy the template, edit CONFIG only, run it:
cp ../build_TEMPLATE.py day3_demo/build_p1.py
cd day3_demo
FACTORY_ROOT=/home/user/vis SURVIVAL_ASSETS=/home/user/vis/survival/assets \
  python build_p1.py
```

`build_TEMPLATE.py` handles the rest: title card (`TITLE_Y`), `PART N` badge, 5 s recap on parts 2+,
end card on the finale, ASR caption alignment, squeeze to ≤49.9 s, segmented render → concat →
overlay → fades → brown-noise ambience → `+faststart`.

## Panel config keys

| key | values | effect |
|---|---|---|
| `pose` | face `sad/surprised/neutral/happy`, mouth `closed/frown`, `arm_left/right`, `leg_left/right` angles | limb/expression puppet |
| `prop` | `cold`, `broken`, `water`, `wood`, `fire`, `fire_hold` | scene prop (broken fence, cloudy bucket, dry wood, fire + pot) |
| `weather` | `dawn`, `morning`, `cloudy`, `storm`, `dusk` | sky gradient + cloud style |
| `look` | `center`, `down`, `up`, `left`, `right` | camera reframe (this is the survival equivalent of the factory's zoompan) |
| `env` | `rain`, `wind`, `embers`, `rain_strength`, `zoom`, `bob` | animated overlays + Ken-Burns push |

## Notes

- **Do not** burn the rig's own `subtitle_portrait()` when the factory burns captions — double text.
  `scene_panel()` already passes `caption=None`.
- Panels are natively 720×1280. The builder upscales to 1080×1920; for maximum sharpness render the
  rig natively at 1080×1920 (uniform ×1.5 on the panel constants).
- `assets/` here is de-duplicated against the original transfer zip (`avatar_source/E_assets` was
  byte-identical). Big media stays out of git via the root `.gitignore`.
