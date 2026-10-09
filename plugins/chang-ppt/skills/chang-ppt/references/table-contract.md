# 표 자동화 계약

## 기본 규격

- 헤더는 네이비·흰 글씨 14pt Bold, 본문은 14pt Regular(강조 셀 Bold 허용)로 작성하라. 색상 정의는 color-system.md를 따른다.
- 본문 행은 중립색·흰색 교차, 모든 경계는 회청색 0.5pt 실선으로 처리하라.
- 셀 여백은 좌우 0.1, 상하 0.03인치, 세로는 가운데 정렬이다.
- 열 폭은 실제 런별 Pretendard 렌더 폭 × 1.04 + 좌우 여백 + 0.08인치 여유로 계산한다.
- 폭이 부족하면 보호하지 않은 넓은 열부터 조정한다. 최소 폭은 자연 폭 이하에서 자연 폭의 50% 또는 0.6인치 중 큰 값이다. 짧은 값·식별자 열은 protected_columns로 보호하라.
- 보호 폭으로도 들어가지 않으면 축약·표 분할을 요청하라. 전체 열 비례 축소나 글자 축소로 해결하지 말라.

## 실행

기본 실행은 커버·프로필·마지막 페이지를 제외하고 표를 가용 영역의 가로 중앙에 배치한다. 세 장보다 적은 시험 파일은 콘텐츠를 적절한 위치에 추가하라.

```powershell
python brand_tables.py input.pptx output.pptx
python brand_tables.py input.pptx output.pptx --config table-layout.json
```

python-pptx, Pillow, lxml과 실제 Pretendard Regular/Bold TTF 또는 OTF가 필요하다. 폰트 경로는 CHANG_PPT_FONT_DIR 환경변수로 지정할 수 있다. 코드 서체는 표 피팅에 사용하지 않는다. 표 안에 긴 코드가 필요하면 별도 코드 블록으로 분리하라.

## 복합 배치 설정

```json
{
  "tables": {
    "3:1": {
      "area_left": 0.8,
      "area_width": 6.5,
      "align": "preserve",
      "protected_columns": [0],
      "header_fill": "1B2A4A",
      "preserve_cell_fills": true,
      "preserve_text_colors": true,
      "companions": ["TableCaption"]
    },
    "4:1": {"skip": true}
  }
}
```

- 키는 1부터 세는 슬라이드 번호:그 슬라이드의 표 번호다. 고정 페이지 설정은 오류로 보고한다.
- area_left/area_width는 표가 차지할 수 있는 영역의 인치 값이다. 복합 화면에서는 반드시 지정하라.
- align=center는 지정 영역 중앙으로 이동한다. preserve는 현재 left를 유지한다. 둘 다 영역 밖이면 오류를 낸다.
- protected_columns는 0부터 세는 열 인덱스다. 줄바꿈하면 안 되는 값을 명시하라.
- preserve_cell_fills/text_colors로 이미 승인된 강조색을 보존하라. 이 옵션은 새 색의 적합성을 검증하지 않는다. 제작자가 대비와 팔레트를 확인해야 한다.
- companions는 함께 수평 이동할 캡션 등의 고유 shape.name이다. 이름 중복·누락은 오류다. 표의 폭 변경 후 캡션 폭과 내부 텍스트 정렬은 제작자가 조정하라.
- 합쳐진 셀은 자동 피팅에서 지원하지 않는다. skip으로 제외하고 수동 검토하라.

## 보장 범위와 한계

코드는 서체·기본 크기·헤더·교차 배경·테두리·여백·세로 정렬·ASCII 언어·열 폭·수평 배치를 적용한다. 원본 고정 페이지는 처리하지 않는다. 행 높이·단어 단위 줄바꿈·캡션 폭·전체 콘텐츠의 수직 중앙 배치·마스터 침범은 자동 보장하지 않는다.

저장 후 반드시 렌더링하여 검토하라. 오류가 발생하면 새 출력 파일을 저장하지 않지만 기존 출력 파일을 삭제하지도 않는다. 종료 코드를 확인하고 오래된 파일을 성공 결과로 사용하지 말라.
