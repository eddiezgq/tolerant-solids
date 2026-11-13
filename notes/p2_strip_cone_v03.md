# P2: existence by strips and cones — v0.3 (2026-11-13)

Status: **draft proof, revised after review `reviews/p2_v02_review.md` (M1–M3, m1–m8); not yet re-reviewed.** The
checker issues (M4) are handled separately in `compute/strip_cone_check3.py` (in progress).

Notation as in P1 (`paper/p1.tex`, Section 2). P1 appendices: A = curved-triangle lemma (Lemma A.1), B = proof of
Thm 5.1 (fans; contains the Federer normal-disk argument and the PL step), C = proof of Prop. 5.3 (re-intersection;
same PL step). K is regular. For a vertex v fix r_v ∈ (0, τ_v), put B_v = B(p_v, r_v) (closed), S_v = ∂B_v,
U = ℝ³ \ ⋃_v int B_v.

## 1. Data

**Strip edges.** For an edge e with faces f, g and vertices v, w, let γ_e be parametrized by arc length on [0, L_e],
let Π(t) be its normal plane, and let reach_e be the reach of γ_e(I_e) for an interval I_e = [a_e, b_e] ⊂ (0, L_e).
Fix ρ_e < min(τ_e, reach_e) and write D(t) = Π(t) ∩ B(γ_e(t), ρ_e) (closed disk).

- **(E1′)** For each t ∈ I_e, the curve β_{f,e} meets D(t) in exactly one point, b*_f(t), and crosses Π(t)
  transversally there. As t runs through I_e, b*_f(t) runs through a single sub-arc of β_{f,e}. The same holds for g.

  (E1′) replaces P1's E2.2 and E1: no tube has to contain the patch sections; only the edge's own boundary curves have
  to stay in a thin normal tube.
- The **chord** is χ_e(t) = [b*_f(t), b*_g(t)] ⊂ D(t), and the **strip** is σ_e = ⋃_{t∈I_e} χ_e(t). The two curves
  J_f = b*_f(I_e) and J_g = b*_g(I_e) are the **junction curves**.

**Re-trimmed edges** (renamed from c_e to q_e to avoid a clash with chords). Here P_f and P_g cross, and the edge is
realized by an arc of their intersection.

- **(R′)**
  - (a) q_e is a C² arc of P_f ∩ P_g along which the two patches are transversal. Its end points lie in the interior of
    U's complement, i.e. in int B_v and int B_w. q_e meets S_v and S_w transversally, each exactly once. q_e ⊂ Z(e).
  - (b) Let P_f^U = P_f ∩ U. Then P_f^U \ q_e has exactly two components. The **kept** one contains the boundary arcs
    of P_f^U that belong to edges other than e. The **discarded** one contains the part of β_{f,e} in U and no other
    boundary of P_f^U. The same holds for g.
  - (c) P̃_f is the closure of the kept component, so its edge-e side is q_e ∩ U. P̃_f is P_f^U cut in this way along
    all re-trimmed edges of f; for strip edges it is unchanged.

## 2. Hypotheses

- **(P0′)** Each P_f is a C² embedded closed disk. Its boundary is the cyclic union of the C² arcs β_{f,e}, meeting at
  the corners.
