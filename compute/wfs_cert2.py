"""Certified lower bound on wfs(M) for a PL surface M, with no unexamined band near M.

Two box tests, then best-first octree refinement.

(1) Cone test (covers the band next to M).
    For a in M let rho(a) be the conical radius: the largest r such that M ∩ B(a, r) equals
    C ∩ B(a, r) for a closed cone C with apex a.
    Lemma: if |p - a| < rho(a)/2 and d(p) > 0, then p is not critical.
    Proof sketch:
      - Every nearest point x of p lies in B(a, rho), and there M agrees with the cone C.
      - Along the ray a + s(x - a), the function s -> |p - a - s(x - a)|^2 has its minimum at s = 1,
        so (p - x).(x - a) = 0.
      - Hence (p - x).(p - a) = |p - x|^2 > 0 for every nearest point x, so 0 is not in their convex hull.
    Computing rho(a): M is the union of "regions", "segments" and "vertices".
      - A region is a planar B-rep face (all its triangles together) or a single triangle of a curved face.
      - Segments are the region boundary edges; vertices are their endpoints.
    rho(a) >= min over the features f with dist(a, f) > tol of dist(a, f).
    So a box (centre c, half-diagonal hd) is certified if, for some a,
        no feature that does not contain a lies within 2(|c - a| + hd) of a.

(2) Direction test (as in wfs_cert.py). If some u has u.(p - x) > 0 for every p in the box and every
    x in M within d(c) + 2hd of c, the box is certified.

Best-first order. Boxes are processed in increasing order of key = max(d(c) - hd, 0).
A child's key is >= its parent's key. So the first uncertified leaf popped gives
LB = its key, and no critical value lies in (0, LB) (up to the cut-off R).

Caveats: double precision, no interval arithmetic. "Contains a" uses tolerance tol.
"""
import sys, time, heapq
import numpy as np
from scipy.spatial import cKDTree
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.TopAbs import TopAbs_EDGE
from OCP.gp import gp_Pnt
import wfs_cert as W


def mesh_features(shape, defl):
    BRepMesh_IncrementalMesh(shape, defl, False, 0.2, True)
    tris, reg, segs = [], [], []
    rid = 0
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current())
        loc = TopLoc_Location()
        T = BRep_Tool.Triangulation_s(f, loc)
        tr = loc.Transformation()
        P = np.array([[*T.Node(i).Transformed(tr).Coord()] for i in range(1, T.NbNodes() + 1)])
        idx = np.array([T.Triangle(i).Get() for i in range(1, T.NbTriangles() + 1)]) - 1
        F = P[idx]
        n = np.cross(F[:, 1] - F[:, 0], F[:, 2] - F[:, 0])
        # zero-area triangles: their point set is a segment made of their edges, which on a closed
        # manifold mesh are edges of neighbouring triangles; drop them from the regions, keep the edges
        good = np.linalg.norm(n, axis=1) > 1e-14 * (np.abs(P).max() + 1) ** 2
        kept_edges = set()
        for t in idx[good]:
            for u, v in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                kept_edges.add((min(u, v), max(u, v)))
        for t in idx[~good]:
            segs += [P[[t[0], t[1]]], P[[t[1], t[2]]], P[[t[2], t[0]]]]
            for u, v in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                if (min(u, v), max(u, v)) not in kept_edges and np.linalg.norm(P[u] - P[v]) > 0:
                    raise RuntimeError("zero-area triangle with an edge not shared by a kept triangle")
        idx, F, n = idx[good], F[good], n[good]
        n /= np.linalg.norm(n, axis=1)[:, None]
        L = np.abs(P).max() + 1
        # planar region: parallel AND consistently oriented normals (review fix: folded triangles
        # with opposite normals would hide boundary edges)
        planar = (np.linalg.norm(np.cross(n, n[0]), axis=1).max() < 1e-9 and (n @ n[0]).min() > 0 and
                  np.abs((F[:, 0] - F[0, 0]) @ n[0]).max() < 1e-9 * L)
        if planar:
            # boundary = directed edges whose reverse does not occur (review fix)
            de = set()
            for t in idx:
                for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                    de.add((a, b))
            segs += [P[[a, b]] for (a, b) in de if (b, a) not in de]
            tris.append(F); reg += [rid] * len(F); rid += 1
        else:
            # curved face: merge edge-adjacent triangles that are coplanar with consistent orientation
            # (e.g. the two halves of a planar strip on a cylinder); real folds stay as boundaries
            m = len(idx); par = list(range(m))
            def find(i):
                while par[i] != i:
                    par[i] = par[par[i]]; i = par[i]
                return i
            owner = {}
            for k, t in enumerate(idx):
                for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                    owner[e] = k
            for k, t in enumerate(idx):
                for (u, v) in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                    j = owner.get((v, u))
                    if j is not None and n[k] @ n[j] > 1 - 1e-12 and abs((P[idx[j]] - P[t[0]]) @ n[k]).max() < 1e-9 * L:
                        par[find(k)] = find(j)
            roots = [find(k) for k in range(m)]
            comp = {}
            for k, r in enumerate(roots):
                comp.setdefault(r, []).append(k)
            for r, ks in comp.items():
                if len(ks) > 1:
                    k0 = ks[0]
                    ok = all(n[k] @ n[k0] > 1 - 1e-12 and
                             abs((P[idx[k]] - P[idx[k0][0]]) @ n[k0]).max() < 1e-9 * L for k in ks)
                    if not ok:
                        for k in ks:
                            roots[k] = ('single', k)
            lab = {r: i for i, r in enumerate(sorted(set(roots), key=str))}
            de = {}
            for k, t in enumerate(idx):
                for (u, v) in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                    de[(u, v)] = lab[roots[k]]
            for (u, v), g in de.items():
                if de.get((v, u)) != g:          # boundary of its merged region (or a fold)
                    segs.append(P[[u, v]])
            tris.append(F); reg += [rid + lab[r] for r in roots]; rid += len(lab)
        ex.Next()
    T = np.vstack(tris); segs = np.array(segs)
    verts = np.unique(segs.reshape(-1, 3), axis=0)   # no rounding (review fix)
    return T, np.array(reg), segs, verts


