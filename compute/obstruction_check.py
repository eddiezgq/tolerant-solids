"""Check the hypotheses of the obstruction lemma (notes/lemma0_v03.md, Lemma O) on planar models.

Lemma O (planar faces f != g, non-parallel planes Pi_f, Pi_g, lambda = Pi_f cap Pi_g, alpha = angle between
the planes): if there are X in lambda and rho > 0 such that, with m_f the unit vector in Pi_f orthogonal to
lambda and J_f = X + [-rho, rho] m_f (and likewise for g),
  O0  for f and g: every boundary arc beta_{f,e} = S_f(pcurve) lies in Z(e), and the end points of the two arcs
      of f at a vertex v lie in Z(v); l_f is the closed loop of the arcs in wire order, consecutive arcs joined
      by the segment between their end points (inside the ball Z(v));
  O1  J_f misses l_f, and the winding number of l_f about the points of J_f is odd;   (same for g)
  O2  J_f misses the closure of pi_f(Z(e)) for every edge e of f;            (same for g)
  O3  every Z(e), e an edge of f or g, is simply connected (here: straight edges, so Z(e) is a capsule
      union two balls, which is contractible when each ball meets the capsule);
  O4  rho sin(alpha) > tau_f |cos alpha| + tau_g  and  rho sin(alpha) > tau_g |cos alpha| + tau_f,
then the model has no realization.

The projection of a capsule of radius r around a segment [a, b] onto a plane is the planar capsule of radius
r around [pi a, pi b], and the projection of a ball is a disk of the same radius, so O2 is a segment-segment
and segment-point distance test in the plane. All tests are in double precision. The witness is reported at half the largest feasible rho. l_f is represented
by a dense polyline of samples of the pcurves (sewing stores many of them as B-splines); the polyline error is
measured and reported.
"""
import sys, math, json
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Line
from OCP.BRepTools import BRepTools_WireExplorer, BRepTools
from OCP.BRepAdaptor import BRepAdaptor_Curve2d
from OCP.TopAbs import TopAbs_REVERSED, TopAbs_WIRE
from OCP.TopExp import TopExp_Explorer


def face_loop(face, nsamp=400):
    """Closed polyline l_f: samples of S_f(pcurve) of each oriented edge of the (single) wire, in wire order.
    Returns (points, arc_ends, polyline_error); arc_ends lists (end of arc i, start of arc i+1)."""
    nw, ex = 0, TopExp_Explorer(face, TopAbs_WIRE)
    while ex.More():
        nw += 1; ex.Next()
    if nw != 1:
        raise ValueError("face with several wires")
    S = BRepAdaptor_Surface(face)
    arcs, err = [], 0.0
    we = BRepTools_WireExplorer(BRepTools.OuterWire_s(face), face)
    while we.More():
        e = we.Current()
        pc = BRepAdaptor_Curve2d(e, face)
        ts = np.linspace(pc.FirstParameter(), pc.LastParameter(), 2 * nsamp + 1)
        if e.Orientation() == TopAbs_REVERSED:
            ts = ts[::-1]
        P = np.array([L.V(S.Value(pc.Value(t).X(), pc.Value(t).Y())) for t in ts])
        Pe, Po = P[::2], P[1::2]          # polyline on even samples; odd samples measure the chord error
        for i in range(len(Po)):
            a3, b3 = Pe[i], Pe[i + 1]; ab = b3 - a3
            tt = np.clip(((Po[i] - a3) @ ab) / max(ab @ ab, 1e-300), 0, 1)
            err = max(err, np.linalg.norm(Po[i] - (a3 + tt * ab)))
        arcs.append(Pe)
        we.Next()
    ends = [(arcs[i][-1], arcs[(i + 1) % len(arcs)][0]) for i in range(len(arcs))]
    return np.concatenate(arcs + [arcs[0][:1]]), ends, err


def winding(loop, X, e1, e2):
    q = np.stack([(loop - X) @ e1, (loop - X) @ e2], 1)
    ang = np.arctan2(q[:, 1], q[:, 0])
    d = np.diff(ang); d = (d + np.pi) % (2 * np.pi) - np.pi
    return int(round(d.sum() / (2 * np.pi)))


