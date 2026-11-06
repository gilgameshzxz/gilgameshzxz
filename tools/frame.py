"""Render one frame of an animated SVG at time t (seconds): frame.py <svg> <t> <out.png>"""
import os
import subprocess
import sys
import tempfile

svg_path, t, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
svg = open(svg_path, encoding="utf-8").read()
html = f"""<html><body style="margin:0;background:#fff">{svg}<script>
const s = document.querySelector('svg');
s.pauseAnimations(); s.setCurrentTime({t});
document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {t * 1000}; }});
</script></body></html>"""
fd, tmp = tempfile.mkstemp(suffix=".html", dir=os.path.dirname(out))
with os.fdopen(fd, "w", encoding="utf-8") as f:
    f.write(html)
w, h = svg.split('width="')[1].split('"')[0], svg.split('height="')[1].split('"')[0]
subprocess.run([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new", "--disable-gpu",
                "--hide-scrollbars", f"--window-size={w},{h}", "--virtual-time-budget=500",
                f"--screenshot={out}", "file:///" + tmp.replace("\\", "/")], capture_output=True)
os.remove(tmp)
print("frame", out)
