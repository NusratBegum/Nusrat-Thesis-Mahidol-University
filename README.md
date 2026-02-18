# Feature Drift Detection via Adversarial Validation

**Master's Thesis** — Faculty of Information and Communication Technology, Mahidol University

**Author:** Nusrat Begum  
**Advisor:** Asst. Prof. Thanapon Noraset, Ph.D.  
**Co-Advisor:** Assoc. Prof. Suppawong Tuarob, Ph.D.

---

## Abstract

Machine learning models in production suffer from "silent failure" when input feature distributions change over time (feature drift). While discriminative methods like D3 (Gözüaçık et al., 2019) can accurately detect drift, they function as "black boxes"—signaling *that* drift occurred without explaining *which* features drifted.

This thesis proposes **Explainable Adversarial Drift Detection (EADD)**, a novel framework that extends adversarial validation with:

1. **Permutation Testing** for statistically principled drift confirmation (p < 0.01)
2. **SHAP-based Root Cause Analysis** identifying which specific features drove the drift
3. **Automated Prescriptions** providing actionable MLOps recommendations

EADD transforms drift detection from a simple alarm into an intelligent diagnostic tool.

---

## Key Contributions

| Contribution | Description |
|--------------|-------------|
| **EADD Framework** | Extends D3 with explainability layer using LightGBM + SHAP |
| **Root Cause Analysis** | Ranks features by drift contribution (e.g., "Age: 45%, Income: 25%") |
| **Permutation Test** | Solves threshold calibration problem cited in Lukats et al. (2025) |
| **Automated Prescriptions** | Maps drift patterns to MLOps actions (univariate → drop feature; multivariate → full retrain) |

---

## Methodology Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Step 1:       │     │   Step 2:       │     │   Step 3:       │
│   Windowing     │────▶│   Adversarial   │────▶│   Permutation   │
│   (Reservoir)   │     │   Validation    │     │   Test          │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   Step 4:       │
                                               │   SHAP Feature  │
                                               │   Attribution   │
                                               └─────────────────┘
```

---

## Repository Structure

| File | Description |
|------|-------------|
| `main.tex` | Main LaTeX document (compiles everything) |
| `thesis.tex` | Thesis content (Chapters 1-5) |
| `abstract.tex` | English abstract |
| `preamble.tex` | Candidate info, committee, keywords |
| `references.bib` | Bibliography (BibTeX) |
| `muthesis2021.cls` | Mahidol University thesis class |
| `figures/` | Figures and diagrams |

---

## Compilation

```bash
latexmk -pdf main.tex
```

Requires: TeX Live 2021+ with `latexmk`, `natbib`, `hyperref`

---

## Keywords

Drift Detection, Adversarial Validation, Feature Drift, SHAP, MLOps, Covariate Shift, Streaming Data

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

This thesis template is based on the [Mahidol University Thesis Template](https://github.com/ICT-Mahidol/MahidolThesis) (2021 version).
