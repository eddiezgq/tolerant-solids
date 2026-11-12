# Referee report: P1 draft v0.1 ("When does a tolerant B-rep define a solid?")

Independent referee, 2026-11-12. Draft not edited.

**Inputs read**
- `paper/p1.tex` and every `paper/sec_*.tex` file.
- `README.md`.
- `notes/uniqueness_v01.md`, `notes/lemma0_v02.md`, `notes/lemma0_v03.md`, `notes/cone_lemma.md`, `notes/lemma0_check_report.md`, `notes/task6_claims.md`.
- Every report in `notes/reviews/`.
- `results/*.json` and `results/cert*.txt`.
- The Lean sources in `lean/Tolerant/`.
- The session literature notes, read-only: `lit_*.md`, `read2_*.md`, `read3_*.md`, `audit/cite_audit_local.md`, `audit/cite_audit_web.md`, `audit/math_audit.md`, `audit/stewart_zidani2008.txt`, and the local `occdoc/` copy.

**Independent checks done for this report**
- **Lean axioms.** I re-ran `lake env lean Axioms.lean` on the scratchpad copy, which is byte-identical to `lean/Tolerant/*.lean`. Output: `propext, Classical.choice, Quot.sound` for all five theorems listed. `grep sorry` finds nothing.
- **JSON values.** I recomputed from the result files the numbers quoted in §4.3 and §7: the exp6c table, the offset volumes against `summarize_occ.py`'s exact formulas, the cusp-vertex count, the route-G vertex ratios, and the obstruction and re-intersection margins.

**Severity scale**
- **fatal:** a stated result is false or cannot be repaired locally.
- **major:** an overclaim, a proof gap, or a fact/number/citation that must change before circulation.
- **minor:** wording, missing detail, or a small mismatch.

## Verdict

**No fatal error.** The uniqueness argument (§3), the cone lemma and its corollary (§4.2), Proposition B and the obstruction theorem (§6) are faithful to their reviewed notes and are correct as far as I can check.

**The draft does not yet meet the project rules in three places.**
1. **The "collar condition is computable" chain (Lemma 4.1) is stated more strongly than anything proved.** The review of Lemma 1 found that part (a) is not meaningful as a PL statement, and that part (b) does not deliver the collar hypothesis of §3. The draft note understates this.
2. **Theorem 5.1 (fans and cones) is presented as a proved theorem, but it is an outline.**
   - Its hypotheses are summarized, not stated.
   - Two of them are non-local, yet the abstract calls them "computable local".
   - The paper says V1(b) and P0 were "checked computationally"; the check report says they were not checked.
   - A gap the reviews left open (the apex estimate) is not mentioned.
   - The review history is misreported.
3. **Several numbers and citations do not match the repository.**
   - "9 cusp vertices" is wrong: the results show 2.
   - The sewn-plate face margin and the face margins in Table 3 are not in `results/`.
   - The OCC "small enough" quotation has no source.
   - The dREG22 title is wrong.
   - The 2006 ASZ paper is listed as "not yet read", but the session notes record a PDF-checked reading.
   - The related-work section omits papers the notes flag as directly relevant to the novelty claims.

---

## A. Overclaims

### 1. Lemma 4.1 (collar): part (a) is meaningless as a PL statement, and part (b) does not deliver §3's collar condition. Severity: MAJOR
**Location:** `sec_collar.tex` lines 10–31. The claim is repeated in `p1.tex` lines 46–47 ("The collar condition reduces to a distance bound…") and `sec_intro.tex` lines 33–35.

**Problem.** `notes/reviews/lemma1_multishell_review.md` found:
- **Issue 8 (MAJOR):** N̄_r(M) is not a polyhedron, so "N̄_r(M) is PL-homeomorphic to M×[−1,1]" has no meaning.
- **Issue 9 (MAJOR):** (b) therefore does not prove the collar condition of §3. That condition needs a compact PL U_i, a PL homeomorphism with M_i×{0} the image of φ_i, and the zones in int U_i.
- **Issue 5 (MAJOR):** step (i) is false as stated. It is repaired by Durfee Props. 3.5 and 3.7 *plus* Tarski–Seidenberg (d_M is semialgebraic), an ambient finite complex, and regular-neighbourhood theory.
- **Issue 7:** two gluing lines are missing.

The draft note at line 29 says only that "the PL … form of (a) also needs a sentence". That understates a structural problem. The review's repair changes the *hypotheses of §3*, and neither `uniqueness_v01.md` nor the paper has made that change. As written, the abstract's claim that the collar condition "reduces to a distance bound below wfs" is not proved.

**Fix.**
1. **Weaken the collar condition** in §3 (lines 7–14) as review #8 recommends: U_i is compact PL, U_i ≅_PL M_i×I, the zones lie in int U_i, the reference φ_i(|K_i|) ⊂ int U_i, and φ_i(|K_i|) ↪ U_i is a homotopy equivalence (not necessarily a level).
2. **Change the proof of Lemma 3.3:** apply it to both G and φ_i(|K_i|), isotope both to Ψ⁻¹(M×0), and compose.
3. **Restate Lemma 4.1** so that (a) is topological, (a′) gives a compact PL U′ ⊂ int N_r with N_d ⊂ int U′ via Moise's uniqueness of PL structures (mark it `\unverified` until checked), and (b) concludes the weakened condition.
4. **Mark the remaining gaps.** Until all this is written, mark Lemma 4.1 visibly as unproved with `\draftnote`, and soften the abstract and intro.

The Moise citation is already on the "to check" list in `sec_open.tex`.

### 2. Theorem 5.1 (fans and cones): stated as a theorem, with an outline that does not carry it. Severity: MAJOR
**Location:** `sec_existence.tex` lines 18–56; `p1.tex` line 49; `sec_intro.tex` lines 37–41.

Compared with `notes/lemma0_v02.md` (§§0–5) and `notes/lemma0_v03.md` §1, there are seven problems.

**(a) The hypotheses are not stated.** Line 19 defers "the full statements, with the constants" to the repository. A theorem whose hypotheses live in a repository is not a theorem of the paper. Lossy points in the summary:
- **E2** is stated as its conclusion ("crosses … exactly once"). v0.2 E2 is a list of sufficient conditions, E2.1–E2.3. The proof uses E2.3 (no return) directly: Q_f ∩ F_{f,e} = k_{f,e} (v0.2 §4, cell structure (b)). E2.3 is not a hypothesis of the paper's theorem.
- **E1 and E2** must hold on the exposed stubs [t_v, a_e] and [b_e, t_w], not only on [a_e, b_e] (v0.2 E2, first line). This range is not stated.
- **ρ_e constant near a_e and b_e.** v0.3 A′ requires ρ_e to be constant *on a neighbourhood of a_e and b_e* as well as on the stubs. The quarter-space argument at k(a_e) uses ρ_e′(a_e) = 0. The paper (line 23) states only "constant on the stubs".
- **P0** also requires P_f to be embedded and P_f ∩ (⋃T ∪ ⋃W) to be a collar of ∂P_f. The paper keeps only "is a disk".
- **S1** has six parts, (a)–(f). The proof uses S1(f), that T_e ∩ W_v = D_e(a_e), which the summary omits.
- **Setting.** The theorem does not say whether K must be regular. v0.2 §0 assumes regularity, and §6 lists how E3′ and P0 change for seams, closed edges and inner wires. `sec_setting.tex` line 8 says instead that "the existence constructions work directly on B-rep complexes".

