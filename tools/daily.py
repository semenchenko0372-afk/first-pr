"""Daily picker: top Twitch clip of the last 24h from N different GTA 6 streamers.

Usage: python3 -I tools/daily.py <work_dir> [count]
- Skips clip ids already listed in tools/used_clips.txt.
- Downloads the chosen clips and transcribes them (tools/find_moments.py).
- Writes <work_dir>/picks.json: [{channel, title, views, duration, url, file, transcript}]
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
work = Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
channels = [c.strip() for c in (ROOT / "channels.txt").read_text().split() if c.strip()]
used_file = ROOT / "used_clips.txt"
used = set(used_file.read_text().split()) if used_file.exists() else set()

best = []
for ch in channels:
    p = subprocess.run(["yt-dlp", "--flat-playlist", "--playlist-end", "6", "--print",
                        "%(id)s\t%(view_count)s\t%(duration)s\t%(webpage_url)s\t%(title)s",
                        f"https://www.twitch.tv/{ch}/clips?filter=clips&range=24hr"],
                       capture_output=True, text=True, timeout=120)
    for line in p.stdout.splitlines():
        parts = line.split("\t", 4)
        if len(parts) < 5 or parts[0] in used:
            continue
        cid, views, dur, url, title = parts
        try:
            views, dur = int(views), float(dur)
        except ValueError:
            continue
        if dur < 12:  # too short to be a short
            continue
        clip = {"id": cid, "channel": ch, "views": views, "duration": dur, "url": url, "title": title}
        # listing order is not reliably by views: keep this channel's most-viewed unused clip
        prev = next((b for b in best if b["channel"] == ch), None)
        if prev is None:
            best.append(clip)
        elif views > prev["views"]:
            best[best.index(prev)] = clip

best.sort(key=lambda c: c["views"], reverse=True)
picks = best[:count + 4]  # spares: some clips turn out off-topic or not ad-safe
for c in picks:
    out = work / f"{c['channel']}_{c['id']}.mp4"
    subprocess.run(["yt-dlp", "-q", "-f", "b", "-o", str(out), c["url"]], check=False, timeout=600)
    c["file"] = str(out)
    an = work / f"an_{c['channel']}"
    subprocess.run([sys.executable, "-I", str(ROOT / "find_moments.py"), str(out), str(an), "1"],
                   capture_output=True, timeout=1800)
    c["transcript"] = str(an / "transcript.json")
(work / "picks.json").write_text(json.dumps(picks, ensure_ascii=False, indent=1))
for c in picks:
    print(f"{c['channel']:<16} {c['views']:>7}  {c['duration']:>4.0f}s  {c['title'][:70]}")
