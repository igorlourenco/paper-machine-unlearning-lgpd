#!/usr/bin/env python3
"""Convert notes/crosswalk.csv into a LaTeX table at paper/tables/crosswalk.tex.

The CSV is the single source of truth for the comparative table in the
paper. Run this script (or `make tables`) after editing the CSV so the
paper always reflects the notes. Standard library only.

CSV layout:
  - first row: header; first cell is the row-label column title, remaining
    cells are legal remedies (table columns).
  - following rows: first cell is an unlearning method family, remaining
    cells are free text (may be empty).

Usage:
  python3 scripts/crosswalk_to_latex.py [--csv PATH] [--out PATH] [--check]

With --check the script exits non-zero if the output file is missing or
differs from what would be generated (used by CI to keep the table in sync).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "notes" / "crosswalk.csv"
DEFAULT_OUT = ROOT / "paper" / "tables" / "crosswalk.tex"

# Characters that are special in LaTeX text mode, in replacement order.
_LATEX_ESCAPES = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]


def escape(text: str) -> str:
    """Escape LaTeX special characters in a plain-text cell."""
    for raw, replacement in _LATEX_ESCAPES:
        text = text.replace(raw, replacement)
    return text


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = [row for row in csv.reader(fh)]
    if not rows:
        raise SystemExit(f"{path}: CSV is empty")
    header, body = rows[0], rows[1:]
    width = len(header)
    if width < 2:
        raise SystemExit(f"{path}: need at least one remedy column")
    # Pad or trim rows so the table stays rectangular even with sloppy CSV.
    body = [(row + [""] * width)[:width] for row in body if any(c.strip() for c in row)]
    return [h.strip() for h in header], [[c.strip() for c in row] for row in body]


def render(header: list[str], body: list[list[str]]) -> str:
    n_remedies = len(header) - 1
    colspec = ">{\\raggedright\\arraybackslash}p{3cm}" + "X" * n_remedies
    lines = [
        "% GENERATED FILE - do not edit by hand.",
        "% Source: notes/crosswalk.csv  Generator: scripts/crosswalk_to_latex.py",
        "\\begin{table}[htbp]",
        "  \\centering",
        "  \\small",
        "  \\caption{Quadro comparativo entre famílias de métodos de desaprendizado e remédios jurídicos}",
        "  \\label{tab:crosswalk}",
        f"  \\begin{{tabularx}}{{\\textwidth}}{{{colspec}}}",
        "    \\toprule",
        "    " + " & ".join(f"\\textbf{{{escape(h)}}}" for h in header) + " \\\\",
        "    \\midrule",
    ]
    for row in body:
        label, cells = row[0], row[1:]
        # Empty cells are rendered empty on purpose so the draft PDF shows
        # what is still missing in the notes.
        lines.append("    " + " & ".join([f"\\textbf{{{escape(label)}}}"] + [escape(c) for c in cells]) + " \\\\")
    lines += [
        "    \\bottomrule",
        "  \\end{tabularx}",
        "\\end{table}",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true", help="verify output is up to date; do not write")
    args = parser.parse_args(argv)

    header, body = read_csv(args.csv)
    output = render(header, body)

    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.exists() else None
        if current != output:
            print(f"{args.out} is out of date; run `make tables`", file=sys.stderr)
            return 1
        print(f"{args.out} is up to date")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    print(f"wrote {args.out} ({len(body)} rows x {len(header) - 1} remedies)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
