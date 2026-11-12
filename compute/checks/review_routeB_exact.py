"""Independent, exact-arithmetic check of Proposition B (re-intersection), B1-B4, notes/lemma0_v03.md Section 2.

Written for the review notes/reviews/lemma0_v03_code_review.md; does not use reintersect_check.py.
Data: review_occ_extract.extract (stored doubles -> Fraction). All comparisons are exact.

  c_v   exact common point of the three face planes at v (Cramer's rule on N_i . x = N_i . O_i).
  B1    |c_v - p_v|^2 < tau_v^2.
  B2    l_e = [c_v0, c_v1] lies in the open capsule N_{tau_e}(gamma_e): distance to a segment is convex, so it
        suffices that both end points are inside.
  B3    P~_f in Z(f). Let K_f be the polygon of the start points of the boundary chords of P_f (corner gaps
        dropped). Every point of K_f is within (max corner gap + max pole deviation of the B-spline pcurves)
        of the true boundary loop of P_f or inside it, hence in N_{tau_f}(P_f) when that bound is < tau_f
        (checked). If K_f is convex, P~_f is covered by K_f and the convex pieces C_j = P~_f minus the open
        inner half-plane of side j of K_f; each C_j is checked to lie in the capsule of the edge of side j
        (all its vertices inside: convexity), or, failing that, in the union of that capsule and the end balls
        after splitting C_j (reported if needed).
  B4    every P~_f strictly convex (hence simple), and for every pair of faces the exact intersection
        P~_f cap P~_g equals the expected common edge / common vertex / empty set.
"""
import sys, os, math, json
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, ".."))
from review_occ_extract import extract, add, sub, mul, dot, cross
from review_lemmaO_exact import prepare, pt_seg_d2, n2, orient2, drop_axis, isqrt_frac


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def solve3(rows, rhs):
    D0 = det3(rows)
    assert D0 != 0
    return tuple(det3([[rhs[r] if c == k else rows[r][c] for c in range(3)] for r in range(3)]) / D0 for k in range(3))


def strictly_convex(P, ax):
    s = [orient2(P[i - 1], P[i], P[(i + 1) % len(P)], ax) for i in range(len(P))]
    return all(x > 0 for x in s) or all(x < 0 for x in s), (1 if s[0] > 0 else -1)


def clip_outside(P, a, b, sgn, ax):
    """P (convex) intersected with the closed half-plane on the OUTER side of the directed line a->b, where the
    polygon K lies on the side orient2(a, b, x) * sgn >= 0. Sutherland-Hodgman, exact."""
    side = lambda x: -sgn * orient2(a, b, x, ax)   # >= 0 : outside-or-on
    out = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]
        sp, sq = side(p), side(q)
        if sp >= 0: out.append(p)
        if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
            t = sp / (sp - sq)
            out.append(add(p, mul(t, sub(q, p))))
    return out


def plane_section(P, N, c0):
    """Exact P cap {x : N.x = c0} for a convex planar polygon P not in that plane: list of points (0, 1 or 2)."""
    s = [dot(N, x) - c0 for x in P]
    pts = []
    for i in range(len(P)):
        j = (i + 1) % len(P)
        if s[i] == 0: pts.append(P[i])
        if (s[i] > 0 and s[j] < 0) or (s[i] < 0 and s[j] > 0):
            t = s[i] / (s[i] - s[j]); pts.append(add(P[i], mul(t, sub(P[j], P[i]))))
    uniq = []
    for p in pts:
        if p not in uniq: uniq.append(p)
    return uniq


def clip_lin(P, phi, c0, ge=True):
    """Convex polygon (or segment, or point) P cut by the closed half-space phi(x) >= c0 (ge) or <= c0, exact."""
    side = (lambda x: phi(x) - c0) if ge else (lambda x: c0 - phi(x))
    if len(P) <= 2:
        if len(P) == 1:
            return P if side(P[0]) >= 0 else []
        a, b = P; sa, sb = side(a), side(b)
        if sa >= 0 and sb >= 0: return [a, b]
        if sa < 0 and sb < 0: return []
        m = add(a, mul(sa / (sa - sb), sub(b, a)))
        return [a, m] if sa >= 0 else [m, b]
    out = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]
        sp, sq = side(p), side(q)
        if sp >= 0: out.append(p)
        if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
            out.append(add(p, mul(sp / (sp - sq), sub(q, p))))
    return out


