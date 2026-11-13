"""P2 phase 1: test a 'strip + cone' vertex construction on sewn models.

Construction tested (no proof yet; this only checks whether its geometric hypotheses hold on samples):
  * faces: the patches P_f themselves (so face zones are respected exactly);
  * edges: the strip of segments [b_f(t), b_g(t)] between the boundary points of the two adjacent patches at the same
    edge parameter t. Both ends lie within dev_e <= tau_e of gamma_e(t), and the tube cross-section is a ball, so the
    strip lies in Z(e) automatically;
  * vertex v: a ball B(p_v, r) with r < tau_v, inside which everything is replaced by the cone from p_v over the loop
    in which the outside pieces (patch sectors and strips) meet the sphere |x - p_v| = r.
The cone over a loop on the sphere is an embedded disk iff the loop is a simple closed curve. We test, for
r = rho * tau_v with rho in RHOS:
  L1  every patch corner and every edge-curve end at v lies inside the ball (|.| < r);
  L2  the loop is simple: measured as strictly monotone azimuth around the mean normal n_v, winding once;
  L3  outside the ball, pieces that must be disjoint have positive sampled distance: strips of different edges, and a
      strip and a patch sector of a face not adjacent to that edge. (Adjacent pieces meet by design.)
Also recorded: whether the patches of the two faces at an edge cross each other near v (then plain strips cannot work
and the faces must be re-trimmed, as in the re-intersection route).
Sampled, double precision. Writes ../results/strip_cone_check.json.
"""
import sys, json, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from lemma0_check_run import sloppy
from tight_vertex_survey import PARTS, GAPS
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.TopAbs import TopAbs_IN
from OCP.gp import gp_Pnt2d

RHOS = [0.85, 0.9, 0.95, 0.99]


