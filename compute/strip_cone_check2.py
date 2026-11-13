"""P2 phase 2, step 1: strip + cone vertex test that also handles poles, seams and any valence.

Same construction as strip_cone_check.py (patches as faces, strips [b_f(t), b_g(t)] as edges, cone from p_v inside
B(p_v, r), r = rho * tau_v). Instead of sweeping a corner sector, each face is sampled on a fine (u,v) grid in a window
around its corner(s) at v, classified IN/OUT with BRepClass_FaceClassifier, and the sphere |x - p_v| = r is
contoured (marching squares, masked to IN). This works at poles (degenerate edges) and seams.

Checks for each vertex and rho in RHOS:
  L1  patch corners and edge-curve ends at v are inside the ball;
  L2  the pieces meet the sphere in ONE simple closed curve: the face arcs, joined at each edge by the strip crossing,
      form a single cycle (each arc end matched to a strip end), and non-adjacent segments are apart;
  L3  outside the ball (up to 3 tau_v): strips of different edges, and a strip and a face not adjacent to its edge,
      are apart.
Also per edge (L4): whether the two patches cross (from strip_cone_check.edge_crossing).
Sampled, double precision. Writes ../results/strip_cone_check2.json.
"""
import sys, json, math
import numpy as np
from skimage import measure
sys.path.insert(0, ".")
import lemma0_check as L
from lemma0_check_run import sloppy
from tight_vertex_survey import PARTS, GAPS
from strip_cone_check import edge_crossing, bisect
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.TopAbs import TopAbs_IN, TopAbs_ON
from OCP.gp import gp_Pnt2d

RHOS = [0.85, 0.9, 0.95, 0.99]
NG = 140


def face_band(M, S, fi, pv, r, R3):
    """Quadtree over the whole (u,v) domain of face fi. Returns (sphere points, cloud) where sphere points are the
    zero crossings of |X-pv|-r along edges of fine IN cells, and cloud are IN sample points with r<|X-pv|<R3.
    Works at poles and seams because it never assumes a local chart around the corner."""
    from OCP.BRepTools import BRepTools
    f = M.F[fi]
    u0, u1, v0, v1 = BRepTools.UVBounds_s(f)
    target = r / 20.0
    sph, cloud = [], []
    stack = [(u0, u1, v0, v1, 0)]
    def X(u, v): return L.V(S.Value(u, v))
    def isin(u, v):
        st = BRepClass_FaceClassifier(f, gp_Pnt2d(u, v), 1e-9).State(); return st == TopAbs_IN or st == TopAbs_ON
    while stack:
        a0, a1, b0, b1, d = stack.pop()
        P = [X(a0, b0), X(a1, b0), X(a0, b1), X(a1, b1), X(0.5 * (a0 + a1), 0.5 * (b0 + b1))]
        diam = max(np.linalg.norm(p - q) for p in P for q in P)
        dist = [np.linalg.norm(p - pv) for p in P]
        lo = min(dist) - diam; hi = max(dist) + diam
        if lo > R3 or hi < r * 0.5:
            continue
        near_sphere = lo <= r <= hi
        if d < 6 or (d < 26 and ((near_sphere and diam > target) or (not near_sphere and diam > 0.4 * r))):
            am, bm = 0.5 * (a0 + a1), 0.5 * (b0 + b1)
            stack += [(a0, am, b0, bm, d + 1), (am, a1, b0, bm, d + 1), (a0, am, bm, b1, d + 1), (am, a1, bm, b1, d + 1)]
            continue
        c = (0.5 * (a0 + a1), 0.5 * (b0 + b1))
        if not isin(*c):
            continue
        if r < dist[4] < R3:
            cloud.append(P[4])
        corners = [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]
        Dv = [np.linalg.norm(X(*q) - pv) - r for q in corners]
        for k in range(4):
            d0, d1 = Dv[k], Dv[(k + 1) % 4]
            if (d0 > 0) != (d1 > 0):
                lam = d0 / (d0 - d1); q0, q1 = np.array(corners[k]), np.array(corners[(k + 1) % 4])
                q = q0 + lam * (q1 - q0)
                if isin(*q):
                    sph.append(X(*q))
    return np.array(sph) if sph else np.zeros((0, 3)), np.array(cloud) if cloud else np.zeros((0, 3))


def clusters(P, link):
    n = len(P); lab = -np.ones(n, int); k = 0
    for i in range(n):
        if lab[i] >= 0: continue
        lab[i] = k; st = [i]
        while st:
            j = st.pop()
            nb = np.where((np.linalg.norm(P - P[j], axis=1) < link) & (lab < 0))[0]
            lab[nb] = k; st.extend(nb.tolist())
        k += 1
    return lab, k


