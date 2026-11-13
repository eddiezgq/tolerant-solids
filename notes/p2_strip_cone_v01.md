# P2: existence by strips and cones — statement draft v0.1 (2026-11-13)

Status: **statement and proof plan only; no proof written, nothing reviewed.** For Eddie to approve before the proof is
written. Notation as in P1 (`paper/p1.tex`, Section 2): tolerant B-rep with points p_v, curves γ_e, trimmed patches P_f,
tolerances τ, augmented zones Z.

## Idea

P1's fan construction cuts every patch at the boundary of a tube around its edge curve and bridges the gap with fans of
radius ρ > dev. At a sewn vertex the tubes of different edges cannot be separated inside the vertex ball (phase 1:
needs ≈ 1.9 τ_v). The strip construction keeps each patch **up to its own boundary** and bridges the two boundaries of
an edge directly by a chord in the normal plane. No tube has to be separated; only chords and patches have to be
disjoint. At each vertex a cone in a ball of radius r < τ_v closes the surface, as in P1.

## Setting

- K regular (as in P1, Theorem 5.1). B-rep extensions (seams, poles) later, if the checks support them.
- For an edge e, Π(t) is the normal plane of γ_e at t, and b*_f(t) = ∂P_f ∩ Π(t) is the point where the boundary of the
  patch f crosses it (P1 notation; unique under E2.2).

## Construction

- **Strip** of e on the edge interval [a_e, b_e] (outside the vertex balls): σ_e = ⋃_t [b*_f(t), b*_g(t)] ⊂ Π(t).
  The realized edge is the midline m_e(t) = (b*_f(t) + b*_g(t))/2; the half of the strip next to f belongs to the
  realized face f.
- **Faces:** P_f minus the vertex balls, plus its two half-strips.
- **Vertex v:** in B(p_v, r_v), r_v < τ_v, the cone from p_v over the loop λ_v = (outside pieces) ∩ ∂B(p_v, r_v).

Zones hold automatically:
- a chord has both ends within dev*_e < τ_e of γ_e(t), and B(γ_e(t), τ_e) ∩ Π(t) is convex, so σ_e ⊂ Z(e) ⊂ Z(f);
- P_f ⊂ Z(f);
- the cone lies in B(p_v, r_v) ⊂ Z(v), which lies in the zones of all incident cells (augmentation).

## Hypotheses (draft)

- **E1′** dev*_e(t) < reach(γ_e|[a_e,b_e]). Then normal disks of radius below the reach are disjoint (Federer 4.8(12),
  as in P1), so chords at different t are disjoint. **This replaces E1 and drops the tube radius ρ_e altogether.**
- **E2.2** t ↦ π_e(β_{f,e}(t)) strictly monotone (as in P1), so b*_f(t) is well defined and continuous.
- **E4 (no crossing, no fold)** For each t, the chord [b*_f(t), b*_g(t)] meets P_f ∪ P_g only at its two ends, and at
  each end it makes a positive angle with the patch's inward tangent half-line. This is the "L4" test. At tangent edges
  it held on every edge tested. At sharp edges it fails in about a sixth to a third of cases, and those edges must be
  re-trimmed instead (P1, Props. 5.2/5.3).
- **V0′** The patch corners and edge-curve ends at v lie in the open ball B(p_v, r_v), with r_v < τ_v.
- **V1′** (a) The outside pieces cross ∂B(p_v, r_v) transversally, and (b) they meet it in one simple closed curve λ_v
  that passes through the pieces in the cyclic order of the link of v. This is the "L2" test.
- **S1′** Outside the vertex balls the following are pairwise disjoint: strips of different edges; a strip and a patch
  of a face not incident to its edge; patches of different faces. This is the "L3" test, plus a patch–patch test.
- **P0′** Each P_f is embedded.

## Expected theorem

Under E1′, E2.2, E4, V0′, V1′, S1′, P0′, the tolerant B-rep has a realization.

## Proof plan

Reuse P1 Appendix A, with fans replaced by chords:
1. h is a topological embedding:
   - chords at different t lie in disjoint normal disks (E1′);
   - a chord meets its two patches only at its ends (E4);
   - global disjointness comes from S1′ and P0′;
   - at the vertex, the cone over the simple curve λ_v is an embedded disk meeting the outside only along λ_v
     (V1′, as in P1).
2. h is bi-Lipschitz on each cell: the chord family is a C¹ ruled surface; along the junction with a patch, E4's
   positive angle gives an embedded tangent cone (P1 Appendix B argument); at the vertex, the cone argument of P1.
3. The secant approximation gives a PL realization (P1 Appendix B).

## Relation to P1 and to phase 1 data

- On sewn models fans fail at every vertex. The strip and cone tests (V0′, V1′, S1′) pass at every vertex the sampler
  handles, except two cusp corners (phase 1 report; step-1 rerun with pole and seam support in
  `results/strip_cone_check2.json`).
- Mixed vertices, where a re-trimmed (crossing) sharp edge meets strip edges, need a combined statement. Plan: re-trim
  only the crossing edges, then apply the strip construction to the re-trimmed model.
