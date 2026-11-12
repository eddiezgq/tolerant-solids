# Proof draft v0 — uniqueness (genus >= 1)

## Setting
- K is a finite regular CW complex: each closed cell σ̄ is a ball, and its boundary is a subcomplex.
- Each shell K_i is a closed, connected surface.
- Each cell σ has a zone Z(σ) ⊆ R³.
- The carrier of σ is C(σ) = ∪_{τ ≤ σ} Z(τ).
- A map f: |K| → R³ is **carried by C** if f(σ̄) ⊆ C(σ) for every σ.
- A **realization** is a PL embedding h with h(int σ) ⊆ Z(σ) for every σ. A realization is automatically carried by C, because σ̄ is the union of the interiors of its faces.
- Monotonicity: if τ ≤ σ then C(τ) ⊆ C(σ).

## Lemma 2 (carrier)
**Statement.** Suppose that for every σ, C(σ) is nonempty and π_j(C(σ)) = 0 for j = 0, …, dim σ. Then any two maps f, g carried by C are homotopic by a homotopy H with H(σ̄ × I) ⊆ C(σ) for every σ.

**Proof.** We define H by induction on k over |K| × {0,1} ∪ |K^(k)| × I.
1. Set H(·,0) = f and H(·,1) = g.
2. Case k = 0. For a vertex v, both f(v) and g(v) lie in C(v), which is path-connected; take a path between them inside C(v).
3. Case k ≥ 1. Let σ be a k-cell. Then σ̄ × I is a (k+1)-ball, and its boundary σ̄×{0,1} ∪ ∂σ̄×I is a k-sphere.
   - On σ̄ × {0,1}, H is f or g, so its image lies in C(σ).
   - On ∂σ̄ × I, H is already defined by the induction hypothesis, with image in ∪ C(τ) ⊆ C(σ).
   - Since π_k(C(σ)) = 0, H extends over σ̄ × I with image in C(σ).
4. The pieces agree on common boundaries, and finitely many closed sets are pasted together, so H is continuous. □

## Lemma 2′ (separation)
**Hypothesis (collar).** All zones of the cells of shell K_i lie in int U_i. Here U_i is a compact PL submanifold of R³ with a PL homeomorphism U_i ≅ M_i × [−1, 1], and the level M_i × 0 is a reference surface given by a PL embedding φ_i that is carried by C.

**Statement.** For any PL realization h, G := h(|K_i|) is a closed surface in int U_i, and the inclusion G ↪ U_i is a homotopy equivalence.

**Proof.**
1. Lemma 2 gives h ≃ φ_i, with the homotopy's image in ∪C(σ) ⊆ int U_i. So this is a homotopy in U_i.
2. φ_i is a homeomorphism onto the level followed by inclusion, which is a homotopy equivalence. Hence h: |K_i| → U_i is a homotopy equivalence.
3. Since h is a homeomorphism from |K_i| onto G, the inclusion G ↪ U_i equals h ∘ h⁻¹ and is a homotopy equivalence. □

## Lemma 3 (upgrade, genus ≥ 1)
**Statement.** Assume Lemma 2′ holds and M_i is not a sphere. Then there is an ambient isotopy of R³, supported in U_i and fixed on ∂U_i, that takes G to M_i.

**Proof.**
- **(a) G is incompressible.** By Lemma 2′, π1(G) → π1(U_i) is an isomorphism, so it is injective. G is not a sphere, so by Waldhausen Lemma 1.1.3 G is incompressible. G is an orientable closed surface in an orientable manifold, hence two-sided, and it is disjoint from ∂U_i.
- **(b) Making G horizontal.** Apply Waldhausen Prop 3.1 to M = F × I with F = M_i (not S²) and G: since ∂G = ∅, the condition ∂G ⊆ F×1 holds vacuously. This gives an isotopy, constant on ∂M, taking G to a surface G′ such that p|G′ is a homeomorphism onto its image. The image p(G′) is open (by invariance of domain) and closed in the connected surface M_i, so p(G′) = M_i. Thus G′ is the graph of a function s: M_i → (−1, 1).
- **(c) Flattening.** On each fiber, apply the piecewise-linear map that fixes ±1 and sends s(x) to (1−t)s(x), for t from 0 to 1. This is an ambient isotopy of U_i, fixed on ∂U_i, taking G′ to M_i × 0.
- **(d) Extension.** Both isotopies are fixed on ∂U_i, so they extend by the identity to all of R³. □

## Theorem (uniqueness, genus ≥ 1)
**Statement.** Assume the carrier condition and the collar condition, that the collars of different shells are pairwise disjoint, and that every shell has genus ≥ 1. Then every PL realization image is ambient isotopic to ∪M_i. Consequently, any two such images are ambient isotopic, and so are the r-sets they bound.

**Proof.** Apply Lemma 3 to each shell. The supports are disjoint, so the isotopies can be run simultaneously. The end map is a homeomorphism of R³, and it takes bounded complementary regions to bounded complementary regions. □

## Standard facts used without separate verification
- Continuity of cellwise extension on a finite CW complex.
- The level inclusion M → M × I is a homotopy equivalence.
- Closed surfaces in R³ are orientable.
- 2D invariance of domain.
- Fiberwise PL flattening is a PL ambient isotopy.
