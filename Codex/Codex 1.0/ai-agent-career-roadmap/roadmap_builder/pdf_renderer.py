"""Render a useful Markdown subset to polished Chinese PDFs with ReportLab."""

from __future__ import annotations

import html
import os
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


def _find_cjk_font() -> tuple[str, str]:
    candidates = [
        os.environ.get("ROADMAP_CJK_FONT", ""),
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.otf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyh.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return "RoadmapCJK", candidate
    raise RuntimeError("未找到可嵌入的中文字体。请设置 ROADMAP_CJK_FONT 指向 Noto Sans CJK、Microsoft YaHei 或系统中文字体。")


FONT, FONT_PATH = _find_cjk_font()
pdfmetrics.registerFont(TTFont(FONT, FONT_PATH, subfontIndex=0 if FONT_PATH.endswith((".ttc", ".otc")) else 0))
addMapping(FONT, 0, 0, FONT)
addMapping(FONT, 0, 1, FONT)
addMapping(FONT, 1, 0, FONT)
addMapping(FONT, 1, 1, FONT)


class RoadmapDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, title: str) -> None:
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
            title=title,
            author="AI Agent Career Roadmap",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="main")
        self.addPageTemplates(PageTemplate(id="content", frames=[frame], onPage=self._header_footer))

    def _header_footer(self, canvas, doc) -> None:  # type: ignore[no-untyped-def]
        canvas.saveState()
        canvas.setFont(FONT, 8)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(self.leftMargin, A4[1] - 11 * mm, self.title[:48])
        canvas.drawRightString(A4[0] - self.rightMargin, 9 * mm, f"第 {doc.page} 页")
        canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
        canvas.line(self.leftMargin, A4[1] - 13 * mm, A4[0] - self.rightMargin, A4[1] - 13 * mm)
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:  # type: ignore[no-untyped-def]
        if isinstance(flowable, Paragraph):
            level = getattr(flowable, "heading_level", None)
            if level in (0, 1, 2):
                text = flowable.getPlainText()
                key = f"heading-{level}-{self.seq.nextf('heading')}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)
                self.notify("TOCEntry", (level, text, self.page, key))


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("RoadmapTitle", parent=base["Title"], fontName=FONT, fontSize=25, leading=34, textColor=colors.HexColor("#111827"), alignment=TA_CENTER, spaceAfter=12 * mm),
        "subtitle": ParagraphStyle("Subtitle", parent=base["Normal"], fontName=FONT, fontSize=10, leading=16, textColor=colors.HexColor("#6B7280"), alignment=TA_CENTER),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontName=FONT, fontSize=18, leading=25, textColor=colors.HexColor("#111827"), spaceBefore=8 * mm, spaceAfter=4 * mm, keepWithNext=True),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontName=FONT, fontSize=14, leading=20, textColor=colors.HexColor("#1F4B43"), spaceBefore=6 * mm, spaceAfter=3 * mm, keepWithNext=True),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontName=FONT, fontSize=11.5, leading=17, textColor=colors.HexColor("#374151"), spaceBefore=4 * mm, spaceAfter=2 * mm, keepWithNext=True),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName=FONT, fontSize=9.6, leading=16, textColor=colors.HexColor("#1F2937"), spaceAfter=2.5 * mm, wordWrap="CJK"),
        "bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName=FONT, fontSize=9.4, leading=15, leftIndent=6 * mm, firstLineIndent=-3 * mm, textColor=colors.HexColor("#1F2937"), spaceAfter=1.5 * mm, wordWrap="CJK"),
        "code": ParagraphStyle("Code", parent=base["Code"], fontName=FONT, fontSize=7.7, leading=11.5, leftIndent=4 * mm, rightIndent=4 * mm, borderColor=colors.HexColor("#D1D5DB"), borderWidth=0.5, borderPadding=7, backColor=colors.HexColor("#F3F4F6"), textColor=colors.HexColor("#111827"), spaceBefore=2 * mm, spaceAfter=4 * mm),
        "toc_title": ParagraphStyle("TocTitle", parent=base["Heading1"], fontName=FONT, fontSize=18, leading=24, textColor=colors.HexColor("#111827"), spaceAfter=5 * mm),
    }


def _inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", escaped)
    return escaped


