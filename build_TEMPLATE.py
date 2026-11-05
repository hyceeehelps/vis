"""CLIPART UNIVERSAL BUILDER — one file builds ANY part of any episode.
USAGE:
  1. In your part folder (e.g. episode_video/part2/), save scenes as  anim_part.py
     (import clipart_engine via sys.path, define SCENES, NIGHT, BEATS — see SAMPLE_anim_part.py)
  2. Put vo1.mp3…voN.mp3 in the same folder.
  3. Fill the CONFIG block below. Run:  python3 build_TEMPLATE.py   (renamed copy is fine)
  4. Keep clipart_engine.py at /home/user (or set FACTORY_ROOT env to its folder).
"""
import subprocess, re, sys, os, math
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.environ.get('FACTORY_ROOT', '/home/user'))
import clipart_engine as ce
import anim_part as AN   # <-- your scene file: SCENES, NIGHT, BEATS
ART = getattr(AN, 'ART', None)   # optional art engine (module) for full-canvas scenes

# ------------------------------- CONFIG --------------------------------------
OUT_BASE  = 'Episode_Title_PartN'
PART_NUM  = 1                 # 1 = no recap, shows title card | 2+ = 5s recap opens the video
FINAL     = False             # True only for the LAST part: adds the "EVENT — YEAR" end card
TITLE_LINES   = ['THE EVENT TITLE', 'LINE TWO']          # part 1 only
ENDCARD_LINES = ['THE EVENT NAME', '— 1788 —']           # FINAL part only
ENDCARD_LIGHT_TEXT = False    # False = black ink (day scene) | True = white (dusk/night scene)
RECAP_SRC = '../part1/Part1_File_Name.mp4'               # parts 2+ only (previous part's file)
N     = 8
GAPS  = [0.2] * 7 + [1.2]    # tail gap; FINAL parts often use [0.2]*7 + [1.8] to let the card breathe
FADE_IN, FADE_OUT = 'white', 'white'   # use 'black' when opening/closing scene is night
BADGE = True                 # top pill: "PART N" / "FINAL PART N" (user rule, Aug 12)
CANVAS = (1080, 1920)        # delivery canvas (all house output is 1080x1920)
RENDER_FPS = 15              # frame PNGs per second (builder retimes to 30fps on encode)
CAP_KW = {}                  # caption style overrides, e.g. {'y_frac':0.80,'size':78}
TITLE_Y = 0.22               # title card centre (clipart); art-engine formats often need 0.12
DRIFT = 0.0                  # slow camera push for full-canvas art parts (e.g. 0.06 = +6%)
SCENE_TARGET = 43.5 if PART_NUM > 1 else 48.5   # manual: 43.5s w/ 5s recap else 48.5s
# ------------------------------------------------------------------------------

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H = CANVAS
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
INK = (28, 28, 28)

def run(cmd, label):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        print(f'FAIL {label}\n{r.stderr[-1500:]}'); sys.exit(1)

def make_overlay(path, lines, y_frac, size, light=False, max_w=940):
    fill = (252, 252, 252) if light else INK
    stroke = (16, 16, 22, 235) if light else (255, 255, 255, 200)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, size)
    while size > 30 and any(d.textlength(l, font=font) > max_w for l in lines):
        size -= 2; font = ImageFont.truetype(FONT_PATH, size)
    spacing = int(size * 1.4)
    y0 = H * y_frac - spacing * (len(lines) - 1) / 2
    for j, line in enumerate(lines):
        d.text((W / 2, y0 + j * spacing), line, font=font, fill=(*fill, 255),
               anchor='mm', stroke_width=max(4, size // 20), stroke_fill=stroke)
    img.save(path)

def make_badge(path, label):
    """Top-center amber pill: 'PART N' / 'FINAL PART N'."""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 42)
    tw = d.textlength(label, font=font)
    pw, ph = tw + 68, 74
    x0, y0 = (W - pw) / 2, 66
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=34,
                        fill=(255, 176, 0, 255), outline=(26, 26, 30, 255), width=5)
    d.text((x0 + pw / 2, y0 + ph / 2 - 2), label, font=font,
           fill=(26, 26, 30, 255), anchor='mm')
    img.save(path)

def duration(path):
    r = subprocess.run([FFMPEG, '-i', path], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))

recap_dur = 0.0
segfiles = []
if PART_NUM > 1:
    run([FFMPEG, '-y', '-sseof', '-5.0', '-i', RECAP_SRC,
         '-vf', 'fps=30,setsar=1,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium',
         '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
         'recap.mp4'], 'recap')
    recap_dur = duration('recap.mp4')
    segfiles.append(os.path.abspath('recap.mp4'))
    print(f'recap: {recap_dur:.2f}s')

raw = [duration(f'vo{i}.mp3') for i in range(1, N + 1)]
natural_total = sum(raw) + sum(GAPS)
rate = max(1.0, natural_total / SCENE_TARGET)
segs = [dd / rate + g for dd, g in zip(raw, GAPS)]
total = recap_dur + sum(segs)
print(f'natural={natural_total:.2f}s  rate={rate:.3f}  final={total:.2f}s')
while total > 49.9:   # squeeze under the 50s ceiling
    SCENE_TARGET -= 0.3
    rate = max(1.0, natural_total / SCENE_TARGET)
    segs = [dd / rate + g for dd, g in zip(raw, GAPS)]
    total = recap_dur + sum(segs)
