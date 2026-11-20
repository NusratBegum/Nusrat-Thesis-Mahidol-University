# Build the thesis: make, make check, make clean
TEX = pdflatex -interaction=nonstopmode -halt-on-error
export PATH := /Library/TeX/texbin:$(PATH)

main.pdf: main.tex preamble.tex thesis.tex chapters/*.tex abstract.tex acknowledgements.tex abbreviations.tex appendix_impl.tex references.bib muthesis2026.cls figures/*
	$(TEX) main.tex >/dev/null
	bibtex main >/dev/null
	$(TEX) main.tex >/dev/null
	$(TEX) main.tex >/dev/null

check: main.pdf
	@n=$$(grep -c "Overfull\|undefined\|^!" main.log); echo "problems: $$n"; test $$n -eq 0

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.synctex.gz chapters/*.aux

.PHONY: check clean