**(b) "Computable local hypotheses" (abstract, `p1.tex` line 49) is false.**
- v0.2 states: "V1 and P0 are non-local hypotheses that are checked computationally; they are not derived from local data."
- The v0.1 review (item 1) calls V1(b) and P0 "topological assumptions that nothing computable implies".

**(c) "Checked computationally" is contradicted by the check report.**
- Lines 32 and 34 say V1(b), S1 and P0 "are checked computationally".
- `notes/lemma0_check_report.md` §1: "Not checked: E2.3 beyond what S1(d) covers, S1(e) for adjacent faces, P0, V1(b)." The README repeats the paper's wording, so it is stale as well.
- These hypotheses hold only on the gapped cube, and only implicitly there: the exact embedding check of the constructed surface implies them.

**(d) A known open gap is not flagged.**
- `lemma0_v03.md` status: "Still open from the reviews: the curvature κ_λ quoted in the apex estimate of v0.2 §5 (λ_v is only C¹)".
- `lemma0_v031_review.md` #23 says the same.
- Step 6 of the outline (line 51, the PL step) depends on that estimate. The paper says nothing about it.

**(e) The review history is misreported.** Line 55 says "Two independent reviews of v0.2 and three of v0.3 found no fatal error."
- The two reviews were of v0 and v0.1 (`lemma0_v0_review.md`, `lemma0_v01_review.md`); v0.2 is the revision made after them.
- The v0 review found a **fatal** error (1a, the tube–ball gap), later fixed.
- The v0.3 reviews (`lemma0_v03_review.md`, `lemma0_v031_review.md`, the code review, the B′ review) covered Lemma O, Propositions B and B′, and the A′/E3′ changes. None of them re-reviewed the v0.2 §4–§5 proof as a whole.

**(f) "Proof outline" is not visibly flagged.** The heading "Construction and proof outline" is the only marker. The abstract ("We prove three kinds of results") and the intro present the theorem as proved.

**(g) The checker does not implement A′ as stated** (`lemma0_v03.md` §1, "Checker status"). The draft flags this only in Table 3's footnote.

**Fix.**
- State every hypothesis in the paper: E1, E2.1–E2.3, E3/E3′, V0, V1(a)/(b), S1(a)–(f), P0 and strictness, the ranges including the stubs, ρ_e constant near a_e and b_e, and the setting (regular K, or the §6 modifications).
- Either include the full proof (v0.2 §4–§5 with the v0.3 changes and the cell-structure argument), or relabel the result "Theorem (conditional; proof outline)" with a `\draftnote` that the PL step has an open gap at the apex (κ_λ).
- Replace "computable local hypotheses" with "computable local hypotheses together with two non-local hypotheses (V1(b), P0)".
- Delete "these are checked computationally" for V1(b), P0 and S1(e). Say they were verified only on the gapped cube, through the exact embedding check.
- Remove the review-count sentence from the proof. If it is kept anywhere, state it correctly.

### 3. Proposition 5.3 (B′): the proof is presented as complete, but the notes call it a sketch. Severity: MINOR
**Location:** `sec_existence.tex` lines 80–112.

**Problem.**
- `lemma0_v03.md` §2′ labels the proof "sketch; it reuses v0.2 §5". It relies on a shape-regular curved triangulation and a secant estimate, and on the same §5 machinery as finding 2.
- The remark at lines 103–112 says the hypotheses "are then checked on samples". It omits two caveats in the notes: "the PL step is not carried out; the vertex part of T is not checked". On the cylinder and pipe, the seam vertices lie on two surfaces only and need exactly that general tangent-cone clause (notes §2′, T).

**Fix.**
- Label the proof a sketch.
- In the remark, state that the vertex part of T was not checked, and add "(edge part of T only)" to every "pass (curved)" entry in Table 3.

### 4. Uniqueness is overstated in the abstract and intro. Severity: MAJOR
**Location:** `p1.tex` line 45 ("all realizations are ambient isotopic"); `sec_intro.tex` line 28 ("any two realizations are ambient isotopic").

**Problem.** Theorem 3.4 proves that the *images* are ambient isotopic. `sec_open.tex` item 2 and Remark 3.5 say explicitly that isotopy of embeddings is not proved.

**Fix.** Write "the images of any two realizations are ambient isotopic". Add the two hypotheses the summaries omit: the reference surface is carried, and the collars are pairwise disjoint.

### 5. The novelty claim for existence is contradicted by literature the session has read. Severity: MAJOR
**Location:** `sec_intro.tex` lines 88–90 ("derive the embedding from checkable hypotheses … As far as we have read, this is new").

**Problem.**
- `audit/cite_audit_local.md` (Milenkovic 1988, AI 37): Milenkovic proves existence of an exact realization in 2D with a uniform ε (p. 388; Thm 6.3). The audit says to "exempt Milenkovic".
- Andersson–Stewart–Zidani 2006 (CAGD 23:599–611) was read with its PDF checked (`read2_B.md` §4). Its Thms 4.1/5.1 derive injectivity of composite parametric patches from checkable conditions, by a degree argument close to Steps 2–3 of Theorem 6.1.
- So "as far as we have read" is false as worded, and "remains to be checked against … the 2006 ASZ paper" (line 90) is stale.

**Fix.** Narrow the claim to "3D B-reps with per-cell (vertex/edge/face) tolerance zones, and the embedding of the whole cell complex". Cite Milenkovic 1988 (2D, uniform ε) and ASZ 2006 (single composite patch, common parameter domain; their §3.7 says separately trimmed B-rep faces need extra inside/outside information) as the closest prior results.

### 6. The related-work section omits the closest isotopy results. Severity: MAJOR
**Location:** `sec_intro.tex` lines 58–91.

