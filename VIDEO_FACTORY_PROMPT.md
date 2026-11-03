# 🎬 VIDEO FACTORY — Master Prompt (Vertical Shorts Pipeline)

**How to use:** In a new chat, paste the entire `MASTER PROMPT` block, then send ONLY a
queue number (e.g. `4` → Great Molasses Flood). The agent writes the script in house
style, produces the video, marks the topic done, and cleans up old episode files.
Alternative inputs: a custom `Title: ...` line, or a full 6-segment script (manual control).
Series = "history's strangest true events". The CONTENT QUEUE (bottom of this file) is the
authoritative checklist — ✅ topics are already produced, NEVER reuse them.

---

## MASTER PROMPT

```
You are my automated scriptwriter + video-production pipeline for a vertical-shorts series
about history's strangest TRUE events. Work autonomously through ALL steps — don't re-ask
questions this prompt already answers.

=== MY INPUT ===
[ONE OF: (a) a queue number (e.g. "4") — look up that topic in my CONTENT QUEUE list
(pasted after this prompt / saved in VIDEO_FACTORY_PROMPT.md), skip anything marked ✅;
(b) a custom "Title: ..." line; (c) a full 6-segment script for manual control]
Topics come ONLY from those inputs — NEVER invent one. If a sent number is already ✅,
say so and take the next unmarked number instead.
NUMBER SENT: ___

=== STEP 0 — WRITE THE SCRIPT (skip if a full script was given) ===
Identify the real historical event (from queue number or title) and write a 30-second
script in EXACT house style:

Format per segment:
  **[0–4 sec]** / **[4–9 sec]** / **[9–15 sec]** / **[15–21 sec]** / **[21–26 sec]** / **[26–30 sec]**
  Each with **Voiceover:** (narration) + **Visual:** (one cinematic image description).
  Final segment adds **On-screen text:** "THE EVENT NAME — YEAR" (uppercase, em-dash).
Title style: "The X That Y" (punchy). Also craft the episode title now.

House beats:
- Beat 1 = HOOK: shocking/mysterious premise + twist tease ("In YEAR, PLACE experienced
  one of the strangest… and somehow, X happened").
- Beat 2 = ORIGIN: named person/place/thing begins it.
- Beat 3 = ESCALATION ("Within days…", chain reaction, spread).
- Beat 4 = CONSEQUENCE: human cost, damage, or absurdity in detail.
- Beat 5 = AFTERMATH: authorities' response / abandonment / deaths / legacy.
- Beat 6 = CLOSER: wry punchline or lingering mystery ("And somehow…", "And yes, this
  actually happened.", "historians still debate exactly what caused it").
- Voiceover: 1–2 short sentences per segment, 12–28 words, plain dramatic narration,
  factual to the real event. Visuals: cinematic historical recreation, era-authentic,
  escalating drama across the six images.
Show me the script briefly, then proceed WITHOUT waiting.

=== STEP 1 — NARRATOR VOICE ===
- If a TTS voice is already registered this session, reuse that voice_id (series consistency).
- Otherwise audition an English masculine narration voice (use_case: narration) via the
  voice tool, using hook lines from the script as audition text. Use the winning voice_id
  for all clips this session.
- 🔴 VOICE GATE (user rule, Aug 13): if the house TTS voice tool is NOT available this
  session → STOP production and TELL THE USER. NEVER substitute another voice or TTS
  engine — the series keeps ONE consistent voice. Wait for the user before generating.

=== STEP 2 — GENERATE ASSETS (do in parallel) ===
🏆 DEFAULT = CLIPART ANIMATION MODE (Experiment #3 winner, user-declared house style Aug 10 — use UNLESS the user asks for another style):
Voiceover: 1 TTS clip per beat (vo1.mp3…voN.mp3), text read EXACTLY; replace "…" with commas.
  If moderation blocks a clip, soften the wording (no gore/violence specifics) and retry.
  TTS budget: the speech tool allows ~10 calls per turn → produce ONE part per turn
  (8 beats), then wait for "continue" / "part 2" for the next part. Never try all parts at once.
Scenes: write anim_pN.py — one scene function per beat on the clipart engine
  `/home/user/clipart_engine.py` — white bg, blob-body figures w/ flat COLOR fills + thick
  black wobbly outlines. person(): hats (tricorne/shako/fez/furcap/turban), faces
  (smile/open/flat/sad/angry/cool), arms (down/up/point/hip/fist/musket), legs
  (stand/walk/none), trim=sash, lean/bob. Props: barrel, tent, fire, bottle, flag, river,
  moon, stars, burst, groundline, horse, cannon, sea, ship, island, gull; night= navy variant.
  Captions auto-burn per scene: **2-word phrases, TRUE-SYNCED** (house default since Aug 12).
  The builder ASR-aligns every beat via `/home/user/align_vo.py` (small vosk model → /tmp):
  per-word timestamps drive the captions, and the AMBER highlight rides the exact spoken word.
  `CAP_CHUNK = 2` default (`1` = max karaoke). Weighted estimator = automatic fallback.
  New props = quick PIL shapes in the anim file (or append to engine).
Builder: copy /home/user/build_TEMPLATE.py (the universal builder shipped in the kit —
  it ALWAYS exists on any restored account; episode build_pN.py folders get purged).
  Parts 2+: prepend 5s recap of previous part's tail (-sseof -5). Part 1: title card overlay
  first 3.6s (UPPERCASE, ≤2 lines). Final part: end card "THE EVENT — YEAR". White/black fades
  matching scene palette; brown-noise ambience 0.03/500Hz. SCENE_TARGET 43.5s w/ recap else
  48.5s; final ≤ ~49.8s; rate auto-compresses VO.
Series format rules (user Aug 10; BADGE UPDATE user Aug 12): amber top pill on EVERY part —
  "PART N", finale = "FINAL PART N" (builder badge mechanic; CONFIG BADGE=True default).
  Min 2 parts per story (2 = thin story, 3 = rich); parts 2+ open with 5s recap;
  non-final parts end on cliffhanger beats (no end card).
QC: ffprobe + 6–9 frame contact strip VIEWED before delivery; fix + re-render on failure.
Tools: ffmpeg via imageio-ffmpeg (re-pip-install if sandbox wiped); Pillow; DejaVu fonts.
Folder: slug_video/partN/. OUT_BASE = Title_With_Underscores_PartN.

LEGACY STEP 2 (AI cinematic stills — pre-Exp3 pipeline, reference only):
Visuals: 6 AI images (scene1.jpg…scene6.jpg). Per-prompt style: cinematic film still,
  photorealistic, era-appropriate, moody consistent color grade (state it), dramatic light,
  room for text overlay; ALWAYS "vertical 9:16 portrait orientation". Scene 1 suits a title
  card; scene 6 the end card.

STEP 2 ALT — ARCHIVAL MODE (real imagery, anti-AI-label; use when asked):
Replace AI images with authentic public-domain sources:
- Primary: Wikimedia Commons API
  (https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search
   &gsrsearch=Q&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url|size&iiurlwidth=1400,
   pick highest-width .jpg ≥900px, rate-limit ~4s/call with 429 backoff).
- Curated picks: en.wikipedia prop=images on that event's article titles — use the
  actual File: names found there (battles, portraits, daguerreotypes).
- Brave image search as fallback for candidates (view before use; skip watermarked).
- Verify via ONE contact strip before building; convert/measure with PIL; save as
  scene1..6.jpg. List sources in upload.txt (public domain art credit).
- Pre-1900 art = public domain, generally safe to use without attribution.

=== STEP 3 — ASSEMBLE (write build script from the APPENDIX; edit only the config block) ===
- Title card = episode title UPPERCASE (≤2 lines), first 3.6s, y≈40%.
- End card = the on-screen text, y≈78%, starting 0.6s into scene 6.
Fixed specs: 1080x1920 30fps H.264 CRF18 AAC192k · Ken Burns zoompan ±14% alternating ·
  Pillow PNG overlays (DejaVu-Bold white + dark stroke, AUTO-SHRINK ≤940px — this ffmpeg
  has NO drawtext) · brown-noise ambience (lowpass ~550Hz, subtle) under VO · vignette PI/4.5 ·
  fade-in 0.5s / fade-out 0.7s · per-clip aresample→[atempo]→stereo→apad/atrim→concat.
TWO CUTS — always both:
  TIGHT (primary, present this): atempo 1.6 uniform, gaps 0.15s, tail 0.6s → <OUT_BASE>_30s.mp4
  NATURAL: atempo 1.0, gaps 0.25s, tail 1.0s → <OUT_BASE>.mp4

=== STEP 4 — QC (mandatory) ===
- ffprobe: tight cut ≈ 26–32s, h264 1080x1920/30 + AAC stereo.
- Extract ≥4 frames (t≈2 title, scene 3, scene 5, end-card moment) → Pillow contact strip
  → VIEW it: text fits frame, scenes match beats. Overflow → shrink + re-render. Delete QC imgs.
- Present the tight cut; mention the natural cut.

=== STEP 5 — UPLOAD METADATA (mandatory) ===
Generate a copy-paste-ready upload block (YouTube Shorts/TikTok/Reels) and show it in
your final message, formatted EXACTLY like this template (also save as upload.txt in
the episode folder):

**Title:**
<Episode Title> <1–2 fitting emojis at the end — e.g. 🍯😱 ⚔️🪣 🧚📷>
**Description:**
<2–3 sentences retelling the story: year, place, event, key numbers, human cost.>
<1–2 sentence disbelief closer, e.g. "It sounds unbelievable… but the X was
terrifyingly real." — vary slightly per episode.>
#<EventCamelCase> #WeirdHistory #History #DidYouKnow #HistoryShorts #Shorts
(Event-specific hashtag first, then ALWAYS those 5 series tags.)

UPLOAD-TITLE PLAYBOOK v2 (from the Aug-10 leaderboard — Emu 1.2K / Beer 210):
- Absurdity FIRST, exactly 2 emojis at the end, year inside title or description.
- Winning patterns: "[Who] went to war / lost a war over [absurd thing] 😱⚔️",
  "The [Place] [Absurd Disaster] of [Year] 🍺😱", "They [absurd event] over [thing] ⚽💥".
- The in-video title card still uses "The X That Y" house style; upload titles get bigger hooks.

=== STEP 6 — HOUSEKEEPING (mandatory) ===
🔴 WORKSPACE BUDGET: ~128 MB / ~10,000 files MAX — files past the cap are SILENTLY DROPPED.
  One clipart part ≈ 750 frame PNGs + segs + QC images → an unmanaged 3-part series ≈ 2,300+
  files and blows the budget mid-build (this has killed a session once). Non-negotiable rules:
- AFTER each part's final MP4 passes QC AND is delivered (RETENTION v2, user Aug 13 — lean
  rule): delete frames/ dirs, segs, concat intermediates, QC images, __pycache__ IMMEDIATELY,
  then ALSO delete vo1–8.mp3, recap.mp4, anim_part.py, build_pN.py once the part is delivered.
  Keep per part ONLY: final .mp4, upload.txt, script.txt (8 beat texts + config/scene notes —
  one tiny file = enough to fully rebuild the part).
- DELIVERY: delete every previous completed *_video folder (keep the CURRENT one until all
  its parts are delivered). Keep VIDEO_FACTORY_PROMPT.md + kit files always.
- BOOT: before starting work in a fresh/restored session, purge any leftover *_video folders
  and frame/seg dirs from previous sessions.
- Update VIDEO_FACTORY_PROMPT.md: mark the queue topic "✅ Ep.N", append the episode to the
  registry, and bump the "Next up" number.

================ APPENDIX v2 — SEGMENTED BUILD (USE THIS; single-pass OOMs with hi-res images) ================
Same inputs/config as the script above, but render per-segment then concat + overlay:
1) make_overlay (title/endcard) + durations as above.
2) For each scene i: single ffmpeg call on ONE looped image + ONE vo clip:
   filters: scale/crop/zoompan/setsar/format/trim [v] and
   aresample(,atempo=R)/aformat/apad/atrim [a]  →  seg_i.mp4 (-c:v libx264 -crf18 -c:a aac 192k).
3) Concat via demuxer:  file list →  ffmpeg -f concat -safe 0 -i list.txt -c copy base.mp4.
4) One light final pass on base.mp4 (+ title.png/endcard.png looped inputs):
   overlay title (enable lte(t,3.6)), overlay endcard (enable gte(t, starts[5]+0.6)),
   vignette PI/4.5, fade in 0.5 / fade out last 0.7, format yuv420p;
   audio: [0:a] + anoisesrc=brown lowpass550 amix →  -movflags +faststart.
5) Verify EVERY subprocess returncode==0 and ffprobe Duration+Streams before QC.
(Build both rates by running steps 2–4 per rate. Permanent working template saved
outside episode folders: /home/user/video_build_template.py)

================ APPENDIX (LEGACY single-pass reference — prefer APPENDIX v2) ================
import subprocess, re, sys
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

# ---- CONFIG (edit per episode) ----
OUT_BASE      = 'Episode_Title'                       # file base name
TITLE_LINES   = ['EPISODE', 'TITLE']                  # uppercase title card (y=0.40)
ENDCARD_LINES = ['ON-SCREEN TEXT', '— YEAR —']        # end card (y=0.78)
# -----------------------------------

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS, N, W, H = 30, 6, 1080, 1920
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def make_overlay(path, lines, y_frac, size, max_w=940):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, size)
    while size > 30 and any(d.textlength(l, font=font) > max_w for l in lines):
        size -= 2; font = ImageFont.truetype(FONT_PATH, size)
    spacing = int(size * 1.35)
    y0 = H * y_frac - spacing * (len(lines) - 1) / 2
    for j, line in enumerate(lines):
        d.text((W/2, y0 + j*spacing), line, font=font, fill=(255,255,255,255),
               anchor='mm', stroke_width=max(3, size//22), stroke_fill=(0,0,0,175))
    img.save(path)

def duration(path):
    p = subprocess.run([FFMPEG, '-i', path], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True)
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', p.stderr)
    return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))

make_overlay('title.png',   TITLE_LINES,   0.40, 88)
make_overlay('endcard.png', ENDCARD_LINES, 0.78, 82)

vos, imgs = [f'vo{i}.mp3' for i in range(1,N+1)], [f'scene{i}.jpg' for i in range(1,N+1)]
raw = [duration(v) for v in vos]

def render(rate, gaps, out):
    segs = [d/rate + g for d, g in zip(raw, gaps)]
    total = sum(segs); starts = [sum(segs[:i]) for i in range(N)]
    cmd = [FFMPEG, '-y']
    for im in imgs: cmd += ['-loop','1','-i',im]
    for vo in vos:  cmd += ['-i',vo]
    cmd += ['-loop','1','-i','title.png','-loop','1','-i','endcard.png']
    F, vl, al = [], [], []
    for i in range(N):
        fr = int(round(segs[i]*FPS))
        z = f'1+0.14*on/{fr}' if i % 2 == 0 else f'1.14-0.14*on/{fr}'
        F.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                 f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                 f"setsar=1,format=yuv420p,trim=duration={segs[i]:.3f}[v{i}]"); vl.append(f'[v{i}]')
        t = f'atempo={rate},' if abs(rate-1) > 1e-6 else ''
        F.append(f"[{N+i}:a]aresample=44100,{t}aformat=channel_layouts=stereo,"
                 f"apad=whole_dur={segs[i]:.3f},atrim=duration={segs[i]:.3f}[a{i}]"); al.append(f'[a{i}]')
    F.append(''.join(vl)+'concat=n=6:v=1:a=0[Vraw]')
    F.append(''.join(al)+'concat=n=6:v=0:a=1[VOA]')
    F.append(f"anoisesrc=color=brown:duration={total:.3f}:amplitude=0.04,lowpass=f=550,volume=0.5[amb]")
    F.append("[VOA][amb]amix=inputs=2:duration=first:normalize=0[A]")
    F.append(f"[Vraw][12:v]overlay=0:0:enable='lte(t,3.6)'[Vt];"
             f"[Vt][13:v]overlay=0:0:enable='gte(t,{starts[5]+0.6:.2f})'[Vc];"
             f"[Vc]vignette=PI/4.5,fade=t=in:st=0:d=0.5,"
             f"fade=t=out:st={total-0.7:.2f}:d=0.7,format=yuv420p[V]")
    cmd += ['-filter_complex',';'.join(F),'-map','[V]','-map','[A]',
            '-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k',
            '-t',f'{total:.3f}',out]
    print(f'render {out}: total={total:.2f}s')
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0: print(r.stderr[-3000:]); sys.exit(r.returncode)

render(1.6, [0.15]*5 + [0.6], f'{OUT_BASE}_30s.mp4')   # tight cut (primary)
render(1.0, [0.25]*5 + [1.0], f'{OUT_BASE}.mp4')       # natural cut
print('ALL DONE')
```

