# Lemma 0 (existence) v0.3, and an obstruction lemma (draft, 2026-11-12)

**Status.** Draft v0.3.2. Three independent reviews, none of which found a fatal error:
a mathematical review ([reviews/lemma0_v03_review.md](reviews/lemma0_v03_review.md)), a code review with exact
re-verification ([reviews/lemma0_v03_code_review.md](reviews/lemma0_v03_code_review.md)), and a second-round review
of the revised text ([reviews/lemma0_v031_review.md](reviews/lemma0_v031_review.md)), which found Lemma O's proof
correct and one gap in its statement (single-wire faces), now fixed. Still open from the reviews: the curvature κ_λ
quoted in the apex estimate of v0.2 §5 (λ_v is only C¹), and the checker issues listed at the end of §1. It extends [lemma0_v02.md](lemma0_v02.md) after the hypothesis checks in
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
- ρ_e is **constant on the stubs** [t_v, a_e] and [b_e, t_w] and on a neighbourhood of a_e and b_e (see below);
- E1: dev*_e(t) < ρ_e(t) < min(τ_e, reach(γ_e|[a_e, b_e])), where dev*_e(t) is the in-normal-plane deviation at t;
- E2.1: ρ_e(t) k_f < 1; E2.3: dist(γ_e(t), P_f ∖ C_f) > ρ_e(t);
- V1(a): the end disks D_e(a_e) have radius ρ_e(a_e).

*Why the proof of v0.2 still applies.*
- The disks D_e(t) lie in the normal planes Π(t), and normal disks of radius below the reach are pairwise
  disjoint whatever their radii. So T_e = ⋃ D_e(t) is still a union of disjoint disks, and every argument in
  §4 of v0.2 is made inside one normal plane at a time.
- k_{f,e}(t) is C¹ in t by the implicit function theorem, because ρ_e is C¹ and the crossing in E2 is transversal.
  k_{f,e}' is transverse to Π(t) whatever ρ_e' is, so the crease arguments along k in v0.2 §5 use only compactness.
- The PL step (§5 of v0.2) needs the pieces to be C¹ on closed triangles. The fans and tube walls are C¹ when γ_e
  is C² and ρ_e is C¹.
