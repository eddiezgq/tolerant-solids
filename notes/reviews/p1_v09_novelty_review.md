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

---

## Follow-up on v0.9 fixes (commit d5046cb)

**Verdict.** Findings A–H are all resolved. The fixes introduce no new overclaims. Three small wording points
remain (N1–N3), all optional.

| Finding | Status | Where |
|---|---|---|
| A | Resolved | Existence "What we add" now separates the two kinds of result. Thm lemma0 constructs a realization, for regular complexes only, conditionally. Props. B/B′ assume an embedded candidate in the zones and only check it. Sampled double-precision checks and the unchecked vertex part of T are stated. "How far we looked" is narrowed to "either kind … with per-cell tolerance zones". |
| B | Resolved | The carrier lemma now only gives a homotopy to the reference inside the collar. The π₁-isomorphism is attributed to that homotopy together with the collar's homotopy-equivalence hypothesis (Lemma separation). This matches the body. |
| C | Resolved | Limits now state that the collar condition is a hypothesis, with Lemma collar's exact requirements: carried PL reference embedding, zones in N_d(M), d < r < wfs(M), disjoint closed r-neighbourhoods, genus ≥ 1. They also state "PL reference surfaces" with triangulated fillets, and "topological isotopy, of images". All match Lemma collar (a′)/(b) and Thm uniqueness. |
| D | Resolved | SPB04 now says "is stated for a smooth closed reference surface", with the tube radius bounded by curvature *and* a double-normal distance. This matches the earlier checked paragraph (l.85–87), and the contrast is balanced ("ours needs a PL reference"). |
| E | Resolved | "Hence for polyhedral surfaces" is gone, and the extension of Fu's argument is marked "our reading". |
| F | Resolved | The text now says "positivity λ(M) > 0 is proved on paper and not formalized". |
| G | Resolved | A Limits line for non-existence now matches the theorem's setting: one pair of planar faces, closed cells that are disks bounded by single wires, O3, and the curved case open. |
| H | Resolved | The abstract says "(topologically) ambient isotopic", "conditional theorem for regular complexes", and that the re-intersection "assumes that the re-trimmed candidate is embedded". "What we prove" adds the same assumption. All three places now agree. |

### Remaining nits (minor, optional)
- **N1. Clause labels for Prop. B (sec_intro, Existence "What we add").** "(clauses C and B1–B3)" names clauses of
  Prop. B′ only. Prop. B states the same assumptions as unlabelled bullets: zone containment, and simple polygons
  meeting exactly in common edges and vertices. Also, for Prop. B the candidate is already PL, so "turn it into a PL
  realization" applies to B′ only.
  - Suggested wording: "(Prop. B: simple polygons meeting exactly in common edges and vertices, in the zones; Prop. B′:
    clauses C and B1–B3)".
- **N2. "Separation-type hypothesis" (Uniqueness, second item).** The reference hypothesis is that its inclusion into
  the collar is a homotopy equivalence, not a separation property.
  - Suggested wording: "a hypothesis on the reference (homotopy equivalence) takes the place of separation, and is
    needed only for the single reference surface".
- **N3. Setting restrictions of Props. B/B′ in the novelty section (optional).** Prop. B: planar faces, degree-three
  vertices. Prop. B′: C² regular parametrizations, with no sphere poles or cone apices. These are in the body and are
  not claimed away, so this is optional.

Nothing else in the changed text goes beyond the body or misdescribes a source.

---

## Follow-up: OCCT source claims (commit 1132302)

Sources:
- OCCT tag V8_0_1 (b8f597c), a sparse checkout plus single-file `git show` from the tag.
- GitHub code search over the OCCT repository, for files outside the checkout. This searches the default branch, not
  the tag.
- The repository's own compute/compare_occ.py, compute/summarize_occ.py, results/compare_occ_default.json and
  README.md.

**Verdict.** Both source claims are correct, and the BRepCheck conclusion is supported. Three wording points need a
small change (S1–S3). One of them (S1) is a factual slip in the offsets sentence: it says "in one case six shells",
but the data show six shells in every wrong case.

### 1. BRepCheck: "never reports a tolerance as too large". Supported.
- **The NYI comment.** BRepCheck_Analyzer.hxx:47, 52 and 56 list `BRepCheck_InvalidToleranceValue NYI` under the
  geometric controls for a vertex, an edge and a face. **OK.**
- **The flag.** BRepCheck_Analyzer.cxx:159 declares `bool isInvalidTolerance = false;`. Its only other occurrence is
  the test at l.264, which guards `aFaceRes->SetStatus(BRepCheck_InvalidToleranceValue)` (l.266). It is never
  assigned. **OK.**
