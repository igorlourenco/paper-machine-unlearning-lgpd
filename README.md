# Machine unlearning and the right to erasure (GDPR / LGPD)

Research repository for a position/review paper, written in Brazilian
Portuguese:

> **Da eliminação à indistinguibilidade: um padrão técnico-jurídico para o
> desaprendizado de máquina sob a LGPD e o RGPD**

Thesis: "deleting data from a model" should be read as making the data
subject's contribution indistinguishable from that of a model that never saw
it, judged against the adversary each law presupposes. The paper is centred
on Brazilian law (LGPD arts. 12, 16 and 18) and uses EU law (GDPR art. 17,
Recital 26, EDPB Opinion 28/2024, CJEU *EDPS v SRB* C-413/23 P) as the
comparative counterpoint. Target venues: Brazilian law journals / CONPEDI
(ABNT layout via abnTeX2); WICS/CSBC (SBC template) is the fallback.

This phase contains only the manuscript and supporting notes. There is no
experimental code yet (`experiments/` is a placeholder).

## Language policy

- Paper content, section titles, in-paper TODOs and everything under
  `notes/`: Brazilian Portuguese.
- Code, scripts, comments, config files, this README and commit messages:
  English.

## Layout

```
paper/            LaTeX manuscript
  main.tex        preamble + \input of sections (swap venue template here)
  sections/       one file per section (01-introducao ... 08-conclusao)
  references.bib  verified references only; "TODO: verificar" marks unchecked fields
  tables/         generated tables (crosswalk.tex is produced from notes/)
  templates/      how to migrate to the SBC or abnTeX2 template later
  .latexmkrc      latexmk config (pdflatex + biber, output in paper/build/)
notes/            reading notes, open questions, schedule (pt-BR)
  fichamentos/    one note per reference, from template.md
  crosswalk.csv   unlearning method families x legal remedies (source of truth)
scripts/          crosswalk_to_latex.py (stdlib only)
experiments/      reserved for the empirical follow-up; intentionally empty
.github/          CI: compiles the PDF on every push and uploads it as an artifact
```

## Building the PDF

Requirements: a TeX distribution with `latexmk`, `biber`, `biblatex-abnt`,
`abntex2` and Portuguese babel support, plus Python 3. BasicTeX on macOS
includes everything except `abntex2`; install it without sudo:

```sh
export PATH="/Library/TeX/texbin:$PATH"
tlmgr init-usertree && tlmgr --usermode install abntex2
```

On Linux, `texlive-full` (or the equivalent subset) has it all.

```sh
make pdf      # regenerate the crosswalk table, then compile -> paper/build/main.pdf
make watch    # same, but recompile on every save (latexmk -pvc)
make clean    # remove auxiliary files
make distclean# also remove paper/build/
```

The Makefile prepends `/Library/TeX/texbin` to `PATH` so BasicTeX works
without shell configuration.

## Regenerating the comparative table

`notes/crosswalk.csv` is the single source of truth. Rows are unlearning
method families, columns are legal remedies, cells are free text. After
editing it:

```sh
make tables   # writes paper/tables/crosswalk.tex
```

`make pdf` runs this automatically. The generated file is committed so the
paper also compiles without Python (e.g. on Overleaf); CI runs
`scripts/crosswalk_to_latex.py --check` and fails if the committed table is
stale. Never edit `paper/tables/crosswalk.tex` by hand.

## Licensing

Two licenses, split by directory (see `LICENSE`):

- **Paper text and notes** (`paper/`, `notes/`, `experiments/`, this README):
  all rights reserved for now. A public license will be chosen at
  publication time.
- **Tooling** (`scripts/`, `Makefile`, `paper/.latexmkrc`, `.github/`): MIT.
