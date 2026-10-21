# Chang HTML

원본은 저장소의 `chang-html/`이다. 이 플러그인은 같은 스킬·템플릿·도구와 에이전트 5종을 Claude Code에 배포한다.

## Claude Code 사용

현재 PC에 개인 스킬과 에이전트로 설치하려면 저장소 루트에서 다음을 실행한다.

```sh
node scripts/build-chang-html-plugin.mjs --install-claude
```

`~/.claude/skills/chang-html/`과 `~/.claude/agents/chang-html-*.md`가 생긴다. Claude Code에서 `/chang-html`로 호출한다. 설치 후 보이지 않으면 새 세션을 시작한다.

마켓플레이스로 설치하는 방법:

```text
/plugin marketplace add donchang07/skills
/plugin install chang-html@donchang-skills
```

플러그인 호출은 `/chang-html:chang-html`, 에이전트 이름은 `chang-html:chang-html-builder`처럼 앞에 플러그인 이름이 붙는다.

## 필요한 것

- Python 3(표준 라이브러리만 사용): `validate.py`, `renumber.py`, `make_instructor.py`
- Node.js + Playwright Chromium: `render.mjs` (없으면 렌더 검사는 not_run으로 보고)

## 배포 확인

```sh
node scripts/build-chang-html-plugin.mjs
node scripts/build-chang-html-plugin.mjs --check
```