def seg_closest(p, S):
    a, b = S[:, 0], S[:, 1]
    ab = b - a
    t = np.clip(((p - a) * ab).sum(1) / np.maximum((ab * ab).sum(1), 1e-300), 0, 1)
    return a + t[:, None] * ab


class Features:
    def __init__(self, T, reg, S, V):
        self.T, self.reg, self.S, self.V = T, reg, S, V
        self.D = W.Dist(T)
        self.smid = S.mean(1); self.shalf = np.linalg.norm(S[:, 1] - S[:, 0], axis=1).max() / 2
        self.stree = cKDTree(self.smid); self.vtree = cKDTree(V)
        self.L = np.abs(T).max() + 1
        self.tol = 1e-10 * self.L

    def nearest(self, p):
        d = self.D.d(p)
        idx = self.D.candidates(p, d * (1 + 1e-12) + 1e-14)
        q = W.closest_on_tris(p, self.T[idx])
        return d, q[np.argmin(np.linalg.norm(q - p, axis=1))]

    def clear_ball(self, a, r):
        """True if no feature that does not contain a lies within distance r of a (=> rho(a) >= r)."""
        tol = self.tol
        idx = self.D.tree.query_ball_point(a, r + self.D.rmax)
        if idx:
            idx = np.array(idx)
            dt = np.linalg.norm(W.closest_on_tris(a, self.T[idx]) - a, axis=1)
            # region distance = min over its triangles; a region "contains a" if that min <= tol
            regs = self.reg[idx]
            for g in np.unique(regs[dt < r]):
                if dt[regs == g].min() > tol:
                    # region g may have triangles outside the query; its true distance is <= this, still < r
                    return False
        si = self.stree.query_ball_point(a, r + self.shalf)
        if si:
            si = np.array(si)
            ds = np.linalg.norm(seg_closest(a, self.S[si]) - a, axis=1)
            if ((ds > tol) & (ds < r)).any():
                return False
        vi = self.vtree.query_ball_point(a, r)
        if vi:
            dv = np.linalg.norm(self.V[vi] - a, axis=1)
            if ((dv > tol) & (dv < r)).any():
                return False
        return True

    def cone_certified(self, c, hd, x0, dc):
        cands = [x0]
        k = min(3, len(self.V))
        _, vi = self.vtree.query(c, k)
        cands += [self.V[i] for i in np.atleast_1d(vi)]
        si = self.stree.query_ball_point(c, dc + 2 * hd + self.shalf)
        if si:
            q = seg_closest(c, self.S[np.array(si)])
            order = np.argsort(np.linalg.norm(q - c, axis=1))[:4]
            cands += list(q[order])
        for a in cands:
            need = 2 * (np.linalg.norm(c - a) + hd)
            if self.clear_ball(a, need * (1 + 1e-9)):
                return True
        return False


