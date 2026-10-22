# 대화 요약과 스토리 설계

distiller가 읽고, story-judge가 대조 기준으로 읽는다. 목표는 대화 전체의 축소판이 아니라 대화가 도달한 결론 하나를 그림으로 증명하는 것이다.

## 1. 원문에서 뽑을 것

`00_source.md`를 끝까지 읽고 아래를 발화 번호와 함께 표로 뽑는다. 원문에 없는 항목은 비워 두고 채워 넣지 않는다.

| 항목 | 질문 | 예 |
| --- | --- | --- |
| 핵심 질문 | 이 대화는 무엇을 알아내려 했나 | 우리 회사 주문 처리는 어디서 막히나 |
| 결론 | 대화가 합의·도달한 답은 무엇인가 | 주문 검토 NG가 BOM 재작성으로 되돌아가 지연된다 |
| 주체 | 누가 행동하나(사람·부서·시스템·에이전트) | 사업부, 공학과, PMC |
| 대상물 | 무엇이 오가나(문서·데이터·코드) | 고객 요구표, BOM, 가격 제시 문서 |
| 행위·단계 | 어떤 순서로 무엇을 하나 | 문의 → 요구표 → BOM → 견적 |
| 분기·조건 | 어디서 갈라지나, 기준은 | 주문 검토 OK/NG |
| 대비 | 전과 후, 기존과 신규가 어떻게 다른가 | 실행자 → 시스템 설계자 |
| 수치·기준 | 그림에 넣을 숫자, 기한, 단위 | 3일 이내 |
| 사용자 표현 | 사용자가 직접 고르거나 강조한 말 | "하네스", "B2A" |

- AI의 제안 중 사용자가 받아들이지 않았거나 수정한 내용은 결론이 아니다. 최종 합의 버전을 쓴다.
- 대화 중 바뀐 내용은 마지막 결정을 쓰고, 바뀐 사실이 메시지의 일부면 대비로 표현한다.
- 사용자 표현은 고쳐 쓰지 않는다. 그림을 볼 사람이 대화 참여자이기 때문이다.

## 2. 스토리 아크 고르기

결론이 어떤 관계를 주장하는지로 아크를 고른다. 겉모양(단계가 몇 개인지)이 아니라 주장의 형태가 기준이다.

| 아크 | 주장의 형태 | 기본 유형 |
| --- | --- | --- |
| 흐름 | A를 거쳐 B가 된다 | linear-process, cycle |
| 책임 | 누가 언제 무엇을 넘긴다 | swimlane |
| 시간 | 언제 무엇이 일어난다/일어날 것이다 | timeline |
| 변화 | 이전과 이후가 이렇게 다르다 | comparison |
| 구조 | 무엇이 무엇 위에서/안에서 동작한다 | architecture, hub-spoke |
| 선택 | 조건에 따라 길이 갈린다 | decision |

하나의 그림에는 아크 하나가 주인이다. 보조 아크는 한 요소로만 얹는다(예: 프로세스 위에 피드백 루프 하나). 두 주장이 대등하면 그림을 두 장으로 나누자고 제안한다.

## 3. 고르고 버리기

- 주 단위(단계·레인·카드·층)는 5~7개를 기본으로 하고 9개를 넘기지 않는다. 넘치면 묶거나 분할한다.
- 각 요소에 포함 근거(발화 번호)를 단다. 근거 없는 요소는 넣지 않는다. 일반 상식으로 보강해야 그림이 성립하면 `assumed: true`로 표시하고 보고한다.
- 결론을 증명하는 데 필요 없는 세부는 제외 목록에 이유와 함께 적는다. story-judge가 누락과 의도적 제외를 구분하는 데 쓴다.

## 4. 메시지 쓰기

- **headline**: 주장형 문장, 20자 안팎. "주문 처리 프로세스"(주제) 대신 "주문 검토 NG가 리드타임을 늘린다"(주장). 사용자가 제목을 지정했으면 따른다.
- **subtitle**: 선택. 범위·전제 한 줄.
- **focal point**: 시선이 처음 닿아야 할 요소 하나(id). 핵심 강조색은 여기에만 쓴다.
- **reading path**: 시선이 지나갈 순서(id 목록). 좌→우 또는 위→아래를 기본으로 한다.
- **takeaway**: 그림 하단 한 줄 결론(선택). headline을 반복하지 않고 "그래서 무엇을 하나"를 쓴다.

## 5. 산출물

### 01_story.md

1. 핵심 질문 / 결론 / 청중과 용도
2. 원문 추출 표(1절)
3. 아크와 유형, 고른 이유, 탈락시킨 후보 유형과 이유. comparison을 골랐으면 [diagram-types.md](diagram-types.md)「대비형 쏠림 막기」 세 질문의 답
4. headline, subtitle, focal point, reading path, takeaway
5. 포함 목록(요소 id ↔ 발화 번호), 제외 목록(내용 ↔ 이유), 가정 목록
6. 5초 테스트 문장: 처음 보는 사람이 5초 뒤 말해야 할 한 문장

