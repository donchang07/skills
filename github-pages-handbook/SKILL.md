---
name: github-pages-handbook
description: 어떤 기술 주제든 한국어 핸드북(레퍼런스 매뉴얼 + 실습 예시)으로 만들어 GitHub Pages에 정적 사이트로 출판한다. 주제는 사용자에게 입력받는다. 전체검색·페이지 내 검색·반응형 디자인 시스템·SVG 도식화·멀티에이전트 품질 검증·비공개 저장소+공개 Pages 배포가 한 세트로 포함된다. "핸드북 만들어줘", "가이드 사이트 만들어줘", "GitHub Pages 핸드북", "기술 문서 사이트 출판" 같은 요청에 사용.
---

# GitHub Pages 핸드북 제작 스킬

특정 주제 하나(`TOPIC`)를 받아, 일관된 품질·디자인·검색·배포로 **한국어 기술 핸드북**을 만들어 GitHub Pages에 출판하는 자립형 스킬이다. 콘텐츠만 갈아끼우면 어떤 주제든 동일한 방식으로 제작된다.

## 시작하면 가장 먼저 할 일

1. **사용자에게 주제(`TOPIC`)를 입력받는다.** 주제는 이 스킬이 임의로 정하지 않는다. 함께 받을 파라미터: `REPO`(URL 슬러그), `OFFICIAL_SOURCES`(공식 1차 자료), `VERSION_TARGET`, `PROJECT_DIR`(새 프로젝트 경로), `OWNER`(GitHub 계정).
2. **`references/BUILD_GUIDE.md` 를 끝까지 읽고 그대로 따른다.** 제작·검증·배포의 모든 절차가 거기 있다.

## 이 스킬에 동봉된 자산 (자립형 — 외부 의존 없음)

```
이 스킬/
├── SKILL.md                       이 파일
├── references/
│   └── BUILD_GUIDE.md             범용 제작 지시서 (자료조사→제작→검증→배포 전 과정)
├── assets/                        docs/assets/ 로 복사할 검색 JS
│   ├── site-search.js             랜딩 전체검색 (DOCS 배열만 교체)
│   └── inpage-search.js           페이지 내 검색 (수정 없이 사용, SVG 라벨 보호 가드 포함)
└── templates/                     docs/ 로 복사할 HTML 골격 + 빈 파일
    ├── index.html                 랜딩(카드 그리드) 골격
    ├── Section_Manual.html        레퍼런스 매뉴얼 골격(컴포넌트 예시 포함)
    ├── Section_Examples.html      실습 예시 골격(초·중·고급 시나리오 카드)
    ├── .nojekyll                  (빈 파일)
    └── .gitignore
```

모든 디자인 토큰·레이아웃·검색 스크립트 연결·홈 링크·검색 색인 전제는 템플릿에 **이미 내장**되어 있다. 새 핸드북은 템플릿을 복사한 뒤 `{{플레이스홀더}}`·`[설명: …]` 부분만 실제 내용으로 채우면 된다.

## 작업 흐름 요약 (상세는 BUILD_GUIDE.md)

1. **파라미터 확정** — 특히 `TOPIC`은 사용자 입력. 섹션 분할안도 사용자에게 확인.
2. **공식 문서 조사** — 추측 금지. `WebSearch`/`WebFetch`로 `OFFICIAL_SOURCES` 확인, 버전·수집일 기록.
3. **자산 복사** — 이 스킬의 `assets/`·`templates/`를 `PROJECT_DIR/docs/`로 복사(BUILD_GUIDE §4).
4. **콘텐츠 작성** — Manual(레퍼런스)+Examples(실습), 핵심 동작 1~3문장, 초·중·고급 시나리오, 맥락적 타당성.
5. **품질 검증(필수)** — §6 내용 검증 하네스(학생→강사, 검토자→종합→적용), §7.5 SVG 도식화(선별), §7 한국어 문법·어순 검수(발행 전 게이트).
6. **검색·메타 마무리** — `site-search.js`의 `DOCS` 교체, 랜딩 최종 업데이트 날짜, `CHANGELOG.md`.
7. **배포·검증** — 비공개 저장소 + 공개 Pages(main/docs), curl 200 + Playwright 렌더 검증.

> 핵심 원칙: **추측보다 확인**(공식 문서에서 확인한 것만), **상대경로만**(GitHub Pages base가 `/<REPO>/`), **검증 후 발행**(§6·§7 통과 전 출판 금지).
