#!/usr/bin/env python3
"""Build BOOK.md and offline HTML from canonical book chapter Markdown files."""
from __future__ import annotations

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/book"

PARTS = [
    (1, "foundations", range(1, 5)),
    (2, "software-engineering", range(5, 14)),
    (3, "llm-applications", range(14, 22)),
    (4, "rag", range(22, 33)),
    (5, "agent-workflows", range(33, 44)),
    (6, "production", range(44, 55)),
    (7, "projects", range(55, 61)),
    (8, "career", range(61, 71)),
]


def chapter_path(number: int) -> Path:
    for part_number, dirname, numbers in PARTS:
        if number in numbers:
            candidates = list((ROOT / f"book/part-{part_number:02d}-{dirname}").glob(f"chapter-{number:02d}-*.md"))
            if len(candidates) != 1:
                raise FileNotFoundError(f"Expected exactly one chapter file for chapter {number}: {candidates}")
            return candidates[0]
    raise ValueError(f"Unknown chapter: {number}")


def rebase_for_book(source: str, chapter_dir: Path | None = None) -> str:
    """Rebase canonical chapter links to the repository-root BOOK.md location."""
    source = source.replace("](../../", "](")
    if chapter_dir is not None:
        relative_dir = chapter_dir.relative_to(ROOT).as_posix()
        source = source.replace("](README.md)", f"]({relative_dir}/README.md)")
        source = source.replace("](chapter-", f"]({relative_dir}/chapter-")
    return source


def assemble() -> str:
    blocks = [
        "# 从设计师到 AI Agent 开发工程师：24 周本地实战教程",
        "",
        "> 本书由 `scripts/build_book.py` 从 `book/` 中的章节源文件自动合并。请修改章节源文件，不要手动修改本文件。",
        "",
    ]
    for filename in ("book-title.md", "copyright.md", "preface.md"):
        blocks.append((ROOT / "book/front-matter" / filename).read_text(encoding="utf-8").strip())
    blocks.append((ROOT / "TABLE_OF_CONTENTS.md").read_text(encoding="utf-8").strip())
    blocks.append("""<section class=\"map-section\">\n<h1>全局学习地图</h1>\n<img src=\"overview/LEARNING_MAP.png\" alt=\"全局学习地图\">\n<p>这张图展示从设计师背景到 AI Agent 开发岗位的阶段依赖、项目里程碑与交付顺序。</p>\n</section>\n\n<section class=\"map-section\">\n<h1>技术能力思维导图</h1>\n<img src=\"overview/TECH_SKILL_MINDMAP.png\" alt=\"技术能力思维导图\">\n</section>\n\n<section class=\"map-section map-page\">\n<h1>24 周路线图</h1>\n<img src=\"overview/ROADMAP_24_WEEKS.png\" alt=\"24 周路线图\">\n</section>\n\n<section class=\"map-section map-page\">\n<h1>项目成长地图</h1>\n<img src=\"overview/PROJECT_MAP.png\" alt=\"项目成长地图\">\n</section>\n""")
    for _, dirname, chapter_range in PARTS:
        readme = ROOT / f"book/part-{PARTS[[p[1] for p in PARTS].index(dirname)][0]:02d}-{dirname}/README.md"
        blocks.append(rebase_for_book(readme.read_text(encoding="utf-8").strip(), readme.parent))
        for number in chapter_range:
            path = chapter_path(number)
            blocks.append(rebase_for_book(path.read_text(encoding="utf-8").strip(), path.parent))
    blocks.append("# 附录")
    for appendix in sorted((ROOT / "book/appendix").glob("*.md")):
        blocks.append(rebase_for_book(appendix.read_text(encoding="utf-8").strip(), appendix.parent))
    return "\n\n".join(blocks) + "\n"


def rebase_for_output(source: str) -> str:
    return re.sub(r"\]\((?!https?://|#|mailto:|data:)([^)]+)\)", r"](../../\1)", source)


def html_document(source: str, base_href: str = "") -> str:
    body = markdown.markdown(source, extensions=["extra", "toc", "tables", "fenced_code", "sane_lists"])
    base = f'<base href="{base_href}">' if base_href else ""
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
<meta charset=\"utf-8\">
{base}
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>从设计师到 AI Agent 开发工程师：24 周本地实战教程</title>
<style>
:root {{ color-scheme: light; }}
body {{ max-width: 960px; margin: 0 auto; padding: 40px 24px 80px; font-family: -apple-system, BlinkMacSystemFont, "Noto Sans CJK SC", "Microsoft YaHei", sans-serif; color: #16202A; line-height: 1.8; }}
h1 {{ color: #102A43; margin-top: 3.2rem; border-bottom: 3px solid #2F80ED; padding-bottom: .5rem; }}
h2 {{ color: #1F4E79; margin-top: 2.3rem; }}
h3 {{ color: #386A8A; margin-top: 1.7rem; }}
a {{ color: #1769AA; }}
table {{ border-collapse: collapse; width: 100%; margin: 1.2rem 0; display: block; overflow-x: auto; }}
th, td {{ border: 1px solid #D8E2EA; padding: .55rem .7rem; text-align: left; vertical-align: top; }}
th {{ background: #EEF5FB; }}
pre {{ background: #102A43; color: #E9F4FF; padding: 16px; overflow-x: auto; border-radius: 8px; }}
code {{ font-family: "SFMono-Regular", Consolas, monospace; }}
blockquote {{ border-left: 4px solid #2F80ED; padding: .2rem 1rem; margin: 1.2rem 0; background: #F4F9FE; }}
img {{ max-width: 100%; height: auto; }}
.map-section {{ break-inside: avoid-page; page-break-inside: avoid; margin-top: 2rem; }}
.map-section img {{ display: block; max-width: 100%; max-height: 205mm; object-fit: contain; margin: 1rem auto; }}
@media print {{
  @page {{ size: A4; margin: 15mm 14mm 16mm; }}
  body {{ max-width: none; padding: 0; font-size: 10pt; }}
  .map-page {{ break-before: page; page-break-before: always; }}
  .map-section h1 {{ margin-top: 0; }}
}}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = assemble()
    (ROOT / "BOOK.md").write_text(source, encoding="utf-8")
    (OUTPUT / "ai-agent-career-roadmap.md").write_text(rebase_for_output(source), encoding="utf-8")
    (ROOT / "BOOK.html").write_text(html_document(source), encoding="utf-8")
    (OUTPUT / "ai-agent-career-roadmap.html").write_text(html_document(source, "../../"), encoding="utf-8")
    print("Built BOOK.md, BOOK.html and output/book reading artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
