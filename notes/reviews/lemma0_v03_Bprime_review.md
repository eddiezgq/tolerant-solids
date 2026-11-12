# Review of lemma0_v03.md §2' (Proposition B', curved re-intersection) and compute/reintersect_curved.py

Reviewer: independent (geometric topology / computational geometry), 2026-11-12.
Scope: §2' of notes/lemma0_v03.md (v0.3.2), compute/reintersect_curved.py, with v0.2 §0/§5 and uniqueness_v01 §1 as
background. Review scripts (all import the checker, none writes to ../results/):
compute/checks/review_B2_run.py, review_B2_T.py, review_B2_T2.py, review_B2_T3.py, review_B2_cyl.py,
review_B2_inpatch.py, review_B2_poly.py, review_B2_B3dense.py, review_B2_B2exact.py.

**Summary.** No fatal error. The proposition is correct in substance, and the margin and secant-map steps hold.
The statement has two gaps: (1) its regularity hypothesis contradicts the seam and closed-edge models it is applied
to; (2) the regularity and corner conditions needed to build h₀ are not stated. The checker has one bug that can turn a
FAIL into a PASS (the transversality measure T). It also has a bias in its distance computation that overstates
the face-strip margins: the cylinder's real margin is 5.0%, not 11%. All B1 and B2 margins in the table are confirmed
exactly.

## A. The proof

**A1 (gap). C asks for a regular cell complex, but the proposition is used on non-regular models.**
C says the patches, curves and points "form a regular cell complex isomorphic to K". The next sentence
of the setting already allows seam edges. Every curved model in the table (cylinder, pipe) has a seam edge and
closed edges (a circle with one vertex), so neither K nor the re-trimmed model is regular, and C is false for them as
written. Two things need fixing:
- State B' for B-rep complexes (v0.2 §6). The open-cell definition of a realization, h(int σ) ⊆ Z(σ), still makes
  sense there.
- For a non-regular complex, "isomorphic" must mean an isomorphism of CW structures that respects the attaching
  maps, for example the seam glued to itself on both sides of the lateral face. Matching incidences is not enough.
  (The face poset determines the complex only in the regular case.)

Also note that uniqueness_v01 needs a regular K, so the existence result for the cylinder only feeds the
uniqueness theorem after subdivision (as v0.2 §6 already says).

**A2 (gap). C gives a homeomorphism h₀, but the proof needs a C¹ immersion on closed cells.**
"The isomorphism of C gives a homeomorphism h₀" is true for regular complexes (cell by cell, using the Alexander
trick). But the proof then uses that h₀ is C¹ with injective differential on each closed cell, and a homeomorphism from
the isomorphism has neither property. The patches being C² does not give it either, because |K| has no
smooth structure of its own.

The clean fix is to take |K| := ⋃P̃_f, with h₀ = id, and triangulate the patches by curved C¹ triangles. Then
"Lip(S − h₀) → 0" needs:
- (i) each P̃_f C² up to its boundary;
- (ii) each γ̃_e a C² *regular* curve. This follows from T by the implicit function theorem (S_f ∩ S_g is transversal),
  and the proof should say so. For a seam, γ̃_e is any C² regular curve on S_f; for a closed edge, a closed C² curve;
- (iii) at every corner of every patch, an interior angle in (0, 2π): no cusps, and no corner of angle 0 or 2π.

(iii) is what makes a shape-regular triangulation with C¹ charts up to the corner possible. It is implied by T at
vertices if "the tangent cone is an embedded PL disk" is read as "each face contributes a non-degenerate planar
sector". Say this explicitly.

**A3 (correct). Closed cells and augmented zones.**
- B1–B3 are stated for closed cells: c_v ∈ Z(v), γ̃_e (closed) ⊆ Z(e), P̃_f (closed) ⊆ Z(f).
- So h₀(σ̄) ⊆ Z(σ) is immediate, and it implies the open-cell condition h₀(int σ) ⊆ Z(σ) of the realization
  definition.
