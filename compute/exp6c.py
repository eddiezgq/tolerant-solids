"""Experiment 6c: three criteria side by side as the tolerance grows.

For each part, set every face/edge/vertex tolerance to tau and record:
  1. BRepCheck_Analyzer validity.
  2. BRepAlgoAPI_Check (geometry + self-interference): validity and the set of statuses.
  3. Our collar condition (Lemma 1b), in three states:
       PROVED  if tau + defl < LB, where LB is the certified wfs lower bound of the PL reference
               surface (wfs_cert2 runs) and defl is the mesh deflection between nominal and PL
               surfaces. All zones then lie in N_{tau+defl}(M) with tau + defl < LB <= wfs.
       FAILS   if tau >= U, where U is an exhibited critical value of the nominal surface
               (a point whose nearest set's convex hull contains it), so wfs <= U <= tau.
       UNKNOWN otherwise.
     LB values come from cert2/3/4/6 runs; U values are exact critical values of the nominal
     geometry (centres, mid-planes, axes), each stated in U_NOTE.
"""
import json, sys
import numpy as np
sys.path.insert(0, ".")
import wfs_cert as W, wfs_cert2 as C, exp6b as E
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check, BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder


def pipe():
    return BRepAlgoAPI_Cut(BRepPrimAPI_MakeCylinder(6.0, 40.0).Shape(),
                           BRepPrimAPI_MakeCylinder(1.0, 40.0).Shape()).Shape()


PARTS = {   # name: (builder, LB or None, defl used for LB, U, note on U)
    "box":          (lambda: W.box(10), 4.5304, 0.01, 5.0, "centre of the cube"),
    "plate":        (lambda: C.plate(4, 1), 0.4360, 0.01, 0.5, "mid-plane"),
    "plate_t0.3":   (lambda: C.plate(4, 0.3), 0.1369, 0.01, 0.15, "mid-plane"),
    "L-shape":      (lambda: W.lshape(10, 2), 0.8944, 0.01, 1.0, "arm mid-axis"),
    "slot_g0.2":    (lambda: C.slot_block(0.2), 0.0861, 0.01, 0.1, "slot mid-plane"),
    "cylinder":     (lambda: W.cyl(3, 10), 2.5121, 0.02, 3.0, "axis between z=3 and z=7"),
    "Lfillet_r0.2": (lambda: C.lshape_inner_fillet(0.2), 0.8938, 0.02, 1.0, "arm mid-axis"),
    "long_cyl":     (lambda: W.cyl(3, 100), None, None, 3.0, "axis"),
    "pipe":         (lambda: pipe(), None, None, 1.0, "axis inside the hole"),
    "torus":        (lambda: E.torus(0.0, 0.0), None, None, 0.5, "core circle"),
}
FRACS = [1e-7, 0.1, 0.25, 0.5, 0.75, 0.9, 1.1, 1.5]   # tau = frac * U (1e-7 means absolute 1e-7)


def collar(tau, LB, defl, U):
    if LB is not None and tau + defl < LB:
        return "已证成立"
    if tau >= U:
        return "已证不成立"
    return "算不出"


rows = []
for name, (mk, LB, defl, U, note) in PARTS.items():
    for f in FRACS:
        tau = 1e-7 if f == 1e-7 else f * U
        s = mk()
        if f != 1e-7:
            E.set_tol(s, tau)
        bc = bool(BRepCheck_Analyzer(s).IsValid())
        ch = BRepAlgoAPI_Check(s, True, True)
        sts = sorted({str(r.GetCheckStatus()).split('.')[-1].replace("BOPAlgo_", "") for r in ch.Result()})
        rows.append(dict(part=name, tau=tau, frac=f, brepcheck=bc, bop=bool(ch.IsValid()), bop_status=sts,
                         collar=collar(tau, LB, defl, U), LB=LB, U=U))
        print(f"{name:13s} tau={tau:<9.4g} BRepCheck={bc!s:5s} BOP={ch.IsValid()!s:5s} {','.join(sts):28s} 领口={rows[-1]['collar']}",
              flush=True)
json.dump(rows, open("exp6c_result.json", "w"), ensure_ascii=False, indent=1)
