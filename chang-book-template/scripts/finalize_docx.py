# -*- coding: utf-8 -*-
"""chang-book-template — Finalize unpacked docx package before re-pack.

books.dotx를 .docx로 단순 복사한 unpacked 디렉토리에는 다음 4가지 잠재 손상 원인이 있습니다.
이 스크립트는 pack 직전에 호출하여 모두 자동 정리합니다.

1) `[Content_Types].xml`의 main document part가 여전히 `template.main+xml`
   → Word가 "이건 템플릿인데 docx로 열려고 한다"고 판단해 손상 모드 진입.
   → 한글이 □□로 보이거나, 심한 경우 "문서를 읽을 수 없습니다" 거부.

2) `word/customizations.xml`이 schema에 안 맞아 Word가 전체 docx를 거부.
   → docx 스킬의 validate.py에서 "No matching global declaration" 에러로 확인 가능.
   → 본 파일은 키 매핑 사용자 설정이고 책 표시에는 영향 없으므로 안전하게 제거.

3) XML 파일들에 `standalone="yes"` 선언이 빠져 있을 수 있음.
   → 일부 Word 변종(특히 Word for Mac, Office 365 웹)에서 손상으로 판정.

4) `styles.xml`의 `<w:rPrDefault>` 안 `<w:rFonts>`가 `eastAsiaTheme="minorEastAsia"`로
   theme 참조 방식이고, `theme1.xml`의 `<a:ea typeface=""/>`가 빈 슬롯.
   → 일부 환경에서 한글 fallback 실패 → 모든 한글이 □ 표시.

사용 예:

    python finalize_docx.py /path/to/unpacked

또는 builder.py 워크플로우 안에서:

    from finalize_docx import finalize
    finalize("/path/to/unpacked")
    # 이어서 pack.py 실행
"""
import os
import re
import sys


TEMPLATE_CT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml'
DOCUMENT_CT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
KOREAN_FONT = 'Pretendard'  # 모든 산출물 서체는 Pretendard로 고정 (SKILL.md §서체 규칙)


def fix_content_type(unpacked_dir):
    """[Content_Types].xml의 main document part를 docx 타입으로 강제.
    또한 customizations.xml Override가 있으면 제거.
    """
    ct_path = os.path.join(unpacked_dir, '[Content_Types].xml')
    if not os.path.exists(ct_path):
        return False, 'Content_Types.xml not found'

    with open(ct_path, 'r', encoding='utf-8') as f:
        ct = f.read()
    original = ct

    # 1) template.main+xml → document.main+xml
    ct = ct.replace(TEMPLATE_CT, DOCUMENT_CT)

    # 2) customizations.xml 관련 Override 제거
    ct = re.sub(
        r'<Override[^/]*PartName="/word/customizations\.xml"[^/]*/>',
        '',
        ct,
    )
    ct = re.sub(
        r'<Override[^/]*ContentType="[^"]*keyMapCustomizations[^"]*"[^/]*/>',
        '',
        ct,
    )

    if ct == original:
        return False, 'no change'
    with open(ct_path, 'w', encoding='utf-8') as f:
        f.write(ct)
    return True, 'patched'


def remove_customizations(unpacked_dir):
    """word/customizations.xml 파일과 관련 relationship 제거."""
    actions = []

    custom_path = os.path.join(unpacked_dir, 'word', 'customizations.xml')
    if os.path.exists(custom_path):
        os.remove(custom_path)
        actions.append('removed word/customizations.xml')

    rels_path = os.path.join(unpacked_dir, 'word', '_rels', 'document.xml.rels')
    if os.path.exists(rels_path):
        with open(rels_path, 'r', encoding='utf-8') as f:
            r = f.read()
        new_r = re.sub(
            r'<Relationship[^/]*Type="http://schemas\.microsoft\.com/office/'
            r'2006/relationships/keyMapCustomizations"[^/]*/>',
            '',
            r,
        )
        if new_r != r:
            with open(rels_path, 'w', encoding='utf-8') as f:
                f.write(new_r)
            actions.append('cleaned word/_rels/document.xml.rels')

    return actions


def add_standalone_declaration(unpacked_dir):
    """모든 .xml과 .rels 파일에 standalone="yes"를 추가."""
    patched = []
    for root, _dirs, files in os.walk(unpacked_dir):
        for name in files:
            if not (name.endswith('.xml') or name.endswith('.rels')):
                continue
            fp = os.path.join(root, name)
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = re.sub(
                r'<\?xml version="1\.0" encoding="UTF-8"\?>',
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                content,
                count=1,
            )
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                patched.append(os.path.relpath(fp, unpacked_dir))
    return patched


