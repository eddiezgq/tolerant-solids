"""Route G (graph construction) for models whose edges are all tangent (G1) -- hypothesis checker.

Construction (see notes/lemma0_v03.md, section 2''):
  Edge e between faces f, g, at parameter t, in the normal plane Pi(t) of gamma_e:
    n(t) = unit sum of the outward normals of f and g at their boundary points ("up"), m(t) = n x T ("across").
    The section of f starts at its boundary point b_f and runs to one side (sign s_f of <u_f, m>), the section of
    g to the other side. For a(t) > max(|x_f|, |x_g|), x = <b - gamma, m>, cut f's section where <. - gamma, m> = s_f a
    and g's where it is s_g a, and join the two cut points P_f, P_g by a segment. The realized edge point is the
    point of that segment with m-coordinate 0. In Pi(t) the result is a graph over the m-axis.
    G-E: |P - gamma| + k_f lambda^2 / 2 < tau_e for both cut points (lambda = length cut off along the section,
         k_f = surface curvature bound), so the segment lies in the tube (a convex disk in Pi(t)).
  Vertex v: the vertical direction n_v is the unit sum of the outward face normals at v; D is the disk of radius
    r_v around p_v in the plane through p_v normal to n_v. Inside the vertical cylinder over D, the surface is
    replaced by the cone from p_v over the loop in which the outside construction meets the cylinder wall.
    G-V1: the face normals at v make an angle < 45 deg with n_v (spread);
    G-V2: r_v is large enough that the edge strips (half-width a) of different edges are disjoint outside D:
          r_v * 2 sin(theta/2) > a_e + a_e' for the projected angle theta between any two edges at v;
    G-V3: every loop point lies in Z(v) = B(p_v, tau_v) (then the cone lies in the ball, which is convex);
          loop points are sampled: strip cut points where the edge crosses the cylinder, and patch points of the
          incident faces in the annulus r_v <= horizontal distance <= 1.1 r_v;
    G-V4: the projected edge directions at v are distinct and each face's corner bisector lies between its two
          edges, so the loop meets the edges in the cyclic order of the link of v.
  Separation (S1-type, coarse): edges with no common vertex are farther apart than tau_e + tau_e'; a vertex ball
    and a non-incident edge are farther apart than tau_v + tau_e.
All checks are sampled, double precision. Not checked: that the patches near v are graphs over the plane of D
beyond the normal-spread test, and P0-type global embedding of the patches.
"""
import sys, math, json
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve2d
from OCP.BRepLProp import BRepLProp_SLProps
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.TopAbs import TopAbs_IN, TopAbs_REVERSED
from OCP.gp import gp_Pnt2d

TANGENT_DEG = 5.0      # an edge counts as tangent if its faces' inward tangents are within this of opposite


def outward_normal(face, u, v):
    pr = BRepLProp_SLProps(BRepAdaptor_Surface(face), u, v, 1, 1e-12)
    n = L.V(pr.Normal())
    return -n if face.Orientation() == TopAbs_REVERSED else n


def face_normal_at(face, oe, t):
    """Outward normal of face at the pcurve point of oe at t. At a singular point of the parametrization (e.g. a
    sphere pole, where Su x Sv = 0 and the computed normal can flip), take the normal slightly inside the edge."""
    from OCP.gp import gp_Pnt, gp_Vec
    pc = BRepAdaptor_Curve2d(oe, face)
    S = BRepAdaptor_Surface(face)
    t0, t1 = pc.FirstParameter(), pc.LastParameter()
    for frac in (0.0, 1e-4, 1e-3, 1e-2):
        tt = t + frac * (t1 - t0) * (1 if abs(t - t0) <= abs(t - t1) else -1)
        uv = pc.Value(tt)
        P, Su, Sv = gp_Pnt(), gp_Vec(), gp_Vec(); S.D1(uv.X(), uv.Y(), P, Su, Sv)
        nu, nv_ = np.linalg.norm(L.V(Su)), np.linalg.norm(L.V(Sv))
        if min(nu, nv_) > 1e-8 * max(nu, nv_, 1e-300):     # not a degenerate (pole) point
            return outward_normal(face, uv.X(), uv.Y())
    return outward_normal(face, uv.X(), uv.Y())


