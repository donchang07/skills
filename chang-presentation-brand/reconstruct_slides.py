"""
v1 `장동인 PPT템플릿.pptx`의 3장 콘텐츠를 v2.0 패턴으로 재구성하여
`template.pptx`에 덮어씌운다.

- 슬라이드 1: 표지 (display-xl 타이틀 + subtitle + author)
- 슬라이드 2: 자기소개 — Image+Text 패턴 (좌 illust-card 인물 자리, 우 텍스트 4 bullet)
- 슬라이드 3: 콘텐츠 가이드 — Comparison Table 패턴 (보통 vs 강조 다이어그램)
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
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, 'template.pptx')
OUTPUT = os.path.join(HERE, 'template.pptx')

# ---- v2.0 색상 ----
HERITAGE_NAVY = RGBColor(0x1B, 0x2A, 0x4A)
HERITAGE_BLUE = RGBColor(0x3A, 0x86, 0xFF)
CANVAS = RGBColor(0xFF, 0xFA, 0xF0)
SURFACE_SOFT = RGBColor(0xFA, 0xF5, 0xE8)
SURFACE_CARD = RGBColor(0xF5, 0xF0, 0xE0)
DIAGONAL_LIGHT = RGBColor(0xD8, 0xE2, 0xF0)
INK = RGBColor(0x0A, 0x0A, 0x0A)
BODY = RGBColor(0x3A, 0x3A, 0x3A)
MUTED = RGBColor(0x6A, 0x6A, 0x6A)
ON_PRIMARY = RGBColor(0xFF, 0xFF, 0xFF)
BRAND_PINK = RGBColor(0xFF, 0x4D, 0x8B)
BRAND_TEAL = RGBColor(0x1A, 0x3A, 0x3A)
BRAND_LAVENDER = RGBColor(0xB8, 0xA4, 0xED)
BRAND_OCHRE = RGBColor(0xE8, 0xB9, 0x4A)
HAIRLINE = RGBColor(0xE5, 0xE5, 0xE5)

# ---- Frame EMU ----
SLIDE_W, SLIDE_H = 12192000, 6858000
STRIPE = (0, 0, 360000, SLIDE_H)
INNER = (486000, 0, 46800, 1051200)
TOPBAR = (360000, 756000, 12240000, 46800)
DIAG = (11530000, 0, 660000, 660000)
GRAD = (360000, 6829800, 11832000, 28200)


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


def set_bg(slide, rgb):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb


def add_rect(slide, x, y, w, h, rgb, *, line=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb
    if not line:
        shp.line.fill.background()
    return shp


def add_diag(slide):
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, *DIAG)
    shp.rotation = 90
    shp.fill.solid()
    shp.fill.fore_color.rgb = DIAGONAL_LIGHT
    shp.line.fill.background()


def add_frame(slide):
    add_rect(slide, *STRIPE, HERITAGE_NAVY)
    add_rect(slide, *INNER, HERITAGE_NAVY)
    add_rect(slide, *TOPBAR, HERITAGE_NAVY)
    add_diag(slide)
    add_rect(slide, *GRAD, HERITAGE_BLUE)


def add_text(slide, text, x, y, w, h, *, font='Pretendard Variable',
             size=14, bold=False, rgb=BODY, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = rgb
    return tb


def add_multiline(slide, lines, x, y, w, h, *, font='Pretendard Variable',
                  size=14, bold=False, rgb=BODY, align=PP_ALIGN.LEFT,
                  line_space=None):
    """lines: list[str] — 각 항목을 별도 단락으로."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_space:
            p.line_spacing = line_space
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = rgb
    return tb


def add_footer(slide):
    add_text(slide, '장동인 | KAIST 김재철AI대학원 · AIBB LAB',
             864000, 6480000, 6048000, 270000,
             size=11, rgb=MUTED, align=PP_ALIGN.LEFT)


def add_page_no(slide, n):
    add_text(slide, f'{n:02d}', 11556000, 162000, 432000, 270000,
             font='Inter', size=11, rgb=MUTED, align=PP_ALIGN.RIGHT)


