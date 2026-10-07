# 핸드북 제작 작업 지시서 — 범용(도메인 무관) · 자립형

> 이 문서는 특정 주제에 묶이지 않은 **"핸드북 제작 엔진"**이다. 주제(`TOPIC`)만 갈아끼우면 어떤 기술 주제든
> 동일한 품질·구조·검색·배포로 한국어 핸드북을 만들어 GitHub Pages에 출판할 수 있다.
>
> **자립형이다.** 필요한 모든 재사용 자산(검색 JS, HTML 골격 템플릿, `.nojekyll`, `.gitignore`)은
> **이 스킬 폴더 안의 `assets/`·`templates/`** 에 들어 있다. 외부 레퍼런스 저장소에 의존하지 않는다.
>
> **세 가지 검증은 선택이 아니라 필수다 — §6, §7, §7.5는 권장.** 내용을 페르소나 서브에이전트로 검증하고,
> 한국어 문법·어순을 별도 서브에이전트로 검수한 뒤에만 발행한다.

이 문서에서 `SKILL_DIR` 는 **이 스킬이 설치된 폴더**(이 파일의 상위, 즉 `references/`의 부모)를 가리킨다.

---

## 0. 시작 전에 — 파라미터 정의 (사용자에게 입력받는다)

새 세션은 먼저 아래 값을 **사용자와 확정**한다. **주제(`TOPIC`)는 반드시 사용자로부터 입력받는다 — 임의로 정하지 않는다.**

| 파라미터 | 의미 | 예시 |
|----------|------|------|
| `TOPIC` | 다룰 주제(한국어 명칭) — **사용자 입력 필수** | "Vercel 사용법" |
| `REPO` | 저장소·URL 슬러그(공개 URL에 노출) | `vercel-handbook` |
| `OFFICIAL_SOURCES` | 공식 1차 자료(URL·CLI 등) | `vercel.com/docs`, `vercel --help` … |
| `VERSION_TARGET` | 콘텐츠가 다루는 버전/플랫폼 기준 | "Vercel CLI vXX / 플랫폼 2026-06" |
| `PROJECT_DIR` | 새 프로젝트(저장소 루트) 절대경로 | `…/Books/Vercel` |
| `OWNER` | GitHub 사용자/조직명(공개 URL·API에 사용) | (사용자 GitHub 계정) |

전역 규칙의 **"추측보다 확인 — 공식 문서 검색 → 명세 → 구현"**을 항상 따른다.

---

## 1. 네이밍 & 공개 정책

- 저장소 이름은 `REPO`. 시리즈 규칙은 주제에 맞게 정한다(예: `<주제>-handbook`). **특정 벤더 prefix를 강요하지 말 것.**
- **비공개 저장소 + 공개 GitHub Pages**(소스는 비공개, 사이트만 공개 — GitHub Pro 필요).
- 공개 URL: `https://<OWNER>.github.io/<REPO>/`. 저장소 이름은 공개 URL에 노출되므로 공개돼도 무방하게.

---

## 2. 주제 자료 조사 (추측 금지)

1. `OFFICIAL_SOURCES`를 `WebSearch`/`WebFetch`로 조사. **공식 문서에서 확인된 것만** 작성한다.
2. 버전(`VERSION_TARGET`)과 **문서 수집일**을 기록(각 문서 버전 박스에 반영).
3. 다룰 범위를 먼저 목록화하고, **문서 섹션 분할안**을 사용자에게 확인받는다.
   - 섹션 패턴은 자유지만, 각 섹션은 **Manual(레퍼런스) + Examples(실습)** 2종을 유지한다.
   - 분량이 적으면 1개 섹션으로 시작, 많으면 사용/제작·기초/심화 등으로 분할.

---

## 3. 산출물 디렉토리 구조

```
PROJECT_DIR/                        (= 저장소 루트, Private)
├── docs/                          ★ GitHub Pages 게시 대상 (main / docs)
│   ├── index.html                 랜딩(카드) — templates/index.html 복사 후 제목·카드만 교체
│   ├── .nojekyll                  빈 파일(templates/에서 복사)
│   ├── assets/
│   │   ├── site-search.js         랜딩 전체검색(복사 후 DOCS 배열만 교체)
│   │   └── inpage-search.js       페이지 내 검색(수정 없이 복사)
│   └── <section-slug>/
│       ├── *_Manual.html          레퍼런스(빠른 참조)  ← templates/Section_Manual.html 복제
│       └── *_Examples.html        실습 예시(시나리오)  ← templates/Section_Examples.html 복제
├── markdown/                      ☆ 미게시. MD 요약(선택)
├── .gitignore                     templates/.gitignore 복사
├── CHANGELOG.md                   변경 이력(비공개, 미게시 — §11)
└── README.md                      저장소 설명
```
- **게시되는 것은 `docs/` 안 HTML뿐.** GitHub Pages 브랜치 배포 폴더는 `/`(root) 또는 `docs`만 허용 → `docs/` 사용.
- 폴더명에 **공백 금지**(공백은 URL에서 `%20`이 됨). `<section-slug>`는 무공백 소문자(예: `using`, `authoring`).

