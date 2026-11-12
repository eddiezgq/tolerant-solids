"""Check the hypotheses of Lemma 0 (v0.2, notes/lemma0_v02.md) on an OpenCascade model.

What is checked, and how strictly:
  * Local hypotheses E1, E2.1, E2.2, E3, V0, V1(a): evaluated on samples along each edge
    (N points per edge), using OpenCascade's own tolerances tau_v, tau_e, tau_f and the measured
    edge deviation dev_e = max |S_f(pcurve(t)) - gamma(t)|. dev_e is used as an upper bound for dev*_e.
  * For each edge we scan rho_e over a log grid in (dev_e, tau_e) and keep the value with the most
    slack; the report gives the feasible rho interval.
  * S1(a)-(d): checked with exact B-rep distances (BRepExtrema) between the relevant topological
    elements, using the chosen rho_e and r_v.
  * Not checked here: E2.3 beyond what S1(d) covers, S1(e) for adjacent faces, P0 and V1(b)
    (the non-local hypotheses). The result is therefore "local hypotheses hold on samples",
    not a certificate.
"""
import sys, json, math
import numpy as np
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_VERTEX, TopAbs_IN, TopAbs_FORWARD, TopAbs_REVERSED
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepLProp import BRepLProp_SLProps, BRepLProp_CLProps
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Vec2d
from OCP.TopExp import TopExp

N = 200


def V(p):
    return np.array([p.X(), p.Y(), p.Z()])


def explore(s, kind, cast):
    out, ex = [], TopExp_Explorer(s, kind)
    while ex.More():
        out.append(cast(ex.Current())); ex.Next()
    return out


def unique(items):
    u = []
    for x in items:
        if not any(x.IsSame(y) for y in u):
            u.append(x)
    return u


def index_of(lst, x):
    for i, y in enumerate(lst):
        if y.IsSame(x):
            return i
    raise KeyError


class Model:
    def __init__(self, shape):
        self.s = shape
        self.F = unique(explore(shape, TopAbs_FACE, TopoDS.Face))
        self.E = [e for e in unique(explore(shape, TopAbs_EDGE, TopoDS.Edge)) if not BRep_Tool.Degenerated_s(e)]
        self.Vx = unique(explore(shape, TopAbs_VERTEX, TopoDS.Vertex))
        # oriented uses of each edge in faces (a seam edge appears twice in one face)
        self.uses = [[] for _ in self.E]
        for fi, f in enumerate(self.F):
            for oe in explore(f, TopAbs_EDGE, TopoDS.Edge):
                if BRep_Tool.Degenerated_s(oe):
                    continue
                self.uses[index_of(self.E, oe)].append((fi, oe))
        self.ev = []
        for e in self.E:
            v0, v1 = TopExp.FirstVertex_s(e), TopExp.LastVertex_s(e)
            self.ev.append((index_of(self.Vx, v0), index_of(self.Vx, v1)))
        self.fv = [set(index_of(self.Vx, v) for v in explore(f, TopAbs_VERTEX, TopoDS.Vertex)) for f in self.F]
        self.fe = [set(index_of(self.E, e) for e in explore(f, TopAbs_EDGE, TopoDS.Edge) if not BRep_Tool.Degenerated_s(e)) for f in self.F]
        self.p = [V(BRep_Tool.Pnt_s(v)) for v in self.Vx]
        self.tv = [BRep_Tool.Tolerance_s(v) for v in self.Vx]
        self.te = [BRep_Tool.Tolerance_s(e) for e in self.E]
        self.tf = [BRep_Tool.Tolerance_s(f) for f in self.F]


def surf_props(f, u, v):
    pr = BRepLProp_SLProps(BRepAdaptor_Surface(f), u, v, 2, 1e-12)
    n = V(pr.Normal()) if pr.IsNormalDefined() else None
    k = max(abs(pr.MaxCurvature()), abs(pr.MinCurvature())) if pr.IsCurvatureDefined() else 0.0
    return n, k


