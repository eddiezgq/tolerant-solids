# Review of Lemma 0 (existence), draft v0.1 (11-12)

Independent reviewer, first reading. Scratch scripts: `audit/r01/e3_eps2.py`, `audit/r01/v1a_offset.py`.

## Verdict summary

| # | Item | Verdict |
|---|---|---|
| 1 | Section 4 justified by the hypotheses | **Correct with fix.** Two citations point to hypotheses that do not cover the case (incident edges and the own vertex region). Several hypotheses are stated only on [a_e, b_e] but are used on the stubs [0, a_e]. Section 2 says "all computable", but V1(b) and P0 are topological assumptions that nothing computable implies. |
| 2 | W_v and λ_v consistency | **Correct with fix.** The pieces and the end disks are right. The *sufficient* condition for V1(a) is **wrong**: there is a concrete counterexample (6A). Also, the condition \|γ(a_e) − p_v\| ≥ r_v + ρ from the v0 review was dropped. |
| 3 | h(f) is a closed disk with boundary h(∂f) | **Correct given P0 + V1(b), but not proved as written.** The order and intersection argument is missing, and h is only defined as an image set, not as a map. |
| 4 | PL step | **Conclusion correct, argument wrong in three places:** C² fails at the apex; C² fails on the fans (they are only C¹); and "non-zero crease angle" is not enough at the vertices of the piece decomposition. All three can be repaired. |
| 5 | E2/E3 quantities | **Correct.** One small improvement: dev* ≤ dev exactly. One definitional repair in E2.3 (overshoot of C_f). The E3 exit-angle bound is confirmed numerically. |
| 6 | Counterexample | Model 6A satisfies the stated *sufficient* conditions for V1(a), and the cone overlaps itself. I found no model that satisfies V1(a), V1(b) and P0 as hypotheses and still breaks the construction. The weak point is that those three hypotheses carry the topology. |

**v0-review fixes.**
- Incorporated: 1a (W_v, T_e as a union of normal disks), 1b (S1(c, d)), 1c (P0), 1d, 1e (V0), 1f (§6), 2a–2c, Q3, Q5.
- Dropped: \|γ(a_e) − p_v\| ≥ r_v + ρ_e, which made D_e(a_e) miss the ball.
- Not carried over: the extension of E1 and E2 to the stubs.

---

## 1. Section 4 against the hypotheses

### 1.1 "No other piece enters W_v: S1(a, c, d)" and "No other piece enters T_e: S1(b)–(d)"

S1(c) covers only w ∉ ∂e. Nothing stated controls:
- the own vertex region W_v against T_e, its fans and γ_e|[a_e, b_e], for v ∈ ∂e;
- the stubs of other edges e′ at v against T_e.

Two failure scenarios:
- **Edge loops back.** e leaves v, turns, and passes within r_v + ρ of p_v at some t > a_e. E1 involves only reach(γ_e|[a_e, b_e]), and S1 does not mention it. T_e then enters B(p_v, r_v), where the cone sectors live.
- **Short a_e.** Take a_e with \|γ(a_e) − p_v\| < r_v + ρ. Then D_e(a_e) partly lies in int B(p_v, r_v) and is **not** contained in ∂W_v.

The draft currently excludes these only implicitly. If V1(b) is read strongly ("the outside pieces meet ∂W_v exactly in λ_v"), then each fan minus its end segment is connected and misses ∂W_v, so it lies outside W_v. That reading works, but the proof cites the wrong items.

**Exact fix.** Add:
- **S1(f).** For v ∈ ∂e:
  - T_e ∩ W_v = D_e(a_e) (resp. D_e(b_e));
  - F_{f,e}, γ_e|[a_e, b_e] and Q_f meet W_v only in λ_v.
- **Metric sufficient condition** for the first clause: dist(p_v, D_e(t)) > r_v for t ∈ [a_e, b_e], and the stubs of the other edges at v miss T_e.

Then cite S1(f) in both injectivity paragraphs.

### 1.2 Stub hypotheses

W_v uses the disks D_e(t) for t ∈ [0, a_e], and λ_v uses "k-curves on tube side walls" there. But E1 (ρ < reach, dev* < ρ) and E2 (exactly one crossing) are stated only for t ∈ [a_e, b_e].

Without them:
- the stub disks can overlap outside the ball, so ∂W_v is not "end disk + side wall + sphere";
- β_{f,e}(t) for t < a_e can leave W_v, so Q_f gets a free boundary arc, which is a hole;
- P_f can cross a stub wall twice, so λ_v is not simple.

