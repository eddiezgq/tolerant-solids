# Review of lemma0_v03.md, draft v0.3.1: Section 3 (Lemma O) and Section 1 (A', E3')

Referee report, 2026-11-12. Independent referee; I formed my view from the draft, lemma0_v02.md §0,
uniqueness_v01.md §1, compute/obstruction_check.py, compute/lemma0_check.py (the A' / E3' parts),
compute/checks/review_lemmaO_exact.py and the result files. Only afterwards did I read
reviews/lemma0_v03_review.md and reviews/lemma0_v03_code_review.md; the fix-tracking table is at the end.

Severity: **fatal** = the result is false or the proof cannot be repaired locally; **gap** = a missing argument or
hypothesis that can be fixed; **minor** = wording, presentation, or an overstatement that does not affect the result.

**Summary.** No fatal error. The proof of Lemma O (Steps 1 to 4) is correct. One gap is in the statement (the
topology of f̄ and ḡ is never stated). Two earlier review items are only partly carried out. The rest is minor: stale
sentences left over from v0.3, two overstatements in Section 1, and one imprecise sentence in the Results remark.

---

## A. Lemma O, step by step

**1. Step 1: correct.**
- Points over y ∈ J_f in U_f are excluded by O2.
- dist(x, P_f) ≥ dist(x, Π_f) = |⟨x − y, n_f⟩|, so the fibre of N_{τ_f}(P_f) lies in the open segment σ_y.
- h(∂f) ⊆ U_f holds because h(ē) ⊆ Z(e) (augmented zones) and h(v) ∈ Z(v) ⊆ Z(e).
- Step 1 uses only P_f ⊆ Π_f. So the lemma holds for *any* subset P_f of Π_f. This settles the question "what is
  P_f on a sewn model" (see finding 13).

**2. Step 2, the homotopy: correct.**
- Shrinking A_v until h(A_v) ⊆ Z(v) is legitimate: Z(v) is open and h is continuous.
- On A_v, the straight-line homotopy stays in the convex ball Z(v), since s_{f,v} ⊆ Z(v) by O0.
- On each square, the boundary loop lies in Z(e):
  - bottom: h on the edge sub-arc;
  - top: β_{f,e};
  - vertical sides: the straight segments over the end points of A_v and A_w. They lie in Z(v), Z(w) ⊆ Z(e).
- O3 (which includes path-connectedness) gives the extension inside Z(e). H stays in U_f, and O2 keeps π_f∘H off J_f.
- The sentence "h(A_v) ⊆ Z(e) ∪ Z(e′)" is true but unused; it can go.
- The new formulation (ℓ_f closed by the segments s_{f,v}, O1 = odd winding number) removes every use of
  simplicity or of a Jordan curve. This is right: the exact check shows that the chord loops of faces 1, 2 and 4 of the
  sewn 30° wedge are *not* simple (`chord_loop_simple`), and face 2 is one of the two witness faces.

**3. Step 2, the degree count: correct, with one genericity condition left implicit (minor; earlier review item 3,
still open).**
- For y ∉ φ(1-skeleton), every preimage lies in the interior of a triangle on which φ is non-degenerate. A degenerate
  triangle maps into the image of its edges. So #φ⁻¹(y) ≡ deg₂ = 1, and injectivity of h gives #(h(f̄) ∩ σ_y) odd.
- Such y exist in J_f only if no 1-simplex of the triangulation projects onto a segment collinear with J_f. Moving X
  generically along λ (Step 3) excludes this, because the bad lines parallel to m_f are finitely many. The draft still
  does not say that this is one purpose of the generic choice of Σ.
- *Fix:* move the genericity paragraph of Step 3 before Step 2, or add this half-sentence to Step 3.

**4. Step 3, genericity of Σ and ρ: correct; the list of what is avoided should be explicit (minor).**
- Either order of choice works.
- With Σ fixed off the vertices, L = h(f̄) ∩ Σ is a compact PL 1-manifold. A value of ρ that avoids the m_f-levels
  |⟨x − X, m_f⟩| of the finitely many vertices of L makes the lines m = ±ρ transverse to L. A polygon edge lying on such
  a line has both end points at that level.