def edge_samples(M, ei):
    """Sample one edge: gamma, tangent, curvature, and for each face use the boundary point,
    deviation, inward in-plane tangent u_f, surface curvature k_f and out-of-plane angle psi_f."""
    e = M.E[ei]
    c = BRepAdaptor_Curve(e)
    a, b = c.FirstParameter(), c.LastParameter()
    ts = np.linspace(a, b, N)
    G, T, K = [], [], []
    for t in ts:
        p, d1 = gp_Pnt(), gp_Vec()
        c.D1(t, p, d1)
        G.append(V(p)); tv = V(d1); T.append(tv / np.linalg.norm(tv))
        pr = BRepLProp_CLProps(c, t, 2, 1e-12)
        K.append(pr.Curvature())
    G, T, K = np.array(G), np.array(T), np.array(K)
    sides = []
    for fi, oe in M.uses[ei]:
        f = M.F[fi]
        S = BRepAdaptor_Surface(f)
        pc = BRepAdaptor_Curve2d(oe, f)
        umin, umax, vmin, vmax = S.FirstUParameter(), S.LastUParameter(), S.FirstVParameter(), S.LastVParameter()
        span = max(1e-9, min(abs(umax - umin) if math.isfinite(umax - umin) else 1.0,
                             abs(vmax - vmin) if math.isfinite(vmax - vmin) else 1.0))
        dev, U, KF, PSI, B = [], [], [], [], []
        for i, t in enumerate(ts):
            uv, duv = gp_Pnt2d(), gp_Vec2d()
            pc.D1(t, uv, duv)
            P, Su, Sv = gp_Pnt(), gp_Vec(), gp_Vec()
            S.D1(uv.X(), uv.Y(), P, Su, Sv)
            dev.append(np.linalg.norm(V(P) - G[i])); B.append(V(P))
            nuv = np.array([-duv.Y(), duv.X()])
            nuv /= max(np.linalg.norm(nuv), 1e-300)
            h = 1e-4 * span
            q = gp_Pnt2d(uv.X() + h * nuv[0], uv.Y() + h * nuv[1])
            st = BRepClass_FaceClassifier(f, q, 1e-9).State()
            sgn = 1.0 if st == TopAbs_IN else -1.0
            d3 = sgn * (nuv[0] * V(Su) + nuv[1] * V(Sv))
            d3 = d3 - (d3 @ T[i]) * T[i]
            U.append(d3 / np.linalg.norm(d3))
            n, k = surf_props(f, uv.X(), uv.Y())
            KF.append(k)
            PSI.append(math.asin(min(1.0, abs(n @ T[i]))) if n is not None else 0.0)
        sides.append(dict(face=fi, B=np.array(B), dev=np.array(dev), u=np.array(U), k=np.array(KF), psi=np.array(PSI)))
    # arc length
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(G, axis=0), axis=1))])
    return dict(G=G, T=T, K=K, s=s, sides=sides)


def edge_reach(sm):
    """Sampled estimate of reach(gamma): min of 1/max curvature and half the smallest distance
    between samples that are far apart along the curve (a double-normal proxy)."""
    G, s, K = sm["G"], sm["s"], sm["K"]
    kmax = K.max()
    r1 = 1 / kmax if kmax > 1e-12 else np.inf
    sep = math.pi / kmax if kmax > 1e-12 else np.inf
    if not math.isfinite(sep) or sep >= s[-1]:
        return r1
    D = np.linalg.norm(G[:, None] - G[None], axis=2)
    ds = np.abs(s[:, None] - s[None])
    if np.linalg.norm(G[0] - G[-1]) < 1e-9 * max(1.0, s[-1]):   # closed edge: cyclic arc length
        ds = np.minimum(ds, s[-1] - ds)
    far = ds >= sep
    r2 = D[far].min() / 2 if far.any() else np.inf
    return min(r1, r2)


def eps_angle(dev, k, rho):
    mu = 1 - rho * k
    if mu <= 0:
        return math.pi / 2
    ell = (dev + math.sqrt(dev * dev + mu * rho * rho)) / mu
    return math.asin(min(1.0, (dev + k * ell * ell / 2) / rho))


def exit_dir(w, u, r):
    """Exit point of the line w + s u (s >= 0, in the normal plane, centre 0) from the circle of radius r.
    Returns the unit direction of the exit point, or None if |w| >= r."""
    if np.linalg.norm(w) >= r:
        return None
    b = w @ u
    s = -b + math.sqrt(b * b - (w @ w) + r * r)
    k = w + s * u
    nk = np.linalg.norm(k)
    if not (nk > 0 and math.isfinite(nk)):
        return None
    return k / nk