**Problem.** The session notes record full-text readings of at least four directly relevant results:
- **Chazal–Cohen-Steiner 2005** (GM 67(5):390–404), verified in `cite_audit_web.md` line 114. Thm 2.1: if S′ is homeomorphic to S, lies in a thickening of S and separates its sides, then S′ is isotopic to S; smoothness is not required. This is essentially the topological content of Lemmas 3.2–3.3, with "separates" in place of "π₁-isomorphism".
- **Sakkalis–Peters–Bisceglio 2004** (CAD 36:1089–1100), Thm 10: ambient isotopy inside a normal tube for smooth closed surfaces. The authors point to APS 2000 for sharp, multi-patch features.
- **Chazal–Cohen-Steiner–Lieutier 2009** (Comput. Geom. 42:566–581), Thms 4.2/4.3: isotopy of offset level sets of general compact sets under Hausdorff perturbation, with explicit μ-reach constants.
- **Shapiro 2008.** The paper describes it only as "studies homotopy conditions". `audit/math_audit.md` (around line 256) records that Shapiro gives conditions for ⋃Z ≃ |K| (Thms 1–2) and names separation/isotopy with containment as open (§5.2, p. 178). That is the gap this paper addresses.

The novelty sentence for Theorem 3.4 ("the new part is the set-up") is therefore not yet supported against the literature the project has itself read.

**Fix.** Add these four, each checked against the notes cited above. Position Theorem 3.4 relative to Chazal–Cohen-Steiner 2005 in particular: per-cell zones, a cell-respecting realization, the collar from wfs, and π₁ in place of separation. Also add Hoffmann–Stewart 2005 or ASZ 2007 for the term "realization S ⊨ Δ" (`read3_ASZ2007.md` §7 recommends this).

### 7. "Certified" is used without its qualifiers. Severity: MINOR
**Location:** `sec_intro.tex` line 35; `sec_collar.tex` lines 70–81; Table 2.

**Problem.** The bound is certified only:
- up to floating point;
- up to the containment tolerance, so the statement is strictly "no critical value in (c·tol, LB)" (`cone_lemma.md`, revisions);
- up to the search cut-off R (`wfs_cert2.py` docstring, "up to the cut-off R").

**Fix.** State all three qualifiers wherever "certified" first appears.

### 8. The OpenCascade findings are stated more strongly than the data show. Severity: MINOR
**Location:** `sec_intro.tex` line 52; `sec_experiments.tex` lines 31–32.

**Problem.**
- **"Misses models whose tolerances exceed the weak feature size."** Only the pipe at τ = 1.3 is shown to have non-isotopic realizations. For the long cylinder, exp6c shows only τ ≥ wfs(nominal).
- **"Collar condition fails for the nominal surface"** (line 32). `task6_review.md` (6c "fails") says this proves only τ ≥ wfs(nominal), "not that Lemma 1b's hypothesis fails … and not non-uniqueness", and asks for the label to be changed.
- **"Collar condition certified"** (line 31). The same review: the carrier condition is not checked, and defl must be the measured face-to-mesh distance. `exp6c.py` still uses the requested deflection.

**Fix.**
- Relabel the two entries "τ + defl < certified LB(M_PL)" and "τ ≥ wfs(nominal) (exhibited critical point)".
- Reword the intro to "accepts models with τ above wfs(nominal), including a pipe with two non-homeomorphic realizations".

---

## B. Mathematical errors or gaps introduced in condensing

### 9. The subdivision of non-regular B-rep complexes is not specified. Severity: MINOR
**Location:** `sec_setting.tex` lines 6–9.

**Problem.** "Must first be subdivided" leaves three things open:
- which zones the new cells receive;
- whether the carrier condition and monotonicity survive;
- whether a realization of T is a realization of the subdivision.

All three hold if each new cell inherits the zone of the open cell it subdivides: monotonicity is preserved, and h(int new) ⊆ h(int old) ⊆ Z(old). The paper should say so. The existence → uniqueness chain (Theorem 5.1 or Proposition 5.3 supplying φ_i) depends on it.

**Fix.** Add the inheritance rule and the one-line argument. Also declare the PL structure on |K|; `proof_v0_review.md` line 188 suggests the order complex of the face poset.

### 10. Small gaps in the Theorem 3.4 proof. Severity: MINOR
**Location:** `sec_uniqueness.tex` lines 104–110.

