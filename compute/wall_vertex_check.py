"""P2 step 4: vertices and global separation for the "wall + chord" construction.

Edges use the first wall (in the order gamma, mid, chord) that passed W1-W5 on the whole edge interval in
compute/wall_chord_check.py and whose bridges enter both vertex balls; if none enters both balls, the first passing
wall is used and the vertex test reports the incomplete bridge arc. Edges where no wall passed are re-trimmed edges (step 3); their vertices are reported as
"needs re-trimmed edge" and not tested here. Seam edges are not covered (as in v3).

Per model (sewn as in P1), ball radius r_v = rho tau_v, rho = 0.95:
  Wall data. For each edge e and t on a grid (dense near both ends), the wall line in Pi(t) (centre c(t), unit normal
    m(t)), the cut points a_f(t), a_g(t) and so the bridge [a_f(t), a_g(t)] (functions of wall_chord_check).
  Vertices.
    V0  as in checker v3 (read from results/strip_cone_check3.json: corners inside the ball, balls disjoint, the ball
        misses non-incident patches and edge tubes); plus: every incident edge interval reaches the ball (step 3).
    V1  the loop lambda_v on S_v:
        face arcs: points of P_f ∩ S_v (quadtree, as in v2/v3), minus the points that lie, inside the tube of radius
          rho_e of an incident edge e of f, on the wrong side of the wall of e (side measured in the normal plane of
          gamma_e through the point, wall data interpolated in t);
        bridge arcs: for lambda in [0,1] (21 values) the first point, going out from v, where
          (1-lambda) a_f(t) + lambda a_g(t) leaves the ball (linear interpolation on the grid);
        tests: each face arc is one cluster (link r/6); its two ends lie within 3r/20 of bridge-arc ends; the
          bridge-arc end at lambda = 0 (1) lies within 3r/20 of the arc of f (g) (the arc is sampled at spacing ~r/20); the pieces are pairwise apart
          (gap > 0.005 r) outside 3r/20-neighbourhoods of the joints.
  Global (S1 for the cut patches).
    face-face: the patches minus the balls (BRepAlgoAPI_Cut) are pairwise apart, except that adjacent patches may meet
      inside the tube of radius rho_e of a common edge (where the walls separate them, step 3): every closest-point
      solution of distance < 1e-9 must lie in such a tube.
    bridges: the bridges of an edge (segments on the grid, outside the balls) are apart from the bridges of every
      other edge and from every patch not incident to the edge.
Sampled, double precision. One model per call: python3 wall_vertex_check.py <index>; with no index, merge the parts
into ../results/wall_vertex_check.json.
"""
import sys, os, json, math, glob
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from lemma0_check_run import sloppy
from tight_vertex_survey import PARTS, GAPS
from patchface import patch_face
from strip_cone_check2 import face_band, clusters
from wall_chord_check import section_chains, walk_from, point_at_arclength, cut, WALLS
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.TopoDS import TopoDS_Compound
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir, gp_Vec

RHO = 0.95
OUT = "../results/wall_vertex_parts"


def P(x): return gp_Pnt(*map(float, x))


def compound(shapes):
    c = TopoDS_Compound(); b = BRep_Builder(); b.MakeCompound(c)
    for s in shapes: b.Add(c, s)
    return c


