"""A visual language for paper figures, after the pipeline figures of
recent machine-learning papers drawn in PowerPoint: grey stage boxes,
agent units with dashed blue tiles, black line-art icons, and color kept for
meaning. A figure script draws with these helpers and calls write(); build.sh
turns the result into a PDF whose text is outlined (no fonts embedded).

Coordinates are SVG user units; a figure W = 1000 units wide placed at a
two-column \\textwidth (about 17.5 cm) makes 1 unit about 0.5 pt, so 12
units are about 6 pt, the smallest legible label.
"""

import os
from pathlib import Path

# Palette. Grey and pale blue carry the structure; color is reserved for
# meaning (green passes, red fails, gold for stores, HIGHLIGHT for new work).
INK = "#1A1A1A"
FRAME = "#B4B4B4"       # outer panel border
GROUP = "#EFEFEF"       # dashed stage boxes
UNIT = "#D9D9D9"        # agent unit (model + tools)
TILE = "#DDEBF7"        # dashed tiles inside a unit
HARNESS = "#F6CD4C"     # a trained or improved component
GOLDBRAIN = "#B8893A"   # a trained model
KHAKI = "#EFE7C2"       # background of graphs and trees
BEIGE = "#EFEBE0"       # secondary annotation boxes
THM = "#B0221B"         # first line of a document icon
PROOF = "#1F5FBF"       # second line of a document icon
OK = "#3DA35D"
OKDARK = "#24733F"
BAD = "#D64541"
ARROW = "#A6A6A6"       # block arrows
CYL = "#F6C343"
CYLTOP = "#F9D978"

SANS = "NarrowB"        # Nimbus Sans Narrow Bold, the figure's label face
SANSR = "Narrow"        # Nimbus Sans Narrow Regular
MONO = "MonoB"          # Nimbus Mono PS Bold, file tags and code marks

out = []


def add(s):
    out.append(s)


def text(x, y, s, size=13, font=SANS, anchor="middle", fill=INK, extra=""):
    add(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
        f'text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>')


