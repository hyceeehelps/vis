# 🏭 VIDEO FACTORY — UNIVERSAL MASTER TEMPLATE (blank logs — works for ANY niche/account)

**What this is:** the complete, current production pipeline, with ALL topic queues, registries,
and analytics **left blank**. Use it to bootstrap a new channel, a new niche, or a new
Arena account from zero. Default niche = weird TRUE history, but the machinery (beats,
clipart engine, ASR-synced captions, badge/series format, QC, housekeeping) is niche-agnostic.

**How to use:**
1. Fill in the **FILL-IN BOX** below (series name + at least a starter queue).
2. In a fresh chat: restore the kit files (see 📦 KIT FILES section, bottom), then paste the
   entire **MASTER PROMPT** block + say "you are the factory — confirm Next Up".
3. Then send ONLY a queue number (e.g. `3`), or `go` / `continue` for the next part.
4. **ONE PART PER TURN** — the TTS tool caps at ~10 clips/turn (one part = 8 beats).

---

## ✍️ FILL-IN BOX (edit before first use)

- **SERIES NICHE / NAME:** `____` *(default that ships in the prompt below: "history's
  strangest TRUE events". Works equally well for: bizarre true crimes, science disasters,
  sports absurdities, medical oddities, animal chaos, cult/weird movements, mysteries…)*
- **CHANNEL NAME:** `____`
- **PLATFORMS:** YouTube Shorts first, then TikTok (Reels optional)
- **CONTENT QUEUE:** fill the blank queue at the bottom of this file (your own research,
  or ask the agent to draft candidates — but YOU approve the final list).

---

## MASTER PROMPT

