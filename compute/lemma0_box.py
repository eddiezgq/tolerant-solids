"""Lemma 0 construction, carried out exactly on a gapped box.

Nominal data (a tolerant B-rep whose pieces do not touch).
- K is the cube complex: 8 vertices, 12 edges, 6 faces.
- Vertices and edges are the corners and edges of the cube [0, L]^3.
- Face patches are squares moved outward by S and shrunk inward by G. For example, the face
  "z = 0" becomes {z = -S, G <= x, y <= L - G}.
- So each patch boundary lies at distance dev = sqrt(G^2 + S^2) from its edge, and no two
  patches touch.
- Tolerances: TAU_E for edges, TAU_V for vertices, TAU_F for faces (tiny).

Construction (Lemma 0 v0.2, with tube radius RHO and stub length A).
- c = sqrt(RHO^2 - S^2), the in-plane offset of the exit point.
- Edge fans: in each normal disk of an edge (outside the stubs), the segment from the edge
  point to the exit point of each adjacent face. Along a straight edge with planar faces this is a flat quad.
- Q_f: the square {c <= x, y <= L - c} on the shifted plane.
- Vertex cone: from the corner over the link polyline on dW_v. For the face with normal axis k,
  between edge axes i and j, the polyline is
  A e_i, A e_i + c e_j - S e_k, c e_i + c e_j - S e_k, c e_i + A e_j - S e_k, A e_j.
- All coordinates are rational (S = 3/10, RHO = 1/2, so c = 2/5), so every check below is exact.

Checks.
1. Zones (exact).
   - Fan points lie within RHO < TAU_E of their edge line.
   - Cone points lie within max|vertex| < TAU_V of the corner.
   - Q_f lies on its patch (distance 0).
2. Embedding (exact). For every pair of triangles, their intersection is contained in the
   geometric elements they share (a vertex, or an edge). Non-coplanar pairs are tested by
   plane clipping and coplanar pairs by 2D polygon clipping, with Fractions.
3. Cell structure.
   - Each face cell's triangles form a disk: connected, Euler characteristic 1, one boundary loop,
     and that loop is the union of the cell's four edge segments.
   - The whole surface is a closed 2-manifold with Euler characteristic 2.
4. Hypotheses of Lemma 0 v0.2 for this model, listed with their numbers.
"""
from fractions import Fraction as Fr
import itertools, json

L, S, G, RHO, A = Fr(10), Fr(3, 10), Fr(2, 10), Fr(1, 2), Fr(1)
C = Fr(2, 5)                         # sqrt(RHO^2 - S^2), exact for these values
assert C * C == RHO * RHO - S * S
TAU_E, TAU_V, TAU_F = Fr(11, 20), Fr(6, 5), Fr(1, 10**7)

E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def add(*vs): return tuple(sum(v[i] for v in vs) for i in range(3))
def mul(k, v): return tuple(k * x for x in v)
def sub(a, b): return tuple(a[i] - b[i] for i in range(3))
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


corners = list(itertools.product((0, 1), repeat=3))


def to_global(corner, local):
    """corner in {0,1}^3; local coordinates have the cube in the positive octant."""
    sgn = [1 - 2 * b for b in corner]
    return tuple(Fr(corner[i]) * L + sgn[i] * local[i] for i in range(3))


tris = []   # (p, q, r, cell)

# vertex cones
for cn in corners:
    O = to_global(cn, (0, 0, 0))
    for k in range(3):
        i, j = [a for a in range(3) if a != k]
        ei, ej, ek = (mul(1, E[i]), mul(1, E[j]), mul(1, E[k]))
        poly_local = [mul(A, ei), add(mul(A, ei), mul(C, ej), mul(-S, ek)), add(mul(C, ei), mul(C, ej), mul(-S, ek)),
                      add(mul(C, ei), mul(A, ej), mul(-S, ek)), mul(A, ej)]
        poly = [to_global(cn, p) for p in poly_local]
        face = (k, cn[k])                      # face: normal axis k, side 0 or 1
        for a_, b_ in zip(poly[:-1], poly[1:]):
            tris.append((O, a_, b_, ("F",) + face))

# edge fans
for i in range(3):
    others = [a for a in range(3) if a != i]
    for side in itertools.product((0, 1), repeat=2):      # which side for the other two axes
        cn0 = [0, 0, 0]
        for a, sd in zip(others, side):
            cn0[a] = sd
        cnA = tuple(cn0); cnB = list(cn0); cnB[i] = 1; cnB = tuple(cnB)
        for k in others:                                    # the face normal axis (the face contains axis i)
            j = [a for a in others if a != k][0]
            ei, ej, ek = E[i], E[j], E[k]
            pA0 = to_global(cnA, mul(A, ei)); pA1 = to_global(cnA, add(mul(A, ei), mul(C, ej), mul(-S, ek)))
            pB0 = to_global(cnB, mul(A, ei)); pB1 = to_global(cnB, add(mul(A, ei), mul(C, ej), mul(-S, ek)))
            face = ("F", k, cnA[k])
            tris += [(pA0, pB0, pB1, face), (pA0, pB1, pA1, face)]

