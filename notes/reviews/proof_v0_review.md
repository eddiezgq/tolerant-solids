# Referee report: proof_v0.md (uniqueness, genus ≥ 1)

Audited file: `audit/proof_v0.md`. Context: `audit/math_audit.md`.
Source checked: Waldhausen, "On irreducible 3-manifolds which are sufficiently large", Ann. of Math. 87 (1968). Statements were checked against the page images for pp. 56–58 and 65–66, and against the text extraction for pp. 58–59 and 67–68.
Facts that are not in this source are marked **[standard, unverified here]**.

## Verdict at a glance

| Item | Verdict |
|---|---|
| Lemma 2 (carrier) | **Correct.** The hypothesis is sufficient but stronger than needed (#1). Regular CW is not needed for the lemma itself, but it is used for "realizations are carried" (#2). |
| Lemma 2′ (separation) | **Correct**, with minor fixes in wording and notation (#3). |
| Lemma 3 (a) | **Correct.** Citing Lemma 1.1.3 (the loop theorem) is more than needed, and the justification is out of order (#4). |
| Lemma 3 (b) | **Correct.** Prop. 3.1 applies to a closed G in a closed F, and there is no torus exception. One small step is missing (#5). |
| Lemma 3 (c) | **Correct as a topological isotopy.** The "standard fact" that it is PL is false as formulated (#6). |
| Lemma 3 (d) | **Correct** (#7). |
| Theorem | **Gap.** The r-set conclusion is not proved, and "r-set" is never defined. Two structural hypotheses are missing (#8, #9, #10). |
| The remark "不再需要 Kneser" | **Mild overclaim** (#11). |

No fatal error was found. The set-level argument (Lemma 2 → 2′ → 3) is sound once the fixes below are made.

---

## Issue 1 — Lemma 2: the hypothesis is sufficient, but more than needed. Severity: MINOR (sharpening)

The inductive step for a k-cell (k ≥ 1) extends a map from the k-sphere ∂(σ̄×I) into C(σ). The sphere is connected, so this uses only:
- π_k of the path component that contains its image;
- for vertices, π_0(C(v)) = 0.

The groups π_j(C(σ)) for 0 < j < dim σ are never used.

So the minimal hypothesis is:
- C(v) is path-connected for every vertex v;
- π_k(C(σ), x) = 0 for every k-cell σ with k ≥ 1 and every x ∈ C(σ).

In particular, a face carrier does **not** need to be simply connected. Only π₂ matters, because the boundary circle has already been mapped compatibly.

The stated hypothesis "π_j = 0 for j ≤ dim σ" is therefore correct and sufficient. "C(σ) nonempty" is redundant, since it follows from π_0 = 0, or from the existence of a carried map.

**Fix.** State the weaker hypothesis. This matters in practice, because it accepts more data.

## Issue 2 — Regular CW: not needed for Lemma 2, needed elsewhere. Severity: MINOR

**Lemma 2 itself.** Characteristic maps Φ_σ: D^k → σ̄ suffice. On D^k×{0,1} ∪ S^{k−1}×I, take the map induced through Φ_σ×id and extend it over D^k×I using π_k(C(σ)) = 0.

The extension factors through σ̄×I for two reasons:
- Φ_σ×id identifies points only on S^{k−1}×I, where the map was already defined through H on ∂σ̄×I.
- Φ_σ×id is a closed surjection from a compact space to a Hausdorff one, hence a quotient map.

This is the usual cellular extension argument [standard, unverified here].

**Where regularity is used:**
- **(i) "A realization is automatically carried."** This needs σ̄ to be a union of whole cells τ ≤ σ. That holds because the Setting assumes ∂σ̄ is a subcomplex. In a general CW complex σ̄ can meet a cell only partially, and C(σ) would then have to be defined as the union of the zones of all cells that meet σ̄.
- **(ii) The relation ≤.** It is never defined. Define τ ≤ σ :⇔ τ ⊆ σ̄.
- **(iii) Monotonicity.** It is listed in the Setting as if it were an assumption, but it follows from the definition of C because ≤ is transitive. Say so.

Practical consequence: a CW version tolerates seam edges and closed edges without subdivision. It does not tolerate faces with holes, which are not cells.

**Continuity (Step 4)** is correct. |K|×I is covered by the finitely many closed sets σ̄×I. Two of them overlap in (σ̄∩σ̄′)×I, a union of lower closed cells times I, where H was defined earlier and every later extension agrees with it. The pasting lemma then applies.

## Issue 3 — Lemma 2′: correct; notation and wording. Severity: MINOR

**The deduction is correct.**
- h|K_i and φ_i are both carried, so Lemma 2 gives a homotopy whose image lies in ⋃_{σ∈K_i} C(σ) ⊆ int U_i.
- φ_i is a homeomorphism onto the level, followed by the inclusion of the level, which is a homotopy equivalence. Hence h: |K_i| → U_i is a homotopy equivalence.
- Write h̄: |K_i| → G for the corestriction. Then the inclusion j: G ↪ U_i equals h∘h̄⁻¹, a homotopy equivalence composed with a homeomorphism.
- G ⊂ int U_i holds because h(|K_i|) ⊆ ⋃C(σ) ⊆ int U_i.

**"φ_i is carried by C" is an assumption, not a conclusion.** It is the right assumption: it is exactly what Lemma 2 needs, and it is checkable from the data. φ_i does not have to be a realization. For Lemma 2′ alone it would suffice to have any carried map |K_i| → U_i that is a homotopy equivalence (or is π₁-injective). The embedding property is needed only so that Lemma 3 has a target surface.

**Fixes:**
- (a) M_i is used both for the abstract surface in M_i×[−1,1] and for the reference surface φ_i(|K_i|). Write Ψ_i: U_i → M_i×[−1,1] for the PL homeomorphism, require Ψ_i(φ_i(|K_i|)) = M_i×0, and call the target of Lemma 3 L_i := φ_i(|K_i|).
- (b) Lemma 3 says "Assume Lemma 2′ holds". A lemma does not "hold" for a given h. Write "under the hypotheses of Lemma 2′".
- (c) Implicit: C(σ) for σ ∈ K_i involves only cells of K_i. This needs K to be the disjoint union of the K_i (#9).

## Issue 4 — Lemma 3(a): correct, but Lemma 1.1.3 is more than needed, and the justification is out of order. Severity: MINOR

Waldhausen's definition, p. 58: *"F is compressible in M in either of the following two cases. (a) There is a non-contractible simple closed curve k in F, and a disc D in M, D̊ ⊂ M̊, such that D ∩ F = ∂D = k. (b) There is a ball E in M, such that E ∩ F = ∂E."*

- Case (b) forces F to be a 2-sphere.
- Case (a) puts k in ker(π₁F → π₁M).

So "π₁-injective and not a sphere ⇒ incompressible" follows **directly from the definition**. The loop theorem in Lemma 1.1.3 (*"F is incompressible, if and only if ker(π₁(F) → π₁(M)) = 0. Since F is either a submanifold of ∂M, or a two-sided proper surface in M, this follows from the loop theorem."*) is needed only for the converse, which is not used here.

If Lemma 1.1.3 is cited anyway, its hypotheses must be checked **before** it is invoked. The doc invokes it first and checks afterwards. The hypotheses, with the definitions on p. 57:
- **"Manifold".** An orientable, compact, connected 3-manifold. U_i is one: connected because M_i ≅ |K_i| is connected.
- **"Surface in M".** *"A surface is a connected 2-manifold. It is compact and/or orientable … A surface F in the manifold M is properly embedded, i.e., F ∩ ∂M = ∂F."* G is connected (K_i is connected), compact, and orientable [closed surfaces in R³; standard, unverified here]. Also G ∩ ∂U_i = ∅ = ∂G.
- **Two-sided.** An orientable surface in an orientable manifold is two-sided [standard, unverified here].
- **PL.** *"Up to §7, we work in the piecewise linear category"* (p. 56). G must be a PL submanifold of U_i in the PL structure U_i inherits from R³, and Ψ_i must be PL in that structure. This holds if:
  - |K| carries a PL structure in which h is PL (#10);
  - a PL-embedded surface in a PL 3-manifold is a (locally flat) PL submanifold [standard, unverified here].

  Add the second point to the list of standard facts.

## Issue 5 — Lemma 3(b): Prop. 3.1 does apply to a closed G in a closed F; one step is missing. Severity: MINOR

**Exact statement** (p. 65): *"In this section, M = F × I is the product of the orientable surface F which is not the 2-sphere, and the interval. p: M → F denotes the projection onto the factor F. … PROPOSITION 3.1. Let G be a system of incompressible surfaces in M. Suppose ∂G is contained in F × 1. Then G is isotopic, by a deformation which is constant on ∂M, to a system G′ such that p | G′ is homeomorphic on each component of G′."*

**Closed F is allowed.** The only restriction on F is "orientable … not the 2-sphere", and "surface" means compact, closed or bounded. No exception for the torus or any other surface is stated or needed.

**The proof covers closed F.** The general case runs *"by induction on (genus F, number of components of ∂F) in lexicographical ordering"*, cutting along a vertical annulus H with *"H ∩ F × 1 … a non-contractible curve which is not parallel to a component of ∂F × 1, and which is disjoint to ∂G"*.
- For a closed F of genus g ≥ 1, both side conditions are vacuous, and cutting along a non-separating curve gives (g−1, 2) < (g, 0).
- For a torus this lands on the annulus, which is a base case (*"in the case where F is a disc, annulus, or 2-sphere with 3 holes"*).

**Closed G is allowed.** "∂G ⊆ F×1" is vacuous when ∂G = ∅. The final step, *"Assume then p|G is locally homeomorphic, but not globally … path l in G with end points q₁ and q₂ such that p(q₁) = p(q₂) …"* (pp. 66–67), works verbatim for closed G.

One caveat: the general case is a sketch (*"by similar arguments as in (a) and (b) … we prove (a) and (b) below"*). That is acceptable as a citation, but say so.

**"Homeomorphic on each component" means a homeomorphism onto its image, not onto F.** Waldhausen's own usage shows this: *"locally homeomorphic, but not globally on each component … This means there is a path l in G with end points q₁ and q₂ such that p(q₁) = p(q₂)"*. So "globally homeomorphic" means injective. For bounded G the image is a proper subsurface. The doc's reading is right.

**The invariance-of-domain step is correct but omits one line.**
- One needs G′ ⊂ int M. This holds because each stage of the deformation is a homeomorphism of M, and homeomorphisms preserve int M.
- Hence p(G′) avoids nothing, and p|G′: G′ → M_i is an injective map between closed 2-manifolds (M_i is closed).
- Its image is open (invariance of domain) and compact, and M_i is connected, so it is onto.
- A continuous bijection from a compact space to a Hausdorff space is a homeomorphism.
- So s := pr₂ ∘ (p|G′)⁻¹ is continuous, with values in (−1, 1).

If F had boundary, the same argument would yield a contradiction, so no closed incompressible G exists there. That is consistent, and does not affect us.

**Fix.**
- Add "G′ ⊂ int M because the deformation is through homeomorphisms of M".
- State that F = M_i is closed, connected and orientable.
- Transport everything through Ψ_i, and note that Waldhausen's I = [0, 1].
- For (c), you need s to be PL. That holds if the end map of Waldhausen's deformation is a PL homeomorphism, which is the meaning of "isotopy" in his PL category [standard, unverified here; his definition on p. 57 only says "a map H: X×I → Y … h_τ … a homeomorphism"].

## Issue 6 — Lemma 3(c): the flattening is a topological ambient isotopy, not a PL one. Severity: MINOR (the "standard fact" is false; the theorem does not need PL)

On the fiber over x, the map that fixes ±1 and sends s(x) to (1−t)s(x) is, for −1 ≤ y ≤ s(x):

y ↦ −1 + (y+1)·(1+(1−t)s(x))/(1+s(x)).

Even if s is PL, this is a rational function in (s(x), y). On a simplex where s is linear, it is not linear in (x, y). So Θ_t is not PL, and (x, y, t) ↦ (Θ_t, t) is not PL either. The listed fact "Fiberwise PL flattening is a PL ambient isotopy" is **false as formulated**.

**What is true.**
- Θ is continuous, because 1 ± s ≥ 1 − max|s| > 0 on compact M_i.
- Each Θ_t is a continuous, fiberwise increasing bijection of the compact space U_i, hence a homeomorphism.
- Θ_0 = id, and Θ_t = id on ∂U_i = M_i×{±1}.

So (c) is a valid **topological** ambient isotopy.

**Fix (choose one).**
- (i) Claim only a topological ambient isotopy. Nothing downstream needs PL. Delete the false standard fact.
- (ii) A PL route that uses Waldhausen's own Note (p. 58): *"if the surfaces F and G in M are parallel, then they are isotopic by an isotopy which is constant on ∂M. (Here the phrase surfaces in M, rather than surfaces in M or ∂M is essential)."*
  - Pick c with max(0, max s) < c < 1.
  - G′ and M_i×c are disjoint surfaces in M.
  - Triangulate M_i so that s is linear on simplices. The staircase triangulation of each prism σ×[s, c] then gives a PL embedding of G′×I onto {s ≤ y ≤ c}, so G′ is parallel to M_i×c.
  - Likewise, M_i×0 is parallel to M_i×c.
  - Compose the two isotopies. This requires s to be PL (#5).

## Issue 7 — Lemma 3(d): extension by the identity is correct. Severity: NONE

- U_i is compact, hence closed in R³.
- Its manifold boundary equals its frontier in R³ [invariance of domain; standard, unverified here].
- Each stage fixes ∂U_i pointwise. Waldhausen's "constant on ∂M" means pointwise, and (c) fixes M_i×{±1}.
- Pasting over the closed cover U_i×I ∪ (R³ − int U_i)×I gives a continuous family of bijections, each with continuous inverse obtained the same way.
- Isotopies of subspaces are ambient by definition (p. 57): *"(b) of subspaces Z₁, Z₂ in X is an isotopy of the identity map on X, such that h₁(Z₁) = Z₂"*.

## Issue 8 — Theorem: the r-set conclusion is not proved, and "r-set" is undefined. Severity: MAJOR (gap; easy to close)

The proof says only that the end map *"takes bounded complementary regions to bounded complementary regions"*. That is not enough.

With several shells, the r-set is a **particular** union of bounded complementary components. For nested shells A ⊃ B, it is the shell-with-cavity between A and B, not the inside of A and not the inside of B. A map that merely sends bounded regions to bounded regions could in principle exchange them.

**Fix.**
1. Define the r-set. For example: the closure of the union of the components of R³ − ∪G_i at odd depth. Depth is measured in the adjacency tree, whose vertices are the components and whose edges are the shells; each shell separates R³ into two pieces [Jordan–Brouwer; standard, unverified here]. The tree is rooted at the unbounded component. Equivalently, it is the unique compact regular closed set with topological boundary exactly ∪G_i. If the B-rep instead defines the r-set by shell orientation, state that definition.
2. Prove it is preserved. Φ₁ is a homeomorphism of R³ with Φ₁(∪G_i) = ∪L_i. It therefore maps complementary components bijectively, preserves adjacency across each shell (Φ₁(G_i) = L_i), and maps the unbounded component to the unbounded one, because Φ₁ has compact support. Hence it preserves depth parity, so Φ₁(r-set of h) = r-set of φ.
3. If orientation is used instead: since h|K_i ≃ φ_i in U_i, the two shells carry the same class in H₂(U_i), so the induced orientations agree, and Φ₁ respects outward sides.

The simultaneous isotopy itself is fine. The U_j are pairwise disjoint and compact, and G_j ⊂ int U_j is disjoint from U_i for i ≠ j, so Φ^i never moves G_j. Paste Φ^i on U_i with the identity elsewhere. "Any two images are ambient isotopic" then follows by composing one isotopy with the inverse of the other.

## Issue 9 — Theorem: missing structural hypotheses. Severity: MINOR

**What is needed and not stated:**
- **K = ⊔ K_i, a disjoint union of subcomplexes.** "Each shell K_i is a closed, connected surface" does not exclude shells that share a vertex or an edge (non-manifold B-reps). Lemma 2′ (C(σ) inside one shell) and the disjoint collars both need this.
- **Each M_i is closed, orientable and not S².** This is automatic from M_i ≅ |K_i| and "genus ≥ 1", but write it, since it is Prop. 3.1's hypothesis on F.
- **"The carrier condition" and "the collar condition"** must be stated in the theorem, not by name: for every σ, and with Ψ_i(φ_i(|K_i|)) = M_i×0.

**What is not needed, and the doc rightly does not assume:**
- **G ⊂ int U_i.** It is derived in Lemma 2′ from "the zones of K_i lie in int U_i".
- **A PL structure on the zones.** Lemma 2 uses only their homotopy groups.
- **Closed zones.**
- **Connectedness of the zones.** π_0 is already in the carrier hypothesis.

## Issue 10 — The PL structure on |K| is never specified. Severity: MINOR

"PL embedding h" presupposes that |K| is a polyhedron. A regular CW complex whose closed cells are only topological balls has no PL structure given in advance.

**Fix.** Declare the PL structure to be that of the order complex of the face poset, which is homeomorphic to |K| for a regular CW complex [standard, unverified here]. In dimension 2 the choice does not matter, since triangulations of surfaces are PL-equivalent [standard, unverified here].

Also note the scope: the theorem covers **PL** realizations only. Piecewise-smooth B-rep realizations need a triangulation step [standard, unverified here] before it applies.

## Issue 11 — The remark "不可压缩性由'包含是同伦等价'直接得到，不再需要 Kneser 不等式". Severity: MINOR (overclaim)

This sentence does not appear in proof_v0.md, so it was reviewed as the claim was supplied.

**What is right.** In the genus ≥ 1 set-level argument, incompressibility follows from π₁-injectivity of G ↪ U_i. Lemma 2′ supplies that, and no degree or genus inequality of Kneser type is used.

**What is overstated:**
1. **"直接" hides inputs.** The step needs:
   - G is not a sphere;
   - G is connected, proper and two-sided;
   - G is PL in U_i's structure (#4).

   The real content sits upstream, in the carrier hypothesis and in φ_i being *exactly* a level of a PL product collar. If the reference surface is only near a level, π₁-injectivity is no longer free. The Kneser route needed the same two inputs (the homology class came from the same homotopy), so the trade is "same hypotheses, different last step", not a reduction in hypotheses.
2. **Citing Lemma 1.1.3 imports the loop theorem**, which is used only for the converse. Either drop the citation and argue from the definition (#4), or do not present the step as elementary while citing the loop theorem.
3. **Kneser-type facts are not removed from the project.** The S² case and the embedding-level upgrade (math_audit #10, #11, which cite Kneser for degree-1 self-maps of S²) still need them.
4. **The deep input is unchanged.** Prop. 3.1 remains, as a sketched induction that itself uses irreducibility of F×I (*"it bounds a ball E in M, since M is irreducible"*, p. 66).

**Fix.** Reword: "In the genus ≥ 1 case, π₁-injectivity, and hence incompressibility, follows from Lemma 2′ and Waldhausen's definition. The Kneser inequality is not used in this step. It is still needed for the S² case and the embedding-level statement."

---

## Corrected skeleton (minimal changes)

- **Setting.**
  - K = ⊔K_i is a finite regular CW complex, with τ ≤ σ :⇔ τ ⊆ σ̄.
  - The PL structure is that of the face-poset order complex.
  - Each K_i is a closed connected surface.
- **Lemma 2.**
  - Hypothesis: C(v) path-connected for every vertex v, and π_k(C(σ), x) = 0 for every k-cell σ (k ≥ 1) and every x.
  - Conclusion unchanged.
- **Lemma 2′.**
  - Ψ_i: U_i → M_i×[−1,1] is a PL homeomorphism with Ψ_i(L_i) = M_i×0, where L_i = φ_i(|K_i|).
  - φ_i is carried, and the zones of K_i lie in int U_i.
  - Proof unchanged.
- **Lemma 3.**
  - (a) Argue from the definition (#4).
  - (b) Add G′ ⊂ int M (#5).
  - (c) Either claim a topological isotopy, or use the PL route through parallel surfaces (#6).
- **Theorem.**
  - Define the r-set and add the depth-parity argument (#8).
  - Add K = ⊔K_i (#9).
  - Remove "Fiberwise PL flattening is a PL ambient isotopy" from the standard facts, or replace it with #6(ii).
  - Add "a PL-embedded surface in a PL 3-manifold is a PL submanifold" and "Jordan–Brouwer" to the standard facts.
