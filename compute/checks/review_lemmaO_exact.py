"""Independent, exact-arithmetic check of the hypotheses O0-O4 of Lemma O (notes/lemma0_v03.md, Section 3).

Written for the review notes/reviews/lemma0_v03_code_review.md. It does not use obstruction_check.py or
lemma0_check.Model; the data come from review_occ_extract.extract (stored doubles -> Fraction).

Exactness:
  * All points, planes, tolerances are the exact rationals of the stored doubles.
  * Pcurves stored as Geom2d_Line: beta is the exact segment between the images of the range end points.
  * Pcurves stored as non-rational clamped Geom2d_BSplineCurve: beta lies in the convex hull of the images of
    its poles and starts/ends at the first/last pole. Every condition is checked on that hull:
      - O0: all poles within tau_e of gamma_e (distance to a convex set is convex, so the hull is inside);
      - O1: the boundary of P_f is replaced by the chord polygon, and every distance to a chord is reduced
        by delta_i = max distance of the poles of use i from its chord (a rational upper bound of it).
  * Unit vectors and the angle alpha are avoided: J_f is taken as X + [-s_f, s_f] M_f with M_f = d x N_f
    (d = N_f x N_g), rational, and O1/O2 are checked on that segment, which contains X + [-rho, rho] m_f as
    soon as s_f^2 |M_f|^2 >= rho^2 (checked). O4 is checked with rational bounds on the two square roots.
  * Every comparison of distances is a comparison of squared rationals.
The only non-exact inputs are the identification of which B-rep entity is which (OCC topology), which is
not a numerical question.
"""
import sys, os, math, json
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, ".."))
from review_occ_extract import extract, add, sub, mul, dot, cross
from OCP.Geom2d import Geom2d_BSplineCurve


