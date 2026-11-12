"""Review: does reintersect_curved.in_patch (BRepClass_FaceClassifier, tol 1e-9) return IN/ON for points
OUTSIDE the trimmed patch but within the (large) sewn edge tolerance of its boundary?"""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R, reintersect_curved as RC
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve2d
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.GeomAbs import GeomAbs_Plane
from OCP.gp import gp_Pnt, gp_Pnt2d, gp_Vec2d
from OCP.TopAbs import TopAbs_IN, TopAbs_ON, TopAbs_OUT
for name in sys.argv[1:] or ["sloppy cylinder g=0.01", "sloppy box g=0.01"]:
    M = L.Model(R.PARTS[name]())
    print("==", name, "edge tolerances", np.round(M.te, 4))
    for fi, f in enumerate(M.F):
        S = BRepAdaptor_Surface(f)
        for k in sorted(M.fe[fi]):
            if M.te[k] < 1e-5: continue
            sm = L.edge_samples(M, k)
            side = [s for s in sm["sides"] if s["face"] == fi][0]
            for j in (50, 100):
                b = side["B"][j]; u = side["u"][j]          # boundary point of P_f, inward tangent
                res = []
                for dfrac in (0.1, 0.5, 1.0, 2.0):
                    x = b - dfrac * M.te[k] * u               # step OUT of the patch, in the surface's tangent plane
                    if S.GetType() != GeomAbs_Plane:
                        continue
                    st = "IN/ON" if RC.in_patch(f, x) else "OUT"
                    dd = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*x)).Vertex(), f); dd.Perform()
                    res.append(f"{dfrac:.1f}tau:{st}(d_face={dd.Value():.4f})")
                if res: print(f" face {fi} edge {k} sample {j}: " + "  ".join(res))
