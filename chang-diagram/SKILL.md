---
name: chang-diagram
description: "AI와 나눈 대화·메모·회의 내용이나 보고서·PDF의 장별 핵심을 요약해 스토리가 있는 다이어그램(SVG+PNG)으로 그립니다. 여러 장을 한 번에 그리는 일괄 모드도 있습니다. 표준 비즈니스·소프트웨어 개발 프로세스, 스윔레인(부서·역할별 책임 흐름), 인포그래픽·타임라인, 전후 비교 카드, 시스템 아키텍처, 순환·의사결정 흐름을 다룹니다. 요약·스토리 설계·제작 에이전트가 만들고 독립 심사 에이전트 2명(스토리·시각)이 루브릭으로 판정합니다. '지금까지 대화를 그림으로', '다이어그램 그려줘', '프로세스도/스윔레인/아키텍처도/인포그래픽/타임라인 만들어줘', '이 내용 도식화' 요청과 기존 다이어그램 수정·다시 그리기·심사만 요청, chang-diagram 스킬 개선에도 사용합니다. 데이터 차트(막대·선 그래프)와 PPT 전체 제작에는 쓰지 않습니다."
---

# Chang Diagram

대화의 결론을 한 장의 그림으로 이야기한다. 그림이 예쁜지보다 처음 보는 사람이 5초 안에 핵심 메시지를, 30초 안에 흐름을 읽어 내는지가 기준이다.

## 정본과 참조

- 저장소 `chang-diagram/`이 정본이고 `plugins/chang-diagram/skills/chang-diagram/`과 `~/.claude/skills/chang-diagram/`은 배포 사본이다.
- 대화 요약과 스토리 설계: [story-distill.md](references/story-distill.md)
- 유형 선택과 유형별 배치 규칙: [diagram-types.md](references/diagram-types.md)
- 캔버스·서체·색·연결선·SVG 작성 계약: [visual-system.md](references/visual-system.md)
- 심사 루브릭과 통과 기준: [review-rubric.md](references/review-rubric.md)
- 렌더링과 자동 검사: `python scripts/render_check.py <svg> --png <png> --report <json> --spec <01_spec.json> --density <normal|dense>`
- 문서 원문 추출: `python scripts/extract_source.py <pdf> --pages 15-16 --out {RUN}/00_source.md --title "<장 이름>" [--skip "<머리글 정규식>"]` (여러 쪽에 반복되는 머리글은 자동 제거, 한 쪽에만 있는 머리글은 `--skip`)
- 여러 그림 미리보기: `python scripts/contact_sheet.py <png 폴더> --out <png>`

## 모드

| mode | 예 | 실행 |
| --- | --- | --- |
| new | "지금까지 대화를 스윔레인으로", "이 메모 도식화" | 아래 팀 흐름 전체 |
| batch | "이 보고서 장별로 그려줘", "PDF 핵심을 여러 장으로" | 아래 「일괄 모드」 |
| redraw | "유형을 바꿔 다시", "스토리를 다시 짜서" | 기존 `{RUN}`에서 distiller부터 다시 |
| small_fix | 라벨 오타, 색, 간격, 화살표 하나, 통과 뒤 남은 🟡 문구 | 팀 없이 메인이 명세·SVG 수정 → render_check → review-rubric.md 「경량 재심사」 |
| review_only | 이미 있는 그림(PNG/SVG)을 평가 | 심사 에이전트 2명만, 원문이 없으면 story-judge의 원문 충실도는 not_run |
| skill_update | 이 스킬 자체 개선 | 팀 없이 정본 수정 → 빌드 `--check` |

애매하면 small_fix로 시작하고, 노드 구조·유형·메시지가 바뀌면 redraw로 전환한다.

## 팀 구성

실행 모드는 서브에이전트 위임 + 생성·검증(Producer-Reviewer)이다. 단계 결과를 파일로 넘기므로 에이전트끼리 대화하지 않는다. 메인이 원문 확보·통합 판정·사용자 보고를 소유한다.

