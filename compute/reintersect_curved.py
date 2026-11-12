"""Route B for curved models: re-intersect the extended face surfaces and re-trim.

1. Each face's underlying surface is extended (periodic directions: full period; others: the face's UV box
   enlarged by EXT model units) and turned into a face.
2. BOPAlgo_MakerVolume splits space by these faces; we keep the solid whose centre of mass is closest to the
   original solid's.
3. Correspondence: a new face goes to the original face whose surface it lies on; a new edge to the original edge
   with the same pair of adjacent faces (nearest one if several); a new vertex to the nearest original vertex.
   The combinatorics must agree with the original model (C: same numbers of faces, edges, vertices; same incidences).
4. Zone checks (sampled):
   B1  new vertex in Z(v);
   B2  new edge: every sample within tau_e of the original edge curve or inside an end-vertex ball;
   B3  new face: walk inward from each sample of its boundary (in the face's UV space) until the point lies in the
       original trimmed patch (UV classification against the original face, same surface); every point on the way
       must be in the original patch, in Z(e) of an edge of the face, or in Z(v) of a vertex of the face.
   B4  the new solid passes BRepCheck_Analyzer and BRepAlgoAPI_Check;
   T   transversality: min over interior samples of min(phi, pi - phi), phi = angle between the two faces' inward
       in-plane tangents at a new edge; it is 0 both for tangent continuation (phi = pi) and for a fold (phi = 0).
       Seams are skipped. The vertex tangent-cone part of T is NOT checked.
Distances to an original edge are measured to a 2000-point polyline of it, minus the measured chord error, so
they are conservative. B3 skips 0.5% of each boundary curve at each end and samples 80 points per curve; a denser
re-check with exact distances is in checks/review_B2_B3dense.py (second review).
Margins are reported as min over samples of (zone radius - distance) / zone radius.
"""
import sys, math, json
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from OCP.BRep import BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeSolid
from OCP.BOPAlgo import BOPAlgo_MakerVolume
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_SHELL, TopAbs_IN, TopAbs_ON, TopAbs_REVERSED
from OCP.TopoDS import TopoDS
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve, BRepAdaptor_Curve2d
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Vec2d

EXT = 1.0


def as_solid(shape):
    ex = TopExp_Explorer(shape, TopAbs_SOLID)
    if ex.More():
        return TopoDS.Solid(ex.Current())
    ex = TopExp_Explorer(shape, TopAbs_SHELL)
    return BRepBuilderAPI_MakeSolid(TopoDS.Shell(ex.Current())).Solid()


def centre(solid):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(solid, g)
    return L.V(g.CentreOfMass()), g.Mass()


def extended_face(f):
    S = BRep_Tool.Surface_s(f)
    A = BRepAdaptor_Surface(f)
    u0, u1, v0, v1 = BRepTools.UVBounds_s(f)
    if A.IsUPeriodic():
        u0, u1 = A.FirstUParameter(), A.FirstUParameter() + A.UPeriod()
    else:
        u0, u1 = u0 - EXT, u1 + EXT
    if A.IsVPeriodic():
        v0, v1 = A.FirstVParameter(), A.FirstVParameter() + A.VPeriod()
    else:
        v0, v1 = v0 - EXT, v1 + EXT
    return BRepBuilderAPI_MakeFace(S, u0, u1, v0, v1, 1e-7).Face()


def surf_dist(f, p):
    pr = GeomAPI_ProjectPointOnSurf(gp_Pnt(*p), BRep_Tool.Surface_s(f))
    return pr.LowerDistance() if pr.NbPoints() else math.inf


def in_patch(f, p):
    """p lies on f's surface: is it in the original trimmed patch (UV classification)?"""
    pr = GeomAPI_ProjectPointOnSurf(gp_Pnt(*p), BRep_Tool.Surface_s(f))
    if not pr.NbPoints():
        return False
    u, v = pr.LowerDistanceParameters()
    st = BRepClass_FaceClassifier(f, gp_Pnt2d(u, v), 1e-9).State()
    return st in (TopAbs_IN, TopAbs_ON)


