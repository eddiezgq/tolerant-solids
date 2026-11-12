"""Experiment 6a: a closed triangulated surface that passes BRepCheck_Analyzer but has NO realization.

Construction: a twisted triangular prism with 8 triangular faces.
  - The bottom triangle is at z = 0 and the top triangle at z = h, rotated by theta.
  - Each side quad is split into two triangles.
  - For large theta, two side triangles that share no vertex have linked boundaries
    (linking number ±1).

No realization (rigorous). Let A and B be non-adjacent triangles whose boundaries are linked, and
assume every tolerance is <= tau with 2 tau < dist(dA, dB).
  1. In any realization, dA' lies in the tau-neighbourhood T_A of dA (vertex balls and edge tubes),
     and dB' lies in T_B. The two neighbourhoods are disjoint.
  2. If tau is below the tube-forming radius of each triangle boundary, T_A is a solid torus with
     core dA. Then dA' winds once around it: it visits the three vertex balls in cyclic order and
     runs along the edge tubes. The same holds for dB'.
  3. Hence lk(dA', dB') = lk(dA, dB) = ±1, so dA' meets every disk bounded by dB', in particular
     the realized face B'.
  4. But A's edges are not incident to B, so an embedding must keep them disjoint. Contradiction.
     (Step 2 uses the vertex-ball/edge-tube structure; for triangles, the tube-forming radius is
     at least the smallest distance from a vertex to the opposite edge times sin(angle)/2.
     The script checks a simpler sufficient margin: tau < 1/4 of the smallest edge-to-non-incident-edge
     distance within each triangle.)

Script:
  - finds theta with a linked non-adjacent pair and reports dist(dA, dB);
  - builds the solid in OpenCascade (polygon faces, sewing, solid) with tolerance tau;
  - runs BRepCheck_Analyzer and BRepAlgoAPI_Check.
"""
import json, itertools
import numpy as np
from OCP.gp import gp_Pnt
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace,
                                BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid)
from OCP.TopoDS import TopoDS
from OCP.TopAbs import TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
import exp6b as E


def prism(theta, h=2.0):
    ang = np.deg2rad([90, 210, 330])
    bot = [np.array([np.cos(a), np.sin(a), 0.0]) for a in ang]
    top = [np.array([np.cos(a + theta), np.sin(a + theta), h]) for a in ang]
    V = bot + top                                   # indices 0,1,2 bottom; 3,4,5 top
    F = [(0, 2, 1), (3, 4, 5)]
    for i in range(3):
        j = (i + 1) % 3
        F += [(i, j, 3 + j), (i, 3 + j, 3 + i)]
    return np.array(V), F


def seg_tri_cross(p, q, a, b, c):
    """Signed crossing of segment pq through triangle abc (0 if none), Moller-Trumbore style."""
    n = np.cross(b - a, c - a)
    dp, dq = n @ (p - a), n @ (q - a)
    if dp * dq >= 0:
        return 0
    x = p + (dp / (dp - dq)) * (q - p)
    for u, v in ((a, b), (b, c), (c, a)):
        if np.cross(v - u, x - u) @ n < 0:
            return 0
    return 1 if dp < 0 else -1


def linking(V, A, B):
    """lk(dA, dB) = algebraic intersection of the loop dA with the disk B."""
    a = V[list(A)]
    return sum(seg_tri_cross(a[k], a[(k + 1) % 3], *V[list(B)]) for k in range(3))


def seg_seg_dist(p, q, r, s, n=200):
    t = np.linspace(0, 1, n)[:, None]
    P = p + t * (q - p); Q = r + t * (s - r)
    return float(np.min(np.linalg.norm(P[:, None] - Q[None], axis=2)))


def loop_dist(V, A, B):
    ea = [(V[A[k]], V[A[(k + 1) % 3]]) for k in range(3)]
    eb = [(V[B[k]], V[B[(k + 1) % 3]]) for k in range(3)]
    return min(seg_seg_dist(*e, *f) for e in ea for f in eb)


best = None
for deg in range(100, 260, 5):
    V, F = prism(np.deg2rad(deg))
    for A, B in itertools.combinations(F, 2):
        if set(A) & set(B):
            continue
        lk = linking(V, A, B)
        if abs(lk) == 1:
            d = loop_dist(V, A, B)
            if best is None or d > best[0]:
                best = (d, deg, A, B, lk)

res = {}
if best is None:
    res["found"] = False
else:
    d, deg, A, B, lk = best
    V, F = prism(np.deg2rad(deg))
    # tube-forming margin inside each triangle: smallest distance between an edge and the opposite vertex
    def inner_margin(T):
        p = V[list(T)]
        return min(np.linalg.norm(np.cross(p[(k + 1) % 3] - p[k], p[(k + 2) % 3] - p[k])) /
                   np.linalg.norm(p[(k + 1) % 3] - p[k]) for k in range(3))
    margin = min(inner_margin(A), inner_margin(B))
    tau = 0.2 * min(d, margin)                   # 2 tau < d, and tau < margin / 4 (well below)
    res.update(found=True, theta_deg=deg, faces_A=list(map(int, A)), faces_B=list(map(int, B)),
               linking=int(lk), dist_boundaries=d, inner_margin=margin, tau=tau,
               two_tau_less_than_dist=2 * tau < d)

    # build in OpenCascade
    sew = BRepBuilderAPI_Sewing(1e-6)
    for f in F:
        poly = BRepBuilderAPI_MakePolygon(*[gp_Pnt(*V[i]) for i in f], True)
        sew.Add(BRepBuilderAPI_MakeFace(poly.Wire(), True).Face())
    sew.Perform()
    sh = sew.SewedShape()
    ex = TopExp_Explorer(sh, TopAbs_SHELL)
    shell = TopoDS.Shell(ex.Current())
    solid = BRepBuilderAPI_MakeSolid(shell).Solid()
    E.set_tol(solid, tau)
    ch = BRepAlgoAPI_Check(solid, True, True)
    res["brepcheck_valid"] = bool(BRepCheck_Analyzer(solid).IsValid())
    res["bop_valid"] = bool(ch.IsValid())
    res["bop_status"] = sorted({str(r.GetCheckStatus()).split('.')[-1] for r in ch.Result()})
print(json.dumps(res, indent=1))
json.dump(res, open("exp6a_result.json", "w"), indent=1)
