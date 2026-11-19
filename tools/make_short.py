"""Cut a vertical 1080x1920 short: facecam on top, gameplay below, burned subtitles.

Usage: python3 -I make_short.py <video> <transcript.json> <start> <end> <out.mp4> [cam=x,y,w,h]
cam is the facecam box in source pixels; omit (or 'none') for gameplay-only layout.
"""
import json, subprocess, sys
from pathlib import Path

video, tr, start, end, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), Path(sys.argv[5])
cam = sys.argv[6] if len(sys.argv) > 6 else "none"
segs = json.loads(Path(tr).read_text()) if tr != "none" else []

def ts(t):
    t = max(0.0, t)
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{int(t%60):02d}.{int(t*100%100):02d}"

# ASS subtitles, short chunks of <=4 words timed proportionally inside each segment
ass = out.with_suffix(".ass")
lines = ["[Script Info]", "PlayResX: 1080", "PlayResY: 1920", "",
         "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginV",
         "Style: D, DejaVu Sans, 78, &H00FFFFFF, &H00000000, &H80000000, 1, 1, 6, 2, 5, 0", "",
         "[Events]", "Format: Layer, Start, End, Style, Text"]
for s in segs:
    if s["end"] < start or s["start"] > end:
        continue
    words = s["text"].split()
    if not words:
        continue
    chunks = [words[i:i + 4] for i in range(0, len(words), 4)]
    span = (s["end"] - s["start"]) / len(chunks)
    for i, c in enumerate(chunks):
        a = s["start"] + i * span - start
        b = a + span
        if b < 0 or a > end - start:
            continue
        lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},D,{{\\pos(540,1060)}}{' '.join(c).upper()}")
ass.write_text("\n".join(lines) + "\n")

if cam != "none":
    x, y, w, h = map(int, cam.split(","))
    vf = (f"[0:v]crop={w}:{h}:{x}:{y},scale=1080:-2,crop=1080:min(ih\\,700)[cam];"
          f"[0:v]crop=ih*1080/1220:ih,scale=1080:1220[game];"
          f"[cam][game]vstack,pad=1080:1920:0:(1920-ih)/2:black,subtitles={ass}[v]")
else:
    vf = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];"
          f"[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,subtitles={ass}[v]")

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-to", str(end), "-i", video,
                "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-r", "30",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart", str(out)], check=True)
print(out)
