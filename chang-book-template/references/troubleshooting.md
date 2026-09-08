# chang-book-template — 트러블슈팅 가이드

books.dotx 기반으로 생성한 .docx가 Word에서 손상으로 거부되거나 한글이 깨져 보이는 경우의 사례·원인·해결법을 정리합니다. 2026년 5월, OpenClaw 5주 교재 빌드 중 실제로 발견된 4가지 손상 패턴을 기반으로 합니다.

해결의 핵심 원칙: **pack.py 직전에 항상 `scripts/finalize_docx.py`를 호출**하여 books.dotx 잔재를 정리합니다.

---

## 사례 1 — Word "문서를 읽을 수 없습니다" 거부

### 증상
파일을 더블클릭하면 Word가 다음 메시지를 띄우고 열기를 거부합니다.

> Microsoft Word
> Word에서 이 문서를 읽을 수 없습니다. 문서가 손상되었을 수 있습니다.
> 다음을 실행하세요. * 파일을 열고 복구하세요. * 텍스트 복구 변환기로 파일을 여세요.

### 원인
`[Content_Types].xml`의 main document part가 여전히 **template** 타입으로 남아 있습니다.

```xml
<!-- 손상 패턴 -->
<Override PartName="/word/document.xml"
  ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"/>
```

books.dotx를 `.docx`로 단순 파일명 변경했을 때 발생합니다. Word는 "이건 template인데 docx 확장자로 열려고 한다"고 판단해 손상으로 거부합니다.

### 해결
`application/vnd.openxmlformats-officedocument.wordprocessingml.**template**.main+xml`을 `**document**.main+xml`로 교체합니다. `finalize_docx.py`의 `fix_content_type()`이 자동 수행합니다.

---

## 사례 2 — validate.py가 customizations.xml schema 위반 보고

### 증상
docx 스킬의 `validate.py` 실행 시 다음 에러:

```
word\customizations.xml: 1 new error(s)
  - Element '{http://schemas.microsoft.com/office/word/2006/wordml}tcg':
    No matching global declaration available for the validation root.
```

pack.py는 `--original` 옵션 덕분에 \"baseline 대비 새 에러 없음\"으로 통과시키지만, 실제 Word for Mac이나 Office 365 웹에서는 더 엄격하게 검증해서 손상으로 판정할 수 있습니다.

### 원인
books.dotx에 포함된 `word/customizations.xml`은 키보드 단축키 사용자화 정보로, OOXML 표준 schema에 정의되지 않은 Microsoft 확장입니다. 책 본문 표시와는 무관합니다.

### 해결
3가지를 함께 제거합니다.
1. `word/customizations.xml` 파일 삭제
2. `word/_rels/document.xml.rels`에서 `keyMapCustomizations` Relationship 제거
3. `[Content_Types].xml`에서 customizations 관련 Override 제거

`finalize_docx.py`의 `remove_customizations()`가 일괄 처리합니다.

---

## 사례 3 — 표지/본문의 한글이 모두 □□□로 보임

### 증상
docx는 정상적으로 열리지만, 표지의 "책 제목" 같은 한글 부분이 모두 빈 사각형(□)으로 표시됩니다. 본문 일부 한글도 폰트가 적용 안 된 듯한 모습입니다.

### 원인 (3중 복합)

1. **`<w:rPrDefault>`의 eastAsia가 theme 참조**:
   ```xml
   <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia"
             w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
   ```

2. **theme1.xml의 빈 한글 슬롯**:
   ```xml
   <a:majorFont>
     <a:ea typeface=""/>   <!-- 비어 있음 -->
     <a:font script="Hang" typeface="맑은 고딕"/>
   </a:majorFont>
   ```

3. **`<w:r>`에 `<w:rPr>` 자체가 없어 폰트 폴백이 운영체제·Word 버전에 의존**.

세 가지 조건이 겹치면 Word는 한글에 적합한 폰트를 찾지 못해 fallback에 실패하고 □를 표시합니다.