---

## 4. 재사용 자산 — 이 스킬에서 복사 (자립형)

모든 자산은 **이 스킬 폴더(`SKILL_DIR`)** 안에 있다. 외부 저장소를 찾지 말 것.

```bash
SKILL_DIR="<이 스킬이 설치된 폴더 절대경로>"   # 예: .../Books/Github Pages Handbook Design Guide
DST="$PROJECT_DIR/docs"
mkdir -p "$DST/assets" "$DST/<section-slug>"

# 검색 JS (assets)
cp "$SKILL_DIR/assets/inpage-search.js" "$DST/assets/inpage-search.js"   # 수정 불필요
cp "$SKILL_DIR/assets/site-search.js"   "$DST/assets/site-search.js"     # DOCS 배열만 교체

# 랜딩 + 빈 파일
cp "$SKILL_DIR/templates/index.html"  "$DST/index.html"                  # 제목·카드만 교체
cp "$SKILL_DIR/templates/.nojekyll"   "$DST/.nojekyll"
cp "$SKILL_DIR/templates/.gitignore"  "$PROJECT_DIR/.gitignore"

# 섹션 문서 (섹션·종류마다 복제해 이름 교체)
cp "$SKILL_DIR/templates/Section_Manual.html"   "$DST/<section-slug>/<Section>_Manual.html"
cp "$SKILL_DIR/templates/Section_Examples.html" "$DST/<section-slug>/<Section>_Examples.html"
```

복사 후 **수정 지점**:
1. `assets/site-search.js`의 `DOCS` 배열 → 새 문서 path·title로 교체(§9).
2. `index.html` → `<title>`/`<h1>`/부제, `.meta` 박스, `.group` 카드(섹션 수만큼), footer.
3. `*_Manual.html`/`*_Examples.html` → `{{플레이스홀더}}`·`[설명: …]`를 실제 내용으로. CSS·레이아웃·검색 스크립트는 **그대로**.

`inpage-search.js`·`.nojekyll`은 **수정 없이** 사용. (`inpage-search.js`에는 SVG 라벨 보호 가드가 이미 포함돼 있어 §7.5 도식을 넣어도 안전하다.)

---

## 5. 콘텐츠 제작 표준

- **공식 문서 우선** — 확인 안 된 내용은 쓰지 않는다.
- **Manual(레퍼런스) + Examples(실습) 2종 분리.** Manual의 각 항목엔 **핵심 동작 1~3문장**(코드만 나열 금지).
- **초급(초록)·중급(파랑)·고급(보라) 3단계** 시나리오.
- **맥락적 타당성** — 예시는 숨은 전제 없이 재현 가능해야. 대상이 자명(현재 폴더 등)하거나 전제를 명시. 페르소나와 난이도 일치.
- **자연스러운 한국어** — 직역 금지(§7에서 별도 검수). 기술 용어·식별자는 원형 유지. 영어 원문 병기하지 않는다.

---

## 6. ★ 필수 ① — 다양한 페르소나 서브에이전트로 "내용" 검증

내용의 정확성·교육효과·맥락 타당성은 **반드시 멀티에이전트 하네스(`Workflow`/서브에이전트)로 검증**한 뒤 반영한다. 혼자 작성하고 끝내지 않는다.

### 6-A. 학생 페르소나 → 강사 (이해도 검증·설명 보강)
생소하거나 어려운 개념·섹션에 적용.

- **학생 페르소나(병렬, 최소 4종):**
  | 페르소나 | 관점 |
  |----------|------|
  | 완전 초보(비전공) | 용어 자체가 생소 — "이게 뭔지·왜 필요한지" |
  | 주니어 | 기본은 알지만 핵심 메커니즘 혼동 |
  | 중급 | 유사 개념과의 차이·실전 패턴 |
  | 시니어/도입 검토자 | 생명주기·경계조건·팀 적용·트레이드오프 |
