"""Experiment 6b (revised): a single-shell, genus-1 model that passes BOTH OpenCascade checks
and has a second realization whose solid is not even homeomorphic to the nominal solid.

Model.
  - A thick pipe: outer radius RO, inner radius RI, height H, along the z-axis.
  - Faces: outer cylinder, inner cylinder, two annular caps. Every face, edge and vertex gets
    tolerance TAU.
  - Expected: BRepCheck_Analyzer and BRepAlgoAPI_Check (with self-interference) both pass.
  - wfs <= RI, because every point of the axis inside the hole is critical. TAU > RI, so the collar
    condition fails.

Realization 1: the nominal geometry. The solid is a solid torus (fundamental group Z).

Realization 2: everything is nominal except the inner face, which becomes a tube around a centreline gamma.
  - gamma runs up the axis with radius RI, then "flares" to a thin tube of radius EPS (horizontal
    cross-sections, z strictly increasing).
  - It rises vertically to a small trefoil arc centred near the inner seam line, rises vertically again,
    flares back to radius RI, and runs up the axis.
  - The solid becomes a pipe with a knotted hole. Its complement contains the knotted arc, and the
    solid's fundamental group is the trefoil group (non-abelian), so the two solids are not homeomorphic.

Checks.
  (z) Zones.
      - Every tube point lies within TAU of the nominal inner face (|r - RI| <= TAU, 0 <= z <= H).
      - Every point that can carry the realized seam edge lies within TAU of the nominal seam line
        (x = RI, y = 0).
      - Edges on the caps and the vertices are unchanged.
  (e) Embedding.
      - Flare cross-sections are horizontal circles at strictly increasing heights.
      - The thin part is a tube of radius EPS around a smooth curve. Check EPS * curvature_max < 1, and
        that the distance between centreline points more than WIN apart in arc length exceeds 2 EPS.
      - The thin part stays clear of the flares: they occupy disjoint height ranges, except where they join.
      - Distance to the outer face and caps stays positive.
  (k) Knot type of the centreline, closed far away, computed with pyknotid (Alexander polynomial and
      determinant): unknot for realization 1, trefoil for realization 2.
"""
import json
import numpy as np

RI, RO, H, TAU = 1.0, 6.0, 40.0, 1.3
EPS = 0.005
KC = np.array([0.6, 0.0])      # knot centre (x, y)
KS, KD = 0.13, 0.12            # trefoil diagram scale (in the x-z plane) and depth scale (y)


def trefoil(t):
    """Trefoil whose diagram lies in the x-z plane (viewed along y); y is the depth at crossings."""
    return np.stack([KC[0] + KS * (np.sin(t) + 2 * np.sin(2 * t)),
                     KC[1] + KD * (-np.sin(3 * t)),
                     H / 2 + KS * (np.cos(t) - 2 * np.cos(2 * t))], -1)


def seg(a, b, n):
    s = np.linspace(0, 1, n)[:, None]
    return a + s * (b - a)


def smooth(s):              # 0..1 smoothstep
    return s * s * (3 - 2 * s)


def chaikin(P, it=6):
    for _ in range(it):
        Q = [P[0]]
        for a, b in zip(P[:-1], P[1:]):
            Q += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        Q.append(P[-1]); P = np.array(Q)
    return P


def resample(P, n):
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    u = np.linspace(0, L[-1], n)
    return np.stack([np.interp(u, L, P[:, k]) for k in range(3)], 1)


# Cut the diagram at its topmost point. One end goes straight up. The other goes up a little,
# out to the right beyond the diagram, then straight down past the bottom, crossing no strand.
tt = np.linspace(0, 2 * np.pi, 20000, endpoint=False)
P = trefoil(tt)
t0 = tt[np.argmax(P[:, 2])]
delta = 0.2
ends = trefoil(np.array([t0 + delta, t0 - delta]))
sgn = 1 if ends[0, 0] > ends[1, 0] else -1           # Pin = right-hand end
arc_t = np.linspace(t0 + sgn * delta, t0 + sgn * (2 * np.pi - delta), 6000)
arc = trefoil(arc_t)
Pin, Pout = arc[0], arc[-1]
ztop, zbot = P[:, 2].max(), P[:, 2].min()
xside = KC[0] + 3.4 * KS
zlo, zhi = zbot - 1.0, ztop + 1.0
z1, z2 = zlo - 6.0, zlo                                 # bottom flare
z3, z4 = zhi, zhi + 6.0                                 # top flare
m = 0.15
# one control polyline for the whole thin part (route, knot arc, rise), smoothed as a single curve so
# that the junctions have no kinks; the end points stay fixed and the ends stay vertical
gap = abs(Pin[0] - Pout[0])
xin, xout = Pin[0] - 0.3 * gap, Pout[0] + 0.3 * gap       # the two tails rise side by side inside the gap
ctrl = np.vstack([[[xside, Pin[1], z2], [xside, Pin[1], z2 + 0.5], [xside, Pin[1], ztop + m],
                   [xin, Pin[1], ztop + m], [xin, Pin[1], Pin[2]]], arc[::60], arc[-1:],
                  [[xout, Pout[1], Pout[2]], [xout, Pout[1], ztop + m], [xout, Pout[1], z3 - 0.5],
                   [xout, Pout[1], z3]]])
