# 시각 체계와 SVG 계약

builder가 따르고 visual-judge와 `render_check.py`가 검사한다. 색은 chang-ppt 색상 체계와 같은 값을 쓴다(강의 슬라이드에 그대로 넣기 위해서다).

## 캔버스

| 용도 | 크기(px) | 비고 |
| --- | --- | --- |
| 슬라이드·문서 기본 | 1600 × 900 | 16:9, chang-ppt 콘텐츠 영역에 들어간다 |
| 세로 인포그래픽 | 1200 × 1800 | comparison 포스터 |
| 정사각 SNS | 1200 × 1200 | |

- 바깥 여백 64px. 제목 영역은 위 64~150px, 하단 takeaway는 아래 여백 위.
- 8px 격자에 좌표·크기를 맞춘다. 같은 역할 노드는 같은 크기.
- 배경은 테마 배경색 단색. 슬라이드에 넣을 그림은 흰 배경을 기본으로 한다.

## 서체 크기 (1600px 폭 기준, 캔버스 폭에 비례)

| 역할 | 크기 | 굵기 |
| --- | --- | --- |
| headline | 40~44 | Bold |
| subtitle | 22~24 | Regular |
| 그룹·레인·열 머리글 | 22~24 | Bold |
| 노드 label | 20~22 | Bold 또는 SemiBold |
| 노드 sub·설명 | 16~18 | Regular |
| 연결 라벨·주석 | 16 | Regular |
| 출처·각주 | 14 | Regular |

- 최소 14px(1600 폭 기준). 이보다 작아야 들어가면 문구를 줄이거나 그림을 나눈다.
- `font-family="Pretendard, 'Malgun Gothic', sans-serif"`. 코드·명령어는 `Consolas, 'D2Coding', monospace`.
- 한 텍스트 줄은 노드 폭 안에 들어가야 한다. SVG `<text>`는 자동 줄바꿈이 없으므로 `<tspan x=… dy=…>`로 직접 나눈다. 한 노드 최대 3줄.

## 색 (light 테마)

| 역할 | 값 |
| --- | --- |
| 제목·기본 구조·진한 머리글 | #1B2A4A |
| 본문 | #2C3E5A |
| 보조 설명·테두리·muted | #7F8FA9 |
| 브랜드 강조선 | #3A86FF |
| 배경 | #FFFFFF |
| 중립 영역·교차 레인 | #F5F5F7 |
| 핵심(focal)·주요 수치 | 선 #B45309, 배경 #FFF4E8 |
| 성과·권고·이후(NEW) | 선 #0F766E, 배경 #EAF6F3 |
| 주의·확인 필요 | 선 #2563EB, 배경 #EDF3FF |
| 위험·중단·실패 | 선 #355C7D, 배경 #EEF2F6 |
| 범주 추가색(기술 세트) | #7C3AED |

dark 테마(사용자가 원할 때만): 배경 #0F1B33, 카드 #172744, 테두리 #3A4E73, 제목 #FFFFFF, 본문 #E6ECF5, 보조 #A9B6CC, 강조 #3A86FF·#2DD4BF·#F59E0B·#A78BFA. 이 값은 이 스킬의 설계 선택이다.

- 강조색은 한 그림에 1~2개. focal 색은 focal 요소에만.
- 위험을 빨강으로 쓰지 않는다. 색만으로 의미를 전달하지 않고 라벨·선 모양을 함께 쓴다.
- 글자와 배경 대비 4.5:1 이상. 연한 배경 위 글자는 #1B2A4A 또는 #2C3E5A.
- 위 표 밖의 색을 쓰면 명세에 이유를 적는다(자동 검사는 경고로 보고한다).

## 연결선

- 주 흐름 실선 2.5~3px, 되돌림·피드백 점선(`stroke-dasharray="8 6"`), 참조 점선(`2 6`).
- 화살촉은 `<marker>` 하나를 정의해 재사용한다. 크기와 모양을 통일한다.
- 직각 경로(가로·세로 선분)를 기본으로 한다. 선이 노드나 글자를 지나가지 않게 한다. 교차가 불가피하면 1회 이하.
- 끝점은 노드 테두리에 닿게 한다(떨어지거나 안으로 파고들지 않게).
- 연결 라벨은 선 가운데 위에 흰(테마 배경) 바탕 사각형을 깔고 쓴다.

## SVG 작성 계약 (자동 검사가 읽는다)

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
  <defs><marker id="arrow" .../></defs>
  <rect width="1600" height="900" fill="#FFFFFF"/>
  <g data-role="title"><text ...>headline</text></g>
  <g data-group="sales" data-container="true">
    <rect data-box="true" .../><text ...>사업부</text>
  </g>
  <g data-node="review">
    <rect data-box="true" x=".." y=".." width=".." height=".." .../>
    <text ...><tspan ...>주문 검토</tspan><tspan ...>OK/NG 판정</tspan></text>
  </g>
  <g data-edge="review->bom">
    <path d="..." marker-end="url(#arrow)" .../>
    <g data-role="edge-label"><rect .../><text ...>NG</text></g>
  </g>
</svg>
```

- 모든 노드는 `<g data-node="{spec id}">`, 그 안에 테두리 도형 하나에 `data-box="true"`(rect·path·polygon·ellipse). 노드의 글자는 이 도형 안에 있어야 한다.
- 레인·층·열은 `<g data-group="{id}" data-container="true">`. 노드와 겹쳐도 검사에서 제외된다.
- 연결은 `<g data-edge="{from}->{to}">`, 실제 선은 그 안의 첫 `path`·`line`·`polyline`. 시작점은 from 노드, 끝점은 to 노드 테두리에서 12px 이내.
- 이모지를 쓰지 않는다. 렌더러마다 모양·색이 달라 팔레트를 벗어난다. 원문의 이모지 표기(예: 🔴)는 낱말("필수 지적")이나 팔레트 색 도형으로 바꾼다.
- 아이콘은 `data-role="icon"`으로 묶는다. 외부 이미지·폰트 링크·스크립트는 넣지 않는다.
- 사람이 고치기 쉽게 좌표는 정수로, 들여쓰기를 유지한다.