- 각 학생이 **구체적 질문 목록**(추상 질문 금지) 생성 → **강사 에이전트**가 모든 질문에 답하는 종합 설명 생성 →
  개념·생명주기·상세·시나리오·주의사항을 산출물에 반영.

### 6-B. 검토자 렌즈 → 종합 → 적용 (예시·서술 검증)
- **검토 렌즈(병렬):** 초보 재현성 / 교육적 초점 / 기술적 정확성 / 실무 현실성
- 각 렌즈가 문제 항목을 `{원문, 심각도, 문제, 수정안}`으로 플래그 → **종합 에이전트**가 중복 통합·확정 →
  파일에 반영. **과편집 금지** — 정말 오해를 유발/재현 불가한 것만 고치고, 멀쩡한 건 둔다.

### 하네스 골격(개념)
```
phase('내용검증')
students = parallel(personas.map(p => agent(질문생성, {schema})))
instructor = agent(모든 질문 종합 답변, {schema})
reviews = parallel(lenses.map(l => agent(렌즈 검토, {schema})))
synthesis = agent(통합·확정 개선안, {schema})
apply = parallel(files.map(f => agent(파일에 반영)))   // 원문 정확 매칭으로 Edit
```
> 항상 **검증→종합→적용** 순. 적용은 원문 문자열을 정확히 찾아 교체(추측으로 엉뚱한 곳 수정 금지).

---

## 7. ★ 필수 ② — 한국어 문법·어순 검수 서브에이전트 (발행 전 게이트)

모든 산문(prose)은 **발행 전에 한국어 검수 하네스를 통과**해야 한다. 영어 직역투·어색한 어순·맞춤법 오류를 잡는다.

### 7-A. 검수자 페르소나(병렬, 렌즈별)
| 검수자 | 잡아내는 것 |
|--------|------------|
| 맞춤법·띄어쓰기 | 한글 맞춤법, 띄어쓰기, 조사(은/는/이/가/을/를) 오류 |
| 어순·직역투 | 영어 번역투 — 피동 남용, 무생물 주어, "~에 대해", "~을 가진다", "~되어진다", 어순 뒤틀림 → 한국어 자연 어순으로 |
| 용어 일관성 | 같은 개념을 다른 말로 혼용하지 않는지, 외래어 표기 일관성 |
| 가독성·톤 | 한 문장 과다 길이, 능동·간결, 교육 대상 눈높이 |

### 7-B. 절대 규칙 (검수 대상 한정)
- **코드·명령어·플래그·식별자·파일경로·URL·HTML 태그는 절대 손대지 않는다.** 오직 **설명 문장(산문)만** 교정.
- **의미를 바꾸지 않는다.** 표현만 자연스럽게. 기술 정확성은 §6에서 이미 검증된 상태를 전제.
- 과교정 금지 — 이미 자연스러운 문장은 그대로 둔다.

### 7-C. 흐름
```
phase('한국어검수')
flags = parallel(proofLenses.map(l => agent(렌즈별 검수, {schema:{flagged:[{원문,유형,수정안,위치}]}})))
merged = agent(중복 통합·확정, {schema})
apply  = parallel(files.map(f => agent(해당 파일의 산문만 교체)))  // 코드/태그 보존
```
- 산출물(HTML/MD) 전체 대상으로, **표·박스·시나리오·툴팁의 설명 문장까지** 빠짐없이.
- 검수 후 **무엇을 왜 고쳤는지 요약**을 사용자에게 보고(샘플 몇 개 포함).

> §6(내용)와 §7(표현)은 **순서가 있다**: 먼저 내용 검증·확정 → 그 다음 한국어 검수. 표현을 먼저 다듬고 내용이 바뀌면 헛수고.

---

## 7.5 ★ 권장 ③ — SVG 전문 디자이너 서브에이전트로 도식화

글로만 설명하기 어려운 **흐름·상태·구조·비교**는 **SVG 다이어그램**으로 시각화한다. **SVG 전문 디자이너 서브에이전트**(`Agent`)에 위임한다.

### 도식화 우선 대상
- **흐름/생명주기** → 플로우차트(노드+화살표, 분기·루프·back-edge)
- **상태/모드 비교** → 좌우 비교도
- **구성/계층 관계** → 트리·구성도(부모-자식·바인딩)
- **단계 절차** → 번호 노드 시퀀스