def seg_seg_dist(p, q, r, s):
    """Distance between segments [p,q] and [r,s] in R^3 (dense sampling of one + exact point-segment)."""
    def ps(x, a, b):
        ab = b - a; t = np.clip(((x - a) @ ab) / max(ab @ ab, 1e-300), 0, 1)
        return np.linalg.norm(x - (a + np.outer(t, ab)), axis=1)
    # exact for segments: min over endpoints and the closest pair of the supporting lines
    best = min(ps(np.array([p, q]), r, s).min(), ps(np.array([r, s]), p, q).min())
    d1, d2, w = q - p, s - r, p - r
    a, b, c, d, e = d1 @ d1, d1 @ d2, d2 @ d2, d1 @ w, d2 @ w
    den = a * c - b * b
    if den > 1e-300:
        sc, tc = (b * e - c * d) / den, (a * e - b * d) / den
        if 0 <= sc <= 1 and 0 <= tc <= 1:
            best = min(best, np.linalg.norm(w + sc * d1 - tc * d2))
    return best


def check(shape, name, verbose=True):
    M = L.Model(shape)
    for f in M.F:
        if BRepAdaptor_Surface(f).GetType() != GeomAbs_Plane:
            return dict(name=name, applicable=False, why="non-planar face")
    for e in M.E:
        if BRepAdaptor_Curve(e).GetType() != GeomAbs_Line:
            return dict(name=name, applicable=False, why="non-straight edge")
    for f in M.F:
        nw, ex = 0, TopExp_Explorer(f, TopAbs_WIRE)
        while ex.More():
            nw += 1; ex.Next()
        if nw != 1:
            return dict(name=name, applicable=False, why="face with several wires")
    sm = [L.edge_samples(M, i) for i in range(len(M.E))]
    pl = []
    for f in M.F:
        P = BRepAdaptor_Surface(f).Plane()
        pl.append((L.V(P.Axis().Direction()), L.V(P.Location())))
    seg = [(s["G"][0], s["G"][-1]) for s in sm]
    # O0
    o0 = min(min((M.te[ei] - sd["dev"].max()) / M.te[ei] for sd in sm[ei]["sides"]) for ei in range(len(M.E)))
    corner = math.inf
    for ei in range(len(M.E)):
        for sd in sm[ei]["sides"]:
            for end, vi in ((0, M.ev[ei][0]), (-1, M.ev[ei][1])):
                corner = min(corner, (M.tv[vi] - np.linalg.norm(sd["B"][end] - M.p[vi])) / M.tv[vi])
    # O3 (sufficient): each end ball meets the capsule, and the two end balls are disjoint or all three sets
    # share a point (nerve lemma for the good cover {capsule, ball, ball})
    def o3_edge(ei):
        v0, v1 = M.ev[ei]
        if not all(np.linalg.norm(seg[ei][k] - M.p[M.ev[ei][k]]) < M.tv[M.ev[ei][k]] + M.te[ei] for k in (0, 1)):
            return False
        if v0 == v1 or np.linalg.norm(M.p[v0] - M.p[v1]) >= M.tv[v0] + M.tv[v1]:
            return True
        return any(np.linalg.norm(x - M.p[v0]) < M.tv[v0] and np.linalg.norm(x - M.p[v1]) < M.tv[v1] for x in seg[ei])
    o3 = all(o3_edge(ei) for ei in range(len(M.E)))
    loops, polyline_err = [], 0.0
    for f in M.F:
        lp, ends, err = face_loop(f)
        loops.append(lp); polyline_err = max(polyline_err, err)
        for a, b in ends:   # each closing segment lies in the (convex) ball of the vertex at that corner
            vi = min(range(len(M.Vx)), key=lambda v: np.linalg.norm(a - M.p[v]))
            corner = min(corner, (M.tv[vi] - max(np.linalg.norm(a - M.p[vi]), np.linalg.norm(b - M.p[vi]))) / M.tv[vi])
    best = None
    for ei in range(len(M.E)):
        fi, gi = [u[0] for u in M.uses[ei]]
        if fi == gi:
            continue
        (nf, of), (ng, og) = pl[fi], pl[gi]
        lam = np.cross(nf, ng); sa = np.linalg.norm(lam)
        if sa < 1e-12:
            continue
        lam /= sa; ca = abs(nf @ ng)
        mf, mg = np.cross(lam, nf), np.cross(lam, ng)
        # a point on lambda
        A = np.array([nf, ng, lam]); X0 = np.linalg.solve(A, np.array([nf @ of, ng @ og, 0.0]))
        # candidate X: projection onto lambda of the edge midpoint, and a few positions along the edge
        for tpar in np.linspace(0.2, 0.8, 7):
            mid = seg[ei][0] + tpar * (seg[ei][1] - seg[ei][0])
            X = X0 + ((mid - X0) @ lam) * lam
            def rho_max(fk, m):
                n, o = pl[fk]
                es = [ej for ej in range(len(M.E)) if fk in [u[0] for u in M.uses[ej]]]
                # O1: winding number of l_f about X is odd; J must miss l_f (checked in ok())
                if winding(loops[fk], X, m, np.cross(n, m)) % 2 == 0:
                    return -1.0, None
                lp = loops[fk]
                # O2: J must miss the projected edge zones of all edges of fk
                def proj(x): return x - ((x - o) @ n) * n
                lo = math.inf
                def jdist(rr, a, b):
                    return seg_seg_dist(X - rr * m, X + rr * m, proj(a), proj(b))
                # largest rr with jdist(rr) > zone radius for all zones (monotone decreasing in rr: bisection)
                def ok(rr):
                    for ej in es:
                        a, b = seg[ej]
                        if jdist(rr, a, b) <= M.te[ej]:
                            return False
                        for vi in M.ev[ej]:
                            if jdist(rr, M.p[vi], M.p[vi]) <= M.tv[vi]:
                                return False
                    for i in range(len(lp) - 1):   # J misses l_f, with a safety distance
                        if seg_seg_dist(X - rr * m, X + rr * m, lp[i], lp[i + 1]) <= 10 * polyline_err + 1e-15:
                            return False
                    return True
                if not ok(0.0):
                    return -1.0, None
                lo_, hi_ = 0.0, 1.0
                while ok(hi_) and hi_ < 1e6:
                    hi_ *= 2
                for _ in range(60):
                    mid_ = (lo_ + hi_) / 2
                    lo_, hi_ = (mid_, hi_) if ok(mid_) else (lo_, mid_)
                return lo_, es
            rf, _ = rho_max(fi, mf); rg, _ = rho_max(gi, mg)
            rho_feasible = min(rf, rg)
            rho = rho_feasible / 2          # report the witness with slack
            if rho <= 0:
                continue
            need = max(M.tf[fi] * ca + M.tf[gi], M.tf[gi] * ca + M.tf[fi]) / sa
            o4 = (rho - need) / rho
            cand = dict(edge=ei, faces=(fi, gi), X=X.tolist(), alpha_deg=math.degrees(math.asin(min(1, sa))),
                        rho=rho, rho_max_feasible=rho_feasible, rho_needed=need, O4_margin=o4)
            if o4 > 0 and (best is None or o4 > best["O4_margin"]):
                best = cand
    res = dict(name=name, applicable=True, O0_dev_margin=o0, O0_corner_margin=corner, O3=o3, witness=best, polyline_error=polyline_err,
               no_realization=bool(best is not None and o0 > 0 and corner > 0 and o3))
    if verbose:
        if best:
            print(f"== {name}: Lemma O hypotheses {'HOLD' if res['no_realization'] else 'fail'}: edge e{best['edge']} "
                  f"faces {best['faces']} alpha {best['alpha_deg']:.1f} deg, witness rho = {best['rho']:.3g} "
                  f"(max feasible {best['rho_max_feasible']:.3g}; O4 needs > {best['rho_needed']:.2g}); "
                  f"O0 margins {o0:.3f}/{corner:.3f}; O3 {o3}; polyline error {polyline_err:.1e}")
        else:
            print(f"== {name}: no crossing witness (O1/O2 fail everywhere); O0 margins {o0:.3f}/{corner:.3f}")
    return res


if __name__ == "__main__":
    import lemma0_check_run as R
    names = sys.argv[1:] or ["sloppy wedge 30deg g=0.01", "sloppy wedge 10deg g=0.01", "sloppy box g=0.01",
                             "sloppy plate t=0.05 g=0.01", "box", "wedge 10deg"]
    out = [check(R.PARTS[n](), n) for n in names]
    json.dump(out, open("../results/obstruction_result.json", "w"), indent=1, default=float)
