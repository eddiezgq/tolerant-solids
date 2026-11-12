import sys; sys.path.insert(0,'.')
import numpy as np, wfs_cert as W, wfs_cert2 as C
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
def pipe(): return BRepAlgoAPI_Cut(BRepPrimAPI_MakeCylinder(6.0, 40.0).Shape(), BRepPrimAPI_MakeCylinder(1.0, 40.0).Shape()).Shape()
def fil_L(r):  # all edges of L filleted
    s = W.lshape(10,2); mk = BRepFilletAPI_MakeFillet(s); ex = TopExp_Explorer(s, TopAbs_EDGE)
    while ex.More(): mk.Add(r, TopoDS.Edge(ex.Current())); ex.Next()
    return mk.Shape()
parts = {"box": lambda: W.box(10), "L-shape(fuse)": lambda: W.lshape(10,2), "slot(cut)": lambda: C.slot_block(0.2),
         "cylinder": lambda: W.cyl(3,10), "filleted box": lambda: W.filleted_box(10,2),
         "L inner fillet": lambda: C.lshape_inner_fillet(0.2), "pipe(cut)": pipe, "L all fillets 0.5": lambda: fil_L(0.5)}
for name, mk in parts.items():
    s = mk(); out = []
    fx = TopExp_Explorer(s, TopAbs_FACE)
    while fx.More():
        f = TopoDS.Face(fx.Current()); S = BRep_Tool.Surface_s(f)
        ex = TopExp_Explorer(f, TopAbs_EDGE)
        while ex.More():
            e = TopoDS.Edge(ex.Current()); tol = BRep_Tool.Tolerance_s(e)
            if BRep_Tool.Degenerated_s(e): ex.Next(); continue
            from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d
            c3 = BRepAdaptor_Curve(e); pc = BRepAdaptor_Curve2d(e, f)
            a, b = c3.FirstParameter(), c3.LastParameter()
            dev = 0.0
            for t in np.linspace(a, b, 60):
                p = c3.Value(t); uv = pc.Value(t); q = S.Value(uv.X(), uv.Y())
                dev = max(dev, p.Distance(q))
            out.append((tol, dev)); ex.Next()
        fx.Next()
    t = np.array(out); pos = t[:,1] > 1e-12
    r = (t[pos,0]/t[pos,1]).min() if pos.any() else float('inf')
    print(f"{name:18s} edge-uses={len(t):3d} tol range [{t[:,0].min():.1e}, {t[:,0].max():.1e}]  max dev {t[:,1].max():.1e}  min tol/dev {r:.3g}")

print("--- worst edges of 'L all fillets 0.5' with normal angle between the two faces at the edge midpoint")
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.BRepLProp import BRepLProp_SLProps
from OCP.TopAbs import TopAbs_REVERSED
s = fil_L(0.5); uses = []
fx = TopExp_Explorer(s, TopAbs_FACE)
while fx.More():
    f = TopoDS.Face(fx.Current()); ex = TopExp_Explorer(f, TopAbs_EDGE)
    while ex.More(): uses.append((TopoDS.Edge(ex.Current()), f)); ex.Next()
    fx.Next()
groups = []
for e, f in uses:
    for g in groups:
        if g[0].IsSame(e): g[1].append(f); break
    else: groups.append((e, [f]))
rows = []
for e, fl in groups:
    if len(fl) != 2 or BRep_Tool.Degenerated_s(e): continue
    c3 = BRepAdaptor_Curve(e); a_, b_ = c3.FirstParameter(), c3.LastParameter()
    devs, ns = [], []
    for f in fl:
        S = BRep_Tool.Surface_s(f); pc = BRepAdaptor_Curve2d(e, f)
        devs.append(max(c3.Value(t).Distance(S.Value(pc.Value(t).X(), pc.Value(t).Y())) for t in np.linspace(a_, b_, 60)))
        uv = pc.Value((a_+b_)/2); pr = BRepLProp_SLProps(BRepAdaptor_Surface(f), uv.X(), uv.Y(), 1, 1e-9)
        n = np.array(pr.Normal().Coord()); n = -n if f.Orientation() == TopAbs_REVERSED else n
        ns.append(n)
    ang = np.degrees(np.arccos(np.clip(ns[0] @ ns[1], -1, 1)))
    tol = BRep_Tool.Tolerance_s(e); dev = max(devs)
    if dev > 1e-9: rows.append((tol/dev, tol, dev, ang))
rows.sort()
for r in rows[:8]: print(f"tol/dev={r[0]:.3f} tol={r[1]:.2e} dev={r[2]:.2e} normal angle={r[3]:.1f} deg (dihedral opening ~ {180-r[3]:.1f})")
print("edges with dev>1e-9:", len(rows), "of", len(groups))
