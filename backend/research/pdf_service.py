from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)


def generate_research_pdf(research):
    """
    Generate a PDF from a completed Research object.

    Returns:
        BytesIO: PDF file in memory.
    """

    # Create an in-memory file.
    buffer = BytesIO()

    # Create the PDF document.
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    # Load default ReportLab styles.
    styles = getSampleStyleSheet()

    # Custom title style.
    title_style = ParagraphStyle(
        "ResearchTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    # Custom heading style.
    heading_style = ParagraphStyle(
        "ResearchHeading",
        parent=styles["Heading2"],
        spaceBefore=15,
        spaceAfter=8,
    )

    # Normal report text.
    body_style = ParagraphStyle(
        "ResearchBody",
        parent=styles["BodyText"],
        leading=16,
        spaceAfter=8,
    )

    story = []

    # ------------------------------------------------
    # TITLE
    # ------------------------------------------------

    story.append(
        Paragraph(
            "ResearchAI Research Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            research.question,
            heading_style,
        )
    )

    story.append(Spacer(1, 10))

    # ------------------------------------------------
    # REPORT CONTENT
    # ------------------------------------------------

    report = research.final_report or ""

    # Split report into lines.
    lines = report.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        # Remove Markdown heading symbols.
        clean_line = line.lstrip("#").strip()

        # Handle headings.
        if line.startswith("#"):
            story.append(
                Paragraph(
                    clean_line,
                    heading_style,
                )
            )

        # Handle bullet points.
        elif line.startswith("- "):
            bullet_text = line[2:].strip()

            story.append(
                Paragraph(
                    f"• {bullet_text}",
                    body_style,
                )
            )

        else:
            story.append(
                Paragraph(
                    clean_line,
                    body_style,
                )
            )

    # ------------------------------------------------
    # BUILD PDF
    # ------------------------------------------------

    document.build(story)

    # Move pointer back to beginning.
    buffer.seek(0)

    return buffer