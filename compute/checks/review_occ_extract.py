"""Independent extraction of planar/straight B-rep data from an OCC shape, as exact rationals.

Written for the review of notes/lemma0_v03.md (does not use lemma0_check.Model or edge_samples).
Every quantity is read from the stored geometry (Geom_Plane / Geom_Line / Geom2d_Line, plus the
TopLoc_Location transformations) and converted to fractions.Fraction exactly; the surfaces, curves and
pcurves are then the exact rational affine maps that OCC evaluates (up to OCC's own rounding when it
evaluates them, which is not part of the mathematical data).
"""
import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from OCP.TopExp import TopExp_Explorer, TopExp
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_WIRE, TopAbs_SHELL, TopAbs_REVERSED, TopAbs_FORWARD
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool, BRep_TEdge
from OCP.BRepTools import BRepTools_WireExplorer
from OCP.TopLoc import TopLoc_Location
from OCP.Geom import Geom_Plane, Geom_Line, Geom_TrimmedCurve
from OCP.Geom2d import Geom2d_Line, Geom2d_TrimmedCurve, Geom2d_BSplineCurve


def F3(x, y, z):
    return (Fr(x), Fr(y), Fr(z))


def add(a, b): return tuple(p + q for p, q in zip(a, b))
def sub(a, b): return tuple(p - q for p, q in zip(a, b))
def mul(s, a): return tuple(s * p for p in a)
def dot(a, b): return sum(p * q for p, q in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


class Trsf:
    """Exact affine map x -> A x + t from a gp_Trsf (its stored doubles: scale * matrix, translation)."""
    def __init__(self, gt=None):
        if gt is None:
            self.A = [[Fr(int(i == j)) for j in range(3)] for i in range(3)]; self.t = (Fr(0),) * 3; return
        s = Fr(gt.ScaleFactor())
        M = gt.HVectorialPart()
        self.A = [[s * Fr(M.Value(i + 1, j + 1)) for j in range(3)] for i in range(3)]
        tr = gt.TranslationPart(); self.t = F3(tr.X(), tr.Y(), tr.Z())
    def pt(self, x): return add(self.lin(x), self.t)
    def lin(self, x): return tuple(sum(self.A[i][j] * x[j] for j in range(3)) for i in range(3))
    def is_identity(self):
        return all(self.A[i][j] == (1 if i == j else 0) for i in range(3) for j in range(3)) and all(c == 0 for c in self.t)


def basis_curve(c, kind):
    while isinstance(c, Geom_TrimmedCurve) or isinstance(c, Geom2d_TrimmedCurve):
        c = c.BasisCurve()
    return c


class ShapeMap:
    """Indexed set of sub-shapes, identity by IsSame (orientation ignored), 1-based like OCC's maps."""
    def __init__(self, shape, kind):
        self.items = []
        ex = TopExp_Explorer(shape, kind)
        while ex.More():
            if self.FindIndex(ex.Current()) == 0:
                self.items.append(ex.Current())
            ex.Next()
    def FindIndex(self, s):
        for i, x in enumerate(self.items):
            if x.IsSame(s):
                return i + 1
        return 0
    def FindKey(self, i): return self.items[i - 1]
    def Extent(self): return len(self.items)


def extract(shape):
    fmap, emap, vmap = ShapeMap(shape, TopAbs_FACE), ShapeMap(shape, TopAbs_EDGE), ShapeMap(shape, TopAbs_VERTEX)
    nf, ne, nv = fmap.Extent(), emap.Extent(), vmap.Extent()
    D = dict(faces=[], edges=[], verts=[], notes=[])
    for i in range(1, nv + 1):
        v = TopoDS.Vertex(vmap.FindKey(i))
        p = BRep_Tool.Pnt_s(v)
        D["verts"].append(dict(p=F3(p.X(), p.Y(), p.Z()), tol=Fr(BRep_Tool.Tolerance_s(v)), tol_f=BRep_Tool.Tolerance_s(v)))
    cast_e = TopoDS.Edge
    cast_f = TopoDS.Face
    cast_w = TopoDS.Wire
    cast_v = TopoDS.Vertex
    for i in range(1, ne + 1):
        e = cast_e(emap.FindKey(i))
        loc = TopLoc_Location()
        c = BRep_Tool.Curve_s(e, loc, 0.0, 0.0); a, b = BRep_Tool.Range_s(e)
        bc = basis_curve(c, 3)
        if not isinstance(bc, Geom_Line):
            raise ValueError(f"edge {i-1}: 3D curve is {bc.DynamicType().Name()}, not a line")
        T = Trsf(loc.Transformation())
        ax = bc.Position(); P = ax.Location(); Dd = ax.Direction()
        P0, d0 = F3(P.X(), P.Y(), P.Z()), F3(Dd.X(), Dd.Y(), Dd.Z())
        a_, b_ = Fr(a), Fr(b)
        g0 = T.pt(add(P0, mul(a_, d0))); g1 = T.pt(add(P0, mul(b_, d0)))
        # vertex at the first / last parameter
        vf = vmap.FindIndex(TopExp.FirstVertex_s(e)) - 1; vl = vmap.FindIndex(TopExp.LastVertex_s(e)) - 1
        D["edges"].append(dict(gamma=(g0, g1), param=(a_, b_), v=(vf, vl), tol=Fr(BRep_Tool.Tolerance_s(e)),
                               tol_f=BRep_Tool.Tolerance_s(e), loc_identity=T.is_identity(),
                               same_param=BRep_Tool.SameParameter_s(e), same_range=BRep_Tool.SameRange_s(e),
                               degenerated=BRep_Tool.Degenerated_s(e), faces=[],
                               stored_pcurves=sum(1 for r in e.TShape().Curves() if r.IsCurveOnSurface())))
    for i in range(1, nf + 1):
        f = cast_f(fmap.FindKey(i))
        loc = TopLoc_Location()
        s = BRep_Tool.Surface_s(f, loc)
        if not isinstance(s, Geom_Plane):
            raise ValueError(f"face {i-1}: surface is {s.DynamicType().Name()}, not a plane")
        T = Trsf(loc.Transformation())
        pos = s.Position()
        O, X, Y = pos.Location(), pos.XDirection(), pos.YDirection()
        O_, X_, Y_ = T.pt(F3(O.X(), O.Y(), O.Z())), T.lin(F3(X.X(), X.Y(), X.Z())), T.lin(F3(Y.X(), Y.Y(), Y.Z()))
        S = lambda u, v, O_=O_, X_=X_, Y_=Y_: add(O_, add(mul(u, X_), mul(v, Y_)))
        N = cross(X_, Y_)
        wires = []
        wex = TopExp_Explorer(f, TopAbs_WIRE)
        while wex.More():
            w = cast_w(wex.Current())
            uses = []
            we = BRepTools_WireExplorer(w, f)
            while we.More():
                oe = we.Current()
                ei = emap.FindIndex(oe) - 1
                c2 = BRep_Tool.CurveOnSurface_s(oe, f, 0.0, 0.0); a2, b2 = BRep_Tool.Range_s(oe, f)
                bc2 = basis_curve(c2, 2)
                A2, B2 = Fr(a2), Fr(b2)
                kind = bc2.DynamicType().Name(); poly_uv = None
                if isinstance(bc2, Geom2d_Line):
                    p2 = bc2.Location(); d2 = bc2.Direction()
                    u0, v0, du, dv = Fr(p2.X()), Fr(p2.Y()), Fr(d2.X()), Fr(d2.Y())
                    beta0 = S(u0 + A2 * du, v0 + A2 * dv); beta1 = S(u0 + B2 * du, v0 + B2 * dv)
                elif isinstance(bc2, Geom2d_BSplineCurve):
                    # the image is contained in the convex hull of the poles; for the review we record the
                    # poles exactly and the curve's end points (evaluated by OCC: not exact)
                    poles = [bc2.Pole(k) for k in range(1, bc2.NbPoles() + 1)]
                    poly_uv = [(Fr(q.X()), Fr(q.Y())) for q in poles]
                    kn = [bc2.Knot(k) for k in range(1, bc2.NbKnots() + 1)]
                    D["notes"].append(f"face {i-1} edge {ei}: BSpline pcurve degree {bc2.Degree()} poles {bc2.NbPoles()} "
                                      f"rational {bc2.IsRational()} knots [{kn[0]}, {kn[-1]}] range [{a2}, {b2}]")
                    dg = bc2.Degree()
                    assert not bc2.IsRational(), "rational BSpline pcurve"
                    assert bc2.Multiplicity(1) == dg + 1 and bc2.Multiplicity(bc2.NbKnots()) == dg + 1, "not clamped"
                    assert kn[0] == a2 and kn[-1] == b2, "pcurve range differs from the knot range"
                    # clamped, full range: the curve starts at the first pole and ends at the last (exactly)
                    beta0 = S(*poly_uv[0]); beta1 = S(*poly_uv[-1])
                else:
                    raise ValueError(f"face {i-1} edge {ei}: pcurve is {kind}")
                rev = oe.Orientation() == TopAbs_REVERSED
                uses.append(dict(edge=ei, rev=rev, beta=(beta0, beta1), pparam=(A2, B2), kind=kind,
                                 poles=None if poly_uv is None else [S(u, v) for u, v in poly_uv]))
                D["edges"][ei]["faces"].append(i - 1)
                we.Next()
            wires.append(uses)
            wex.Next()
        D["faces"].append(dict(O=O_, X=X_, Y=Y_, N=N, tol=Fr(BRep_Tool.Tolerance_s(f)), tol_f=BRep_Tool.Tolerance_s(f),
                               loc_identity=T.is_identity(), wires=wires, reversed=f.Orientation() == TopAbs_REVERSED))
    return D


def on_plane(face, x):
    return dot(sub(x, face["O"]), face["N"]) == 0


def summarize(D):
    import math
    out = []
    out.append(f"F={len(D['faces'])} E={len(D['edges'])} V={len(D['verts'])}")
    for k, f in enumerate(D["faces"]):
        out.append(f" f{k}: tol {f['tol_f']:.3g} wires {len(f['wires'])} uses {[u['edge'] for u in f['wires'][0]]} loc_id {f['loc_identity']}")
    for k, e in enumerate(D["edges"]):
        out.append(f" e{k}: v{e['v']} faces {e['faces']} tol {e['tol_f']:.4g} SP {e['same_param']} SR {e['same_range']} pc {e['stored_pcurves']} loc_id {e['loc_identity']}")
    for k, v in enumerate(D["verts"]):
        out.append(f" v{k}: tol {v['tol_f']:.4g} p {[float(c) for c in v['p']]}")
    out += [" note: " + n for n in D["notes"]]
    return "\n".join(out)


if __name__ == "__main__":
    import lemma0_check_run as R
    for n in sys.argv[1:]:
        D = extract(R.PARTS[n]())
        print("==", n); print(summarize(D))
