"""Web output for figstyle figures: writes a standalone, responsive SVG that
uses the site's fonts instead of building a font-free PDF.

Usage in a figure script:
    from web import *            # figstyle primitives plus write_svg
    ... draw ...
    write_svg("overview", W, H, "Accessible description of the figure")
The SVG lands in static/fig-<name>.svg and is inlined into the pages by the
site build.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figstyle  # noqa: E402
from figstyle import *  # noqa: E402,F401,F403

# On the website, the one highlight is the site's accent (teal), not orange.
figstyle.HIGHLIGHT = "#0F6E63"
HIGHLIGHT = figstyle.HIGHLIGHT

ROOT = Path(__file__).resolve().parents[2]
FONT_MAP = {
    'font-family="NarrowB"': 'font-family="\'Source Sans 3\', \'Helvetica Neue\', Arial, sans-serif" font-weight="600"',
    'font-family="Narrow"': 'font-family="\'Source Sans 3\', \'Helvetica Neue\', Arial, sans-serif" font-weight="400"',
    'font-family="MonoB"': 'font-family="\'Source Code Pro\', Menlo, monospace" font-weight="600"',
}


def write_svg(name, w, h, desc):
    body = "\n".join(figstyle.out)
    for a, b in FONT_MAP.items():
        body = body.replace(a, b)
    body = body.replace('url(#tip)', f'url(#{name}-tip)').replace('url(#tiphl)', f'url(#{name}-tiphl)')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="{desc}" class="fig-svg">'
           f'<defs><marker id="{name}-tip" viewBox="0 0 10 10" refX="8.5" refY="5" '
           'markerWidth="5.2" markerHeight="5.2" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 Z" fill="{figstyle.INK}"/></marker>'
           f'<marker id="{name}-tiphl" viewBox="0 0 10 10" refX="8.5" refY="5" '
           'markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 Z" fill="{HIGHLIGHT}"/></marker></defs>\n'
           f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>\n{body}\n</svg>\n')
    dest = ROOT / "static" / f"fig-{name}.svg"
    dest.write_text(svg)
    print("wrote", dest.relative_to(ROOT))
