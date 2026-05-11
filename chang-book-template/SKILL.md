---
name: chang-book-template
description: "KAIST AI대학원 장동인 교수의 책 집필·편집 전용 Word 스킬입니다. 신규 원고는 books.dotx 템플릿으로 생성하고, 기존 원고는 일관된 편집 표준(단락 간격, 부 단위 머리말/꼬리말, 페이지 번호 정렬, 쉬운 한국어 문체, 의사결정 주체 분업)을 강제합니다. 책, 도서, 챕터, 책 원고, 책 초안, 책 표지, 목차, 단행본 작성·편집 요청 시 자동으로 활성화됩니다. '책 써줘', '챕터 써줘', '~에 관한 책', '단행본 원고', '도서 원고', 'Word로 책', '.docx로 책', '책 편집해줘', '원고 다듬어줘' 같은 모든 요청은 이 스킬을 사용해야 합니다. 자매 스킬 chang-presentation-brand와 짝을 이루어 책 → 강의 PPT 변환 워크플로우를 지원합니다. 단순 보고서/메모/제안서 등 책이 아닌 일반 Word 문서에는 이 스킬을 사용하지 마세요(이 경우 표준 docx 스킬 사용)."
---

# 장동인 책 집필 템플릿 (chang-book-template)

## 1. 개요

이 스킬은 장동인 교수의 책 집필 전용 Word 템플릿(`books.dotx`)을 사용하여 .docx 형태의 책 원고를 생성합니다. 단행본·전문서 단위의 장문 콘텐츠를 일관된 스타일로 작성하기 위해 설계되었습니다.

**자매 스킬과의 관계**: 이 스킬로 만든 책 챕터는 `chang-presentation-brand` 스킬로 강의 PPT로 변환할 때 자연스럽게 매핑되도록 구조가 설계되어 있습니다. 즉, 한 번의 집필이 책과 강의 자료 양쪽에 활용되는 것이 이 스킬의 핵심 가치입니다.

---

## 2. 절대 규칙

1. **항상 `assets/books.dotx`를 기반으로 사용** — docx-js나 python-docx로 처음부터 만들지 마세요. 한국어 폰트 매핑과 사용자 정의 스타일(책 제목1, ChapterTitle, Info Box 등)이 손상됩니다.
2. **unpack → edit XML → repack 방식**으로 작업 — `/mnt/skills/public/docx/scripts/office/`의 unpack/pack 스크립트를 그대로 활용합니다.
3. **출력은 `.docx`** — `.dotx`는 템플릿 형식이므로 작업본은 항상 `.docx`로 저장합니다.
4. **임의로 폰트, 색상, 크기를 바꾸지 말 것** — 모든 시각 속성은 템플릿의 styles.xml에 이미 정의되어 있으므로 `<w:pStyle>`로 스타일 ID만 지정합니다.
5. **표지·목차·본문 모두 한 .docx 파일에 통합** — 사용자가 별도 요청하지 않는 한 분리하지 않습니다.

---

## 3. 책 구조 (스킬이 자동 생성하는 표준 구조)

표준 책 한 권은 다음 4개 영역으로 구성됩니다.

### 3.1 표지 (Cover)
- **책 제목1** (스타일 ID `11`): 메인 타이틀
- **부제** (스타일 ID `Char`): 보조 타이틀
- **저자명**: "장동인 (Dong In Chang)" 기본값, 사용자 변경 가능
- **Version 정보** (스타일 ID `Version`): 버전·날짜

### 3.2 목차 (Table of Contents)
- **TOC 제목1** (스타일 ID `TOC1`): "목차" 또는 "Contents" 제목
- 목차 본문은 Word에서 자동 생성되는 필드(`TOC \o "1-3"`)를 삽입합니다. 사용자가 Word에서 F9로 새로 고침하면 채워집니다.

### 3.3 챕터 본문 (Chapter Body)
각 챕터는 다음과 같은 위계 구조를 갖습니다.
- **Chapter Title** (스타일 ID `ChapterTitle`) 또는 **heading 1** (스타일 ID `10`): 챕터 표지
- **heading 2** (`2`) → 절(Section)
- **heading 3** (`3`) → 소절(Subsection)
- **heading 4~5** (`4`, `5`) → 더 세부 구분
- **Body Text** (`a2`) 또는 **Normal Indent** (`a6`): 본문
- **Bullet** (`Bullet`): 검은 bullet
- **Number List** (`NumberList`): 번호 리스트
- **Info Box** (`InfoBox`): 가운데 정렬 강조 박스
- **생각할점** (`af6`): 인사이트/사고 박스 (책 특유의 박스)
- **Highlighted Variable** (`HighlightedVariable`): 파란색 강조 텍스트

