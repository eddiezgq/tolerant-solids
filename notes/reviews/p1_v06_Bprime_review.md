# Referee report: Proposition 5.3 ("Curved, transversal") and its proof (Appendix B), p1 v0.6

Reviewer: independent (geometric topology / computational geometry), 2026-11-12.
Scope: the statement of Proposition `prop:Bprime` in `paper/sec_existence.tex` and its proof in
`paper/sec_proofBprime.tex`. Background read: `sec_setting.tex` (zones, realization, PL convention), Appendix A
(`sec_proof51.tex`, PL step), the earlier review `notes/reviews/lemma0_v03_Bprime_review.md`, and the table and remark in
`sec_experiments.tex` only where they quote this proposition. No file other than this report was changed.

**Summary.** No fatal error. The strategy (take the re-trimmed surface itself as the model of |K|, build a piecewise-C¹
homeomorphism h₀ by curved triangles, show it is bi-Lipschitz, replace it by a fine secant map) is sound, and the
margin and secant steps are correct. The earlier review's main points (A1, A2) have been taken in. What remains:
two hypotheses that the proof uses are not stated (finding 1: what "isomorphic as a B-rep complex" means; finding 2:
injectivity and domain of the face parametrizations), and the step that makes h₀ well defined on shared edges rests on
a citation that, as cited, does not obviously give what is needed (finding 3). All three have short, concrete fixes.
The rest are minor.

---

## 1. Statement

