# Evidence ledger

Paths below are relative to `CompactKernelResearch/` unless stated otherwise. Primary data are in `results/extended/`. Date of verification: 2026-11-02. `prepare.py` and `provenance.json` provide exact filters, hashes and aggregation methods. The same records can share a field, pose, offset or seed; rows are not independent experiments.

| Claim / manuscript location | Type | Support and verification | Interpretation limit |
|---|---|---|---|
| Fixed n=4, frozen protocol | Observation | `protocol.json`, `selection.json`; prepare.py checks version/order and every source hash | No other protocol pooled |
| Kernel, normalization, compact support, C4 boundary | Mathematical consequence | `core.kernel`, `comparators.basis`; fifth-order boundary zero of (1-s²/r²)^5 | No positive-definiteness inference; DOC equations still pending |
| Finite sum and square collocation | Implementation | `comparators.collocation/build`; displayed equations derived from code | Square does not imply invertible |
| Grid center geometry and 4h margin | Implementation | `core.lattice`, `comparators.build` | Evaluation only within [-1,1]^D |
| Nearest admissible level; ties and duplicates | Implementation | `core.select_isoline_nodes`, `geometry.Geometry.project_level`, `comparators.build` | Exact analytical projectors supply more information than grid samples |
| LU and residual threshold | Implementation | `comparators.build` | Residual is not condition estimate or surface accuracy |
| Active candidate count | Mathematical consequence | Lattice centers inside radius r fit inside a D-dimensional box with O(1+r/h) coordinates per axis | Fixed D/rho and neighbor access; excludes trees/solve |
| Wendland/cubic/EDT formulas | Implementation/background | `comparators.basis/build`, Wendland record below | No claim EDT preserves continuous zero level |
| Training settings and finite search | Observation | `experiment4.tune`; `training.json` 234 rows; `selection.json` | Mean of six training band errors; not global optimum |
| Frozen choice/tuning costs, Table selection | Observation | Every entry of `selection.json`; script table maps each method to config and tuning_seconds | Includes all candidates and failures; counters have different meanings |
| Held-out settings and counts | Observation | `experiment4.case/evaluate_holdout`; `holdout.json` 972 rows | 2D-trained parameters transferred to 3D |
| All medians, abstract and errors table | Observation | Filter successful holdout rows by method/dim; median band_rmse, gradient_rmse, available H; seed min/max of three medians. Field/seed values checked against summary | H omits missing/unresolved distances; missingness must be read with counts. Ranges are descriptive |
| Close PG grid/cubic errors | Bounded interpretation | Verified medians 0.0135285/0.0128315 (2D), 0.0194621/0.0184655 (3D) | No equivalence or significance claim |
| No overall isoline benefit | Bounded interpretation | PG isoline medians 0.0146536/0.0496070 and paired examples | No causal mechanism established |
| Favorable/unfavorable geometry illustrations | Reconstructed observation | `provenance.json` examples; smallest/largest paired 2D PG isoline/grid band ratios, reconstructed at saved pose/h/offset; compare RMSE to raw rows | Deliberately selected extremes, not representative sample; no new tuning |
| Analytical kernel plot | Mathematical illustration | `prepare.py` calls actual basis on 400 radii, n=4 | No empirical performance inferred |
| Gradient/eikonal/normal definitions | Implementation | `quality.reference_gradient/gradient_quality` | Numerical regularity mask, not full medial axis |
| Offset point-cloud metric | Implementation | `experiment2.offset_metrics`, `quality.measure` | Not continuous Hausdorff bound; unresolved levels omitted from distance medians |
| Digital topology and clipping | Implementation | `quality.topology` | Connectivity and grid dependent; b0/b1/b2 agreement excludes boundary flag |
| 432 resolution records; thin torus | Observation | `experiment5.run`, `resolution.json`; table filters shape=torus, t=-.19, method PG grid/isolines/cubic | Same fields evaluated at three resolutions; no convergence proof |
| 13/19/8 failure-map counts | Observation | Counter of `failure_map.json` flag; 40 rows verified | Coverage overrides quality; counts not success probabilities; repeated grid configurations |
| Resource timings, payload and H table | Observation | `resources.json`, dim=3,h=.4; each method; recorded build/query medians, arithmetic mean offset H | Only torus pose 47 degrees/shift .01; excludes tuning |
| Editing table | Observation | Same resource filter; cached and rebuilt times; median of three recorded error values | Errors from 256 Sobol probes, not held-out bands; shifts .01,-.01,.02 |
| Peak RSS/factors/metadata distinctions | Implementation | `resource_worker.run`, `editing.prepare/benchmark` | Editing peak includes preceding stages, not isolated increment |
| Pareto definition | Implementation | `quality.pareto_mask`, `experiment6.resources` | Separate dimension, includes both h; excludes preparation/tuning objectives |
| Seven conclusion functions | Interpretation/future work | Above evidence and bounded scope | External geometries/3D tuning/convergence are future work |
| No laboratory/industrial claim | Scope | Analytical geometry generators and numerical pipeline | No external validation supplied |

## Literature verification and citation roles

| BibTeX key | Role and verified fields | Verification source/method | Status |
|---|---|---|---|
| frisken2000 | Grid/adaptive distance-field context; author names, title, SIGGRAPH, 2000, 249–254 | Author-institution publication listing: https://www.merl.com/publications/?tags=frisken | Listing verified; full proceedings expansion optional; no DOI asserted |
| wendland1995 | Compact RBF family and limits of transferring theory; author/year/volume/pages/DOI | Official university record opened: https://eref.uni-bayreuth.de/id/eprint/55365/ | Verified metadata except title wording discrepancy (“basis”); see completion list |
| kaleniuk2025 | Methodological antecedent, not evidence for this benchmark's numerical results | Journal search record https://ric.zp.edu.ua/article/view/324222 ; institution https://eir.zp.edu.ua/items/2b14ec25-43e5-4c1e-b32a-e69826ad7dc5 ; official citing article https://nasu-periodicals.org.ua/index.php/its/article/view/29831 | Metadata corroborated in indexed official records; direct journal page timeout and DOC-equation inspection pending |
| felzenszwalb2012 | Discrete distance reconstruction context, not attribution of SciPy algorithm | Publisher page opened https://theoryofcomputing.org/articles/v008a019/ | Author/title/year/volume/article/pages/DOI directly verified |

Literature gaps on error theory, gradient constraints, topology and comprehensive novelty are explicit manuscript markers. Library implementation facts are attributed to repository code, not passed off as primary scientific publications.