### 서브에이전트 사용법
`Agent`로 "SVG 다이어그램 전문 디자이너" 페르소나에 **디자인 토큰(§8) + 도식화할 텍스트 + 규격(아래)**을 주고 **완결된 인라인 `<svg>` 마크업만 반환**받는다(임베드는 본체가). 여러 장은 같은 스펙을 한 에이전트에 줘 일관성 확보.

### SVG 규격 (반드시)
- **인라인 SVG**(외부 리소스·이미지·폰트 금지) → 자립형 단일 파일 유지. `<figure>`로 감싸고 `<figcaption>`에 "그림 N. 한 줄 설명".
- 반응형: `viewBox` + `width="100%" height="auto"` + `style="max-width:<px>;height:auto;display:block;margin:18px auto;"`(고정 px width 금지).
- 접근성: `role="img"` + `<title>`/`<desc>`.
- **§8 디자인 토큰 색상만** 사용. 일반 텍스트 시스템/Noto Sans KR, 명령어·식별자 monospace, 화살표는 `<marker>`. 한국어 라벨, 텍스트 잘림 없게(글자당 폭 ~13px@13px / 11px@11px 가정, `text-anchor="middle"`, 박스 넉넉히).
- 과한 그라데이션·그림자 금지. 정보 전달 우선.

### 검증·순서
- 다이어그램 내용은 **§6에서 검증된 본문과 일치**해야 한다.
- §13 Playwright 검증에 **SVG 렌더(가시성·viewBox·모바일 가로 넘침 없음)** 포함.
- 권장 순서: §6 내용 확정 → **SVG 도식화** → §7 한국어 검수(캡션·라벨 산문도 검수 대상).
- **최적 지점에만** 넣는다 — 모든 단락에 억지로 넣지 말고, 그림이 실제로 이해를 높이는 곳에 선별 적용.
- `inpage-search.js`에는 SVG `<text>`에 `<mark>`가 주입되지 않도록 하는 가드가 이미 들어 있다(라벨 깨짐 방지).

---

## 8. 디자인 시스템 (시각 일관성 — 템플릿에 내장됨)

화이트 배경 + 인라인 `<style>`(외부 CSS 없음, 자립형 단일 파일). `templates/` 의 토큰 그대로:
```css
:root{
  --bg:#ffffff; --bg2:#f6f8fa; --bg3:#eef1f4; --border:#d0d7de;
  --text:#1f2328; --text-dim:#636c76;
  --accent:#0969da; --accent2:#1a7f37; --accent3:#953800; --accent4:#6639ba; --accent5:#cf222e; --accent6:#0550ae;
}
body{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif; }
```
핵심 컴포넌트(템플릿에 예시 골격으로 들어 있음): 2단 레이아웃(좌측 고정 `nav` 270px + `main`), **버전 박스**(대상 버전·문서 URL·**문서 수집일**), 개념/명령 트리(`.tree-box`), **배지**(라벨은 주제에 맞게 재정의), 표, **실습 카드** `.scenario-card`(레벨 배지 + `.tip-box`/`.warning-box`).
- 표 짝수행 배경 `#f6f8fa`(⚠️ 어두운 색 금지 — 가독성). 표·박스 안 긴 설명은 `<ul>/<ol>`로 구조화(평문 `1) 2) 3)` 금지).
- 새 문서는 `templates/`의 `Section_Manual.html`/`Section_Examples.html`을 복제해 골격 유지, **내용만** 교체가 가장 빠르고 일관적.

---

## 9. 검색 (복사·연결 — 템플릿에 스크립트 태그 내장)

위치 분리(한 화면 검색창 1개): **랜딩=사이트 전체 검색** + **각 문서=페이지 내 검색**. 템플릿에 아래가 이미 들어 있다:
```html
<!-- docs/index.html : </body> 직전 -->            <script src="assets/site-search.js" defer></script>
<!-- docs/<section>/*.html : </body> 직전 -->      <script src="../assets/inpage-search.js" defer></script>
```
- **필수 수정**: `assets/site-search.js`의 `DOCS` 배열을 새 문서 목록(path는 docs/ 기준 상대, title은 표시명)으로 교체.
- 색인 전제(템플릿이 이미 충족): 매뉴얼류 `main` 안 `<h2 id>`(섹션)+`<h3>`(안에 `<code>`) / 예시류 `.scenario-card[id]`(안에 `<strong>` 제목, `<span>` 레벨).
- ⚠️ 페이지 내 검색은 **사이드바 nav를 필터링하지 않는다**(묶음 라벨이 통째로 사라지는 문제). 되살리지 말 것.

---

## 10. 네비게이션 — 홈 링크 (템플릿에 내장)

