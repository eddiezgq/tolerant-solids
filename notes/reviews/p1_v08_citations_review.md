# Referee report: p1 Draft v0.8 (commit ccc487d), citation checks and rewritten proof passages

Scope: the v0.8 citation checks and the three rewritten proof passages. Each claim was compared with the source
text extracts and, where a symbol mattered, with rendered PDF pages (Durfee pp. 523 and 525). Quotations are kept
short.

**Verdict.** The rewritten arguments are correct, and almost all citations now match their sources. One
substantive gap remains (M1): Waldhausen's proof of Prop. 3.1 needs irreducibility of F×I for compact F *with
boundary*, which is exactly the case on the cited page 66, and the new Lemma covers only closed F. The fix is easy.
Two places still say the Moise citation is unchecked and describe the wrong Moise theorem (M2). The rest is minor.

---

## Major

**M1. sec_uniqueness.tex:88–89 and Lemma at 100–124: the irreducibility input covers only the top level of Waldhausen's induction.**
- What Waldhausen does: the explicit use "since M is irreducible" on p. 66 is in the *special case* of the proof of
  Prop. 3.1, where F is a disc, an annulus or a pair of pants (so F has boundary). The general case (p. 67) works by
  induction on (genus F, number of boundary components). It cuts F×I along a vertical annulus and repeats "similar
  arguments as in (a) and (b)", so it needs irreducibility of F′×I for every intermediate F′. All of these except
  the starting surface have nonempty boundary. The proof ends at the top of p. 68.
- The problem: the paper says "Waldhausen's proof of Proposition 3.1 uses that F×I is irreducible [p. 66]. For
  closed F of genus at least one this is Lemma 5.x". That is accurate as far as it goes, but the page it cites is the
  bounded case, which the Lemma does not cover.
- Fix (one of these):
  - (a) Extend the Lemma to every compact orientable F other than S². For ∂F ≠ ∅ the universal cover F̃ is a simply
    connected surface with boundary. It PL-embeds in R², and the same proof goes through: points of
    (R²∖F̃)×I and of R³∖R²×[0,1] reach infinity by vertical rays that miss S̃. For F a disc, Γ is trivial.
  - (b) Add "F×I for ∂F ≠ ∅ is a handlebody, irreducible by Alexander's theorem" to the list of standard facts.
- Also cite pp. 65–68 rather than 65–67 (line 81).

**M2. Stale "still to be checked" statements about Moise, and the wrong theorem named.**
- p1.tex:48–50 (abstract): "one step relies on Moise's theorem that homeomorphic 3-manifolds are PL homeomorphic,
  whose citation is still to be checked against the original."
- sec_intro.tex:46–48: "One step relies on Moise's theorem on PL structures of 3-manifolds, whose citation is still
  to be checked against the original."
- The (a′) proof now uses Thm 35.2: a homeomorphism of a polyhedral 3-manifold with boundary into a PL 3-manifold
  can be approximated by a PL homeomorphism. I checked it on p. 251, and its use is correct (see §2 below). So both
  passages are now false twice over: the citation is checked, and the theorem is misdescribed.
- They also contradict sec_open.tex:4–6, which says all results quoted in proofs have been checked.
- Fix: replace both with something like "one step uses Moise's PL approximation theorem [Moise77, Thm 35.2]", or
  drop the caveat.

---

## 1. sec_collar.tex Step 1 (Durfee)

- **Def. 3.1 (p. 523, checked on the rendered page).** The conditions are: M semialgebraic in Rⁿ; X ⊂ M compact
  semialgebraic; α proper semialgebraic; α ≥ 0; α⁻¹(0) = X. Durfee's "semialgebraic function" includes continuity
  (p. 518). The example list explicitly includes non-smooth functions.
  - d|_Q meets every condition. It is continuous. It is semialgebraic by Tarski–Seidenberg, because M is a finite
    union of triangles. It is proper, because Q is compact. Its zero set is M.
  - The claim "asks exactly this and no smoothness" is accurate. **OK.**
