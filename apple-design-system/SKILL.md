---
name: apple-design-system
description: 애플(Apple) 디자인 시스템 스타일의 프레젠테이션(PPT/PPTX)과 워드 문서(DOCX)를 만들 때 반드시 사용하는 스킬입니다. 사용자가 "애플 스타일", "애플 디자인", "Apple design system", "키노트 스타일", "미니멀 PPT", "애플처럼 깔끔하게" 등을 언급하며 슬라이드·덱·프레젠테이션 또는 Word·docx 문서·핸드북·리포트 제작을 요청하면 명시적으로 스킬 이름을 말하지 않아도 항상 이 스킬을 적용하세요. 애플 특유의 대형 타이포그래피, 넉넉한 여백, 무채색 지배 + 단일 블루 강조, 표지·마지막 장 블랙 / 본문 화이트 배경 규칙을 강제하며, PPTX·DOCX 모든 산출물에 Pretendard 서체를 강제합니다.
---

# Apple Design System — 프레젠테이션·문서 스킬

애플의 디자인 문법으로 **PPTX**와 **DOCX**를 생성하기 위한 규칙 모음입니다. 이 스킬이 활성화되면 아래 규칙은 선택이 아니라 **강제**입니다. 실제 파일 생성 절차(pptxgenjs·python-docx 사용법, 검증, QA)는 범용 pptx/docx 스킬을 함께 따르되, 디자인 결정은 전부 이 문서가 우선합니다.

- 슬라이드를 만들 때 → 1~7절
- Word 문서(.docx)를 만들 때 → 1·2절(배경·토큰) + **9절(DOCX 규칙)**
- **서체는 산출물 종류와 무관하게 언제나 `Pretendard`** (3절). 이 규칙에 예외는 없다.

## 1. 배경 규칙 (최우선 — 예외 없음)

- **표지(첫 번째 슬라이드)와 마지막 슬라이드: 블랙 배경 (`000000`)**
- **그 외 모든 본문 슬라이드: 화이트 배경 (`FFFFFF`)**
- 이 구조를 슬라이드 수와 무관하게 일관되게 유지한다. 중간에 다크 슬라이드를 임의로 넣지 않는다. 사용자가 명시적으로 다른 배경을 요청한 경우에만 예외를 허용한다.
- 블랙 슬라이드의 텍스트: 흰색(`FFFFFF`) 주 텍스트, 회색(`86868B`) 보조 텍스트, 블루(`0071E3`) 강조.
- 화이트 슬라이드의 텍스트: 잉크(`1D1D1F`) 주 텍스트, 회색(`86868B`) 보조 텍스트, 블루(`0071E3`) 강조.

## 2. 디자인 토큰

| 토큰 | 값 | 용도 |
|---|---|---|
| Ink | `1D1D1F` | 화이트 배경의 제목·본문 |
| Gray | `86868B` | 보조 텍스트, 캡션 (양쪽 배경 공통) |
| Surface | `F5F5F7` | 화이트 배경 위 카드·패널 |
| Blue | `0071E3` | 단 하나의 강조색. 링크·버튼 문구·키워드·대형 숫자 |
| Black | `000000` | 표지·마지막 장 배경 전용 |
| White | `FFFFFF` | 본문 배경, 블랙 슬라이드의 주 텍스트 |

- 강조색은 **블루 하나만** 사용한다. 초록·빨강·주황 등 제2의 유채색을 절대 추가하지 않는다.
- Surface 카드는 화이트 배경 위에서만 사용하고, 테두리는 없거나 `E5E5EA` 1pt 이하.

## 3. 타이포그래피

- 서체: **Pretendard** — PPTX·DOCX 모두 예외 없이 고정한다. Arial·맑은 고딕·Segoe UI·Noto Sans KR로 대체하지 않는다.
  - 굵기는 Regular / Bold 두 가지만 쓴다. `Pretendard Light`·`Pretendard SemiBold` 같은 별도 패밀리를 섞지 않는다.
  - 고정폭이 필요한 코드·표 정렬 블록만 `Consolas` 예외.
  - PPTX/DOCX 모두 서체를 임베드하지 않으면 미설치 PC에서 대체된다. 배포용이면 **PDF를 함께 만들거나** Office의 "파일에 글꼴 포함"을 켜도록 안내한다.
  - DOCX는 `w:rFonts`의 `ascii·hAnsi·cs·eastAsia`를 모두 지정해야 한다 → 9절 참조.
