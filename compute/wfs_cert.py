"""Certified lower bound on the critical values of the distance function to a PL surface.

Setting: M is a triangle mesh (a closed PL surface), and d(p) = min over triangles T of dist(p, T).
A point p off M is critical iff 0 lies in the convex hull of the unit vectors (p - x)/d(p),
where x ranges over the nearest points of p on M.

Box test (tightened: every point x nearest to some p in the box has |x - centre| <= rho with
rho = d(centre) + 2 * half_diagonal; each candidate triangle is clipped to a polygon containing
the disk where that ball meets the triangle's plane. A cube instead of the ball does NOT work:
its section by a face plane does not shrink as the box shrinks, so corners never certify.) Let B be an axis-aligned box and C a set of candidate triangles that contains every
triangle that can be nearest to some point of B. If there is a direction u with
    u . (p - x) > 0   for all p in B and all x in the triangles of C,
then no point of B is critical.

The set {p - x} is the Minkowski sum B + (-T). It is a polytope whose vertices lie among
(corner of B) - (vertex of T). So the test is a small LP over those vectors:
    maximise t  subject to  u . v >= t  for every such vector v,  with -1 <= u_i <= 1.
The box is certified iff the optimum t is > 0.

Octree. Start from a box that covers N_R(M). Split every box that fails the test, until its half-size is <= max(s_min, rel * d(centre)).
Boxes with d >= R are dropped. Boxes lying entirely inside the band d < eps0 are dropped too;
critical points there are NOT examined by this script.

Output. Every critical value in [eps0, R) is >= LB, where
    LB = min over the uncertified leaf boxes of (d(centre) - half_diagonal).
This is the certified part. The arithmetic is double precision; there is no interval arithmetic
yet, so this is not a machine proof.
"""
import sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import cKDTree
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location


def mesh_tris(shape, defl):
    BRepMesh_IncrementalMesh(shape, defl, False, 0.2, True)
    out = []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current())
        loc = TopLoc_Location()
        T = BRep_Tool.Triangulation_s(f, loc)
        tr = loc.Transformation()
        P = np.array([[*T.Node(i).Transformed(tr).Coord()] for i in range(1, T.NbNodes() + 1)])
        for i in range(1, T.NbTriangles() + 1):
            a, b, c = T.Triangle(i).Get()
            out.append(P[[a - 1, b - 1, c - 1]])
        ex.Next()
    return np.array(out)


def closest_on_tris(p, T):
    """Closest points from point p to each triangle in T (n,3,3); Ericson's region method, vectorised."""
    a, b, c = T[:, 0], T[:, 1], T[:, 2]
    ab, ac, ap = b - a, c - a, p - a
    d1, d2 = (ab * ap).sum(1), (ac * ap).sum(1)
    bp = p - b
    d3, d4 = (ab * bp).sum(1), (ac * bp).sum(1)
    cp = p - c
    d5, d6 = (ab * cp).sum(1), (ac * cp).sum(1)
    va = d3 * d6 - d5 * d4
    vb = d5 * d2 - d1 * d6
    vc = d1 * d4 - d3 * d2
    res = np.empty_like(a)
    done = np.zeros(len(T), bool)

    def put(mask, val):
        nonlocal done
        m = mask & ~done
        res[m] = val[m] if val.ndim == 2 else val
        done |= m

    put((d1 <= 0) & (d2 <= 0), a)
    put((d3 >= 0) & (d4 <= d3), b)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = d1 / (d1 - d3)
        put((vc <= 0) & (d1 >= 0) & (d3 <= 0), a + v[:, None] * ab)
        put((d6 >= 0) & (d5 <= d6), c)
        w = d2 / (d2 - d6)
        put((vb <= 0) & (d2 >= 0) & (d6 <= 0), a + w[:, None] * ac)
        w2 = (d4 - d3) / ((d4 - d3) + (d5 - d6))
        put((va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0), b + w2[:, None] * (c - b))
        den = 1.0 / (va + vb + vc)
        v2, w3 = vb * den, vc * den
        put(np.ones(len(T), bool), a + ab * v2[:, None] + ac * w3[:, None])
    return res


