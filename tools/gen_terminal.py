"""Generate assets/terminal.svg: a looping fake shell session."""
import sys
from html import escape

OUT = sys.argv[1]

LINES = [
    ("cmd", "define reality"),
    ("out", "ERROR: definition not found. did you mean: ???", "#ff7b72"),
    ("cmd", "npm install meaning"),
    ("out", "npm ERR! 404  'meaning' is not in the registry.", "#ff7b72"),
    ("out", "npm WARN  try instead: npm install vibes --save-dev", "#e3b341"),
    ("cmd", "git blame universe"),
    ("out", "fatal: no author. 13.8 billion years of commits, 0 commit messages.", "#ff7b72"),
    ("cmd", "sudo make gilgamesh --immortal"),
    ("out", "[sudo] password for gilgamesh: ************", "#8b949e"),
    ("out", "gilgamesh is not in the sudoers file. This incident will be reported to Enkidu.", "#e3b341"),
    ("cmd", "ls -la /gates"),
    ("out", "drwxr-xr-x  gate_1 .. gate_6     7 toll(s)     modified: 2100 BC", "#8b949e"),
    ("out", "d?????????  gate_7               ??? bytes     modified: before time", "#d2a8ff"),
    ("cmd", "cd /gates/gate_7"),
    ("out", "bash: cd: gate_7: you are already inside it", "#e3b341"),
    ("cmd", "ping meaning"),
    ("out", "Request timed out. Request timed out. The timeout became the answer.", "#8b949e"),
    ("cmd", "rm -rf ./definitions"),
    ("out", "✓ removed everything. the experiment completed successfully. exit code 0", "#3fb950"),
    ("cmd", ""),
]

W, CH, LH, X0, Y0 = 1000, 9.0, 21, 24, 66
PROMPT = "morcelagox@reality:~$"
CMD_X = X0 + (len(PROMPT) + 1) * CH

# timeline
t, times = 0.6, []
for ln in LINES:
    if ln[0] == "cmd":
        typing = max(len(ln[1]) * 0.06, 0.01)
        times.append((t, t + typing))
        t += typing + 0.45
    else:
        times.append((t, t))
        t += 0.35
T = t + 4.0  # hold the full screen
H = Y0 + LH * len(LINES) + 10

pct = lambda s: f"{s / T * 100:.3f}%"
css, body = [], []
for i, (ln, (a, b)) in enumerate(zip(LINES, times)):
    y = Y0 + i * LH
    last = i == len(LINES) - 1
    css.append(
        f"@keyframes s{i}{{0%,{pct(a)}{{opacity:0}}{pct(a + 0.01)},96%{{opacity:1}}98%,100%{{opacity:0}}}}"
        f".s{i}{{opacity:0;animation:s{i} {T:.2f}s infinite}}"
    )
    if ln[0] == "cmd":
        n = len(ln[1])
        w = n * CH
        css.append(
            f"@keyframes t{i}{{0%,{pct(a)}{{transform:translateX(0);animation-timing-function:steps({max(n,1)},end)}}"
            f"{pct(b)},100%{{transform:translateX({w:.1f}px)}}}}"
            f".t{i}{{animation:t{i} {T:.2f}s infinite}}"
        )
        if not last:
            css.append(
                f"@keyframes k{i}{{0%,{pct(b + 0.3)}{{opacity:1}}{pct(b + 0.31)},100%{{opacity:0}}}}"
                f".k{i}{{animation:k{i} {T:.2f}s infinite}}"
            )
        cmd = ""
        if n:
            cmd = (f'<text x="{CMD_X}" y="{y}" class="cmd" textLength="{w:.1f}" '
                   f'lengthAdjust="spacingAndGlyphs">{escape(ln[1], quote=False)}</text>')
        cursor_cls = "blink" if last else f"k{i}"
        body.append(
            f'<g class="s{i}">'
            f'<text x="{X0}" y="{y}" textLength="{len(PROMPT) * CH:.1f}" lengthAdjust="spacingAndGlyphs">'
            f'<tspan fill="#3fb950">morcelagox@reality</tspan><tspan fill="#8b949e">:</tspan>'
            f'<tspan fill="#58a6ff">~</tspan><tspan fill="#8b949e">$</tspan></text>'
            f'{cmd}'
            f'<g class="t{i}"><rect x="{CMD_X}" y="{y - 15}" width="{W}" height="{LH}" fill="#0d1117"/>'
            f'<rect x="{CMD_X}" y="{y - 14}" width="9" height="18" fill="#f0f6fc" class="{cursor_cls}"/></g>'
            f'</g>'
        )
    else:
        body.append(f'<text x="{X0}" y="{y}" fill="{ln[2]}" class="s{i}">{escape(ln[1], quote=False)}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="12"/></clipPath>
    <clipPath id="screen"><rect x="12" y="40" width="{W - 24}" height="{H - 44}"/></clipPath>
  </defs>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size: 15px; white-space: pre; }}
    .cmd {{ fill: #f0f6fc; }}
    .bar {{ font-size: 13px; fill: #8b949e; }}
    .blink {{ animation: bl 1s infinite steps(1); }}
    @keyframes bl {{ 50% {{ opacity: 0 }} }}
    {"".join(css)}
  </style>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="#0d1117"/>
    <rect width="{W}" height="34" fill="#161b22"/>
    <circle cx="22" cy="17" r="6" fill="#ff5f57"/>
    <circle cx="42" cy="17" r="6" fill="#febc2e"/>
    <circle cx="62" cy="17" r="6" fill="#28c840"/>
    <text x="{W // 2}" y="22" text-anchor="middle" class="bar">morcelagox@reality: ~ — bash — 80x∞</text>
    <g clip-path="url(#screen)">
      {"".join(body)}
    </g>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="#30363d"/>
</svg>
'''
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT}  cycle={T:.1f}s height={H}")