# ---------- exact helpers ----------
def isqrt_frac(q, lo=True, bits=80):
    """Rational lower (lo=True) or upper bound of sqrt(q), q >= 0 rational, relative error ~ 2^-bits."""
    if q == 0:
        return Fr(0)
    s = 2 ** bits
    n = math.isqrt(q.numerator * s * s // q.denominator)   # floor(sqrt(q) * s) up to floor in the division
    r = Fr(n, s)
    while r * r > q: r -= Fr(1, s)
    if lo:
        return r
    while r * r < q: r += Fr(1, s)
    return r


def n2(a): return dot(a, a)


def pt_seg_d2(x, a, b):
    ab = sub(b, a); L = n2(ab)
    if L == 0:
        return n2(sub(x, a))
    t = dot(sub(x, a), ab) / L
    t = min(max(t, Fr(0)), Fr(1))
    return n2(sub(x, add(a, mul(t, ab))))


def drop_axis(N):
    k = max(range(3), key=lambda i: abs(N[i]))
    return [i for i in range(3) if i != k]


def orient2(p, q, r, ax):
    i, j = ax
    return (q[i] - p[i]) * (r[j] - p[j]) - (q[j] - p[j]) * (r[i] - p[i])


def segs_intersect_coplanar(a, b, c, d, ax):
    o1, o2, o3, o4 = orient2(a, b, c, ax), orient2(a, b, d, ax), orient2(c, d, a, ax), orient2(c, d, b, ax)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True
    def on(p, q, r):   # r on segment [p, q], given collinear
        i, j = ax
        return min(p[i], q[i]) <= r[i] <= max(p[i], q[i]) and min(p[j], q[j]) <= r[j] <= max(p[j], q[j])
    return (o1 == 0 and on(a, b, c)) or (o2 == 0 and on(a, b, d)) or (o3 == 0 and on(c, d, a)) or (o4 == 0 and on(c, d, b))


def seg_seg_d2_coplanar(a, b, c, d, ax):
    if segs_intersect_coplanar(a, b, c, d, ax):
        return Fr(0)
    return min(pt_seg_d2(a, c, d), pt_seg_d2(b, c, d), pt_seg_d2(c, a, b), pt_seg_d2(d, a, b))


def winding(x, poly, ax):
    """Exact winding number of the closed polygon poly around x (x not on poly), in the 2D chart ax."""
    i, j = ax; w = 0
    for k in range(len(poly)):
        a, b = poly[k], poly[(k + 1) % len(poly)]
        if a[j] <= x[j]:
            if b[j] > x[j] and orient2(a, b, x, ax) > 0: w += 1
        else:
            if b[j] <= x[j] and orient2(a, b, x, ax) < 0: w -= 1
    return w


def simple_polygon(poly, ax):
    k = len(poly)
    for p in range(k):
        for q in range(p + 1, k):
            if q == p + 1 or (p == 0 and q == k - 1):
                continue
            if segs_intersect_coplanar(poly[p], poly[(p + 1) % k], poly[q], poly[(q + 1) % k], ax):
                return False
    # adjacent sides must only share their common vertex (no fold-back): check non-collinear overlap
    for p in range(k):
        a, b, c = poly[p - 1], poly[p], poly[(p + 1) % k]
        if orient2(a, b, c, ax) == 0 and dot(sub(a, b), sub(c, b)) > 0:
            return False
    return True


# ---------- model preparation ----------
def prepare(D):
    """For every face: the closed boundary as a list of pieces (chord a->b, delta2 bound, kind, edge)."""
    for fi, f in enumerate(D["faces"]):
        assert len(f["wires"]) == 1, "multi-wire face"
        for u in f["wires"][0]:
            for x in (u["beta"][0], u["beta"][1]):
                assert dot(sub(x, f["O"]), f["N"]) == 0, "beta end point off the plane"
        pieces, gaps = [], []
        W = f["wires"][0]
        for k, u in enumerate(W):
            a, b = u["beta"]
            if u["rev"]: a, b = b, a
            hull = u["poles"] if u["poles"] is not None else [a, b]
            d2 = max(pt_seg_d2(p, a, b) for p in hull)
            pieces.append(dict(a=a, b=b, delta2=d2, edge=u["edge"], kind="beta", hull=hull, use=u))
            nxt = W[(k + 1) % len(W)]
            na = nxt["beta"][1] if nxt["rev"] else nxt["beta"][0]
            gaps.append(n2(sub(na, b)))
            if na != b:
                pieces.append(dict(a=b, b=na, delta2=Fr(0), edge=None, kind="gap", hull=[b, na]))
        f["pieces"], f["gaps2"] = pieces, gaps
        f["poly"] = [p["a"] for p in pieces]
        f["ax"] = drop_axis(f["N"])
    return D


def check_O0_O3(D, faces):
    """O0 for the given faces; O3 for all their edges. Returns margins (floats) and booleans."""
    E, Vt = D["edges"], D["verts"]
    o0_dev, o0_corner, o3 = math.inf, math.inf, True
    details = []
    for fi in faces:
        f = D["faces"][fi]
        for u in f["wires"][0]:
            e = E[u["edge"]]; g0, g1 = e["gamma"]
            hull = u["poles"] if u["poles"] is not None else list(u["beta"])
            m = max(pt_seg_d2(p, g0, g1) for p in hull)
            ok = m < e["tol"] ** 2
            o0_dev = min(o0_dev, 1 - math.sqrt(m / e["tol"] ** 2))
            # corners: beta(first param) is at the first vertex of the edge (vertex at the first parameter)
            for end, vi in ((0, e["v"][0]), (1, e["v"][1])):
                c2 = n2(sub(u["beta"][end], Vt[vi]["p"]))
                o0_corner = min(o0_corner, 1 - math.sqrt(c2 / Vt[vi]["tol"] ** 2))
                ok = ok and c2 < Vt[vi]["tol"] ** 2
            details.append((fi, u["edge"], ok))
    edges = sorted({u["edge"] for fi in faces for u in D["faces"][fi]["wires"][0]})
    for ei in edges:
        e = E[ei]; g0, g1 = e["gamma"]; v0, v1 = e["v"]
        for vi in (v0, v1):   # each ball meets the open capsule: dist(p_v, gamma) < tau_v + tau_e
            o3 = o3 and pt_seg_d2(Vt[vi]["p"], g0, g1) < (Vt[vi]["tol"] + e["tol"]) ** 2
        # the two end balls are disjoint (needed for the contractibility fact of Section 4)
        o3 = o3 and n2(sub(Vt[v0]["p"], Vt[v1]["p"])) >= (Vt[v0]["tol"] + Vt[v1]["tol"]) ** 2
    return dict(O0_ok=all(d[2] for d in details), O0_dev_margin=o0_dev, O0_corner_margin=o0_corner, O3_ok=o3,
                gaps=[float(math.sqrt(g)) for fi in faces for g in D["faces"][fi]["gaps2"]])


def check_J(D, fi, X, M, s, need_inside=True):
    """O1 and O2 for J = X + [-s, s] M on face fi. Returns (ok, O1 margin, O2 margin, detail)."""
    f = D["faces"][fi]; ax = f["ax"]; tf = f["tol"]
    P, Q = sub(X, mul(s, M)), add(X, mul(s, M))
    assert dot(sub(P, f["O"]), f["N"]) == 0 and dot(sub(Q, f["O"]), f["N"]) == 0, "J not in the face plane"
    poly = f["poly"]
    # Step 2 of the proof only needs: the boundary loop of P_f has winding number +-1 around every y in J_f.
    # That holds if it holds at X and J stays at positive distance from the loop (checked below). Simplicity
    # of the loop (the "Jordan curve" of O1) is NOT required and is reported separately, since the sewn
    # boundaries have corner gaps of ~1e-16 that make the closed chord loop fold back on itself.
    w = winding(X, poly, ax)
    if abs(w) != 1:
        return False, None, None, f"winding {w}"
    o1 = math.inf; ok = True
    for pc in f["pieces"]:
        d2 = seg_seg_d2_coplanar(P, Q, pc["a"], pc["b"], ax)
        dl = isqrt_frac(pc["delta2"], lo=False)
        need = tf + dl
        ok = ok and d2 > need * need
        o1 = min(o1, math.sqrt(d2) / float(need) - 1 if need > 0 else math.inf)
    # O2: J misses cl pi_f(Z(e)) for every edge e of f
    N, O = f["N"], f["O"]; NN = n2(N)
    proj = lambda x: sub(x, mul(dot(sub(x, O), N) / NN, N))
    o2 = math.inf; worst = None
    for u in f["wires"][0]:
        e = D["edges"][u["edge"]]; a, b = proj(e["gamma"][0]), proj(e["gamma"][1])
        d2 = seg_seg_d2_coplanar(P, Q, a, b, ax)
        ok = ok and d2 > e["tol"] ** 2
        r = math.sqrt(d2 / e["tol"] ** 2) - 1
        if r < o2: o2, worst = r, f"tube e{u['edge']}"
        for vi in e["v"]:
            pv = proj(D["verts"][vi]["p"])
            d2 = pt_seg_d2(pv, P, Q)
            ok = ok and d2 > D["verts"][vi]["tol"] ** 2
            r = math.sqrt(d2 / D["verts"][vi]["tol"] ** 2) - 1
            if r < o2: o2, worst = r, f"ball v{vi}"
    return ok, o1, o2, worst


def witness_search(D, ei, tpars=tuple(Fr(k, 20) for k in range(1, 20))):
    e = D["edges"][ei]
    fi, gi = e["faces"]
    if fi == gi:
        return None
    F, G = D["faces"][fi], D["faces"][gi]
    Nf, Ng = F["N"], G["N"]
    d = cross(Nf, Ng)
    if n2(d) == 0:
        return None
    Mf, Mg = cross(d, Nf), cross(d, Ng)
    c = dot(Nf, Ng)
    # O4 bound: rho * |d| > tau_f |c| + tau_g |Nf||Ng| (and symmetric); with dlo <= |d|, NNhi >= |Nf||Ng|
    dlo = isqrt_frac(n2(d), lo=True); NNhi = isqrt_frac(n2(Nf) * n2(Ng), lo=False)
    rho_need = max(F["tol"] * abs(c) + G["tol"] * NNhi, G["tol"] * abs(c) + F["tol"] * NNhi) / dlo
    Mf_lo, Mg_lo = isqrt_frac(n2(Mf), lo=True), isqrt_frac(n2(Mg), lo=True)
    best = None
    g0, g1 = e["gamma"]
    for t in tpars:
        mid = add(g0, mul(t, sub(g1, g0)))
        # X: the point of lambda in the plane through mid orthogonal to d (Cramer, exact)
        rows = [Nf, Ng, d]; rhs = [dot(Nf, F["O"]), dot(Ng, G["O"]), dot(d, mid)]
        det = lambda m: (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                         + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        D0 = det(rows)
        X = tuple(det([[rhs[r] if cc == k else rows[r][cc] for cc in range(3)] for r in range(3)]) / D0 for k in range(3))
        assert dot(Nf, X) == rhs[0] and dot(Ng, X) == rhs[1]
        def feasible(rho):
            sf, sg = rho / Mf_lo, rho / Mg_lo          # s |M| >= rho since |M| >= M_lo
            a = check_J(D, fi, X, Mf, sf); b = check_J(D, gi, X, Mg, sg)
            return a[0] and b[0], a, b
        if not feasible(Fr(0))[0]:
            continue
        lo, hi = Fr(0), Fr(1)
        while feasible(hi)[0] and hi < 100: lo, hi = hi, hi * 2
        for _ in range(30):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if feasible(m)[0] else (lo, m)
        rho = Fr(lo).limit_denominator(10 ** 9)
        if rho > lo: rho = lo
        ok, a, b = feasible(rho)
        if not ok or not rho > rho_need:
            continue
        # sanity: s |M| >= rho exactly
        assert (rho / Mf_lo) ** 2 * n2(Mf) >= rho ** 2 and (rho / Mg_lo) ** 2 * n2(Mg) >= rho ** 2
        cand = dict(edge=ei, faces=(fi, gi), t=float(t), X=[float(x) for x in X], X_exact=[str(x) for x in X],
                    rho=float(rho), rho_exact=str(rho), rho_needed_O4=float(rho_need), O4_ratio=float(rho / rho_need),
                    alpha_deg=math.degrees(math.atan2(math.sqrt(float(n2(d))), abs(float(c)))),
                    O1_margin_f=a[1], O2_margin_f=a[2], O2_binding_f=a[3],
                    O1_margin_g=b[1], O2_margin_g=b[2], O2_binding_g=b[3])
        # margins at half the maximal rho (a witness with room to spare)
        rh = rho / 2
        ok2, a2, b2 = feasible(rh)
        assert ok2 and rh > rho_need
        cand["half"] = dict(rho=float(rh), rho_exact=str(rh), O4_ratio=float(rh / rho_need), O1_margin_f=a2[1],
                            O2_margin_f=a2[2], O2_binding_f=a2[3], O1_margin_g=b2[1], O2_margin_g=b2[2], O2_binding_g=b2[3])
        if best is None or cand["rho"] > best["rho"]:
            best = cand
    return best


def run(name, shape):
    D = prepare(extract(shape))
    out = dict(name=name, F=len(D["faces"]), E=len(D["edges"]), V=len(D["verts"]))
    # manifold check
    out["edges_used_twice"] = all(len(e["faces"]) == 2 and e["faces"][0] != e["faces"][1] for e in D["edges"])
    out["bspline_pcurves"] = sum(1 for f in D["faces"] for u in f["wires"][0] if u["poles"] is not None)
    out["max_pole_delta"] = max(math.sqrt(p["delta2"]) for f in D["faces"] for p in f["pieces"])
    out["max_corner_gap"] = max(math.sqrt(g) for f in D["faces"] for g in f["gaps2"])
    out["tau_f"] = sorted({f["tol_f"] for f in D["faces"]})
    out["chord_loop_simple"] = {fi: simple_polygon(f["poly"], f["ax"]) for fi, f in enumerate(D["faces"])}
    wit = []
    for ei in range(len(D["edges"])):
        w = witness_search(D, ei)
        if w is not None:
            w.update(check_O0_O3(D, w["faces"]))
            wit.append(w)
    out["witnesses"] = wit
    out["all_faces_O0_O3"] = check_O0_O3(D, range(len(D["faces"])))
    return out


if __name__ == "__main__":
    import lemma0_check_run as R
    names = sys.argv[1:] or ["sloppy wedge 30deg g=0.01"]
    res = []
    for n in names:
        r = run(n, R.PARTS[n]())
        res.append(r)
        print(json.dumps(r, indent=1, default=str))
    json.dump(res, open(os.path.join(HERE, "review_lemmaO_exact_result.json"), "w"), indent=1, default=str)
