"""Rebuild the trimmed patch P_f of a face from its own pcurves (the B-rep face shares 3D edge curves with its
neighbours, so distances between B-rep faces are 0 along every edge; the patches themselves need not touch)."""
from OCP.BRepTools import BRepTools_WireExplorer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_WIRE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCP.BRepLib import BRepLib


def patch_face(f):
    S = BRep_Tool.Surface_s(f); wires = []
    ex = TopExp_Explorer(f, TopAbs_WIRE)
    while ex.More():
        w = TopoDS.Wire(ex.Current()); mw = BRepBuilderAPI_MakeWire()
        we = BRepTools_WireExplorer(w, f)
        while we.More():
            e = we.Current(); a, b = BRep_Tool.Range_s(e)
            c2 = BRep_Tool.CurveOnSurface_s(e, f, a, b)
            ne = BRepBuilderAPI_MakeEdge(c2, S, a, b).Edge(); BRepLib.BuildCurves3d_s(ne)
            mw.Add(ne); we.Next()
        if not mw.IsDone():
            return None
        wires.append(mw.Wire()); ex.Next()
    mf = BRepBuilderAPI_MakeFace(S, wires[0], True)
    for w in wires[1:]:
        mf.Add(w)
    return mf.Face() if mf.IsDone() else None