모든 문서 `nav` 최상단(템플릿에 이미 있음):
```html
<a href="../index.html" style="font-weight:700;color:#0969da;margin-bottom:8px;border-bottom:1px solid #d0d7de;padding-bottom:10px;">← 핸드북 홈</a>
```

---

## 11. 버전 관리 — 발행일 & 변경 이력

- **공개 사이트(랜딩)** → 랜딩 `.meta` 박스에 **최종 업데이트 날짜만**: `<br>최종 업데이트 <strong>YYYY년 M월 D일</strong>`
- **변경 이력** → 저장소 root `CHANGELOG.md`(비공개·미게시), 최신 항목 맨 위, `YYYY-MM-DD`.
- per-doc 버전 박스("문서 수집일"·"대상 버전")는 랜딩 날짜와 **의미가 다름**(혼동 말 것).
- ⚠️ 수동 날짜는 드리프트한다 — **배포 직전** 랜딩 날짜 갱신 + CHANGELOG 항목 추가.

---

## 12. 배포 절차 (변수만 교체)

```bash
cd "$PROJECT_DIR"
git init -b main
xattr -w 'com.apple.fileprovider.ignore#P' 1 "$(pwd)/.git"          # 클라우드 동기화 폴더(Dropbox 등)가 .git 동기화 안 하게
xattr -p 'com.apple.fileprovider.ignore#P' "$(pwd)/.git"            # → 1 확인
git add . && git commit -m "Publish $REPO (static site, docs/)"
gh repo create "$REPO" --private --source=. --push                  # 비공개 + 푸시
gh api -X POST "/repos/$OWNER/$REPO/pages" \
  -f build_type=legacy -f "source[branch]=main" -f "source[path]=/docs"
gh api "/repos/$OWNER/$REPO/pages/builds/latest" --jq '.status+" "+.commit'   # built 대기
```
- 갱신: `docs/` 수정 → 랜딩 날짜·CHANGELOG 갱신 → `git add . && git commit && git push`(Pages 자동 재빌드).
- 전제: `gh` 인증·git user 설정. 비공개 저장소 + 공개 Pages는 **GitHub Pro 이상** 필요. 정적 HTML이라 `.nojekyll`로 Jekyll 우회.

---

## 13. 검증 절차

```bash
CURL=$(command -v curl || echo /usr/bin/curl)    # curl이 PATH에 없으면 절대경로로
BASE="https://$OWNER.github.io/$REPO"
for st in / "/<section-slug>/<문서>.html" ; do $CURL -s -o /dev/null -w "%{http_code}  $st\n" "$BASE$st"; done
```
- **Playwright headless 렌더 검증**(`/tmp`에 임시 설치 → 실행 → `rm -rf` 정리): 랜딩 카드 수, 각 문서 "← 핸드북 홈" **visible**, 랜딩 전체검색 결과·이동·`?q=` 자동 하이라이트, 페이지 내 검색 하이라이트·개수·nav 유지. SVG 도식이 있으면 `figure`별 스크린샷으로 오버플로·겹침 확인.
- `docs/` 밖 파일(CHANGELOG 등)은 사이트에서 404(미게시) 확인. 모바일 375px 레이아웃.

---

## 14. 함정·교훈 (반복 금지)

| 함정 | 대응 |
|------|------|
| 클라우드 동기화 폴더가 `.git` 동기화 → 손상 | `xattr -w 'com.apple.fileprovider.ignore#P' 1 .git`. 프로젝트는 동기화 폴더 안에 그대로(분산 회피) |
| 무료 플랜 비공개 Pages 불가 | GitHub Pro. 게시 폴더는 `/` 또는 `docs`만 |
| 폴더명 공백 → `%20` URL | 무공백 슬러그 + 교차 링크 수정 |
| 절대경로 링크 깨짐 | **상대경로만**(base가 `/REPO/`) |
| 표 짝수행 어두운 배경 → 가독성 0 | `#f6f8fa` |
| 한 문단 `1) 2) 3)` 평문 → 줄바꿈 안 됨 | `<ol>/<ul>` 구조화 |
| 페이지 내 검색 nav 필터가 묶음 라벨 통째로 숨김 | nav 필터링 제거(하이라이트만) |
| 페이지 내 검색이 SVG `<text>`에 `<mark>` 주입 → 라벨 깨짐 | `inpage-search.js`에 SVG 네임스페이스 제외 가드(이미 포함) |
| 하위→루트 복귀 링크 누락 | 모든 nav 상단 "← 핸드북 홈"(템플릿에 내장) |
| CDN `max-age=600` 캐시 | 검증은 `?cb=$(date +%s)`/Playwright, 브라우저 ⌘+Shift+R |
| `curl` PATH 없음 / zsh `status` 예약어 | curl 절대경로 / 루프 변수 `st` |
| 예시의 숨은 전제 | 재현 가능하게(현재 폴더 대상) 또는 전제 명시 |
| **검증 생략하고 발행** | §6 내용 검증 + §7 한국어 검수 **둘 다 통과 후** 발행 |