- Alternatively, choose ρ first, avoiding the m_f-levels of the triangulation vertices (these levels do not depend on
  X ∈ λ, because m_f ⊥ λ), and then choose Σ.
- The draft's justification (a triangle in the plane ⟨x − X, m_f⟩ = ρ) explains why ρ must be generic, but it does not
  say which values ρ must avoid.
- ρ and Σ are shared by f and g. The union of the two finite exclusion sets is still finite. Say so.
- Openness of O1 and O2 in X and ρ is correct: J_f is compact, ℓ_f is compact and cl π_f(U_f) is closed. O1 is
  preserved under any decrease of ρ.

**5. Step 3, the parity argument: correct.**
- ∂M_f lies on the short sides:
  - h(∂f) ∩ R_f = ∅ by O2 (the reason is now given);
  - the long sides are not met, by Step 1.
- A circle component is a Jordan polygon in the convex set R_f. Its bounded complementary domain is an open subset of
  R_f, hence of int R_f. So the end points of the closed fibre, which lie on ∂R_f, are outside it.
- An arc with both ends on one short side, closed up by that side, is again a Jordan curve. σ_y does not meet that
  short side, because y ≠ X ± ρ m_f.
- Transversality of σ_y to M_f follows from the regular-value choice. At a preimage point inside a triangle T, n_f ∉
  span(T) (φ is non-degenerate on T), so T ∩ Σ is not parallel to n_f. The generic y must also avoid the vertices of
  M_f, which is finitely many exclusions; "generic" covers this.
- So some component is an arc joining the two short sides.

**6. Step 4: correct.**
- On the short sides, |w| ≥ ρ sin α − τ_f cos α > τ_g, by the first inequality of O4. w has opposite signs on the two
  short sides.
- The sub-arc from the last point with w = −τ_g before the first point with w = +τ_g lies in Q. It touches neither
  u = ±τ_f, since a_f does not meet the long sides.
- Symmetrically for a_g, using the second inequality of O4.
- The square lemma applies through the linear chart (u/τ_f, w/τ_g).
- The common point lies over J_f and over J_g. By Step 1 for f and for g, it is h(p) = h(q) with p ∈ int f and
  q ∈ int g. These are distinct because f ≠ g. So h is not injective.
- The line "Q lies inside both rectangles" is correct ((τ_g + τ_f cos α)/sin α < ρ). It is not needed for the
  argument, because the sub-arcs lie in Q by construction. Harmless.

**7. The conclusion follows.** Given the statement as written and K regular (lemma0_v02 §0), the proof is complete.

## B. Missing hypotheses and scope

**8. Gap (statement): the topology of f̄ and ḡ is never stated, and a multi-wire face does not fit O0.**
- Step 2 uses "∂f is a circle" and "f̄ is a disk". O0 speaks of "the closed loop … in the cyclic order of ∂f".
- This holds in the regular-CW setting of lemma0_v02 §0, but Lemma O is advertised for OCC models. There:
  - a planar face can have inner wires;
  - `obstruction_check.py` raises `ValueError("face with several wires")` instead of reporting "not applicable";
  - the exact checker asserts a single wire.
- The earlier review asked for a scope sentence here. It is still absent.
- *Fix:* state "f̄ and ḡ are closed 2-cells (one wire each)". Optionally, generalize: for a face with k wires, f̄ is a
  disk with k − 1 holes, ℓ_f is the union of k loops, and O1 becomes "the sum of the winding numbers is odd". The mod-2
  degree argument goes through unchanged.
- Closed edges (v = w) and non-regular attaching maps are harmless if Step 2 is phrased through the characteristic map
  χ: D² → f̄, since all preimages over J_f are interior points. A single sentence suffices.
- Seams do not occur on planar faces.

**9. Minor: O0 does not define which end of β_{f,e} is "at v".**
- The square in Step 2 closes up only if the end of β_{f,e} joined to s_{f,v} is the end that corresponds to v in
  the orientation of e.
