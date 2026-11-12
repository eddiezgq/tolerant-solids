# Referee report: multi-shell r-set argument and Lemma 1 (collar via wfs)

**Inputs audited**
- Text 1: the multi-shell r-set argument.
- Text 2: Lemma 1a/1b, wfs route.
- `wfs_probe.py`.
- Context: `proof_v0.md`, `proof_v0_review.md`.

**Independent checks written for this report**
- `audit/wfs_check.py`, `audit/wfs_check2.py`, `audit/wfs_check3.py`. These use pure numpy/scipy with analytic surface samples, because OCP is not installed here.

**Marking conventions**
- **[verified]**: the statement was read in the source (quoted, with its number).
- **[not verified]**: the source could not be reached or read.
- **[standard, unverified here]**: classical, but not checked against a source in this audit.

## Verdict at a glance

| Item | Verdict |
|---|---|
| Text 1, multi-shell argument | **Correct.** One redundancy, one scope note, one simpler proof available (#1–#4). |
| Lemma 1a statement | **True** for closed PL surfaces. As proved, step (i) is wrong as stated and miscited, step (ii) is miscited, and the "PL upgrade" is not meaningful as stated (#5–#8). |
| Lemma 1b | **Does not deliver the collar hypothesis as written,** because N_r is not PL. Fixable (#9). Two hypotheses are missing: disjointness of the collars and that φ is carried (#10). |
| "wfs unstable / μ-reach" remark | **Correct,** but the μ-reach route degenerates at sharp edges (#11). |
| Expected exact wfs values | **All five are correct.** The L-shape has no exterior critical point (#12). |
| Numerics as sanity check | **Weak.** The matches depend on the grid aligning with the symmetric test shapes. A grid offset of 0.1 makes the probe miss the cube centre entirely, so the probe can **over**estimate wfs (#13–#14). |

---

## Text 1: multi-shell argument

### Issue 1: the argument is correct. Severity: NONE (state two facts explicitly)

**Steps checked:**
- **Shells are separated.** Each G_j (and M_j) is a closed, connected surface, so R³∖G_j has exactly two components, each with frontier G_j [Jordan–Brouwer; standard, unverified here]. Connectedness of each shell is needed here, and it comes from K = ⊔K_i with K_i connected (proof_v0_review #9).
- **Φ(G_j) = M_j for every j, not just shell by shell.** Φ = Φ^1∘…∘Φ^n with pairwise disjoint supports U_i. For i ≠ j, Φ^i is the identity on U_j ⊇ G_j ∪ M_j. Hence Φ(G_j) = Φ^j(G_j) = M_j.
  - Say this explicitly. It also uses M_j = Ψ_j⁻¹(M_j×0) ⊂ int U_j.
- **Sides are preserved.** Φ is a homeomorphism of R³ with Φ(G_j) = M_j, so it maps the two components of R³∖G_j bijectively onto the two components of R³∖M_j.
- **Depth is preserved.** For x ∉ ∪G, the claim "x on the bounded side of G_j ⇔ Φ(x) on the bounded side of M_j" holds for **every** j. Where x lies relative to the collars is irrelevant, because the argument uses only the global homeomorphism Φ and the single surface G_j. So nothing is missing on that point. Depth is preserved pointwise on R³∖∪G.
- **Conclusion.** Φ(O_G) = O_M, where O is the open odd-depth set. Hence Φ(cl O_G) = cl O_M.
- For two realizations, Φ′⁻¹∘Φ maps r-set to r-set and is the end of an ambient isotopy.

**Fix.** Add the one-line justification of Φ(G_j) = M_j for all j, and state that each shell is connected.

### Issue 2: "identity outside a compact set ⇒ unbounded ↦ unbounded" is right, but the hypothesis is not needed. Severity: MINOR

**The stated argument is valid.**
- Pick a ball B containing supp Φ ∪ G_j ∪ M_j.
- R³∖B is connected and lies in the unbounded component of both complements.
- A point x ∉ B has Φ(x) = x. Hence Φ maps the unbounded component W of R³∖G_j to the component containing x, which is the unbounded one.

**Compact support is not needed.** Every homeomorphism of R³ maps a set with compact closure to a set with compact closure. So the bounded component goes to a bounded component, and therefore the unbounded one goes to the unbounded one.

**Fix.** Either keep the argument or replace it with this one line. Removing the support hypothesis makes the r-set statement hold for any homeomorphism Φ with Φ(G_j) = M_j for all j.

### Issue 3: odd depth vs the B-rep convention; regularity. Severity: MINOR (add a remark)

**Agreement with the B-rep convention.** For a valid B-rep the two definitions agree:
- Outer shells have outward normals and void shells have inward normals.
- Disjoint lumps have depth 1.
- A void inside a lump has depth 2.
- A lump nested inside that void has depth 3, which is odd, so it is solid. This is correct.

**Where they differ.** Only when orientations are inconsistent. The odd-depth rule ignores orientation, so it silently "repairs" a mis-oriented void shell. State that orientation consistency is a separate validity check, or that the r-set is **defined** by parity.

**Regular closed: yes.**
- Depth is locally constant on the open set R³∖∪S, so O is open.
- Near any point of S_j, the other S_k are at positive distance, so crossing S_j changes depth by exactly 1. Every point of S_j therefore lies in cl O and in cl E, where E is the open even-depth set.
- Hence R := cl O = O ∪ ∪S_j = R³∖E.
- R is the closure of an open set, so it is regular closed.
- R is bounded, because depth is 0 outside a ball. Its topological boundary is exactly ∪S_j.

If "r-set" means Requicha's r-set (bounded, regular, semianalytic), add that R is semianalytic when the S_j are, which holds for PL shells.

### Issue 4: a shorter, intrinsic proof. Severity: SUGGESTION

**Characterization.** R is the **unique** compact regular closed set with ∂R = ∪S_j.
- Each component of R³∖∪S lies entirely in int R or entirely in ext R.
- Two components adjacent across S_j cannot lie on the same side. Otherwise points of S_j would be interior or exterior points, not boundary points.
- The adjacency graph is connected, because R³ is connected.
- The unbounded component is exterior.
- Hence the 2-colouring is forced.

**Consequence.** Φ(R_G) is compact and regular closed, with ∂Φ(R_G) = Φ(∪G) = ∪M. By uniqueness, Φ(R_G) = R_M. No depth bookkeeping is needed.

### Scope note for Text 1

"The homeomorphism Φ obtained above" exists only under Lemma 3, so every shell must have genus ≥ 1. Shells that are spheres are not covered.

---

## Text 2: Lemma 1

### Sources actually read

**S1. Chazal & Lieutier, "Stability and computation of topological invariants of solids in Rⁿ", DCG 37:601–617 (2007), doi 10.1007/s00454-007-1309-8** [verified, via Springer PDF text]
- **Prop. 3.4 (isotopy lemma).** *"If 0 < ρ1 < ρ2 are such that Oρ1\Oρ2 does not contain any critical point of R, then all the levels R⁻¹(ρ), ρ ∈ [ρ1, ρ2], are homeomorphic topological manifolds and Oρ1\Oρ2 = {x ∈ O: ρ1 ≤ R(x) ≤ ρ2} is homeomorphic to R⁻¹(ρ1) × [ρ1, ρ2]. As a consequence, Oρ1 and Oρ2 are homeomorphic and thus homotopy equivalent."*
  - Here O is a **bounded open** set and R(x) = d(x, Oᶜ).
  - O_d is defined as {R > d}. The displayed shell {ρ1 ≤ R ≤ ρ2} uses closed bounds, so the paper's endpoint convention is slightly inconsistent. This is harmless.
- **Def. 3.1.** wfs(O) is the distance between Oᶜ and the set of singular points of ∇.
- **Lemma 2.2.** *"A point x is a singular point of ∇ if and only if it lies in the convex hull of"* Γ(x).
- **Prop. 3.6.** *"Let O ⊂ Rⁿ be a subanalytic bounded open set. The set of critical values of R … is finite. In particular, wfs(O) > 0."* The paper credits the semialgebraic case to Fu [p. 1045].
- **§4.3.** *"The wfs of a compact subset K of Rⁿ is the wfs of its complement Rⁿ\K … one can define its wfs in the same way as for bounded open sets."*
- **Warning in the paper:** *"the homology groups of K and the homology groups of its thickenings are not always the same."* So K ↪ K^ε is **not** covered by wfs theory.

**S2. Chazal, Cohen-Steiner & Lieutier, "A sampling theory for compact sets in Euclidean space", DCG 2009** [verified, via scispace PDF text]
- **§2.1.** Θ_K(x) is the centre of the smallest ball enclosing Γ_K(x), equivalently the point of conv Γ_K(x) nearest to x. ∇_K(x) = (x − Θ_K(x))/R_K(x), and ‖∇_K‖² = 1 − F_K²/R_K².
- **§2.2.** *"wfs(K) … infimum of the positive critical values"*; *"wfs(K) may be equal to zero."*
- **Lemma 2.1.** *"If 0 < α, β < wfs(K), then Kα and Kβ are homeomorphic and even isotopic. The same holds for the complements."* It cites Chazal–Lieutier [6], not Grove.
- **Def. 4.3.** r_μ(K) = inf{d | χ_K(d) < μ}.

**S3. Grove 1993** [not verified directly; the paper was not reachable]
- Secondary statement from Chazal & Michel, arXiv:1710.04019, Lemma 1 "(Isotopy Lemma)", credited to Grove (1993). For a distance-like φ with r1 < r2 and no critical point in φ⁻¹([r1, r2]): *"all the sublevel sets φ⁻¹([0, r]) are isotopic for r ∈ [r1, r2]."*
- This is **isotopy of sublevel sets**. It does not state a product structure for the shell.

**S4. Chazal & Lieutier, "The λ-medial axis", Graphical Models 67(4):304–331 (2005)** [not verified]
- Only the bibliographic record was reachable. Its content was not checked.

**S5. Lieutier, CAD 36 (2004)**
- Gives homotopy equivalence of an open set with its medial axis. That is homotopy only, and does not bear on a product structure. [content not re-read here]

**S6. Durfee, "Neighborhoods of algebraic sets", Trans. AMS 276 (1983)** [verified, via scispace PDF text, OCR partly garbled]
- **Def. 3.1.** A semialgebraic rug function is a proper semialgebraic a: M → R, with a ≥ 0 and a⁻¹(0) = X, where X is compact.
- **Def. 3.4.** T = a⁻¹[0, δ] for *"a suitably small positive number δ"*. No explicit bound is given.
- **Prop. 3.5.** For two such neighborhoods there are homeomorphisms h_t of M with h₀ = id, *"h_t|X is the identity, for all t"*, and h₁(T₁) = T₂.
- **Prop. 3.7.** *"suppose that T is a PL regular neighborhood of X in M. Then T is a semialgebraic neighborhood of X in M"*. Here X ⊂ T ⊂ M are finite simplicial complexes.

### Issue 5: Lemma 1a is true, but step (i) is false as stated and has no citation. Severity: MAJOR (proof gap; repairable)

**What is wrong.**
- "N_ε(M) is a regular neighbourhood" is **false as stated**. N_ε is not a polyhedron: its boundary has spherical and cylindrical patches at vertices and convex edges.
- "Homeomorphic to one" is true, but it is not a "standard" consequence of the wfs theory. S1 warns explicitly that K and its thickenings can differ.

**Repair (Durfee).**
- For a compact polyhedron M, d_M is semialgebraic (Tarski–Seidenberg) [standard, unverified here]. It is proper, nonnegative and has zero set M, so it is a semialgebraic rug function.
- Take the ambient space to be a large simplicial cube, because Prop. 3.7 needs a finite complex.
- For small δ, Prop. 3.5 and Prop. 3.7 then give N_δ(M) ≅ R **rel M**, where R is a PL regular neighbourhood.
- For a closed, two-sided, locally flat PL surface, R ≅_PL M×[−1,1] with M = M×0 [regular neighbourhood theory, Rourke–Sanderson; standard, unverified here].
- Durfee's δ is unquantified. That is harmless, since (ii) carries it up to any r < wfs.

**Also state:** wfs(M) > 0 for a PL surface, by S1 Prop. 3.6 (subanalytic) or Fu (semialgebraic). Prop. 3.6 is stated for bounded open sets, so apply it as in #6.

### Issue 6: step (ii) is miscited, and needs a word on applying it to unbounded or compact sets. Severity: MINOR

**Citation.**
- The **product** statement N_b∖int N_a ≅ ∂N_a×[a, b] and "levels are topological manifolds" are S1 **Prop. 3.4** (DCG 2007).
- Grove 1993, as quoted in S3, gives isotopy of sublevel sets, not a product.
- CCSL 2009 Lemma 2.1 gives "homeomorphic and even isotopic" offsets, also not a product.
- The λ-medial-axis paper is unverified.
- **Fix:** cite Chazal–Lieutier DCG 2007, Prop. 3.4.

**Ranges.**
- Prop. 3.4 is stated for 0 < ρ1 < ρ2 with no critical point in the closed shell. Lemma 2.1 of S2 is stated for 0 < α, β < wfs, so α = β is allowed trivially.
- The text's ε ≤ a < b < wfs is therefore fine.

**Answers to the specific questions.**
- **Does it give a product, or only isotopy or homotopy?** S1 gives the **product**. Grove and S2 give only isotopy or homeomorphism of the offsets.
- **Is ∂N_a a topological 2-manifold for 0 < a < wfs?** **Yes**, by Prop. 3.4 with ρ1 = a < ρ2 < wfs.
  - Add one line: ∂N_a = d⁻¹(a). The inclusion ⊆ always holds. Equality holds because a point with d = a that is not in cl{d > a} is a local maximum of d, hence critical.

**Applying Prop. 3.4 to a compact M.**
- **Inside component:** apply Prop. 3.4 to O_in, where R = d_M exactly.
- **Outside component:** apply it to O = B(0, ρ)∖M with ρ large. The extra critical points created by the sphere have values of order ρ/2, far above the shell.
- Alternatively, rely on the §4.3 extension in S1, which is stated without proof.

### Issue 7: combining (i) and (ii). Severity: MINOR (missing lines)

N_r = N_ε ∪ (shell). Two points have to be said:
- **(a) Matching the boundaries.** Prop. 3.4 gives some homeomorphism shell ≅ S×[ε, r]. It must send S×ε to ∂N_ε, which holds after composing with a flip on each component. Then reparametrize by the restriction to S×ε, so that the inner end is the identity.
- **(b) Absorbing the collar.** Attaching an outer collar to N_ε ≅ M×[−1,1] gives a manifold homeomorphic to N_ε, by a homeomorphism fixed near M [Brown's collaring theorem; standard, unverified here].

The result is N_r ≅ M×[−1,1] with M ↦ M×0, so the claimed pair homeomorphism **is** obtained, topologically.

### Issue 8: "upgrade to PL by Moise" is not meaningful as written. Severity: MAJOR (affects Lemma 1b)

**The problem.** N_r is not a polyhedron, so "N_r ≅_PL M×[−1,1]" has no meaning. But the collar hypothesis of proof_v0 (Lemma 2′) needs a **compact PL submanifold** U ⊂ R³ and a PL homeomorphism Ψ with Ψ(M) = M×0. Waldhausen (Lemma 3) works in the PL category.

**Repair.**
1. int N_r is an open subset of R³, hence a PL 3-manifold. By invariance of domain and #7, it is homeomorphic to M×(−1,1).
2. By Moise (3-manifolds have unique PL structures; noncompact manifolds are allowed) [standard, unverified here], there is a PL homeomorphism Ψ: int N_r → M×(−1,1).
3. N_d is compact, so N_d ⊂ Ψ⁻¹(M×(−c, c)) for some c < 1. Set U′ := Ψ⁻¹(M×[−c, c]). It is a compact PL submanifold, PL ≅ M×I.
4. Ψ(M) need **not** be M×0. Do not ask for that. Instead:
   - M ↪ U′ is a homotopy equivalence (two-of-three, using M ↪ int N_r and U′ ↪ int N_r).
   - So M is π₁-injective and not a sphere, hence incompressible.
   - Apply Lemma 3 to G **and** to M, isotope both to Ψ⁻¹(M×0), and compose.
5. Consequently, Lemma 2′ and Lemma 3 should take the weaker collar hypothesis: U is compact PL, U ≅_PL F×I, zones ⊂ int U, the reference M ⊂ int U is PL, and M ↪ U is a homotopy equivalence.

### Issue 9: Lemma 1b does not prove the collar hypothesis as written. Severity: MAJOR (repaired by #8)

- **What is correct.** Zones ⊂ N_d ⊂ {d_M < r} = int N_r for r < wfs, by the local-maximum argument in #6.
- **What is missing.** U = N_r is not PL, and there is no PL Ψ with Ψ(M) = M×0. With #8, the corrected statement is:
  - If d < wfs(M), then there is a compact PL U′ with N_d ⊂ int U′, U′ ≅_PL M×I, and M ↪ U′ a homotopy equivalence.
  - This is sufficient for the weakened Lemma 2′ and Lemma 3.

### Issue 10: Lemma 1b omits two hypotheses the theorem needs. Severity: MAJOR (sufficiency)

- **(a) Disjoint collars.** Disjointness needs r_i + r_j < dist(M_i, M_j), because N_a(A) ∩ N_b(B) ≠ ∅ iff dist(A, B) ≤ a + b.
  - Using per-shell wfs(M_i) does not see the other shells.
  - Simplest fix: require d < wfs(∪M_j). If two offsets touched at some r, the midpoint of a closest pair would be a critical point of value dist/2 ≤ r. So r < wfs(∪M) forces disjointness.
  - This is stricter: it also bounds wall thickness between nested shells.
- **(b) φ_i carried by C.** The reference embedding must satisfy φ_i(σ̄) ⊆ C(σ) for every σ. This does not follow from d < wfs.
  - It is automatic if each nominal open cell lies in its own zone.
  - Otherwise list it as a separate check.

### Issue 11: the instability / μ-reach remark. Severity: MINOR (practical caveat)

**What is correct.**
- wfs is not continuous under Hausdorff perturbation. S2 §2.2: *"may be equal to zero"*.
- r_μ ≤ wfs, because critical points have χ = 0 < μ. So a positive μ-reach is a valid lower bound.

**The caveat.** On a PL surface, points on the bisector of an edge with dihedral angle α (measured on the side considered) have |∇d| = sin(α/2), arbitrarily close to M.
- Hence r_μ(M) = 0 for every μ ≥ min_e sin(α_e/2), and vertices add further constraints.
- The μ-reach route therefore needs μ < sin(α_min/2), and the CCSL sampling constants degrade as μ → 0.

**Recommendation.** For an exactly known PL reference M, compute wfs(M) itself exactly (#14) and use μ-reach only for approximated M.

**Sharp dihedral angles.**
- They do **not** give a counterexample to Lemma 1a. The proof in #5–#7 holds for every closed PL surface, and wfs stays > 0.
- They do break the numerics (#13).

---

## Numerics

### Issue 12: the expected exact values are all correct. Severity: NONE

| Shape | Value | Reason |
|---|---|---|
| Box | a/2 | Exterior of a convex body: nearest point unique, so \|∇\| = 1. Interior: the only critical point is the centre. A non-cube box would give min side/2. |
| Cylinder | min(R, H/2) | If H/2 < R: mid-plane saddles with value H/2. If R < H/2: axis points with Γ = a circle, value R. Rim-edge bisector has \|∇\| = sin 45°. |
| Plate | t/2 | Same as box. |
| Filleted box (r = 2) | 5 | Equal-radius fillets make it close to the Minkowski sum of a cube of side 6 and B(2). Centre value 2 + 3 = 5. |
| L-shape (L = 10, w = 2) | 1 | See below. |

The filleted box assumes OCC's vertex blend is spherical for equal radii [not verified].

**L-shape interior.** Arm-axis points have Γ = 4 feet, value 1. The corner cube centre (1,1,1) is also critical with value 1 (segment (1,1,0)–(1,1,2)). Every interior point has d ≤ 1.

**L-shape exterior: no critical point.**
- Critical points lie in conv(K) = (pentagon)×[0, 2].
- In the notch, Γ(p) lies in the plane z = p_z, because the top and bottom faces do not cover the notch. So the problem reduces to the 2D polygon.
- In 2D, the candidate pairs are face/face, face/corner and corner/corner. Each forces p to be the midpoint of its feet, and each fails. Example: p = (10,10) has Γ = {(10,2), (2,10)}, whose midpoint (6,6) ≠ p.
- At the reflex edge, the bisector gives |∇| = sin 45°.

**Numerical confirmation** (`wfs_check.py`, z-slices 0.6 / 1.0 / 1.4 / 2.6):
- Exterior minimum estimated |∇| = 0.47.
- Interior points flagged below 0.08: minimum d = 1.000.

### Issue 13: the probe is not a sound sanity check as built. Severity: MAJOR (for any use beyond these five shapes)

The gradient formula is right (S2 §2.1). The discretization is not.

**(a) Grid-alignment artefact: misses true critical points, so wfs is overestimated.**
- Off the medial axis the true |∇| = 1. The probe flags a grid point only if Γ_η = {samples within d + η} reaches the second sheet, which needs offset ≲ η/2.
- With η = 2·spacing ≈ 0.02–0.08 and h = 0.1–0.25, detection works only when grid nodes land on the symmetry planes. They do for axis-aligned test shapes whose bounding box starts on the grid.
- `wfs_check3.py` (cube a = 10, h = 0.25, η = 0.078), with the same algorithm:

  | Grid offset | Min estimated \|∇\| | Flagged min d |
  |---|---|---|
  | 0.0 | 0.003 | 5.000 |
  | 0.03 | 0.007 | 4.970 |
  | **0.1** | **0.413** | **none (∞)** |

- So "matches the exact value" is partly built into the test design. On a general part the probe can miss the smallest critical value, which is the unsafe direction for d < wfs.

**(b) η-inflation bias: false positives.**
- At p = (2.4, 2.4, 1.4) outside the L reflex edge, the true |∇| is 0.707. The probe returns **0.474**.
- This is not a Bădoiu–Clarkson error: 60, 600, 6000 and 60000 iterations all give 0.470–0.474.
- It is the MEB of the two inflated discs, of radius √(2dη) ≈ 0.13 at d = 0.4. The relative error is about √(2η/d), which exceeds thr = 0.08 everywhere d < 2η/thr² ≈ 300η.
- At a sharp edge, sin(α/2) < 0.08 already for α < 9.2°, so any dihedral angle below about 9° is flagged as "critical" even with exact Γ.

**(c) Values below 2h are never examined** (keep = d > 2h): below 0.5 for the box and 0.4 for the L-shape. Small-wfs features, which are the ones that matter, are invisible.

**(d) Bădoiu–Clarkson after 60 iterations** had centre error of at most 0.037·radius on my two-cluster test, so it is not the dominant error. Its worst-case bound is about r/√k ≈ 0.13 r, which is above the threshold, so an exact MEB is still preferable.

### Issue 14: recommended replacement. Severity: SUGGESTION

For a PL reference M, compute wfs **exactly**.
- A critical point p satisfies p ∈ conv Γ(p). By Carathéodory, |Γ| ≤ 4 suffices.
- Enumerate tuples of 2–4 features (faces, edges, vertices) and solve the equidistance system together with the "p in hull of feet" condition.
- Keep the candidates whose nearest-feature check passes.
- Use exact or interval arithmetic. This is O(n⁴) in the worst case, and can be pruned with a bounding-volume hierarchy.

If the grid probe is kept:
- Randomize the grid offset and report the minimum over offsets.
- Take η ≥ √3·h, so that every grid cell's critical point is seen. This gives a conservative (low) estimate.
- Replace Bădoiu–Clarkson with an exact MEB (Welzl) or a nearest-point-of-hull QP.
- Label the output an "upper-bound-risk heuristic", never a check that certifies d < wfs.

---

## Summary of fixes

1. **Text 1:** add Φ(G_j) = M_j for all j and connectedness of the shells. Optionally drop the compact-support hypothesis (#2) or use the uniqueness characterization (#4). Add the orientation remark (#3). Restrict to genus ≥ 1.
2. **Lemma 1a:**
   - Replace (i) with Durfee 1983 Props. 3.5 and 3.7 plus regular-neighbourhood theory.
   - Cite Chazal–Lieutier DCG 2007 Prop. 3.4 for (ii).
   - Add the two gluing lines (#7).
   - Drop "upgrade to PL" in favour of #8.
3. **Collar hypothesis (Lemma 2′/3):** weaken to "U compact PL ≅ F×I, M ↪ U a homotopy equivalence". Apply Lemma 3 to G and to M separately.
4. **Lemma 1b:** conclude the weakened hypothesis. Add the disjointness condition (r_i + r_j < dist, or d < wfs(∪M)) and the check that φ is carried.
5. **Numerics:** do not treat the matches as evidence of correctness on general parts. Prefer exact wfs for PL M.
