# P2: existence by strips and cones — v0.2 (2026-11-13)

Status: **draft proof, not yet reviewed.** Supersedes the statement in `p2_strip_cone_v01.md`, which is kept for its
data notes. Notation as in P1 (`paper/p1.tex`, Section 2). K is regular (every closed cell is a ball whose boundary
is a subcomplex); seams and poles are handled in the checker but not in this statement.

## 1. Data and construction

For a vertex v we fix r_v with 0 < r_v < τ_v and write B_v = B(p_v, r_v) (closed), S_v = ∂B_v. For an edge e with
faces f, g and vertices v, w, Π(t) is the normal plane of γ_e at t.

Each edge is of one of two kinds; the kind is part of the data of the construction.

- **Strip edges.** On an interval I_e = [a_e, b_e] ⊂ (0,1), the boundary curve of each adjacent patch crosses Π(t)
  in exactly one point b*_f(t), b*_g(t), and the **chord** c_e(t) = [b*_f(t), b*_g(t)] ⊂ Π(t) is non-degenerate. The
  **strip** is σ_e = ⋃_{t∈I_e} c_e(t).
- **Re-trimmed edges.** The patches P_f and P_g cross transversally along a C² arc c_e (the re-trimmed edge). P̃_f is
  the closure of the component of P_f \ c_e that contains the interior of P_f away from e (the part of P_f beyond c_e
  is discarded), and likewise P̃_g.

For a strip edge, set P̃_f = P_f near e. A face can have edges of both kinds; P̃_f is P_f cut along its re-trimmed
edges.

The **outside surface** is

  Σ_out = ( ⋃_f P̃_f ∪ ⋃_{strip e} σ_e ) \ ⋃_v int B_v.

The **realized surface** is Σ = Σ_out ∪ ⋃_v C_v, where C_v is the cone from p_v over λ_v = Σ_out ∩ S_v.

## 2. Hypotheses

Let reach_e be the reach of the arc γ_e(I_e).

- **(P0′)** Each patch P_f is a C² embedded closed disk; its boundary is the closed curve of the pcurve images
  β_{f,e}, which are C² arcs meeting at the corners.
- **(E1′)** For a strip edge and t ∈ I_e: |b*_f(t) − γ_e(t)| < min(τ_e, reach_e), and likewise for g. The boundary
  curve of P_f crosses Π(t) transversally at b*_f(t).
- **(E4)** For a strip edge and t ∈ I_e:
  - (a) c_e(t) meets P̃_f ∪ P̃_g only at its two end points;
  - (b) no fold: at b*_f(t), the direction of the chord is not in the closed tangent half-plane of P_f along its
    boundary (T_{b*}P_f ∩ {inward}), and likewise at b*_g(t).
- **(R′)** For a re-trimmed edge, between the balls: c_e is a single transversal C² arc of P_f ∩ P_g, lies in Z(e),
  and its ends lie in int B_v and int B_w. (These are P1 Prop. 5.3 clauses R, B2 and T, restricted to this edge.)
- **(V0′)** For every vertex v: the corners of the patches at v, the end points γ_e(0 or 1) of the edges at v, the
  chords c_e(a_e) or c_e(b_e) at the v-end, and the ends of the re-trimmed arcs at v all lie in int B_v. The balls
  B_v are pairwise disjoint, and B_v meets no patch, strip or re-trimmed arc that is not incident to v.
- **(V1′)** For every vertex v:
  - (a) each piece of Σ_out (a patch P̃_f, a strip σ_e) is transversal to S_v, and so is each junction curve between
    two pieces (b*_f(I_e), c_e);
  - (b) λ_v is one simple closed curve. It consists of exactly one arc of each incident face and one chord-arc of each
    incident strip edge, in the cyclic order of the link of v.
- **(S1′)** Outside ⋃ int B_v the following are pairwise disjoint:
  - P̃_f and P̃_g for f ≠ g, except along a common re-trimmed arc;
  - σ_e and σ_{e′} for e ≠ e′;
  - σ_e and P̃_h for h not incident to e.

## 3. Theorem (draft)

Under (P0′), (E1′), (E4), (R′), (V0′), (V1′), (S1′) the tolerant B-rep has a realization.

## 4. Proof

### Step 1. Zones

