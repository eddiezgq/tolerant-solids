"""Route B for sharp edges: re-intersection.

For a model whose faces are planar and whose vertices each have exactly three distinct faces,
re-intersect the face planes: each vertex becomes c_v = the common point of its three planes, and
each edge becomes the segment [c_v0, c_v1], which lies on both of its face planes. The re-intersected
polyhedron is a realization (before any PL step, it is already PL) if
  B1  |c_v - p_v| < tau_v                                  (vertex in its zone)
  B2  every point of [c_v0, c_v1] lies in Z(e)              (tube of radius tau_e around gamma_e, or end balls)
  B3  every point of the new face polygon lies in Z(f)      (within tau_f of P_f, or in Z(e) of one of its
                                                             edges, or in Z(v) of one of its vertices)
  B4  the polyhedron is embedded                            (OpenCascade validity + self-intersection check
                                                             on the exact polyhedron, tolerance 1e-9)
B1-B3 are checked on samples (edges: 400 points; faces: a grid of ~ 4000 points per polygon, with exact
point-to-segment and point-to-polygon distances). Margins are reported as min over samples of
(zone radius - distance) / zone radius.
"""
import sys, math, json
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Plane
from OCP.TopAbs import TopAbs_REVERSED
from OCP.gp import gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.TopoDS import TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SHELL


def seg_dist(x, a, b):
    ab = b - a; t = np.clip(((x - a) @ ab) / max(ab @ ab, 1e-300), 0, 1)
    return np.linalg.norm(x - (a + np.outer(t, ab) if x.ndim > 1 else a + t * ab), axis=-1)


def poly_dist(x, P, n):
    """Distance from points x to the planar convex-or-not polygon P (k x 3) with unit normal n."""
    k = len(P)
    h = (x - P[0]) @ n
    y = x - np.outer(h, n)
    # inside test by winding in the polygon plane
    e1 = P[1] - P[0]; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    Q = np.stack([(P - P[0]) @ e1, (P - P[0]) @ e2], 1)
    yq = np.stack([(y - P[0]) @ e1, (y - P[0]) @ e2], 1)
    inside = np.zeros(len(x), bool)
    for i in range(k):
        a, b = Q[i], Q[(i + 1) % k]
        cond = (a[1] > yq[:, 1]) != (b[1] > yq[:, 1])
        xi = a[0] + (yq[:, 1] - a[1]) * (b[0] - a[0]) / np.where(b[1] - a[1] == 0, 1e-300, b[1] - a[1])
        inside ^= cond & (yq[:, 0] < xi)
    db = np.min([seg_dist(x, P[i], P[(i + 1) % k]) for i in range(k)], axis=0)
    return np.where(inside, np.abs(h), db)


def face_polygon(M, fi, sm_all):
    """Ordered boundary vertex indices of face fi (single wire, straight edges)."""
    es = [ei for ei in range(len(M.E)) if fi in [u[0] for u in M.uses[ei]]]
    adj = {}
    for ei in es:
        a, b = M.ev[ei]
        adj.setdefault(a, []).append((b, ei)); adj.setdefault(b, []).append((a, ei))
    start = M.ev[es[0]][0]; order, prev, cur = [start], None, start
    while True:
        nxt = [v for v, e in adj[cur] if v != prev]
        if not nxt or nxt[0] == start:
            break
        prev, cur = cur, nxt[0]; order.append(cur)
    return order, es


