"""P2 step 3: the "wall + chord" edge construction (notes/p2_phase1_report.md, end), edge part.

For an edge e with patches f, g and a parameter t, work in the normal plane Pi(t) of gamma_e:
  A, B   the section curves of the rebuilt patches P_f, P_g by Pi(t) (BRepAlgoAPI_Section), each taken as the chained
         component that ends at the patch boundary point nearest gamma(t) (b_f, b_g), walked from that end inward;
  d_f    the inward direction of A at b_f (chord from b_f to the point of A at arc length 0.3 tau_e), likewise d_g;
  wall   the line through a centre c(t) with direction w = T x (d_f - d_g) (the internal bisector of d_f, d_g; for a G1
         edge d_f ~ -d_g and w is the common normal); m = (d_f - d_g)/|.| is its normal, A belongs to side m > 0,
         B to side m < 0. Three walls are tried, one choice for all t of an edge: bisector direction through
         c = gamma(t) ("gamma") or through c = (b_f + b_g)/2 ("mid"), and the line through b_f and b_g itself ("chord",
         the P2 strip). The union of the wall lines over t is the wall surface W_e.
  cut    if b_f lies on B's side, A is cut at its first crossing a_f with the wall and only the part after a_f is kept
         (A'); otherwise A' = A and a_f = b_f. Likewise for B. The edge cell in Pi(t) is the bridge [a_f, a_g]; it lies
         in the wall line when both patches were cut, and it is the P2 strip chord when neither was.
Conditions at each t of the edge interval I_e (as in checker v3: from the last sample near v_a whose bridge lies in the
vertex ball of radius rho tau_v, or where the patches no longer meet Pi(t) inside the ball, to the first such sample
near v_b):
  W1  inside D(t) = disk of radius rho_e = 0.999 tau_e, each patch section has exactly one component;
  W2  a_f, a_g lie in D(t) (so the bridge lies in the zone of e);
  W3  inside D(t), A' lies strictly on side m > 0 after a_f and B' strictly on side m < 0 after a_g;
  W4  inside the disk of radius 3 tau_e, A' and B' are disjoint and the bridge meets them only at its ends;
  W5  where a patch is cut, the crossing is transversal (minimum angle to the wall recorded).
Continuity of a_f, a_g in t is recorded (max |delta a| / |delta gamma| over consecutive samples).
Sampled, double precision. One model per call: python3 wall_chord_check.py <index>; with no index, merge the parts into
../results/wall_chord_check.json and print the comparison with checker v3 (../results/strip_cone_check3.json).
"""
import sys, os, json, math, glob
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L
from lemma0_check_run import sloppy
from tight_vertex_survey import PARTS, GAPS
from patchface import patch_face
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir, gp_Vec

RHO = 0.95
NT = 70
OUT = "../results/wall_chord_parts"


def section_chains(face, pln, gpt, R):
    """Section curves of a face by a plane, chained into polylines; only pieces within distance R of gpt."""
    sec = BRepAlgoAPI_Section(face, pln, False); sec.ComputePCurveOn1(False)
    sec.SetNonDestructive(True)   # do not change tolerances of the patch (that changes later sections)
    sec.Build()
    polys = []
    ex = TopExp_Explorer(sec.Shape(), TopAbs_EDGE)
    while ex.More():
        c = BRepAdaptor_Curve(TopoDS.Edge(ex.Current()))
        a, b = c.FirstParameter(), c.LastParameter()
        P = np.array([L.V(c.Value(u)) for u in np.linspace(a, b, 300)])
        if np.min(np.linalg.norm(P - gpt, axis=1)) < R:
            polys.append(P)
        ex.Next()
    # chain pieces with coinciding ends
    tol = 1e-7
    chains = []
    while polys:
        cur = polys.pop()
        grown = True
        while grown:
            grown = False
            for i, Q in enumerate(polys):
                if np.linalg.norm(cur[-1] - Q[0]) < tol: cur = np.vstack([cur, Q[1:]])
                elif np.linalg.norm(cur[-1] - Q[-1]) < tol: cur = np.vstack([cur, Q[::-1][1:]])
                elif np.linalg.norm(cur[0] - Q[-1]) < tol: cur = np.vstack([Q, cur[1:]])
                elif np.linalg.norm(cur[0] - Q[0]) < tol: cur = np.vstack([Q[::-1], cur[1:]])
                else: continue
                polys.pop(i); grown = True; break
        chains.append(cur)
    return chains


