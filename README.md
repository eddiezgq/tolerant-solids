# tolerant-solids

**When does a tolerant B-rep define a unique solid?**

CAD kernels store solids as boundary representations (B-reps) whose geometry does not fit together exactly. Edges, vertices and faces carry tolerances, and the "real" solid is only implied. This repository asks two questions:
- **Existence:** is there at least one embedded surface that respects all the tolerances (a *realization*)?
- **Uniqueness:** are all realizations the same up to ambient isotopy?

It contains the proof drafts, certified computations and experiments for the first paper (P1) of a research programme on this question. The programme is run by Eddie (Guoqing) Zhang, with AI assistance (Claude) for proofs, code and review. Every claim below states its status. Nothing marked *draft* should be read as proved.

## Status (2026-11-12, phase 1)

| Item | Status |
| --- | --- |
| Uniqueness theorem, genus ≥ 1 shells, set-level isotopy | Draft proof, two independent reviews. Current text: [notes/uniqueness_v01.md](notes/uniqueness_v01.md). The first draft and the reviews are in [notes/proof_v0.md](notes/proof_v0.md) and [notes/reviews/](notes/reviews/). The proof uses Waldhausen 1968, Prop. 3.1. Sphere shells and isotopy at the level of embeddings are not done. |
| Lemma 0 (existence): local cone/fan construction | Draft v0.2, a *conditional* theorem with two non-local hypotheses (V1(b), P0), which were verified only on the gapped cube (implicitly, through the exact embedding check). Versions v0 and v0.1 had two independent reviews (the first found a fatal error, since fixed); the v0.2 proof as a whole has not been re-reviewed, and its PL step has one open gap at the cone apex ([notes/lemma0_v02.md](notes/lemma0_v02.md)). Demonstrated exactly on a gapped cube ([compute/lemma0_box.py](compute/lemma0_box.py)). Its local hypotheses were checked on 17 OpenCascade models ([notes/lemma0_check_report.md](notes/lemma0_check_report.md), sampled): exact models pass; sewn models with OCC's tolerance of 1.05 x deviation fail at the vertices, and a second construction (re-intersection) realizes some of them. Draft v0.3.2 ([notes/lemma0_v03.md](notes/lemma0_v03.md), three independent reviews, no fatal error found) adds a variable tube radius, the re-intersection proposition, and an **obstruction lemma** (Lemma O): hypotheses under which a tolerant B-rep has no realization. |
| Paper P1, English draft | [paper/p1.pdf](paper/p1.pdf), v0.3 after three independent reviews ([notes/reviews/p1_draft_v01_review.md](notes/reviews/p1_draft_v01_review.md)). Unchecked citations are marked in red, open steps in orange. Not for circulation. |
| Sewn wedges (30°, 10°) | Lemma O's hypotheses hold, re-verified in exact rational arithmetic; both models pass `BRepCheck_Analyzer` and `BRepAlgoAPI_Check`. So, by Lemma O, they have no realization. Lemma O is a reviewed draft, not a published or refereed result. |
| Cone lemma: no critical points of the distance function within half the conical radius of a polyhedral surface; Corollary B (pointwise form) | Machine-checked in Lean 4 + Mathlib ([lean/Tolerant/Cone.lean](lean/Tolerant/Cone.lean)), with no `sorry` and standard axioms only. That wfs > 0 for semialgebraic sets is known (Fu, Duke Math. J. 1985; we have not yet checked the original). The explicit conical-radius bound was not found in the literature we checked; that does not make it new. |
| Definitions (zones, carriers, carried maps) and the convex-carrier case of Lemma 2 (the straight-line homotopy stays carried) | Machine-checked in Lean ([lean/Tolerant/Carrier.lean](lean/Tolerant/Carrier.lean)). The general Lemma 2 (contractible carriers, induction over skeleta) is not formalised. |
| Certified lower bound on the weak feature size (wfs) of a triangle mesh | Implemented ([compute/wfs_cert2.py](compute/wfs_cert2.py)) and independently reviewed. Uses double precision, not interval arithmetic. |
| Experiments: OpenCascade checks vs. realizability | Done and reviewed ([compute/exp6a.py](compute/exp6a.py), [exp6b2.py](compute/exp6b2.py), [exp6c.py](compute/exp6c.py)). |

