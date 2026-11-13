"""P2 checker v3: tests the hypotheses of notes/p2_strip_cone_v03.md for the construction as stated there
(addresses review M4 of notes/reviews/p2_v02_review.md).

Per model (sewn as in P1) and a ball ratio rho (r_v = rho * tau_v):
  Edges. For every edge e, on a grid of parameters t:
    E1'  the pcurve image beta_{f,e} meets the normal disk D(t) = Pi(t) ∩ B(gamma(t), rho_e), rho_e = 0.999 min(tau_e,
         reach_e), in exactly one point b*_f(t), transversally; likewise for g. (Sign changes of <beta(s)-gamma(t),
         gamma'(t)> over a dense sampling of beta, restricted to D(t).)
    E4a  the chord [b*_f, b*_g] minus 2% at each end has positive distance (BRepExtrema) from the faces f and g.
    E4b  the chord direction is not in the closed inward tangent half-plane of the patch at its end (angle recorded).
    An edge where E4a fails somewhere on its interval is a re-trimmed edge: then
    R'   the surfaces of f and g intersect (GeomAPI_IntSS) in a curve q_e that stays within tau_e of gamma_e between the
         balls, with the patches transversal along it (angle between normals recorded).
    The interval I_e runs between the last parameter whose chord lies inside B_v and the first whose chord lies inside
    B_w (by convexity, both chord ends inside suffice).
  Vertices.
    V0'  corners, gamma ends and the end chords lie in int B_v; balls pairwise disjoint; B_v misses every face not
         incident to v (BRepExtrema point-face) and every strip not incident to v (distance to gamma - rho_e).
    V1'  lambda_v: each face arc (quadtree, as in strip_cone_check2) is one component; the chord-arc of every strip edge
         (points X(t,lambda) on S_v) is computed on the sphere; at a re-trimmed edge the two face arcs are cut at q_e ∩ S_v.
         Joints: each face-arc end must coincide (within r/40) with the end of a chord-arc or a q_e point; the pieces
         must be pairwise apart outside 3r/20-neighbourhoods of the joints. NOT YET TESTED: transversality (V1'a) and
         that each face arc is a single arc rather than one cluster of samples.
  Global.
    S1'  faces cut by the balls (BRepAlgoAPI_Cut) are pairwise at positive distance, except pairs along a re-trimmed
         edge; strips (as compounds of chord edges over all of I_e) are apart from each other and from non-incident cut
         faces.
    P0'  recorded as the surface types (plane, cylinder, sphere, torus, cone are embedded surfaces).
Sampled, double precision. One model per call: python3 strip_cone_check3.py <index>; with no index, merge parts.
"""
import sys, os, json, math, glob
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from lemma0_check_run import sloppy
from tight_vertex_survey import PARTS, GAPS
from strip_cone_check import bisect
from strip_cone_check2 import face_band, clusters
from patchface import patch_face
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeVertex
from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRep import BRep_Tool, BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.GeomAPI import GeomAPI_IntSS
from OCP.gp import gp_Pnt

NT = 90          # edge parameter samples
NB = 1500        # pcurve samples for the E1' crossing count
RHO = 0.95


def P(x): return gp_Pnt(*map(float, x))


def dist_shapes(a, b):
    d = BRepExtrema_DistShapeShape(a, b)
    return d.Value() if d.IsDone() else float("nan")


def compound(shapes):
    c = TopoDS_Compound(); bld = BRep_Builder(); bld.MakeCompound(c)
    for s in shapes: bld.Add(c, s)
    return c