thin_all = resample(chaikin(ctrl, 7), 12000)
thin_all[0] = ctrl[0]; thin_all[-1] = ctrl[-1]
pieces = []
zb = np.linspace(0, z1, 400); pieces.append((np.stack([0 * zb, 0 * zb, zb], 1), np.full(len(zb), RI)))
s = np.linspace(0, 1, 2000); w = smooth(s)
fl1 = np.stack([w * xside, w * Pin[1], z1 + s * (z2 - z1)], 1)
pieces.append((fl1, RI + w * (EPS - RI)))
pieces.append((thin_all, np.full(len(thin_all), EPS)))
fl2 = np.stack([(1 - w) * xout, (1 - w) * Pout[1], z3 + s * (z4 - z3)], 1)
pieces.append((fl2, EPS + w * (RI - EPS)))
zt = np.linspace(z4, H, 400); pieces.append((np.stack([0 * zt, 0 * zt, zt], 1), np.full(len(zt), RI)))

res = dict(RI=RI, RO=RO, H=H, TAU=TAU, EPS=EPS)

# ---- (z) zones -----------------------------------------------------------------------------
ang = np.linspace(0, 2 * np.pi, 64, endpoint=False)
worst_face, worst_seam = 0.0, 0.0
for k, (C, rad) in enumerate(pieces):
    horiz = k in (0, 1, 3, 4)                      # horizontal cross-sections
    if horiz:
        pts = C[:, None, :] + rad[:, None, None] * np.stack([np.cos(ang), np.sin(ang), 0 * ang], -1)[None]
        seam = C + rad[:, None] * np.array([1.0, 0, 0])
    else:                                          # thin tube: every point within EPS of the centreline
        pts = C[:, None, :] + EPS * np.stack([np.cos(ang), np.sin(ang), 0 * ang], -1)[None]   # sample
        seam = C
    pts = pts.reshape(-1, 3)
    r = np.hypot(pts[:, 0], pts[:, 1])
    worst_face = max(worst_face, float(np.max(np.abs(r - RI))) + (0 if horiz else EPS))
    dseam = np.hypot(seam[:, 0] - RI, seam[:, 1]) + (0 if horiz else EPS)
    worst_seam = max(worst_seam, float(dseam.max()))
    assert pts[:, 2].min() >= -1e-9 and pts[:, 2].max() <= H + 1e-9
res["max_dist_to_nominal_inner_face"] = worst_face
res["max_dist_seam_to_nominal_seam"] = worst_seam
res["zones_ok"] = worst_face <= TAU and worst_seam <= TAU

# ---- (e) embedding ---------------------------------------------------------------------------
res["flare_heights_increasing"] = bool(np.all(np.diff(fl1[:, 2]) > 0) and np.all(np.diff(fl2[:, 2]) > 0))
thin = thin_all


def curvature_max(C):
    d1 = np.gradient(C, axis=0); d2 = np.gradient(d1, axis=0)
    k = np.linalg.norm(np.cross(d1, d2), axis=1) / np.linalg.norm(d1, axis=1) ** 3
    return float(k[2:-2].max())


