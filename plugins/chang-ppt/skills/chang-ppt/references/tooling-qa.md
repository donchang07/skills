# 재사용 도구와 결과 검증

반복 편집·실제 렌더·스킬 및 PPT 결과 검증 때 읽는다. 아래 경로는 이 스킬 폴더 기준이다. 문서·도구 업데이트와 실제 PPT의 시각 검증은 구분한다.

## 환경과 입력

Claude Code 등에서 presentations 스킬이 제공되지 않으면 그 설치를 필수로 요구하지 않는다. 이 스킬의 편집·검증 스크립트와 현재 사용 가능한 도구를 사용한다. 동봉 편집기는 Windows PowerPoint COM용이다. 다른 운영체제에서는 이용 가능한 PPT 편집·렌더 도구로 같은 계약을 구현하고 미지원 항목을 기록한다. Python 구조 검증기는 운영체제와 독립적이다.

PPT 작업 전에 설치된 presentations 스킬을 읽고 실제 제공되는 편집 도구를 확인한다. Windows PowerPoint COM을 사용할 때는 PowerPoint와 Pretendard 설치를 확인한다. 다른 렌더러를 사용하면 렌더러와 글꼴 대체 여부를 기록하고, PowerPoint에서 확인한 결과라고 하지 않는다. 한글 파일은 명시적인 UTF-8로 읽고 쓴다. Windows PowerShell에서 Python으로 한글 코드를 파이프 전달하지 말고 UTF-8 파일로 저장하여 실행한다. JSON은 BOM 없이 저장하거나 읽을 때 utf-8-sig로 처리한다. 터미널 표시가 깨졌다는 이유만으로 원본 인코딩이 손상됐다고 단정하지 않는다.

## Narrative 편집 계약과 실행

`scripts/apply_narrative.ps1`은 이미 설명 공간이 확보된 PPT의 narrative만 추가·교체한다. 본문을 자동 재배치하거나 도형 충돌을 완전히 해결하는 도구가 아니다. 먼저 story-contract.md의 설계를 완료한다. 좌표 단위는 point(72pt=1인치)다. 서체는 Pretendard 14pt이며 임의 축소하지 않는다.

```json
{
  "font_size_pt": 14,
  "preserve_nonstory": true,
  "preserve_notes": true,
  "preserve_brand": true,
  "layout": {"x": 50, "y": 410, "width": 860, "height": 78, "gap": 7},
  "slides": [
    {"slide_id": 300, "role": "content", "headline": "핵심 관계를 설명하는 문장입니다.", "detail": "이 관계가 뜻하는 의미와 적용 조건을 설명합니다."},
    {"slide_id": 301, "role": "part"}
  ]
}
```

예시의 ID는 대상 PPT에서 추출한 실제 SlideID로 교체한다. `slide_index`는 순서가 확정된 일회 작업에서만 보조적으로 사용한다. `slides`는 이번 작업 대상으로 제한할 수 있다. 좌표는 13⅓×7.5인치 덱의 예이며 실제 본문·출처와 대조해 정한다. 각 장에 `layout`을 지정할 수 있다. 일반 설명은 무배경이 기본이며 사용자 채택 패널 유지 여부는 도구의 panel 옵션으로 명시한다. 기존 본문·캡션을 통합하는 변경은 이 도구 밖에서 명시적으로 처리한다.

```powershell
powershell -NoProfile -File scripts/apply_narrative.ps1 -Source source.pptx -Output revised.pptx -Contract contract.json -RenderDir renders
python scripts/inspect_deck.py --source source.pptx --result revised.pptx --contract contract.json --report qa.json
```

편집기는 관리 대상 narrative 도형만 교체하고 출력 PPTX와 metrics를 저장한다. 명시된 headline/detail을 사용하므로 마침표 기반 분리가 없다. 같은 원본·출력 경로 및 기존 결과 덮어쓰기는 거부한다. 재실행은 직전 결과를 새 입력으로 하고 새 결과 경로를 사용한다. `RenderDir`을 지정하면 실제 PowerPoint PNG를 생성한다. 화면을 사람이 검토한 것과 PNG 생성은 별개다.

## 결과 QA

`inspect_deck.py`는 표준 Python 라이브러리로 원본·결과 PPTX를 비교한다. 계약의 역할별 narrative 유무, 문구·굵기·14pt·가운데 정렬, 슬라이드 ID/순서, 고정 페이지, 비대상 도형, 노트, 마스터·레이아웃을 확인한다. `preserve_*`는 narrative만 편집할 때 true가 기본이다. 본문·노트 변경이 요청된 경우 해당 항목을 false로 완화할 수 있지만, 그 범위는 별도 편집 계약으로 명시하고 실제 diff를 검토해야 한다. 검사기를 통과시키려고 보존 옵션을 무조건 끄지 않는다.

정적 검사는 줄바꿈의 실제 결과, 글꼴 대체, 가림, 광학적 중앙 정렬을 증명하지 않으며 `visual_validation: not_run`을 남긴다. 실제 렌더에서 강조 한 줄, 설명의 다음 줄 시작, 두 텍스트의 중심, 잘림·겹침, 출처 간격, 도형 연결 방향·끝점을 확인한다. 전체 덱의 순서·고정 페이지를 확인하고 변경 장은 개별 이미지로 검토한다. 여러 장을 한 번에 출력하다 이미지가 잘렸다면 미확인 장을 작은 묶음 또는 개별로 다시 연다.

신규 덱의 형식만 검사하려면 source=result를 사용할 수 있으나 원본 보존 검증 근거로 삼지 않는다. 일반 전체 재설계는 narrative 전용 검증 외에 설치된 presentations의 package/geometry 검사와 시각 검토를 병행한다. 기존 경계 경고는 원본에서도 존재하는지 비교해 이번 변경의 오류와 구분한다.

## 도구 자체 검증과 최종 기록

도구를 변경하면 실제 복사본에 두 번 적용해 관리 도형 수·문구가 같고 원본 지문이 불변인지 확인한다. 글자가 넘치는 경우와 문구·굵기가 잘못된 결과를 실패로 탐지하는지도 확인한다. 텍스트만 적은 장, 긴 한글, 표·코드, 출처 있는 장, Part 구분을 대표 사례로 삼고 변경과 관련된 사례만 재실행한다. 모든 새 도구에 무관한 전체 덱 검사를 강제하지 않는다.

스킬 구조 검사는 `python scripts/check_skill.py`로 실행한다. 기본 대상은 스크립트가 속한 스킬이며 다른 사본은 `--skill-root <경로>`로 지정한다. 이 검사는 frontmatter·참조·표 코드 AST·템플릿 패키지를 확인한다. 동작 검증이나 실제 PPT 렌더링을 대신하지 않는다.

원본·결과 raw SHA-256, 기준 스킬, 계약, 렌더 환경, metrics, 개별 화면 확인 범위와 발견 사항을 함께 저장한다. QA 보고서와 최종 PPT가 확정된 뒤에만 하네스에 결과를 등록한다. 자세한 부분 재실행·협업 절차는 [orchestration.md](orchestration.md)를 따른다.