class Edge:
    def __init__(self, M, ei):
        self.M, self.ei = M, ei
        self.c = BRepAdaptor_Curve(M.E[ei]); self.a, self.b = self.c.FirstParameter(), self.c.LastParameter()
        sm = L.edge_samples(M, ei, ts=np.linspace(self.a, self.b, 200))
        self.reach = L.edge_reach(sm)
        self.rho = 0.999 * min(M.te[ei], self.reach)
        self.sides = []
        for fi, oe in M.uses[ei]:
            pc = BRepAdaptor_Curve2d(oe, M.F[fi]); S = BRepAdaptor_Surface(M.F[fi])
            s = np.linspace(self.a, self.b, NB)
            B = np.array([L.V(S.Value(pc.Value(x).X(), pc.Value(x).Y())) for x in s])
            self.sides.append(dict(fi=fi, pc=pc, S=S, s=s, B=B))

    def gamma(self, t):
        p, d = gp_Pnt(), __import__("OCP.gp", fromlist=["gp_Vec"]).gp_Vec()
        self.c.D1(t, p, d); d = L.V(d); return L.V(p), d / np.linalg.norm(d)

    def bstar(self, side, t):
        """Unique crossing of beta with D(t); returns (point, ok, transversality cosine) or (None, False, reason)."""
        g, T = self.gamma(t)
        B, s = side["B"], side["s"]
        h = (B - g) @ T
        S, pc = side["S"], side["pc"]
        f = lambda x: float((L.V(S.Value(pc.Value(x).X(), pc.Value(x).Y())) - g) @ T)
        hits = []
        for i in range(len(s) - 1):
            if (h[i] > 0) != (h[i + 1] > 0):
                x = bisect(f, s[i], s[i + 1])
                bp = L.V(S.Value(pc.Value(x).X(), pc.Value(x).Y()))
                if np.linalg.norm(bp - g) < self.rho:
                    hits.append((x, bp))
        if len(hits) != 1:
            return None, False, f"{len(hits)} crossings in D(t)"
        x, bp = hits[0]
        dx = 1e-6 * (self.b - self.a)
        bq = L.V(S.Value(pc.Value(x + dx).X(), pc.Value(x + dx).Y()))
        tang = (bq - bp) / np.linalg.norm(bq - bp)
        return bp, True, abs(float(tang @ T))


def inward_halfplane_angle(side, bp, chord_dir):
    """Angle between the chord direction and the closed inward tangent half-plane of the patch at bp."""
    from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
    S = side["S"]; surf = BRep_Tool.Surface_s(side["S"].Face()) if hasattr(side["S"], "Face") else None
    # normal and inward direction from nearby samples of the patch boundary and the surface
    pr = GeomAPI_ProjectPointOnSurf(P(bp), BRep_Tool.Surface_s(side["face"]))
    u, v = pr.LowerDistanceParameters()
    n, _ = L.surf_props(side["face"], u, v)
    k = int(np.argmin(np.linalg.norm(side["B"] - bp, axis=1)))
    k2 = min(k + 1, len(side["B"]) - 1); k1 = max(k - 1, 0)
    tb = side["B"][k2] - side["B"][k1]; tb /= np.linalg.norm(tb)
    w = np.cross(n, tb); w /= np.linalg.norm(w)
    # pick the inward sign: the side of the boundary where the patch is (classifier on a nudged uv point)
    from OCP.BRepClass import BRepClass_FaceClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt2d
    du = 1e-5
    ok = False
    for sgn in (1, -1):
        q = bp + sgn * w * 1e-4 * max(1.0, np.linalg.norm(bp))
        pr2 = GeomAPI_ProjectPointOnSurf(P(q), BRep_Tool.Surface_s(side["face"]))
        uu, vv = pr2.LowerDistanceParameters()
        if BRepClass_FaceClassifier(side["face"], gp_Pnt2d(uu, vv), 1e-9).State() == TopAbs_IN:
            w = sgn * w; ok = True; break
    d = chord_dir / np.linalg.norm(chord_dir)
    # distance of d to the half-plane {a tb + b w, b >= 0}
    dn = float(d @ n); dw = float(d @ w)
    if dw >= 0:
        return math.degrees(math.asin(min(1, abs(dn))))
    return math.degrees(math.asin(min(1, math.sqrt(dn * dn + dw * dw))))


