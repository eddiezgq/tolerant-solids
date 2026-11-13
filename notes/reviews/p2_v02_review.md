# Review: P2 strips and cones, draft v0.2 (notes/p2_strip_cone_v02.md)

Reviewed against:
- `notes/p2_strip_cone_v01.md` and `notes/p2_phase1_report.md`;
- P1 as it stands (`paper/sec_setting.tex`, `sec_proof51.tex` = Appendix B, `sec_curvedtri.tex` = Appendix A /
  Lemma A.1, `sec_proofBprime.tex` = Appendix C; numbering from `p1.aux`);
- the checker `compute/strip_cone_check2.py` (plus `edge_crossing` in `strip_cone_check.py` and `edge_samples` in
  `lemma0_check.py`).

Standard: as strict as for P1.

**Verdict.** The construction is sound in outline, and most steps can be repaired with short arguments. The zone
argument (Step 1) is correct. But the draft is not yet a proof. Four major issues:
- **M1.** The definition of b*_f(t) is ill-posed as written.
- **M2.** The re-trimmed (mixed) case is not well defined.
- **M3.** "Lemma A" is not what P1 proves, and the apex and λ_v-corner arguments are missing. The missing parts can be
  taken from P1, but not in the form claimed.
- **M4.** The checker tests a different strip from the one in the theorem, and several hypotheses are not tested at
  all.

---

## Major

