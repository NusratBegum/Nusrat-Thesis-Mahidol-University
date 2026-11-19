# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

LaTeX source of Nusrat Begum's M.Sc. thesis, "Feature Drift Detection Techniques via Adversarial Validation" (Mahidol University, advisor Asst. Prof. Thanapon Noraset). Working branch: `concept-drift-adversarial-thesis` (not `main`). The advisor reads the thesis in Overleaf, which is a separate git remote and must be synced after each push.

Overleaf sync: the Overleaf project (git bridge, branch `main`) has its own history with no commits in common with GitHub. Each sync is one snapshot commit on top of Overleaf `main` whose tree is this repo's HEAD without `CLAUDE.md`, message "Sync with GitHub <sha>: <summary>". Before syncing, check that Overleaf's tree still equals the last synced GitHub commit (no edits made in Overleaf). The git token is supplied by the user; never write it into a remote, file or commit.

## Commands

```bash
export PATH=/Library/TeX/texbin:$PATH
pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
grep -c "Overfull\|undefined\|^!" main.log        # must be 0
make && make check                                # the same, via the Makefile
```

`latexmk` is not installed locally. `main.pdf` is committed; rebuild it before committing text changes.

## Structure

- `main.tex` loads the class `muthesis2026.cls` (Mahidol template, FGS announcement PR07284) and inputs `preamble.tex` (names, committee, keywords), `abstract.tex`, `thesis.tex` (which inputs `chapters/ch1.tex` to `ch6.tex`, one file per chapter since 19 Nov 2026) and `appendix_impl.tex`. It also patches three template problems (lists of tables/figures, REFERENCES in the contents, `\inputrows`); keep those patches. Pseudocode uses `algorithm` + `algpseudocode`.
- Chapter 4 reports the final registered test of the code repo (`experiments/results_final/`); its tables are typed by hand from those CSV files and its figures are the vector PDFs made by `make_final_figures.py` (copied into `figures/`). Every number must match `docs/status/THESIS_FACTS_2026-11-19.md` in the workspace and the result files.
- `figures/tikz_*.tex` are the method diagrams (TikZ, vector); `figures/figure-1.png` and `temporal_drift_patterns.pdf` are the Chapter 2 concept figures.
- Numbers quoted in prose are typed by hand. After regenerating tables, check every number in the abstract, Ch 1 contributions and Ch 4-6 against the result files.

## Writing rules (from the advisor)

- Never "novel"/"novelty"; no em-dashes; avoid "explainability"; modest claims ("we propose").
- Findings as short paragraphs tied to a hypothesis, never numbered lists.
- Cite terms on first use; use "classifier two-sample test (C2ST)".
- Literature review groups methods and compares them, not one paper per paragraph.
- Long captions need a short form: `\caption[Short]{Long}`.
- Keep the proposal title. Hypotheses as approved by the advisor on 18 Nov 2026: H1 (slow drift; not worse on abrupt), H2 and H3 in the proposal's wording, H4 worded for TreeSHAP in any classifier-based detector (never "EADD" in H4). Limitations go at the end of the Discussion. Report outcomes honestly.
- International track: no Thai abstract or title needed.