def bisect(fun, lo, hi, it=50):
    flo = fun(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi); fm = fun(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


class Ctx:
    def __init__(self, M):
        self.M = M
        self.S = [BRepAdaptor_Surface(f) for f in M.F]
        self.crv = [BRepAdaptor_Curve(e) for e in M.E]

    def X(self, fi, uv):
        return L.V(self.S[fi].Value(uv[0], uv[1]))

    def pcurve(self, fi, ei):
        for f2, oe in self.M.uses[ei]:
            if f2 == fi:
                return BRepAdaptor_Curve2d(oe, self.M.F[fi])
        return None


def vertex_data(C, vi, ends):
    """ends: list of (ei, end) at vi. Returns faces at v with their two edges, corner uv and boundary functions."""
    M = C.M
    faces = {}
    for ei, end in ends:
        c = C.crv[ei]; a, b = c.FirstParameter(), c.LastParameter()
        tv = a if end == 0 else b
        tin = (lambda s, a=a, b=b, end=end: a + s * (b - a) if end == 0 else b - s * (b - a))
        for fi, oe in M.uses[ei]:
            faces.setdefault(fi, []).append(dict(edge=ei, tv=tv, tin=tin, pc=BRepAdaptor_Curve2d(oe, M.F[fi])))
    return faces


def sector_samples(C, fi, sides, pv, r, nphi=24):
    """Points of patch fi on the sphere |x-pv|=r, swept across the corner sector; also radial rays for L3."""
    if len(sides) != 2:
        return None
    pc0, pc1 = sides[0]["pc"], sides[1]["pc"]
    c0 = np.array([pc0.Value(sides[0]["tv"]).X(), pc0.Value(sides[0]["tv"]).Y()])
    def dirn(sd):
        p = sd["pc"].Value(sd["tin"](1e-3)); d = np.array([p.X(), p.Y()]) - c0
        return d / np.linalg.norm(d)
    d1, d2 = dirn(sides[0]), dirn(sides[1])
    # choose the rotation from d1 to d2 that passes through the face interior
    ang = math.atan2(d1[0] * d2[1] - d1[1] * d2[0], d1 @ d2)
    cands = [ang, ang - math.copysign(2 * math.pi, ang)]
    span = float(np.linalg.norm(C.X(fi, c0) - C.X(fi, c0 + 1e-3 * d1))) / 1e-3
    best = None
    for A in cands:
        mid = A / 2
        w = np.array([math.cos(mid) * d1[0] - math.sin(mid) * d1[1], math.sin(mid) * d1[0] + math.cos(mid) * d1[1]])
        q = c0 + w * (0.01 * r / max(span, 1e-12))
        if BRepClass_FaceClassifier(C.M.F[fi], gp_Pnt2d(q[0], q[1]), 1e-9).State() == TopAbs_IN:
            best = A; break
    if best is None:
        best = cands[0]
    pts = []
    for k in range(nphi + 1):
        phi = best * k / nphi
        w = np.array([math.cos(phi) * d1[0] - math.sin(phi) * d1[1], math.sin(phi) * d1[0] + math.cos(phi) * d1[1]])
        f = lambda s: float(np.linalg.norm(C.X(fi, c0 + s * w) - pv)) - r
        smax = 4 * r / max(span, 1e-12)
        if f(0) >= 0 or f(smax) <= 0:
            pts.append(None); continue
        s = bisect(f, 0.0, smax)
        pts.append((C.X(fi, c0 + s * w), c0, w, s))
    return pts


def boundary_point_at(C, fi, sd, pv, r):
    """Point of b_f (pcurve image) at distance r from pv, with its edge parameter."""
    f = lambda s: float(np.linalg.norm(C.X(fi, [sd["pc"].Value(sd["tin"](s)).X(), sd["pc"].Value(sd["tin"](s)).Y()]) - pv)) - r
    if f(0) >= 0 or f(0.5) <= 0:
        return None
    s = bisect(f, 0.0, 0.5)
    p = sd["pc"].Value(sd["tin"](s))
    return C.X(fi, [p.X(), p.Y()]), s


def check_vertex(C, vi, ends, rho, nsamp=12):
    M = C.M
    pv, tv = M.p[vi], M.tv[vi]
    r = rho * tv
    faces = vertex_data(C, vi, ends)
    out = dict(rho=rho)
    # L1
    far = 0.0
    for fi, sds in faces.items():
        for sd in sds:
            p = sd["pc"].Value(sd["tv"]); far = max(far, float(np.linalg.norm(C.X(fi, [p.X(), p.Y()]) - pv)))
    for ei, end in ends:
        c = C.crv[ei]; t = c.FirstParameter() if end == 0 else c.LastParameter()
        far = max(far, float(np.linalg.norm(L.V(c.Value(t)) - pv)))
    out["L1"] = far < r
    # loop: sector arcs joined at each edge by the strip crossing (straight segment between the two arc ends)
    sect = {}
    for fi, sds in faces.items():
        sect[fi] = sector_samples(C, fi, sds, pv, r)
    if any(v is None or any(p is None for p in v) for v in sect.values()):
        out["L2"] = False; out["note"] = "a patch sector does not cross the sphere cleanly"; return out
    # arc of face fi runs from its side 0 edge to its side 1 edge
    fedges = {fi: (sds[0]["edge"], sds[1]["edge"]) for fi, sds in faces.items()}
    start = next(iter(fedges)); order = [start]; cur_edge = fedges[start][1]
    while True:
        nxt = [fi for fi in fedges if fi != order[-1] and cur_edge in fedges[fi]]
        if not nxt: out["L2"] = False; out["note"] = "link not a cycle"; return out
        fi = nxt[0]
        if fi == start: break
        order.append(fi); cur_edge = fedges[fi][1] if fedges[fi][0] == cur_edge else fedges[fi][0]
        if len(order) > len(fedges): out["L2"] = False; out["note"] = "link not a cycle"; return out
    loop = []
    prev_edge = fedges[start][0]
    for fi in order:
        arc = [p[0] for p in sect[fi]]
        if fedges[fi][0] != prev_edge:   # traverse from the edge we arrived by
            arc = arc[::-1]
        loop.extend(arc)
        prev_edge = fedges[fi][1] if fedges[fi][0] == prev_edge else fedges[fi][0]
    loop = np.array(loop + [loop[0]])
    segs = list(zip(loop[:-1], loop[1:]))
    def segdist(p, q, a, b):
        # min distance between segments pq and ab (sampled)
        P = p + np.linspace(0, 1, 9)[:, None] * (q - p); A = a + np.linspace(0, 1, 9)[:, None] * (b - a)
        return float(np.min(np.linalg.norm(P[:, None, :] - A[None, :, :], axis=2)))
    nseg = len(segs); md = float("inf")
    for i in range(nseg):
        for j in range(i + 2, nseg):
            if i == 0 and j == nseg - 1: continue
            md = min(md, segdist(*segs[i], *segs[j]))
    out["L2_min_gap_over_r"] = md / r
    out["L2"] = md / r > 1e-3
    # L3: outside-ball samples of strips and sectors
    strips = {}
    for ei, end in ends:
        sides = [(fi, sd) for fi, sds in faces.items() for sd in sds if sd["edge"] == ei]
        if len(sides) != 2:
            continue
        P = []
        for s in np.linspace(0.0, 0.3, 60):
            ab = []
            for fi, sd in sides:
                p = sd["pc"].Value(sd["tin"](s)); ab.append(C.X(fi, [p.X(), p.Y()]))
            for lam in np.linspace(0, 1, 7):
                x = (1 - lam) * ab[0] + lam * ab[1]
                if r < np.linalg.norm(x - pv) < 3 * tv:
                    P.append(x)
        strips[ei] = (np.array(P) if P else np.zeros((0, 3)), {fi for fi, _ in sides})
    secpts = {}
    for fi, arcs in sect.items():
        P = []
        for x, c0, w, s0 in arcs:
            for m in np.linspace(1.0, 4.0, 16):
                y = C.X(fi, c0 + m * s0 * w)
                if r < np.linalg.norm(y - pv) < 3 * tv:
                    P.append(y)
        secpts[fi] = np.array(P) if P else np.zeros((0, 3))
    def mind(A, B):
        if len(A) == 0 or len(B) == 0: return float("inf")
        return float(np.min(np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)))
    worst = float("inf")
    ek = list(strips)
    for i in range(len(ek)):
        for j in range(i + 1, len(ek)):
            worst = min(worst, mind(strips[ek[i]][0], strips[ek[j]][0]))
        for fi in secpts:
            if fi not in strips[ek[i]][1]:
                worst = min(worst, mind(strips[ek[i]][0], secpts[fi]))
    out["L3_min_dist_over_tau_v"] = worst / tv
    return out


