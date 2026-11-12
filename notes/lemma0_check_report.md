# Checking the hypotheses of Lemma 0 on OpenCascade models (phase 2, item 2)

**Status (2026-11-12).** Computational report, not yet independently reviewed. The checks are sampled
(double precision, 200 samples per edge), not certified. Nothing here is a proof; the proposed changes to
Lemma 0 in Section 4 are a plan for v0.3.

Scripts: [compute/lemma0_check.py](../compute/lemma0_check.py) (route A: the fan/cone construction of
[lemma0_v02.md](lemma0_v02.md)), [compute/reintersect_check.py](../compute/reintersect_check.py) (route B:
re-intersection), [compute/lemma0_check_run.py](../compute/lemma0_check_run.py) (the 14 models).
Results: [results/lemma0_check_result.json](../results/lemma0_check_result.json),
[results/reintersect_result.json](../results/reintersect_result.json).

## 1. What is checked

Route A, Lemma 0 v0.2 with OpenCascade's own tolerances tau_v, tau_e, tau_f:
- E1, E2.1, E2.2 (first-order form), E3, V0, V1(a) (straight radial sufficient condition), on samples.
- dev_e is measured as max |S_f(pcurve(t)) - gamma_e(t)| and used as an upper bound for dev*_e.
- For each edge, rho_e is scanned over (dev_e, tau_e) and the value with the most slack is kept.
- Two relaxations that are *not yet* in v0.2 (Section 4):
  - **E3'**: instead of the worst-case bound E3, compute the actual exit points of the two face sections on
    the circle of radius rho, with the curvature uncertainty eta = 2 k_f rho^2 (chord <= 2 rho).
  - **A' (variable radius)**: rho_e(t) = (1 + m) env(t), where env is the slope-0.05 Lipschitz upper envelope
    of the pointwise deviation dev(t). This lets the tube shrink near vertices where the deviation is small.
- S1(a)-(d) with exact B-rep distances (BRepExtrema) for the chosen rho_e and r_v.
- Not checked: E2.3 beyond what S1(d) covers, S1(e) for adjacent faces, P0, V1(b).

Route B, re-intersection (planar faces, vertices with exactly three faces): replace each vertex by the common
point of its three face planes and each edge by the segment between its new end points. Check that the new
vertices, edges and faces lie in Z(v), Z(e), Z(f) (B1-B3, sampled), and that the resulting polyhedron is
embedded (B4: BRepCheck and BRepAlgoAPI_Check on the exact polyhedron).

"Sloppy" models imitate imported data: every face is moved by a random vector of length g/2 to g, and the faces
are sewn back with BRepBuilderAPI_Sewing (tolerance 4g). Sewing sets tau_e = 1.05 x the measured deviation.

## 2. Results

| Model | OCC: BRepCheck / BOP check | tau_e / dev (min) | Route A (v0.2) | Route A with A' | Route B |
| --- | --- | --- | --- | --- | --- |
| box, cylinder, pipe (cut), slot (cut), filleted box r=2, wedge 10 deg (exact) | valid / valid | > 10^7 | pass | - | box, wedge: pass |
| L-shape, inner fillet 0.2 (fused) | valid / valid | > 10^8 | fail: 9 cusp vertices | fail | n/a (curved) |
| L-shape, all edges filleted 0.5 | valid / valid | 1.05 | fail: V1(a) at 6 fillet edges | **pass** | n/a |
| sloppy box g = 0.01, 0.1 | valid / valid | 1.05 | fail: V1(a) | fail: V1(a) | **pass**, margins: vertex 45%, edge 13%, face 13% |
| sloppy plate t = 0.05, g = 0.01 | valid / **invalid** | 1.05 | fail: V1(a) | fail | **pass**, same margins |
| sloppy wedge 30 deg, g = 0.01 | valid / valid | 1.05 | fail: V1(a) | fail | fail: edge outside tube by 49% |
| sloppy wedge 10 deg, g = 0.01 | valid / valid | 1.05 | fail: V1(a) | fail | fail: edge outside tube by 3x, vertex by 50% |
| sloppy cylinder g = 0.01 | valid / valid | 1.05 | fail: V1(a) | fail | not implemented (curved) |

