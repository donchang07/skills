# Chang PPT

원본은 저장소의 `chang-ppt/`다. 이 플러그인은 동일한 스킬·템플릿·도구를 Claude Code에 배포한다.

## Claude Code 사용

현재 PC에 개인 스킬로 설치하려면 저장소 루트에서 다음을 실행한다.

```sh
node scripts/build-chang-ppt-plugin.mjs --install-claude
```

Claude Code에서 `/chang-ppt`로 호출한다. 설치 후 현재 세션에 보이지 않으면 새 세션을 시작한다.

마켓플레이스로 설치하는 방법:

```text
/plugin marketplace add donchang07/skills
/plugin install chang-ppt@donchang-skills
```

플러그인 호출은 `/chang-ppt:chang-ppt`다. 개인 설치와 플러그인 중 원하는 방식을 사용한다.

Windows 편집 도구는 PowerPoint와 Pretendard가 필요하다. Python 구조 검증기는 표준 라이브러리만 사용한다. Codex 전용 하네스나 presentations 스킬이 없어도 공통 스토리·브랜드·검증 계약을 적용할 수 있다.

## 배포 확인

```sh
node scripts/build-chang-ppt-plugin.mjs
node scripts/build-chang-ppt-plugin.mjs --check
```

[Claude Code 스킬 문서](https://code.claude.com/docs/en/skills), [플러그인 명세](https://code.claude.com/docs/en/plugins-reference)