### 3.4 부록·체크리스트
- **Checklist** (`Checklist`): 체크된 항목
- **Checklist-X** (`Checklist-X`): 체크되지 않은 항목

---

## 4. 워크플로우 (사용자 요청 → .docx 생성)

### 4.1 입력 형식 (권장: 마크다운)

장동인교수님은 마크다운으로 초안을 주시거나 대화로 챕터 구조를 지시하십니다. 두 경우 모두 다음 매핑 규칙을 따릅니다.

`references/style_map.md`에 마크다운 ↔ Word 스타일 매핑표가 있으니 처음 작업 시 반드시 참고하세요.

### 4.2 표준 절차

다음 단계를 순서대로 따르세요.

**Step 1. 템플릿 사본 만들기**

```bash
cp <skill-path>/assets/books.dotx /home/claude/working/book.docx
```

확장자를 `.dotx` → `.docx`로 변경합니다. 템플릿의 모든 스타일이 그대로 유지됩니다.

**Step 2. 템플릿 압축 해제**

```bash
python /mnt/skills/public/docx/scripts/office/unpack.py /home/claude/working/book.docx /home/claude/working/unpacked/
```

**Step 3. 책 콘텐츠를 builder.py로 작성**

XML을 직접 작성하지 마시고, 스킬에 동봉된 `scripts/builder.py` 헬퍼를 사용하세요. 이 모듈은 books.dotx의 모든 스타일 ID와 자동 번호 매김 비활성화 규칙을 이미 알고 있습니다.

```python
import sys
sys.path.insert(0, "<skill-path>/scripts")
from builder import (
    build_cover, build_toc, build_section, build_chapter,
    build_part, build_appendix, assemble_body, write_document_xml,
)

cover = build_cover(
    title_main="기업이 바이브코딩으로 일하는 법",
    title_sub="[가제]",
    subtitle="현업 바이브 코딩과 그 뒤를 받치는 7가지 준비",
    author="장동인",
    affiliations=["KAIST 김재철AI대학원 책임교수", "AIBB LAB 대표"],
    notes=["본 문서는 출판 기획용 상세 목차안입니다."],
)

toc = build_toc()  # 목차 자동 필드 삽입

part1 = build_part(
    title="제1부 — 왜 바이브 코딩이 AX의 핵심 키인가",
    chapters=[
        {
            "title": "1장. DX와 AX의 결정적 차이",
            "key_message": "디지털 전환은 프로세스의 디지털화...",
            "main_content": ["DX와 AX의 정의 차이...", "..."],
            "case_data": ["Deloitte 2026 State of AI: ...", "..."],
            "ceo_takeaway": "CEO는 AX를 DX의 연장으로 다루지 말아야...",
        },
    ],
)

body = assemble_body([cover, toc, part1])
write_document_xml("/home/claude/working/unpacked/word/document.xml", body)
```

builder.py가 자동으로 처리하는 것들:
- **자동 번호 매김 비활성화** (heading 1/2/TOC1) — 7.5절 참고
- **sectPr 보존** — 짝수/홀수 footer, 페이지 번호 유지
- **표지·목차·챕터 표준 구조** — 사용자가 데이터만 주면 자동으로 책 구조 생성
- **CEO 시사점 자동 InfoBox 처리** — 임원 독자 가독성 최적화

**Step 4. 압축 다시 만들기**

```bash
python /mnt/skills/public/docx/scripts/office/pack.py /home/claude/working/unpacked/ /home/claude/working/book_final.docx --original /home/claude/working/book.docx
```

`--original` 옵션은 원본 템플릿의 메타데이터·관계를 보존하므로 반드시 지정합니다.

**Step 5. 출력 디렉토리로 이동**

```bash
cp /home/claude/working/book_final.docx /mnt/user-data/outputs/<책이름>.docx
```

그리고 `present_files`로 사용자에게 제시합니다.

**Step 6. (권장) 시각 검증**

