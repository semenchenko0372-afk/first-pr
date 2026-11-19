"""Find candidate highlight moments in a stream recording.

Usage: python3 -I find_moments.py <video> <out_dir> [top_n]
Scores 1-second loudness (ffmpeg ebur128 momentary), transcribes with
faster-whisper, then ranks ~30s windows by loudness peaks + speech energy
(exclamations, caps, swears, laughter).
"""
import json, re, subprocess, sys
from pathlib import Path

video, out = Path(sys.argv[1]), Path(sys.argv[2])
top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
out.mkdir(parents=True, exist_ok=True)

# 1. Loudness per second
p = subprocess.run(["ffmpeg", "-nostats", "-i", str(video), "-vn", "-af", "ebur128", "-f", "null", "-"],
                   capture_output=True, text=True)
loud = {}
for m in re.finditer(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)", p.stderr):
    loud[int(float(m.group(1)))] = max(loud.get(int(float(m.group(1))), -120), float(m.group(2)))
dur = max(loud) if loud else 0

# 2. Transcript
import numpy as np
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
                      "-f", "s16le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = model.transcribe(audio, language="en", vad_filter=True, word_timestamps=False)
segments = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs]
(out / "transcript.json").write_text(json.dumps(segments, ensure_ascii=False, indent=1))

HYPE = re.compile(r"\b(oh my god|bro|what|no+|yes+|let'?s go|w+h+a+t|ayo|bruh|haha+|crazy|insane|run|help|cops?|police|shoot|dead|died|wow|holy)\b", re.I)
SWEAR = re.compile(r"\b(f+u+c+k\w*|shit\w*|damn|hell)\b", re.I)

def speech_score(a, b):
    s = 0.0
    for seg in segments:
        if seg["end"] < a or seg["start"] > b:
            continue
        t = seg["text"]
        s += len(HYPE.findall(t)) * 1.0 + len(SWEAR.findall(t)) * 1.5 + t.count("!") * 0.5
        s += sum(1 for w in t.split() if len(w) > 2 and w.isupper()) * 0.7
    return s

vals = sorted(loud.values())
base = vals[len(vals) // 2] if vals else -30
WIN = 30
cands = []
for start in range(0, max(1, dur - WIN), 5):
    window = [loud.get(t, -120) for t in range(start, start + WIN)]
    peak = max(window)
    spikes = sum(1 for v in window if v > base + 8)
    score = (peak - base) * 0.6 + spikes * 0.8 + speech_score(start, start + WIN) * 1.2
    cands.append((score, start))
cands.sort(reverse=True)
picked = []
for score, start in cands:
    if all(abs(start - s) >= WIN for _, s in picked):
        picked.append((score, start))
    if len(picked) >= top_n:
        break
picked.sort(key=lambda x: x[1])
result = []
for score, start in picked:
    text = " ".join(s["text"] for s in segments if s["end"] >= start and s["start"] <= start + WIN)
    result.append({"start": start, "end": start + WIN, "score": round(score, 1), "text": text})
(out / "moments.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
for r in result:
    print(f"{r['start']//60:02d}:{r['start']%60:02d}  score={r['score']}  {r['text'][:160]}")