def relevant_points_proj(tris, cen, hd, rho):
    """Superset of every possible nearest point (on these triangles) of every p in the box
    (centre cen, half-diagonal hd); rho = d(cen) + 2 hd.
    A nearest point x of p lies in one of three places:
      - in a triangle's interior: then x is p's orthogonal projection on the plane, so x lies within hd
        of the projection q of cen, and within rho of cen;
      - in an edge's interior: then x is p's projection on the edge line (same two bounds);
      - at a vertex within rho of cen.
    Each piece is convex and we keep its vertices; the LP is linear, so that suffices."""
    out = []
    for t in tris:
        a, b, c = t
        for v in t:
            if np.linalg.norm(v - cen) <= rho:
                out.append(v[None])
        for u, v in ((a, b), (b, c), (c, a)):
            e = v - u; L2 = e @ e
            if L2 == 0:
                continue
            t0 = (cen - u) @ e / L2
            foot = u + t0 * e
            dl2 = (cen - foot) @ (cen - foot)
            if rho * rho < dl2:
                continue
            r = min(hd, np.sqrt(rho * rho - dl2)) / np.sqrt(L2)
            lo_, hi_ = max(t0 - r, 0.0), min(t0 + r, 1.0)
            if lo_ <= hi_:
                out.append(np.array([u + lo_ * e, u + hi_ * e]))
        n = np.cross(b - a, c - a); nn = np.linalg.norm(n)
        if nn <= 1e-9 * max((b - a) @ (b - a), (c - a) @ (c - a), (c - b) @ (c - b)):
            out.append(t)      # sliver: normal unreliable, keep the whole triangle (superset)
            continue
        n = n / nn
        delta = n @ (cen - a)
        if rho * rho < delta * delta:
            continue
        r = min(hd, np.sqrt(rho * rho - delta * delta))
        q = cen - delta * n
        e1 = (b - a) / np.linalg.norm(b - a); e2 = np.cross(n, e1)
        P = t
        for th in W.ANG:
            w = np.cos(th) * e1 + np.sin(th) * e2
            P = W.clip_half(P, w, w @ q + r)
            if len(P) == 0:
                break
        if len(P):
            out.append(P)
    return np.vstack(out) if out else np.zeros((0, 3))


def certify(F, R, s_min, rel=0.05, max_boxes=3_000_000):
    T = F.T
    lo, hi = T.reshape(-1, 3).min(0) - R, T.reshape(-1, 3).max(0) + R
    h0 = (hi - lo).max() / 2
    heap = [(0.0, 0, tuple((lo + hi) / 2), h0)]
    cnt = 1; n_box = 0; n_cone = 0; n_lp = 0; t0 = time.time()
    while heap:
        key, _, cen, h = heapq.heappop(heap)
        cen = np.array(cen); n_box += 1
        if n_box % 200000 == 0:
            print(f"   ... {n_box} boxes, key={key:.5f}, heap={len(heap)}, {time.time() - t0:.0f}s", flush=True)
        if n_box > max_boxes:
            return key, cen, n_box, n_cone, n_lp, "stopped at max_boxes: certified only (0, key)"
        hd = h * np.sqrt(3)
        dc, x0 = F.nearest(cen)
        if dc - hd >= R:
            continue
        if dc > hd:
            rho = (dc + 2 * hd) * (1 + 1e-12)
            cand = F.D.candidates(cen, rho)
            X = relevant_points_proj(T[cand], cen, hd, rho)
            if len(X) and W.box_certified(cen, h, X):
                n_lp += 1; continue
        if F.cone_certified(cen, hd, x0, dc):
            n_cone += 1; continue
        if h <= max(s_min, rel * dc):
            return max(dc - hd, 0.0), cen, n_box, n_cone, n_lp, "first uncertified leaf"
        for s in W.SIGNS:
            c2 = cen + s * h / 2; h2 = h / 2
            d2 = F.D.d(c2)
            cnt += 1
            heapq.heappush(heap, (max(d2 - h2 * np.sqrt(3), 0.0), cnt, tuple(c2), h2))
    return R, None, n_box, n_cone, n_lp, "no uncertified box below R"


