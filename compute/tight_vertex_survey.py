"""P2 phase 1: survey of vertices of sewn models, especially models with tangent (G1) edges.

For each model (exact part -> faces moved by up to g -> BRepBuilderAPI_Sewing at 4g) and each vertex v we record:
  tau_v, and for each incident edge e: tau_e, dev_e (max over sides and samples of |beta_{f,e}(t) - gamma_e(t)|),
  the type of e at v (sharp or tangent: angle between the inward tangents of its two faces at the end sample),
  the distance from p_v to the end gamma_e(end) and to the patch corners beta_{f,e}(end);
  for each pair of incident edges, the angle theta between their directions at v.
Derived quantities (all lengths divided by tau_v):
  corner   = max distance from p_v to a patch corner or edge-curve end at v;
  sep      = max over pairs of (dev_e + dev_e') / sin(min(theta, 90 deg)): beyond this distance from p_v, normal
             disks of radius just above dev around the two edge curves no longer meet (straight-line model);
  need     = max(corner, sep): the fan/cone construction needs a ball radius r_v with need < r_v/tau_v < 1.
  in_tubes = for each patch corner c at v, whether c lies in Z(e) for both edges e of its face at v; and the largest
             ratio |c - gamma_e(end)| / tau_e, i.e. how deep the corner sits in the edge tubes.
Sampled, double precision. Writes ../results/tight_vertex_survey.json.
"""
import sys, json, math
import numpy as np
sys.path.insert(0, ".")
import wfs_cert as W, wfs_cert2 as C
import lemma0_check as L
from lemma0_check_run import sloppy, fil_L
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet, BRepFilletAPI_MakeChamfer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCP.GC import GC_MakeArcOfCircle
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt, gp_Vec


def edges_of(s):
    out, ex = [], TopExp_Explorer(s, TopAbs_EDGE)
    while ex.More():
        out.append(TopoDS.Edge(ex.Current())); ex.Next()
    return out


def fillet_some(s, r, pick):
    mk = BRepFilletAPI_MakeFillet(s)
    for e in edges_of(s):
        c = BRepAdaptor_Curve(e)
        p0, p1 = L.V(c.Value(c.FirstParameter())), L.V(c.Value(c.LastParameter()))
        if pick(p0, p1):
            mk.Add(r, e)
    return mk.Shape()


def chamfer_box(a, d):
    s = W.box(a); mk = BRepFilletAPI_MakeChamfer(s)
    for e in edges_of(s):
        mk.Add(d, e)
    return mk.Shape()


def stadium(L_, R, H):
    """Prism over a stadium (two half-circles joined by segments): all side edges are tangent."""
    p = [gp_Pnt(0, -R, 0), gp_Pnt(L_, -R, 0), gp_Pnt(L_, R, 0), gp_Pnt(0, R, 0)]
    a1 = GC_MakeArcOfCircle(p[1], gp_Pnt(L_ + R, 0, 0), p[2]).Value()
    a2 = GC_MakeArcOfCircle(p[3], gp_Pnt(-R, 0, 0), p[0]).Value()
    w = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(p[0], p[1]).Edge(), BRepBuilderAPI_MakeEdge(a1).Edge(),
                                BRepBuilderAPI_MakeEdge(p[2], p[3]).Edge(), BRepBuilderAPI_MakeEdge(a2).Edge()).Wire()
    return BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(w).Face(), gp_Vec(0, 0, H)).Shape()


def cyl_top_fillet(R, H, r):
    return fillet_some(W.cyl(R, H), r, lambda p0, p1: p0[2] > H - 1e-6 and p1[2] > H - 1e-6)


PARTS = {
    "box (control)": lambda: W.box(10),
    "chamfered box d1": lambda: chamfer_box(10, 1.0),
    "filleted box r2": lambda: W.filleted_box(10, 2),
    "filleted box r0.5": lambda: W.filleted_box(10, 0.5),
    "box, one edge filleted r2": lambda: fillet_some(W.box(10), 2, lambda p0, p1: p0[2] < 1e-6 and p1[2] < 1e-6 and p0[1] < 1e-6 and p1[1] < 1e-6),
    "box, top edges filleted r2": lambda: fillet_some(W.box(10), 2, lambda p0, p1: p0[2] > 10 - 1e-6 and p1[2] > 10 - 1e-6),
    "L inner fillet 0.2": lambda: C.lshape_inner_fillet(0.2),
    "L all fillets 0.5": lambda: fil_L(0.5),
    "stadium prism": lambda: stadium(6, 2, 3),
    "cylinder, top fillet r1": lambda: cyl_top_fillet(3, 10, 1),
}
GAPS = [0.001, 0.01]