- *Fix:* "the end of β_{f,e} at the parameter of γ_e's end at v". The code review confirmed that both checkers use
  this parameter-based correspondence for the O0 corner test.
- `obstruction_check.py` assigns the vertex of each closing segment by *nearest vertex*. This is equivalent here, but
  it is a heuristic.

**10. Other cases asked about.**
- *X near a vertex:* covered. U_f contains the vertex balls of f, and O2 removes their shadows. The exact witness is
  in fact at edge parameter t = 0.05, close to an end, and passes with the tube of e0 binding.
- *Coplanar or parallel faces:* excluded by "planes not parallel". Other faces of K play no role.
- *Several edges between f and g, or none:* irrelevant; the lemma does not use adjacency.
- *P_f undefined on sewn data:* irrelevant (finding 1).

## C. Statements that claim more than is proved, or are stale

**11. Minor: Step 2, first bullet, is stale.**
- "By O0, ∂P_f is a loop that runs through the same sequence of edge zones and vertex zones."
- The draft itself says ∂P_f is not a closed loop on the sewn models. The object is ℓ_f.
- *Fix:* replace ∂P_f by ℓ_f.

**12. Minor: Remark 3 is stale.**
- It says Step 2 uses planarity because "the boundary of P_f is a Jordan curve in the plane". Step 2 no longer uses
  any Jordan curve. It uses ℓ_f ⊆ Π_f and O1.
- For curved patches, the real issue is replacing π_f by the nearest-point projection onto S_f within its reach, in
  both Step 1 and Step 2.
- Correspondingly, the §4 fact "the winding number of a simple closed polygon about an interior point is ±1" is no
  longer used and can be dropped.

**13. Minor: the Setting's parenthesis could say more.** Since only P_f ⊆ Π_f is used (finding 1), the lemma needs no
definition of P_f at all. Saying so closes the "P_f needs a definition" point of the code review more cleanly than
the current wording.

**14. Minor: the Status line overstates.** "The gaps they found are fixed below" is not fully true:
- the scope sentence on multi-wire faces (finding 8) is missing;
- the regular-value remark (finding 3) is missing;
- the Proposition B setting still says "P_f is a polygon in Π_f" (code review, finding 2).

## D. Results remark versus the JSON files

**15. The numbers match.**

| Claim | Source | Value |
| --- | --- | --- |
| 30°: largest feasible ρ 1.6e-3 | obstruction_result.json | 1.617e-3 |
| 30°: witness ρ 8.1e-4 | obstruction_result.json | 8.085e-4 |
| 30°: O4 needs 3.7e-7 | obstruction_result.json | 3.73e-7 |
| 30°: O0 margins 4.8% / 30% | obstruction_result.json | 0.0476 / 0.3017 |
| 10°: largest feasible ρ 0.016, witness ρ 8.0e-3 | obstruction_result.json | 1.605e-2 / 8.02e-3 |
| Exact: O2 margins 35% / 15% | review_lemmaO_exact_result.json (`half`) | 0.347 / 0.147 |
| Sewn box, sewn plate, exact box, exact wedge: no witness | both files | witness null / [] |
| O3 true | both files | true |

- "Sewn box and plate realized by Proposition B" is supported exactly by
  compute/checks/review_routeB_exact_result.json, which covers both: B1–B4 hold.
  - Section 2's remark mentions only the box. Cite the plate too.
- "Exact box and wedge realized by route A" is supported by lemma0_check_result.json (`ok: true`, all edges via E3).
  - That is a double-precision sampled check, but both models are polyhedra that trivially realize themselves.

**16. Minor: "at the 30° witness" refers to two different witnesses.**
- The exact search reports its witness at edge parameter t = 0.05, with X ≈ (0.01148, 0.00629, 0.2534).
- The double-precision witness in obstruction_result.json is at X ≈ (0.01148, 0.00629, 1.0034), from t = 0.2.
- The ρ values coincide, but X does not: the two witnesses differ along λ.
- *Fix:* "at the exact search's own witness (same ρ, a different X on λ)".
- Also, "exactly 1 − 1/1.05" agrees only to about 1e-11 (double precision) or 1e-13 (exact run). Write "equal, up to
  rounding, to 1 − 1/1.05".

