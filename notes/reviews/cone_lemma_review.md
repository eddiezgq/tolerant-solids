# Review of cone_lemma.md and its implementation (wfs_cert2.py / wfs_cert.py)

Reviewer verdict summary

| Item | Verdict |
|---|---|
| 1. Lemma A | **Correct** (two minor wording points) |
| 2. Corollary B, λ(M) > 0 | **Correct with fix** (finiteness of g is justified wrongly; conclusion holds) |
| 3. Claim C | **Correct with fix**: true for conforming, non-folded planar-face triangulations and exact incidence; false for folded triangulations (counterexample below); only valid up to `tol` |
| 4. Code soundness | **Correct with fix**: ordering, search, radii, LP and return value are sound; two small holes (degenerate triangles skipped in `relevant_points`; numeric "contains a") |
| 5. Literature | Qualitative wfs > 0 for semialgebraic sets (so polyhedra) is known (Fu 1985). The quantitative conical-radius bound was not found in a brief search; the key identity is the standard orthogonality of projection onto a cone. Do not claim novelty of the identity. |

Test scripts: `audit/t_cone.py` (empirical check + fold counterexample), `audit/t_degen.py`.

---

## 1. Lemma A — correct

Line by line:

- Step 1: d(p) ≤ |p−a| < r/2 and |x−a| ≤ |x−p| + |p−a| < r. Correct. Γ(p) ≠ ∅ because M is compact (closed suffices).
- Step 2: x ∈ M ∩ B(a,r) = C ∩ B(a,r), so x ∈ C, so y_s = a + s(x−a) ∈ C for all s ≥ 0. For s ∈ (0, r/|x−a|) — an open interval containing 1 because |x−a| < r — y_s ∈ C ∩ B(a,r) ⊂ M. Hence f(s) = |p−y_s|² ≥ d(p)² = f(1) on an open interval around 1; f is a smooth quadratic, so f′(1) = −2⟨p−x, x−a⟩ = 0. If x = a the identity is trivial. Correct.
- Step 3: ⟨p−x, p−a⟩ = |p−x|² + ⟨p−x, x−a⟩ = d(p)² > 0, so u = p−a separates 0 from conv{(p−x)/d}. Correct.

Remarks (not errors):
- The hypothesis "r < ρ(a)" is used only to get *some* admissible radius r′ ≥ r (the admissible set is downward closed: if M∩B(a,r′) = C∩B(a,r′) then the same C works for every smaller radius). State this one line explicitly. Using r ≤ ρ(a) when the sup is attained also works.
- Closedness of C is never used. Say "B(a,r) is the open ball".
- The identity ⟨p − π(p), π(p) − a⟩ = 0 for nearest points on a cone with apex a is the classical fact for projections onto cones (Moreau-type orthogonality; the proof above does not need convexity). Cite it as standard rather than new.

Empirical check (t_cone.py): on the L-shape and slot_g0.2 meshes, for ~12 000 random p in boxes that `clear_ball` certified with candidate a, max |cos∠(p−x, x−a)| = 2e-11. Consistent with the lemma.

## 2. Corollary B and λ(M) > 0 — correct with fix