# ============== Slide 1: Cover ==============
def build_cover(slide):
    remove_all_shapes(slide)
    set_bg(slide, CANVAS)
    add_frame(slide)

    # Eyebrow (uppercase 라벨)
    add_text(slide, 'KAIST · AIBB LAB', 0, 1620000, SLIDE_W, 360000,
             font='Inter', size=11, bold=True, rgb=HERITAGE_BLUE,
             align=PP_ALIGN.CENTER)

    # Display-xl 타이틀 (60pt 권장 → 한글 가독성 고려해 54pt)
    add_text(slide, 'AI 트렌드 및 활용 전략',
             0, 2160000, SLIDE_W, 1080000,
             size=54, bold=True, rgb=INK, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)

    # 가는 구분선 (heritage-blue)
    add_rect(slide, 5544000, 3528000, 1080000, 18000, HERITAGE_BLUE)

    # 발표자
    add_text(slide, '장 동 인', 0, 3780000, SLIDE_W, 540000,
             size=28, bold=True, rgb=INK, align=PP_ALIGN.CENTER)

    # 소속
    add_text(slide, 'KAIST 김재철AI대학원 책임교수 · AIBB LAB 대표',
             0, 4392000, SLIDE_W, 360000,
             size=14, rgb=MUTED, align=PP_ALIGN.CENTER)

    add_footer(slide)
    add_page_no(slide, 1)


# ============== Slide 2: Profile (Image+Text) ==============
def build_profile(slide):
    remove_all_shapes(slide)
    set_bg(slide, CANVAS)
    add_frame(slide)

    # 슬라이드 제목 (상단 가로 실선 위)
    add_text(slide, 'Profile', 360000, 270000, 11472000, 432000,
             size=20, bold=True, rgb=INK, align=PP_ALIGN.CENTER)

    # 부제목 (가로 실선 아래, heritage-blue bold)
    add_text(slide, '“기업과 AI를 아는 교수”  장동인',
             864000, 882000, 10464000, 378000,
             size=16, bold=True, rgb=HERITAGE_BLUE, align=PP_ALIGN.CENTER)

    # 콘텐츠 영역: top 1900000(약 5.29cm)
    # 좌측 illust-card: 인물 사진 자리 (surface-soft 배경, square)
    # 1.15 : 1 비율 — 좌 5.04M EMU + 우 4.38M EMU 정도
    illust_x, illust_y = 1152000, 1900000
    illust_w, illust_h = 4320000, 3960000
    add_rect(slide, illust_x, illust_y, illust_w, illust_h, SURFACE_SOFT)
    # 안내 텍스트(인물 사진 placeholder)
    add_text(slide, '[ 인물 사진 ]',
             illust_x, illust_y, illust_w, illust_h,
             size=14, rgb=MUTED, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)

    # 우측 텍스트 영역
    txt_x = 5832000
    txt_w = 5544000

    # eyebrow
    add_text(slide, 'PROFILE', txt_x, 1900000, txt_w, 270000,
             font='Inter', size=10, bold=True, rgb=HERITAGE_BLUE)

    # headline (큰 제목)
    add_text(slide, '장 동 인', txt_x, 2196000, txt_w, 540000,
             size=32, bold=True, rgb=INK)

    # body lead
    add_text(slide,
             'KAIST 김재철AI대학원 책임교수 (CAIO 과정 담당)',
             txt_x, 2772000, txt_w, 324000,
             size=14, rgb=BODY)
    add_text(slide,
             'AIBB Lab 대표 — AI · Big Data 전략 컨설팅',
             txt_x, 3060000, txt_w, 324000,
             size=14, rgb=BODY)

    # 4개 항목 — pink dot bullet 흉내 (작은 사각형 + 텍스트)
    items = [
        ('경력',     '前 삼성SDS · IBM · KT 컨설팅, 데이터·AI 임원'),
        ('전문분야', 'AI 도입 전략, CEO/실무자 AI 코딩 스쿨 운영'),
        ('학력',     '서울과학종합대학원 경영학박사(Big Data) · USC'),
        ('자격증',   'Google TensorFlow Developer (2020.5)'),
    ]
    bullet_y = 3528000
    row_h = 504000
    for i, (label, desc) in enumerate(items):
        y = bullet_y + i * row_h
        # 작은 navy 사각형 마커
        add_rect(slide, txt_x, y + 90000, 90000, 90000, HERITAGE_NAVY)
        # 라벨 (Inter caption-uppercase 스타일, navy)
        add_text(slide, label, txt_x + 198000, y, 1080000, 270000,
                 size=11, bold=True, rgb=HERITAGE_NAVY)
        # 설명
        add_text(slide, desc, txt_x + 1296000, y, txt_w - 1296000, 360000,
                 size=13, rgb=BODY)

    add_footer(slide)
    add_page_no(slide, 2)