- **Def. 3.4 (p. 525).** T = α⁻¹[0,δ] "for a suitably small positive number δ". Durfee makes "suitably small"
  precise: take an α-stratification with X a union of strata, and let J be the strata disjoint from X whose closures
  meet X. Then δ must be small enough that 0 < α ≤ δ forces x into those strata.
  - Durfee does not prove that such a δ exists, but it is immediate. Finitely many strata; a stratum whose closure
    misses X is at positive distance from the compact set X; and properness of α makes α⁻¹[0,δ] shrink to X.
  - No hidden hypothesis beyond this. The paper's "for suitably small δ" and then "take δ < r" is fine.
  - Optional: one sentence noting that such a δ exists.
- **Prop. 3.5 (p. 525).** Gives a continuous family hₜ: M → M, 0 ≤ t ≤ 1, with h₀ = id, hₜ|_X = id for all t, and
  h₁(T₁) = T₂ (in fact an S-isomorphism). With Durfee's M = Q and X = the surface, this is exactly what lines 35–36
  state. **OK.**
- **Prop. 3.7 (p. 526).** Hypotheses: "X ⊂ T ⊂ M finite simplicial complexes in Rⁿ, T a PL regular neighbourhood of
  X in M."
  - These hold: M (the surface) ⊂ R ⊂ Q, with R a subcomplex of a subdivision of Q.
  - Durfee's proof is a sketch. It builds a derived neighbourhood from a simplexwise-linear α and appeals to
    uniqueness of regular neighbourhoods (Hudson).
  - I checked that it is sound: if h is a PL homeomorphism fixing X, then α∘h⁻¹ is again simplexwise linear, and the
    "suitably small" condition holds for δ below the vertex values. **OK.**
- **Minor (line 39).** "Its frontier S_δ = {d = δ}" is used before it is justified. That a point with d = δ is not
  interior to N̄_δ needs non-criticality: δ < wfs, by the same directional-derivative argument as Step 3. Add
  "(Step 3)" or move the remark.

## 2. sec_collar.tex (a′) (Moise Thm 35.2)

- **The theorem (p. 251).** Let M₁, M₂ be PL 3-manifolds, K a polyhedral 3-manifold with boundary in M₁, h: K → M₂
  a homeomorphism (into), and φ ≫ 0 on K. Then there is a PLH f: K → M₂ that φ-approximates h.
- **The hypotheses are met.**
  - M₁ = M×(−1,1) is a PL 3-manifold, since M is a triangulated surface.
  - K = M×[−b,b] is a polyhedral 3-manifold with boundary in it.
  - M₂ = R³.
  - h = g|_K is a homeomorphism into R³.
  - A constant ε > 0 is strongly positive on the compact set K.
- **The setup steps are correct.**
  - g exists: the interior of N̄_r is N_r (Step 3), and homeomorphisms preserve manifold interiors.
  - g⁻¹(N̄_d) is compact, so it lies in M×[−a,a].
  - g(∂K) misses N̄_d.
- **The depth argument is correct and complete.**
  - |f − g| < ε < dist(g(∂K), N̄_d), so the straight-line homotopy misses x. Hence the inside/outside status of x
    relative to each of the two boundary surfaces agrees for f and for g. x is also not on f(∂K) = ∂U.
  - For U ≅ M×I with ∂U = B₁ ⊔ B₂: R³∖(B₁∪B₂) has 3 components (Alexander duality); int U is adjacent to both
    surfaces; the unbounded component has depth 0. So the depths are 0, 1, 2 with int U = depth 1. This matches
    Definition def:solid (depth = number of bounded components containing x).
  - So x ∈ int U.
  - U is a compact PL submanifold, PL-homeomorphic to M×[−1,1], and lies in N_r. **OK.**
- **Minor (line 100).** "The compact sets g(K) and R³∖N_r(M)": R³∖N_r is closed, not compact. The positive distance
  still holds (compact vs. closed and disjoint). Reword.
- **Minor (lines 104–108, 125–129).** These facts are used but are not in the standard-facts list: the mod-2 degree
  of the radial projection detects inside/outside of an embedded closed surface, and that degree is homotopy
  invariant. Add them. Alexander duality is flagged inline but not in the list.

## 3. sec_uniqueness.tex (Waldhausen; new irreducibility Lemma)