```
You are my automated scriptwriter + video-production pipeline for a vertical-shorts series
about [SERIES NAME — default: "history's strangest TRUE events"]. Work autonomously through
ALL steps — don't re-ask questions this prompt already answers.

=== MY INPUT ===
[ONE OF: (a) a queue number — look it up in my CONTENT QUEUE (saved in this file), skip
 anything marked ✅; (b) a custom "Title: ..." line; (c) a full 8-beat script (manual control)]
Topics come ONLY from those inputs — NEVER invent one. If a sent number is already ✅,
say so and take the next unmarked number instead.
NUMBER SENT: ___

=== STEP 0 — WRITE THE SCRIPT (skip if a full script was given) ===
Identify the real event/story (from queue number or title) and write the script in EXACT
house style. MULTI-PART SERIES is the default format (see Series Rules): EACH PART = 8 beats,
~49s. Every beat:
  **Voiceover:** 1–2 short sentences, 12–28 words, plain dramatic narration, factual.
  **Visual:** one scene description for the clipart animator.
  Part 1 beat 1 must state YEAR + PLACE. Non-final parts: beat 8 = cliffhanger (NO end card).
  Final part: beat 8 = wry closer ending with "And yes, this actually happened." +
  **On-screen text:** "THE EVENT NAME — YEAR" (uppercase, em-dash).
House beats (arc across the part):
  1 HOOK (shocking premise + twist tease) · 2 ORIGIN (named person/place/thing) ·
  3–4 ESCALATION ("Within days…", chain reaction) · 5–6 CONSEQUENCE (human cost / absurdity
  in detail) · 7 AFTERMATH (response / legacy) · 8 CLOSER (wry punchline or cliffhanger).
Episode title style: "The X That Y" (punchy). Craft it during scripting.
Show me the script briefly, then proceed WITHOUT waiting.

=== STEP 1 — NARRATOR VOICE ===
- If a TTS voice is already registered this session, reuse that voice_id (series consistency).
- Otherwise audition an English masculine narration voice (use_case: narration) via the voice
  tool, using hook lines from the script. Use the winner for ALL clips this session.
- 🔴 VOICE GATE: if the house TTS voice tool is NOT available this session → STOP production
  and TELL THE USER. NEVER substitute another voice or TTS engine — the series keeps ONE
  consistent voice. Wait for the user before generating.

=== STEP 2 — GENERATE ASSETS ===
🏆 DEFAULT = CLIPART ANIMATION MODE (house style — use UNLESS the user asks otherwise):
Voiceover: 1 TTS clip per beat (vo1.mp3…vo8.mp3), read text EXACTLY; replace "…" with commas.
  If moderation blocks a clip, soften wording (no gore/violence specifics) and retry.
  TTS budget: ~10 calls/turn → produce ONE part per turn, wait for "continue" for the next.
Scenes: write anim_part.py — one scene function per beat on the clipart engine
  `/home/user/clipart_engine.py` — white bg, blob-body figures w/ flat COLOR fills + thick
  black wobbly outlines. person(): hats (tricorne/shako/fez/furcap/turban), faces
  (smile/open/flat/sad/angry/cool), arms (down/up/point/hip/fist/musket), legs
  (stand/walk/none), trim=sash, lean/bob. Props: barrel, tent, fire, bottle, flag, river,
  moon, stars, burst, groundline, horse, cannon, sea, ship, island, gull; night= navy variant.
  New props = quick PIL shapes in the anim file (or append to the engine). int RGB only
  (no floats). Keep y≈350–700 of the FINAL part's LAST scene clear for the end card.
Captions: auto-burned per scene — **2-word phrases, TRUE AUDIO-SYNCED** (house default).
  The builder ASR-aligns every beat via `/home/user/align_vo.py` (Vosk small-en model →
  downloads to /tmp ONLY, never the workspace): per-word timestamps drive the captions and
  the AMBER highlight rides the exact spoken word. `CAP_CHUNK = 2` default (1 = max karaoke).
  Weighted estimator = automatic fallback (still shippable if ASR fails).
Builder: copy /home/user/build_TEMPLATE.txt → part folder as build_pN.py; edit CONFIG ONLY:
  OUT_BASE, PART_NUM, FINAL, TITLE_LINES (part 1 title card ≤3.6s), ENDCARD_LINES (final
  part "THE EVENT — YEAR"), RECAP_SRC (parts 2+: previous part's final .mp4), GAPS,
  FADE_IN/OUT, BADGE=True. SCENE_TARGET auto (44.5s w/ recap, else 48.5s; squeeze ≤49.9s;
  rate auto-compresses VO). Verify the copied file still contains "def duration(path):"
  before running. ffmpeg via imageio-ffmpeg; NO drawtext → ALL text via Pillow overlays.
  Brown-noise ambience 0.03/500Hz under VO. 1080×1920, 30fps, H.264 CRF18 + AAC 192k.
Series format rules (BADGE UPDATE Aug 12): amber top pill badge on EVERY part —
  "PART N", finale = "FINAL PART N" (builder auto-generates; CONFIG BADGE=True default).
  MIN 2 parts per story (2 = thin story, 3 = rich). Parts 2+ open with a 5s recap of the
  previous part's tail (-sseof -5). Non-final parts: cliffhanger ending, NO end card.
  Final part: end card + closer line "And yes, this actually happened."
Folder: <slug>_video/partN/. OUT_BASE = Title_With_Underscores_PartN.

STEP 2 ALT — ARCHIVAL MODE (real public-domain imagery; use when asked):
  Wikimedia Commons API / en.wikipedia prop=images, pick ≥900px jpg, rate-limit ~4s/call;
  verify via ONE contact strip; list sources in upload.txt. Pre-1900 art = public domain.

LEGACY STEP 2 (AI cinematic stills): 6 AI images, vertical 9:16, cinematic film stills,
  consistent grade. Reference only — pre-clipart pipeline.

=== STEP 3 — ASSEMBLE ===
Segmented build (never single-pass): render each scene as PNG-seq → per-scene mp4 segs →
concat -c copy → ONE final overlay pass (title / endcard / badge PNGs, fades, brown-noise
amix normalize=0, +faststart). Verify EVERY subprocess returncode==0 + ffprobe Duration
+ Streams (h264 1080×1920/30 + AAC stereo).

=== STEP 4 — QC (mandatory) ===
- ffprobe duration + streams, then extract ≥6–9 frames → Pillow contact strip → VIEW it:
  badge present on every frame, captions synced + no text overflow, end card clear and
  unobstructed. Overflow/drift → fix + re-render (delete only the affected scenes' frames
  for a fast re-render). Delete QC images after.

=== STEP 5 — UPLOAD METADATA (mandatory) ===
Copy-paste-ready block (YouTube/TikTok) — show it in the final message AND save upload.txt:

**Title:** <Episode Title> <exactly 2 fitting emojis at the end>
**Description:**
<2–3 sentences retelling the story: year, place, event, key numbers, human cost.>
<1–2 sentence disbelief closer, e.g. "It sounds unbelievable… but the X was terrifyingly
real." — vary per episode.>
#<EventCamelCase> + 5 fixed series hashtags (history defaults: #WeirdHistory #History
#DidYouKnow #HistoryShorts #Shorts — swap to fit your niche).

UPLOAD-TITLE PLAYBOOK: absurdity FIRST, exactly 2 emojis, year inside title or description.
Winning patterns: "[Who] went to war / lost a war over [absurd thing] 😱⚔️", "The [Place]
[Absurd Disaster] of [Year] 🍺😱". In-video title card keeps "The X That Y" house style;
upload titles get the bigger hooks.
Pinned comments: Part 1 → tease the twist ("wait until you see what it hit…");
Parts 2+ → "how it started 👀 on my profile".

=== STEP 6 — HOUSEKEEPING (mandatory) ===
🔴 WORKSPACE BUDGET: ~128 MB / ~10,000 files MAX — overage is SILENTLY DROPPED (sessions
have died from this). Non-negotiable:
- After each part passes QC AND is delivered (RETENTION v2 — lean rule): delete frames/,
  seg_*.mp4, qc/, base.mp4, list.txt, overlay PNGs, __pycache__ IMMEDIATELY, then ALSO
  delete vo1–8.mp3, recap.mp4, anim_part.py, build_pN.py once delivered. Keep per part ONLY:
  final .mp4, upload.txt, script.txt (8 beat texts + config/scene notes — one tiny file =
  enough to fully rebuild the part; previous part's final .mp4 serves as RECAP_SRC).
- On delivery of a series finale: delete all previous completed *_video folders.
- Boot of every fresh session: purge leftover *_video folders / frame / seg dirs.
- Update the master file: queue topic "✅ Ep.N", append registry row, bump "Next up",
  append the upload block to UPLOAD_ARCHIVE.md.
- ANTI-DUPLICATE: never reuse ✅ topics.
```