def clip_components(P2, R):
    """Number of components of a 2D polyline inside the disk |x| < R."""
    ins = np.linalg.norm(P2, axis=1) < R
    return int(np.sum(ins[1:] & ~ins[:-1]) + (1 if ins[0] else 0))


def seg_hit(p, q, a, b):
    d1, d2 = q - p, b - a
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-300: return None
    w = a - p
    s = (w[0] * d2[1] - w[1] * d2[0]) / den; u = (w[0] * d1[1] - w[1] * d1[0]) / den
    return (s, u) if (0 <= s <= 1 and 0 <= u <= 1) else None


def poly_meets(P, Q):
    """Do two 2D polylines intersect? (vectorised segment test)"""
    if len(P) < 2 or len(Q) < 2: return False
    p, r = P[:-1][:, None, :], (P[1:] - P[:-1])[:, None, :]
    q, s = Q[:-1][None, :, :], (Q[1:] - Q[:-1])[None, :, :]
    cr = lambda x, y: x[..., 0] * y[..., 1] - x[..., 1] * y[..., 0]
    den = cr(r, s); qp = q - p
    with np.errstate(divide="ignore", invalid="ignore"):
        tt = cr(qp, s) / den; uu = cr(qp, r) / den
    return bool(np.any((np.abs(den) > 1e-300) & (tt >= 0) & (tt <= 1) & (uu >= 0) & (uu <= 1)))


def walk_from(P2, start_idx_end):
    """Orient a chained 2D polyline so it starts at the given end (0 = first point, -1 = last)."""
    return P2 if start_idx_end == 0 else P2[::-1]


def point_at_arclength(P, s):
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    if s >= d[-1]: return P[-1]
    i = int(np.searchsorted(d, s)); f = (s - d[i - 1]) / (d[i] - d[i - 1])
    return P[i - 1] + f * (P[i] - P[i - 1])


def cut(P, c, m, side):
    """P walked from its boundary end. side = +1/-1: the side of the wall (normal m through c) P must keep.
    Returns (a, kept polyline, cut?, crossing angle deg)."""
    h = (P - c) @ m * side
    if h[0] > 0:
        return P[0], P, False, None
    k = np.nonzero(h > 0)[0]
    if len(k) == 0:
        return None, None, None, None
    i = int(k[0]); f = h[i - 1] / (h[i - 1] - h[i]); a = P[i - 1] + f * (P[i] - P[i - 1])
    seg = P[i] - P[i - 1]
    ang = math.degrees(math.asin(min(1.0, abs(float(seg @ m)) / np.linalg.norm(seg))))
    return a, np.vstack([a, P[i:]]), True, ang


WALLS = ("gamma", "mid", "chord")