- **The Lemma's proof is correct for closed F of genus ≥ 1.**
  - Lifting works: S is simply connected, so it lifts to embedded spheres, and distinct lifts are disjoint.
  - Moise Thm 17.12 (ch. 17, pp. 117–126) indeed gives a PLH of R³ taking S to the boundary of a 3-simplex. So S̃
    bounds a PL 3-cell.
  - The vertical-ray argument puts B̃ inside R²×I.
  - The "disjoint or nested" step is correct. An implicit step: γB̃ is *the* cell bounded by γS̃, because the cell
    bounded by a 2-sphere in R³ is unique.
  - Torsion-freeness plus proper discontinuity rules out nesting, so q is injective on B̃.
  - Genus ≥ 1 is used exactly where needed: F̃ is noncompact.
  - Minor: the statement "every PL 2-sphere in F×I" relies on the properly-embedded convention (bullet 1). Put
    "in F×(0,1)" or "properly embedded" in the statement itself.
- **Accuracy of "Waldhausen's proof uses irreducibility of F×I (p. 66)":** true, but see M1. The p. 66 use is the
  bounded-F base case, and p. 67 uses it implicitly at each induction level.
- **Step (d) is correct.**
  - p. 57, definition (b): an isotopy of subspaces Z₁, Z₂ in X is an isotopy of the identity of X with h₁(Z₁) = Z₂.
  - Prop. 3.1 (p. 65) says G "is isotopic, by a deformation which is constant on ∂M". So the isotopy is ambient on U
    and fixed on ∂U, and it extends by the identity. **OK.**
- **Conventions (§0, pp. 56–57).** These match the use:
  - PL category up to §7.
  - Manifold = orientable 3-manifold, compact. U is a compact PL submanifold of R³, PL via Ψ.
  - Surfaces are connected and compact/orientable unless stated otherwise. G is a closed connected orientable PL
    surface.
  - Properly embedded means F ∩ ∂M = ∂F, and G ⊂ int U.
  - Prop. 3.1 needs F orientable and not S². That holds: M is orientable and not a sphere.
- **Incompressibility (p. 58).** Waldhausen's definition has case (a), a disc with non-contractible boundary, and
  case (b), a sphere bounding a ball.
  - The argument by π₁-injectivity is the easy direction, and it is right.
  - Case (b) is excluded because G is not a sphere.
  - Correct, and the paper correctly avoids Lemma 1.1.3 (loop theorem).

## 4. sec_intro.tex: Fu and APS

- **APS00 Thm 1 (lines 122–126; source p. 612).** The paper's summary matches Assumption 2: properly joined (in the
  same way) for all t, one-to-one, non-singular Jacobian, adjacent patches nontangential for all t. It omits
  Assumption 1 (control points C¹ in t, X ∈ C²), which is acceptable in a summary. APS's Definition 2 (tangent
  vectors at a common point not parallel and identically directed) is indeed close to clause T. Not overclaimed.
  **OK.**
- **Fu §5.3 (lines 136–140; source p. 1045).** Fu's definition is "a certain fixed finite set of algebraic
  inequalities all hold", and he assumes S compact. So the remark about a single system is fair, and the extension to
  finite unions is valid.
  - Minor overclaim: "the argument uses only Tarski–Seidenberg". Fu's argument also uses a decomposition of the
    semialgebraic graph into finitely many smooth submanifolds (his ref. [28]), his Lemma 4.3, and Sard's theorem.
    All of these hold for general semialgebraic sets, so the conclusion stands. Suggested wording: "uses only tools
    valid for all semialgebraic sets (Tarski–Seidenberg, a finite smooth decomposition, Sard)".
  - Trivial: "since critical points lie off the set" is unnecessary. In Fu's formulation points of S are critical with
    value 0, and finiteness alone gives a positive minimum of the positive critical values.

## 5. sec_open / sec_obstruction / sec_experiments

- **sec_open.tex:9–11.** Accurate. Prop. 3.1 explicitly excludes F = S² (p. 65). Calling Moise Thm 17.12 "the
  natural tool" is a remark, not a claim.
- **sec_obstruction.tex:110–111, 125.** Accurate. Two paths in a square (here an affine image, the parallelogram Q)
  joining opposite sides must meet. This is the standard Brouwer/Poincaré–Miranda consequence, correctly listed as a
  standard fact.