**17. Minor: "largest feasible ρ" is the largest ρ at the X positions that were searched.** It is not a global maximum
over λ. For the double-precision checker these are seven positions, t ∈ [0.2, 0.8]. At ρ_max the O2 margin for g is
7e-8, so the bound is tight there, as the code review noted. The witness at ρ_max/2 is the one to quote, and the draft
quotes it.

## E. Section 1 (A', E3')

**18. Correct: the A' core claims.**
- Normal disks of radius below the reach are pairwise disjoint whatever their radii (Federer).
- ⟨k′, γ′⟩ = |γ′|² − ⟨k − γ, γ″⟩ ≥ 1 − ρκ > 0 for arc length, independent of ρ′. So k′ is transverse to Π(t).
- k is C¹ by the implicit function theorem.
- The fans are C¹ when γ ∈ C² and ρ ∈ C¹.
- ⟨k′, r̂⟩ = ρ′ is correct: differentiate |k − γ|² = ρ² and use ⟨r̂, γ′⟩ = 0.
- Keeping ρ constant on the stubs and near a_e, b_e does restore both v0.2 arguments.

**19. Minor (overclaim): "a radius that widens towards a_e makes a ray from p_v meet ∂W_v three times".**
- For a straight stub with p_v on the axis, star-shapedness fails exactly where ρ(t)/t increases, that is, where
  tρ′ > ρ. A radius that widens slowly (0 < tρ′ < ρ) is harmless. The earlier review's counter-case grows from ρ₀ to
  2ρ₀ over a short stretch.
- Similarly, the quarter-space argument at k(a_e) needs only ρ′(a_e) ≥ 0 (with the side-wall tangent −k′), not
  ρ′ = 0. With ρ′ = 0 the tangent lies on the face ⟨·, r̂⟩ = 0, which is how v0.2 is written.
- *Fix:* "a radius with tρ′ > ρ somewhere on the stub …"; "needs ⟨k′, r̂⟩ = 0 as written in v0.2 (ρ′(a_e) ≥ 0 would
  do)". Neither change affects the adopted fix.

**20. Minor: the η bound for E3' is justified with the wrong length.**
- "Within k_f s²/2 of its tangent line over length s ≤ 2ρ" mixes arc length and chord.
- The section arc from the boundary point to the exit point has arc length up to ℓ_f, by v0.2 E2.3. With dev* close
  to ρ, ℓ_f = (dev* + √(dev*² + μρ²))/μ exceeds 2ρ; for example ≈ 2.41ρ at μ = 1.
- The code (`e3_actual`, "chord ≤ 2r") uses η = 2k_f r². This is not an upper bound when k_f ρ is not small, and the
  "between the two offset lines" argument also presumes the section is a graph over its tangent line.
- *Fix:* use η = k_f ℓ_f²/2, which v0.2's `eps_angle` already uses for E3. The draft already says the E3' check is
  sampled and not a proof, so no stated result changes.

**21. Minor: the checker's variable radius is neither C¹ nor constant near the vertices, and E3' is not checked at the
stub radius.**
- In lemma0_check.py, ρ(t) = (1 + m)·env(t), where env is a max of cones with slope 0.05. That is Lipschitz, not C¹.
- Near a vertex, V1(a) is checked with rend = max ρ over the samples within 2τ_v of the vertex. But E3' (`e3_actual`)
  is evaluated at ρ(t), not at the constant value rend that A' would use on the stub. E3' is not monotone in ρ.
- The upper bounds (ρ < τ_e, ρk_f < 1) do hold at rend, since rend is one of the checked values.
- The draft discloses only "does not yet build the constant pieces explicitly".
- This matters for any result that relies on the "E3 var" route. In the current results that is the model
  "L all fillets 0.5" (6 edges). Section 1 itself quotes no such result.
- *Fix:* either say so in Section 1, or have the checker evaluate E3' at rend on the stub range and smooth the
  envelope.

