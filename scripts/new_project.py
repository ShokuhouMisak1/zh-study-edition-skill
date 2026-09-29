#!/usr/bin/env python3
"""Scaffold a Chinese study-edition LaTeX project from the bundled AJbook template.

Usage:
  python new_project.py <target_dir> --zh-title "线性优化初步" --en-title "A First Course in Linear Optimization" \
      --author "Jon Lee" --citation "Jon Lee, A First Course in Linear Optimization, 4th ed., 2024" \
      [--edition ", 4th ed."] [--license "原文以 CC BY 3.0 协议发布."] \
      [--chapters "Let's Get Started" "Modeling" ...] [--terms "reduced cost, pivot, ratio test"]

Creates <target_dir> with main.tex, mysetup.tex, the AJbook files, latexmkrc, Makefile,
.gitignore, references.bib, chapters/ch00-front.tex and one stub chapters/chNN.tex per
--chapters entry (English original titles), and wires the \\include lines into main.tex.
Refuses to overwrite an existing non-empty directory.
"""
import argparse
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "template"


def tex_escape(s: str) -> str:
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")]:
        s = s.replace(a, b)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--zh-title", required=True)
    ap.add_argument("--en-title", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--citation", required=True, help="full citation of the source, one line")
    ap.add_argument("--edition", default="")
    ap.add_argument("--license", default="原文的版权归原作者所有; 本版仅供个人学习使用, 请勿公开传播.",
                    help="one Chinese sentence describing the source license")
    ap.add_argument("--chapters", nargs="*", default=[], help="original (English) chapter titles, in order")
    ap.add_argument("--terms", default="reduced cost、pivot", help="2-3 example English terms for the reading note")
    a = ap.parse_args()

    dst = pathlib.Path(a.target).expanduser().resolve()
    if dst.exists() and any(dst.iterdir()):
        sys.exit(f"refusing to overwrite non-empty directory: {dst}")
    shutil.copytree(TEMPLATE, dst, dirs_exist_ok=True)
    (dst / "gitignore").rename(dst / ".gitignore")

    subs = {
        "__ZH_TITLE__": a.zh_title,
        "__EN_TITLE__": tex_escape(a.en_title),
        "__AUTHOR__": tex_escape(a.author),
        "__SOURCE_CITATION__": tex_escape(a.citation),
        "__EDITION__": tex_escape(a.edition),
        "__LICENSE_SENTENCE__": a.license,
        "__TERM_EXAMPLES__": a.terms,
    }
    for p in [dst / "main.tex", dst / "chapters" / "ch00-front.tex"]:
        s = p.read_text(encoding="utf-8")
        for k, v in subs.items():
            s = s.replace(k, v)
        p.write_text(s, encoding="utf-8")

    stub = (dst / "chapters" / "ch01.tex").read_text(encoding="utf-8")
    (dst / "chapters" / "ch01.tex").unlink()
    titles = a.chapters or ["Chapter One"]
    includes = []
    for i, t in enumerate(titles, 1):
        name = f"ch{i:02d}"
        body = (stub.replace("__ORIGINAL_CHAPTER_TITLE__", tex_escape(t))
                    .replace("__ORIGINAL_SECTION_TITLE__", "Section title")
                    .replace("ch:1", f"ch:{i}").replace("sec:1.1", f"sec:{i}.1").replace("exo:1.1", f"exo:{i}.1"))
        (dst / "chapters" / f"{name}.tex").write_text(body, encoding="utf-8")
        includes.append(f"\t\\include{{chapters/{name}}}")
    m = (dst / "main.tex").read_text(encoding="utf-8")
    m = m.replace("\t\\include{chapters/ch01}\n\t% \\include{chapters/ch02} ...", "\n".join(includes))
    (dst / "main.tex").write_text(m, encoding="utf-8")
    print(f"created {dst} with {len(titles)} chapter stub(s)")


if __name__ == "__main__":
    main()