def fix_korean_default_font(unpacked_dir):
    """styles.xml의 docDefaults에 명시적 한글 폰트 적용 + theme1.xml의 빈 ea typeface 채움."""
    actions = []

    # 1) styles.xml docDefaults
    styles_path = os.path.join(unpacked_dir, 'word', 'styles.xml')
    if os.path.exists(styles_path):
        with open(styles_path, 'r', encoding='utf-8') as f:
            s = f.read()

        # eastAsiaTheme="minorEastAsia" → eastAsia="맑은 고딕"
        new_s = re.sub(
            r'(<w:rPrDefault>.*?<w:rFonts[^/]*)w:eastAsiaTheme="[^"]*"([^/]*/>.*?</w:rPrDefault>)',
            rf'\1w:eastAsia="{KOREAN_FONT}"\2',
            s,
            count=1,
            flags=re.DOTALL,
        )
        if new_s != s:
            with open(styles_path, 'w', encoding='utf-8') as f:
                f.write(new_s)
            actions.append(f'styles.xml docDefaults eastAsia="{KOREAN_FONT}"')

    # 2) theme1.xml의 빈 ea typeface 채움
    theme_path = os.path.join(unpacked_dir, 'word', 'theme', 'theme1.xml')
    if os.path.exists(theme_path):
        with open(theme_path, 'r', encoding='utf-8') as f:
            t = f.read()
        new_t = t.replace(
            '<a:ea typeface=""/>',
            f'<a:ea typeface="{KOREAN_FONT}"/>',
        )
        if new_t != t:
            with open(theme_path, 'w', encoding='utf-8') as f:
                f.write(new_t)
            actions.append(f'theme1.xml empty <a:ea> filled with {KOREAN_FONT}')

    # 3) 책 제목1(11) 스타일에 eastAsia 추가 (Book Antiqua만 있을 경우)
    if os.path.exists(styles_path):
        with open(styles_path, 'r', encoding='utf-8') as f:
            s = f.read()
        pat = r'(<w:style[^>]*w:styleId="11"[^>]*>.*?</w:style>)'
        m = re.search(pat, s, re.DOTALL)
        if m:
            block = m.group(1)
            rfonts_match = re.search(r'<w:rFonts ([^/]*)/>', block)
            if (
                rfonts_match
                and 'w:eastAsia' not in rfonts_match.group(1)
                and 'w:eastAsiaTheme' not in rfonts_match.group(1)
            ):
                new_attrs = rfonts_match.group(1) + f' w:eastAsia="{KOREAN_FONT}"'
                new_rfonts = f'<w:rFonts {new_attrs}/>'
                new_block = block.replace(rfonts_match.group(0), new_rfonts, 1)
                s = s.replace(block, new_block, 1)
                with open(styles_path, 'w', encoding='utf-8') as f:
                    f.write(s)
                actions.append('styles.xml style "11" (책 제목1) eastAsia 추가')

    # 4) 서체 드리프트 차단 — 남아 있는 구서체를 Pretendard로 강제 교체
    #    (본문을 손으로 편집하다 다른 폰트가 섞여 들어오는 것을 막는다)
    LEGACY = ['맑은 고딕', 'Book Antiqua', 'Times New Roman', 'Times',
              'Arial Narrow', 'Arial', '굴림체', '돋움체', '바탕']
    targets = [
        os.path.join(unpacked_dir, 'word', 'styles.xml'),
        os.path.join(unpacked_dir, 'word', 'document.xml'),
        os.path.join(unpacked_dir, 'word', 'header1.xml'),
        os.path.join(unpacked_dir, 'word', 'footer1.xml'),
        os.path.join(unpacked_dir, 'word', 'footer2.xml'),
    ]
    swapped = 0
    for path in targets:
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
        original = s
        for face in LEGACY:
            for attr in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
                s = s.replace(f'w:{attr}="{face}"', f'w:{attr}="{KOREAN_FONT}"')
        if s != original:
            swapped += 1
            with open(path, 'w', encoding='utf-8') as f:
                f.write(s)
    if swapped:
        actions.append(f'구서체 → {KOREAN_FONT} 강제 교체 ({swapped}개 파트)')

    return actions


def finalize(unpacked_dir, verbose=True):
    """4가지 후처리를 순서대로 실행하고 결과를 리포트."""
    report = {
        'content_type': fix_content_type(unpacked_dir),
        'customizations_removed': remove_customizations(unpacked_dir),
        'standalone_added': add_standalone_declaration(unpacked_dir),
        'korean_font_applied': fix_korean_default_font(unpacked_dir),
    }
    if verbose:
        print('=== finalize_docx report ===')
        for k, v in report.items():
            print(f'  {k}: {v}')
    return report


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python finalize_docx.py <unpacked_dir>')
        sys.exit(1)
    finalize(sys.argv[1])
