"""Generate assets/glitch.svg: a corrupted-signal divider reused between README sections."""
import random
import sys
from html import escape

OUT = sys.argv[1]
W, H = 1000, 64
FONT = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
random.seed(7)  # seven, obviously

MSGS = [
    "TRANSMISSION FROM GATE VII",
    "D3F1N1T10N N0T F0UND",
    "you were not supposed to scroll here",
    "███ REDACTED BY THE GUARD ███",
    "the README is reading you back",
    "signal: ??? · source: before time",
    "do not count the gates",
]
STEP = 2.6
T = STEP * len(MSGS)
pct = lambda s: f"{s / T * 100:.3f}%"

css, msgs = [], []
for i, m in enumerate(MSGS):
    a, b = i * STEP, (i + 1) * STEP
    css.append(
        f"@keyframes m{i}{{0%,{pct(a)}{{opacity:0}}{pct(a + .05)},{pct(b - .05)}{{opacity:1}}{pct(b)},100%{{opacity:0}}}}"
        f".m{i}{{opacity:0;animation:m{i} {T:.1f}s infinite steps(1)}}"
    )
    t = escape(m, quote=False)
    attrs = f'x="{W // 2}" y="{H // 2}" text-anchor="middle" dominant-baseline="central"'
    msgs.append(
        f'<g class="m{i}">'
        f'<text {attrs} class="msg rr">{t}</text>'
        f'<text {attrs} class="msg cc">{t}</text>'
        f'<text {attrs} class="msg ww">{t}</text></g>'
    )

# blocks of corruption that flash at pseudo-random moments
blocks = []
for _ in range(26):
    x, y = random.randint(0, W - 120), random.randint(4, H - 12)
    w, h = random.randint(20, 160), random.choice([2, 3, 4, 6, 9])
    col = random.choice(["#ff3b6b", "#22d3ee", "#f0f6fc", "#0d1117", "#a371f7", "#e3b341"])
    dur = random.choice([1.7, 2.3, 3.1, 3.7, 4.3])
    on = random.uniform(.05, .9)
    blocks.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" opacity="0">'
        f'<animate attributeName="opacity" values="0;.85;0" keyTimes="0;{on:.2f};1" calcMode="discrete" '
        f'dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="x" values="{x};{x + random.randint(-80, 80)};{x}" calcMode="discrete" '
        f'dur="{dur * 1.3:.1f}s" repeatCount="indefinite"/></rect>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="8"/></clipPath>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".35"/></pattern>
    <linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f0f6fc" stop-opacity="0"/><stop offset=".5" stop-color="#f0f6fc" stop-opacity=".12"/><stop offset="1" stop-color="#f0f6fc" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    text {{ font-family: {FONT}; }}
    .msg {{ font-size: 17px; font-weight: 700; letter-spacing: 3px; }}
    .ww {{ fill: #f0f6fc; animation: jw 2.2s infinite steps(1); }}
    .rr {{ fill: #ff3b6b; opacity: .8; animation: jr 2.2s infinite steps(1); }}
    .cc {{ fill: #22d3ee; opacity: .8; animation: jc 2.2s infinite steps(1); }}
    @keyframes jw {{ 0%,60%,100% {{ transform: translate(0,0) }} 62% {{ transform: translate(-4px,1px) skewX(-15deg) }} 66% {{ transform: translate(5px,0) }} 70% {{ transform: translate(0,-1px) }} }}
    @keyframes jr {{ 0%,100% {{ transform: translate(-2px,0) }} 62% {{ transform: translate(-9px,2px) }} 66% {{ transform: translate(6px,-1px) }} 70% {{ transform: translate(-2px,0) }} }}
    @keyframes jc {{ 0%,100% {{ transform: translate(2px,0) }} 62% {{ transform: translate(9px,-2px) }} 66% {{ transform: translate(-6px,1px) }} 70% {{ transform: translate(2px,0) }} }}
    .sweep {{ animation: sw 3.3s linear infinite; }}
    @keyframes sw {{ from {{ transform: translateY(-{H}px) }} to {{ transform: translateY({H}px) }} }}
    .flick {{ animation: fk 4.1s infinite steps(1); }}
    @keyframes fk {{ 0%,100% {{ opacity: 1 }} 41% {{ opacity: .35 }} 43% {{ opacity: 1 }} 77% {{ opacity: .6 }} 78% {{ opacity: 1 }} }}
    .side {{ font-size: 10px; fill: #6e7681; letter-spacing: 1px; }}
    {"".join(css)}
  </style>
  <g clip-path="url(#card)" class="flick">
    <rect width="{W}" height="{H}" fill="#0d1117"/>
    <line x1="0" y1="{H // 2}" x2="{W}" y2="{H // 2}" stroke="#21262d"/>
    <text x="14" y="{H // 2 + 4}" class="side">CH-07 ▓▒░</text>
    <text x="{W - 14}" y="{H // 2 + 4}" text-anchor="end" class="side">░▒▓ NO SIGNAL</text>
    {"".join(msgs)}
    {"".join(blocks)}
    <rect width="{W}" height="{H}" fill="url(#scan)"/>
    <rect width="{W}" height="{H}" fill="url(#sweep)" class="sweep"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="none" stroke="#30363d"/>
</svg>
'''
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, f"cycle={T:.1f}s")