커밋 메시지 끝: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

---

## 15. 실행 체크리스트

- [ ] 파라미터 확정(**TOPIC은 사용자 입력**/REPO/OFFICIAL_SOURCES/VERSION_TARGET/PROJECT_DIR/OWNER), 섹션 분할안 사용자 확인
- [ ] 공식 문서 조사(버전·수집일 기록)
- [ ] **이 스킬 `assets/`·`templates/`** 에서 `*.js`·`.nojekyll`·`index.html`·`.gitignore`·`Section_*.html` 복사(§4)
- [ ] `docs/<section>/` `*_Manual.html`(레퍼런스)+`*_Examples.html`(실습) 작성 — 플레이스홀더를 실제 내용으로, 핵심 동작 1~3문장, 3단계 시나리오, 맥락적 타당성
- [ ] **§6 내용 검증 하네스 실행**(학생→강사, 검토자→종합→적용)
- [ ] **§7.5 SVG 도식화**(선별) — 흐름·구조·비교 등 최적 지점
- [ ] **§7 한국어 문법·어순 검수 하네스 실행**(코드 보존, 산문만, 과교정 금지) — 발행 전 필수 게이트
- [ ] `site-search.js` `DOCS` 교체, `index.html` 제목·카드 교체
- [ ] 랜딩 최종 업데이트 날짜 + `CHANGELOG.md`
- [ ] git init + `.git` 동기화 제외 + 커밋 → `gh repo create --private --source=. --push` → Pages(main/docs) → built
- [ ] curl 200 + Playwright 렌더 검증 + 임시파일 정리

---

## 16. 전달용 킥오프 프롬프트 (파라미터만 채워 새 세션에 붙여넣기)

```text
이 스킬의 제작 지시서(references/BUILD_GUIDE.md)를 먼저 끝까지 읽고 그대로 따라줘.

[작업] <TOPIC> 을(를) 깊게 다루는 한국어 핸드북을 만들어 GitHub Pages로 출판한다.
[파라미터]
- TOPIC = <사용자가 정한 주제. 예: Vercel 사용법>
- REPO  = <예: vercel-handbook>   (공개 URL에 노출되는 슬러그)
- OFFICIAL_SOURCES = <공식 문서·CLI 목록>
- VERSION_TARGET = <콘텐츠가 다루는 버전/플랫폼 기준>
- PROJECT_DIR = <새 프로젝트 폴더 절대경로>
- OWNER = <GitHub 계정/조직>

[필수 — 생략 불가]
- 추측 금지: WebSearch/WebFetch로 OFFICIAL_SOURCES 확인 후에만 작성. 버전·수집일 기록.
- §6 내용 검증 하네스(학생→강사, 검토자 렌즈→종합→적용)를 반드시 실행.
- §7.5 SVG 전문 디자이너 서브에이전트로 흐름·구조·비교 개념을 도식화(최적 지점에 선별).
- §7 한국어 문법·어순 검수 하네스를 발행 전 반드시 실행. 코드·식별자는 손대지 말고 산문만 교정, 의미 변경·과교정 금지.
- 재사용 자산은 이 스킬의 assets/·templates/ 에서 복사(디자인·검색·배포는 도메인 무관). 콘텐츠만 새로 작성.
- 배포: 비공개 저장소 + 공개 Pages(main/docs), 클라우드 동기화 폴더는 .git만 제외, 단일 위치 유지.
- 검증: curl 200 + Playwright headless(홈링크 visible, 검색 동작, ?q= 자동 하이라이트).

[진행 방식] 먼저 (1) 자료 조사 계획 (2) 섹션 분할안을 제시하고, 구현 착수 전 핵심 결정은 나에게 확인받아라.
```

---

*이 지시서는 도메인 무관 범용판이다. 재사용 자산(검색 JS·HTML 골격·`.nojekyll`·`.gitignore`)은 이 스킬의 `assets/`·`templates/`에 동봉되어 있다.*