**1.1 (major). C is not precise: "a cell structure on Σ isomorphic to K as a B-rep complex" is not defined.**
- The paper never defines a B-rep complex or its isomorphisms. `sec_setting.tex` says K is a finite CW complex, but a
  face with inner wires is not an open 2-cell, so such a K is not a CW complex at all (the setting calls it "not
  regular", which is a different defect).
- The added clause "seams are glued to themselves and closed edges have one vertex" is incidence information. For a
  non-regular complex it does not determine the complex (e.g. the boundary word of a cylinder face, e₁ s e₂⁻¹ s⁻¹,
  versus e₁ s e₂⁻¹ s, have the same incidences).
- The proof uses exactly one thing: a homeomorphism φ: |K| → Σ with φ(int σ) = int σ̃ for every cell (it pulls T back
  to |K| and composes S with h₀⁻¹∘φ).
- **Fix.** State C as: "there is a homeomorphism φ: |K| → Σ that maps each open cell σ of K onto the corresponding open
  cell σ̃ of Σ, where the open cells of Σ are the points c_v, the curves γ̃_e minus their end points, and the patches
  P̃_f minus their boundary curves." This covers seams, closed edges, faces with inner wires, and faces whose boundary
  touches itself at a vertex, with no further words. It also implies that Σ is a disjoint union of closed surfaces and
  that distinct patches meet only along common edges and vertices, which the proof uses for injectivity.
- Suggest also fixing the sentence in `sec_setting.tex` ("K is a finite CW complex") to "a finite cell-like complex
  whose faces are compact surfaces", or similar, so that the faces with holes the paper wants to cover are in scope.
  (Outside the strict scope of this review, but 1.1 depends on it.)

**1.2 (major). The face parametrizations must be injective (up to the seam periods) and C² on a neighbourhood of the
closed region. Neither is stated, and both are used.**
- "h₀ is injective by C" requires that X_f, restricted to the closed parameter region D_f, is injective except for the
  identification of the two copies of each seam. C alone does not give it: if D_f is an annulus of width 4π on a
  cylinder of period 2π, X_f covers P̃_f twice, C can still hold for the set P̃_f, and h₀ is not injective. R speaks of
  "the preimages", which silently presupposes a fundamental domain.
- "h₀ is C¹ up to the boundary on each closed triangle" requires X_f to be C² (or at least C¹ with injective
  differential) on an open set containing D_f. Re-trimmed patches usually extend past the original patch, so this is a
  real requirement on the extended surface.
- Also say explicitly that X_f is periodic in the seam directions (X_f(u + P) = X_f(u) for the period vector P). The
  seam bullet of the proof ("in the periodic parameter domain the two triangles are adjacent") needs this, and so does
  the agreement of the two triangle maps on a seam edge (see 2.2).
- **Fix.** Replace the first sentence by: "Each S_f has a C² regular parametrization X_f: U_f → ℝ³, U_f open in ℝ² or
  in a quotient ℝ²/Λ_f by a lattice of periods; there is a compact region D_f ⊂ U_f with X_f(D_f) = P̃_f and X_f
  injective on D_f (in the quotient)." With the quotient formulation, "across a seam the region continues
  periodically" becomes automatic, and faces on periodic surfaces without a seam edge (allowed by some kernels) are also
  covered.
- Singular parametrizations (sphere poles, cone apices, degenerate edges) are excluded by "regular". That is fine, but
  say it, since spherical faces are common and the reader may expect them to be covered.

**1.3 (minor). R: the corner angles must be in (0, 2π), and the boundary curves must be simple.**
- "Positive interior angles (no cusps)" admits the angle 2π, an inward cusp, at which no shape-regular triangulation
  with a corner vertex exists. Write "interior angles in (0, 2π)".
- "C² regular curves" can self-intersect. Write "the boundary of D_f is a finite disjoint union of closed curves, each
  piecewise C² regular and simple, with corners only at preimages of the c_v".
- At a vertex where a face's boundary passes twice (pinched face) or across a seam, one face has several corners. Say
  that the angle condition is per corner of D_f, not per face.

**1.4 (minor). T should hold up to the end points of each edge, and its vertex clause should be phrased per corner.**
- Bi-Lipschitz along an edge needs a lower bound on the angle between S_f and S_g that is uniform up to the end points;
  with T "at every point of the closed curve γ̃_e" this follows by compactness. As written, "along every non-seam
  edge" could be read as the open edge, and the angle could tend to 0 at c_v. The vertex clause of T does not repair
  this by itself (it controls the tangent cone at c_v, not the approach along the edge, though in fact the two are
  linked by C¹-up-to-the-corner; see 3.4).
- "The union of the tangent sectors of the incident patches": at a seam vertex one patch contributes two sectors, and
  for a reflex corner the "tangent sector spanned by two rays" is ambiguous. Define the tangent sector of a corner as
  dX_f applied to the tangent sector of D_f at that corner. Then "positive opening angle" follows from R and the
  regularity of X_f and need not be assumed in T.

**1.5 (minor, optional strengthening). The edge clause of T is stronger than the proof needs.**
- The proof uses T along edges only to get two *distinct* half-planes in the tangent cone. If S_f and S_g are tangent
  along the edge and the patches continue across it (interior dihedral angle π, a G¹ edge), the tangent cone is a plane,
  which is equally good for bi-Lipschitz. Only a fold (angle 0) is harmful. The regularity of γ̃_e is assumed in R, so
  transversality is not needed for it either.
- So T along edges can be weakened to "the inward tangent half-planes of the two patches are distinct at every point
  of γ̃_e". This would make the proposition applicable in principle to filleted models and to faces split on one
  surface, which the table currently marks "not applicable (tangent faces)". Whether a re-trimmed model with small
  margins exists for them is a separate, computational question. Optional; at least note in a remark that the edge
  part of T is only used through "no fold".

**1.6 (minor). "Σ bounds a solid" is redundant or vague.**
- With Definition `def:solid`, any finite family of pairwise disjoint closed surfaces bounds a solid, and C (as fixed
  in 1.1) already makes Σ such a family. The proof never uses the hypothesis.
- If something stronger is meant (consistent orientation, the same solid as the original model), it is not used either.
- **Fix.** Delete it, or move it to a remark ("Σ then bounds a solid in the sense of Definition 2.5").

**1.7 (correct). Closed cells in B1–B3.** B2 and B3 are stated for the closed curve γ̃_e and the closed patch P̃_f, so
h₀(σ̄) ⊆ Z(σ) is immediate for every cell, including the end points. Augmentation is not needed for the inclusion
itself, only to make B2/B3 satisfiable near the vertices (as the previous review noted).

---

## 2. Construction of the curved triangulation and of h₀

**2.1 (major). The Lenoir citation does not clearly give the property the proof needs, and that property is what makes
h₀ well defined.**
- The proof needs, for a triangle with vertices a₁, a₂ on a boundary curve and a₃ inside, a map F from the reference
  triangle such that:
  (a) on the curved side it is exactly s ↦ ĉ(t₀ + s(t₁ − t₀)), for a *prescribed* parametrization ĉ coming from one
  3D parametrization of γ̃_e, so that the two faces at a shared edge give the same map into ℝ³;
  (b) it is affine on the two straight sides;
  (c) it is C¹ up to the boundary, including at a₃ and at the corners;
  (d) it is a diffeomorphism onto the curved triangle for fine meshes.
- (a) is the crux of "the two adjacent triangle maps agree on a shared edge". To this referee's recollection (not
  rechecked against the original), Lenoir's transformation is constructed for one domain from a boundary representation
  relative to the chord, and the parametrization it induces on the curved side is determined by the construction, not
  prescribed. If so, two faces using Lenoir's map in their own parameter planes would induce *different* maps of the
  shared edge into ℝ³, and h₀ would not be well defined. The bibliography and the proof already flag the citation as
  unverified; this is the specific point to check.
- (c) is not automatic from (a)+(b): Zlámal's classical blending, F = affine + (λ₁ + λ₂) ψ(λ₂/(λ₁ + λ₂)), satisfies (a),
  (b) and (d) but is only Lipschitz at a₃: its derivative there, ψ(s) + (1 − s)ψ′(s), depends on the direction s of
  approach.
