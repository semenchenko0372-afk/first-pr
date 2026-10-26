"""Narration with ESpeech-TTS-1 RL-V2 (Russian F5-TTS, Apache 2.0), cloned from a reference clip.

Usage (CPU is fine, ~10-30 s per line):
  python tools/espeech.py --ref ref.wav [--ref-text "..."] --lines lines.tsv --out assets/voice [--speed 0.92]

lines.tsv: "<id>\t<text>" per line. Writes <out>/<id>.wav (24 kHz mono).
Without --ref-text the reference is transcribed with faster-whisper.
"""
import argparse
import pathlib

import soundfile as sf
import torch
import torchaudio
from huggingface_hub import hf_hub_download
from f5_tts.infer.utils_infer import infer_process, load_model, load_vocoder, preprocess_ref_audio_text
from f5_tts.model import DiT
from ruaccent import RUAccent

MODEL_CFG = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)


def _sf_load(path, *args, **kwargs):
    # torchaudio.load now needs torchcodec's native libs; soundfile reads WAV fine.
    wav, sr = sf.read(path, dtype="float32", always_2d=True)
    return torch.from_numpy(wav.T.copy()), sr


torchaudio.load = _sf_load


def transcribe(path: str) -> str:
    from faster_whisper import WhisperModel

    import torchaudio.functional as AF

    wav, sr = sf.read(path, dtype="float32", always_2d=True)
    audio = AF.resample(torch.from_numpy(wav.mean(axis=1)), sr, 16000).numpy()
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio, language="ru", beam_size=5)
    return " ".join(s.text.strip() for s in segments).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--ref-text")
    ap.add_argument("--lines", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--speed", type=float, default=0.92)
    ap.add_argument("--nfe", type=int, default=32)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--only", help="comma-separated ids to render")
    a = ap.parse_args()

    ref_text = a.ref_text or transcribe(a.ref)
    print("reference text:", ref_text)

    model_path = hf_hub_download("ESpeech/ESpeech-TTS-1_RL-V2", "espeech_tts_rlv2.pt")
    vocab_path = hf_hub_download("ESpeech/ESpeech-TTS-1_RL-V2", "vocab.txt")
    model = load_model(DiT, MODEL_CFG, model_path, vocab_file=vocab_path, device="cpu")
    vocoder = load_vocoder(device="cpu")
    acc = RUAccent()
    acc.load(omograph_model_size="turbo3.1", use_dictionary=True, tiny_mode=False)

    ref_audio, ref_text_p = preprocess_ref_audio_text(a.ref, acc.process_all(ref_text))
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
        gen = text if "+" in text else acc.process_all(text)
        wav, sr, _ = infer_process(ref_audio, ref_text_p, gen, model, vocoder,
                                   nfe_step=a.nfe, speed=a.speed, cross_fade_duration=0.15, device="cpu")
        sf.write(out / f"{lid}.wav", wav, sr)
        print("wrote", lid, gen, round(len(wav) / sr, 2), "s", flush=True)


if __name__ == "__main__":
    main()
