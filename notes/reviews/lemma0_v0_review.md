# Review of Lemma 0 (existence), draft v0 (11-12)

Reviewer stance: skeptical. Every problem comes with a counterexample or a failure scenario, followed by an exact fix.

## Verdict summary

| Q | Topic | Verdict |
|---|---|---|
| 1 | Construction | **Wrong as written; correct with fix.** It fails at every vertex, even on an exact cube corner, because of the gap between the tube end and the ball (1a). Several hypotheses are also missing or garbled (1b–1f). |
| 2 | E2 / E3 strength | **Correct with fix.** E2 is reasonable away from vertices, but the argument "transverse ⇒ crosses once" is wrong; the fix is a convexity argument. E3 needs a real margin τ_e > dev_e: with τ_e close to dev_e it fails on a 90° edge (2c). |
| 3 | PL approximation | **Wrong as justified; correct with fix.** Injectivity is not an open condition in C⁰. The fix uses bi-Lipschitz plus secant interpolation, and makes the zone inequalities strict. |
| 4 | Literature | The cone/fan construction is **not** in ASZ 2007 or Stewart–Zidani 2008, as far as the local texts show. Both use a different realization (Whitney-extension perturbation), and both **assume** that it embeds rather than derive it. APS 2000 and ASZ 2006 are not available locally and were not read. |
| 5 | Quantitative E2/E3 | Sufficient conditions are given below, with leading-order forms. |

---

## Q1. Construction

### 1a. Gap at the junction of tube and ball (fatal as written)

Step 2 builds fans on normal disks D_ρ(t) centred at γ_e(t) **outside** B(p_v, r_v). Step 4 cones inside the sphere. Near the sphere, the round sphere and the flat normal disks do not fit together.

**Counterexample (exact cube corner, dev = 0).**
- Setup: p_v = 0 and γ_e(t) = (t, 0, 0). Face f is the plane z = 0 with y ≥ 0, and face g is the plane y = 0 with z ≥ 0.
- The edge leaves the ball at (r, 0, 0). The first normal disk is D(r) = {x = r, y² + z² ≤ ρ²}. It is tangent to the sphere there.
- **Reading A: "tube" = metric tube N_ρ(γ_e).** Step 3 discards the patch in L = {(x, y, 0) : 0 < y ≤ ρ, √(r² − y²) ≤ x < r}. L lies outside the ball and inside N_ρ(γ_e), but no fan covers it, because every fan lies in a disk with x ≥ r. The result is a hole in h(f), even with exact data.
- **Reading B: "tube" = union of the outside normal disks.** With exact data this works. Now give f a gap dev > 0, so P_f = {z = 0, y ≥ dev}. The kept patch then has the free boundary segment {(x, dev, 0) : √(r² − dev²) ≤ x < r}, which nothing glues to. The hole is bounded by:
  - that segment;
  - the fan end segment from (r, 0, 0) to (r, dev, 0);
  - a sphere arc.
- **V1 is unsatisfiable here.** The trace of f on the sphere starts at (√(r² − dev²), dev, 0), not at the edge point. The fan meets the sphere only at the single point (r, 0, 0), and tangentially.

So V1 fails for the most ordinary gapped model, a box. This is the "part of γ_e and the fans between the tube region and the ball" that the question asks about.

**Fix: replace the round ball by a star-shaped vertex region whose boundary contains the end disks.**
- For each edge end at v, choose a parameter a_e with |γ_e(a_e) − p_v| ≥ r_v + ρ_e, so that D_ρ(a_e) ∩ B(p_v, r_v) = ∅.
- Define
  - W_v = B(p_v, r_v) ∪ ⋃_{e∋v} ⋃_{t between v and a_e} D_ρ(t);
  - T_e = ⋃_{t∈[a_e, b_e]} D_ρ(t). This is a union of normal disks, not the metric neighbourhood, so there are no end caps.
- Replace V1 by:
  - **V1′(a).** W_v is strictly star-shaped with respect to p_v (every ray from p_v meets ∂W_v once, transversally), and W_v ⊂ int B(p_v, τ_v).
  - **V1′(b).** The data outside W_v meets ∂W_v transversally in a simple closed curve. On it, the fan segment of each incident face f in the end disk D_ρ(a_e) runs from γ_e(a_e) to k_{f,e}(a_e). Each face arc joins the points of the two edges of f at v. The cyclic order agrees with lk(v, K).
