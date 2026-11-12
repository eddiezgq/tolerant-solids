"""Review: inward tangents on the re-trimmed (MakerVolume) model, to see where T's minimum comes from."""
import sys, math
import numpy as np
sys.path.insert(0, ".")
import lemma0_check as L, lemma0_check_run as R, reintersect_curved as RC
from OCP.BOPAlgo import BOPAlgo_MakerVolume
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_IN
from OCP.TopoDS import TopoDS
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.BRepAdaptor import BRepAdaptor_Curve2d, BRepAdaptor_Surface
from OCP.gp import gp_Pnt2d, gp_Vec2d

def rebuild(shape):
    M = L.Model(shape); c0, _ = RC.centre(RC.as_solid(shape))
    mv = BOPAlgo_MakerVolume()
    for f in M.F: mv.AddArgument(RC.extended_face(f))
    mv.Perform()
    sols, ex = [], TopExp_Explorer(mv.Shape(), TopAbs_SOLID)
    while ex.More(): sols.append(TopoDS.Solid(ex.Current())); ex.Next()
    return M, L.Model(min(sols, key=lambda s: np.linalg.norm(RC.centre(s)[0] - c0)))

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "sloppy wedge 30deg g=0.01"
    M, N = rebuild(R.PARTS[name]())
    for i in range(len(N.E)):
        sm = L.edge_samples(N, i); sd = sm["sides"]
        if len(sd) != 2 or sd[0]["face"] == sd[1]["face"]: continue
        a, b = sd[0]["u"][100], sd[1]["u"][100]
        ang = math.degrees(math.acos(np.clip(a @ b, -1, 1)))
        print(i, np.round(sm["G"][100], 2), np.round(a, 3), np.round(b, 3), "angle %.1f T %.1f" % (ang, 180 - ang))