## Main experimental findings (OpenCascade 8.0.1, the parts in this repository only)

- **Certified wfs bounds**: "no critical value in (0, LB)".

  | Part | Certified LB | Exact wfs |
  | --- | --- | --- |
  | Cube with side 10 | 4.530 | 5 |
  | Plate 4×4×1 | 0.436 | 0.5 |
  | L-shape | 0.894 | 1 |
  | L-shape with a 0.2 inner fillet | 0.894 | 1 |

  The fillet shrinks the classical reach to 0.2 but leaves the certified wfs bound unchanged.
- **`BRepCheck_Analyzer` does not respond to the size of the tolerance.** It accepted every model, at every tolerance tested.
- **`BRepAlgoAPI_Check` is a heuristic.**
  - It reports false self-intersections where our collar condition is certified, e.g. on a filleted L-shape at τ = 0.1 < wfs = 1.
  - It misses cases where τ exceeds the wfs of the nominal surface.
- **A model that passes both checks but has two non-homeomorphic realizations** (exp6b2.py):
  - the model is a thick pipe with tolerance 1.3 × the hole radius;
  - one realization ties a trefoil in the hole (knot determinant 3, against 1 for the nominal pipe).

  This shows that the collar hypothesis of the uniqueness theorem cannot be dropped.
- **A model that passes `BRepCheck` but has no realization** (exp6a.py): it contains two linked triangles. This is a reproducible record of a known phenomenon.
- **Offsets:** in its default mode, `BRepOffsetAPI_MakeOffsetShape` returns a geometrically wrong solid that BRepCheck accepts. This happens on a filleted cube once the offset exceeds the fillet radius, still inside the wfs-safe range.

## Layout

```
compute/          Python scripts (OpenCascade via cadquery-ocp, numpy, scipy, pyknotid)
  wfs_cert.py       octree + LP certified wfs lower bound (v1; leaves a band near M unchecked)
  wfs_cert2.py      v2: adds the cone lemma near M and best-first search; this is the version to use
  compare_occ.py    OpenCascade checks, thickness heuristics and offset tests
  summarize_occ.py  checks offset volumes against exact formulas
  exp6a.py, exp6b.py, exp6b2.py, exp6c.py   task-6 experiments
  lemma0_box.py     exact (rational) Lemma 0 construction on a gapped cube
  checks/           negative controls and independent checks used in the reviews
lean/             Lean 4 project (Mathlib); Tolerant/Cone.lean is the cone lemma
notes/            proof drafts (English); notes/reviews/ holds the independent review reports
results/          outputs of the runs reported above
```

## Reproduce

```bash
python -m venv occ && . occ/bin/activate
pip install -r requirements.txt
cd compute
python lemma0_box.py                         # about 1 min, exact arithmetic
python exp6a.py
python wfs_cert2.py box plate L-shape        # a few minutes
PYTHONPATH=. python checks/lemma0_box_negcontrol.py   # must report embedding violations
```

Lean (needs elan):

```bash
cd lean && lake exe cache get && lake build
lake env lean Axioms.lean                    # prints the axioms the cone lemma depends on
```

## Caveats

- The certified wfs computation uses double precision, not interval arithmetic.
- pyknotid misses crossings when segments are very short. `exp6b2.py` scales curves by 100 first; a reviewer cross-checked the result with Fox colourings.
- The experiments cover a few primitive and boolean parts in one kernel version. They are not a survey of industrial models.

## License

- Code (`compute/`, `lean/`): MIT, see [LICENSE](LICENSE).
- Notes and documentation (`notes/`, this README): CC BY 4.0, see [LICENSE-docs](LICENSE-docs).