- Then cone from p_v over that curve. The cone is embedded by star-shapedness, it is glued exactly along ∂W_v, and the end fan segments now lie on ∂W_v.
- Sufficient condition for V1′(a): on [0, a_e], ∠(γ_e′(t), γ_e(t) − p_v) ≤ β_v < π/2, and ρ is small next to r_v cos β_v. In the straight radial case W_v is ball ∪ cylinder, which is convex.
- Check on the cube: the trace of f on ∂W_v is the end-disk segment, then the line y = ρ on the cylinder wall, then the sphere arc. That is an arc starting at the edge point, as required.
- **Cost of the fix (affects Q2).** The end disks of two edges at angle θ are disjoint only if |γ(a_e) − p_v| > ρ / sin(θ/2). This needs τ_v > ρ·√(1 + 1/sin²(θ/2)), with ρ > dev_e.
  - Cube corner: τ_v > √3·dev_e.
  - 10° corner: τ_v > about 11.5·dev_e.
  - Cusp vertices (two edges leaving v tangentially, θ = 0): the tubes overlap along a length of about √(4ρ/|Δκ|), which is far larger than typical τ_v. The construction cannot work there. Exclude cusp vertices explicitly, or treat them separately.
  - OCC's usual invariant τ_v ≥ τ_e does not imply any of these bounds.

### 1b. S1, last clause, is a tautology, and the real condition is missing

"Outside all balls and tubes, the patches … miss non-incident tubes and balls" is trivially true.

**Counterexample (thin wall of thickness w < ρ).**
- The top face P_top passes within ρ of a bottom edge e, which is not incident to top.
- The patches do not intersect, so S1 as written holds.
- Step 3 deletes the part of P_top that lies inside T_e, and no fan of top replaces it. The result is a hole.

**Fix.** Make the missing condition explicit:
- **S1(d).** P_f ∩ T_e = ∅ for e ⊄ ∂f, and P_f ∩ W_v = ∅ for v ∉ ∂f.
- **S1(e)** (also missing). T_e ∩ W_w = ∅ for w ∉ ∂e, and γ_e misses W_w as well. Without it, a non-incident edge passing through a vertex ball would be overwritten by the cone.

S1(d) and S1(e) exclude sliver faces and thin walls of width below 2ρ. In imported models with loose healing tolerances that is a real restriction; record it as a limitation.

### 1c. Missing: each patch must itself be embedded

S1 only requires different patches to be disjoint.

**Fix.** Add **P0**: P_f ∖ int(⋃T ∪ ⋃W) is embedded, and is a closed disk onto which P_f retracts. In other words, P_f ∩ (⋃T_e ∪ ⋃W_v) is a collar of ∂P_f.

This collar property is also exactly what makes h(f) a 2-cell with boundary h(∂f). The draft never checks that the image cell structure is isomorphic to K.

### 1d. "Cone over an embedded graph is embedded" (question 1c)

- **True.** (s, y) ↦ p_v + s(y − p_v) is injective for s > 0 when each ray meets the sphere, or ∂W_v, once.
- **Not sufficient on its own.** It also needs:
  - 1b's S1(e), so that nothing else is inside the vertex region;
  - V1′(b)'s combinatorics. With only "one point per edge, one arc per face", nothing forces each arc to join the right two edge points in the order of lk(v).

### 1e. Data at vertices

The draft never requires γ_e's endpoint, or the corner of P_f, to lie in int B(p_v, r_v). Since r_v ≤ τ_v is free, take r_v small: then γ_e(0) lies outside the ball and the edge never reaches the cone.

**Fix.** Require dist(p_v, γ_e(0)) < r_v and dist(p_v, corners of P_f) < r_v, and require γ_e to cross ∂W_v exactly once (part of V1′).

### 1f. Applicability of "regular CW complex"

A regular CW complex excludes three things that are standard in B-reps:
- seam edges, such as the lateral face of a cylinder (an edge used twice by one face);
- closed edges with a single vertex, such as a full circle;
- faces with inner wires, such as a plate face with a hole (an annulus, not a 2-cell).

**Fix.** Either:
- state Lemma 0 for "B-rep complexes", in which faces are compact surfaces with boundary and an edge may occur twice in ∂f. The construction never uses that faces are disks once P0 is phrased as "the collar complement is homeomorphic to the face". E3 then refers to the two sheets of f at a seam, and V1′ counts edge **ends**, not edges; or
- add a preprocessing lemma that cuts faces with zero-deviation edges.

### 1g. Zone membership

Zone membership is fine once the inequalities are strict:
- ρ_e < τ_e and W_v ⊂ int B(p_v, τ_v), so there is slack for step 5;
- the fans lie in T_e ⊂ N_ρ(γ_e) ⊂ Z(e) ⊂ Z(f);
- the cones lie in W_v ⊂ Z(v).