- c_e(t) has both ends in the disk Π(t) ∩ B(γ_e(t), τ_e) (E1′). That disk is convex, so c_e(t) ⊂ Z(e).
- P̃_f ⊂ P_f ⊂ Z(f).
- A re-trimmed arc c_e lies in Z(e) by (R′).
- C_v ⊂ B_v ⊂ B(p_v, τ_v) = Z(v), since a ball is convex and contains p_v and λ_v.
- By augmentation Z(v) ⊂ Z(e) ⊂ Z(f) for v < e < f.

So once the cell structure of Step 4 is fixed, every open cell lies in its zone: a face's cell is made of patch,
half-strips and cone sectors; an edge's cell of a strip midline or re-trimmed arc and two cone rays; a vertex is p_v.

### Step 2. Each strip is an embedded band

- For s ≠ t in I_e, c_e(s) ⊂ Π(s) ∩ B(γ_e(s), ρ) and c_e(t) ⊂ Π(t) ∩ B(γ_e(t), ρ) with ρ < reach_e (E1′). By
  Federer 4.8(12) (as in P1, Appendix A), the normal disks of radius ρ < reach at different points are disjoint.
- So (t, λ) ↦ (1−λ) b*_f(t) + λ b*_g(t) is injective on I_e × [0,1], hence a homeomorphism onto σ_e.
- b*_f is C¹: implicit function theorem, using the transversal crossing (E1′), C² data and the C¹ dependence of Π(t)
  on t. The map has rank 2: the λ-derivative is the chord, which lies in Π(t). The t-derivative has the component
  ⟨γ′, ·⟩ of the moving plane: π_e(b*_f(t)) = γ_e(t), so its tangential part is nonzero.

### Step 3. Σ_out is a compact surface with boundary ⋃ λ_v

- **Interior points of a patch, strip or re-trimmed arc away from the spheres** have a disk neighbourhood:
  - patches are embedded (P0′);
  - strips are embedded bands (Step 2);
  - a strip meets its patches only along the junction curves (E4a);
  - two patches meet only along re-trimmed arcs (S1′), where they cross transversally (R′) and are cut, leaving two
    half-disks glued along c_e;
  - pieces that are not adjacent are disjoint (S1′).
- At a junction point b*_f(t), the patch P̃_f and the strip σ_e are two C¹ half-disks glued along a C¹ curve, meeting
  only along it (E4a). Their union is a topological disk neighbourhood.
- Near S_v, transversality (V1′a) makes Σ_out a surface with boundary S_v ∩ Σ_out = λ_v. Nothing else of Σ_out meets
  B_v (V0′).
- Compactness: finitely many compact pieces, intersected with a closed set.

### Step 4. Σ_out is homeomorphic to |K| minus open vertex stars, cell by cell

- **Faces.** P_f is a closed disk (P0′). Cutting it along its re-trimmed arcs keeps a disk P̃_f whose boundary is a
  cyclic sequence of boundary arcs (at strip edges) and arcs c_e (at re-trimmed edges). P̃_f ∩ B_v is the corner piece
  at v. By (V1′b), S_v ∩ P̃_f is a single arc. That arc joins the two boundary arcs of P̃_f at v and cuts off a disk
  containing the corner; nothing else of P̃_f lies in B_v, since P̃_f is connected and every other point is outside B_v.
  So P̃_f \ ⋃ int B_v is a closed disk Q_f whose boundary alternates: edge arcs, and sphere arcs at the vertices of f.
- **Strip edges.** σ_e ≅ I_e × [0,1] (Step 2). The two end chords c_e(a_e), c_e(b_e) lie in int B_v, int B_w (V0′).
  S_v ∩ σ_e is a single arc (V1′b) separating the end chord from the rest. So σ_e \ (int B_v ∪ int B_w) is a closed
  disk R_e ≅ [0,1]², whose sides are the two junction curves and whose ends are the two sphere arcs.
- **Re-trimmed edges.** c_e \ (int B_v ∪ int B_w) is a single arc (R′, V0′, V1′a).
- **Gluing.**
  - Q_f is glued to R_e along the junction curve b*_f, for each strip edge e of f.
  - Q_f is glued to Q_g directly along c_e, for each re-trimmed edge.
  - The cyclic order at each vertex is that of the link (V1′b).
  - The resulting space is the abstract surface obtained from |K| by removing a small open star at each vertex. The
    homeomorphism maps the open face f to int Q_f ∪ the two half-strips, the open edge e to the midline of R_e (or
    to int c_e), and each removed star to the corresponding B_v.

