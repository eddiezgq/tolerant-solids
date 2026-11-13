# Overclaim review: "What is new and what is not" (p1 v0.9, commit e3925ab)

Standard applied: nothing may be claimed new or proved beyond what the body proves, and every description of prior
work must match its source.

How each source was checked:
- **Read in earlier rounds:** Waldhausen68, CCS05, Fu85, CL07, APS00. Checked against the source text.
- **No PDF available:** SPB04, ASZ06, ASZ07, SZ08, Milenkovic88, dREG22. Compared with the earlier Related-work
  paragraphs of sec_intro.tex, which were checked in earlier rounds.

Line numbers refer to sec_intro.tex in v0.9.

**Verdict.** Every description of prior work matches its source or the earlier checked paragraph. One description is
incomplete (SPB04, item D). The "What we add / limits" parts are not yet at the strict standard. Three major
findings:
- Existence: the novelty text omits that Props. B/B′ assume an embedded re-trimmed model, and that Thm lemma0 covers
  regular complexes only.
- Uniqueness: the role of the carrier lemma is overstated.
- Uniqueness: the most important limit, that the collar needs a carried PL reference embedding, is missing.

All fixes are wording changes. No result needs to change.

---

## Major

**A. Existence, "What we add" and "How far we looked" (l.177–179).**
- The text says: "Sufficient conditions under which a 3D B-rep with per-cell tolerance zones has a realization …
  Propositions B and B′ cover sharp edges with tight tolerances."
- The body is narrower:
  - Prop. B assumes that the polygons P̃_f are simple and meet exactly in their common edges and vertices.
  - Prop. B′ assumes a re-trimmed model Σ with a cellwise homeomorphism |K| → Σ (C) lying in the zones (B1–B3). Its
    content is the passage from such a model to a PL realization.
  - sec_existence:4–6 says so plainly: "assume that the re-trimmed model is embedded, which is checked
    computationally on the model itself".
  - For curved models the check is sampled in double precision, and the vertex part of T is not checked
    (sec_existence:148–150).
  - Thm lemma0 is proved for regular complexes only: no seams, closed edges or inner wires (sec_existence:10–15,
    sec_open item 2). The novelty section omits this, although "What we prove" (l.55–56) states it.
- Combined with "We did not find an existence result of this kind for 3D B-reps", the section reads as more than the
  body proves.
- Fix: in "What we add", say that Thm lemma0 (regular complexes, conditional, two non-local hypotheses) derives
  embeddedness from local and disjointness conditions. Say that Props. B/B′ reduce existence to checking an explicit
  candidate: they *assume* the re-trimmed model is embedded and in the zones. Add to "Not covered":
  - B-rep complexes (seams, closed edges, inner wires) for the fan construction;
  - curved candidates are checked only on samples, without the vertex part of T.

**B. Uniqueness, second item of "What we add" (l.143–145).**
- The text says the carrier lemma "derives the π₁-isomorphism needed for Waldhausen's theorem from contractible
  carriers".
- In the body, the carrier lemma only gives a homotopy from h to the reference φ_i inside int U_i.
- The π₁-isomorphism comes from Lemma separation. That lemma needs the collar-condition hypothesis that the inclusion
  of the reference φ_i(|K_i|) into U_i is a homotopy equivalence.
- So "one does not have to know in advance that a realization separates…" is true only because one must know the
  homotopy-equivalence property for *a* reference surface instead.
- Fix: "Together with a reference surface whose inclusion is a homotopy equivalence (collar condition), the carrier
  lemma gives the π₁-isomorphism for every realization. So the separation hypothesis of [CCS05] and the
  one-intersection hypothesis of [SPB04] are needed only for the reference, not for each realization."
- Minor point: the carrier condition in the body is weaker than contractibility (path-connected, π_k = 0). That is
  fine as stated.

**C. Uniqueness, "Limits" (l.150) and third item of "What we add" (l.146–148).**
- The Limits list (genus 0; images, not embeddings) leaves out the main restriction.
- The collar condition is a hypothesis of the theorem. Lemma collar supplies it only when all of the following hold:
  - the reference M_i is a closed PL surface given as a *carried PL embedding* φ of the shell, so it is itself
    realization-like;
  - all zones lie in N_d(M_i) with d < r < wfs(M_i);
  - the sets N̄_r(M_i) are pairwise disjoint;
  - genus ≥ 1.
- "Reference surfaces may have sharp edges and small fillets" is correct only for PL references. A fillet enters as a
  triangulated surface, and the wfs bounds computed in Section 4 are for M_PL, in the stated qualified sense.
- The isotopy is topological (Thm uniqueness (1); Lemma horizontal (c)).
- Fix: add to Limits:
  - "the collar condition is a hypothesis; Lemma collar supplies it when a carried PL reference embedding is known
    whose distance to all zones is below its wfs";
  - "the isotopy is topological".
- Also say "polyhedral reference surfaces (sharp edges, triangulated fillets)".

## Minor

