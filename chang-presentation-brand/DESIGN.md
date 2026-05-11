# DESIGN.md
## chang-presentation-brand v2.1 통합 디자인 시스템

장동인교수 (KAIST 김재철AI대학원 · AIBB LAB) 발표 자료, CAIO 강의 슬라이드, CAIO 웹포털, AI 워크북, LLM 진단도구 등 모든 디지털 자산에 적용되는 통합 비주얼 시스템입니다.

본 문서는 2026년 5월 3일 자로 v2.0(cream canvas)에서 v2.1로 개정된 사양을 정의합니다. v2.1의 핵심 변경은 (1) canvas를 cream(#fffaf0)에서 pure white(#ffffff)로 전환하여 인쇄·빔프로젝터 환경에서의 콘트라스트를 극대화하고, (2) 우상단 대각선 삼각형의 회전을 90°→180°로 조정하여 직각이 우상단 코너에 정확히 위치하도록 하는 것입니다. 헤리티지 frame(좌측 navy stripe, 안쪽 가는 수직선, 상단 가로 실선, 우상단 대각선, 하단 그라디언트)은 유지됩니다.

---

## 1. 브랜드 보이스

### 1.1 정의

기본 분위기는 pure white canvas 위에 dark navy ink 타이포그래피와 saturated single-color 카드가 리듬감 있게 놓이는 구조입니다. KAIST/AIBB LAB의 학문적 권위감(navy)과 AI 시대의 명료함(white + saturated 카드)을 결합합니다.

### 1.2 핵심 특성

(1) Pure white canvas (#ffffff)를 모든 슬라이드와 페이지의 기본 floor로 사용하여 인쇄·빔프로젝터 환경에서의 콘트라스트를 극대화합니다.

(2) Heritage Navy (#1B2A4A)는 좌측 stripe·상단 가로 실선·헤드라인·primary CTA에 사용하는 시그니처 색상입니다.

(3) Heritage Blue (#3A86FF)는 부제목·accent·하단 그라디언트·timeline 진행 바에 사용합니다.

(4) Saturated 6색 feature card palette를 콘텐츠 슬라이드의 강조 블록·통계 카드·핵심 메시지에 사용합니다.

(5) Pretendard Variable(한글) + Inter(영문/숫자)를 weight 500 + negative letter-spacing으로 통일합니다.

(6) **모든 콘텐츠 박스는 square box(border-radius 0)** 입니다. Frame이 직각이면 콘텐츠도 직각이라는 기하학적 문법을 따릅니다.

(7) 96px section spacing으로 여백 리듬을 확보합니다.

(8) Footer와 마지막 슬라이드도 white로 마감하여 dark footer가 끊어내는 일반 SaaS 톤과 차별화합니다.

---

## 2. Heritage Frame (정확한 사양)

장동인교수님의 직접 측정으로 확정된 cm 수치입니다. PPTX 16:9 슬라이드 33.867cm × 19.05cm, HTML 1280px × 720px 기준 환산 비율은 1cm ≈ 37.795px, 1cm = 360,000 EMU입니다.

### 2.1 좌측 굵은 navy stripe

| 항목 | cm | HTML px | PPTX EMU | 색상 |
|---|---|---|---|---|
| 가로 위치 | 0 | 0 | 0 | — |
| 세로 위치 | 0 | 0 | 0 | — |
| 너비 | 약 1.0 | 38 | 360000 | #1B2A4A |
| 높이 | 19.05 (전체) | 720 | 6858000 | #1B2A4A |

### 2.2 좌측 안쪽 가는 수직선

| 항목 | cm | HTML px | PPTX EMU | 색상 |
|---|---|---|---|---|
| 가로 위치 | 1.35 | 51 | 486000 | — |
| 세로 위치 | 0 | 0 | 0 | — |
| 너비 | 0.13 | 5 | 46800 | #1B2A4A |
| 높이 | 2.92 | 110 | 1051200 | #1B2A4A |

### 2.3 상단 가로 실선

| 항목 | cm | HTML px | PPTX EMU | 색상 |
|---|---|---|---|---|
| 가로 위치 | 1.0 | 38 | 360000 | — |
| 세로 위치 | 2.1 | 79 | 756000 | — |
| 너비 | 34.0 | 1288 | 12240000 | #1B2A4A |
| 높이 | 0.13 | 5 | 46800 | #1B2A4A |

핵심 디자인 결정: 가로 실선은 좌측 굵은 stripe(0~38px)의 우측 끝과 정확히 맞닿아 시작합니다(left:38px). 이로써 좌측 stripe과 가로 실선이 빈틈없이 L자 frame을 이루며, 게슈탈트 폐쇄성(Closure) 원리에 따라 청중 무의식에 "공식 문서"의 시각 코드가 안정적으로 전달됩니다.

### 2.4 우상단 옅은 대각선 도형

| 항목 | cm | HTML px | 색상 |
|---|---|---|---|
| 위치 | 우상단 코너 | top:0, right:0 | — |
| 크기 | 약 1.85 × 1.85 | 70 × 70 | #d8e2f0 (옅은 navy gray) |
| 형태 | RIGHT_TRIANGLE, **rotation 180°** | CSS clip-path 또는 border 기법 | — |

핵심: PowerPoint(python-pptx)에서는 RIGHT_TRIANGLE을 180° 회전시켜 직각이 우상단 코너에 정확히 위치하도록 합니다. 빗변은 좌상단↘우하단 방향으로 흐르며, 페이지 번호(우상단)와 시각적으로 정합합니다.

### 2.5 하단 그라디언트 라인

| 항목 | cm | HTML px | 색상 |
|---|---|---|---|
| 가로 위치 | 1.0 (좌측 stripe 우측) | 38 | — |
| 세로 위치 | 19.05 - 0.08 (하단) | bottom:0 | — |
| 너비 | 32.87 | 1242 | — |
| 높이 | 0.08 | 3 | linear-gradient(90deg, #3A86FF 0%, #ffffff 100%) |

---

## 3. 색상 시스템

### 3.1 Heritage (chang-presentation-brand 시그니처)

| Token | HEX | 용도 |
|---|---|---|
| heritage-navy | #1B2A4A | 좌측 stripe, 상단 가로 실선, 헤드라인 본문, primary CTA |
| heritage-blue | #3A86FF | 부제목, 하단 그라디언트, timeline 진행 바, accent |
| heritage-blue-soft | #2C3E5A | 본문 강조, sub-headline |

### 3.2 Surface (Clay 차용)

| Token | HEX | 용도 |
|---|---|---|
| canvas | #ffffff | 모든 슬라이드와 페이지의 기본 배경 |
| surface-soft | #faf5e8 | Footer, CTA 밴드, illust-card 배경 |
| surface-card | #f5f0e0 | cream 카드 (보조 정보) |
| surface-strong | #ebe6d6 | 강조 밴드 |
| hairline | #e5e5e5 | 카드/입력 필드 1px 테두리 |

### 3.3 Brand & Accent (Clay 차용)

| Token | HEX | 권장 용도 |
|---|---|---|
| brand-pink | #ff4d8b | 핵심 통계, 큰 CTA, 매수 시그널 |
| brand-teal | #1a3a3a | Featured 솔루션, 추천 가격티어, 핵심 결론 |
| brand-lavender | #b8a4ed | AI 에이전트, LLM 관련 카드 |
| brand-peach | #ffb084 | 일반 기업 사례, 따뜻한 메시지 |
| brand-ochre | #e8b94a | 강사진, 커뮤니티, 전문가 카드 |
| brand-mint | #a4d4c5 | 일러스트 보조, 작은 배지 |
| brand-coral | #ff6b5a | 하이라이트 강조 |

### 3.4 Text

| Token | HEX | 용도 |
|---|---|---|
| ink | #0a0a0a | 헤드라인, 본문 주요 텍스트 |
| body-strong | #1a1a1a | 강조 본문, lead paragraph |
| body | #3a3a3a | 일반 본문 |
| muted | #6a6a6a | sub-heading, breadcrumb, footer 본문 |
| muted-soft | #9a9a9a | 캡션, 작은 글씨 |
| on-primary | #ffffff | navy/teal/dark 배경 위 텍스트 |

### 3.5 Semantic

| Token | HEX | 용도 |
|---|---|---|
| success | #22c55e | 매수 가격대 진입, 진단 통과 |
| warning | #f59e0b | 고평가 구간, 진단 주의 |
| error | #ef4444 | 검증 오류, 손절 영역 |
| timeline-track | #4a4a4a | 미진행 구간 dark gray 라인 |

### 3.6 색 조합 원칙

(1) 헤드라인은 항상 black(#000000) 또는 heritage-navy 사용. 본문은 body(#3a3a3a) 기본.

(2) 부제목은 heritage-blue + bold(weight 700)로 통일.

(3) 한 페이지 내 saturated 색은 최대 3종까지만 사용.

(4) 같은 saturated 색 카드를 연속 두 번 배치 금지.

(5) 각 saturated 카드의 텍스트 색상 규칙:
- pink, teal, dark 배경 → on-primary (white)
- lavender, peach, ochre, mint, white 배경 → ink (dark)

(6) 좌측 stripe과 상단 가로 실선은 항상 heritage-navy(#1B2A4A)로 고정.

---

## 4. 타이포그래피

### 4.1 폰트 스택

| 용도 | 한글 | 영문/숫자 |
|---|---|---|
| Display | Pretendard Variable, weight 500–700 | Inter, weight 500 |
| Body | Pretendard Variable, weight 400 | Inter, weight 400 |
| Monospace | D2Coding | JetBrains Mono |

Fallback 스택:
- 한글: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, '맑은 고딕', sans-serif
- 영문: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif

### 4.2 Hierarchy

| Token | Web (px) | PPTX (pt) | Weight | Line Height | Letter Spacing | 용도 |
|---|---|---|---|---|---|---|
| display-xl | 72 | 60 | 500 | 1.0 | -2.5px | 표지 메인 타이틀 |
| display-lg | 56 | 44 | 500 | 1.05 | -2px | Section divider |
| display-md | 40 | 32 | 500 | 1.1 | -1px | CTA 밴드 |
| display-sm | 32 | 24 | 600 | 1.15 | -0.5px | feature card 타이틀 |
| **slide-title** | **27** | **20** | **700** | **1.2** | **-0.5px** | **콘텐츠 슬라이드 제목 (black)** |
| **slide-subtitle** | **21** | **16** | **700** | **1.45** | **0** | **콘텐츠 슬라이드 부제목 (heritage-blue)** |
| title-lg | 24 | 20 | 600 | 1.3 | -0.3px | 큰 카드 타이틀 |
| title-md | 18 | 16 | 600 | 1.4 | 0 | 카드 타이틀 |
| title-sm | 16 | 14 | 600 | 1.4 | 0 | 작은 카드 타이틀 |
| body-md | 16 | 14 | 400 | 1.55 | 0 | 일반 본문 |
| body-sm | 14 | 12 | 400 | 1.55 | 0 | footer, 작은 본문 |
| caption | 13 | 11 | 500 | 1.4 | 0 | 캡션, 배지 |
| caption-uppercase | 12 | 10 | 600 | 1.4 | 1.5px | 섹션 라벨 |

### 4.3 원칙

(1) 콘텐츠 슬라이드 제목은 black 20pt, weight 700, 중앙 정렬, 상단 가로 실선 위에 배치.

(2) 부제목은 heritage-blue 16pt, weight 700, 중앙 정렬, 상단 가로 실선 아래 배치.

(3) Display는 weight 500을 절대값으로 고정 (단, 슬라이드 제목·부제목은 700 사용).

(4) 한·영 혼용 시 Pretendard와 Inter 자동 fallback에 위임.

---

## 5. 레이아웃 & 여백

### 5.1 Spacing 토큰

| Token | Value | 용도 |
|---|---|---|
| xxs | 4px | 아이콘-라벨 간격 |
| xs | 8px | 인라인 요소 간격 |
| sm | 12px | 작은 카드 내부 |
| md | 16px | 표준 카드 내부 padding |
| lg | 24px | 카드 간격 |
| xl | 32px | feature card 내부 padding |
| xxl | 48px | 섹션 내 그룹 간 |
| section | 96px | 주요 editorial 섹션 간 |

### 5.2 콘텐츠 영역

(1) 콘텐츠 영역 좌우 여백: left:96px, right:96px (PPTX 기준 약 2.54cm)

(2) 콘텐츠 영역 상단: top:200px (PPTX 기준 약 5.29cm) — 가로 실선 79px + 부제목 영역 + 여백

(3) 콘텐츠 영역 하단: bottom:60px (footer 영역 위)

(4) 16:9 PPTX 표준: 13.333" × 7.5", 콘텐츠 영역 내부 약 28.78cm × 14.41cm

---

## 6. 형태 (Shape)

### 6.1 핵심 원칙: Square Box

**Frame이 직각이면 콘텐츠도 직각**입니다. chang-presentation-brand의 navy 직각 frame이 시그니처이므로, 콘텐츠 박스(stat-card, compare-card, chart-card, insight-card, pyramid-layer, illust-card 등)는 모두 border-radius 0의 square box로 통일합니다.

이는 Clay.com의 24px 둥근 모서리 시스템과 가장 큰 차이점입니다. Clay는 frame이 없으므로 카드를 둥글게 처리해도 충돌하지 않지만, chang-presentation-brand는 직각 frame과 통합되려면 모든 박스가 직각이어야 합니다.

### 6.2 예외 (원형 유지)

(1) timeline-node — 번호를 담는 원형 (border-radius:50%)

(2) bullet point dot — 작은 원형 마커 (8×8px brand-pink)

(3) 인물 사진 마스킹 — 원형(아바타) 사용 가능

이 외 모든 사각형 콘텐츠는 직각 모서리를 유지합니다.

---

## 7. 슬라이드 패턴 6종

각 패턴은 모두 동일한 헤리티지 frame을 공유하며, 콘텐츠 영역(top:200px, left/right:96px)만 다양화됩니다.

### 7.1 통계 콜아웃 (Statistics Callout)

3개의 saturated 카드를 grid로 배치하여 핵심 통계를 시각화합니다. Inter 84pt 큰 숫자가 voltage 핵심입니다.

구성 요소: 3 stat-cards (pink/teal/ochre 권장 조합) → 각 카드는 [상단 라벨 + 큰 숫자 + 단위 + 하단 설명] 4 layer

### 7.2 비교 표 (Comparison Table)

좌우 2칼럼 카드로 두 옵션을 비교합니다. 우측 카드를 brand-teal로 featured 처리하고 우상단 pink "Featured" 배지를 배치합니다.

### 7.3 차트 + 인사이트 (Chart + Insight)

좌측 1.4 비율 chart-card(white 배경 + hairline 테두리)에 막대 그래프, 우측 1.0 비율 lavender insight-card에 핵심 메시지 + 본문을 배치합니다.

### 7.4 다이어그램 (Diagram)

5계층 메모리 등 계층 구조를 가로형 계단으로 시각화합니다. 위에서 아래로 60% → 70% → 82% → 92% → 100% 너비로 점증, 각 계층마다 [이름 + 설명 + 스펙] 3 column grid.

### 7.5 이미지 + 텍스트 (Image + Text)

좌측 1.15 비율 illust-card(surface-soft 배경)에 SVG 일러스트 또는 3D claymation, 우측 1.0 비율 텍스트 영역 [eyebrow + 헤드라인 + 본문 + bullet 4개].

### 7.6 타임라인 (Timeline)

4개 노드를 가로축에 배치하고 진행률을 heritage-blue + dark gray(#4a4a4a)로 시각화합니다. 라벨은 위·아래 교차 배치로 시각 리듬을 확보합니다.

---

## 8. 컴포넌트

### 8.1 Buttons

(1) button-primary — heritage-navy 배경, white 텍스트, padding 12×20, 직각 모서리

(2) button-secondary — canvas 배경, ink 텍스트, 1px hairline

(3) button-on-color — saturated 카드 위에 white 배경 반전 사용

### 8.2 Cards

(1) stat-card-{pink|teal|ochre|lavender|peach|mint|coral} — saturated 색 배경, padding 32×30, square

(2) compare-card / compare-card.featured — white 또는 teal 배경, padding 28×30

(3) chart-card — white 배경, 1px hairline, padding 24×28

(4) insight-card — lavender 배경, padding 28

(5) pyramid-layer — saturated 색 layer, padding 10×22, height 56

(6) illust-card — surface-soft 배경, SVG 또는 이미지 100% 채움

### 8.3 Inputs

(1) text-input — canvas 배경, 1px hairline, padding 12×16, height 44, square

### 8.4 Badges

(1) compare-badge — pink 배경, white 텍스트, padding 6×14, square

### 8.5 Footer

(1) footer 형식: "장동인 | KAIST 김재철AI대학원 · AIBB LAB"

(2) 페이지 번호: 우상단 13px Inter, muted 색상

---

## 9. Do's and Don'ts

### 9.1 Do

(1) 모든 페이지를 white canvas(#ffffff)에 anchor.

(2) 좌측 굵은 navy stripe + 안쪽 가는 짧은 수직선 + 상단 가로 실선의 정확한 cm 사양 준수.

(3) 좌측 stripe과 상단 가로 실선이 38px 지점에서 정확히 맞닿도록 배치(L자 폐쇄).

(4) 콘텐츠 슬라이드 제목은 black 20pt 700, 부제목은 heritage-blue 16pt 700, 모두 중앙 정렬.

(5) saturated 카드 6색을 페이지 내 최대 3종, 동일 색 연속 배치 금지.

(6) 모든 콘텐츠 박스를 square box(border-radius 0)로 통일.

(7) Footer는 "장동인 | KAIST 김재철AI대학원 · AIBB LAB" 형식.

(8) 페이지 번호는 우상단 Inter 13px.

### 9.2 Don't

(1) cool gray·cream·기타 톤 canvas 사용 금지. 배경은 항상 white(#ffffff)로 고정.

(2) 가로 실선을 좌측 stripe과 떨어뜨려 배치 금지 (L자 폐쇄 깨짐).

(3) saturated 카드를 6색 외 추가 금지.

(4) 콘텐츠 박스에 둥근 모서리 사용 금지.

(5) 같은 brand 색 카드 연속 두 번 배치 금지.

(6) 슬라이드 제목 아래 강조선 그리기 금지 (이미 가로 실선이 있음).

(7) 본문 텍스트 가운데 정렬 금지 (좌측 정렬 원칙).

(8) Footer/Thank You 슬라이드에 dark navy 배경 금지.

(9) 헤드라인-본문 간 폰트 family 혼용 금지.

---

## 10. 구현 토큰

### 10.1 CSS Variables (CAIO 웹포털용)

```css
:root {
  /* Heritage */
  --color-heritage-navy: #1B2A4A;
  --color-heritage-blue: #3A86FF;
  --color-heritage-blue-soft: #2C3E5A;

  /* Surface */
  --color-canvas: #ffffff;
  --color-surface-soft: #faf5e8;
  --color-surface-card: #f5f0e0;
  --color-surface-strong: #ebe6d6;
  --color-hairline: #e5e5e5;

  /* Brand */
  --color-brand-pink: #ff4d8b;
  --color-brand-teal: #1a3a3a;
  --color-brand-lavender: #b8a4ed;
  --color-brand-peach: #ffb084;
  --color-brand-ochre: #e8b94a;
  --color-brand-mint: #a4d4c5;
  --color-brand-coral: #ff6b5a;

  /* Text */
  --color-ink: #0a0a0a;
  --color-body-strong: #1a1a1a;
  --color-body: #3a3a3a;
  --color-muted: #6a6a6a;
  --color-muted-soft: #9a9a9a;
  --color-on-primary: #ffffff;

  /* Semantic */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-timeline-track: #4a4a4a;

  /* Spacing */
  --space-xxs: 4px; --space-xs: 8px; --space-sm: 12px;
  --space-md: 16px; --space-lg: 24px; --space-xl: 32px;
  --space-xxl: 48px; --space-section: 96px;

  /* Font */
  --font-display: 'Pretendard Variable', Inter, -apple-system, sans-serif;
  --font-body: 'Pretendard Variable', Inter, -apple-system, sans-serif;
  --font-mono: 'D2Coding', 'JetBrains Mono', monospace;
}
```

### 10.2 PPTX EMU 정수표

PPTX OOXML XML 작성 시 사용. 1cm = 360,000 EMU.

| 요소 | x (EMU) | y (EMU) | width (EMU) | height (EMU) |
|---|---|---|---|---|
| 슬라이드 자체 | 0 | 0 | 12192000 | 6858000 |
| 좌측 굵은 stripe | 0 | 0 | 360000 | 6858000 |
| 좌측 안쪽 수직선 | 486000 | 0 | 46800 | 1051200 |
| 상단 가로 실선 | 360000 | 756000 | 12240000 | 46800 |
| 우상단 대각선 (rotation 180°) | 11530000 | 0 | 660000 | 660000 |
| 하단 그라디언트 | 360000 | 6829800 | 11832000 | 28200 |

---

## 11. 버전 이력

### v2.1 (2026-05-03) — 본 문서

(1) Canvas 색상을 cream(#fffaf0)에서 pure white(#ffffff)로 전환. 인쇄·빔프로젝터 환경에서의 콘트라스트 극대화가 목적이며, 모든 슬라이드/페이지의 기본 background는 white로 고정.

(2) 우상단 옅은 대각선 도형의 회전 사양을 90°→180°로 조정. RIGHT_TRIANGLE의 직각이 우상단 코너에 정확히 위치하여 페이지 번호와 시각적으로 정합.

(3) 하단 그라디언트 라인의 종점 색상을 #fffaf0→#ffffff로 동기화.

(4) "v2.0의 cream-tinted 따뜻함"을 "v2.1의 pure white 명료함"으로 브랜드 보이스 재정의.

### v2.0 (2026-05-03)

(1) v1.0 cool-gray canvas → cream canvas (#fffaf0) 전면 전환

(2) Clay.com의 saturated 6색 카드 시스템 차용

(3) 한글 폰트 맑은 고딕 → Pretendard Variable 1순위 변경

(4) 콘텐츠 박스를 square box로 통일 (둥근 모서리 제거)

(5) 부제목 색상을 black → heritage-blue bold로 변경

(6) 헤리티지 frame의 정확한 cm 사양 확정 (좌측 stripe 1.0cm, 안쪽 수직선 0.13×2.92cm at 1.35cm, 가로 실선 0.13×34cm at y=2.1cm)

(7) Timeline 미진행 구간 색상을 surface-strong → dark gray(#4a4a4a)로 변경

(8) 6종 슬라이드 패턴 표준화 (Statistics, Comparison, Chart+Insight, Diagram, Image+Text, Timeline)

### v1.0 (이전)

cool-gray canvas + heritage navy 단일톤. 둥근 모서리 사용. 한글 맑은 고딕 + 영문 Segoe UI.

---

본 문서는 v2.1로, 2026년 5월 3일 자 chang-presentation-brand 디자인 시스템 공식 사양입니다. 향후 발견되는 시각적 충돌, 한글 가독성 이슈, PPTX 렌더링 차이를 반영하여 v2.x로 점진 개선됩니다.