print(f'locking rate={rate:.3f}  final={total:.2f}s')

# ---- true caption sync: ASR-align every beat (small vosk model lives in /tmp) ----
sched = [None] * N
try:
    import align_vo
    sched = align_vo.build([f'vo{i+1}.mp3' for i in range(N)], AN.BEATS, segs, rate)
    print('captions: ASR-aligned per word (vosk)')
except Exception as e:
    print(f'captions: weighted fallback ({e})')

CAPN = getattr(AN, 'CAP_CHUNK', 2)
for i in range(N):
    nframes = int(math.ceil(segs[i] * RENDER_FPS)) + 1
    print(f'scene {i+1}: {nframes} frames')
    frac = max(0.05, (segs[i] - GAPS[i]) / segs[i])   # speech portion of the scene (no tail gap)
    ce.render_scene(AN.SCENES[i], nframes, f'frames/s{i+1}',
                    AN.BEATS[i], night=AN.NIGHT[i], seed0=(i + 1) * 37,
                    chunk_n=CAPN, caption_frac=frac, caption_schedule=sched[i],
                    bg=AN.BG[i] if hasattr(AN, 'BG') else None,
                    cap_kw=CAP_KW or None, size=(W, H),
                    panel=AN.PANEL_FN[i] if (ART is not None and hasattr(AN, 'PANEL_FN')) else None,
                    drift=DRIFT)

overlays = []
if PART_NUM == 1:
    make_overlay('title.png', TITLE_LINES, TITLE_Y, 96)
if FINAL:
    make_overlay('endcard.png', ENDCARD_LINES, 0.26, 100, light=ENDCARD_LIGHT_TEXT)
if BADGE:
    make_badge('badge.png', f'FINAL PART {PART_NUM}' if FINAL else f'PART {PART_NUM}')

for i in range(N):
    tt = f'atempo={rate},' if rate > 1.001 else ''
    seg = f'seg_{i}.mp4'
    run([FFMPEG, '-y',
         '-framerate', str(RENDER_FPS), '-i', f'frames/s{i+1}/f%04d.png', '-i', f'vo{i+1}.mp3',
         '-filter_complex',
         f"[0:v]fps=30,setsar=1,format=yuv420p,trim=duration={segs[i]:.3f}[v];"
         f"[1:a]aresample=44100,{tt}aformat=channel_layouts=stereo,"
         f"apad=whole_dur={segs[i]:.3f},atrim=duration={segs[i]:.3f}[a]",
         '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
         '-c:a', 'aac', '-b:a', '192k', '-t', f'{segs[i]:.3f}', seg], f'seg{i}')
    segfiles.append(os.path.abspath(seg))

with open('list.txt', 'w') as fh:
    for s in segfiles:
        fh.write(f"file '{s}'\n")
run([FFMPEG, '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'base.mp4'], 'concat')

fc = "[0:v]"
vi = 0
ins = [FFMPEG, '-y', '-i', 'base.mp4']
if PART_NUM == 1:
    ins += ['-loop', '1', '-i', 'title.png']
if FINAL:
    ins += ['-loop', '1', '-i', 'endcard.png']
if BADGE:
    ins += ['-loop', '1', '-i', 'badge.png']
chain = []
cur = '0:v'
step = 0
if PART_NUM == 1:
    chain.append(f"[{cur}][{step+1}:v]overlay=0:0:enable='lte(t,3.6)'[V{step}]"); cur = f'V{step}'; step += 1
if FINAL:
    ec_t = recap_dur + sum(segs[:N - 1]) + 0.9
    ov_i = (1 if PART_NUM == 1 else 0) + 1
    chain.append(f"[{cur}][{ov_i}:v]overlay=0:0:enable='gte(t,{ec_t:.2f})'[V{step}]"); cur = f'V{step}'; step += 1
if BADGE:
    b_i = 1 + (1 if PART_NUM == 1 else 0) + (1 if FINAL else 0)
    chain.append(f"[{cur}][{b_i}:v]overlay=0:0[V{step}]"); cur = f'V{step}'; step += 1
vnode = f'[{cur}]' if step else '[0:v]'
chain.append(f"{vnode}fade=t=in:st=0:d=0.4:color={FADE_IN},"
             f"fade=t=out:st={total-0.7:.2f}:d=0.7:color={FADE_OUT},format=yuv420p[V]")
filt = ';'.join(chain) + (f";[0:a]aformat=channel_layouts=stereo[A0];"
    f"anoisesrc=color=brown:duration={total:.3f}:amplitude=0.03,lowpass=f=500,volume=0.5[amb];"
    f"[A0][amb]amix=inputs=2:duration=first:normalize=0[A]")
run(ins + ['-filter_complex', filt,
     '-map', '[V]', '-map', '[A]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
     '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', f'{total:.3f}',
     f'{OUT_BASE}.mp4'], 'final')

for s in segfiles[1 if PART_NUM > 1 else 0:] + (['base.mp4'] if True else []):
    os.path.exists(s) and os.remove(s)
print(f'DONE -> {OUT_BASE}.mp4 ({total:.2f}s)')
