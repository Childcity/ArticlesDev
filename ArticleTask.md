# Task: write an article based on the CompactKernelResearch study

## Objective and required skill

Prepare an original research manuscript in English based on the completed extended experiments 4–6. Apply **[scopus-article-reference-style](scopus-article-reference-style.md)**: read that file in full before drafting, including its paragraph models, mathematical rules, declarations, and completion checks.

Working title:

**Offset fidelity and computational trade-offs in compact pseudo-Gaussian approximation of signed distance fields**

The title may be refined to match the manuscript's actual content. The central question is: what trade-off between field and offset accuracy, geometric correctness, memory, and computational cost is offered by pseudo-Gaussian interpolation, Wendland kernels, and grid interpolation under the specified comparison protocol?

The contribution is a reproducible comparative study, an evaluation of parameter transfer to independent geometries, and a quantitative assessment of the method's applicability. Establish the novelty of specific findings through a literature review; do not attribute the invention of a new basis kernel to this work.

No target journal has been specified. Prepare a **journal-style draft** following the skill's structure. List the journal choice and its current author guidelines as separate items requiring confirmation. The skill's name does not establish indexing status, manuscript suitability, or readiness for submission.

## 1. Study scope

- Main experimental protocol: **`extended-4-6-n4-v1`**.
- The pseudo-Gaussian kernel uses standard, fixed smoothness **n=4**. Tune the support radius and isoline spacing.
- Present this protocol throughout the manuscript without recounting changes to experimental settings.
- The study is computational: analytical SDFs, mathematical properties, and numerical measurements. No laboratory, clinical, or industrial experiments were conducted.
- Compare nine implementations: `pg_grid`, `pg_isolines`, `wendland_c2_grid`, `wendland_c2_isolines`, `wendland_c4_grid`, `wendland_c4_isolines`, `linear`, `cubic`, and `cubic_redistance`.
- The primary evidence for the article's results is in `CompactKernelResearch/results/extended/`. Include illustrations or supporting checks from other materials only after verifying their parameters, provenance, and consistency with n=4.

## 2. Required materials

All paths below are relative to the repository root.

### Research questions and study descriptions

| File | Purpose |
|---|---|
| `scopus-article-reference-style.md` | Required rules for style, structure, and research integrity |
| `CompactKernelResearch.md` | Research questions and mathematical motivation |
| `papers/2025_Pseudo_Gaussian_Modeling/pseudo_gaussian_grid_ric_formatted (2).doc` | Published source paper and stylistic reference |
| `CompactKernelResearch/Experiment4.tex` | Parameter selection and independent evaluation |
| `CompactKernelResearch/Experiment5.tex` | Offsets, gradients, digital topology, and resolution |
| `CompactKernelResearch/Experiment6.tex` | Failure map, resources, editing, and Pareto comparisons |
| `CompactKernelResearch/ExtendedResearch.md` | Summary of results and limitations |
| `CompactKernelResearch/NextStep.tex` | Concise summary of conclusions |
| `CompactKernelResearch/README.md` | Reproduction instructions, metric definitions, and technical qualifications |

The current source paper has the `.doc` extension. Check its equations directly against that document; do not treat supporting notes as a verbatim transcription. Number equations and figures anew in the manuscript. The writing skill is self-contained for stylistic purposes, but it does not replace verification of scientific claims against their sources.

### Data: `CompactKernelResearch/results/extended/`

| File | Use |
|---|---|
| `protocol.json` | Protocol version, n=4, candidates, seeds, map configurations, software versions, and code hashes |
| `training.csv` / `training.json` | Evaluations of all training candidates, timings, and call counters |
| `selection.json` | Parameters selected before the final evaluation |
| `holdout.csv` / `holdout.json` | Raw independent evaluation results |
| `by_shape.json` | Descriptive summaries for individual geometries |
| `resolution.csv` / `resolution.json` | Results at three extraction resolutions |
| `failure_map.csv` / `failure_map.json` | Configurations, residuals, coverage, rank, and threshold flags |
| `resources.json` | Repeated timings, memory, cached updates, full rebuilds, editing errors, and Pareto results |
| `resources.csv` | Tabular representation of resource measurements |
| `summary.json` | Aggregate metrics; verify them against the raw data |
| `tests.txt` | Implementation checks, not proof of mathematical convergence or superiority |

### Code for an accurate Methods section