def check(shape, name):
    M = L.Model(shape)
    planes = []
    for f in M.F:
        S = BRepAdaptor_Surface(f)
        if S.GetType() != GeomAbs_Plane:
            return dict(name=name, applicable=False, why="non-planar face")
        pl = S.Plane(); ax = pl.Axis()
        n = L.V(ax.Direction()); o = L.V(pl.Location())
        planes.append((n, n @ o))
    sm_all = [L.edge_samples(M, ei) for ei in range(len(M.E))]
    vf = [sorted(fi for fi in range(len(M.F)) if vi in M.fv[fi]) for vi in range(len(M.Vx))]
    if any(len(x) != 3 for x in vf):
        return dict(name=name, applicable=False, why="vertex not of degree 3")
    c = []
    for vi, fs in enumerate(vf):
        A = np.array([planes[f][0] for f in fs]); b = np.array([planes[f][1] for f in fs])
        c.append(np.linalg.solve(A, b))
    res = dict(name=name, applicable=True, fails=[])
    mB1 = min((M.tv[v] - np.linalg.norm(c[v] - M.p[v])) / M.tv[v] for v in range(len(M.Vx)))
    res["B1_margin"] = mB1
    if mB1 <= 0: res["fails"].append("B1")
    # zone membership helpers
    def in_Ze(x, ei):   # distance-based slack for Z(e) = tube U end balls
        G = sm_all[ei]["G"]
        dt = np.min([seg_dist(x, G[i], G[i + 1]) for i in range(len(G) - 1)], axis=0)
        s = (M.te[ei] - dt) / M.te[ei]
        for v in M.ev[ei]:
            s = np.maximum(s, (M.tv[v] - np.linalg.norm(x - M.p[v], axis=-1)) / M.tv[v])
        return s
    mB2 = math.inf
    for ei in range(len(M.E)):
        a, b = c[M.ev[ei][0]], c[M.ev[ei][1]]
        x = a + np.outer(np.linspace(0, 1, 400), b - a)
        mB2 = min(mB2, in_Ze(x, ei).min())
    res["B2_margin"] = mB2
    if mB2 <= 0: res["fails"].append("B2")
    mB3 = math.inf
    faces_new = []
    for fi, f in enumerate(M.F):
        order, es = face_polygon(M, fi, sm_all)
        Pn = np.array([c[v] for v in order])
        # original polygon from the OCC vertices of the face's boundary points (planar: P_f = polygon of
        # the boundary points of its pcurves); use the sampled boundary points B of each edge use
        Bpts = np.concatenate([sd["B"] for ei in es for sd in sm_all[ei]["sides"] if sd["face"] == fi])
        n = planes[fi][0]
        Po = np.array([sm_all[ei]["sides"][[sd["face"] for sd in sm_all[ei]["sides"]].index(fi)]["B"][0] for ei in es])
        # sample the new polygon on a grid (fan triangulation from vertex 0)
        pts = []
        for i in range(1, len(Pn) - 1):
            A, B, C = Pn[0], Pn[i], Pn[i + 1]
            m = 60
            for p in range(m + 1):
                for q in range(m + 1 - p):
                    pts.append(A + (B - A) * p / m + (C - A) * q / m)
        pts = np.array(pts)
        # P_f: polygon through the face's own boundary (its edge uses' boundary points, in wire order)
        Pold = []
        for v in order:
            # corner of the old patch at v: boundary point of an edge use at that end
            for ei in es:
                if v in M.ev[ei]:
                    sd = [sd for sd in sm_all[ei]["sides"] if sd["face"] == fi][0]
                    Pold.append(sd["B"][0] if M.ev[ei][0] == v else sd["B"][-1]); break
        Pold = np.array(Pold)
        slack = (M.tf[fi] - poly_dist(pts, Pold, n)) / M.tf[fi]
        for ei in es:
            slack = np.maximum(slack, in_Ze(pts, ei))
        mB3 = min(mB3, slack.min())
        faces_new.append(Pn)
    res["B3_margin"] = mB3
    if mB3 <= 0: res["fails"].append("B3")
    # B4: build the exact polyhedron and check it
    sew = BRepBuilderAPI_Sewing(1e-9)
    for Pn in faces_new:
        mp = BRepBuilderAPI_MakePolygon()
        for p in Pn: mp.Add(gp_Pnt(*p))
        mp.Close()
        sew.Add(BRepBuilderAPI_MakeFace(mp.Wire(), True).Face())
    sew.Perform(); sh = sew.SewedShape()
    ex = TopExp_Explorer(sh, TopAbs_SHELL)
    ok4 = False
    if ex.More():
        so = BRepBuilderAPI_MakeSolid(TopoDS.Shell(ex.Current())).Solid()
        chk = BRepAlgoAPI_Check(so, True, True)
        ok4 = BRepCheck_Analyzer(so).IsValid() and chk.IsValid()
    res["B4_embedded"] = ok4
    if not ok4: res["fails"].append("B4")
    res["ok"] = not res["fails"]
    print(f"== {name}: re-intersection {'PASS' if res['ok'] else 'FAIL ' + ','.join(res['fails'])}"
          f"  margins: vertex {mB1:.3f}, edge {mB2:.3f}, face {mB3:.3f}; embedded {ok4}")
    return res


if __name__ == "__main__":
    import lemma0_check_run as R
    names = sys.argv[1:] or [n for n in R.PARTS if n.startswith("sloppy") and "cylinder" not in n] + ["box", "wedge 10deg"]
    out = [check(R.PARTS[n](), n) for n in names]
    json.dump(out, open("../results/reintersect_result.json", "w"), indent=1, default=float)