---

## Q2. Is E2 too strong, or unsatisfiable?

### 2a. The convex-gap argument in the draft is incomplete

"Boundary within dev, transverse at the wall ⇒ crosses once" does not follow. Transversality at a crossing says nothing about how many crossings there are.

A correct argument works in the normal plane Π(t). Let c(s) be the arc-length section of P_f starting at its boundary point b_f(t), with |b_f(t) − γ(t)| ≤ dev*, and let g(s) = |c(s) − γ(t)|². Then

g″ = 2(1 + ⟨c − γ, c″⟩) ≥ 2(1 − ρk),

where k = κ_f / cos ψ_f is a bound for the section curvature (Meusnier). If ρk < 1, g is strictly convex inside the disk. From g(0) < ρ² it then crosses ρ² **exactly once**, and does so with g′ > 0, which is transversal.

### 2b. Overlap

**Overlap does not by itself cause a double crossing.** The boundary point is still inside the tube (dev* < ρ), and the convexity argument does not care which side γ_e the boundary lies on.

Double crossings do come from three other situations.

1. **Strong curvature or a narrow patch.** If ρk ≥ 1, take for example a fillet face of radius R < ρ next to the edge, or a narrow rib face. Its section can stay inside the disk (no k-curve at all), or leave and re-enter (two crossings).
2. **Non-monotone pcurve image.** A SameParameter bound |β(t) − γ(t)| ≤ dev does not prevent β from moving back and forth along γ.
   - Example: β(t) = γ(t + ε sin Ωt) + (small helix), with ε ≤ dev and Ω large.
   - β is injective and within dev, but crosses some normal planes three times. Then b_f(t) is not unique and E2 fails.
   - ASZ's Lipschitz constant L of the discrepancy is exactly the quantity that rules this out.
3. **Return of the patch.** P_f can come back within ρ of γ_e far from its boundary, for example a curled flange.

**Typical models.** Interior edges of mechanical parts with tolerance ≪ (curvature radius, sliver width) satisfy E2. The risky cases are:
- small fillets combined with loose tolerances;
- slivers and thin walls;
- re-approximated pcurves;
- the τ_e ≈ dev margin in 2c.

### 2c. E3 needs a margin τ_e > dev_e that the draft does not mention

**Counterexample (90° edge, overlap).**
- In Π(t): f has boundary point (0, d) and runs in direction (1, 0); g has boundary point (d, 0) and runs in direction (0, 1). Both are within d of γ(t).
- The exit points are (√(ρ² − d²), d) and (d, √(ρ² − d²)). They coincide when d = ρ/√2.
- Then the two fans share a radial segment, and the result is not embedded.

So on a right-angle edge E3 needs ρ > √2·dev*. In general it needs α > 2 arcsin(dev*/ρ) or more.

If OCC's edge tolerance equals the measured deviation (τ_e = dev_e), the range dev_e < ρ ≤ τ_e is empty. If τ_e = 1.05·dev, E3 needs α > 144°, so every 90° edge fails.

**Fix.** Make the margin a hypothesis: τ_e ≥ c·dev*_e, with c chosen from Q5. Alternatively, use the ASZ realization (Q4), which needs no ρ > dev margin for the edge gluing.

---

## Q3. PL approximation

### 3a. "All conditions are open" is false in C⁰

A PL approximation converges in C⁰, but injectivity is not C⁰-open. A C⁰-close approximation can fold or overlap at the creases, which are k, γ_e and ∂W_v. Approximating the pieces separately, with non-matching triangulations along shared curves, also leaves gaps.

### 3b. Fix

1. **h is bi-Lipschitz on |K|.** Use the path metric of the image. h is injective, compact and locally bi-Lipschitz, so it is globally bi-Lipschitz with some constant c > 0. Locally bi-Lipschitz holds because every crease has a non-zero opening angle:
   - **Fan/patch along k.** The fan leaves k in direction −r̂, the patch leaves in a direction with c′·r̂ > 0 (2a). The angle is > 90°, so there is no fold.
   - **Fan/fan along γ_e.** The angle between the two exit points is > 0 by E3.
   - **Cone/outside along ∂W_v.** By strict star-shapedness, the cone's direction −(x − p_v) points into W_v and the outside piece points out.
2. **Choose a triangulation.** Use a shape-regular triangulation of |K| that:
   - refines the decomposition into patch pieces, fan strips and cone sectors;
   - has p_v as a vertex;
   - triangulates the cone sectors radially;
   - is fine enough that h is C² on every closed triangle.