# ============== Slide 3: Content Guide (Comparison) ==============
def build_guide(slide):
    remove_all_shapes(slide)
    set_bg(slide, CANVAS)
    add_frame(slide)

    # 제목
    add_text(slide, '콘텐츠 가이드', 360000, 270000, 11472000, 432000,
             size=20, bold=True, rgb=INK, align=PP_ALIGN.CENTER)
    # 부제목
    add_text(slide, '슬라이드 타이포그래피 · 다이어그램 표준',
             864000, 882000, 10464000, 378000,
             size=16, bold=True, rgb=HERITAGE_BLUE, align=PP_ALIGN.CENTER)

    # 좌측: 일반 다이어그램 카드 (white + hairline)
    L_x, L_y, L_w, L_h = 1152000, 2016000, 4392000, 3960000
    # 테두리 효과: 좌측 카드를 white로
    card_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, L_x, L_y, L_w, L_h)
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = ON_PRIMARY
    card_l.line.color.rgb = HAIRLINE
    card_l.line.width = Pt(0.75)
    # eyebrow
    add_text(slide, 'STANDARD', L_x + 360000, L_y + 360000, L_w - 720000, 270000,
             font='Inter', size=10, bold=True, rgb=MUTED)
    # title
    add_text(slide, '다이어그램 (보통)',
             L_x + 360000, L_y + 666000, L_w - 720000, 540000,
             size=24, bold=True, rgb=INK)
    # divider
    add_rect(slide, L_x + 360000, L_y + 1278000, 360000, 18000, HAIRLINE)
    # type spec lines
    spec_l = [
        '• Headline — Pretendard 20pt, Bold, ink',
        '• 소제목   — Pretendard 16pt, Bold, navy',
        '• 본문     — Pretendard 14pt, Regular, body',
        '• 카드 배경 — canvas / white',
        '• 테두리   — 1px hairline (#e5e5e5)',
    ]
    add_multiline(slide, spec_l,
                  L_x + 360000, L_y + 1404000, L_w - 720000, L_h - 1764000,
                  size=13, rgb=BODY, line_space=1.55)

    # 우측: 강조(featured) 다이어그램 — teal 배경 + pink Featured 배지
    R_x, R_y, R_w, R_h = 6660000, 2016000, 4392000, 3960000
    add_rect(slide, R_x, R_y, R_w, R_h, BRAND_TEAL)

    # Featured 배지 (우상단 pink)
    badge_x = R_x + R_w - 1296000
    badge_y = R_y - 162000
    add_rect(slide, badge_x, badge_y, 1188000, 324000, BRAND_PINK)
    add_text(slide, 'FEATURED', badge_x, badge_y, 1188000, 324000,
             font='Inter', size=10, bold=True, rgb=ON_PRIMARY,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # eyebrow
    add_text(slide, 'EMPHASIS', R_x + 360000, R_y + 360000, R_w - 720000, 270000,
             font='Inter', size=10, bold=True, rgb=BRAND_PINK)
    # title
    add_text(slide, '다이어그램 (강조)',
             R_x + 360000, R_y + 666000, R_w - 720000, 540000,
             size=24, bold=True, rgb=ON_PRIMARY)
    # divider (white)
    add_rect(slide, R_x + 360000, R_y + 1278000, 360000, 18000, ON_PRIMARY)
    # spec lines (white)
    spec_r = [
        '• Headline — Pretendard 20pt, Bold, white',
        '• 소제목   — Pretendard 16pt, Bold, blue',
        '• 본문     — Pretendard 14pt, Regular, white',
        '• 카드 배경 — brand-teal #1a3a3a',
        '• 사용 — 핵심 결론 / Featured 솔루션',
    ]
    add_multiline(slide, spec_r,
                  R_x + 360000, R_y + 1404000, R_w - 720000, R_h - 1764000,
                  size=13, rgb=ON_PRIMARY, line_space=1.55)

    add_footer(slide)
    add_page_no(slide, 3)


def main():
    if not os.path.exists(BASE):
        raise SystemExit(f'기존 template.pptx 없음: {BASE}')
    prs = Presentation(BASE)
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    if len(prs.slides) < 3:
        raise SystemExit(f'슬라이드 3장 필요. 현재 {len(prs.slides)}장')

    builders = [build_cover, build_profile, build_guide]
    for i, (slide, build) in enumerate(zip(prs.slides, builders), start=1):
        build(slide)
        print(f'슬라이드 {i:02d} 재구성 완료')

    prs.save(OUTPUT)
    print(f'저장 완료: {OUTPUT}')


if __name__ == '__main__':
    main()