def plate(a, t): return BRepPrimAPI_MakeBox(a, a, t).Shape()
def slot_block(g):
    blk = BRepPrimAPI_MakeBox(10, 10, 4).Shape()
    cut = BRepPrimAPI_MakeBox(gp_Pnt(-1, 5 - g / 2, 2), 12, g, 3).Shape()
    return BRepAlgoAPI_Cut(blk, cut).Shape()
def lshape_inner_fillet(r):
    s = W.lshape(10, 2)
    mk = BRepFilletAPI_MakeFillet(s)
    ex = TopExp_Explorer(s, TopAbs_EDGE)
    from OCP.BRepAdaptor import BRepAdaptor_Curve
    while ex.More():
        e = TopoDS.Edge(ex.Current())
        c = BRepAdaptor_Curve(e)
        p0, p1 = c.Value(c.FirstParameter()), c.Value(c.LastParameter())
        if abs(p0.X() - 2) < 1e-9 and abs(p0.Y() - 2) < 1e-9 and abs(p1.X() - 2) < 1e-9 and abs(p1.Y() - 2) < 1e-9:
            mk.Add(r, e)
        ex.Next()
    return mk.Shape()


CASES = {
    "box":      (lambda: W.box(10), 5.0, dict(R=6, s_min=1e-5, defl=0.01)),
    "plate":    (lambda: plate(4, 1), 0.5, dict(R=1.0, s_min=1e-5, defl=0.01)),
    "L-shape":  (lambda: W.lshape(10, 2), 1.0, dict(R=1.5, s_min=1e-5, defl=0.01)),
    "cylinder": (lambda: W.cyl(3, 10), 3.0, dict(R=3.5, s_min=1e-5, defl=0.02)),
    "filleted": (lambda: W.filleted_box(10, 2), 5.0, dict(R=6, s_min=1e-5, defl=0.05)),
    "plate_t0.3": (lambda: plate(4, 0.3), 0.15, dict(R=0.3, s_min=1e-6, defl=0.01)),
    "plate_t0.1": (lambda: plate(4, 0.1), 0.05, dict(R=0.1, s_min=1e-6, defl=0.01, rel=0.1)),
    "slot_g0.2":  (lambda: slot_block(0.2), 0.1, dict(R=0.2, s_min=1e-6, defl=0.01, rel=0.1)),
    "plate_t0.03": (lambda: plate(4, 0.03), 0.015, dict(R=0.03, s_min=1e-7, defl=0.01)),
    "slot_g0.05": (lambda: slot_block(0.05), 0.025, dict(R=0.05, s_min=1e-7, defl=0.01)),
    "Lfillet_r0.2": (lambda: lshape_inner_fillet(0.2), 1.0, dict(R=1.5, s_min=1e-6, defl=0.02)),
    "Lfillet_r0.05": (lambda: lshape_inner_fillet(0.05), 1.0, dict(R=1.5, s_min=1e-6, defl=0.01)),
}

if __name__ == "__main__":
    for name in sys.argv[1:]:
        mk, exact, kw = CASES[name]
        kw = dict(kw); defl = kw.pop("defl")
        F = Features(*mesh_features(mk(), defl))
        t0 = time.time()
        LB, where, nb, nc, nl, how = certify(F, **kw)
        print(f"{name:14s} tris={len(F.T):5d} exact(smooth)={exact:<5} no critical value in (0, {LB:.4f}) "
              f"[{how}] at {np.round(where, 3) if where is not None else '-'}  boxes={nb} cone={nc} lp={nl} "
              f"{time.time() - t0:.0f}s", flush=True)