def e3_actual(sm, sides, idx, r_in, kf):
    """E3': at every sample, the true exit points of the two face sections on the circle of radius r
    around gamma(t) are separated by more than the curvature uncertainty. The section of face f is
    within eta = k_f ell^2 / 2 of its tangent line inside the disk, ell = arc-length bound of v0.2 E2.3; the exit point therefore
    lies between the exits of the two lines offset by +-eta. Returns the minimum angular slack."""
    worst = math.inf
    for i in idx:
        r = r_in[i] if np.ndim(r_in) else r_in
        T = sm["T"][i]
        dirs, half = [], []
        for sd, k in zip(sides, kf):
            w = sd["B"][i] - sm["G"][i]; w = w - (w @ T) * T
            u = sd["u"][i]
            mu = 1 - r * k
            if mu <= 0:
                return -math.inf
            dl = np.linalg.norm(w)
            ell = (dl + math.sqrt(dl * dl + mu * r * r)) / mu
            eta = k * ell * ell / 2
            nrm = np.cross(T, u)
            c = exit_dir(w, u, r)
            lo, hi = exit_dir(w - eta * nrm, u, r), exit_dir(w + eta * nrm, u, r)
            if c is None or lo is None or hi is None:
                return -math.inf
            dirs.append(c)
            half.append(max(math.acos(np.clip(c @ lo, -1, 1)), math.acos(np.clip(c @ hi, -1, 1))))
        sep = math.acos(np.clip(dirs[0] @ dirs[1], -1, 1))
        v = sep - half[0] - half[1]
        if not math.isfinite(v):
            return -math.inf
        worst = min(worst, v)
    return worst


def vertex_angles(M, sm_all):
    """theta_v: smallest angle between outgoing edge tangents at v (each edge end counts)."""
    dirs = [[] for _ in M.Vx]
    for ei, sm in enumerate(sm_all):
        v0, v1 = M.ev[ei]
        dirs[v0].append(sm["T"][0]); dirs[v1].append(-sm["T"][-1])
    th = []
    for d in dirs:
        m = math.pi
        for i in range(len(d)):
            for j in range(i + 1, len(d)):
                m = min(m, math.acos(np.clip(d[i] @ d[j], -1, 1)))
        th.append(m)
    return th


