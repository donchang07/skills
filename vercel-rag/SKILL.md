---
name: vercel-rag
classification: capability
classification-reason: "Reference guide capturing architecture decisions and bug fixes for a specific integration (PDF RAG ingestion on Vercel + Supabase), not a repeatable multi-step user workflow."
deprecation-risk: none
effort: medium
description: |
  Vercel(Next.js Route Handlers + Python serverless functions) + Supabase(Storage, pgvector)
  환경에서 PDF 업로드 → 표/다이어그램까지 포함한 RAG 파이프라인을 만들 때 실제로 부딪혔던
  플랫폼 제약과 버그, 그리고 그 해결책을 정리한 레퍼런스.
  Triggers: PDF RAG, PDF 업로드, pdfplumber, Vercel Python function, Supabase Storage 업로드,
  413 Request Entity Too Large, 504 timeout, DOMMatrix is not defined, pdf-parse
  Keywords: RAG, PDF, pdfplumber, pdf-parse, Vercel serverless, Python function, Supabase Storage,
  signed URL, maxDuration, timeout, middleware, DOMMatrix
argument-hint: "(no args — reference this skill when building or debugging PDF ingestion on Vercel+Supabase)"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# vercel-rag

Vercel(Next.js) + Supabase 스택에서 **PDF를 업로드해 표/다이어그램까지 포함한 RAG 파이프라인**을 만들 때
실제로 겪은 5개의 서로 다른 실패와 그 원인/해결책을 정리한 가이드. 처음부터 이 문서를 읽고 시작하면
같은 시행착오를 반복하지 않는다.

## 언제 이 스킬을 참고하는가

- PDF/문서를 업로드해서 벡터DB에 넣는 RAG 기능을 Vercel + Supabase로 만들 때
- "표가 잘 안 뽑혀요", "이미지/다이어그램 설명이 필요해요" 같은 요구가 있을 때
- `pdf-parse`를 썼는데 `DOMMatrix is not defined` 같은 에러가 날 때
- 파일 업로드에서 `413 Request Entity Too Large` 또는 `504` 타임아웃이 날 때

## 최종 아키텍처 (검증됨)

```
브라우저
  │  1. PDF를 Supabase Storage에 "직접" 업로드 (Next.js 서버를 거치지 않음)
  ▼
Supabase Storage (private bucket, RLS: 본인 폴더만 read/write/delete)
  │
  │  2. 브라우저 → Next.js Route Handler: { storagePath, filename } 만 JSON으로 전달 (파일 본문 없음)
  ▼
Next.js Route Handler (app/api/rag/ingest/route.ts)
  │  3. Storage signed URL 생성 (createSignedUrl, 120초 유효)
  │  4. Python 함수에는 signed URL만 JSON으로 전달 (파일 본문을 절대 다시 실어나르지 않음)
  ▼
Vercel Python 함수 (api/pdf_extract.py, pdfplumber)
  │  5. signed URL로 직접 PDF 다운로드 (urllib.request — outbound fetch라 inbound body 제한과 무관)
  │  6. 페이지별 text / table(마크다운 변환) / 페이지 이미지(base64, JPEG) 추출
  ▼
Next.js Route Handler로 결과 반환
  │  7. 페이지 이미지가 있으면 비전 LLM 호출(동시성 4~6개로 제한)해 다이어그램만 설명
  │  8. 페이지별 [텍스트 + 표 + 다이어그램 설명]을 합쳐 청킹 → 임베딩 → pgvector insert
  │  9. finally 블록에서 Storage 원본 PDF 삭제 (처리 후 폐기 — 추출된 텍스트/임베딩만 남김)
```

## 겪은 문제 5가지와 원인/해결

### 1. `pdf-parse` v2 → `ReferenceError: DOMMatrix is not defined`
- **원인**: `pdf-parse` v2.x는 내부적으로 `pdfjs-dist`를 쓰는데, 브라우저 전용 API(`DOMMatrix` 등)를
  참조하는 코드 경로를 Node.js 서버리스 환경에서도 타는 경우가 있다.