class WallEdge:
    """Wall data of one edge on a parameter grid."""

    def __init__(self, M, PF, ei, wall):
        self.M, self.ei, self.wall = M, ei, wall
        self.c = BRepAdaptor_Curve(M.E[ei]); self.a0, self.b0 = self.c.FirstParameter(), self.c.LastParameter()
        (self.f, _), (self.g, _) = M.uses[ei]
        self.te = M.te[ei]
        sm = L.edge_samples(M, ei, ts=np.linspace(self.a0, self.b0, 200)); self.reach = L.edge_reach(sm)
        self.rho_e = 0.999 * min(self.te, self.reach)
        self.beta = []
        for fi, oe in M.uses[ei]:
            pc = BRepAdaptor_Curve2d(oe, M.F[fi]); S = BRepAdaptor_Surface(M.F[fi])
            self.beta.append(np.array([L.V(S.Value(pc.Value(x).X(), pc.Value(x).Y()))
                                       for x in np.linspace(self.a0, self.b0, 4000)]))
        Lp = self.b0 - self.a0
        geo = np.geomspace(1e-6, 0.05, 60) * Lp
        self.ts = np.unique(np.concatenate([self.a0 + geo, np.linspace(self.a0, self.b0, 60), self.b0 - geo]))
        self.rows = [self.at(t, PF) for t in self.ts]

    def dist_poly(self, x, B):
        A, D = B[:-1], B[1:] - B[:-1]
        u = np.clip(np.einsum("ij,ij->i", x - A, D) / np.maximum(np.einsum("ij,ij->i", D, D), 1e-300), 0, 1)
        return float(np.min(np.linalg.norm(A + u[:, None] * D - x, axis=1)))

    def at(self, t, PF):
        p, d = gp_Pnt(), gp_Vec(); self.c.D1(t, p, d); gpt, T = L.V(p), L.V(d) / d.Magnitude()
        pln = gp_Pln(gp_Pnt(*gpt), gp_Dir(*T))
        e1 = np.cross(T, [1, 0, 0])
        if np.linalg.norm(e1) < 0.3: e1 = np.cross(T, [0, 1, 0])
        e1 /= np.linalg.norm(e1); e2 = np.cross(T, e1)
        to2 = lambda X: np.stack([(X - gpt) @ e1, (X - gpt) @ e2], axis=-1)
        to3 = lambda x: gpt + x[0] * e1 + x[1] * e2
        sides = []
        for si, fi in enumerate((self.f, self.g)):
            ch = section_chains(PF[fi], pln, gpt, 3 * self.te)
            ends = [(np.linalg.norm(C[k] - gpt), j, k) for j, C in enumerate(ch) for k in (0, -1)
                    if self.dist_poly(C[k], self.beta[si]) < 0.05 * self.te]
            if not ends: return dict(t=t, gpt=gpt, ok=False)
            best = min(ends); sides.append(to2(walk_from(ch[best[1]], best[2])))
        Pf, Pg = sides
        bf, bg = Pf[0], Pg[0]
        df = point_at_arclength(Pf, 0.3 * self.te) - bf; dg = point_at_arclength(Pg, 0.3 * self.te) - bg
        df /= np.linalg.norm(df); dg /= np.linalg.norm(dg)
        if self.wall == "chord":
            w = bg - bf
            if np.linalg.norm(w) < 1e-12 * self.te: return dict(t=t, gpt=gpt, ok=False)
            w /= np.linalg.norm(w); m = np.array([-w[1], w[0]])
            if m @ (df - dg) < 0: m = -m
            cc = 0.5 * (bf + bg)
        else:
            m = df - dg
            if np.linalg.norm(m) < 1e-9: return dict(t=t, gpt=gpt, ok=False)
            m /= np.linalg.norm(m)
            cc = np.zeros(2) if self.wall == "gamma" else 0.5 * (bf + bg)
        af = cut(Pf, cc, m, +1)[0]; ag = cut(Pg, cc, m, -1)[0]
        if af is None or ag is None: return dict(t=t, gpt=gpt, ok=False)
        return dict(t=t, gpt=gpt, T=T, ok=True, c3=to3(cc), m3=m[0] * e1 + m[1] * e2, af=to3(af), ag=to3(ag))

    def wall_side(self, x, which):
        """Signed side of x w.r.t. the wall (positive = the side kept by face `which` (0 = f, 1 = g)), or None if x is
        not in the tube of radius rho_e. Wall data interpolated linearly in t."""
        # nearest grid sample, then refine t by one Newton step on <x - gamma(t), T(t)> = 0
        G = np.array([r["gpt"] for r in self.rows])
        i = int(np.argmin(np.linalg.norm(G - x, axis=1)))
        t = self.ts[i]
        for _ in range(3):
            p, d, dd = gp_Pnt(), gp_Vec(), gp_Vec(); self.c.D2(t, p, d, dd)
            g0, g1, g2 = L.V(p), L.V(d), L.V(dd)
            fval = (x - g0) @ g1; fder = -(g1 @ g1) + (x - g0) @ g2
            if fder == 0: break
            t = min(max(t - fval / fder, self.a0), self.b0)
        p = gp_Pnt(); self.c.D0(t, p); g0 = L.V(p)
        if np.linalg.norm(x - g0) >= self.rho_e: return None
        j = int(np.searchsorted(self.ts, t)); j0, j1 = max(j - 1, 0), min(j, len(self.ts) - 1)
        r0, r1 = self.rows[j0], self.rows[j1]
        if not (r0["ok"] and r1["ok"]):
            rr = r0 if r0["ok"] else (r1 if r1["ok"] else None)
            if rr is None: return float("nan")
            c3, m3 = rr["c3"] - rr["gpt"] + g0, rr["m3"]
        else:
            s = 0.0 if j1 == j0 else (t - self.ts[j0]) / (self.ts[j1] - self.ts[j0])
            c3 = (1 - s) * (r0["c3"] - r0["gpt"]) + s * (r1["c3"] - r1["gpt"]) + g0
            m3 = (1 - s) * r0["m3"] + s * r1["m3"]
            T = (1 - s) * r0["T"] + s * r1["T"]; T /= np.linalg.norm(T)
            m3 = m3 - (m3 @ T) * T; m3 /= np.linalg.norm(m3)
        h = float((x - c3) @ m3)
        return h if which == 0 else -h

    def bridge_arc(self, v, pv, r):
        """Points where (1-lam) a_f + lam a_g first leaves B(pv, r), going out from vertex v."""
        rows = self.rows if self.M.ev[self.ei][0] == v else self.rows[::-1]
        arc = []
        for lam in np.linspace(0, 1, 21):
            prev = None
            for rw in rows:
                if not rw["ok"]: prev = None; continue
                X = (1 - lam) * rw["af"] + lam * rw["ag"]; dcur = np.linalg.norm(X - pv) - r
                if prev is not None and prev[1] < 0 <= dcur:
                    s = prev[1] / (prev[1] - dcur); arc.append(prev[0] + s * (X - prev[0])); break
                prev = (X, dcur)
        return np.array(arc)

    def bridges_outside(self, balls_c, balls_r):
        segs = []
        for rw in self.rows:
            if not rw["ok"]: continue
            if any(np.linalg.norm(rw["af"] - c) < r and np.linalg.norm(rw["ag"] - c) < r for c, r in zip(balls_c, balls_r)):
                continue
            if np.linalg.norm(rw["af"] - rw["ag"]) > 1e-12:
                segs.append(BRepBuilderAPI_MakeEdge(P(rw["af"]), P(rw["ag"])).Edge())
        return compound(segs) if segs else None


