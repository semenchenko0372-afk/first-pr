import sys, torch, soundfile as sf, numpy as np
torch.set_num_threads(2)
from demucs.pretrained import get_model
from demucs.apply import apply_model
m = get_model("htdemucs"); m.eval()
wav, sr = sf.read(sys.argv[1], dtype="float32", always_2d=True)
x = torch.from_numpy(wav.T.copy())
ref = x.mean(0); x = (x - ref.mean()) / ref.std()
with torch.no_grad():
    out = apply_model(m, x[None], device="cpu", split=True, overlap=0.1, progress=True)[0]
out = out * ref.std() + ref.mean()
v = m.sources.index("vocals")
sf.write("vocals.wav", out[v].T.numpy(), sr)
sf.write("background.wav", (out.sum(0) - out[v]).T.numpy(), sr)
print("SEP DONE")