- **Fix (recommended): replace the citation by a short self-contained lemma.** Let ĉ: [t₀, t₁] → U_f be the pulled-back
  C² curve, a₁ = ĉ(t₀), a₂ = ĉ(t₁), ψ(s) = ĉ(t₀ + s(t₁ − t₀)) − ((1 − s)a₁ + s a₂), and in barycentric coordinates
  (λ₁, λ₂, λ₃), μ = λ₁ + λ₂,

      F(λ) = λ₁a₁ + λ₂a₂ + λ₃a₃ + μ² ψ(λ₂/μ)   (and F = a₃ at μ = 0).

  Then:
  - on λ₃ = 0 (μ = 1) F reproduces ĉ exactly, with s = λ₂: property (a);
  - on λ₂ = 0 and λ₁ = 0, ψ(0) = ψ(1) = 0, so F is affine: (b);
  - for μ > 0, F is C¹ (C² if ĉ is). Near a₃, the correction is O(μ²) and its derivative is
    2μψ dμ + μ²ψ′ ds with |ds| = O(1/μ), so it is O(μ) → 0: F is C¹ at a₃ with DF(a₃) affine: (c);
  - with h the mesh size, |ψ|, |ψ′|, |ψ″| = O(h²) because ĉ is C² and the parameter speed is O(h). So
    DF = A + O(h²) = A(I + O(h)) when the chord triangle is shape-regular (‖A⁻¹‖ = O(1/h)), and
    |F(x) − F(y) − A(x − y)| ≤ C h²|x − y| < |A(x − y)| on the convex reference triangle. So F is injective with
    invertible differential for small h, and by a degree argument its image is the curved triangle: (d).

  This is half a page, removes the `\unverified` marker for this appendix, and is uniform at the corners of D_f, since
  ĉ is C² up to its end points. The same lemma serves Appendix A, where the same citation is used for Q_f.

**2.2 (correct, given 1.2 and 2.1). Agreement on shared edges.**
- *Interior straight edges of one face:* both adjacent maps are affine on the edge with the same end points, hence
  equal as maps of the abstract edge. Correct.
- *Edges on γ̃_e between faces f ≠ g:* both use s ↦ X_f(ĉ_f(t₀ + s(t₁ − t₀))) = γ̃_e(t₀ + s(t₁ − t₀)) =
  X_g(ĉ_g(…)). Correct provided (i) the T-vertices on γ̃_e are chosen once in 3D and pulled back to both faces (the
  proof says so), and (ii) the triangle maps have property 2.1(a).
- *Seam edges:* the triangles on the two sides use ĉ and ĉ + P with the same parameter, and X_f(ĉ(t) + P) =
  X_f(ĉ(t)). Correct once periodicity of X_f is stated (1.2). The seam must be a union of T-edges (it is, since T
  subdivides the cells), so no triangle straddles it.
- *Closed edges:* the one 3D parametrization is periodic; its vertex c_v is a T-vertex. Correct, but see 2.4 on
  simpliciality.

**2.3 (minor). Existence of the curved triangulation: give the construction, because the obvious one fails at corners.**
- A triangle at a corner of D_f whose two sides run along the two boundary arcs would have two curved edges. "At most
  one curved edge" therefore requires at least two triangles at every corner, separated by a straight interior edge
  from the corner. Likewise an "ear" triangle with two consecutive boundary chords must be avoided.
- The boundary vertices are fixed in 3D for both faces at once, so the interior triangulation of each face must not
  add Steiner points on the boundary (or they must be added to both faces).
- **Fix.** Three lines suffice: choose T-vertices on each γ̃_e at 3D spacing ≈ h; in each D_f take the chord polygon
  (simple for small h, by R); triangulate it shape-regularly without boundary Steiner points and with one interior
  vertex near each corner joined to the corner, so that no triangle has two boundary chords; replace each boundary
  chord by its arc. Since the arc deviates from its chord by O(h²) ≪ h·sin θ_min, the curved triangles tile D_f. The
  shape-regularity constant depends on the smallest corner angle, which is positive by R.

**2.4 (minor). T must be a simplicial complex, and the metric on |T| must be specified.**
- A closed edge with one vertex, a seam, or a face that is a thin annulus can produce double edges or loops for a
  coarse choice of vertices. "Fine enough" fixes it, but say "at least three T-vertices on each closed edge and h small
  enough that T is a simplicial complex".
- The proof says "straight reference triangle" without saying which. The parameter-domain chord triangles cannot serve
  as the metric simplices of |T|: a shared edge on γ̃_e has different chord lengths in D_f and D_g, so they do not glue
  isometrically. Use standard (equilateral) simplices, composing F with the affine map from the standard simplex. This
  is the metric in which shape regularity of the *refinements* and the intrinsic length metric of section 3 are meant.

**2.5 (correct). h₀ is C¹ up to the boundary with injective differential on each closed triangle,** given 1.2 and 2.1:
X_f is C² regular on a neighbourhood of D_f and F is a C¹ diffeomorphism onto the curved triangle.

---

## 3. Bi-Lipschitz

**3.1 (minor). Several shells: the intrinsic metric is infinite between shells.**
- |K| has n components. The intrinsic length metric is +∞ between points of different shells, so "Lip(S − h₀) below the
  bi-Lipschitz constant" proves injectivity only within a shell. (The same gap is in Appendix A.)
- **Fix.** Add: "Different shells: h₀ maps them to disjoint compact sets at distance δ > 0; for |S − h₀| < δ/2, S maps
  them to disjoint sets." Or metrize |K| by the intrinsic metric on each shell and a constant (say diam) between shells,
  and note that the per-triangle estimate is applied within shells.

