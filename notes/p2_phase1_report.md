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
