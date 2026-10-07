# donchang-skills

장동인 교수의 Claude Code·Codex 스킬 모음입니다. 각 스킬은 `plugins/<이름>/`에 플러그인으로 묶여 있습니다.

| 플러그인 | 내용 |
|---|---|
| `to-prd` | 업무 브리프를 bkit용 화면 중심 PRD와 읽기용 HTML로 정리 |
| `chang-ppt` | 강의·발표 자료에 KAIST AI대학원 브랜드 스타일 적용 |
| `chang-book` | 책 원고를 books.dotx 템플릿과 편집 표준에 맞춰 Word로 집필·편집 |
| `github-pages-handbook` | 기술 주제를 한국어 핸드북으로 만들어 GitHub Pages로 출판 |
| `vercel-rag` | Vercel + Supabase PDF RAG 구축 시 제약·버그·해결책 레퍼런스 |

## Claude Code에 설치

```bash
claude plugin marketplace add donchang07/skills
claude plugin install chang-ppt@donchang-skills   # 필요한 플러그인마다 실행
```

대화형 세션에서는 `/plugin marketplace add donchang07/skills` 후 `/plugin`에서 골라 설치합니다.
이 저장소의 `.claude/settings.json`에는 마켓플레이스와 전체 플러그인이 등록되어 있어, 이 저장소에서 연 세션은 자동으로 설치를 제안합니다.
다른 저장소에서도 쓰려면 같은 `extraKnownMarketplaces`·`enabledPlugins` 설정을 그 저장소나 사용자 설정(`~/.claude/settings.json`)에 넣습니다.

## 유지보수

편집 원본은 루트의 스킬 폴더(`chang-ppt/` 등)이고, `plugins/<이름>/skills/<이름>/`은 생성된 배포본입니다. 배포본을 직접 고치지 않습니다.

```bash
node scripts/build-to-prd-plugin.mjs          # to-prd 배포본 생성
node scripts/build-skill-plugins.mjs          # 나머지 스킬 배포본 생성
node scripts/build-skill-plugins.mjs --check  # 원본·배포본·버전 일치 확인
claude plugin validate .
```

스킬을 바꾸면 해당 플러그인의 `plugin.json` 3종과 `.claude-plugin/marketplace.json`의 버전을 함께 올립니다.