def cover_convex(P, e, Vt, ngrid=400):
    """Exact proof that the convex set conv(P) lies in Z(e) = capsule(gamma_e, tau_e) U B(p_v0) U B(p_v1).
    Either conv(P) is in the capsule, or it is cut at rational values t1 <= t2 of the edge parameter
    s(x) = (x - g0).(g1 - g0)/|g1 - g0|^2 into three convex pieces lying in B(p_v0), the capsule, B(p_v1).
    Returns (ok, capsule margin of the middle piece, description)."""
    g0, g1 = e["gamma"]; v0, v1 = e["v"]
    r2 = e["tol"] ** 2
    inC = lambda Q: all(pt_seg_d2(x, g0, g1) < r2 for x in Q)
    inB = lambda Q, v: all(n2(sub(x, Vt[v]["p"])) < Vt[v]["tol"] ** 2 for x in Q)
    marg = lambda Q: 1 - math.sqrt(max(pt_seg_d2(x, g0, g1) for x in Q) / r2) if Q else math.inf
    if inC(P):
        return True, marg(P), "in capsule"
    dg = sub(g1, g0); L2 = n2(dg)
    phi = lambda x: dot(sub(x, g0), dg) / L2
    s_lo, s_hi = min(phi(x) for x in P), max(phi(x) for x in P)
    # t1: largest grid value with {s <= t1} in B(v0); t2: smallest with {s >= t2} in B(v1)
    r0 = Vt[v0]["tol"] / isqrt_frac(L2, lo=True); r1 = Vt[v1]["tol"] / isqrt_frac(L2, lo=True)
    t1 = s_lo
    for k in range(ngrid + 1):
        t = s_lo + Fr(k, ngrid) * 2 * r0
        Q = clip_lin(P, phi, t, ge=False)
        if Q and not inB(Q, v0): break
        t1 = t
    t2 = s_hi
    for k in range(ngrid + 1):
        t = s_hi - Fr(k, ngrid) * 2 * r1
        Q = clip_lin(P, phi, t, ge=True)
        if Q and not inB(Q, v1): break
        t2 = t
    if t1 > t2:
        t1 = t2
    Mid = clip_lin(clip_lin(P, phi, t1, ge=True), phi, t2, ge=False)
    ok = (not clip_lin(P, phi, t1, ge=False) or inB(clip_lin(P, phi, t1, ge=False), v0)) and \
         (not clip_lin(P, phi, t2, ge=True) or inB(clip_lin(P, phi, t2, ge=True), v1)) and (not Mid or inC(Mid))
    return ok, marg(Mid), f"split at s = {float(t1):.3g}, {float(t2):.3g} (edge parameter)"


