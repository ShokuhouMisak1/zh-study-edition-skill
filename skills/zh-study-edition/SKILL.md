---
name: zh-study-edition
description: 把英文教材、课件 (slides/PPT/PDF 讲义)、lecture notes 改造成给中国学生用的“中文讲解 + 英文术语”学习版讲义 (AJbook LaTeX 模板, 编译成 PDF, 放进 private GitHub 仓库)。叙述译成中文, 专有名词/定理名/章节标题保留原文英文以便对照原书和做作业, 原文讲得简略的地方加“补充讲解”方框 (数值例子用代码验证), 改正笔误并注明。凡是用户想把英文课本/课件/讲义翻成中文、做中文版/中文讲义/中文笔记、“改造成中文教材”、帮同学或学生提高读英文教材的效率、或给英文课程材料写详细中文解释时, 都应使用本 skill, 即使用户没有提到 LaTeX 或模板。
---

# 英文教材/课件 → 中文学习版讲义

产出一份**能对照原文**、把原文没讲清楚的地方讲清楚的中文讲义：
- 叙述与讲解用中文；**术语、定理名、章节标题用原文英文** (学生的作业、考试、Piazza 都是英文词，中文译名反而对不上)。
- 原文完整翻译；新增讲解放在 “补充讲解” 方框 (`jiedu`) 或 “译注” (`\yizhu`) 里，与原作者的内容分开。
- AJbook 文档类 (XeLaTeX)，`latexmk` 编译成 PDF，放进用户的 **private** GitHub 仓库。

本 skill 只做这条核心流程。不做交互 demo 网站、Jupyter notebooks 或 CI，除非用户另外要求。

详细规范在 `references/` 里，按需阅读：
- `references/style-guide.md`：术语、结构、补充讲解、图、习题的写作规范。**动笔前必读**，并把路径发给每个子 agent。
- `references/latex-notes.md`：模板已修过的坑 (字体、索引)、超宽处理、并行编译。
- `references/parallel-work.md`：多章并行的分工方法、子 agent 任务说明模板、合并与统一检查。
- `references/slides.md`：输入是课件 (slides/PPT) 时的额外做法。

脚本在 `scripts/` (python3，需要 poppler 与 TeX Live)：`new_project.py` 生成项目骨架，`extract_source.py` 抽取原文，`term_check.py` 检查术语一致性，`build_report.py` 汇总编译问题。

## 流程

### 0. 弄清输入与范围

需要知道的 (能从上下文判断就不要问)：
- 原文文件在哪 (PDF / PPTX / LaTeX 源 / 网址)、哪些章节或哪几讲、用户在上哪门课。
- 仓库名 (默认按原文书名取一个短名，如 `linear-optimization-zh`)。

原文要从网上下载时，先告诉用户文件名、来源、大小，征得同意再下载；用完的临时下载文件按用户意愿删除。不要把受版权保护的原文 PDF/PPT 提交到仓库 (模板的 `.gitignore` 已忽略 `source/`)。

### 1. 查版权

在前言页如实写明原文的版权状态，并决定能不能公开：
- 开放许可 (如 CC BY)：可以改编；前言写明原作者、许可、所做改动 (模板的 ch00-front 已有这个结构)。原文中作者声明取自网络的图片通常不在许可范围内，不要收录。
- 没有开放许可 (大多数课件、商业教材)：只作个人/本课学习用，仓库保持 private，不要公开发布。前言用 `new_project.py` 默认的版权句子。
- 拿不准就按“没有开放许可”处理，并告诉用户。

### 2. 读原文、定术语表

```bash
python <skill>/scripts/extract_source.py <原文.pdf|.pptx> <工作目录>/src
```
得到逐页文本和一个大致目录 (outline.txt)。然后：
1. 定章节划分，以及 PDF 页码和书页的偏移。
2. **先定术语表**，再动笔，这是全书一致的关键。从原文的 index / 定义处 / 粗体词整理出核心术语，写成 `TERMS.tsv` (`中文\tEnglish`，中文列写常见译名，供 `term_check.py` 查漏改)，同时写一张“保留中文”的基础词表 (见 style-guide §1)。
3. 记下原文里每章最跳步、最难懂的几处，后面作为补充讲解的重点。

