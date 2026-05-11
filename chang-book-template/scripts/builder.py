# -*- coding: utf-8 -*-
"""
chang-book-template — Reusable book builder helpers.

This module provides paragraph builder functions that produce Word XML
matching the books.dotx template. Use it to construct a book document
without re-deriving the style IDs or numbering rules each time.

Typical usage:

    from builder import (
        build_cover, build_toc, build_part, build_chapter,
        assemble_body, write_document_xml,
    )

    # Define your content (your data, your structure)
    cover_xml = build_cover(
        title_main="기업이 바이브코딩으로 일하는 법",
        title_sub="[가제]",
        subtitle="현업 바이브 코딩과 그 뒤를 받치는 7가지 준비",
        author="장동인",
        affiliations=["KAIST 김재철AI대학원 책임교수", "AIBB LAB 대표"],
        notes=["본 문서는 출판 기획용 상세 목차안입니다."],
    )
    toc_xml = build_toc()
    part_xml = build_part(
        title="제1부 — 왜 바이브 코딩이 AX의 핵심 키인가",
        chapters=[
            build_chapter(
                title="1장. DX와 AX의 결정적 차이",
                key_message="...",
                main_content=["DX와 AX의 정의 차이...", "..."],
                case_data=["Deloitte 2026 State of AI...", "..."],
                ceo_takeaway="CEO는 AX를 DX의 연장으로...",
            ),
        ],
    )

    body = assemble_body([cover_xml, toc_xml, part_xml])
    write_document_xml("/path/to/unpacked/word/document.xml", body)

Then run pack.py to produce the final .docx.
"""
import re
from xml.sax.saxutils import escape as xml_escape


# ============================================================================
# Style ID constants from books.dotx
# ============================================================================
STYLE_BOOK_TITLE = "11"           # 책 제목1 (68pt Book Antiqua) - cover main title
STYLE_HEADING_1 = "10"            # heading 1 (auto page break)
STYLE_HEADING_2 = "2"             # heading 2
STYLE_HEADING_3 = "3"             # heading 3
STYLE_HEADING_4 = "4"             # heading 4
STYLE_HEADING_5 = "5"             # heading 5
STYLE_BODY = "a2"                 # Body Text
STYLE_BODY_INDENT = "a6"          # Normal Indent
STYLE_BULLET = "Bullet"           # Black bullet (numId=7, KEEP)
STYLE_NUMBER_LIST = "NumberList"  # Numbered list (numId=6, KEEP)
STYLE_INFO_BOX = "InfoBox"        # Info Box (centered emphasis)
STYLE_THINK_POINT = "af6"         # 생각할점 (book-specific reflection box)
STYLE_VERSION = "Version"         # Version info (Book Antiqua 18pt Bold)
STYLE_TOC1 = "TOC1"               # TOC heading
STYLE_CAPTION = "af8"             # Image caption
STYLE_CHECKLIST = "Checklist"
STYLE_CHECKLIST_X = "Checklist-X"


# Heading styles whose numbering must be explicitly disabled when used
# (heading 1 has numId=46, heading 2 has numId=13, TOC1 inherits from heading 2).
_HEADING_STYLES_WITH_NUMBERING = {STYLE_HEADING_1, STYLE_HEADING_2, STYLE_TOC1}


# ============================================================================
# Low-level paragraph builders
# ============================================================================
def esc(text):
    """Escape XML special characters."""
    return xml_escape(str(text))


