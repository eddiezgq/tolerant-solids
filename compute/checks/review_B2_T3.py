"""Review: per-edge min of the T measure and where along the edge it occurs (sample index of N=200)."""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R
from review_B2_T2 import rebuild
name = sys.argv[1] if len(sys.argv) > 1 else "sloppy wedge 30deg g=0.01"
M, N = rebuild(R.PARTS[name]())
for i in range(len(N.E)):
    sd = L.edge_samples(N, i)["sides"]
    if len(sd) != 2 or sd[0]["face"] == sd[1]["face"]: continue
    T = np.array([180 - math.degrees(math.acos(np.clip(a @ b, -1, 1))) for a, b in zip(sd[0]["u"], sd[1]["u"])])
    j = int(np.argmin(T)); print(i, "min T %.1f at sample %d; median %.1f; #samples with T<60: %d" % (T[j], j, np.median(T), (T < 60).sum()))
