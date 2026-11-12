import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Convex.Hull

/-!
# 锥面引理（第 1 阶段，引理 1 的近曲面部分）

设 `M` 是实内积空间中的集合，`a ∈ M`。若 `M` 在 `a` 的半径 `r` 球内是以 `a` 为顶点的锥
（`LocallyConicalAt M a r`），且 `‖p - a‖ < r / 2`，则 `p` 的每个最近点 `x` 都满足
`⟪p - x, p - a⟫ = ‖p - x‖²`；于是 `p ∉ M` 时 `p` 不是距离函数的临界点。

这里“临界点”取 Grove–Shiohama / Lieutier 的定义：`0` 属于 `{p - x : x 是 p 的最近点}` 的凸包
（是否单位化不影响 `0` 是否在凸包里）。
-/

open RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- `x` 是 `p` 在 `M` 上的一个最近点。 -/
def IsNearest (M : Set E) (p x : E) : Prop := x ∈ M ∧ ∀ y ∈ M, ‖p - x‖ ≤ ‖p - y‖

/-- `p` 是到 `M` 的距离函数的临界点。 -/
def IsCritical (M : Set E) (p : E) : Prop :=
  (0 : E) ∈ convexHull ℝ {v | ∃ x, IsNearest M p x ∧ v = p - x}

/-- `M` 在 `a` 的 `r` 球内是以 `a` 为顶点的锥：球内的点沿着过 `a` 的射线伸缩、只要仍在球内，就仍在 `M` 里。 -/
def LocallyConicalAt (M : Set E) (a : E) (r : ℝ) : Prop :=
  ∀ y ∈ M, ‖y - a‖ < r → ∀ s : ℝ, 0 ≤ s → ‖s • (y - a)‖ < r → a + s • (y - a) ∈ M

/-- 关键恒等式：最近点 `x` 处，`p - x` 与射线方向 `x - a` 正交。 -/
theorem inner_eq_zero_of_conical {M : Set E} {a p x : E} {r : ℝ}
    (hcone : LocallyConicalAt M a r) (ha : a ∈ M) (hpa : ‖p - a‖ < r / 2)
    (hx : IsNearest M p x) : ⟪p - x, x - a⟫ = 0 := by
  obtain ⟨hxM, hmin⟩ := hx
  set w := p - x with hw
  set d := x - a with hd
  -- ‖d‖ < r
  have hpx : ‖w‖ ≤ ‖p - a‖ := hmin a ha
  have hdr : ‖d‖ < r := by
    have : d = (p - a) - w := by simp [hw, hd]
    calc ‖d‖ = ‖(p - a) - w‖ := by rw [this]
      _ ≤ ‖p - a‖ + ‖w‖ := norm_sub_le _ _
      _ < r := by linarith
  by_contra hc
  set c := ⟪w, d⟫ with hcdef
  have hd0 : d ≠ 0 := by
    intro h; apply hc; rw [hcdef, h, inner_zero_right]
  have hdpos : 0 < ‖d‖ := norm_pos_iff.mpr hd0
  -- 对 |t| 足够小，点 a + (1 + t)•d 在 M 里，于是 ‖w - t•d‖ ≥ ‖w‖
  have key : ∀ t : ℝ, |t| * ‖d‖ < r - ‖d‖ → |t| ≤ 1 → ‖w‖ ^ 2 ≤ ‖w - t • d‖ ^ 2 := by
    intro t ht ht1
    have hs : (0 : ℝ) ≤ 1 + t := by
      have := neg_abs_le t; linarith
    have hball : ‖(1 + t) • d‖ < r := by
      rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg hs]
      have : (1 + t) * ‖d‖ ≤ ‖d‖ + |t| * ‖d‖ := by
        have := le_abs_self t; nlinarith [hdpos]
      linarith
    have hmem := hcone x hxM hdr (1 + t) hs hball
    have h1 : p - (a + (1 + t) • d) = w - t • d := by
      simp only [hw, hd, add_smul, one_smul]; abel
    have := hmin _ hmem
    rw [h1] at this
    exact pow_le_pow_left₀ (norm_nonneg _) this 2
  -- 展开：‖w - t d‖² = ‖w‖² - 2 t c + t² ‖d‖²
  have expand : ∀ t : ℝ, ‖w - t • d‖ ^ 2 = ‖w‖ ^ 2 - 2 * t * c + t ^ 2 * ‖d‖ ^ 2 := by
    intro t
    rw [norm_sub_sq_real, real_inner_smul_right, norm_smul, Real.norm_eq_abs, mul_pow, sq_abs]
    ring
  -- 取 t = ε c，ε > 0 足够小，得到 -2 ε c² + ε² c² ‖d‖² ≥ 0，矛盾
  have hc2 : 0 < c ^ 2 := by positivity
  set K := (|c| + 1) * (‖d‖ + 1) with hK
  have hKpos : 0 < K := by positivity
  have hgap : 0 < r - ‖d‖ := by linarith
  set ε := min (1 / (‖d‖ ^ 2 + 1)) (min (1 / K) ((r - ‖d‖) / K)) / 2 with hε
  have hεpos : 0 < ε := by positivity
  have hε1 : ε * ‖d‖ ^ 2 < 1 := by
    have : ε ≤ 1 / (‖d‖ ^ 2 + 1) / 2 := by
      have := min_le_left (1 / (‖d‖ ^ 2 + 1)) (min (1 / K) ((r - ‖d‖) / K)); linarith
    have h2 : 1 / (‖d‖ ^ 2 + 1) / 2 * ‖d‖ ^ 2 < 1 := by
      rw [div_div, div_mul_eq_mul_div, one_mul, div_lt_one (by positivity)]; nlinarith
    calc ε * ‖d‖ ^ 2 ≤ 1 / (‖d‖ ^ 2 + 1) / 2 * ‖d‖ ^ 2 := by gcongr
      _ < 1 := h2
  have hεK : ε * K < r - ‖d‖ ∧ ε * K ≤ 1 := by
    have hm : ε ≤ min (1 / K) ((r - ‖d‖) / K) / 2 := by
      have := min_le_right (1 / (‖d‖ ^ 2 + 1)) (min (1 / K) ((r - ‖d‖) / K)); linarith
    constructor
    · have : ε ≤ (r - ‖d‖) / K / 2 := by
        have := min_le_right (1 / K) ((r - ‖d‖) / K); linarith
      calc ε * K ≤ (r - ‖d‖) / K / 2 * K := by gcongr
        _ = (r - ‖d‖) / 2 := by field_simp
        _ < r - ‖d‖ := by linarith
    · have : ε ≤ 1 / K / 2 := by
        have := min_le_left (1 / K) ((r - ‖d‖) / K); linarith
      calc ε * K ≤ 1 / K / 2 * K := by gcongr
        _ = 1 / 2 := by field_simp
        _ ≤ 1 := by norm_num
  have habs : |ε * c| * ‖d‖ ≤ ε * K ∧ |ε * c| ≤ ε * K := by
    rw [abs_mul, abs_of_pos hεpos]
    constructor
    · have : |c| * ‖d‖ ≤ K := by
        rw [hK]; nlinarith [abs_nonneg c, norm_nonneg d]
      nlinarith
    · have : |c| ≤ K := by
        rw [hK]; nlinarith [abs_nonneg c, norm_nonneg d]
      nlinarith
  have hk := key (ε * c) (by linarith [habs.1, hεK.1]) (by linarith [habs.2, hεK.2])
  rw [expand] at hk
  -- hk : ‖w‖² ≤ ‖w‖² - 2 ε c² + ε² c² ‖d‖²
  have : ε * c ^ 2 * (ε * ‖d‖ ^ 2 - 2) < 0 := by
    have : ε * ‖d‖ ^ 2 - 2 < 0 := by linarith
    have : 0 < ε * c ^ 2 := by positivity
    nlinarith
  nlinarith