- *Why ρ_e is constant near the vertices* (found in review). Two places in v0.2 use ρ_e' = 0 there:
  - the V1(a) sufficient condition: a straight stub with p_v on its axis (t measured from p_v) is star-shaped from
    p_v only if t ρ_e'(t) < ρ_e(t); where t ρ_e'(t) > ρ_e(t), a ray from p_v meets ∂W_v three times;
  - the quarter-space argument at k(a_e) in §5 uses ⟨k', r̂⟩ = ρ_e'(a_e); v0.2 has 0 there (the second review notes
    that ρ_e'(a_e) ≥ 0 would also do).
  Keeping ρ_e constant on the stubs and near a_e, b_e is the simplest way to keep both.
- *Checker status* (second review). compute/lemma0_check.py does not yet implement A' as stated: its variable
  radius is a Lipschitz envelope, not C¹, and it does not re-check E3/E3' with the constant radius on the stubs.
  Its acceptance of the six "E3 var" edges of the model "L all fillets 0.5" is therefore provisional.

**E3' (what E3 is used for).** Replace E3 by: *for every t in [t_v, t_w], the exit points k_{f,e}(t) and k_{g,e}(t)
are distinct.*
- §4 of v0.2 uses E3 only to say that the two radii in D_e(t) meet only at the centre. §5 uses it for a positive
  crease angle along γ_e; distinctness, continuity and compactness give a positive lower bound.
- E3 of v0.2 is a sufficient condition for E3' that holds for every position of the boundary points within dev*
  of γ_e. E3' can be checked on the actual data. The checker computes the exit points of the tangent lines of the
  sections, with an angular error bound from η = k_f ℓ_f²/2: a section of curvature ≤ k_f stays within k_f s²/2 of
  its tangent line over arc length s, and the arc inside the disk has length at most ℓ_f of v0.2 E2.3 (up to about
  2.41ρ, more than the chord bound 2ρ used in the first version). That computation is a sampled check, not a proof.

## 2. Proposition B (re-intersection, planar, degree three)

**Setting.** Every face f has planar data: S_f is a plane Π_f, and P_f ⊆ Π_f. Every vertex v lies
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
- The content is that B1–B4 are checkable. For the sewn box and the sewn plate they hold with margins 45% (B1) and
  13% (B2). The code review re-checked B1–B4 on both in exact rational arithmetic, including B3 (by covering each new face with
  convex pieces, each inside one zone) and B4 (all faces strictly convex, all 15 face pairs meet exactly in the
  expected edge or not at all) ([../compute/checks/review_routeB_exact.py](../compute/checks/review_routeB_exact.py)).
  The sampled B3 margin printed by reintersect_check.py is not meaningful (its grid is coarser than the strips it
  should resolve) and is not quoted.
- The proposition needs the three planes at each vertex to be independent; it does not apply when two faces at a
  vertex are coplanar.
- Curved faces: Proposition B' below.
- Vertices with four or more faces need a different vertex piece. Models mixing tangent edges (route A) and
  sharp edges (route B) need a vertex construction that combines the two. Open.

## 2'. Proposition B' (re-intersection, curved, transversal)

**Setting.** Every face f lies on a C² surface S_f. A *re-trimmed model* consists of compact patches P̃_f ⊆ S_f,
curves γ̃_e and points c_v such that ⋃ P̃_f is the boundary of a compact solid, and the cells (patches, curves,
points) form a regular cell complex isomorphic to K by an isomorphism sending f, e, v to P̃_f, γ̃_e, c_v
(condition **C**). For an edge e between two different faces f, g, the curve γ̃_e lies on S_f ∩ S_g. For a seam
edge (f on both sides) it is a curve on S_f.

**Proposition B'.** Assume C and
- B1–B3 as in Proposition B, for the closed cells: c_v ∈ Z(v), γ̃_e ⊆ Z(e), P̃_f ⊆ Z(f);
- B4: distinct cells of the re-trimmed model meet only in their common faces;
- T (transversality): along every non-seam edge, S_f and S_g meet at a positive angle; and at every vertex the
  tangent cone of ⋃ P̃_f is an embedded PL disk (true, for instance, when three faces meet at v with linearly
  independent normals).
Then the tolerant B-rep has a realization.

*Proof (sketch; it reuses v0.2 §5).*
- The isomorphism of C gives a homeomorphism h₀: |K| → ⋃ P̃_f with h₀(σ̄) ⊆ Z(σ) for every cell (B1–B4).
  Since h₀(σ̄) is compact and Z(σ) is open, there is a margin m > 0 with N_m(h₀(σ̄)) ⊆ Z(σ) for all σ.
- h₀ is C¹ on each closed cell (the patches and curves are C²). It is bi-Lipschitz: inside a cell by
  regularity; across an edge by T (a positive crease angle; across a seam there is no crease); at a vertex by the
  tangent-cone condition, as in v0.2 §5 ("points where three or more pieces meet").
- Take a shape-regular triangulation of |K| that refines the cells and has the vertices of K as vertices. The
  secant map S (linear on each triangle, equal to h₀ at the triangulation's vertices) satisfies Lip(S − h₀) → 0
  and |S − h₀| → 0 as the mesh size → 0. So S is injective once Lip(S − h₀) is below the bi-Lipschitz constant,
  and S(σ̄) ⊆ Z(σ) once |S − h₀| < m. S is PL. □

*Computation.* [../compute/reintersect_curved.py](../compute/reintersect_curved.py):
1. extends each face's surface;
2. rebuilds the solid with OpenCascade's BOPAlgo_MakerVolume;
3. checks C by matching faces to surfaces, edges to face pairs, and vertices to nearest vertices;
4. checks B1 and B2 on samples;
5. checks B3 by walking inward from 80 samples per boundary curve until the original patch is reached;
6. checks B4 with OpenCascade's validity checks, and T by the angle between the faces along each edge.

This is a sampled, double-precision check; the PL step is not carried out.

| Model | C | margins: vertex / edge / face strip | min crease angle | result |
| --- | --- | --- | --- | --- |
| sewn cylinder g = 0.01 | yes | 55% / 35% / 11% | 90° | pass |
| sewn cylinder g = 0.05 | yes | 55% / 11% / 10% | 90° | pass |
| sewn pipe (cylinder minus cylinder) g = 0.01 | yes | 53% / 16% / 3.6% | 90° | pass |
| sewn box g = 0.01 | yes | 45% / 13% / 4.9% | 90° | pass (agrees with the planar check) |
| sewn wedge 30° g = 0.01 | yes | 32% / −49% / 10% | 30° | fail B2 (consistent with Lemma O) |
| exact cylinder, exact box | yes | 100% | 90° | pass |
| sewn filleted box g = 0.001 | **no** (3 faces instead of 26) | – | – | not applicable |

On the sewn filleted box, the fillet surfaces are tangent to their neighbours, so the extended surfaces do not
re-intersect along the old edges and the rebuilt solid is a different shape. Route A also fails there: 47 edges
fail V1(a), because the deviation is constant along each edge, so the tube radius cannot shrink near the
vertices. So neither construction covers sewn models with tangent (G1) edges at present.

**Plan (not done): route G (graph construction) for tangent edges and smooth vertices.** Near a point where all
the faces involved are G1-continuous, they are graphs over one common plane. A realization can then be built as a
single graph over that plane: on each face region it follows that face's height; near a projected edge it
interpolates between the two heights inside the edge tube; near a vertex it uses the ball. Being a graph, it is
embedded locally automatically. On sewn data the two boundary curves at a tangent edge are offset from γ_e mostly
along the common normal, so the interpolation stays inside the tube when dev_e < τ_e. Hypotheses and proof to be
written.

## 3. Lemma O (obstruction)

**Setting.** Two faces f ≠ g whose closed cells f̄, ḡ are disks, each bounded by a single wire (a face with inner
wires is not covered; the same degree argument should give a version where the sum of the winding numbers of
the wires is odd, not written). Planar data: P_f ⊆ Π_f, P_g ⊆ Π_g, with the planes not parallel. (P_f need not
be a polygon: sewing stores many boundary curves as B-splines, and consecutive boundary curves miss each other by
about 1e-15. Only the loop ℓ_f of O0 is used.)
- λ = Π_f ∩ Π_g; α ∈ (0, π/2] is the angle between the planes; n_f, n_g are unit normals;
- m_f is a unit vector in Π_f orthogonal to λ, and m_g likewise;
- π_f is the orthogonal projection onto Π_f;
- U_f = ⋃_{e<f} Z(e), which contains the zones of the vertices of f.

**Lemma O.** Suppose there are X ∈ λ and ρ > 0 such that, for J_f = X + [−ρ, ρ] m_f and J_g = X + [−ρ, ρ] m_g:
- **O0** (boundary loop) β_{f,e} ⊆ Z(e) for every edge e of f, and at every vertex v of f the end points of the
  two arcs of f at v lie in Z(v). (β_{f,e} is parametrized along e, so for e from v to w its end "at v" is β_{f,e}(0);
  for a closed edge both ends are at its vertex.) Let ℓ_f be the closed loop formed by the arcs β_{f,e} in the cyclic order of ∂f,
  where consecutive arcs at v are joined by the straight segment s_{f,v} between their end points; s_{f,v} ⊆ Z(v)
  because the ball is convex. The same holds for g;
- **O1** J_f ∩ ℓ_f = ∅, and the winding number of ℓ_f (in Π_f) about the points of J_f is odd; the same holds for g;
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
- ∂f is a circle made of the edges e < f and the vertices of f, in the order of the wire.
- Parametrize ℓ_f over ∂f: a small closed arc A_v ⊆ ∂f around each vertex v goes to s_{f,v}, and the rest of each
  edge e goes to β_{f,e}. Build a homotopy H: ∂f × [0, 1] → U_f from h|_{∂f} to this parametrization:
  - on A_v, h(A_v) ⊆ Z(e) ∪ Z(e') for the two edges at v, and s_{f,v} ⊆ Z(v). Shrink A_v so that h(A_v) ⊆ Z(v)
    (h is continuous, h(v) ∈ Z(v), and Z(v) is open). Then use the straight-line homotopy inside the ball Z(v);
  - on the rest of an edge e from v to w, the boundary of the square (ē ∖ (A_v ∪ A_w)) × [0, 1] is already mapped
    into Z(e): h(ē) ⊆ Z(e), β_{f,e} ⊆ Z(e) (O0), and the two vertical sides are segments inside Z(v), Z(w) ⊆ Z(e).
    By O3 this loop is null-homotopic in Z(e), so H extends over the
    square inside Z(e).
- By O2, π_f ∘ H avoids every y ∈ J_f. So φ|_{∂f} and ℓ_f have the same winding number around y.
- By O1 that winding number is odd. Hence the mod-2 degree of φ at y is 1. Fix a triangulation of f̄ on which h is
  linear. For y that is not in φ(1-skeleton), #φ^{-1}(y) is odd; by Step 1, #(h(f̄) ∩ σ_y) is then odd. Once Σ is
  generic (Step 3), the line Σ ∩ Π_f ⊇ J_f meets φ(1-skeleton) in finitely many points, so all but finitely many
  y ∈ J_f are of this kind.

**Step 3 (a crossing arc in the slice).**
- Let Σ be the plane through X orthogonal to λ; it contains n_f, m_f, n_g and m_g. Choose the position of Σ along λ
  generic, and shrink ρ slightly to a generic value. O1, O2 and O4 are open conditions in X (along λ) and in ρ, so
  they still hold. One ρ serves f and g: it must avoid the finitely many values for which one of the planes
  ⟨x − X, m_f⟩ = ±ρ, ⟨x − X, m_g⟩ = ±ρ contains a vertex of the triangulations of h(f̄), h(ḡ). Genericity of ρ
  is needed: a triangle of h(f̄) lying in the plane ⟨x − X, m_f⟩ = ρ would otherwise defeat transversality at the
  short sides for every position of Σ. Generic Σ means: Σ contains no vertex of these triangulations and meets
  no edge of them in more than a point (all but finitely many positions along λ).
- R_f = J_f + [−τ_f, τ_f] n_f is a rectangle in Σ. Its long sides are y ± τ_f n_f, and its short sides are
  X ± ρ m_f + [−τ_f, τ_f] n_f.
- M_f := h(f̄) ∩ R_f. Since h is PL and Σ and ρ are generic, M_f is a compact 1-manifold whose boundary is
  M_f ∩ ∂R_f, met transversally.
  - It does not meet h(∂f): π_f(R_f) = J_f, h(∂f) ⊆ U_f, and by O2 no point of U_f lies over J_f.
  - By Step 1 it does not meet the long sides: h(f̄) over J_f lies in the open slab.
  - Hence its boundary lies on the short sides.
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
- Q lies inside both rectangles: on Q, |⟨x − X, m_f⟩| ≤ (τ_g + τ_f cos α)/sin α < ρ by O4, and likewise for m_g.
- Q is a parallelogram, homeomorphic to a square by (u, w) ↦ (u/τ_f, w/τ_g). Two paths in a square that join
  the two pairs of opposite sides intersect.
- So h(f̄) and h(ḡ) have a common point x. By Step 1, x = h(p) with p ∈ int f, and x = h(q) with q ∈ int g. Hence
  p ≠ q, so h is not injective. □

**Remarks.**
1. *Why O4 is mild.* Face tolerances are tiny (OpenCascade's default τ_f is 1e-7), so O4 needs only ρ larger
   than about 2τ/sin α. The binding conditions are O1 and O2: the crossing of the two patches must lie away from
   the shadows of the edge and vertex zones of f and g.
2. *Checking it.* [../compute/obstruction_check.py](../compute/obstruction_check.py) checks O0–O4 for planar
   models with straight edges. Z(e) is then a capsule plus two balls. O3 is tested by the sufficient condition:
   each ball meets the capsule, and the two balls are disjoint or all three sets share a point. (Each ball meeting
   the capsule is not enough: if the balls meet each other but the three sets have no common point, Z(e) has the
   homotopy type of a circle.) The projection of a capsule of radius r onto a plane is a planar capsule of radius r, so O2 is a
   distance test. Results (double precision; not exact arithmetic):
   - sewn wedge 30°: the largest feasible ρ is 1.6e-3; the witness uses ρ = 8.1e-4 against the 3.7e-7 that O4
     needs; O0 margins 4.8% (1 − 1/1.05 up to rounding; 1.05 is the sewing factor) and 30%;
   - sewn wedge 10°: largest feasible ρ = 0.016, witness ρ = 8.0e-3;
   - the code review re-verified both wedges independently in exact rational arithmetic
     ([../compute/checks/review_lemmaO_exact.py](../compute/checks/review_lemmaO_exact.py)). Its witness for the 30°
     wedge lies at a different point X along the same edge, with the same ρ; there the O2 margins are 35% and 15%;
   - sewn box, sewn plate, exact box and exact wedge: no witness. This is consistent: the first two are realized by
     Proposition B, and the last two by route A.
   Both sewn wedges pass BRepCheck_Analyzer and BRepAlgoAPI_Check.
3. *Curved patches.* The proof uses planarity in Step 1 (the fibre of π_f is a segment of the slab) and in Step 2
   (the winding number of ℓ_f is taken in the plane Π_f, onto which π_f projects). A tubular-neighbourhood version should work for C² patches
   with τ_f below their reach; not written.
4. *Relation to exp6a.* exp6a builds a model with two linked triangles, which passes BRepCheck but has no
   realization; that is a constructed example of a known phenomenon. The sewn wedges are produced by one ordinary
   sewing operation, and they also pass BRepAlgoAPI_Check.

## 4. Standard facts used, not separately checked against sources

- Mod-2 degree of a PL map f̄ → R² at a value off the image of the boundary: it equals the winding number of the
  boundary loop mod 2, and it equals the parity of the number of preimages of a regular value.
- General position: a generic plane meets a PL surface in a compact 1-manifold, and a generic segment meets a
  PL 1-manifold transversally in finitely many points.
- Two paths in a square that join the two pairs of opposite sides intersect. Maehara (Amer. Math. Monthly 91
  (1984)) proves it from the Brouwer fixed point theorem and uses it to prove the Jordan curve theorem; the
  original has not been checked.
- A union of an open convex set C and open balls B_1, B_2 with C ∩ B_i ≠ ∅, such that B_1 ∩ B_2 = ∅ or
  C ∩ B_1 ∩ B_2 ≠ ∅, is contractible (nerve lemma for a good cover).
- A segment meeting a PL circle in the plane transversally, with both end points outside the disk the circle
  bounds, meets it an even number of times (Step 3).
- The winding number of a loop about a point is invariant under homotopies of the loop that avoid the point.
- A PL map is linear on the simplices of some triangulation.
- The mod-2 degree is invariant under homotopy of the boundary loop in the complement of the point (used in Step 2
  together with the winding number).
- Normal disks of radius below the reach of a C² curve are pairwise disjoint (Federer 1959).
- The implicit function theorem (C¹ dependence of k_{f,e} on t).