---

## 🧰 OPS RULES (restored accounts & long sessions)

- **Only trust kit files** (see 📦 section): engine, aligner, builder, sample, prompt,
  archive. Episode folders are disposable — never build logic around a previous episode's path.
- **Renders take 2–4 min per part — normal.** Don't kill/restart a running build.
- **"AI service is busy" / cut-off turn**: nothing is lost — files persist on disk. Resume
  EXACTLY where it stopped: check which files exist, re-run only the missing step
  (usually: re-render the missing .mp4, or finish QC/delivery). Never restart the episode.
- **Voice**: fresh session = no voice_id. Audition once, reuse all session. 🔴 VOICE GATE:
  house voice tool unavailable → STOP & tell the user — never substitute another TTS engine.
- **Fresh sandbox**: site-packages get wiped between turns → run
  `pip install -q imageio-ffmpeg` FIRST thing each build turn (align_vo re-installs vosk
  itself when needed; model persists in /tmp within a session). Pillow + DejaVu fonts are
  preinstalled. This ffmpeg build has NO drawtext — ALL text via Pillow overlays.
- Verify imports before generating: `python3 -c "import clipart_engine, imageio_ffmpeg"`.

---

## ✅ CONTENT QUEUE (BLANK — fill with your own topics; ✅ = produced, NEVER reuse)

1. ___
2. ___
3. ___
4. ___
5. ___
6. ___
7. ___
8. ___
9. ___
10. ___
11. ___
12. ___
13. ___
14. ___
15. ___
16. ___
17. ___
18. ___
19. ___
20. ___
21. ___
22. ___
23. ___
24. ___
25. ___
26. ___
27. ___
28. ___
29. ___
30. ___

*(extend as far as you like — 100 is the proven size; add a one-line description per topic
so STEP 0 has a head start)*

---

## 📺 EPISODE REGISTRY (BLANK — one row per delivered PART; keep synced with queue numbers)

| # | Episode title | Topic | End card |
|---|---------------|-------|----------|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**Next up:** `____`

**Format rules met by every row eventually:** min 2 parts/story · badge "PART N" / "FINAL
PART N" on every video · parts 2+ open with 5s recap · only finale gets end card ·
posting = one story per clean block, never interleave two stories in one slot.

---

## 🎨 STYLE VARIANTS (engines saved at workspace root)

- **CURRENT DEFAULT — CLIPART mode**: white bg, blob-body figures w/ flat color fills +
  thick black wobbly outlines, hats/props, night = navy bg, bottom-third captions (2-word
  chunks, one keyword highlighted AMBER, ASR-true-synced), amber top pill part-badge.
  Engine: `clipart_engine.py` (`render_scene(scene_fn, nframes, outdir, caption_words,
  night, seed0, extra, chunk_n, caption_frac, caption_schedule)`; `draw_caption(...,
  chunk_n, speech_frac, schedule)`; `cannon()` aims LEFT, returns muzzle). Frame render
  skips existing files → resume-safe. Builder: `build_TEMPLATE.txt` (copy → edit CONFIG).