def run(name, shape):
    D = prepare(extract(shape))
    F, E, Vt = D["faces"], D["edges"], D["verts"]
    res = dict(name=name)
    vfaces = [set() for _ in Vt]
    for fi, f in enumerate(F):
        for u in f["wires"][0]:
            for vi in E[u["edge"]]["v"]:
                vfaces[vi].add(fi)
    assert all(len(s) == 3 for s in vfaces), "vertex not of degree 3"
    c = []
    for vi, fs in enumerate(vfaces):
        fs = sorted(fs)
        c.append(solve3([F[k]["N"] for k in fs], [dot(F[k]["N"], F[k]["O"]) for k in fs]))
    # B1
    b1 = [(1 - math.sqrt(n2(sub(c[v], Vt[v]["p"])) / Vt[v]["tol"] ** 2), n2(sub(c[v], Vt[v]["p"])) < Vt[v]["tol"] ** 2) for v in range(len(Vt))]
    res["B1_ok"] = all(x[1] for x in b1); res["B1_margin"] = min(x[0] for x in b1)
    # B2
    b2 = []
    for ei, e in enumerate(E):
        ok, m, how = cover_convex([c[e["v"][0]], c[e["v"][1]]], e, Vt)
        b2.append((m, ok, ei, how))
    res["B2_ok"] = all(x[1] for x in b2); res["B2_capsule_margin"] = min(x[0] for x in b2)
    res["B2_detail"] = [x for x in b2 if not x[1] or x[3] != "in capsule"]
    res["B2_binding_edge"] = min(b2)[2]
    # new face polygons in wire order
    Pn = []
    for fi, f in enumerate(F):
        order = []
        for u in f["wires"][0]:
            e = E[u["edge"]]
            order.append(e["v"][1] if u["rev"] else e["v"][0])
        Pn.append((order, [c[v] for v in order]))
        for v in order:
            assert dot(sub(c[v], f["O"]), f["N"]) == 0
    # B3
    b3_ok, b3_margin, b3_detail = True, math.inf, []
    for fi, f in enumerate(F):
        ax = f["ax"]
        W = f["wires"][0]
        K = []
        for u in W:
            a, b = u["beta"]
            K.append(b if u["rev"] else a)
        convK, sgn = strictly_convex(K, ax)
        # K within (gap + delta) of the true boundary loop of P_f, side by side
        bound2 = Fr(0)
        for i, u in enumerate(W):
            a, b = u["beta"]
            if u["rev"]: a, b = b, a
            nxt = K[(i + 1) % len(K)]
            gap = isqrt_frac(n2(sub(nxt, b)), lo=False)
            dl = max(isqrt_frac(p["delta2"], lo=False) for p in f["pieces"] if p.get("use") is u)
            bound2 = max(bound2, (gap + dl) ** 2)
        near_ok = bound2 < f["tol"] ** 2
        if not (convK and near_ok):
            b3_ok = False; b3_detail.append((fi, "K not convex" if not convK else "K too far from P_f")); continue
        order, P = Pn[fi]
        for j, u in enumerate(W):
            Cj = clip_outside(P, K[j], K[(j + 1) % len(K)], sgn, ax)
            if not Cj:
                continue
            e = E[u["edge"]]
            ok, m, how = cover_convex(Cj, e, Vt)
            b3_margin = min(b3_margin, m)
            if not ok or how != "in capsule":
                b3_detail.append((fi, j, u["edge"], ok, how))
            if not ok:
                b3_ok = False
    res["B3_ok"] = b3_ok; res["B3_margin_pieces"] = b3_margin; res["B3_detail"] = b3_detail
    # B4
    b4_ok, b4_detail = True, []
    for fi, f in enumerate(F):
        conv, _ = strictly_convex(Pn[fi][1], f["ax"])
        if not conv:
            b4_ok = False; b4_detail.append((fi, "new face polygon not strictly convex"))
    edge_of = {}
    for ei, e in enumerate(E):
        edge_of[frozenset(e["faces"])] = ei
    for fi in range(len(F)):
        for gi in range(fi + 1, len(F)):
            Pf, Pg = Pn[fi][1], Pn[gi][1]
            Nf, Ng = F[fi]["N"], F[gi]["N"]
            d = cross(Nf, Ng)
            shared_v = set(Pn[fi][0]) & set(Pn[gi][0])
            if n2(d) == 0:
                same = dot(Ng, F[fi]["O"]) == dot(Ng, F[gi]["O"])
                if same:
                    b4_ok = False; b4_detail.append((fi, gi, "coplanar faces (not handled)"))
                continue
            If = plane_section(Pf, Ng, dot(Ng, F[gi]["O"]))
            Ig = plane_section(Pg, Nf, dot(Nf, F[fi]["O"]))
            # both are point sets on the line Pi_f cap Pi_g; parametrize by d
            def rng(I):
                if not I: return None
                ts = [dot(d, x) for x in I]; return (min(ts), max(ts))
            rf, rg = rng(If), rng(Ig)
            inter = None
            if rf and rg:
                lo, hi = max(rf[0], rg[0]), min(rf[1], rg[1])
                if lo <= hi: inter = (lo, hi)
            if frozenset((fi, gi)) in edge_of:
                e = E[edge_of[frozenset((fi, gi))]]
                exp = tuple(sorted((dot(d, c[e["v"][0]]), dot(d, c[e["v"][1]]))))
            elif len(shared_v) == 1:
                v = shared_v.pop(); exp = (dot(d, c[v]), dot(d, c[v]))
            else:
                exp = None
            if inter != exp:
                b4_ok = False; b4_detail.append((fi, gi, "intersection differs", str(inter), str(exp)))
    # the c_v are distinct
    b4_ok = b4_ok and len(set(c)) == len(c)
    res["B4_ok"] = b4_ok; res["B4_detail"] = b4_detail
    res["c_v"] = [[float(x) for x in p] for p in c]
    return res


if __name__ == "__main__":
    import lemma0_check_run as R
    names = sys.argv[1:] or ["sloppy box g=0.01"]
    out = []
    for n in names:
        r = run(n, R.PARTS[n]())
        out.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != "c_v"}, indent=1, default=str))
    json.dump(out, open(os.path.join(HERE, "review_routeB_exact_result.json"), "w"), indent=1, default=str)
