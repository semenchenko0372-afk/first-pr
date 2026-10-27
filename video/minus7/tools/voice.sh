#!/usr/bin/env bash
# Builds assets/voice.wav from assets/voice/pNN.mp3 placed at the times in voice-timing.txt.
# Run from the project root: bash tools/voice.sh   (then bash tools/mix.sh)
set -euo pipefail
cd "$(dirname "$0")/.."
V=assets/voice
for f in $V/p*.mp3; do
  id=$(basename "$f" .mp3)
  # Trim the synthesiser's leading and trailing silence.
  ffmpeg -loglevel error -y -i "$f" -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse" -ar 48000 -ac 1 "$V/$id.wav"
done
# The whisper: thinner, slower, with a short slap of room.
ffmpeg -loglevel error -y -i $V/p20.wav -af "highpass=f=300,lowpass=f=6000,asetrate=48000*0.92,aresample=48000,atempo=0.95,aecho=0.6:0.5:60|120:0.35|0.2,volume=0.9" $V/p20fx.wav

inputs=(); filt=""; mix=""; i=0
while read -r id t; do
  f=$V/$id.wav; [ "$id" = p20 ] && f=$V/p20fx.wav
  inputs+=(-i "$f")
  ms=$(python3 -c "print(int($t*1000))")
  filt+="[$i:a]adelay=$ms|$ms[a$i];"; mix+="[a$i]"; i=$((i+1))
done < voice-timing.txt
ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "${filt}${mix}amix=inputs=$i:normalize=0,apad=whole_dur=59.7[o]" -map "[o]" -ar 48000 -ac 1 assets/voice.wav
echo "wrote assets/voice.wav"
