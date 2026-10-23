# Feature Drift Detection via Adversarial Validation

**Master's Thesis**, Faculty of Information and Communication Technology, Mahidol University

**Author:** Nusrat Begum  
**Advisor:** Asst. Prof. Thanapon Noraset, Ph.D.  
**Co-Advisor:** Assoc. Prof. Suppawong Tuarob, Ph.D.

---

## Abstract

Unsupervised drift detectors can signal that the input distribution of a deployed model has changed, but D3 (Gözüaçık et al., 2019), a discriminative detector recommended by the benchmark of Lukats et al. (2024), relies on an uncalibrated AUC threshold, compares two short adjacent windows, and gives no indication of which features changed.

This thesis proposes **Enhanced Adversarial Drift Detection (EADD)**, an integrated framework that combines:

1. A **LightGBM classifier two-sample test** (C2ST) with a **reservoir-sampled reference window**
2. **Prediction entropy monitoring** ($H_{pred}$)
3. An **adaptive sequential permutation test (ASPT)** that confirms a clear drift after 20 of 199 permutations
4. A **TreeSHAP ranking** of the features behind each confirmed drift

An ablation with a LightGBM version of D3 shows that EADD's advantage on gradual and incremental drift comes from its long-memory reference window rather than from the classifier, and that the permutation test changes decisions only when the AUC threshold is lowered.

---

## Contributions

| Contribution | Description |
|--------------|-------------|
| **EADD framework** | Integrates LightGBM C2ST, reservoir-sampled reference window, $H_{pred}$, ASPT and TreeSHAP ranking |
| **ASPT** | Sequential Monte Carlo stopping (Gandy, 2009) for the C2ST permutation test; 90% fewer permutations for clear decisions |
| **Evaluation and ablation** | Seven unsupervised baselines on synthetic and 13 real-world streams; ablation separating classifier, window sizes, reference memory, threshold and permutation test |

---

## Methodology Overview

```
Input stream -> Step 1: reservoir-sampled W_ref, sliding W_cur
             -> Step 2: LightGBM C2ST (AUC, H_pred)
             -> AUC > tau ? -> Step 3: ASPT (p < alpha ?)
             -> Step 4: TreeSHAP feature ranking -> drift report
```

---

## Repository Structure

| File | Description |
|------|-------------|
| `main.tex` | Main LaTeX document (Thesis plan, Traditional Format) |
| `thesis.tex` | Thesis content (Chapters 1-6, as required by PR07284) |
| `abstract.tex` | English abstract |
| `acknowledgements.tex` | Acknowledgements |
| `abbreviations.tex` | List of abbreviations |
| `appendix_impl.tex` | Appendix: implementation details |
| `preamble.tex` | Candidate info, committee, keywords, biography |
| `references.bib` | Bibliography (BibTeX, `unsrtnat` style) |
| `muthesis2026.cls` | Mahidol University thesis class (2026 version) |
| `figures/` | Figures and diagrams |

Experiment code and results: [unsupervised-concept-drift-detection](https://github.com/NusratBegum/unsupervised-concept-drift-detection).

---

## Compilation

```bash
latexmk -pdf main.tex
```

Requires: TeX Live 2021+ with `latexmk`, `natbib`, `hyperref`, `tikz`, `pgfplots`

---

## Keywords

Drift Detection, Classifier Two-Sample Test, Permutation Test, Covariate Drift, MLOps

---

## Citation

```bibtex
@mastersthesis{Begum2026,
  author  = {Nusrat Begum},
  title   = {Feature Drift Detection via Adversarial Validation},
  school  = {Mahidol University},
  year    = {2026},
  type    = {Master's Thesis}
}
```

---

## License

**Copyright © 2026 Nusrat Begum.** Licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). See [LICENSE](LICENSE).

| Allowed | Not allowed |
|---|---|
| Share unmodified copy for non-commercial use, with attribution | Commercial use of any kind |
| Cite the thesis in academic work | Modification, translation, or derivative works |
| Personal scholarly reading | Removing attribution or this notice |

**Commercial licensing inquiries:** `nusrat.beg@student.mahidol.ac.th`

**Thesis template attribution:** The LaTeX template is based on the [Mahidol University Thesis Template](https://github.com/ICT-Mahidol/MahidolThesis) (2026 version, updated for FGS announcement PR07284). `muthesis2026.cls` retains its own licensing.

**Institutional note:** Student retains copyright under Mahidol FGS policy; the university holds a non-exclusive right to archive and distribute the thesis for academic purposes.
