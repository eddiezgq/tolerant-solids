# Lemma 0 (existence), draft v0.2 (11-12). Revised after two reviews (lemma0_v0_review.md, lemma0_v01_review.md).

Status: conditional existence theorem. V1 and P0 are non-local hypotheses that are checked computationally; they are not derived from local data. With them, the second review found no counterexample.

## 0. Setting
- K is a finite regular CW complex whose shells are closed surfaces. Section 6 discusses B-rep complexes with seams, closed edges and multi-wire faces.
- Data:
  - a point p_v for each vertex;
  - a C² curve γ_e: [0, 1] → R³ for each edge;
  - for each face, a C² surface S_f with a compact trimmed patch P_f ⊂ S_f.
- ∂P_f is a union of pcurve images β_{f,e}. SameParameter gives |β_{f,e}(t) − γ_e(t)| ≤ dev_e ≤ τ_e.
- Zones:
  - Z(v) = B(p_v, τ_v);
  - Z(e) = N_{τ_e}(γ_e) ∪ Z(endpoints);
  - Z(f) = N_{τ_f}(P_f) ∪ ⋃_{e<f} Z(e).
  - All of these are open sets.
- A realization is a PL embedding h: |K| → R³ with h(int σ) ⊆ Z(σ).

## 1. Auxiliary sets
- For an edge e:
  - choose ρ_e and parameters 0 < a_e < b_e < 1;
  - D_e(t) is the closed normal disk of radius ρ_e at γ_e(t), in the normal plane Π(t);
  - T_e = ⋃_{t∈[a_e,b_e]} D_e(t), the union of normal disks (no end caps).
- For a vertex v: choose r_v and W_v = B(p_v, r_v) ∪ ⋃_{e∋v} ⋃_{t between v and a_e (resp. b_e)} D_e(t).

## 2. Hypotheses (all computable from the data)
**E1 (edge tube).**
- dev*_e < ρ_e < min(τ_e, reach(γ_e|[a_e, b_e])).
- dev*_e is the in-normal-plane deviation of the boundary points b_{f,e}(t) := ∂P_f ∩ Π(t) near γ_e(t). dev*_e ≤ dev_e.

**E2 (each adjacent face crosses its tube wall exactly once).** For every e, every f > e, and every t in [a_e, b_e] and on the exposed stubs [t_v, a_e] and [b_e, t_w]. Here t_v is the last parameter with γ_e(t) ∈ B(p_v, r_v). E1 is required on the same range.
1. ψ_f < π/2, where ψ_f is the maximum angle between γ_e′ and T P_f inside T_e. Also ρ_e k_f < 1, with k_f = κ_f / cos ψ_f.
2. The projection t ↦ π_e(β_{f,e}(t)) onto γ_e is strictly monotone. A sufficient first-order condition is L_e + κ_γ dev*_e < 1, where L_e is the arc-length Lipschitz constant of β_{f,e} − γ_e.
3. No return: dist(γ_e(t), P_f ∖ C_f) > ρ_e. Here C_f is the union of the section arcs from b_{f,e} up to their exit point (length ≤ ℓ_f), with ℓ_f = (dev* + √(dev*² + μρ²))/μ and μ = 1 − ρk_f; these arcs exist inside P_f.

**E3 (exit points distinct).**
- α_e(t) > ε_f + ε_g, where ε = arcsin(min{1, (dev*_e + k ℓ²/2)/ρ_e}).
- α_e(t) is the angle between the in-plane tangents u_f, u_g of the two sections at their boundary points, pointing into the patches.
- Leading order: α > 2√(2 k dev*) with ρ = √(2 dev*/k) when that is ≤ τ_e; otherwise α > 2(dev*/τ_e + kτ_e/2).
- Necessary in the straight case: τ_e > dev*/sin(α/2).

**V0.** γ_e(0) and the corners of P_f at v lie in int B(p_v, r_v).

**V1 (vertex region; (b) is a non-local hypothesis, checked computationally).**
- (a) W_v is strictly star-shaped with respect to p_v (each ray from p_v meets ∂W_v once, transversally), and W_v ⊂ int B(p_v, τ_v).
  - Sufficient (corrected after the second review; the v0.1 clause was wrong, see counterexample 6A in lemma0_v01_review.md):
    - ρ_e > |P⊥(γ_e(t) − p_v)| on the exposed stub [t_v, a_e], where P⊥ is the projection onto the normal plane Π(t). So p_v lies within ρ_e of the stub's tangent lines.
    - The end disks of different edges are disjoint: |γ_e(a_e) − p_v| ≥ max(r_v + ρ_e, ρ_e / sin(θ_v/2)).
    - Otherwise, move the cone apex or blend the edge into p_v first.
  - In the straight radial case this needs τ_v > ρ √(1 + 1/sin²(θ_v/2)).
  - Cusp vertices (θ_v = 0) are excluded.
