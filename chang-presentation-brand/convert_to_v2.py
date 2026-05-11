"""
chang-presentation-brand template.pptx를 v2.0으로 변환하는 스크립트.

동작:
- template.pptx가 존재하면 template_v1_backup.pptx로 백업 후 v2.0 frame으로 변환.
- 존재하지 않으면 새 16:9 빈 프리젠테이션을 생성하여 v2.0 frame을 적용.
- 슬라이드가 0장이면 1장의 빈 슬라이드를 만들어 v2.0 frame을 입힘.
"""

import os
import sys
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

# ====== 설정 ======
# v1 원본은 한국어 파일명(`장동인 PPT템플릿.pptx`)으로 보관, v2 결과는
# SKILL.md 규약에 맞춰 `template.pptx`로 저장한다.
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_CANDIDATES = [
    os.path.join(HERE, '장동인 PPT템플릿.pptx'),
    os.path.join(HERE, 'template.pptx'),
]
SOURCE = next((p for p in SOURCE_CANDIDATES if os.path.exists(p)), None)
BACKUP = (
    os.path.join(HERE, os.path.splitext(os.path.basename(SOURCE))[0] + '_v1_backup.pptx')
    if SOURCE else None
)
OUTPUT = os.path.join(HERE, 'template.pptx')

# ====== v2.1 색상 ======
HERITAGE_NAVY = RGBColor(0x1B, 0x2A, 0x4A)
HERITAGE_BLUE = RGBColor(0x3A, 0x86, 0xFF)
CANVAS = RGBColor(0xFF, 0xFF, 0xFF)  # v2.1: cream(#fffaf0) → white(#ffffff)
DIAGONAL_LIGHT = RGBColor(0xD8, 0xE2, 0xF0)
INK = RGBColor(0x0A, 0x0A, 0x0A)
MUTED = RGBColor(0x6A, 0x6A, 0x6A)

# ====== 헤리티지 Frame 사양 (EMU) ======
SLIDE_W = 12192000
SLIDE_H = 6858000

STRIPE_X, STRIPE_Y = 0, 0
STRIPE_W, STRIPE_H = 360000, SLIDE_H

INNER_X, INNER_Y = 486000, 0
INNER_W, INNER_H = 46800, 1051200

TOPBAR_X, TOPBAR_Y = 360000, 756000
TOPBAR_W, TOPBAR_H = 12240000, 46800

DIAG_X, DIAG_Y = 11530000, 0
DIAG_W, DIAG_H = 660000, 660000

GRAD_X, GRAD_Y = 360000, 6829800
GRAD_W, GRAD_H = 11832000, 28200


def remove_all_shapes(slide):
    sp_tree = slide.shapes._spTree
    targets = (
        sp_tree.findall(qn('p:sp'))
        + sp_tree.findall(qn('p:pic'))
        + sp_tree.findall(qn('p:cxnSp'))
        + sp_tree.findall(qn('p:graphicFrame'))
    )
    for sp in targets:
        sp_tree.remove(sp)


def set_slide_background(slide, rgb):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb


def add_filled_rect(slide, x, y, w, h, rgb):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb
    shape.line.fill.background()
    return shape


def add_diagonal_triangle(slide, x, y, w, h, rgb):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, x, y, w, h)
    # v2.1: rotation 90° → 180° (직각이 우상단 코너에 정확히 위치)
    shape.rotation = 180
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb
    shape.line.fill.background()
    return shape


def add_heritage_frame(slide):
    add_filled_rect(slide, STRIPE_X, STRIPE_Y, STRIPE_W, STRIPE_H, HERITAGE_NAVY)
    add_filled_rect(slide, INNER_X, INNER_Y, INNER_W, INNER_H, HERITAGE_NAVY)
    add_filled_rect(slide, TOPBAR_X, TOPBAR_Y, TOPBAR_W, TOPBAR_H, HERITAGE_NAVY)
    add_diagonal_triangle(slide, DIAG_X, DIAG_Y, DIAG_W, DIAG_H, DIAGONAL_LIGHT)
    add_filled_rect(slide, GRAD_X, GRAD_Y, GRAD_W, GRAD_H, HERITAGE_BLUE)


def add_textbox(slide, text, x, y, w, h, *, font_name, size_pt, bold, rgb, align):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = rgb
    return tb


def add_title_textbox(slide, text='슬라이드 제목'):
    return add_textbox(
        slide, text, 360000, 270000, 11472000, 432000,
        font_name='Pretendard Variable', size_pt=20, bold=True,
        rgb=INK, align=PP_ALIGN.CENTER,
    )


def add_subtitle_textbox(slide, text='부제목 — heritage-blue bold'):
    return add_textbox(
        slide, text, 864000, 882000, 10464000, 378000,
        font_name='Pretendard Variable', size_pt=16, bold=True,
        rgb=HERITAGE_BLUE, align=PP_ALIGN.CENTER,
    )


def add_footer_textbox(slide, name='장동인', org='KAIST 김재철AI대학원 · AIBB LAB'):
    return add_textbox(
        slide, f'{name} | {org}', 864000, 6480000, 6048000, 270000,
        font_name='Pretendard Variable', size_pt=11, bold=False,
        rgb=MUTED, align=PP_ALIGN.LEFT,
    )


def add_page_number(slide, num):
    return add_textbox(
        slide, f'{num:02d}', 11556000, 162000, 432000, 270000,
        font_name='Inter', size_pt=11, bold=False,
        rgb=MUTED, align=PP_ALIGN.RIGHT,
    )


def main():
    if SOURCE:
        shutil.copy(SOURCE, BACKUP)
        print(f'백업 완료: {SOURCE} → {BACKUP}')
        prs = Presentation(SOURCE)
    else:
        print('기존 source PPTX 없음 — 새 16:9 프리젠테이션 생성')
        prs = Presentation()

    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    if len(prs.slides) == 0:
        blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[-1]
        prs.slides.add_slide(blank_layout)
        print('빈 슬라이드 1장 추가')

    for idx, slide in enumerate(prs.slides, start=1):
        remove_all_shapes(slide)
        set_slide_background(slide, CANVAS)
        add_heritage_frame(slide)
        add_title_textbox(slide)
        add_subtitle_textbox(slide)
        add_footer_textbox(slide)
        add_page_number(slide, idx)
        print(f'슬라이드 {idx:02d} v2.0 변환 완료')

    prs.save(OUTPUT)
    print(f'저장 완료: {OUTPUT}')
    if os.path.exists(BACKUP):
        print(f'백업 위치: {BACKUP}')


if __name__ == '__main__':
    main()