| 에이전트 | 모델 | 맡는 일 | 쓰기 범위 |
| --- | --- | --- | --- |
| `chang-diagram-distiller` | opus | 원문 요약, 핵심 메시지, 스토리 아크, 유형 선택, 다이어그램 명세 | `{RUN}/01_*` |
| `chang-diagram-builder` | opus | 명세대로 SVG 제작, 렌더·자동 검사, 기계적 오류 자가 수정 | `{RUN}/02_*` |
| `chang-diagram-story-judge` | opus | 냉독(cold read) 후 원문·명세 대조, 스토리 심사. 수정하지 않음 | `{RUN}/03_story_*` |
| `chang-diagram-visual-judge` | sonnet | 자동 검사 결과와 렌더 이미지로 시각 심사. 수정하지 않음 | `{RUN}/03_visual_*` |

플러그인 설치 시 이름 앞에 `chang-diagram:`이 붙을 수 있다. 사용 가능한 에이전트 목록에서 실제 이름을 확인하고, 없으면 `~/.claude/agents/`의 같은 정의를 기본 서브에이전트에 전달해 실행한 사실을 기록한다.

## 작업 폴더

- `{RUN}` = 현재 작업 디렉터리의 `_workspace/chang-diagram/{YYYYMMDD}_{이름}/`. 스킬 설치 폴더를 작업 폴더로 쓰지 않는다.
- 결과물은 사용자가 지정한 경로, 없으면 `{RUN}/final/{이름}.svg`와 `.png`.
- 이전 버전 파일을 덮어쓰지 않고 `_v{N}`을 올린다.

## 흐름

1. **원문 확보 (메인)**: 서브에이전트는 이 대화를 볼 수 없다. 그림의 근거가 될 대화·메모를 요약하지 말고 원문 그대로 `{RUN}/00_source.md`에 옮긴다. 발화마다 `[T1]`, `[T2]`… 번호와 화자(사용자/AI)를 붙인다. 문서·PDF가 원문이면 `extract_source.py`로 단락마다 `[T#] (p.쪽)`을 붙여 옮긴다. 너무 길면 관련 없는 구간만 빼고 뺀 범위를 적는다. 이어서 `{RUN}/00_packet.md`에 mode, 청중, 용도(강의 슬라이드/문서/SNS), 캔버스, 테마, 언어(원문과 그림 언어가 다르면 번역 규칙), `density`(`normal` 기본, 사용자가 "글자가 많아도 좋다"고 하면 `dense`), 사용자가 지정한 유형·문구·강조점, 결과 경로를 쓴다. 정보가 없으면 합리적 가정을 표시하고 진행한다.
2. **요약·설계**: `chang-diagram-distiller` → `01_story.md`(메시지·아크·유형 근거·포함/제외 목록)와 `01_spec.json`(노드·연결·그룹·출처 매핑).
3. **제작**: `chang-diagram-builder` → `02_diagram_v1.svg`, `02_diagram_v1.png`, `02_check_v1.json`. 자동 검사 오류는 builder가 스스로 0건으로 만든 뒤 넘긴다(최대 3회, 남으면 그대로 보고). 메인은 builder에게 명세와 다른 형태 지시(연결을 빼라, 화살표를 바꿔라, 캔버스를 바꿔라)를 하지 않는다. 형태를 바꿔야 하면 distiller가 명세를 고친 뒤 builder를 부른다. 명세와 그림이 어긋나면 심사 기준도 어긋나기 때문이다.
4. **심사 (병렬)**: 한 메시지에서 `chang-diagram-story-judge`와 `chang-diagram-visual-judge`를 함께 호출한다. 두 심사자는 서로의 보고서를 읽지 않는다.
5. **통합 판정 (메인)**: [review-rubric.md](references/review-rubric.md)의 통과 기준으로 두 보고서를 합친다. 내용 지적은 distiller→builder, 화면 지적은 builder로 보낸다. 두 심사가 충돌하면 내용은 story-judge, 형식은 visual-judge를 따르고 판단 근거를 `04_decision_v{N}.md`에 적는다.
6. **수정 반복**: 수정 후 지적받은 심사자만 다시 부른다. 수정·재심사는 최대 2회. 남은 🔴는 통과로 바꾸지 않고 보고한다.
7. **완료 (메인)**: 최종 SVG·PNG를 결과 경로에 복사하고 `{RUN}/05_manifest.json`(원문 범위, 버전별 점수, 최종 판정, 렌더러·글꼴, not_run)을 쓴다. 사용자에게 결과 경로, 한 줄 메시지, 최종 점수, 남은 지적을 보고하고 PNG를 보여 준다.

### 일괄 모드 (batch)

