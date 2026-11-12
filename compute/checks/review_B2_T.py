"""Review: what does the T measure of reintersect_curved see? Print inward tangents u_f, u_g per edge."""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R
for name in sys.argv[1:] or ["wedge 10deg"]:
    s = R.PARTS[name]() if name in R.PARTS else R.wedge(float(name))
    M = L.Model(s)
    print("==", name)
    for i in range(len(M.E)):
        sm = L.edge_samples(M, i); sd = sm["sides"]
        if len(sd) != 2 or sd[0]["face"] == sd[1]["face"]:
            continue
        a, b = sd[0]["u"][100], sd[1]["u"][100]
        ang = math.degrees(math.acos(np.clip(a @ b, -1, 1)))
        print(i, "mid", np.round(sm["G"][100], 2), "u_f", np.round(a, 3), "u_g", np.round(b, 3), "angle(u_f,u_g)=%.1f  T=%.1f" % (ang, 180 - ang))