**Problem.** Two one-line justifications are missing:
- Φ(G_j) = M_j for *every* j, because for i ≠ j the isotopy Φ^i is the identity on U_j (`lemma1_multishell_review.md` #1).
- A homeomorphism of R³ maps the bounded component to the bounded one, because it maps sets with compact closure to sets with compact closure (same review, #2).

Also, the horizontality step rests on Waldhausen's Prop. 3.1, whose proof is brief and uses the irreducibility of F×I (`proof_v0_review.md` line 207; `uniqueness_v01.md` §7). That fact is not marked.

**Fix.** Add the two lines. Add a remark that Prop. 3.1 uses irreducibility of F×I (Moise, Hempel), marked `\unverified` until checked.

### 11. Standard facts are used without the "not checked" marking the notes carry. Severity: MINOR
**Location:** throughout §§3–6.

**Problem.** The notes list the standard facts each proof uses but did not check against a source (`uniqueness_v01.md` §6, `lemma0_v03.md` §4). The paper drops these lists:
- Jordan–Brouwer;
- invariance of domain;
- regular-neighbourhood theory;
- the Tarski–Seidenberg semialgebraicity of d_M;
- Brown collaring;
- mod-2 degree and general position;
- the nerve lemma behind the O3 test;
- disjointness of normal disks below the reach (Federer);
- the PL local conical structure of polyhedra (used in Corollary 4.4).

Under the project rule, unchecked facts must be visible.

**Fix.** Add a short "Standard facts used" paragraph per section, with textbook citations marked `\unverified`, or carry the notes' lists over.

### 12. The definition of wfs is attributed to the wrong source. Severity: MINOR
**Location:** `sec_collar.tex` line 6.

**Problem.** Chazal–Lieutier 2007 defines wfs for bounded *open* sets (Def. 3.1, via singular points of ∇), and extends it to compact sets only in §4.3, without proof (`lemma1_multishell_review.md` S1). "Infimum of the positive critical values" for a compact set is the wording of Chazal–Cohen-Steiner–Lieutier, DCG 2009, §2.2 (S2, verified).

**Fix.** Cite CCSL 2009 §2.2 for the definition. Alternatively, cite CL07 §4.3 and say how it applies to M. Note that positivity is also in CL07 Prop. 3.6 (subanalytic, verified), which would let the paper rely less on dREG22.

### 13. Several statements are imprecise. Severity: MINOR
- **`sec_setting.tex` lines 19–20.** "OpenCascade requires dev_e ≤ τ_e" uses the parameter-wise deviation. The BRep format specification §7.3 (`cite_audit_web.md` C) defines the edge tolerance as a one-sided Hausdorff distance. Say which definition is meant: SameParameter is the parameter-wise check.
- **`sec_setting.tex` lines 40–42.** The closed-cell condition fails mainly because τ_f is tiny: h(v) would have to lie within τ_f of every incident patch. The draft attributes the failure to "vertex tolerances exceed edge tolerances". Reword.
- **Proposition 5.2** (`sec_existence.tex` lines 66–74). Add "each face is a disk bounded by a single wire". With inner wires the polygon P̃_f is not defined.
- **The certified-bound section** (`sec_collar.tex` lines 72–75). The ρ(a) lower bound is sound only for planar regions whose boundary segments cover ∂R, after the global coplanarity re-check (`cone_lemma_review.md`, follow-up §4). One sentence is enough.
- **Table 2 header** (`sec_collar.tex` lines 84–96). "exact wfs" is the wfs of the smooth part, while the certified bound is for the triangulated mesh M_PL. For the 248-triangle cylinder, wfs(M_PL) < 3. Label the column "exact wfs (smooth part)".

---

## C. Numbers and facts (§4.3, §7) against the result files and notes

| Location | Paper | Source | Status |
|---|---|---|---|
| Table 2 | 4.530 / 0.436 / 0.137 / 0.894 / 0.894 / 0.086 / 2.512 | `cert3_A`, `cert4_A`, `cert4_B`, `cert6_B` (4.5304, 0.4360, 0.1369, 0.8944, 0.8938, 0.0861, 2.5121); exp6c LB | match |
| Table 2 | exact wfs 5 / 0.5 / 0.15 / 1 / 1 / 0.1 / 3 | exp6c U; lemma1 review #12 | match (smooth parts; see #13) |
| `sec_experiments.tex` line 79 | "fails (9 cusp vertices)" | `lemma0_check_result.json`: 9 failures, of which **2** are cusp vertices (v0, v5) and 7 are edge V1(a) failures. `lemma0_check_report.md` §2 says "9 cusp vertices" | **MISMATCH (major)**. Fix: "2 cusp vertices (9 V1(a) failures)", and correct the report |
| Line 79 | "passes after merging coplanar faces" | Only in the check report, finding 2. The merged model is not in `results/` | **not in results**: add the run to `results/` |
| Line 81 | sewn plate: 45% / 13% / **5.9%** | The 45%/13% are in `reintersect_result.json`. The 5.9% face margin is the reviewer's dense re-check for the **box** only (`lemma0_v03.md` §2′ table). No plate face margin exists anywhere | **unsupported (major)**. Fix: give the plate's face margin from the exact B3 check (`review_routeB_exact.py` covers the plate), or write "—" |
| Lines 80–84 | face margins 5.9 / 5.0 / 8.9 / 5.1% | `reintersect_curved_result.json` holds the superseded checker values: box 4.9%, cylinder 0.01 8.4%, cylinder 0.05 9.4%, pipe 5.2%. The paper's values come from `compute/checks/review_B2_B3dense.py`, whose output is not in `results/`. For the box, the "dense" 5.9% is *larger* than the checker's 4.9%, the reverse of the stated bias | **mismatch with results (major)**. Fix: store the dense re-check output in `results/`, and explain or recheck the box value |
| Line 100 | "patch corners up to 0.84 τ_v" | `route_g_result.json`: max corner/τ_v = **0.852** | **MISMATCH (minor)**: 0.85 |
| Line 11, line 96 | "Sewing sets each edge tolerance to 1.05 times the measured deviation" | Ratio is 1.05 on planar edges; 1.0485 (cylinder g = 0.01), 1.0496 (cylinder g = 0.05) and 1.0499 (pipe) on curved edges | minor: "1.05 times OCC's own deviation estimate (1.048–1.05 against our measurement)" |
| Line 41 | Gauss integral −1.000000009 | Only in `task6_claims.md`; `exp6a_result.json` has "linking": −1 | minor: add the Gauss value to the JSON |
| Line 41 | loops farther apart than 2τ | 0.4037 sampled (exact 0.403674, task6 review) > 0.1615 | match |
| Lines 48–52 | radius 0.005; 0.983 ≤ 1.3; εκ_max = 0.31; 0.036 > 2ε; det 3 | `exp6b2_result.json` | match. Add: window 0.04 < π/κ_max = 0.0504 (in the JSON), which the task6 review says is needed for the embedding criterion to be sufficient |
| Lines 62–63 | ρ_max 1.6e-3, O4 needs 3.7e-7; 10° wedge 1.6e-2 | `obstruction_result.json`: 1.617e-3, 3.73e-7, 1.605e-2 | match. Minor: "largest feasible ρ at the X positions searched" (v031 review #17) |
| Line 61 | outside the tube by 49% / about 3× | `reintersect_result.json` B2 −0.494, −2.98 | match |
| Line 64 | exact check confirmed O0–O4 on both wedges | `lemma0_v03_code_review.md` | match |
| Table 1, rows 4–6 | sewn plate BOP invalid; Lfillet τ = 0.1 BOP SelfIntersect; long_cyl τ = 3.3 BOP valid | `lemma0_check_report.md`; `exp6c_result.json` | match |
| Lines 106–108 | half-distance 5 vs 3; ×97 | `compare_occ_default.json`: cylinder 5.0; Lfillet_r0.05 0.01036 vs 1, so ×96.6 | match |
| Lines 109–111 | offset errors 44% to over a thousandfold, within the wfs-safe range | default mode, filleted box: r = 2.5 → ×1.44; r = 4.95 → ×3600; also 6 shells instead of 1 | match. Optional: mention the wrong shell count |
| Example 5.2 | 216 triangles, exact checks | `lemma0_box_result.json` | match |
| `sec_open.tex` line 17 | exact exceptions: gapped cube, wedges, box | The sewn plate was also re-checked exactly (code review) | minor: add the plate |

**Also stale in `README.md`** (not the paper, but the same claims):
- "Its hypotheses were checked on 14 OpenCascade models": `lemma0_check_result.json` has 17 entries.
- V1(b) and P0 "checked computationally": see #2(c).

---

## D. Citations

"Checked" means that a repository note or review, or the session audit, records the claim as read in the original.

| Cite | Use in the draft | Record | Verdict |
|---|---|---|---|
| Jackson95 | tradition of local tolerances; Segal/Jackson introduced them; "basis of the local-tolerance approach used by commercial kernels" | `cite_audit_web` A, B: bibliography and §3.1 checked; Jackson is the public description of *Parasolid* | OK, except "commercial kernels" (plural) is unsupported. **Minor:** "the published description of Parasolid's approach" |
| OCCT | OCC requires pcurve images within τ_e and edge ends within τ_v | `cite_audit_web` C: BRep format specification §7.2–7.4 checked | OK. Cite the section |
| OCCT, implicit (`sec_experiments.tex` line 111) | "The documentation asks only for a 'small enough' offset" | **Not found** in `occdoc/modeling_algos.md` or any audit | **MAJOR:** a quotation with no checked source. Find the passage and cite it, or delete the sentence |
| QiShapiro06b | "conventional answer: valid if an exact solid exists in the zones"; ε-solidity does not require one | `cite_audit_web` B line 91: checked. The original also requires *the same boundary combinatorial structure* | **Minor:** add that clause |
| QiShapiro06 | ε-solidity, a single global tolerance | `cite_audit_web` B line 90 (CAD 2006 read); `cite_audit_local`: the bounding interval may be induced with spatially varying δ′ (SMI 2005 §4) | **Minor:** qualify "single global" |
| Shapiro08 | homotopy conditions for tolerant queries | checked (`cite_audit_local`) | OK. Under-described: see #6 |
| SSP01 | interval solids up to homeomorphism | bibliography checked; content from the author's draft (`lit_A2` §2) | OK. No theorem numbers are cited, so the draft numbering does not matter |
| Segal90 | vertex and edge tolerances | checked: "Each vertex, edge, and face is assigned its own tolerance" | OK. Segal also had face tolerances |
| ASZ07 | constructs a solid by perturbation; pp. 819–820 a posteriori check | `read3_ASZ2007.md`, `lemma0_v0_review` Q4: pp. 819–820 quoted | OK |
| SZ08, p. 188 | "make a similar assumption" | `lemma0_v0_review` Q4: p. 188 quoted from `audit/stewart_zidani2008.txt` | OK. Add that SZ derive a normal-vector bound (p. 191) *intended* to exclude extra intersections |
| ChazalLieutier07 | definition of wfs; stability theory; Prop. 3.4 (isotopy lemma) | Prop. 3.4 verified (lemma1 review S1). The definition is not as stated (#12). "wfs … due to Chazal–Lieutier" is a priority claim that was not checked | **Minor:** fix the definition source; soften "due to" to "see" |
| Federer59 | reach | `cite_audit_web` line 110: Def. 4.1, read via notes | OK |
| Durfee83, Props. 3.5, 3.7 | small-radius regular neighbourhood | verified, with OCR partly garbled (lemma1 review S6). Page range marked `\unverified` | OK. The application also needs Tarski–Seidenberg and a finite ambient complex (#1) |
| Waldhausen68, Prop. 3.1, pp. 58, 65–66, §0 | incompressibility, horizontality | verified against page images (`proof_v0_review.md` line 4) | OK. The proof continues to p. 67; cite pp. 65–67 |
| dREG22, Thm. 2.5 | positivity of wfs for semialgebraic sets; attributes it to Fu | Thm. 2.5 quoted (`cone_lemma_review.md` §5) | **Bibliography entry wrong (major).** Title given: "Sampling and homology via bottlenecks" (a different di Rocco–Eklund paper). The review records arXiv:2209.01654 as "**Computing geometric feature sizes for algebraic manifolds**". Fix the title |
| Fu85 | wfs > 0 | not opened; marked `\unverified{whole entry}` | OK as marked. Notes give 52(4):1025–1046, from dREG22 |
| APS00 | "not yet read" | bibliography via Crossref; content not read | OK as marked |
| "2006 ASZ paper" (no `\cite`, `\unverified`) | "not yet read" | **Read**, with Thm. 4.1 PDF-checked (`read2_B.md` §4); bibliography checked in `cite_audit_web` A (CAGD 23(7):599–611, "Conditions for use of a non-selfintersection conjecture"; ASZ 2007's reference list prints the title as "Proof of …") | **Major (stale):** add a bibliography entry, remove "not yet read", and discuss it (#5). Also update `lemma0_v02.md` §6.4 and the `sec_open.tex` draft note |
| Maehara 1984 (no `\cite`) | square lemma | not checked; marked `\unverified` | OK as marked. Add a bibliography entry once checked |
| repo | repository URL | not checked whether the repository is public | **Minor:** confirm before circulation |

**Claims that need a citation but have none:**
- the PL Schoenflies theorem (`sec_open.tex` item 1);
- "knot exterior … π₁ non-abelian" (`sec_experiments.tex` line 51), which needs Dehn's lemma or standard knot theory;
- "Alexander's horned sphere" (standard; fine).

Mark the first two `\unverified` or cite them.

**`sec_open.tex` draft note, lines 25–27.** The "check before submission" list needs updating:
- add the Durfee page range, the dREG22 title, the OCC offset sentence and the Chazal–Cohen-Steiner 2005 journal-version numbering;
- remove ASZ 2006, which has been read.

---

## E. Other referee points

### 14. The reviewed proof of the twisted prism should replace the paper's version. Severity: MINOR
**Location:** `sec_experiments.tex` lines 42–43.

**Problem.** "Stay in disjoint tubular neighbourhoods and are homotopic to the cores" is the argument `task6_review.md` asked to replace. Its Step 2 says the solid-torus framing is unnecessary and the stated margin is meaningless. The correct argument is the convexity homotopy inside the capsules C_e, plus invariance of the linking number.

**Fix.** Use the review's two-line argument.

### 15. Review-status sentences do not belong in a submitted paper. Severity: MINOR
**Location:** `sec_existence.tex` line 55; `sec_obstruction.tex` lines 91–92.

**Problem.** These sentences report internal review history.

**Fix.** Move them to a draft note or the README. If they are kept, state them correctly (#2(e)).

### 16. Fidelity of the Lean appendix. Severity: MINOR
**Location:** `sec_lean.tex`; `sec_collar.tex` lines 67–68.

**Problem.** The Lean hypothesis `LocallyConicalAt M a r` is the radial-closure property inside the open ball. The paper's ρ(a) definition implies it, but they are not the same statement. Lean's `Carried` is pointwise on open cells, which agrees with the paper's closed-cell definition by monotonicity (`carrier_mono`). Positivity of λ(M) for polyhedra is not formalized.

My rerun confirms the axiom claim. The build log in the scratchpad dated 11-11 shows a failed build, but that predates the current sources; the 11-12 oleans and my rerun are clean.

**Fix.** Add one sentence on each correspondence, and state that positivity of λ is on paper only.

### 17. The abstract summary of the obstruction theorem drops hypotheses. Severity: MINOR
**Location:** `p1.tex` lines 52–53.

**Problem.** "Two planar patches cross transversally away from the shadows" omits O0 (boundary arcs in their zones), O1 (odd winding), O3 (simply connected edge zones) and the single-wire disk assumption.

**Fix.** Add "under explicit conditions" or name them.

### 18. The genus and collar conditions both refer to M_i. Severity: MINOR
**Location:** `sec_uniqueness.tex` line 15.

**Problem.** If the collar condition is weakened as in #1, the reference surface is no longer M_i×{0}.

**Fix.** State the genus condition on |K_i|, which is equivalent.

---

## Summary of required changes, in order of priority
1. **Lemma 4.1:** weaken the collar condition of §3 and rewrite the lemma (#1), or mark it unproved and soften the abstract and intro.
2. **Theorem 5.1:**
   - state all hypotheses in the paper;
   - correct "computable local" and "checked computationally";
   - flag the open apex gap;
   - label the proof an outline;
   - correct the review history (#2).
3. **Numbers** (§C):
   - 9 → 2 cusp vertices;
   - the sewn-plate face margin;
   - store the dense face-margin re-check in `results/`;
   - 0.84 → 0.85.
4. **Citations** (§D):
   - fix the dREG22 title;
   - source or delete the OCC "small enough" quotation;
   - mark ASZ 2006 as read, add its bibliography entry, and discuss it.
5. **Novelty and related work** (#5, #6):
   - add Milenkovic 1988, ASZ 2006, Chazal–Cohen-Steiner 2005, Sakkalis–Peters–Bisceglio 2004 and CCSL 2009;
   - narrow the novelty claims.
6. **Abstract and intro:** say "images" in the uniqueness claim (#4).
7. **Minor items:** #3 and #7–#18.

---

# Follow-up on v0.2

Second pass on draft v0.2 (commit 84b718f), 2026-11-12. The draft was not edited.

**Read:** every `paper/sec_*.tex`, `p1.tex`, the commit diff, `results/reintersect_B3_dense.txt`, and the changed notes and README.

**Checked the new text against:**
- for Shapiro 2008 §5.2, the original text (`pdfs/shapiro2008_chapter.txt`, p. 178);
- for SPB04 (Thm 10, C1/C2, Cor. 8) and ASZ06, `read2_B.md`;
- for CCS05, `lit_A4_isotopy.md` §3 and `cite_audit_web.md` line 114;
- for Milenkovic, `cite_audit_local.md` and `cite_audit_web.md`;
- for CCSL09 DCG §2.2, `lemma1_multishell_review.md` S2.

**Verdict.** All 18 findings are addressed, in full or in part.
- The new mathematics in §3 and in Lemma 4.1(b) is **correct**. A few small statements are missing; they are listed below.
- No new fatal or major problem was found.
- What remains open is flagged honestly in the draft: Lemma 4.1(a′), the outline of Lemma 4.1(a), and the apex gap in Theorem 5.1.
- Three small new imprecisions were introduced: in the Shapiro paraphrase, the SPB04 paraphrase, and the CL07 positivity sentence.
- The repository notes now lag the paper: `uniqueness_v01.md` still has the old collar condition, and `lemma0_v02.md` has stale statements.

## F1. Status of the 18 findings

| # | Status | Where / remark |
|---|---|---|
| 1 Collar | **Fixed, with a step openly conditional.** | `sec_uniqueness.tex` lines 7–17: weakened collar condition. Lines 61–96: Lemma 3.3. `sec_collar.tex` lines 149–194: (a) is now topological; (a′) is an explicit `\draftnote` saying (b) is conditional on it. Abstract (`p1.tex` lines 47–49) and intro (lines 46–47) say "modulo a PL-taming step". Still outlined: the two steps of (a) noted at lines 173–175. See F2 for the new mathematics. |
| 2 Theorem 5.1 | **Fixed** (a)–(g). | `sec_existence.tex` lines 75–155. All hypotheses are stated, including E2.1–E2.3, the stubs, ρ constant near a_e and b_e, the full S1 and P0, and the B-rep setting. Lines 125–127: V1(b) and P0 are declared non-local and verified only on the gapped cube. Title line 129: "conditional, proof outline". Lines 152–154: the apex gap. The review-count sentence is removed. Residual minor point: intro line 55 and abstract call the rest "computable local conditions", but S1(b), (d) and (e) are global (pairwise-disjointness) conditions. Computable, yes; local, no. Say "computable conditions, two of them non-local in the stronger sense". |
| 3 Prop. B′ | **Fixed.** | Line 191: "Proof sketch". Lines 205–208: vertex part of T not checked, PL step not carried out. The "pass (curved)" caveat is in the text below Table 3 (line 110), not in the table itself. Acceptable, but a table footnote would be safer. |
| 4 "Images" | **Fixed.** | `p1.tex` line 47; intro line 39. |
| 5 Existence novelty | **Fixed.** | Intro lines 130–133, with Milenkovic and ASZ06. |
| 6 Related work | **Mostly fixed.** | CCS05, SPB04, Shapiro 2008 and ASZ06 added (intro lines 77–118; `sec_uniqueness.tex` remark, lines 127–131). Not added: Chazal–Cohen-Steiner–Lieutier, *Comput. Geom.* 42 (2009), Thms 4.2/4.3 (isotopy of offset level sets under Hausdorff perturbation). The DCG 2009 paper cited instead is a different one. Minor now that CCS05 is cited. Wording issues are in F3. |
| 7 "Certified" | **Fixed.** | `sec_collar.tex` lines 234–237; Table 2 caption; intro line 50. |
| 8 OCC findings | **Fixed.** | Table 1 rows 5–6 relabelled (lines 32–34); intro lines 68–70. |
| 9 Subdivision | **Fixed, one point to add.** | `sec_setting.tex` lines 8–11. The inheritance rule keeps monotonicity, as claimed. But the **carrier condition must then be checked on the subdivided complex**. A new edge inside a face f has carrier Z(f), so subdividing faces adds the hypothesis π₁(Z(f)) = 0. The original condition asks only π₂(Z(f)) = 0 for faces. Contractible zones cover it, but say so. |
| 10 Theorem 3.4 proof | **Fixed.** | Lines 113–118. Irreducibility of F×I is marked `\unverified` (line 88). |
| 11 Standard facts | **Mostly fixed.** | Lists added in §3 (remark), §4 (Lemma 4.1 proof, Cor. 4.4), §6 (remark). The fan construction has no list: Federer for disjointness of normal disks, the implicit function theorem, the secant/bi-Lipschitz approximation. Minor. |
| 12 wfs definition | **Fixed.** | `sec_collar.tex` lines 143–145. |
| 13 Imprecise statements | **Fixed** (all five). | `sec_setting.tex` lines 22–25, 45–49; Prop. 5.2, line 166; `sec_collar.tex` lines 240–242; Table 2 header and caption. |
| 14 Twisted prism | **Fixed.** | `sec_experiments.tex` lines 42–50: the convexity argument. |
| 15 Review sentences | **Fixed.** | Removed from §5 and §6. |
| 16 Lean appendix | **Fixed.** | `sec_lean.tex`, new paragraph. |
| 17 Abstract obstruction | **Fixed.** | `p1.tex` line 57: "Under explicit conditions". |
| 18 Genus on \|K_i\| | **Fixed.** | `sec_uniqueness.tex` line 18. See F2 for the consequence. |

## F2. The new mathematics

### F2.1 Weakened collar condition, Lemmas 3.2–3.3, Theorem 3.4 (`sec_uniqueness.tex`). Correct; three statements missing (minor)
**What is correct.**
- **Lemma 3.2.** The carrier homotopy h ≃ φ_i lies in int U_i. Hence h: |K_i| → U_i is homotopic to φ_i, a homeomorphism onto φ_i(|K_i|) followed by an inclusion that is a homotopy equivalence by hypothesis. So h is a homotopy equivalence, and so is G ↪ U_i = h∘h⁻¹.
- **Lemma 3.3.** Its hypothesis is now intrinsic (G ↪ U a homotopy equivalence). It isotopes G straight to the level Ψ⁻¹(M×0). This is simpler than review #8's "apply to G and to the reference, then compose", and equally valid. The reference surface is needed only to obtain the homotopy equivalence in Lemma 3.2.
- **Theorem 3.4.** Correct. The added lines on Φ(G_j) and on bounded components are right.

**Missing statements.**
1. **M_i is not a sphere.** The genus hypothesis is now on |K_i|, but Lemma 3.3 assumes "M not a sphere". The proof of Theorem 3.4 should say why the two agree: |K_i| ≅ φ_i(|K_i|) ≃ U_i ≃ M_i, and closed surfaces are determined by π₁. So M_i is not a sphere.
2. **M_i is orientable.** Waldhausen's Prop. 3.1 requires F orientable. Here M_i × [−1,1] ≅ U_i ⊂ R³ is orientable, so M_i is. One line, in (b) of Lemma 3.3.
3. **M_i is connected.** The collar condition says only "a closed surface M_i". Connectedness follows from U_i ≃ |K_i|, which is connected, but state it or put it in the definition. The flattening step (c), "p(G′) open and closed in the connected surface M", uses it.

### F2.2 Lemma 4.1(b): π₁-surjectivity, Hopficity, asphericity, Whitehead (`sec_collar.tex` lines 182–193). Correct
Step by step:
- **The composite M ↪ U ↪ N̄_r(M) is literally the inclusion M ↪ N̄_r(M)**, since U ⊆ N̄_r(M) by (a′).
  - By (a), a homeomorphism N̄_r → M×[−1,1] takes M *onto* M×{0}. Under it, the inclusion becomes the level inclusion, which is a homotopy equivalence. So the composite is one.
  - "Onto" is automatic: an injective map of a closed connected surface into a connected closed surface is onto, by invariance of domain. Writing "M onto M×{0}" removes the question. This answers the coordinator's point: nothing is missing, but say "onto".
- **π₁(U) → π₁(N̄_r) is onto.** It follows from the composite π₁(M) → π₁(U) → π₁(N̄_r) being an isomorphism. Base points can be taken on M ⊂ U.
- **Hopficity step.**
  - π₁(U) ≅ π₁(M) by (a′), because U ≅ M×[−1,1] with the *same* M.
  - π₁(N̄_r) ≅ π₁(M) by (a).
  - For a surjection f: G₁ → G₂ with G₁ ≅ G₂ ≅ G Hopfian, take an isomorphism α: G₂ → G₁. Then α∘f is a surjective endomorphism of G₁, hence injective, so f is injective.
  - Closed orientable surface groups are finitely generated and residually finite, hence Hopfian (Mal'cev). The genus-0 case is trivial in any case.
  - Then π₁(M) → π₁(U) is an isomorphism, because the composite with the isomorphism π₁(U) → π₁(N̄_r) is one.
- **Whitehead step.**
  - M and U are compact polyhedra, so CW complexes, and both are connected: U ≅ M×I with M connected, as Lemma 4.1 assumes.
  - πₙ = 0 for n ≥ 2 on both sides: closed surfaces of positive genus are aspherical, and U ≃ M.
  - The inclusion induces isomorphisms on all πₙ, so it is a homotopy equivalence.

The coordinator asked whether U is connected: yes, by the above.

**Two minor points.**
- **The argument is more general than needed.** Under the review-#8 construction, U′ = Ψ⁻¹(M×[−c,c]) for a PL homeomorphism Ψ of int N_r. There U′ ↪ int N_r is a homotopy equivalence trivially, and two-out-of-three suffices. The Hopfian argument covers any U as in (a′), which is a sensible choice while (a′) is unwritten. Keep it.
- **The conditional note understates the dependency.** (b) depends on (a), which is itself only outlined (draft note, lines 173–175), as well as on (a′). The (a′) note says only "(b) … is conditional on (a′)". Say "on (a′) and on the details of (a)".

**The (a′) sketch, line 177.** The note says "a topological product collar in a 3-manifold contains a PL one between any two of its levels". As phrased this is not obviously a standard statement. The cleaner route is review #8's:
1. int N_r(M) is an open subset of R³, hence a PL 3-manifold.
2. It is homeomorphic to M×(−1,1) by (a).
3. By Moise, it is PL-homeomorphic to M×(−1,1).
4. Take U′ = Ψ⁻¹(M×[−c,c]), with c < 1 chosen so that N̄_d ⊂ int U′ (possible because N̄_d is compact in int N_r).

The draft rightly marks this `\unverified`. Prefer this wording when (a′) is written.

### F2.3 Subdivision (`sec_setting.tex` lines 8–11)
Correct as far as it goes; see F1 #9 for the additional carrier hypothesis.

## F3. New related-work and novelty text (`sec_intro.tex` lines 75–135)

| Claim | Source check | Verdict |
|---|---|---|
| Milenkovic: in the plane, with uniform ε, normalized data have an exact realization within ε/2 | `cite_audit_local`: p. 388 "polygonal path does not stray further than ½ε"; title and venue correct (`cite_audit_web`, `pdfs/88a47791…`) | **OK.** Optionally add "(p. 388)" |
| SPB04 Thm 10: ambient isotopy for a closed surface in a normal tube of a smooth closed surface that meets each normal fibre once | `read2_B.md` §3: Thm 10, PDF-checked. F is a compact nonsingular 2-manifold and **ρ is as in Cor. 8**, i.e. satisfies C1 (no principal curvature ±1/ρ) and 2ρ < c (the double-normal constant). Conclusion "W is ambient isotopic to F". Title "Isotopic approximations and interval solids" correct | **Minor:** add "of a radius ρ bounded by curvature and the double-normal distance". Without it, "normal tube" reads as any tube |
| Shapiro 2008 §5.2 | Original p. 178: "the homotopy condition alone is not sufficient. A valid boundary representation is also an orientable 2-cycle that separates … It is not immediately clear how to extend **these notions** to the union of tolerant zones … but it is likely that **the notion of separation used to establish conditions for curve and surface isotopy** … will be useful." | **Minor imprecision.** What is "not immediately clear" is how to extend *orientable separating 2-cycle* to the union of zones. The isotopy literature's separation notion is what he expects to be *useful*. The draft merges the two. Suggested: "…notes that the homotopy condition alone is not sufficient, since a valid boundary representation must also be an orientable 2-cycle separating space; it is 'not immediately clear' how to extend these notions to unions of tolerance zones, though the notion of separation used in isotopy results 'will likely be useful' (p. 178)." Note also that the next paragraph treats containment \|σ\| ⊆ Z_σ as a much stronger demand with "no formal arguments either for or against". Realizations satisfy exactly that containment, so it is worth one clause |
| ASZ06: checkable injectivity conditions for one composite parametric surface on a common domain, by a degree argument; §3.7 inside/outside information | `read2_B.md` §4: Thms 4.1/5.1, the degree argument (Lemma 4.1, Deimling); §3.7 quoted. Title "Conditions for use of …" and 23(7) match `cite_audit_web` A | **OK** |
| SZ08: derive a normal-vector bound intended to exclude extraneous intersections | `lemma0_v0_review` Q4: p. 191 bound; p. 188 quote | **OK** |
| CCS05 Thm 2.1, intro and §3 remark ("isotopic to S in the thickening") | `lit_A4` §3: conference and report versions, Thm 2.1, conclusion "S′ is isotopic to S in M" with M the thickening; hypotheses: S, S′ compact orientable surfaces in R³, S′ ≅ S. The journal version was not read; the bibliography entry marks its numbering `\unverified` | **OK.** The `\unverified` mark is on the bibliography entry, so it shows once. Consider also tagging the in-text "Thm. 2.1" |
| CCSL09dcg §2.2: definition of wfs; offsets isotopic below wfs (Lemma 2.1) | lemma1 review S2: §2.2 and Lemma 2.1 verified; bibliography matches `cite_audit_web` A (DCG 41(3):461–479) | **OK** |
| "Positivity also follows for subanalytic sets from [CL07]" | CL07 Prop. 3.6 is for **bounded open** sets. For a compact set it needs the §4.3 extension, which CL07 states without proof (lemma1 review S1, #6) | **Minor:** cite "[CL07, Prop. 3.6 with §4.3]" and say that §4.3 is stated without proof there, or that it is applied to the two sides as in Lemma 4.1(a) |
| Novelty, uniqueness: "collar obtained from wfs" | That step is conditional on (a′) | **Minor:** add "(conditionally, Lemma 4.1)" |
| Novelty, existence | Supported by the reading notes | **OK** |

## F4. Numbers (§C) and citations (§D), revisited

**Numbers.**

| Item | Status |
|---|---|
| 9 → 2 cusp vertices (`sec_experiments.tex` line 89; check report) | **Fixed** |
| "Passes after merging coplanar faces" | **Not fixed.** The merged run is still not in `results/` |
| Sewn-plate face margin, 5.9% | **Fixed.** `results/reintersect_B3_dense.txt` gives 0.0591 for the plate |
| Face margins in Table 3 | **Fixed.** The caption rule "smaller of the checker value and the dense re-check" reproduces every entry: box min(4.9, 5.9) = 4.9; cylinder 0.01 min(8.4, 5.0); cylinder 0.05 min(9.4, 8.9); pipe min(5.2, 5.1); plate dense only, 5.9. `lemma0_v03.md` updated to match. Neither value is certified, so the margins remain sampled, as the caption says |
| 0.84 → 0.85 | **Fixed** (line 113) |
| Factor 1.05 | **Fixed** (lines 10–12) |
| Gauss integral −1.000000009 | **Not fixed.** `exp6a_result.json` still has only `linking: -1`. Add the value or cite `task6_claims.md` |
| Window < π/κ_max | **Fixed** (line 58) |
| "Largest feasible ρ at the positions searched" | **Fixed** (line 71) |
| Six shells | **Fixed** (line 123) |
| Sewn plate exact re-check (`sec_open`) | **Fixed** |
| README "14 models", "checked computationally" | **Fixed** in the README |

**Stale notes, outside the paper.**
- `notes/lemma0_v02.md` lines 3, 44 and 66 still say V1(b) and P0 are "checked computationally".
- `notes/lemma0_v02.md` line 150 still says ASZ 2006 is unread.
- `notes/uniqueness_v01.md` still states the old collar condition (M_i×{0} = image of φ_i) and the old Lemma 3.
- The README says the uniqueness proof has had "two independent reviews". Those reviews were of the old version. The v0.2 collar condition and Lemma 4.1(b) have had only this pass.

**Citations.**

| Item | Status |
|---|---|
| Jackson "commercial kernels" | **Fixed** (line 13) |
| OCCT section | **Fixed** (bibliography line 39) |
| OCC "small enough" quotation | **Fixed** (deleted) |
| Qi–Shapiro combinatorial-structure clause | **Fixed** (line 19) |
| Qi–Shapiro "single global" | **Fixed** (phrase dropped) |
| Shapiro 2008 | **Partly fixed:** see F3 |
| SZ08 normal-vector bound | **Fixed** |
| CL07 definition and "due to" | **Fixed** |
| Waldhausen pp. 65–67 | **Fixed** |
| dREG22 title | **Fixed** |
| ASZ06 | **Fixed:** bibliography entry and discussion |
| Maehara | Still `\unverified`, no bibliography entry; acceptable while unread |
| repo "(public repository)" | **Not verified by this referee.** Confirm the repository is public before circulation |
| PL Schoenflies and knot exterior | **Fixed** (marked) |
| Draft-note check list | **Fixed** (`sec_open.tex`) |

## F5. New overclaims

None of major severity. Minor items:
1. **"Computable local conditions"** (intro line 55): S1 is global. See F1 #2.
2. **The SPB04 and Shapiro paraphrases**: see F3.
3. **"Positivity also follows for subanalytic sets from [CL07]"**: see F3.
4. **Novelty, uniqueness: "the collar obtained from wfs"**: add "conditionally".
5. **`sec_existence.tex` line 69**: "Neither assumes that a perturbed surface embeds as a whole". That is true of the fan construction, which assumes only that each patch embeds (P0). Proposition B′ assumes the whole re-trimmed model embeds (C, "bounding a solid"). The re-trimmed model is a re-intersected rather than perturbed surface, so the sentence is literally true, but a reader comparing with ASZ will read it as "derives embedding". Add "Proposition 5.3 assumes the re-trimmed model is embedded, which is checked computationally".

## Remaining to do, in priority order
1. **Theorem 3.4 proof:** add three lines (M_i not a sphere, M_i orientable, M_i connected; F2.1).
2. **Lemma 4.1:** say "onto M×{0}" in (a); say that (b) depends on (a) and (a′); use the Moise route for (a′) when it is written (F2.2).
3. **Subdivision:** state that the carrier condition is checked on the subdivided complex (F1 #9).
4. **Related-work wording:** fix the Shapiro, SPB04 and CL07 sentences (F3).
5. **Results and notes:** add the merged-L run and the Gauss value to `results/`; update `uniqueness_v01.md` and `lemma0_v02.md`; have the new §3/§4.1(b) text reviewed once more independently, as the project rules require for new proof text.
