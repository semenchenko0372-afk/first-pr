import sys, json, soundfile as sf
from faster_whisper import WhisperModel
from faster_whisper.vad import get_speech_timestamps, VadOptions
SR = 16000
audio, _ = sf.read(sys.argv[1], dtype="float32")
regions = get_speech_timestamps(audio, VadOptions(min_silence_duration_ms=700, speech_pad_ms=200))
# склеиваем близкие куски речи в реплики
groups = []
for r in regions:
    s, e = r["start"] / SR, r["end"] / SR
    if groups and s - groups[-1][1] < 1.0 and e - groups[-1][0] < 20:
        groups[-1][1] = e
    else:
        groups.append([s, e])
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
out = []
for s, e in groups:
    clip = audio[int(s * SR):int(e * SR)]
    lang, prob, allp = m.detect_language(clip)
    top = sorted(allp, key=lambda x: -x[1])[:3]
    segs, _ = m.transcribe(clip, language=lang, beam_size=5, condition_on_previous_text=False)
    text = " ".join(x.text.strip() for x in segs).strip()
    out.append({"start": round(s, 2), "end": round(e, 2), "lang": lang, "prob": round(prob, 2),
                "top": [[l, round(p, 2)] for l, p in top], "text": text})
    print(f"[{s:7.2f}-{e:7.2f}] {lang} {prob:.2f} {top[1][0]}:{top[1][1]:.2f} | {text}", flush=True)
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE", len(out))
