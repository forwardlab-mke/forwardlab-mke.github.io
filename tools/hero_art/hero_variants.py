"""Five hero-art options (800x600 SVG) built on an MRI-derived brain.

Brain outline, sulci, and depth isolines come from the MNI152 template
(see mri_brain.py and brain_svg.py -> brain_paths.json). Deterministic.
"""
import json
import random
from pathlib import Path

B = json.load(open(Path(__file__).with_name("brain_paths.json")))
OUT = Path(__file__).resolve().parents[2] / "assets" / "img"

BLUE, BLUE_DK, BLUE_DKR = "#0074c8", "#005a9c", "#004f8a"
GREEN, LIGHT, PALE, SOFT = "#007065", "#7eb8e0", "#c1ddf4", "#e8f2fb"
W, H = B["width"], B["height"]
OUTLINE, SULCI, ISO = B["outline"], B["sulci"], B["iso"]
MASK, (MX, MY), S = B["mask"], B["mask_origin"], B["S"]

# True when a logo is layered over the lower part of the art (darkens the bottom band and
# shifts the drawing up to make room). The ForWARD site has no overlay yet, so art is centered.
LOGO_OVERLAY = False
BASE = '<rect width="800" height="600" fill="url(#base)"/>' if LOGO_OVERLAY else ""

SOURCE = "Brain outline and sulci derived from the MNI152 T1 template (lateral view, left hemisphere)."


def inside(px, py):
    """Point in brain (local, unscaled-by-k px)?"""
    c, r = int(px / S + MX), int(py / S + MY)
    return 0 <= r < len(MASK) and 0 <= c < len(MASK[0]) and MASK[r][c] == 1


def svg(body, defs="", note=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
  <!-- {note}
       {SOURCE} -->
  <defs>
    <clipPath id="brainClip"><path d="{OUTLINE}"/></clipPath>
    <linearGradient id="base" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0.5" stop-color="{BLUE_DK}" stop-opacity="0"/>
      <stop offset="0.82" stop-color="{BLUE_DK}" stop-opacity="0.72"/>
      <stop offset="1" stop-color="{BLUE_DKR}" stop-opacity="0.95"/>
    </linearGradient>
{defs}
  </defs>
{body}
</svg>
"""


def at(k, cx, top):
    """Place the brain scaled by k, centered on cx, top edge at `top`."""
    return f'transform="translate({cx - W * k / 2:.1f} {top:.1f}) scale({k})"'


def sulci_fill(color, opacity):
    return f'<g fill="{color}" opacity="{opacity}">' + "".join(f'<path d="{d}"/>' for d in SULCI) + "</g>"


# ---------------------------------------------------------------------------
def v1():
    """Trajectories inside: the logo's fan lines flow through the brain."""
    k = 0.72
    lines = []
    for i in range(22):
        t = i / 21
        end_y = -40 + t * (H + 60)
        col = PALE if i % 2 else LIGHT
        op = 0.3 + 0.55 * (1 - abs(t - 0.45) * 1.6)
        lines.append(f'<path d="M-40 {H * 0.86:.0f} C{W * 0.3:.0f} {H * 0.84:.0f} {W * 0.52:.0f} {end_y + 90:.0f} {W + 40:.0f} {end_y:.0f}" '
                     f'stroke="{col}" opacity="{max(op, 0.2):.2f}"/>')
    body = f"""  <rect width="800" height="600" fill="{BLUE}"/>
  <g {at(k, 400, 34 if LOGO_OVERLAY else (600 - H * k) / 2)}>
    <path d="{OUTLINE}" fill="#0b7cc9"/>
    <g clip-path="url(#brainClip)" fill="none" stroke-width="{3.4 / k:.1f}" stroke-linecap="round">
      {"".join(lines)}
    </g>
    {sulci_fill(BLUE_DK, 0.35)}
    <path d="{OUTLINE}" fill="none" stroke="#fff" stroke-width="{4 / k:.1f}" stroke-linejoin="round"/>
  </g>
  {BASE}"""
    return svg(body, note="Option 1, Trajectories inside: the logo's fan lines flow through the brain.")


def v2():
    """Connectome: nodes and links inside the brain; hubs are logo-style dots."""
    k = 0.72
    rnd = random.Random(11)
    pts = []
    while len(pts) < 58:
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        if inside(x, y) and all((x - a) ** 2 + (y - b) ** 2 > 52 ** 2 for a, b in pts):
            pts.append((x, y))
    edges = set()
    for i, (x, y) in enumerate(pts):
        for j in sorted(range(len(pts)), key=lambda j: (pts[j][0] - x) ** 2 + (pts[j][1] - y) ** 2)[1:4]:
            edges.add(tuple(sorted((i, j))))
    hubs = set(rnd.sample(range(len(pts)), 8))
    e = "".join(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}"/>' for i, j in sorted(edges))
    n = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{12 / k:.1f}" fill="{GREEN}" stroke="#fff" stroke-width="{4.5 / k:.1f}"/>' if i in hubs
        else f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{5 / k:.1f}" fill="#fff" opacity="0.92"/>'
        for i, (x, y) in enumerate(pts))
    body = f"""  <rect width="800" height="600" fill="url(#glow2)"/>
  <g {at(k, 400, 34)}>
    <path d="{OUTLINE}" fill="{BLUE}" fill-opacity="0.35" stroke="{LIGHT}" stroke-width="{2.6 / k:.1f}" stroke-dasharray="{2 / k:.1f} {9 / k:.1f}" stroke-linecap="round"/>
    {sulci_fill(LIGHT, 0.12)}
    <g stroke="{PALE}" stroke-width="{1.8 / k:.1f}" opacity="0.55">{e}</g>
    {n}
  </g>
  {BASE}"""
    defs = f"""    <radialGradient id="glow2" cx="0.5" cy="0.36" r="0.65">
      <stop offset="0" stop-color="{BLUE}"/>
      <stop offset="1" stop-color="{BLUE_DKR}"/>
    </radialGradient>"""
    return svg(body, defs, note="Option 2, Connectome: nodes and links inside the brain; hubs use the logo's white-ringed green dots.")