- Proof of Corollary B: correct. If 0 < d(p) < λ ≤ g(x), the sup gives a with ρ(a)/2 − |x−a| > d(p), then |p−a| ≤ d(p) + |x−a| < ρ(a)/2; choose r with 2|p−a| < r < ρ(a). Fine. (If ρ(a) = ∞ the choice of r is still possible; see next bullet for why it is finite anyway.)
- **"g is finite: ρ is bounded when M is compact and not a cone" — wrong reason, right conclusion.** A compact set is never a cone unless it is a point, and "not a cone" is not what bounds ρ. Correct argument: if M ≠ {a} and M∩B(a,r) = C∩B(a,r) with r > R_a := max_{y∈M}|y−a|, pick y ∈ M, y ≠ a; then the ray through y lies in C, so a + t(y−a)/|y−a| ∈ M for t < r, i.e. M has a point at distance > R_a from a — contradiction. Hence ρ(a) ≤ R_a ≤ diam M, and g ≤ diam M/2. **Fix:** replace the parenthesis by this argument and assume M has at least two points.
- g is a sup of 1-Lipschitz functions and finite, hence 1-Lipschitz (thus continuous). Correct.
- g(x) ≥ ρ(x)/2 > 0. Correct.
- ρ(x) > 0 for every x in a finite union of closed triangles: correct; give the one-line proof: let r be smaller than the distance from x to every triangle, edge and vertex that does not contain x (finitely many closed sets, all at positive distance). Each triangle T ∋ x is convex, and T∩B(x,r) = (x + tangent cone of T at x) ∩ B(x,r); a union of cones with apex x is a cone. No manifold or closed-surface hypothesis is needed; self-intersections are fine.
- Continuous positive g on compact M has positive minimum. Correct.

Note: λ(M) is about the *mesh* M, not the CAD solid. On curved faces each triangle is its own region, so λ(M) is of the order of half the local triangle size; the cone test alone gives a small number there and must be combined with the LP test (as the code does).

## 3. Claim C — correct with fix

### Why it is right under the right hypotheses
Let D = plane(R) ∩ B(a,r), a disk centred at a (a ∈ R). Suppose (H) the "boundary segments" of R cover the relative boundary ∂R of R in its plane. If every segment meeting B(a,r) contains a and no segment endpoint other than a lies in B(a,r), then each such segment meets B(a,r) in a full chord through a (a interior to the segment) or in a radius (a an endpoint). The rays cut D into open sectors; each sector is connected and misses ∂R, so it is entirely in R or entirely outside. Hence R ∩ D is a union of closed sectors and rays at a — a cone ∩ B. **Non-convexity, reflex corners at a, and holes cause no problem**: a reflex corner just gives a sector of angle > π, and hole edges are boundary segments like any other. Several regions in different planes: each R∩B(a,r) = C_R ∩ B(a,r), so M∩B(a,r) = (∪C_R) ∩ B(a,r), and a union of cones with common apex is a cone. Correct.

Also needed and implicit: **a ∈ M**. `clear_ball` returns True vacuously if no feature is within r, so for a ∉ M it would "certify" anything. All candidates in `cone_certified` (x0, segment endpoints, closest points on segments) are on M, so the code is fine; state "a ∈ M" in Claim C.

### Where hypothesis (H) fails: edges used once ≠ boundary for folded triangulations
`mesh_features` counts *undirected* edge uses. An edge used twice by two triangles lying on the *same* side of it is on ∂R but is dropped.

Counterexample (run in t_cone.py with the exact segment rule and `Features.clear_ball`): plane z = 0, A=(0,0), B=(10,0), C=(5,10), D=(5,5); triangles (A,B,C) and (A,B,D), both counter-clockwise, D inside the first. Edge AB is used twice, so the segments are BC, CA, BD, DA; AB is missing. For a = (5, 0.05, 0): `clear_ball(a, 1.0)` returns **True**, but M∩B(a,1) is the half-disk y ≥ 0 whose edge y = 0 does not pass through a — not a cone. Lemma A's identity then fails, e.g. p = (5, −0.2, 0.1): x = (5,0,0), ⟨p−x, x−a⟩ = 0.01 ≠ 0. (Here no critical point appears because the half-disk is convex, so this shows the proof does not cover such input, not a wrong final number.) BRepMesh normally gives conforming, non-folded planar-face triangulations, so the current test cases are probably unaffected; but the code does not check it, and the `planar` test accepts antiparallel normals (`cross(n, n0)` is 0 for n = −n0), so a flipped triangle passes.

T-junctions and duplicated nodes only *add* once-used edges (extra features) — conservative, harmless.

