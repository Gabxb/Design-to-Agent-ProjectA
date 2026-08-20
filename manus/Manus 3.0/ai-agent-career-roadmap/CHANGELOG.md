# Changelog

## 2026-08-20

### Added
- 初始化可本地保存的 AI Agent 学习系统、三套学习方案和 24 周路线图。
- 创建周计划、每日任务、知识库、项目定义、进度管理和自动化脚本。

### Changed
- 无。

### Fixed
- 无。

### Affected Files
- 根目录及所有初始化学习文件。

## 2026-08-20

### Added
- 新增 `INDEX.md`，提供按时间、能力、项目、动作和目录结构的总导航。
- 新增 `roadmap/LEARNING_OUTLINE.md`，以阶段、能力、项目与质量线梳理完整学习路线。
- 新增可编辑的 Mermaid 思维导图源文件和 PNG 总览图。

### Changed
- 更新 `README.md` 和 `START_HERE.md`，加入“先看整体、再进入当天任务”的导航路径。

### Fixed
- 无。

### Affected Files
- INDEX.md
- README.md
- START_HERE.md
- roadmap/LEARNING_OUTLINE.md
- roadmap/LEARNING_MINDMAP.md
- roadmap/LEARNING_MINDMAP.mmd
- roadmap/LEARNING_MINDMAP.png

## 2026-08-20

### Added
- 新增 `book/` 书籍式教程层，包含前言、目录、6 个分部导读、24 个章节导航和 4 组附录。
- 新增 `scripts/generate_book.py`，可在保留原始学习文件的前提下重建教程阅读层。

### Changed
- 更新 `INDEX.md`，将书籍教程作为连续学习的首要导航入口。

### Fixed
- 修正章节中 7 天每日任务的独立链接格式。

### Affected Files
- INDEX.md
- book/README.md
- book/00_PREFACE.md
- book/CONTENTS.md
- book/chapters/
- book/appendices/
- scripts/generate_book.py

## 2026-08-20

### Added
- 新增《从设计师到 AI Agent 开发工程师：24 周本地实战教程》的 70 个核心章节、最小可运行示例、前置页面和工具书附录。
- 新增 `overview/` 全局大纲、一页总览、学习地图、技术能力思维导图、24周路线图、项目成长图、岗位准备路径与六个阶段子图。
- 新增全书 Markdown、离线 HTML、正式 PDF、SVG/PNG 图示、三套方案路线图及项目架构/Agent 工作流图。
- 新增书籍生成、PDF、图示、链接、报告、方案与书籍进度维护脚本。

### Changed
- 更新根目录 README、START_HERE、每周计划与每日任务，建立书籍—周计划—每日执行—项目的相对导航。
- 将 `progress/progress.json` 扩展为包含当前篇章、章节与项目进度的书籍学习状态。

### Fixed
- 修正 Mermaid SVG 交付路径，保留 Mermaid 为可编辑主源并同步生成SVG/PNG阅读资产。

### Affected Files
- BOOK.md
- BOOK.html
- BOOK.pdf
- TABLE_OF_CONTENTS.md
- READING_GUIDE.md
- QUICK_REFERENCE.md
- overview/
- book/front-matter/
- book/part-01-foundations/ 至 book/part-08-career/
- book/appendix/
- book/examples/
- weeks/
- projects/
- plans/
- output/
- generate_book.py
- update_book.py
- scripts/
