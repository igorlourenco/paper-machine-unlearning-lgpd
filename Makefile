# Build entry points. Requires a TeX distribution with latexmk + biber
# (BasicTeX on macOS is enough) and Python 3.
PAPER_DIR := paper
MAIN      := main
PDF       := $(PAPER_DIR)/build/$(MAIN).pdf
CSV       := notes/crosswalk.csv
TABLE     := $(PAPER_DIR)/tables/crosswalk.tex
PYTHON    ?= python3

# macOS BasicTeX installs outside the default PATH.
export PATH := /Library/TeX/texbin:$(PATH)

.PHONY: pdf tables check-tables watch clean distclean

pdf: tables
	cd $(PAPER_DIR) && latexmk -pdf $(MAIN).tex

tables: $(TABLE)

$(TABLE): $(CSV) scripts/crosswalk_to_latex.py
	$(PYTHON) scripts/crosswalk_to_latex.py --csv $(CSV) --out $(TABLE)

check-tables:
	$(PYTHON) scripts/crosswalk_to_latex.py --csv $(CSV) --out $(TABLE) --check

watch: tables
	cd $(PAPER_DIR) && latexmk -pdf -pvc $(MAIN).tex

clean:
	cd $(PAPER_DIR) && latexmk -c $(MAIN).tex

distclean:
	cd $(PAPER_DIR) && latexmk -C $(MAIN).tex
	rm -rf $(PAPER_DIR)/build
