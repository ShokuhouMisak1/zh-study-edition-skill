# LaTeX 与模板: 已知的坑和做法

模板是 AJbook 文档类 (李文威《代数学方法》, CC BY 4.0, 经 lichuang/latex-template)。`assets/template/` 里的版本已经修过下面前三个问题，直接用 `scripts/new_project.py` 生成项目即可。

## 已修复 (知道原因, 以免改坏)

1. **字体**：原版 `\setsansfont{TeX Gyre Heros}` 按字体名找，macOS / CI 上找不到 → 改为按文件名 `texgyreheros-*.otf` 载入。原版的定理名/标题用 Noto Sans CJK SC，未安装时 fontspec 报错 → 用 `\IfFontExistsTF` 自动退回 FandolHei (TeX Live 自带)。
2. **索引**：原版 `\usepackage[xindy, splitindex]{imakeidx}` + `program=truexindy`：`splitindex` 生成的 `.idx` 格式 xindy 读不了，得到**空索引**；`truexindy` 在 macOS 上不存在。→ 去掉 `splitindex`，`program=xindy`，并由 `latexmkrc` 的 `$makeindex` 调用 xindy (不需要 `-shell-escape`)。
3. **编译链**：用 `latexmk` (配置在 `latexmkrc`：xelatex + biber + xindy，自动重跑到交叉引用稳定)。`make` 即 `latexmk main.tex`。

## 常见问题

- **长英文节标题超宽**：titles-setup 的节标题放在一个方框里，英文长标题不会断行。可以用短标题 + 缩小词距：
  `\section[Long Original Title]{{\spaceskip=0.2em plus 0.02em\relax Long Original Title}}\label{sec:3.1}` (目录/页眉用短参数)。
- **定理可选参数太长超宽**：ntheorem 的标题是不可断的盒子。定理名只写原文英文名，不要 “中文名 (English name)”。
- **表格超宽**：`\small`，或调 `\setlength{\tabcolsep}{4pt}`，或把表头拆两行；长表用 `longtable` (mysetup 已载入)。
- **`\T` 宏**：mysetup 没定义转置宏；按原文写法 (如原文用 `'` 表示转置就定义 `\newcommand{\T}{^{\prime}}`)，在 mysetup 里统一定义。
- AJbook 注释里说 “如果文中未使用 `\cite` 和 `\index` 可能报错”：至少保留一个 `\index`；没有文献时 `\printbibliography` 只会给警告。

## 检查构建

```bash
latexmk main.tex            # 或 make
python <skill>/scripts/build_report.py .   # 错误 / 未定义引用 / 超宽 (按章节文件归类)
```

目标：0 错误、0 未定义引用、没有 > 5pt 的 Overfull。渲染几页看版面：

```bash
pdftoppm -r 40 -f 1 -l 40 -png main.pdf /tmp/pages/p   # 再拼成缩略图看整体 (PIL)
```

## 并行编译

多个 agent 同时改不同章节时，**不要在项目目录里同时编译** (会互相覆盖 .aux)。每人把项目 `cp -R` 到自己的临时目录，同步自己的文件，在 `main.tex` 加 `\includeonly{chapters/chNN}` 编两遍。跨章引用在 includeonly 下会显示未定义，最后统一全量编译时再查。

## 字体提示

- macOS 的 MacTeX 默认不把 TeX 字体注册到系统，按字体名找 TeX Gyre / Fandol 会失败，所以模板一律按文件名载入。
- 需要更好看的黑体：`brew install --cask font-noto-sans-cjk-sc` (装后自动启用)。