3. **Use the secant (vertex-interpolating) map S.**
   - Lip(S − h) ≤ C·(mesh)·|D²h| / sin θ_min → 0, and |S − h| ≤ C·(mesh)²·|D²h|.
   - Then |S(x) − S(y)| ≥ (c − Lip(S − h))·|x − y| > 0, so S is injective.
   - On cone sectors, S is exactly the cone over the inscribed polygon.
4. **Zones.** Take mesh small enough that |S − h| is below the slack min(τ_e − ρ_e, dist(W_v, ∂B(p_v, τ_v)), τ_f-margin). Then h(int σ) ⊆ Z(σ) survives.

(A citation alternative is the taming of locally flat surfaces in R³ (Bing/Moise). I did not verify a source for it here, so I give no citation.)

---

## Q4. Literature (only the local texts were read)

### ASZ 2007, SIAM J. Sci. Comput. 29(2), pp. 811–826

File: `pdfs2/2dcdd9cf…040604303.txt`.

- **Realization.** It is not a cone/fan construction. Each patch is perturbed by the Whitney/McShane extension of the boundary discrepancy:
  - p. 818, (3.1): "δ(p) = β^k([p^k]^{-1}(p)) − F(p), p ∈ ∂D";
  - p. 819, Prop. 3.2: the extension satisfies "|δ(p)| ≤ sup_{q∈∂D} |δ(q)|".
  - Edge curves are reconciled with the vertices by linear interpolation of the endpoint differences: p. 817, "β^k(t) = b^k(t) + (1 − t)[v − b^k(0)] + t[v′ − b^k(1)]".
- **Embedding is assumed, not proved.** p. 819–820: "each perturbed patch … must not self-intersect, adjacent perturbed patches … may intersect only at a common corner point or along a common boundary curve, and nonadjacent perturbed patches must be disjoint. If all of the above conditions are satisfied, then S is well defined".
  - Some a priori criteria are given on p. 820: injectivity "provided that the product of L and a Lipschitz constant for F^{-1} is less than 1".
  - The same page continues: "adjacent patches sharing a common edge or vertex cannot be dealt with in this way … it will be necessary to rely on a posteriori (computational) verification."
- **Normal bound.** p. 825: the third component of the normal is "no smaller than 1 − L² − O(L³)".
- **"Proof of correctness" / "Proj. Approx."** No section with these titles appears in this text. The non-self-intersection paper is only cited, as ref. [24] (ASZ, CAGD 23 (2006) 599–611, cited on p. 820), and was not read.

### Stewart–Zidani 2008, LNCS 5045, pp. 181–192

File: `audit/stewart_zidani2008.txt`.

- p. 185: the perturbed patches "fit together in a way that is exactly consistent with the topological data".
- p. 188: "the patches provided by Whitney Extension guarantee that adjoining patches will meet properly at a common edge, but we must exclude the possibility that there are other intersections".
- p. 191: "cos φ ≥ 1 − (L²/2)(E + 2F + G)/(EG − F²)".
- No vertex cones, no tubes, no fans.

### Andersson–Peters–Stewart 2000

Not available locally and not read. ASZ cites it as ref. [10], "Equivalence of topological form for curvilinear geometric objects", IJCGA 10 (2000) 609–622. ASZ footnote 7 (p. 820) says it gives "sufficient conditions that perturbations of the control points should produce an object, linked to the original by an ambient isotopy". Whether it uses tubes or fans is unknown. **Obtain it before claiming novelty.**

### Assessment

| Point | Status |
|---|---|
| Local cone/fan realization of a tolerant B-rep | Not found in the two texts read. That does not show it is new. |
| Relationship to ASZ | ASZ's realization is a **different, cheaper route** to the same goal: patches meet exactly along the β curves, and every patch lies in N_{dev}(P_f), so zone membership is automatic. |
| What ASZ leaves open | The extraneous-intersection / embedding step, which is assumed. |
| Value of Lemma 0 | Deriving embedding from local tolerance hypotheses is the part that would add something beyond ASZ. |

Recommendation: state the relationship explicitly, and consider proving Lemma 0 with the ASZ perturbation plus Q5-type normal-angle conditions near edges.

---

## Q5. Quantitative sufficient conditions (for each edge e, adjacent face f, and t outside the W_v)

### Notation

