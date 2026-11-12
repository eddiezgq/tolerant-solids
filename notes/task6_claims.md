# Task 6 claims to audit (11-12)

Definitions, as in the P1 phase-1 doc:
- A tolerant B-rep T = (K, g, τ) has tolerance zones: a ball around each vertex, a tube around each edge, and a τ-neighbourhood of each face patch.
- A realization is a PL embedding h of |K| with h(int σ) ⊆ Z(σ) for every cell σ.
- OCC's "BRepCheck" is BRepCheck_Analyzer. "BOP check" is BRepAlgoAPI_Check(shape, true, true), which checks geometry and self-interference.

## 6a (exp6a.py): a model that passes BRepCheck and has no realization
- Model: a twisted triangular prism. The bottom triangle is at z = 0 and the top at z = 2, rotated 150°. The 8 faces are planar triangles, sewn into a solid, with all tolerances 0.081.
- Results: BRepCheck is valid. The BOP check reports SelfIntersect.
- Two non-adjacent faces A = (0,4,3) and B = (1,2,5) have linked boundary loops. The linking number is −1 by crossing count and −1.000000009 by the Gauss integral. dist(∂A, ∂B) = 0.404 > 2τ.
- **Claim: no realization exists.**
  1. In a realization, ∂A' lies in the τ-neighbourhood T_A of ∂A, and ∂B' lies in T_B. These are disjoint because 2τ < dist(∂A, ∂B).
  2. T_A is a solid torus with core ∂A, and ∂A' is homotopic to the core inside T_A: it passes through the vertex balls in cyclic order along the edge tubes. The same holds for B.
  3. Hence lk(∂A', ∂B') = −1, so ∂A' meets the disk B', which contradicts embeddedness.
- Check especially step 2.
  - Is the τ-neighbourhood of a triangle boundary a solid torus? For which τ? (Corners!)
  - Does "each open edge maps into its tube, each vertex into its ball" really force ∂A' to be homotopic to the core? Could the image of an edge wander through another edge's tube? Note that tubes of adjacent edges overlap near the shared vertex.

## 6b (exp6b2.py): a model that passes both checks and has two non-homeomorphic realizations
- Model: a thick pipe with inner radius 1, outer radius 6 and height 40. All tolerances are 1.3. BRepCheck is valid and the BOP check is valid (both measured; at τ = 1.5 the BOP check reports TooSmallEdge).
- Realization 2 changes only the inner cylindrical face.
  - The face becomes a tube around a centreline that runs up the axis (radius 1).
  - It flares to radius 0.005 using horizontal cross-sections at strictly increasing heights.
  - It follows a long trefoil, flares back, and runs up the axis.
  - The boundary circles and vertices are unchanged.
- Script results:
  - max distance of the realized inner face to the nominal inner face: 0.983 ≤ 1.3;
  - max distance of the realized seam to the nominal seam line: 0.763 ≤ 1.3;
  - EPS · κ_max = 0.31;
  - nonlocal minimum centreline distance: 0.036 > 2 · EPS;
  - knot determinant of the closed centreline: 3 (nominal: 1).
- **Claim:** the realization-2 solid is B³ minus an open regular neighbourhood of a knotted (trefoil) proper arc. This is homeomorphic to the trefoil exterior, whose π1 is non-abelian. The nominal solid is a solid torus (π1 = Z). Hence they are not homeomorphic, and so not isotopic.
- Also claimed: wfs(nominal) ≤ 1, because points of the axis inside the hole are critical (the nearest set is a circle around the point), and 1 < 1.3.
- Please check:
  - whether the embedding criteria used (EPS · κ < 1 plus a nonlocal distance > 2 EPS with window 8 EPS) suffice for the tube to be embedded;
  - whether the flare/tube junction is handled;
  - whether the seam-edge zone check is correct (the seam edge is realized somewhere on the tube; the script bounds the whole thin region);
  - the topology claim;
  - the knot computation (pyknotid needs scaling by 100; see the script comment);
  - the meaning of "both checks pass": BRepCheck is valid and BRepAlgoAPI_Check(…, true, true).IsValid() is true.

## 6c (exp6c.py): three criteria side by side
- The collar condition is marked "proved" when τ + mesh deflection < certified LB, and "fails" when τ ≥ an exhibited critical value.
- Check that this classification follows from Lemma 1b as stated: zones ⊆ N_d(M) with d < r < wfs, plus disjoint collars for multi-shell (all parts here are single-shell), plus carrier condition.
  - Is "zones ⊆ N_{τ+defl}(M_PL)" right?
  - The face zone is the τ-neighbourhood of the nominal face, and the nominal face is within defl of the mesh. Is the OCC deflection a bound on the Hausdorff distance between the nominal face and the mesh?
- Check whether any table entry over-claims.