가능하면 PDF로 변환하여 한두 페이지를 시각 확인하시기 바랍니다.

```bash
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf book_final.docx
pdftoppm -jpeg -r 100 -f 1 -l 4 book_final.pdf preview
```

LibreOffice는 Book Antiqua 폰트가 없을 수 있으므로 표지 메인 타이틀이 다른 폰트로 보일 수 있으나, Word에서는 정상 표시됩니다.

---

## 5. 핵심 스타일 매핑 요약 (자주 쓰는 것만)

| 마크다운 | Word 스타일 ID | 스타일 이름 | 용도 |
|---------|----------------|-------------|------|
| 책 표지 메인 | `11` | 책 제목1 | 표지 메인 타이틀 (68pt) |
| 챕터 표지 | `ChapterTitle` 또는 `10` | Chapter Title / heading 1 | 챕터 시작 |
| `# 제목` | `10` | heading 1 | 챕터 (자동 페이지 분리) |
| `## 제목` | `2` | heading 2 | 절 |
| `### 제목` | `3` | heading 3 | 소절 |
| `#### 제목` | `4` | heading 4 | 항 |
| `##### 제목` | `5` | heading 5 | 목 |
| 일반 본문 | `a2` | Body Text | 표준 본문 |
| 들여쓰기 본문 | `a6` | Normal Indent | 한 칸 들여쓰기 본문 |
| `- 항목` | `Bullet` | Bullet | 검은 bullet |
| `1. 항목` | `NumberList` | Number List | 번호 리스트 |
| 강조 박스 | `InfoBox` | Info Box | 가운데 정렬 강조 박스 |
| 인사이트 박스 | `af6` | 생각할점 | 책 특유의 사고 박스 |
| `**파란강조**` | `HighlightedVariable` (run style) | Highlighted Variable | 파란색 강조 (run 단위) |
| 이미지 캡션 | `af8` | 이미지 | 이미지 캡션 |
| 체크 항목 | `Checklist` | Checklist | 체크된 항목 |
| 미체크 항목 | `Checklist-X` | Checklist-X | 미체크 항목 |
| 목차 제목 | `TOC1` | TOC 제목1 | "목차" 텍스트 |

전체 매핑은 `references/style_map.md` 참고.

---

## 6. 자매 스킬과의 연계 (책 ↔ PPT)

장동인교수님은 책을 쓴 후 그 내용을 강의 PPT로 변환하는 작업을 자주 하십니다. 두 스킬이 자연스럽게 짝을 이루도록 다음 원칙을 따릅니다.

- **챕터 1개 ≈ PPT 1개 섹션**: heading 1 → PPT 섹션 구분 슬라이드
- **heading 2 ≈ PPT 슬라이드 1장 제목**: 즉, 절 단위가 슬라이드 단위입니다.
- **Bullet/NumberList → 슬라이드 본문 bullet**: 그대로 옮겨갑니다.
- **InfoBox → PPT 강조 박스 슬라이드**: 별도 슬라이드 또는 강조 영역
- **생각할점 → 토론용 슬라이드**: 강의 중 토론을 유도할 때

또한 §9.5에 정의된 **두 개의 축 골격**(1·2·3·4부 ↔ 5·6·7·8부 ↔ 9부)은 PPT 강의 구성 시에도 동일하게 적용됩니다 — 앞 축은 "가능성과 실행" 강의 시리즈, 뒤 축은 "준비와 거버넌스" 강의 시리즈로 분리하는 기준이 됩니다.

자세한 변환 가이드는 `references/book_to_ppt_workflow.md` 참고.

---

## 7. 작업 시 반드시 확인할 점

### 7.1 한국어 텍스트 처리
한국어 텍스트가 포함된 `<w:t>` 요소는 앞뒤 공백이 있을 경우 반드시 `xml:space="preserve"` 속성을 추가합니다.

### 7.2 스마트 따옴표
새 텍스트의 따옴표는 XML 엔티티로 표기합니다.
- `&#x2018;` ' (왼쪽 작은따옴표)
- `&#x2019;` ' (오른쪽 작은따옴표 / 아포스트로피)
- `&#x201C;` " (왼쪽 큰따옴표)
- `&#x201D;` " (오른쪽 큰따옴표)

### 7.3 검증
pack 후 반드시 다음으로 검증합니다.