def v3():
    """Clean line art on light; standard logo on a blue band."""
    k = 0.6
    traj = "M-10 300 C120 296 190 272 260 248 S400 186 470 158 S560 112 630 84"
    body = f"""  <rect width="800" height="600" fill="{SOFT}"/>
  <g {at(k, 400, 20)}>
    <path d="{OUTLINE}" fill="#fff" stroke="{BLUE}" stroke-width="{4.5 / k:.1f}" stroke-linejoin="round"/>
    {sulci_fill(BLUE, 0.85)}
  </g>
  <g transform="translate(90 40)">
    <path d="{traj}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/>
    <path d="{traj}" fill="none" stroke="{GREEN}" stroke-width="8" stroke-linecap="round"/>
    <g fill="{GREEN}" stroke="#fff" stroke-width="4.5"><circle cx="-10" cy="300" r="12"/><circle cx="260" cy="248" r="12"/><circle cx="470" cy="158" r="12"/><circle cx="630" cy="84" r="13"/></g>
  </g>
  <rect y="384" width="800" height="216" fill="{BLUE}"/>"""
    return svg(body, note="Option 3, Clean line art on light: blue MRI-derived brain with the green trajectory; standard logo on a blue band.")


def v4():
    """Lifespan: child, teen, adult brains growing along the trajectory."""
    traj = "M30 400 C110 398 150 392 200 378 S320 330 390 298 S560 206 760 118"
    brains = []
    for k, cx, top in [(0.17, 200, 290), (0.26, 392, 196), (0.4, 610, 58)]:
        brains.append(f"""  <g {at(k, cx, top)}>
    <path d="{OUTLINE}" fill="#0b7cc9" stroke="{PALE}" stroke-width="{3 / k:.1f}"/>
    {sulci_fill(PALE, 0.75)}
  </g>""")
    dy = 0 if LOGO_OVERLAY else 65  # content spans y 58-411; center it when nothing sits below
    body = f"""  <rect width="800" height="600" fill="{BLUE}"/>
  <g transform="translate(0 {dy})">
  <path d="{traj}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/>
  <path d="{traj}" fill="none" stroke="{GREEN}" stroke-width="8" stroke-linecap="round"/>
{chr(10).join(brains)}
  <g fill="{GREEN}" stroke="#fff" stroke-width="4.5"><circle cx="30" cy="400" r="11"/><circle cx="200" cy="378" r="12"/><circle cx="390" cy="298" r="13"/><circle cx="760" cy="118" r="14"/></g>
  </g>
  {BASE}"""
    return svg(body, note="Option 4, Lifespan: child, teen, and adult brains growing along the trajectory line.")


def v5():
    """Depth map: MRI depth isolines, warming from pale blue to green."""
    k = 0.72
    cols = [PALE, "#a3cbed", LIGHT, "#3f9bc0", "#2b9f8f"]
    rings = "".join(f'<path d="{d}" stroke="{cols[int(lv)]}"/>' for lv, ds in ISO.items() for d in ds)
    body = f"""  <rect width="800" height="600" fill="{BLUE_DKR}"/>
  <rect width="800" height="600" fill="url(#glow2)"/>
  <g {at(k, 400, 34)}>
    <path d="{OUTLINE}" fill="{BLUE}" fill-opacity="0.45"/>
    {sulci_fill(GREEN, 0.55)}
    <g fill="none" stroke-width="{2.4 / k:.1f}" opacity="0.9">{rings}</g>
    <path d="{OUTLINE}" fill="none" stroke="#fff" stroke-width="{3.5 / k:.1f}"/>
  </g>
  {BASE}"""
    defs = f"""    <radialGradient id="glow2" cx="0.5" cy="0.36" r="0.65">
      <stop offset="0" stop-color="{BLUE}"/>
      <stop offset="1" stop-color="{BLUE_DKR}"/>
    </radialGradient>"""
    return svg(body, defs, note="Option 5, Depth map: cortical depth isolines like an MRI map, sulci in green.")


# The home page rotates options 1 and 4. Options 2, 3 and 5 stay here in case you want them.
ROTATION = [("hero-brain-1.svg", v1), ("hero-brain-2.svg", v4)]

if __name__ == "__main__":
    for name, fn in ROTATION:
        (OUT / name).write_text(fn())
        print(name, round((OUT / name).stat().st_size / 1024), "KB")
