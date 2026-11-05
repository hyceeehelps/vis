"""MERGE DEMO — Farm Survival Day 2 in the VIDEO FACTORY's part format.

This file is the whole point of the merge: it is a normal factory `anim_part.py`
(SCENES / NIGHT / BEATS / CAP_CHUNK, exactly like SAMPLE_anim_part.py), except the art
comes from the SURVIVAL rig (`../rig.py`) instead of `clipart_engine` primitives.

  Factory supplies:  part structure, badges, title/end card, recap, ASR caption sync,
                     squeeze-to-49.9s pacing, segmented ffmpeg assembler, QC, delivery.
  Survival supplies: the E avatar rig, the hand-drawn farm panel, and the POV
                     (first-person survival journal: cold, thirsty, needs fire).

Demo scope: 6 beats using ONLY the narration that exists in the supplied voiceover
(the original 5 sentences, split at the real pause after "…after the rain.").
A production part uses 8 beats of ~5.5s narration and tops out at ~49.x s.

Panel keys consumed by rig.scene_panel():
  pose    : face/mouth/arm_left/arm_right/leg_left/leg_right angles
  prop    : 'cold' | 'broken' | 'water' | 'wood' | 'fire' | 'fire_hold'
  weather : 'dawn' | 'morning' | 'cloudy' | 'storm' | 'dusk'
  look    : 'center' | 'down' | 'up' | 'left' | 'right'   (camera reframe = our zoompan)
  env     : {'rain':True,'wind':True,'embers':True,'rain_strength':1.0,'bob':px}
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # repo root
sys.path.insert(0, os.environ.get('FACTORY_ROOT', ROOT))
sys.path.insert(0, os.path.join(ROOT, 'survival'))   # rig.py lives in survival/
import rig                     # survival art + E avatar rig

ART = rig                      # tells build_TEMPLATE this part renders full panels
CAP_CHUNK = 2                  # house default: 2-word ASR-synced captions

# ---------------------------------------------------------------- poses -------
COLD   = {'face': 'sad',       'mouth': 'frown',  'arm_left': 42,  'arm_right': -42, 'leg_left': 5,   'leg_right': -5}
FENCE  = {'face': 'surprised', 'mouth': 'frown',  'arm_left': -8,  'arm_right': 48,  'leg_left': 12,  'leg_right': -10}
WATER  = {'face': 'sad',       'mouth': 'frown',  'arm_left': 8,   'arm_right': 52,  'leg_left': -4,  'leg_right': 5}
WOOD   = {'face': 'sad',       'mouth': 'frown',  'arm_left': -43, 'arm_right': -5,  'leg_left': -8,  'leg_right': 8}
FIRE   = {'face': 'neutral',   'mouth': 'closed', 'arm_left': 10,  'arm_right': 35,  'leg_left': -5,  'leg_right': 5}

# ---------------------------------------------------------------- panels ------
PANELS = [
    # 1 — dawn after the storm: wet ground, broken fence, E still shivering (hook)
    dict(pose=COLD,  prop='broken', weather='dawn',   look='down',   env={'rain': True, 'wind': True, 'rain_strength': 0.6}),
    # 2 — the fence: something could get in, or out
    dict(pose=FENCE, prop='broken', weather='cloudy', look='right',  env={'wind': True}),
    # 3 — the water is still cloudy (push in on the bucket)
    dict(pose=WATER, prop='water',  weather='cloudy', look='up',     env={'wind': True, 'zoom': 1.12}),
    # 4 — can't drink it like this: I need fire
    dict(pose=WATER, prop='water',  weather='cloudy', look='center', env={'wind': True, 'zoom': 1.05}),
    # 5 — dry wood is hard to find after the rain
    dict(pose=WOOD,  prop='wood',   weather='cloudy', look='left',   env={'wind': True}),
    # 6 — but a few pieces under the barn roof: the flame catches
    dict(pose=FIRE,  prop='fire',   weather='dusk',   look='center', env={'embers': True}),
]

BG = [(252, 250, 246)] * len(PANELS)      # factory canvas colour (panel covers it anyway)
NIGHT = [False] * len(PANELS)

BEATS = [
    ["Day", "2.", "The", "storm", "didn't", "stop", "until", "morning.", "I'm", "cold,",
     "and", "my", "hands", "won't", "stop", "shaking."],
    ["The", "fence", "is", "broken.", "Something", "could", "get", "in.", "Or", "out."],
    ["That", "water", "from", "yesterday", "is", "still", "cloudy."],
    ["I", "can't", "drink", "it", "like", "this.", "I", "need", "fire."],
    ["Dry", "wood", "is", "hard", "to", "find", "after", "the", "rain."],
    ["But", "I", "find", "a", "few", "pieces", "under", "the", "barn", "roof."],
]


def _scene(i):
    """Factory scene signature (d, f, n, t) -> the rig-drawn panel for beat i."""
    def fn(d, f, n, t):
        rig.PANEL = PANELS[i]
        return rig.scene_panel(d, f, n, t)
    return fn


def _panel(i):
    """Same panel for the whole-canvas hook the builder pastes in (f, n, t)."""
    def fn(f, n, t):
        rig.PANEL = PANELS[i]
        return rig.scene_panel(None, f, n, t)
    return fn


SCENES = [_scene(i) for i in range(len(PANELS))]
PANEL_FN = [_panel(i) for i in range(len(PANELS))]