class Dist:
    def __init__(self, T):
        self.T = T
        self.cen = T.mean(1)
        self.rad = np.linalg.norm(T - self.cen[:, None], axis=2).max(1)
        self.tree = cKDTree(self.cen)
        self.rmax = self.rad.max()

    def tri_dists(self, p, idx):
        q = closest_on_tris(p, self.T[idx])
        return np.linalg.norm(p - q, axis=1)

    def d(self, p):
        # expanding search: the nearest triangle has a centroid within d + rmax
        r = self.rmax
        while True:
            idx = self.tree.query_ball_point(p, r)
            if idx:
                ds = self.tri_dists(p, idx)
                m = ds.min()
                if m + self.rmax <= r:
                    return m
            r *= 2

    def candidates(self, p, bound):
        idx = np.array(self.tree.query_ball_point(p, bound + self.rmax), dtype=int)
        ds = self.tri_dists(p, idx)
        return idx[ds <= bound]


SIGNS = np.array([[i, j, k] for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)], float)


def clip_poly(P, axis, val, keep_le):
    """Clip convex polygon P (k,3) by half-space x[axis] <= val (keep_le) or >= val."""
    out = []
    k = len(P)
    for i in range(k):
        a, b = P[i], P[(i + 1) % k]
        ina = a[axis] <= val if keep_le else a[axis] >= val
        inb = b[axis] <= val if keep_le else b[axis] >= val
        if ina:
            out.append(a)
        if ina != inb:
            t = (val - a[axis]) / (b[axis] - a[axis])
            out.append(a + t * (b - a))
    return np.array(out) if out else np.zeros((0, 3))


def clip_half(P, w, val):
    """Clip convex polygon P (k,3) to the half-space w.x <= val."""
    out = []
    k = len(P)
    for i in range(k):
        a, b = P[i], P[(i + 1) % k]
        fa, fb = w @ a - val, w @ b - val
        if fa <= 0:
            out.append(a)
        if (fa <= 0) != (fb <= 0):
            out.append(a + (fa / (fa - fb)) * (b - a))
    return np.array(out) if out else np.zeros((0, 3))


KGON = 8
ANG = 2 * np.pi * np.arange(KGON) / KGON


def relevant_points(tris, cen, rho):
    """Every point x of M that is nearest to some p in the box satisfies |x - cen| <= rho.
    For each triangle, the ball meets its plane in a disk (centre c', radius r'); we clip the
    triangle by the KGON half-planes of a polygon whose inradius is r' (so it contains the disk).
    The clipped piece is convex and contains every relevant point of the triangle."""
    pts = []
    for t in tris:
        a, b, c = t
        n = np.cross(b - a, c - a)
        nn = np.linalg.norm(n)
        if nn == 0:
            pts.append(t)   # degenerate triangle: keep its vertices (review fix); its hull is a segment
            continue
        n /= nn
        delta = n @ (cen - a)
        r2 = rho * rho - delta * delta
        if r2 < 0:
            continue
        r = np.sqrt(r2)
        cp = cen - delta * n
        e1 = (b - a) / np.linalg.norm(b - a)
        e2 = np.cross(n, e1)
        P = t
        for th in ANG:
            w = np.cos(th) * e1 + np.sin(th) * e2
            P = clip_half(P, w, w @ cp + r)
            if len(P) == 0:
                break
        if len(P):
            pts.append(P)
    return np.vstack(pts) if pts else np.zeros((0, 3))


