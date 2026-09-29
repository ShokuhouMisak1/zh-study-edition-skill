# 课件 (slides) → 中文讲义

课件信息密度低、跳跃大、很多内容只在老师口头讲。直接逐页翻译没有用；目标是把它**展开成一份能自学的讲义**，同时能随时对回原 slide。

## 读取

- PDF 课件：`extract_source.py deck.pdf out/`，一页 = 一张 slide。
- PPT/PPTX：同一脚本，先用 LibreOffice 转 PDF (保留版面，便于看图和公式)；没有 LibreOffice 时退回 python-pptx 只取文字 (含演讲者备注 `[notes]`——备注往往是最有用的讲解)。
- 公式、图表必须看渲染页：`pdftoppm -r 110 -f N -l N -png deck.pdf /tmp/s`，再用 Read 看图。

## 结构

- 一个 lecture / 一份 deck → 一个 `\chapter{<原 lecture 标题>}`；deck 内按 slide 的标题分组成 `\section` / `\subsection` (相邻同标题或 “(cont.)” 的 slides 合并)。
- 多份 deck 属于同一门课时，一个项目、每个 lecture 一章；书名用课程名，前言写明课程代号与学期。
- 在每段对应内容末尾加 `\slideref{12}` (或 `\slideref{12--14}`)，方便学生上课时对照。

## 写法

- slide 上的 bullet 往往是半句话：写成完整的中文段落，把 bullet 之间的逻辑连起来 (“因为… 所以…”)。
- slide 上的每个公式/结论，补上推导或至少说明从哪来；slide 跳掉的例子计算过程补全 (放 jiedu，用代码验证数字)。
- slide 中的术语照样用英文；老师的记号 (变量名、上下标) 与 slide 完全一致。
- 仅是标题页、目录页、“Questions?”、纯图片页的 slide 不必成节，在前后文里提一句即可。
- 课件里的图：能重画的重画；截图类 (他人论文插图、网页截图) 只在 `\yizhu` 里说明 “见 slide N”。

## 版权

课件通常**没有开放许可**，是老师的课程材料。只做个人/本课学习用，仓库保持 private，不要公开发布、不要把原课件文件提交到仓库 (`.gitignore` 已忽略 `source/`)。前言的版权说明用默认句子 (“原文的版权归原作者所有; 本版仅供个人学习使用, 请勿公开传播”)。
