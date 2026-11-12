"""Run lemma0_check on exact OpenCascade parts and on 'sloppy' parts that imitate imported data:
faces are moved apart by up to g and then sewn (BRepBuilderAPI_Sewing), so the sewn edges carry
tolerances of the order of the gaps."""
import sys, json, math
import numpy as np
sys.path.insert(0, ".")
import wfs_cert as W, wfs_cert2 as C
import lemma0_check as L
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt, gp_Vec, gp_Trsf
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing, BRepBuilderAPI_Transform, BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet


def faces(s):
    out, ex = [], TopExp_Explorer(s, TopAbs_FACE)
    while ex.More():
        out.append(TopoDS.Face(ex.Current())); ex.Next()
    return out


def sloppy(shape, g, seed=1, sew_factor=4.0):
    rng = np.random.default_rng(seed)
    sew = BRepBuilderAPI_Sewing(sew_factor * g)
    for f in faces(shape):
        d = rng.normal(size=3); d *= g * rng.uniform(0.5, 1.0) / np.linalg.norm(d)
        tr = gp_Trsf(); tr.SetTranslation(gp_Vec(*d))
        sew.Add(BRepBuilderAPI_Transform(f, tr, True).Shape())
    sew.Perform()
    return sew.SewedShape()


def wedge(angle_deg, L=10.0, H=5.0):
    a = math.radians(angle_deg)
    poly = BRepBuilderAPI_MakePolygon(gp_Pnt(0, 0, 0), gp_Pnt(L, -L * math.tan(a / 2), 0),
                                      gp_Pnt(L, L * math.tan(a / 2), 0), True)
    f = BRepBuilderAPI_MakeFace(poly.Wire()).Face()
    return BRepPrimAPI_MakePrism(f, gp_Vec(0, 0, H)).Shape()


def pipe():
    return BRepAlgoAPI_Cut(BRepPrimAPI_MakeCylinder(6.0, 40.0).Shape(), BRepPrimAPI_MakeCylinder(1.0, 40.0).Shape()).Shape()


def fil_L(r):
    s = W.lshape(10, 2); mk = BRepFilletAPI_MakeFillet(s); ex = TopExp_Explorer(s, TopAbs_EDGE)
    while ex.More():
        mk.Add(r, TopoDS.Edge(ex.Current())); ex.Next()
    return mk.Shape()


PARTS = {
    "box": lambda: W.box(10),
    "cylinder": lambda: W.cyl(3, 10),
    "pipe(cut)": pipe,
    "slot_g0.2": lambda: C.slot_block(0.2),
    "filleted box r2": lambda: W.filleted_box(10, 2),
    "L inner fillet 0.2": lambda: C.lshape_inner_fillet(0.2),
    "L all fillets 0.5": lambda: fil_L(0.5),
    "wedge 10deg": lambda: wedge(10),
    "sloppy box g=0.01": lambda: sloppy(W.box(10), 0.01),
    "sloppy box g=0.1": lambda: sloppy(W.box(10), 0.1),
    "sloppy wedge 30deg g=0.01": lambda: sloppy(wedge(30), 0.01),
    "sloppy wedge 10deg g=0.01": lambda: sloppy(wedge(10), 0.01),
    "sloppy plate t=0.05 g=0.01": lambda: sloppy(C.plate(4, 0.05), 0.01),
    "sloppy cylinder g=0.01": lambda: sloppy(W.cyl(3, 10), 0.01),
}

if __name__ == "__main__":
    names = sys.argv[1:] or list(PARTS)
    out = []
    for n in names:
        try:
            r = L.check(PARTS[n](), n)
        except Exception as ex:
            print(f"== {n}: ERROR {type(ex).__name__}: {ex}")
            r = dict(name=n, error=str(ex))
        out.append(r)
    json.dump(out, open("lemma0_check_result.json", "w"), indent=1, default=float)
