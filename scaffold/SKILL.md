---
name: scaffold
description: 사용자가 명시적으로 프로젝트 또는 레포를 스캐폴드/초기 세팅해 달라고 요청할 때만 사용한다. 실제 기능 구현 전에 패키지와 기본 앱 구조를 준비한다.
---

# Scaffold

## 사용 조건

사용자가 명시적으로 "스캐폴드", "초기 세팅", "레포 세팅", "프로젝트 세팅"처럼 실제 작업 전 준비를 요청할 때만 이 스킬을 사용한다.

기능 구현, UI 구현, DB 설계, 인증 구현, 화면 목업 작성 요청에는 이 스킬을 자동으로 사용하지 않는다. 그런 작업은 별도 요청이 있을 때 진행한다.

## 기본 스택

사용자가 다른 기술 스택을 명시하지 않으면 다음을 기본값으로 사용한다.

- TypeScript
- Next.js App Router
- Tailwind CSS
- Supabase

**Tailwind CSS를 기본으로 포함한다.** 사용자가 명시적으로 제외를 요청하거나 다른 CSS 솔루션을 명시하면 그 요청을 우선한다.

사용자가 특정 스택을 명시하면 그 요청을 우선한다. 예를 들어 Vite, Remix, 다른 DB를 명시하면 기본값을 고집하지 않는다.

## 작업 범위

스캐폴드의 목표는 "실제 작업을 시작할 수 있는 최소 레포 상태"를 만드는 것이다.

포함할 것:

- 필요한 패키지 설치
- Next.js App Router 기반 기본 앱 생성 또는 기존 앱 보정
- Tailwind CSS 기본 포함
- Supabase 클라이언트 패키지 설치
- docs/DESIGN.md에 지정된 아이콘 라이브러리 설치
- 빌드가 통과하는지 확인

포함하지 않을 것:

- 실제 기능 구현
- 인증 플로우 구현
- DB 스키마/마이그레이션 작성
- UI 화면 제작
- 테스트 세팅
- 배포 세팅
- 복잡한 아키텍처 리팩터링

## 진행 순서

### 1. 현재 레포 상태 확인

먼저 현재 디렉터리와 레포 상태를 확인한다.

```bash
pwd
git status --short
rg --files -g 'package.json' -g 'package-lock.json' -g 'app/**' -g 'src/app/**'
```

`package.json`이 이미 있으면 새 프로젝트를 덮어씌우지 말고, 기존 구조에 필요한 패키지와 설정만 보정한다.

현재 디렉터리에 `CLAUDE.md`, `AGENTS.md`, `docs/` 같은 비-Next 파일이 이미 있어도, step 2의 임시 폴더 병합 방식을 쓰면 덮어쓰지 않고 앱을 생성할 수 있다. 기존 파일과 사용자 변경사항은 삭제하거나 덮어쓰지 않는다.

### 2. Next.js 앱 생성

`package.json`이 없는 새 레포라면 `create-next-app`으로 앱을 생성한다.

주의: `create-next-app .`은 현재 폴더가 비어 있을 때만 동작한다. 폴더 안전 목록(`.git`, `.gitignore`, `README.md`, `docs/`, `LICENSE` 등)에 없는 파일이 하나라도 있으면 `The directory ... contains files that could conflict` 에러로 멈춘다. `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.env.example` 등이 여기서 충돌한다. 이 안전 목록은 create-next-app 패키지에 하드코딩돼 있어 플래그로 넓힐 수 없다.

따라서 빈 임시 폴더에 생성한 뒤 현재 폴더로 **덮어쓰지 않고 병합**한다.

```bash
# 1) 빈 임시 폴더에 생성한다. 폴더가 비어 있으니 충돌이 발생하지 않는다.
npx create-next-app@latest .scaffold-tmp --ts --app --tailwind --import-alias "@/*" --disable-git --yes

# 2) 생성 결과를 현재 폴더로 병합한다. -n(no-clobber)이라 기존 파일은 건드리지 않는다.
cp -Rn .scaffold-tmp/. ./

# 3) 임시 폴더를 정리한다.
rm -rf .scaffold-tmp
```