- **1차 해결**: `pdf-parse@1.1.1`(구버전, 순수 텍스트 추출)로 다운그레이드.
- **2차 문제**: v1은 webpack으로 번들링하면 `index.js`의 디버그 코드가 실행되어
  `ENOENT: .../test/data/05-versions-space.pdf`를 찾으려는 별개의 버그가 있다.
  → `import pdfParse from "pdf-parse/lib/pdf-parse.js"`처럼 **내부 lib 경로로 직접 import**해서 우회.
  타입 선언이 없으므로 `declare module "pdf-parse/lib/pdf-parse.js"` ambient d.ts 파일을 하나 추가해야 한다.
- **최종 해결(이 프로젝트)**: 표/레이아웃 품질이 중요해서 아예 `pdf-parse` 자체를 걷어내고
  Python `pdfplumber`로 교체했다. 단순 텍스트만 필요하면 위의 v1 우회 방식으로 충분하다.

### 2. 표/다이어그램 품질이 필요하면 Node엔 답이 없다 → Vercel Python 함수
- LangChain.js의 PDF 로더도 결국 `pdf-parse`를 감싼 것일 뿐이라, 표 구조 복원 능력은 없다.
- **PDFPlumber(Python)** 는 `pdfminer.six` 위에서 문자 좌표를 분석해 표를 복원하는데, JS 포트가 없다.
- **다행히 Vercel은 Next.js와 같은 프로젝트 안에 Python 서버리스 함수를 네이티브로 지원한다**:
  - 레포 루트의 `api/` 디렉토리(Next.js의 `app/api`와는 별개)에 `.py` 파일을 두면 자동으로
    `/api/<파일이름>` 엔드포인트가 된다. 서로 라우팅 충돌 없음.
  - 핸들러 형태는 `http.server.BaseHTTPRequestHandler`를 상속한 `handler`라는 이름의 클래스,
    `do_POST(self)` 메서드 안에서 `self.rfile`로 읽고 `self.wfile.write`로 응답:
    ```python
    from http.server import BaseHTTPRequestHandler

    class handler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            # ... 처리 ...
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response_bytes)
    ```
  - 같은 디렉토리(또는 레포 루트)에 `api/requirements.txt`를 두면 자동으로 pip install 된다.
    (예: `pdfplumber`, `Pillow`)

### 3. 파일 업로드가 `413 Request Entity Too Large` — 두 번 걸린다
- Vercel 서버리스 함수는 **inbound 요청 본문이 약 4.5MB로 제한**된다. 이 제한은 두 지점에서 걸린다:
  1. 브라우저 → Next.js Route Handler로 파일을 `FormData`/body로 올릴 때
  2. (놓치기 쉬움) Next.js Route Handler가 그 파일을 **다시 Python 함수로 그대로 전달**할 때 —
     이것도 "inbound 요청"이라 똑같이 4.5MB 제한을 받는다.
- **해결**:
  1. 브라우저에서 **Supabase Storage에 직접 업로드**(Next.js 서버를 아예 거치지 않음) —
     Supabase JS 클라이언트로 `supabase.storage.from(bucket).upload(path, file)`.
  2. Next.js Route Handler는 파일을 "받지 않고", `{ storagePath, filename }`만 JSON으로 받는다.
  3. Route Handler는 `supabase.storage.from(bucket).createSignedUrl(path, 120)`으로 짧은 유효기간의
     signed URL을 만들어 Python 함수에 **그 URL만** 전달한다 (JSON, 몇백 바이트).
  4. Python 함수는 `urllib.request.urlopen(signed_url)`로 **자기가 직접** 파일을 다운로드한다 —
     이건 outbound fetch라서 inbound body 제한과 무관하다.
  - Storage 버킷은 private으로 만들고, RLS로 `(storage.foldername(name))[1] = auth.uid()::text`
    패턴을 써서 "본인 폴더"만 read/write/delete 되도록 제한한다.
  - **파일명에 한글/공백이 들어가면 Storage 키가 "Invalid key" 에러**를 낼 수 있다 —
    Storage 오브젝트 경로는 `${user.id}/${crypto.randomUUID()}.pdf`처럼 UUID 기반으로 만들고,
    원래 파일명은 DB 컬럼(표시용)으로만 별도 저장한다.

