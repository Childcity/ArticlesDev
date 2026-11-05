# Article draft

`main.tex` is the English journal-style draft; `main.pdf` is its compiled version. `references.bib` is the cited bibliography. This is an incomplete submission draft: see `CompletionList.md` for exact evidence and author items. The manuscript does not claim confirmed novelty or submission readiness.

From this directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ../../.venv/bin/python prepare.py
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Requirements: the research requirements file, XeLaTeX, BibTeX, DejaVu Serif. The script uses existing results from `../results/extended/`, checks protocol, counts, source hashes, field-error/seed aggregates, and reconstructs two already-recorded 2D configurations for matched figures. It does not rerun training, alter the frozen selection, or replace archived timings. It generates tables, an analytical kernel plot, two geometry examples, and `provenance.json`. All input JSON SHA256 hashes and example settings are retained there. Relative paths resolve from the script location.

The main evidence is protocol `extended-4-6-n4-v1` at repository commit `b514b8eb05587a0e4d8ff2aeb86e4684062bd09a`. The original recorded environment is Python 3.12.14, NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2 and scikit-image 0.26.0 on Linux x86_64. Timing results describe the archived runtime, not the current article-generation run. No physical unit calibration, full hardware specification or industrial validation is supplied.

The original README commands were previously checked in this session: 96 tests passed; `generate.py` completed. Those commands concern implementation checks and earlier experiments, not a rerun of the extended evidence. Generated earlier results were restored before this work. The article script leaves all research inputs unchanged.

`EvidenceLedger.md` records scientific support and verification limits. `ParagraphPlan.md` maps the required writing functions. Journal selection and author declarations remain open.

## Ukrainian translation and review

- `main.uk.tex` / `main.uk.pdf`: complete Ukrainian translation; original figure PDFs are reused, with translated captions and table headers. Mathematical notation, numerical results and unresolved source/author markers are preserved. Bibliography titles remain in their original language.
- `Review.uk.md`: substantive Ukrainian review of structure, novelty, results and limitations, based on commit `84c3f01`, code/data inspection and a targeted literature search. Includes reproducible descriptive comparisons, source links and prioritized recommendations.
- During review the publisher page became accessible and revealed that the 2025 antecedent has five authors. The shared bibliography and English prose were corrected; this does not establish authorship of the present manuscript. Other review recommendations remain proposed revisions.

Build the Ukrainian version from this directory (XeLaTeX, Polyglossia and a Cyrillic-capable DejaVu Serif font):

```bash
../../.venv/bin/python localize_tables.py
xelatex -interaction=nonstopmode -halt-on-error main.uk.tex
bibtex main.uk
xelatex -interaction=nonstopmode -halt-on-error main.uk.tex
xelatex -interaction=nonstopmode -halt-on-error main.uk.tex
```

Run `localize_tables.py` after `prepare.py` when regenerating data tables. It replaces headers only, preserving every data row. The review introduces no new benchmark runs. Its relative differences are derived from the existing raw records.

Translation checks and the current TeX hyphenation limitation are documented in `TranslationNotes.uk.md`. The Ukrainian PDF was inspected on all 12 pages. Both versions compile with resolved references and no missing characters or overfull boxes.

## Torus previews (not included in the manuscripts)

From this directory, generate separate reference / PG grid / PG isolines comparisons:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ../../.venv/bin/python preview_torus.py
```

Outputs are PNG and PDF files in `previews/torus/`: a 3D surface and an `xz` cross-section at `y=0` for each grid spacing (`h=0.4`, `0.5`). The default is seed 10, zero offset, with a 65³ display grid and a 201² slice grid. In the slices, black dashed contours are the reference and blue contours are the displayed field. All panels share the same scale and 3D viewing angle. Empty model surfaces are explicitly labelled.

The generator reconstructs the frozen configurations from `selection.json`, verifies research source hashes and checks band RMSE against `holdout.json` at the archived resolution. Display resolution is independent of interpolation spacing. `manifest.json` records parameters, input hashes, metric checks and output names. No training is repeated; neither manuscript nor its figures are modified.

Optional arguments: `--seed 11`, `--h 0.4`, `--offsets -0.1 0 0.1`, `--resolution 81`, `--slice-resolution 301`, `--output /tmp/torus-preview`. Use a separate output directory for alternative settings to retain the default previews and their manifest.
