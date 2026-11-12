# Referee report: p1 v0.4, Lemma 4.1 (a), (a′), (b) and Appendix A (proof of Theorem 5.1)

Scope: only `paper/sec_collar.tex`, Lemma 4.1 (Collar), and `paper/sec_proof51.tex`, read against the hypotheses in
`paper/sec_existence.tex` §5.1. I could not open the PDFs of Durfee 1983 or Chazal–Lieutier 2007 in this session.
Statements attributed to them below are checked against the quotations in the task. Items marked "verify" need a look
at the source.

Severity: **fatal** means the result does not follow and no local fix is known. **Major** means a real gap or overclaim
that needs new text but has a clear fix. **Minor** means wording, a missing short argument, or a misstatement that
does not affect the conclusion.

---

## Part A. Lemma 4.1 (Collar)

### A1. Outer side: restricting the Prop. 3.4 homeomorphism to A₊ (minor)
The set-up is correct. Take O = Ω₊ ∩ B(0,𝓡) with 𝓡 > 2r + max_M|y|. Then for x ∈ O, R(x) = min(d(x), 𝓡 − |x|), and
{δ ≤ R ≤ r} is the disjoint union of two pieces:
- A₊, which lies in {|x| ≤ max|y| + r};
- the shell {𝓡 − r ≤ |x| ≤ 𝓡 − δ}, which lies in {|x| ≥ 𝓡 − r > max|y| + r}.

There are no ties. On A₊ we have 𝓡 − |x| ≥ 𝓡 − max|y| − r > r ≥ d. On the shell, d ≥ 𝓡 − r − max|y| > r ≥ R. So on
A₊ the nearest-point set for R is Γ(x), and on the shell it is the single radial point. Neither piece contains a
critical point.

The gap is in the last bullet. As quoted, Prop. 3.4 gives only *some* homeomorphism
Φ: R⁻¹(δ) × [δ,r] → A₊ ⊔ Shell, not a level-preserving one. Here R⁻¹(δ) = S_δ⁺ ⊔ (sphere of radius 𝓡 − δ). The
components of the product are C × [δ,r], one for each component C of R⁻¹(δ). So restricting Φ to A₊ gives
A₊ ≅ C × [δ,r] for *some* union C of components. It does not give S_δ⁺ directly.

**Fix (two sentences).**
1. R⁻¹(δ) has exactly two components, because S_δ⁺ ≅ M is connected by Step 1. The shell is one component of the
   union, so A₊ is the other one, and A₊ ≅ C × [δ,r] with C connected.
2. S_δ⁺ is a boundary component of A₊ (A2), and every boundary component of C × [δ,r] is a copy of C. Hence C ≅ S_δ⁺.

This argument needs no genus hypothesis. If CL07's construction (a gradient-flow homeomorphism) is in fact
level-preserving, citing that is an alternative.

### A2. ∂A± as a manifold is the two level sets (minor; the claim is true, but the argument is missing)
Step 3 needs S_δ^± to be a whole boundary component of A±. Here is the argument:
- A± is a compact 3-manifold in R³ (Step 2). By invariance of domain, a point is a manifold-boundary point of A± iff it
  is a frontier point of A± in R³.
- Points with δ < d < r are interior points.
- A point x with d(x) = δ is a limit of points with d < δ: move along the segment to a nearest point.
- A point x with d(x) = r is a limit of points with d > r, because x is not critical (the same fact as in (a′); see A7).
- So ∂A± = S_δ^± ⊔ S_r^±. S_δ^± is connected (Step 1) and closed, so it is exactly one component.

With this, Step 3 is correct:
- a homeomorphism C × [δ,r] → A± (C connected) sends C × {δ} or C × {r} onto S_δ^±;
- after an optional flip and composition with (Φ|)⁻¹ on that end, one gets a collar S_δ^± × [0,1] → A± that is the
  identity on S_δ^± × {0};
- gluing these collars to N̄_δ ≅ M × [−1,1] along M × {±1} by the pasting lemma gives M × [−2,2], with M ↦ M × {0}.

Add the four bullets above to Step 3, or to Step 2, as a short paragraph.

### A3. Step 1 details (minor; one item to verify)
- (verify) Durfee's Def. 3.1. Check that the semialgebraic rug functions of §3 need only be *continuous*. In
  particular, check that d (not d²) qualifies and that no C¹/C² hypothesis is imposed. Also check that Props. 3.5 and
  3.7 give a homeomorphism of N̄_δ onto a regular neighbourhood *fixing M*, or at least a homeomorphism of pairs. "Rel
  M" is load-bearing: it gives "M ↦ M × {0}" in (a), which (b) uses. If Durfee gives only a homeomorphism of pairs
  (N̄_δ, M) ≅ (R, M), that is enough, and the text should say so.