- 위계는 크기와 굵기로만 만든다. 밑줄·이탤릭 남용·장식선 금지.

| 요소 | 크기 | 굵기 |
|---|---|---|
| 표지 히어로 타이틀 | 72–96pt | Bold |
| 스테이트먼트(한 줄 선언) | 44–54pt | Bold |
| 본문 슬라이드 제목 | 36–40pt | Bold |
| 카드 제목 | 20–24pt | Bold |
| 본문 | 14–16pt | Regular |
| 캡션 | 12–13pt | Regular, Gray |
| 대형 숫자 콜아웃 | 110–130pt | Bold, Blue |

## 4. 레이아웃 원칙

- **한 화면, 한 메시지.** 내용이 많으면 슬라이드를 나눈다.
- 여백: 좌우 최소 0.9인치, 요소 간 0.3인치 이상. 화면의 40% 이상을 비운다.
- 표지·마지막 장·스테이트먼트·대형 숫자는 **중앙 정렬**, 본문 텍스트는 **좌측 정렬**.
- 카드형 콘텐츠는 라운드 사각형(`roundRect`, rectRadius 0.14–0.16) + Surface 배경.
- 링크성 문구는 블루로 "자세히 보기 ›" 형태.
- 덱 구조 권장: 블랙 표지 → 화이트 본문(스테이트먼트/카드/데이터) → 블랙 클로징.

## 5. 금지 사항

- 제목 아래 장식선(accent line), 색상 바, 사이드 스트라이프 금지
- 그라데이션·과한 그림자·다중 유채색 금지
- 크림/베이지 배경 금지 — 배경은 오직 블랙(표지·마지막)과 화이트(본문)
- 애플 로고, Apple 상표 이미지, 제품 사진의 무단 삽입 금지 (스타일만 차용)
- 본문 슬라이드 중앙 정렬 남용 금지

## 6. pptxgenjs 시작 코드

새 덱을 만들 때 아래 토큰 상수와 배경 패턴으로 시작한다.

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5

const INK = "1D1D1F", GRAY = "86868B", BLUE = "0071E3";
const SURFACE = "F5F5F7", WHITE = "FFFFFF", BLACK = "000000";
const FONT = "Pretendard";   // 예외 없음 (미설치 PC 대비 PDF 병행 배포)

// 표지 — 반드시 블랙
let cover = pres.addSlide();
cover.background = { color: BLACK };

// 본문 — 반드시 화이트
let body = pres.addSlide();
body.background = { color: WHITE };

// 마지막 장 — 반드시 블랙
let closing = pres.addSlide();
closing.background = { color: BLACK };
```

색상 값에 `#`을 붙이지 않는다(파일 손상). 텍스트 정렬이 필요한 곳은 `margin: 0`.

## 7. QA 체크리스트

파일 생성 후 반드시 확인한다.

1. 첫 슬라이드와 마지막 슬라이드 배경이 블랙인가? 나머지가 전부 화이트인가?
2. 모든 텍스트 서체가 Pretendard인가? (Arial·맑은 고딕이 남아 있지 않은지 확인)
3. 유채색이 블루 하나뿐인가?
4. 모든 텍스트가 배경과 충분한 대비를 갖는가? (블랙 배경에 Ink 텍스트 금지)
5. 장식선·색상 바가 없는가?
6. pptx 검증 스크립트(validate.py)를 통과했는가?
7. 슬라이드 이미지를 렌더링해 오버플로·겹침을 눈으로 확인했는가?

## 8. 참고 자산

- `assets/apple_design_sample.pptx` — 이 스킬의 규칙을 모두 적용한 7장짜리 레퍼런스 덱. 레이아웃 패턴(히어로, 스테이트먼트, 타이포 스케일, 컬러 팔레트, 원칙 카드, 대형 숫자, 클로징)이 필요할 때 참조한다.

## 9. Word 문서(.docx) 규칙

슬라이드가 아니라 **문서**를 만들 때 적용한다. 1절(배경)과 2절(토큰)은 그대로 유효하다.

### 9.1 서체 — Pretendard 강제 (예외 없음)

