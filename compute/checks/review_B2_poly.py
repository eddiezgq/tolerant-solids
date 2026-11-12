"""Review: at the worst dense-B3 point of 'sloppy cylinder g=0.01', compare reintersect_curved's polyline distance
(200 samples of the old edge) with the exact point-curve distance."""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R
from OCP.BRep import BRep_Tool
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.gp import gp_Pnt
M = L.Model(R.PARTS["sloppy cylinder g=0.01"]())
x = np.array([-1.2427, 2.7322, 0.0005])
for k in range(len(M.E)):
    G = L.edge_samples(M, k)["G"]; a, b = G[:-1], G[1:]; ab = b - a
    t = np.clip(np.einsum('ij,ij->i', x - a, ab) / np.maximum(np.einsum('ij,ij->i', ab, ab), 1e-300), 0, 1)
    dp = np.min(np.linalg.norm(x - (a + t[:, None] * ab), axis=1))
    c = BRep_Tool.Curve_s(M.E[k], 0.0, 0.0); u0, u1 = BRep_Tool.Range_s(M.E[k])
    pr = GeomAPI_ProjectPointOnCurve(gp_Pnt(*x), c, u0, u1); de = pr.LowerDistance() if pr.NbPoints() else min(np.linalg.norm(L.V(c.Value(u)) - x) for u in (u0, u1))
    print(k, f"tau {M.te[k]:.5f} polyline {dp:.6f} exact {de:.6f} -> slack poly {(M.te[k]-dp)/M.te[k]:.4f} exact {(M.te[k]-de)/M.te[k]:.4f}")