(OCC checks: BRepCheck_Analyzer and BRepAlgoAPI_Check(shape, True, True); for the sloppy parts they were run on
the sewn shell made into a solid.)

## 3. Findings

1. **Exact models pass route A.** With OpenCascade's default tolerance 1e-7 and machine-precision deviations, all
   local hypotheses and S1(a)-(d) hold by a factor of about 10^7.
2. **Cusp vertices occur in ordinary OpenCascade output.** Filleting the inner edge of an L-shape made by a fuse
   leaves the top face split along the fuse seam; the split piece is bounded by a straight edge and a tangent arc,
   which meet at interior angle 0. V1 of Lemma 0 excludes such vertices. Merging coplanar faces
   (ShapeUpgrade_UnifySameDomain) removes them, whether it is applied before or after the fillet: the merged
   model (9 faces, 21 edges, 14 vertices) passes route A.
3. **The constant tube radius of v0.2 is the binding restriction for fillets.** On the filleted L-shape, OCC sets
   tau_e = 1.05 dev at the tangent fillet edges, with dev about 4e-3 in the middle of the edge and about 4e-4 at
   its ends. A constant rho > dev does not fit into the vertex balls (tau_v = 0.0101 at vertices with
   theta_v = 32 deg); a radius that follows the local deviation does (A').
4. **For sewn data, the edge stage needs E3' and the vertex stage of route A fails.** With tau_e = 1.05 dev, the
   worst-case E3 fails at every sharp edge; the actual exit points (E3') are well separated. But at a box corner
   three tubes of radius > dev must fit into a vertex ball of radius about tau_e, which is impossible for
   theta_v = 90 deg (needs tau_v > sqrt(3) dev). Along a straight sewn edge the deviation is constant, so A'
   does not help.
5. **Re-intersection (route B) realizes the sewn box and plate** with 13% margin. So these models have
   realizations that v0.2 cannot produce.
6. **Sewn sharp wedges: a candidate for "passes both OCC checks, has no realization".** On the 30 deg and 10 deg
   sewn wedges, the two planar patches at the sharp edge cross each other along a line that lies outside the edge
   tube (by 49% and about 3x of tau_e) and outside all vertex balls. Both OCC checks accept the models.
   *Sketch, not proved:* outside the edge and vertex zones, h(f) lies in the tau_f-slab of P_f and has degree 1
   over P_f (its boundary loop is homotopic to the boundary of P_f inside the edge zones), and likewise for g.
   Two degree-1 sheets in transversally crossing slabs must meet near the crossing line, so no embedding exists.
   This needs a written proof and a review before it can be claimed.
7. **BRepAlgoAPI_Check again reports a false positive:** it rejects the sewn 0.05-thick plate, which route B
   realizes.

## 4. Plan for Lemma 0 v0.3

- **A' (variable radius):** allow rho_e(t) with dev*_e(t) < rho_e(t) < tau_e and |rho_e'| small. The proof of
  v0.2 should go through with the disks D_e(t) of variable radius; the extra condition is that the fan strips stay
  transversal (a bound on |rho'|).
- **E3' (actual exit points):** replace E3 by the condition that the actual exit points are separated by more
  than the curvature uncertainty. E3 stays as a sufficient condition that is easy to state.
- **Route B (re-intersection)** for sharp edges with tau_e close to dev: the realization is the B-rep re-trimmed
  by surface-surface intersection; conditions B1-B4. Degree-3 vertices only; higher degree is open.
  Mixed models (route A at tangent edges, route B at sharp ones) need a vertex construction that combines them.
- **Obstruction lemma:** if two adjacent patches cross transversally outside all edge and vertex zones, there is
  no realization. Write the proof (Section 3, item 6) and have it reviewed.
- **Cusp vertices:** merging coplanar faces removed them in the one case seen; state this as a preprocessing step,
  and extend V1 only if cusps between genuinely different surfaces turn up.
- Curved route B (sewn cylinder) needs surface-surface intersection (GeomAPI_IntSS); not done.
