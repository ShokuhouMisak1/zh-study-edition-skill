#!/usr/bin/env python3
"""Summarize a LaTeX build: errors, undefined references/citations, overfull boxes mapped to files.

Usage:
  python build_report.py <project_dir> [main]      # reads <main>.log (default main.log)

Run after `latexmk`. Overfull boxes are attributed to the chapter file that was open when the
warning was written (tracked from the '(./chapters/xxx.tex' markers in the log), which is what
you need to fix them — the raw log line numbers alone are ambiguous across \\include'd files.
Exit code 1 on errors or undefined references.
"""
import pathlib
import re
import subprocess
import sys


def main():
    proj = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    name = sys.argv[2] if len(sys.argv) > 2 else "main"
    log = (proj / f"{name}.log").read_text(encoding="utf-8", errors="replace").splitlines()
    cur, errs, undef, over = "main.tex", [], set(), []
    for i, line in enumerate(log):
        for m in re.finditer(r"\(\./([\w./-]+\.tex)", line):
            cur = m.group(1)
        if line.startswith("!") or re.match(r"^\./.*:\d+:", line):
            errs.append(" ".join(log[i:i + 3]))
        m = re.search(r"(Reference|Citation) [`'](.+?)' .*undefined", line)
        if m:
            undef.add(f"{m.group(1)} {m.group(2)}")
        m = re.match(r"Overfull \\([hv])box \(([\d.]+)pt too (wide|high)\)(.*)", line)
        if m:
            over.append((cur, float(m.group(2)), m.group(1), m.group(4).strip()))
    pdf = proj / f"{name}.pdf"
    pages = ""
    if pdf.exists():
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        pages = re.search(r"Pages:\s+(\d+)", out).group(1) if "Pages" in out else "?"
    print(f"pages: {pages}   errors: {len(errs)}   undefined: {len(undef)}   overfull: {len(over)}")
    for e in errs[:20]:
        print("  ERROR", e[:200])
    for u in sorted(undef):
        print("  UNDEF", u)
    for f, pt, kind, where in sorted(over, key=lambda x: -x[1]):
        flag = "  (visible, fix)" if pt > 5 else ""
        print(f"  OVERFULL {kind} {pt:6.2f}pt  {f}  {where}{flag}")
    sys.exit(1 if errs or undef else 0)


if __name__ == "__main__":
    main()