def p_styled(style_id, text, run_extras="", disable_numbering=None):
    """Make a single paragraph with given style and text.

    `disable_numbering` defaults to True for heading 1 / heading 2 / TOC1
    because those styles inherit auto-numbering from books.dotx that
    conflicts with manually-numbered chapter titles.

    Pass disable_numbering=False explicitly if you actually want auto numbers.
    """
    if disable_numbering is None:
        disable_numbering = style_id in _HEADING_STYLES_WITH_NUMBERING

    num_off = ""
    if disable_numbering:
        num_off = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'

    return (
        f'<w:p><w:pPr><w:pStyle w:val="{style_id}"/>{num_off}</w:pPr>'
        f'<w:r>{run_extras}<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    )


def p_plain(text, style_id=STYLE_BODY):
    """Plain body paragraph."""
    return p_styled(style_id, text)


def p_bullet(text):
    """Black bullet item. Numbering is preserved (visual marker)."""
    return p_styled(STYLE_BULLET, text, disable_numbering=False)


def p_number_list(text):
    """Numbered list item. Numbering is preserved (visual marker)."""
    return p_styled(STYLE_NUMBER_LIST, text, disable_numbering=False)


def p_info_box(text):
    """Info box (centered emphasis). Use for CEO takeaways or key callouts."""
    return p_styled(STYLE_INFO_BOX, text)


def p_think_point(text):
    """Reflection box (생각할점). Use for chapter-end thinking prompts."""
    return p_styled(STYLE_THINK_POINT, text)


def p_empty():
    """Empty paragraph for spacing."""
    return '<w:p/>'


def p_page_break():
    """Explicit page break."""
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def p_bold(text, style_id=STYLE_BODY):
    """Body paragraph with bold run."""
    return (
        f'<w:p><w:pPr><w:pStyle w:val="{style_id}"/></w:pPr>'
        f'<w:r><w:rPr><w:b/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    )


# ============================================================================
# High-level section builders
# ============================================================================
def build_cover(title_main, title_sub=None, subtitle=None,
                author=None, affiliations=None, notes=None):
    """Build a cover page.

    Args:
        title_main: Main book title (rendered with 책 제목1, 68pt)
        title_sub: Small tag above main title (e.g. "[가제]")
        subtitle: Subtitle below main title
        author: Author name (rendered bold)
        affiliations: List of affiliation lines
        notes: List of footer notes (e.g. publishing notes)
    """
    parts = [p_empty(), p_empty(), p_empty()]
    if title_sub:
        parts.append(p_plain(title_sub))
    parts.append(p_styled(STYLE_BOOK_TITLE, title_main))
    if subtitle:
        parts.append(p_styled(STYLE_HEADING_3, subtitle))
    parts.extend([p_empty(), p_empty()])
    if author:
        parts.append(p_bold(author))
    if affiliations:
        for line in affiliations:
            parts.append(p_plain(line))
    if notes:
        parts.extend([p_empty(), p_empty()])
        for note in notes:
            parts.append(p_plain(note))
    parts.append(p_page_break())
    return "\n".join(parts)


def build_toc(heading="목차",
              field_code='TOC \\o "1-3" \\h \\z \\u',
              placeholder="Word에서 F9를 눌러 목차를 새로 고침하세요."):
    """Build the table-of-contents page with an embedded TOC field.

    Word will populate the TOC when the user presses F9.
    """
    parts = [p_styled(STYLE_TOC1, heading)]
    parts.append(
        '<w:p>'
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        f'<w:r><w:instrText xml:space="preserve">{esc(field_code)} </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f'<w:r><w:t xml:space="preserve">{esc(placeholder)}</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        '</w:p>'
    )
    parts.append(p_page_break())
    return "\n".join(parts)


def build_section(heading, level=1, body=None, bullets=None, subsections=None):
    """Build a generic section with a heading, optional body, bullets, and nested subsections.

    Args:
        heading: Section heading text
        level: 1, 2, or 3 (mapped to heading 1/2/3 style)
        body: Optional list of body paragraphs (strings)
        bullets: Optional list of bullet items
        subsections: Optional list of nested section dicts:
            {"heading": str, "level": int, "body": [...], "bullets": [...]}
    """
    style_map = {1: STYLE_HEADING_1, 2: STYLE_HEADING_2, 3: STYLE_HEADING_3,
                 4: STYLE_HEADING_4, 5: STYLE_HEADING_5}
    style_id = style_map[level]
    parts = [p_styled(style_id, heading)]
    if body:
        for para in body:
            parts.append(p_plain(para))
    if bullets:
        for item in bullets:
            parts.append(p_bullet(item))
    if subsections:
        for sub in subsections:
            parts.append(build_section(**sub))
    return "\n".join(parts)


def build_chapter(title, key_message=None, main_content=None,
                  main_content_label="주요 다룰 내용",
                  case_data=None, ceo_takeaway=None,
                  think_points=None, title_level=2):
    """Build a chapter following the standard chang-book pattern.

    Standard structure: Title → 핵심 메시지 → 주요 다룰 내용 → 핵심 사례 및 데이터 → CEO에게 주는 시사점 → 생각할점

    Args:
        title: Chapter title (e.g. "1장. DX와 AX의 결정적 차이")
        key_message: Single-paragraph key message
        main_content: List of bullets describing main content
        main_content_label: Label for the main content section (default "주요 다룰 내용",
                            use "주요 내용" for prologue/epilogue)
        case_data: List of bullets for case studies and data
        ceo_takeaway: CEO takeaway text (rendered as InfoBox)
        think_points: Optional list of reflection prompts (rendered as 생각할점)
        title_level: 1 or 2 (default 2 — typical for chapters under a part)
    """
    style_map = {1: STYLE_HEADING_1, 2: STYLE_HEADING_2}
    title_style = style_map[title_level]
    parts = [p_styled(title_style, title)]

    if key_message:
        parts.append(p_styled(STYLE_HEADING_3, "핵심 메시지"))
        parts.append(p_plain(key_message))

    if main_content:
        parts.append(p_styled(STYLE_HEADING_3, main_content_label))
        for bullet in main_content:
            parts.append(p_bullet(bullet))

    if case_data:
        parts.append(p_styled(STYLE_HEADING_3, "핵심 사례 및 데이터"))
        for bullet in case_data:
            parts.append(p_bullet(bullet))

    if ceo_takeaway:
        parts.append(p_styled(STYLE_HEADING_3, "CEO에게 주는 시사점"))
        parts.append(p_info_box(ceo_takeaway))

    if think_points:
        parts.append(p_styled(STYLE_HEADING_3, "생각할 점"))
        for point in think_points:
            parts.append(p_think_point(point))

    return "\n".join(parts)


def build_part(title, chapters):
    """Build a Part (제N부) containing multiple chapters.

    The part title is rendered as heading 1 (auto page break).
    Chapters are rendered as heading 2.
    """
    parts = [p_styled(STYLE_HEADING_1, title)]
    for chapter in chapters:
        if isinstance(chapter, dict):
            parts.append(build_chapter(**chapter))
        elif isinstance(chapter, str):
            # Already built XML
            parts.append(chapter)
        else:
            raise TypeError(f"chapter must be dict or str, got {type(chapter)}")
    return "\n".join(parts)


def build_appendix(title="부록", items=None):
    """Build an appendix section with multiple sub-items.

    Args:
        title: Appendix main title
        items: List of dicts with {"title": str, "body": str or list}
    """
    parts = [p_styled(STYLE_HEADING_1, title)]
    if items:
        for item in items:
            parts.append(p_styled(STYLE_HEADING_2, item["title"]))
            body = item.get("body", "")
            if isinstance(body, list):
                for para in body:
                    parts.append(p_plain(para))
            else:
                parts.append(p_plain(body))
    return "\n".join(parts)


# ============================================================================
# Body assembly + document.xml writer
# ============================================================================
def assemble_body(sections):
    """Concatenate XML section strings into a single body content string."""
    return "\n".join(sections)


def write_document_xml(document_xml_path, body_content):
    """Replace the body content in document.xml while preserving sectPr.

    sectPr (page setup, even/odd footers) MUST be preserved or the page
    layout will break.

    Args:
        document_xml_path: Path to the unpacked word/document.xml
        body_content: Concatenated body XML (output of assemble_body)
    """
    with open(document_xml_path, "r", encoding="utf-8") as f:
        original = f.read()

    body_match = re.search(
        r"(<w:body>)(.*?)(<w:sectPr.*?</w:sectPr>)\s*(</w:body>)",
        original, re.DOTALL
    )
    if not body_match:
        raise RuntimeError(
            "Could not find <w:body>...<w:sectPr>...</w:body> pattern in document.xml"
        )

    body_open = body_match.group(1)
    sectpr = body_match.group(3)
    body_close = body_match.group(4)

    new_body = f"{body_open}\n{body_content}\n{sectpr}\n{body_close}"
    new_doc = original[:body_match.start()] + new_body + original[body_match.end():]

    with open(document_xml_path, "w", encoding="utf-8") as f:
        f.write(new_doc)

    return {
        "total_chars": len(new_doc),
        "body_chars": len(body_content),
        "approx_paragraphs": body_content.count("<w:p"),
    }