```bash
python /mnt/skills/public/docx/scripts/office/validate.py /home/claude/working/book_final.docx
```

검증 실패 시 unpack → 수정 → pack 사이클을 반복합니다.

### 7.4 LibreOffice 한국어 렌더링 주의
LibreOffice로 PDF 변환 시 한국어 폰트가 깨질 수 있습니다. 이 경우 Microsoft Word에서 직접 PDF로 저장하시도록 사용자에게 안내합니다.

### 7.5 자동 번호 매김 비활성화 (중요)

books.dotx의 heading 1(`10`)과 heading 2(`2`) 스타일은 numbering을 자동 부여하도록 설정되어 있습니다.

- heading 1: `numId=46`
- heading 2: `numId=13`
- TOC1(목차 제목)은 heading 2를 `basedOn`으로 하므로 동일한 numId를 상속

장동인교수님은 본문에 직접 "제1부", "1장", "2장" 같은 챕터 번호를 부여하시므로, **자동 번호 매김은 항상 끄는 것이 표준 동작**입니다. 자동 번호를 켜면 "1. 책 기획 의도", "5. 제3부 — ..." 같은 충돌이 발생합니다.

heading 1, heading 2, TOC1 단락에는 다음 XML을 명시적으로 추가하여 자동 번호를 비활성화합니다.

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="10"/>
    <w:numPr>
      <w:ilvl w:val="0"/>
      <w:numId w:val="0"/>
    </w:numPr>
  </w:pPr>
  <w:r><w:t>제1부 — 왜 바이브 코딩이 AX의 핵심 키인가</w:t></w:r>
</w:p>
```

`numId=0`은 numbering의 명시적 비활성화 표시입니다. styles.xml은 그대로 두므로 다른 문서에는 영향이 없습니다.

**예외**: 사용자가 명시적으로 "장 번호를 자동으로 매겨줘"라고 요청한 경우에만 비활성화를 생략합니다.

### 7.6 Bullet과 NumberList numbering은 유지

heading과 달리, Bullet(`numId=7`)과 NumberList(`numId=6`)는 **유지해야 합니다**. 이들은 검은 점 / 숫자 리스트의 시각 표시를 numbering으로 구현하므로, 끄면 그냥 들여쓰기된 단락이 되어버립니다.

---

## 8. 출력 형식 (사용자에게 제시)

작업 완료 후 사용자에게 다음을 알립니다.

1. **파일 위치**: `/mnt/user-data/outputs/<책이름>.docx`
2. **목차 새로 고침 안내**: Word에서 파일을 연 후 F9를 눌러 목차를 자동 생성하시도록 안내
3. **페이지 수**: 대략적인 페이지 수
4. **다음 단계 제안**: PPT 변환을 원하시면 `chang-presentation-brand` 스킬로 자연스럽게 연결

---

## 9. 편집 표준 (기존 .docx 원고 편집 시)

> books.dotx로 생성한 후 또는 외부에서 받은 .docx 원고를 다듬을 때 적용하는 Office.js 기반 편집 규칙입니다.

이 섹션의 규칙은 기존 .docx 원고를 Office.js(Word JavaScript API, `execute_office_js`)로 편집할 때 적용합니다. **신규 생성 시에는 §2~§7의 books.dotx 워크플로우를 따르고, 기존 원고 편집 시에는 본 섹션의 표준을 따릅니다.** 두 워크플로우는 충돌 없이 보완적이며, builder.py로 생성된 원고에도 본 표준이 자연스럽게 적용되도록 설계되어 있습니다.

활성화 조건:
- 사용자가 "책", "원고", "단행본", "도서"라고 부르는 .docx 작업
- `<doc_state>`에 "프롤로그", "제N부", "에필로그", "부록"의 한국어 구조가 보이는 문서
- 사용자가 책 기획·구성·집필 관련 편집을 요청

활성화하지 않는 경우:
- 발표 슬라이드(.pptx) — `chang-presentation-brand` 사용
- 계약서·법무 문서

### 9.1 단락 사이 간격 (line spacing between paragraphs)

본문 단락(Normal, ListParagraph 스타일)의 `spaceAfter`를 **해당 단락 글자 크기의 50%**로 설정합니다. Heading 단락은 자체 스타일 간격을 유지(건드리지 않음).

```javascript
// execute_office_js
const paras = context.document.body.paragraphs;
paras.load("items/styleBuiltIn, items/font/size, items/spaceAfter");
await context.sync();

