# latexmk configuration for the paper. Run from the paper/ directory
# (the Makefile does this for you).
$pdf_mode = 1;              # pdflatex
$bibtex_use = 2;            # run biber and allow cleanup of .bbl
$biber = 'biber %O %S';
$out_dir = 'build';
$aux_dir = 'build';
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 %O %S';
$clean_ext = 'synctex.gz run.xml bbl bcf blg nav snm xdv %R-blx.bib';
