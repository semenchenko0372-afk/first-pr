"""The hero's head-and-shoulders rig as SVG, drawn around (0, 0).

`head(p)` returns markup whose ids are prefixed with `p` so the same rig can sit in
several scenes. Animate these groups:
  {p}-head     whole head (tilt, nod)
  {p}-irisL/R  look direction (x, y)
  {p}-lidL/R   blink (scaleY 0 open -> 1 closed, origin at the top of the eye)
  {p}-browL/R  worry (rotation, y)
  {p}-mN / {p}-mO / {p}-mT  mouth states: neutral, open, tight (opacity)
  {p}-sweat    a drop on the temple
Run `python3 tools/char.py build` to substitute %%CHAR:<prefix>%% markers in compositions/.
"""
import pathlib
import re
import sys

SKIN = "#e3ae86"
SKIN_SHADE = "#c48a63"
HAIR = "#1d1512"
HOOD = "#4f6b47"
HOOD_DARK = "#3c5436"


def head(p: str) -> str:
    return f"""
<g id="{p}-char">
  <!-- hoodie and shoulders -->
  <path d="M-360 760 L-350 420 C-340 270 -220 205 -120 190 L120 190 C220 205 340 270 350 420 L360 760 Z" fill="{HOOD}" />
  <path d="M-120 190 C-150 250 -140 320 -90 350 L0 300 L90 350 C140 320 150 250 120 190 Z" fill="{HOOD_DARK}" />
  <path d="M-350 420 C-330 330 -260 270 -190 250 C-230 320 -250 420 -250 760 L-360 760 Z" fill="{HOOD_DARK}" opacity="0.7" />
  <path d="M-38 300 L-46 470" stroke="#d9d3c2" stroke-width="9" stroke-linecap="round" />
  <path d="M38 300 L46 470" stroke="#d9d3c2" stroke-width="9" stroke-linecap="round" />
  <circle cx="-46" cy="476" r="9" fill="#b9b3a2" /><circle cx="46" cy="476" r="9" fill="#b9b3a2" />
  <!-- lanyard and office badge -->
  <path d="M-70 205 L-10 420 M70 205 L10 420" stroke="#b8322b" stroke-width="12" fill="none" />
  <rect x="-48" y="418" width="96" height="128" rx="10" fill="#f2f2ee" stroke="#9a9a94" stroke-width="3" />
  <rect x="-34" y="436" width="34" height="42" rx="4" fill="#8aa0b8" />
  <rect x="6" y="440" width="30" height="7" rx="3" fill="#7d7d78" />
  <rect x="6" y="456" width="22" height="7" rx="3" fill="#a5a59f" />
  <rect x="-34" y="494" width="70" height="8" rx="4" fill="#b8322b" />
  <!-- neck -->
  <path d="M-62 110 L-62 215 C-30 240 30 240 62 215 L62 110 Z" fill="{SKIN_SHADE}" />
  <g id="{p}-head">
    <ellipse cx="-158" cy="-10" rx="26" ry="40" fill="{SKIN}" />
    <ellipse cx="158" cy="-10" rx="26" ry="40" fill="{SKIN_SHADE}" />
    <path d="M-160 -10 q8 -16 6 10" stroke="{SKIN_SHADE}" stroke-width="5" fill="none" />
    <path d="M0 -220 C110 -220 162 -140 162 -40 C162 70 92 152 0 152 C-92 152 -162 70 -162 -40 C-162 -140 -110 -220 0 -220 Z" fill="{SKIN}" />
    <path d="M44 -214 C132 -188 166 -112 162 -30 C156 70 92 150 0 152 C74 120 116 40 102 -60 C92 -140 66 -190 44 -214 Z" fill="{SKIN_SHADE}" opacity="0.6" />
    <ellipse cx="-92" cy="52" rx="30" ry="16" fill="#e98c78" opacity="0.25" />
    <ellipse cx="92" cy="52" rx="30" ry="16" fill="#e98c78" opacity="0.2" />
    <!-- jaw shadow -->
    <path d="M-90 120 C-40 156 40 156 90 120" stroke="{SKIN_SHADE}" stroke-width="10" fill="none" opacity="0.5" />
    <!-- eyes -->
    <g id="{p}-eyeL" transform="translate(-62 -14)">
      <ellipse rx="34" ry="27" fill="#f6f1ea" />
      <g id="{p}-irisL"><circle r="17" fill="#5a3826" /><circle r="8" fill="#140c08" /><circle cx="6" cy="-7" r="5" fill="#ffffff" /></g>
      <path d="M-36 -4 C-26 -30 26 -30 36 -6" stroke="#20160f" stroke-width="7" fill="none" stroke-linecap="round" />
      <ellipse id="{p}-lidL" cx="0" cy="0" rx="37" ry="30" fill="{SKIN}" />
      <path d="M-26 34 C-10 40 10 40 26 33" stroke="{SKIN_SHADE}" stroke-width="5" fill="none" opacity="0.7" />
    </g>
    <g id="{p}-eyeR" transform="translate(62 -14)">
      <ellipse rx="34" ry="27" fill="#f3ece4" />
      <g id="{p}-irisR"><circle r="17" fill="#5a3826" /><circle r="8" fill="#140c08" /><circle cx="6" cy="-7" r="5" fill="#ffffff" /></g>
      <path d="M-36 -6 C-26 -30 26 -30 36 -4" stroke="#20160f" stroke-width="7" fill="none" stroke-linecap="round" />
      <ellipse id="{p}-lidR" cx="0" cy="0" rx="37" ry="30" fill="{SKIN_SHADE}" />
      <path d="M-26 33 C-10 40 10 40 26 34" stroke="{SKIN_SHADE}" stroke-width="5" fill="none" opacity="0.7" />
    </g>
    <!-- brows -->
    <path id="{p}-browL" d="M-100 -78 C-80 -92 -48 -94 -26 -84" stroke="{HAIR}" stroke-width="15" fill="none" stroke-linecap="round" />
    <path id="{p}-browR" d="M26 -84 C48 -94 80 -92 100 -78" stroke="{HAIR}" stroke-width="15" fill="none" stroke-linecap="round" />
    <!-- nose -->
    <path d="M-4 18 C-8 40 -10 52 4 58 C14 62 24 56 22 50" stroke="#a96e4b" stroke-width="6" fill="none" stroke-linecap="round" />
    <!-- mouths -->
    <path id="{p}-mN" d="M-32 96 Q0 104 32 94" stroke="#6b3324" stroke-width="7" fill="none" stroke-linecap="round" />
    <g id="{p}-mO" opacity="0"><ellipse cx="0" cy="100" rx="17" ry="21" fill="#3d1512" /><ellipse cx="0" cy="112" rx="10" ry="6" fill="#b8574d" /></g>
    <path id="{p}-mT" d="M-26 98 Q0 88 26 98" stroke="#6b3324" stroke-width="7" fill="none" stroke-linecap="round" opacity="0" />
    <!-- hair -->
    <path d="M-172 -30 C-196 -170 -106 -258 8 -252 C126 -250 196 -170 172 -30 C162 -84 144 -116 114 -134 C104 -100 70 -92 40 -112 C22 -86 -24 -88 -46 -116 C-78 -92 -120 -100 -140 -124 C-152 -96 -162 -66 -172 -30 Z" fill="{HAIR}" />
    <path d="M-120 -196 C-80 -228 -10 -236 50 -220" stroke="#3b2c25" stroke-width="10" fill="none" stroke-linecap="round" />
    <path d="M30 -112 C40 -140 60 -160 84 -168" stroke="#3b2c25" stroke-width="7" fill="none" stroke-linecap="round" />
    <path id="{p}-sweat" d="M118 -96 C112 -80 108 -70 118 -64 C128 -70 124 -80 118 -96 Z" fill="#dff1ff" opacity="0" />
  </g>
</g>"""


def build() -> None:
    root = pathlib.Path(__file__).resolve().parent.parent / "compositions"
    for f in root.glob("*.html"):
        text = f.read_text()
        new = re.sub(r"%%CHAR:([a-z0-9]+)%%", lambda m: head(m.group(1)), text)
        if new != text:
            f.write_text(new)
            print("built", f.name)


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        build()
    else:
        print(head(sys.argv[1] if len(sys.argv) > 1 else "c"))
