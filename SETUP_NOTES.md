# 🏭 VIDEO FACTORY — TRANSFER KIT (set up a second Arena account)

## ⚠️ FILE TYPES: Arena chat uploads REJECT `.py` — so the code ships as `.txt`
Upload everything as-is, then tell the receiving agent: **"convert the uploaded .txt code files back to .py"** and it will copy them to `.py` (agents can write any file; only uploads are type-restricted).

## Files in this zip
| File | What it does |
|---|---|
| `VIDEO_FACTORY_PROMPT.md` | THE MASTER MANUAL — queue, rules, style, registry, OPS RULES. Paste its whole text into the new chat (or attach the file + say "read this, you are the factory"). |
| `FACTORY_TEMPLATE.md` | BLANK-LOG universal version of the manual (any niche/account) + full kit restore instructions (txt→py copy commands). Use THIS one to start a fresh series or niche from zero; use the manual to continue THIS channel. |
| `clipart_engine.txt` | The animation engine → agent restores it as `/home/user/clipart_engine.py`. |
| `build_TEMPLATE.txt` | Universal builder → restore as `/home/user/build_TEMPLATE.py`. Copy into each `episode_slug/partN/` folder, edit CONFIG, run. **This is the ONLY builder — episode-folder builders get purged.** |
| `SAMPLE_anim_part.txt` | A real, working scene file (335 Years' War P1) — reference for writing new ones. |
| `align_vo.txt` | Caption-sync module → restore as `/home/user/align_vo.py`. The builder auto-calls it: it ASR-listens to each vo clip (small Vosk model, auto-downloads to /tmp — NOT the workspace) and gives captions TRUE per-word sync. If it fails, builders fall back to the weighted estimator — builds never break. |
| `RESCUE_MESSAGE.txt` | Paste-ready recovery + rules block — use it if a session crashes or before the very first build, your call. |
| `historyclipart_style_ref.jpg` | The look we're riffing on (optional style calibration reference). |
| `UPLOAD_ARCHIVE.md` | Every upload block so far (optional but keeps titles/descriptions consistent). |

## Boot sequence on the new account (2 minutes)
1. Upload ALL files → then say: **"Restore the factory: rename the .txt code files to .py (clipart_engine.txt → /home/user/clipart_engine.py, build_TEMPLATE.txt → /home/user/build_TEMPLATE.py, SAMPLE_anim_part.txt → /home/user/SAMPLE_anim_part.py, align_vo.txt → /home/user/align_vo.py), verify they import (python3 -c \"import clipart_engine, imageio_ffmpeg\"), then read VIDEO_FACTORY_PROMPT.md — you are the video factory. Confirm Next Up."**
2. If a session wipe nuked packages: the agent runs `pip install imageio-ffmpeg` (Pillow + fonts are preinstalled by the sandbox).
3. **Voice**: each account/session gets its own voice — let the agent audition a masculine English narration voice ONCE (it knows how), pick the winner, it reuses it for every clip of that session.
4. Then just send queue numbers / "continue" exactly like here. **ONE PART PER TURN** (TTS tool caps at ~10 clips/turn) — say "continue" for the next part.

## Rules of the line (baked into the prompt file — the MUST-KNOW subset)
- Clipart mode = default style. Min 2 parts per story, 3 for rich ones.
- Top badge on every part: amber pill "PART N" / finale "FINAL PART N"; parts 2+ open with a 5s recap of the previous tail; only the final part gets an end card.
- ≤50s per part, 1080×1920, h264 + AAC, brown-noise ambience.
- 🔴 **Workspace budget: ~128 MB / ~10,000 files — overage is SILENTLY DROPPED.** After each part passes QC: delete frames/, segs*, QC images immediately; after delivery delete previous `*_video` slugs; at boot purge leftovers.
- 🛟 **"AI service is busy" mid-build** = just resend your last message; files persist on disk, the agent resumes the missing step only.
- 🔴 **Voice gate (Aug 13, updated Aug 19)**: default house voice tool unavailable → use the stand-in voice of record: **en-US-GuyNeural via edge-tts** (user-picked by audition, Aug 19). Never switch voices silently; only if the user revokes the stand-in too → STOP and ask.
- **Lean keep-list (Aug 13)**: after a part is delivered, its folder keeps ONLY the final .mp4 + upload.txt + script.txt (beats + scene notes). vo*/anim/build/recap files are deleted immediately after QC + delivery.

## Coordination between the two accounts (avoid collisions)
- Split by queue numbers: e.g. this account takes even milestones, the other takes odd — or simply: whichever account you say "12" in owns that episode's ALL parts.
- Both accounts edit their own copies of the prompt file; at day's end, copy the newest registry/queue lines into ONE master and re-paste to the other account when needed.