### 4. 미들웨어가 내부 서버간 호출까지 `/login`으로 튕긴다
- 로그인 안 된 요청을 `/login`으로 리다이렉트하는 전역 `middleware.ts`가 있다면,
  **Next.js가 자기 자신의 다른 API(Python 함수 포함)를 서버사이드로 fetch할 때도 이 미들웨어에 걸린다.**
- 증상: 직접 `curl`로 Python 함수를 호출하면 `307 Redirecting...`이 온다.
- **해결**: 브라우저가 직접 호출하지 않고 서버간 호출 전용인 내부 엔드포인트(예: `/api/pdf_extract`)를
  미들웨어의 public/제외 경로 목록에 명시적으로 추가한다.

### 5. 504 타임아웃 — 페이지별 비전 모델 호출이 누적된다
- 다이어그램 설명을 위해 페이지 이미지를 비전 LLM에 넣는 구조라면, **업로드 처리 시간이 페이지 수에
  비례**해서 늘어난다. 기본 `maxDuration`(짧으면 10초)로는 몇 페이지만 넘어가도 타임아웃 난다.
- **해결**:
  - Next.js Route Handler: `export const maxDuration = 300;` (플랜에 따라 상한 다름 — Hobby는 보통
    60초 근방, Pro 이상은 훨씬 큼. 배포가 실패하면 상한을 낮춰가며 확인)
  - Python 함수: `vercel.json`에 `{"functions": {"api/pdf_extract.py": {"maxDuration": 300}}}`
  - `memory` 키는 Vercel의 Fluid Compute(Active CPU 과금) 하에서는 **무시되고 경고만 뜬다** —
    설정에서 빼는 게 깔끔하다.
  - 비전 모델 호출은 순차/완전병렬이 아니라 **동시성 4~6개로 제한한 배치**로 처리한다
    (작은 concurrency-limited mapper를 직접 구현하면 충분, 새 의존성 불필요).

## 디버깅 체크리스트

1. 에러 메시지가 애매하면(`요청이 실패했어요 (500)` 같은) — **하위 함수의 실제 에러 바디를
   그대로 상위로 전파**하도록 고쳐라. 그래야 413/500/504가 다른 원인임을 구분할 수 있다.
2. `413` → 어느 hop에서 몇 MB가 어떤 방향(inbound)으로 가는지부터 확인.
3. `504`/타임아웃 → `maxDuration` 설정과, 페이지 수 × LLM 호출 시간을 곱해서 추정.
4. Python 함수가 이상하면 `curl -X POST <url> --data-binary @file.pdf`로 **직접** 때려서
   Next.js 레이어를 배제하고 원인을 좁혀라.
5. 업로드 원본 파일은 처리 끝나면 (성공/실패 무관하게 `finally`에서) Storage에서 삭제해서
   비용과 개인정보 보관을 최소화한다.

## 관련 파일 (이 프로젝트 기준 예시)

- `api/pdf_extract.py`, `api/requirements.txt` — Python 추출 함수
- `vercel.json` — 함수별 `maxDuration` 설정
- `app/api/rag/ingest/route.ts` — signed URL 중계 + 비전 호출 + 청킹/임베딩
- `lib/pdfPageDescribe.ts` — 페이지 이미지 → 다이어그램 설명 (비전 LLM)
- `middleware.ts` — 내부 전용 엔드포인트를 public 경로로 예외 처리
- Supabase Storage 버킷 + RLS 정책 (마이그레이션 SQL로 관리)
