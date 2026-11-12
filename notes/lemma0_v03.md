# Lemma 0 (existence) v0.3, and an obstruction lemma (draft, 2026-11-12)

**Status.** Draft, not yet reviewed. It extends [lemma0_v02.md](lemma0_v02.md) after the hypothesis checks in
[lemma0_check_report.md](lemma0_check_report.md). Three changes:
1. Route A (the fan/cone construction of v0.2) with a variable tube radius (A') and with E3 replaced by the
   condition it is used for (E3').
2. Proposition B: re-intersection, for planar models whose vertices have three faces.
3. Lemma O: a sufficient condition for a tolerant B-rep to have **no** realization.

Notation is that of v0.2: zones Z(v) = B(p_v, tau_v), Z(e) = N_{tau_e}(gamma_e) ∪ Z(endpoints),
Z(f) = N_{tau_f}(P_f) ∪ ⋃_{e<f} Z(e), all open. A realization is a PL embedding h: |K| → R³ with
h(int σ) ⊆ Z(σ); then h(σ̄) ⊆ Z(σ) for every cell (augmented zones, see uniqueness_v01.md §1).

## 1. Route A: changes to v0.2

**A' (variable radius).** In v0.2 replace the constant ρ_e by a C¹ function ρ_e(t) > 0. In E1, E2, E3, V1(a)
and S1, read ρ_e as ρ_e(t) at the parameter in question:
- E1: dev*_e(t) < ρ_e(t) < min(τ_e, reach(γ_e|[a_e, b_e])), where dev*_e(t) is the in-normal-plane deviation at t;
- E2.1: ρ_e(t) k_f < 1; E2.3: dist(γ_e(t), P_f ∖ C_f) > ρ_e(t);
- V1(a): the end disks D_e(a_e) have radius ρ_e(a_e).

*Why the proof of v0.2 still applies.*
- The disks D_e(t) lie in the normal planes Π(t), and normal disks of radius below the reach are pairwise
  disjoint whatever their radii. So T_e = ⋃ D_e(t) is still a union of disjoint disks, and every argument in
  §4 of v0.2 is made inside one normal plane at a time.
- k_{f,e}(t) is continuous in t because ρ_e is continuous and the crossing in E2 is transversal.
- The PL step (§5 of v0.2) needs the pieces to be C¹ on closed triangles. The fans and tube walls are C¹ when γ_e
  is C² and ρ_e is C¹. No bound on |ρ_e'| is needed.

**E3' (what E3 is used for).** Replace E3 by: *for every t in [t_v, t_w], the exit points k_{f,e}(t) and k_{g,e}(t)
are distinct.*
- §4 of v0.2 uses E3 only to say that the two radii in D_e(t) meet only at the centre. §5 uses it for a positive
  crease angle along γ_e; distinctness, continuity and compactness give a positive lower bound.
- E3 of v0.2 is a sufficient condition for E3' that holds for every position of the boundary points within dev*
  of γ_e. E3' can be checked on the actual data. The checker computes the exit points of the tangent lines of the
  sections, with an angular error bound from η = 2 k_f ρ² (a section of curvature ≤ k_f stays within k_f s²/2 of
  its tangent line over length s ≤ 2ρ). That computation is a sampled check, not a proof.

## 2. Proposition B (re-intersection, planar, degree three)

**Setting.** Every face f has planar data: S_f is a plane Π_f, and P_f is a polygon in Π_f. Every vertex v lies
on exactly three faces, and the three planes are linearly independent. Let c_v be their common point. For an
edge e from v to w, let ℓ_e = [c_v, c_w]; it lies in both face planes of e. For a face f with vertices
v_1, …, v_k in the cyclic order of ∂f, let P̃_f be the polygon c_{v_1} … c_{v_k} in Π_f.

**Proposition B.** Assume
- B1 c_v ∈ Z(v) for every v;
- B2 ℓ_e ⊆ Z(e) for every e;
- B3 P̃_f ⊆ Z(f) for every f;
- B4 each P̃_f is a simple polygon, and two of the polygons P̃_f, P̃_g meet exactly in their common edges and vertices
  (in the c's), and in nothing else.

Then the cellular map h: |K| → ⋃ P̃_f that sends v to c_v, ē onto ℓ_e linearly and each face onto P̃_f (by a PL
homeomorphism extending the boundary map) is a realization.

*Proof.* h is a PL homeomorphism onto ⋃P̃_f, since the polygons are disks (B4), glued along the edges exactly as in
K (B4). Zones: h(v) = c_v ∈ Z(v), h(int e) ⊆ ℓ_e ⊆ Z(e), h(int f) ⊆ P̃_f ⊆ Z(f). □

*Remarks.*
- The content is that B1–B4 are checkable. For the sewn box and plate of the report they hold with margins 45%
  (B1), 13% (B2, B3); B4 was checked with OpenCascade on the exact polyhedron, not with exact arithmetic.
- For curved faces, the same idea uses surface–surface intersection curves; it then needs the PL step of v0.2 §5,
  with bi-Lipschitz constants from the transversality of the surfaces. Not written.
- Vertices with four or more faces need a different vertex piece. Models mixing tangent edges (route A) and
  sharp edges (route B) need a vertex construction that combines the two. Open.

## 3. Lemma O (obstruction)

**Setting.** Two faces f ≠ g with planar data: P_f ⊆ Π_f, P_g ⊆ Π_g, with the planes not parallel.
- λ = Π_f ∩ Π_g; α ∈ (0, π/2] is the angle between the planes; n_f, n_g are unit normals;
- m_f is a unit vector in Π_f orthogonal to λ, and m_g likewise;
- π_f is the orthogonal projection onto Π_f;
- U_f = ⋃_{e<f} Z(e), which contains the zones of the vertices of f.

**Lemma O.** Suppose there are X ∈ λ and ρ > 0 such that, for J_f = X + [−ρ, ρ] m_f and J_g = X + [−ρ, ρ] m_g:
- **O0** for every edge e of f, the boundary arc β_{f,e} of P_f lies in Z(e), and every corner of P_f lies in the
  zone of its vertex; the same holds for g;
- **O1** J_f ⊆ P_f, and dist(J_f, ∂P_f) > τ_f; the same holds for g;
- **O2** J_f ∩ cl π_f(U_f) = ∅ and J_g ∩ cl π_g(U_g) = ∅;
- **O3** Z(e) is simply connected for every edge e of f or of g;
- **O4** ρ sin α > τ_f cos α + τ_g and ρ sin α > τ_g cos α + τ_f.

Then the tolerant B-rep has no realization.

*Proof.* Suppose h is a realization. Write φ = π_f ∘ h|_f̄: f̄ → Π_f, where f̄ is the closed 2-cell, a disk.

**Step 1 (h(f) lies over J_f only in the slab).**
- Let y ∈ J_f. h(f̄) ⊆ Z(f) = N_{τ_f}(P_f) ∪ U_f.
- By O2, no point of U_f projects to y. So every point of h(f̄) over y lies in N_{τ_f}(P_f).
- P_f lies in the plane Π_f, so π_f^{-1}(y) ∩ N_{τ_f}(P_f) ⊆ σ_y := y + (−τ_f, τ_f) n_f.
- Hence h(f̄) ∩ π_f^{-1}(y) = h(f̄) ∩ σ_y. Also h(∂f) ⊆ U_f, so these points are images of interior points of f.

**Step 2 (degree one).**
- ∂f is a circle made of edges e < f and vertices. By O0, ∂P_f is a loop that runs through the same sequence of
  edge zones and vertex zones.
- Build a homotopy H: ∂f × [0, 1] → U_f from h|_{∂f} to a parametrization of ∂P_f:
  - at a vertex v, use the straight segment from h(v) to the corner of P_f at v (both lie in the ball Z(v));
  - on an edge e, the boundary of the square ē × [0, 1] is already mapped into Z(e): h(ē) ⊆ Z(e), β_{f,e} ⊆ Z(e) (O0),
    and the vertex segments lie in Z(v) ⊆ Z(e). By O3 this loop is null-homotopic in Z(e), so H extends over the
    square inside Z(e).
- By O2, π_f ∘ H avoids every y ∈ J_f. So φ|_{∂f} and the boundary of the polygon P_f have the same winding number
  around y.
- P_f is a polygon bounded by a Jordan curve and y ∈ int P_f (O1), so that winding number is ±1.
- Hence the mod-2 degree of φ at y is 1. For y that is not the image of the 1-skeleton of a triangulation on which h
  is linear, #φ^{-1}(y) is odd. By Step 1, #(h(f̄) ∩ σ_y) is then odd.

**Step 3 (a crossing arc in the slice).**
- Let Σ be the plane through X orthogonal to λ; it contains n_f, m_f, n_g and m_g. Choose the position of Σ along λ
  generic. The steps below hold for every position near X, since O1, O2 and O4 are open conditions, so we may move
  X slightly along λ.
- R_f = J_f + [−τ_f, τ_f] n_f is a rectangle in Σ. Its long sides are y ± τ_f n_f, and its short sides are
  X ± ρ m_f + [−τ_f, τ_f] n_f.
- M_f := h(f̄) ∩ R_f. Since h is PL and Σ is generic, M_f is a compact 1-manifold.
  - By Step 1 it does not meet the long sides: h(f̄) over J_f lies in the open slab.
  - Its boundary lies on the short sides.
- Take a generic fibre σ_y (y ∈ J_f), which crosses R_f from long side to long side. By Step 2, M_f meets it an odd
  number of times.
  - A circle component of M_f meets σ_y an even number of times: the endpoints of σ_y are on ∂R_f, outside the circle.
  - An arc component with both ends on the same short side also meets σ_y an even number of times: close it up with
    a piece of that short side, which σ_y does not meet.
  - So some arc a_f ⊆ M_f joins the two short sides of R_f.
- Likewise, there is an arc a_g ⊆ h(ḡ) ∩ R_g joining the two short sides of R_g.

**Step 4 (the arcs meet).**
- In Σ, use the coordinates u = ⟨x − X, n_f⟩ and w = ⟨x − X, n_g⟩. They are independent because the planes are not
  parallel.
- The strip of R_f is |u| < τ_f, the strip of R_g is |w| < τ_g, and their intersection is the parallelogram
  Q = {|u| ≤ τ_f, |w| ≤ τ_g}.
- The short sides of R_f lie at m_f = ±ρ. There ⟨±ρ m_f + s n_f, n_g⟩ = ±ρ⟨m_f, n_g⟩ + s⟨n_f, n_g⟩ with
  |⟨m_f, n_g⟩| = sin α and |⟨n_f, n_g⟩| = cos α. By O4, w > τ_g on one short side and w < −τ_g on the other.
  So the ends of a_f lie on opposite sides of the strip |w| ≤ τ_g.
- a_f stays in |u| < τ_f. Take the last point of a_f with w = −τ_g before its first point with w = +τ_g (or the
  reverse). The sub-arc between them lies in Q and joins the side w = −τ_g to the side w = +τ_g.
  - Q's sides u = ±τ_f lie on the long sides of R_f, which a_f does not meet.
- Symmetrically, a sub-arc of a_g lies in Q and joins u = −τ_f to u = +τ_f.
- Q is a parallelogram, homeomorphic to a square by (u, w) ↦ (u/τ_f, w/τ_g). Two paths in a square that join
  the two pairs of opposite sides intersect.
- So h(f̄) and h(ḡ) have a common point x. By Step 1, x = h(p) with p ∈ int f, and x = h(q) with q ∈ int g. Hence
  p ≠ q, so h is not injective. □

**Remarks.**
1. *Why O4 is mild.* Face tolerances are tiny (OpenCascade's default τ_f is 1e-7), so O4 needs only ρ larger
   than about 2τ/sin α. The binding conditions are O1 and O2: the crossing of the two patches must lie away from
   the shadows of the edge and vertex zones of f and g.
2. *Checking it.* [../compute/obstruction_check.py](../compute/obstruction_check.py) checks O0–O4 for planar
   models with straight edges. Z(e) is then a capsule plus two balls, which is contractible when each ball meets
   the capsule. The projection of a capsule of radius r onto a plane is a planar capsule of radius r, so O2 is a
   distance test. Results (double precision; not exact arithmetic):
   - sewn wedge 30°: holds with ρ = 1.6e-3 against the 3.7e-7 that O4 needs; O0 margins 4.8% and 30%;
   - sewn wedge 10°: holds with ρ = 0.016;
   - sewn box, sewn plate, exact box and exact wedge: no witness. This is consistent: the first two are realized by
     Proposition B, and the last two by route A.
   Both sewn wedges pass BRepCheck_Analyzer and BRepAlgoAPI_Check.
3. *Curved patches.* The proof uses planarity in Step 1 (the fibre of π_f is a segment of the slab) and in Step 2
   (the boundary of P_f is a Jordan curve in the plane). A tubular-neighbourhood version should work for C² patches
   with τ_f below their reach; not written.
4. *Relation to exp6a.* exp6a builds a model with two linked triangles, which passes BRepCheck but has no
   realization; that is a constructed example of a known phenomenon. The sewn wedges are produced by one ordinary
   sewing operation, and they also pass BRepAlgoAPI_Check.

## 4. Standard facts used, not separately checked against sources

- Mod-2 degree of a PL map f̄ → R² at a value off the image of the boundary: it equals the winding number of the
  boundary loop mod 2, and it equals the parity of the number of preimages of a regular value.
- General position: a generic plane meets a PL surface in a compact 1-manifold, and a generic segment meets a
  PL 1-manifold transversally in finitely many points.
- Two paths in a square that join the two pairs of opposite sides intersect. It is a consequence of the Jordan
  curve theorem, and also follows from the Poincaré–Miranda theorem. Maehara (Amer. Math. Monthly 91 (1984)) uses
  it in a proof of the Jordan curve theorem; the original has not been checked.
- A union of a convex open set and open balls that each meet it in a convex set, with the balls pairwise disjoint,
  is contractible.