def edge_check(M, PF, ei, rv):
    c = BRepAdaptor_Curve(M.E[ei]); a0, b0 = c.FirstParameter(), c.LastParameter()
    (f, _), (g, _) = M.uses[ei]
    te = M.te[ei]
    sm = L.edge_samples(M, ei, ts=np.linspace(a0, b0, 200)); reach = L.edge_reach(sm)
    rho_e = 0.999 * min(te, reach)
    va, vb = M.ev[ei]
    Lp = b0 - a0
    geo = np.geomspace(1e-5, 0.05, 15) * Lp
    ts = np.unique(np.concatenate([a0 + geo, np.linspace(a0, b0, NT), b0 - geo]))
    R3 = 3 * te
    # boundary curves beta_{f,e}, beta_{g,e} (pcurve images), to recognise the section end that lies on this edge
    from OCP.BRepAdaptor import BRepAdaptor_Curve2d, BRepAdaptor_Surface
    beta = []
    for fi, oe in M.uses[ei]:
        pc = BRepAdaptor_Curve2d(oe, M.F[fi]); S = BRepAdaptor_Surface(M.F[fi])
        beta.append(np.array([L.V(S.Value(pc.Value(x).X(), pc.Value(x).Y())) for x in np.linspace(a0, b0, 4000)]))
    def dist_poly(x, B):
        A, D = B[:-1], B[1:] - B[:-1]
        u = np.clip(np.einsum("ij,ij->i", x - A, D) / np.maximum(np.einsum("ij,ij->i", D, D), 1e-300), 0, 1)
        return float(np.min(np.linalg.norm(A + u[:, None] * D - x, axis=1)))
    # sections once per t
    secs = []
    for t in ts:
        p, d = gp_Pnt(), gp_Vec(); c.D1(t, p, d); gpt, T = L.V(p), L.V(d) / d.Magnitude()
        pln = gp_Pln(gp_Pnt(*gpt), gp_Dir(*T))
        e1 = np.cross(T, [1, 0, 0])
        if np.linalg.norm(e1) < 0.3: e1 = np.cross(T, [0, 1, 0])
        e1 /= np.linalg.norm(e1); e2 = np.cross(T, e1)
        to2 = lambda X: np.stack([(X - gpt) @ e1, (X - gpt) @ e2], axis=-1)
        sides = []
        for si, fi in enumerate((f, g)):
            ch = section_chains(PF[fi], pln, gpt, R3)
            ends = [(np.linalg.norm(C[k] - gpt), j, k) for j, C in enumerate(ch) for k in (0, -1)
                    if dist_poly(C[k], beta[si]) < 0.05 * te]
            if not ends:
                sides = None; break
            best = min(ends)
            sides.append(dict(P=to2(walk_from(ch[best[1]], best[2])), ncomp=sum(clip_components(to2(C), rho_e) for C in ch)))
        secs.append((t, gpt, e1, e2, sides))
    in_ball = lambda X: any(np.linalg.norm(X - M.p[w]) < rv[w] for w in (va, vb))
    res = {}
    for wall in WALLS:
        status, data = [], []
        for t, gpt, e1, e2, sides in secs:
            to3 = lambda x: gpt + x[0] * e1 + x[1] * e2
            if sides is None:
                status.append("ball" if in_ball(gpt) else "no section"); data.append(None); continue
            Pf, Pg = sides[0]["P"], sides[1]["P"]
            bf, bg = Pf[0], Pg[0]
            df = point_at_arclength(Pf, 0.3 * te) - bf; dg = point_at_arclength(Pg, 0.3 * te) - bg
            df /= np.linalg.norm(df); dg /= np.linalg.norm(dg)
            if wall == "chord":
                w = bg - bf
                if np.linalg.norm(w) < 1e-12 * te:
                    status.append("W0 chord degenerate"); data.append(None); continue
                w /= np.linalg.norm(w); m = np.array([-w[1], w[0]])
                if m @ (df - dg) < 0: m = -m
                cc = 0.5 * (bf + bg)
            else:
                m = df - dg
                if np.linalg.norm(m) < 1e-9:
                    status.append("d_f = d_g (cusp)"); data.append(None); continue
                m /= np.linalg.norm(m)
                cc = np.zeros(2) if wall == "gamma" else 0.5 * (bf + bg)
            af, Af, cutf, angf = cut(Pf, cc, m, +1)
            ag, Ag, cutg, angg = cut(Pg, cc, m, -1)
            if af is not None and ag is not None and in_ball(to3(af)) and in_ball(to3(ag)) and \
                    any(np.linalg.norm(to3(af) - M.p[x]) < rv[x] and np.linalg.norm(to3(ag) - M.p[x]) < rv[x] for x in (va, vb)):
                status.append("ball"); data.append(None); continue
            why = None
            if af is None or ag is None:
                why = "W3 patch never reaches its side"
            elif sides[0]["ncomp"] != 1 or sides[1]["ncomp"] != 1:
                why = "W1 components in D(t)"
            elif np.linalg.norm(af) >= rho_e or np.linalg.norm(ag) >= rho_e:
                why = "W2 bridge end outside D(t)"
            else:
                inD = lambda X: X[np.linalg.norm(X, axis=1) < rho_e]
                hf = (inD(Af[1:]) - cc) @ m; hg = (inD(Ag[1:]) - cc) @ m
                if (len(hf) and hf.min() <= 0) or (len(hg) and hg.max() >= 0):
                    why = "W3 kept part re-enters the other side"
                else:
                    in3 = lambda X: X[: (np.argmax(np.linalg.norm(X, axis=1) > R3) or len(X))]
                    Af3, Ag3 = in3(Af), in3(Ag)
                    if poly_meets(Af3, Ag3):
                        why = "W4 kept parts meet"
                    elif np.linalg.norm(ag - af) > 1e-12:
                        br = np.array([af + 1e-3 * (ag - af), ag - 1e-3 * (ag - af)])
                        if poly_meets(br, Af3) or poly_meets(br, Ag3):
                            why = "W4 bridge meets a kept part"
            status.append(why or "ok")
            data.append((gpt, to3(af), to3(ag), cutf or cutg, [x for x in (angf, angg) if x is not None]) if why is None else None)
        n = len(status)
        lo = max([i for i in range(n // 2) if status[i] == "ball"] + [-1])
        hi = min([i for i in range(n // 2, n) if status[i] == "ball"] + [n])
        rec = dict(fail={}, examples=[], n_t=0, n_cut=0, min_cross_deg=90.0, max_jump=0.0,
                   ends_reach_balls=bool(lo >= 0 and hi < n))
        prev = None
        for i in range(lo + 1, hi):
            st = status[i]
            if st == "ball":   # a ball sample in the middle: treat as a gap in the interval
                prev = None; continue
            rec["n_t"] += 1
            if st != "ok":
                rec["fail"][st] = rec["fail"].get(st, 0) + 1
                if len(rec["examples"]) < 3: rec["examples"].append((float((secs[i][0] - a0) / Lp), st))
                prev = None; continue
            gpt, A3, B3, wascut, angs = data[i]
            rec["n_cut"] += bool(wascut)
            if angs: rec["min_cross_deg"] = min(rec["min_cross_deg"], min(angs))
            if prev is not None:
                dgam = np.linalg.norm(gpt - prev[0])
                if dgam > 0:
                    rec["max_jump"] = max(rec["max_jump"], max(np.linalg.norm(A3 - prev[1]), np.linalg.norm(B3 - prev[2])) / dgam)
            prev = (gpt, A3, B3)
        rec["ok"] = not rec["fail"] and rec["n_t"] > 0
        res[wall] = rec
    return dict(tau_e=te, reach=reach, faces=[int(f), int(g)], **res)


def run(index):
    name, g = [(n, g) for n in PARTS for g in GAPS][index]
    key = f"{name}, g={g}"
    M = L.Model(sloppy(PARTS[name](), g))
    PF = [patch_face(fc) for fc in M.F]
    PF = [p if p is not None else fc for p, fc in zip(PF, M.F)]
    rv = [RHO * M.tv[v] for v in range(len(M.Vx))]
    out = dict(key=key, rho=RHO, edges={})
    for ei in range(len(M.E)):
        if len(M.uses[ei]) != 2 or M.uses[ei][0][0] == M.uses[ei][1][0]:
            out["edges"][ei] = dict(kind="seam/other (not covered)"); continue
        try:
            out["edges"][ei] = edge_check(M, PF, ei, rv)
        except Exception as ex:
            out["edges"][ei] = dict(error=repr(ex))
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/{index:02d}.json", "w"), indent=1, default=float)
    ok = [e for e in out["edges"].values() if any(e.get(w, {}).get("ok") for w in WALLS)]
    print(key, f"edges passing (some wall): {len(ok)}/{len(out['edges'])}", flush=True)


def main():
    v3 = json.load(open("../results/strip_cone_check3.json"))
    allp = {}
    for fn in sorted(glob.glob(f"{OUT}/*.json")):
        d = json.load(open(fn)); allp[d["key"]] = d
    for key, d in allp.items():
        e3 = v3.get(key, {}).get("edges", {})
        rows = dict(n=0, wall_ok=0, gamma_ok=0, mid_ok=0, chord_ok=0, v3_strip_ok=0, v3_bad_now_ok=0, v3_bad_still_bad=[], new_fail=[])
        for ei, e in d["edges"].items():
            if "gamma" not in e: continue
            rows["n"] += 1
            okw = {w: e[w]["ok"] for w in WALLS}
            for w in WALLS: rows[f"{w}_ok"] += okw[w]
            okg = any(okw.values()); okm = okg; rows["wall_ok"] += okg
            r3 = e3.get(ei, {})
            v3ok = r3.get("kind") == "strip" and r3.get("E1_fail", 1) == 0 and r3.get("E4a_fail", 1) == 0
            rows["v3_strip_ok"] += v3ok
            if not v3ok:
                if okg or okm: rows["v3_bad_now_ok"] += 1
                else: rows["v3_bad_still_bad"].append((ei, {w: e[w]["fail"] for w in WALLS}))
            elif not (okg or okm):
                rows["new_fail"].append((ei, {w: e[w]["fail"] for w in WALLS}))
        d["summary"] = rows
        print(key, {k: v for k, v in rows.items()})
    json.dump(allp, open("../results/wall_chord_check.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    if len(sys.argv) > 1: run(int(sys.argv[1]))
    else: main()
