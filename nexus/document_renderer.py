from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclass(frozen=True, slots=True)
class RenderedDocument:
    html_path: Path
    pdf_path: Path | None
    docx_path: Path | None


class ExecutiveDocumentRenderer:
    """Render ATELIER Markdown into branded, print-ready HTML and PDF."""

    def __init__(self, template_dir: Path | None = None):
        resolved = template_dir or Path(__file__).parent.parent / "templates"
        self.environment = Environment(
            loader=FileSystemLoader(resolved),
            autoescape=select_autoescape(("html", "xml")),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(
        self,
        *,
        title: str,
        content: str,
        output_dir: Path,
        slug: str,
        export_pdf: bool = True,
        export_docx: bool = True,
    ) -> RenderedDocument:
        output_dir.mkdir(parents=True, exist_ok=True)
        converter = markdown.Markdown(
            extensions=("tables", "fenced_code", "sane_lists", "toc"),
            extension_configs={"toc": {"permalink": False}},
        )
        body_html = converter.convert(content)
        headings = self._flatten_toc(converter.toc_tokens)
        template = self.environment.get_template("executive_report.html.j2")
        html = template.render(title=title, body_html=body_html, headings=headings)
        html_path = output_dir / f"{slug}.html"
        html_path.write_text(html, encoding="utf-8")

        docx_path: Path | None = None
        if export_docx:
            from nexus.word_renderer import WordDocumentRenderer

            docx_path = output_dir / f"{slug}.docx"
            WordDocumentRenderer().render(
                title=title,
                content=content,
                output_path=docx_path,
            )

        pdf_path: Path | None = None
        if export_pdf:
            pdf_path = output_dir / f"{slug}.pdf"
            if sys.platform == "darwin":
                from nexus.reportlab_pdf import render_reportlab_pdf

                render_reportlab_pdf(title, content, pdf_path)
                return RenderedDocument(
                    html_path=html_path,
                    pdf_path=pdf_path,
                    docx_path=docx_path,
                )
            try:
                from weasyprint import HTML

                HTML(
                    filename=str(html_path),
                    base_url=str(output_dir.resolve()),
                ).write_pdf(pdf_path)
            except (ImportError, OSError):
                from nexus.reportlab_pdf import render_reportlab_pdf

                render_reportlab_pdf(title, content, pdf_path)
        return RenderedDocument(
            html_path=html_path,
            pdf_path=pdf_path,
            docx_path=docx_path,
        )

    @classmethod
    def _flatten_toc(cls, tokens: list[dict[str, object]]) -> list[dict[str, str | int]]:
        result: list[dict[str, str | int]] = []
        for token in tokens:
            level = int(token["level"])
            if level in {2, 3}:
                result.append(
                    {
                        "level": level,
                        "label": str(token["name"]),
                        "anchor": str(token["id"]),
                    }
                )
            children = token.get("children", [])
            if isinstance(children, list):
                result.extend(cls._flatten_toc(children))
        return result