- **sec_experiments.tex:59–63.** Correct.
  - A knot admits a non-trivial Fox 3-colouring iff 3 | det.
  - A non-trivial colouring uses all three colours and sends meridians to transpositions, so it gives a surjection
    onto S₃, which is non-abelian.
  - Solid torus: π₁ = Z.
  - Minor: "homeomorphic to the trefoil exterior" rests on the construction (the centreline follows a trefoil), while
    the script certifies only det = 3. The non-homeomorphism argument needs only det = 3, so say "a knot exterior
    (determinant 3)" or cite the construction.

## 6. sec_biblio.tex

| Entry | Source data | Status |
|---|---|---|
| Durfee83 | Trans. AMS 276, no. 2 (April 1983), 517–530 | matches (issue "(2)" may be added) |
| Fu85 | Duke Math. J. 52(4) (1985) 1025–1046 | matches |
| APS00 | IJCGA 10(6) (2000) 609–622 | matches |
| Moise77 | GTM 47, Springer, New York, 1977 (ch. 17 pp. 117–126; ch. 35 pp. 247–252) | matches |
| Waldhausen68 | Ann. of Math. 87 (1968), no. 1, 56–88 | matches |

## 7. Checked / unchecked markers

- M2 above: the abstract and the intro still say the Moise citation is unchecked.
- sec_open.tex:4–6 says all literature results used in proofs are checked. I could not verify this for
  ChazalLieutier07 (Prop. 3.4, Lemma 2.2), CCSL09dcg (§§2.1–2.2) or Federer59 (sec_proof51), because no source
  extracts were provided. The author should confirm that these were checked.
- The CCS05 `\unverified` (sec_biblio:13) and the draftnote (sec_open:31) are still red/orange. That is consistent,
  because CCS05 appears only in remarks and the intro, not in proofs. It must still be resolved before submission
  (p1.tex:9).
- No item that is now checked is still marked with `\unverified`.

## Summary of minor items

1. sec_collar:39: the frontier = {d = δ} needs the non-criticality argument.
2. sec_collar:100: "compact" should be "closed" for R³∖N_r.
3. sec_collar:125–129: add mod-2 degree/inside criterion and Alexander duality to the standard facts.
4. sec_uniqueness:101–106: put the properly-embedded convention into the Lemma statement.
5. sec_uniqueness:81: pp. 65–68.
6. sec_intro:137–140: Fu's argument also uses a finite smooth decomposition and Sard, not only Tarski–Seidenberg.
7. sec_experiments:59–60: "trefoil exterior" is stronger than what is certified (det = 3), though harmless.
8. Durfee biblio: optionally add issue 2.

---

## Follow-up on v0.8.1 (commit 5716c78)

**Verdict.** All requested fixes are correct. They introduce no new errors. M1 and M2 are resolved, and so are the
minor items that were addressed. Nothing major remains.

### M1: Lemma lem:irreducible (sec_uniqueness.tex)
- **The statement is right.** It now covers compact orientable F ≠ S² and restricts to spheres in int(F×I). This
  matches Waldhausen's definition of irreducibility (p. 58: a ball E with E ∩ S = ∂E).
- **The case ∂F ≠ ∅ is correct.**
  - F×I is PL homeomorphic to a handlebody H. Irreducibility is intrinsic, so the choice of embedding H ⊂ R³ does
    not matter.
  - ∂(F×I) = F×0 ∪ ∂F×I ∪ F×1 is connected when ∂F ≠ ∅. So R³∖∂H has two components (by Alexander duality, or
    Jordan–Brouwer). One of them is int H, so R³∖H is connected and unbounded.
  - R³∖H is disjoint from S ⊂ int H, so it lies in the unbounded component of R³∖S. Hence the Schoenflies cell
    B ⊂ H.
  - Disc, annulus, pants and every surface produced by cutting are covered. Orientability is what makes F×I a
    handlebody that embeds in R³.
- **The closed case is unchanged** and was already correct. The new sentence on torsion-freeness and proper
  discontinuity is a good addition.
- **The Waldhausen sentence in (b) is now accurate.** Irreducibility is used explicitly in the base case on p. 66 and,
  through "similar arguments", at each level of the induction on p. 67. The proof ends on p. 68, and the citation is
  now pp. 65–68.