def _make_heading(text: str, style: ParagraphStyle, level: int) -> Paragraph:
    paragraph = Paragraph(_inline(text), style)
    paragraph.heading_level = level  # type: ignore[attr-defined]
    return paragraph


def _table_from(lines: list[str], styles: dict[str, ParagraphStyle], width: float) -> Table:
    raw_rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    if len(raw_rows) > 1 and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in raw_rows[1]):
        raw_rows.pop(1)
    columns = max(len(row) for row in raw_rows)
    data = []
    for row in raw_rows:
        padded = row + [""] * (columns - len(row))
        data.append([Paragraph(_inline(cell), styles["body"]) for cell in padded])
    table = Table(data, colWidths=[width / columns] * columns, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F0EE")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#163C35")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def _parse_markdown(markdown: str, styles: dict[str, ParagraphStyle], width: float) -> tuple[str, list[object]]:
    lines = markdown.splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "AI Agent Career Roadmap")
    story: list[object] = []
    paragraph_buffer: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_buffer:
            text = " ".join(item.strip() for item in paragraph_buffer)
            story.append(Paragraph(_inline(text), styles["body"]))
            paragraph_buffer.clear()

    index = 0
    in_code = False
    code_lines: list[str] = []
    first_h1 = True
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code_lines), styles["code"], maxLineLength=92))
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            index += 1
            continue
        if in_code:
            code_lines.append(line)
            index += 1
            continue
        if line.startswith("|") and index + 1 < len(lines) and lines[index + 1].startswith("|"):
            flush_paragraph()
            table_lines = []
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(_table_from(table_lines, styles, width))
            story.append(Spacer(1, 3 * mm))
            continue
        if line.startswith("# "):
            flush_paragraph()
            if first_h1:
                first_h1 = False
            else:
                story.append(_make_heading(line[2:].strip(), styles["h1"], 0))
        elif line.startswith("## "):
            flush_paragraph()
            story.append(_make_heading(line[3:].strip(), styles["h2"], 1))
        elif line.startswith("### "):
            flush_paragraph()
            story.append(_make_heading(line[4:].strip(), styles["h3"], 2))
        elif re.match(r"^[-*] ", line):
            flush_paragraph()
            story.append(Paragraph("• " + _inline(line[2:].strip()), styles["bullet"]))
        elif re.match(r"^\d+\. ", line):
            flush_paragraph()
            marker, value = line.split(". ", 1)
            story.append(Paragraph(f"{marker}. " + _inline(value), styles["bullet"]))
        elif line.strip() in {"---", ""}:
            flush_paragraph()
            if line.strip() == "---":
                story.append(Spacer(1, 2 * mm))
        elif line.lstrip().startswith("<!--"):
            flush_paragraph()
        else:
            paragraph_buffer.append(line)
        index += 1
    flush_paragraph()
    return title, story


def markdown_to_pdf(source: Path, output: Path) -> None:
    markdown = source.read_text(encoding="utf-8")
    styles = _styles()
    doc = RoadmapDocTemplate(str(output), title=source.stem.replace("_", " "))
    title, content = _parse_markdown(markdown, styles, doc.width)

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(name="TOC0", fontName=FONT, fontSize=10, leading=17, leftIndent=0, firstLineIndent=0, textColor=colors.HexColor("#111827")),
        ParagraphStyle(name="TOC1", fontName=FONT, fontSize=9, leading=15, leftIndent=5 * mm, firstLineIndent=0, textColor=colors.HexColor("#374151")),
        ParagraphStyle(name="TOC2", fontName=FONT, fontSize=8.5, leading=14, leftIndent=10 * mm, firstLineIndent=0, textColor=colors.HexColor("#6B7280")),
    ]
    cover_title = Paragraph(_inline(title), styles["title"])
    cover_title.heading_level = 0  # type: ignore[attr-defined]
    story: list[object] = [
        Spacer(1, 45 * mm),
        cover_title,
        Paragraph("AI Agent 工程学习系统 · 本地可维护版本", styles["subtitle"]),
        Spacer(1, 8 * mm),
        Paragraph(f"源文件：{html.escape(source.name)}", styles["subtitle"]),
        PageBreak(),
        Paragraph("目录", styles["toc_title"]),
        toc,
        PageBreak(),
    ]
    story.extend(content)
    doc.multiBuild(story)