def survey(shape):
    M = L.Model(shape)
    nv = len(M.Vx)
    inc = [[] for _ in range(nv)]
    for ei, (a, b) in enumerate(M.ev):
        if a >= 0: inc[a].append((ei, 0))
        if b >= 0 and b != a: inc[b].append((ei, 1))
    # per-edge data
    E = {}
    for ei in range(len(M.E)):
        c = BRepAdaptor_Curve(M.E[ei])
        a, b = c.FirstParameter(), c.LastParameter()
        dense = L.edge_samples(M, ei, ts=np.linspace(a, b, 120))
        dev = max(float(s["dev"].max()) for s in dense["sides"]) if dense["sides"] else 0.0
        ends = L.edge_samples(M, ei, ts=np.array([a, a + 1e-4 * (b - a), b - 1e-4 * (b - a), b]))
        E[ei] = dict(dev=dev, ends=ends)
    out = []
    for vi in range(nv):
        if not inc[vi]:
            continue
        pv, tv = M.p[vi], M.tv[vi]
        rec = dict(tau_v=tv, max_tau_e=max(M.te[ei] for ei, _ in inc[vi]), edges=[], corners=[])
        dirs = []
        for ei, end in inc[vi]:
            en = E[ei]["ends"]
            k = 0 if end == 0 else 3          # end sample index
            kk = 1 if end == 0 else 2         # just inside
            g_end = en["G"][k]
            d = en["G"][kk] - en["G"][k]; d /= np.linalg.norm(d)
            dirs.append((ei, d))
            sides = en["sides"]
            if len(sides) == 2:
                u0, u1 = sides[0]["u"][kk], sides[1]["u"][kk]
                ang = math.degrees(math.acos(max(-1, min(1, float(u0 @ u1)))))
                kind = "tangent" if ang > 175 else "sharp"
            else:
                ang, kind = None, "seam/other"
            rec["edges"].append(dict(edge=ei, tau_e=M.te[ei], dev=E[ei]["dev"], kind=kind, inward_angle=ang,
                                     gamma_end=float(np.linalg.norm(g_end - pv)) / tv))
            for s in sides:
                cpt = s["B"][k]
                rec["corners"].append(dict(face=s["face"], edge=ei, dist=float(np.linalg.norm(cpt - pv)) / tv,
                                           depth_in_tube=float(np.linalg.norm(cpt - g_end)) / M.te[ei], pt=cpt))
        # corners: group by face, check membership in both edge tubes of that face at v
        byface = {}
        for c in rec["corners"]:
            byface.setdefault(c["face"], []).append(c)
        tube_ok = []
        for f, cs in byface.items():
            for c in cs:
                inside = []
                for ei, end in inc[vi]:
                    if ei not in M.fe[f]:
                        continue
                    en = E[ei]["ends"]; g_end = en["G"][0 if end == 0 else 3]
                    inside.append(float(np.linalg.norm(c["pt"] - g_end)) / M.te[ei])
                tube_ok.append(max(inside) if inside else None)
        for c in rec["corners"]:
            c.pop("pt")
        sep = 0.0
        for i in range(len(dirs)):
            for j in range(i + 1, len(dirs)):
                th = math.acos(max(-1, min(1, float(dirs[i][1] @ dirs[j][1]))))
                s = math.sin(min(th, math.pi / 2))
                dsum = E[dirs[i][0]]["dev"] + E[dirs[j][0]]["dev"]
                sep = max(sep, dsum / max(s, 1e-9) / tv)
        kinds = sorted(set(e["kind"] for e in rec["edges"]))
        corner = max([c["dist"] for c in rec["corners"]] + [e["gamma_end"] for e in rec["edges"]])
        rec.update(kind="+".join(kinds), corner=corner, sep=sep, need=max(corner, sep),
                   corner_tube_depth=max([t for t in tube_ok if t is not None], default=None))
        out.append(rec)
    return M, out


def main():
    res = {}
    for name, mk in PARTS.items():
        for g in GAPS:
            key = f"{name}, g={g}"
            try:
                shape = sloppy(mk(), g)
                M, recs = survey(shape)
            except Exception as ex:
                res[key] = dict(error=repr(ex)); print(key, "ERROR", ex, flush=True); continue
            need = [r["need"] for r in recs]
            byk = {}
            for r in recs:
                byk.setdefault(r["kind"], []).append(r)
            summ = {k: dict(n=len(v), need_max=max(x["need"] for x in v), corner_max=max(x["corner"] for x in v),
                            sep_max=max(x["sep"] for x in v),
                            fan_feasible=sum(1 for x in v if x["need"] < 1),
                            tauv_over_maxtaue=max(x["tau_v"] / x["max_tau_e"] for x in v),
                            corner_tube_depth_max=max((x["corner_tube_depth"] or 0) for x in v)) for k, v in byk.items()}
            res[key] = dict(n_vertices=len(recs), n_faces=len(M.F), n_edges=len(M.E), by_kind=summ, vertices=recs)
            print(key, json.dumps(summ), flush=True)
    json.dump(res, open("../results/tight_vertex_survey.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