- `CompactKernelResearch/core.py`: basis kernel, collocation, and `select_isoline_nodes()`.
- `CompactKernelResearch/geometry.py`: exact SDFs and level-set projectors.
- `CompactKernelResearch/comparators.py`: comparator formulas, candidate sets, solvers, and field representations.
- `CompactKernelResearch/experiment4.py`: training and independent geometries, seeds, and selection objective.
- `CompactKernelResearch/experiment5.py`: fixed fields evaluated on different extraction grids.
- `CompactKernelResearch/quality.py`: errors, gradients, regularity mask, Betti numbers, and Pareto dominance.
- `CompactKernelResearch/experiment6.py`, `resource_worker.py`, and `editing.py`: failure map, isolated resource measurements, and editing modes.
- `CompactKernelResearch/run_extended.py`: stage ordering and freezing parameter selection before independent evaluation.
- `CompactKernelResearch/tests/test_extended.py`: mathematical, geometric, and protocol checks.

## 3. Deliverables

Create a dedicated **`CompactKernelResearch/Article/`** directory containing:

1. `main.tex` — the complete English manuscript; `main.pdf` — an inspected compilation, if a compiler is available.
2. `references.bib` — actual cited sources with verified bibliographic details. Explicitly identify unverified entries in the completion list.
3. `EvidenceLedger.md` — a table mapping each claim to its type, supporting file/data row/aggregation method/source, and limits of interpretation. For literature, record the verification method and status.
4. `ParagraphPlan.md` — a paragraph plan mapped to the relevant functions in the skill. Use labels S001–S139 only here, not in the manuscript.
5. `CompletionList.md` — a concise list of missing author details, confirmations, sources, and journal requirements.
6. `README.md` — the main file, compilation command, data provenance, and reproduction limitations.

Add `figures/`, `tables/`, and a reproducible preparation script if needed. Use the existing results and research code as evidence; additional calculations and new illustrations must have their own provenance records. Do not substitute undocumented additional experiments for the specified protocol.

## 4. Required mathematical account

Use distinct notation for dimension D, domain, centers c_j, interpolation locations y_i, coefficients a_j, grid spacing h, support radius r, ratio ρ=r/h, and level spacing Δ. Do not use q for both an integer isoline index and a normalized radial coordinate.

Introduce and explain:

- The kernel `φ₄,r(s)=(1−s²/r²)_+⁵`, its normalization, compact support, C⁴ smoothness, and behavior at the support boundary. Do not infer positive definiteness or accuracy from smoothness alone.
- The field `f(x)=Σⱼ aⱼ φ₄,r(‖x−cⱼ‖)` and the system `Aᵢⱼ=φ₄,r(‖yᵢ−cⱼ‖)`, `Aa=d(y)`.
- The distinction between fixed centers and selected fitting locations. Describe `y_i=c_i` and the nearest admissible point in the union of levels `d(y)=kΔ`, where k is an integer, `0<Δ≤h`, and `‖y_i−c_i‖<r`.
- Rules for nonunique selection, empty levels, support checks, coincident locations, and solver residuals, following the actual implementation.
- The distinction between an implicit field with a desired zero set and an exact SDF. Agreement at level zero does not establish unit gradient magnitude or accurate offsets.
- The Wendland C²/C⁴ formulas, the specific cubic not-a-knot scheme, and the discrete cubic+EDT baseline, including its additional cost and possible surface drift.
- Definitions of band RMSE, gradient error, eikonal residual, normal direction, and discrete distance between offset surfaces.

The estimate `O((1+r/h)^D)` concerns the number of active candidates. Constant cost with respect to the total number of centers requires fixed D and ρ and appropriate access to neighboring centers. Describe the actual use of cKDTree and batched evaluation; do not extend the active-kernel count to the complete cost of tree construction, search, factorization, or the implementation as a whole.

The field is used within the specified domain. Do not describe a finite sum of compact kernels without an extension rule as a globally exact SDF.

## 5. Experimental protocol and interpretation

Describe the experiments that were performed, rather than a proposed future program:

