# Uniqueness of realizations of a tolerant B-rep (genus ≥ 1): proof draft v0.1

**Status (2026-11-12).** Draft. It has had two independent reviews: [reviews/proof_v0_review.md](reviews/proof_v0_review.md) and [reviews/lemma1_multishell_review.md](reviews/lemma1_multishell_review.md). No fatal errors were found, and all the corrections they asked for are made here. The multi-shell argument in Section 5 has also been reviewed and found correct. This is the English version of the text in the phase-1 working document. [proof_v0.md](proof_v0.md) is the earlier v0.

Not covered here:
- sphere shells (genus 0);
- isotopy *as embeddings*, rather than of images;
- the existence of a realization (Lemma 0, see [lemma0_v02.md](lemma0_v02.md));
- the computation of the collar (Lemma 1, see the certified weak-feature-size code in `compute/`).

## 1. Setting and definitions

**Complex.**
- K is a finite *regular* CW complex: each closed cell σ̄ is a ball, and its boundary is a subcomplex.
- K is the disjoint union of shells K_1, …, K_n, and each |K_i| is a closed connected surface.
- τ ≤ σ means that τ is a face of σ (including τ = σ).
- B-rep faces with holes, seam edges and closed edges are not regular. They must be subdivided first.

**Zones.**
- Each cell σ has an open tolerance zone Z(σ) ⊂ R³.
- The zones are *augmented*:
  - a vertex zone is a ball;
  - an edge zone is the tube of the edge plus the balls of its end vertices;
  - a face zone is the τ_f-neighbourhood of the trimmed patch plus the zones of its boundary edges.
- The **carrier** of σ is C(σ) = ⋃_{τ≤σ} Z(τ). With augmented zones, C(σ) = Z(σ). C is monotone: τ ≤ σ implies C(τ) ⊆ C(σ).

**Realization.**
- A realization is a PL embedding h: |K| → R³ with h(int σ) ⊆ Z(σ) for every cell σ. This is the *open-cell* condition: the closed-cell condition can be unsatisfiable for reasonable models when vertex ≥ edge ≥ face tolerances.
- Tameness (PL) rules out wild embeddings such as Alexander's horned sphere.
- A continuous map f: |K| → R³ is **carried by C** if f(σ̄) ⊆ C(σ) for all σ.
- A realization is carried by C: σ̄ is the union of the interiors of the faces of σ (regularity), and each of them maps into its own zone, which lies in C(σ).

Machine-checked in Lean ([../lean/Tolerant/Carrier.lean](../lean/Tolerant/Carrier.lean)):
- the definitions;
- monotonicity of C and C = Z for augmented zones;
- "realizations are carried";
- the convex-carrier special case of Lemma 2.

## 2. Hypotheses

**Carrier condition.** C(v) is path-connected for every vertex v, and π_k(C(σ)) = 0 for every k-cell σ with k ≥ 1. Contractible carriers suffice.

**Collar condition.** For each shell K_i there are:
- a compact PL submanifold U_i ⊂ R³;
- a PL homeomorphism U_i ≅ M_i × [−1, 1].

Their properties:
- M_i × {0} is the image of a PL embedding φ_i: |K_i| → R³ that is carried by C (a *reference surface*);
- all zones of the cells of K_i lie in int U_i;
- the U_i are pairwise disjoint.

Lemma 1 reduces the collar condition to a computable inequality: zones within distance d of M_i with d < wfs(M_i), plus disjoint collars. Lemma 0 supplies a reference surface.

**Genus.** Each M_i has genus ≥ 1.

## 3. Lemmas

**Lemma 2 (carrier).** Under the carrier condition, any two maps f, g: |K| → R³ carried by C are homotopic by a homotopy H with H(σ̄ × I) ⊆ C(σ) for every σ.

*Proof.* Define H on |K| × {0, 1} ∪ |K^{(k)}| × I by induction on k, keeping H(σ̄ × I) ⊆ C(σ). Start with H(·, 0) = f and H(·, 1) = g.
- k = 0: for a vertex v, f(v) and g(v) lie in C(v), which is path-connected. Take a path between them.
- k ≥ 1: let σ be a k-cell. Then σ̄ × I is a (k+1)-ball whose boundary σ̄ × {0, 1} ∪ ∂σ̄ × I is a k-sphere. H is already defined on that sphere:
  - on σ̄ × {0, 1} it is f or g, with image in C(σ);
  - on ∂σ̄ × I it is defined by induction, with image in ⋃_{τ<σ} C(τ) ⊆ C(σ).

  Since π_k(C(σ)) = 0, H extends over σ̄ × I with image in C(σ).
- The definitions agree on common boundaries. A finite union of closed sets glued continuously gives a continuous H. □

**Lemma 2′ (separation).** Assume the carrier and collar conditions, and let h be a PL realization. Then G := h(|K_i|) is a closed surface in int U_i, and the inclusion G ↪ U_i is a homotopy equivalence.

*Proof.*
- Apply Lemma 2 on K_i to h and φ_i. The homotopy has image in ⋃ C(σ) ⊆ int U_i, so it is a homotopy in U_i.
- φ_i: |K_i| → U_i is a homeomorphism onto the level M_i × {0} followed by inclusion, which is a homotopy equivalence. Hence h: |K_i| → U_i is a homotopy equivalence too.
- h is a homeomorphism from |K_i| onto G, so the inclusion G ↪ U_i, which equals h ∘ h⁻¹, is a homotopy equivalence. □