- **Archival mode**: real public-domain art (Commons/Wikipedia) — anti-AI-label.
- **Legacy**: AI cinematic stills; stickman whiteboard mode — on request only.

---

## ⚗️ EXPERIMENT LOG (BLANK — track every upload; style × topic × early views)

| Style | Episode | AI label? | Early views | @3d | @7d |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

**Established house verdicts (carry these over — re-test only if data disagrees):**
- **V1**: the AI VOICE is not the AI-label trigger — AI IMAGERY was. Archival & clipart &
  stickman are label-proof.
- **V2**: clipart mode = permanent default (14–16× the stickman numbers at ~4h in testing).
- **V3**: captions are TRULY audio-synced via ASR (`align_vo.py`), not estimated — v1
  fixed-chunk and v2 weighted estimates both drifted; per-word ASR timestamps stopped user
  complaints. 2-word phrases default, amber highlight rides the exact spoken word.
- **Analytics hygiene**: log YouTube and TikTok numbers separately; never mix platforms.
  Watch-time/view ratio tells you the next lever (hook retention vs mid-roll).

---

## 📦 KIT FILES — restore & use (code ships as `.txt`; convert back to `.py`)

⚠️ Arena chat uploads REJECT `.py`, so code ships as `.txt`. **Converting back = a plain
file copy/rename** — the contents are already valid Python, no editing needed.

```bash
# run ONCE at the start of a fresh/restored session (and whenever the .py files are missing):
cp /home/user/clipart_engine.txt  /home/user/clipart_engine.py
cp /home/user/align_vo.txt        /home/user/align_vo.py
pip install -q imageio-ffmpeg
python3 -c "import clipart_engine, imageio_ffmpeg; print('engine OK')"
```

| File (as shipped) | Restored as | What it is / how it's used |
|---|---|---|
| `clipart_engine.txt` | `/home/user/clipart_engine.py` | The animation engine. Episode anim files `import clipart_engine` and define one scene fn per beat; `render_scene()` draws the PNG frames. Never edit per-episode logic here — new one-off props go in the episode's `anim_part.py`. |
| `align_vo.txt` | `/home/user/align_vo.py` | Caption-sync module. The builder auto-imports it (guarded try/except). It ASR-listens to each `voN.mp3` (Vosk small-en model, auto-downloads to **/tmp**, never the workspace) and returns per-word timestamps → captions pop on the exact spoken word. If it fails, the builder falls back to the weighted estimator — builds never break, but prefer ASR. |
| `build_TEMPLATE.txt` | copy → `<slug>_video/partN/build_pN.py` | The universal builder (title/endcard/badge overlays, recap splice, ASR caption alignment, squeeze-to-target, QC-friendly ffmpeg graph). **Never run the template in place** — copy into the part folder, edit the CONFIG block only, run it there. Check `def duration(path):` survived your edit before running. |
| `SAMPLE_anim_part.txt` | reference only (optionally `.py`) | A real working scene file (335 Years' War P1) — copy its patterns when writing a new episode's `anim_part.py`. Nothing imports it. |
| `VIDEO_FACTORY_PROMPT.md` | — | The LIVE manual for the current channel (real queue/registry/analytics). Keep as reference; update it after every delivery. |
| `FACTORY_TEMPLATE.md` | — | THIS file — blank-log universal version for new niches/accounts. |
| `SETUP_NOTES.md` | — | Boot sequence + rules-of-the-line cheat sheet. |
| `PROCESS_STEPS.md` | — | 12-step runbook of one full part build. |
| `RESCUE_MESSAGE.txt` | — | Paste-ready recovery block if a session crashes mid-build. |
| `UPLOAD_ARCHIVE.md` | — | Every upload block so far (title/description/hashtags) — keeps copy consistent; append after every delivery. |
| `historyclipart_style_ref.jpg` | — | The visual reference the clipart style riffs on. |

**Per-turn build boot (every time the sandbox may have been wiped):**
```bash
pip install -q imageio-ffmpeg
[ -f /home/user/clipart_engine.py ] || cp /home/user/clipart_engine.txt /home/user/clipart_engine.py
[ -f /home/user/align_vo.py ]       || cp /home/user/align_vo.txt /home/user/align_vo.py
```

**Coordination across accounts (if running 2+):** split by queue numbers (whichever account
gets told a number owns ALL its parts); each account keeps its own prompt file; at day's end
merge registry/queue lines into ONE master and re-share.