- **(E1′)** as above, for every strip edge.
- **(E4)** For every strip edge and t ∈ I_e:
  - (a) χ_e(t) meets P̃_f ∪ P̃_g only at its two end points, and b*_f(t) ≠ b*_g(t);
  - (b) the direction of χ_e(t) at b*_f(t) does not lie in the closed inward tangent half-plane of P_f at b*_f(t)
    (P_f's tangent plane, on the inner side of its boundary), and likewise at b*_g(t).
- **(R′)** as above, for every re-trimmed edge.
- **(V0′)** For every vertex v:
  - the corners of the patches at v, the ends γ_e(0 or L_e) at v, the end chord χ_e(a_e) or χ_e(b_e) at v, and the
    ends of the re-trimmed arcs at v lie in int B_v;
  - the balls are pairwise disjoint;
  - B_v meets no patch, strip or re-trimmed arc that is not incident to v.
- **(V1′)** For every vertex v:
  - (a) every piece of Σ_U (each P̃_f and σ_e) is transversal to S_v, and so is each of its boundary curves that
    reaches S_v: junction curves, β-arcs, re-trimmed arcs;
  - (b) λ_v := Σ_U ∩ S_v, where Σ_U = (⋃_f P̃_f ∪ ⋃_e σ_e) ∩ U, is one simple closed curve. It consists of exactly
    one arc of each incident face and one chord-arc (σ_e ∩ S_v) of each incident strip edge, in the cyclic order of the
    link of v. Consecutive face arcs meet at a re-trimmed edge.
- **(S1′)** In U the following are pairwise disjoint:
  - P̃_f and P̃_g for f ≠ g, except along a common re-trimmed arc;
  - σ_e and σ_{e′} for e ≠ e′;
  - σ_e and P̃_h for h not incident to e.

## 3. Theorem (draft)

Under (P0′), (E1′), (E4), (R′), (V0′), (V1′) and (S1′), the tolerant B-rep has a realization.

## 4. Proof

### Step 1. Zones
- χ_e(t) ⊂ D(t) ⊂ B(γ_e(t), τ_e), which is convex, so χ_e(t) ⊂ Z(e).
- P̃_f ⊂ Z(f), and q_e ⊂ Z(e) by (R′a).
- The cone C_v ⊂ B_v ⊂ Z(v).
- By augmentation Z(v) ⊂ Z(e) ⊂ Z(f) for v < e < f.

The cells in Step 4 consist of these pieces. Each closed cell is compact and lies in its open zone, so there is a
margin m > 0. The reviewer confirmed this step for v0.2.

### Step 2. The strip is an embedded C¹ band
- **Injective.**
  - Chords at different t lie in the disks D(t) of radius ρ_e < reach_e.
  - These disks are pairwise disjoint by Federer 4.8(12), with the half-space normal cone at the end points (P1,
    Appendix B, "Injectivity").
  - Each chord is a nondegenerate segment (E4a).
  - So X(t, λ) = (1−λ) b*_f(t) + λ b*_g(t) is injective on I_e × [0,1].
- **C¹.** b*_f is C¹ by the implicit function theorem. The ingredients are: β_{f,e} is C²; Π(t) depends C¹ on t (γ_e
  is C²); the crossing is transversal (E1′); and uniqueness in D(t) gives a global continuous, hence C¹, selection.
- **Rank 2 (m1).** Differentiate ⟨b*_f(t) − γ_e(t), γ_e′(t)⟩ = 0:
  ⟨b*_f′, γ_e′⟩ = 1 − ⟨b*_f − γ_e, γ_e″⟩ ≥ 1 − κ ρ_e > 0, since ρ_e < reach_e ≤ 1/κ.
  So ⟨∂_t X, γ_e′⟩ > 0, while ∂_λ X = b*_g − b*_f ≠ 0 lies in Π(t) ⟂ γ_e′. In particular b*_f′ ∉ Π(t).

### Step 3. Σ_U is a compact surface with boundary ⋃_v λ_v
- **Interior points.**
  - In a patch: the patch is embedded (P0′).
  - In a strip: Step 2.
  - At a junction point of J_f: P̃_f and σ_e are C¹ half-disks with common edge J_f. They meet only along J_f, by (E4a)
    and Step 2. Their union is a disk.
  - On a re-trimmed arc: P̃_f and P̃_g are transversal C² half-disks with common edge q_e (R′).
  - Non-adjacent pieces are disjoint (S1′).
- **Points of S_v (m2).** Each piece, together with each of its boundary curves, is transversal to S_v (V1′a). So
  piece ∩ U is locally a C¹ manifold with corners: a half-disk at an interior point of S_v ∩ piece, and a quarter-disk
  where a boundary curve meets S_v. Two quarter-disks glued along their common edge (a junction curve, or q_e) form a
  half-disk with boundary on S_v.
- **No free boundary.** The only boundary of Σ_U is ⋃ λ_v. Every other boundary arc of a piece is glued:
  - J_f is glued to the strip;
  - q_e is glued to the other face;
  - the parts of β_{f,e} not in J_f lie inside the balls (Step 4, (iv));
  - the end chords lie inside the balls (V0′).

### Step 4. Cell structure (m3, m4)
- **(i) Faces.**
  - P̃_f is a closed disk: P_f^U cut along re-trimmed arcs (R′b,c).
  - A_v(f) := P̃_f ∩ S_v is one arc (V1′b). Its end points are where the two boundary curves of P̃_f at v (a junction
    curve or a re-trimmed arc) cross S_v. This is forced: λ_v is a closed curve made of face arcs and chord-arcs, so
    each end of a face arc must also be an end of a chord-arc or of the next face arc.
  - So A_v(f) is a properly embedded arc in a disk and splits it into two disks. The side containing the corner at v
    lies in int B_v. The other side contains f's other corners; it lies in U because it misses S_v and contains points
    of the disjoint balls B_w, w ≠ v (V0′; regular K gives f ≥ 2 vertices).
  - Doing this at every vertex of f gives a closed disk Q_f. Its boundary alternates between edge sides (junction
    curves or re-trimmed arcs) and sphere arcs A_v(f).
- **(ii) Strip edges.** σ_e ≅ I_e × [0,1] (Step 2). The end chords lie in int B_v, int B_w (V0′). σ_e ∩ S_v is one arc
  (V1′b). Its ends lie on the two *different* junction curves, by the cyclic order in (V1′b): the chord-arc sits
  between the arcs of f and of g. So R_e := σ_e ∩ U is a closed disk with two sides J_f, J_g and two ends on S_v, S_w.
- **(iii) Re-trimmed edges.** q_e ∩ U is one arc (R′a).
- **(iv) Consequence.** The parts of β_{f,e} outside the junction curve J_f lie in the discarded corner disks, hence in
  the balls.
- **(v) Gluing.** Glue Q_f to R_e along J_f, and Q_f to Q_g along q_e ∩ U. The result is |K| with a small open star
  removed at each vertex, and the cyclic order at v is that of the link. The cells are:
  - open face f ↦ int Q_f ∪ (the half of R_e next to f, for every strip edge e of f) ∪ (later) its cone sector;
  - open edge e ↦ midline of R_e (or int q_e ∩ U) ∪ (later) two open cone rays;
  - vertex v ↦ p_v.

### Step 5. Cones
- λ_v is a simple closed curve on the round sphere S_v centred at p_v.
- The radial cone C_v = {p_v + s(x − p_v) : x ∈ λ_v, s ∈ [0,1]} is an embedded closed disk, since distinct rays from
  p_v meet only at p_v.
- C_v ⊂ B_v, and C_v ∩ U = λ_v = Σ_U ∩ B_v.
- So Σ = Σ_U ∪ ⋃ C_v is embedded.
- The cone structure extends the cell map of Step 4 over the removed stars: face sector over A_v(f) and halves of the
  adjacent chord-arcs; edge rays to the end of the midline (or of q_e); apex to v.
- h₀: |K| → Σ is a topological embedding with each open cell in its zone, i.e. a topological realization.

### Step 6. From topological to PL (M3)
We use P1's PL step (Appendix B "The PL step", and Appendix C) in the form it actually proves:

> **(PL step, P1.)** Suppose
> - h₀ is bi-Lipschitz on each shell for the intrinsic metric of a triangulation T that subdivides the cells;
> - T is shape-regular on the triangles where h₀ is C¹ up to the boundary;
> - T is radial on cone sectors, where h₀(s, y) = p_v + s(φ(y) − p_v) with φ C¹ on each base segment;
> - different shells are mapped at positive distance.
>
> Then fine secant maps are PL realizations within the margin m.

The secant estimates are: on ordinary triangles Lip(S − h₀) ≤ C ω(Dh₀, mesh)/sin θ_min; on radial triangles
(S − h₀)(s, y) = s·e(y), so D(S − h₀) is constant along rays and → 0 with the mesh.

Its hypotheses hold here.
- **Triangulation (m5).**
  - Strips are triangulated in the (t, λ) chart (C¹, with a uniform modulus of continuity by compactness), patch pieces
    in their C² charts, by P1's curved triangles (Lemma A.1, C¹ version).
  - The boundary curves are C¹ regular in their charts:
    - sphere arcs by the implicit function theorem applied to |X − p_v|² − r_v², whose gradient is nonzero
      (transversality, V1′a);
    - junction curves as λ = 0, 1 in the strip chart and as pcurve images in the patch chart;
    - re-trimmed arcs by transversal intersection (C²).
  - Shared curves get one common parametrization: junction curves by t, sphere arcs by the link parametrization φ of
    λ_v, re-trimmed arcs by one parametrization in ℝ³.
  - Corners of pieces get an extra interior vertex, as in P1.
  - Cone sectors are triangulated radially over the vertices of λ_v.
- **Locally bi-Lipschitz.**
  - Inside pieces: C¹ with injective differential.
  - Along a junction curve: P_f's tangent half-plane H_f and the strip's tangent half-plane H_s are distinct (E4b),
    and they share the boundary line spanned by b*_f′. That line is not in Π(t) (Step 2).
  - Along a re-trimmed arc: transversality (R′a).
  - Along the interior of a face arc or chord-arc of λ_v: the outside piece lies in the outer closed half-space at x
    and is transversal to S_v; the cone is radial, in the inner half-space. Their half-planes are distinct.
  - **At a corner x of λ_v (M3(1),(2)).**
    - Let J be the tangent line of the junction curve (or of q_e) at x. J is transversal to T_xS_v (V1′a).
    - The two outside half-planes H₁ ≠ H₂ contain J, so H₁ ∩ T_xS_v and H₂ ∩ T_xS_v are rays ℓ₁ ≠ ℓ₂ (no cusp of
      λ_v at x).
    - The tangent cone at x is: H₁ ∪ H₂, in the outer half-space, meeting T_xS_v only in ℓ₁ ∪ ℓ₂ and each other only
      along J; together with the cone sub-sectors span⁺(ℓ₁, w), span⁺(w, ℓ₂), where w = p_v − x, in the inner
      half-space.
    - These four sectors meet only along common rays, in cyclic order, so the tangent cone is an embedded disk.
  - **At the apex p_v.**
    - λ_v is a simple closed piecewise-C¹ curve on S_v with no cusps (previous bullet), so its arc-length
      parametrization φ is bi-Lipschitz onto λ_v.
    - Then (s, y) ↦ p_v + s(φ(y) − p_v) is bi-Lipschitz near the apex, by homogeneity: for points at radii s₁, s₂ and
      link parameters y₁, y₂, the distance is comparable to |s₁ − s₂| + min(s₁, s₂)|y₁ − y₂|, the intrinsic distance
      of the cone.
- **Global.** Locally bi-Lipschitz + injective + compact ⇒ bi-Lipschitz on each shell. Shells are disjoint compact
  sets.

So a fine secant map is a PL realization. ∎

## 5. Remaining points
1. **Seams and poles:** not covered by this statement (regular K). They need P1 Prop. 5.3's edge-graph formalism.
2. **(V0′) ball disjointness, (S1′) globally, (P0′), (E1′), (R′):** to be tested by the new checker.
3. **Cusp corners** (face angle 0) violate (V1′b), as observed. Whether such data are realizable at all is open.
4. **Note on "no tube radius" (m7):** (E1′) still asks the boundary curves to stay within ρ_e < reach_e of γ_e, a
   radius condition. It is weaker than P1's E1, because nothing has to separate the tubes of different edges inside the
   vertex ball.