**Exact fix (makes "segments ⊇ ∂R" provable):**
1. In the planar branch require consistent orientation: `(n @ n[0]).min() > 1 - 1e-9` (not `|n × n0|` small). Otherwise treat the face as non-planar (each triangle its own region — always sound).
2. Count **directed** edges. An undirected edge is interior only if it is used exactly once in each direction (a→b and b→a); every other edge is a boundary segment. With consistent orientation, an edge used once in each direction has one triangle on each side, so its relative interior is interior to R; an interior vertex not on any segment then has a closed fan around it. Every other boundary point lies on a listed segment.

### Tolerance (concern 4)
"Contains a" is `dist ≤ tol` with tol = 1e-10·(max|coord|+1). Also `verts` are rounded to 12 decimals, so a vertex candidate a can be ~5e-13 off M. If some feature not containing a is within tol of a (near-touching faces, a slightly non-planar "planar" face accepted by the 1e-9 test), M∩B(a,r) is a cone only up to a perturbation of size tol, and critical points with values of order tol / sin(smallest angle in the configuration) can be certified away. So the certified statement is "no critical value in (c·tol, LB)", not "(0, LB)".
**Fix:** decide "contains a" combinatorially, not numerically. Each candidate carries its cell: a mesh vertex id (x0 from the vertex branch of `closest_on_tris`, or a segment endpoint), an edge id (x0 from an edge branch, or a closest point on a segment), or a triangle id. A feature contains a iff it is incident to that cell (after welding duplicated node coordinates across faces by exact equality). Every non-incident feature, however close, then counts against the ball. Use the unrounded vertex coordinates for candidates. If this is not done, state the (c·tol, LB) caveat in the result.

## 4. Code soundness — correct with fix

Checked and sound:
- **Key monotonicity.** Child centre c2 has |c2 − c| = h√3/2 = hd/2, so d(c2) ≥ d(c) − hd/2 and d(c2) − hd/2 ≥ d(c) − hd. With max(·,0) the child key ≥ parent key. Every p in a box has d(p) ≥ d(c) − hd, so key ≤ inf_box d. Hence popped keys are non-decreasing, and when a box with key k is popped, every point with d < k lies in boxes already certified or cut off. The returned value on "first uncertified leaf" equals the popped key (dc = D.d(cen) is the same function used for the push). `max_boxes` return of `key` is also valid. Empty heap → no critical value in (0, R).
- **Root box** covers bbox(M) + R, which contains {d < R}. Correct.
- **Cut-off** d − hd ≥ R ⇒ every point of the box has d ≥ R. Correct.
- **Dist.d expanding search**: any triangle with distance < m has centroid within m + rmax ≤ r, so it was queried. Correct.
- **candidates(p, bound)**: centroid within bound + rmax, filtered by true distance ≤ bound. Correct.
- **LP test radius**: nearest point x of p in the box satisfies |x − c| ≤ d(p) + hd ≤ d(c) + 2hd. Candidate triangles and the octagon clip (inradius r′, so it contains the disk) are correct; u·(p − x) is bilinear, so checking corners × clipped-polygon vertices is exact for the convex pieces. Correct.
- **clear_ball query radii**: triangles r + rmax (centroid), segments r + shalf (midpoint), vertices r. All supersets of "within r". Region "contains a" via min over queried triangles is right because a triangle containing a is always queried. The ×(1+1e-9) margin on r absorbs rounding in the `< r` comparisons.
- **Box rule**: need = 2(|c−a| + hd), r = need(1+1e-9), so |p − a| ≤ need/2 < r/2 ≤ ρ(a)/2. Correct.
- **Leaf rule** only stops refinement; it cannot certify. Correct.

Holes to fix:
1. `relevant_points` (wfs_cert.py line 175) **skips triangles with zero area** (`nn == 0`). A degenerate triangle is still a segment of M and may hold nearest points; skipping it can make the LP certify a box wrongly. Fix: for `nn == 0`, append its three vertices (their convex hull contains the segment, so this is conservative). `closest_on_tris` handles collinear triangles correctly in my tests (t_degen.py), so `Dist` is fine.
2. Numeric containment / vertex rounding — see Section 3, Tolerance.
3. Folded planar triangulation — see Section 3 (fix in `mesh_features`).

