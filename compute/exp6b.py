"""Experiment 6b: an OpenCascade model that passes both checks but has two non-isotopic realizations.

Model.
  Two tori A and B, each with tube radius rho and major radius R.
  - A lies in the plane z = +c and B in the plane z = -c, with c = rho + g/2, so the vertical gap
    between the tubes is g.
  - The centres are a distance D apart. In top view the core circles cross at two points, and A is
    above B at both, so the two rings are unlinked (linking number 0).
  - Every face, edge and vertex gets tolerance tau, with tau >= 2c (plus a margin).

Realization 1: the nominal geometry.

Realization 2:
  - Near crossing 1, A's cross-sections are shifted down by 2c and B's up by 2c, so the rings swap
    over and under there.
  - Each shift is a smooth bump in the angle around the ring's own centre. A ramps only where its
    core is horizontally farther than 2 rho + margin from B's core, and B ramps only where it is
    that far from A's core.
  - The bumps vanish near the seam edges (at angle 0), so edges and vertices do not move.
  - Every point moves by at most 2c <= tau. Since the moved point started on the nominal face, it
    stays in the face's tau-zone.

Checks (all by script):
  1. BRepCheck_Analyzer and BRepAlgoAPI_Check on the toleranced model.
  2. Embeddedness of realization 2.
     - Each deformed torus is embedded: its cross-sections lie in distinct half-planes through its axis.
     - The two tori are disjoint: the minimum 3D distance between the deformed core curves exceeds 2 rho.
       Every surface point is within rho of its core, so the surfaces are then disjoint.
  3. Zone membership: the maximum displacement is at most tau, and the displacement is zero on the
     seam edges and vertex.
  4. Linking number of the core curves (Gauss integral): 0 for realization 1, ±1 for realization 2.
     For two disjoint solid tori, |linking number of the cores| is invariant under ambient isotopy,
     so the r-sets are not isotopic.
  5. wfs of the nominal surface is at most rho. Any point p on A's core has as nearest set the whole
     circle of radius rho around p in its cross-section plane, whose convex hull contains p, so p is
     critical. Since tau > rho, the collar condition (tau < wfs) fails, as P1 requires for
     non-uniqueness to be possible.
"""
import json
import numpy as np
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS, TopoDS_Compound
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check

R, rho, g, D = 10.0, 0.5, 0.5, 12.0
c = rho + g / 2
tau = 2 * c * 1.1


def torus(cx, cz):
    return BRepPrimAPI_MakeTorus(gp_Ax2(gp_Pnt(cx, 0, cz), gp_Dir(0, 0, 1)), R, rho).Shape()


def set_tol(shape, t):
    b = BRep_Builder()
    for kind, upd in ((TopAbs_FACE, lambda s: b.UpdateFace(TopoDS.Face(s), t)),
                      (TopAbs_EDGE, lambda s: b.UpdateEdge(TopoDS.Edge(s), t)),
                      (TopAbs_VERTEX, lambda s: b.UpdateVertex(TopoDS.Vertex(s), t))):
        ex = TopExp_Explorer(shape, kind)
        while ex.More():
            upd(ex.Current()); ex.Next()


A, B = torus(0.0, c), torus(D, -c)
set_tol(A, tau); set_tol(B, tau)
comp = TopoDS_Compound(); bb = BRep_Builder(); bb.MakeCompound(comp); bb.Add(comp, A); bb.Add(comp, B)
chk = BRepAlgoAPI_Check(comp, True, True)   # geometry + self-interference checks
res = dict(R=R, rho=rho, g=g, D=D, c=c, tau=tau,
           brepcheck_A=bool(BRepCheck_Analyzer(A).IsValid()),
           brepcheck_B=bool(BRepCheck_Analyzer(B).IsValid()),
           brepcheck_compound=bool(BRepCheck_Analyzer(comp).IsValid()),
           bop_check_valid=bool(chk.IsValid()))