---

## 🧰 OPS RULES (restored accounts & long sessions)

- **Only trust files that SHIP IN THE KIT**: `clipart_engine.py`, `build_TEMPLATE.py`,
  `SAMPLE_anim_part.py`, this prompt, the archive. Episode folders are disposable — never
  build logic around a path from a previous episode.
- **Renders take 2–4 min per part — that's normal.** Don't kill/restart a running build.
- **"AI service is busy" / cut-off turn**: nothing is lost — files persist on disk. On the
  next message, resume EXACTLY where you stopped: check which files exist, re-run only the
  missing step (usually: re-render the part whose .mp4 is absent, or finish QC/delivery).
  Do NOT restart the episode or re-write finished scenes.
- **Voice**: fresh session = no voice_id. Audition once (masculine English, use_case
  narration), then reuse that id for every clip of the session.
- **Fresh sandbox**: `pip install imageio-ffmpeg` before the first build; Pillow + DejaVu
  fonts are preinstalled. This ffmpeg build has NO drawtext — ALL text via Pillow overlays.
- Verify imports before generating (`python3 -c "import clipart_engine, imageio_ffmpeg"`).
- 🔴 **VOICE GATE (user, Aug 13; updated Aug 19)**: house TTS voice tool unavailable → tell the user; never switch voices silently. **Exception = the STAND-IN VOICE OF RECORD: en-US-GuyNeural (edge-tts), user-picked by audition Aug 19 — when the house tool is offline, Guy voices the build and the gate counts as satisfied.** (Prior one-off approvals: Ep.15 P2 ChristopherNeural Aug 13; the auditioned Guy also voices Ep.18 P1.)

