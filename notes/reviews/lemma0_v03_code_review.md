# Code review: Lemma O and route B checks (lemma0_v03.md, lemma0_check_report.md)

Reviewer: independent agent, 2026-11-12. Scope:
- the code behind the Section 3 remarks of [../lemma0_v03.md](../lemma0_v03.md): Lemma O hypotheses on the sewn wedges, no witness on the sewn box and plate;
- route B (B1–B4) in [../lemma0_check_report.md](../lemma0_check_report.md).

No existing file was modified.

## Summary

- **The claims stand.** They are now confirmed in exact rational arithmetic, using code written independently from the statements:
  - O0–O4 hold on both sewn wedges.
  - B1–B4 hold on the sewn box (and on the sewn plate). This includes B4 (embeddedness), which was checked exactly.
  - B2 fails on the sewn 30° wedge, as reported.
- **No bug was found that turns a reported PASS/HOLD into a failure.**
- **Two hypotheses are literally false on the sewn models:**
  - "P_f is a polygon";
  - "P_f is bounded by a Jordan curve" (in O1 / Step 2 and in B4's setting).
- In both cases the proofs only use weaker properties, and those properties hold. The statements should be reworded (findings 2 and 3).
- **The sampled B3 check in `reintersect_check.py` is too coarse to test anything beyond B2** (finding 6).

## Independent scripts (new)

- `compute/checks/review_occ_extract.py` reads the stored OCC geometry directly and converts every double exactly to `fractions.Fraction`:
  - `Geom_Plane` with its `TopLoc_Location` transformation;
  - `Geom_Line` 3D curves with `BRep_Tool.Range`;
  - the stored pcurves: `Geom2d_Line`, or clamped non-rational `Geom2d_BSplineCurve`, whose poles are recorded;
  - vertex points;
  - `BRep_Tool.Tolerance` of vertices, edges and faces.

  It does not use `lemma0_check.Model` or `edge_samples`.
- `compute/checks/review_lemmaO_exact.py` checks O0–O4 exactly and searches for a witness (X, ρ). Results are in `compute/checks/review_lemmaO_exact_result.json`.
- `compute/checks/review_routeB_exact.py` checks B1–B4 exactly. Results are in `compute/checks/review_routeB_exact_result.json`.

How exactness is obtained:
- All comparisons are between squared rational distances.
- Square roots appear only in O4 and in the δ bounds, and only through rational lower/upper bounds.
- J_f is taken as X + [−s, s]M_f with the rational vector M_f = (N_f × N_g) × N_f, and s|M_f| ≥ ρ is checked. O1 and O2 are monotone in J, so checking them on this segment is enough.
- B-spline pcurves are handled with the convex-hull property:
  - the curve starts and ends exactly at its first and last pole (clamped knots, full range; this is asserted);
  - the curve lies in the hull of its poles.
- The only non-numerical input is OCC's topology: which edge belongs to which face, and which vertex is at which end.

## Findings

### 1. [Confirmation] Lemma O hypotheses on the sewn wedges hold, exactly

For both wedges the witness is at edge e0, faces f0 and f2 (the two sides of the sharp edge), and the search found it at edge parameter t = 0.05. Here τ_f = τ_g = 1e-7.

| Model | ρ_max (exact search) | ρ needed by O4 | At ρ = ρ_max/2: O2 margin (f / g) | At ρ_max/2: O1 margin, as dist/(τ_f+δ) − 1 |
| --- | --- | --- | --- | --- |
| sewn wedge 30° | 1.617e-3 | 3.73e-7 | 34.7% / 14.7% (binding: projected tube of e0) | > 4.8e4 |
| sewn wedge 10° | 1.605e-2 | 1.14e-6 | 152% / 146% | > 1.1e5 |

- **Witness for 30°:** X ≈ (0.0114776, 0.0062948, 0.2533868), with exact rationals in the JSON. ρ = 1736283/2147483648 ≈ 8.09e-4, which is 2166 times what O4 needs.
- **O0** (all faces): pcurve hull within the edge capsule with margin 4.76%, exactly 1 − 1/1.05, the sewing factor. Corners are in the vertex balls with margin 30.2% overall, 62.6% on the two witness faces.
- **O3:** each end ball meets its capsule, and the two end balls of every edge are disjoint.
- **O4:** holds by a factor of more than 2000.
- These values agree with obstruction_check.py: ρ = 1.62e-3 and 0.016, O0 margins 0.048 and 0.302.
- **No witness was found on the sewn box, the sewn plate, the exact box or the exact wedge 10°.** This is consistent with the note. (It is a negative search result, as in the original.)

### 2. [Medium; statement and code] The sewn pcurves are B-splines, not lines, so P_f is not a polygon

- `BRepBuilderAPI_Sewing` re-approximates pcurves. Of the stored pcurves, 9 of 18 edge uses on the sewn wedge and 12 of 24 on the sewn box are `Geom2d_BSplineCurve`, with degrees 1 to 11 and up to 34 poles.
- The 3D curves are `Geom_Line` and the surfaces are `Geom_Plane`, as the code assumes.
- The poles deviate from the chord by at most δ = 2.0e-12 (wedges) and 4.8e-12 (box).
- So the hypothesis "P_f is a polygon in Π_f" (Lemma O setting, Proposition B setting) is false in exact terms.
- `obstruction_check.py` and `reintersect_check.py` check only `BRepAdaptor_Curve(e).GetType()` and the surface type. They never look at the pcurve type, and they replace β_{f,e} by the chord between its end samples.
- **Numerical effect:** none. δ ≈ 1e-12 is negligible beside every margin (τ_f = 1e-7; τ_e ≈ 5e-3).
- **Mathematical effect:** the proofs survive if the hypothesis is weakened. The straight-line homotopy from β to its chord stays in the hull of the poles, so it moves each point by at most δ. Then:
  - O1 holds with the chord polygon when every distance is reduced by δ;
  - O0 holds when all poles are inside the capsule;
  - B3 holds when δ (plus the corner gaps) is below τ_f.
- **Recommended changes:**
  - State the lemmas for planar P_f whose boundary loop is within δ of a polygon, or simply for a planar P_f with a closed boundary loop.
  - Add to the checkers a pcurve-type check and a pole-deviation bound.

### 3. [Medium; statement] ∂P_f is not a closed Jordan curve on the sewn models

- Consecutive pcurve images do not meet exactly. The corner gaps are up to 3.6e-15 on the wedge and 1.8e-15 on the box.
- The chord loop closed by these gap segments is provably not simple, by exact test:
  - sewn wedge 30°: faces 1, 2, 4;
  - sewn box: faces 1, 4;
  - the cause: consecutive chords overshoot each other, so the loop crosses and folds back at the 1e-16 scale.
- Whether the true B-spline loop is simple cannot be decided at the 1e-12 level.
- So "P_f is a polygon bounded by a Jordan curve" (Step 2 of Lemma O) is not literally satisfied, and "P_f" as a region needs a definition.
- **What the proof actually uses:** that the boundary loop of P_f has winding number ±1 around each y ∈ J_f. The exact check verifies this: winding number ±1 at X, and J_f at distance > τ_f + δ from the loop.
- **Suggested rewording of O1:** "the boundary loop of P_f (pcurve images joined by the corner segments, which lie in the vertex balls) has winding number ±1 around every point of J_f, and its distance to J_f is > τ_f".
- **Step 2, vertex case:** say that the corner segment lies in Z(v), which is convex, so the homotopy still runs inside U_f.
- **Define P_f** as the loop together with its points of nonzero winding.
- **In the code:** the ray-casting test in `obstruction_check.py` (lines 92–101) runs over the β chords only, which do not form a closed polyline. The parity is right unless the ray passes through a gap. That did not happen here, but the test is fragile.

### 4. [Low; code] O3 check omits ball disjointness

- The fact in Section 4 ("convex set plus balls … pairwise disjoint") needs the two end balls of an edge to be disjoint.
- `obstruction_check.py` (lines 65–66) checks only that each ball meets the capsule.
- If the two balls overlapped without a common point in the capsule, Z(e) could be an annulus (nerve = triangle with no triple point).
- The exact check confirms disjointness on all models tested (edges of length ≥ 0.05, against balls of radius ≤ 0.016).

### 5. [Low; code] The witness is reported at the edge of feasibility

- `rho_max` bisects to the largest feasible ρ. At that value the binding O2 slack is 7e-8 relative, so the reported HOLD depends on floating-point comparisons at that edge.
- The conclusion is not affected: any ρ above the O4 bound works, and at ρ_max/2 the margins are 15–150% (finding 1).
- **Recommendation:** report a witness with slack (for example ρ_max/2) and the margins there.

### 6. [Medium; code] The sampled B3 check in reintersect_check.py tests almost nothing beyond B2

- The face grid has 60 subdivisions per fan triangle. On a 10 × 10 face that is a spacing of about 0.17, while the strip between P̃_f and P_f is about 0.01 wide.
- Interior grid points lie deep inside P_f. The only informative samples are on ∂P̃_f, that is, on the segments ℓ_e already covered by B2.
- That is why the reported face margin (0.131) equals the edge margin (0.131).
- **Exact result:** B3 still holds on the sewn box and plate. The method:
  - P̃_f is covered by the convex polygon K_f of chord start points. K_f lies within (gap + δ) < τ_f of the boundary loop, so K_f ⊆ N_{τ_f}(P_f).
  - The rest of P̃_f is covered by the convex pieces outside each side of K_f.
  - Each piece is cut at rational edge parameters into sub-pieces lying in B(v_0), the capsule, and B(v_1), and every vertex of every sub-piece is tested exactly.
  - The smallest capsule margin of a middle sub-piece is 4.9%. This is a property of this decomposition, not an intrinsic margin.
- **Do not quote "B3 margin 13%."**

### 7. [Confirmation] Route B on the sewn box, exactly

| Check | Result |
| --- | --- |
| B1 | Holds, margin 45.5% (1 − \|c_v − p_v\|/τ_v). |
| B2 | Holds. Capsule margin 13.07%; the binding edge is e11. On 5 of the 12 edges, the ends of ℓ_e near the vertices leave the capsule and are covered by the vertex balls through an exact split. |
| B3 | Holds (see finding 6). |
| B4 | **Checked exactly, and cheaply.** Every P̃_f is strictly convex (exact orientation tests), the 8 points c_v are distinct, and for each of the 15 face pairs the exact intersection P̃_f ∩ P̃_g is the expected one. Adjacent faces meet in exactly [c_v, c_w]; opposite faces are disjoint. The intersection is computed by exact plane sections of each convex polygon and a comparison of the two intervals on the line Π_f ∩ Π_g. So the re-intersected polyhedron is embedded. |

- The same holds for the sewn plate (t = 0.05), with identical B1/B2 margins.
- On the sewn 30° wedge, B2 fails at e0 with capsule margin −49.4%, which matches the report's "edge outside tube by 49%". B1, B3 and B4 hold there.
- `reintersect_check.py`'s B4 used sewing at 1e-9 plus BRepCheck and the BOP check, which is not a proof. The exact check above replaces it.
- The B4 method assumes convex faces. Non-convex faces would need an exact polygon–polygon intersection.

### 8. [Info] The plate is not an independent test of the margins

- The sewn plate and the sewn box use the same RNG seed and have six faces enumerated in the same order, so they receive the same translation vectors.
- Their B1 and B2 margins agree to 1e-14: 0.4550 and 0.1307.
- "Same margins" in the report is therefore expected, not a coincidence. The plate does differ in geometry (short thickness edges, where B2 relies on the vertex balls on 3 edges).

### 9. [Low; reproducibility] Output paths

- `reintersect_check.py` and `lemma0_check_run.py` write their JSON into the current directory (`compute/`).
- `obstruction_check.py` writes to `../results/`.
- The report links `results/…`. The files are present in `results/`, presumably moved by hand.

### 10. [Info] Items checked and found correct

- **Planes:** `BRepAdaptor_Surface(f).Plane()` includes the face location. Face f4 of the sewn wedge has a non-identity location, and the exact check, which applies the transformation itself, agrees.
- **Vertices and edges:** Z(v) is centred at the stored vertex point p_v. γ_e is the 3D curve over the edge's range, not the segment between the vertex points. Both are correct per v0.2 §0.
- **Vertex at each end:** `TopExp.FirstVertex` is the vertex at the first parameter. The pcurve start β(a) corresponds to γ(a). Confirmed by the positive corner and B2 split checks.
- **Tolerances:** read with `BRep_Tool.Tolerance` for vertex, edge and face. Face tolerances are 1e-7 on all sewn faces; sewing does not raise them.
- **Normals and angles:**
  - m_f = λ × n_f is a unit vector in Π_f orthogonal to λ.
  - O4 uses |cos α|, and α ∈ (0, π/2].
  - Face orientation plays no role.
- **Exactness of O0:** the same-parameter deviation |β(t) − γ(t)| is an upper bound for the set distance, so it is conservative. On 200 samples it is exact up to rounding for straight β, because the maximum is at the ends.
- **Proof of Lemma O:** read alongside the checks; no gap found in Steps 1–4. In particular:
  - Q ⊂ R_f ∩ R_g follows from O4, because points of Q have |⟨x − X, m_f⟩| ≤ (τ_g + τ_f cos α)/sin α < ρ;
  - the boundary of M_f lies on the short sides because h(∂f) ⊂ U_f, which projects off J_f.
