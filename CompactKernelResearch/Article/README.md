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
