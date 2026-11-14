"""P2 step 4: vertices and global separation for the "wall + chord" construction.

Edges use the first wall (in the order gamma, mid, chord) that passed W1-W5 on the whole edge interval in
compute/wall_chord_check.py and whose bridges enter both vertex balls; if none enters both balls, the first passing
wall is used and the vertex test reports the incomplete bridge arc. Edges where no wall passed are re-trimmed edges (step 3); their vertices are reported as
"needs re-trimmed edge" and not tested here. Seam edges are not covered (as in v3).

Per model (sewn as in P1), ball radius r_v = rho_v tau_v; per vertex the first rho_v in (0.95, 0.99, 0.999) that
passes is used (any r_v < tau_v is allowed by the construction):
  Wall data. For each edge e and t on a grid (dense near both ends), the wall line in Pi(t) (centre c(t), unit normal
    m(t)), the cut points a_f(t), a_g(t) and so the bridge [a_f(t), a_g(t)] (functions of wall_chord_check).
  Vertices.
    V0  as in checker v3 (read from results/strip_cone_check3.json: corners inside the ball, balls disjoint, the ball
        misses non-incident patches and edge tubes); plus: every incident edge interval reaches the ball (step 3).
    V1  the loop lambda_v on S_v:
        face arcs: points of P_f ∩ S_v (BRepAlgoAPI_Section of the patch with the sphere), minus the points that lie
          on the wrong side of the wall of an incident edge e of f within the removed piece (side measured in the normal
          plane of gamma_e through the point, wall data interpolated in t; "within" = closer to gamma_e than
          max(rho_e, 1.05 x the farthest point of the removed piece of the section in the neighbouring grid planes));
        bridge arcs: for lambda in [0,1] (21 values) the first point, going out from v, where
          (1-lambda) a_f(t) + lambda a_g(t) leaves the ball (linear interpolation on the grid);
        tests: each face arc is one curve (section edges chained after the wall cuts); its two ends lie within r/20 of bridge-arc ends; the
          bridge-arc end at lambda = 0 (1) lies within r/20 of the arc of f (g); the pieces are pairwise apart
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
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Copy
from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Section
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.TopoDS import TopoDS_Compound
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir, gp_Vec

RHO = 0.95
RHOS = (0.95, 0.99, 0.999)   # per-vertex ball ratio: the first that passes is used
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
        af, Kf, _, _ = cut(Pf, cc, m, +1); ag, Kg, _, _ = cut(Pg, cc, m, -1)
        if af is None or ag is None: return dict(t=t, gpt=gpt, ok=False)
        # radius (from gamma) reached by the removed piece of each section (from b to the cut point)
        def reach_removed(Pp, K):
            n = len(Pp) - len(K) + 1
            return float(np.max(np.linalg.norm(Pp[:max(n, 1)], axis=1)))
        return dict(t=t, gpt=gpt, T=T, ok=True, c3=to3(cc), m3=m[0] * e1 + m[1] * e2, af=to3(af), ag=to3(ag),
                    Rrem=(reach_removed(Pf, Kf), reach_removed(Pg, Kg)))

    def limit_at(self, v, pv, r):
        """The edge interval I_e starts (from the end at v) at the last grid plane whose bridge lies inside B(pv, r);
        the wall acts only beyond it. Stores the limiting parameter."""
        idx = range(len(self.rows)) if self.M.ev[self.ei][0] == v else range(len(self.rows) - 1, -1, -1)
        lim = None
        for i in idx:
            rw = self.rows[i]
            if rw["ok"] and not (np.linalg.norm(rw["af"] - pv) < r and np.linalg.norm(rw["ag"] - pv) < r):
                break
            if rw["ok"]: lim = self.ts[i]
        self.lims = getattr(self, "lims", {}); self.lims[v] = (lim, self.M.ev[self.ei][0] == v)

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
        p, d = gp_Pnt(), gp_Vec(); self.c.D1(t, p, d); g0 = L.V(p); T0 = L.V(d) / d.Magnitude()
        if abs(float((x - g0) @ T0)) > 1e-3 * np.linalg.norm(x - g0):
            return None   # x is not in a normal plane of gamma_e (its foot is an end of the curve)
        for lim, at_start in getattr(self, "lims", {}).values():
            if lim is not None and ((at_start and t <= lim) or (not at_start and t >= lim)):
                return None   # plane outside the edge interval I_e (bridge inside the vertex ball): no wall there
        j = int(np.searchsorted(self.ts, t)); j0, j1 = max(j - 1, 0), min(j, len(self.ts) - 1)
        r0, r1 = self.rows[j0], self.rows[j1]
        Rrem = max([rw["Rrem"][which] for rw in (r0, r1) if rw["ok"]] + [0.0])
        if np.linalg.norm(x - g0) >= max(self.rho_e, 1.05 * Rrem): return None
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

    def bridge_arc(self, v, pv, r, PF=None):
        """Points where (1-lam) a_f + lam a_g first leaves B(pv, r), going out from vertex v (linear interpolation
        between grid planes; with PF given, the two ends lam = 0, 1 are refined by bisection in t on exact sections)."""
        order = list(range(len(self.rows))) if self.M.ev[self.ei][0] == v else list(range(len(self.rows) - 1, -1, -1))
        arc = []
        for lam in np.linspace(0, 1, 21):
            prev = None
            for i in order:
                rw = self.rows[i]
                if not rw["ok"]: prev = None; continue
                X = (1 - lam) * rw["af"] + lam * rw["ag"]; dcur = np.linalg.norm(X - pv) - r
                if prev is not None and prev[1] < 0 <= dcur:
                    s = prev[1] / (prev[1] - dcur); Y = prev[0] + s * (X - prev[0])
                    if PF is not None and lam in (0.0, 1.0):
                        t0, t1 = self.ts[prev[2]], self.ts[i]
                        for _ in range(30):
                            tm = 0.5 * (t0 + t1); rm = self.at(tm, PF)
                            if not rm["ok"]: break
                            Xm = (1 - lam) * rm["af"] + lam * rm["ag"]
                            if np.linalg.norm(Xm - pv) < r: t0 = tm
                            else: t1 = tm
                            Y = Xm
                    arc.append(Y); break
                prev = (X, dcur, i)
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
    edge_res = json.load(open(f"../results/wall_chord_parts/{index:02d}.json"))["edges"]
    v3 = json.load(open("../results/strip_cone_check3.json"))[key]["vertices"]
    WE, kind = {}, {}
    for ei in range(len(M.E)):
        e = edge_res[str(ei)]
        if "gamma" not in e: kind[ei] = "seam"; continue
        ok = [w for w in WALLS if e[w]["ok"]]
        if not ok: kind[ei] = "re-trimmed"; continue
        # first wall that passed the edge test and whose bridges enter both vertex balls (V0), smallest ratio first
        cache, we = {}, None
        for rho in RHOS:
            for w in ok:
                if w not in cache: cache[w] = WallEdge(M, PF, ei, w)
                if all(len(cache[w].bridge_arc(x, M.p[x], rho * M.tv[x])) == 21 for x in set(M.ev[ei])):
                    we = cache[w]; break
            if we is not None: break
        if we is None: we = cache[ok[0]]
        kind[ei] = we.wall; WE[ei] = we
    inc = [[] for _ in range(nv)]
    for ei, (a, b) in enumerate(M.ev):
        inc[a].append(ei)
        if b != a: inc[b].append(ei)
    out = dict(key=key, rhos=RHOS, edge_wall=kind, vertices={}, global_={})
    rv_max = [RHOS[-1] * M.tv[v] for v in range(nv)]

    def sphere_arc(fi, pv, r):
        """P_f ∩ S_v as a list of polylines (one per section edge)."""
        # non-destructive: earlier Boolean operations must not change tolerances of the shared patch
        sec = BRepAlgoAPI_Section(PF[fi], BRepPrimAPI_MakeSphere(P(pv), r).Shape(), False)
        sec.SetNonDestructive(True); sec.Build()
        segs = []
        ex = TopExp_Explorer(sec.Shape(), TopAbs_EDGE)
        while ex.More():
            c = BRepAdaptor_Curve(TopoDS.Edge(ex.Current()))
            us = np.linspace(c.FirstParameter(), c.LastParameter(), 2000)
            Q = np.array([L.V(c.Value(u)) for u in us])
            # resample uniformly in arc length (the section curves are not parametrized by arc length)
            sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]
            n = max(int(sl[-1] / (r / 400)), 2)
            ut = np.interp(np.linspace(0, sl[-1], n), sl, us)
            segs.append(np.array([L.V(c.Value(u)) for u in ut]))
            ex.Next()
        return segs

    def chain(runs, tol):
        """Join polylines whose ends coincide; returns the list of chains."""
        runs = [R for R in runs if len(R) >= 2]
        out = []
        while runs:
            cur = runs.pop(); grown = True
            while grown:
                grown = False
                for i, Q in enumerate(runs):
                    if np.linalg.norm(cur[-1] - Q[0]) < tol: cur = np.vstack([cur, Q[1:]])
                    elif np.linalg.norm(cur[-1] - Q[-1]) < tol: cur = np.vstack([cur, Q[::-1][1:]])
                    elif np.linalg.norm(cur[0] - Q[-1]) < tol: cur = np.vstack([Q, cur[1:]])
                    elif np.linalg.norm(cur[0] - Q[0]) < tol: cur = np.vstack([Q[::-1], cur[1:]])
                    else: continue
                    runs.pop(i); grown = True; break
            out.append(cur)
        return out

    def vertex_test(v, rho):
        pv, r = M.p[v], rho * M.tv[v]
        s3 = 0.95 / rho
        rec = dict(rho=rho, V0_corners_inside=v3[str(v)]["V0_corners_inside"],
                   V0_ball_disjoint=all(np.linalg.norm(pv - M.p[w]) > r + rv_max[w] for w in range(nv) if w != v),
                   V0_miss_faces_over_r=v3[str(v)]["V0_miss_faces_over_r"] * s3,
                   V0_miss_strips_over_r=v3[str(v)]["V0_miss_strips_over_r"] * s3)
        note = None
        faces = sorted({fi for ei in inc[v] for fi, _ in M.uses[ei]})
        arcs, chains = {}, {}
        for fi in faces:
            runs = []
            for S in chain(sphere_arc(fi, pv, r), 0.01 * r):   # OCC splits the section; rejoin first
                keep = np.ones(len(S), bool)
                for ei in inc[v]:
                    fs = [x for x, _ in M.uses[ei]]
                    if fi not in fs: continue
                    which = fs.index(fi)
                    for k, x in enumerate(S):
                        h = WE[ei].wall_side(x, which)
                        if h is not None and not math.isnan(h) and h < -1e-9 * r: keep[k] = False   # nan: no wall data
                # split into runs of kept points
                idx = np.nonzero(keep)[0]
                if len(idx):
                    br = np.nonzero(np.diff(idx) > 1)[0]
                    for part in np.split(idx, br + 1): runs.append(S[part])
            chains[fi] = chain(runs, 1e-6 * r + 1e-9)
            arcs[fi] = np.vstack(chains[fi]) if chains[fi] else np.zeros((0, 3))
        pieces, joints = [], []
        for ei in inc[v]:
            A = WE[ei].bridge_arc(v, pv, r, PF)
            if len(A) < 21: note = note or f"edge {ei}: bridge arc incomplete ({len(A)}/21)"
            if len(A) < 2: continue
            pieces.append(("bridge", ei, A)); joints += [A[0], A[-1]]
            for end_, fi in ((A[0], WE[ei].f), (A[-1], WE[ei].g)):
                if len(arcs.get(fi, [])) == 0 or np.min(np.linalg.norm(arcs[fi] - end_, axis=1)) > r / 20:
                    dk = float(np.min(np.linalg.norm(arcs[fi] - end_, axis=1)) / r) if len(arcs.get(fi, [])) else None
                    da = float(min(np.min(np.linalg.norm(S - end_, axis=1)) for S in sphere_arc(fi, pv, r)) / r) \
                        if sphere_arc(fi, pv, r) else None
                    note = note or f"edge {ei}: bridge end not on the arc of face {fi} (to kept arc {dk:.4f} r, to whole section {da:.4f} r)"
        if os.environ.get("WV_DUMP") == str(v):
            np.savez(f"/tmp/wv_dump_{v}_{rho}.npz", **{f"arc{fi}": A for fi, A in arcs.items()},
                     **{f"br{p[1]}": p[2] for p in pieces if p[0] == "bridge"},
                     **{f"sec{fi}": np.vstack(sphere_arc(fi, pv, r)) for fi in arcs},
                     **{f"type{fi}": np.array([str(BRepAdaptor_Surface(PF[fi]).GetType()), str(BRepAdaptor_Surface(M.F[fi]).GetType())]) for fi in arcs},
                     pv=pv, r=r)
        for fi, A in arcs.items():
            if len(A) == 0: note = note or f"face {fi}: no arc"; continue
            if len(chains[fi]) != 1:
                Cs = chains[fi]
                gaps = [min(np.linalg.norm(a - b) for a in (Cs[0][0], Cs[0][-1]) for b in (C[0], C[-1])) / r for C in Cs[1:]]
                lens = [float(np.sum(np.linalg.norm(np.diff(C, axis=0), axis=1)) / r) for C in Cs]
                note = note or f"face {fi}: {len(Cs)} arcs (lengths/r {np.round(lens, 4).tolist()}, end gaps/r {np.round(gaps, 6).tolist()})"
            pieces.append(("face", fi, A))
            for C in chains[fi]:
                for e in (C[0], C[-1]):
                    if min([np.linalg.norm(e - q) for q in joints] + [np.inf]) > r / 20:
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
                         and rec["V0_miss_strips_over_r"] > 1 and rec["V1_ok"])
        return rec

    rv = []
    for v in range(nv):
        bad = [ei for ei in inc[v] if kind[ei] in ("seam", "re-trimmed")]
        if bad:
            out["vertices"][v] = dict(status="not tested: " + ", ".join(f"edge {ei} {kind[ei]}" for ei in bad), ok=None)
            rv.append(RHO * M.tv[v]); continue
        tried = []
        for rho in RHOS:
            rec = vertex_test(v, rho); tried.append((rho, rec["V1_note"], rec["ok"]))
            if rec["ok"]: break
        rec["tried"] = tried
        out["vertices"][v] = rec; rv.append(rec["rho"] * M.tv[v])
    # ---------------- global ----------------
    balls = [BRepPrimAPI_MakeSphere(P(M.p[v]), rv[v]).Shape() for v in range(nv)]
    cutF = []
    for fi in range(len(M.F)):
        sh = PF[fi]
        for b in balls:
            op = BRepAlgoAPI_Cut(); op.SetNonDestructive(True)
            from OCP.TopTools import TopTools_ListOfShape
            a1, a2 = TopTools_ListOfShape(), TopTools_ListOfShape(); a1.Append(sh); a2.Append(b)
            op.SetArguments(a1); op.SetTools(a2); op.Build(); sh = op.Shape()
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