def check(shape, name, verbose=True):
    M = L.Model(shape)
    orig = as_solid(shape)
    c0, vol0 = centre(orig)
    mv = BOPAlgo_MakerVolume()
    for f in M.F:
        mv.AddArgument(extended_face(f))
    mv.Perform()
    sols, ex = [], TopExp_Explorer(mv.Shape(), TopAbs_SOLID)
    while ex.More():
        sols.append(TopoDS.Solid(ex.Current())); ex.Next()
    if not sols:
        return dict(name=name, ok=False, why="MakerVolume produced no solid")
    new = min(sols, key=lambda s: np.linalg.norm(centre(s)[0] - c0))
    N = L.Model(new)
    res = dict(name=name, fails=[], vol_ratio=centre(new)[1] / vol0)
    # correspondence
    fmap = []
    for f in N.F:
        A = BRepAdaptor_Surface(f)
        u = (A.FirstUParameter() + A.LastUParameter()) / 2; v = (A.FirstVParameter() + A.LastVParameter()) / 2
        uv0, uv1, vv0, vv1 = BRepTools.UVBounds_s(f)
        p = L.V(A.Value((uv0 + uv1) / 2, (vv0 + vv1) / 2))
        fmap.append(min(range(len(M.F)), key=lambda k: surf_dist(M.F[k], p)))
    emap = []
    for ei in range(len(N.E)):
        pair = sorted(fmap[u[0]] for u in N.uses[ei])
        cand = [k for k in range(len(M.E)) if sorted(u[0] for u in M.uses[k]) == pair]
        mid = L.edge_samples(N, ei)["G"][len(L.edge_samples(N, ei)["G"]) // 2]
        emap.append(min(cand, key=lambda k: np.min(np.linalg.norm(L.edge_samples(M, k)["G"] - mid, axis=1))) if cand else None)
    vmap = [min(range(len(M.Vx)), key=lambda k: np.linalg.norm(N.p[i] - M.p[k])) for i in range(len(N.Vx))]
    comb = (len(N.F), len(N.E), len(N.Vx)) == (len(M.F), len(M.E), len(M.Vx)) and None not in emap \
        and len(set(fmap)) == len(M.F) and len(set(emap)) == len(M.E) and len(set(vmap)) == len(M.Vx) \
        and all(sorted(vmap[v] for v in N.ev[i]) == sorted(M.ev[emap[i]]) for i in range(len(N.E)))
    res["C_combinatorics"] = bool(comb)
    if not comb:
        res["fails"].append("C"); res["ok"] = False
        if verbose:
            print(f"== {name}: combinatorics differ: new F/E/V {len(N.F)}/{len(N.E)}/{len(N.Vx)} vs {len(M.F)}/{len(M.E)}/{len(M.Vx)}")
        return res
    # B1
    b1 = min((M.tv[vmap[i]] - np.linalg.norm(N.p[i] - M.p[vmap[i]])) / M.tv[vmap[i]] for i in range(len(N.Vx)))
    # B2
    def fine_poly(e, n=2000):
        c = BRepAdaptor_Curve(e)
        ts = np.linspace(c.FirstParameter(), c.LastParameter(), 2 * n + 1)
        P = np.array([L.V(c.Value(t)) for t in ts])
        Pe, Po = P[::2], P[1::2]
        a, b = Pe[:-1], Pe[1:]; ab = b - a
        t = np.clip(np.einsum('ij,ij->i', Po - a, ab) / np.maximum(np.einsum('ij,ij->i', ab, ab), 1e-300), 0, 1)
        err = np.max(np.linalg.norm(Po - (a + t[:, None] * ab), axis=1))
        return Pe, err
    Gold, Gerr = zip(*[fine_poly(e) for e in M.E])
    def dist_poly(x, G):
        a, b = G[:-1], G[1:]; ab = b - a
        t = np.clip(np.einsum('ij,ij->i', x - a, ab) / np.maximum(np.einsum('ij,ij->i', ab, ab), 1e-300), 0, 1)
        return np.min(np.linalg.norm(x - (a + t[:, None] * ab), axis=1))
    def ze_slack(x, k):
        s = (M.te[k] - dist_poly(x, Gold[k]) - Gerr[k]) / M.te[k]   # polyline distance can exceed the true one by <= err
        for v in M.ev[k]:
            s = max(s, (M.tv[v] - np.linalg.norm(x - M.p[v])) / M.tv[v])
        return s
    b2 = math.inf
    Nsm = [L.edge_samples(N, i) for i in range(len(N.E))]
    for i in range(len(N.E)):
        for x in Nsm[i]["G"]:
            b2 = min(b2, ze_slack(x, emap[i]))
    # B3: walk inward from boundary samples of each new face
    b3, walked, unreached = math.inf, 0, []
    for fi, f in enumerate(N.F):
        of = M.F[fmap[fi]]
        es_old = sorted(M.fe[fmap[fi]]); vs_old = sorted(M.fv[fmap[fi]])
        S = BRepAdaptor_Surface(f)
        ex = TopExp_Explorer(f, L.TopAbs_EDGE)
        while ex.More():
            oe = TopoDS.Edge(ex.Current()); ex.Next()
            if BRep_Tool.Degenerated_s(oe):
                continue
            pc = BRepAdaptor_Curve2d(oe, f)
            t0, t1 = pc.FirstParameter(), pc.LastParameter()
            # interior samples only: at a corner the inward direction of one edge runs along the next edge
            for t in t0 + (t1 - t0) * np.linspace(0.005, 0.995, 80):
                uv, duv = gp_Pnt2d(), gp_Vec2d(); pc.D1(t, uv, duv)
                nuv = np.array([-duv.Y(), duv.X()]); nuv /= max(np.linalg.norm(nuv), 1e-300)
                q = gp_Pnt2d(uv.X() + 1e-6 * nuv[0], uv.Y() + 1e-6 * nuv[1])
                if BRepClass_FaceClassifier(f, q, 1e-9).State() != TopAbs_IN:
                    nuv = -nuv
                # 3D length per unit uv step along nuv
                P, Su, Sv = gp_Pnt(), gp_Vec(), gp_Vec(); S.D1(uv.X(), uv.Y(), P, Su, Sv)
                speed = np.linalg.norm(nuv[0] * L.V(Su) + nuv[1] * L.V(Sv))
                hmax = 3 * max(M.te[k] for k in es_old) / max(speed, 1e-300)
                for s in np.linspace(0, hmax, 60):
                    x = L.V(S.Value(uv.X() + s * nuv[0], uv.Y() + s * nuv[1]))
                    walked += 1
                    if in_patch(of, x):
                        break       # reached the original patch: the rest of the walk is inside Z(f)
                    sl = max([ze_slack(x, k) for k in es_old] + [(M.tv[v] - np.linalg.norm(x - M.p[v])) / M.tv[v] for v in vs_old])
                    b3 = min(b3, sl)
                else:
                    unreached.append((fi, float(t)))
                    b3 = min(b3, -math.inf)   # never reached the original patch within the walk
    # B4
    b4 = BRepCheck_Analyzer(new).IsValid() and BRepAlgoAPI_Check(new, True, True).IsValid()
    # T: transversality along new edges
    tmin = math.pi
    for i in range(len(N.E)):
        sides = Nsm[i]["sides"]
        if len(sides) == 2 and sides[0]["face"] != sides[1]["face"]:
            for a, b in list(zip(sides[0]["u"], sides[1]["u"]))[2:-2]:     # interior samples
                phi = math.acos(np.clip(a @ b, -1, 1))
                tmin = min(tmin, phi, math.pi - phi)    # 0 for tangent continuation and for a fold
    res.update(B1_margin=b1, B2_margin=b2, B3_margin=b3, B4=bool(b4), transversality_min_deg=math.degrees(tmin), walked=walked,
               unreached=unreached[:10], n_unreached=len(unreached))
    for k, ok in (("B1", b1 > 0), ("B2", b2 > 0), ("B3", b3 > 0), ("B4", b4), ("T", tmin > 1e-6)):
        if not ok:
            res["fails"].append(k)
    res["ok"] = not res["fails"]
    if verbose:
        print(f"== {name}: curved re-intersection {'PASS' if res['ok'] else 'FAIL ' + ','.join(res['fails'])}"
              f"  margins: vertex {b1:.3f}, edge {b2:.3f}, face strip {b3:.3f}; valid {b4}; "
              f"min crease angle {math.degrees(tmin):.1f} deg; volume ratio {res['vol_ratio']:.5f}")
    return res


if __name__ == "__main__":
    import lemma0_check_run as R
    names = sys.argv[1:] or ["sloppy cylinder g=0.01", "sloppy box g=0.01", "sloppy wedge 30deg g=0.01", "cylinder", "box"]
    out = [check(R.PARTS[n](), n) for n in names]
    json.dump(out, open("../results/reintersect_curved_result.json", "w"), indent=1, default=float)