def dist(a, b):
    d = BRepExtrema_DistShapeShape(a, b)
    return (d.Value(), [L.V(d.PointOnShape1(k)) for k in range(1, d.NbSolution() + 1)]) if d.IsDone() else (float("nan"), [])


def run(index):
    name, gap = [(n, g) for n in PARTS for g in GAPS][index]
    key = f"{name}, g={gap}"
    M = L.Model(sloppy(PARTS[name](), gap))
    PF = [patch_face(fc) for fc in M.F]
    PF = [p if p is not None else fc for p, fc in zip(PF, M.F)]
    nv = len(M.Vx)
    rv = [RHO * M.tv[v] for v in range(nv)]
    edge_res = json.load(open(f"../results/wall_chord_parts/{index:02d}.json"))["edges"]
    v3 = json.load(open("../results/strip_cone_check3.json"))[key]["vertices"]
    WE, kind = {}, {}
    for ei in range(len(M.E)):
        e = edge_res[str(ei)]
        if "gamma" not in e: kind[ei] = "seam"; continue
        ok = [w for w in WALLS if e[w]["ok"]]
        if not ok: kind[ei] = "re-trimmed"; continue
        # first wall that passed the edge test and whose bridges enter both vertex balls (V0)
        first = None
        for w in ok:
            we = WallEdge(M, PF, ei, w); first = first or we
            if all(len(we.bridge_arc(x, M.p[x], rv[x])) == 21 for x in set(M.ev[ei])):
                break
        else:
            we = first
        kind[ei] = we.wall; WE[ei] = we
    inc = [[] for _ in range(nv)]
    for ei, (a, b) in enumerate(M.ev):
        inc[a].append(ei)
        if b != a: inc[b].append(ei)
    out = dict(key=key, rho=RHO, edge_wall=kind, vertices={}, global_={})
    for v in range(nv):
        pv, r = M.p[v], rv[v]
        rec = {k: v3[str(v)][k] for k in ("V0_corners_inside", "V0_ball_disjoint", "V0_miss_faces_over_r", "V0_miss_strips_over_r")}
        rec["V0_edges_reach_ball"] = all(edge_res[str(ei)].get(kind[ei], {}).get("ends_reach_balls", False)
                                         for ei in inc[v] if ei in WE)
        bad = [ei for ei in inc[v] if kind[ei] in ("seam", "re-trimmed")]
        if bad:
            rec["status"] = "not tested: " + ", ".join(f"edge {ei} {kind[ei]}" for ei in bad)
            rec["ok"] = None; out["vertices"][v] = rec; continue
        note = None
        faces = sorted({fi for ei in inc[v] for fi, _ in M.uses[ei]})
        arcs = {}
        for fi in faces:
            S = BRepAdaptor_Surface(M.F[fi]); sph, _ = face_band(M, S, fi, pv, r, 1.2 * r)
            sph = np.array(sph)
            if len(sph) > 1500: sph = sph[:: int(math.ceil(len(sph) / 1500))]
            keep = np.ones(len(sph), bool)
            for ei in inc[v]:
                fs = [x for x, _ in M.uses[ei]]
                if fi not in fs: continue
                which = fs.index(fi)
                for k, x in enumerate(sph):
                    h = WE[ei].wall_side(x, which)
                    if h is not None and not math.isnan(h) and h < -1e-9 * r: keep[k] = False   # nan: no wall data there (vertex region)
            arcs[fi] = sph[keep]
        pieces, joints = [], []
        for ei in inc[v]:
            A = WE[ei].bridge_arc(v, pv, r)
            if len(A) < 21: note = note or f"edge {ei}: bridge arc incomplete ({len(A)}/21)"
            if len(A) < 2: continue
            pieces.append(("bridge", ei, A)); joints += [A[0], A[-1]]
            for end, fi in ((A[0], WE[ei].f), (A[-1], WE[ei].g)):
                if len(arcs.get(fi, [])) == 0 or np.min(np.linalg.norm(arcs[fi] - end, axis=1)) > 3 * r / 20:
                    note = note or f"edge {ei}: bridge end not on the arc of face {fi}"
        for fi, A in arcs.items():
            if len(A) == 0: note = note or f"face {fi}: no arc"; continue
            _, k = clusters(A, r / 6)
            if k != 1: note = note or f"face {fi}: {k} arcs"
            pieces.append(("face", fi, A))
            Dm = np.linalg.norm(A[:, None] - A[None], axis=2); i, j = np.unravel_index(np.argmax(Dm), Dm.shape)
            for e in (A[i], A[j]):
                if min([np.linalg.norm(e - q) for q in joints] + [np.inf]) > 3 * r / 20:
                    note = note or f"face {fi}: arc end not at a joint"
        md = float("inf")
        for i in range(len(pieces)):
            for j in range(i + 1, len(pieces)):
                A, B = pieces[i][2], pieces[j][2]
                Dm = np.linalg.norm(A[:, None] - B[None], axis=2)
                for q in joints:
                    Dm = np.where((np.linalg.norm(A - q, axis=1)[:, None] < 3 * r / 20) |
                                  (np.linalg.norm(B - q, axis=1)[None, :] < 3 * r / 20), np.inf, Dm)
                md = min(md, float(Dm.min()))
        rec["V1_min_gap_over_r"] = md / r
        rec["V1_note"] = note
        rec["V1_ok"] = note is None and md / r > 0.005
        rec["ok"] = bool(rec["V0_corners_inside"] and rec["V0_ball_disjoint"] and rec["V0_miss_faces_over_r"] > 1
                         and rec["V0_miss_strips_over_r"] > 1 and rec["V0_edges_reach_ball"] and rec["V1_ok"])
        out["vertices"][v] = rec
    # ---------------- global ----------------
    balls = [BRepPrimAPI_MakeSphere(P(M.p[v]), rv[v]).Shape() for v in range(nv)]
    cutF = []
    for fi in range(len(M.F)):
        sh = PF[fi]
        for b in balls: sh = BRepAlgoAPI_Cut(sh, b).Shape()
        cutF.append(sh)
    shared = {}
    for ei in range(len(M.E)):
        if kind[ei] in WALLS:
            shared.setdefault(tuple(sorted((WE[ei].f, WE[ei].g))), []).append(ei)
    ff, ff_bad = float("inf"), []
    for i in range(len(M.F)):
        for j in range(i + 1, len(M.F)):
            d, sols = dist(cutF[i], cutF[j])
            if d < 1e-9 and (i, j) in shared:
                outside = [x for x in sols if all(WE[ei].wall_side(x, 0) is None for ei in shared[(i, j)])]
                if outside: ff_bad.append((i, j)); ff = min(ff, 0.0)
            elif d < 1e-9 and any(kind[ei] == "re-trimmed" and {M.uses[ei][0][0], M.uses[ei][1][0]} == {i, j}
                                  for ei in range(len(M.E))):
                pass   # along a re-trimmed edge (not covered here)
            else:
                ff = min(ff, d)
                if d < 1e-9: ff_bad.append((i, j))
    br = {ei: WE[ei].bridges_outside([M.p[v] for v in range(nv)], rv) for ei in WE}
    br = {k: s for k, s in br.items() if s is not None}
    bb, bf = float("inf"), float("inf")
    ks = list(br)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            bb = min(bb, dist(br[ks[i]], br[ks[j]])[0])
    for ei, s in br.items():
        for fi in range(len(M.F)):
            if fi not in (WE[ei].f, WE[ei].g): bf = min(bf, dist(s, cutF[fi])[0])
    out["global_"] = dict(face_face_min=ff, face_face_bad_pairs=ff_bad, bridge_bridge_min=bb, bridge_face_min=bf)
    vs = list(out["vertices"].values())
    out["summary"] = dict(vertices_ok=sum(1 for x in vs if x["ok"]), vertices_tested=sum(1 for x in vs if x["ok"] is not None),
                          vertices=nv, global_ok=bool(not ff_bad and bb > 0 and bf > 0))
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/{index:02d}.json", "w"), indent=1, default=float)
    print(key, json.dumps(out["summary"]), json.dumps(out["global_"], default=float),
          {v: x["V1_note"] for v, x in out["vertices"].items() if x["ok"] is False}, flush=True)


def main():
    res = {}
    for fn in sorted(glob.glob(f"{OUT}/*.json")):
        d = json.load(open(fn)); res[d["key"]] = d
    json.dump(res, open("../results/wall_vertex_check.json", "w"), indent=1, default=float)
    for k, d in res.items(): print(k, d["summary"])


if __name__ == "__main__":
    if len(sys.argv) > 1: run(int(sys.argv[1]))
    else: main()
