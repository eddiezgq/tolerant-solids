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