def check_vertex(M, Ss, vi, ends, rho):
    pv, tv = M.p[vi], M.tv[vi]; r = rho * tv
    out = dict(rho=rho)
    # uses at v per face
    uses = {}
    far = 0.0
    strips = {}
    for ei, end in ends:
        c = BRepAdaptor_Curve(M.E[ei]); a, b = c.FirstParameter(), c.LastParameter()
        tvx = a if end == 0 else b
        far = max(far, float(np.linalg.norm(L.V(c.Value(tvx)) - pv)))
        tin = (lambda s, a=a, b=b, end=end: a + s * (b - a) if end == 0 else b - s * (b - a))
        sides = []
        for fi, oe in M.uses[ei]:
            uses.setdefault(fi, []).append((ei, oe, tvx))
            pc = BRepAdaptor_Curve2d(oe, M.F[fi])
            bf = (lambda s, pc=pc, fi=fi, tin=tin: L.V(Ss[fi].Value(pc.Value(tin(s)).X(), pc.Value(tin(s)).Y())))
            far = max(far, float(np.linalg.norm(bf(0.0) - pv)))
            sides.append((fi, bf))
        strips[ei] = sides
    out["L1"] = far < r
    if not out["L1"]:
        return out
    # strip crossings with the sphere: for each edge with two sides, the two boundary points at distance r
    conn = []
    for ei, sides in strips.items():
        if len(sides) != 2 or sides[0][0] == sides[1][0]:
            # seam edge (same face twice): the two sides are joined inside the face's own parameter window
            pass
        ends_e = []
        for fi, bf in sides:
            g = lambda s: float(np.linalg.norm(bf(s) - pv)) - r
            if g(0) >= 0 or g(0.5) <= 0:
                out["L2"] = False; out["note"] = f"boundary of face {fi} at edge {ei} does not cross the sphere"; return out
            s = bisect(g, 0.0, 0.5); ends_e.append((fi, bf(s)))
        if len(ends_e) == 2:
            conn.append((ei, ends_e[0], ends_e[1]))
    # face pieces on the sphere: one arc per face, containing both of its strip ends; arcs of different faces apart
    sph, clouds = {}, {}
    for fi in uses:
        sph[fi], clouds[fi] = face_band(M, Ss[fi], fi, pv, r, 3 * tv)
    link = r / 6.0
    md = float("inf")
    for fi, P in sph.items():
        if len(P) == 0:
            out["L2"] = False; out["note"] = f"face {fi} does not meet the sphere"; return out
        lab, k = clusters(P, link)
        if k != 1:
            out["L2"] = False; out["note"] = f"face {fi} meets the sphere in {k} pieces"; return out
        for ei, (fa, pa), (fb, pb) in conn:
            for fx, px in ((fa, pa), (fb, pb)):
                if fx == fi and np.min(np.linalg.norm(P - px, axis=1)) > link:
                    out["L2"] = False; out["note"] = f"strip end of edge {ei} not on the arc of face {fi}"; return out
    fis = list(sph)
    for i in range(len(fis)):
        for j in range(i + 1, len(fis)):
            A, B = sph[fis[i]], sph[fis[j]]
            md = min(md, float(np.min(np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2))))
    for ei, (fa, pa), (fb, pb) in conn:
        seg = np.linspace(pa, pb, 15)[2:-2]
        for fi in fis:
            if fi not in (fa, fb):
                md = min(md, float(np.min(np.linalg.norm(sph[fi][:, None, :] - seg[None, :, :], axis=2))))
    out["L2_min_gap_over_r"] = md / r
    out["L2"] = md / r > 0.01
    # L3
    spts = {}
    for ei, sides in strips.items():
        if len(sides) != 2:
            continue
        P = []
        for s in np.linspace(0, 0.3, 80):
            a, b = sides[0][1](s), sides[1][1](s)
            for lam in np.linspace(0, 1, 7):
                x = (1 - lam) * a + lam * b
                if r < np.linalg.norm(x - pv) < 3 * tv: P.append(x)
        spts[ei] = (np.array(P) if P else np.zeros((0, 3)), {sides[0][0], sides[1][0]})
    def mind(A, B):
        if len(A) == 0 or len(B) == 0: return float("inf")
        return float(np.min(np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)))
    worst = float("inf"); ek = list(spts)
    for i in range(len(ek)):
        for j in range(i + 1, len(ek)):
            worst = min(worst, mind(spts[ek[i]][0], spts[ek[j]][0]))
        for fi, cl in clouds.items():
            if fi not in spts[ek[i]][1]:
                worst = min(worst, mind(spts[ek[i]][0], cl[::3]))
    out["L3_min_dist_over_tau_v"] = worst / tv
    return out


def run_model(args):
    name, g = args
    from tight_vertex_survey import PARTS as P
    key = f"{name}, g={g}"
    M = L.Model(sloppy(P[name](), g)); Ss = [BRepAdaptor_Surface(f) for f in M.F]
    inc = [[] for _ in M.Vx]
    for ei, (a, b) in enumerate(M.ev):
        inc[a].append((ei, 0))
        if b != a: inc[b].append((ei, 1))
    rows = []
    for vi in range(len(M.Vx)):
        if not inc[vi]:
            continue
        best = None
        for rho in RHOS:
            try:
                o = check_vertex(M, Ss, vi, inc[vi], rho)
            except Exception as ex:
                o = dict(rho=rho, error=repr(ex))
            o["ok"] = bool(o.get("L1") and o.get("L2") and o.get("L3_min_dist_over_tau_v", 0) > 0.02)
            if best is None or o["ok"] or (o.get("L1") and not best.get("L1")):
                best = o
            if o["ok"]:
                break
        rows.append(dict(vertex=vi, valence=len(inc[vi]), **best))
    cross = [edge_crossing(M, ei) for ei in range(len(M.E))]
    n_cross = sum(1 for x in cross if x)
    fails = {}
    for x in rows:
        if not x["ok"]:
            why = "error" if "error" in x else ("L1" if not x.get("L1") else ("L2" if not x.get("L2") else "L3"))
            fails[why] = fails.get(why, 0) + 1
    r = dict(n=len(rows), n_ok=sum(x["ok"] for x in rows), fails=fails, edges_crossing=n_cross, n_edges=len(M.E), rows=rows)
    print(f"{key}: {r['n_ok']}/{len(rows)} vertices pass; fails {fails}; edges crossing {n_cross}/{len(M.E)}", flush=True)
    return key, r


def main():
    import multiprocessing as mp
    jobs = [(n, g) for n in PARTS for g in GAPS]
    with mp.get_context("spawn").Pool(min(len(jobs), max(1, mp.cpu_count()))) as pool:
        res = dict(pool.map(run_model, jobs, chunksize=1))
    json.dump(res, open("../results/strip_cone_check2.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