Not soundness bugs: segment endpoints along straight face edges subdivided by mesh nodes count as vertices, which caps ρ estimates at about half the edge-node spacing near such edges (only costs boxes). Double precision without interval arithmetic remains the stated caveat.

## 5. Literature (only sources actually opened)

- di Rocco, Eklund, Gäfvert, *Computing geometric feature sizes for algebraic manifolds*, arXiv:2209.01654. Theorem 2.5: "If X is semialgebraic, then d_X(B) is finite, and so wfs(X) > 0," citing J. H. G. Fu, *Tubular neighborhoods in Euclidean spaces*, Duke Math. J. 52(4):1025–1046, 1985. It uses the same Chazal–Lieutier critical-point definition. A finite union of triangles is semialgebraic, so **wfs(M) > 0 is known**; Corollary B's contribution is an explicit, computable lower bound (λ(M)), not positivity.
- I did not find, in a brief search, a published statement of Lemma A in terms of a "conical radius" or of λ(M). Its core step is the standard orthogonality of nearest points on a cone. Say "we did not find this explicit bound in the literature", not "new".

---

## Follow-up: relevant_points_proj

Reviewed the current `wfs_cert2.py` (mesh_features with union-find, `relevant_points_proj`, `certify` with rel = 0.05). Test: `audit/t_proj.py` (re-solves the same LP to get u, then samples p in each LP-certified box, computes all true nearest points x and checks u·(p−x) > 0).

| Item | Verdict |
|---|---|
| 1. Cases (a), (b), (c) | **Correct** (neighbours and curvature do not matter) |
| 2. Degenerate triangles | **Correct in relevant_points_proj**; **correct with fix** in mesh_features (dropped triangles leave T) |
| 3. Candidate triangles | **Correct** |
| 4. Other paths | **Correct with fix**: curved-face union-find can merge a non-planar region (drift); otherwise sound |

### 1. Cases (a)–(c) — correct
- (a) If x is in the relative interior of T ⊂ M and x is a nearest point of p on M, then x minimises |p − y| over y ∈ T near x, so p − x ⊥ plane(T) and x = proj_plane(T)(p). The argument is local: it uses only T ⊂ M and x ∈ relint T. Whether the neighbours are coplanar, or the face is curved, makes no difference. Orthogonal projection is 1-Lipschitz, so |x − q| ≤ |p − c| ≤ hd with q = proj(c). Also |x − c| ≤ d(p) + |p − c| ≤ d(c) + 2hd = ρ. The plane points satisfying both bounds form the disk (q, min(hd, √(ρ² − δ²))). The 8 half-planes w·y ≤ w·q + r circumscribe it, so the clipped triangle is a convex superset of T ∩ disk. Correct.
- (b) The same argument on the segment e ⊂ M: x ∈ relint e ⇒ p − x ⊥ e ⇒ x = proj_line(p), within hd of foot(c) and within ρ of c. The parameter interval [t0 − r, t0 + r] ∩ [0,1] with r = min(hd, √(ρ² − dl²))/|e| is exactly that set (closed). Correct.
- (c) Vertices with |v − c| ≤ ρ. Correct.
- Every point of a closed triangle lies in its relative interior, in the relative interior of an edge, or at a vertex, so the three cases are exhaustive. Each kept piece is the convex hull of the kept points, and u·(p − x) is bilinear, so testing corners × kept points is exact. Correct.
- Empirical check (t_proj.py): see the results line at the end of this section.

