# 마크다운 ↔ Word 스타일 전체 매핑표

이 문서는 `chang-book-template` 스킬에서 사용하는 모든 스타일의 매핑을 정리합니다. 작업 시 이 표를 기준으로 마크다운 또는 사용자 지시를 Word XML로 변환합니다.

## 1. 표지 영역 (Cover)

| 요소 | 스타일 ID | 스타일 이름 | 폰트/크기 | 비고 |
|------|----------|-------------|----------|------|
| 메인 타이틀 | `11` | 책 제목1 | Book Antiqua, 68pt | 표지 가장 큰 텍스트 |
| 부제 | `Char` | 부제 Char | (run 스타일) | 메인 타이틀 보조 |
| 저자 | `a2` | Body Text | 기본 본문 | "장동인 (Dong In Chang)" |
| Version | `Version` | Version | Book Antiqua, 18pt, Bold | 버전 정보 |
| 날짜 | `13` | 날짜1 | (커스텀) | 출간일/작성일 |
| 타이틀 바 | `TitleBar` | Title Bar | 36pt | 부속 장식 영역 |

## 2. 목차 영역 (Table of Contents)

| 요소 | 스타일 ID | 스타일 이름 | 비고 |
|------|----------|-------------|------|
| "목차" 제목 | `TOC1` | TOC 제목1 | 목차 섹션의 메인 타이틀 |
| TOC 1단 | `12` | toc 1 | Times New Roman Bold |
| TOC 2단 | `20` | toc 2 | (자동 생성) |
| TOC 3단 | `30` | toc 3 | (자동 생성) |
| TOC 4단 | `40` | toc 4 | (자동 생성) |
| TOC 5단 | `50` | toc 5 | (자동 생성) |

목차는 사용자가 직접 작성하지 않고 Word 필드(`TOC \o "1-3" \h \z \u`)를 삽입한 후 F9로 자동 생성합니다.

## 3. 챕터 본문 (Body)

### 3.1 제목 위계

| 마크다운 | 스타일 ID | 스타일 이름 | 폰트/크기 | 자동 페이지 분리 |
|---------|----------|-------------|----------|-----------------|
| 챕터 표지 (별도) | `ChapterTitle` | Chapter Title | (커스텀) | 예 |
| `# 제목` | `10` | heading 1 | MajorHAnsi, 48pt | 예 |
| `## 제목` | `2` | heading 2 | MajorHAnsi, 36pt, Bold | 예 |
| `### 제목` | `3` | heading 3 | 28pt, Bold, 검정 | 아니오 |
| `#### 제목` | `4` | heading 4 | MajorHAnsi, 24pt, Bold | 아니오 |
| `##### 제목` | `5` | heading 5 | MajorHAnsi | 아니오 |
| `###### 제목` | `6` | heading 6 | Bold | 아니오 |

### 3.2 본문 단락

| 마크다운 | 스타일 ID | 스타일 이름 | 용도 |
|---------|----------|-------------|------|
| 일반 단락 (기본) | `a2` | Body Text | 가장 흔히 쓰는 본문 |
| 들여쓰기 단락 (Ctrl+=) | `a6` | Normal Indent | 인용·예시·중첩 본문 |
| Body Text Indent | `af` | Body Text Indent | 보조 들여쓰기 본문 |
| Hanging Indent | `hangingindent` | hanging indent | 행걸이 들여쓰기 |

### 3.3 리스트

| 마크다운 | 스타일 ID | 스타일 이름 | 용도 |
|---------|----------|-------------|------|
| `- 항목` | `Bullet` | Bullet | 기본 검은 bullet (Ctrl+7) |
| `1. 항목` | `NumberList` | Number List | 번호 리스트 (Ctrl+6) |
| 추가 들여쓰기 bullet | `21` | List 2 | 2단 리스트 |
| 추가 bullet | `22` | List Bullet 2 | 2단 bullet |
| `ae` (List Bullet) | `ae` | List Bullet | Word 기본 bullet |
| `af5` (List Paragraph) | `af5` | List Paragraph | 일반 리스트 단락 |

### 3.4 강조·박스

| 마크다운/지시 | 스타일 ID | 스타일 이름 | 용도 |
|--------------|----------|-------------|------|
| 강조 박스 (Ctrl+8) | `InfoBox` | Info Box | 가운데 정렬 강조 박스 |
| 인사이트 박스 | `af6` | 생각할점 | 책 특유의 사고 유도 박스 |
| `**파란강조**` | (run 스타일) `HighlightedVariable` | Highlighted Variable | 파란색 인라인 강조 |
| 굵은 글씨 | (run 스타일) `af9` | Strong | `<w:b/>` 또는 Strong run 스타일 |
| 강조 (이탤릭) | (run 스타일) `af4` | Emphasis | `<w:i/>` 또는 Emphasis run 스타일 |
| 미묘한 강조 | (run 스타일) `af3` | Subtle Emphasis | 약한 강조 |
| 강한 강조 | (run 스타일) `afa` | Intense Emphasis | 매우 강한 강조 |
| 강한 인용 | `af7` | Intense Reference | 인용/참조 강조 |