- Augmentation (Z(v) ⊆ Z(e) ⊆ Z(f)) is not even needed for this step. It is what lets B2 and B3 pass near the
  ends, where γ̃_e leaves the tube but stays in the vertex balls. For the cylinder's seam (τ_e = 1e-7), B2 holds only
  because the two ends of the new seam lie in the vertex balls.
- B4 is not used for the zone inclusions, only for injectivity. It is already contained in C: a cell complex in
  R³ whose cells meet only in common faces. **(minor)** B4 is redundant.

**A4 (correct). The margin argument.** h₀(σ̄) is compact, Z(σ) is open, and there are finitely many cells, so m > 0
exists. Since S(x) is within |S − h₀| of h₀(x) ∈ h₀(σ̄), the condition |S − h₀|_∞ < m gives S(σ̄) ⊆ Z(σ). For this,
the triangulation must refine the cells, so that S restricted to σ̄ only interpolates points of h₀(σ̄); the text says
it does.

**A5 (correct, with A2). Bi-Lipschitz and the secant map.**
- h₀ is injective (C) on a compact set and locally bi-Lipschitz, so it is globally bi-Lipschitz. Use the path
  metric of |K|, the same metric in which Lip(S − h₀) is measured; then |S(x) − S(y)| ≥ (c − Lip(S − h₀)) d(x, y).
- Locally bi-Lipschitz holds:
  - inside cells, by (i);
  - across a non-seam edge, because two half-planes with a common boundary line form an embedded PL surface
    unless they coincide. T (distinct tangent planes) excludes coinciding half-planes.
  - Strictly, bi-Lipschitz needs only that the dihedral angle φ ≠ 0. φ = π (tangent continuation) is harmless for
    bi-Lipschitz. T is needed beyond that for the regularity of γ̃_e (A2(ii)), which is the real reason to require it.
  - across a seam, h₀ is C¹ with no crease;
  - at vertices, by the tangent-cone condition, exactly as in v0.2 §5.
- The secant argument transfers and is simpler than in v0.2: there is no cone apex, so the open κ_λ issue of
  v0.2 §5 does not arise here.

**A6 (minor). The parenthetical "true when three faces meet at v with linearly independent normals" is true only
together with B4.** With independent normals n_1, n_2, n_3 at c_v:
- Φ = (F_1, F_2, F_3), with F_i local defining functions, is a local C² diffeomorphism. In that chart the three
  surfaces are the coordinate planes, the edges lie on the coordinate half-axes, and each patch near c_v is one
  quadrant or three quadrants of its plane.
- The edge directions r_1, r_2, r_3 are independent: det[n₁×n₂, n₂×n₃, n₃×n₁] = (det N)² ≠ 0.
- Two three-quadrant (reflex) sectors share the ray −r of their common axis. So the tangent cone fails to be
  embedded exactly when the patches overlap along the continuation of an edge curve, and B4 excludes that.
- The argument should be written as: independent normals + B4 ⇒ the chart picture is embedded ⇒ the tangent cone is
  embedded and h₀ is locally bi-Lipschitz.
- The cylinder's seam vertices are degree three but lie on only **two** surfaces. They are covered by the general
  clause (two half-planes at 90°), not by the parenthetical.

**A7 (minor). Exact versus computed re-trimmed model.**
- B' is about the exact re-intersection. The OpenCascade model is itself a tolerant B-rep, with new tolerances
  1e-7 to 1.5e-7 here: its edge curves approximate S_f ∩ S_g, and its pcurve images differ from them by up to that
  tolerance.
- The certificate should either use the exact curves or add the new tolerances to the measured deviations.
- For the plane–cylinder models, the computed edges agree with the analytic circles to 4e-16, so nothing changes
  there.

## B. The checker (reintersect_curved.py)

**B1 (gap; FAIL → PASS). T measures π − φ, which does not detect folds.**
- `tmin = π − acos(u_f·u_g)` uses the *inward in-plane* tangents. Their angle is the interior dihedral angle φ, so the
  measure is π − φ.