- (b) The part of the construction outside W_v meets ∂W_v transversally in one simple closed curve λ_v. On λ_v:
  - each incident edge contributes the point γ_e(a_e);
  - each incident face f contributes an arc from the edge point of one of its edges at v to that of the other;
  - this arc runs along the fan segment [γ_e(a_e), k_{f,e}(a_e)] in the end disk, then along k_{f,e} or P_f on the side walls and the sphere;
  - the cyclic order agrees with lk(v, K).

**S1 (separation).**
- (a) The W_v are pairwise disjoint.
- (b) The T_e are pairwise disjoint.
- (c) γ_e and T_e miss W_w for w ∉ ∂e.
- (d) P_f misses T_e for e ⊄ ∂f, and misses W_v for v ∉ ∂f.
- (e) Outside ⋃T ∪ ⋃W, the patch pieces are pairwise disjoint.
- (f) T_e ∩ W_v = D_e(a_e) for v ∈ ∂e, and every piece outside W_v meets W_v only in λ_v.

**P0 (patch; non-local hypothesis, checked computationally).** Each P_f is embedded, and P_f ∩ (⋃T ∪ ⋃W) is a collar of ∂P_f. So Q_f := P_f ∖ int(⋃T ∪ ⋃W) is a closed disk, and ∂Q_f = ⋃ k_{f,e} ∪ (arcs on ∂W_v).

**Strictness.** ρ_e < τ_e and W_v ⊂ int B(p_v, τ_v). Write m > 0 for the minimum zone margin.

## 3. Construction
1. h(v) = p_v.
2. On [a_e, b_e], h(e) = γ_e. In each D_e(t), the radial segment from γ_e(t) to k_{f,e}(t) is assigned to f. Here k_{f,e}(t) is the unique exit point given by E2. The fan strip is F_{f,e} = ⋃_t [γ_e(t), k_{f,e}(t)].
3. Face f outside the vertex regions is Q_f ∪ ⋃_{e<f} F_{f,e}.
4. Inside W_v, take the cone from p_v over λ_v: every x ∈ λ_v is joined to p_v by a segment.
   - The cone over the edge point of e gives h(e) between v and a_e.
   - The cone over f's arc gives a sector of h(f).
5. PL step (Section 5).

## 4. Proof that h (before the PL step) is a continuous injective map with h(int σ) ⊆ Z(σ)
**Pieces and their supports.**
- Q_f ⊂ P_f, outside int ⋃T and int ⋃W.
- F_{f,e} ⊂ T_e.
- The cone sectors and edge stubs lie in W_v.

**Injectivity inside T_e.**
- The D_e(t) are pairwise disjoint (E1: ρ < reach).
- In each D_e(t) the realization consists of the centre and two radii to distinct boundary points (E3). These meet only at the centre.
- No other piece enters T_e: S1(b)–(d), S1(f), and P0 (the patches of f > e enter T_e only in their collar, which is removed).

**Injectivity inside W_v.**
- The cone map (s, x) ↦ p_v + s(x − p_v), for s ∈ (0, 1] and x ∈ λ_v, is injective because each ray meets ∂W_v once (V1a) and λ_v is simple (V1b).
- No other piece enters W_v: S1(a, c, d) for non-incident pieces, and S1(f) for incident ones.

**Injectivity outside ⋃T ∪ ⋃W.** By S1(e), and since each Q_f is embedded (P0).

**Continuity and cell structure.**
- Q_f and F_{f,e} agree along k_{f,e}.
- The fans and Q_f agree with the cone along λ_v, because λ_v is exactly the trace of these pieces on ∂W_v (V1b).
- So h(f) = Q_f ∪ fans ∪ sectors is a closed disk whose boundary is the union of the h(e), e < f, in the order of ∂f.
  - Q_f is a disk (P0).
  - Each fan is a strip glued along k_{f,e}.
  - Each sector is a triangle-like region glued along an arc of λ_v.

**Cell structure (added after the second review).**
- (a) Order. ∂Q_f is a single circle made of the curves k_{f,e} and the arcs A_{f,v} on ∂W_v (P0). V1(b) gives exactly one arc per vertex of f, joining k_{f,e}(a_e) to k_{f,e′}(a_{e′}). So the pieces form a 2-regular graph isomorphic to ∂f, the only cycle through all of them is ∂Q_f, and the cyclic order is forced.
- (b) Exact intersections.
  - Q_f ∩ F_{f,e} = k_{f,e}, by E2.3 and S1(f).
  - (Q_f ∪ fans) ∩ sector_{f,v} = A_{f,v}, by star-shapedness and S1(f).
  - Gluing two disks along a boundary arc that is their whole intersection gives a disk. By induction, h(f) is a closed disk with ∂h(f) = ⋃_{e<f} h(e).