### M2: stale Moise text
- The abstract (p1.tex) no longer mentions Moise. The intro (sec_intro.tex:47–48) now cites Thm 35.2 as an
  approximation theorem, which is correct.
- No remaining occurrences of "still to be checked", "Hauptvermutung" or "PL structures" in the .tex files.

### Minors
- **sec_collar Step 1.** The frontier justification is fine: δ < wfs, so the Step 3 directional-derivative argument
  applies at level δ, and {d = δ} ⊂ Fr. The reverse inclusion is by continuity. The forward reference to Step 3 is
  acceptable.
- **sec_collar (a′).** The "compact / closed" wording is now correct.
- **sec_collar, standard-facts list.** It now includes the mod-2 degree side test and Alexander duality.
- **sec_intro, Fu.** The new wording is accurate. Fu's Lemma 4.3 exists (it is Ferry's lemma, on p. ~1041), and it is
  the lemma used in §5.3. The trivial remark "since critical points lie off the set" is still there. It is harmless
  and optional.
- **sec_experiments.** "Trefoil exterior" is gone. The argument now rests only on det = 3, which is what the script
  certifies.

### Still open (unchanged, not v0.8.1 regressions)
- CCS05: the `\unverified` mark and the draft note remain, as intended (remarks only).
- Commit c2210c5 records checks of CL07 Prop. 3.4 / Lemma 2.2. I did not re-verify CCSL09dcg §§2.1–2.2 or Federer59
  (sec_proof51), because no extracts were provided. The author should make sure the claim in sec_open:4–6 covers them.
- Optional, not requested: issue number "(2)" for Durfee in the bibliography.

---

## Follow-up on v0.8.2 (commit aeacfd5)

**Verdict.** All three newly checked citations match their sources. The Federer deduction is correct. No
`\unverified` or `\draftnote` markers remain. There is one wording point in sec_proof51 (minor) and one residual
caveat on the claim in sec_open.

### (1) CCS05, Thm 2.1 (Graphical Models 67 (2005), p. 392)
- **Setting.** S and S′ are compact orientable surfaces embedded in R³ (§2).
- **Definition 2.2.** A topological thickening M of S is the image of a homeomorphism Φ: S×[0,1] → M with
  Φ(S×{1/2}) = S. Its sides are Φ(S×0) and Φ(S×1).
- **Thm 2.1.** If (1) S′ ≅ S, (2) S′ ⊂ M and (3) S′ separates the sides of M, then S′ is isotopic to S in M.
- **The paper's descriptions match.** sec_intro.tex:119–121 and sec_uniqueness.tex:167–169 ("compact orientable
  surface S′ ≅ S lying in a thickening of S and separating its sides is isotopic to S in the thickening") are
  accurate. Theorem numbering in the journal version is 2.1, so removing the `\unverified` mark is justified.
  Bibliographic data (67(5), 390–404) match.

### (2) CCSL09 DCG, §2.2 (p. 465)
- **Critical points.** §2.2 ("Critical Point Theory for Distance Functions") defines them by ∇_K(x) = 0, and
  "equivalently" as the points x lying in the convex hull of Γ_K(x). This is the same as 0 ∈ conv{x − y : y ∈ Γ(x)},
  the paper's definition (sec_collar:5).
- **wfs.** §2.2 defines wfs(K) as the infimum of the positive critical values.
- Both the definition at sec_collar:6 ("§2.2") and the changed citation at sec_collar:54 ("see also §2.2") are now
  correct. §2.1 is the gradient and flow, so the change from §2.1 was right.

### (3) Federer 1959, Thm 4.8 (sec_proof51.tex:47–52)
- **What the cited parts say.**
  - 4.8(2), p. 434: P = {v : ξ(a+v) = a} ⊂ Q ⊂ Nor(A,a).
  - 4.8(12), p. 435: if reach(A,a) > r > 0, then Nor(A,a) = {λv : λ ≥ 0, |v| = r, ξ(a+v) = a}.
  - The page numbers are right.