# face interiors Q_f
for k in range(3):
    i, j = [a for a in range(3) if a != k]
    for side in (0, 1):
        def P(u, v):
            p = [None] * 3
            p[i], p[j] = u, v
            p[k] = -S if side == 0 else L + S
            return tuple(p)
        # boundary split at the same points as the cones and fans (no T-junctions); fan from centre
        uv = [(C, C), (A, C), (L - A, C), (L - C, C), (L - C, A), (L - C, L - A), (L - C, L - C),
              (L - A, L - C), (A, L - C), (C, L - C), (C, L - A), (C, A)]
        q = [P(u, v) for u, v in uv]
        ctr = P(L / 2, L / 2)
        for a_, b_ in zip(q, q[1:] + q[:1]):
            tris.append((ctr, a_, b_, ("F", k, side)))

res = {"n_triangles": len(tris), "dev": "sqrt(G^2+S^2) = %.4f" % float((G * G + S * S) ** 0.5)}

# ---------------- zones (exact) ----------------
def dist2_point_line(p, a, d):
    w = sub(p, a); cr = cross(w, d)
    return dot(cr, cr) / dot(d, d)


zone_ok = True
for (p, q, r, cell) in tris:
    _, k, side = cell
    pts = (p, q, r)
    on_patch = all(x[k] == (-S if side == 0 else L + S) and all(
        G <= x[a] <= L - G for a in range(3) if a != k) for x in pts)
    if on_patch:
        continue                                     # distance 0 to the patch
    # else: must be within an edge tube (rho) or a vertex ball (tau_v) of an incident cell
    # vertex cone: one vertex is a cube corner
    corner_pts = [x for x in pts if all(c in (0, L) for c in x)]
    if corner_pts and all(c in (0, L) for c in corner_pts[0]):
        O = corner_pts[0]
        if all(dot(sub(x, O), sub(x, O)) < TAU_V ** 2 for x in pts):
            continue
    # fan: all three points within rho of one cube edge line incident to this face
    okfan = False
    for i in range(3):
        if i == k:
            continue
        for b in itertools.product((0, L), repeat=3):
            if b[k] != (0 if side == 0 else L):
                continue
            a0 = list(b); a0[i] = Fr(0); a0 = tuple(a0)
            if all(dist2_point_line(x, a0, E[i]) <= RHO * RHO for x in pts):
                okfan = True
    if not okfan:
        zone_ok = False
res["zones_ok_exact"] = zone_ok and RHO < TAU_E

# ---------------- embedding (exact) ----------------
def orient(a, b, c, d):
    return dot(sub(b, a), cross(sub(c, a), sub(d, a)))


def clip_poly_halfspace(poly, n, off):
    """keep n.x <= off ; exact Fractions"""
    out = []
    for idx in range(len(poly)):
        a, b = poly[idx], poly[(idx + 1) % len(poly)]
        fa, fb = dot(n, a) - off, dot(n, b) - off
        if fa <= 0: out.append(a)
        if (fa < 0 < fb) or (fb < 0 < fa):
            t = fa / (fa - fb)
            out.append(add(a, mul(t, sub(b, a))))
    return out


def tri_intersection(T1, T2):
    """Exact intersection of two closed triangles, as a list of points (convex hull)."""
    # clip T1 by the 'prism' of T2 when coplanar; otherwise clip T1 to plane of T2 and T2's edges
    n2 = cross(sub(T2[1], T2[0]), sub(T2[2], T2[0]))
    d1 = [dot(n2, sub(x, T2[0])) for x in T1]
    if all(v == 0 for v in d1):                         # coplanar: clip T1 by T2's edge half-planes
        poly = list(T1)
        for a_, b_ in ((0, 1), (1, 2), (2, 0)):
            e = sub(T2[b_], T2[a_]); nn = cross(n2, e)      # inward normal is +nn
            c3 = T2[3 - a_ - b_]
            if dot(nn, sub(c3, T2[a_])) < 0: nn = mul(-1, nn)
            poly = clip_poly_halfspace(poly, mul(-1, nn), -dot(nn, T2[a_]))
            if not poly: return []
        return poly
    # non-coplanar: intersection lies on plane of T2; take T1 ∩ plane(T2), then clip by T2's edges
    seg = []
    for a_, b_ in ((0, 1), (1, 2), (2, 0)):
        fa, fb = d1[a_], d1[b_]
        if fa == 0: seg.append(T1[a_])
        if (fa < 0 < fb) or (fb < 0 < fa):
            t = fa / (fa - fb); seg.append(add(T1[a_], mul(t, sub(T1[b_], T1[a_]))))
    seg = list(dict.fromkeys(seg))
    if not seg: return []
    poly = seg
    for a_, b_ in ((0, 1), (1, 2), (2, 0)):
        e = sub(T2[b_], T2[a_]); nn = cross(n2, e); c3 = T2[3 - a_ - b_]
        if dot(nn, sub(c3, T2[a_])) < 0: nn = mul(-1, nn)
        if len(poly) == 1:
            poly = [p for p in poly if dot(nn, sub(p, T2[a_])) >= 0]
        else:
            poly = clip_poly_halfspace(poly, mul(-1, nn), -dot(nn, T2[a_]))
        if not poly: return []
    return poly