### Step 5. Cones

- λ_v is a simple closed curve on S_v (V1′b), so the radial cone C_v = {p_v + s(x − p_v) : x ∈ λ_v, s ∈ [0,1]} is an
  embedded closed disk, since radial projection from p_v is injective on rays. C_v ⊂ B_v and C_v ∩ S_v = λ_v.
- Σ_out ∩ B_v = λ_v (Step 3). So Σ = Σ_out ∪ ⋃ C_v is embedded, and is homeomorphic to |K| by Step 4.
- Map the star of v onto C_v by the cone structure, with p_v ↦ v; the edges at v go to the rays to the end points of
  their midlines or arcs, and the faces to the cone sectors over their arcs.

So h₀: |K| → Σ is a topological embedding with every open cell in its zone (Step 1). It is a topological
realization.

### Step 6. PL approximation

We use the argument of P1, Appendix B, in the following form.

> **Lemma A (from P1, Appendix B).** Let h₀: |K| → R³ be a topological embedding. Suppose |K| has a finite
> triangulation T, subdividing the cells, such that h₀ is C¹ with injective differential on each closed triangle,
> and h₀ is locally bi-Lipschitz. Then for every m > 0 a fine secant approximation of h₀ is a PL embedding within m
> of h₀.

Here a margin m > 0 exists because each closed cell is compact and lies in its open zone. So the secant
approximation is a realization.

Hypotheses of Lemma A:
- **C¹ pieces.** Patches (C²), strips (C¹ by Step 2) and cones away from the apex are C¹ with injective differential.
  Triangulate each closed piece by curved triangles reproducing the shared boundary curves (P1, Lemma C.1, for C¹
  curves). The cone at the apex is covered by the cone structure itself: triangles with a corner at p_v, mapped
  radially, which are C¹ up to the apex in the parametrization (s, θ) ↦ p_v + s(λ(θ) − p_v) with injective
  differential for s > 0. **Gap:** at s = 0 the differential degenerates. P1 had the same issue at vertices and handled
  it with the tangent-cone (blow-up) argument (P1, Appendix B, vertex bullet); here the tangent cone at p_v is C_v
  itself, an embedded disk. To be written out.
- **Locally bi-Lipschitz.**
  - Inside pieces: C¹ with injective differential.
  - Along junction curves between a patch and a strip: the two tangent half-planes are distinct by the no-fold
    condition (E4b), so the tangent cone is an embedded disk.
  - Along re-trimmed arcs: transversality (R′).
  - Along λ_v: the cone is radial and the outside piece is transversal to S_v (V1′a), so the inward and outward
    half-planes are distinct.
  - At p_v: the cone, as above.

The secant approximation is then a PL realization. ∎ (modulo the gap in Step 6)

## 5. Notes and gaps

1. **Gap (Step 6):** write the cone-apex bi-Lipschitz argument; reuse P1 Appendix B's blow-up.
2. **Regular K only.** Seams and poles are covered by the checker (`compute/strip_cone_check2.py`) but not by this
   statement. A seam vertex has a face appearing twice in the link; a pole has a degenerate edge. Both need the
   edge-graph formalism of P1 Prop. 5.3 (clause R).
3. **(V0′) includes that B_v misses non-incident pieces.** The checker's L3 only tests outside the ball up to 3 τ_v;
   add a direct test.
4. **(S1′) and (E4a) are global.** The checker tests them on samples near the vertices (L3) and per normal plane (L4).
   A global patch–patch test (as P1's S1(e)) is needed for whole models.
5. **Cusp corners** (face angle 0) violate (V1′b), as observed. Whether such data can still be realizable is open.
6. **What is new compared with P1.**
   - No tube radius ρ_e: the strip bridges the actual gap between the two patches, and the patches are kept up to their
     own boundaries.
   - At a sewn vertex the vertex ball only has to contain the corners (≈ 0.65–0.84 τ_v), not separate tubes
     (≈ 1.9 τ_v).
