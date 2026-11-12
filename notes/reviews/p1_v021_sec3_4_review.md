# Referee report: p1 v0.21, Sections 2–3 and Lemma 4.1

Scope: `paper/sec_setting.tex` (definitions), `paper/sec_uniqueness.tex` (carrier condition, weakened collar
condition, Lemmas 3.1–3.3, Theorem 3.4), `paper/sec_collar.tex` Lemma 4.1 (a), (a′), (b). I did not have access
to Waldhausen 1968, Moise, Durfee, Chazal–Lieutier or CCSL09. Where a finding depends on the exact wording of
a source, I say so.

## Summary

The logical skeleton is sound. The weakened collar condition (the reference is a homotopy-equivalent surface in
int U_i, not necessarily a level) is enough for Theorem 3.4: Lemma 3.2 uses only that the inclusion is a
homotopy equivalence, and Lemma 3.3 is a correct use of the standard fact that a closed incompressible
non-sphere surface in F×I is isotopic to a level. The π1/Hopfian/Whitehead argument in Lemma 4.1(b) is correct.
The planned route for (a′) works and is short. I found no fatal error. There is one major honesty and dependency
issue: (b) also depends on (a), which is only outlined, but the draft note says (b) depends only on (a′). There
are also several minor gaps: what Waldhausen's isotopy fixes, the category of the final isotopy, an incorrect
"alternatively" sentence, the PL structure of a non-regular K, and basepoint and connectedness conventions.

## Findings

