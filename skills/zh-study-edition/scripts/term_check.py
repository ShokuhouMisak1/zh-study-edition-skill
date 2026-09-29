#!/usr/bin/env python3
"""Check terminology consistency across the chapter files.

Usage:
  python term_check.py <project_dir> <glossary.tsv> [--keep 矩阵,向量,...]

glossary.tsv: one term per line, "中文<TAB>English" (lines starting with # ignored).
Reports:
  1. leftover Chinese terms from the glossary still present in chapters/*.tex (file:line + context),
     skipping words in --keep and lines that are pure LaTeX comments;
  2. English spelling variants that differ only by case / hyphen / space / plural
     (e.g. "halfspace" vs "half-space", "simplex algorithm" vs "Simplex Algorithm"),
     so you can unify them to the source's spelling;
  3. \\index entries that still contain Chinese or '@' sort keys.
Exit code 1 if anything is reported. It only reports: fixing needs judgement (a Chinese word may
be ordinary usage in context, e.g. 基本 vs 基 = basis).
"""
import argparse
import collections
import pathlib
import re
import sys

CJK = re.compile(r"[\u4e00-\u9fff]")


def norm(t):
    t = t.lower().replace("-", "").replace(" ", "")
    return t[:-1] if t.endswith("s") else t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("glossary")
    ap.add_argument("--keep", default="")
    a = ap.parse_args()
    keep = {w for w in a.keep.split(",") if w}
    gl = []
    for line in pathlib.Path(a.glossary).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#") or "\t" not in line:
            continue
        zh, en = line.split("\t", 1)
        gl.append((zh.strip(), en.strip()))
    files = sorted(pathlib.Path(a.project, "chapters").glob("*.tex"))
    bad = 0

    print("== 1. leftover Chinese terms")
    zh_terms = sorted({z for z, _ in gl if z and z not in keep}, key=len, reverse=True)
    for f in files:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("%"):
                continue
            for z in zh_terms:
                if z in line:
                    i = line.index(z)
                    print(f"  {f.name}:{n}: [{z}] …{line[max(0, i - 25):i + len(z) + 25].strip()}…")
                    bad += 1
                    break

    print("== 2. English spelling variants")
    en_terms = {e for _, e in gl for e in re.split(r"\s*/\s*", e) if e}
    seen = collections.defaultdict(collections.Counter)
    text = "\n".join(f.read_text(encoding="utf-8") for f in files)
    for e in en_terms:
        words = re.split(r"[\s-]+", e)
        pat = r"\b" + r"[\s-]*".join(map(re.escape, words)) + r"s?\b"
        for m in re.finditer(pat, text, re.I):
            seen[norm(e)][m.group(0)] += 1
    for k, c in sorted(seen.items()):
        # ignore plural -s and a capital first letter (sentence start); flag the rest
        forms = {(f[:-1] if f.endswith("s") and f[:-1] in c else f) for f in c}
        forms = {f[0].lower() + f[1:] for f in forms}
        if len(forms) > 1:  # differ in inner case, hyphen or spacing
            print("  " + ", ".join(f"{f!r}x{n}" for f, n in c.most_common()))
            bad += 1

    print("== 3. index entries with Chinese or @ keys")
    for f in files:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in re.finditer(r"\\index\{([^}]*)\}", line):
                if CJK.search(m.group(1)) or "@" in m.group(1):
                    print(f"  {f.name}:{n}: {m.group(0)}")
                    bad += 1
    print(f"-- {bad} item(s) to review")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