**22. E3' as a replacement for E3: correct.**
- Distinct exit points mean the two radii meet only at the centre.
- Continuity and compactness give a positive crease angle. An angle of π is not a degeneracy.
- E3' gives r̂_f ≠ r̂_g at γ(a_e).
- Requiring E3' on [t_v, t_w] rather than [a_e, b_e] is stronger than needed, which is harmless.

**23. Minor, carried over from v0.2 and not addressed.** The apex estimate in v0.2 §5 still uses κ_λ, although λ_v is
only C¹ (earlier review item 10). Section 1 of v0.3.1 is where variable-radius regularity is discussed, so it would be
the place to record the replacement by a modulus of continuity.

## F. Earlier review items: fixed in the current text?

| Item | Status |
| --- | --- |
| Review 1, item 2 (boundary loop, corners, gaps) | Fixed: O0/ℓ_f with segments s_{f,v}. The "which end is at v" detail is missing (finding 9). Step 2 bullet 1 is stale (finding 11). |
| Review 1, item 3 (regular values on J_f) | **Not done** (finding 3). |
| Review 1, item 4 (generic ρ; why ∂M_f lies on the short sides) | Fixed. The list of values to avoid is implicit (finding 4). |
| Review 1, item 5 (y avoids vertices of L) | Covered by "generic fibre". |
| Review 1, item 6 (Q ⊂ {\|a\| < ρ}) | Fixed. |
| Review 1, item 7 (drop the τ_f margin in O1) | Fixed. |
| Review 1, item 8 (O3 test weaker than simple connectivity) | Fixed in the text, the §4 fact and both checkers: triple-point test, or disjoint balls in the exact check. |
| Review 1, missing-hypotheses item (multi-wire scope sentence) | **Not done** (finding 8). |
| Review 1, item 9 (ρ′ = 0 near the vertices) | Fixed in the text. Wording overclaims (finding 19). The checker is not aligned (finding 21). |
| Review 1, item 10 (k ∈ C¹; κ_λ) | C¹ fixed. κ_λ not addressed (finding 23). |
| Review 1, item 12 (coplanar scope for Proposition B) | Fixed. |
| Review 1, item 13 (§4 facts, Maehara via Brouwer) | Fixed. One listed fact is now unused (finding 12). |
| Code review, item 2 (P_f not a polygon) | Fixed for Lemma O. **Not fixed** in the Proposition B setting (line 52). |
| Code review, item 3 (∂P_f not a Jordan curve) | Fixed in O0/O1. Stale in Step 2 and Remark 3 (findings 11, 12). The checker now uses a closed polyline and an angle-sum winding number. |
| Code review, item 4 (O3 ball disjointness) | Fixed. |
| Code review, item 5 (witness at the edge of feasibility) | Fixed: ρ_max/2 is reported. |
| Code review, item 6 (B3 sampled margin) | Fixed: no longer quoted. |

---

## Verdict

Lemma O is correct. Hypotheses O0–O4, read in the regular-CW setting where f̄ and ḡ are disks, do imply that no
realization exists. Every step checks:
- the localisation in the slab;
- the boundary-loop homotopy inside the edge and vertex zones;
- the mod-2 degree count;
- the generic slice and generic ρ;
- the parity argument;
- the sub-arc and square-crossing argument.

The new formulation through ℓ_f correctly avoids any simplicity assumption, which the sewn data would violate. The one
gap is in the statement: it should say that f and g are single-wire 2-cells, or generalize O1 to a sum of winding
numbers, as the earlier review requested. The remaining items are presentation:
- an explicit regular-value clause;
- the list of values the generic ρ avoids;
- the definition of the end of β_{f,e} at v;
- stale sentences in Step 2 and Remark 3.

The Results remark agrees with both JSON files, except that the exact and double-precision witnesses use different
points X on λ. Section 1 is sound in substance, but:
- its explanation of why ρ must be constant overstates the failure (tρ′ > ρ, not mere widening);
- the E3' error bound uses the chord where it needs the arc length;
- the checker does not implement the variable radius that A' describes.

All of these are local fixes. None affects the conclusion that the two sewn wedges have no realization, which rests on
the exact re-verification.