**Lemma 3 (upgrade, genus ≥ 1).** Under the hypotheses of Lemma 2′, if M_i is not a sphere, there is an ambient isotopy of R³, supported in U_i and fixed on ∂U_i, that carries G to M_i × {0}.

*Proof.*
- **(a) G is incompressible.**
  - By Lemma 2′, π_1(G) → π_1(U_i) is an isomorphism, in particular injective.
  - Waldhausen's definition of incompressibility (Ann. of Math. 87 (1968) 56–88, p. 58) then applies directly. The boundary of a compressing disk would be a closed curve that is not contractible in G but is contractible in U_i, which contradicts injectivity.
  - G is not a sphere, so case (b) of that definition does not arise.
  - The converse direction (Lemma 1.1.3, which needs the loop theorem) is not used.
  - G is a closed orientable surface in an orientable 3-manifold, hence two-sided, and it is disjoint from ∂U_i. So it satisfies Waldhausen's conventions for surfaces (§0).
- **(b) G can be made horizontal.**
  - Apply Waldhausen's Proposition 3.1 (pp. 65–66) to U_i = M_i × I (M_i orientable, not a sphere) and the incompressible surface G (∂G = ∅, so the condition "∂G ⊆ F × 1" holds vacuously).
  - It gives an isotopy, constant on ∂U_i, from G to a surface G′ such that the projection p: G′ → M_i is a homeomorphism onto its image. Proposition 3.1 needs only F orientable and not a sphere, so tori are included. "Homeomorphism on each component" means a homeomorphism onto the image (p. 66).
  - G′ lies in int U_i. p(G′) is open (invariance of domain in dimension 2) and closed in the connected surface M_i, so p(G′) = M_i. Hence G′ is the graph of a function s: M_i → (−1, 1).
- **(c) Flatten.**
  - On each fibre {x} × [−1, 1], take the piecewise-linear homeomorphism that fixes both ends and sends s(x) to (1 − t)·s(x), for t from 0 to 1.
  - This gives an ambient isotopy of U_i, fixed on ∂U_i, that carries G′ to M_i × {0}. It is topological; this formula is not PL.
  - PL alternative: the region between G′ and M_i × {0} is a product region, so the two surfaces are parallel and hence isotopic (Waldhausen, p. 58).
- **(d) Extend.** Both isotopies are fixed on ∂U_i, so they extend by the identity to R³. □

## 4. Theorem (uniqueness, genus ≥ 1)

Assume the carrier condition, the collar condition with pairwise disjoint collars, and genus ≥ 1 for every shell. Then:
1. the image of any PL realization is ambient isotopic to ⋃ M_i;
2. hence the images of any two PL realizations are ambient isotopic;
3. and the r-sets they bound (Section 5) are ambient isotopic.

*Proof.*
- Apply Lemma 3 shell by shell. The isotopies have pairwise disjoint supports, so they can run simultaneously.
- The end map of the resulting ambient isotopy is a homeomorphism Φ of R³ with Φ(G_i) = M_i for every i.
- Section 5 shows that Φ carries the bounded r-set to the corresponding one. □

## 5. Multi-shell r-sets

**Definition.** Let S_1, …, S_n be pairwise disjoint closed surfaces in R³.
- The depth of a point x is the number of S_j that have x on their bounded side.
- The r-set they bound is the closure of the set of points of odd depth. This is the usual convention for outer shells plus cavities.

**Argument.**
- Φ is the end map of an ambient isotopy supported in the compact set ⋃U_i.
- Φ(G_j) = M_j for every j. On U_j the isotopies of the other shells are the identity, and each shell is connected.
- Φ is a homeomorphism of R³, so it maps the unbounded component of R³ ∖ G_j onto the unbounded component of R³ ∖ M_j, and the bounded component onto the bounded component. This uses the Jordan–Brouwer separation theorem: a closed surface separates R³ into exactly two components.
- So x is on the bounded side of G_j if and only if Φ(x) is on the bounded side of M_j. Depth is preserved, and Φ maps one r-set exactly onto the other.
- For two realizations with maps Φ and Φ′, the composite Φ′⁻¹ ∘ Φ gives the result.

**Remark.** When the shells are consistently oriented, the parity definition agrees with the B-rep convention (outer shells, cavities, nested solids). A wrongly oriented shell is silently ignored by it, so a validity check must test orientation separately.

## 6. Standard facts used but not separately checked against sources

- Continuity of cell-by-cell extension on a finite CW complex.
- The level inclusion M ↪ M × I is a homotopy equivalence.
- Closed surfaces in R³ are orientable.
- Invariance of domain in dimension 2.
- The fibrewise flattening is a topological ambient isotopy.
- The Jordan–Brouwer separation theorem.
- Sources still to be checked, requested from the library: Moise, *Geometric Topology in Dimensions 2 and 3*, ch. 17 and 35; Hempel, *3-Manifolds*, ch. 6 and 10. These cover the irreducibility of F × I (used for the PL alternative and for later extensions) and the PL Schoenflies theorem (for the sphere case).

## 7. Comparison with the earlier draft

- Step (a) no longer uses the Kneser inequality.
- The cost is that the collar must be built around φ_i, and most of the weight falls on Waldhausen's Proposition 3.1, whose proof in the original is brief.
- The sphere case and isotopy as embeddings still need Kneser-type facts.
- Experiment 6b shows that the collar hypothesis cannot be dropped. In [../compute/exp6b2.py](../compute/exp6b2.py), a model that passes both OpenCascade checks has two realizations whose solids are not even homeomorphic.
