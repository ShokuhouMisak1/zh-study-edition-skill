# zh-study-edition (Claude skill)

把英文教材、课件 (slides / PPT / PDF 讲义) 改造成给中国学生用的 **“中文讲解 + 英文术语” 学习版讲义**：

- 叙述译成中文；专有名词、定理名、章节标题保留原文英文，方便对照原书、做作业；
- 原文讲得简略的地方加 “补充讲解” 方框 (数值例子用代码验证)，改正笔误并注明；
- AJbook LaTeX 模板 (XeLaTeX + latexmk)，编译成 PDF，放进 private GitHub 仓库。

流程提炼自 Jon Lee《A First Course in Linear Optimization》中文学习版项目。

## 目录

```
SKILL.md                 主流程
references/              写作规范、LaTeX 注意事项、多章并行、课件处理
scripts/                 new_project.py / extract_source.py / term_check.py / build_report.py
assets/template/         修好的 AJbook 模板 (字体可移植、xindy 索引可用)
```

## 安装

- Claude Code：把本目录复制到 `~/.claude/skills/zh-study-edition/` (个人) 或项目的 `.claude/skills/` 下。
- Claude 应用：导入打包好的 `zh-study-edition.skill`。

依赖：TeX Live (xelatex, biber, xindy, latexmk)、poppler (pdftotext, pdftoppm)、python3；处理 PPTX 时另需 LibreOffice 或 `python-pptx`。

## 用法示例

> 这是我这学期 EECS 551 的 slides (lecture1-5.pdf)，帮我做成中文讲义，术语保持英文，没讲清楚的地方给我详细解释一下。

## 许可

模板 (AJbook) 为李文威的作品，CC BY 4.0，见 `assets/template/LICENSE-template-CC-BY-4.0.txt`。
