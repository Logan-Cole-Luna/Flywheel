"""How Flywheel works: libraries feed a shared index, five tools act on it,
results go back to each library, and findings return to the index."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from web import *  # noqa: E402,F403

W, H = 1000, 372

# Libraries
stage(16, 30, 180, 290, "Libraries", "in Lean")
for i, (cy, name) in enumerate(((112, "Library A"), (186, "Library B"), (260, "Library C"))):
    cylinder(58, cy, 40, 30)
    text(90, cy - 2, name, size=14, anchor="start")
    text(90, cy + 15, "own repository", size=12, font=SANSR, anchor="start", fill="#3A3A3A")
block_arrow(200, 284, 176)
text(242, 158, "declarations", size=12.5, font=SANSR)

# Flywheel: index, bus, five tools, references
stage(290, 30, 430, 290, "Flywheel", "shared tools")
text(338, 140, "shared index", size=12.5, font=SANSR)
database(338, 176)
path("M355,176 H380")
path("M380,97 V273")
steps = [("1. Semantic search", "find matches across libraries"),
         ("2. Canonicity checking", "compare with references"),
         ("3. Harmonization", "prove bridge lemmas"),
         ("4. Proof quality", "score robustness and reuse"),
         ("5. Faithfulness", "check translations into Lean")]
for i, (t, s) in enumerate(steps):
    y = 78 + i * 44
    path(f"M380,{y + 19} H394")
    step(396, y, 200, 38, t, s)
stack(672, 141, ".lean", s=0.8)
text(672, 96, "reference", size=12.5, font=SANSR)
text(672, 110, "definitions", size=12.5, font=SANSR)
arrow("M650,141 H600")
gate(604, 185, "checked in Lean")

# Results
block_arrow(724, 776, 176)
text(750, 158, "results", size=12.5, font=SANSR)
stage(780, 30, 204, 290, "Results", "per library")
doc(816, 104, ".lean", s=1.0, medal=True)
text(844, 102, "Bridge lemma", size=14, anchor="start")
text(844, 118, "pull request", size=12, font=SANSR, anchor="start", fill="#3A3A3A")
badge(816, 190, ok=False, r=11)
text(844, 188, "Divergence", size=14, anchor="start")
text(844, 204, "report to maintainers", size=12, font=SANSR, anchor="start", fill="#3A3A3A")
badge(816, 262, ok=True, r=11)
text(844, 260, "No change", size=14, anchor="start")
text(844, 276, "already canonical", size=12, font=SANSR, anchor="start", fill="#3A3A3A")

# Feedback into the index
arrow("M882,320 V350 H338 V196", dash="5 3.5")
note(610, 354, "findings return to the index as training data")

write_svg("overview", W, H, "Libraries send declarations to a shared index. Five Flywheel tools act on it: semantic search, canonicity checking against reference definitions, harmonization, proof quality, and faithfulness checking, with results checked in Lean. Each library receives a bridge lemma as a pull request, a divergence report, or no change, and findings return to the index as training data.")