### 1. (Major) Lemma 4.1(b) depends on (a) as well as (a′), and (a) is only outlined
The first bullet of (b) uses (a): "the composite M ↪ U ↪ N̄_r(M) is a homotopy equivalence". The route for
(a′) also starts from (a). The proof of (a) is marked "in outline", and two of its steps (applying Prop. 3.4 to
d_M, and the gluing) are pushed to a repository note. The draft note under (a′), the intro (l. 47, l. 130) and
the abstract all say the reduction is conditional on (a′) only, "a PL-taming step". That understates what is
missing.
*Fix:* Say "Lemma 4.1(b) is conditional on (a) and (a′)", or finish (a) in the paper. For (a), the cleaner citation
is probably the isotopy lemma for the distance function to an arbitrary compact set, already in
CCSL09dcg (Grove's isotopy lemma; please check its number there). This avoids applying Chazal–Lieutier Prop. 3.4,
which is stated for the complement of a bounded open set, "on both sides". Write out the gluing explicitly: the
Durfee homeomorphism sends ∂N̄_δ to the two boundary components M×{±1} of the regular neighbourhood. The
collar {δ ≤ d ≤ r} ≅ d^{-1}(δ)×[δ,r] then attaches to these, and M×[-1,1] ∪ (M×{±1})×[0,1] ≅ M×[-1,1], with M
still at level 0. Until (a) is done, (a) and (a′) should not sit in a `lemma` environment as asserted
statements. Mark them as claims, or split the lemma so that only (b) is a lemma, with (a) and (a′) as stated
hypotheses.

### 2. (Minor, but must be checked against the source) What Waldhausen's Prop. 3.1 isotopy fixes, and whether it is ambient
Lemma 3.3(b) says Prop. 3.1 gives "an isotopy, constant on ∂U". Lemma 3.3 and Theorem 3.4 need an *ambient*
isotopy of U fixed pointwise on ∂U, so that it extends by the identity. Please confirm two things in the paper.
(i) Waldhausen's "isotopy" is ambient (his §0/§1 conventions), or else invoke PL isotopy extension. (ii) The
isotopy is constant on all of ∂(F×I) = F×0 ∪ F×1. In the boundary-relative statement the isotopy may be
constant only on F×0 (or on F×0 ∪ ∂F×I), and F×1 may only be preserved setwise.
*Fix if (ii) fails:* G is compact in int U, so apply Prop. 3.1 in U′ = Ψ^{-1}(M×[−1+ε, 1−ε]) ⊃ G. The resulting
ambient isotopy φ_t of U′ restricts to isotopies of the two boundary levels. Taper it across the collars
M×[1−ε, 1] (and likewise at the bottom) by (x, 1−ε+u) ↦ (φ_{t(1−u/ε)}(x), 1−ε+u). The result is fixed on ∂U. This
standard trick costs two lines.
Also check the page range: the paper cites pp. 65–67, while the review request says pp. 58, 65–66. Check the
section label "[§0]" too.

### 3. (Minor) The form of Prop. 3.1's conclusion
The paper says the conclusion is "p|G′ is a homeomorphism onto its image". If Waldhausen's wording is instead
"p|G′ is a covering" (or "G′ is horizontal"), add one line. An embedded closed surface transverse to the
I-fibres that covers F with degree k has k sheets ordered by height, so it is disconnected unless k = 1. G is
connected (finding 7), so k = 1. The invariance-of-domain step that follows is correct. s takes values in
(−1, 1) because an ambient isotopy fixed on ∂U preserves int U. Say this explicitly.

### 4. (Minor) The "alternatively" sentence in Lemma 3.3(c) is wrong as stated
"The region between G′ and the level is a product region". If s takes the value 0 or changes sign, G′ meets
M×{0}, so "the region between" is not defined.
*Fix:* Compare G′ with a level M×{c} where c < min s. The region {c ≤ y ≤ s(x)} is a product. Then move
M×{c} to M×{0}. Or simply delete the sentence; the fibrewise flattening is enough.

### 5. (Minor) The category of the final isotopy
Step (c) is only a topological ambient isotopy: the fibrewise maps are rational in s, not PL. The paper says
so in (c), but Theorem 3.4 says "ambient isotopic" without a category, and the abstract and intro do the same.
*Fix:* State "topologically ambient isotopic" in Theorem 3.4. If PL is wanted, cite a PL parallelism result for
disjoint incompressible surfaces that cobound a product in the PL category. Topological is fully adequate for
the stated conclusions about images and solids.

### 6. (Minor) PL structure on |K| when K is not regular; a simpler definition of realization
sec_setting.tex l. 13 says "|K| carries the PL structure of the order complex of its face poset". This is false
for non-regular K: a closed edge has face poset {v < e}, whose order complex is an interval, not a circle. Yet a
realization of the *original* (non-regular) B-rep is required to be a PL embedding. Also, whether h is PL depends
on the chosen PL structure, not just on its PL-homeomorphism class.
*Fix (recommended):* Define a realization as a topological embedding h with h(int σ) ⊆ Z(σ) whose image is a
polyhedron. A compact 2-polyhedron that is a topological 2-manifold is a PL surface, since vertex links must be
circles. Lemma 3.2 uses only continuity of h, and Lemma 3.3 uses only that G is a closed PL surface. This
removes every dependence on the PL structure of |K| and makes the subdivision remark trivially correct.
Otherwise, say that the PL structure is that of a fixed regular subdivision, and that the theorem holds for
any such choice.

### 7. (Minor) Connectedness and basepoint conventions
- Carrier condition: "π_k(C(σ)) = 0" should say "at every basepoint". Path-connectedness for k ≥ 1 is not
  needed, since the image of ∂(σ̄×I) is connected. This is fine as written once basepoints are fixed.
- Subdivision rule (l. 11–12): new vertices inside f or e get the carrier Z(f) or Z(e), and the carrier condition
  for vertices then needs these zones to be path-connected. Nothing in Definition 2.1 guarantees this:
  N_{τ_e}(γ_e) need not meet N_{τ_f}(P_f) unless dev_e < τ_e + τ_f. Add "Z(f) (resp. Z(e)) path-connected"
  next to "π1(Z(f)) = 0", or say "contractible" throughout.
- Lemma 3.3: state that G is connected. This follows from G ≃ U ≃ M connected, since a homotopy equivalence
  gives a bijection on π0, but the proof uses it (that G is not a sphere, and the degree-one step).
- Lemma 3.2: say "closed PL surface". Lemma 3.3 needs PL, and it holds because h is a PL embedding.

### 8. (Minor) The collar-condition remarks on M_i are right but terse
- *Connected:* M_i ≃ U_i ≃ φ_i(|K_i|) ≅ |K_i|. Correct.
- *Orientable:* U_i is a compact codimension-0 submanifold of R^3, hence orientable, and M×I orientable ⇔ M
  orientable. Correct.
- *Not a sphere:* this follows because π1(M_i) ≅ π1(|K_i|) ≠ 1, and every closed surface other than S^2 has
  nontrivial π1. Write that clause.
- Also say that M_i is a closed *PL* surface, since Ψ_i is a PL homeomorphism.
- Note that "genus ≥ 1" silently means orientable genus. This is harmless, since a realization in R^3 forces
  orientability, but say it.

### 9. (Minor) Lemma 4.1 statement: notation and per-shell constants
In (b), "M = φ(|K_i|)" is the reference surface in R^3, but the next clause writes N̄_r(M_i), and in Section 3
M_i is the abstract factor of U_i. Make d and r per shell (d_i < r_i < wfs(M_i)), apply (a) and (a′) shell by
shell, and say "with U_i = U and abstract factor M_i := φ_i(|K_i|)".

### 10. (Minor) The hypothesis is understated in the abstract and intro
p1.tex l. 45–46 and sec_intro.tex l. 36–37 describe the collar condition as "a product collar containing its
zones and a (carried) reference surface". They omit the requirement that the inclusion of the reference be a
homotopy equivalence, and that requirement is essential. A reference surface bounding a small ball inside the
collar would satisfy the stated wording. Add "whose inclusion is a homotopy equivalence" or "that is
π1-isomorphic to the collar". The section title "The collar condition is computable" overclaims while (a) and
(a′) are open, and while L is certified only in the qualified sense (double precision, tolerance, cut-off R).
Something like "Reducing the collar condition to a distance bound" is safer.

### 11. (Minor, outside the strict scope, but it bears on applying Lemma 4.1) What L certifies
§4.3 certifies "no critical value in (c·tol, L)". Lemma 4.1 needs r < wfs, that is, no critical value in (0, r].
The interval (0, c·tol] is not covered by the computation as described. Either argue that it is covered (for a
polyhedron, Corollary 4.3 gives a positive λ, so tiny distances are handled by the cone lemma if the near-M
boxes are certified down to 0), or state the gap.

### 12. (Minor) Standard-facts list
Moise is cited only through `\unverified` and has no bibliography entry. Add it, and check whether the 3D
Hauptvermutung is ch. 35 or ch. 36 of *Geometric Topology in Dimensions 2 and 3*, and that it covers
noncompact 3-manifolds; Moise's theorem does. Add to the "used without checking" lists the isotopy extension
theorem (or ambientness of Waldhausen's isotopy), orientability of compact codimension-0 submanifolds of R^3,
and irreducibility of F×I. The last is marked `\unverified` and is correct for F ≠ S^2, RP^2; Hempel, Lemma 10.2
or the surrounding text, is the usual reference.

## Answers to the specific questions

1. **The weakened collar condition suffices.** The reference enters only through Lemma 3.2, which needs just a
   homotopy equivalence. Lemma 3.3 is correctly stated and proved for any closed PL surface G ⊂ int U whose
   inclusion is a homotopy equivalence:
   - The incompressibility argument is correct and needs only π1-injectivity.
   - Waldhausen's conventions are met: G is two-sided because it is orientable in an orientable manifold, it is
     disjoint from ∂U, ∂G = ∅ so "∂G ⊂ F×1" holds vacuously, and F = M is orientable and not a sphere.
   - What remains is to confirm the two points in findings 2 and 3 against the text (ambient, fixed on all of
     ∂U, homeomorphism or covering).
   - The claim "M_i connected, orientable, not a sphere" is justified, with the one-line additions in finding 8.
2. **Lemma 3.2: yes.** The carrier lemma gives H(σ̄×I) ⊆ C(σ) = Z(σ) ⊆ int U_i, so h ≃ φ_i as maps into U_i.
   The rest is correct.
3. **Theorem 3.4 is correct.** The simultaneous isotopy is well defined by the pasting lemma, since the U_i are
   disjoint compact sets and each isotopy is fixed on ∂U_i. Φ(G_j) is the level because the other isotopies are
   the identity on U_j. Depth is preserved because a homeomorphism of R^3 permutes the complementary
   components and preserves relative compactness, so bounded goes to bounded. Item 2 follows via
   Φ′_t^{-1}∘Φ_t. The only caveat is the category (finding 5).
4. **Lemma 4.1(b) is correct.**
   - Surjectivity on π1 follows from the composite being an isomorphism.
   - The Hopfian step is valid: composing with an abstract isomorphism gives a surjective endomorphism of a
     Hopfian group, which is therefore injective.
   - π1(M) → π1(U) is then an isomorphism, and Whitehead applies to aspherical CW complexes (compact
     polyhedra).
   - The hypotheses used are: U connected (from U ≅ M×I), genus ≥ 1 (needed for asphericity, and the argument
     fails for S^2), and (a) in addition to (a′) (finding 1).
5. **(a′): the marking is honest. (a): the marking is honest locally but misreported in the dependency note and
   abstract (finding 1).** The planned route for (a′) works and is nearly complete:
   - (i) By (a), int N̄_r(M) (manifold interior = topological interior, by invariance of domain) is homeomorphic
     to M×(−1,1).
   - (ii) As an open subset of R^3 it is a PL 3-manifold. By Moise (the 3D Hauptvermutung, including the
     noncompact case) there is a PL homeomorphism g: M×(−1,1) → int N̄_r(M).
   - (iii) N̄_d(M) = {dist ≤ d} ⊂ {dist < r} ⊆ int N̄_r(M) is compact, so g^{-1}(N̄_d(M)) ⊂ M×(−a, a) for some
     a < 1.
   - (iv) Take U = g(M×[−b, b]) with a < b < 1. Then U is a compact PL submanifold, N̄_d ⊂ int U,
     U ⊂ int N̄_r, and U ≅_PL M×[−1,1].
   - g need not send M to level 0. That is exactly why (b) uses the π1 argument.
   - What has to be proved or cited: (a) itself, the precise Moise statement, and steps (iii)–(iv), which are a
     few lines.
6. **Overclaims and hidden assumptions:**
   - Finding 1: the dependency on (a) is unreported.
   - Finding 10: the abstract and intro omit the homotopy-equivalence hypothesis, and the section title
     overclaims.
   - Finding 6: a PL structure is assumed on non-regular |K|.
   - Finding 7: path-connectedness of the zones that carry new vertices.
   - Finding 11: the (0, c·tol] gap in the certified bound.

## Verdict

Section 3 (Theorem 3.4 with the weakened collar condition) is **correct, subject to minor revisions**. Before
calling it proved, confirm against Waldhausen's text that the Prop. 3.1 isotopy is ambient and fixed on all of
∂U, or add the tapering fix. Also state the category of the isotopy and fix the "alternatively" sentence.
Lemma 4.1(b) is **correct as a conditional statement**, but it is conditional on (a) and (a′), not on (a′)
alone. The dependency notes in Section 4, the intro and the abstract need **major revision** to say so. The
route for (a′) works and should take under half a page once Moise is cited properly. (a) still needs to be
written out in full. No fatal errors were found.
