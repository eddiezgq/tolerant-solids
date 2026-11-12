# Task 6 review (independent, 2026-11-12)

Scratch scripts: `audit/r6/` (a.py, pipe.py, seam.py, b_geom.py, knot2.py, defl.py; outputs in the same folder).
No existing script was modified.

## Summary of verdicts

| Claim | Verdict |
|---|---|
| 6a no realization | **Correct with fix**: the conclusion holds, but step 2 should be replaced. The solid-torus claim is unnecessary, and the script's stated margin is meaningless. |
| 6a numbers | Correct. The exact dist(∂A,∂B) is 0.403674 (the sampled value 0.403708 slightly over-estimates it); 2τ = 0.1615. BRepCheck valid / BOP SelfIntersect reproduced. |
| 6b "both checks pass" at τ=1.3 | Correct (re-measured: BRepCheck valid, BOP valid for τ ∈ {1.0, 1.2, 1.3, 1.4}; τ = 1.5 gives TooSmallEdge). **But exp6b2.py does not measure it.** It must be added to the script or result JSON. |
| 6b embedding criteria | **Correct with fix**: sufficient here, but only because 8·EPS < π/κ_max. As a general criterion it is insufficient. |
| 6b flare/thin junction | Correct |
| 6b seam zone check | Correct (conservative) |
| 6b topology | Correct. Minor wording fix: "non-trivial knot" suffices. |
| 6b knot computation | The result is correct (det 3). pyknotid **without** ×100 scaling reports det 1 (finds 0 crossings), so the scaling is load-bearing. An independent coloring-matrix computation confirms det 3. |
| 6b wfs(nominal) ≤ 1 | Correct |
| 6c "proved" | Correct for all table rows, with fixes to the justification (deflection semantics, carrier condition not checked). |
| 6c "fails" | **Correct only under a narrower reading.** It proves τ ≥ wfs(nominal). It does not prove that Lemma 1b's hypothesis fails for every reference surface M, and it does not prove non-uniqueness. The label must say so. |

---

## 6a

### Step 1 (disjoint neighbourhoods): correct
Every zone of ∂A (3 vertex balls, 3 edge tubes of radius τ) lies in N_τ(∂A), and likewise for B.
Since dist(∂A,∂B) = 0.40367 > 2τ = 0.16148, the two neighbourhoods T_A and T_B are disjoint, with positive distance between them.
The exact segment–segment minimum (audit/r6/a.py) is 0.403674. The script's 200-sample value (0.403708) is an over-estimate, but the error is harmless.

### Step 2: the conclusion is right, but the argument should be replaced
The claims ask whether the τ-neighbourhood of a triangle boundary is a solid torus.
- For a planar triangle, write x = (p, z) with p in the plane. Then d(x,∂T)² = d_plane(p,∂T)² + z².
- So N_τ(∂T) fibres over the planar set U = {p : d(p,∂T) < τ} with interval fibres.
- U is an open annulus iff τ < inradius r.
- Hence N_τ(∂T) is a solid torus iff τ < r. Here r_A = r_B = 0.6025, so τ = 0.081 satisfies it.

The script's stated margin is wrong as written: "τ < ¼ of the smallest edge-to-non-incident-edge distance within each triangle" is vacuous, because a triangle has no non-incident edge pairs. The code actually uses the minimum altitude (1.509), which is not the relevant quantity either. The docstring's "tube-forming radius ≥ … sin(angle)/2" is unproved.

Being a solid torus is not enough anyway. A loop in a solid torus can have any winding number. What matters is the homotopy class of ∂A' in T_A, and that follows from **convexity**, with no τ-bound beyond Step 1:

- Let C_e be the capsule (τ-neighbourhood of the closed segment e). It is convex, and it contains the vertex balls B(v,τ) of both endpoints (vertex tolerance = edge tolerance here).
- The realization gives h(e) ⊂ C_e: the interior lies in the tube, and the endpoints lie in the balls, which are inside C_e.
  - The image of an edge **can** pass through the neighbouring tube where C_e ∩ C_e' ≠ ∅, but it cannot leave C_e.
  - So the overlap is harmless.