- Parameter selection uses a circle and a square, seeds 0–2, 512 Sobol points per sample, a band RMSE objective, and at most six distinct candidates per parameterized method. Schemes without tuning parameters use one specified configuration.
- Freeze the selection before evaluation. Independent geometries are a capsule, rounded box, narrow-neck polygon, two disks, sphere, and torus; use seeds 10–12, new poses, two h values, and three offsets.
- Parameters selected in 2D are transferred to 3D without separate tuning. Account for this limitation explicitly in the conclusions.
- Reproduce the domain, float64 precision, common centers, margin 4h, and exact h/offset settings from the code and protocol. Separately identify the failure map's margin of 3h.
- Dataset size: 234 training evaluations, 972 records of offset metrics from independent evaluation, 432 resolution-study records, 40 map configurations, and 36 resource cases. Do not describe all these records as independent statistical experiments.
- Explain that the same maximum candidate count does not imply the same amount of geometric information. SDF API counts and projection calls/points have different meanings; tuning time includes candidates and failures.
- Describe the numerical regularity mask for the reference gradient precisely. It checks central differences at two step sizes and gradient magnitude; it is not a complete analytical description of the medial axis.
- For topology, specify foreground connectivity 4/6, background connectivity 8/26, Betti numbers b0/b1/b2, Euler characteristic, and the domain-boundary flag. Three resolutions provide an empirical check, not a convergence proof.
- At n=4, the map varies h, ρ, Δ/h, and node strategy. `quality_threshold`, based on H>0.1 or digital topology, is a diagnostic threshold flag, not proof of geometric inadmissibility.
- Resource measurements use separate subprocesses, one BLAS/OMP thread, three repetitions, and batches of 256/2048/8192 queries. The resource geometries are a capsule in 2D and a torus in 3D, not the entire independent evaluation set.
- Distinguish numerical payload, metadata, L/U factor storage, native peak RSS, construction, projection, and queries. `editing_peak_rss_bytes` is a cumulative maximum that includes preceding process stages, not isolated memory consumption for editing alone.
- Explain cached updates with fixed original interpolation locations and full rebuilds that select locations again. For isolines, a cached update is not a new adaptive placement of fitting points. Compare quality after editing as well.
- Define Pareto dominance separately for 2D/3D using offset error, payload, and query time. Report preparation and tuning costs additionally.

Present medians and ranges of seed-specific medians as descriptive statistics. Do not invent confidence intervals, p-values, or statistical significance.

## 6. Numerical checkpoints and conclusions

Before use, check these values against `summary.json` and the raw records. This table contains median field RMSE within the evaluation band, not continuous-surface error:

| Method | 2D | 3D |
|---|---:|---:|
| `pg_grid` | 0.0135285 | 0.0194621 |
| `pg_isolines` | 0.0146536 | 0.0496070 |
| `cubic` | 0.0128315 | 0.0184655 |
| `wendland_c2_grid` | 0.0127767 | 0.0176876 |
| `wendland_c4_grid` | 0.0132542 | 0.0155254 |

Develop the following conclusions within the limits of the evidence:

1. The pseudo-Gaussian sum with grid locations achieved accuracy close to cubic interpolation under the tested conditions. This does not establish equivalence.
2. An overall advantage of isoline-based location selection was not confirmed on the independent set. Describe local improvements and worse cases together; do not present their causes as established without further analysis.
3. Smoothness, fitting residuals, field accuracy, gradients, offsets, and topology are distinct properties.
4. The map contains 13 configurations within the threshold, 19 with a quality flag, and 8 with uncovered points. Do not interpret these fractions as probabilities of method success.
5. Usefulness depends on the workload and resource trade-off. Support any torus example at a particular h with records from `resources.json`; do not generalize it to every geometry.
6. Even the exact reference for a thin torus may be under-resolved. Digital components and holes on one grid do not establish the topology of the continuous field.

Literature novelty, global guarantees, and industrial performance do not follow from this benchmark. Future directions include separate 3D tuning, external geometries, larger scales, and justified stability/convergence estimates. Do not describe these directions as completed work.

## 7. Manuscript structure and style

Follow the skill's argumentative sequence:

1. **Title, authors, abstract, keywords.** Use two connected abstract paragraphs: the practical problem; then the contribution, actual result, and main limitation. Include only confirmed author details. Add Ukrainian front matter and UDC only when required by the journal.
2. **Problem statement.** Use two paragraphs: the SDF representation/evaluation problem and the specific research question.
3. **Literature review.** Cover six functions: grid representations; alternative models; the position of our comparison; adjacent RBF research; gradient/additional constraints; and motivation for the chosen protocol. Specify the role of every citation.
4. **Methods.** Explain the overall procedure, component definition, interpolant construction, centers and fitting locations, solution procedure, 2D/3D formulation, parameter selection, and reproducible comparison conditions.
5. **Selection of interpolation points and comparative evaluation.** Describe the baseline, isoline selection, independent parameter selection, and observations. Connect examples to quantitative measurements.
6. **Discussion.** Address successful and unsuccessful cases, parameter effects, coverage, distinctions between metrics, topological discretization, resources, and editing. Map the refinement-experiment functions S106–S108 to the actual selection and independent evaluation; do not add a fictional optimization study.
7. **Conclusion.** Preserve the seven functions S110–S116: contribution and bounded finding; computation; storage; freedom to choose fitting locations; practical implementation; unresolved parameter questions; and the principal next research step. Use connected paragraphs and adapt their length appropriately.
8. **Declarations and References.** Include confirmed information or explicitly marked unresolved draft items only.

