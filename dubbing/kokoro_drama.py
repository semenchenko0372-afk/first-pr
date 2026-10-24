import re, sys, time, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro(sys.argv[1] + "/kokoro-v1.0.onnx", sys.argv[1] + "/voices-v1.0.bin")
text = open(sys.argv[2], encoding="utf-8").read()
SPEED, SENT_PAUSE, PARA_PAUSE = 0.85, 0.55, 1.3
paras = [p.strip() for p in text.split("\n\n") if p.strip()]
for voice in sys.argv[4:]:
    t = time.time(); out = []; sr = 24000
    lang = "en-us" if voice[0] == "a" else "en-gb"
    for p in paras:
        sents = []
        for s in re.split(r'(?<=[.!?])\s+|(?<=[.!?]["”])\s+', p):
            if sents and re.search(r'\b(Mr|Mrs|Ms|Dr|St)\.$', sents[-1]):
                sents[-1] += " " + s  # не разрывать "Mrs. Patel"
            elif s:
                sents.append(s)
        for i, s in enumerate(sents):
            a, sr = k.create(s, voice=voice, speed=SPEED, lang=lang)
            pause = PARA_PAUSE if i == len(sents) - 1 else SENT_PAUSE
            out += [a, np.zeros(int(sr * pause), dtype=a.dtype)]
    sf.write(f"{sys.argv[3]}_{voice}.wav", np.concatenate(out), sr)
    print(voice, "ok", round(time.time() - t), "s")