보고서의 장별 그림처럼 같은 원문 묶음에서 여러 장을 그릴 때 쓴다.

1. **원문 일괄 추출 (메인)**: 장마다 `{RUN}/{NN}-{slug}/`를 만들고 `extract_source.py`로 `00_source.md`를 쓴다. 보고서라면 장 전체보다 장 요약(Highlights·Key findings) 쪽을 우선하고, 추출한 쪽 범위를 기록한다. 추출 결과의 단락 수를 장마다 확인해 빠진 쪽이 없는지 본다.
2. **공통 패킷**: 청중·용도·언어·density·캔버스·출처 표기는 모든 장에 같게 쓴다. 작업 도중 기준을 바꾸면(예: density) 모든 장의 패킷을 함께 고치고 결정 이유를 남긴다.
3. **유형 분포 (메인)**: distiller를 병렬로 돌리고, 결과 유형을 표로 모은다. 한 유형이 절반을 넘으면 그 장들의 distiller에게 [diagram-types.md](references/diagram-types.md)「대비형 쏠림 막기」를 근거로 차선 유형 검토를 요청한다. 원문 성격상 한 유형이 맞으면 그 판단을 사용자 보고에 적는다.
4. **장별 파이프라인**: 각 장은 단일 그림과 같은 흐름(제작 → 병렬 심사 → 수정 최대 2회)을 독립적으로 밟는다. 끝난 장부터 다음 단계로 넘긴다. 수정 회차에는 같은 distiller·builder를 이어서 불러(SendMessage) 맥락을 유지한다.
5. **진행표 (메인)**: `{RUN}/progress.md`에 장 | 단계 | 버전 | story | visual | 🔴 | 판정을 갱신한다. 통과한 장은 바로 `final/`과 `05_manifest.json`을 쓴다.
6. **마무리**: 모든 장의 최종 PNG·SVG를 `{RUN}/ALL/`에 모으고 `contact_sheet.py`로 한 장짜리 미리보기를 만든다. 사용자 보고에는 장별 headline·점수·남은 지적과 유형 분포를 넣는다.

### 시안 경합 (선택)

distiller가 유형 후보 2개를 비슷한 근거로 제시했거나 사용자가 시안 비교를 원하면 builder가 A/B 두 시안을 만들고, story-judge가 두 시안을 냉독해 더 빨리 메시지가 읽히는 쪽을 고른다. 선택된 시안만 이후 반복에 들어간다. 기본은 단일 시안이다.

## 부분 재실행

- 같은 이름의 `{RUN}`이 있으면 후속 요청으로 본다. 문구·화살표 수정은 builder만, 메시지·유형 변경은 distiller부터 다시 실행한다.
- 새 대화 내용이 추가되면 `00_source.md`에 이어 붙이고 새 발화 번호를 쓴다. 다른 주제면 새 `{RUN}`을 만든다.

## 오류 처리

- 렌더러(Playwright Chromium)를 쓸 수 없으면 PNG와 자동 검사는 not_run으로 기록하고 visual-judge는 SVG 소스만으로 판정할 수 없는 항목을 not_run으로 둔다. 렌더 없이 통과라고 하지 않는다.
- 에이전트가 실패하면 원인을 확인해 1회 재시도한다. 같은 원인으로 다시 실패하면 남은 산출물로 보고한다. 메인이 심사자의 점수를 추측해 채우지 않는다.

## 테스트 시나리오

1. **대화 → 스윔레인**: 주문 처리 절차를 논의한 대화 + "부서별로 그려줘" → swimlane, 레인 = 부서, 분기(NG) 표시 → 두 심사 통과.
2. **대화 → 전후 비교 인포그래픽**: "Gen AI에서 Agentic AI로 바뀌는 4가지" 대화 → comparison 카드 4열 × OLD/NEW → story-judge가 냉독으로 "4가지 변화"를 읽어 내는지 확인.
3. **small_fix**: "3번 상자 문구만 바꿔" → 메인 수정 → render_check → visual-judge만.
4. **오류 흐름**: 노드 14개로 밀도 🔴가 2회 연속 → 3회차 없이 분할(2장) 제안과 함께 보고.
5. **일괄 모드**: 425쪽 보고서 + "장별로, 글자 많아도 좋다" → 장별 Highlights 추출, density dense, 유형 분포 확인, 장별 파이프라인, `ALL/`과 미리보기 시트.
