"""Review: denser B3 for the re-trimmed model, including the corner regions that reintersect_curved skips.
(a) walks as in reintersect_curved but from 1000 boundary samples per edge (t in [0,1] incl. ends), 200 steps,
    a walk that leaves the new face or never reaches the old patch is only an error if it leaves the zones;
(b) at each new vertex, a UV grid (81x81, half-width 4*tau_max in 3D) restricted to the new face and outside
    the old patch.  Slack = max over the face's old edge zones (exact curve projection) and vertex balls."""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R, reintersect_curved as RC
from review_B2_T2 import rebuild
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve2d
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve, GeomAPI_ProjectPointOnSurf
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_IN, TopAbs_ON
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Vec2d

name = sys.argv[1] if len(sys.argv) > 1 else "sloppy box g=0.01"
NS = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
M, N = rebuild(R.PARTS[name]())
fmap = []
for f in N.F:
    A = BRepAdaptor_Surface(f); a, b, c, d = RC.BRepTools.UVBounds_s(f)
    p = L.V(A.Value((a + b) / 2, (c + d) / 2)); fmap.append(min(range(len(M.F)), key=lambda k: RC.surf_dist(M.F[k], p)))
curves = []
for e in M.E:
    assert e.Location().IsIdentity()
    curves.append((BRep_Tool.Curve_s(e, 0.0, 0.0),) + tuple(BRep_Tool.Range_s(e)))
def dcurve(x, k):
    c, a, b = curves[k]; pr = GeomAPI_ProjectPointOnCurve(gp_Pnt(*x), c, a, b)
    d = pr.LowerDistance() if pr.NbPoints() else math.inf
    return min(d, np.linalg.norm(L.V(c.Value(a)) - x), np.linalg.norm(L.V(c.Value(b)) - x))
def slack(x, es, vs):
    s = max((M.te[k] - dcurve(x, k)) / M.te[k] for k in es)
    return max([s] + [(M.tv[v] - np.linalg.norm(x - M.p[v])) / M.tv[v] for v in vs])
worst = (math.inf, None)
for fi, f in enumerate(N.F):
    of = M.F[fmap[fi]]; es = sorted(M.fe[fmap[fi]]); vs = sorted(M.fv[fmap[fi]])
    S = BRepAdaptor_Surface(f); tmax = max(M.te[k] for k in es)
    fw = (math.inf, None)
    ex = TopExp_Explorer(f, TopAbs_EDGE)
    while ex.More():
        oe = TopoDS.Edge(ex.Current()); ex.Next()
        if BRep_Tool.Degenerated_s(oe): continue
        pc = BRepAdaptor_Curve2d(oe, f); t0, t1 = pc.FirstParameter(), pc.LastParameter()
        for t in np.linspace(t0, t1, NS):
            uv, duv = gp_Pnt2d(), gp_Vec2d(); pc.D1(t, uv, duv)
            nuv = np.array([-duv.Y(), duv.X()]); nuv /= np.linalg.norm(nuv)
            q = gp_Pnt2d(uv.X() + 1e-6 * nuv[0], uv.Y() + 1e-6 * nuv[1])
            if BRepClass_FaceClassifier(f, q, 1e-9).State() != TopAbs_IN: nuv = -nuv
            P, Su, Sv = gp_Pnt(), gp_Vec(), gp_Vec(); S.D1(uv.X(), uv.Y(), P, Su, Sv)
            sp = np.linalg.norm(nuv[0] * L.V(Su) + nuv[1] * L.V(Sv))
            for s in np.linspace(0, 4 * tmax / sp, 200):
                q2 = gp_Pnt2d(uv.X() + s * nuv[0], uv.Y() + s * nuv[1])
                if s > 0 and BRepClass_FaceClassifier(f, q2, 1e-9).State() not in (TopAbs_IN, TopAbs_ON): break  # left the new face
                x = L.V(S.Value(q2.X(), q2.Y()))
                if RC.in_patch(of, x): break
                sl = slack(x, es, vs)
                if sl < fw[0]: fw = (sl, ("walk", np.round(x, 4)))
    # corner grids
    for vi in sorted(N.fv[fi]):
        pr = GeomAPI_ProjectPointOnSurf(gp_Pnt(*N.p[vi]), BRep_Tool.Surface_s(f)); u0, v0 = pr.LowerDistanceParameters()
        P, Su, Sv = gp_Pnt(), gp_Vec(), gp_Vec(); S.D1(u0, v0, P, Su, Sv)
        hu, hv = 4 * tmax / np.linalg.norm(L.V(Su)), 4 * tmax / np.linalg.norm(L.V(Sv))
        for du in np.linspace(-hu, hu, 81):
            for dv in np.linspace(-hv, hv, 81):
                for uu in (u0 + du, u0 + du + 2 * math.pi, u0 + du - 2 * math.pi):
                    if BRepClass_FaceClassifier(f, gp_Pnt2d(uu, v0 + dv), 1e-9).State() not in (TopAbs_IN, TopAbs_ON): continue
                    x = L.V(S.Value(uu, v0 + dv))
                    if RC.in_patch(of, x): continue
                    sl = slack(x, es, vs)
                    if sl < fw[0]: fw = (sl, ("corner", np.round(x, 4)))
    print(f"new face {fi} (old {fmap[fi]}): dense B3 margin {fw[0]:.4f} at {fw[1]}", flush=True)
    worst = min(worst, fw, key=lambda z: z[0])
print("dense B3 margin", worst)