def check(shape, name, verbose=True):
    M = L.Model(shape)
    # samples: uniform along the edge, plus dense near each end (within 5 tau_v of the vertex in arc length)
    from OCP.BRepAdaptor import BRepAdaptor_Curve
    from OCP.gp import gp_Pnt, gp_Vec
    ts_all = []
    for i, e in enumerate(M.E):
        c = BRepAdaptor_Curve(e); t0, t1 = c.FirstParameter(), c.LastParameter()
        parts = [np.linspace(t0, t1, L.N)]
        for tv_end, vi, sgn in ((t0, M.ev[i][0], 1), (t1, M.ev[i][1], -1)):
            p_, d_ = gp_Pnt(), gp_Vec(); c.D1(tv_end, p_, d_)
            dt = min(5 * M.tv[vi] / max(d_.Magnitude(), 1e-300), (t1 - t0) / 4)
            parts.append(tv_end + sgn * np.geomspace(1e-4, 1.0, 80) * dt)
        ts_all.append(np.unique(np.concatenate(parts)))
    sm = [L.edge_samples(M, i, ts_all[i]) for i in range(len(M.E))]
    NS = [len(t) for t in ts_all]
    res = dict(name=name, fails=[])
    # applicability: every edge tangent
    worst_tan = 0.0
    for i, s in enumerate(sm):
        sd = s["sides"]
        if len(sd) != 2:
            return dict(name=name, applicable=False, why="non-manifold edge")
        # tangency is judged on the uniform samples away from the ends (near a sphere pole the computed in-plane
        # tangent is unreliable)
        uni = np.isin(ts_all[i], np.linspace(ts_all[i][0], ts_all[i][-1], L.N))
        for a, b in list(zip(sd[0]["u"][uni], sd[1]["u"][uni]))[2:-2]:
            worst_tan = max(worst_tan, 180 - math.degrees(math.acos(np.clip(a @ b, -1, 1))))
    if worst_tan > TANGENT_DEG:
        res.update(applicable=False, why=f"not all edges tangent (worst {worst_tan:.1f} deg)")
        if verbose:
            print(f"== {name}: route G not applicable ({res['why']})")
        return res
    res["applicable"] = True
    # normals along each edge, per side
    # vertex frames
    nv = []
    spread = []
    for vi in range(len(M.Vx)):
        ns = []
        for ei in range(len(M.E)):
            for end, vv in ((0, M.ev[ei][0]), (-1, M.ev[ei][1])):
                if vv != vi:
                    continue
                for fi, oe in M.uses[ei]:
                    ns.append(face_normal_at(M.F[fi], oe, ts_all[ei][end]))
        n = np.sum(ns, axis=0); n /= np.linalg.norm(n)
        nv.append(n)
        spread.append(max(math.degrees(math.acos(np.clip(x @ n, -1, 1))) for x in ns))
    res["G_V1_max_spread_deg"] = max(spread)
    if max(spread) >= 45:
        res["fails"].append("G-V1")
    # edge part: a(t) and cut points
    a_of = []
    e_margin = math.inf
    for ei in range(len(M.E)):
        s = sm[ei]; T = s["T"]; G = s["G"]
        sides = s["sides"]
        A = np.zeros(NS[ei]); Pc = [None] * NS[ei]; Cuts = [None] * NS[ei]
        for i in range(NS[ei]):
            # sides[k] was sampled from M.uses[ei][k] (same order; a seam gives two uses of one face)
            ns = [face_normal_at(M.F[fi], oe, ts_all[ei][i]) for fi, oe in M.uses[ei]]
            n = ns[0] + ns[1]; n -= (n @ T[i]) * T[i]; n /= np.linalg.norm(n)
            m = np.cross(n, T[i])
            xs, pts = [], []
            for sd in sides:
                w = sd["B"][i] - G[i]; w -= (w @ T[i]) * T[i]
                xs.append(w @ m)
            a = max(abs(x) for x in xs) * (1 + 1e-3) + 1e-6 * M.te[ei]
            A[i] = a
            cut = []
            for sd, x in zip(sides, xs):
                u = sd["u"][i]; um = u @ m
                if abs(um) < 1e-9:
                    cut = None; break
                sgn = 1.0 if um > 0 else -1.0
                lam = (sgn * a - x) / um
                if lam < 0:
                    cut = None; break
                w = sd["B"][i] - G[i]; w -= (w @ T[i]) * T[i]
                P = w + lam * u
                k = sd["k"][i]
                cut.append((np.linalg.norm(P) + k * lam * lam / 2, sgn, G[i] + P, k * lam * lam / 2))
            if cut is None or cut[0][1] == cut[1][1]:
                e_margin = -math.inf; continue
            # only the part of the edge outside the vertex cylinders is constrained; vertex part uses the cone
            e_margin_i = min((M.te[ei] - c[0]) / M.te[ei] for c in cut)
            Pc[i] = e_margin_i
            Cuts[i] = [(c[2], c[3]) for c in cut]      # 3D cut points and their curvature slack
        a_of.append(A)
        s["A"] = A; s["Emargin"] = Pc; s["Cuts"] = Cuts
    # vertex radius r_v (G-V2), then edge margins outside D, loop (G-V3), order (G-V4)
    rv = []
    diag = []
    order_ok = True
    for vi in range(len(M.Vx)):
        n = nv[vi]
        dirs, hds, As, faces_of = [], [], [], []
        corner = 0.0
        for ei in range(len(M.E)):
            for end, vv in ((0, M.ev[ei][0]), (-1, M.ev[ei][1])):
                if vv != vi:
                    continue
                d = sm[ei]["T"][end] * (1 if end == 0 else -1)
                d = d - (d @ n) * n; d /= np.linalg.norm(d)
                dirs.append(d)
                half = slice(0, NS[ei] // 2) if end == 0 else slice(NS[ei] // 2, NS[ei])
                Gs = sm[ei]["G"][half] - M.p[vi]
                hds.append(np.linalg.norm(Gs - np.outer(Gs @ n, n), axis=1))
                As.append(a_of[ei][half])
                faces_of.append(sorted(u[0] for u in M.uses[ei]))
                # the edge's end point and the patch corners must lie over D (the strips start outside D)
                for P in [sm[ei]["G"][end]] + [sd["B"][end] for sd in sm[ei]["sides"]]:
                    q = P - M.p[vi]
                    corner = max(corner, np.linalg.norm(q - (q @ n) * n))
        # smallest r >= 1.01 * corner such that, for every pair of edges at v, the strips are disjoint outside D:
        # A_i(r) + A_j(r) < 2 r sin(theta/2) / 1.5, with A_i(r) = max strip half-width over samples at
        # horizontal distance >= r (conservative: the right side is taken at the smallest radius r)
        lo = max(1.01 * corner, 1e-9 * M.tv[vi])
        cands = np.geomspace(lo, max(2 * M.tv[vi], 2 * lo), 300)
        r = math.inf
        for rr in cands:
            ok = True
            for i in range(len(dirs)):
                for j in range(i + 1, len(dirs)):
                    th = math.acos(np.clip(dirs[i] @ dirs[j], -1, 1))
                    if th < 1e-6:
                        ok = False; break
                    Ai = As[i][hds[i] >= rr].max() if (hds[i] >= rr).any() else 0.0
                    Aj = As[j][hds[j] >= rr].max() if (hds[j] >= rr).any() else 0.0
                    if not (1.5 * (Ai + Aj) < 2 * rr * math.sin(th / 2)):
                        ok = False; break
                if not ok:
                    break
            if ok:
                r = rr; break
        rv.append(r)
        diag.append(dict(v=vi, tau_v=M.tv[vi], corner=corner, r=r,
                         A_near=[float(As[k][hds[k] <= 2 * M.tv[vi]].max()) if (hds[k] <= 2 * M.tv[vi]).any() else 0.0 for k in range(len(As))],
                         theta_deg=[math.degrees(math.acos(np.clip(dirs[i] @ dirs[j], -1, 1))) for i in range(len(dirs)) for j in range(i + 1, len(dirs))]))
        # G-V4: angular order -- each face lies between its two edges at v
        e1 = dirs[0]; e2 = np.cross(n, e1)
        ang = [math.atan2(d @ e2, d @ e1) % (2 * math.pi) for d in dirs]
        order = sorted(range(len(dirs)), key=lambda k: ang[k])
        for k in range(len(order)):
            fa, fb = set(faces_of[order[k]]), set(faces_of[order[(k + 1) % len(order)]])
            if not (fa & fb):
                order_ok = False
    res["G_V4_order"] = order_ok
    res["vertex_diag"] = diag
    if not order_ok:
        res["fails"].append("G-V4")
    # edge margins outside the vertex cylinders
    em = math.inf
    for ei in range(len(M.E)):
        G = sm[ei]["G"]
        for i in range(NS[ei]):
            inside = False
            for vi in M.ev[ei]:
                d = G[i] - M.p[vi]
                if np.linalg.norm(d - (d @ nv[vi]) * nv[vi]) <= rv[vi]:
                    inside = True
            if inside:
                continue
            v = sm[ei]["Emargin"][i]
            em = min(em, -math.inf if v is None else v)
    res["G_E_margin"] = em
    if not em > 0:
        res["fails"].append("G-E")
    # G-V3: loop points
    vm = math.inf
    for vi in range(len(M.Vx)):
        n, r = nv[vi], rv[vi]
        pts = []
        for ei in range(len(M.E)):
            if vi not in M.ev[ei]:
                continue
            G = sm[ei]["G"]
            hd = np.array([np.linalg.norm((g - M.p[vi]) - ((g - M.p[vi]) @ n) * n) for g in G])
            # samples of the edge just outside the cylinder: the strip there lies within its cut points' distance
            idx = np.nonzero((hd >= r) & (hd <= 1.1 * r + 1e-12))[0]
            for i in idx:
                cuts = sm[ei]["Cuts"][i]
                if cuts is None:
                    pts.append(math.inf); continue
                # the strip in this normal plane is the segment between the two cut points (convex ball)
                for P, slack in cuts:
                    pts.append(np.linalg.norm(P - M.p[vi]) + slack)
        # patch points of incident faces in the annulus: sample around each corner in UV
        for ei in range(len(M.E)):
            for end, vv in ((0, M.ev[ei][0]), (-1, M.ev[ei][1])):
                if vv != vi:
                    continue
                for fi, oe in M.uses[ei]:
                    f = M.F[fi]; S = BRepAdaptor_Surface(f)
                    pc = BRepAdaptor_Curve2d(oe, f)
                    uv = pc.Value(ts_all[ei][end])
                    from OCP.gp import gp_Pnt, gp_Vec
                    P, Su, Sv = gp_Pnt(), gp_Vec(), gp_Vec(); S.D1(uv.X(), uv.Y(), P, Su, Sv)
                    sp = max(min(np.linalg.norm(L.V(Su)), np.linalg.norm(L.V(Sv))), 1e-12)
                    R = 1.3 * r / sp
                    for rr in np.linspace(0.2, 1.0, 9) * R:
                        for ph in np.linspace(0, 2 * math.pi, 48, endpoint=False):
                            q = gp_Pnt2d(uv.X() + rr * math.cos(ph), uv.Y() + rr * math.sin(ph))
                            if BRepClass_FaceClassifier(f, q, 1e-9).State() != TopAbs_IN:
                                continue
                            x = L.V(S.Value(q.X(), q.Y()))
                            d = x - M.p[vi]
                            h = np.linalg.norm(d - (d @ n) * n)
                            if r <= h <= 1.1 * r:
                                pts.append(np.linalg.norm(d))
        if pts:
            vm = min(vm, (M.tv[vi] - max(pts)) / M.tv[vi])
    res["G_V3_margin"] = vm
    res["r_over_tau_v_max"] = max(r / t for r, t in zip(rv, M.tv))
    if not vm > 0:
        res["fails"].append("G-V3")
    # separation (coarse)
    def dist(a, b):
        d = BRepExtrema_DistShapeShape(a, b); return d.Value() if d.IsDone() else float("nan")
    sep = math.inf
    for i in range(len(M.E)):
        for j in range(i + 1, len(M.E)):
            if set(M.ev[i]) & set(M.ev[j]):
                continue
            sep = min(sep, dist(M.E[i], M.E[j]) / (M.te[i] + M.te[j]) - 1)
    for ei in range(len(M.E)):
        for vi in range(len(M.Vx)):
            if vi in M.ev[ei]:
                continue
            sep = min(sep, dist(M.E[ei], M.Vx[vi]) / (M.te[ei] + M.tv[vi]) - 1)
    res["S_margin"] = sep
    if not sep > 0:
        res["fails"].append("S")
    res["ok"] = not res["fails"]
    if verbose:
        print(f"== {name}: route G {'PASS' if res['ok'] else 'FAIL ' + ','.join(res['fails'])}  "
              f"spread {max(spread):.1f} deg; edge margin {em:.3f}; loop-in-ball margin {vm:.3f}; "
              f"r_v/tau_v <= {res['r_over_tau_v_max']:.2f}; order {order_ok}; separation {sep:.2f}")
    return res


if __name__ == "__main__":
    import lemma0_check_run as R
    names = sys.argv[1:] or ["sloppy filleted box g=0.001", "filleted box r2", "sloppy box g=0.01"]
    out = [check(R.PARTS[n](), n) for n in names]
    json.dump(out, open("../results/route_g_result.json", "w"), indent=1, default=float)