### 3.5 표

| 요소 | 스타일 ID | 스타일 이름 | 비고 |
|------|----------|-------------|------|
| 표 본문 | `TableText` | Table Text | 16pt |
| 표 헤더 | `TableHeading` | Table Heading | Bold |

### 3.6 부속 요소

| 요소 | 스타일 ID | 스타일 이름 | 비고 |
|------|----------|-------------|------|
| 이미지 캡션 | `af8` | 이미지 | 이미지 아래 캡션 |
| 일반 캡션 | `a8` | caption | 굴림체, 16pt |
| Footer (홀수) | `FooterOdd` | Footer Odd | Book Antiqua, 16pt |
| Footer (짝수) | `FooterEven` | Footer Even | Book Antiqua, 16pt |
| Footer (기본) | `aa` | footer | |
| Header | `a9` | header | 16pt |
| 페이지 번호 | `a7` | page number | Book Antiqua, 16pt |
| 각주 참조 | `ab` | footnote reference | 16pt |
| 각주 본문 | `ac` | footnote text | |

### 3.7 체크리스트

| 마크다운 | 스타일 ID | 스타일 이름 | 비고 |
|---------|----------|-------------|------|
| `- [x] 항목` | `Checklist` | Checklist | 체크된 항목 |
| `- [ ] 항목` | `Checklist-X` | Checklist-X | 미체크 항목 |

### 3.8 기타 특수 스타일

| 스타일 ID | 스타일 이름 | 용도 |
|----------|-------------|------|
| `Legal` | Legal | 법적 고지 단락 |
| `HeadingBar` | Heading Bar | 제목 위/아래 흰색 바 (장식) |
| `tty80`, `tty132`, `tty180` | tty 계열 | 모노스페이스 (코드용으로 추정) |
| `tty80indent` | tty80 indent | 들여쓰기된 모노스페이스 |
| `039cm1` | 스타일 캡션 + 들여쓰기 | 0.39cm 들여쓰기 캡션 |

## 4. XML 작성 패턴

### 4.1 일반 단락

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="a2"/>
  </w:pPr>
  <w:r>
    <w:t>본문 내용입니다.</w:t>
  </w:r>
</w:p>
```

### 4.2 인라인 강조 (파란 강조)

```xml
<w:p>
  <w:pPr><w:pStyle w:val="a2"/></w:pPr>
  <w:r><w:t xml:space="preserve">일반 본문에 </w:t></w:r>
  <w:r>
    <w:rPr><w:rStyle w:val="HighlightedVariable"/></w:rPr>
    <w:t>파란색 강조</w:t>
  </w:r>
  <w:r><w:t xml:space="preserve"> 텍스트입니다.</w:t></w:r>
</w:p>
```

### 4.3 굵은 글씨 (run-level bold)

```xml
<w:r>
  <w:rPr><w:b/></w:rPr>
  <w:t>굵은 글씨</w:t>
</w:r>
```

### 4.4 챕터 시작 (자동 페이지 분리 포함)

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="10"/>
  </w:pPr>
  <w:r>
    <w:t>1장. 바이브 코딩이란 무엇인가</w:t>
  </w:r>
</w:p>
```

heading 1 스타일이 페이지 분리를 자동으로 처리하므로 별도 page break는 필요 없습니다.

### 4.5 명시적 페이지 분리

```xml
<w:p>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
```

### 4.6 Bullet 리스트

```xml
<w:p>
  <w:pPr><w:pStyle w:val="Bullet"/></w:pPr>
  <w:r><w:t>첫 번째 항목</w:t></w:r>
</w:p>
<w:p>
  <w:pPr><w:pStyle w:val="Bullet"/></w:pPr>
  <w:r><w:t>두 번째 항목</w:t></w:r>
</w:p>
```

### 4.7 InfoBox 강조 박스

```xml
<w:p>
  <w:pPr><w:pStyle w:val="InfoBox"/></w:pPr>
  <w:r><w:t>이 부분은 강조 박스입니다.</w:t></w:r>
</w:p>
```

## 5. 작업 시 흔한 실수 방지

1. **`<w:body>` 끝의 `<w:sectPr>`은 절대 삭제하지 말 것**: 페이지 크기, 짝수/홀수 footer 설정이 들어있습니다.
2. **`<w:t>`에 공백이 포함되면 `xml:space="preserve"` 추가**: 공백이 사라집니다.
3. **스타일 ID는 정확히 일치해야 함**: `"10"`은 heading 1이고 `"1"`은 그냥 "스타일1"입니다(일반 본문 아님).
4. **한 단락 = 하나의 `<w:p>`**: 줄바꿈을 위해 `<w:p>`를 분리하지, `<w:br/>`을 함부로 쓰지 마세요.
5. **표(table)는 `<w:tbl>` 안에 `<w:tr>`, `<w:tc>`**: 단락이 아닙니다.