- It is 0 only for tangent continuation (φ = π). For a fin or knife edge with φ → 0, which is the case where the
  surfaces become tangent and the crease collapses, it tends to **180°** and passes.
- Measured on the exact 10° wedge (review_B2_T.py), the knife edge gives T = 170°.
- Fix: use the angle between the tangent planes, min(φ, π − φ), equivalently asin|n_f × n_g|.

**B2 (minor, but the table is wrong). The "min crease angle" column comes from the vertex samples.**
- On the sewn 30° wedge, the knife edge reads 150° at every interior sample. The reported 30° comes from sample 0,
  the vertex (review_B2_T3.py). There the inward-direction test (a step of 1e-4·span along the pcurve normal) leaves
  an acute corner, the code flips the sign of u, and the angle becomes 180° − 150° = 30°.
- It agrees with the true dihedral angle only by coincidence. Drop the end samples, and fix B1, before quoting this
  column.

**B3 (gap). T at vertices is not checked at all.**
The tangent-cone condition of B' has no counterpart in the code. Add it:
- either the independent-normals + B4 test of A6;
- or a direct check that the face sectors at c_v are non-degenerate and meet only along the edge rays.

**B4 (gap; biases margins upward). Distances are measured to a 200-point polyline of the old edge.**
- A chord of a circle lies inside it, so for points on the concave side the polyline distance is too small. The
  error is up to the sagitta R(1 − cos(π/199)): 3.7e-4 for R = 3, which is 6.5% of τ_e = 5.8e-3.
- At the worst face-strip point of the sewn cylinder, (−1.243, 2.732, 0.0005), the polyline gives slack 9.9% and the
  exact projection gives 5.0% (review_B2_poly.py).
- So the table's face-strip margin for "sewn cylinder g = 0.01" is **5.0%, not 11%**. A real B3 margin below about
  6% on a curved edge could be reported as positive.
- B2 is affected the same way in principle, though in these models the B2 minima happen to be unaffected (see C).
- Fix: use GeomAPI_ProjectPointOnCurve on the original 3D curve, as the review scripts do.

**B5 (minor). B3 does not cover all of P̃_f ∖ P_f.**
The walk checks only points on UV-normal segments from 80 samples per edge, stopping at the first point in P_f.
- *Stopping at the original patch is sound for the points it skips on that segment.* in_patch classifies the UV
  projection with tolerance 1e-9. I checked that it is strict: points 0.1τ_e outside ∂P_f are OUT on all faces of
  the sewn cylinder and box (review_B2_inpatch.py). Since the new face lies on the same Geom surface, a point in P_f
  is in Z(f).
- *What is not covered:*
  - **the corners.** The code skips t < 0.5% and t > 99.5% of each edge, which on a box edge is 0.05, about three to
    five times τ;
  - **the gaps between samples.** Samples are 0.13 apart on the box edges, against strips about 0.01 wide;
  - **regions of P̃_f ∖ P_f not reached by any normal segment before it first meets P_f**, for example a notch in
    ∂P_f.
  - The step 3τ_max/59 is not tied to the smallest τ_e of the face (on the box, half a step is up to 9% of the
    smallest τ_e).
  - Also, in_patch does not test the distance to the surface. surf_dist exists but is unused. This is harmless only
    because MakerVolume keeps the same surfaces.
- *My denser check* (review_B2_B3dense.py) uses exact curve projection, 300–400 walks per edge with ends
  included, 200 steps, and an 81×81 UV grid around every new vertex. Face-strip margins:

  | Model | table | dense recheck |
  | --- | --- | --- |
  | sewn cylinder g = 0.01 | 11% | **5.0%** |
  | sewn cylinder g = 0.05 | 10% | 8.9% |
  | sewn pipe g = 0.01 | 3.6% | 5.1% |
  | sewn box g = 0.01 | 4.9% | 5.9% |

  All remain positive, so no table verdict changes. The corners are fine for these models.