let touched = 0;
for (const p of paras.items) {
  const s = p.styleBuiltIn;
  if (s === "Normal" || s === "ListParagraph") {
    const sz = p.font.size || 11;  // 본문 기본 11pt
    p.spaceAfter = sz * 0.5;  // points 단위
    touched++;
  }
}
await context.sync();
```

**Done when**: Normal 한 단락을 sample로 load하여 `spaceAfter`가 `font.size × 0.5`와 같음을 확인.

### 9.2 페이지 번호는 푸터의 오른쪽 끝, 부 제목은 왼쪽

각 부(Part)는 별도 섹션이며, 푸터에는 왼쪽에 부 제목, 오른쪽에 페이지 번호가 들어갑니다. 예: `제1부 — 왜 바이브 코딩이 AX의 핵심 키인가    8`

표준 형식:
- **왼쪽 정렬**: 부/장 제목
- **오른쪽 정렬**: 페이지 번호 (Word PAGE 필드 사용 — 리터럴 숫자 금지)

```javascript
// execute_office_js — 섹션별 푸터 설정
const sections = context.document.sections;
sections.load("items");
await context.sync();

for (const section of sections.items) {
  const footer = section.getFooter("Primary");
  footer.clear();
  // 왼쪽 부제목 + 탭 + 페이지 필드
  const partTitle = "제N부 — 부 제목";  // 섹션별로 다르게
  footer.insertText(partTitle + "\t", "Start");
  const endRange = footer.getRange("End");
  endRange.insertField("End", "Page");
}
await context.sync();
```

오른쪽 정렬을 위해서는 푸터 단락에 오른쪽 탭 스톱이 설정되어 있어야 합니다(Word 기본 푸터 스타일에 보통 우측 탭이 잡혀 있음). 안 잡혀 있으면 paragraphFormat을 통해 추가해야 하지만, Word.js에서 탭 스톱 API가 제한적이므로 사용자에게 **"Word에서 푸터 단락의 오른쪽 탭이 페이지 오른쪽 끝에 잡혀 있어야 합니다"**라고 안내합니다.

**Done when**: 푸터 텍스트 read-back 시 부제목 + `\t` + PAGE 필드가 보이고, 인쇄 미리보기에서 페이지 번호가 우측에 위치.

### 9.3 한국어 본문 문체 — 쉬운 말 원칙

CEO/임원 독자가 한 번 읽고 이해할 수 있게 작성합니다.

- **전문 용어 + 괄호 안 쉬운 설명**: `LLM(대규모 언어 모델)`, `EVCP(전사 바이브 코딩 플랫폼, Enterprise Vibe Coding Platform)`, `SI(시스템 통합 사업자)`, `KPI(핵심성과지표)`처럼 첫 등장 시 풀어 줍니다. 두 번째 등장부터는 약어만 사용 가능.
- **외래어 음차 + 한 줄 의미 설명**: `하니스 엔지니어링(Harness Engineering, 에이전트 운용 골격 설계)`, `카오스(Chaos, 무질서한 도입 혼란)`처럼 음차한 다음 의미를 적습니다.
- **불릿 항목 표준 형식**: `**짧은 한국어 제목** (영문 명칭) — 한두 문장 설명. (N부에서 본격 분석)` 형태. 9가지 기술 목록(프롤로그)이 표준입니다.
- **존댓말(~합니다체) 일관 사용**: 책 본문 전체에서 일관되게 사용합니다. 반말·구어체 금지.
- **수동태 회피, 능동태 우선**.
- **숫자는 한글 단위로 보조 설명**: "1만 명 회사에서 평균 3,000개의 미관리 AI가 발견됩니다"처럼 큰 숫자에 단위를 명확화합니다.

### 9.4 의사결정 주체 — 절대 흐리지 말 것

AX(AI 전환)를 설명할 때 모델이 의사결정을 한다는 표현은 금지합니다. 정확한 표현:

- ✅ **"AX는 의사결정의 추론과 옵션 생성을 모델이 담당하고 최종 판단과 책임은 인간이 지는 분업 전환"**
- ❌ "AX는 의사결정 자체를 모델이 수행하는 본질 전환"
- ❌ "AI가 결정한다 / AI가 결단한다"

검토 시 `search_doc_text` 등으로 "의사결정", "결단", "결정"이 모델·AI를 주어로 하는 문장이 있는지 확인합니다.

### 9.5 책 전체 골격 — 두 개의 축

이 책의 일관된 프레임은 두 개의 축입니다. 새 콘텐츠 작성·요약·재구성 시 이 프레임을 흐리지 않아야 합니다.

- **앞 축 (가능성과 실행)**: 현업 바이브 코딩 → 자동화·예측·시뮬레이션·최적화 4단계 가치 → Harness Engineering → AI Native 도약 (1·2·3·4부)
- **뒤 축 (준비와 거버넌스)**: 도메인 지식 오케스트레이션 → 부서별 SOP 재설계 → EVCP 7대 컴포넌트 → 검증의 과학 (5·6·7·8부)
- **결과**: 매출·이익·고객만족·인재의 4가지 폭발 (9부)

핵심 메시지나 프롤로그를 다시 쓸 때 이 구조와 일관되게 정렬합니다.

---

## 10. 편집 워크플로우 체크리스트와 예제

### 10.1 워크플로우 체크리스트

책 원고에 어떤 편집을 수행한 직후 다음을 점검합니다.

1. **단락 간격** — 새로 삽입한 Normal/ListParagraph에 `spaceAfter = font.size × 0.5` 적용했는가
2. **헤딩 스타일** — Heading1(16pt)·Heading2(14pt)·Heading3(12pt) 고수, 직접 `font.size` 오버라이드 금지
3. **문체** — 영문 전문 용어가 첫 등장이면 한국어 풀이를 괄호로 붙였는가
4. **의사결정 주어** — "AI가 결정한다" 류 표현이 들어가지 않았는가
5. **두 개의 축 일관성** — 새 요약/구성 설명이 1·2·3·4부 ↔ 5·6·7·8부 ↔ 9부 골격을 따르는가
6. **푸터** — 부가 새로 추가되었다면 해당 섹션의 푸터에 "부제목 + `\t` + PAGE 필드" 구성이 되어 있는가

### 10.2 예제

**새 단락 삽입 (간격 자동 적용)**

```javascript
const p = anchor.insertParagraph("새 본문 내용입니다.", "After");
p.styleBuiltIn = "Normal";
p.font.name = "맑은 고딕";
const sz = p.font.size || 11;
p.spaceAfter = sz * 0.5;
```

**9가지 기술 형식의 불릿 작성**

`**사내 일하는 방식의 자동 적용 (Harness Engineering)** — 직원마다 다르게 일하던 절차를 회사의 표준으로 자동 적용시키는 장치. 신입 직원도 첫날부터 사내 베테랑 수준의 절차를 따라 일하게 됩니다. (3부에서 본격 분석)`

**부 시작 시 푸터 설정 패턴**

```javascript
const sections = context.document.sections;
sections.load("items");
await context.sync();

