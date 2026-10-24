"""Заменяет выбранные реплики английской озвучкой Kokoro поверх оригинального фона.
Использование: mix_dub.py plan.json vocals.wav background.wav kokoro_dir out.wav
plan.json: [{"start": сек, "end": сек, "text": "...", "voice": "af_heart"}]"""
import json, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
from kokoro_onnx import Kokoro

plan_p, voc_p, bg_p, kdir, out_p = sys.argv[1:6]
plan = sorted(json.load(open(plan_p, encoding="utf-8")), key=lambda x: x["start"])
voc, sr = sf.read(voc_p, dtype="float32", always_2d=True)
bg, _ = sf.read(bg_p, dtype="float32", always_2d=True)
k = Kokoro(f"{kdir}/kokoro-v1.0.onnx", f"{kdir}/voices-v1.0.bin")
FADE = int(0.05 * sr)
dub = np.zeros_like(voc)
gain_env = np.ones(len(voc), dtype="float32")  # 0 там, где оригинальный голос заглушён

def tts(text, voice, speed):
    a, ksr = k.create(text, voice=voice, speed=speed, lang="en-us" if voice[0] == "a" else "en-gb")
    return resample_poly(a, sr, ksr).astype("float32")

for i, p in enumerate(plan):
    s, e = int(p["start"] * sr), int(p["end"] * sr)
    nxt = int(plan[i + 1]["start"] * sr) if i + 1 < len(plan) else len(voc)
    room = min(nxt, len(voc)) - s - int(0.1 * sr)   # можно залезть в паузу до следующей реплики
    speed, a = 1.0, tts(p["text"], p["voice"], 1.0)
    while len(a) > room and speed < 1.35:
        speed = round(speed + 0.08, 2)
        a = tts(p["text"], p["voice"], speed)
    a = a[:max(room, 1)]
    # громкость как у оригинальной реплики
    orig = voc[s:e].mean(1)
    rms_o = float(np.sqrt((orig ** 2).mean()) + 1e-6)
    rms_a = float(np.sqrt((a ** 2).mean()) + 1e-6)
    a *= min(rms_o / rms_a, 4.0)
    dub[s:s + len(a)] += a[:, None]
    # заглушаем оригинальный голос на всё время реплики (и оригинала, и дубляжа)
    ms, me = s, max(e, s + len(a))
    gain_env[ms:me] = 0
    gain_env[max(ms - FADE, 0):ms] = np.minimum(gain_env[max(ms - FADE, 0):ms], np.linspace(1, 0, ms - max(ms - FADE, 0)))
    gain_env[me:me + FADE] = np.minimum(gain_env[me:me + FADE], np.linspace(0, 1, len(gain_env[me:me + FADE])))
    print(f"[{p['start']:7.2f}] speed={speed} {len(a)/sr:.1f}s/{(e-s)/sr:.1f}s  {p['text'][:60]}", flush=True)

mix = bg[:len(voc)] + voc * gain_env[:, None] + dub
peak = float(np.abs(mix).max())
if peak > 0.99:
    mix *= 0.99 / peak
sf.write(out_p, mix, sr)
print("MIX DONE", round(len(mix) / sr, 1), "s")