**B6 (minor). C checks incidences only.**
- Matching is done by incidence: faces by the nearest underlying surface at the face's UV-box centre, edges by face
  pair (nearest midpoint), and vertices by nearest point, followed by a bijectivity test and an edge–vertex
  consistency test.
- A wrong matching is unlikely to pass. Faces lie exactly on their source surfaces, the bijections and incidences
  must agree, and a mis-matched vertex or edge would show up in B1 or B2.
- But it does not check face topology (number of wires, disk versus annulus), the cyclic order of edges in each wire,
  or the seam self-gluing. Those are what A1 needs for non-regular complexes.
- It also does not check that each new edge lies on S_f ∩ S_g (A7).
- More robust: MakerVolume's history (Modified/Generated), together with a comparison of the wire structure.

**B7 (minor). B4 relies on BRepCheck_Analyzer and BRepAlgoAPI_Check in double precision.**
This is acceptable for a "sampled, double-precision check", and B4 is implied by C anyway (A3).

## C. Independent recheck of "sewn cylinder g = 0.01"

**Data.** The sewn model has:
- planes z = 9.996691 and z = 0.000466;
- a cylinder with axis (0.003542, 0.008421, ·) along z, R = 3, x-direction (1, 0, 0);
- τ_v = 0.01029 and 0.00577; τ_e of the circles = 0.01029 and 0.00577; seam τ_e = 1e-7; τ_f = 1e-7.

**Analytic re-trimmed model.**
- The circles are the intersections of each plane with the cylinder.
- c_v is the point where the seam line u = 0, (3.003542, 0.008421, z), meets each plane.
- The OpenCascade vertices agree with the analytic ones to 0 and 5e-20, and the OpenCascade edges to 4e-16.

**B1.**
- Top vertex: |c_v − p_v| = 0.00450, margin **0.562**.
- Bottom vertex: |c_v − p_v| = 0.00262, margin **0.546**.
- The minimum, **0.546**, confirms the table's 55%.

**B2.** Exact projection onto the original edge curves (GeomAPI_ProjectPointOnCurve), 20 001 samples per circle and
4 001 on the seam:
- top circle: margin **0.3494**, minimum near (3.0035, 0.0122, 9.9967), close to the vertex; the largest distance to
  the old curve is 0.0067 < τ_e = 0.0103;
- bottom circle: 0.494;
- seam: 0.546. The new seam lies on the old seam line, and its overhanging ends lie in the vertex balls.
- The minimum, **0.349**, confirms the table's 35%.

**Other models.** The same exact computation (review_B2_B2exact.py) reproduces the table's B1 and B2 values for the
cylinder at g = 0.05 (0.547 / 0.107), the pipe (0.525 / 0.162), the box (0.455 / 0.131) and the wedge (0.319 / −0.494).

## Verdict

- **The proposition is acceptable as a proof sketch after two statement fixes.** Neither is fatal:
  - A1: allow B-rep complexes (seams, closed edges) with an isomorphism that respects the attaching maps, or
    subdivide;
  - A2: state the regularity of the patches and of γ̃_e (derived from T), and the non-degenerate-corner condition,
    and build h₀ as the identity on a curved triangulation of ⋃P̃_f.
  
  The margin argument and the transfer of the v0.2 §5 secant argument are correct. The independent-normals remark
  needs B4 (A6).
- **Before the table is quoted, the checker needs these fixes:**
  - fix T (B1, the one FAIL → PASS bug) and drop the end samples (B2);
  - add the vertex tangent-cone check (B3);
  - replace polyline distances by exact projection (B4);
  - densify B3 and include the corners (B5).
- **Corrected table entries:**
  - face-strip margins: cylinder g = 0.01 **5.0%**, cylinder g = 0.05 8.9%, pipe 5.1%, box 5.9%;
  - min crease angle for the sewn 30° wedge: 30° in the current measure is an artifact. With the corrected measure
    the knife edge gives 30°, legitimately.
  - The vertex and edge margins (55% / 35%, etc.) are confirmed. No pass/fail verdict in the table changes.