- Homotope h(e) rel endpoints to the segment [h(v), h(w)] inside C_e (straight-line homotopy; C_e is convex).
- Then slide each h(v) to v along a straight line. Every segment involved has both ends in C_e, so it stays in C_e.
- This gives a free homotopy ∂A' ≃ ∂A inside T_A = C_e1 ∪ C_e2 ∪ C_e3.
- Since T_A ∩ T_B = ∅, linking number is invariant under homotopy of one component in the complement of the other (lk(α,β) = [α] ∈ H_1(R³∖β)). Hence
  lk(∂A',∂B') = lk(∂A,∂B') = lk(∂A,∂B) = −1.

**Correct sufficient condition.** Let τ_v and τ_e be the vertex and edge tolerances. The condition is
dist(⋃_{σ⊂∂A} Z(σ), ⋃_{σ⊂∂B} Z(σ)) > 0,
which is implied by dist(∂A,∂B) > max_{σ⊂∂A} τ_σ + max_{σ⊂∂B} τ_σ.

If τ_v > τ_e, the same argument works with T_A = balls ∪ capsules. Each h(e) enters B(v)∩C_e near its ends, so it can be replaced by a piecewise-straight path through convex pieces.

No inradius or solid-torus condition is needed. τ = 0.0807 meets the condition with a large margin (0.1615 < 0.4037).

### Step 3: correct
- B' = h(B) is a PL (hence tame) disk.
- If ∂A' ∩ B' = ∅, then ∂A' ⊂ R³∖B', which is simply connected (B' is cellular), so lk = 0. Contradiction.
- ∂A' ∩ ∂B' = ∅ by Step 1, so ∂A' meets int B'.
- A and B share no vertex, so the cells of ∂A are disjoint from int B in |K|, and an embedding must keep their images disjoint. Contradiction.

**Fix to write:** replace step 2 with the convexity homotopy and drop the solid-torus and "margin" text (or keep "solid torus iff τ < inradius" as a remark only). Also note that the result is "passes BRepCheck, fails BOP", so it separates the two checks.

---

## 6b

### "Both checks pass"
exp6b2.py builds no OCC shape and does not record BRepCheck/BOP results. I re-ran BRepAlgoAPI_Cut(cyl(6,40), cyl(1,40)) with all tolerances set to τ (audit/r6/pipe.py):

| τ | BRepCheck | BOP check |
|---|---|---|
| 1.0, 1.2, 1.3, 1.4 | valid | valid |
| 1.5 | valid | TooSmallEdge |

This agrees with the claim and with the exp6c pipe rows (1.1 valid, 1.5 TooSmallEdge).
**Fix:** add the check to exp6b2.py so that the result JSON carries it.

The nominal seams are at (1,0,z) and (6,0,z) (audit/r6/seam.py), as the script assumes.

### Embedding criteria
For a C^{1,1} curve, the tube of radius ε is embedded iff ε < reach. Reach = min(1/κ_max, ½·shortest doubly-critical chord).

**Lemma.** If κ ≤ K and |s−t| < π/K, the chord from γ(s) to γ(t) is not perpendicular to T(s).
Proof: T(s)·(γ(t)−γ(s)) ≥ ∫₀^{|t−s|} cos(Ku) du = sin(K|t−s|)/K > 0.
So doubly-critical chords need arc separation ≥ π/K. The nonlocal test must cover all pairs with separation ≥ π/K, which means **WIN ≤ π/κ_max** is required.

The stated criterion (εκ < 1, window 8ε) is **not sufficient in general**. Counterexample: when εκ ≈ 0.9, π/κ ≈ 3.5ε < 8ε. A coil of radius 1.11ε has adjacent turns at arc separation ≈ 7ε < WIN, so a pitch < 2ε self-intersects undetected.

Here, on the Chaikin-12 refinement (≈ the quadratic B-spline limit):

| Quantity | Value |
|---|---|
| ε·κ_max | 0.3087 (script: 0.3116) |
| π/κ_max | 10.18ε > 8ε, so the window is OK |
| Min distance for pairs with separation > 8ε | 0.0361 (script: 0.0364) |
| Min distance for pairs with separation > π/κ | 0.0449 |

Both are ≫ 2ε = 0.01, so reach ≥ min(0.0162, 0.018) > ε = 0.005. **Embedded.**

Discretization: sample spacing is 5.5e-4, and the resampled polyline is within 1.6e-4 of the refined curve. Both are negligible against the margins.

**Fix:**
- State WIN ≤ π/κ_max as part of the criterion and assert it in the script.
- Note that a PL approximation of the smooth tube preserves all strict inequalities: the zone slack is ≥ 0.3 and the reach slack is ≥ 0.011.

### Flare/thin junction: correct
- Flares are unions of single horizontal circles at strictly increasing heights, so they are embedded.
- The thin centreline is exactly vertical for 1.15 (start) and 0.94 (end), measured on the refined curve, because the first three and last three control points are collinear and vertical. Its normal disks there are horizontal circles, at heights ≥ z2 (start) and ≤ z3 (end).
- The thin z-range is exactly [z2, z3]. The rest of the thin tube sits at z ≥ ~19.6 − ε.
- Smoothstep gives zero radius- and centre-derivatives at the joins, so the surface is G¹ there.
- Axis pieces, flares and thin part occupy disjoint z-ranges except at the shared junction circles.
- The maximum radius is 1.049 < 6, so the tube is clear of the outer face. The caps are unchanged.

### Seam-edge zone: correct
- Thin part: for every tube point (centreline + ε), the script bounds the distance to the line x=1, y=0. That covers any arc on the tube, whatever route the realized seam takes.
- Flares: the seam is taken as C + r·(1,0,0). Any simple arc on the realized annulus from the bottom circle to the top circle, through the seam vertices, is a valid seam image, so a specific choice is legitimate.
- All seam points have 0 ≤ z ≤ H.
- The maximum distance is 0.763 < 1.3.

### Topology: correct
- The realized solid is the cylinder (≅ B³) minus an open regular neighbourhood of a proper arc α.
- B³∖N(α) ≅ S³∖N(K), where K = α ∪ a trivial arc outside B³. The far loop is such an arc: it stays outside r ≤ 6 and 0 ≤ z ≤ H.
- det(K) = 3 ≠ 1, so K is non-trivial. By Dehn's lemma, π₁(exterior) ≇ Z, while the nominal solid torus has π₁ = Z.
- Hence the two solids are not homeomorphic, and the realizations are not isotopic.

Wording fix: "non-trivial knot" suffices. If "trefoil" is kept, justify it: in the x–z projection the diagram has exactly the 3 trefoil crossings. I checked that the excised top arc t0 ± 0.2 (t0 = 1.445) contains none of the crossing parameters (0.27/3.92, 1.82/4.46, 2.36/6.01), and that the detour route adds no crossings.

### Knot computation
The script's thin-tube subsampling ([::4]) was re-run under 5 random rotations (seeds 0–4) in audit/r6/knot2.py, with log audit/r6/knot2.out.

**Independent method.** My own code:
- finds the crossings exactly, by segment intersection in the projection;
- reads over/under from the interpolated depth (minimum depth gap at a crossing ≥ 0.15, so there are no near-degenerate crossings);
- builds the Fox coloring matrix (2·over − under_in − under_out per crossing) and takes |det| of a minor.

Results:

| Seed | Diagram crossings | Independent det | pyknotid ×1 | pyknotid ×100 |
|---|---|---|---|---|
| 0 | 9 | 3 | det 1, Gauss code empty | 3 |
| 1 | 4 | 3 | det 1, Gauss code empty | 3 |
| 2 | 3 | 3 | det 1, Gauss code empty | 3 |
| 3 | 3 | 3 | — | 3 |
| 4 | 7 | 3 | — | — |

At scale 1, pyknotid finds **no crossings**, so its det 1 is an artefact. The ×100 scaling is load-bearing and correct to use.

The determinant is rotation-independent and agrees across both methods, so the knot is **non-trivial (det 3)**. Nominal: unknot (det 1).

**Fix:**
- Record the independent determinant (or several rotations) in the result.
- Flag in the script that pyknotid's crossing finder has an absolute length threshold. Do not cite pyknotid alone at unit scale.

### wfs(nominal) ≤ 1: correct
- Take an axis point at height z ∈ (0, H). Its distance to the inner face is 1, and its distance to the cap annuli is √(1+z²) > 1, so its nearest set is the circle r = 1 at height z.
- The convex hull of that circle contains the point, so the point is critical.
- Hence wfs ≤ 1 < 1.3.

---

## 6c

### Does the classification follow from Lemma 1b?

**PROVED (τ + defl < LB).**
- Needed: nominal surface ⊆ N_defl(M_PL), i.e. one-sided max_{P∈nominal} min_{Q∈mesh} |P−Q| ≤ defl. Then every zone (vertex ball, edge tube, face τ-neighbourhood, all centred on nominal points) ⊆ N_{τ+defl}(M_PL).
- LB ≤ wfs(M_PL), because the certificate gives no critical value in (0, LB) and LB < cut-off R in every case used. Then d = τ + defl < r < LB ≤ wfs(M_PL).
- All parts are single-shell.
- So "zones ⊆ N_{τ+defl}(M_PL)" is right, **given** the deflection bound.

**Deflection semantics.** I could not open the OCC user guide online: the web pages at dev.opencascade.org redirect to occt3d.com, and that fetch was blocked. So I cite only the local copy of the OCC BRep format spec, `occdoc/brep_format.md` lines 1478–1480. It defines a stored triangulation's deflection d by
max_{P∈S} min_{Q∈T} |Q−P| ≤ d.
That is exactly the needed direction (surface → mesh).

But this is the **meaning of the stored value**, not a guarantee that BRepMesh_IncrementalMesh achieves the *requested* value. BRepMesh estimates deflection at sample points, so it is not a certified bound in general.

For the parts actually used, the requested deflection is a valid bound:
- **Planar faces:** the mesh tiles the planar polygon exactly, so the distance is 0.
- **Cylinders and the cylindrical fillet:** the Hausdorff distance is the chord sagitta R(1−cos(Δθ/2)), which is computable exactly. I measured it (audit/r6/defl.py, exact point-to-triangle):

| Part | Requested defl | Stored Deflection | Actual (face → mesh) |
|---|---|---|---|
| cylinder (R=3) | 0.02 | 0.00373 | 0.00373 |
| Lfillet_r0.2 | 0.02 | 0.00024 | 0.00024 |

Planar caps: ≤ the same sagitta.

**Fix:** in exp6c/cert, use defl := the measured (or analytically computed sagitta) face→mesh distance, not the requested parameter. Cite the brep_format definition only as the meaning of the stored field.

**Carrier condition.** exp6c checks only the collar inequality; the carrier condition of Lemma 1b is not checked. "已证成立" must be labelled "collar condition (d < wfs(M_PL)) holds", not "Lemma 1b applies / realization unique", unless the carrier condition is checked too.

**FAILS (τ ≥ U).**
- U is an exhibited critical value of the *nominal* surface, so wfs(nominal) ≤ U ≤ τ. That is correct.
- I checked all ten U values: cube centre 5; plate mid-plane 0.5 and 0.15; L arm mid-axis 1; slot mid-plane 0.1; cylinder axis 3 (caps ≥ 5 away at the chosen heights); pipe axis 1; torus core 0.5; long cylinder 3. Each nearest set (2 opposite points, or a circle) has the point in its convex hull.
- But this proves only "τ ≥ wfs(nominal)". The PROVED branch uses a different reference surface (M_PL with d = τ + defl), and wfs is not continuous under Hausdorff perturbation, so FAILS does not show that Lemma 1b's hypothesis fails for M_PL or any other M.
- For the polygonal cylinder prism, wfs(M_PL) ≤ apothem < 3, so it does fail there too. That is a separate check, not a consequence of the table.
- FAILS also says nothing about uniqueness. 6b is the separate witness of non-uniqueness, for the pipe.
- **Fix:** relabel as "τ ≥ wfs(nominal) (exhibited critical point)". Optionally add a column "τ + defl ≥ U_PL" with U_PL a critical value of M_PL, so both branches refer to the same M.

### Over-claims in the table
- With the actual deflections, no PROVED row is wrong numerically.
- Tightest rows:
  - slot τ=0.075: 0.085 < 0.0861. Margin 0.0011; true defl = 0 (planar), so the real margin is 0.0111.
  - box τ=4.5: 4.51 < 4.5304.
- The certificate is double precision without interval arithmetic (wfs_cert2 docstring), so "proved" is "certified up to floating point". At the 0.001 margin this should be stated.
- Lfillet_r0.2 shows BOP SelfIntersect at τ = 0.1–0.75 while the collar condition holds. This is not a contradiction: BOP flags overlapping tolerance zones of non-adjacent sub-shapes. Phrase it as "BOP is stricter than needed" rather than as a failure.
- Rows with τ = 1e-7 do not call set_tol, so they use OCC default tolerances (1e-7). Consistent.