### 해결
`finalize_docx.py`의 `fix_korean_default_font()`가 다음을 수행합니다.
- `<w:rPrDefault>` 안 `eastAsiaTheme="minorEastAsia"` → `eastAsia="맑은 고딕"` 명시적 교체
- `<a:ea typeface=""/>` 빈 슬롯 2곳 → `<a:ea typeface="맑은 고딕"/>`
- 책 제목1(스타일 ID `11`) 같은 Book Antiqua 전용 스타일에 `w:eastAsia="맑은 고딕"` 추가

### 참고: 참조 docx의 정상 패턴

장동인 교수가 직접 만든 정상 .docx의 docDefaults는 다음과 같이 처음부터 명시적입니다.

```xml
<w:rPrDefault>
  <w:rPr>
    <w:rFonts w:ascii="맑은 고딕" w:eastAsia="맑은 고딕"
              w:hAnsi="맑은 고딕" w:cs="맑은 고딕"/>
    <w:sz w:val="22"/><w:szCs w:val="22"/>
    <w:lang w:val="en-US" w:eastAsia="ko-KR" w:bidi="ar-SA"/>
  </w:rPr>
</w:rPrDefault>
```

books.dotx도 이 형태가 되도록 finalize 단계에서 강제합니다.

---

## 사례 4 — XML 선언에 standalone 누락

### 증상
다른 모든 조치를 했음에도 Word for Mac 또는 일부 Office 변종이 손상 메시지를 띄움.

### 원인
파일 첫 줄이 `<?xml version="1.0" encoding="UTF-8"?>`로 끝나고 `standalone="yes"`가 빠져 있습니다. 일부 OOXML 구현은 standalone 명시를 엄격하게 요구합니다.

장동인 교수가 직접 만든 정상 .docx의 첫 줄은:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
```

### 해결
`finalize_docx.py`의 `add_standalone_declaration()`이 모든 .xml과 .rels 파일에 `standalone="yes"`를 추가합니다.

---

## 권장 워크플로우 (실패 방지)

```bash
# 1. 템플릿 복사
cp <skill-path>/assets/books.dotx /tmp/book.docx

# 2. 압축 해제
python office/unpack.py /tmp/book.docx /tmp/unpacked/

# 3. builder.py로 본문 작성 (document.xml 생성)
python build_book.py  # 사용자 빌드 스크립트

# 4. *** 반드시 finalize 단계 추가 ***
python <skill-path>/scripts/finalize_docx.py /tmp/unpacked/

# 5. 다시 압축
python office/pack.py /tmp/unpacked/ /tmp/book_final.docx --original /tmp/book.docx

# 6. (권장) Word에서 직접 열어 한글·표지 확인
```

Step 4를 건너뛰면 위 4가지 사례 중 하나 이상이 발생합니다.

---

## 디버깅 보조

손상이 발생했는데 원인을 모를 때 다음 진단 스크립트를 실행합니다.

```python
import zipfile, re
path = 'C:/path/to/your.docx'
with zipfile.ZipFile(path, 'r') as z:
    ct = z.read('[Content_Types].xml').decode('utf-8')
    if 'template.main+xml' in ct:
        print('❌ Content Type still template (사례 1)')
    if 'word/customizations.xml' in z.namelist():
        print('❌ customizations.xml present (사례 2 위험)')
    d = z.read('word/document.xml').decode('utf-8')
    if 'standalone="yes"' not in d:
        print('❌ standalone="yes" missing (사례 4)')
    s = z.read('word/styles.xml').decode('utf-8')
    if 'eastAsiaTheme="minorEastAsia"' in s:
        print('❌ docDefaults still uses eastAsiaTheme (사례 3)')
```

모든 ❌가 나오지 않으면 finalize가 정상 완료된 것입니다.

---

## 참조 사례

이 문서의 모든 사례는 2026-05-20 OpenClaw 5주 교재 빌드 중 실제 발생한 손상을 분석하여 작성되었습니다. 해결 패턴은 장동인 교수가 직접 만든 정상 docx(`Claude_Code_실습.docx`, 2026-05-13)와 비교 분석한 결과를 반영했습니다.