- 본문·제목·표·캡션의 라틴/한글 모두 **`Pretendard`** 를 쓴다. Arial·맑은 고딕·Noto Sans KR로 대체하지 않는다.
- python-docx는 `w:rFonts`의 **`ascii` · `hAnsi` · `cs` · `eastAsia` 네 속성을 모두** `Pretendard`로 지정해야 한글이 다른 서체로 떨어지지 않는다. `run.font.name` 만 설정하면 eastAsia가 비어 한글이 대체된다.
- 유일한 예외는 **고정폭이 필요한 코드·트리·표 정렬 블록**이며 `Consolas`를 쓴다.
- 굵기는 Regular/Bold만 사용한다(Pretendard Light·SemiBold 등 별도 패밀리를 섞지 않는다).

```python
def set_font(run, name='Pretendard', size=10.5, color=INK, bold=False):
    run.font.name, run.font.size, run.font.color.rgb, run.bold = name, Pt(size), color, bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts')) or rpr.insert(0, OxmlElement('w:rFonts'))
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rf.set(qn(attr), name)
    rf.set(qn('w:eastAsia'), 'Consolas' if name == 'Consolas' else 'Pretendard')
```

- Normal·Heading 1~3 스타일에도 같은 서체를 지정한다(`style.element.rPr.rFonts` 의 `eastAsia` 포함).
- **배포 시 주의:** docx는 서체를 임베드하지 않으므로 Pretendard 미설치 PC에서는 대체된다. 배포용이면 **PDF를 함께 생성**하거나 Word의 "파일에 글꼴 포함"을 안내한다.

### 9.2 페이지와 타이포 스케일

- A4, 여백 상하 2.8cm / 좌우 3.0cm 이상. 문서에서도 여백이 디자인이다.
- 바닥글에 페이지 번호만 Gray 9pt 가운데. 머리글은 비운다. 장식선 금지.

| 요소 | 크기 | 색·굵기 |
|---|---|---|
| 표지 타이틀 | 32–36pt | White Bold (블랙 전면) |
| 장(chapter) 제목 | 24–28pt | Ink Bold |
| 절 제목 | 16–18pt | Ink Bold |
| 소제목 | 12–13pt | Ink Bold |
| 본문 | 10.5pt, 줄간 1.5 | Ink |
| 캡션·라벨 | 8.5–9pt | Gray |
| 코드 블록 | 9pt Consolas | Ink on Surface |

### 9.3 표지·마지막 장 — 전면 블랙 구현법

DOCX에는 페이지 단위 배경이 없다. **여백 0인 별도 섹션 + 단일 셀 표**로 만든다.

- 표지/클로징 섹션: 상하좌우 여백 0, 머리글·바닥글 문단을 1pt로 축소(그러지 않으면 본문 높이를 잠식해 빈 페이지가 생긴다).
- 셀: 너비 = 용지 폭(21cm), 행 높이 `exact` 29.3cm, 세로 가운데 정렬, 테두리 없음, 배경 `000000`.
- 표 뒤에 남는 필수 문단은 1pt·행간 고정으로 만들어 페이지가 넘어가지 않게 한다.

### 9.4 본문 요소

- **카드/노트**: 테두리 없는 단일 셀 표 + Surface 배경. 상단에 8.5pt Gray 라벨("주의·팁·정리") 한 줄. 좌측 컬러 스트라이프 금지.
- **표**: 가로선만(`E5E5EA` 0.5pt), 세로선 없음. 머리행은 Surface 배경 + Bold, `tblHeader`로 페이지 넘김 시 반복.
- **목록**: 번호는 Blue Bold, 불릿은 Gray `·`. 들여쓰기 0.75cm 내어쓰기.
- **본문 링크**: Blue, 밑줄 없음.
- 구분선(`<hr>` 성격)은 선을 긋지 말고 **여백으로** 표현한다.
- 목차는 TOC 필드(`TOC \o "1-2" \h \z \u`)를 `dirty="true"`로 넣어 Word가 열 때 갱신하게 한다.

### 9.5 DOCX QA 체크리스트

1. 모든 런의 `eastAsia`가 Pretendard인가? (한글이 맑은 고딕으로 떨어지지 않았는지 육안 확인)
2. 표지·마지막 장이 전면 블랙이며, 그 뒤에 빈 페이지가 생기지 않았는가?
3. 유채색이 Blue 하나뿐인가? 장식선·스트라이프가 없는가?
4. 표에 세로선이 없고 머리행이 반복되는가?
5. PDF로 변환해 **전 페이지를 렌더링**하고 빈 페이지·오버플로·잘린 표를 눈으로 확인했는가?
6. 원본(마크다운·HTML 등)의 텍스트가 누락 없이 옮겨졌는지 자동 대조했는가?