def on_segment(p, a, b):
    if cross(sub(p, a), sub(b, a)) != (0, 0, 0): return False
    t = dot(sub(p, a), sub(b, a)); return 0 <= t <= dot(sub(b, a), sub(b, a))


bad = []
for (i1, t1), (i2, t2) in itertools.combinations(enumerate(tris), 2):
    T1, T2 = t1[:3], t2[:3]
    # quick bbox reject
    if any(max(x[a] for x in T1) < min(x[a] for x in T2) or max(x[a] for x in T2) < min(x[a] for x in T1) for a in range(3)):
        continue
    P = tri_intersection(T1, T2) + tri_intersection(T2, T1)
    if not P: continue
    shared = [v for v in T1 if v in T2]
    def allowed(p):
        if p in shared: return True
        return len(shared) == 2 and on_segment(p, shared[0], shared[1])
    if not all(allowed(p) for p in P):
        bad.append((i1, i2))
res["embedding_violations"] = len(bad)

# ---------------- cell structure ----------------
from collections import defaultdict
def cell_stats(ts):
    V = {p for t in ts for p in t[:3]}
    edges = defaultdict(int)
    for t in ts:
        for a_, b_ in ((0, 1), (1, 2), (2, 0)):
            edges[frozenset((t[a_], t[b_]))] += 1
    chi = len(V) - len(edges) + len(ts)
    bnd = [e for e, n in edges.items() if n == 1]
    nonman = [e for e, n in edges.items() if n > 2]
    return chi, bnd, nonman


# merge collinear boundary pieces: count boundary loops via graph components
def loops(bnd):
    adj = defaultdict(set)
    for e in bnd:
        a_, b_ = tuple(e); adj[a_].add(b_); adj[b_].add(a_)
    seen, comps = set(), 0
    for v in adj:
        if v in seen: continue
        comps += 1; stack = [v]
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x); stack += list(adj[x])
    return comps, all(len(n) == 2 for n in adj.values())


faces = defaultdict(list)
for t in tris: faces[t[3]].append(t)
face_ok = {}
for f, ts in faces.items():
    chi, bnd, nonman = cell_stats(ts)
    nl, simple = loops(bnd)
    # boundary must lie on the cube edges (the edge realizations)
    on_edges = all(sum(1 for a in range(3) if p[a] in (0, L)) >= 2 for e in bnd for p in e)
    face_ok[str(f)] = dict(chi=chi, boundary_loops=nl, simple=simple, nonmanifold=len(nonman), boundary_on_edges=on_edges)
res["faces_are_disks"] = all(v["chi"] == 1 and v["boundary_loops"] == 1 and v["simple"] and v["nonmanifold"] == 0
                             and v["boundary_on_edges"] for v in face_ok.values())
chi, bnd, nonman = cell_stats(tris)
res["surface"] = dict(euler=chi, boundary_edges=len(bnd), nonmanifold_edges=len(nonman))

# ---------------- hypotheses of Lemma 0 v0.2 (numbers for this model) ----------------
dev = (float(G) ** 2 + float(S) ** 2) ** 0.5
res["hypotheses"] = {
    "E1 dev < rho < min(tau_e, reach)": [dev, float(RHO), float(TAU_E), "reach = inf (straight edges)"],
    "E3 (90 deg edges) tau_e > dev / sin(45 deg)": [float(TAU_E), dev / 0.7071],
    "exit points distinct": "c e_j - S e_k vs c e_k - S e_j, distinct since c != -S",
    "V0 patch corner inside B(p_v, r_v), r_v = 0.45": [(2 * float(G) ** 2 + float(S) ** 2) ** 0.5, 0.45],
    "V1(a) end disks disjoint: A >= max(r_v + rho, rho/sin45)": [float(A), max(0.45 + 0.5, 0.5 / 0.7071)],
    "W_v within B(p_v, tau_v): sqrt(A^2 + rho^2) < tau_v": [(1 + 0.25) ** 0.5, float(TAU_V)],
    "S1 thin features": "none (box side 10 >> 2 rho)",
}
print(json.dumps(res, indent=1, default=str))
json.dump(res, open("lemma0_box_result.json", "w"), indent=1, default=str)
