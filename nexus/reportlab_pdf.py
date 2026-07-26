from __future__ import annotations

import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

INK = colors.HexColor("#14213D")
MUTED = colors.HexColor("#64748B")
ACCENT = colors.HexColor("#006D77")
ACCENT_SOFT = colors.HexColor("#E8F3F3")
LINE = colors.HexColor("#DBE4EA")
SURFACE = colors.HexColor("#F6F8FA")


class ExecutiveDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=20 * mm,
            title="NEXUS CORE v2 Executive Report",
            author="DJIGO DJIBI",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="content")
        self.addPageTemplates(PageTemplate(id="report", frames=(frame,), onPage=self._footer))

    def _footer(self, canvas, doc) -> None:
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(18 * mm, 9 * mm, "NEXUS CORE v2 · CONFIDENTIEL")
        canvas.drawRightString(192 * mm, 9 * mm, f"PAGE {doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:
        if isinstance(flowable, Paragraph) and flowable.style.name in {"Heading2", "Heading3"}:
            if flowable.getPlainText() == "Table des matières":
                return
            level = 0 if flowable.style.name == "Heading2" else 1
            key = f"heading-{self.seq.nextf('heading')}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, level=level, closed=False)
            self.notify("TOCEntry", (level, flowable.getPlainText(), self.page, key))


def render_reportlab_pdf(title: str, content: str, output_path: Path) -> None:
    styles = _styles()
    story = [
        Spacer(1, 54 * mm),
        Paragraph("NEXUS CORE v2 · EXECUTIVE REPORT", styles["Eyebrow"]),
        Spacer(1, 8 * mm),
        Paragraph(escape(title), styles["CoverTitle"]),
        Spacer(1, 8 * mm),
        HRFlowable(width=42 * mm, thickness=2, color=ACCENT, hAlign="LEFT"),
        Spacer(1, 9 * mm),
        Paragraph("PREPARED BY", styles["Prepared"]),
        Paragraph("DJIGO DJIBI", styles["PreparedName"]),
        Paragraph(
            "CX Consultant | Strategic Product &amp; UX/UI Designer | AI Front-End Developer",
            styles["Prepared"],
        ),
        PageBreak(),
        Paragraph("SOMMAIRE", styles["Eyebrow"]),
        Spacer(1, 6 * mm),
        Paragraph("Table des matières", styles["Heading2"]),
        Spacer(1, 6 * mm),
    ]
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC2", fontName="Helvetica-Bold", fontSize=10, leading=15, textColor=INK),
        ParagraphStyle(
            "TOC3",
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            leftIndent=8 * mm,
            textColor=MUTED,
        ),
    ]
    story.extend((toc, PageBreak()))
    story.extend(_markdown_flowables(content, styles))
    document = ExecutiveDocTemplate(str(output_path))
    document.multiBuild(story)


def _styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    return {
        "Eyebrow": ParagraphStyle(
            "Eyebrow",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=11,
            textColor=ACCENT,
            spaceAfter=3 * mm,
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            parent=sample["Title"],
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=33,
            textColor=INK,
            alignment=TA_LEFT,
        ),
        "Prepared": ParagraphStyle(
            "Prepared",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=12,
            textColor=MUTED,
        ),
        "PreparedName": ParagraphStyle(
            "PreparedName",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=18,
            textColor=INK,
        ),
        "Heading2": ParagraphStyle(
            "Heading2",
            parent=sample["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=19,
            leading=22,
            textColor=INK,
            spaceBefore=10 * mm,
            spaceAfter=4 * mm,
            keepWithNext=True,
        ),
        "Heading3": ParagraphStyle(
            "Heading3",
            parent=sample["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=ACCENT,
            spaceBefore=6 * mm,
            spaceAfter=3 * mm,
            keepWithNext=True,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            textColor=INK,
            spaceAfter=3 * mm,
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            parent=sample["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=colors.white,
        ),
        "Bullet": ParagraphStyle(
            "Bullet",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            leftIndent=6 * mm,
            firstLineIndent=-3 * mm,
            textColor=INK,
            spaceAfter=1.5 * mm,
        ),
        "Callout": ParagraphStyle(
            "Callout",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            leftIndent=5 * mm,
            rightIndent=5 * mm,
            borderColor=ACCENT,
            borderWidth=1,
            borderPadding=10,
            backColor=ACCENT_SOFT,
            textColor=INK,
            spaceBefore=4 * mm,
            spaceAfter=5 * mm,
        ),
    }


def _inline(text: str) -> str:
    clean = escape(text.strip())
    clean = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", clean)
    clean = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", clean)
    return clean


def _markdown_flowables(content: str, styles: dict[str, ParagraphStyle]) -> list:
    lines = content.splitlines()
    output: list = []
    paragraph: list[str] = []
    index = 0

    def flush() -> None:
        if paragraph:
            output.append(Paragraph(_inline(" ".join(paragraph)), styles["Body"]))
            paragraph.clear()

    while index < len(lines):
        line = lines[index].rstrip()
        if line.startswith("## "):
            flush()
            output.append(Paragraph(_inline(line[3:]), styles["Heading2"]))
        elif line.startswith("### "):
            flush()
            output.append(Paragraph(_inline(line[4:]), styles["Heading3"]))
        elif line.startswith("> "):
            flush()
            output.append(Paragraph(_inline(line[2:]), styles["Callout"]))
        elif re.match(r"^(?:[-*]|\d+\.)\s+", line):
            flush()
            marker, text = line.split(maxsplit=1)
            bullet = "•" if marker in {"-", "*"} else marker
            output.append(Paragraph(f"{bullet} {_inline(text)}", styles["Bullet"]))
        elif line.startswith("|") and index + 1 < len(lines) and lines[index + 1].startswith("|"):
            flush()
            table_lines = [line]
            index += 1
            table_lines.append(lines[index])
            while index + 1 < len(lines) and lines[index + 1].startswith("|"):
                index += 1
                table_lines.append(lines[index])
            output.append(_table(table_lines, styles))
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
        index += 1
    flush()
    return output


def _table(lines: list[str], styles: dict[str, ParagraphStyle]) -> Table:
    rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines]
    if len(rows) > 1 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        rows.pop(1)
    formatted = []
    for row_index, row in enumerate(rows):
        style = styles["TableHeader"] if row_index == 0 else styles["Body"]
        formatted.append([Paragraph(_inline(cell), style) for cell in row])
    table = Table(formatted, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), (colors.white, SURFACE)),
                ("LINEBELOW", (0, 1), (-1, -1), 0.5, LINE),
            ]
        )
    )
    return table
