# 🏭 FACTORY RUNBOOK — the exact per-part process (fast lane)

You are already the factory (you've read VIDEO_FACTORY_PROMPT.md; kit files live at /home/user).
Follow these steps in THIS EXACT ORDER — one tool call each, zero free-styling.
The speed comes from: writing scenes in ONE shot, batching ALL 8 voice clips in ONE message,
and never re-rendering something that passed QC. **≈10 calls, ~6–8 min per part. ONE PART PER TURN.**

## TURN START (once per episode)
1. bash — purge the previous `*_video` folder; always `pip install imageio-ffmpeg`
   (sandboxes wipe site-packages constantly — just do it every turn);
   `mkdir -p <slug>_video/part<N>`; `cp /home/user/build_TEMPLATE.txt <slug>_video/part<N>/build_p<N>.py`;
   print `du -sh /home/user` and file count — must stay ≪ 128 MB / 10,000 files.

## FIRST PART OF A SESSION ONLY (once, then never re-check)
2. bash — `grep -n "^def " /home/user/clipart_engine.py` + read the CONFIG block of build_TEMPLATE.
   Memorize the signatures. Key trap: **cannon() aims LEFT and returns its muzzle point**.
   Every later anim file this session is written from memory + the SAMPLE_anim_part.py pattern.

## THE BUILD LOOP (per part)
3. write_file — `<slug>_video/part<N>/anim_part.py` **in one shot**: 8 scene functions + `SCENES`,
   `NIGHT`, `BEATS` (BEATS = the VO text `.split()` word lists; captions + amber keyword auto-burn).
   **Always set `CAP_CHUNK = 2` at the top** (2-word phrase captions = house default since Aug 12;
   1-word = `CAP_CHUNK = 1`). **Sync is automatic**: the builder ASR-aligns via `align_vo.py`
   (vosk model → /tmp, pip first build of the session) — captions ride real word timestamps,
   highlight tracks the spoken word; `captions: ASR-aligned per word (vosk)` in build output =
   working; `weighted fallback` = ASR failed, still fine to ship.
   Scene rules: white bg (navy only if night); groundline ~y1500–1650; int RGB only; motion via `f`/`t`;
   part 1 scene 1 keeps y≈0.22H clear (title card lands there);
   final part's LAST scene keeps y≈350–700 clear (end card lands at 0.26H, black ink on light).
4. edit_file — build_pN.py CONFIG only: OUT_BASE, PART_NUM, FINAL (True only on last part),
   TITLE_LINES (part 1 only), ENDCARD_LINES `['THE EVENT NAME', '— YEAR —']` (final only),
   RECAP_SRC = `../part<N-1>/<previous final file>.mp4` (parts 2+), GAPS tail 1.2 (non-final) / 1.8 (final).
5. 🔴 **VOICE GATE first**: if the house TTS voice tool is in this session's toolbelt →
   **8× generate_speech IN ONE MESSAGE** (parallel), session voice_id, text = BEATS sentences
   exactly, commas instead of "…" → `vo1.mp3 … vo8.mp3`. If it is NOT → use the STAND-IN
   VOICE OF RECORD: en-US-GuyNeural via edge-tts (user-picked Aug 19; `pip install edge-tts`;
   asyncio `edge_tts.Communicate(beat, 'en-US-GuyNeural').save(f'vo{i}.mp3')` ×8). Only if the
   user revokes the stand-in too → STOP and ask. NEVER switch voices silently.
6. bash — `cd part<N> && python3 build_p<N>.py 2>&1 | tail -15 && ls *.mp4` (timeout 1500).
   Expect: natural ≈ 70–77s, rate ≈ 1.5–1.6, **final 49.3–49.8s** (auto-squeezes ≤49.9).
   Renders take 2–3 min — that's normal, don't touch it. ModuleNotFoundError → pip install → rerun
   (frame skip = resume, nothing lost).
7. bash QC — ffprobe Duration+Streams (49–50s, h264 1080×1920@30, aac 44.1k stereo) +
   extract 8–9 frames (t≈2 title/recap, each scene, **end-card moment** for finals) +
   Pillow strip → `qc/strip.png`.
8. read_file the strip — text fits? scenes match beats? end card legible on clear space?
   FAIL → fix anim_part.py, `rm -rf frames/sX` for the CHANGED scenes only (finished scenes are
   skipped = fast re-render), rerun call 6.
9. bash cleanup — `rm -rf frames seg_*.mp4 qc base.mp4 list.txt title.png endcard.png __pycache__`
   (parts 2+: recap.mp4 too once the series is done). Then write `script.txt` (8 beat texts +
   scene/config notes — one tiny rebuild source) and delete vo1–8.mp3 + anim_part.py + build_pN.py.
   **Keep per part ONLY: final .mp4, upload.txt, script.txt** (RETENTION v2, user Aug 13).
10. write_file upload.txt — title = playbook v2 (absurdity first, EXACTLY 2 emojis, year somewhere),
    description = 2–3 sentences + disbelief closer + `#<Event> #WeirdHistory #History #DidYouKnow #HistoryShorts #Shorts`.
    P1 pin: tease the twist. P2+ pin (REQUIRED): "how it started 👀 on my profile".
11. bash + edits — append the block to UPLOAD_ARCHIVE.md; update VIDEO_FACTORY_PROMPT.md
    (queue 🟡→✅, registry row, Next-up bump); **update FACTORY_TRACKER.xlsx** (add the row:
    ep/part, badge, in-video title, paste-ready upload title w/ emojis, end card, style,
    voice, date — user tracks titles there, keep it current); rebuild the transfer zip if
    manuals changed.
12. present_file the mp4 + paste the upload block in chat. **STOP — wait for "continue"/next number.**

## FAILURE PLAYBOOK (don't panic, don't replan)
- **"AI service is busy" / cut-off turn** → files persist on disk; resume at the exact missing step.
- **TTS moderation block** → soften the wording (no gore/violence specifics), retry that one clip.
- **Build error** → read the tail, fix, rerun — frames already rendered are skipped, rerun costs ~1 min.
