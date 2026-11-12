"""Route A check on the fused L-shape with an inner fillet, after merging coplanar faces
(ShapeUpgrade_UnifySameDomain), in both orders. Supports the claim in notes/lemma0_check_report.md, finding 2."""
import sys, json
sys.path.insert(0, ".")
import wfs_cert as W, wfs_cert2 as C, lemma0_check as L
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve


def unify(s):
    u = ShapeUpgrade_UnifySameDomain(s, True, True, False); u.Build(); return u.Shape()


def fillet_inner(s, r):
    mk = BRepFilletAPI_MakeFillet(s); ex = TopExp_Explorer(s, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge(ex.Current()); c = BRepAdaptor_Curve(e)
        p0, p1 = c.Value(c.FirstParameter()), c.Value(c.LastParameter())
        if abs(p0.X()-2) < 1e-9 and abs(p0.Y()-2) < 1e-9 and abs(p1.X()-2) < 1e-9 and abs(p1.Y()-2) < 1e-9:
            mk.Add(r, e)
        ex.Next()
    return mk.Shape()


out = [L.check(fillet_inner(unify(W.lshape(10, 2)), 0.2), "L: fuse -> unify -> inner fillet 0.2"),
       L.check(unify(C.lshape_inner_fillet(0.2)), "L: fuse -> inner fillet 0.2 -> unify")]
json.dump(out, open("../results/merged_L_check_result.json", "w"), indent=1, default=float)
