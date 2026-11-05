# 🔀 MERGE CHECK — Video Factory × Farm Survival

**Verdict: possible, and already proven.** A working prototype of the merged pipeline exists in
`survival/day2_demo/` — `Farm_Survival_Day2_Part1.mp4`, 22.37 s, **1080×1920 @30fps, H.264 CRF18 +
AAC 44.1k stereo**, house `PART 1` amber badge, house title card, 2-word amber-highlight captions,
brown-noise ambience, `+faststart`. It was produced by the *factory builder* from the *survival rig*,
not by either project's original renderer.

---

## 1. What each side actually owns

| Layer | Video Factory (paSTory) | Farm Survival |
|---|---|---|
| **Visual system** | white bg + flat-colour blobs + thick wobbly outlines (clipart engine) | hand-drawn farm panel, gradient sky presets, the **E red-pepper avatar** rig |
| **Shell / formatting** | 1080×1920 · 30fps · H.264 CRF18 + AAC 192k · **PART N / FINAL PART N** amber pill · title card 3.6 s · recap 5 s on parts 2+ · end card on finale · white/black fades · brown-noise ambience | 720×1280 · 24fps · **FARM SURVIVAL • DAY N** pill · burned subtitles at the bottom |
| **Structure** | 8 beats, hook→origin→escalation→consequence→aftermath→closer, min 2 parts, ≥5 s cliffhanger | 5–8 journal sentences, one panel per sentence, no parts |
| **Captions** | ASR-synced per word (Vosk → `align_vo.py`), 2-word chunks, amber keyword | character-count estimate → up to ~0.9 s drift |
| **Audio** | 1 VO clip per beat (TTS or supplied), atempo auto-squeeze, ambience bed | single VO track, 1.25× speed, 1.8 s lead, **9.5 s silent tail**, no bed |
| **POV / writing** | third-person narrator about a *historical event* | **first-person survival journal** ("I'm cold", "I need fire") about *E's day* |
| **Delivery** | `script.txt` + `upload.txt` + registry/queue/tracker/archive updates, retention cleanup | `README.md` + `WORKFLOW.md` + self-contained rebuild |

**The split you asked for is clean:** formatting/workflow/design → factory; avatar + POV → survival.
Nothing in the factory's assembler assumes clipart, and nothing in the survival rig assumes a slideshow.

---

## 2. Proven integration points (all built, all tested)

1. **`build_TEMPLATE.py` is now media-agnostic.**
   - `CANVAS` (default `1080×1920`), `RENDER_FPS`, `TITLE_Y`, `DRIFT`, `CAP_KW` are new CONFIG keys.
   - New optional hooks: `AN.ART` (an alternative art engine), `AN.PANEL_FN[i]` (a per-frame
     full-canvas renderer), `AN.BG[i]` (per-scene canvas colour).
   - `SCENE_TARGET` fixed to **43.5 s with recap / 48.5 s without**, matching the manual (was 44.5).
2. **`clipart_engine.render_scene()`** gained a `panel=` hook: another engine renders the whole frame,
   the factory still burns its captions on top, and `drift=` applies the factory's Ken-Burns push.
   `draw_caption()` gained `y_frac`, `max_w`, `scale` so house captions fit a 720-px-wide panel.
3. **`survival/rig.py`** is the Day 2 renderer minus its timeline/encoder, with motion + framing added:
   `scene_panel(d, f, n, t)`, per-frame flame phases, idle bob, rain (with ground splashes), wind,
   ember flicker, `camera_look()` (down/up/left/right reframes), `env['zoom']`, cached backgrounds.
4. **`survival/day2_demo/anim_part.py`** is an ordinary factory `anim_part.py` — `SCENES / PANELS /
   BEATS / NIGHT / CAP_CHUNK` — that points at the rig. **This is the whole merge contract: a part
   is a beat list + a panel config per beat.**
5. **End-to-end build verified:** 6 beats, auto rate 1.000, badge, title, captions, ambience, mux.

### Motion result
| | frozen frames | median frame diff |
|---|---|---|
| Original Day 2 | **94.8 %** (a slideshow with 6 crossfades) | 0.000 |
| Merged Part 1 | **63.6 %** (strict 0.02 threshold at 180×320) | 0.009 |

Visible now: rain + splashes, drifting clouds, grass sway, walking legs, flame flicker with glow,
5 % camera push, per-beat reframe, fades. Still cheap to render (~100 s for 22 s of video).

---

## 3. Friction — what has to be decided, not coded