- The text does not justify that the two components M × {±1} land in *different* complementary components. Argument:
  each of M × (0,1] and M × [−1,0) is connected, so it lies in one of Ω±. Since M = ∂Ω₊ = ∂Ω₋ (Jordan–Brouwer), every
  neighbourhood of a point of M meets both Ω₊ and Ω₋, so the two halves lie in different components.
- Say explicitly that δ < r (and δ ≤ d is not needed).

### A4. Form of Prop. 3.4 as quoted (minor; verify)
As quoted, "O_{ρ1} \ O_{ρ2} = {ρ1 ≤ R ≤ ρ2}" is inconsistent with either usual convention for O_ρ, which makes the
difference set half-open. Check the exact statement. The application is unaffected either way:
- r < wfs is strict, so the hypothesis "no critical point" holds on any closed shell [δ, r′] with r′ < wfs;
- if CL07's conclusion concerns a half-open set, apply it with ρ₂ = r and take the closure, or use the closed-shell
  form if CL07 states it.
State which form is used.

### A5. Matching the two notions of "critical" (no issue)
CL07 define ∇R(x) = (x − Θ(x))/R(x), where Θ(x) is the centre of the smallest ball enclosing Γ(x).
- If ∇R(x) = 0, then x = Θ(x), and Θ(x) ∈ conv Γ(x).
- Conversely, if x ∈ conv Γ(x), then x is the centre of the smallest enclosing ball, because all of Γ(x) lies on the
  sphere about x.

So ∇R = 0 iff x ∈ conv Γ(x), which is the paper's definition. On the inner side, R = d and Γ_R = Γ, by the
first-exit-point argument; this is stated correctly. On the outer side the identification holds on A₊ because there
are no ties (A1). Correct as written; citing CCSL09 §2.1 is fine.

### A6. (a′) via Moise (minor)
The argument is correct.
- N_r is open, so it has a PL structure. M × (−1,1) has the product structure.
- The Hauptvermutung for 3-manifolds gives a PL homeomorphism g, including in the noncompact case. That is Moise's
  theorem; cite Moise, Ann. of Math. 56 (1952), or the corresponding theorem in the 1977 book, to resolve the
  `\unverified` tag.
- g⁻¹(N̄_d) is compact because N̄_d ⊂ N_r (d < r), so it lies in M × [−a,a].
- U = g(M × [−b,b]) has inter U = g(M × (−b,b)), since g is an open map onto an open subset of R³.

All claims follow. The remark that g need not send M to a level is accurate and consistent with the collar condition
in §3.

