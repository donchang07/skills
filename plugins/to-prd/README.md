# to-prd 플러그인

업무 브리프를 bkit용 PRD로 만드는 스킬과 템플릿·핸드북·디자인 기준·검증 스크립트를 포함합니다. 별도 MCP 서버나 서비스 로그인은 필요하지 않습니다.

## 설치

```bash
codex plugin marketplace add donchang07/skills --ref main
codex plugin add to-prd@donchang-skills
```

앱을 재시작한 뒤 새 채팅에서 to-prd를 선택하거나 업무 브리프를 전달해 PRD 작성을 요청합니다.

## 업데이트

```bash
codex plugin marketplace upgrade donchang-skills
```

앱을 재시작하고 새 채팅에서 사용합니다. 설치 상태는 `codex plugin list --json`으로 확인합니다.

## 유지보수

편집 원본은 저장소 루트의 `to-prd/`입니다. 이 폴더의 `skills/to-prd/`는 생성된 배포본입니다.

```bash
node to-prd/scripts/check_sync.mjs
node scripts/build-to-prd-plugin.mjs
node scripts/build-to-prd-plugin.mjs --check
```

스킬이나 자산을 수정한 뒤 배포본도 생성해 함께 커밋합니다. 새 버전을 배포할 때 `plugin.json`과 `.codex-plugin/plugin.json`의 버전을 함께 변경합니다. 동기화 검사는 Python과 python-docx를 사용하며 `CODEX_DOCX_PYTHON`으로 Python 실행 파일을 지정할 수 있습니다.

이 저장소의 GitHub 마켓플레이스에서 배포합니다. OpenAI 전체 공개 플러그인 디렉터리에 심사·게시된 플러그인은 아닙니다.
