import Mathlib.Topology.Basic
import Mathlib.Topology.MetricSpace.HausdorffDistance

/-! 第 0 阶段环境检查：正则闭集（closure (interior s) = s）的一个小引理，确认 Mathlib 可用。 -/

open Set

/-- Requicha 意义下的正则闭集。 -/
def IsRegClosed {X : Type*} [TopologicalSpace X] (s : Set X) : Prop := closure (interior s) = s

/-- 正则化 k·i 的结果总是正则闭集。 -/
theorem isRegClosed_closure_interior {X : Type*} [TopologicalSpace X] (s : Set X) :
    IsRegClosed (closure (interior s)) := by
  unfold IsRegClosed
  apply Subset.antisymm
  · exact (closure_mono interior_subset).trans closure_closure.subset
  · exact closure_mono (interior_maximal subset_closure isOpen_interior)