### A7. "inter N̄_r = N_r" (minor)
True. The cited reason ("a point with d = r is not critical, so d takes larger values arbitrarily near it") is the
standard fact: if x is not critical, there is a unit u with ⟨u, x − y⟩ > 0 for all y ∈ Γ(x), and the one-sided
derivative of d in direction u is min_{y∈Γ(x)} ⟨u, (x−y)/|x−y|⟩ > 0. Cite it (Lieutier 2004, or Grove's critical
point theory, or CL07's generalized gradient), or add this one-line proof. The same fact is used in A2.

### A8. (b) (no issue; minor wording)
The argument is correct:
- the composite M → U → N̄_r is a homotopy equivalence by (a), so π₁(U) → π₁(N̄_r) is onto;
- π₁(U) ≅ π₁(N̄_r) ≅ π₁(M), and surface groups are Hopfian, so that map is an isomorphism, and therefore so is
  π₁(M) → π₁(U);
- by asphericity and Whitehead's theorem, the inclusion is a homotopy equivalence.

"Suppose (a′) holds" is odd, since (a′) is proved. Write "Let U be as in (a′)". Note that A1 does not need the genus
hypothesis. The genus hypothesis enters only in (b), so "genus ≥ 1" could be moved from the lemma header into (b).

**Verdict on Part A.** Correct. The outer-side application of Prop. 3.4 is valid: the shell splits into two pieces
with no ties and no critical points. The criticality notions agree. Gluing without level-preservation works once A1
and A2 are written out. (a′) and "inter N̄_r = N_r" are right. Only minor items remain, plus two source checks
(Durfee's regularity and "rel M"; the exact form of CL07 Prop. 3.4).

---

## Part B. Appendix A: proof of Theorem 5.1

### B1. The construction of h as a map is not actually given (major)
The paragraph "h as a map" first extends a boundary homeomorphism by Alexander's trick. That extension has no
regularity. It then imposes two requirements that the Alexander extension does not satisfy:
- piecewise C¹ "by straightening the C¹ boundary of Q_f";
- radial on the cone sectors.

The bi-Lipschitz claim and the secant estimate both need more than this. h must be a homeomorphism f → h(f) such that,
on a decomposition of the domain f into polygonal pieces with the same combinatorics as the image pieces (Q_f, fans,
cone sectors):
1. each piece map is C¹ up to the boundary, including corners, with injective differential, except at the apex;
2. the piece maps agree on shared edges.

Requirement 2 is the delicate one:
- the fan map (t,σ) ↦ γ_e(t) + σ(k(t) − γ_e(t)) fixes the parametrization of the crease k by t, so the map on Q_f must
  restrict to t ↦ k(t) on that edge;
- the sector map is radial, so it fixes the parametrization of λ_v, which then has to agree with both Q_f and the fans
  on their traces.

∂Q_f is also not C¹. It has corners where λ_v crosses the edges of ∂W_v (B2).

**Fix.** Replace the paragraph with an explicit piecewise construction:
- Choose the domain as a polyhedral complex L, a subdivision of |K|, whose 2-cells correspond to the pieces. The
  sector cells are cones from v over a polygonal link arc, and the link has a vertex at the preimage of every corner of
  λ_v.
- Fans: use the (t,σ) chart. It is C¹ with injective differential, since ∂_t has γ′-component ≥ 1 − σκρ > 0 and
  ∂_σ = k − γ ∈ Π(t).
- Sectors: use the radial map.
- Q_f: work in the chart of P_f and use a curved-triangle blending map with prescribed edge parametrizations
  (Gordon–Hall / Zlámal / Lenoir-type isoparametric elements). Such a map is C¹ up to the boundary and invertible on
  sufficiently small triangles. Cite a source.

Alternatively, follow the Prop. B′ sketch: build a curved shape-regular triangulation of h(|K|) piece by piece and
take its abstract complex as the domain. Either way, "Alexander's trick" should go; it does not give the stated
properties.

### B2. Corners of λ_v and of ∂W_v are not treated, and φ is only piecewise C¹ (major)
λ_v is not C¹:
- It has a corner at γ_e(a_e), where the two fan radii meet.
- It has a corner at k_{f,e}(a_e), where the radius in the cap D_e(a_e) meets the side-wall trace.
- It has a corner wherever it crosses an edge of ∂W_v, i.e. the junction of the stub cylinder with the ball sphere.
  Every face arc must cross such a junction twice.

Consequences:
- (i) "φ is a C¹ parametrization of the arc A_{f,v}" is false as stated. The apex estimate needs φ ∈ C¹ only on each
  base segment of a radial triangle. So require the corner preimages to be link vertices, and state that φ is C¹ with
  φ′ ≠ 0 on each link segment between consecutive corners. With that, the new apex argument goes through (B5).
- (ii) The list "Where three or more pieces meet (k(a_e), γ(a_e), corners of ∂W_v)" names the corners of ∂W_v but
  gives no argument for them.
- (iii) "∂Q_f is C¹" is used in "h as a map" and is false at the junction corners. (At k(a_e) it *is* C¹, because ρ is
  constant near a_e.)

**Fix for (ii).** Use the same tangent-cone argument as at k(a_e). Let x be a corner of λ_v on an edge of ∂W_v.
- Let T_x be the tangent cone of W_v at x. At a ball/cylinder junction W_v is a union of two convex sets, so T_x is the
  union of two half-spaces.
- Strict star-shapedness (B8) gives w = p_v − x ∈ inter T_x, so the two cone sub-sectors span⁺(ℓ₁, w) and
  span⁺(w, ℓ₂) lie in T_x. Here ℓ₁, ℓ₂ are the half-tangents of λ_v, one in each face of T_x.
- The tangent sector of Q_f lies in the closure of the complement of T_x, which is a convex wedge. This needs
  transversality of P_f to both smooth strata of ∂W_v *and* to the junction curve, which V1(b) must then require.
- So the three sectors meet only along ℓ₁, w and ℓ₂, and the tangent cone is a disk.

Also add, as a hypothesis or a lemma, that λ_v meets the junction curves transversally and avoids any vertices of
∂W_v.

### B3. The quarter-space sentence at k(a_e) is inverted (minor, but false as written)
"The fan and Q_f tangent sectors lie in the closed quarter-space {⟨·,γ′⟩ ≤ 0, ⟨·,r̂⟩ ≤ 0} … The cone sectors lie
inside it." As written, both families lie in the same set, which separates nothing. The correct picture at k(a_e) has
four tangent sectors (with ρ′(a_e) = 0, so k′ ⊥ r̂):
- the fan sector, span⁺(k′, −r̂), which lies in {⟨·,γ′⟩ ≥ 0};
- the Q_f half-plane, bounded by the line ℝk′ and containing c′ with ⟨c′, r̂⟩ > 0, which lies in {⟨·,r̂⟩ ≥ 0};
- the two cone sub-sectors, span⁺(−r̂, w) and span⁺(w, −k′), which lie in the quarter-space
  Q = {⟨·,γ′⟩ ≤ 0, ⟨·,r̂⟩ ≤ 0}, with w = p_v − k(a_e) ∈ inter Q.

So the correct statement is: "the fan and Q_f sectors lie in the closure of the complement of Q, and the cone sectors
lie in Q." The shared rays are:
- k′, between the fan and Q_f (omitted in the text);
- −r̂, between the fan and a cone sub-sector;
- w, between the two cone sub-sectors (omitted);
- −k′, between a cone sub-sector and Q_f.

The two cone sub-sectors do not fold onto each other. If −r̂, w and −k′ are coplanar, w ∈ inter Q forces
w = −a r̂ − b k′ with a, b > 0, so w lies strictly between them. Add this sentence. The argument at γ(a_e) is correct
as written: the fans lie in {⟨·,γ′⟩ ≥ 0}, the sectors in {⟨·,γ′⟩ ≤ 0} with ⟨w₀,γ′⟩ < 0, and they share only
r̂_f ≠ r̂_g.

### B4. "Shape-regular" conflicts with "radial on the cone sectors" (minor)
A triangle with apex v and a base segment of length ε on the link has diameter about |y − v|, which does not shrink,
and an apex angle about ε. So the triangulation cannot be both shape-regular and radial on the sectors. The proof in
fact uses two separate estimates, one for each kind of triangle. Say: "shape-regular off the cone sectors, radial on
them". Note that conformity holds: the sector triangles meet the fine triangles only along their base segments.

### B5. The new apex computation: correct in substance, misstated in one line (minor)
The identity is correct, under conditions that should be stated:
- the domain sector is the cone from v over a *polygonal* link arc;
- each base [y₀,y₁] of a radial triangle is a sub-segment of one link edge, so "segment of the link", not "chord";
- h(v + s(y − v)) = p_v + s(φ(y) − p_v) for y on the link, with φ = h restricted to the link, parametrized by domain
  arc length.

Since S is affine on the triangle (v, y₀, y₁), a point v + s(y − v) with y = (1−u)y₀ + uy₁ has barycentric
coordinates (1−s, s(1−u), su). Hence S = p_v + s(φ̂(y) − p_v) and (S − h) = s·e(y), where e = φ̂ − φ is affine minus
φ in the same parameter u. This is exactly homogeneous of degree one. If the base were a genuine chord, not lying on
the link, the formula for h on the triangle would involve the radial projection of y onto the link, and the identity
would fail. So the wording matters.

The derivative line is wrong as written:
- It mixes the domain point y with the image apex p_v. It should read |y − v|.
- Write x = v + s(y − v), with u the arc length along the base and τ its unit vector. Then ∂_s(S−h) = e(y) for
  ∂_s x = y − v, and ∂_u(S−h) = s e′(u) for ∂_u x = sτ.
- So D(S−h)·τ = e′(u), with *no* division by the distance to the apex. The stated bound |φ̂′ − φ′|/|y − p_v| is off
  by the factor 1/|y − v|. That factor is not scale-invariant: it *under*estimates when |y − v| > 1.
- The correct bound is ‖D(S−h)‖ ≤ (|e|/|y − v| + |e′|)/sin β. Here β is the angle between the ray y − v and the link
  edge. It is bounded below by the fixed domain geometry, since the domain link is transverse to the rays.
- Use |e′| ≤ ω(φ′, mesh), because φ̂′ is the mean of φ′ over the base, and |e| ≤ mesh · ω(φ′, mesh).
- D(S−h) is constant along rays, so the bound holds uniformly up to the apex. The triangle is convex and S − h is
  continuous at v, so Lip ≤ C ω(φ′, mesh) → 0.

The conclusion "only φ ∈ C¹ (on each link segment) is needed" is right. The curvature of λ_v is indeed not needed.
Replace the two sub-bullets with the computation above.

### B6. From per-triangle to global Lipschitz bounds (minor)
Both secant estimates are per triangle. Injectivity uses |S(x) − S(y)| ≥ |h(x) − h(y)| − Lip(S−h)|x − y| for
arbitrary x, y. This needs a global constant in the metric in which h is bi-Lipschitz. Use the intrinsic (length)
metric of the polyhedron |L|. It is bi-Lipschitz equivalent to the extrinsic one for a compact polyhedron, and in it a
per-cell Lipschitz bound is a global bound. State this. The estimate "away from the apexes"
(Lip ≤ C ω(Dh, mesh)/sin θ_min) is correct, provided h is C¹ *up to the boundary* on each closed triangle. That holds
only after B1 and B2: the triangulation must refine all pieces and have every corner as a vertex. Piecewise-C¹ h is
then enough, because the estimate is per triangle.

### B7. Scope: seams, closed edges and inner wires (major, as an overclaim)
§5.1 begins "K is regular (every face a disk bounded by a single wire)" and then gives readings of the hypotheses "for
B-rep complexes" with seam edges, closed edges and inner wires. None of these is regular, and the proof does not cover
them:
- for a seam, both fan sheets of f lie in T_e and meet along γ_e, so "gluing two disks along a boundary arc" produces
  an annulus;
- for an inner wire, Q_f is not a disk and the "2-regular graph with one cycle" argument fails.

Either restrict Theorem 5.1 explicitly to regular K, which is all the appendix proves, and mark the B-rep readings as
unproved, or prove the adapted cases.

### B8. "Strictly star-shaped" is used but never defined (minor)
The proof uses the property in three places: γ(a_e), k(a_e), and the creases along ∂W_v. In each it needs the
following: for every x ∈ ∂W_v, the vector p_v − x lies in the *interior* of the tangent cone of W_v at x. Each ray
then meets ∂W_v once and transversally. State this as the definition in V1(a). It also gives the apex claim "λ_v
transverse to the rays", including at the corners of λ_v.

### B9. Creases along ∂W_v also need V1(b) transversality (minor)
A positive opening angle between a cone sector and an outside piece needs two things:
- the cone's half-tangent w points strictly into W_v, which is B8;
- the outside piece leaves strictly outward, which is the transversality in V1(b).

Cite both. For the fans, "transversal" means that the fan meets the cap plane Π(a_e) along a radius, with tangent
plane containing k′ (or γ′), which is not in Π(a_e). Say so, since V1(b) is phrased for a curve trace.

### B10. Two arcs both called A_{f,v} (minor)
- In "Order", A_{f,v} is the arc of ∂Q_f on ∂W_v, from k_{f,e}(a_e) to k_{f,e′}(a_{e′}).
- In "Exact intersections" and in the definition of φ, A_{f,v} is the arc of λ_v contributed by f. That arc runs from
  γ_e(a_e) to γ_{e′}(a_{e′}) and includes the two cap radii.

Use two names. The sector is the cone over the longer arc.

### B11. Smaller points (minor)
- **Injectivity elsewhere.** S1(e) covers only points outside the closed set ⋃T ∪ ⋃W. Contacts between different Q_f
  on ∂T_e or ∂W_v are excluded by other facts:
  - on ∂T_e, by E3′ (k_f ≠ k_g) and S1(d);
  - on ∂W_v, by the simplicity of λ_v and E3′.

  Say so.
- **Injectivity inside T_e.** Q_f ∩ D_e(t) = {k_{f,e}(t)} also uses the fact that the section arc cannot touch
  ∂D_e(t) from inside before it exits. That holds because (|c|²/2)″ = 1 + ⟨c, c″⟩ ≥ 1 − ρk_f > 0 (E2.1). The same
  computation gives the strict ⟨c′, r̂⟩ > 0 used at the creases and for the C¹ dependence of k_{f,e} on t through the
  implicit function theorem. Worth one line.
- **Apex bi-Lipschitz.** The bi-Lipschitz property of the whole star of v needs the radial projection of λ_v to S² to
  be a bi-Lipschitz embedding. It is injective by V1(a). It is locally bi-Lipschitz by transversality, and at corners
  by the no-fold argument of B3 and B2. Also, φ must be bi-Lipschitz (φ′ ≠ 0). The current one-sentence argument omits
  the corners.
- **Order.** "One arc per vertex of f" should read "one arc per corner of f". This is the same thing for regular K;
  see B7.
- **Crease along k.** "Angle exceeds 90°" is the angle in Π(t) between −r̂ and c′, not the dihedral angle. What the
  argument needs is that the two half-planes differ. Since k′ ∉ Π(t), they could coincide only if c′ were parallel to
  −r̂, which ⟨c′, r̂⟩ > 0 rules out. Phrase it that way.

### Checked and correct (no change needed)
- **Disjointness of normal disks.** Federer 4.8(12) applies with ρ < reach of γ|[a_e,b_e], including at the end
  disks. As stated, this does not depend on ρ being constant.
- **Two radii inside one disk.** Two radii to the distinct points k_f and k_g meet only at the centre.
- **No foreign piece in T_e or W_v.** This follows from S1(b)–(d), (f) and P0, with the collar removed.
- **Cone map.** It is injective, from strict star-shapedness and the simplicity of λ_v.
- **∂Q_f is a single 2-regular cycle.** Its cyclic order is forced by V1(b), for regular K.
- **Gluing.** Gluing disks along arcs that are their whole intersection gives h(f) as a disk with
  ∂h(f) = ⋃ h(e), for regular K.
- **Zones.** The zones are monotone under augmentation. Margin m > 0 holds by compactness. The edge stubs map to
  straight segments in W_v ⊆ Z(v) ⊆ Z(e).
- **Local to global.** An injective, locally bi-Lipschitz map on a compact space is bi-Lipschitz.
- **Secant map.** S agrees with h on the radial stub edges, since h is linear in s there. S is PL and injective, and
  |S − h| < m gives the zone condition.

**Verdict on Part B.** No fatal error. The fans-and-cones construction, the injectivity argument and the cell-structure
argument are sound for regular K. The new apex argument is the right idea. (S − h) = s(φ̂ − φ) holds exactly when the
base of each radial triangle lies on a polygonal domain link. Because the error is homogeneous, Lip(S − h) → 0 needs
only φ ∈ C¹ on each link segment, with no curvature. The derivative line must be rewritten (B5).

Three items need real text:
- B1: an actual construction of a piecewise-C¹, edge-compatible h. Alexander's trick does not deliver it.
- B2: the corners of λ_v and ∂W_v, where φ is only piecewise C¹ and the tangent-cone argument is missing.
- B7: the scope claim for seams, closed edges and inner wires.

B3 is a sign or wording error in a key sentence and must be corrected, though the argument survives.

---

## Overall verdict
- **Lemma 4.1:** accept after minor revision (A1, A2, A3, A7 short additions; two source checks).
- **Appendix A:** major revision. B1, B2 and B7 are each fixable with standard tools. B3 and B5 are local corrections.
  After that, Theorem 5.1 (for regular K) is proved at the level of rigour of the rest of the paper.

---

# Follow-up on v0.5

I read the revised `sec_collar.tex` (Lemma 4.1), `sec_existence.tex` §5.1 and `sec_proof51.tex`. Line numbers refer to
the v0.5 files.

## Status of the v0.4 findings

| Item | Status | Where / comment |
| --- | --- | --- |
| A1 (outer side, which component) | **Fixed** | collar l.59–63, completed in Step 3, l.80. Correct. |
| A2 (∂A± = level sets) | **Fixed** | collar l.70–80. Correct. |
| A3 (Durfee; sides of N̄_δ; δ < r) | **Fixed in the text, source check pending** | l.32–41. The argument for the two sides is correct. The `\unverified` tag on Durfee's regularity and on "rel M" remains, as it should. |
| A4 (form of CL07 Prop. 3.4) | **Partly fixed** | l.64–65. The new fallback is invalid; see N4. |
| A5 (criticality notions) | No change needed | — |
| A6 (Moise, noncompact case) | **Fixed, tag pending** | l.95–96. Moise 1952 is now cited. |
| A7 (inter N̄_r = N_r) | **Fixed** | l.75–77 and l.90–91. The proof is given. The derivative formula for d should be added to the list of standard facts or cited (N9). |
| A8 (wording; where genus is used) | **Fixed** | Genus is now assumed only in (b), l.18. (a) and (a′) are correct for a sphere too. |
| B1 (construction of h) | **Largely fixed** | proof51 l.98–136. Residual issues: N1 and N5. |
| B2 (corners of λ_v; junctions) | **Fixed in substance** | l.34–42 and l.170–179; V1(b) strengthened (existence l.51–56). The justification at the junctions has a gap (N2). |
| B3 (quarter-space sentence) | **Fixed** | l.155–166. Correct, including the shared rays and the no-fold argument. |
| B4 (shape-regular vs radial) | **Fixed** | l.186–193. |
| B5 (apex derivative) | **Fixed** | l.199–217. Correct; notation remark in N6. |
| B6 (intrinsic metric) | **Fixed** | l.139–140 and l.218–222. |
| B7 (scope: seams, closed edges, inner wires) | **Fixed** | existence l.11–15. The scope is now restricted and stated honestly. |
| B8 ("strictly star-shaped" undefined) | **Fixed, with a new overclaim** | existence l.48–50; see N3. |
| B9 (creases on ∂W_v need V1(b)) | **Fixed** | l.151–153. Wording remark in N7. |
| B10 (two arcs named A_{f,v}) | **Fixed** | l.14–19. A_{f,v} and Λ_{f,v} are now used consistently. |
| B11 (smaller points) | **Fixed** | Injectivity on ∂T/∂W: l.70–72. Convexity computation: l.5–9, correct; it also gives ⟨c′,r̂⟩ > 0 strictly. Apex: l.180–183. "Per corner": l.78. Crease along k: l.147–149. |

## Checks of the new text

**Edge agreement of the cell maps (the main question).** I checked every kind of shared edge.
- *Fan / Q_f along k_{f,e}.* Both cells use the parametrization t ↦ k(t) (l.111, l.122–123). They agree.
- *Fan / sector along the end radius at a_e.* The fan gives σ ↦ γ(a_e) + σ(k(a_e) − γ(a_e)), which is affine. φ is
  chosen to equal it (l.118). They agree.
- *Q_f / sector along A_{f,v}.* Both use φ. The definition is circular as written: l.118–119 says φ "agrees with the
  parametrization used for Q_f", and l.123 says Q_f uses "the restriction of φ". Harmless, but write it as one choice:
  first fix φ on A_{f,v} as any C¹ regular parametrization that is affine in the domain link coordinate on each
  segment, and then use it on both sides.
- *Sector_f / sector_g along the stub [p_v, γ_e(a_e)].* Both cells are radial over the same link vertex y_e, so both
  give s ↦ p_v + s(γ_e(a_e) − p_v). They agree.
- *Fan_f / fan_g along γ_e.* Both give σ = 0, t ↦ γ_e(t). They agree if the two domain cells induce the same affine t
  on their common edge. Say so.
- *Domain fan cell.* The chart is defined on the rectangle [a_e,b_e]×[0,1]. The domain cell of L is a convex
  quadrilateral, so precompose with a bilinear diffeomorphism. It is affine on each edge, so edge agreement survives.
  One sentence.

With these, the cell maps glue to a homeomorphism. Each cell map is injective, and the image pieces meet exactly
according to the cell structure.

**Fan differential (l.109–110).** Correct. With k = γ + ρu and ρ′ = 0 or not, ⟨k′,γ′⟩ ≥ 1 − ρκ, so
⟨∂_t, γ′⟩ = 1 + σ(⟨k′,γ′⟩ − 1) ≥ 1 − σρκ > 0. Also ∂_σ ∈ Π(t) is nonzero and orthogonal to γ′.

**Exit points (l.5–9).** Correct. While |c| ≤ ρ we have (|c|²/2)″ ≥ 1 − ρk_f > 0, so |c|² is strictly convex up to the
first hit. Its derivative there is at least (ρ² − dev*²)/(2σ*) > 0, which gives ⟨c′,r̂⟩ > 0 strictly. E2.3 excludes
re-entry. The C¹ dependence on t then follows from the implicit function theorem.

**Revised apex estimate (l.199–217).** Correct.
- The barycentric computation and (S−h) = s·e(y) are right, because the base lies on one link segment.
- ∂_s(S−h) = e(y) and D(S−h)·τ = de/d(arc length).
- The bound ‖D(S−h)‖ ≤ (|e|/|y−v| + |e′|)/sin β is right, with β bounded below by the domain geometry.
- |e′| ≤ ω and |e| ≤ mesh·ω.
- D(S−h) is constant along rays, so the bound holds uniformly up to the apex, and Lip(S−h) → 0.

**Junction crossings (l.170–179).** The conclusion is right, but one step is unjustified (N2).

## New findings

**N1. Sector cells are not C¹ on the whole closed cell (minor).**
- l.99–100 claims h is "C¹, with injective differential, on each closed domain cell (except at the apexes)". A sector
  cell is the cone over a link arc that contains corners: k_{f,e}(a_e), the junction crossings, and k_{f,e′}(a_{e′}).
  The radial map is only piecewise C¹ there. It is C¹ on each sub-cone over one link segment, and it has creases along
  the rays from v to the corner preimages.
- These rays are creases of h. They are not in the crease list (l.145–154), and neither are the stub rays between
  sector_f and sector_g.
- Fix: make the sub-cones the cells of L. Note that along a ray the tangent half-planes are constant, by homogeneity.
  So the no-fold argument at the corner x (or at γ(a_e) for a stub ray) gives the positive opening angle along the
  whole open ray.
- The radial map has injective differential on each sub-cone, since φ′(y) is not parallel to φ(y) − p_v. That is
  transversality of λ_v to the rays, including for the end radii, where w has a γ′-component. Say so.

**N2. Junction crossings: "w ∈ inter T_x, so the sub-sectors lie in T_x" is a non sequitur (minor).**
T_x = H₁ ∪ H₂ is not convex.
- *Counterexample to the inference.* Take ℓ₁ ∈ ∂H₁ with ℓ₁ ∉ H₂, and w ∈ inter H₂ with w ∉ H₁. Then span⁺(ℓ₁, w)
  contains vectors in the open wedge ∁H₁ ∩ ∁H₂.
- *Correct reason.* Star-shapedness itself: each segment [p_v, y], for y ∈ λ_v near x, lies in W_v. So the tangent cone
  span⁺(ℓᵢ, w) of the cone surface lies in T_x. Equivalently, this forces w ∈ H₁ ∩ H₂.
- *Consequence.* With w ∈ H₁ ∩ H₂, each sub-sector meets the face where its half-tangent lies only along ℓᵢ. The
  outside sector, P ∩ (closed complementary wedge), is the convex sector between ℓ₁ and ℓ₂. So the only shared rays are
  ℓ₁ and ℓ₂.
- *Missing no-fold step.* The no-fold of the two cone sub-sectors is not argued at the junction, and not at γ(a_e)
  either.
  - At the junction, ℓ₁ and ℓ₂ span the tangent plane P of the outside piece. If w ∈ P, then w lies outside the convex
    sector between ℓ₁ and ℓ₂, because that sector is in the closed complement of T_x and w ∈ inter T_x. So w is
    strictly between them on the reflex side, and there is no fold.
  - At γ(a_e), r̂_f and r̂_g lie in Π while w₀ ∉ Π. No fold.
- Add these two sentences.

**N3. V1(a): the parenthetical "so each ray from p_v meets ∂W_v once" does not follow from the local definition (minor
logically, easy fix).**
- At a junction point x, T_x is a union of two half-spaces. Both p_v − x and x − p_v can then lie in T_x, so the ray
  through x can graze ∂W_v at x and stay inside W_v. That gives two points of ∂W_v on one ray. Both the injectivity of
  the cone map (l.61–62) and the cone construction use "once".
- I believe the local condition at nearby smooth points rules out the transversal-grazing case. The tangential case is
  not obviously excluded, and the text gives no argument either way.
- Fix: make the global property part of the hypothesis: "each ray from p_v meets ∂W_v in exactly one point".
  Equivalently, add "x − p_v ∉ T_x" to the local condition. The checker can test this directly.

**N4. Collar l.64–65: the half-open fallback is invalid as stated (minor).**
"Apply it with a slightly larger r′ < wfs and restrict" works only if the homeomorphism is level-preserving.
Restricting an arbitrary homeomorphism {δ ≤ R ≤ r′} ≅ C × [δ, r′] to {δ ≤ R ≤ r} gives no product structure. That is
exactly the issue A1/A2 worked around. Fix: either rely on the closed-shell form, if that is what CL07 states (keep the
tag), or cite the fact that CL07's homeomorphism is built by integrating a flow along which R is strictly increasing.
That makes it level-preserving, and then restriction is fine.

**N5. Q_f cells: the Gordon–Hall citation and the domain side (minor; tag already present).**
- Triangular transfinite (Boolean-sum) interpolants with three curved edges can have singular or non-C¹ derivatives
  at the vertices. "C¹ up to the boundary" at a corner of ∂Q_f is the delicate point.
- Safer construction: refine so that each curved triangle has at most one curved edge. Two triangles meet at every
  corner of ∂Q_f, so this is always possible. Then use the one-curved-edge maps of Lenoir (SIAM J. Numer. Anal. 23,
  1986) or Bernardi (SIAM J. Numer. Anal. 26, 1989). These are C^m up to the boundary and invertible for fine
  subdivisions, given C¹ edge data.
- Note that the corner angles of Q_f at junction crossings lie in (0, π). The complement of W_v is locally a convex
  wedge, and transversality of P_f excludes 0. So the corner triangles are non-degenerate.
- State also that the domain Q_f cell of L is triangulated by straight triangles with the same combinatorics as the
  curved subdivision, so L is refined accordingly. At present l.102 has a single 2-cell for Q_f, and l.126 subdivides
  only the image.

**N6. Apex notation (minor).**
u is "proportional to arc length", but ∂_u x = s(y₁ − y₀) = s|y₁ − y₀|τ, not sτ. Then D(S−h)·τ is the derivative of
e with respect to arc length, and the bound |e′| ≤ ω(φ′, mesh) is for that derivative. Define ′ as d/d(arc length),
or take u to be arc length.

**N7. Fan tangent plane along the end radius (minor).**
l.153 says the tangent plane "contains k′ or γ′". It contains ∂_t = γ′ + σ(k′ − γ′), which is neither in general.
Write instead: it contains ∂_t, whose γ′-component is at least 1 − σρκ > 0, so the plane is not Π(a_e).

**N8. From "tangent cone is an embedded disk" to local bi-Lipschitz (minor).**
This step needs a stated fact: a map that is C¹ up to a point on each of finitely many closed domain sectors, and whose
piecewise-linear tangent map at that point is injective, is bi-Lipschitz near the point. It requires one-sided C¹ up to
the corner on each sector, which is where N5 matters. Add it to the list of standard facts at l.228–232.

**N9. Collar l.75–77 (minor).** The one-sided derivative formula d′(x; u) = min_{y∈Γ(x)} ⟨u, (x−y)/|x−y|⟩ should be
cited (e.g. Lieutier 2004, Lemma 1) or listed among the standard facts.

## Overclaims
- None at the level of the theorems. Theorem 5.1 is now stated for regular K only. Lemma 4.1's genus hypothesis sits
  where it is used.
- The two small overclaims are the V1(a) parenthetical (N3) and the half-open fallback in the collar proof (N4).

## Verdict on v0.5
- **Lemma 4.1:** accept, subject to the three source checks already tagged: Durfee's regularity and "rel M", the exact
  form of CL07 Prop. 3.4, and Moise for the noncompact case. N4 must be fixed if the CL07 statement is half-open. N9 is
  cosmetic.
- **Appendix A:** minor revision. The piecewise construction of h now closes: the cell maps agree on every shared edge
  (modulo the two one-line clarifications above). The tangent-cone arguments at k(a_e) and γ(a_e) are correct. The
  revised apex estimate is correct. What remains is local:
  - N1: make the sub-cones the cells, and treat the corner rays as creases by homogeneity;
  - N2: correct the junction justification and add the no-fold sentences;
  - N3: state ray-once as a hypothesis;
  - N5: one-curved-edge elements and the domain triangulation;
  - N6–N8: notation and a standard fact.

  None of these threatens the theorem.