- **The deduction is correct.**
  - Let v ∈ Nor(A,a) with 0 < |v| < reach(A) ≤ reach(A,a). Apply (12) with r = |v|: v = λw with |w| = |v|, so λ = 1
    and ξ(a+v) = a.
  - a+v lies in the ball of radius reach(A,a) about a, which is contained in Unp(A) by Definition 4.1. So a is the
    unique nearest point.
  - Strictly, only (12) and Definition 4.1 are needed. Citing (2) is harmless.
- **The normal-cone claim is correct.**
  - Nor(A,a) = Dual[Tan(A,a)] (Definition 4.4 / Remark 4.5).
  - At an interior point of a C¹ regular arc, Tan is the tangent line, so Nor is the normal plane.
  - At an end point, Tan is the ray {sγ′(a) : s ≥ 0}, so Nor is the half-space {v · γ′(a) ≤ 0}. This contains the
    normal plane.
  - Disjointness follows: a common point of D_e(t) and D_e(s) would have the unique nearest point γ(t) = γ(s), so
    t = s by injectivity.
  - The tangent-cone fact is now listed among the standard facts (line ~254). Good.
- **Minor wording (line 50).** "The normal cone is the dual of the tangent cone, a line at interior points and a ray
  at the end points" reads as if the *normal* cone were a line or a ray. Suggested wording: "The tangent cone is the
  tangent line at interior points and a ray at the end points; its dual, the normal cone, is then the normal plane,
  respectively a half-space, and contains the normal plane in both cases."
- The paper assumes the disk radii are below reach(A). A compact embedded C² arc with end points has positive reach
  (Federer §4, introduction: C² submanifolds with boundary), so this assumption can be met. No issue.

### (4) Markers and the claim in sec_open
- `grep` finds no `\unverified{` or `\draftnote{` uses. Only the macro definitions in p1.tex remain, which is fine.
  An empty line is left at the end of sec_open.tex, which is harmless.
- **Literature results used in proofs, and what I checked:**

  | Citation | Used in proof for | Checked |
  |---|---|---|
  | Durfee83 | Defs. 3.1/3.4, Props. 3.5/3.7 | ✓ (by me) |
  | Moise77 | Thms 17.12, 35.2 | ✓ |
  | Waldhausen68 | pp. 57, 58, 65–68 | ✓ |
  | CCSL09dcg | §2.2 | ✓ |
  | Federer59 | Thm 4.8 | ✓ |
  | ChazalLieutier07 | Lemma 2.2, Prop. 3.4 | author's check (commit c2210c5); I had no extract and did not re-verify |
  | OCCT | definitions | documentation, not a mathematical result |

  CCS05, APS00, Fu85 and dREG22 are cited only in the intro or in remarks. CCS05, APS00 and Fu85 are checked; dREG22
  was not supplied to me.
- So the claim in sec_open:4–6 is true for everything I could check. It rests on the author's own check for
  ChazalLieutier07, whose original was not provided to this referee. If an independent check is wanted, supply the
  CL07 PDF.

### Overall
Ready as far as citations are concerned. The only remaining edit is the optional rewording of sec_proof51 line 50,
plus an independent look at CL07 if desired.

---

## Follow-up on v0.8.3 (Chazal–Lieutier) (commit 84d7a47)

Source: Chazal–Lieutier, DCG 37 (2007) 601–617. I used the text extract and rendered p. 608 to check the statement
of Prop. 3.4.

**Verdict.** Every use of ChazalLieutier07 matches the source, including the corrected Prop. 3.6 sentence. Both
applications in collar Step 2 satisfy the hypotheses of Prop. 3.4. No new issues. With this, the claim in sec_open:4–6
("checked against the originals") is now verified independently for every literature result used in a proof.

### Uses checked
- **sec_collar.tex:7, wfs ("see also").**
  - Def. 3.1 (p. 606) defines wfs(O) of a bounded open O as the distance from O^c to the singular points of ∇.
  - §3.2 (p. 608) restates it as the infimum of the critical values of R.
  - §4.3 (p. 613) defines the wfs of a compact K as that of R^n∖K, "in the same way" although that set is unbounded.
  - This agrees with the paper's definition: every critical point off M has a positive value. **OK.**
- **sec_collar.tex:52–54, Lemma 2.2 (p. 604).** "A point x is a singular point of ∇ iff it lies in the convex hull of
  Γ(x)." This matches "vanishing of their gradient field … iff x lies in the convex hull of its nearest boundary
  points". **OK.**