---

## ✅ CONTENT QUEUE — 100 topics (✅ = already produced, do NOT reuse)

1. ✅ **Great Emu War (1932)** — Ep.1
2. ✅ **Dancing Plague of 1518** — Ep.2
3. ✅ **London Beer Flood (1814)** — Ep.3
4. ✅ **Great Molasses Flood (1919)** — Ep.4
5. ✅ **War of the Bucket (1325)** — Ep.5
6. ✅ **Pig War (1859)** — Ep.6
7. ✅ **War of Jenkins' Ear (1739)** — Ep.7
8. ✅ **Pastry War (1838)** — Ep.8 *(archival-mode experiment: real public-domain art via Wikimedia Commons, zero AI visuals)*
9. ✅ **Lobster War (1961)** — Ep.9 *(experiment 2: stickman hand-drawn animation, 49s single cut, 8 beats)*
10. ✅ **Football War (1969)** — Ep.10 *(stickman mode; 8 beats, 49s)*
11. ✅ **Battle of Karánsebes (1788)** — Ep.11 P1–P3 done: **3-PART series** *(Experiment #3 clipart mode: white bg, blob color-fill figures, captions w/ amber keyword; seamless format — NO part labels in-video; P2/P3 open with 5s recap of previous tail; P3 finale end card "THE BATTLE OF KARÁNSEBES — 1788")*.
12. ✅ **Three Hundred and Thirty-Five Years' War (1651–1986)** — Ep.12 P1–P3 all delivered: **3-PART** *(clipart; P1 declaration arc, P2 334-year montage, P3 Roy Duncan + 1986 Treaty of Scilly, end card "THE 335 YEARS' WAR — 1651–1986")*.
13. ✅ **Kettle War (1784)** — Ep.13 **2-PART series COMPLETE** *(clipart; thin story)* — P1 "THE WAR OF ONE CANNONBALL" *(Scheldt standoff → single shot → mystery-impact cliffhanger)* + P2 finale *(soup-kettle reveal → instant surrender → Fontainebleau 1785 → trophy kettle; end card "THE KETTLE WAR — 1784")*.
14. ✅ **Toledo War (1835)** — Ep.14 **2-PART series COMPLETE** — P1 "THE MAP THAT STARTED A WAR" *(standoff cliffhanger)* + P2 finale "THE WAR WITH ONE INJURY" *(🧪 1-word karaoke captions experiment; Two Stickney penknife → Jackson removes Mason → 1836 deal → UP copper jackpot; end card "THE TOLEDO WAR — 1835")*.
15. ✅ **Great Stink of 1858** — Ep.15 **2-PART series COMPLETE** *(clipart; 2-word ASR captions; first badge-era episode)* — P1 "THE SMELL THAT STOPPED PARLIAMENT" *(sewer London → heatwave → Parliament panics → lime curtains → Queen's aborted cruise → looming-cloud cliffhanger)* + P2 finale "THE SMELL THAT SAVED LONDON" *(Bazalgette's intercepting sewers: 82 miles dug by hand, 300M bricks, 16 years → stink fades, cholera stops, still running today; badge "FINAL PART 2"; end card "THE GREAT STINK — 1858")*.
16. ✅ **Great Moon Hoax (1835)** — Ep.16 **2-PART COMPLETE** *(off-session builds)* — P1 "The Newspaper That Found Moon People" / upload "A Newspaper Found Life on the Moon in 1835 🙂🌕" *(256 views @Aug 19; TikTok covers made here)* + P2 "The Moon Hoax That Fooled the Whole World 😂📰" *(17 views @Aug 19; end card "THE GREAT MOON HOAX — 1835")*.
17. ✅ **War of the Worlds Broadcast (1938)** — Ep.17 **2-PART COMPLETE** *(off-session builds)* — P1 "A Radio Play Caused Real Panic in 1938 📻😱" *(51 views @Aug 19)* + P2 "The Radio Panic That Made Orson Welles a Star 📻⭐" *(35 views @Aug 19; end card "WAR OF THE WORLDS — 1938"; parts posted 24h apart — cadence break flagged)*.
18. ✅ **Tulip Mania (1630s)** — Ep.18 **2-PART series COMPLETE** *(both parts delivered Aug 19, voice = Guy stand-in; ASR captions; badges)* — P1 "THE FLOWER THAT COST MORE THAN A HOUSE" *(SAME PRICE gag → FASHION FEVER → WIND TRADE → 5,500 GUILDERS → sailor-onion → silent-auction ". . .")* + P2 finale "The Bubble That Taught Nothing" *(silence spreads → cliff chart → −99% mansion→onion → PAY! trap → ruins triptych → courts VOID → every-bubble byword; end card "TULIP MANIA — 1637")*.
19. ✅ **South Sea Bubble (1720)** — Ep.19 **2-PART series COMPLETE** Sept 6 — P1 "The Bubble That Tricked the Smartest Man Alive" (49.33s: debt rain → MONOPOLY → 1 SHIP/YEAR → SHARES! → £128→£1,000 → BUBBLE Co. ??? → Newton 2× → dive-back cliff) + P2 "The Madness of People" (49.90s: SELL! → −90% → −£20k PLANETS/PEOPLE → FURY! → TOWER/SEIZED → Walpole PM #1 → snake-sack NO. → EST. 1720; end card "THE SOUTH SEA BUBBLE — 1720").
20. 🟡 **Mississippi Bubble (1720)** — Ep.20 P1 DELIVERED Sept 6 ("The Bubble That Invented the Millionaire", 49.37s, Guy stand-in, ASR captions, QC 10/10); P2 finale pending.
21. Cardiff Giant (1869) – A "petrified man" turned out to be a carved stone hoax.
22. Piltdown Man (1912) – A famous "early human" fossil was actually a fake.
23. Cottingley Fairies (1917) – Two girls faked photos of fairies; even Sir Arthur Conan Doyle believed them.
24. Feejee Mermaid – P.T. Barnum displayed a mummified "mermaid" made of a monkey and a fish.
25. Kensington Runestone – A Viking runestone in Minnesota is likely a hoax.
26. Loch Ness Monster Photo (1934) – The famous "Surgeon's Photo" was later admitted to be a hoax.
27. Roswell Incident (1947) – The US military said "flying saucer," then said "weather balloon."
28. Tunguska Event (1908) – A giant blast flattened 2,000 square km of Siberian forest without leaving a crater.
29. Dyatlov Pass Incident (1959) – Nine hikers died in the Ural Mountains under bizarre circumstances.
30. Roanoke Colony (1587) – An entire English colony vanished, leaving only the word "CROATOAN" on a tree.
31. Mary Celeste (1872) – A ship was found adrift with its crew gone and supplies untouched.
32. Somerton Man (1948) – A dead man on an Australian beach with a mysterious coded note; never identified.
33. Green Children of Woolpit – Legend says two green-skinned children appeared in medieval England.
34. Nika Riots (532) – Chariot racing fans in Constantinople rioted and nearly overthrew the emperor.
35. Cadaver Synod (897) – Pope Stephen VI put his predecessor's rotting corpse on trial.
36. Defenestration of Prague (1618) – Throwing officials out a window helped start the Thirty Years' War.
37. Caligula's Horse – The Roman emperor allegedly planned to make his favorite horse a consul.
38. Charles VI of France – He believed he was made of glass and might break.
39. Ludwig II of Bavaria – The "Mad King" built bizarre fairytale castles and died mysteriously.
40. Münster Rebellion (1534) – Radical Anabaptists took over Münster, setting up a polygamous theocratic kingdom.
41. Great Cat Massacre (1730s) – Paris apprentices ritually killed cats as a strange workplace protest.
42. Medieval Animal Trials – In Europe, pigs, rats, and even insects were put on trial for crimes.
43. The Hanged Sow of Falaise (1386) – A pig was publicly executed for killing a child.
44. Peter the Great's Beard Tax – Russians had to pay a tax to keep their beards.
45. Tichborne Claimant – A butcher pretended to be a missing aristocrat; the trial became a Victorian sensation.
46. Great Stork Derby (1930s) – A Toronto millionaire's will rewarded the woman who had the most babies.
47. Year Without a Summer (1816) – Snow fell in July after the eruption of Mount Tambora.
48. Carrington Event (1859) – A solar storm made telegraphs spark and work without power.
49. Lake Nyos Disaster (1986) – A lake released a CO2 cloud, suffocating over 1,700 people.
50. Red Rain of Kerala (2001) – Rain fell red in India; the cause is still debated.
51. Great Chicago Fire (1871) – Blamed on Mrs. O'Leary's cow, but that's probably a myth.
52. Peshtigo Fire (1871) – America's deadliest wildfire, same day as Chicago, far less famous.
53. King Alexander I of Greece – Died in 1920 after being bitten by a pet monkey.
54. Aeschylus's Death – The playwright was supposedly killed by an eagle dropping a tortoise on his head.
55. Chrysippus's Death – The philosopher allegedly died laughing at a donkey eating figs.
56. Bobby Leach – Survived Niagara Falls in a barrel, then died after slipping on an orange peel.
57. Henry I of England – Reportedly died after eating too many lampreys.
58. Tycho Brahe – Death popularly blamed on refusing to leave a banquet to urinate.
59. Zachary Taylor – The US president died after eating cherries and milk on a hot July day.
60. Clement Vallandigham – The lawyer accidentally shot himself in court while demonstrating a gun.
61. Spring-heeled Jack – A mysterious leaping figure terrified Victorian London.
62. Mad Gasser of Mattoon (1944) – A phantom gas attacker struck an Illinois town; nobody was caught.
63. London Monster (1788–1790) – A man attacked women with pins and sent terrible letters.
64. Battle of Los Angeles (1942) – Anti-aircraft guns fired at a mystery object for hours; no plane found.
65. Acoustic Kitty – The CIA bugged a cat to spy; it was hit by a car.
66. Bat Bomb (WWII) – The US planned to drop bats carrying tiny incendiary bombs on Japan.
67. Project Habakkuk – The Allies planned a giant aircraft carrier made of ice.
68. Pigeon-Guided Missiles – B.F. Skinner tried to guide missiles with trained pigeons.
69. Soviet Anti-Tank Dogs – Dogs trained to run under tanks with explosives on their backs.
70. Emperor Norton – A San Francisco man proclaimed himself Emperor of the US; the city played along.
71. Andrew Jackson's Parrot – Removed from his funeral for swearing nonstop.
72. War of the Stray Dog (1925) – Greece and Bulgaria clashed after a soldier chased his dog across the border.
73. War of the Golden Stool (1900) – British demand for the sacred Ashanti stool sparked a war.
74. Pope Joan – Legend says a woman once became pope.
75. Hanno the Elephant – A Renaissance pope's beloved pet elephant.
76. 1904 Olympic Marathon – The winner took strychnine and brandy mid-race.
77. Shizo Kanakuri – Quit the 1912 Olympic marathon and went home; "finished" 54 years later.
78. Great New England Vampire Panic – 1800s New Englanders dug up relatives suspected of vampirism.
79. Salem Witch Trials (1692) – "Spectral evidence" sent innocents to their deaths.
80. Miracle of the Sun (1917) – A huge crowd in Portugal claimed the sun "danced."
81. Kingdom of Redonda – An uninhabited Caribbean island became a "literary kingdom."
82. Republic of Minerva (1972) – Libertarians built a nation on a reef; Tonga annexed it.
83. Conch Republic (1982) – Key West "seceded" from the US over a border checkpoint.
84. Aroostook War (1838) – Maine vs New Brunswick lumberjack border conflict with no real battles.
85. Cod Wars – Iceland and Britain repeatedly "fought" over fishing rights.
86. Tarrare – An 18th-century Frenchman who could (and did) eat anything.
87. Black Dinner (1440) – Two young earls executed after a banquet; may have inspired "Game of Thrones."
88. Tamerlane's Curse – Soviet exhumation of the tomb in 1941 was followed by the Nazi invasion.
89. Tutankhamun's Curse – Deaths among the tomb's opening party fueled legend.
90. Anglo-Zanzibar War (1896) – It lasted only about 38 to 45 minutes.
91. Christmas Truce (1914) – WWI soldiers stopped fighting and played football in no man's land.
92. Philadelphia Experiment – A rumored Navy experiment that allegedly made a ship invisible.
93. Kelly-Hopkinsville Encounter (1955) – A Kentucky family reported an attack by "little green men."
94. Mary Reeser Case (1951) – A woman burned to ashes without the room catching fire.
95. Homo floresiensis – "Hobbit" humans lived in Indonesia as recently as 50,000 years ago.
96. Mary Toft (1726) – An Englishwoman convinced doctors she was giving birth to rabbits.
97. Sumerian King List – Ancient records list kings ruling for tens of thousands of years.
98. Bath School Disaster (1927) – A school board member blew up a Michigan school, killing 45.
99. Operation Paul Bunyan (1976) – A huge US military show of force just to cut down a tree in the DMZ.
100. Flight 19 (1945) – Five Navy bombers vanished over the Bermuda Triangle, and the rescue plane vanished too.

---

## 📺 EPISODE REGISTRY — numbering synced: Pig War onward, queue #N = Episode #N.
(The Ocean was the unnumbered Pilot and stays outside the sync.)

| # | Episode title | Topic | End card |
|---|---------------|-------|----------|
| Pilot | **The Ocean Has a Secret** | Great Blue Hole mystery (trial episode) | "Would you dive down?" |
| 1 | **The War Australia Lost to Emus** | Queue #1 — Great Emu War, 1932 | "THE GREAT EMU WAR — 1932" |
| 2 | **The Dancing Plague That Nobody Could Stop** | Queue #2 — Dancing Plague of 1518 | "THE DANCING PLAGUE — 1518" |
| 3 | **The Beer Flood That Killed 8 People** | Queue #3 — London Beer Flood, 1814 | "THE LONDON BEER FLOOD — 1814" |
| 4 | **The Molasses Wave That Swallowed Boston** | Queue #4 — Great Molasses Flood, 1919 | "THE GREAT MOLASSES FLOOD — 1919" |
| 5 | **The War That Started Over a Bucket** | Queue #5 — War of the Bucket, 1325 | "THE WAR OF THE BUCKET — 1325" |
| 6 | **The War That Only Killed a Pig** | Queue #6 — Pig War, 1859 | "THE PIG WAR — 1859" |
| 7 | **The Ear That Started a War** | Queue #7 — War of Jenkins' Ear, 1739 | "WAR OF JENKINS' EAR — 1739" |
| 8 | **The War Over a Pastry Shop** | Queue #8 — Pastry War, 1838 *(archival-mode experiment)* | "THE PASTRY WAR — 1838" |
| 9 | **The Lobster War That Almost Happened** | Queue #9 — Lobster War, 1961 *(stickman-animation experiment)* | "THE LOBSTER WAR — 1961" |
| 10 | **The War Over a Football Match** | Queue #10 — Football War, 1969 *(stickman mode)* | "THE FOOTBALL WAR — 1969" |
| 11 P1 | **The Army That Defeated Itself (part 1)** | Queue #11 — Battle of Karánsebes, 1788 *(clipart experiment #3; v2: NO part numbers anywhere in-video; ends on black-out BANG cliffhanger)* | (none — cliffhanger cut) |
| 11 P2 | **The Army That Fought Itself in the Dark** | Queue #11 — part 2 *(opens with 5s recap cold-open = tail of P1; night chaos: HALT/ALLAH, volleys, cavalry, cannons; dawn cliffhanger)* | (none — dawn cut to part 3) |
| 11 P3 | **The Enemy Arrived Two Days LATE to the Battle** | Queue #11 — finale *(5s recap from P2; Ottoman arrival, Emperor's humiliation, schnapps merchants)* | "THE BATTLE OF KARÁNSEBES — 1788" |
| 12 P1 | **The War Where No One Fought** | Queue #12 — 335 Years' War, 1651 *(clipart; ships/sea/islands; ends on total silence cliffhanger)* | (none — seagull cut) |
| 12 P2 | **Two Countries Forgot They Were at War for 334 Years** | Queue #12 — part 2 *(time-montage: treaties, rust, steam, cars, Moon rocket, 1985 beach; envelope cliffhanger)* | (none — envelope cut) |
| 12 P3 | **The War Nobody Noticed Was Still Going — for 335 Years** | Queue #12 — finale *(Roy Duncan archives → embassy check → ambassador sails 1986 → treaty signing → dusk peace)* | "THE 335 YEARS' WAR — 1651–1986" |
| 13 P1 | **The War of One Cannonball** | Queue #13 — Kettle War, 1784 *(clipart; 2-part; Emperor Joseph II vs closed Scheldt → the Dolphin sails → Fort Liefkenshoek → ONE shot → mystery-impact cliffhanger, kettle hidden)* | (none — impact cut) |
| 13 P2 | **The Soup Pot That Ended a War** | Queue #13 — finale *(5s recap cold-open; CLONK! kettle reveal → lunch destroyed, 0 hurt → white flag → stunned Austrians → silence → "PEACE, 1785" table → 1 SHOT/0 HURT memorial → trophy kettle)* | "THE KETTLE WAR — 1784" |
| 14 P1 | **The Map That Started a War** | Queue #14 — Toledo War, 1835 *(clipart; 2-part; wrong 1787 map line → Ohio redraws it → MI constitution claims Toledo → Boy Governor (24) vs Gov. Lucas → sheriffs arrest Ohioans, armed surveyors → two militia columns → standoff cliffhanger "WHO FIRES FIRST?")* | (none — standoff cut) |
| 14 P2 | **The War With One Injury** | Queue #14 — finale *(🧪 caption experiment — v1 1-word, v2 sync-weighted, **v3 shipped: 2-word captions (producer choice)**; sheriff steps out → "TWO" → penknife escape → sweating armies → Jackson REMOVED → THE DEAL 1836 → "WORTHLESS?" snow → COPPER! jackpot)* | "THE TOLEDO WAR — 1835" |
| 15 P1 | **The Smell That Stopped Parliament** | Queue #15 — Great Stink, 1858 *(clipart; FIRST episode with top badge "PART 1" — user rule Aug 12; 2.5M people, one sewer-river → flush-toilet craze + heatwave → "THE GREAT STINK" → Parliament panic → lime curtains → Queen's ABORT cruise → looming-cloud cliffhanger)* | (none — cloud cut) |
| 15 P2 | **The Smell That Saved London** | Queue #15 — finale *(5s recap from P1; Bazalgette hired → INTERCEPTORS plan diagram → 300,000,000 BRICKS trench dig → 16-year city-wide worksite → clean-Thames miracle + cholera stops → London Eye "TODAY" tunnel cross-section → buried-the-problem closer; badge "FINAL PART 2"; voice = edge-tts en-US-ChristopherNeural — user approved Aug 13)* | "THE GREAT STINK — 1858" |
| 16 P1 | **The Newspaper That Found Moon People** | Queue #16 — Great Moon Hoax, 1835 *(built off-session; covers v1/v2 made here; upload title "A Newspaper Found Life on the Moon in 1835 🙂🌕"; 256 views @Aug 19)* | (none — rival-editor cliffhanger) |
| 16 P2 | **The Moon Hoax That Fooled the Whole World** | Queue #16 — finale *(built off-session; upload title same + 😂📰; 17 views @Aug 19)* | "THE GREAT MOON HOAX — 1835" |
| 17 P1 | **A Radio Play Caused Real Panic in 1938** | Queue #17 — War of the Worlds, 1938 *(built off-session; upload title same + 📻😱; 51 views @Aug 19)* | (none — cliffhanger) |
| 17 P2 | **The Radio Panic That Made Orson Welles a Star** | Queue #17 — finale *(built off-session; upload title same + 📻⭐; 35 views @Aug 19)* | "WAR OF THE WORLDS — 1938" |
| 18 P1 | **The Flower That Cost More Than a House** | Queue #18 — Tulip Mania, 1636 *(clipart; PART 1 badge; voice = stand-in Guy, user-picked Aug 19; "PRICE: SAME" tag → Ottoman bulb arrival → broken tulips + FASHION FEVER → tavern wind-trade craze → WIND TRADE papers → 5,500 GUILDERS house-vs-bulb scale → sailor eats bulb, JAIL SOON → auctioneer + paddles-down silent ". . ." cliffhanger)* | (none — silent cut) |
| 18 P2 | **The Bubble That Taught Nothing** | Queue #18 — finale *(5s recap from P1 silent-auction tail; silence spreads → red-cliff price chart → −99% mansion-to-onion scale flip → PAY! contract trap, torn IOUs → weaver/family/jailed-sailor ruins triptych → courts stamp VOID, wind trade evaporates → "1637" book + EVERY BUBBLE thought → IOU-and-onion closer; badge "FINAL PART 2"; voice = Guy)* | "TULIP MANIA — 1637" |
| 19 P1 | **The Bubble That Tricked the Smartest Man Alive** | Queue #19 — South Sea Bubble, 1711–1720 *(clipart; PART 1 badge; voice = stand-in Guy; £ debt rain + WAR DEBT London → SOUTH SEA Co. MONOPOLY handoff, DEBT barrel → Spain allows ONE ship/year → SHARES! counter, fine print → £128→£1,000 rocket chart, swooning MPs → coin rain + BUBBLE Co. "purpose: ???" → Newton (hand-drawn wig, "cool" face) 2× cashes out, apple gag → insiders sneak off with £ sacks + Newton dives back in at the very top, ". . ." cliffhanger)* | (none — cliffhanger cut) |
| 19 P2 | **The Madness of People** | Queue #19 — finale *(5s recap from P1 dive-back cliff tail; SELL! counter stampede → −90% cliff chart £1,000→£100 → Newton −£20,000, winged coins flee, "MOTION OF PLANETS: OK / PEOPLE: ???" bubble → FURY! riot torches → directors behind TOWER bars, SEIZED estate barrel (bars layered over bodies) → Walpole stitches "FIXED", PM #1 → snake-sack proposal "THAMES??" Parliament "NO." → EST. 1720 plaque + wind-blown IOU closer; badge "FINAL PART 2"; voice = Guy)* | "THE SOUTH SEA BUBBLE — 1720" |
| 20 P1 | **The Bubble That Invented the Millionaire** | Queue #20 — Mississippi Bubble, Paris 1715–1719 *(clipart; PART 1 badge; voice = Guy; BANKRUPT Paris + EMPTY chest, gambler Law arrives w/ suitcase + floating aces → WANTED duelist opens BANQUE, Regent approves → PRINT! LIVRES rain + note stack → LOUISIANA parchment w/ map-ship + gold bursts + whisper trail → 500→18,000 rocket + "MILLIONAIRE (new word!)" sign → hunchback back-for-rent casino → crowned Law RICHER THAN THE KING* (*on paper) on note stack → Prince de Conti + three GOLD wagons + wondering bystanders "?" ". . ." cliff)* | (none — cliffhanger cut) |
| ?? | **He Invented a Sport. It Killed Him at 39** | ⚠️ NON-QUEUE video (Aug 15, built in an unknown session; 294 views @Aug 19) — topic NOT in our 100; origin unconfirmed, investigating | ? |
| TC1 P1 | **The Case That Split a Jury** | NON-QUEUE special, user-directed Sept 6 *(Lindsay Clancy — Duxbury Jan 2023 → trial July 2026; house engine, SOMBER treatment: documentary props only, NO victims/act depicted, no gags, no wry closer; PART 1 badge; Guy; 49.53s, ASR)* | (none — trial cliff) |
| TC1 P2 | **The Trial That Could Not Decide** | TC1 finale *(5s recap; 5 WEEKS ~80 WITNESSES courtroom → dueling expert docs → PREMEDITATED vs A DISEASE scale → AUGUST 27 jury 9+3 files out → animated 23 HOURS clock, "WE CANNOT AGREE" note → "KEEP TRYING." → "WITH A HEAVY HEART…" 2nd note → red MISTRIAL stamp SEPT 4 2026 → RETRY/PLEA/DISMISS doors, NEXT: SEPT 29 → 3-candle memorial closer; FINAL PART 2 badge; Guy; 49.83s)* | "CORA, DAWSON & CALLAN — 2023" (memorial end card) |

Next up: **Episode 20 P2 = Mississippi Bubble FINALE** *(Ep.20 P1 DELIVERED Sept 6 — 49.35s "The Bubble That Invented the Millionaire", Guy, ASR captions, QC 10/10; P2 = 5s recap from wagon-cliff tail → wagons multiply into a full bank run → gold promises break → shares collapse → Law flees France in disguise → France swears off banks for generations → wry closer; end card "THE MISSISSIPPI BUBBLE — 1720")*. **Ep.19 COMPLETE** (same-day series, Sept 6). After the finale: default queue #21 Cardiff Giant 🗿 — the flavor break finally lands 🎉. ⛔ voice-gated (Guy = stand-in of record). **TC1 SPECIAL (non-queue, user-directed) DELIVERED Sept 6: Lindsay Clancy 2-part (49.53s + 49.83s, QC pass, somber treatment — do not gag-ify; retrial news → update offer pending).** Registry rows TC1 P1/P2. **Ep.18 COMPLETE** (P1 49.51s + P2 49.80s, both QC all-pass, Sept 6). **Ep.16 + Ep.17 built COMPLETE off-session** (see registry). ⚠️ **Sept 6: views declining since the Stink peak — diagnosis + repair list in the Experiment log: fix hashtags-in-titles + backfill descriptions (blocks in `BACKFILL_DESCRIPTIONS_Aug19.txt`), verify P2 pin comments, keep P1/P2 ~3h apart same day, identify the Aug 15 non-queue sport video, get Analytics "Viewed vs swiped" + traffic sources.** Off-session scripts are NOT archived here — rebuilds must re-derive from published videos. Workspace ~16 MB (Retention v2). **Style default: CLIPART MODE for everything going forward (user decision, Aug 10).** Multi-part format (user approved): no part labels in-video, next part opens with 5s recap of previous tail. **Part-count rule (user, Aug 10): MINIMUM 2 parts per story — 2 parts for thin/short stories, 3 parts for rich ones (no single-part episodes in this phase).** **Posting schedule rule (user, Aug 10): 6 uploads/day = 2 complete stories/day, each story posted as its OWN clean block (finish all parts of story A before story B starts) — never interleave two stories in one slot; every upload is a distinct episode; ~3h between uploads.**

### 🎨 STYLE VARIANTS (experiments so far — engine files saved at workspace root)
- **CURRENT DEFAULT (since Aug 10): CLIPART mode (see below) for ALL future episodes.**
- **Legacy default**: AI cinematic stills. **Archival mode (Ep.8)**: real public-domain art via Commons — see STEP 2 ALT.
- **Stickman mode (Ep.9)**: hand-drawn frame-by-frame whiteboard animation with light motion.
  Engine: `/home/user/stickman_anim_engine.py` (wobbly-line primitives, stickman/boat/lobster/flag/kangaroo,
  scene functions → PNG frames). Builder: `/home/user/stickman_build_template.py`
  (PNG-seq segmented render, dark-ink overlays on paper bg, white fades, quiet ambience,
- **Clipart mode (Ep.11, Experiment #3 — inspired by TikTok @historyclipart, made OURS)**:
  white background, blob-body figures w/ flat COLOR fills + thick black wobbly outlines,
  heads w/ dot eyes + simple mouths, hats (tricorne/shako/fez), props (barrel/tent/fire/bottle/
  flag/river/moon/burst), night scenes w/ navy bg, bottom-third captions auto-chunked (3 words,
  one keyword highlighted AMBER — theirs uses green), top title card + small amber part-badge.
  Engine: `/home/user/clipart_engine.py` (`render_scene(scene_fn, nframes, outdir, caption_words, night)`).
  Builder pattern: `/home/user/build_TEMPLATE.py` (kit file — copy → override OUT_BASE/
  TITLE_LINES/ENDCARD_LINES/RECAP_SRC/FINAL + point at the part's anim module). 3-part cliffhanger structure:
  P1/P2 end-cards tease next part; P3 uses standard "EVENT NAME — YEAR" end card.
  8-beat structure OK, auto-compress to ≤ TARGET_MAX seconds, single cut).

---

## ⚗️ EXPERIMENT LOG (all live on YouTube from Aug 10, 2026 — fill results in when known)

Snapshot @9h41m (Aug 10): Emu 1.2K · Beer 210 · Dancing 37 · Lobster(stickman) 15 ·
Bucket 3 · Molasses 3 · Pastry(archival) 3 · Jenkins 1 · Pig 1.
Early read: TOPIC/TITLE is the dominant variable so far (Emu & Beer are AI-stills but
outperformed everything) — style variants not yet decided. User retitled on upload:
Emu → "Australia Lost a War... to Emus 🦘💀", Beer → "The London Beer Flood of 1814 🍺😱",
Dancing → "The Dancing Plague of 1518 💃😨" (check if this title pattern drove the win).
Snapshot @1:04pm (Aug 10, Studio screenshot): Football(stickman) 0 · Lobster 14 · Pastry 4 · Jenkins 2.
Snapshot @4:08pm (Aug 10, Studio screenshot): Karánsebes clipart uploads 246 & 207 (user CONFIRMED both rows come from the dupe title — he forgot to swap titles between uploads; P1 IS posted) · Football 31 · P3 scheduled. Parts funnel is WORKING (vs Lobster 15 as prior stickman best today).
Snapshot @12:56am (Aug 11, Studio screenshot): Karánsebes upload ("Army That Fought Itself in the Dark") 429 (still climbing from the 246/207 pair) · Karánsebes P3 ("Enemy Arrived Two Days LATE") 4 · 335 P1 4 · 335 P2 1 · 335 P3 0. All Notices clean, all Public. ⚠️ UPLOAD BUG: 4 of the 5 newest uploads went live with NO description/hashtags ("Add description" rows) — user to backfill from UPLOAD_ARCHIVE.md blocks. Read: NOT a shadowban — old Short still being served; new ones in normal 0–5h cold-start.
Snapshot @2:27am (Aug 12, Analytics screenshot): **7d total 2,907 views · 7.0h watch · +6 subs (realtime 9)** · realtime 48h = 3,874 views (velocity RISING — most views are <48h old) · top content: Karánsebes "The Army That Fou…" **1,093** (channel's 2nd 1K video after Emu 1.2K; clipart #1). Curve flat Aug 4–8 → ramp Aug 9 → ~1.3–1.5K/day. Read: clipart era fully validated; Aug 11 (post-shadowban-check day!) likely biggest day. Watch-time/view ≈ 8.7s → next lever = swipe-away retention in first 2s (check "Viewed vs swiped" on Karánsebes).
Snapshot @2:31am (Aug 19, Content-list screenshot): step-down across the board — Stink P1 1,101 (Aug 13) · Toledo P2 185 · Stink P2 638 · Moon P1 256 · Moon P2 **17** · NON-QUEUE "He Invented a Sport. It Killed Him at 39" 294 · Radio P1 51 · Radio P2 35. ALL visible rows show **"Add description"** (metadata bug RETURNED) and **hashtags inside TITLES** (whole upload block pasted into title). Reads: (1) P2 funnel broken — P2 views as % of P1: Stink 58% → Moon 6.6%; pin comments + 5s recap unverified on off-session parts; Radio P1/P2 posted 24h apart = block-cadence break; Moon P1+P2 dumped same day as a third upload = buried. (2) Hygiene regression is NOT the killer by itself (Stink P1 hit 1,101 with the same bug) but costs search/tag signals — fix per upload, once. (3) Topic drift: Aug 15 video is NOT in our 100 (origin unconfirmed — topic-guard breach on whichever session built it). (4) Notices clean, all Public → not strikes; Shorts still serving small numbers = algorithmic throttle, not ban. NEEDED: Analytics screenshots — "Viewed vs swiped away", retention curve, traffic sources — to confirm hook fatigue before next P1.
User is ALSO cross-posting every episode to TikTok for extra data — track TikTok views separately; do not mix into YouTube numbers.

| Style | Episode | AI label? | Early views | @3d | @7d |
|---|---|---|---|---|---|
| AI stills | Ep.1 Ocean (pilot) | ? | n/a in snapshot | | |
| AI stills | Ep.2 Emu | ? | 1.2K | | |
| AI stills | Ep.3 Dancing Plague | ? | 37 | | |
| AI stills | Ep.4 Beer Flood | ? | 210 | | |
| AI stills | Ep.5 Molasses | ? | 3 | | |
| AI stills | Ep.6 Bucket | ? | 3 | | |
| AI stills | Ep.7 Pig War | ✅ auto-labeled | 1 | | |
| AI stills | Ep.8 Jenkins' Ear | not labeled at upload | 1 | | |
| Archival (exp.1) | Ep.9a Pastry War | ✅ NO LABEL | 3 | | |
| Stickman (exp.2) | Ep.9 Lobster War | ✅ NO LABEL | 15 | | |
| Stickman | Ep.10 Football War | ? (uploaded clean per dash) | 0@1pm | | |
| Clipart (exp.3) | Ep.11 P1 Karánsebes | ? | 246 @~4h* | | |
| Clipart (exp.3) | Ep.11 P2 Karánsebes | ? | 207 @~4h* | | |
| Clipart (exp.3) | Ep.11 P3 Karánsebes | | scheduled | | |
| Clipart | Ep.12 P1 335 Years' War | | | | |
| Clipart | Ep.12 P2 335 Years' War | | | | |
| Clipart | Ep.12 P3 335 Years' War | | | | |
| Clipart | Ep.13 P1+P2 Kettle War | | | | |
| Clipart | Ep.14 P1 Toledo War (3-word captions) | | | | |
| Clipart + 🧪1-word karaoke | Ep.14 P2 Toledo War | ? | new Aug 12 | | |

🏆 VERDICT #3 (Aug 12, USER-ORDERED + USER-STILL-UNHAPPY → FINAL FIX): **captions are now TRULY
audio-synced, not estimated.** Estimation v2 (weighting) still drifted; the real fix = listen to the
audio. New module **`/home/user/align_vo.py`** (kit file): Vosk small-en ASR (auto-installs, model
lives in /tmp) returns per-word timestamps per vo clip; difflib maps them to script words
(homophone/OOV-safe — "Two Stickney" case proven); captions pop at real word starts and the AMBER
highlight rides the currently-spoken word. 2-word phrases = default (`CAP_CHUNK=2`; 1 = max karaoke).
If ASR ever fails, builders auto-fall back to the weighted estimator — builds never break.
Whole pending slate (Ep.13 P1/P2, Ep.14 P1/P2) rebuilt with it Aug 12. Pipeline ~+15s per part.

*P1/P2 both showed the SAME title at snapshot time (user forgot to swap) — pairing by thumbnail.

⚗️ VERDICT #1 (Aug 10, confirmed): the AI VOICE is NOT the label trigger — AI IMAGERY was.
Both archival and stickman styles are label-proof; AI-stills enforcement is inconsistent
(Pig flagged, Jenkins not). Narrator stays regardless of style choice.

🏆 VERDICT #2 (Aug 10, USER-DECIDED): **CLIPART MODE (Experiment #3) IS THE PERMANENT DEFAULT**
for all future episodes. Evidence: Karánsebes P1/P2 hit 246/207 views within ~4h — 14–16× the
best stickman numbers that day (Lobster 15, Football 31) — zero labels, plus the 3-part
recap-funnel format demonstrably hooks viewers. Legacy styles remain available on request only.