- (c) h as a map. Fix a homeomorphism h|∂f: ∂f → ∂h(f) that respects the cells. Extend it over f by the Alexander trick, through a chart of the disk h(f) in which the boundary is straightened. For Section 5, take this extension piecewise C¹ (straighten the C¹ boundary of Q_f in the parameter domain of P_f).

**Zones.**
- Q_f ⊂ P_f ⊂ Z(f).
- F_{f,e} ⊂ T_e ⊂ N_{ρ}(γ_e) ⊂ Z(e) ⊂ Z(f).
- The cone parts lie in W_v ⊂ B(p_v, τ_v) = Z(v) ⊂ Z(e), Z(f) for incident e, f.
- h(int e) ⊂ γ_e ∪ W_v ⊂ Z(e).
- All inclusions have margin ≥ m.

## 5. PL step
- **h is bi-Lipschitz.** It is injective on a compact set and locally bi-Lipschitz: every crease has a non-zero opening angle.
  - Fan/patch along k: the fan leaves k in direction −r̂, and the patch section leaves with c′·r̂ > 0 (strict convexity in E2). So the angle is > 90°.
  - Fan/fan along γ_e: E3.
  - Cone/outside along ∂W_v: strict star-shapedness.
- **Points where three or more pieces meet** (k_{f,e}(a_e), γ_e(a_e), corners of ∂W_v). Non-zero crease angles are not enough there; the tangent cone must be an embedded PL disk.
  - At k(a_e): the fan and Q_f tangent sectors lie in the closed quarter-space {⟨·, γ′⟩ ≤ 0, ⟨·, r̂⟩ ≤ 0}. The cone sectors lie inside it, with −(x − p_v) in its interior. The only shared rays are −r̂ and the side-wall tangent, each between adjacent sectors.
  - At γ(a_e): the fans lie in ⟨·, γ′⟩ ≥ 0 and the sectors in ⟨·, γ′⟩ ≤ 0. They share only the rays r̂_f ≠ r̂_g (E3).
- **Regularity.** Π(t) depends on γ′, so the fans, k and the stub walls are only C¹ when γ is C². The secant estimate needs only C¹: Lip(S − h) ≤ C·ω(Dh, mesh)/sin θ_min → 0, where ω is a modulus of continuity.
- **Apex.** On radial triangles at p_v, h is homogeneous of degree 1 and not C² up to the apex. But S − h is degree-1 homogeneous there too, with radial derivative O(mesh²·κ_λ) and angular derivative O(mesh·κ_λ). So Lip(S − h) = O(mesh) uniformly. Bi-Lipschitz at the apex holds because λ_v is transverse to the rays and |x − p_v| is bounded below on λ_v.
- **Secant map.** Take a shape-regular triangulation of |K| that:
  - refines the piece decomposition;
  - has p_v as a vertex;
  - is radial on the cone sectors;
  - has h of class C¹ on every closed triangle away from the apexes.
- Then the secant (vertex-interpolating) map S satisfies Lip(S − h) → 0 and |S − h| → 0 as the mesh size → 0.
  - So S is injective once Lip(S − h) < bi-Lipschitz constant.
  - S stays in the zones once |S − h| < m.

## 6. Scope and remarks
1. **B-rep complexes.**
   - Seam edges: E3 then refers to the two sheets of f.
   - Closed edges with one vertex: V1 counts edge ends.
   - Faces with inner wires: P0 becomes "Q_f is homeomorphic to the face".
   - The construction never uses that faces are disks except through P0. Lemma 2 (uniqueness) assumes regularity, so for now the joint theorem needs a subdivision step.
2. **Margins.**
   - E3 needs τ_e > dev*/sin(α/2).
   - If OpenCascade's edge tolerance equals the measured deviation (τ_e = dev_e), this construction does not apply. An alternative route (ASZ Whitney-extension perturbation plus normal-angle conditions near edges) may avoid the ρ > dev margin. Open.
3. **Thin features.** S1(d) excludes walls and slivers thinner than about 2ρ.
4. **Literature.**
   - ASZ 2007 (pp. 819–820) and Stewart–Zidani 2008 (p. 188) assume that the perturbed patches embed; ASZ says adjacent patches need a posteriori verification.
   - APS 2000 and ASZ 2006 have not been read yet. Do not claim novelty before reading them.
5. **Output.** h is the reference surface M for Lemma 1. Each closed cell lies in its carrier.
