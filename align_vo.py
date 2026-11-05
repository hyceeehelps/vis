"""align_vo — TRUE caption sync for the paSTory factory.
Listens to each voI.mp3 with a small Vosk ASR model (downloaded to /tmp, never the
workspace) and returns per-word start times. Matches ASR words to the script's words
(difflib, homophone/OOV-safe) and converts to per-scene caption schedules.

Builder use:
    import align_vo
    sched = align_vo.build([f'vo{i+1}.mp3' for i in range(N)], AN.BEATS, segs, rate)
    # sched[i] = list of per-word START fractions (0..1) within scene i, or None on failure
    ce.render_scene(..., caption_schedule=sched[i])
Falls back gracefully: if Vosk/model/audio fail, .build() raises and the builder's
weighted estimator takes over (schedule=None).
"""
import difflib, json, os, subprocess, sys, wave, zipfile, urllib.request

MODEL_DIR = '/tmp/vosk-model-small-en-us-0.15'
MODEL_URL = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'
_m = None

def _model():
    global _m
    if _m is not None:
        return _m
    try:
        import vosk
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'vosk'], check=True)
        import vosk
    if not os.path.isdir(MODEL_DIR):
        dst = '/tmp/vosk-model.zip'
        urllib.request.urlretrieve(MODEL_URL, dst)
        zipfile.ZipFile(dst).extractall('/tmp')
        os.remove(dst)
    vosk.SetLogLevel(-1)
    _m = vosk.Model(MODEL_DIR)
    return _m

def words_of(mp3_path):
    """ASR a vo clip -> [(word, start, end), ...] in clip-relative seconds."""
    import imageio_ffmpeg
    import vosk
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    wav = '/tmp/_align_%d.wav' % (abs(hash(mp3_path)) % 99999)
    subprocess.run([ff, '-y', '-i', mp3_path, '-ar', '16000', '-ac', '1', wav],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    rec = vosk.KaldiRecognizer(_model(), 16000)
    rec.SetWords(True)
    with wave.open(wav, 'rb') as wf:
        while True:
            data = wf.readframes(4000)
            if not data:
                break
            rec.AcceptWaveform(data)
    res = json.loads(rec.FinalResult())
    try:
        os.remove(wav)
    except OSError:
        pass
    return [(w['word'], float(w['start']), float(w['end'])) for w in res.get('result', [])]

def _norm(w):
    return ''.join(ch for ch in w.upper() if ch.isalnum())

def align(script_words, recog):
    """Per-word start SECONDS (clip-relative) for each script word.
    Anchors on exact token matches (homophones are anchored by their neighbors),
    interpolates the gaps by character weight."""
    A = [_norm(w) for w in script_words]
    B = [_norm(r[0]) for r in recog]
    n = len(script_words)
    starts = [None] * n
    anchors = []                                   # (script_idx, time of ASR START)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                anchors.append((i1 + k, recog[j1 + k][1], recog[j1 + k][2]))
    if not anchors:                                # ASR produced nothing usable
        span = (recog[-1][2] if recog else 1.0) / n
        return [k * span for k in range(n)]
    # leading words: fan out from 0 to first anchor
    first_a, first_s, _ = anchors[0]
    lead = A[:first_a]
    if lead:
        tot = sum(1 + len(w) for w in lead) or 1
        acc = 0.0
        for k, w in enumerate(lead):
            starts[k] = acc
            acc += first_s * (1 + len(w)) / tot
    # interior gaps between anchors
    for (a0, s0, e0), (a1, s1, _e1) in zip(anchors, anchors[1:]):
        starts[a0] = s0
        gap_words = A[a0 + 1:a1]
        if gap_words:
            tot = sum(1 + len(w) for w in gap_words) or 1
            acc = e0
            span = max(s1 - e0, 0.0)
            for k, w in enumerate(gap_words):
                starts[a0 + 1 + k] = acc
                acc += span * (1 + len(w)) / tot
    # trailing words after the last anchor
    last_a, last_s, last_e = anchors[-1]
    starts[last_a] = last_s
    tail = A[last_a + 1:]
    if tail:
        clip_end = recog[-1][2]
        tot = sum(1 + len(w) for w in tail) or 1
        acc = last_e
        span = max(clip_end - last_e, 0.0)
        for k, w in enumerate(tail):
            starts[last_a + 1 + k] = acc
            acc += span * (1 + len(w)) / tot
    return [0.0 if s is None else s for s in starts]

def build(vos, beats, segs, rate):
    """vos=[vo paths], beats=[word lists], segs=scene durations, rate=atempo factor.
    Returns per-scene list of word-START fractions (0..0.995)."""
    out = []
    for i, vo in enumerate(vos):
        recog = words_of(vo)
        st = align(beats[i], recog)                 # seconds, clip-relative
        fr = [min(0.995, max(0.0, (s / rate) / segs[i])) for s in st]
        out.append(fr)
    return out
