#!/usr/bin/env bash
# Builds assets/soundtrack.wav: narration + music bed + timed effects.
# Run from the project root: bash tools/mix.sh
set -euo pipefail
cd "$(dirname "$0")/.."
S=assets/sfx
DUR=59.7

# name  file                    start(s)  volume  extra filter
cues=(
  "click      $S/click.mp3            8.00  0.55"
  "rumble     RUMBLE                  9.10  0.50"
  "tick5      $S/click-soft.mp3       9.30  0.30"
  "tick4      $S/click-soft.mp3      11.01  0.30"
  "tick3      $S/click-soft.mp3      12.99  0.30"
  "tick2      $S/click-soft.mp3      14.00  0.30"
  "tick1      $S/click-soft.mp3      15.82  0.30"
  "race       $S/glitch-3.mp3        17.20  0.35"
  "flick1     $S/glitch-1.mp3        19.05  0.40"
  "minus7     $S/impact-bass-1.mp3   20.80  0.75"
  "flick2     $S/glitch-3.mp3        23.40  0.25"
  "doors      $S/whoosh-cinematic.mp3 26.00 0.35"
  "torch      $S/click.mp3           28.55  0.60"
  "cctv       $S/glitch-3.mp3        33.75  0.35"
  "figure     $S/impact-bass-2.mp3   41.90  0.70"
  "glitchfig  $S/glitch-1.mp3        42.15  0.40"
  "riser      $S/riser.mp3           45.00  0.30"
  "heart      $S/heartbeat.wav       46.80  0.80"
  "black      $S/impact-bass-1.mp3   54.95  0.85"
)

inputs=(-i assets/voice.wav -ss 0 -t $DUR -i "$S/Ossuary_6_-_Air.mp3")
filters="[0:a]aresample=48000,volume=1.0[voice];"
# Music bed: rises with the track, drops away under the whisper, gone on the black card.
filters+="[1:a]aresample=48000,volume=0.55,afade=t=in:d=1.5,volume='if(between(t,52.1,54.95),0.35,if(gt(t,54.95),0,1))':eval=frame[bed];"
mixes="[voice][bed]"
n=2
for c in "${cues[@]}"; do
  read -r name file start vol <<<"$c"
  ms=$(python3 -c "print(int($start*1000))")
  if [ "$file" = RUMBLE ]; then
    # Elevator travel: band-limited brown noise, 9.8 s, fades in and out.
    inputs+=(-f lavfi -t 9.8 -i "anoisesrc=color=brown:seed=7:sample_rate=48000")
    filters+="[$n:a]highpass=f=70,lowpass=f=420,volume=$vol,afade=t=in:d=0.8,afade=t=out:st=8.6:d=1.2,adelay=$ms|$ms[c$n];"
  else
    inputs+=(-i "$file")
    filters+="[$n:a]aresample=48000,aformat=channel_layouts=mono,volume=$vol,adelay=$ms|$ms[c$n];"
  fi
  mixes+="[c$n]"
  n=$((n+1))
done
filters+="${mixes}amix=inputs=$n:normalize=0:duration=longest,atrim=0:$DUR,alimiter=limit=0.89,loudnorm=I=-15:TP=-1.5:LRA=11[out]"

ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -ac 2 assets/soundtrack.wav
echo "wrote assets/soundtrack.wav"