res["eps_times_curvature_max"] = EPS * curvature_max(thin_all)
seglen = np.linalg.norm(np.diff(thin, axis=0), axis=1)
sarc = np.concatenate([[0], np.cumsum(seglen)])
from scipy.spatial import cKDTree
tree = cKDTree(thin)
WIN = 8 * EPS
pairs = tree.query_pairs(2 * EPS + 0.01, output_type="ndarray")
far = np.abs(sarc[pairs[:, 0]] - sarc[pairs[:, 1]]) > WIN
res["close_far_pairs_in_thin_tube"] = int(far.sum())
pr = tree.query_pairs(0.3, output_type="ndarray")
farm = np.abs(sarc[pr[:, 0]] - sarc[pr[:, 1]]) > WIN
dmin = float(np.min(np.linalg.norm(thin[pr[farm, 0]] - thin[pr[farm, 1]], axis=1))) if farm.any() else 0.3
res["thin_tube_min_nonlocal_centreline_dist"] = float(dmin)
res["thin_tube_embedded"] = res["eps_times_curvature_max"] < 1 and dmin > 2 * EPS
res["thin_part_z_range"] = [float(thin[:, 2].min()), float(thin[:, 2].max())]
res["flare_z_ranges"] = [[z1, z2], [z3, z4]]
res["thin_clear_of_flares"] = thin[:, 2].min() >= z2 - 1e-9 and thin[:, 2].max() <= z3 + 1e-9
res["max_radius_of_realized_inner_surface"] = float(max(
    np.max(np.hypot(C[:, 0], C[:, 1]) + rad) for C, rad in pieces))
res["clear_of_outer_face"] = res["max_radius_of_realized_inner_surface"] < RO

# ---- (k) knot type -------------------------------------------------------------------------
for _a, _t in (("float", float), ("int", int), ("complex", complex), ("bool", bool)):
    if not hasattr(np, _a): setattr(np, _a, _t)      # pyknotid uses removed numpy aliases
from pyknotid.spacecurves import Knot
cl = np.vstack([C[::4] if k == 2 else C[::20] for k, (C, _) in enumerate(pieces)])
cl = cl[np.r_[True, np.linalg.norm(np.diff(cl, axis=0), axis=1) > 1e-9]]
far_loop = np.array([[0, 0, H + 5], [50, 0, H + 5], [50, 0, -5], [0, 0, -5]])
closed2 = np.vstack([cl, far_loop])
axis = np.stack([np.zeros(400), np.zeros(400), np.linspace(0, H, 400)], 1)
closed1 = np.vstack([axis, far_loop])
# rotate generically first: vertical segments would project to points along the default z view
rng = np.random.default_rng(7)
Qm, _ = np.linalg.qr(rng.normal(size=(3, 3)))
res["knot_view_rotation_seed"] = 7
# pyknotid misses crossings when segments are very short (verified: a trefoil sampled with segments
# of length ~1e-3 reads as unknotted); knot type is scale invariant, so scale up by 100 first
SC = 100.0
res["knot_scale_factor"] = SC
k2, k1 = Knot(SC * closed2 @ Qm.T, verbose=False), Knot(SC * closed1 @ Qm.T, verbose=False)
res["alexander_realization2"] = str(k2.alexander_polynomial())
res["determinant_realization2"] = int(round(abs(k2.determinant())))
res["alexander_nominal"] = str(k1.alexander_polynomial())
res["determinant_nominal"] = int(round(abs(k1.determinant())))
res = {k: (bool(v) if isinstance(v, np.bool_) else v) for k, v in res.items()}
print(json.dumps(res, indent=1))
json.dump(res, open("exp6b2_result.json", "w"), indent=1)

# ---- OpenCascade checks on the toleranced nominal model (review fix: record them here) -------
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Check
from OCP.BRepCheck import BRepCheck_Analyzer
import exp6b as E
pipe = BRepAlgoAPI_Cut(BRepPrimAPI_MakeCylinder(RO, H).Shape(), BRepPrimAPI_MakeCylinder(RI, H).Shape()).Shape()
E.set_tol(pipe, TAU)
chk = BRepAlgoAPI_Check(pipe, True, True)
res["occ_brepcheck_valid"] = bool(BRepCheck_Analyzer(pipe).IsValid())
res["occ_bop_check_valid"] = bool(chk.IsValid())
res["occ_bop_status"] = sorted({str(r.GetCheckStatus()).split('.')[-1] for r in chk.Result()})
res["window_vs_pi_over_kappa"] = [8 * EPS, float(np.pi * EPS / res["eps_times_curvature_max"])]
print(json.dumps({k: res[k] for k in ("occ_brepcheck_valid", "occ_bop_check_valid", "occ_bop_status", "window_vs_pi_over_kappa")}))
json.dump(res, open("exp6b2_result.json", "w"), indent=1)