def run(index, rho=RHO):
    name, g = [(n, g) for n in PARTS for g in GAPS][index]
    key = f"{name}, g={g}"
    shape = sloppy(PARTS[name](), g)
    M = L.Model(shape)
    PF = [patch_face(f) for f in M.F]
    if any(p is None for p in PF):
        print(key, "patch rebuild failed", flush=True)
    PF = [p if p is not None else f for p, f in zip(PF, M.F)]
    nv = len(M.Vx)
    rv = [rho * M.tv[v] for v in range(nv)]
    out = dict(key=key, rho=rho, edges={}, vertices={}, global_={})
    # balls
    balls = [BRepPrimAPI_MakeSphere(P(M.p[v]), rv[v]).Shape() for v in range(nv)]
    cutF = []
    for fi in range(len(M.F)):
        sh = PF[fi]
        for b in balls:
            sh = BRepAlgoAPI_Cut(sh, b).Shape()
        cutF.append(sh)
    # ---------------- edges ----------------
    E, CH = {}, {}
    for ei in range(len(M.E)):
        ed = Edge(M, ei); E[ei] = ed
        for sd in ed.sides: sd["face"] = M.F[sd["fi"]]
        rec = dict(reach=ed.reach, rho_e=ed.rho, tau_e=M.te[ei], kind="strip")
        if len(ed.sides) != 2 or ed.sides[0]["fi"] == ed.sides[1]["fi"]:
            rec["kind"] = "seam/other (not covered)"; out["edges"][ei] = rec; continue
        va, vb = M.ev[ei]
        Lp = ed.b - ed.a
        geo = np.geomspace(1e-6, 0.05, 40) * Lp
        ts = np.unique(np.concatenate([ed.a + geo, np.linspace(ed.a, ed.b, NT), ed.b - geo]))
        chords, e1_fail, e4a_fail, e4b_min, trans_min = [], [], [], 90.0, 1.0
        for t in ts:
            bs = [ed.bstar(sd, t) for sd in ed.sides]
            ins = [np.linalg.norm(x[0] - M.p[va]) < rv[va] if x[0] is not None else False for x in bs] + \
                  [np.linalg.norm(x[0] - M.p[vb]) < rv[vb] if x[0] is not None else False for x in bs]
            in_a, in_b = ins[0] and ins[1], ins[2] and ins[3]
            if in_a or in_b:
                chords.append((t, None, None, "in ball"))
                continue
            gt = ed.gamma(t)[0]
            if not (bs[0][1] and bs[1][1]) and any(np.linalg.norm(gt - M.p[w]) + ed.rho < rv[w] for w in (va, vb)):
                chords.append((t, None, None, "in ball")); continue
            if not (bs[0][1] and bs[1][1]):
                e1_fail.append((float(t), bs[0][2] if not bs[0][1] else bs[1][2])); chords.append((t, None, None, "E1'"))
                continue
            trans_min = min(trans_min, bs[0][2], bs[1][2])
            p, q = bs[0][0], bs[1][0]
            chords.append((t, p, q, "ok"))
            if np.linalg.norm(p - q) < 1e-12:
                e4a_fail.append(float(t)); continue
            a, b = p + 0.02 * (q - p), q - 0.02 * (q - p)
            sub = BRepBuilderAPI_MakeEdge(P(a), P(b)).Edge()
            dmin = min(dist_shapes(sub, PF[ed.sides[0]["fi"]]), dist_shapes(sub, PF[ed.sides[1]["fi"]]))
            if not dmin > 1e-9:
                e4a_fail.append(float(t))
            try:
                e4b_min = min(e4b_min, inward_halfplane_angle(ed.sides[0], p, q - p), inward_halfplane_angle(ed.sides[1], q, p - q))
            except Exception:
                pass
        st = [c[3] for c in chords]
        lo = max([i for i in range(len(st)) if st[i] == "in ball" and i < len(st) // 2] + [-1])
        hi = min([i for i in range(len(st)) if st[i] == "in ball" and i >= len(st) // 2] + [len(st)])
        rec["V0_end_chords_in_balls"] = bool(lo >= 0 and hi < len(st))
        e1_fail = [x for x in e1_fail if ts[lo + 1] <= x[0] <= ts[hi - 1]] if lo + 1 <= hi - 1 else e1_fail
        e4a_fail = [x for x in e4a_fail if ts[lo + 1] <= x <= ts[hi - 1]] if lo + 1 <= hi - 1 else e4a_fail
        rec.update(E1_fail=len(e1_fail), E1_examples=e1_fail[:3], E4a_fail=len(e4a_fail), E4b_min_angle_deg=e4b_min,
                   transversality_min_cos=trans_min, n_interval=sum(1 for c in chords if c[3] == "ok"))
        rec["patches_cross"] = bool(dist_shapes(cutF[ed.sides[0]["fi"]], cutF[ed.sides[1]["fi"]]) < 1e-9)
        if e4a_fail or rec["patches_cross"]:
            rec["kind"] = "re-trimmed"
            # R': intersection curve of the two surfaces near gamma
            s1 = BRep_Tool.Surface_s(M.F[ed.sides[0]["fi"]]); s2 = BRep_Tool.Surface_s(M.F[ed.sides[1]["fi"]])
            inter = GeomAPI_IntSS(s1, s2, 1e-9)
            best = None
            if inter.IsDone():
                for k in range(1, inter.NbLines() + 1):
                    cv = inter.Line(k)
                    from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
                    G = [ed.gamma(t)[0] for t, c in zip(ts, chords) if c[3] != "in ball"]
                    dd, params = [], []
                    for gpt in G:
                        pr = GeomAPI_ProjectPointOnCurve(P(gpt), cv)
                        if pr.NbPoints() == 0:
                            dd.append(float("inf")); continue
                        dd.append(pr.LowerDistance()); params.append(pr.LowerDistanceParameter())
                    m = max(dd) if dd else float("inf")
                    if best is None or m < best[0]:
                        if params:
                            u0, u1 = min(params), max(params); pad = 0.1 * (u1 - u0) + 1e-9
                            pts = np.array([L.V(cv.Value(x)) for x in np.linspace(u0 - pad, u1 + pad, 4000)])
                        else:
                            pts = np.zeros((0, 3))
                        best = (m, pts, cv, (u0 - pad, u1 + pad) if params else None)
            if best is None:
                rec["R_ok"] = False; rec["R_note"] = "no intersection curve"
            else:
                rec["R_max_dist_to_gamma_over_tau_e"] = best[0] / M.te[ei]
                rec["R_ok"] = best[0] < M.te[ei]
                CH[ei] = ("q", (best[2], best[3]))
        else:
            CH[ei] = ("strip", [(t, p, q) for t, p, q, s in chords if s == "ok"])
        out["edges"][ei] = rec
    # ---------------- vertices ----------------
    inc = [[] for _ in range(nv)]
    for ei, (a, b) in enumerate(M.ev):
        inc[a].append(ei)
        if b != a: inc[b].append(ei)
    for v in range(nv):
        pv, r = M.p[v], rv[v]
        rec = {}
        far = 0.0
        for ei in inc[v]:
            ed = E[ei]
            for t in (ed.a, ed.b):
                gp = ed.gamma(t)[0]
                if np.linalg.norm(gp - pv) < 2 * M.tv[v]: far = max(far, np.linalg.norm(gp - pv))
            for sd in ed.sides:
                for x in (sd["B"][0], sd["B"][-1]):
                    if np.linalg.norm(x - pv) < 2 * M.tv[v]: far = max(far, np.linalg.norm(x - pv))
        rec["V0_corners_inside"] = bool(far < r)
        rec["V0_ball_disjoint"] = all(np.linalg.norm(pv - M.p[w]) > r + rv[w] for w in range(nv) if w != v)
        vtx = BRepBuilderAPI_MakeVertex(P(pv)).Vertex()
        nonf = [fi for fi in range(len(M.F)) if v not in M.fv[fi]]
        rec["V0_miss_faces_over_r"] = min([dist_shapes(vtx, PF[fi]) for fi in nonf] + [float("inf")]) / r
        none_ = [ei for ei in range(len(M.E)) if ei not in inc[v]]
        rec["V0_miss_strips_over_r"] = min([(dist_shapes(vtx, M.E[ei]) - E[ei].rho) for ei in none_] + [float("inf")]) / r
        # V1': lambda_v
        arcs = {}
        for fi in {sd["fi"] for ei in inc[v] for sd in E[ei].sides}:
            S = BRepAdaptor_Surface(M.F[fi]); sph, _ = face_band(M, S, fi, pv, r, 1.2 * r)
            arcs[fi] = sph
        joints, pieces, note = [], [], None
        for ei in inc[v]:
            kind, data = CH.get(ei, (None, None))
            if kind == "strip":
                ed = E[ei]; tv_end = ed.a if M.ev[ei][0] == v else ed.b; sgn = 1 if tv_end == ed.a else -1
                Lp = ed.b - ed.a
                def X(t, lam):
                    b0 = ed.bstar(ed.sides[0], t); b1 = ed.bstar(ed.sides[1], t)
                    if not (b0[1] and b1[1]): return None
                    return (1 - lam) * b0[0] + lam * b1[0]
                arc = []
                grid = tv_end + sgn * np.geomspace(1e-7, 0.3, 120) * Lp
                for lam in np.linspace(0, 1, 21):
                    prev = None
                    for t in grid:
                        x = X(t, lam)
                        if x is None: prev = None; continue
                        dcur = np.linalg.norm(x - pv) - r
                        if prev is not None and (prev[1] < 0) != (dcur < 0):
                            def F(tt):
                                y = X(tt, lam); return (np.linalg.norm(y - pv) - r) if y is not None else prev[1]
                            tt = bisect(F, prev[0], t); y = X(tt, lam)
                            if y is not None: arc.append(y)
                            break
                        prev = (t, dcur)
                if len(arc) < 21: note = note or f"edge {ei}: chord-arc incomplete ({len(arc)}/21)"
                if len(arc) < 2: continue
                arc = np.array(arc); pieces.append(("strip", ei, arc)); joints += [arc[0], arc[-1]]
            elif kind == "q":
                cv, rng = data
                if rng is None: note = note or f"edge {ei}: no q_e"; continue
                us = np.linspace(rng[0], rng[1], 40000)
                D = np.array([np.linalg.norm(L.V(cv.Value(u)) - pv) - r for u in us])
                cand = [i for i in range(len(us) - 1) if (D[i] < 0) != (D[i + 1] < 0)]
                if not cand: note = note or f"edge {ei}: q_e does not reach S_v"; continue
                ed = E[ei]; tv_end = ed.a if M.ev[ei][0] == v else ed.b; sgn = 1 if tv_end == ed.a else -1
                gg = tv_end + sgn * np.geomspace(1e-8, 0.5, 400) * (ed.b - ed.a)
                gref = None
                for x0, x1 in zip(gg[:-1], gg[1:]):
                    if (np.linalg.norm(ed.gamma(x0)[0] - pv) < r) != (np.linalg.norm(ed.gamma(x1)[0] - pv) < r):
                        gref = ed.gamma(0.5 * (x0 + x1))[0]; break
                if gref is None: gref = ed.gamma(tv_end + sgn * 0.01 * (ed.b - ed.a))[0]
                i = min(cand, key=lambda k: np.linalg.norm(L.V(cv.Value(us[k])) - gref))
                u = bisect(lambda x: np.linalg.norm(L.V(cv.Value(x)) - pv) - r, us[i], us[i + 1])
                q = L.V(cv.Value(u)); joints.append(q)
                from strip_cone_check2 import trim_from
                for sd in E[ei].sides:
                    A = arcs.get(sd["fi"])
                    if A is None or len(A) == 0: continue
                    # the discarded part of the face arc runs from beta_{f,e} ∩ S_v to q
                    ed = E[ei]; tv_end = ed.a if M.ev[ei][0] == v else ed.b; sgn = 1 if tv_end == ed.a else -1
                    Sx, pc = sd["S"], sd["pc"]
                    bet = lambda x: L.V(Sx.Value(pc.Value(x).X(), pc.Value(x).Y()))
                    grid = tv_end + sgn * np.geomspace(1e-8, 0.3, 200) * (ed.b - ed.a)
                    end = None
                    for x0, x1 in zip(grid[:-1], grid[1:]):
                        if (np.linalg.norm(bet(x0) - pv) - r < 0) != (np.linalg.norm(bet(x1) - pv) - r < 0):
                            end = bet(bisect(lambda x: np.linalg.norm(bet(x) - pv) - r, x0, x1)); break
                    if end is None:
                        note = note or f"edge {ei}: beta of face {sd['fi']} does not cross S_v"; continue
                    dq = float(np.min(np.linalg.norm(A - q, axis=1)))
                    if dq > r / 10:
                        note = note or f"edge {ei}: q_e ∩ S_v is not on the arc of face {sd['fi']} (dist {dq / r:.2f} r)"; continue
                    arcs[sd["fi"]] = trim_from(A, end, q)
        for fi, A in arcs.items():
            if len(A) == 0: note = note or f"face {fi}: no arc"; continue
            lab, k = clusters(A, r / 6)
            if k != 1: note = note or f"face {fi}: {k} arcs"
            pieces.append(("face", fi, A))
        tolj = r / 40
        # joints: every face arc end must be near a joint
        for kind, idx, A in pieces:
            if kind != "face": continue
            from strip_cone_check2 import order_chain
            C = order_chain(A, A[0]); ends = [C[0], C[-1]]
            # order_chain from an arbitrary point may not start at an end; use the two points farthest apart
            Dm = np.linalg.norm(A[:, None] - A[None], axis=2); i, j = np.unravel_index(np.argmax(Dm), Dm.shape)
            for e in (A[i], A[j]):
                if min([np.linalg.norm(e - q) for q in joints] + [np.inf]) > max(tolj, 3 * r / 20):
                    note = note or f"face {idx}: arc end not at a joint"
        md = float("inf")
        for i in range(len(pieces)):
            for j in range(i + 1, len(pieces)):
                A, B = pieces[i][2], pieces[j][2]
                Dm = np.linalg.norm(A[:, None] - B[None], axis=2)
                for q in joints:
                    Dm = np.where((np.linalg.norm(A - q, axis=1)[:, None] < 3 * r / 20) | (np.linalg.norm(B - q, axis=1)[None, :] < 3 * r / 20), np.inf, Dm)
                md = min(md, float(Dm.min()))
        rec["V1_min_gap_over_r"] = md / r
        rec["V1_note"] = note
        rec["V1_ok"] = note is None and md / r > 0.005
        rec["ok"] = bool(rec["V0_corners_inside"] and rec["V0_ball_disjoint"] and rec["V0_miss_faces_over_r"] > 1
                         and rec["V0_miss_strips_over_r"] > 1 and rec["V1_ok"])
        out["vertices"][v] = rec
    # ---------------- global S1' ----------------
    allb = balls[0]
    for b in balls[1:]:
        allb = BRepAlgoAPI_Cut(allb, BRepAlgoAPI_Cut(allb, b).Shape()).Shape() if False else allb
    retr = {ei for ei, r_ in out["edges"].items() if r_.get("kind") == "re-trimmed"}
    adj_retr = {tuple(sorted((E[ei].sides[0]["fi"], E[ei].sides[1]["fi"]))) for ei in retr}
    ff = float("inf")
    for i in range(len(M.F)):
        for j in range(i + 1, len(M.F)):
            if (i, j) in adj_retr: continue
            ff = min(ff, dist_shapes(cutF[i], cutF[j]))
    strips = {}
    for ei, (kind, data) in CH.items():
        if kind == "strip" and data:
            strips[ei] = compound([BRepBuilderAPI_MakeEdge(P(p), P(q)).Edge() for t, p, q in data if np.linalg.norm(p - q) > 1e-12])
    ss = float("inf")
    ks = list(strips)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            ss = min(ss, dist_shapes(strips[ks[i]], strips[ks[j]]))
    sf = float("inf")
    for ei, cs in strips.items():
        fs = {sd["fi"] for sd in E[ei].sides}
        for fi in range(len(M.F)):
            if fi not in fs: sf = min(sf, dist_shapes(cs, cutF[fi]))
    out["global_"] = dict(face_face_min=ff, strip_strip_min=ss, strip_face_min=sf,
                          surface_types=sorted({str(BRepAdaptor_Surface(f).GetType()).split('_')[-1] for f in M.F}))
    nv_ok = sum(1 for r_ in out["vertices"].values() if r_["ok"])
    ne = len(out["edges"])
    summ = dict(vertices_ok=f"{nv_ok}/{nv}",
                edges_strip=sum(1 for r_ in out["edges"].values() if r_["kind"] == "strip"),
                edges_retrimmed=len(retr),
                edges_E1_fail=sum(1 for r_ in out["edges"].values() if r_.get("E1_fail")),
                retrimmed_R_fail=sum(1 for ei in retr if not out["edges"][ei].get("R_ok")),
                E4b_min_angle_deg=min([r_.get("E4b_min_angle_deg", 90) for r_ in out["edges"].values()]),
                **{k: v for k, v in out["global_"].items() if k != "surface_types"})
    out["summary"] = summ
    print(key, json.dumps(summ, default=float), flush=True)
    return key, out


def main():
    if len(sys.argv) > 1:
        i = int(sys.argv[1]); key, out = run(i)
        os.makedirs("../results/strip_cone_v3_parts", exist_ok=True)
        json.dump({key: out}, open(f"../results/strip_cone_v3_parts/{i:02d}.json", "w"), indent=1, default=float)
        return
    res = {}
    for f in sorted(glob.glob("../results/strip_cone_v3_parts/*.json")):
        res.update(json.load(open(f)))
    json.dump(res, open("../results/strip_cone_check3.json", "w"), indent=1, default=float)
    print(len(res), "models merged")


if __name__ == "__main__":
    main()