def main():
    res = {}
    for name, mk in PARTS.items():
        for g in GAPS:
            key = f"{name}, g={g}"
            try:
                M = L.Model(sloppy(mk(), g)); C = Ctx(M)
            except Exception as ex:
                res[key] = dict(error=repr(ex)); continue
            inc = [[] for _ in M.Vx]
            for ei, (a, b) in enumerate(M.ev):
                inc[a].append((ei, 0))
                if b != a: inc[b].append((ei, 1))
            rows = []
            for vi in range(len(M.Vx)):
                if len(inc[vi]) < 3:
                    continue
                best = None
                for rho in RHOS:
                    try:
                        o = check_vertex(C, vi, inc[vi], rho)
                    except Exception as ex:
                        o = dict(rho=rho, error=repr(ex))
                    ok = o.get("L1") and o.get("L2") and o.get("L3_min_dist_over_tau_v", 0) > 0.02
                    o["ok"] = bool(ok)
                    if best is None or (ok and not best["ok"]):
                        best = o
                    if ok:
                        break
                rows.append(dict(vertex=vi, valence=len(inc[vi]), **best))
            n_ok = sum(1 for x in rows if x["ok"])
            fails = {}
            for x in rows:
                if not x["ok"]:
                    why = "L1" if not x.get("L1") else ("L2" if not x.get("L2") else "L3")
                    if "error" in x: why = "error"
                    fails[why] = fails.get(why, 0) + 1
            res[key] = dict(n=len(rows), n_ok=n_ok, fails=fails, rows=rows)
            print(f"{key}: {n_ok}/{len(rows)} vertices pass; fails {fails}", flush=True)
    json.dump(res, open("../results/strip_cone_check.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main()


def edge_crossing(M, ei, n=150):
    """L4: do the two patches at edge ei cross each other near the edge? In the normal plane at gamma(t), model each
    patch by the ray from its boundary point b in its inward tangent direction u, and solve b_f + s u_f = b_g + s' u_g.
    A solution with s, s' > 0 means the patches cross (the strip between b_f and b_g would then not be embedded)."""
    c = BRepAdaptor_Curve(M.E[ei]); a, b = c.FirstParameter(), c.LastParameter()
    sm = L.edge_samples(M, ei, ts=np.linspace(a, b, n)[1:-1])
    if len(sm["sides"]) != 2:
        return None
    f, g = sm["sides"]
    cross = 0
    for i in range(len(sm["G"])):
        T = sm["T"][i]
        bf, bg = f["B"][i] - (f["B"][i] - sm["G"][i]) @ T * T, g["B"][i] - (g["B"][i] - sm["G"][i]) @ T * T
        uf, ug = f["u"][i], g["u"][i]
        A = np.stack([uf, -ug], axis=1)
        sol, *_ = np.linalg.lstsq(A, bg - bf, rcond=None)
        res = np.linalg.norm(A @ sol - (bg - bf))
        if abs(float(uf @ ug)) > 0.999:      # (anti)parallel: tangent edge, no transversal crossing
            continue
        if sol[0] > 0 and sol[1] > 0 and res < 1e-6 + 1e-3 * np.linalg.norm(bg - bf):
            cross += 1
    return cross / len(sm["G"])


def main_edges():
    res = {}
    for name, mk in PARTS.items():
        for g in GAPS:
            key = f"{name}, g={g}"
            M = L.Model(sloppy(mk(), g))
            fr = [edge_crossing(M, ei) for ei in range(len(M.E))]
            fr = [x for x in fr if x is not None]
            n_cross = sum(1 for x in fr if x > 0)
            res[key] = dict(n_edges=len(fr), n_edges_crossing=n_cross)
            print(f"{key}: {n_cross}/{len(fr)} edges whose patches cross", flush=True)
    json.dump(res, open("../results/strip_edge_crossing.json", "w"), indent=1)