def check(shape, name, verbose=True):
    M = Model(shape)
    sm_all = [edge_samples(M, ei) for ei in range(len(M.E))]
    theta = vertex_angles(M, sm_all)
    fails = []
    # V0: r_v must contain the edge ends and the patch corners at v
    rv_need = [0.0] * len(M.Vx)
    for ei, sm in enumerate(sm_all):
        v0, v1 = M.ev[ei]
        rv_need[v0] = max(rv_need[v0], np.linalg.norm(sm["G"][0] - M.p[v0]), *[np.linalg.norm(sd["B"][0] - M.p[v0]) for sd in sm["sides"]])
        rv_need[v1] = max(rv_need[v1], np.linalg.norm(sm["G"][-1] - M.p[v1]), *[np.linalg.norm(sd["B"][-1] - M.p[v1]) for sd in sm["sides"]])
    rv = [max(1.01 * x, 1e-3 * t) for x, t in zip(rv_need, M.tv)]
    for vi in range(len(M.Vx)):
        if not rv[vi] < M.tv[vi]:
            fails.append(("V0", f"v{vi}", f"edge ends/corners at distance {rv_need[vi]:.3g} >= tau_v {M.tv[vi]:.3g}"))
        if theta[vi] < 1e-6:
            fails.append(("V1a", f"v{vi}", "cusp vertex (theta_v = 0)"))
    rows = []
    rho = [None] * len(M.E)
    for ei, sm in enumerate(sm_all):
        te = M.te[ei]
        sides = sm["sides"]
        if len(sides) != 2:
            fails.append(("topology", f"e{ei}", f"edge used {len(sides)} times (not manifold)"))
            continue
        dev = max(sd["dev"].max() for sd in sides)
        v0, v1 = M.ev[ei]
        # samples outside the vertex balls (the edge part treated by E1-E3, stubs included)
        out = (np.linalg.norm(sm["G"] - M.p[v0], axis=1) >= rv[v0]) & (np.linalg.norm(sm["G"] - M.p[v1], axis=1) >= rv[v1])
        if not out.any():
            fails.append(("V1a", f"e{ei}", "edge lies inside its vertex balls"))
            continue
        reach = edge_reach(sm)
        alpha = np.array([math.acos(np.clip(a @ b, -1, 1)) for a, b in zip(sides[0]["u"], sides[1]["u"])])[out]
        kf = [sd["k"][out].max() / max(math.cos(sd["psi"][out].max()), 1e-12) for sd in sides]
        psi = max(sd["psi"][out].max() for sd in sides)
        # E2.2 first-order: arc-length Lipschitz constant of beta - gamma
        L = 0.0
        for sd in sides:
            # vector deviation is not stored; use |d dev / ds| as a lower proxy plus curvature term
            dd = np.abs(np.diff(sd["dev"])) / np.maximum(np.diff(sm["s"]), 1e-300)
            L = max(L, dd.max() if len(dd) else 0.0)
        kg = sm["K"][out].max()
        # vertex-side upper bound on rho: straight radial case of V1(a): tau_v > rho*sqrt(1+1/sin^2(theta/2)),
        # plus the end disk needs r_v + rho <= |gamma(a)-p_v| with the disk inside B(p_v, tau_v)
        def vtx_ok(r):
            for vi in (v0, v1):
                th = theta[vi]
                if th < 1e-6:
                    return False
                da = max(rv[vi] + r, r / math.sin(th / 2))
                if not math.hypot(da, r) < M.tv[vi]:
                    return False
            return True
        hi = min(te, reach)
        best = None
        edge_ok = False
        if dev < hi:
            for r in np.geomspace(max(dev, 1e-300) * (1 + 1e-9) if dev > 0 else hi * 1e-6, hi * (1 - 1e-9), 400):
                if not (dev < r < hi):
                    continue
                if any(r * k >= 1 for k in kf):
                    continue
                e3 = alpha.min() - eps_angle(dev, kf[0], r) - eps_angle(dev, kf[1], r)
                via = "E3"
                if e3 <= 0:
                    e3 = e3_actual(sm, sides, np.nonzero(out)[0], r, kf); via = "E3'"
                if e3 <= 0:
                    continue
                edge_ok = True
                if not vtx_ok(r):
                    continue
                slack = min(e3, 1 - r / te, 1 - dev / r)
                if best is None or slack > best[1]:
                    best = (r, slack, via)
        if best is None and edge_ok is not None:
            # A': variable radius rho(t) = (1+m) * env(t), env = 1-Lipschitz-in-slope LR envelope of dev(t)
            LR = 0.05
            devt = np.max([sd["dev"] for sd in sides], axis=0)
            ss = sm["s"]
            env = np.max(devt[None, :] - LR * np.abs(ss[:, None] - ss[None, :]), axis=1)
            idx = np.nonzero(out)[0]
            for m in np.geomspace(1e-4, 10, 120):
                rt = (1 + m) * np.maximum(env, hi * 1e-6)
                if not (rt[idx] < hi).all() or any((rt[idx] * k >= 1).any() for k in kf):
                    continue
                e3 = min(alpha[j] - eps_angle(devt[i], kf[0], rt[i]) - eps_angle(devt[i], kf[1], rt[i]) for j, i in enumerate(idx))
                via = "E3 var"
                if e3 <= 0:
                    e3 = e3_actual(sm, sides, idx, rt, kf); via = "E3' var"
                if e3 <= 0:
                    continue
                edge_ok = True
                ok = True
                for vi, end in ((v0, 0), (v1, -1)):
                    near = np.linalg.norm(sm["G"] - M.p[vi], axis=1) <= 2 * M.tv[vi]
                    near &= out
                    rend = rt[near].max() if near.any() else rt[idx[0] if end == 0 else idx[-1]]
                    th = theta[vi]
                    if th < 1e-6:
                        ok = False; break
                    da = max(rv[vi] + rend, rend / math.sin(th / 2))
                    if not math.hypot(da, rend) < M.tv[vi]:
                        ok = False; break
                if not ok:
                    continue
                slack = min(e3, (1 - rt[idx] / te).min(), m / (1 + m))
                if best is None or slack > best[1]:
                    best = (float(rt[idx].max()), slack, via)
        why = []
        if not dev < te: why.append(f"E1: dev {dev:.3g} >= tau_e {te:.3g}")
        if not dev < reach: why.append(f"E1: dev >= reach(gamma) {reach:.3g}")
        if psi >= math.pi / 2 - 1e-9: why.append("E2.1: face tangent plane contains the normal plane")
        if L + kg * dev >= 1: why.append(f"E2.2: L+kappa*dev = {L + kg*dev:.3g} >= 1")
        if best is None and not why:
            # identify which of E3 / vertex is responsible at the best E1 value
            r = math.sqrt(max(dev, 1e-300) * hi)
            if not edge_ok:
                why.append(f"E3/E3': no rho in (dev, tau_e) separates the exit points (alpha_min {math.degrees(alpha.min()):.1f} deg, tau_e/dev {te/dev:.3g})")
            else:
                why.append("V1a: no rho fits both the edge (rho>dev) and the vertex balls")
        for w in why:
            fails.append((w.split(":")[0], f"e{ei}", w))
        if best is not None and not why:
            rho[ei] = best[0]
        rows.append(dict(edge=ei, tau_e=te, dev=dev, ratio=te / dev if dev > 0 else float("inf"),
                         alpha_min_deg=math.degrees(alpha.min()), reach=reach, rho=best[0] if best else None,
                         via=best[2] if best else None))
    # S1 with exact B-rep distances
    def dist(a, b):
        d = BRepExtrema_DistShapeShape(a, b)
        return d.Value() if d.IsDone() else float("nan")
    s1 = 0
    for i in range(len(M.Vx)):
        for j in range(i + 1, len(M.Vx)):
            if np.linalg.norm(M.p[i] - M.p[j]) <= rv[i] + rv[j]:
                fails.append(("S1a", f"v{i},v{j}", "vertex regions overlap")); s1 += 1
    for i in range(len(M.E)):
        for j in range(i + 1, len(M.E)):
            if rho[i] is None or rho[j] is None or set(M.ev[i]) & set(M.ev[j]):
                continue
            d = dist(M.E[i], M.E[j])
            if d <= rho[i] + rho[j]:
                fails.append(("S1b", f"e{i},e{j}", f"tubes overlap: dist {d:.3g} <= {rho[i]+rho[j]:.3g}")); s1 += 1
    for ei in range(len(M.E)):
        if rho[ei] is None:
            continue
        for vi in range(len(M.Vx)):
            if vi in M.ev[ei]:
                continue
            d = dist(M.E[ei], M.Vx[vi])
            if d <= rv[vi] + rho[ei]:
                fails.append(("S1c", f"e{ei},v{vi}", f"dist {d:.3g} <= {rv[vi]+rho[ei]:.3g}")); s1 += 1
        for fi in range(len(M.F)):
            if ei in M.fe[fi] or set(M.ev[ei]) & M.fv[fi]:
                continue
            d = dist(M.E[ei], M.F[fi])
            if d <= rho[ei]:
                fails.append(("S1d", f"e{ei},f{fi}", f"dist {d:.3g} <= rho {rho[ei]:.3g}")); s1 += 1
    for fi in range(len(M.F)):
        for vi in range(len(M.Vx)):
            if vi in M.fv[fi]:
                continue
            d = dist(M.F[fi], M.Vx[vi])
            if d <= rv[vi]:
                fails.append(("S1d", f"f{fi},v{vi}", f"dist {d:.3g} <= r_v {rv[vi]:.3g}")); s1 += 1
    for i in range(len(M.F)):
        for j in range(i + 1, len(M.F)):
            if M.fv[i] & M.fv[j]:
                continue
            d = dist(M.F[i], M.F[j])
            if d <= 0:
                fails.append(("S1e", f"f{i},f{j}", "non-adjacent faces touch")); s1 += 1
    res = dict(name=name, faces=len(M.F), edges=len(M.E), vertices=len(M.Vx),
               tau_v=[min(M.tv), max(M.tv)], tau_e=[min(M.te), max(M.te)],
               theta_min_deg=math.degrees(min(theta)) if theta else None,
               edges_detail=rows, fails=fails, ok=not fails)
    if verbose:
        ratios = [r["ratio"] for r in rows if math.isfinite(r["ratio"])]
        print(f"== {name}: F={len(M.F)} E={len(M.E)} V={len(M.Vx)}  tau_e in [{min(M.te):.2e},{max(M.te):.2e}]"
              f"  min tau_e/dev = {min(ratios) if ratios else float('inf'):.3g}  theta_min = {res['theta_min_deg']:.1f} deg"
              f"  alpha_min = {min(r['alpha_min_deg'] for r in rows):.1f} deg")
        print("   local hypotheses + S1(a-d) on samples:", "PASS" if not fails else f"FAIL ({len(fails)})")
        seen = {}
        for f in fails:
            seen.setdefault(f[0], []).append(f)
        for k, lst in seen.items():
            print(f"   {k}: {len(lst)} x, e.g. {lst[0][1]}: {lst[0][2]}")
    return res
