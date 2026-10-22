# 부품 목록

`assets/template.html`에서 복제해 쓴다. 템플릿의 각 부품 앞 주석에 쓰임이 적혀 있다. 자리표시 `{{…}}`는 모두 바꾼다(남으면 `validate.py`가 실패).

| 부품 | 쓰는 곳 | 규칙 |
|---|---|---|
| toolbar | 맨 위 고정 | 파일 이름·버전·기준일, 「교안 다운로드」「PDF로 인쇄」 |
| hero | 첫 화면 | 큰 제목·리드·의미색 범례. 핵심 장면 데모는 선택(버튼 `aria-pressed`, 키보드 조작, 첫 로딩 때 한 번만 움직임) |
| rail | 1280px 이상 왼쪽 고정 목차 | `main` 밖. 링크 `href="#sNN"`, 번호 `<span>NN</span>` |
| section | 장 | `main > section id="sNN"`, `h2.ch` 바로 뒤 `<!--NOTE:NN-->`, 첫 문단 `.lead`(「이 장의 목표」) |
| map | 여러 방식을 두 축으로 정리 | 가로축 칸 + 칩. 의미색 칩은 해당 방식에만 |
| tbl | 비교표 | 표 머리 ink. 핵심 행은 `key`로 굵게·왼쪽 막대. 막대·색에는 범례 한 줄 |
| fig-wrap | SVG 흐름도 | 화살표에 의미 라벨. 휴대폰에서 옆으로 밀림 → 흐림과 안내 문구 |
| criteria + pair | 판단 기준, 권고/중단 조건 | 중단 조건은 어두운 상자 |
| prep | 실습 전 준비 | 번호 목록 |
| folder | 결과 폴더 구조 | D2Coding, 한글 2칸 기준 열 맞춤 |
| code | 복사 프롬프트 한 개 | `<pre id>` + `copyPrompt('id')` 버튼 + [완료 조건] |
| steps tabs | 순서 있는 실습 Lab | `switchTab('tabN')`, 버튼 `btn-tabN`, 인쇄 시 모두 펼침 |
| method card (mx) | 방식 하나를 만들고 묻는 실습 | 머리(큰 번호·이름·한 줄 설명) + 메타 알약(필요한 것·집중 질문·결과 파일) + 「만드는 프롬프트」「질문 스크립트」 쌍(1024px 이상 두 열). 정리 카드는 `mx-final` |
| human steps | 사람이 직접 할 단계 | 번호 목록, 프롬프트와 분리 |
| caution | 주의·보안·저작권 | 왼쪽 막대 상자 |
| src | 장 끝 출처 줄 | 「출처: 짧은 이름 (YYYY-MM-DD 확인)」, 날짜 nowrap |
| checks (dark) | 핵심 체크리스트 | ink 바탕 장 하나, 두 열 |
| refs | 출처와 기준일 장 | 전체 URL 모음 |

## id 규칙

- 장: `s01`부터 빈칸 없이. 강사 가이드는 `instructor-guide`(빌드가 넣는다).
- 프롬프트: 짧고 뜻 있는 이름(`p1-1`, `m4-build`, `k0-env`). 원고의 `(id: …)`와 같아야 한다. 한 번 배포한 id는 바꾸지 않는다.
- 탭: `tab0`~`tabN`, 버튼 `btn-tab0`~`btn-tabN`.

## 이전 형식 교안

claude-remote-control v2.0 이하(Tailwind·둥근 상자)와 chang-ppt 템플릿으로 만든 교안은 이전 형식이다. 사용자가 디자인 전환을 요청하지 않으면 그 형식을 유지하고 검사 도구만 쓴다.