def box_certified(cen, h, X):
    corners = cen + h * SIGNS                       # 8 x 3
    V = (corners[None, :, :] - X[:, None, :]).reshape(-1, 3)
    u0 = cen - X.mean(0)                            # cheap guess; any u with u.v > 0 for all v suffices
    if (V @ u0).min() > 1e-12 * np.linalg.norm(u0):
        return True
    # maximise t s.t. -u.v + t <= 0 ; variables (u0,u1,u2,t)
    A = np.hstack([-V, np.ones((len(V), 1))])
    res = linprog(c=[0, 0, 0, -1], A_ub=A, b_ub=np.zeros(len(V)),
                  bounds=[(-1, 1)] * 3 + [(None, 1)], method="highs")
    return res.status == 0 and -res.fun > 1e-9


def certify(T, R, eps0, s_min, rel=0.03):
    D = Dist(T)
    lo, hi = T.reshape(-1, 3).min(0) - R, T.reshape(-1, 3).max(0) + R
    h0 = (hi - lo).max() / 2
    stack = [((lo + hi) / 2, h0)]
    LB, worst, n_box, n_leaf = np.inf, None, 0, 0
    t0 = time.time()
    while stack:
        cen, h = stack.pop()
        n_box += 1
        if n_box % 200000 == 0:
            print(f"   ... {n_box} boxes, {len(stack)} queued, leaves={n_leaf}, LB so far={LB:.4f}, "
                  f"{time.time() - t0:.0f}s", flush=True)
        hd = h * np.sqrt(3)
        dc = D.d(cen)
        if dc - hd >= R or dc + hd < eps0:
            continue
        if dc > hd:   # box does not meet M
            cand = D.candidates(cen, dc + 2 * hd)
            X = relevant_points(T[cand], cen, dc + 2 * hd)
            if len(X) and box_certified(cen, h, X):
                continue
        if h <= max(s_min, rel * dc):
            n_leaf += 1
            lb = max(dc - hd, 0.0)
            if lb < LB:
                LB, worst = lb, cen
            continue
        for s in SIGNS:
            stack.append((cen + s * h / 2, h / 2))
    return LB, worst, n_box, n_leaf


def box(a): return BRepPrimAPI_MakeBox(a, a, a).Shape()
def cyl(R, H): return BRepPrimAPI_MakeCylinder(R, H).Shape()
def plate(a, t): return BRepPrimAPI_MakeBox(a, a, t).Shape()
def lshape(L, w):
    return BRepAlgoAPI_Fuse(BRepPrimAPI_MakeBox(L, w, w).Shape(), BRepPrimAPI_MakeBox(w, L, w).Shape()).Shape()
def filleted_box(a, r):
    s = box(a); mk = BRepFilletAPI_MakeFillet(s)
    ex = TopExp_Explorer(s, TopAbs_EDGE)
    while ex.More():
        mk.Add(r, TopoDS.Edge(ex.Current())); ex.Next()
    return mk.Shape()


if __name__ == "__main__":
    cases = [
        ("box a=10", box(10), 5.0, dict(R=6, eps0=0.2, s_min=0.002, defl=0.01)),
        ("plate 4x4x1", plate(4, 1), 0.5, dict(R=1.0, eps0=0.05, s_min=0.001, defl=0.01)),
        ("L-shape L=10 w=2", lshape(10, 2), 1.0, dict(R=1.5, eps0=0.1, s_min=0.002, defl=0.01)),
        ("cylinder R=3 H=10", cyl(3, 10), 3.0, dict(R=3.5, eps0=0.2, s_min=0.002, defl=0.02)),
        ("filleted box a=10 r=2", filleted_box(10, 2), 5.0, dict(R=6, eps0=0.2, s_min=0.002, defl=0.05)),
    ]
    only = sys.argv[1:]
    for name, shape, exact, kw in cases:
        if only and not any(o in name for o in only):
            continue
        T = mesh_tris(shape, kw.pop("defl"))
        t0 = time.time()
        LB, worst, nb, nl = certify(T, **kw)
        print(f"{name:24s} tris={len(T):5d} exact(smooth)={exact:<4} certified: no critical value in "
              f"[{kw['eps0']}, {LB:.4f}); worst box at {np.round(worst, 3)}  boxes={nb} leaves={nl} "
              f"{time.time() - t0:.0f}s", flush=True)
