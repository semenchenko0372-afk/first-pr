import sys, time, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro(sys.argv[1] + "/kokoro-v1.0.onnx", sys.argv[1] + "/voices-v1.0.bin")
text = open(sys.argv[2], encoding="utf-8").read()
paras = [p.strip() for p in text.split("\n\n") if p.strip()]
for voice in sys.argv[4:]:
    t = time.time(); out = []; sr = 24000
    for p in paras:
        a, sr = k.create(p, voice=voice, speed=0.92, lang="en-us" if voice[0] == "a" else "en-gb")
        out += [a, np.zeros(int(sr * 0.8), dtype=a.dtype)]
    sf.write(f"{sys.argv[3]}_{voice}.wav", np.concatenate(out), sr)
    print(voice, "ok", round(time.time() - t), "s")
