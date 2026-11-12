"""Compare our certified wfs with what OpenCascade itself offers, on the same parts.

For each part:
  1. Check: BRepCheck_Analyzer(shape).IsValid().
  2. Wall-thickness estimate: the minimum distance between faces that share no vertex
     (BRepExtrema_DistShapeShape). Half of it is the usual "half wall thickness" estimate.
     Also: the smallest radius of curvature among analytic faces. This bounds the classical reach
     from above, and concave sharp edges make the reach 0.
  3. Offsets: BRepOffsetAPI_MakeOffsetShape (PerformByJoin, arc joins), at signed distances
     s * wfs_exact for several s, inward (negative) and outward (positive).
     For each offset we record:
       - done / exception / timeout;
       - BRepCheck validity;
       - number of shells;
       - Euler characteristic of the meshed result (V - E + F after merging coincident nodes);
       - |volume|.
     Theory (Chazal-Lieutier offsets): for |r| < wfs the offset surface is isotopic to M, so the
     shell count and the Euler characteristic must be unchanged.
Each offset runs in its own subprocess with a time limit.
"""
import sys, json, multiprocessing as mp
import numpy as np


def build(name):
    import wfs_cert2 as C
    return C.CASES[name][0](), C.CASES[name][1]


def check_and_thickness(name):
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    from OCP.TopExp import TopExp, TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE, TopAbs_VERTEX
    from OCP.TopoDS import TopoDS
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_Cone
    s, exact = build(name)
    valid = BRepCheck_Analyzer(s).IsValid()
    faces, ex = [], TopExp_Explorer(s, TopAbs_FACE)
    while ex.More():
        faces.append(TopoDS.Face(ex.Current())); ex.Next()
    verts = []
    for f in faces:
        vl, ev = [], TopExp_Explorer(f, TopAbs_VERTEX)
        while ev.More():
            vl.append(ev.Current()); ev.Next()
        verts.append(vl)
    def share(i, j):
        return any(a.IsSame(b) for a in verts[i] for b in verts[j])
    best = (np.inf, None)
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            if share(i, j):
                continue
            d = BRepExtrema_DistShapeShape(faces[i], faces[j])
            if d.IsDone() and d.Value() < best[0]:
                best = (d.Value(), (i, j))
    rmin = np.inf
    for f in faces:
        a = BRepAdaptor_Surface(f)
        t = a.GetType()
        if t == GeomAbs_Cylinder: rmin = min(rmin, a.Cylinder().Radius())
        elif t == GeomAbs_Sphere: rmin = min(rmin, a.Sphere().Radius())
        elif t == GeomAbs_Torus: rmin = min(rmin, a.Torus().MinorRadius())
    return dict(name=name, exact=exact, valid=bool(valid), n_faces=len(faces),
                min_dist_nonadjacent=float(best[0]), half_min_dist=float(best[0] / 2),
                min_curv_radius=(None if rmin == np.inf else float(rmin)))


def euler_of(shape):
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.BRep import BRep_Tool
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopoDS import TopoDS
    from OCP.TopLoc import TopLoc_Location
    BRepMesh_IncrementalMesh(shape, 0.01, False, 0.2, False)
    pts, tris = [], []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current()); loc = TopLoc_Location()
        T = BRep_Tool.Triangulation_s(f, loc)
        if T is None:
            return None
        tr = loc.Transformation(); base = len(pts)
        pts += [[*T.Node(i).Transformed(tr).Coord()] for i in range(1, T.NbNodes() + 1)]
        tris += [[base + k - 1 for k in T.Triangle(i).Get()] for i in range(1, T.NbTriangles() + 1)]
        ex.Next()
    P = np.round(np.array(pts), 7)
    _, inv = np.unique(P, axis=0, return_inverse=True)
    Tr = inv.reshape(-1)[np.array(tris)]
    Tr = Tr[(Tr[:, 0] != Tr[:, 1]) & (Tr[:, 1] != Tr[:, 2]) & (Tr[:, 0] != Tr[:, 2])]
    E = {tuple(sorted(e)) for t in Tr for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0]))}
    V = len(np.unique(Tr))
    return int(V - len(E) + len(Tr))


def one_offset(args):
    name, r, q, INTER = args
    try:
        from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeOffsetShape
        from OCP.BRepOffset import BRepOffset_Skin
        from OCP.GeomAbs import GeomAbs_Arc
        from OCP.BRepCheck import BRepCheck_Analyzer
        from OCP.GProp import GProp_GProps
        from OCP.BRepGProp import BRepGProp
        from OCP.TopExp import TopExp_Explorer
        from OCP.TopAbs import TopAbs_SHELL
        s, _ = build(name)
        mk = BRepOffsetAPI_MakeOffsetShape()
        mk.PerformByJoin(s, r, 1e-6, BRepOffset_Skin, INTER, False, GeomAbs_Arc)
        if not mk.IsDone():
            q.put(dict(status="not done")); return
        out = mk.Shape()
        if out.IsNull():
            q.put(dict(status="empty result")); return
        nsh = 0; ex = TopExp_Explorer(out, TopAbs_SHELL)
        while ex.More(): nsh += 1; ex.Next()
        g = GProp_GProps(); BRepGProp.VolumeProperties_s(out, g)
        q.put(dict(status="done", valid=bool(BRepCheck_Analyzer(out).IsValid()), shells=nsh,
                   euler=euler_of(out), volume=abs(g.Mass())))
    except Exception as e:
        q.put(dict(status="exception", err=str(e)[:120]))


def offset(name, r, timeout=120, INTER=False):
    import queue as _q
    ctx = mp.get_context("spawn"); q = ctx.Queue(); p = ctx.Process(target=one_offset, args=((name, r, q, INTER),)); p.start()
    try:
        res = q.get(timeout=timeout)          # read first: a child blocks on exit until its queue is drained
    except _q.Empty:
        res = dict(status="timeout") if p.is_alive() else dict(status="crashed", code=p.exitcode)
    p.join(5)
    if p.is_alive():
        p.terminate()
    return res


if __name__ == "__main__":
    INTER = sys.argv[1] == "inter"
    names = sys.argv[2:]
    S = [0.25, 0.5, 0.75, 0.9, 0.99, 1.01, 1.1, 1.5]
    out = []
    for nm in names:
        rec = check_and_thickness(nm)
        print(json.dumps(rec, ensure_ascii=False), flush=True)
        base = offset(nm, 0.0) if False else None
        rec["euler0"] = euler_of(build(nm)[0])
        rec["offsets"] = {}
        for sgn in (-1, 1):
            for s in S:
                r = sgn * s * rec["exact"]
                res = offset(nm, r, INTER=INTER)
                rec["offsets"][f"{sgn * s:+.2f}"] = res
                print(f"  {nm} offset {sgn * s:+.2f}*wfs = {r:+.4f}: {res}", flush=True)
        out.append(rec)
    json.dump(out, open("compare_occ_" + ("inter" if INTER else "default") + ".json", "w"), ensure_ascii=False, indent=1)