def rect(x, y, w, h, rx=0, fill="none", stroke=INK, sw=1.4, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>')


def path(d, stroke=INK, sw=1.4, fill="none", dash=None, extra=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da} '
        f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def arrow(d, dash=None, sw=1.6, color=None):
    """An arrow; with `color` HIGHLIGHT it uses the highlight head."""
    tip = "tiphl" if color == HIGHLIGHT else "tip"
    path(d, stroke=color or INK, sw=sw, dash=dash, extra=f'marker-end="url(#{tip})"')


def block_arrow(x0, x1, y, h=22, head=16):
    """Thick grey arrow for the main flow between stages."""
    t = h * 0.42
    add(f'<polygon points="{x0},{y - t} {x1 - head},{y - t} {x1 - head},{y - h / 2 - 4} '
        f'{x1},{y} {x1 - head},{y + h / 2 + 4} {x1 - head},{y + t} {x0},{y + t}" '
        f'fill="{ARROW}"/>')


def note(x, y, s, size=12.5, anchor="middle", backing=True, width=None,
         fill=INK):
    """A label sitting on a line, on a white backing."""
    if backing:
        w = width if width else len(s) * size * 0.41 + 6
        x0 = x - w / 2 if anchor == "middle" else x - 4
        rect(x0, y - size * 0.8, w, size * 1.1, fill="#FFFFFF", stroke="none", sw=0)
    text(x, y, s, size=size, font=SANSR, anchor=anchor, fill=fill)


# ----------------------------------------------------------------- icons

def brain(cx, cy, s=1.0, color=INK):
    """A model: half brain, half circuit (box 60 x 50)."""
    add(f'<g transform="translate({cx - 30 * s},{cy - 25 * s}) scale({s})" '
        f'fill="none" stroke="{color}" stroke-width="{1.7 / s ** 0.3:.2f}" '
        f'stroke-linecap="round" stroke-linejoin="round">')
    add('<path d="M30,4 C24,2 17,4 15,9 C9,9 5,14 6,20 C2,23 1,30 4,34 '
        'C2,39 5,45 11,46 C13,50 20,51 24,48 C26,50 29,50 30,48 Z"/>')
    add('<path d="M15,9 C14,13 17,16 21,15 M6,20 C9,22 13,21 14,18 '
        'M4,34 C8,33 11,30 11,27 M11,46 C11,42 14,40 18,40 M30,22 C26,21 22,23 22,27 '
        'C22,30 25,32 29,31 M24,48 C23,45 25,42 29,42 M21,15 C23,10 27,10 30,11 '
        'M14,30 C17,30 19,33 18,36"/>')
    add('<path d="M30,9 H39 L43,5 M30,17 H49 M30,25 H37 L42,30 H50 '
        'M30,35 H45 M30,43 H38 L42,47"/>')
    for x, y in ((45.5, 3.5), (51.5, 17), (52.5, 30), (47.5, 35), (44, 48.5)):
        add(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#FFFFFF"/>')
    add('</g>')


def window(cx, cy, s=1.0, fill="#FFFFFF"):
    """Tools or a harness: a window with a title bar and a code mark (56 x 44)."""
    add(f'<g transform="translate({cx - 28 * s},{cy - 22 * s}) scale({s})">')
    rect(1, 1, 54, 42, rx=4, fill=fill, sw=1.8)
    path("M1,11 H55", sw=1.8)
    for x in (7, 12, 17):
        add(f'<circle cx="{x}" cy="6" r="1.6" fill="{INK}"/>')
    text(28, 34, "&lt;/&gt;", size=19, font=SANS)
    add('</g>')


def tile(x, y, w, h, label, icon):
    rect(x, y, w, h, rx=7, fill=TILE, stroke=INK, sw=1.2, dash="4 2.5")
    icon(x + w / 2, y + (h - 14) / 2 + 1)
    text(x + w / 2, y + h - 7, label, size=11.5)


def unit(x, y, w, h, name, tiles):
    """Agent unit: grey rounded box holding dashed tiles, its name underneath.
    `tiles` is a list of (label, icon), icon a function of the tile centre."""
    rect(x, y, w, h, rx=9, fill=UNIT, stroke=INK, sw=1.6)
    n = len(tiles)
    gap = 6
    tw = (w - 2 * gap - (n - 1) * gap) / n
    th = h - 2 * gap - 17
    for i, (label, icon) in enumerate(tiles):
        tile(x + gap + i * (tw + gap), y + gap, tw, th, label, icon)
    text(x + w / 2, y + h - 6, name, size=13.5)


def doc(cx, cy, tag, s=1.0, medal=False, proved=True):
    """Document: code mark, two colored lines, file tag (36 x 46). With
    `proved` False the second line reads sorry in grey; `medal` adds a ribbon
    for a verified or final output."""
    add(f'<g transform="translate({cx - 18 * s},{cy - 23 * s}) scale({s})">')
    path("M1,1 H26 L35,10 V45 H1 Z", fill="#FFFFFF", sw=1.6)
    path("M26,1 V10 H35", sw=1.3)
    rect(4, 4, 13, 8, rx=1, fill="#FFFFFF", sw=1.0)
    text(10.5, 10.6, "&lt;/&gt;", size=6.5, font=MONO)
    text(18, 22, "thm", size=9.5, font=MONO, fill=THM)
    path("M8,24.5 H28", stroke=THM, sw=1.1)
    color = PROOF if proved else "#8A8A8A"
    text(18, 33, "proof" if proved else "sorry", size=9.5, font=MONO, fill=color)
    path("M5,35.5 H31", stroke=color, sw=1.1)
    tw = len(tag) * 5.4 + 5
    rect(35 - tw + 4, 39, tw, 10, rx=2.5, fill=INK, stroke="none", sw=0)
    text(35 - tw / 2 + 4, 46.8, tag, size=8.5, font=MONO, fill="#FFFFFF")
    if medal:
        path("M28,-2 L25,8 L29,6 L31,10 L33,0 Z", fill="#C0392B", stroke="#7A1F17", sw=0.6)
        path("M34,-2 L37,8 L33,6 L31,10 L29,0 Z", fill="#C0392B", stroke="#7A1F17", sw=0.6)
        add('<circle cx="31" cy="-5" r="6" fill="#F2C230" stroke="#9C7413" stroke-width="0.9"/>')
        path("M31,-8.6 L32.1,-6.1 L34.6,-5.8 L32.7,-4.1 L33.2,-1.5 L31,-2.8 "
             "L28.8,-1.5 L29.3,-4.1 L27.4,-5.8 L29.9,-6.1 Z", fill="#FFF3B0", stroke="none", sw=0)
    add('</g>')


def lean_logo(x, y, s=1.0, sw=1.5):
    """The Lean logo, L, E reversed, A turned, N, in thin strokes (62 x 20)."""
    add(f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{INK}" '
        f'stroke-width="{sw}" stroke-linejoin="miter">')
    add('<path d="M1,0 V20 H12 M16,0 H28 V20 H16 M18,10 H28 M32,0 L38,20 L44,0 '
        'M34.4,8 H41.6 M48,20 V0 L60,20 V0"/>')
    add('</g>')


def badge(cx, cy, ok=True, r=8):
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{OK if ok else BAD}"/>')
    if ok:
        path(f"M{cx - r * .45},{cy + r * .02} L{cx - r * .1},{cy + r * .38} "
             f"L{cx + r * .5},{cy - r * .38}", stroke="#FFFFFF", sw=2.2)
    else:
        path(f"M{cx - r * .38},{cy - r * .38} L{cx + r * .38},{cy + r * .38} "
             f"M{cx - r * .38},{cy + r * .38} L{cx + r * .38},{cy - r * .38}",
             stroke="#FFFFFF", sw=2.2)


def gate(x, y, label, anchor="start"):
    """Green pill for a check that must pass before the flow continues."""
    w = len(label) * 6.1 + 22
    x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
    rect(x0, y - 9, w, 18, rx=9, fill=OK, stroke=OKDARK, sw=1.0)
    badge(x0 + 9, y, r=5.5)
    path(f"M{x0 + 6.6},{y} L{x0 + 8.4},{y + 2} L{x0 + 11.6},{y - 2}", stroke=OK, sw=1.6)
    text(x0 + 17, y + 4.3, label, size=11.5, anchor="start", fill="#FFFFFF")


def dag(x, y, s=1.0):
    """A small dependency graph or search tree on khaki: green done, red
    open, a gold star on the goal (box 48 x 48)."""
    add(f'<g transform="translate({x},{y}) scale({s})">')
    rect(0, 0, 48, 48, rx=2, fill=KHAKI, stroke="#9A9A9A", sw=1.0)
    for d in ("M12,10 L22,23", "M36,10 L26,23", "M36,10 L37,25", "M24,27 L24,36",
              "M37,29 L27,38"):
        path(d, sw=1.1)
    for cx, cy, r, c in ((12, 9, 4, OK), (36, 9, 4, OK), (24, 25, 4.2, OK),
                         (37, 27, 3, BAD)):
        add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="{INK}" '
            f'stroke-width="0.9"/>')
    add(f'<circle cx="24" cy="40" r="5.5" fill="{OK}" stroke="{INK}" stroke-width="0.9"/>')
    path("M27,36.3 L28,38.4 L30.3,38.7 L28.6,40.3 L29.1,42.6 L27,41.4 L24.9,42.6 "
         "L25.4,40.3 L23.7,38.7 L26,38.4 Z", fill="#F5C242", stroke="#9C7413", sw=0.6)
    add('</g>')


def library(cx, top, lines=("Verified", "Library")):
    """Gold cylinder with books and a bulb: a dataset or a store of results."""
    w, h, ry = 128, 60, 10
    x0 = cx - w / 2
    # books and bulb on the lid
    bx = cx - 30
    for i, (c, off, bw) in enumerate((("#2F8F9D", 0, 44), ("#E07A2E", 4, 40),
                                      ("#3F6FB0", -2, 46))):
        yb = top - 6 - (i + 1) * 7
        rect(bx + off, yb, bw, 7, rx=2, fill=c, stroke=INK, sw=1.0)
        path(f"M{bx + off + bw - 6},{yb + 1.5} V{yb + 5.5}", stroke="#FFFFFF", sw=0.9)
    bulb_x, bulb_y = cx + 26, top - 26
    add(f'<circle cx="{bulb_x}" cy="{bulb_y}" r="7.5" fill="#FFE27A" stroke="{INK}" '
        f'stroke-width="1.1"/>')
    rect(bulb_x - 3.5, bulb_y + 7, 7, 6, rx=1, fill="#9A9A9A", stroke=INK, sw=0.9)
    for dx, dy, ex, ey in ((0, -11, 0, -15), (-9, -6, -12, -9), (9, -6, 12, -9),
                           (-10, 1, -14, 1), (10, 1, 14, 1)):
        path(f"M{bulb_x + dx},{bulb_y + dy} L{bulb_x + ex},{bulb_y + ey}", sw=1.1)
    # cylinder
    path(f"M{x0},{top} V{top + h} A{w / 2},{ry} 0 0 0 {x0 + w},{top + h} V{top}",
         fill=CYL, sw=1.6)
    add(f'<ellipse cx="{cx}" cy="{top}" rx="{w / 2}" ry="{ry}" fill="{CYLTOP}" '
        f'stroke="{INK}" stroke-width="1.6"/>')
    for i, line in enumerate(lines):
        text(cx, top + 28 + 18 * i, line, size=16)


ACCENT = "#2F6DB5"     # a second marker color, e.g. steps of one mode
HIGHLIGHT = "#E0861C"  # the one highlight: elements added in this work


def step(x, y, w, h, title, sub, accent=None):
    """White step box with a bold title and a grey gloss; `accent` draws a
    colored stripe on the left (a step of one mode, or new work)."""
    rect(x, y, w, h, rx=6, fill="#FFFFFF", stroke="#7A7A7A", sw=1.1)
    if accent:
        path(f"M{x + 2.5},{y + 5} V{y + h - 5}", stroke=accent, sw=4.5)
    text(x + 8, y + 16, title, size=13.5, anchor="start")
    text(x + 8, y + 31, sub, size=12, font=SANSR, anchor="start", fill="#3A3A3A")


def stage(x, y, w, h, key, title, indent=9):
    """Dashed grey stage box headed "Key (title)": key bold, title regular."""
    rect(x, y, w, h, fill=GROUP, stroke=INK, sw=1.2, dash="5 3")
    add(f'<text x="{x + indent}" y="{y + 21}" font-size="17.5" fill="{INK}" text-anchor="start">'
        f'<tspan font-family="{SANS}">{key}</tspan>'
        f'<tspan font-family="{SANSR}"> ({title})</tspan></text>')



def circle(cx, cy, r, fill="#FFFFFF", stroke=INK, sw=1.2):
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{sw}"/>')


def pill(cx, cy, label, fill=BAD, stroke="#9E2E2B"):
    """A colored outcome pill, e.g. a red "disproved" beside a green gate."""
    w = len(label) * 6.4 + 16
    rect(cx - w / 2, cy - 9, w, 18, rx=9, fill=fill, stroke=stroke, sw=1.0)
    text(cx, cy + 4.3, label, size=11.5, fill="#FFFFFF")


def stack(cx, cy, tag, s=0.9):
    """Several documents: two blank pages behind a document icon."""
    for d in (8, 4):
        path(f"M{cx - 16 * s + d},{cy - 22 * s - d} h{23 * s} l{9 * s},{9 * s} "
             f"v{35 * s} h{-32 * s} Z", fill="#FFFFFF", sw=1.2)
    doc(cx, cy, tag, s=s)


def cylinder(cx, cy, w, h, fill=CYL, top=CYLTOP):
    ry = w * 0.16
    path(f"M{cx - w / 2},{cy - h / 2} V{cy + h / 2} A{w / 2},{ry} 0 0 0 "
         f"{cx + w / 2},{cy + h / 2} V{cy - h / 2}", fill=fill, sw=1.4)
    add(f'<ellipse cx="{cx}" cy="{cy - h / 2}" rx="{w / 2}" ry="{ry}" fill="{top}" '
        f'stroke="{INK}" stroke-width="1.4"/>')


def database(cx, cy):
    """An index or database: a pale blue cylinder with bands."""
    cylinder(cx, cy, 34, 34, TILE, "#EEF4FB")
    for dy in (-4, 7):
        path(f"M{cx - 17},{cy + dy} A17,5.4 0 0 0 {cx + 17},{cy + dy}", sw=1.1)


def padlock(cx, cy):
    """A sandbox or other confinement, beside a stage heading."""
    path(f"M{cx - 5},{cy - 3} V{cy - 7} A5,5 0 0 1 {cx + 5},{cy - 7} V{cy - 3}",
         sw=1.8)
    rect(cx - 8, cy - 3, 16, 13, rx=2, fill=CYL, stroke=INK, sw=1.4)


def sub(s):
    """Subscript inside a text label, e.g. "t" + sub(1)."""
    return f'<tspan baseline-shift="sub" font-size="75%">{s}</tspan>'


# The URW base-35 fonts (Helvetica, Times, and Courier clones) of Ghostscript.
FONTS = os.environ.get("FIGURE_FONTS", "/usr/share/fonts/opentype/urw-base35")


def write(script, w, h):
    """Write figure.html next to the figure script; build.sh prints it."""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">'
           '<defs><marker id="tip" viewBox="0 0 10 10" refX="8.5" refY="5" '
           'markerWidth="5.2" markerHeight="5.2" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 Z" fill="{INK}"/></marker>'
           '<marker id="tiphl" viewBox="0 0 10 10" refX="8.5" refY="5" '
           'markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 Z" fill="{HIGHLIGHT}"/></marker></defs>'
           + "\n".join(out) + "</svg>")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{font-family:{SANS}; src:url(file://{FONTS}/NimbusSansNarrow-Bold.otf)}}
@font-face {{font-family:{SANSR}; src:url(file://{FONTS}/NimbusSansNarrow-Regular.otf)}}
@font-face {{font-family:{MONO}; src:url(file://{FONTS}/NimbusMonoPS-Bold.otf)}}
@page {{size:{w}px {h}px; margin:0}}
html, body {{margin:0; padding:0}} svg {{display:block}}
</style></head><body>{svg}</body></html>"""
    Path(script).with_name("figure.html").write_text(html)
