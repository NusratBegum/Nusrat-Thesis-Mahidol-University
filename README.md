# Enhanced Adversarial Drift Detection for MLOps Feature Monitoring

**Master's Thesis**, Faculty of Information and Communication Technology, Mahidol University

**Author:** Nusrat Begum  
**Advisor:** Asst. Prof. Thanapon Noraset, Ph.D.  
**Co-Advisors:** Asst. Prof. Akara Supratak, Ph.D.; Asst. Prof. Siripen Pongpaichet, Ph.D.

**Defense:** 8 December 2026, 10:00-12:00  
**Status (19 Nov 2026):** full draft rewritten around the final registered test and submitted to the advisor; advisor review on 23 Nov 2026.

---

## Abstract

This thesis studies adversarial validation, the classifier two-sample test (C2ST), for unsupervised feature drift detection in data streams and proposes the **Explainable Adversarial Drift Detector (EADD)**: a LightGBM C2ST with a reservoir-sampled reference window, a permutation test whose null distribution comes from earlier windows of the same stream, an adaptive sequential permutation test (ASPT) that stops early when the evidence is clear, and a TreeSHAP ranking of the features behind each alarm.

EADD is compared with D3 and with D3 using the same LightGBM classifier (D3-LightGBM) in an identical setup (windows 500/200, AUC threshold 0.7, 5-fold cross-validation, a check every 50 samples), on 35 synthetic, injected-drift real and no-drift streams, with every test registered before its runs and run on fresh seeds. In the final test, EADD finds every slow (gradual or incremental) drift point where D3-LightGBM finds about half (recall 1.00 vs 0.53) and is not slower on abrupt drift (H1); it raises about 3.5 times fewer false alarms on autocorrelated streams without drift (H2); ASPT gives the same recall, delay and false alarms as the full permutation test with a third of the permutations (H3); and TreeSHAP attribution names the drifting feature in 98% of detections (H4). Newer online detectors (MMD-Online, LSDD-Online) detect faster but raise about five times more false alarms.

Code, raw runs and the registered plans: [unsupervised-concept-drift-detection](https://github.com/NusratBegum/unsupervised-concept-drift-detection).

---

## Where each result comes from

| Thesis part | Source |
|---|---|
| Chapter 4 tables and figures | `experiments/results_final/` (final registered test, seeds 3000-3009) and `experiments/results_confirm/` in the code repository |
| Registered plans (hypotheses, tests, decision rules) | `experiments/results_confirm/PREREGISTRATION.md` in the code repository |
| Every number in the text | must match the result files; checked by an independent review before each submission |

---

## Repository Structure

| File | Description |
|------|-------------|
| `main.tex` | Main LaTeX document (Thesis plan, Traditional Format) |
| `thesis.tex`, `chapters/ch1.tex`-`ch6.tex` | Thesis content: `thesis.tex` inputs one file per chapter (Chapters 1-6, as required by PR07284) |
| `abstract.tex` | English abstract |
| `acknowledgements.tex` | Acknowledgements |
| `abbreviations.tex` | List of abbreviations |
| `appendix_impl.tex` | Appendix: implementation details |
| `preamble.tex` | Candidate info, committee, keywords, biography |
| `references.bib` | Bibliography (BibTeX, `unsrtnat` style) |
| `muthesis2026.cls` | Mahidol University thesis class (2026 version) |
| `figures/` | Vector figures: `fig_*.pdf` (Chapter 4, made by `make_final_figures.py` in the code repository from `experiments/results_final/`), `tikz_*.tex` (method diagrams, Chapter 3) |
| `main.pdf` | Compiled thesis (rebuilt before each commit) |
| `Makefile` | `make` builds `main.pdf`; `make check` fails on errors, overfull boxes or undefined references; `make clean` removes build files |
| `CITATION.cff` | Citation metadata |

Experiment code and results: [unsupervised-concept-drift-detection](https://github.com/NusratBegum/unsupervised-concept-drift-detection).

---

## Compilation

```bash
make          # pdflatex, bibtex, pdflatex x2 -> main.pdf
make check    # 0 errors, 0 overfull boxes, 0 undefined references required
```

Requires: TeX Live 2021+ with `natbib`, `hyperref`, `tikz`, `pgfplots`. On Overleaf, `main.tex` is the main document.

---

## Keywords

Feature Drift Detection, Adversarial Validation, Classifier Two-Sample Test, Permutation Test, Data Streams

---

## Citation

```bibtex
@mastersthesis{Begum2026,
  author  = {Nusrat Begum},
  title   = {Enhanced Adversarial Drift Detection for {MLOps} Feature Monitoring},
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
