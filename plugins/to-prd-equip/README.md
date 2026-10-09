# to-prd-equip 플러그인 (초안 0.1.0)

장비 소프트웨어용 PRD 스킬 두 개를 함께 배포합니다. 별도 MCP 서버나 서비스 로그인은 필요하지 않습니다.

| 스킬 | 역할 |
|---|---|
| `to-prd-equip` | 고객 변경 요청서와 현재 상태 문서로 bkit용 변경 영역 PRD(제품·고객 정본, feature PRD, 착수 게이트)를 만듭니다 |
| `code-prd-equip` | 현장 기준 버전의 소스에서 변경 영역의 현재 상태를 근거·신뢰도와 함께 추출합니다. 값은 확인 전까지 `[역추출]`입니다 |

## 설치

Claude Code:

```text
/plugin install to-prd-equip --marketplace donchang07/skills
```

이전 버전 Claude Code에서는 `/plugin marketplace add donchang07/skills` 후 `/plugin install to-prd-equip@donchang-skills`를 씁니다.

Codex:

```bash
codex plugin marketplace add donchang07/skills --ref main
codex plugin add to-prd-equip@donchang-skills
```

앱을 재시작한 뒤 새 채팅에서 고객 변경 요청서를 전달하거나, 장비 소스의 현재 상태 추출을 요청합니다.

## 업데이트

Claude Code는 `/plugin marketplace update donchang-skills`, Codex는 `codex plugin marketplace upgrade donchang-skills`로 받습니다.

## 유지보수

편집 원본은 저장소 루트의 `to-prd-equip/`과 `code-prd-equip/`입니다. 이 폴더의 `skills/`는 생성된 배포본이므로 직접 고치지 않습니다.

```bash
node scripts/build-to-prd-equip-plugin.mjs
node scripts/build-to-prd-equip-plugin.mjs --check
```

새 버전을 배포할 때 `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`의 버전을 함께 바꿉니다. 버전의 앞 두 자리는 고객 변경 요청서 양식 버전(`to-prd-equip/references/request-mapping.md`)과 같아야 합니다.

이 저장소의 GitHub 마켓플레이스에서 배포합니다. 초안이므로 실제 고객 요청서·소스로 보정하기 전까지 결과를 사람이 검토해야 합니다.