- **sec_collar.tex:55–56, "which they reproduce from Grove's critical point theory for distance functions".**
  - p. 608: they "satisfy an Isotopy Lemma [21], that we reproduce below (Proposition 3.4)".
  - [21] is K. Grove, *Critical point theory for distance functions*, Proc. Symp. Pure Math. 54.
  - Accurate. (Grove–Shiohama [22] is cited separately for the origin of the critical-point notion.) **OK.**
- **sec_collar.tex:68–72, closed-shell form.**
  - Standing convention (§2.1, p. 603): O is a bounded open subset of R^n and R(x) = d(x, O^c).
  - Prop. 3.4 (p. 608, checked on the rendered page): if 0 < ρ₁ < ρ₂ and $\overline{O}_{\rho_1}\setminus O_{\rho_2}$
    contains no critical point of R, then the levels are homeomorphic topological manifolds, and
    $\overline{O}_{\rho_1}\setminus O_{\rho_2}=\{\rho_1\le R\le\rho_2\}$ is homeomorphic to R⁻¹(ρ₁)×[ρ₁,ρ₂]. Here
    O_ρ = {R > ρ}.
  - The paper puts its hypothesis on the whole set {ρ₁ ≤ R ≤ ρ₂}. That set contains the source's
    $\overline{O}_{\rho_1}\setminus O_{\rho_2}$, so the paper's hypothesis is at least as strong. Its conclusion is
    the source's, word for word.
  - The paper does not mention ρ₁ > 0, but it is automatic here (ρ₁ = δ > 0). **OK.**
- **sec_intro.tex:115–116, "wfs and the isotopy of offsets below it are studied by CL07".** Fair.
  - The Remark on p. 607 derives homeomorphism of O and O_d from Prop. 3.4.
  - The proof of Thm 4.5 (p. 613) says that, by Prop. 3.4, the thickenings K^λ and K^μ are isotopic for
    0 < λ, μ < wfs(K).
- **sec_intro.tex:141–144, Prop. 3.6 and §4.3 (corrected sentence).** Accurate.
  - Prop. 3.6 (p. 609): for a bounded subanalytic open O, the set of critical values of R is finite, so wfs(O) > 0.
    It is stated without proof.
  - The text then says it "has been proven by Fu [18, p. 1045] for semialgebraic sets. The proof adapts easily to
    piecewise analytic sets and may be found in [7]". [7] is Chazal–Lieutier, *The λ-medial axis*, Graphical Models
    67(4) (2005), an earlier paper of theirs.
  - §4.3 defines wfs for compact sets via the complement, as the paper now says.
  - The old wording ("prove it … extension stated in §4.3 without proof") was indeed unsupported. The correction is
    right.

### Do the Step 2 applications meet Prop. 3.4's hypotheses?
- **Inner side.**
  - O = Ω₋ is bounded and open.
  - O^c = M ∪ Ω₊, and nearest points from Ω₋ lie on M. So R = d and Γ_O = Γ_M on Ω₋, and the criticality notions
    agree by Lemma 2.2.
  - Points with δ ≤ d ≤ r < wfs(M) are not critical.
  - Hypotheses met with ρ₁ = δ > 0 and ρ₂ = r. **OK.**
- **Outer side.**
  - O = Ω₊ ∩ B(0, ℛ) is bounded and open, and R = min(d, ℛ − |x|).
  - With ℛ > 2r + max_M |y|:
    - d(x) ≤ r implies |x| ≤ max|y| + r, so ℛ − |x| > r ≥ d. Thus R = d and Γ_O = Γ_M (strict inequality).
    - ℛ − |x| ≤ r implies |x| ≥ ℛ − r > max|y| + r, so d > r ≥ R. Thus Γ_O is the single radial point, which does not
      equal x, so x is not critical.
  - So the shell {δ ≤ R ≤ r} is the disjoint union described in the paper and contains no critical point. Prop. 3.4
    applies. **OK.**
  - Optional: say "strictly" for the comparison of the two distances, since the equality of Γ_O and Γ_M relies on it.

### Bibliography
ChazalLieutier07, DCG 37 (2007) 601–617, matches the source header. The issue number is not shown in the extract.
