"""P2 step 2: what happens at tangent edges whose patches meet.

For each edge of a sewn model whose two rebuilt patches meet (distance 0), and for t on a grid along the edge, cut both
patches with the normal plane Pi(t) (BRepAlgoAPI_Section) and look at the two section curves inside the disk of radius
3 tau_e around gamma(t). Records: how many intersection points the two sections have there, their distance to gamma(t)
(over tau_e), the angle between the sections at the intersection (crossing vs tangency), and the boundary points
b*_f, b*_g (where each section ends). Sampled, double precision. Writes ../results/tangent_contact.json.
"""
import sys, json, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from lemma0_check_run import sloppy
from tight_vertex_survey import PARTS
from patchface import patch_face
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir, gp_Vec


def section_polyline(face, pln):
    sec = BRepAlgoAPI_Section(face, pln, False); sec.ComputePCurveOn1(False); sec.Build()
    out = []
    ex = TopExp_Explorer(sec.Shape(), TopAbs_EDGE)
    while ex.More():
        c = BRepAdaptor_Curve(TopoDS.Edge(ex.Current()))
        out.append(np.array([L.V(c.Value(u)) for u in np.linspace(c.FirstParameter(), c.LastParameter(), 400)]))
        ex.Next()
    return out


def seg_inter(p, q, a, b):
    """Intersection of 2D segments pq and ab (in plane coords); returns (point, angle) or None."""
    d1, d2 = q - p, b - a
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-300: return None
    w = a - p
    s = (w[0] * d2[1] - w[1] * d2[0]) / den; u = (w[0] * d1[1] - w[1] * d1[0]) / den
    if 0 <= s <= 1 and 0 <= u <= 1:
        ang = math.degrees(math.asin(min(1, abs(den) / (np.linalg.norm(d1) * np.linalg.norm(d2)))))
        return p + s * d1, ang
    return None


def analyze(name, g, edges=None, nt=60):
    M = L.Model(sloppy(PARTS[name](), g))
    PF = [patch_face(f) for f in M.F]
    res = {}
    for ei in range(len(M.E)):
        if len(M.uses[ei]) != 2: continue
        (f, _), (h, _) = M.uses[ei]
        if f == h or PF[f] is None or PF[h] is None: continue
        if edges is not None and ei not in edges: continue
        if BRepExtrema_DistShapeShape(PF[f], PF[h]).Value() > 1e-9: continue
        c = BRepAdaptor_Curve(M.E[ei]); a, b = c.FirstParameter(), c.LastParameter()
        rows = []
        for t in np.linspace(a, b, nt + 2)[1:-1]:
            p, d = gp_Pnt(), gp_Vec(); c.D1(t, p, d); gpt, T = L.V(p), L.V(d) / d.Magnitude()
            if min(np.linalg.norm(gpt - q) for q in M.p) < 3 * max(M.tv):  # skip near vertices
                continue
            pln = gp_Pln(gp_Pnt(*gpt), gp_Dir(*T))
            e1 = np.cross(T, [1, 0, 0]);
            if np.linalg.norm(e1) < 0.1: e1 = np.cross(T, [0, 1, 0])
            e1 /= np.linalg.norm(e1); e2 = np.cross(T, e1)
            R = 3 * M.te[ei]
            def loc(P):
                P = P[np.linalg.norm(P - gpt, axis=1) < R]
                return np.stack([(P - gpt) @ e1, (P - gpt) @ e2], axis=1) if len(P) else np.zeros((0, 2))
            A = [loc(P) for P in section_polyline(PF[f], pln)]; B = [loc(P) for P in section_polyline(PF[h], pln)]
            hits = []
            for Pa in A:
                for Pb in B:
                    for i in range(len(Pa) - 1):
                        for j in range(len(Pb) - 1):
                            r = seg_inter(Pa[i], Pa[i + 1], Pb[j], Pb[j + 1])
                            if r: hits.append((float(np.linalg.norm(r[0]) / M.te[ei]), r[1]))
            rows.append(dict(t=float(t), n_hits=len(hits), hits=hits[:4],
                             minsep=float(min([np.min(np.linalg.norm(Pa[:, None] - Pb[None], axis=2)) for Pa in A for Pb in B if len(Pa) and len(Pb)] + [np.inf]) / M.te[ei])))
        res[ei] = dict(tau_e=M.te[ei], rows=rows,
                       frac_t_with_contact=float(np.mean([r["n_hits"] > 0 for r in rows])) if rows else None,
                       max_angle_deg=max([h[1] for r in rows for h in r["hits"]] + [0]),
                       max_dist_over_tau=max([h[0] for r in rows for h in r["hits"]] + [0]))
        print(name, g, "edge", ei, {k: v for k, v in res[ei].items() if k != "rows"}, flush=True)
    return res


if __name__ == "__main__":
    out = {}
    for name, g in [("L all fillets 0.5", 0.001), ("filleted box r0.5", 0.01), ("box, top edges filleted r2", 0.001)]:
        out[f"{name}, g={g}"] = analyze(name, g)
    json.dump(out, open("../results/tangent_contact.json", "w"), indent=1, default=float)