P0 and V1(b) *assume* these conclusions away. That contradicts the heading "all computable from the data".

**Exact fix.** Extend E1 and E2.1–E2.3 to t ∈ [t_v, a_e], where t_v is the parameter at which D_e(t) first leaves B(p_v, r_v). Then state P0 and V1(b) as consequences that can be checked. Otherwise, relabel them honestly as non-local topological hypotheses.

### 1.3 Other steps

These hold as stated:
- injectivity in T_e (via E1 and Federer's normal-disk property);
- injectivity of the cone given V1(a) and V1(b);
- injectivity outside the regions (S1(e) for open complements; on ∂T and ∂W, E3, S1(d) and V1(b) take over);
- the zones.

---

## 2. W_v and λ_v

### 2.1 What holds

**∂W_v.** With disjoint stub disks (§1.2) and D_e(a_e) ∩ B = ∅ (S1(f)), ∂W_v consists of three kinds of piece:
- the sphere outside the stubs;
- the stub side walls;
- the end disks D_e(a_e).

D_e(a_e) does lie in ∂W_v, because the disks for t > a_e belong to T_e, not W_v. It also lies in T_e, so the two regions are glued along it, which is what S1(f) formalises.

**Q_f near the end disk.** int(T ∪ W) contains the relative interior of D_e(a_e). So Q_f meets the end disk only at k_{f,e}(a_e), and f's trace on the end disk is exactly the fan segment.

**f's arc on λ_v.** It reads fan segment of e, then the trace of P_f on the stub wall of e, the sphere and the stub wall of e′, then fan segment of e′. That is consistent.

**Adjacent faces.** The fan segments of f and g meet only at γ_e(a_e), by E3 at t = a_e. Their traces on the walls and the sphere are disjoint only through V1(b) ("simple"). Overlapping patches can intersect each other inside T_e ∪ W_v, which is fine, but nothing except V1(b) keeps that intersection curve off ∂W_v.

### 2.2 The sufficient condition for V1(a) is wrong

**Correct condition.** At a stub wall point x = γ(t) + ρn, with n ⊥ γ′(t) and outward normal n, the ray exits transversally if and only if ⟨x − p_v, n⟩ > 0. This is equivalent to

**ρ_e > \|P_{γ′(t)⊥}(γ_e(t) − p_v)\| = \|γ_e(t) − p_v\| · sin ∠(γ′_e(t), γ_e(t) − p_v)**

for every t at which the wall is exposed (outside the ball).

**What the draft says instead.** "β_v < π/2 and ρ small relative to r_v cos β_v." This points the **wrong direction**: the correct condition needs β_v small relative to ρ / \|γ − p_v\|.

**Concrete failure.** See 6A.

**Consequences.**
- *Curved edge (chord L, curvature κ).* The condition becomes κL²/2 < ρ. Together with L > ρ / sin(θ/2), this needs ρ < 2 sin²(θ_v/2)/κ.
- *Vertex off the edge line.* The offset must be < ρ_e. Tolerant B-reps often have τ_v ≫ τ_e, with the vertex point off the edge by much more than τ_e. The construction then fails unless the apex is moved. Option (ii) of the fix makes the offset near 0; the remaining work is checking that the new edge curve passes V1(a).

**Exact fix.** Replace the clause with the displayed inequality on the exposed stub, plus ⟨γ_e(a_e) − p_v, γ′_e(a_e)⟩ > 0 (the end disk is then automatic). Two further fixes are possible:
- (i) take as apex any point q_v ∈ B(p_v, τ_v) that satisfies this inequality (h(v) = q_v is still in Z(v));
- (ii) first replace γ_e near v by the ASZ-style blend β(t) + (1 − t)(p_v − β(0)), so the edge ends at p_v.

---

## 3. Cell structure

**What is missing.** "Q_f is a disk, fans are strips glued along k, sectors are glued along arcs, so h(f) is a disk" leaves out three things:

- **(a) The order argument.** From P0 (∂Q_f is a single circle made of the k_{f,e} and of arcs on ∂W_v) and V1(b) (exactly one arc A_{f,v} per vertex, joining k_{f,e}(a_e) to k_{f,e′}(a_{e′})):
  - the arcs form a 2-regular graph isomorphic to ∂f;
  - the only cycle through all of them is ∂Q_f;
  - so the cyclic order is forced.
- **(b) The exact intersections:**
  - Q_f ∩ F_{f,e} = k_{f,e}, by E2.3 and S1(f);
  - (Q_f ∪ fans) ∩ sector_{f,v} = A_{f,v}, by star-shapedness and S1(f).

  Gluing two disks along a common boundary arc that is their whole intersection gives a disk.
- **(c) h as a map.** The construction defines only h(f) as a set. Define h|f by extending the homeomorphism h|∂f : ∂f → ∂h(f), using the Alexander trick (or Schoenflies in a chart).

For §5 you also need a parametrisation that is piecewise C¹: straighten the C¹ boundary of Q_f in the parameter domain of P_f.

**Verdict.** True under P0 and V1(b), and only a sketch as written. Add (a)–(c), roughly one paragraph.

---

## 4. PL step

**(a) Apex.** On a radial triangle (p_v, x_1, x_2) whose base arc of λ_v is curved, h(s, x) = p + s(x̃(x) − p) is homogeneous of degree 1. Its D²h grows like 1/\|y\|, so it is **not C² on the closed triangle**. The bound Lip(S − h) ≤ C·mesh·\|D²h\| does not apply there.

The conclusion still holds:
- S − h is degree-1 homogeneous on a full radial triangle;
- its radial derivative is O(mesh²·κ_λ) and its angular derivative is O(mesh·κ_λ);
- so Lip(S − h) = O(mesh) uniformly.

Equivalently, use graded levels with spacing proportional to s and the scaling argument.

*Fix:* replace "C² on every closed triangle" by this homogeneity estimate on the apex triangles.

Bi-Lipschitz at the apex holds:
- λ_v is transverse to the rays (V1(a));
- \|x − p_v\| is bounded below on λ_v.

So the radial projection of λ_v is bi-Lipschitz.

**(b) Regularity.** Π(t) depends on γ′, which is only C¹ when γ is C². Hence:
- k(t), the fan parametrisation and the stub walls are only **C¹**;
- the C² claim is false.

*Fix:* the secant estimate needs only C¹: Lip(S − h) ≤ C·ω(Dh, mesh)/sin θ_min → 0. State that, or assume γ ∈ C³.

**(c) Vertices of the piece decomposition.** At points where three or more pieces meet, such as k_{f,e}(a_e), γ_e(a_e), and the corners of ∂W_v, non-zero crease angles do **not** imply local bi-Lipschitz. Non-adjacent sectors of the tangent cone could overlap.

*Fix:* require that the tangent cone at such a point is an embedded PL disk, and prove it.
- **At k(a_e):** the fan and Q_f tangent sectors lie in the closed complement of the tangent cone of W_v, which is the quarter-space {⟨·, γ′⟩ ≤ 0, ⟨·, r̂⟩ ≤ 0}. The cone sectors lie inside it, and −(x − p_v) lies in its interior by the inequality of §2.2. The only shared rays are −r̂ and τ_sw, each between adjacent sectors.
- **At γ(a_e):** the fans lie in ⟨·, γ′⟩ ≥ 0 and the sectors in ⟨·, γ′⟩ ≤ 0. They share only the rays r̂_f ≠ r̂_g (E3).

**(d) Creases.** The fan/patch angle is > 90° and is verified: k′ ⊥ r̂ because ⟨k′ − γ′, k − γ⟩ = 0. The fan/fan angle (E3) and the cone/outside angle are fine.

**(e) Zones and injectivity.** S is injective once Lip(S − h) is below the bi-Lipschitz constant, using the intrinsic metric on \|K\|. It stays in the zones once \|S − h\| < m. Both are correct.

---

## 5. Re-derivation of E2 and E3

### E2.1 (convexity)

- **Meusnier.** In Π(t), the section's principal normal makes the angle φ with N, and cos φ = \|N − ⟨N, γ′⟩γ′\| = cos ψ. So k = κ_f / cos ψ is correct.
- **Convexity.** g = \|c − γ\|² gives g″ = 2(1 + ⟨c − γ, c″⟩) ≥ 2μ inside D. At the first time s* with g = ρ², g′(s*) ≥ (ρ² − dev*²)/s* > 0, so the exit is transversal.
- **Section length.** g ≥ −2dev*·s + μs² gives s* ≤ ℓ = (dev* + √(dev*² + μρ²))/μ, which is correct.

### dev*

b(t) ∈ D(t) and ρ < reach, so γ(t) is the nearest point (Federer 4.8(12)). Hence \|b(t) − γ(t)\| = dist(b, γ) ≤ \|β(t′) − γ(t′)\| ≤ dev.

So **dev* ≤ dev exactly.** Replace "= dev + O(κ dev²)".

### E2.2 (monotone projection)

σ′ = ⟨β′, γ′(σ)⟩ / (1 − ⟨β − γ(σ), γ″(σ)⟩). The numerator is ≥ cos(κ\|t − σ\|) − L, and the denominator is ≥ 1 − κ·dev*.

So L + κ·dev* < 1 is sufficient (it dominates the κ²dev² term). Correct.

### E2.3 (overshoot of C_f)

C_f uses arcs of length ℓ, which extend **past** their own exit points. Points of P_f on the overshoot of a section at t′ could in principle lie in D(t), and then the condition no longer forces P_f ∩ D(t) to be a single arc.

*Fix:* define C_f = ⋃_t c_t([0, s*(t)]) (truncated at the exit), and state no-return as P_f ∩ T_e = C_f. A computable sufficient version is dist(γ(t), P_f ∖ C_f^ℓ) > ρ together with (ρ + ℓ + dev*)·κ_γ < 1. That makes the squared distance from overshoot points convex along γ, so the critical point is unique.

### E3 (exit-angle bound)

Perpendicular offset ≤ dev* + ks²/2, so sin(angle) ≤ q/ρ. My one worry was the case where the exit lies behind b, which would make the angle obtuse.

**Numerical test** (`r01/e3_eps2.py`):
- 20,000 random sections with constant or bang-bang curvature \|κ\| ≤ k, kρ < 0.95, dev* < 0.95ρ;
- no violation of angle ≤ ε, and none with q < 1.

The formula is correct.

**Leading order.** min over ρ of (dev*/ρ + kρ/2) is attained at ρ = √(2dev*/k) and gives α > 2√(2k·dev*). Correct, with "< τ_e" strict.

**Necessity.** Two lines at distance d from γ, crossing at angle α, have their farthest intersection at distance d / sin(α/2). So τ_e > dev*/sin(α/2) is necessary in the worst case. Correct.

---

## 6. Counterexamples

### 6A. Stated sufficient condition for V1(a) holds, but the cone overlaps (`r01/v1a_offset.py`)

**Setup.**
- p_v = 0, τ_v = 10, r_v = 6.
- Edge γ(x) = (x, 2, 0) for x ∈ [4, 9], with a_e at x = 9. So γ(0) = (4, 2, 0) is in int B(0, 6), and V0 holds.
- τ_e = 1, ρ = 0.5, dev = 0.1.
- Face f lies in the plane z = 0, on the side y ≤ 2 − dev (towards p_v).

**Checks against the hypotheses.**
- β_v = max ∠ = 26.6° < 90°.
- ρ = 0.5 ≪ r_v cos β_v = 5.37.
- \|γ(a_e)\| + ρ = 9.72 < τ_v.

**Failure.** The ray from p_v through x = (8, 1.5, 0), a point on the near stub wall and on f's trace, crosses ∂W_v at s = 0.737, 1.0 and 1.125:
- it leaves the ball at (5.90, 1.11, 0), which is also on f's trace on λ_v;
- it re-enters through the wall at x.

So two points of λ_v lie on one ray, and the cone sector of f folds over itself: h is not injective.

The violated true condition is offset 2 > ρ = 0.5. Fix: §2.2.

### 6B. Hypotheses stated only on [a_e, b_e]

A fillet face whose curvature satisfies ρk ≥ 1 only on the stub part [t_v, a_e] passes E1–E3 as stated. It then crosses the stub wall twice, and the cone gets an extra arc. This is excluded only by assuming V1(b) and P0 (§1.2).

### 6C. No counterexample under the full hypotheses

With V1(a), V1(b) and P0 taken as hypotheses (strong reading), I could not break the construction. It is sound modulo §1.1, §3 and §4.

---

## Required edits (drop-in)

1. Add **S1(f)**: T_e ∩ W_v = D_e(a_e), and the outside pieces meet W_v only in λ_v. Cite it in §4.
2. Extend E1 and E2 to the exposed stub [t_v, a_e]. Then turn P0 and V1(b) into consequences, or label them as non-local hypotheses.
3. Replace the sufficient clause of V1(a) with ρ_e > \|P_⊥(γ_e(t) − p_v)\| on the exposed stub, or move the apex / blend the edge into p_v.
4. In §4, add the cell-structure argument and the definition of h as a map (§3 (a)–(c)).
5. In §5:
   - apex: homogeneity estimate;
   - regularity: C¹ plus modulus of continuity;
   - tangent-cone embedding at the vertices of the piece decomposition.
6. Change "dev* = dev + O(…)" to dev* ≤ dev. Truncate C_f at the exit.