### 2. Degenerate triangles
- In `relevant_points_proj`: for a zero-area triangle the point set is a segment covered by its longest edge. Every point is a vertex or in the relative interior of one of the edges, and these are handled by (b)/(c) before the `nn == 0` skip; `L2 == 0` edges are points and are covered by (c). Correct.
- Numerical caveat (slivers, nn tiny but > 0): n = cross/|cross| can have a large relative error, so q and the clip polygon may be slightly off, and this can exclude true nearest points. **Fix:** if nn < 1e-8·|b−a|·|c−a| (or similar), skip the projection clip and append the whole triangle (its 3 vertices); that is always sound because the triangle is convex.
- In `mesh_features`: triangles with |n| ≤ 1e-14·L² are removed from **T itself** (`F = F[good]` before `tris.append`). So `Dist`, `candidates`, the LP and `clear_ball` all work on M′ = M minus those triangles. Their edges are kept as segments. That is harmless only if each such edge lies on kept triangles (true on a closed manifold BRepMesh, as the comment says). If not, two problems follow: (i) the certificate is for M′, not M; (ii) a cone candidate a taken from such a dangling segment is **not on M′**. Then `clear_ball` can return True vacuously when no region lies within r, which certifies a box Lemma A does not cover. **Fix:** either keep zero-area triangles in T (only drop them from regions), or assert at build time that every dropped edge's endpoints and the segment itself lie on some kept triangle (distance ≤ tol), and abort otherwise.

### 3. Candidate triangles — correct
A nearest point x of any p in the box satisfies |x − c| ≤ d(p) + |p − c| ≤ d(c) + 2|p − c| ≤ d(c) + 2hd. The triangle holding x therefore has dist(c, T) ≤ d(c) + 2hd, and `candidates` returns exactly the triangles with dist ≤ bound (its centroid query uses bound + rmax). Correct. Equality is reached only in the limit (a box corner), so the `<=` comparisons have no slack against rounding. Optional hardening: pass ρ·(1 + 1e-12) to both `candidates` and `relevant_points_proj`.

### 4. Other paths
- **Curved-face union-find can merge a non-planar region (proof gap).** The merge test is *pairwise*: n_k·n_j > 1 − 1e-12 (dihedral angle < 1.4e-6 rad) and the neighbour's vertices within 1e-9·L of the plane of k. Union-find is transitive, so a chain of individually "coplanar" pairs can drift. Example: a gently curved B-spline or toroidal face with radius R_c ≈ 1e4, mesh size s = 0.01, L ≈ 10. Each pair has angle s/R_c = 1e-6 and offset ≈ s²/R_c = 1e-8 < 1e-9·L ≈ 1.1e-8, so they are all merged. A merged region of diameter 10 then sags about D²/(8R_c) ≈ 1e-3, far above tol. Claim C (planar sector argument) does not apply to such a region, so `clear_ball` can report ρ(a) ≥ r where M∩B(a,r) is not a cone. In practice, a boundary-free, nearly flat PL sheet has no critical points next to it: all nearest-point vectors from one side point into a narrow cone around its normal. So I do not expect a wrong number. But the proof as written does not cover it. The planar branch does not have this problem because it compares every triangle with one reference n[0] and one point F[0,0].
  **Fix:** after union-find, re-check each component globally, as the planar branch does: all normals against the component's first normal (n·n0 > 1 − 1e-12) and all its vertices within 1e-9·L of that plane. If a component fails, split it back into single triangles (always sound).
- The directed-edge boundary rules (planar and curved) are right for consistently oriented triangles. Duplicate directed edges (non-manifold input) only overwrite `owner`/`de` entries, and I found no case where this hides a true boundary edge. BRepMesh output is manifold per face anyway.
- `certify`: unchanged logic. Key monotonicity, the cut-off, the leaf rule (rel = 0.05 only changes when refinement stops, not soundness) and the return values are still sound. The `dc > hd` guard before the LP is fine (the LP cannot succeed on boxes meeting M).
- Remaining global caveats, unchanged: numeric containment with tol (Section 3 of the main review), double precision, no interval arithmetic.

**Empirical results (t_proj.py)**, 20 sampled p per LP-certified box, all true nearest points checked against the LP's u:
- slot_g0.2: 3332 boxes, 0 violations, min u·(p−x)/d = 0.79
- cylinder: 3336 boxes, 0 violations, min 0.37
- Lfillet_r0.05: 3338 boxes, 0 violations, min 0.13
