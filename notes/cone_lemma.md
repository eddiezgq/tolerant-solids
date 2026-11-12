# Cone lemma (near-surface band) — claim to audit

## Setting
- M ⊂ R³ is a compact set; in our use, M is a closed PL surface, a finite union of triangles.
- d(p) = dist(p, M), and Γ(p) is the set of nearest points of p.
- p ∉ M is **critical** iff 0 ∈ conv{(p − x)/d(p) : x ∈ Γ(p)}. This is the Grove–Shiohama / Lieutier notion used for wfs.
- wfs(M) is the infimum of the positive critical values.

## Definition (conical radius)
For a ∈ M, ρ(a) is the supremum of r > 0 such that M ∩ B(a, r) = C ∩ B(a, r) for some closed cone C with apex a. A cone with apex a is a set C with a + s(y − a) ∈ C for all y ∈ C and s ≥ 0.

## Lemma A
Let a ∈ M, r < ρ(a), and let p satisfy |p − a| < r/2 and p ∉ M. Then p is not critical.

**Proof.**
1. **Nearest points lie in the ball.** Because a ∈ M, d(p) ≤ |p − a| < r/2. For x ∈ Γ(p), |x − a| ≤ |x − p| + |p − a| < r. So Γ(p) ⊂ M ∩ B(a, r) = C ∩ B(a, r).
2. **The ray argument.**
   - Fix x ∈ Γ(p). For s near 1, y_s = a + s(x − a) lies in C. Its distance to a is s|x − a|, which is < r for s near 1, so y_s ∈ B(a, r) and hence y_s ∈ M.
   - Therefore f(s) = |p − y_s|² has a local minimum at s = 1 among s near 1 (an interior point if x ≠ a; if x = a the next identity is trivial).
   - So f′(1) = 0, which gives ⟨p − x, x − a⟩ = 0.
3. **Conclusion.** ⟨p − x, p − a⟩ = |p − x|² + ⟨p − x, x − a⟩ = d(p)² > 0 for every x ∈ Γ(p). With u = p − a, u·v > 0 for every v in the set {(p − x)/d}, so 0 is not in its convex hull. ∎

## Corollary B
Let λ(M) = inf_{x ∈ M} sup_{a ∈ M} (ρ(a)/2 − |x − a|). Then d has no critical point p with 0 < d(p) < λ(M), so wfs(M) ≥ λ(M).

**Proof.** Take p with d(p) < λ and x ∈ Γ(p). Choose a with ρ(a)/2 − |x − a| > d(p). Then |p − a| ≤ d(p) + |x − a| < ρ(a)/2, and Lemma A applies (pick r slightly below ρ(a)). ∎

**Claim: λ(M) > 0 for a finite union of triangles.**
- ρ(a) > 0 for every a ∈ M, because M is locally conical at every point of a polyhedron.
- g(x) = sup_a (ρ(a)/2 − |x − a|) is a supremum of 1-Lipschitz functions, hence 1-Lipschitz (it is finite: ρ is bounded when M is compact and not a cone).
- g(x) ≥ ρ(x)/2 > 0 (take a = x).
- M is compact, so min g > 0.

## How the code computes a lower bound for ρ(a)
- **Features.** M is split into features:
  - regions: a planar B-rep face as one region (all its triangles), or each triangle of a curved face as its own region;
  - segments: the boundary edges of the regions;
  - vertices: the endpoints of those segments.
- **Claim C.** If no feature f with a ∉ f (tested as dist(a, f) > tol) lies within distance r of a, then M ∩ B(a, r) is a cone with apex a inside B(a, r), so ρ(a) ≥ r.
- **Argument.**
  - Every region meeting B(a, r) contains a. Otherwise the region, at distance < r, is a feature not containing a.
  - A region R is a closed convex-or-not planar polygon containing a. For R ∩ B(a, r) to be conical at a, it suffices that every boundary segment meeting B(a, r) contains a, and that no vertex other than a lies in B(a, r).
    - Then ∂R ∩ B consists of segments through a, so R ∩ B is a union of closed sectors at a.
  - A union of such conical pieces is conical.
- **Box test.** A box with centre c and half-diagonal hd is certified if some candidate a has no such feature within 2(|c − a| + hd). Every p in the box then has |p − a| ≤ |c − a| + hd < r/2.

## Concerns to check
1. **Lemma A, f′(1) = 0.** Is s = 1 an interior minimum? This needs y_s ∈ M for s on both sides of 1, which needs |x − a| < r. That holds by step 1.
2. **Claim C, non-convex planar regions.** Is the sector argument right when R is not convex? What if a lies on ∂R at a reflex corner?
3. **Claim C, multiple regions.** Several regions meet at a with different planes. Is the union a cone? (Each piece is a cone, so the union is too.)
4. **Tolerance.** "Contains a" is decided numerically with tol = 1e-10·L.
5. **Literature.** Is Lemma A or Corollary B known? Look for distance functions of polyhedra or conical sets, and "critical points of distance function near a stratified/conical set". Do not claim novelty.

## Revisions after review (11-11, see cone_lemma_review.md)
- **Lemma A.** Use the open ball B(a, r); any r < ρ(a) works. The verdict was "correct".
- **Corollary B.** g is finite because ρ(a) ≤ diam M whenever M has more than one point. This replaces the earlier reason.
- **Claim C.** Holds when the boundary segments cover ∂R.
  - The code now accepts a planar region only if its triangle normals are parallel and consistently oriented.
  - Boundary = the directed edges whose reverse does not occur.
  - Counterexample to the old undirected count: folded triangles (A,B,C), (A,B,D).
- **Zero-area triangles.** The filleted box mesh has some. On a closed manifold mesh, a zero-area triangle's points lie on edges of its neighbours.
  - Such triangles are now dropped from the regions, but their edges are kept as segments.
  - relevant_points keeps the vertices of a degenerate triangle.
- **Tolerance.** "Contains a" is decided by tol = 1e-10·L. Strictly, the statement is "no critical value in (c·tol, LB)".
  - This is part of the double-precision caveat.
  - The exact fix is to decide containment from mesh incidence instead.
- **Literature.**
  - wfs > 0 for semialgebraic sets, including polyhedra: Fu, Duke Math. J. 52 (1985), as cited in di Rocco–Eklund–Gäfvert, arXiv:2209.01654, Thm 2.5. Fu's original was NOT opened.
  - The explicit conical-radius bound λ(M): not found in the literature, which is not the same as new.