**3.2 (correct). "Injective + locally bi-Lipschitz on a compact space ⇒ bi-Lipschitz",** within a shell, with the
intrinsic metric: the upper bound is global because per-triangle Lipschitz bounds add along paths; the lower bound by
the usual compactness argument (a sequence with ratio → 0 has limits x, y; x ≠ y contradicts injectivity, x = y
contradicts local bi-Lipschitz). The inequality |S(x) − S(y)| ≥ (c − Lip(S − h₀)) d(x, y) is applied in the same
metric. Correct.

**3.3 (correct, minor wording). Inside faces, across interior edges and across seams.** The face map is a
piecewise-C¹ homeomorphism of a planar (or cylindrical) region with invertible differential on each closed piece,
composed with a regular injective X_f. That such a planar map is locally bi-Lipschitz at interior T-vertices needs the
one-line argument that its tangent map is a degree-one, sectorwise orientation-preserving PL map of the plane, hence a
homeomorphism; this is the planar case of the "embedded tangent cone" fact and can be cited as such. At T-vertices
lying on γ̃_e (not vertices of K), the triangle sectors on each side tile the two tangent half-planes, so the
non-seam-edge argument applies there too. Say so in one sentence.

**3.4 (correct, given 1.4). Along non-seam edges.** With transversal tangent planes the two inward tangent half-planes
of the patches lie in different planes, so their angle is in (0, π) and they are distinct. That they are the tangent
half-planes of the patches uses R (each patch lies locally on one side of its C² boundary curve). The lower bound must
be uniform up to the end points (1.4).

**3.5 (correct). At vertices.** The standard fact "C¹-up-to-the-vertex pieces whose tangent sectors form an embedded
disk ⇒ locally bi-Lipschitz" applies: here, unlike the cone apex of Appendix A, h₀ is C¹ up to the vertex on every
closed triangle (2.1(c)), so the blow-up argument (rescale at r_n = max distance to c_v, pass to the tangent cone,
use C¹ convergence on each sector for nearby pairs) goes through. State in the list of standard facts that the pieces
must be C¹ up to the vertex; that is what this proof has and what Appendix A lacked.
- The vertex clause of T is the only hypothesis that is not checked in the experiments (the remark and the table
  footnote say so; that is accurate and not an overclaim).

---

## 4. Secant step and zone margins

**4.1 (correct). The margin.** Closed cells of Σ are compact and contained in the open zones (B1–B3), finitely many,
so m > 0 exists with N_m(σ̄_Σ) ⊆ Z(σ).

**4.2 (correct). S maps closed cells into zones.** T subdivides the cells, so for x ∈ σ̄ the triangle (or T-edge) of x
lies in σ̄ and S(x) is within |S − h₀| < m of h₀(x) ∈ σ̄_Σ. Vertices of K are T-vertices and S(c_v) = c_v ∈ Z(v)
exactly; edges are unions of T-edges on which S interpolates points of γ̃_e. So S(σ̄) ⊆ Z(σ) for vertices, edges and
faces, hence S(int σ) ⊆ Z(σ).

**4.3 (minor). The refinement and the estimate.**
- "Refined if necessary" should mean: refine each simplex of T affinely (e.g. red refinement of the standard simplex),
  not re-triangulate. Then h₀ stays C¹ on each *original* closed triangle, ω(Dh₀, mesh) → 0 on each of finitely many
  triangles, and θ_min does not decrease.
- The estimate is |S − h₀| ≤ mesh · ω(Dh₀, mesh), which is better than C·mesh; either is enough.

**4.4 (minor). S is a PL embedding of |K| with the right cell structure, once the PL convention is fixed.**
- S∘h₀⁻¹∘φ: |K| → ℝ³ is linear on the simplices of φ⁻¹(h₀(T)), which subdivides the cells of K; it is injective
  (3.1/3.2), hence an embedding. Correct.
- `sec_setting.tex` gives |K| "the PL structure of a regular subdivision" without saying which. The proof chooses T.
  Say in the setting that a realization is PL with respect to *some* triangulation of |K| subdividing its cells, and
  note that any two such are related by a cell-preserving PL homeomorphism (dimension 2), so the notion does not depend
  on the choice.

---

## 5. Overclaims and hidden assumptions

**5.1 (minor).** `sec_open.tex` item 2 says "Proposition 5.3 covers them" (seams, closed edges, inner wires). True
after 1.1 and 1.2; until then, the coverage of inner wires and seams rests on undefined notions.

**5.2 (minor).** The final list of "standard facts used without separate checking" should add: injectivity of a
continuous injection of a compact space as an embedding (trivial), the planar degree argument of 3.3, and, if 2.1 is
not adopted, that the cited curved-triangle map reproduces a *prescribed* parametrization (2.1(a)), which is the one
item in the list that is not standard.

**5.3 (no issue).** The checking remark and the table footnote correctly state that the vertex part of T is not
checked numerically and that the PL step is an existence argument, not a computation. No overclaim found there.

---

## Verdict

**Correct in substance; accept after revisions. No fatal error.**

Required (major):
1. Define C as a homeomorphism φ: |K| → Σ carrying open cells to open cells (1.1).
2. State that each X_f is C² regular on a neighbourhood of a compact region D_f, periodic in the seam directions, and
   injective on D_f modulo periods (1.2).
