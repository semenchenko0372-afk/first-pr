import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
import soundfile as sf
audio, _ = sf.read(sys.argv[1], dtype="float32")
segs, info = m.transcribe(audio, beam_size=5)
print("LANG", info.language, round(info.language_probability, 2))
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
