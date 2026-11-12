"""Review: B1/B2 with exact point-curve projection (not a 200-point polyline) and 4000 samples per new edge."""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R, reintersect_curved as RC
from review_B2_T2 import rebuild
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.gp import gp_Pnt
for name in sys.argv[1:]:
    M, N = rebuild(R.PARTS[name]())
    curves = [(BRep_Tool.Curve_s(e, 0.0, 0.0),) + tuple(BRep_Tool.Range_s(e)) for e in M.E]
    def dcurve(x, k):
        c, a, b = curves[k]; pr = GeomAPI_ProjectPointOnCurve(gp_Pnt(*x), c, a, b)
        d = pr.LowerDistance() if pr.NbPoints() else math.inf
        return min(d, np.linalg.norm(L.V(c.Value(a)) - x), np.linalg.norm(L.V(c.Value(b)) - x))
    vmap = [min(range(len(M.Vx)), key=lambda k: np.linalg.norm(N.p[i] - M.p[k])) for i in range(len(N.Vx))]
    b1 = min((M.tv[vmap[i]] - np.linalg.norm(N.p[i] - M.p[vmap[i]])) / M.tv[vmap[i]] for i in range(len(N.Vx)))
    b2 = math.inf
    for i, e in enumerate(N.E):
        # same matching rule as reintersect_curved: same vertex pair, nearest midpoint
        c = BRepAdaptor_Curve(e); ts = np.linspace(c.FirstParameter(), c.LastParameter(), 4000)
        X = [L.V(c.Value(t)) for t in ts]
        cand = [k for k in range(len(M.E)) if sorted(M.ev[k]) == sorted(vmap[v] for v in N.ev[i])]
        k = min(cand, key=lambda k: dcurve(X[2000], k))
        for x in X:
            s = (M.te[k] - dcurve(x, k)) / M.te[k]
            for v in M.ev[k]: s = max(s, (M.tv[v] - np.linalg.norm(x - M.p[v])) / M.tv[v])
            b2 = min(b2, s)
    print(f"{name}: exact B1 {b1:.4f}  exact B2 {b2:.4f}; new-model max edge tol {max(N.te):.1e}, vertex tol {max(N.tv):.1e}", flush=True)