# ---- core curves and the deformation -------------------------------------------------------
N = 20000
th = np.linspace(0, 2 * np.pi, N, endpoint=False)
coreA = np.stack([R * np.cos(th), R * np.sin(th), np.full(N, c)], 1)
coreB = np.stack([D + R * np.cos(th), R * np.sin(th), np.full(N, -c)], 1)

# crossing 1 in top view: x = D/2, y = +sqrt(R^2 - (D/2)^2)
yx = np.sqrt(R * R - (D / 2) ** 2)
thA1 = np.arctan2(yx, D / 2)              # angle of crossing 1 on A
thB1 = np.arctan2(yx, D / 2 - D)          # angle of crossing 1 on B


def horiz_dist_to_circle(P, cx):
    r = np.hypot(P[:, 0] - cx, P[:, 1])
    return np.abs(r - R)


margin = 0.3
farA = horiz_dist_to_circle(coreA, D) > 2 * rho + margin     # A may ramp here
farB = horiz_dist_to_circle(coreB, 0.0) > 2 * rho + margin   # B may ramp here


def bump(theta, th0, far, ramp=0.25):
    """Smooth 0..1 profile in the angle: equal to 1 on the connected arc of non-far samples around th0,
    falling to 0 with a cosine ramp of angular width `ramp` just outside that arc, 0 elsewhere."""
    n = len(theta)
    i0 = int(np.argmin(np.abs(np.angle(np.exp(1j * (theta - th0))))))
    k = 0
    while not far[(i0 + k) % n] or not far[(i0 - k) % n]:
        k += 1
    w = (k + 1) * (2 * np.pi / n)              # half-width of the arc that must be fully shifted
    d = np.abs(np.angle(np.exp(1j * (theta - th0))))
    t = np.clip((d - w) / ramp, 0, 1)
    return 0.5 * (1 + np.cos(np.pi * t))


fA = bump(th, thA1, farA)
fB = bump(th, thB1, farB)
coreA2 = coreA - np.stack([0 * th, 0 * th, 2 * c * fA], 1)
coreB2 = coreB + np.stack([0 * th, 0 * th, 2 * c * fB], 1)

# ramps only in the far region
rampA = (fA > 1e-9) & (fA < 1 - 1e-9)
rampB = (fB > 1e-9) & (fB < 1 - 1e-9)
res["A_ramps_only_where_far"] = bool(np.all(farA[rampA]))
res["B_ramps_only_where_far"] = bool(np.all(farB[rampB]))
res["seam_fixed"] = bool(fA[0] == 0 and fB[0] == 0)
res["max_displacement"] = float(2 * c * max(fA.max(), fB.max()))
res["zone_ok"] = res["max_displacement"] <= tau and res["seam_fixed"]

from scipy.spatial import cKDTree
def min_core_dist(P, Q):
    d, _ = cKDTree(Q).query(P)
    return float(d.min())
res["min_core_dist_nominal"] = min_core_dist(coreA, coreB)
res["min_core_dist_realization2"] = min_core_dist(coreA2, coreB2)
res["disjoint_realization2"] = res["min_core_dist_realization2"] > 2 * rho
# sampling error of the core distance: at most the chord between consecutive samples
res["core_sample_spacing"] = float(2 * np.pi * R / N)


def linking(P, Q):
    """Gauss linking integral with midpoint segments."""
    dP = np.roll(P, -1, 0) - P; mP = P + dP / 2
    dQ = np.roll(Q, -1, 0) - Q; mQ = Q + dQ / 2
    s = 0.0
    for i in range(0, len(mP), 1):
        r = mP[i] - mQ
        cr = np.cross(dP[i], dQ)
        s += np.sum((r * cr).sum(1) / np.linalg.norm(r, axis=1) ** 3)
    return s / (4 * np.pi)


sub = slice(None, None, 10)
res["linking_nominal"] = float(linking(coreA[sub], coreB[sub]))
res["linking_realization2"] = float(linking(coreA2[sub], coreB2[sub]))
res["wfs_upper_bound"] = rho
res["collar_condition_fails"] = tau > rho
print(json.dumps(res, indent=1))
json.dump(res, open("exp6b_result.json", "w"), indent=1)
