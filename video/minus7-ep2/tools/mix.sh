#!/usr/bin/env bash
# Builds assets/soundtrack.wav: narration + music bed + timed effects.
# Run from the project root: bash tools/mix.sh
set -euo pipefail
cd "$(dirname "$0")/.."
S=assets/sfx
DUR=61

# name  file                    start(s)  volume
cues=(
  "breath0    $S/breath.mp3           0.10  0.30"
  "turn       $S/whoosh-cinematic.mp3 0.90  0.30"
  "cctv       $S/glitch-3.mp3         5.60  0.30"
  "looks      $S/impact-bass-2.mp3   11.60  0.70"
  "crtoff     $S/crtoff.mp3          14.30  0.70"
  "reflect    $S/impact-bass-1.mp3   19.45  0.85"
  "run        $S/run.mp3             21.40  0.80"
  "breath1    $S/breath.mp3          22.60  0.55"
  "doorclose  $S/doorclose.mp3       24.60  0.75"
  "faceflash  $S/glitch-1.mp3        25.55  0.45"
  "buttons1   $S/buttons.mp3         26.90  0.70"
  "buttons2   $S/buttons.mp3         28.40  0.70"
  "liftup     $S/liftup.mp3          30.20  0.60"
  "tick3      $S/click-soft.mp3      32.70  0.30"
  "tick2      $S/click-soft.mp3      34.00  0.30"
  "tick1      $S/click-soft.mp3      35.30  0.30"
  "tick0      $S/click-soft.mp3      37.20  0.35"
  "jolt       $S/impact-bass-2.mp3   38.00  0.60"
  "ding       $S/ding.mp3            40.85  0.55"
  "doors      $S/whoosh-cinematic.mp3 41.00 0.30"
  "scratch    $S/scratch.mp3         45.40  0.75"
  "heart      $S/heartbeat.wav       49.80  0.70"
  "black      $S/impact-bass-1.mp3   56.00  0.85"
)

# Music bed: a later, darker stretch of the same track as part 1.
inputs=(-i assets/voice.wav -ss 60 -t $DUR -i "$S/Ossuary_6_-_Air.mp3")
filters="[0:a]aresample=48000,volume=1.0[voice];"
filters+="[1:a]aresample=48000,volume=0.42,afade=t=in:d=2,volume='if(between(t,48.3,56.0),0.45,if(gt(t,56.0),0,1))':eval=frame[bed];"
mixes="[voice][bed]"
n=2
for c in "${cues[@]}"; do
  read -r name file start vol <<<"$c"
  ms=$(python3 -c "print(int($start*1000))")
  inputs+=(-i "$file")
  filters+="[$n:a]aresample=48000,aformat=channel_layouts=mono,volume=$vol,adelay=$ms|$ms[c$n];"
  mixes+="[c$n]"
  n=$((n+1))
done
filters+="${mixes}amix=inputs=$n:normalize=0:duration=longest,atrim=0:$DUR,alimiter=limit=0.89,loudnorm=I=-15:TP=-1.5:LRA=11[out]"

ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -ac 2 assets/soundtrack.wav
echo "wrote assets/soundtrack.wav"
