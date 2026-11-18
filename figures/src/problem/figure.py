"""The two costs of uncoordinated libraries: drift and duplication."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from web import *  # noqa: E402,F403

W, H = 1000, 226

# Drift
stage(16, 16, 476, 196, "Drift", "same name, different meaning")
path("M134,102 H376", dash="5 3.5")
pill(255, 102, "different meaning")
for cx, name, gloss in ((108, "Library A", "multi-tape machines"), (402, "Library B", "unary input")):
    doc(cx, 100, ".lean", s=1.15)
    text(cx, 150, name, size=14)
    text(cx, 166, gloss, size=12, font=SANSR, fill="#3A3A3A")
    gate(cx, 190, "accepted by Lean", anchor="middle")

# Duplication
stage(508, 16, 476, 196, "Duplication", "one result, proved again")
for cx, name in ((600, "Library A"), (746, "Library B"), (892, "Library C")):
    doc(cx, 100, ".lean", s=1.15)
    text(cx, 150, name, size=14)
    text(cx, 166, "same lemma", size=12, font=SANSR, fill="#3A3A3A")
path("M580,182 V188 H912 V182", sw=1.2)
note(746, 200, "proved three times, usable in one library each")

write_svg("problem", W, H, "Drift: two libraries define polynomial time differently, with multi-tape machines and with unary input. Lean accepts both, but they have different meanings. Duplication: three libraries prove the same lemma separately, and each proof is usable only in its own library.")
