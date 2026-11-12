# Review of lemma0_v03.md (Lemma O, Proposition B, A'/E3')

Referee report, 2026-11-12. Read against lemma0_v02.md, uniqueness_v01.md §1, and compute/obstruction_check.py (O3 and the polygon construction only).
Severity: **fatal** (the result is false or the proof cannot be repaired locally), **gap** (missing argument or hypothesis that can be fixed), **minor**.

No fatal errors found. Lemma O is correct once one hypothesis is made explicit (finding 2) and two genericity choices are spelled out (findings 4 and 5). Section 1 has one real gap: the claim "no bound on ρ′ is needed" is false at the vertex ends (finding 9).

---

## Lemma O, step by step

**1. Step 1: correct.**
- For x = y + s n_f with y ∈ Π_f, every point of P_f ⊂ Π_f satisfies |x − p| ≥ |s|. So dist(x, P_f) < τ_f gives |s| < τ_f, whatever part of P_f is nearest. Far parts of P_f do no harm.
- Z(f) contains only the zones of edges and vertices *of f*, and O2 excludes the whole of U_f, far edges included. Edges not adjacent to f are not in Z(f) at all.
- h(∂f) ⊆ U_f holds because h(ē) ⊆ Z(e) (augmented zones) and h(v) ∈ Z(v) ⊆ Z(e).
- Step 1 really is confined to the open segment σ_y.

**2. Step 2: gap. The boundary of P_f must be stated as the concatenation of the β_{f,e} in the order of ∂f.**
- The homotopy needs a loop c: ∂f → Π_f with c(v) = "corner of P_f at v" and c(ē) = β_{f,e}, traversed from the corner at one end of e to the corner at the other. The square boundary ē × {0,1} ∪ ∂ē × I closes up only if β_{f,e} *ends exactly* at the corners chosen for its two vertices.
- The conclusion "winding number ±1" also needs c to be a homeomorphism onto the Jordan curve ∂P_f.
- None of this is in the Setting. That section says only "planar data". O0 presupposes a corner–vertex correspondence that is never defined.
- In a sewn model, the pcurve endpoints of consecutive edges of a wire need not coincide. Then "the polygon P_f" is not determined by the β's.
- The checker builds P_f from segments [B[0], B[-1]] per edge. It does not check that consecutive endpoints coincide, and its ray-casting parity is meaningless on a non-closed chain.
- **Fix:** add hypothesis O0′. P_f is a closed disk. Each β_{f,e} is an arc from c_{f,v} to c_{f,w}, where v, w are the ends of e. The corners are distinct. ∂P_f = ⋃_{e<f} β_{f,e}, and two β's meet only at a shared corner. Alternatively, allow gaps and close them with segments inside the ball Z(v), and define P_f as the region bounded by the closed chain, which must be simple.
- The checker must test the same condition.
- With O0′ the rest of Step 2 is correct:
  - the vertex segments lie in the convex ball Z(v) ⊆ Z(e);
  - O3 lets the homotopy extend over each square inside Z(e);
  - π_f∘H stays in π_f(U_f), which is disjoint from J_f;
  - the winding number is homotopy invariant in Π_f ∖ {y};
  - deg₂ = 1 and #φ⁻¹(y) is odd for y off φ(1-skeleton). A degenerate triangle maps into the image of its edges, so it is covered.
  - Injectivity of h gives #(h(f̄) ∩ σ_y) odd.

**3. Step 2: minor. Regular values on J_f.**
- If the projection of a 1-simplex of the triangulation is collinear with J_f, then no y on that overlap is a regular value.
- The Step 3 move of X along λ removes this case, since only finitely many segments are involved. Say so in Step 2, or move the genericity paragraph before Step 2.

