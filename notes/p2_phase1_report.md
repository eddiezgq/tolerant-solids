# P2 phase 1: vertices of sewn models (report, 2026-11-13)

Scope: 10 parts × 2 gap sizes (g = 0.001, 0.01), faces moved by up to g and re-sewn with `BRepBuilderAPI_Sewing` at
4g (as in P1). Parts: box; chamfered box; filleted boxes r = 2 and 0.5; box with one filleted edge; box with the top
edges filleted; L with inner fillet 0.2; L with all edges filleted 0.5; stadium prism; cylinder with filleted top.
Scripts: `compute/tight_vertex_survey.py`, `compute/strip_cone_check.py`. Results:
`results/tight_vertex_survey.json`, `results/strip_cone_check.json`, `results/strip_edge_crossing.json`.
Everything is sampled, double precision, and has not been independently reviewed yet.

## Finding 1. Why the fan construction fails at sewn vertices: the tubes, not the corners

- Sewing sets τ_v = max τ_e at every vertex (ratio exactly 1.0 in all models except some vertices of the all-fillet L).
- Patch corners sit at 0.65–0.84 τ_v from p_v (up to 1.0 τ_v at a few vertices of the all-fillet L). So corners
  alone would fit inside a ball of radius < τ_v.
- The fan construction also needs the normal disks of radius > dev around different edges to be disjoint outside the
  ball. For two edges at angle θ this needs a ball radius of about (dev_e + dev_e')/sin θ. Since τ_e ≈ 1.05 dev_e,
  this is ≈ 1.9 τ_v at a right-angled vertex. Measured: 1.79–2.19 τ_v at every vertex of every model, sharp and
  tangent alike (control: plain sewn box 1.90).
- So fans fail at **every** sewn vertex for a structural reason. This is independent of tangency. P1 avoided it for
  sharp edges by re-intersection; for tangent edges that computation is not available.
- The deviation is largest at the vertex: patch corners lie at depth 0.952 τ_e = dev/τ_e from the edge-curve ends.

## Finding 2. Tangent edges: the two patches never cross

In the normal plane at each edge sample, model each patch by the ray from its boundary point in its inward tangent
direction, and test whether the rays of the two patches meet.

| model | edges whose patches cross |
| --- | --- |
| box | 2/12 |
| chamfered box | 8/48 |
| box, one fillet / top fillets | 6/15, 5/20 (all of them sharp edges) |
| L inner fillet | 5/33 |
| filleted boxes, stadium prism, filleted cylinder | 0 |
| L all fillets | 0/92 (g = 0.001), 1/92 (g = 0.01) |

At sharp edges the patches cross in roughly a sixth to a third of the cases (depending on how the faces happened to
move), so they must be re-trimmed (P1, re-intersection). At tangent edges the two patches leave the edge in opposite
directions and do not cross; at most they overlap as two stacked layers.

## Finding 3. A "strip + cone" vertex construction passes almost everywhere

Construction tested (hypotheses only, no proof yet):
- faces: the patches themselves;
- edges: the strip of segments [b_f(t), b_g(t)] between the boundary points of the two patches. Both ends lie within
  dev_e ≤ τ_e of γ_e(t), so the strip lies in Z(e) automatically. Unlike fans, strips have no width beyond the gap
  between the patches, so there is no tube-separation condition;
- vertex: inside B(p_v, ρ τ_v), ρ < 1, the cone from p_v over the loop in which the outside pieces meet the sphere.

Tests at ρ ∈ {0.85, 0.90, 0.95, 0.99}: L1 corners and edge ends inside the ball; L2 the loop on the sphere is simple;
L3 outside the ball, strips of different edges, and a strip and a non-adjacent patch, are apart.

| model (both gaps give the same counts) | vertices passing |
| --- | --- |
| box, chamfered box, one-fillet box, top-fillet box, stadium prism | all (8, 24, 10, 12, 8) |
| filleted box r = 2 and r = 0.5 | 16/24 |
| L inner fillet 0.2 | 18/20 |
| L all fillets 0.5 | 35/46 |
| cylinder, top fillet | 0/1 |

Every failure falls in one of two classes:
- **Sampler limitation, not geometry (8 + 8 + 11 + 1 vertices):** the vertex is on a sphere patch with a degenerate
  (pole) edge, or on a seam, and the script cannot sweep the patch sector in parameter space. These are the
  parametrizations P1 also excluded (Prop. 5.3, clause P).
- **Cusp corners (2 vertices of the fused L):** two edges leave the vertex in the same direction, a face corner of
  angle 0. Here the loop touches itself (gap 0). P1 already found these 2 cusp vertices in the exact model; they
  come from not merging coplanar faces after the fuse.

## What this suggests for phase 2

A P2 existence theorem by **strips along non-crossing edges, re-trimming along crossing edges, and cones at
vertices**:
- it removes the tube-separation obstruction that makes fans fail at every sewn vertex;
- its edge hypothesis for tangent edges (no crossing, monotone strip) held on all tangent edges tested;
- its vertex hypothesis (simple loop on a sphere of radius < τ_v, transversality, separation) held at every vertex
  the sampler could handle, except genuine cusp corners.

Open points before a theorem: handle pole and seam vertices in the checker (and in the statement); prove that the
strip + cone map is a topological embedding with each cell in its zone and then PL-approximate it (the P1 secant
argument should carry over); decide what to do at cusp corners (probably an obstruction, or a hypothesis that excludes
them); and the mixed case where a crossing (re-trimmed) edge meets a strip edge at a vertex.

---

# Phase 2, step 1 results (checker v3, 2026-11-13 evening)

Checker `compute/strip_cone_check3.py` tests the hypotheses of `notes/p2_strip_cone_v04.md` as stated (patches rebuilt
from pcurves; chords in normal planes; q_e by surface intersection). 18 of 20 models done; the two filleted-box r = 2
models are being rerun after a memory fix. Vertices passing all hypotheses:

| model | g = 0.001 | g = 0.01 |
| --- | --- | --- |
| box | 8/8 | 8/8 |
| chamfered box | 23/24 | 23/24 |
| box, one edge filleted | 10/10 | 10/10 |
| box, top edges filleted | 9/12 | 9/12 |
| filleted box r = 0.5 | 22/24 | 19/24 |
| L inner fillet 0.2 | 18/20 | 18/20 |
| L all fillets 0.5 | 32/46 | 27/46 |
| stadium prism | 4/8 | 4/8 |
| cylinder, top fillet | 0/3 | 0/3 |

Failure classes:
1. **Tangent edges whose patches touch or cross along the edge (main finding).** Rebuilding the true patches shows that
   at some tangent (G1) edges the two patches meet each other within 0–0.16 τ_e of the edge curve (L all fillets: 7–8 of
   92 edges; filleted box r = 0.5 at g = 0.01: 2; top-filleted box: 1; filleted cylinder: 1). The phase-1 ray model
   missed this because it treated tangent edges as never crossing. There the strip construction is not allowed
   (S1′/E4a), and re-trimming along the crossing is ill-conditioned (nearly tangent surfaces; the surface–surface
   intersection returns curves far from the edge, so R′ fails as computed). Most V1′ failures of the fillet models
   ("q_e does not reach S_v") come from these edges. **This, not the vertex, is the hard core of the tangent-edge
   case.**
2. **E1′ fails on a few edges** (chamfered box g = 0.01: 1; filleted box r = 0.5: 1 each; L all fillets: 2–3): the patch
   boundary leaves the normal disk of radius 0.999 τ_e. Sewing sets τ_e = 1.05 dev_e with dev_e measured at equal
   parameters, and the normal-plane offset can exceed it. A chord at equal parameters would always stay within dev_e,
   but its injectivity needs a different argument.
3. **Cusp corners** (L inner fillet, 2 vertices) as before.
4. **Unexplained / possibly checker artefacts:** stadium prism (4 vertices, "arc end not at a joint"), filleted cylinder
   (seam vertices, not covered by the statement), a few "gap small" vertices. To be inspected.

## Step 2: what the "touching" tangent edges are (2026-11-13, evening)

- Normal-plane sections (`compute/tangent_contact.py`, `results/tangent_contact.json`): away from the vertices, the two
  patches at these edges do **not** meet in almost any section (contact in at most 1 of 56 sections, on 3 edges).
- The contact found by the patch–patch distance is a boundary point of one patch lying 0.24–0.51 τ_e inside the other
  patch.
- Example (L all fillets, edge 9): faces 2 and 5 are **two pieces of the same fillet cylinder** (radius 0.5, axis along
  y), split by a circular edge. After the faces are moved, the two cylinders are parallel with axes about 0.001 apart,
  and the pieces overlap slightly along the axis. In the overlap the two nearly identical surfaces cross. The edge is
  not a geometric feature, only a split.
- So the hard tangent edges are of the type **"continuation of (almost) the same surface with overlap"**. Neither the
  strip (the patches overlap) nor re-trimming along the crossing (nearly identical surfaces, ill-conditioned) applies.

Proposed unified edge construction ("wall + chord"): for each edge choose a C¹ wall surface W_e through γ_e,
transversal to both patches (for a G1 edge: spanned by γ′ and the common normal; for a sharp edge: a bisecting
surface). Cut each patch along W_e, keeping its own side, and bridge the two cut curves inside W_e by chords in
W_e ∩ Π(t).
- With no overlap and no crossing it reduces to the strip.
- It removes overlaps of any kind (same-surface pieces, stacked layers, crossings), as long as each patch meets W_e in
  one curve near γ_e within the tube.
- In the example the wall is the plane y = y0 of the circular edge, and the two cut curves are circles within the
  axis offset (≈ τ_e) of γ_e.
- To test next, and to check whether it also covers the sharp re-trimmed edges.

## Step 3: "wall + chord" edge test (2026-11-13, night)

Checker `compute/wall_chord_check.py` (results `results/wall_chord_check.json`, per model in `results/wall_chord_parts/`).
In each normal plane Pi(t) it cuts the two patch sections along a wall line and bridges the two cut points (conditions
W1–W5 in the script header). Three walls per edge, one choice for the whole edge: bisector line through gamma(t),
bisector line through the midpoint of b_f, b_g, and the line through b_f, b_g (= the P2 strip). Edge interval as in
checker v3. Only the section end lying on beta_{f,e} is used (inside a vertex ball the nearest section end can belong to
another edge of the same face).

| | edges | pass with some wall | v3 strip passed | v3 failed, wall passes | fail both |
| --- | --- | --- | --- | --- | --- |
| all 20 models (seams excluded) | 662 | 659 | 580 | 79 | 3 |

- **Every overlapping same-surface edge passes** (L all fillets: 92/92 at both gaps; filleted boxes 48/48; top-fillet
  box 20/20; filleted cylinder 3/3). This was the failure class 1 of step 1.
- **Sharp crossing edges that v3 had to re-trim pass with the wall too** (box 2/2, chamfered box, one-fillet box), except
  3: chamfered box g = 0.001 edge 9 (one sample at 0.07% of the edge, next to the vertex) and L inner fillet edge 20 at
  both gaps (samples 3–6% from the cusp vertex 5). All three are re-trimmed edges with R′ passing in v3, so **every
  edge of every model is covered by wall or re-trimming.** Edge 20 fails next to a cusp vertex, the known exception.
- The E1′ failures of step 1 disappear: the wall cut points lie well inside D(t).
- The bisector wall through gamma(t) suffices for 643 of 659 edges; the midpoint wall adds 12, the chord wall 4.
- Conditioning: the minimum crossing angle between a patch section and its wall is 3.2° (5th percentile 45°); the cut
  points move continuously (|Δa|/|Δγ| ≤ 1.07 between consecutive samples).
- **Not yet tested:** vertices with wall cells (the cone over the new loop on S_v, V0/V1), and the global separation S1′
  for the cut patches. The vertex test has to be redone with the wall construction before the theorem is rewritten.
