import sys; sys.path.insert(0,'.')
import exp6b as E
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Check
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
def pipe(ri, ro, H):
    return BRepAlgoAPI_Cut(BRepPrimAPI_MakeCylinder(ro, H).Shape(), BRepPrimAPI_MakeCylinder(ri, H).Shape()).Shape()
def count(s, k):
    n=0; ex=TopExp_Explorer(s,k)
    while ex.More(): n+=1; ex.Next()
    return n
for tau in (1e-7, 1.0, 1.3, 1.5):
    s = pipe(1.0, 6.0, 40.0)
    if tau > 1e-6: E.set_tol(s, tau)
    ch = BRepAlgoAPI_Check(s, True, True)
    print("pipe tau", tau, "faces", count(s,TopAbs_FACE), "edges", count(s,TopAbs_EDGE), BRepCheck_Analyzer(s).IsValid(), ch.IsValid(), sorted({str(r.GetCheckStatus()).split('.')[-1] for r in ch.Result()}))