**4. Step 3: gap (easily fixed). Making Σ generic does not make the short sides transverse.**
- A generic plane Σ (one that misses all vertices of h's triangulation, a one-parameter family suffices) gives L := h(f̄) ∩ Σ, a compact PL 1-manifold with ∂L ⊂ h(∂f).
- M_f = L ∩ R_f is a 1-manifold with boundary on the short sides only if L crosses the lines m = ±ρ transversally.
- Counter-case: h(f̄) contains a thin vertical triangle in the plane {⟨x − X, m_f⟩ = ρ}, with |s| < τ_f. Then L contains a segment of the short side for every position of Σ. Point contacts give 0-dimensional components.
- **Fix:** after fixing Σ, decrease ρ slightly, so that no vertex of L has m-coordinate ±ρ. O1, O2 and O4 are open in ρ, and O4 survives a decrease if it is kept strict.
- Also state why ∂M_f lies on the short sides: ∂L ⊂ h(∂f) ⊂ U_f, and π_f(R_f) = J_f is disjoint from π_f(U_f) by O2. So h(∂f) ∩ R_f = ∅. The draft asserts this without a reason.

**5. Step 3: correct once finding 4 is fixed.**
- Parity argument:
  - circles lie in int R_f;
  - an arc with both ends on one short side, closed up by that side, is a Jordan curve;
  - the endpoints of σ_y lie on ∂R_f off that curve, so they are in the unbounded component;
  - a transverse segment between two points of the same component meets a Jordan curve an even number of times.
- The generic y must also avoid the m-coordinates of the vertices of L, so that σ_y is transverse to L. That is finitely many exclusions.
- Moving X along λ is legitimate:
  - O1 and O2 are strict inequalities between compact and closed sets, so they are open in X;
  - O0, O3 and O4 do not depend on X.

**6. Step 4: correct.**
- On a short side of R_f, |w| ≥ ρ sin α − τ_f cos α > τ_g (O4). The sign of w is sign(±⟨m_f, n_g⟩), so it is opposite on the two short sides.
- The sub-arc from the last w = −τ_g before the first w = +τ_g has −τ_g < w < τ_g in its interior and |u| < τ_f throughout, so it lies in Q.
- The same holds for a_g, using the second inequality of O4.
- One fact is used without being stated: Q ⊂ {|a| < ρ}, since |a| sin α ≤ |w| + |u| cos α < ρ sin α. So Q's sides u = ±τ_f really are inside the long sides of R_f. Add this line.
- The intersection point x lies on a_f ⊂ R_f, so π_f(x) ∈ J_f, and Step 1 gives x = h(p) with p ∈ int f. Likewise x = h(q) with q ∈ int g. int f ∩ int g = ∅, so injectivity fails.
- The conclusion follows from the stated definition of realization (embedding with h(σ̄) ⊆ Z(σ), derived from the open-cell condition and augmented zones).
- PL is used only for general position. The square lemma is used correctly.

**7. Minor: O1's margin τ_f is never used.**
- Steps 1–4 need only J_f ⊆ int P_f.
- Weaken O1 to J_f ⊆ int P_f (likewise for g). This also makes the checker's O1, which measures distance along m only, adequate.

**8. Gap: O3 as checked is weaker than O3.**
- Remark 2 and obstruction_check.py (line 65) test only "each vertex ball meets the capsule". That does not imply that Z(e) is simply connected.
- Counter-case: take p_v, p_w offset by d from the ends A, B of the axis, on the same side, with τ_v = τ_w = r, L = |AB| slightly below 2r, and r − τ_e < d < r.
  - The balls meet each other, and each meets the capsule.
  - The triple intersection is empty.
  - The nerve is a hollow triangle, so Z(e) ≃ S¹.
- The fact in §4 correctly requires pairwise disjoint balls. Its alternative clause "or the triple intersection is non-empty" is enough.
- Add this test to the checker. It is likely harmless for the reported wedges, but it must be checked.
- §4's phrase "each meeting it in a convex set" is vacuous, because an intersection of convex sets is convex. It should say "non-empty intersection".

**Missing hypotheses?**
- *X near a vertex:* handled, since U_f contains the vertex balls and O2 excludes their shadows.
- *Vertex zones intersecting:* matters only through O3 (finding 8).
- *Faces with several boundary components:* outside the lemma, because K is regular. The degree argument does extend (sum of windings mod 2, with y outside the holes). But applying the lemma to a *subdivided* B-rep needs zones for the new cut edges, which the B-rep does not supply. State this in the scope.
- *P_f embedded and a disk:* this is finding 2.

## Section 1 (A', E3′)

**9. Gap: "No bound on |ρ_e′| is needed" is false at the vertex ends. Two places in v0.2 use ρ′ = 0 there.**

*(a) The V1(a) sufficient condition.*
- With variable radius, the stub disks D_e(t), for t ∈ [t_v, a_e], have radius ρ(t).
- Take a straight edge with p_v on the axis. The stub tube is {r ≤ ρ(t)}, and it is star-shaped from p_v iff ρ(t)/t is non-increasing. Strict star-shapedness needs t ρ′(t) < ρ(t).
- The v0.2 sufficient condition (ρ > |P⊥(γ − p_v)|, here 0 < ρ) does not ensure this. Counter-case: ρ ≡ ρ₀ near the ball, then growing to 2ρ₀ at a_e. A ray of slope just above ρ₀/t₁ leaves the narrow part and re-enters the wide part, so it meets ∂W_v three times.
- V1(a) is stated as a hypothesis, so the lemma itself is not wrong. But the listed sufficient condition and the proof sketch no longer support it.

*(b) v0.2 §5, the tangent cone at k(a_e).*
- The quarter-space argument places the tangent of the side-wall curve on the face ⟨·, r̂⟩ = 0.
- With variable radius, ⟨k′, r̂⟩ = ρ′(a_e), which is not zero. For one sign of ρ′, the tangent leaves the closed quarter-space and the stated containment fails.

*Fix:* require ρ_e to be constant on a neighbourhood of [t_v, a_e] and of [b_e, t_w]. Then the v0.2 arguments apply verbatim there. Otherwise add t ρ′ < ρ (star-shapedness) and redo the tangent-cone analysis.

Elsewhere, compactness does suffice:
- The fan/patch crease along k: k′ is transverse to Π(t), because ⟨k′, γ′⟩ = |γ′|²(1 − ρκ⟨r̂, N⟩) > 0, independent of ρ′. The 3-D dihedral angle is a continuous positive function, so it is bounded below.
- The fan/fan crease along γ: the dihedral angle equals the in-plane angle between r̂_f and r̂_g.

**10. Minor.**
- *k is C¹.* The draft says only "continuous". The PL step needs k to be C¹. This follows from the implicit function theorem: P_f is C², the wall is C¹ when ρ is C¹, and both are transverse to Π(t), so their traces cross transversally. Say so.
- *Curvature of λ_v.* The apex estimate in v0.2 §5 quotes κ_λ, but λ_v is only C¹. This was already so in v0.2. Replace κ_λ by a modulus of continuity of the tangent of λ_v; the conclusion Lip(S − h) → 0 still holds.

**11. E3′: correct.**
- Distinct exit points mean the two radii meet only at the centre.
- Continuity and compactness give a positive crease angle along γ.
- The only other use of E3 in v0.2 is at γ(a_e) in §5 (r̂_f ≠ r̂_g), and E3′ gives that.
- As the draft says, the checker's tangent-line computation is sampled, so E3′ is not certified for all t.

## Section 2 (Proposition B)

**12. Correct; minor points only.**
- Well-definedness:
  - c_v lies on Π_f for every face f at v;
  - ℓ_e lies in both face planes of e;
  - the sides of P̃_f are exactly the ℓ_e, e < f, because consecutive vertices of f are joined by edges of f.
- Injectivity across cells and distinctness of the c_v follow from B4, since every vertex lies on some face.
- A continuous bijection from a compact space to a Hausdorff one is a homeomorphism, so h is a homeomorphism.
- B4 was checked in floating point, so "holds for the sewn box and plate" is numerical evidence, not a proof. The remark says this; keep it.
- Scope: B fails whenever two faces at a vertex are coplanar (split planar faces). This is worth one line.

## Section 4 (standard facts)

**13. Minor: the listed facts are standard; corrections and omissions follow.**

Corrections to the list:
- *Square lemma.* Maehara (Amer. Math. Monthly 91 (1984) 641–643) *proves* it from Brouwer's fixed point theorem and then derives the Jordan curve theorem from it. Deriving it from the JCT is possible but not immediate. Cite it as "via Brouwer".
- *General position.* State that a generic member of the one-parameter family of planes orthogonal to λ is enough (avoiding finitely many vertices). Also add the separate genericity of ρ (finding 4).

Facts used but not listed:
1. The mod-2 crossing parity of a transverse segment with a Jordan curve (Step 3).
2. A simple polygon has winding number ±1 about each interior point (Step 2).
3. Homotopy invariance of the winding number in the punctured plane.
4. A PL embedding of a regular CW surface is linear on some triangulation subdividing the cells.
5. Federer's fact: normal disks of radius below the reach are pairwise disjoint (Section 1).
6. The implicit function theorem, for k ∈ C¹.

---

## Verdict

Lemma O is sound. Steps 1 and 4 are correct as written, and Steps 2 and 3 are correct after local repairs:
- add an explicit hypothesis that ∂P_f is the Jordan curve formed by the β_{f,e} in the order of ∂f, with corners at their common endpoints;
- choose ρ generically, so that the short sides are transverse to the slice;
- say why ∂M_f avoids R_f except on the short sides;
- note that Q ⊂ {|a| < ρ} follows from O4.

The obstruction for the sewn wedges is not yet certified, for two reasons:
- the checker's O3 test (ball meets capsule) is weaker than simple connectivity;
- the checker assumes, but does not test, that the pcurve endpoints close up into a simple polygon.

Both gaps have to be closed in the checker. O1's τ_f margin is unnecessary. Proposition B is correct. In Section 1, E3′ is a valid replacement for E3. The variable-radius extension A' is valid in the tube interiors, but not at the vertex ends: the V1(a) sufficient condition and the corner tangent-cone argument of v0.2 §5 both use ρ′ = 0. The simplest fix is to keep ρ_e constant near the stubs.
