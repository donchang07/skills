# -*- coding: utf-8 -*-
"""
chang-book-template — Minimal usage example.

Run this from the working directory after unpacking books.dotx:

    cp <skill-dir>/assets/books.dotx /home/claude/working/book.docx
    python /mnt/skills/public/docx/scripts/office/unpack.py \
        /home/claude/working/book.docx /home/claude/working/unpacked/
    python <skill-dir>/scripts/example_build.py
    # *** 필수: pack 직전에 finalize 호출 (SKILL.md §7.7 참고) ***
    python <skill-dir>/scripts/finalize_docx.py /home/claude/working/unpacked/
    python /mnt/skills/public/docx/scripts/office/pack.py \
        /home/claude/working/unpacked/ /home/claude/working/book_final.docx \
        --original /home/claude/working/book.docx

The example produces a 3-page mini book to verify the template works.
finalize_docx.py 단계를 빠뜨리면 Word가 손상으로 거부하거나 한글이 □로 표시됩니다.
"""
import sys
import os

# Make the builder module importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from builder import (
    build_cover, build_toc, build_section, build_chapter,
    build_part, assemble_body, write_document_xml,
)


def main():
    cover = build_cover(
        title_main="예제 책 제목",
        title_sub="[예제]",
        subtitle="chang-book-template 동작 검증용 미니 도서",
        author="장동인",
        affiliations=["KAIST 김재철AI대학원 책임교수", "AIBB LAB 대표"],
        notes=["이 문서는 스킬 동작 확인용 예제입니다."],
    )

    toc = build_toc()

    intro = build_section(
        heading="머리말",
        level=1,
        body=[
            "이 책은 chang-book-template 스킬이 실제로 books.dotx 템플릿을 "
            "정확히 적용하는지를 검증하기 위한 최소 예제입니다."
        ],
        bullets=[
            "표지의 책 제목1 스타일 적용 확인",
            "목차 자동 필드 작동 확인",
            "InfoBox 강조 박스 작동 확인",
        ],
    )

    part = build_part(
        title="제1부 — 검증 대상",
        chapters=[
            {
                "title": "1장. 핵심 기능 검증",
                "key_message": "스킬이 books.dotx의 모든 핵심 스타일을 깨뜨리지 않고 적용해야 합니다.",
                "main_content": [
                    "표지: 책 제목1 (68pt Book Antiqua)",
                    "본문: heading 1, 2, 3 위계",
                    "리스트: Bullet과 NumberList 시각 표시",
                    "강조: InfoBox 박스",
                ],
                "case_data": [
                    "1차 빌드에서 자동 번호 매김 충돌 발견",
                    "build_book.py 수정으로 즉시 해결",
                    "SKILL.md에 영구 반영",
                ],
                "ceo_takeaway": "스킬은 사용을 통해 학습합니다. 첫 빌드의 발견을 영구 자산으로 만드는 것이 핵심입니다.",
            },
        ],
    )

    body = assemble_body([cover, toc, intro, part])

    document_xml = "/home/claude/working/unpacked/word/document.xml"
    if not os.path.exists(document_xml):
        print(f"ERROR: {document_xml} not found.")
        print("Run unpack.py first (see module docstring).")
        sys.exit(1)

    stats = write_document_xml(document_xml, body)
    print(f"Wrote document.xml ({stats['total_chars']} chars, "
          f"{stats['approx_paragraphs']} paragraphs)")

    # docx 손상 방지 후처리 (SKILL.md §2 절대 규칙 #6, §7.7 참고)
    from finalize_docx import finalize
    unpacked_dir = os.path.dirname(os.path.dirname(document_xml))  # /unpacked
    print()
    finalize(unpacked_dir)


if __name__ == "__main__":
    main()