### 3. 生成项目骨架

```bash
python <skill>/scripts/new_project.py <仓库目录> --zh-title "<中文书名>" --en-title "<原书名>" \
  --author "<作者>" --citation "<完整引用>" [--edition ", 4th ed."] \
  [--license "<一句中文版权说明>"] --chapters "<原章标题1>" "<原章标题2>" ... --terms "reduced cost、pivot"
cd <仓库目录> && latexmk main.tex && python <skill>/scripts/build_report.py .
```
先确认空骨架能编译 (0 错误)，再开始写。按原文记号在 `mysetup.tex` 里补宏 (如原文用 `'` 表示转置，就加 `\newcommand{\T}{^{\prime}}`)。

### 4. 逐章翻译 + 补充讲解

按 `references/style-guide.md` 写。要点：
- 完整翻译，结构、标题、编号与原文一一对应；label 用原编号 (`thm:6.3`)。
- 原文跳步或讲得简略的地方，要尽可能讲细：补全证明步骤，给小的数值例子 (最好贯穿全章)，解释直觉和假设为什么需要。所有新增内容都放进 `jiedu` 或 `\yizhu`。
- 数值例子里的每个数都用 python (numpy/scipy/sympy) 算过；公式对照渲染的原文页面，不要只看抽取出来的文本。
- 原文笔误改正，并用 `\yizhu` 注明原文写法。
- 习题完整翻译，只给思路提示，不写完整解答。
- 图按原文数据重画 (图中文字用英文)；网络照片、漫画不收录，在原位置用译注说明。

超过 2–3 章时，按 `references/parallel-work.md` 用子 agent 并行，每章一个。主 agent 先准备好术语表、共享的 BRIEF.md 和每章的讲解重点；子 agent 在各自的副本里编译，不在项目目录里互相覆盖。

### 5. 合并、统一、检查

这一步不能省，并行写出来的东西一定有不一致：
```bash
latexmk main.tex && python <skill>/scripts/build_report.py .
python <skill>/scripts/term_check.py . TERMS.tsv --keep 矩阵,向量,约束,目标函数,...
```
- 目标是 0 错误、0 未定义引用，并修掉 > 5pt 的超宽。
- 逐条处理 `term_check` 的输出：有漏改的中文术语、英文写法不一致 (照原文统一)、索引项里的中文。报告的只是候选，要看上下文再判断。
- 标题统一 (习题节叫 `Exercises`)，合并各 agent 报告里的新术语和 bib 条目，更新前言的改动列表。
- 渲染一组缩略图 (`pdftoppm -r 40` + PIL 拼图) 看整体版面，并抽查几个补充讲解里的数字。

### 6. 提交到 private 仓库

```bash
git init -b main && git add -A && git commit -m "..."     # 提交作者用用户本机的 git 配置
gh repo create <owner>/<name> --private --source=. --remote=origin --push
```
- 编译好的 `main.pdf` 也提交，方便在 GitHub 上直接看。
- 按章提交 (一章一个 commit)，便于回看。
- 不要改写已推送的历史。
- 写 README：原文与许可、与原文的区别、翻译进度表、编译方法、常见中文译名对照表 (书里用英文，这张表只供查中文资料时对照)。

### 7. 交付

把 PDF 发给用户，并简短汇报：
- 仓库链接与页数；
- 编译状态；
- 每章补充了哪些讲解；
- 改正了哪些原文笔误；
- 省略了什么 (图片等) 以及原因；
- 还没做完的部分。

## 做得好的标准

- 学生拿着原书/原 slide，能在讲义里按标题和编号找到同一处，术语与原文逐字对得上。
- 原文最难懂的几处，讲义里都有补充讲解，而且讲解里的数字都算过、是对的。
- 读者分得清哪些是原作者写的、哪些是中文版加的。
- PDF 编译干净，版面没有溢出，索引是英文的，且内容不为空。
