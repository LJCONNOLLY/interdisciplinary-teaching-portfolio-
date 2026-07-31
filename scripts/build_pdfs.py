#!/usr/bin/env python3
"""
Development-time PDF generator for the teaching portfolio site.

Reads the source .docx files at the repo root ("Teaching Statement.docx",
"Connolly CV.docx") and regenerates the downloadable PDFs linked from the
site (assets/teaching-statement.pdf, assets/cv.pdf). Re-run this only when
those source docx files change.

LibreOffice's headless --convert-to pdf is not reliable in every
environment, so this renders directly from the docx's own paragraph/bold
structure using reportlab, styled with the site's own palette. It is not a
pixel-perfect reproduction of the original Word formatting -- it is a
plain, readable PDF of the same real text, which is all the site needs.

Usage:
    pip3 install reportlab
    python3 scripts/build_pdfs.py
"""

import zipfile
import xml.etree.ElementTree as ET

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate

INK = HexColor("#152413")
FOREST = HexColor("#30422D")
FROND = HexColor("#4A5D44")

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_docx_paragraphs(path):
    """Returns a list of {"text": str, "bold": bool} per paragraph. `bold`
    is True if any run in the paragraph is bold -- used downstream to infer
    heading level, since docx has no clean semantic heading tag here."""
    with zipfile.ZipFile(path) as z:
        xml_content = z.read("word/document.xml")
    root = ET.fromstring(xml_content)
    paragraphs = []
    for p in root.iter(f"{W_NS}p"):
        texts = []
        is_bold = False
        for r in p.iter(f"{W_NS}r"):
            rpr = r.find(f"{W_NS}rPr")
            if rpr is not None and rpr.find(f"{W_NS}b") is not None:
                is_bold = True
            for t in r.iter(f"{W_NS}t"):
                texts.append(t.text or "")
        text = "".join(texts).strip()
        if text:
            paragraphs.append({"text": text, "bold": is_bold})
    return paragraphs


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


title_style = ParagraphStyle(
    "Title", fontName="Helvetica-Bold", fontSize=20, textColor=INK,
    spaceAfter=16, alignment=TA_LEFT,
)
section_style = ParagraphStyle(
    "Section", fontName="Helvetica-Bold", fontSize=13, textColor=FOREST,
    spaceBefore=16, spaceAfter=6, alignment=TA_LEFT,
)
subheader_style = ParagraphStyle(
    "Sub", fontName="Helvetica-Bold", fontSize=10.5, textColor=FROND,
    spaceBefore=4, spaceAfter=1, alignment=TA_LEFT,
)
body_style = ParagraphStyle(
    "Body", fontName="Times-Roman", fontSize=10.5, textColor=INK,
    leading=15, spaceAfter=6, alignment=TA_LEFT,
)


def build_doc(out_path, pdf_title, story):
    doc = SimpleDocTemplate(
        out_path, pagesize=LETTER,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
        topMargin=0.9 * inch, bottomMargin=0.9 * inch,
        title=pdf_title,
    )
    doc.build(story)
    print(f"wrote {out_path}")


def build_teaching_statement():
    paragraphs = extract_docx_paragraphs("Teaching Statement.docx")
    story = []
    for i, p in enumerate(paragraphs):
        if i == 0:
            story.append(Paragraph(esc(p["text"]), title_style))
        elif p["bold"]:
            story.append(Paragraph(esc(p["text"]), section_style))
        else:
            story.append(Paragraph(esc(p["text"]), body_style))
    build_doc(
        "assets/teaching-statement.pdf",
        "LJ Connolly - Teaching Statement",
        story,
    )


def build_cv():
    paragraphs = extract_docx_paragraphs("Connolly CV.docx")
    story = []
    for i, p in enumerate(paragraphs):
        text, bold = p["text"], p["bold"]
        if i == 0:
            story.append(Paragraph(esc(text), title_style))
        elif bold and text.replace("&", "").replace(" ", "").isupper():
            story.append(Paragraph(esc(text), section_style))
        elif bold:
            story.append(Paragraph(esc(text), subheader_style))
        else:
            story.append(Paragraph(esc(text), body_style))
    build_doc("assets/cv.pdf", "LJ Connolly - Curriculum Vitae", story)


if __name__ == "__main__":
    print("Building teaching-statement.pdf...")
    build_teaching_statement()
    print("Building cv.pdf...")
    build_cv()