| # | Issue | Why it matters | Recommendation |
|---|---|---|---|
| 1 | **POV vs history** | The factory's beats are written *about an event*; survival is *E's first-person journal*. Merging the format with a real historical event needs a framing decision: is E a **witness/narrator inside the event**, or do we keep survival as its own series? | Keep **two series on one pipeline**: `paSTory` (history, E absent) and `Farm Survival` (E's POV, no history). The merge is *tooling + formatting*, not topic-blending. If you do want E in a history story, make him a period-costumed narrator — cost: a new hat/prop set on the rig. |
| 2 | **Canvas** | Panels are natively **720×1280**; the house spec is **1080×1920**. The builder upscales (confirmed in the demo), which softens the line art ~1.5×. | Keep 1080×1920 delivery (platform-safe) and **render the rig at 1080×1920** (all coordinates in `rig.py` are multiples of 720/1280 — a uniform ×1.5 pass). Demo keeps the upscale so it stays a fair 1:1 test. |
| 3 | **Two subtitle systems** | The rig burns its own subtitles; the factory burns ASR captions on top. Both at once = double text. | Factory wins: pass `caption=None` in art-engine mode (done in `scene_panel`), keep the rig's `subtitle_portrait()` only for standalone survival builds. |
| 4 | **Voice gate (blocker for production here)** | House TTS tool is absent in this sandbox and the sanctioned stand-in (edge-tts `en-US-GuyNeural`) can't reach `speech.platform.bing.com`. | Nothing to code: **supply the VO** (or run this in an account where TTS works) and the exact same builder will render. The demo uses your own `voiceover_1_25x.mp3`, so the audio path is already proven. |
| 5 | **ASR captions unavailable** | `align_vo.py` needs Vosk + the model from alphacephei.com — unreachable here (pip-installable vosk is, model isn't). Demo fell back to the weighted estimator (sync within ~1 chunk). | Production build in a normal account = true sync. Optionally add a "measure real sentence pauses with numpy RMS" fallback, which is what I used to cut the VO for the demo — cheap, no network. |
| 6 | **Burned title vs factory title** | The rig draws `FARM SURVIVAL • DAY 2` inside the panel; the factory draws its own title card at `TITLE_Y`. | `title_badge_portrait(img, label=None)` now takes a label, and the builder's title card sits at `TITLE_Y=0.14` clear of the `PART 1` pill (QC'd). Standalone builds keep the rig pill; factory parts can pass `show_title=False`. |
| 7 | **Episode/day semantics** | Factory = parts of one story (P1→P2 recap, finale end card). Survival = days of one season (Day 1→Day 2…). | Same mechanic, different label: `DAY N` badge instead of `PART N`, `RECAP_SRC = ../day<N-1>/…`, and the **finale** = end of a season → end card. One-line change in `make_badge` label + CONFIG. |
| 8 | **Repo weight** | Your zip is 17 MB (16.9 MB of it media). Committing per-day renders will blow the 128 MB cap fast. | Keep the repo to **code + small art** (~1 MB: `assets/` E layers + barn). Big media (mp4, VO, avatar_source 7.9 MB) stays out via `.gitignore` / external storage. Duplicate `assets/` copies also fold into one. |

---

## 4. What a production part looks like after the merge

```
<slug>_video/part1/
├─ anim_part.py        # 8 beats + PANELS (pose/prop/weather/look/env)   ← survival grammar
├─ build_p1.py         # build_TEMPLATE copy, CONFIG only                 ← factory grammar
├─ vo/1/vo1.mp3 … vo/8/vo8.mp3
└─ Farm_Survival_Day3_Part1.mp4   +  upload.txt  +  script.txt
```

Run: `FACTORY_ROOT=/home/user/vis SURVIVAL_ASSETS=…/survival/assets python build_p1.py`
Builds: frames → segs → concat → badge/title/end-card overlay → fades → ambience → `+faststart`,
squeezed to ≤49.9 s, then QC strip, then `upload.txt` in the house playbook (2 emojis, year/place,
`#WeirdHistory` block) — the full factory delivery ritual applies unchanged.

---

## 5. Bottom line

- **Design/formatting/workflow from the factory: yes, 100 % reusable** (badges, title/end cards,
  recap funnel, 48–50 s pacing, captions, ambience, QC, metadata, retention rules).
- **Avatar + POV from survival: yes, portable** — it becomes `rig.py` + a beat/panel table.
- **Two real frictions:** the POV decision (§3.1) and the voice gate (§3.4). Everything else is already
  wired and demonstrated in `survival/day2_demo/`.
- **Next step on your word:** render the rig natively at 1080×1920, then build a full 8-beat
  Day 3 part (≈49 s) the moment VO is available.