| Symbol | Meaning |
|---|---|
| dev*_e | max_t \|b_f(t) − γ_e(t)\|, measured inside Π(t). Equals dev_e + O(κ_γ·dev_e²). |
| κ_f | max \|principal curvature\| of P_f within T_e |
| ψ_f | max angle between γ_e′ and T P_f there |
| k_f | κ_f / cos ψ_f (bound on section curvature) |
| μ_f | 1 − ρ·k_f |
| ℓ_f | (dev* + √(dev*² + μ_f ρ²)) / μ_f (maximum section length to the wall) |
| α_e(t) | angle between u_f and u_g, the unit in-plane tangents of the two sections at their boundary points, pointing into the patches (= dihedral opening angle, in [0, π]) |

### E2 holds if all of the following hold

1. dev*_e < ρ_e < reach(γ_e|[a_e, b_e]).
2. ψ_f < π/2 and ρ_e·k_f < 1.
3. **Monotone boundary.** The projection t ↦ π_e(β_f(t)) is strictly monotone. To first order this holds if L_e + κ_γ·dev*_e < 1, where L_e is the Lipschitz constant of the discrepancy β_f − γ_e with respect to arc length, i.e. ASZ's L.
4. **No return.** dist(γ_e(t), P_f ∖ C_f) > ρ_e, where C_f is the union of the section arcs of length ≤ ℓ_f starting at β_f. These arcs must also exist: P_f extends at least ℓ_f beyond β_f in each section.

Then each section crosses the wall exactly once, transversally (2a), and the set of exit points k_{f,e} is a curve meeting every normal circle once.

### E3 holds if

α_e(t) > ε_f + ε_g, where ε_f = arcsin( min{1, (dev*_e + k_f ℓ_f²/2) / ρ_e} ).

Proof sketch: the exit point equals b + s*·u + e with |e| ≤ k s*²/2 and s* ≤ ℓ. Its perpendicular offset from the ray along u is at most dev* + kℓ²/2, so its direction is within ε of u.

### Leading order (dev*, kρ ≪ 1)

- ε ≈ dev*/ρ + kρ/2.
- This is minimised at ρ = √(2·dev*/k), giving **α_e > 2·√(2·k·dev*)**, provided √(2·dev*/k) ≤ τ_e.
- Otherwise take ρ = τ_e, and the condition is **α_e > 2·(dev*/τ_e + k·τ_e/2)**.
- Worst-case necessity: in the straight-section case of 2c, α_e > 2·arcsin(dev*/ρ) is needed. So τ_e must exceed dev*/sin(α_e/2): √2·dev* for a 90° edge.

### Worked numbers

| Case | Requirement |
|---|---|
| dev* ≤ ρ/10, kρ ≤ 1/10 | ℓ ≤ 1.17ρ, ε ≤ 9.7°, so α > 19.4° suffices |
| dev* ≤ ρ/4, kρ ≤ 1/4 | ℓ ≤ 1.54ρ, ε ≤ 33°, so α > 66° |

### Vertex side

Combine with the vertex conditions from 1a:
- |γ_e(a_e) − p_v| > ρ / sin(θ_min/2);
- W_v ⊂ int B(p_v, τ_v), i.e. τ_v > ρ·√(1 + 1/sin²(θ_min/2)) for straight radial edges;
- the radial-transversality angle β_v < π/2.

---

## Corrected hypothesis list (drop-in)

| Label | Hypothesis |
|---|---|
| E1 | dev*_e < ρ_e < min(τ_e, reach(γ_e\|[a_e, b_e])), with T_e the union of normal disks |
| E2 | Q5 E2 conditions 1–4 |
| E3 | Q5 E3 condition |
| V0 | γ_e ends and P_f corners lie in int B(p_v, r_v) |
| V1′ | (a) W_v strictly star-shaped, W_v ⊂ int B(p_v, τ_v); (b) link curve on ∂W_v with the correct combinatorics |
| S1 | (a) W_v pairwise disjoint; (b) T_e pairwise disjoint (including incident edges, outside W_v); (c) γ_e and T_e miss W_w for w ∉ ∂e; (d) P_f misses T_e (e ⊄ ∂f) and W_v (v ∉ ∂f); (e) outside ⋃T ∪ ⋃W the patch pieces are pairwise disjoint |
| P0 | Each P_f is embedded, and P_f ∩ (⋃T ∪ ⋃W) is a collar of ∂P_f |
| Strictness | ρ_e < τ_e, and zone margins positive |
| Complex | B-rep complex (seams, closed edges, multi-wire faces allowed), or a preprocessing cut |

Construction step 4 becomes "cone over the link on ∂W_v". Step 5 becomes the bi-Lipschitz secant argument of Q3.
