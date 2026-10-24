import sys, json, soundfile as sf
from faster_whisper import WhisperModel
SR = 16000
audio, _ = sf.read(sys.argv[1], dtype="float32")
groups = json.load(open(sys.argv[2], encoding="utf-8"))
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
for g in groups:
    clip = audio[int(g["start"] * SR):int(g["end"] * SR)]
    res = {}
    for lang in ["en", "ru", "zh", "th"]:
        segs = list(m.transcribe(clip, language=lang, beam_size=5, condition_on_previous_text=False)[0])
        if not segs:
            res[lang] = (-9.0, 1.0, "")
            continue
        n = sum(len(s.tokens) for s in segs) or 1
        lp = sum(s.avg_logprob * len(s.tokens) for s in segs) / n
        res[lang] = (round(lp, 3), round(max(s.no_speech_prob for s in segs), 2), " ".join(s.text.strip() for s in segs))
    best = max(res, key=lambda l: res[l][0])
    g["scores"] = {l: v[0] for l, v in res.items()}
    g["texts"] = {l: v[2] for l, v in res.items()}
    g["nospeech"] = res[best][1]
    g["best"] = best
    sc = " ".join(f"{l}:{v[0]}" for l, v in res.items())
    print(f"[{g['start']:7.2f}-{g['end']:7.2f}] BEST={best} ns={res[best][1]} {sc}\n    en: {res['en'][2]}\n    {best}: {res[best][2]}", flush=True)
json.dump(groups, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE")