const partTitles = [
  "프롤로그 — AX 시대, CEO의 결단",
  "제1부 — 왜 바이브 코딩이 AX의 핵심 키인가",
  "제2부 — 바이브 코딩이 만드는 새로운 가치",
  // ... 섹션 순서대로
];

for (let i = 0; i < sections.items.length; i++) {
  const footer = sections.items[i].getFooter("Primary");
  footer.clear();
  footer.insertText((partTitles[i] || "") + "\t", "Start");
  footer.getRange("End").insertField("End", "Page");
}
await context.sync();
```

---

## 11. 의존성

- **Python** (stdlib만 필요)
- **`/mnt/skills/public/docx/scripts/office/unpack.py`, `pack.py`, `validate.py`** — docx 스킬과 함께 설치
- **books.dotx 템플릿** — 이 스킬의 `assets/`에 동봉

---

## 12. 디렉토리 구조

```
chang-book-template/
├── SKILL.md                          # 이 파일
├── assets/
│   └── books.dotx                    # 장동인 교수의 책 템플릿 원본
├── scripts/
│   ├── builder.py                    # 재사용 가능한 책 빌더 헬퍼 (필수)
│   └── example_build.py              # 사용 예제 (3페이지 미니 책)
└── references/
    ├── style_map.md                  # 전체 스타일 매핑표 (마크다운 ↔ Word)
    └── book_to_ppt_workflow.md       # 책 → PPT 변환 가이드
```