### M1. Strip edges: b*_f(t) is not well defined (§1, E1′, Step 2)
- **The definition fails.** "The boundary curve of each adjacent patch crosses Π(t) in exactly one point" cannot hold
  as written. ∂P_f is a closed curve and Π(t) is a whole plane. A closed curve that crosses a plane transversally does
  so an even number of times.
  - v0.1 localized the definition (b*_f = ∂P_f ∩ Π(t) "unique under E2.2", P1's monotonicity of π_e(β_{f,e})).
  - v0.2 dropped E2.2 without a replacement.
- **Needed:**
  - b*_f(t) must be the point of **β_{f,e}** (the edge's own pcurve image) in Π(t) ∩ B(γ_e(t), ρ_e), with
    ρ_e < min(τ_e, reach_e).
  - It must be unique there.
  - t ↦ b*_f(t) must sweep a single sub-arc of β_{f,e}. E2.2 gives this, or an equivalent graph condition.
- **Why it matters.** Without this, E1′ ("|b*_f(t) − γ_e(t)| < …") refers to an undefined point. The IFT argument in
  Step 2 then gives only a local C¹ branch, not a global continuous selection. The strip could also attach to the
  wrong boundary arc of P_f.

### M2. Re-trimmed edges and mixed vertices: P̃_f is not well defined (§1, R′, V1′, Steps 3–4) (Question 4)
- **The cut does not separate.** "P̃_f is the closure of the component of P_f ∖ c_e that contains the interior of P_f
  away from e" is ill-posed. By (R′), the ends of c_e lie in int B_v and int B_w, typically at interior points of
  P_f. Then P_f ∖ c_e is connected, so "the component" does not exist. "The interior of P_f away from e" is also
  undefined.
  - The cut only separates after the balls are removed. In P1 Prop. 5.4 the re-trimmed model is given as a whole,
    with arcs that run from vertex to vertex.
- **Needed hypotheses** (or a definition of P̃_f on P_f ∖ ⋃ int B_v):
  - (a) (P_f ∖ ⋃_v int B_v) ∖ c_e has exactly two components;
  - (b) the discarded one contains β_{f,e} ∖ ⋃ int B_v and no other point of ∂P_f;
  - (c) the kept one, P̃_f, meets S_v in a single arc that ends on c_e ∩ S_v;
  - (d) c_e is transversal to S_v.
- **Notation clash.** c_e is used both for the chord c_e(t) of a strip edge and for the re-trimmed arc c_e.
  - In (V1′a), "junction curve between two pieces (b*_f(I_e), c_e)" is ambiguous. If it means the re-trimmed arc,
    then (d) is there, but it should be explicit.
  - Rename one of the two, for example chord κ_e(t) and re-trimmed arc c_e.
- **What does hold.** Given (a)–(d), the mixed vertex works.
  - Along c_e two transversal kept half-disks meet: a crease. (S1′) excludes all other P̃_f ∩ P̃_g contacts.
  - On S_v the face arcs of f and g meet at c_e ∩ S_v, so λ_v gets a corner there.
  - (E4a) for a neighbouring strip edge is stated with P̃, which is the right set.
- **What the checker does instead.** It does not compute c_e. At the vertex it accepts a "crossing" when the two full
  face arcs come within r/6 of each other, and trims at the closest pair (see M4).

### M3. Step 6: "Lemma A" is not what P1 Appendix B proves, and two local cases are missing (Question 2)
- **What P1 proves** (Appendix B, "The PL step"; Appendix C follows the same scheme):
  - (i) h is bi-Lipschitz in the intrinsic metric of each shell. This is shown by local analysis: injective
    differential inside cells, tangent-cone arguments along creases and at their crossings, and **homogeneity** at the
    apex. Global bi-Lipschitz then follows from injectivity and compactness.
  - (ii) The triangulation is shape-regular off the sectors and **radial** on the sector cells. On ordinary triangles
    the per-triangle estimate gives Lip(S − h) ≤ C ω(Dh, mesh)/sin θ_min.
  - (iii) On radial triangles (S − h)(x) = s·e(y), so D(S − h) is constant along rays. This gives Lip(S − h) → 0 up to
    the apex using only that φ is C¹ on each link segment.
  - (iv) Shells are separated by δ > 0.
- **Where Lemma A differs from this.**
  - Its hypothesis "h₀ C¹ with injective differential on each closed triangle" excludes the cone triangles. P1 does
    not prove the lemma in that form.
  - It omits shape regularity of the refinements, the intrinsic metric, and the separation of shells.
  - A fair restatement: *if h₀ is a bi-Lipschitz embedding (intrinsic metric per shell), and |K| has triangulations
    refining the cells, shape-regular where h₀ is C¹ up to the boundary of each triangle, and radial on cone sectors
    where h₀ = p_v + s(φ(y) − p_v) with φ C¹ on each base segment, then fine secant maps are PL realizations.* That is
    P1's argument.
- **What is missing at the apex.**
  - The note says P1 used a "tangent-cone (blow-up)" argument at vertices. It did not. P1 used homogeneity for
    bi-Lipschitz and the radial-triangle estimate (iii) for the secant step.
  - For bi-Lipschitz, the blow-up/homogeneity remark is enough. In P2 it is even simpler than in P1, because λ_v lies
    on the round sphere S_v centred at p_v. h₀ is bi-Lipschitz on the star exactly when the link parametrization φ of
    λ_v is bi-Lipschitz, that is, when λ_v is a simple closed piecewise-C¹ curve with **no cusp** at its corners.
  - For the secant step the remark is not enough. Estimate (iii) is needed, which requires radial triangles on the
    cone sectors whose bases lie on λ_v. Import it explicitly.
- **λ_v corners are not treated anywhere in Step 6.** λ_v has corners where a junction curve b*_f(I_e) meets S_v and
  where a re-trimmed arc meets S_v. There, four sectors meet: two outside pieces and two cone sub-sectors. Two things
  are needed:
  - (1) **No cusp of λ_v.** At a junction point x, the patch and strip half-planes H_f ≠ H_s (E4b) share a boundary
    line J. J is transversal to T_xS_v (V1′a), so H_f ∩ T_xS_v and H_s ∩ T_xS_v are two *distinct* rays ℓ₁ ≠ ℓ₂. The
    same holds at re-trimmed points, using transversality of P_f, P_g along c_e (R′) and c_e being transversal to S_v.
  - (2) **The tangent cone at x is an embedded disk.**
    - The outside sectors lie in the closed outer half-space {⟨·, x − p_v⟩ ≥ 0}. They meet T_xS_v only in ℓ₁, ℓ₂
      (transversality), and each other only along J (E4b).
    - The cone sub-sectors are span⁺(ℓ₁, w) and span⁺(w, ℓ₂) with w = p_v − x normal to T_xS_v. They lie in the inner
      half-space and do not fold, since ℓ₁ ≠ ℓ₂ in T_xS_v.

  Both points are short, and easier than P1's star-shaped case, but they must be written. They also supply the no-cusp
  input to the apex argument.

---

## Minor

**m1. Step 2, rank-2 argument (Question 1).** The conclusion is right, but the justification ("π_e(b*_f) = γ_e, so its
tangential part is nonzero") is not a proof. Write it out:
- With γ_e in arc length, differentiate ⟨b*_f(t) − γ_e(t), γ_e′(t)⟩ = 0. This gives
  ⟨b*_f′, γ_e′⟩ = 1 − ⟨b*_f − γ_e, γ_e″⟩ ≥ 1 − κ|b*_f − γ_e|.
- This is > 0 because |b*_f − γ_e| < reach_e ≤ 1/κ_max.
- So ⟨∂_t X, γ_e′⟩ ≥ 1 − κρ > 0, while ∂_λ X = b*_g − b*_f ∈ Π(t) is nonzero.

The same computation shows b*_f′ ∉ Π(t), which Step 6 uses implicitly. The rest of Step 2 is correct: injectivity
from Federer 4.8(12) with the half-space normal cone at the end points (as checked for P1), the IFT for C¹ (γ_e C²,
β_{f,e} C¹, transversal crossing), and the embedded C¹ band. It needs M1 for a global C¹ selection b*_f.

**m2. Step 3, points of S_v.** At points where S_v meets a junction curve or a re-trimmed arc, the claim needs the
following argument. Each piece, with its boundary curve, is transversal to S_v (V1′a). So each piece ∖ int B_v is
locally a C¹ quarter-disk, a manifold with corners. Two quarter-disks glued along the junction edge form a closed
half-disk with boundary on S_v. State this, and make (V1′a) explicitly cover boundary curves and re-trimmed arcs (see
M2(d)).
- "Nothing else of Σ_out meets B_v (V0′)" holds by the definition of Σ_out, not by (V0′).

**m3. Step 4, the single arc (Question 1).** "Nothing else of P̃_f lies in B_v, since P̃_f is connected and every
other point is outside B_v" is circular. A correct argument:
- A = P̃_f ∩ S_v is one arc (V1′b). Its end points are the two junction (or re-trimmed) points at v. This is forced:
  λ_v is a closed curve made of these arcs, so every end of a face arc must be the end of a chord-arc or of the
  neighbouring face arc. Hence each boundary arc of P̃_f at v crosses S_v exactly once.
- So A is a properly embedded arc in the disk P̃_f and splits it into two disks D₁, D₂. Each Dᵢ ∖ A is connected and
  misses S_v.
- D₁ contains the corner (in int B_v), so D₁ ⊂ B_v.
- D₂ contains another corner of f. It lies in B_w, which is disjoint from B_v (V0′), so D₂ ∩ int B_v = ∅. Regular K
  gives f at least two vertices.
- The same derivation shows that the parts of β_{f,e} outside I_e lie inside the balls. Step 3 needs this, because
  otherwise Σ_out has unglued boundary.
- For the strip: S_v ∩ σ_e must end on *different* junction curves. This follows from the cyclic order in (V1′b);
  say so.

**m4. Step 4, the face cell.** "int Q_f ∪ the two half-strips" should read "the half-strips of all strip edges of f",
plus the face arc on S_v, the halves of the adjacent chord-arcs, and the cone sectors (Step 5). The open edge e should
be the midline (or int c_e) plus the two open cone rays.

**m5. Lemma A.1 coverage (Question 2, second part).** P1's curved-triangle lemma is **Lemma A.1** (Appendix A), not
"Lemma C.1". It covers the strips and the sphere-cut pieces, provided the following is said:
- Strips are triangulated in the (t, λ) chart and patches in the S_f chart. The chart of σ_e is only C¹, but A.1 and
  the secant estimate need only C¹ and a uniform modulus of continuity, which compactness gives.
- Every boundary curve is C¹ regular in its chart:
  - sphere arcs, by the IFT applied to |X − p_v|² − r_v² with nonzero gradient (transversality, V1′a);
  - junction curves, as the coordinate line λ = 0 or 1 in the strip chart and the pcurve image in the patch chart;
  - re-trimmed arcs, by transversal intersection (C²).
- Shared curves get one common parametrization: junction curves by t, sphere arcs by the link parametrization φ (as in
  P1), and re-trimmed arcs by one parametrization of c_e in R³.
- Corners of the pieces (angles in (0, π)) are handled as in P1, with an interior vertex near each corner so that no
  triangle has two curved sides.

The cone sectors are *not* covered by A.1. They need the radial triangulation (M3).

**m6. P1 cross-references.** P2 cites P1 with the wrong appendix letters. The Federer normal-disk argument is in
Appendix B ("Injectivity", not "Appendix A"). The secant/bi-Lipschitz argument is Appendix B ("The PL step") and
Appendix C. The curved-triangle lemma is A.1.

**m7. "No tube radius".** Note 6 says the construction has "no tube radius ρ_e". It still needs
|b*_f − γ_e| < reach_e (E1′), which is a radius condition, though a weaker one than P1's tube separation. Reword.

**m8. E4b.** The condition is correct and sufficient for distinct half-planes. Write it as "the chord direction does
not lie in the closed inward tangent half-plane of P_f at b*_f(t)". The boundary case of the chord lying along the
junction tangent cannot occur, since b*_f′ ∉ Π(t) (m1).

---

## Question 3: zones (Step 1). No error.
- With P1's augmented open zones: chord ends at distance < τ_e from γ_e(t) (E1′, strict), and the open ball is convex.
  So c_e(t) ⊂ B(γ_e(t), τ_e) ⊂ N_{τ_e}(γ_e) ⊂ Z(e).
- The half-strips lie in Z(e) ⊂ Z(f); P̃_f ⊂ P_f ⊂ Z(f); re-trimmed arcs lie in Z(e) by (R′); C_v ⊂ B_v ⊂ Z(v), since
  r_v < τ_v and the closed ball lies in the open one.
- The margin m > 0 exists because h₀(σ̄) is compact in the open Z(σ), and the secant map with triangles subdividing
  cells stays within m.
- Side remark: E1′ is stated for the normal-plane point b*. On sewn data this is ≤ dev_e (and so < τ_e) whenever
  b* lies within reach, because γ_e(t) is then the nearest point of γ_e to b*.

## Question 5: what the checker does not test
Gaps 3 and 4 are already known. In addition:
1. **It checks a different strip (major, part of M4).** `check_vertex` builds strips from boundary points at **equal
   parameter s**, (1 − λ) β_f(s) + λ β_g(s). `edge_crossing` projects the equal-parameter boundary point orthogonally
   onto Π(t). Neither is the theorem's chord [b*_f(t), b*_g(t)] between the points where β_f and β_g *cross* Π(t). So
   L2/L3/L4 are evidence about a neighbouring construction, not about σ_e.
2. **E1′ is not tested.** Neither reach_e nor the transversal crossing of β_{f,e} with Π(t) is computed.
3. **E4a and E4b are not tested.**
   - L4 models each patch by its tangent ray in the normal plane and asks whether the rays cross. That is neither
     E4a (the chord meets the curved patches only at its ends) nor E4b (no fold).
   - For tangent edges (|u_f·u_g| > 0.999) the test is **skipped** and counted as "no crossing". Yet phase 1 notes
     that such patches may overlap as stacked layers, which is exactly where E4a can fail.
4. **V1′a (transversality) is not tested anywhere.**
5. **V1′b is only partly tested.**
   - Face arcs are clustered into one piece (link r/6), but simplicity of each arc is not checked.
   - The strip ends are only required to lie within r/6 of the arc, not to be its end points.
   - The cyclic order of the link is not checked.
   - The separation test masks a neighbourhood of 0.15 r around every re-trimmed joint.
   - The strip part of λ_v is replaced by the straight segment between the two sphere crossings. That segment lies
     inside the ball, not on S_v.
6. **R′ is not tested at all.** c_e is not computed. There is no check that it is a single transversal arc, that it
   lies in Z(e) (P1's B2-type margin), or that its ends lie in the balls. At the vertex, "the arcs cross" is accepted
   when they come within r/6 of each other.
7. **The rest of V0′ is not tested:** pairwise disjointness of the balls, the ends of re-trimmed arcs in the balls,
   and the v-end chords (I_e is never defined in the code). **P0′** (patch embedded) is not tested either.
8. **L3 is local.** It samples only s ∈ [0, 0.3] of each edge and stops at 3 τ_v (this adds to gap 4).

So the phase-1 statement that the strip/cone hypotheses "held at every vertex the sampler could handle" should be
narrowed to "the sampled tests L1–L4 passed", with the list above stated.

---

## Summary
| # | Severity | Where | Issue |
|---|---|---|---|
| M1 | major | §1, E1′, Step 2 | b*_f(t) ill-defined: a closed curve meets a plane an even number of times. Localize to β_{f,e} in a small normal disk; restore E2.2 or a graph condition. |
| M2 | major | §1, R′, V1′, Steps 3–4 | P̃_f ill-defined: c_e does not separate P_f. Add hypotheses (a)–(d). Fix the c_e notation clash. |
| M3 | major | Step 6 | Lemma A misstates P1, whose apex argument is homogeneity plus radial triangles, not blow-up. λ_v corners (no-cusp and four-sector tangent cone) are missing. Repairable as sketched. |
| M4 | major | checker | Tests equal-parameter chords, not normal-plane chords. E1′, E4, V1′a, R′, V0′ (partly) and P0′ are untested. |
| m1 | minor | Step 2 | Write out the rank-2 computation (1 − κρ > 0). |
| m2 | minor | Step 3 | Transversality and corners argument at S_v; V1′a should cover boundary and re-trimmed curves. |
| m3 | minor | Step 4 | Circular single-arc argument; replace with the separation argument. |
| m4 | minor | Step 4 | Face and edge cells listed incompletely. |
| m5 | minor | Step 6 | A.1 covers strips and sphere-cut pieces with stated charts and parametrizations; not the cones. |
| m6 | minor | references | P1 appendix letters are wrong. |
| m7 | minor | Note 6 | "No tube radius" is overstated (the reach condition remains). |
| m8 | minor | E4b | Wording. |

---

## Follow-up on v0.3 (notes/p2_strip_cone_v03.md)

Scope: M1–M3 and m1–m8. M4 (the checker) is out of scope.

**Verdict.**
- **M1:** closed.
- **M3:** closed. The new corner and apex arguments are correct, after one wording fix (N2).
- **M2:** much improved but **not fully closed**. (R′a) is sound. (R′b,c) clash with how Step 4(i) uses them, and one
  hypothesis is missing for faces that have re-trimmed edges (N1). The fix is short.
- **m1–m8:** all addressed.
- **New:** three minor wording points (N3–N5).

### M1: closed
- (E1′) now localizes b*_f(t) to the closed normal disk D(t) of radius ρ_e < min(τ_e, reach_e) on the edge's own arc
  β_{f,e}. It requires a transversal crossing and a single swept sub-arc.
- This gives a global C¹ selection. Uniqueness in the compact D(t) gives continuity (a limit of b*(t_n) lies in
  β ∩ D(t)). The implicit function theorem then gives C¹.
- E1′ is now well posed.
- The rank-2 computation (m1) is correct, with |b* − γ_e| ≤ ρ_e < reach_e ≤ 1/κ. Optional: list "reach ≤ minimal
  radius of curvature for a C² arc" as a standard fact.

### M2: (R′) is mostly sound; one gap remains (N1, major but easy)
- **(R′a)** is sound. q_e ∩ U is one properly embedded arc running from S_v to S_w. It has transversal patches along
  it, transversal crossings of S_v and S_w, and q_e ⊂ Z(e). The renaming to q_e removes the clash with the chords χ_e.
- **N1. The order of definitions in (R′b,c) and Step 4(i) is inconsistent.**
  1. (R′b) says the discarded component "contains the part of β_{f,e} in U and **no other boundary of P_f^U**". But
     P_f^U = P_f ∩ U has boundary arcs on the spheres as well. The discarded sliver between q_e and β_{f,e} always
     contains a piece of P_f ∩ S_v at each end. Read literally, (b) cannot hold. It should say "no other part of
     ∂P_f".
  2. By (R′c), P̃_f ⊂ P_f^U ⊂ U for *every* face (for strip edges "unchanged" means P_f^U). Yet Step 4(i) splits
     P̃_f by A_v(f) and says "the side containing the corner at v lies in int B_v". P̃_f contains no corner, and is
     not yet known to be a disk.
     - The step "P̃_f is a closed disk: P_f^U cut along re-trimmed arcs" assumes that P_f^U is a disk. Nothing proves
       this.
     - "It lies in U because it … contains points of the balls B_w" is self-contradictory, since B_w ⊄ U. The intended
       claim is "lies outside int B_v".
  3. The corner-separation argument must be run on **P_f**, which is a disk by (P0′). For that one needs **P_f ∩ S_v
     to be a single arc** for each vertex v of f.
     - For faces with only strip edges, this follows from (V1′b), because there P̃_f ∩ S_v = P_f ∩ S_v.
     - For a face with a re-trimmed edge at v, (V1′b) only controls P̃_f ∩ S_v. The discarded side could meet S_v in
       further arcs.
- **Suggested repair.** Put this order into (R′) and (V1′):
  - (i) P_f ∩ S_v is one arc A′_v(f), transversal, with ends on the two boundary arcs of P_f at v. Then the separation
    argument on P_f makes P_f^U a closed disk.
  - (ii) q_e ∩ U is a properly embedded arc in that disk with ends on A′_v(f) and A′_w(f), so it splits P_f^U into
    two disks.
  - (iii) The discarded one contains β_{f,e} ∩ U and no other part of ∂P_f.
  - (iv) Then P̃_f is a closed disk, and A_v(f) is the kept sub-arc of A′_v(f), ending at q_e ∩ S_v.

  With this, the mixed-vertex treatment (Steps 3 and 4(iii)–(v); λ_v's corner at q_e ∩ S_v) is sound.
- **Step 4(ii), (iv) and Step 3 "no free boundary"** are correct once (i) is in place. That β_{f,e} outside J_f lies in
  the balls follows from the separation on P_f.

### M3: closed (with N2)
- **The PL step.** The quoted lemma now matches what P1 Appendices B and C prove:
  - bi-Lipschitz in the intrinsic metric of each shell;
  - shape-regular triangles where h₀ is C¹ up to the boundary;
  - radial triangles on the cone sectors with φ C¹ on each base segment;
  - shells at positive distance;
  - the two estimates, including D(S − h₀) constant along rays.

  Triangulating the sectors radially over the vertices of λ_v, which include its corners, matches P1.
- **Lemma A.1 use (m5).** Correct as now stated:
  - strips in the C¹ (t, λ) chart, patches in C² charts;
  - sphere arcs C¹ by the implicit function theorem;
  - common parametrizations on shared curves;
  - an extra interior vertex at corners.
- **Corner of λ_v.**
  - The no-cusp step is correct. H₁ and H₂ are distinct half-planes with common boundary line J ⊄ T_xS_v. Each meets
    T_xS_v in one ray. The rays are distinct: if they coincided, that ray would lie in both planes, so in J, which
    contradicts J ⊄ T_xS_v. If H₁ and H₂ are coplanar (smooth passage), the rays are opposite, which is fine.
  - **N2 (wording, needed for correctness).** The outside part of the tangent cone is **not** H₁ ∪ H₂. Each H_i
    contains the whole line J, including its inward half. The outside pieces are cut by S_v, so their tangent cones
    are the sectors span⁺(j⁺, ℓ₁) and span⁺(j⁺, ℓ₂), where j⁺ is the outward ray of J. With that correction, the four
    sectors are span⁺(ℓ₁, j⁺), span⁺(j⁺, ℓ₂), span⁺(ℓ₂, w), span⁺(w, ℓ₁).
    - The outer pair lies in the closed outer half-space. It touches T_xS_v only in ℓ₁, ℓ₂, because j⁺ is strictly
      outward. The two outer sectors meet only along j⁺ (E4b, or transversality along q_e).
    - The inner pair lies in the inner half-space and does not fold, since ℓ₁ ≠ ℓ₂ and w is normal.
    - So the tangent cone is an embedded disk. As written ("H₁ ∪ H₂, in the outer half-space") the claim is false and
      must be corrected.
- **Apex.** Correct.
  - Since |φ − p_v| = r_v, the identity |aφ₁ − bφ₂|² = r_v²((a − b)² + ab|φ̂₁ − φ̂₂|²) gives the stated comparability
    with |s₁ − s₂| + min(s₁, s₂)|y₁ − y₂| (φ̂ = unit vectors).
  - φ is bi-Lipschitz because λ_v is a simple closed piecewise-C¹ curve without cusps.
  - Homogeneity makes this global on the cone. It also covers the rays over corners of λ_v, which P1 had to treat
    separately.
- The along-junction, along-q_e and along-face-arc bullets are correct. The global step (injective + locally
  bi-Lipschitz + compact) is as in P1.

### m1–m8
All addressed:
- m1: Step 2.
- m2: Step 3, quarter-disks.
- m3: Step 4(i), subject to N1.
- m4: Step 4(v).
- m5: Step 6.
- m6: the appendix letters are now correct (A = A.1, B = Federer and the PL step, C).
- m7: Note 4.
- m8: E4b wording.

### New minor points
- **N3.** Step 1 contains "The reviewer confirmed this step for v0.2." Remove it from any text meant for the paper.
- **N4.** Remaining point 2 lists what the new checker must test, but omits (E4a,b) and (V1′a,b). Gaps 3 and 4 and
  M4's list covered these. Keep the list complete.
- **N5.** Note 4 says (E1′) is "weaker than P1's E1". That is not quite a comparison of like with like. The gain is
  that no tube *separation* between different edges is needed (P1's S1/V-type conditions), not a weaker E1. Suggested
  wording: "a radius condition of the same kind, but with no separation of tubes of different edges".

### Summary
| Item | Status |
|---|---|
| M1 | closed |
| M2 | open in one place (N1): make P_f ∩ S_v one arc a hypothesis, run the separation on P_f, then cut along q_e; fix the "no other boundary" wording |
| M3 | closed, with the N2 correction of the corner tangent cone |
| m1–m8 | closed |
| N2–N5 | minor wording |
