"""Stages of a canonicity check."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from web import *  # noqa: E402,F403

W, H = 1000, 200

doc(52, 100, ".lean", s=1.1)
text(52, 146, "definition", size=12.5, font=SANSR)
block_arrow(82, 128, 100)
step(132, 78, 176, 44, "1. Locate", "pair with its reference")
block_arrow(312, 358, 100)
step(362, 78, 196, 44, "2. Refute", "SAT/SMT on small instances")

# counterexample branch
arrow("M558,90 C584,90 584,48 606,48")
badge(620, 48, ok=False, r=11)
text(642, 45, "Counterexample", size=14, anchor="start")
text(642, 61, "divergence report to maintainers", size=12, font=SANSR, anchor="start", fill="#3A3A3A")

# no counterexample branch
arrow("M558,110 C584,110 584,152 606,152")
badge(620, 152, ok=True, r=11)
arrow("M634,152 H666")
step(670, 130, 150, 44, "3. Confirm", "prove in Lean")
arrow("M820,152 H860")
doc(890, 150, ".lean", s=1.1, medal=True)
text(918, 148, "Bridge", size=14, anchor="start")
text(918, 164, "lemma", size=14, anchor="start")

write_svg("canonicity", W, H, "A definition is located against its reference, then tested on small instances with a SAT/SMT solver. A counterexample produces a divergence report. Otherwise the equivalence is proved in Lean, producing a bridge lemma.")
