# Lemma 0 (existence) proof draft v0 (11-12). Audit this.

## Definitions (P1, revised)
- K is a finite regular CW complex whose shells are closed connected surfaces.
- Data:
  - a point p_v for each vertex;
  - a 3D curve γ_e for each edge;
  - a trimmed surface patch P_f for each face, whose boundary is the image of the pcurves.
    The pcurve images deviate from γ_e by dev_e ≤ τ_e (the OCC SameParameter convention).
- Zones (augmented):
  - Z(v) = B(p_v, τ_v);
  - Z(e) = N_{τ_e}(γ_e) ∪ Z(endpoints);
  - Z(f) = N_{τ_f}(P_f) ∪ ⋃_{e ⊂ ∂f} Z(e).
- A realization is a PL embedding h: |K| → R³ with h(int σ) ⊆ Z(σ). This is the open-cell definition.

## Hypotheses
Choose radii r_v ≤ τ_v and ρ_e ≤ τ_e.
- E1: dev_e < ρ_e < reach(γ_e) (outside the vertex balls), so the normal disks of N_ρ(γ_e) are pairwise disjoint.
- E2: outside the vertex balls, each adjacent face patch P_f meets the tube wall ∂N_ρ(γ_e) transversally, in one curve k_{f,e} that meets every normal circle exactly once.
- E3: on each normal circle, the exit points of the two adjacent faces are distinct.
- V1: the part outside B(p_v, r_v) (curves, fans, patches) meets the sphere ∂B(p_v, r_v) transversally, in an embedded graph: one point per incident edge and one arc per incident face.
- S1:
  - the vertex balls are pairwise disjoint;
  - tubes of non-incident edges are disjoint;
  - tubes of incident edges meet only inside the common vertex ball;
  - outside all balls and tubes, the patches are pairwise disjoint and miss non-incident tubes and balls.

## Construction
1. h(v) = p_v.
2. Outside the balls, h(e) = γ_e. In each normal disk, the radial segment from γ_e(t) to k_{f,e}(t) is assigned to face f. These segments are the "edge fans".
3. h(f) = the part of P_f outside all tubes (by E2 its boundary is the union of the k_{f,e}), together with its fan strips.
4. Inside B(p_v, r_v), replace everything by the cone from p_v over the link graph on the sphere.
5. PL-approximate. All conditions are open, so a fine enough approximation stays embedded and inside the zones.

## Zone membership
- Patches lie in N_{τ_f}(P_f).
- Fans lie in N_ρ(γ_e) ⊆ Z(e) ⊆ Z(f).
- Cones lie in B(p_v, r_v) ⊆ Z(v), which is contained in the zones of the incident edges and faces.
- γ_e lies in Z(e).

## Output
The realization serves as the reference surface M of Lemma 1. Each closed cell lies in its carrier.

## Questions for the reviewer
1. Is the construction correct? Watch for:
   - gaps at the junction of fans with vertex cones;
   - the part of γ_e and the fans between the tube region and the ball;
   - whether "a cone over an embedded graph is embedded" suffices together with S1;
   - a face patch that also enters a non-adjacent edge's tube.
2. Is E2 too strong, or not satisfiable for typical models?
   - At a convex edge with a gap, P_f's boundary lies within dev_e of γ_e, so the patch crosses the tube wall once if it is transverse there.
   - With an overlap, does the patch possibly cross the wall twice?
3. Is the PL-approximation step fine?
4. Literature: is this construction (local cone/fan realization of a tolerant B-rep) already in Andersson–Stewart–Zidani 2007 (Proj. Approx. / "Proof of correctness"), Stewart–Zidani 2008, or Andersson–Peters–Stewart 2000? Local text copies are in pdfs2/ (ASZ 2007 = 2dcdd9cf*040604303.txt) and audit/stewart_zidani2008.txt. Quote page numbers only from text you actually read.
5. Give a quantitative sufficient condition for E2 and E3 in terms of patch curvature, the angle between the patch and the edge direction, the dihedral angle, and dev_e/ρ_e, if you can.
