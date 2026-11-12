import Mathlib.Analysis.Convex.Basic
import Mathlib.Topology.UnitInterval
import Mathlib.Topology.Algebra.Module.Basic
import Mathlib.Analysis.Normed.Module.Basic

/-!
# Tolerance zones, carriers, and the convex case of the carrier lemma (Lemma 2)

`ι` indexes the cells of a tolerant B-rep (vertices, edges, faces), partially ordered by
"is a face of". `zone σ` is the tolerance zone of the cell `σ`, and the carrier is
`carrier σ = ⋃ τ ≤ σ, zone τ`.

A map `h : X → E` from the underlying space `X = |K|` is *carried* if every point lands in the
carrier of the open cell containing it (`cellOf x`). A realization satisfies the stronger
condition `h x ∈ zone (cellOf x)`.

Proved here:
* the carrier is monotone, and with augmented (monotone) zones it equals the zone;
* a realization is carried, and closed cells map into their carriers;
* **convex case of Lemma 2**: if every carrier is convex, any two continuous carried maps
  are joined by the straight-line homotopy, which is carried at every time.

The general Lemma 2 (contractible carriers, induction over skeleta) needs CW-complex homotopy
theory and is not formalised here.
-/

open Set

variable {ι : Type*} [PartialOrder ι] {E : Type*}

/-- Carrier of a cell: union of the zones of the cell and of all its faces. -/
def carrier (zone : ι → Set E) (σ : ι) : Set E := ⋃ τ ∈ Iic σ, zone τ

theorem zone_subset_carrier (zone : ι → Set E) (σ : ι) : zone σ ⊆ carrier zone σ :=
  subset_biUnion_of_mem (u := zone) (show σ ∈ Iic σ from le_refl σ)

theorem carrier_mono (zone : ι → Set E) {σ σ' : ι} (h : σ ≤ σ') :
    carrier zone σ ⊆ carrier zone σ' :=
  biUnion_subset_biUnion_left (Iic_subset_Iic.mpr h)

/-- With augmented zones (`τ ≤ σ → zone τ ⊆ zone σ`), the carrier is just the zone. -/
theorem carrier_eq_zone_of_mono (zone : ι → Set E) (hz : Monotone zone) (σ : ι) :
    carrier zone σ = zone σ := by
  apply Subset.antisymm
  · exact iUnion₂_subset fun τ hτ => hz hτ
  · exact zone_subset_carrier zone σ

variable {X : Type*}

/-- `h` is carried by `C`: each point goes into the carrier of its open cell. -/
def Carried (cellOf : X → ι) (C : ι → Set E) (h : X → E) : Prop := ∀ x, h x ∈ C (cellOf x)

/-- A realization (open-cell condition) is carried by the carriers. -/
theorem carried_of_realization (cellOf : X → ι) (zone : ι → Set E) {h : X → E}
    (hh : Carried cellOf zone h) : Carried cellOf (carrier zone) h :=
  fun x => zone_subset_carrier zone _ (hh x)

/-- Closed cells go into carriers: if every point of the closed cell `σ` lies in an open cell
`≤ σ`, then a realization maps the closed cell into `carrier σ`. -/
theorem image_closedCell_subset_carrier (cellOf : X → ι) (zone : ι → Set E) {h : X → E}
    (hh : Carried cellOf zone h) (σ : ι) (closedCell : Set X)
    (hcl : ∀ x ∈ closedCell, cellOf x ≤ σ) : h '' closedCell ⊆ carrier zone σ := by
  rintro _ ⟨x, hx, rfl⟩
  exact carrier_mono zone (hcl x hx) (zone_subset_carrier zone _ (hh x))

/-- **Convex case of Lemma 2.** If every carrier is convex, the straight-line homotopy between
two carried maps is carried at every time. -/
theorem carried_straightLine [AddCommGroup E] [Module ℝ E] {cellOf : X → ι} {C : ι → Set E}
    (hC : ∀ σ, Convex ℝ (C σ)) {f g : X → E} (hf : Carried cellOf C f) (hg : Carried cellOf C g)
    (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    Carried cellOf C (fun x => (1 - t) • f x + t • g x) :=
  fun x => hC (cellOf x) (hf x) (hg x) (by linarith) ht0 (by ring)

/-- The straight-line homotopy is continuous (for continuous `f`, `g`). Together with
`carried_straightLine`, this gives the convex case of Lemma 2: carried maps are homotopic
through carried maps. -/
theorem continuous_straightLine [TopologicalSpace X] [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f g : X → E} (hf : Continuous f) (hg : Continuous g) :
    Continuous (fun p : unitInterval × X => (1 - (p.1 : ℝ)) • f p.2 + (p.1 : ℝ) • g p.2) := by
  fun_prop
