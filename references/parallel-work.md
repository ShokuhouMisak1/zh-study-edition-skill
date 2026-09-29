# 多章并行: 分工、任务说明模板、合并

一章教材 (15–30 页) 的翻译 + 补充讲解大约是一个子 agent 的合理工作量。超过 2–3 章时，用 Agent 工具并行：每个 agent 负责一章 (特别长的章拆成两半，后半写到 `chNN-part2.tex`，由前半的文件末尾 `\input` 引入)。

## 分工前先准备好 (主 agent 做)

1. **项目骨架**已生成并能编译 (`new_project.py` + 空章节)。
2. **术语表** `TERMS.tsv` (中文\tEnglish) + “保留中文” 列表：从原文的 index / 定义 / 粗体词整理核心术语 (几十到上百条)，写进一个共享的说明文件。所有 agent 必须照用，全书才一致。表外的新术语由各 agent 查原文决定，并在报告里列出。
3. **原文文本**：`extract_source.py` 的输出 (full.txt / pages/)，以及原文 PDF 路径和 “PDF 页码 = 书页 + 偏移”。
4. **一个共享的任务说明文件** (BRIEF.md)，内容按下面模板。

## BRIEF.md 模板 (按项目填写)

```
# 任务说明 (所有子任务共用)
项目: <原文完整引用> 的中文学习版 (AJbook LaTeX, XeLaTeX)。已完成: <…>
路径: 项目 PROJ=<绝对路径>; 原文 PDF=<路径> (PDF 页 = 书页 + <偏移>); 原文文本=<full.txt 路径>
先读: PROJ/mysetup.tex (jiedu, \yizhu, \slideref, 宏), 已完成的章节 (学风格), <skill>/references/style-guide.md (全部规范)
术语: 核心对照表 <TERMS.tsv 路径> 必须照用; 保留中文: <列表>
Label: 原文带编号的条目用原编号: thm:6.3, lem:7.7, cor:8.19, ex:8.14 (Example), exo:6.3 (Exercise), sec:8.4, fig:7.1
       已有 label: <grep -oh '\\label{[^}]*}' PROJ/chapters/*.tex 的结果或说明>
图: 前缀 fig<章号>, 放 PROJ/figures/, 绘图脚本也放那里; 网络照片/漫画不收录
只改: 你负责的文件与 figures/<前缀>*; 不改 main.tex/mysetup.tex/references.bib/其他章节; 不运行 git; 需要新宏包或 bib 条目写在报告里
编译: cp -R PROJ 到 <scratch>/build-<前缀>, \includeonly 你的章节, xelatex 两遍, 0 错误, 你的部分无未定义引用, 无明显 Overfull; 渲染几页看版面
报告 (简短, 中文): 翻译范围; 补充讲解要点 (每条一句); 改正的笔误; 省略了什么; 表外新术语 (中文→English); 需合并的 bib/宏包; 遗留问题
```

每个 agent 的 prompt 只需：“先完整阅读 BRIEF.md 并严格遵守。你负责: <章节/页码范围/文本行号范围>, 文件 <chNN.tex>, 图片前缀 <figNN>。补充讲解重点建议: <这一章原文最跳步/最难懂的 3–5 处>”。给出 “重点建议” 能明显提高讲解质量——主 agent 先快速读一遍原文目录和难点再写。

## 合并与统一 (主 agent 做, 不要省)

1. 全量编译 + `build_report.py`：0 错误、0 未定义引用；修掉 > 5pt 的 Overfull。
2. `term_check.py PROJ TERMS.tsv --keep <保留列表>`：
   - 漏改的中文术语 (逐条看上下文，很多是普通用法)；
   - 英文写法不一致 (half-space / halfspace, Simplex Algorithm / simplex algorithm)：统一成原文写法 (数一下原文里哪种多)；
   - 索引项里的中文和 `@` 键。
3. 标题统一：`grep -ohE '\\(chapter|section)\{[^}]*\}' chapters/*.tex`，习题节都叫 `Exercises`。
4. 合并各 agent 报告里的新术语、bib 条目、宏包需求。
5. 更新前言的 “所作的改动” 列表 (新增了哪些图、省略了什么)。
6. 渲染缩略图整体看一遍版面 (空白页、方框溢出、图太大)。
7. 抽查：随机挑几个补充讲解里的数字，自己用代码再算一遍。
