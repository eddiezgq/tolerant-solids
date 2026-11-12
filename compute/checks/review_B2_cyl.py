"""Review: independent B1/B2 check for 'sloppy cylinder g=0.01'.
New vertices/edges are computed analytically from the face surfaces (plane z=c cuts a cylinder with vertical axis
in a circle; the seam line u=0 of the cylinder cuts each plane in a point), then compared against the ORIGINAL
edge curves by exact point-curve projection (GeomAPI_ProjectPointOnCurve), not by a sampled polyline."""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R
from review_B2_T2 import rebuild
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.gp import gp_Pnt

name = sys.argv[1] if len(sys.argv) > 1 else "sloppy cylinder g=0.01"
M, N = rebuild(R.PARTS[name]())
print("orig F/E/V", len(M.F), len(M.E), len(M.Vx), " tol_v", np.round(M.tv, 5), " tol_e", np.round(M.te, 5), " tol_f", M.tf)
planes, cyl = [], None
for fi, f in enumerate(M.F):
    A = BRepAdaptor_Surface(f)
    if A.GetType() == GeomAbs_Plane:
        pl = A.Plane(); n = L.V(pl.Axis().Direction()); o = L.V(pl.Location())
        assert abs(abs(n[2]) - 1) < 1e-12; planes.append((fi, o[2]))
    elif A.GetType() == GeomAbs_Cylinder:
        c = A.Cylinder(); ax = c.Position(); cyl = (fi, L.V(ax.Location()), L.V(ax.Direction()), L.V(ax.XDirection()), c.Radius())
print("planes z:", planes, " cylinder: loc", cyl[1], "dir", cyl[2], "xdir", cyl[3], "R", cyl[4])
cf, C0, D, X, Rr = cyl
assert np.allclose(np.abs(D), [0, 0, 1])

def dist_curve(x, e):
    loc = e.Location(); assert loc.IsIdentity()
    c = BRep_Tool.Curve_s(e, 0.0, 0.0); a, b = BRep_Tool.Range_s(e)
    pr = GeomAPI_ProjectPointOnCurve(gp_Pnt(*x), c, a, b)
    d = pr.LowerDistance() if pr.NbPoints() else math.inf
    # also the curve end points (projection only finds interior extrema)
    for t in (a, b):
        d = min(d, np.linalg.norm(L.V(c.Value(t)) - x))
    return d

def slack(x, k):
    s = (M.te[k] - dist_curve(x, M.E[k])) / M.te[k]
    for v in M.ev[k]:
        s = max(s, (M.tv[v] - np.linalg.norm(x - M.p[v])) / M.tv[v])
    return s

# analytic new vertices: seam line (u = 0) of the cylinder meets each plane
seam_xy = C0[:2] + Rr * X[:2]
b1 = []
for fi, z in planes:
    cv = np.array([seam_xy[0], seam_xy[1], z])
    # original vertex on this plane's circle
    vi = min(range(len(M.Vx)), key=lambda k: np.linalg.norm(M.p[k] - cv))
    m = (M.tv[vi] - np.linalg.norm(cv - M.p[vi])) / M.tv[vi]
    b1.append(m); print(f"vertex on plane z={z:.5f}: c_v={np.round(cv,5)} p_v={np.round(M.p[vi],5)} |c-p|={np.linalg.norm(cv-M.p[vi]):.5f} tau_v={M.tv[vi]:.5f} margin {m:.4f}")
    # and the OCC vertex of the rebuilt model
    j = min(range(len(N.Vx)), key=lambda k: np.linalg.norm(N.p[k] - cv)); print("   OCC new vertex differs from analytic by", np.linalg.norm(N.p[j] - cv), "new tol", N.tv[j])

# analytic circles and the seam segment, densely sampled, exact projection onto original curves
b2 = {}
for k in range(len(M.E)):
    faces = sorted(set(u[0] for u in M.uses[k]))
    if faces == [cf]:            # seam
        zs = sorted(z for _, z in planes)
        pts = [np.array([seam_xy[0], seam_xy[1], z]) for z in np.linspace(zs[0], zs[1], 4001)]
        lab = "seam"
    else:
        z = dict(planes)[[f for f in faces if f != cf][0]]
        th = np.linspace(0, 2 * math.pi, 20001)
        Y = np.cross(D, X)
        pts = [np.array([C0[0], C0[1], z]) + Rr * (math.cos(t) * X + math.sin(t) * Y) for t in th]
        lab = f"circle z={z:.5f}"
    sl = np.array([slack(x, k) for x in pts])
    j = int(np.argmin(sl)); b2[k] = sl[j]
    tube_only = np.array([(M.te[k] - dist_curve(x, M.E[k])) / M.te[k] for x in pts])
    print(f"edge {k} ({lab}): tau_e={M.te[k]:.5f}  B2 margin {sl[j]:.4f} at {np.round(pts[j],4)};  tube-only margin min {tube_only.min():.4f}, max dist {M.te[k]*(1-tube_only.min()):.5f}")
print("independent: B1 margin", min(b1), " B2 margin", min(b2.values()))
# new-model edges vs analytic: max distance of OCC new edge samples to the analytic circle / line
for i in range(len(N.E)):
    G = L.edge_samples(N, i)["G"]
    r = np.linalg.norm(G[:, :2] - C0[:2], axis=1)
    print(f"new edge {i}: tol {N.te[i]:.2e}; |r-R| max {np.abs(r-Rr).max():.2e}; z range {G[:,2].min():.5f}..{G[:,2].max():.5f}")
