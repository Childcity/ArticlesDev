# Literature verification

Checked on 15 November 2026 using only the Codex built-in browser for online research. The user-specified Word predecessor on G: was read directly, without modification. Its progression from sampled fields to learned representations, RBF reconstruction and Gaussian interpolation informed the new review. This is a focused narrative review, not a systematic search or an exhaustive novelty assessment.

All 12 entries are cited in `main.tex`. The `unsrt` style numbers them by first citation. The requested 2020 and 2022 studies appear last as references 11 and 12. Linked bibliography notes make source links visible because `unsrt` does not print the `doi` and `url` fields itself.

| No. / key | Browser verification | Use in review |
| --- | --- | --- |
| 1 / frisken2000 | [ACM](https://dl.acm.org/doi/10.1145/344779.344899): four authors, title, 2000, pp. 249–254, DOI and abstract. Replaced the generic MERL author-search link with the specific publication record. | Adaptively sampled distance fields and operations including offsets. |
| 2 / sommer2022 | [CVF](https://openaccess.thecvf.com/content/CVPR2022/html/Sommer_Gradient-SDF_A_Semi-Implicit_Surface_Representation_for_3D_Reconstruction_CVPR_2022_paper.html): authors, CVPR 2022, pp. 6280–6289 and abstract. | Signed distances and gradients stored together at voxels. |
| 3 / li2024 | [IEEE](https://ieeexplore.ieee.org/document/9969571): six authors, expanded abstract and metadata; volume 30, issue 3, March 2024, pp. 1743–1755; online publication 2 December 2022. | Sparse voxels with learned geometry and appearance; removal of empty voxels during training. |
| 4 / park2019 | [CVF](https://openaccess.thecvf.com/content_CVPR_2019/html/Park_DeepSDF_Learning_Continuous_Signed_Distance_Functions_for_Shape_Representation_CVPR_2019_paper.html) and [author preprint](https://arxiv.org/abs/1901.05103): authors, abstract, CVPR 2019, pp. 165–174. | Continuous learned SDF representation of a shape class; context, not a tested baseline. |
| 5 / mo2022 | [Bentham](https://www.eurekaselect.com/article/116518): Jiahui Mo, Huahao Shou and Wei Chen; volume 16, issue 5, 2022, article e070721194551, 18 pages; online publication 7 July 2021; DOI and abstract. | Review of 125 articles on RBF/HRBF reconstruction, including global and compact support. |
| 6 / majdisova2017 | [Author-deposited arXiv record](https://arxiv.org/abs/1806.07705): authors, abstract, journal reference (2017, volume 51, pp. 728–743), journal DOI. ScienceDirect presented a CAPTCHA, which was not completed. | RBF approximation, accuracy, stability and memory. |
| 7 / macedo2009 | [IEEE](https://ieeexplore.ieee.org/document/5395267): authors, conference, year, DOI and expanded abstract. The pp. 1–8 range is also in the 2025 publisher's reference list. | Hermite interpolation of scattered points and normals. |
| 8 / wendland1995 | [Springer](https://link.springer.com/article/10.1007/BF02123482): author, 1995, volume 4, pp. 389–396, DOI and abstract. | Positive definite compact radial functions of minimal polynomial degree for specified dimension and smoothness. Their guarantees are not attributed to the pseudo-Gaussian kernel. |
| 9 / felzenszwalb2012 | [Author's Brown University page](https://cs.brown.edu/people/pfelzens/dt/index.html): title, authors, volume 8, article 19, September 2012, paper/code links. [Crossref deposit](https://api.crossref.org/works/10.4086/toc.2012.v008a019) confirms authors, year, volume, pp. 415–428 and DOI. Its title is empty and issue is 1, so the author's explicit article number 19 is retained. Journal DOI destination timed out. | Context for the sampled-grid distance transform comparator, not validation of this manuscript's cubic-plus-EDT pipeline. |
| 10 / kaleniuk2025 | [Publisher](https://ric.zp.edu.ua/article/view/324222): five authors, abstract, 2025 issue 1, pp. 30–37, DOI. The supplied Word manuscript's construction, examples and discussion were also read. | Direct antecedent: regular centers, movable fitting points, compact coefficients, successful examples and failure cases. |
| 11 / sydorenko2020 | [Publisher-deposited Crossref record](https://api.crossref.org/works/10.15407/csc.2020.06.021): personal authors, title, December 2020, issue 6 (290), pp. 21–28, DOI, abstract. Affiliation organizations interleaved in the deposit's author array were excluded. Journal-site access was unavailable. | Selection of the variable Gaussian-interpolation parameter on elementary functions. |
| 12 / sydorenko2022 | [Publisher-deposited Crossref record](https://api.crossref.org/works/10.15407/csc.2022.03.003): four personal authors, title, 2022, issue 3 (299), pp. **3–10**, DOI, abstract. Affiliation organizations interleaved in the author array were excluded. Journal HTTP page failed; HTTPS reported an expired certificate, which was not bypassed. | Gaussian interpolation of spiral-like curves, interpolation steps and nonuniform data. |

## Metadata corrections

- The 2022 spiral-curves paper has pp. **3–10** in its publisher's Crossref deposit, rather than the supplied and predecessor's **1–10**. The manuscript uses the deposited range.
- Mo, Shou and Chen are the family names; the predecessor inverted name components. The current publisher displays an article identifier, used here instead of the unconfirmed pp. 49–66 range.
- Vox-Surf is cited by its 2024 journal issue, while retaining the DOI containing 2022.
- The required 2025 entry retains all five authors and the requested key `kaleniuk2025`; prose attribution uses its first author, Ausheva.

Bibliographic and abstract checks do not mean every full paper was read. Technical descriptions are restricted to the accessible primary records and supplied predecessor. Connections to the present benchmark are the review's synthesis. No experimental results or benchmark implementation were changed.

## Local validation

The English manuscript was built with XeLaTeX, BibTeX and two further XeLaTeX passes. All 12 citations resolve; references 11 and 12 are the requested 2020 and 2022 papers. The 13-page PDF was rendered for visual inspection, with the literature-review and bibliography pages also inspected individually. There are no overfull/underfull boxes, missing-character warnings or unresolved references. The existing missing-author warning remains. BibTeX reports number-without-volume warnings for the three issue-numbered Ukrainian journals; no volume was invented to suppress them. The pre-existing modified PDF was copied to a temporary backup before rebuilding.