/-- 引理 A：在锥形邻域里，每个最近点 `x` 满足 `⟪p - x, p - a⟫ = ‖p - x‖²`。 -/
theorem inner_sub_eq_norm_sq_of_conical {M : Set E} {a p x : E} {r : ℝ}
    (hcone : LocallyConicalAt M a r) (ha : a ∈ M) (hpa : ‖p - a‖ < r / 2)
    (hx : IsNearest M p x) : ⟪p - x, p - a⟫ = ‖p - x‖ ^ 2 := by
  have h0 := inner_eq_zero_of_conical hcone ha hpa hx
  have : p - a = (p - x) + (x - a) := by abel
  rw [this, inner_add_right, h0, add_zero, real_inner_self_eq_norm_sq]

/-- 若所有 `v ∈ S` 都有 `⟪u, v⟫ > 0`，则 `0` 不在 `S` 的凸包里。 -/
theorem zero_not_mem_convexHull_of_inner_pos {S : Set E} (u : E)
    (h : ∀ v ∈ S, 0 < ⟪u, v⟫) : (0 : E) ∉ convexHull ℝ S := by
  have hconv : Convex ℝ {v : E | 0 < ⟪u, v⟫} :=
    convex_halfSpace_gt (f := fun v => ⟪u, v⟫)
      ⟨fun x y => inner_add_right u x y, fun c x => real_inner_smul_right u x c⟩ 0
  intro h0
  have := convexHull_min (fun v hv => h v hv) hconv h0
  simp at this

/-- 引理 A 的结论：`p ∉ M`、`‖p - a‖ < r / 2` 时，`p` 不是临界点。 -/
theorem not_isCritical_of_conical {M : Set E} {a p : E} {r : ℝ}
    (hcone : LocallyConicalAt M a r) (ha : a ∈ M) (hpa : ‖p - a‖ < r / 2) (hp : p ∉ M) :
    ¬ IsCritical M p := by
  apply zero_not_mem_convexHull_of_inner_pos (p - a)
  rintro v ⟨x, hx, rfl⟩
  have hxp : p - x ≠ 0 := by
    intro h; apply hp; rw [sub_eq_zero.mp h]; exact hx.1
  rw [real_inner_comm, inner_sub_eq_norm_sq_of_conical hcone ha hpa hx]
  positivity

/-- **Corollary B (pointwise form).** Suppose the nearest point `x` of `p ∉ M` has a conical
neighbourhood that reaches past `p`: there are `a ∈ M` and `r` with `M` conical at `a` in radius
`r`, and `‖x - a‖ + δ < r / 2`, where `δ ≥ ‖p - x‖`. Then `p` is not critical.
Hence `wfs(M) ≥ λ(M) = inf_x sup_a (ρ(a)/2 - ‖x - a‖)`. -/
theorem not_isCritical_of_conicalCover {M : Set E} {p x : E} {δ : ℝ} (hp : p ∉ M)
    (hx : IsNearest M p x) (hδ : ‖p - x‖ ≤ δ)
    (hcov : ∃ a ∈ M, ∃ r : ℝ, LocallyConicalAt M a r ∧ ‖x - a‖ + δ < r / 2) :
    ¬ IsCritical M p := by
  obtain ⟨a, ha, r, hc, hlt⟩ := hcov
  apply not_isCritical_of_conical hc ha _ hp
  have := norm_sub_le_norm_sub_add_norm_sub p x a
  linarith