In `ParagraphPlan.md`, map the draft to the skill's functions, including the roles of figures and equations. Mark inapplicable functions with a reason; do not invent results to fill them. Add a separate Results section if the journal requires it, preserving the sequence of definition, evidence, and limitation.

Write explanatory academic English with one main claim per paragraph. Use “we” for actions actually performed by the authors, present tense for definitions, and past tense for completed procedures. Do not copy conversational expressions, typographical errors, or absolute statements from the source paper.

## 8. Figures and tables

The main existing figures are in `CompactKernelResearch/results/extended/`:

- `holdout.pdf` — independent comparison;
- `resolution.pdf` — dependence on extraction-grid resolution;
- `torus_topology.pdf` — thin torus and digital topology;
- `failure_map.pdf` — parameter map at n=4;
- `pareto.pdf` — trade-offs between accuracy, memory, and time.

Also plan the roles of an overview comparison, kernel behavior, baseline/isoline results, and a specific unsuccessful case. The skill's figure roles may be combined in multipanel figures. Do not artificially require exactly eight figures. An aggregate plot does not replace an illustration of an individual geometry.

Choose specific examples from actual configurations. For newly rendered figures, retain the code and parameters and check them against the data. Identify a new schematic or analytical plot explicitly as such. Captions must state the method, h, ρ, Δ/h, offset level, and resolution when these affect interpretation. Use consistent scales, domains, and legends in matched panels.

The main tables should cover the protocol and selection; independent errors; topology/resolution; and resources and editing. Place large raw tables in supplementary material or the repository. Do not imply statistical independence among repeated offsets and grids.

## 9. Literature and declarations

Verify sources on compact RBFs/Wendland kernels, SDF approximation, offsets, distance reconstruction, interpolation errors, digital topology, and related comparative studies. Cite the original paper using verified bibliographic metadata. Distinguish library documentation and implementations from primary scientific publications.

Use numerical citations in order of first appearance unless the journal specifies otherwise. Verify authors, title, year, venue, pages/article number, and DOI against original publications or official records. Do not automatically reuse the reference paper's eleven sources. If online verification is unavailable, identify the specific unverified entries; do not invent DOIs or literature-review findings.

Authorship, author order, affiliations, ORCID identifiers, and corresponding-author details require confirmation. Git names and email addresses do not establish the manuscript's author block. Competing interests, funding, licensing, and data/code availability conditions also require separate confirmation.

The numerical CSV/JSON files are research data created by this study: a no-data declaration is inappropriate. Describe AI assistance in the research/manuscript according to actual use and journal policy; do not assert the absence of AI assistance or completed author review without evidence.

Use the skill's required draft markers: `{SOURCE REQUIRED: ...}`, `{RESULT REQUIRED: ...}`, and `{AUTHOR CONFIRMATION: ...}`. Collect them in `CompletionList.md`; do not fill them with plausible invented information. Missing journal details or author declarations must not block drafting sections supported by the available materials.

## 10. Workflow and acceptance criteria

1. Read the skill and research materials; verify the protocol version and n=4. Create the evidence ledger and notation glossary.
2. Prepare the paragraph plan and map it to the skill's functions.
3. Draft the mathematical formulation, Methods, and protocol; then the results and Discussion, including limitations.
4. Prepare and inspect tables/figures with traceable provenance. Check every rounded value against the raw data.
5. Draft the Problem statement, verified Literature review, and Conclusion. Finalize the title and two-paragraph abstract last.
6. Add declarations and references, explicitly listing items requiring confirmation.
7. Compile and inspect the PDF: equations, captions, tables, fonts, line breaks, and cross-references. If compilation is unavailable, record the specific limitation in `CompletionList.md`.

The deliverable is acceptable when:

- every claim and number has a source or an explicitly stated evidence status;
- n=4 is consistent across Methods, abstract, results, captions, and conclusions;
- the manuscript preserves the skill's argument and relevant paragraph functions while using original wording;
- calibration, independent evaluation, discretization, and resource results are distinguished;
- negative results and applicability limits are reported fully;
- citations, equations, figures, and tables are correctly linked and numbered consecutively;
- there are no unsupported claims of a globally exact SDF, universal improvement, guaranteed topology, a global optimum, or constant O(1) cost for the complete implementation;
- passing tests is not presented as proof of scientific superiority;
- labels S001–S139, template instructions, and borrowed author declarations do not appear in the manuscript;
- outstanding questions are collected in a separate concise list, and the draft's completion status is stated honestly.