- `--disable-git`: 임시 폴더 안에 중첩 git 레포가 생기는 걸 막는다. 현재 레포의 `.git`은 그대로 둔다.
- `--yes`: 프롬프트 없이 기본 스택(TypeScript, App Router, Tailwind, import alias `@/*`)으로 생성한다.
- `cp -Rn .scaffold-tmp/. ./`: 숨김 파일까지 포함해 복사하되, 이미 있는 파일(`CLAUDE.md`, `docs/`, `README.md` 등)은 덮어쓰지 않는다.
- 병합 후 `.gitignore`를 확인한다. 기존 `.gitignore`가 보존돼서 `node_modules/`, `.next/`가 빠져 있으면 추가한다.

현재 폴더가 완전히 비어 있다면 임시 폴더 없이 `npx create-next-app@latest . --ts --app --tailwind --import-alias "@/*" --yes`를 바로 써도 된다.

`create-next-app` 옵션이 현재 버전과 맞지 않으면 `npx create-next-app@latest --help`로 확인한 뒤 같은 의도를 유지하는 최신 옵션으로 실행한다.

### 3. Supabase 패키지 설치

Supabase는 SSR/App Router 환경을 고려해 다음 패키지를 설치한다.

```bash
npm install @supabase/supabase-js @supabase/ssr
```

이 단계에서는 Supabase 프로젝트 생성, 인증 wiring, DB schema, RLS 정책 작성까지 진행하지 않는다. 사용자가 명시적으로 요청하면 별도 작업으로 진행한다.

환경 변수 파일을 만들 필요가 있으면 실제 secret을 쓰지 말고 예시 파일만 만든다.

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=
```

`service_role`, secret key, DB password 같은 민감한 값은 클라이언트에 노출되는 `NEXT_PUBLIC_` 변수에 넣지 않는다.

### 4. 아이콘 라이브러리 추가

`docs/DESIGN.md`에 지정된 아이콘 라이브러리를 확인한다. 프론트메터의 아이콘 필드를 우선 보고, 없으면 본문 Iconography 섹션을 참고한다. (예: `lucide-react`)

확인한 패키지를 `package.json`의 `dependencies`에 명시한 뒤 설치 명령으로 가져온다.

```bash
npm install
```

검증되지 않은 패키지를 임의로 `npm install <pkg>`로 즉석 설치하지 않는다. 설치할 의존성은 먼저 `package.json`에 명시한다.

`docs/DESIGN.md`가 없거나 아이콘 라이브러리를 특정할 수 없으면 임의로 고르지 말고 사용자에게 확인한다.

### 5. 빌드 검증

패키지 설치 후 최소 검증만 수행한다.

```bash
npm run build
```

빌드가 실패하면 스캐폴드 범위 안에서 해결 가능한 설정/패키지 문제만 수정한다. 기능 구현이 필요한 실패라면 원인을 설명하고 멈춘다.

테스트는 기본 범위에 포함하지 않는다.

### 6. 커밋

작업을 마치면 작성한 파일을 커밋한다.

## 작업 원칙

- 의존성은 `package.json`에 명시한 뒤 설치 명령으로 반영한다. 검증되지 않은 패키지를 근거 없이 임의로 `npm install <pkg>`로 즉석 설치하지 않는다. lockfile은 직접 손으로 편집하지 않는다.
- 기존 파일과 사용자 변경사항을 덮어쓰지 않는다.
- 새 기술 스택을 임의로 추가하지 않는다.
- Tailwind는 기본으로 포함한다. 사용자가 명시적으로 제외를 요청할 때만 뺀다.
- Supabase는 패키지 설치 수준까지만 기본 처리한다.
- 스캐폴드 완료 후 실제 구현으로 이어가지 않는다. 다음 작업은 사용자의 별도 지시를 기다린다.

## 완료 기준

- [ ] 기본 스택 또는 사용자가 명시한 스택이 반영되어 있다.
- [ ] 패키지 설치가 완료되어 있다.
- [ ] Supabase 기본 패키지가 설치되어 있다. 단, 사용자가 Supabase 제외를 요청했다면 생략한다.
- [ ] docs/DESIGN.md에 지정된 아이콘 라이브러리가 `package.json`에 명시되고 설치되어 있다.
- [ ] Tailwind가 기본으로 포함되어 있다. 단, 사용자가 제외를 요청했다면 생략한다.
- [ ] 빌드 명령이 통과한다.
- [ ] 실제 기능 구현, UI 구현, DB 설계는 시작하지 않았다.
- [ ] 커밋이 완료되어 있다.