- **Every SetStatus path in BRepCheck (tag source).**
  - Literal statuses: within BRepCheck the literal `BRepCheck_InvalidToleranceValue` appears only in
    BRepCheck_Status.hxx (enum), BRepCheck.cxx (print), Analyzer.hxx (comments) and Analyzer.cxx:266 (the dead
    branch).
  - Status passed through a variable: one case, Analyzer.cxx:81–85, `SetStatus(ste)`. Here `ste` comes from
    `BRepCheck_Edge::CheckPolygonOnTriangulation`, which returns only `BRepCheck_NoError` or
    `BRepCheck_InvalidPolygonOnTriangulation`. The other `ste` variables (l.184, 235) only read existing status lists.
  - BRepCheck_Vertex, BRepCheck_Edge and BRepCheck_Face never name the status. Their tolerance tests have the form
    "deviation > tolerance → error" (for example BRepCheck_Vertex.cxx:145–233 and 256–268), so a tolerance can only be
    reported as too *small*.
  - The vertex case in the analyzer explicitly checks nothing (Analyzer.cxx:68–75).
- **Outside BRepCheck.** Code search finds one other file: src/Draw/TKTopTest/BRepTest/BRepTest_CheckCommands.cxx:843.
  I checked it at the tag. It only reads a counter, `NbProblems->Value(BRepCheck_InvalidToleranceValue)`, for the
  report, and sets nothing. Caveat: code search covers the default branch and exact-token matches. The tag files I
  fetched agree with it.
- **Conclusion.** The paper's wording ("no other file sets the status"; "BRepCheck never reports a tolerance as too
  large") is supported.
- **S2 (minor, sec_intro ~l.69).** The new clause sits next to "accepts models regardless of the size of the
  tolerances". That phrase is too broad: BRepCheck *does* reject tolerances that are too small (deviation > tolerance).
  - Suggested wording: "accepts models however large their tolerances are; in the source, its tolerance-value check is
    declared but not implemented."

### 2. Offsets: mechanism, hedging, and the offset range.
- **BRepOffset.cxx.** `BRepOffset::Surface` adds the offset to the radius (subtracts it if the axis is indirect) and
  sets `BRepOffset_Reversed` when the new radius is ≤ −Tol:
  - cylinder, l.64–86 (the reversed cylinder is still built, with |radius|);
  - sphere, l.110–137;
  - torus (minor radius), l.153–166.

  `BRepOffset_Offset` gets its status from this function (BRepOffset_Offset.cxx:524). **OK**, with the scope noted in
  S3.
- **BuildOffsetByArc.** BRepOffset_MakeOffset.cxx:2101–2108 skips a face when
  `SF.Status() == BRepOffset_Reversed || SF.Status() == BRepOffset_Degenerated`. The comment is quoted exactly:
  "Degenerated or returned faces are not stored." **OK.**
- **Default mode.** `BRepOffsetAPI_MakeOffsetShape::PerformByJoin` defaults to Intersection = false and
  Join = GeomAbs_Arc (header at the tag). compare_occ.py calls it with exactly these settings (l.112). So "default
  mode" and the BuildOffsetByArc path agree.
  - Supporting evidence: the same offsets in "inter" mode give correct volumes (summarize_occ output).
- **Range.** compare_occ_default.json and summarize_occ.py, for the filleted box (edge 10, fillet 2, wfs 5):

  | Inward offset | Offset value | Relation to fillet radius / wfs | Result |
  |---|---|---|---|
  | −0.25·wfs | 1.25 | below the fillet radius | volume correct |
  | −0.5, −0.75, −0.9, −0.99 ·wfs | 2.5, 3.75, 4.5, 4.95 | above the fillet radius, below wfs | volume errors 44%, 476%, 3500%, 359900%; every result valid per BRepCheck |
  | −1.01 to −1.5 ·wfs | beyond wfs | outside the wfs-safe range | non-empty results where the exact offset is empty |

  - All outward offsets are correct.
  - So "inward offsets larger than the fillet radius but within the wfs-safe range" and "errors from 44% to over a
    thousandfold" match the data and the README (l.46). **OK.**
- **S1 (minor, factual; the sentence was edited in this commit).** "and in one case six shells instead of one" is
  wrong. All four wrong results inside the wfs-safe range have `shells: 6` (and Euler characteristic 6), as do the
  three beyond wfs.
  - Fix: "with six shells instead of one in every such case".
- **Hedging.**
  - "A plausible mechanism …" and "We have not traced the rest of the algorithm" are suitably hedged.
  - **S3 (minor).** The next sentence is stated flatly: "These failures do not involve tolerances; they are failures of
    face-by-face offsetting when faces must disappear." This goes beyond what was traced.
    - Suggested wording: "These failures appear not to involve tolerances; they look like failures of face-by-face
      offsetting when faces must disappear."
  - **S3 (scope).** The Reversed status is set only for cylindrical, spherical and toroidal faces. For other surface
    types (for example B-spline fillet patches), `BRepOffset::Surface` sets no such status. I could not confirm the
    surface types of the fillet faces of the test part, because OCP is not installed here. min_curv_radius = 2.0 in the
    results shows that analytic faces of radius 2 exist. Suggested wording: "when the offset radius of a cylindrical,
    spherical or toroidal fillet face becomes negative".

### Summary
- Claim 1 (BRepCheck): supported, including every SetStatus path and the files outside BRepCheck. S2 is a wording
  point in the intro.
- Claim 2 (offsets): the source facts are correct, the default mode matches the script, and the range matches the
  data.
- Fixes needed: S1 (the "one case" of six shells is wrong) and S3 (one unhedged sentence; restrict to analytic fillet
  faces).
