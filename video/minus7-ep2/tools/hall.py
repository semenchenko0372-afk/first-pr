"""The minus-seventh-floor corridor from part 1, as reusable SVG.

`hall(p, far)` returns <defs> + world + darkness markup with ids prefixed by `p`.
  far = "monitor" | "lift" | "none" picks what waits at the end of the corridor.
Animate:  {p}-beam (attr cx, cy, r)  torch hole in the darkness
          {p}-warmc (attr cx, cy, r) warm core of the torch
          {p}-world                  the corridor itself (camera moves)
Scratches on the left wall are drawn by `TALLY_JS` (call drawTallies("{p}")).
Run `python3 tools/build.py` to expand %%HALL:<prefix>:<far>%% and %%CHAR:<prefix>%% markers.
"""


def hall(p: str, far: str = "none") -> str:
    ends = {
        "monitor": f"""
        <g id="{p}-far">
          <ellipse cx="540" cy="850" rx="150" ry="110" fill="url(#{p}-mglow)" />
          <rect x="497" y="818" width="86" height="64" rx="6" fill="#20252b" />
          <rect x="504" y="824" width="72" height="50" fill="#d8f7ff" />
        </g>""",
        "lift": f"""
        <g id="{p}-far">
          <ellipse cx="540" cy="830" rx="260" ry="200" fill="url(#{p}-redglow)" />
          <rect x="470" y="740" width="140" height="210" fill="#b0261d" />
          <rect x="478" y="748" width="124" height="202" fill="#e2463a" opacity="0.65" />
          <rect x="440" y="728" width="200" height="14" fill="#1a1c20" />
          <rect x="455" y="740" width="15" height="210" fill="#2a2e33" />
          <rect x="610" y="740" width="15" height="210" fill="#2a2e33" />
        </g>""",
        "none": "",
    }[far]
    return f"""
<defs>
  <linearGradient id="{p}-ceil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#555b63" /><stop offset="1" stop-color="#1d2024" /></linearGradient>
  <linearGradient id="{p}-floor" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#6c6e72" /><stop offset="1" stop-color="#24262a" /></linearGradient>
  <linearGradient id="{p}-wl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#848a92" /><stop offset="1" stop-color="#2a2e33" /></linearGradient>
  <linearGradient id="{p}-wr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#7a8087" /><stop offset="1" stop-color="#272b30" /></linearGradient>
  <radialGradient id="{p}-hole" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#000" /><stop offset="0.55" stop-color="#000" stop-opacity="0.75" /><stop offset="1" stop-color="#fff" />
  </radialGradient>
  <radialGradient id="{p}-warm" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff3d6" stop-opacity="0.38" /><stop offset="1" stop-color="#fff3d6" stop-opacity="0" />
  </radialGradient>
  <radialGradient id="{p}-mglow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#bff3ff" stop-opacity="0.75" /><stop offset="1" stop-color="#bff3ff" stop-opacity="0" />
  </radialGradient>
  <radialGradient id="{p}-redglow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#ff3a2a" stop-opacity="0.55" /><stop offset="1" stop-color="#ff3a2a" stop-opacity="0" />
  </radialGradient>
  <mask id="{p}-mask" maskUnits="userSpaceOnUse" x="-400" y="-400" width="1880" height="2720">
    <rect x="-400" y="-400" width="1880" height="2720" fill="#fff" />
    <circle id="{p}-beam" cx="540" cy="900" r="0" fill="url(#{p}-hole)" />
  </mask>
</defs>
<g id="{p}-world">
  <polygon points="0,0 1080,0 690,700 390,700" fill="url(#{p}-ceil)" />
  <polygon points="0,1920 1080,1920 690,950 390,950" fill="url(#{p}-floor)" />
  <polygon points="0,0 390,700 390,950 0,1920" fill="url(#{p}-wl)" />
  <polygon points="1080,0 690,700 690,950 1080,1920" fill="url(#{p}-wr)" />
  <rect x="390" y="700" width="300" height="250" fill="#101215" />
  <g stroke="#0e1013" stroke-width="4" opacity="0.7">
    <line x1="0" y1="560" x2="390" y2="810" /><line x1="1080" y1="560" x2="690" y2="810" />
    <line x1="180" y1="320" x2="180" y2="1480" /><line x1="300" y1="535" x2="300" y2="1170" />
    <line x1="900" y1="320" x2="900" y2="1480" /><line x1="780" y1="535" x2="780" y2="1170" />
  </g>
  <path d="M120 0 L455 700" stroke="#2b2f34" stroke-width="34" />
  <path d="M120 0 L455 700" stroke="#6c737b" stroke-width="6" opacity="0.5" />
  <path d="M230 0 L475 700" stroke="#24282c" stroke-width="20" />
  <g fill="none" stroke="#2a2e33" stroke-width="6"><rect x="460" y="300" width="160" height="40" /><rect x="500" y="520" width="80" height="20" /></g>
  <polygon points="840,560 960,430 960,1580 840,1260" fill="#24282d" />
  <polygon points="850,580 950,470 950,1540 850,1240" fill="none" stroke="#0d0f12" stroke-width="5" />
  <circle cx="868" cy="930" r="8" fill="#6a6f75" />
  <g id="{p}-scratch" stroke="#c9ccd0" stroke-width="3" opacity="0.55" fill="none"></g>
  <g transform="matrix(0.62 0.42 0 1 60 900)" font-family="Space Mono, monospace" font-size="38" fill="#d6d9dc" opacity="0.6">
    <text x="0" y="0">23:47</text><text x="0" y="60">23:47</text><text x="120" y="20">23:47</text>
    <text x="20" y="130">23:47</text><text x="140" y="100">23:47</text><text x="60" y="200">23:47</text>
  </g>
  <ellipse cx="380" cy="1500" rx="170" ry="34" fill="#7d8792" opacity="0.18" />
  <ellipse cx="700" cy="1250" rx="110" ry="18" fill="#7d8792" opacity="0.14" />
  <path d="M1080 1700 C900 1650 760 1500 640 1300 C600 1220 600 1100 560 950" stroke="#0b0c0e" stroke-width="12" fill="none" />
  <rect x="470" y="880" width="140" height="70" fill="#1a1c20" />
</g>
<rect x="-400" y="-400" width="1880" height="2720" fill="#000" mask="url(#{p}-mask)" opacity="0.93" />
<circle id="{p}-warmc" cx="540" cy="900" r="0" fill="url(#{p}-warm)" />
{ends}"""


TALLY_JS = """
function drawTallies(p) {
  const NS = "http://www.w3.org/2000/svg";
  let seed = 19;
  const r = () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const sc = document.getElementById(p + "-scratch");
  for (let k = 0; k < 16; k++) {
    const x0 = 30 + r() * 280, y0 = 880 + r() * 420, sy = 0.6 + (x0 / 390) * -0.2;
    for (let i = 0; i < 5; i++) {
      const l = document.createElementNS(NS, "line"), x = x0 + i * 10;
      l.setAttribute("x1", x); l.setAttribute("y1", y0 + x * 0.5 * sy);
      l.setAttribute("x2", x + 2); l.setAttribute("y2", y0 + 46 + x * 0.5 * sy);
      if (i === 4) { l.setAttribute("x1", x0 - 6); l.setAttribute("y1", y0 + 10); l.setAttribute("x2", x0 + 44); l.setAttribute("y2", y0 + 34); }
      sc.appendChild(l);
    }
  }
}
"""