### 01_spec.json

```json
{
  "type": "swimlane",
  "canvas": {"width": 1600, "height": 900, "theme": "light"},
  "headline": "주문 검토 NG가 리드타임을 늘린다",
  "subtitle": "고객 문의부터 배송 결제까지 5개 부서",
  "focal": "review",
  "reading_path": ["inquiry", "req", "bom", "quote", "review", "ship"],
  "palette_set": "기본 비즈니스",
  "groups": [{"id": "sales", "label": "사업부", "kind": "lane"}],
  "nodes": [
    {"id": "review", "label": "주문 검토", "sub": "OK/NG 판정", "group": "sales",
     "shape": "decision", "role": "focal", "source": ["T7", "T9"]}
  ],
  "edges": [
    {"from": "review", "to": "bom", "label": "NG", "style": "dashed", "source": ["T9"]}
  ],
  "annotations": [{"id": "note1", "text": "...", "near": "review", "source": ["T10"]}],
  "takeaway": "NG 기준을 견적 단계로 앞당기면 재작업이 줄어든다",
  "assumed": []
}
```

- `label`은 12자 안팎, `sub`는 20자 안팎. 길면 줄이는 쪽을 택하고 원문 표현은 `sub`나 주석으로 옮긴다. `sub`의 `\n`은 줄바꿈 지시다. 수치와 단위, 화살표 앞뒤는 한 줄에 둔다.
- 줄 수 상한은 `00_packet.md`의 `density`를 따른다: `normal`은 본문 3줄, `dense`는 본문 5줄. 상한을 넘기면 문구를 줄이거나 그림을 나눈다.
- `role`: `focal`(1개), `normal`, `muted`(맥락용 흐린 요소).
- `shape`: `box`, `pill`, `decision`, `doc`, `db`, `actor`, `card`, `layer`, `milestone`.
- `style`: `solid`(주 흐름), `dashed`(되돌림·피드백·선택), `dotted`(참조·영향).
- 방향이 없는 연결(대비·짝)은 `"undirected": true`를 단다. builder는 화살촉 없이 그린다.
- 유형별 필수 필드는 [diagram-types.md](diagram-types.md)를 따른다. 필드 이름을 새로 만들지 않는다. 그룹은 `groups[].kind`(`lane`, `layer`, `zone`, `column`, `row`), 노드의 소속은 `group` 또는 comparison의 `column`·`row`, 카드 꼬리표는 `tag`, 주석 위치는 `near` 또는 `placement`(`bottom-band`, `top-band`)만 쓴다. 꼭 필요한 새 필드는 `01_story.md`에 뜻을 적는다.

### comparison 예시 (same_time)

```json
{
  "type": "comparison", "contrast_mode": "same_time",
  "canvas": {"width": 1600, "height": 900, "theme": "light"},
  "groups": [
    {"id": "bench", "label": "벤치마크", "kind": "column"},
    {"id": "top", "label": "최고 성과", "kind": "row"},
    {"id": "low", "label": "아직 약한 곳", "kind": "row"}
  ],
  "nodes": [
    {"id": "bench_top", "column": "bench", "row": "top", "label": "HLE +30%p", "sub": "1년 만에", "source": ["T1"]},
    {"id": "bench_low", "column": "bench", "row": "low", "label": "점수 자체도 불안", "sub": "문항 오류 최대 42%", "tag": "측정 한계", "source": ["T5"]}
  ],
  "edges": [{"from": "bench_top", "to": "bench_low", "label": "하지만", "style": "dotted", "undirected": true, "source": ["T1", "T5"]}]
}
```

## 6. 수치와 표기

- 수치는 원문 값 그대로 쓴다. 반올림·추정·기간 환산(예: "12년 누적")은 하지 않는다.
- 단위만 바꾸는 정확한 환산은 허용한다: "1.2 million people" → "120만 명", "$3.7 billion" → "$3.7B". 값이 바뀌지 않아야 한다. 한국어 문장 안에서는 한국어 수 단위를 우선하고, 통화·모델 규모처럼 원문 표기가 관용인 경우("200 million+ 파라미터", "$285.9 billion")는 원문을 둔다. 한 그림 안에서는 같은 종류의 수치를 한 방식으로 통일한다.
- 원문의 한정어(several, nearly, as little as, more than)를 빼거나 반대로 옮기지 않는다: "as little as 3%p" → "3%p에 불과"(○), "최소 3%p"(×).
- 주체(미국, 민간, 25개국 중앙값 등)와 기준 시점을 수치 옆에 붙인다. 빠지면 전체 수치로 읽힌다.
- 그림에 보이는 문구에 "원문", "명세" 같은 제작 용어를 쓰지 않는다. "보고서", "조사" 등 청중의 말로 쓴다.