**D. SPB04 (l.138–139, 147–148). The specific question.**
- The earlier, checked paragraph (l.85–87) says: ambient isotopy for a closed surface inside a normal tube of a
  *smooth closed* surface, meeting each normal fibre once, with the tube radius "bounded by curvature **and by a
  double-normal distance**".
- "Needs a smooth reference surface" is supported, though "is stated for" is safer than "needs" without the PDF.
- "A tube radius bounded by its curvature" is supported but incomplete: it drops the double-normal bound.
- The contrast is also slightly one-sided. Their reference is smooth, and ours must be PL (see C). Both are setting
  restrictions, not an advantage on our side.
- Suggested wording: "The result of [SPB04] is stated for a smooth closed reference surface, with the tube radius
  bounded by curvature and by a double-normal distance; ours uses a polyhedral reference and its wfs."
- The "Known" sentence at l.138–139 is consistent with the earlier paragraph. It says "isotopy" where the earlier
  text says "ambient isotopy"; that is acceptable.

**E. wfs bound, "Known" (l.155).**
- The text says: "That wfs(M) > 0 for compact semialgebraic M, hence for polyhedral surfaces."
- Fu proves finiteness for his basic semialgebraic sets, and dREG22 states positivity in general. The extension to
  finite unions is the paper's own reading (l.159–161). The last sentence of the item makes this clear enough.
- Optional: "(for unions, by the same argument)".
- The CL07 sentence matches the source (checked in the v0.8.3 round), and so does the Fu §5.3 description (v0.8
  round). dREG22 is consistent with the earlier paragraph.

**F. wfs bound, "What we add" (l.162–163).** Accurate.
- Lean covers the cone lemma and the pointwise form of Cor. lambda only.
- Positivity λ > 0 for polyhedra uses the local conical structure, which is listed as standard and not
  machine-checked.
- "Key cone lemma is machine-checked" is correct. Optional: note that positivity is not formalized.

**G. Non-existence (l.186–189).** No limits are stated. The theorem covers:
- one pair of faces with *planar* data;
- faces that are disks bounded by a single wire;
- simply connected edge zones (O3).

The curved version is open (Remark; sec_open item 7). Add a "Limits" line. "Checkable" is fair: O0–O4 were verified
in exact arithmetic for the wedges.

**H. Consistency with the abstract and with "What we prove".**
- The Uniqueness wording matches "What we prove" (l.34–42) and the abstract.
- The abstract says "ambient isotopic". Thm uniqueness (1) says "by a topological isotopy". Optional: add
  "(topological)" to the abstract or to the limits.
- Existence: neither the abstract nor "What we prove" (l.58–59) says that the re-intersection construction assumes
  the re-trimmed model is embedded. The abstract also omits "regular complexes". "Under stated hypotheses" covers
  this formally, but after fix A the three places should say the same thing.
- "What we prove" mentions the octree wfs bounds with their qualifications. The novelty section does not claim
  anything about them, which is fine.

**I. Prior-work descriptions without a PDF (Milenkovic88, ASZ06, ASZ07, SZ08).**
- l.170–173 match l.82–83 and l.100–110. "Existence in the plane, with one uniform tolerance" is a fair
  abbreviation.
- APS00 (l.174–175) matches the source (checked in the v0.8 round). It is an isotopy-under-perturbation result
  rather than an existence result, so listing it under "Existence — Known" is a little odd but not wrong.

**J. Waldhausen and CCS05 (l.136–138).** Accurate.
- Waldhausen: Prop. 3.1 gives an isotopy to a surface G′ whose projection p restricts to a homeomorphism on each
  component of G′. For closed G this means a graph, so "made horizontal" is fair.
- Prop. 3.1 requires F ≠ S², which the genus hypothesis guarantees.
- CCS05 Thm 2.1 is described correctly.

**K. Experiments (l.193–196).** Supported by counterexamples in both directions:
- the knotted pipe and the sewn wedge pass both checks;
- the sewn plate is realizable but fails the BOP check.

The scope statement is adequate.

## Summary list
1. Major A: Existence novelty omits that Props. B/B′ assume an embedded candidate, the sampled/unchecked curved
   hypotheses, and the regular-complex restriction of Thm lemma0.
2. Major B: the carrier lemma is said to derive the π₁-isomorphism from carriers alone. It also needs the reference
   homotopy equivalence from the collar condition.
3. Major C: the uniqueness limits omit that the collar condition is a hypothesis, met via Lemma collar only with a
   carried PL reference embedding whose distance to the zones is below its wfs. They also omit PL-only references and
   the topological isotopy.
4. Minor D: SPB04 is "supported but incomplete": add the double-normal bound, use "is stated for", and balance the
   contrast with our PL requirement.
5. Minor E/F: label the extension of Fu's argument to unions as the paper's own reading. Optionally note that
   positivity of λ is not formalized.
6. Minor G: add a Limits line for non-existence: planar, disk faces, simply connected edge zones.
7. Minor H: align the abstract and "What we prove" with fix A. Optionally say "topological" for the isotopy.
8. All other prior-work descriptions match their sources or the earlier checked paragraphs.
