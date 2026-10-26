"""Narration with Chatterbox Multilingual (Resemble AI, MIT), cloned from a reference clip.

Usage:
  python tools/chatterbox_tts.py --ref ref.wav --lines lines.tsv --out DIR [--exaggeration 0.7] [--cfg 0.3]

lines.tsv: "<id>\t<text>" per line; writes DIR/<id>.wav.
exaggeration raises emotional intensity (0.5 neutral, 0.7-1.0 dramatic); a lower cfg slows and loosens delivery.
Chatterbox embeds an inaudible Perth watermark in its output.
"""
import argparse
import pathlib

import soundfile as sf
import torch
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--lines", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--exaggeration", type=float, default=0.7)
    ap.add_argument("--cfg", type=float, default=0.3)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--only", help="comma-separated ids to render")
    a = ap.parse_args()

    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    for row in pathlib.Path(a.lines).read_text().splitlines():
        if not row.strip():
            continue
        lid, text = row.split("\t", 1)
        if only and lid not in only:
            continue
        torch.manual_seed(a.seed)
        wav = model.generate(text, language_id="ru", audio_prompt_path=a.ref,
                             exaggeration=a.exaggeration, cfg_weight=a.cfg, temperature=a.temperature)
        sf.write(out / f"{lid}.wav", wav.squeeze(0).numpy(), model.sr)
        print("wrote", lid, text, round(wav.shape[-1] / model.sr, 2), "s", flush=True)


if __name__ == "__main__":
    main()