3. Replace the Lenoir citation by the explicit blending map F = affine + μ²ψ(λ₂/μ) and its four-line lemma, or verify
   that Lenoir's map reproduces a prescribed parametrization of the curved side and is C¹ at the opposite vertex (2.1).
   Without one of these, h₀ is not shown to be well defined on shared edges.

Recommended (minor): angles in (0, 2π) and simple boundary curves (1.3); T up to edge end points and per-corner
sectors (1.4); drop "bounds a solid" (1.6); construct the curved triangulation explicitly at corners (2.3); simplicial
T with standard simplices as the metric (2.4); handle several shells (3.1); affine refinement (4.3); fix the PL
convention (4.4). Optional: weaken the edge part of T to "no fold", which would bring G¹ edges into scope (1.5).

---

# Follow-up on v0.7

Read: `sec_setting.tex`, Proposition `prop:Bprime` and its remarks in `sec_existence.tex`, `sec_proofBprime.tex`, the new
`sec_curvedtri.tex` (Lemma C.1), the changed parts of `sec_proof51.tex`, and the places in `sec_open.tex`,
`sec_experiments.tex` and `sec_biblio.tex` that refer to them. No file of the draft was edited.

**Summary.** The three major findings of the first pass are addressed. Lemma C.1 is correct. The weakened T ("no
fold") is enough for the bi-Lipschitz step, G¹ edges included. There is one new major gap, which the quotient
formulation of seams introduced: seams are no longer covered by R or by the triangulation (N1). A second gap is in
Appendix A: Lemma C.1 assumes C² curves, but Appendix A uses it on curves that are only C¹ (N2); a C¹ version of the
lemma holds with the same proof. The rest is wording.

## F. Status of the first-pass findings

| # | Status | Where / comment |
|---|---|---|
| 1.1 C undefined | **fixed**, with a residue | C is now a homeomorphism carrying open cells (prop. clause C); `sec_setting.tex` §Complexes redefines K as a B-rep cell complex. Residue: for a face with a seam, "open face = interior of the face" (setting) and "patch minus its boundary curves" (C) both *contain* the seam, so the open cells are not disjoint. See N1. |
| 1.2 X_f injective, C² near D_f, periodic | **fixed** | Clause P (quotient by a lattice Λ_f, X_f injective on D_f, singular parametrizations excluded). But see N1 for what the quotient does to seams. |
| 1.3 angles (0,2π), simple curves | **fixed** | Clause R. |
| 1.4 T up to end points, per-corner sectors | **fixed**, wording | Clause T. "Inward tangent half-plane ... end points included" is undefined at a corner (there the patch has a sector, not a half-plane). See N3. |
| 1.5 weaken T to no-fold | **done** | Clause T and the first remark after the proposition. Verified in §G below. |
| 1.6 "bounds a solid" | **fixed** | Moved to the remark. |
| 2.1 Lenoir citation | **fixed** | Lemma C.1 (`sec_curvedtri.tex`), used in both appendices. The Lenoir entry is gone from `sec_biblio.tex` and from the list in `sec_open.tex`. Proof checked in §H. |
| 2.2 agreement on shared edges | **fixed** for interior and non-seam edges; **partly** for seams | `sec_proofBprime.tex`, "h₀ agrees on shared edges". The seam case is right once seams are triangulated, which the construction no longer says (N1). |
| 2.3 explicit triangulation | **partly** | Steps 1–4 of "A curved triangulation of Σ" handle corners, ears and shared boundary vertices correctly, but only for curves on ∂D_f. Seams lie in the interior of D_f in the quotient and are not mentioned (N1). |
| 2.4 simplicial T, metric | **fixed** | At least three vertices on a closed edge; standard simplices. Nit: N5. |
| 2.5 C¹ up to the boundary | **fixed** | Via Lemma C.1(c),(d) and P. |
| 3.1 several shells | **fixed** in both appendices | `sec_proofBprime.tex` "Between shells"; `sec_proof51.tex` l.147–149 and l.243. |
| 3.2 compactness argument | correct, unchanged | — |
| 3.3 planar degree argument, T-vertices on edges | **fixed** | "Inside a face" and "Along a non-seam edge" bullets; added to the list of standard facts. |
| 3.4 uniform angle along edges | **fixed** | "By compactness of γ̃_e and continuity". Needs the half-plane at the end points to be defined (N3). |
| 3.5 C¹ up to the vertex | **fixed** | Vertex bullet and the list of standard facts. |
| 4.1, 4.2 margin, zones | correct, unchanged | — |
| 4.3 affine refinement | **fixed** | First line of "Secant approximation". |
| 4.4 PL convention | **fixed** | `sec_setting.tex`: PL = linear on some triangulation subdividing the cells, with the 2D uniqueness flagged as a standard fact. |
| 5.1 `sec_open` "covers them" | **partly** | True for closed edges and inner wires; for seams only after N1. Items 5 and 6 of `sec_open.tex` are now partly stale (N4). |
| 5.2 list of standard facts | **fixed** | — |
| 5.3 checking remark | still accurate in substance; wording is stale (N4) | — |

## G. Does "no fold" suffice? Yes.

- **Along an edge.** Two half-planes with the same boundary line are either in different planes, or in the same plane
  on opposite sides of the line (G¹), or equal. "Distinct" excludes only the last. In the first two cases they meet
  only in the line, so the tangent cone is an embedded union of two half-planes. h₀ is C¹ up to the edge from each
  side (Lemma C.1 and P), so the usual argument gives local bi-Lipschitz, with a constant uniform along the edge once
  the angle is bounded below. Transversality is not used anywhere else: the regularity of γ̃_e comes from R and P, not
  from an implicit-function argument. A G¹ edge is therefore fine, and in the G¹ case the tangent cone is a plane.
- **At a vertex.** The vertex clause (sectors meet only along common rays, in cyclic order) does not depend on the edge
  clause. It allows adjacent sectors that are coplanar on opposite sides of their common ray (G¹ edges at the vertex),
  and the blow-up argument needs only that clause and C¹ up to the corner. Correct.
- **The end points of the edge clause are redundant.** If the two limiting half-planes along a ray at c_v coincided,
  the two adjacent sectors would overlap near that ray (both have positive opening angle on the same side), which the
  vertex clause forbids. By C¹ up to the corner, the half-planes along the open edge converge to these limits, so the
  uniform lower bound along the closed edge follows from the open-edge clause plus the vertex clause.
- **The secant step** does not see the difference between transversal and G¹ edges.
- **The remark** ("applies in principle to filleted models, provided a re-trimmed model ... is available") is correctly
  conditional and is not an overclaim.

## H. Lemma C.1: correct (for C² curves)

- (a), (b): correct. On λ₁ = 0 we have s = 1; on λ₂ = 0, s = 0; both are fine at μ = 0 as well.
- (c): correct. |ds| = |λ₁dλ₂ − λ₂dλ₁|/μ² ≤ 1/μ, so |dG| ≤ 2μ|ψ| + μ|ψ′| → 0. Also |G| ≤ μ² sup|ψ| = o(|x − a₃|),
  since μ is comparable to the distance to a₃. So G is differentiable at a₃ with derivative 0, and DG is continuous
  there. Suggest adding that one line: the text shows only that dG → 0, which by itself does not show that G is
  differentiable at a₃. (It follows from continuity of G plus dG → 0 along segments, but say it.)
- (d): correct. Rolle gives |ψ′| ≤ sup|ψ″| and |ψ| ≤ sup|ψ″|/8, and |DG| ≤ 2|ψ| + |ψ′| = O(h²). The injectivity
  estimate on the convex Δ, DF = A(I + O(h)), the simplicity of the boundary curve (the arc's tangent at a₁ is within
  O(h) of the chord, and the segments are at angle ≥ θ_min), and the invariance-of-domain argument for the image are
  all fine.
- The remark on the μ¹ blending is correct.

## I. New findings

**N1 (major, introduced in v0.7). Seams are no longer covered by R or by the triangulation.**
- With U_f a quotient ℝ²/Λ_f and X_f injective on D_f ⊂ U_f, a seam's preimage is a curve in the *interior* of D_f.
  (On a cylinder face, D_f is a closed annulus and the seam is a cross-cut.) Then:
  - R constrains only ∂D_f. Nothing says the seam preimage is a simple C² regular curve, that it meets ∂D_f only at
    preimages of c_v, or that it meets ∂D_f at nonzero angle on each side. Step 1 of the proof ("fix one C² regular
    parametrization of each γ̃_e") is therefore unsupported for seams. Step 1 for non-seam edges follows from R and P.
  - Steps 2–4 build chord polygons and corner fans only from curves on ∂D_f, and step 3 triangulates "the chord region
    ... with no extra vertices on its boundary", which neither puts the seam vertices into T nor makes the seam a union
    of T-edges. Then T does not subdivide the cells, and the margin/zone step (which needs every simplex inside one
    closed cell) fails for the seam edge and for the open face.
  - At a seam vertex, ∂D_f is typically smooth (angle π), so it is not a "corner". Step 3 puts no interior vertex there,
    and a triangle with the seam and the boundary arc as two curved sides is not excluded.
  - T's vertex clause defines sectors through "corners of D_f". A vertex where two seams cross inside D_f (a torus
    face) has no corner at all.
  - Setting and C: for a seam face, "the interior of the face" and "the patch minus its boundary curves" contain the
    seam, so they are not the open 2-cell of a cell structure (as already noted under 1.1).
- **Fix** (a paragraph):
  - In R, speak of the *edge graph* E_f ⊂ D_f: the preimage of all edge curves of f, seams included. Ask that its
    edges are simple C² regular curves meeting only at preimages of the c_v. Also ask that every sector of D_f ∖ E_f at
    a vertex preimage has angle in (0, 2π). (For a seam ending on a smooth boundary curve, this asks for angles in
    (0, π) on both sides, i.e. the seam is not tangent to the boundary.)
  - In C and in `sec_setting.tex`, the open face is X_f(int D_f ∖ E_f), the patch minus *all* its edge curves.
  - In T, the tangent sectors are dX_f of these sectors.
  - In the proof, steps 2–3 work in D_f cut along its seams (a compact planar region, glued back afterwards). Equivalently:
    treat the seam chords as constrained interior edges with their vertices fixed in step 1, and put a corner fan at
    every sector of D_f ∖ E_f, not only at corners of ∂D_f. Lemma C.1 is then applied on both sides of each seam chord.
  - With this, 2.2's seam case and the seam bullet of the bi-Lipschitz step are correct as written.

**N2 (major for Appendix A; outside the original scope). Lemma C.1 assumes C², but Appendix A uses it on C¹ curves.**
- `sec_proof51.tex` l.128 says ∂Q_f is piecewise C¹. Its pieces are k_{f,e}, which is C¹ in t (l.9, implicit
  function theorem; ρ_e is only C¹ by its definition in `sec_existence.tex`), and A_{f,v}, parametrized by a "C¹ regular"
  φ (l.111). Lemma C.1 requires a C² curve with uniform C² bounds, so as stated it does not apply there.
- **Fix:** state the lemma for C¹ curves; the proof carries over. With ω the modulus of continuity of ĉ′:
  - |ψ′(s)| = |t₁ − t₀|·|ĉ′(t) − mean of ĉ′ over [t₀, t₁]| ≤ |t₁ − t₀|·ω(|t₁ − t₀|) = O(h·ω(h)), and |ψ| ≤ sup|ψ′|;
  - so |DG| = O(h ω(h)) and DF = A(I + O(ω(h))) → A(I + o(1)), which is all that injectivity, invertibility and the
    secant estimate use;
  - (c) uses only ψ ∈ C¹; the arc is within O(h ω(h)) = o(h) of its chord, which is enough for the image argument.
  - Keep the C² statement as the special case with O(h) error, or replace it.

**N3 (minor). T's edge clause at end points.** "Inward tangent half-plane ... end points included" is undefined at c_v,
where a patch has a sector. Either define it as the limit along the edge (the half-plane of T_{c_v}S_f bounded by the
edge tangent that contains the sector near that ray), or drop "end points included" and note that the end-point case
follows from the vertex clause (§G, third bullet). The proof's "by compactness and continuity" sentence then cites that.

**N4 (minor). Stale wording after weakening T.**
- `sec_existence.tex`, checking remark: "the vertex part of the transversality hypothesis" should be "the vertex part
  of T". Note also that the checker tests transversality, which is stronger than T's edge clause; that is fine, but say
  so.
- `sec_experiments.tex` l.110: "Re-intersection avoids this, but needs transversal faces." Now only the *computation*
  of the re-trimmed model needs transversality; the proposition does not. Table row "sewn filleted box ... not
  applicable (tangent faces)": say "(re-trimmed model not computable by re-intersection)".
- `sec_open.tex` item 6 (mixed vertices "need a construction combining fans and re-intersection") and item 5 (tight
  vertices with tangent edges): Proposition 5.3 now covers such vertices *if* a re-trimmed model exists. The open part
  is to produce one with positive margins. Reword so the paper does not say both "covered in principle" and "needs a
  new construction".

**N5 (minor nit).** "Between shells a constant distance": for this to be a metric the constant must be at least half
the largest shell diameter. Since the shells are now argued separately, simpler: "we do not compare points of
different shells in this metric".

**N6 (minor).** Lemma C.1(c): add the line showing that G itself is differentiable at a₃ (|G| = O(μ²)); see §H.

## Verdict on v0.7

**Lemma C.1 and the no-fold weakening are correct.** All first-pass findings are fixed except where seams are
involved. One required change remains for Proposition 5.3: **N1**, putting seams back into R, C, T, the setting and
the triangulation, which is about a paragraph. One required change remains for Appendix A: **N2**, the C¹ form of
Lemma C.1. With these two, I consider the proof of Proposition 5.3 complete modulo the standard facts listed in
Appendix B. N3–N6 are wording.

---

# Follow-up on v0.7.1

Read at commit 6c361ba: Proposition `prop:Bprime` and its remarks (`sec_existence.tex`), `sec_proofBprime.tex`,
`sec_curvedtri.tex`, `sec_setting.tex` §Complexes, the shell metric and Lemma C.1 use in `sec_proof51.tex` (l.128–149,
241–243), `sec_experiments.tex` l.86–116 and `sec_open.tex`. No draft file was edited.

## Status of N1–N6

| # | Status | Check |
|---|---|---|
| N1 seams | **closed** | R now speaks of the edge graph G_f, seams included, with all sector angles in (0, 2π); smooth seam vertices are covered. C and `sec_setting.tex` now say open face = face minus all edges, seams included. T's vertex sectors are now dX_f of the G_f-sectors. Appendix B cuts D_f along G_f and puts a corner fan in every sector at every G_f-vertex. Seam arcs are now unions of T-edges (step 4), so T subdivides the cells and the zone step holds for seams. Step 1 (C² regular parametrization of each γ̃_e) is now supported by R and P for seams too. The seam case of the edge argument ("opposite in the tangent plane of S_f") is correct. |
| N2 C¹ lemma | **closed** | Checked below. Appendix A's pieces k_{f,e} (C¹ in t) and A_{f,v} (C¹ regular φ) now meet the hypotheses: a finite family of compact C¹ curves has a uniform modulus. |
| N3 T at end points | **closed** | T's edge clause is now stated for interior points only. The parenthesis in T and the bi-Lipschitz bullet ("near the end points the vertex argument takes over") are correct, because the blow-up argument gives a bi-Lipschitz constant on a whole neighbourhood of c_v, edge points included. |
| N4 wording | **closed** | `sec_existence.tex` remark: "vertex part of hypothesis T". `sec_experiments.tex` l.110–112: transversality is now attributed to the computation only. Table row: "computation not applicable (tangent faces)". `sec_open.tex`: the new item "Re-trimmed models for tangent edges" replaces "Mixed vertices" and is consistent with the remark after the proposition and with "Tight vertices". Item 2's "(Proposition covers them)" is now true. |
| N5 shell metric | **closed** | Both appendices now use the intrinsic metric per shell and argue between shells by δ/2. |
| N6 G at a₃ | **closed** | C.1(c): |G| ≤ μ² max|ψ|. μ = 1 − λ₃ is comparable to |x − a₃|, so this gives DG(a₃) = 0, and |dG| = O(μ) gives continuity. |

## Lemma C.1 (C¹ version): correct

- (a), (b), (c): correct as written. For μ > 0, s = λ₂/μ is smooth and ψ ∈ C¹, so F ∈ C¹ off a₃; at a₃ see N6.
- (d): ψ′(s) = Δt(ĉ′(t₀ + sΔt) − mean ĉ′) is right, because a₂ − a₁ = Δt · mean ĉ′. This gives
  |ψ′| ≤ |Δt| ω(|Δt|) and |ψ| ≤ max|ψ′|, so |DG| ≤ 2|ψ| + |ψ′| = O(h ω(h)) and A⁻¹DG = O(ω(h)).
- The injectivity estimate on convex Δ is correct.
- The image argument is correct: the arc stays within O(hω(h)) = o(h) of its chord, its tangent at a₁ is within angle
  O(ω(h)) of the chord, and the segments are at angle ≥ θ_min.
- One small hypothesis gap, see M4.

## New findings (all minor; no new major or fatal issue)

**M1. That ∂D_f ⊆ G_f is used but only implied.**
- The old R said ∂D_f consists of edge preimages. The new R speaks only of G_f, and step 2 ("each region bounded by arcs
  of G_f") needs ∂D_f ⊆ G_f.
- It does follow from C + P. Suppose p ∈ ∂D_f ∖ G_f. Then X_f(p) lies in the open face, which is open in Σ and
  contained in X_f(D_f). Since X_f|D_f is a homeomorphism onto its image (compact, injective), p has a neighbourhood
  in D_f that is an open disk. By invariance of domain in U_f, p is interior to D_f, a contradiction.
- Fix: add "Since C makes each open face open in Σ, ∂D_f ⊆ G_f", or put ∂D_f ⊆ G_f into R.

**M2. R: "Its edges are simple C² regular arcs, or simple closed curves."**
- Every edge of K has a vertex, so a closed edge is a loop based at a vertex of G_f. A closed curve with no vertex is
  not possible, but the wording allows it.
- Also, at its base vertex a loop may have a corner. The sector condition covers that.
- Fix: write "arcs between vertices, or loops at a vertex".

**M3. After cutting, the regions need not be simple polygons.**
- A face with inner wires gives a multiply connected region.
- The quotient formulation also allows a face on a periodic surface without a seam edge (a flat annulus in ℝ²/Λ_f),
  which is a flat surface, not a planar region.
- The construction still works: triangulate locally with straight chords in the flat metric.
- Fix: in step 2 and in the first standard fact, change "simple polygon" to "compact flat polygonal surface (possibly
  multiply connected, or in the flat quotient) with prescribed boundary vertices".
- Related, cosmetic: the seam bullet of "h₀ agrees on shared edges" no longer needs periodicity. Both sides use the same
  pulled-back arc in U_f, since D_f lives in the quotient.

**M4. Lemma C.1(d) needs the speed of ĉ bounded below.**
- The hypothesis "|t₁ − t₀| times the speed is O(h)" bounds |Δt|·|ĉ′|. The estimate |ψ′| ≤ |Δt| ω(|Δt|) = O(hω(h))
  needs |Δt| = O(h) itself, so it needs |ĉ′| ≥ c > 0 uniformly ("uniformly regular").
- It also implicitly uses ω(Ch) ≤ C′ω(h), which holds for a subadditive (e.g. concave) modulus.
- Both hold in both appendices (finitely many compact regular curves, arc-length-type parametrizations). Add
  "with speed bounded below" and "ω subadditive" to the hypotheses of (d).

## Verdict on v0.7.1

**N1–N6 are closed.** Lemma C.1 in its C¹ form is correct and now applies in both appendices. The no-fold form of T,
with the vertex clause, is sufficient. I found no new error and no overclaim; M1–M4 are wording or hypothesis-precision
items. **I consider the proof of Proposition 5.3 complete, modulo the standard facts listed at the end of Appendix B
and Appendix C, and acceptable for submission once M1–M4 are fixed.**
