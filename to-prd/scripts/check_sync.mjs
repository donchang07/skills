#!/usr/bin/env node
// 템플릿·핸드북에는 현업 사용법만 두고 내부 계약은 스킬에서 검사한다.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const mapping=read('references/brief-mapping.md'), skill=read('SKILL.md');
const version=mapping.match(/브리프 버전: (v\d+\.\d+)/)?.[1];
const names=[`PRD템플릿_${version}.docx`,`PRD작성핸드북_${version}.docx`];
const python=process.env.CODEX_DOCX_PYTHON||(process.platform==='win32'?path.resolve(path.dirname(process.execPath),'../../python/python.exe'):'python3');
function docx(name){
 const code="import json,sys; from docx import Document; d=Document(sys.argv[1]); print(json.dumps({'title':d.core_properties.title,'paragraphs':[p.text for p in d.paragraphs],'headings':[p.text for p in d.paragraphs if p.style.name=='Heading 1']},ensure_ascii=True))";
 return JSON.parse(execFileSync(python,['-c',code,path.join(root,'assets/brief',name)],{encoding:'utf8'}));
}
const tpl=docx(names[0]), hb=docx(names[1]), results=[];
const check=(name,ok)=>results.push({name,ok:Boolean(ok)});
check('브리프 버전',version);
check('현행 DOCX 두 개만 배포',fs.readdirSync(path.join(root,'assets/brief')).filter(p=>p.endsWith('.docx')).sort().join('|')===names.slice().sort().join('|'));
check('파일명 참조 일치',[skill,mapping,read('README.md')].every(t=>names.every(n=>t.includes(n))));
check('파일 속성 버전',[tpl,hb].every(d=>d.title.includes(version)));
check('템플릿 제목',tpl.paragraphs[0]==='to-prd를 사용하기 위한 PRD 템플릿');
check('핸드북 제목',hb.paragraphs[0]==='to-prd 핸드북');
const headings=['1 업무 문제와 목표','2 사용자와 업무 흐름','3 필요한 화면과 기능','4 업무 규칙과 예외','5 데이터와 필수 조건','6 완료 기준과 참고 자료'];
check('템플릿 6개 장',JSON.stringify(tpl.headings)===JSON.stringify(headings));
check('모든 장의 PRD 매핑',headings.every(h=>mapping.includes('| '+h+' |')));
check('핸드북 4개 장',JSON.stringify(hb.headings)===JSON.stringify(['1 템플릿 작성','2 to-prd 실행','3 결과 검토','4 변경 및 개발 요청']));
check('핸드북 현행 템플릿 참조',hb.paragraphs.join('\n').includes(names[0]));
check('현업 문서 내부 기술 설명 제거',[tpl,hb].every(d=>!/기본값|Playwright|match rate|data-testid/.test(d.paragraphs.join('\n'))));
check('핵심 업무 입력 유지',['현재 불편한 점','원하는 변화','이번에 제외할 것과 이유','AI를 사용하는 경우','반드시 지킬 조건','반드시 끝까지 되어야 할 업무','성공을 확인할 기준'].every(t=>tpl.paragraphs.join('\n').includes(t)&&mapping.includes(t)));
const aiLabels=['AI가 잘했다고 볼 기준','AI가 절대 하면 안 되는 것','AI가 확신이 없을 때','사람이 반드시 확인할 조건','비용과 기다릴 수 있는 시간','문제가 생기면 되돌릴 조건'];
check('AI 입력 6칸: 템플릿 ↔ 매핑',aiLabels.every(t=>tpl.paragraphs.join('\n').includes(t)&&mapping.includes('| '+t+' |')));
check('AI 입력 6칸: 핸드북 안내',['잘했다고 볼 기준','절대 하면 안 되는 것','사람이 반드시 확인할 조건','되돌릴 조건','확인용 실제 사례'].every(t=>hb.paragraphs.join('\n').includes(t)));
check('성공 지표 입력: 템플릿 ↔ 핸드북 ↔ 스킬',tpl.paragraphs.join('\n').includes('언제 누가 확인할지')&&hb.paragraphs.join('\n').includes('언제 누가 확인')&&skill.includes('G-*')&&mapping.includes('_review.md')&&skill.includes('_review.md'));
check('확정 판정: 템플릿 ↔ 핸드북 ↔ 매핑',tpl.paragraphs.join('\n').includes('(추정)')&&hb.paragraphs.join('\n').includes('(추정)')&&mapping.includes('`(추정)` 표시')&&skill.includes('확정이라는 말을 아낀다'));
check('변경 영향 안내: 핸드북 ↔ 스킬',hb.paragraphs.join('\n').includes('다시 손봐야 할 것')&&skill.includes('부록 C')&&read('assets/prd-template.md').includes('## 부록 C. 변경 이력과 영향'));
check('작성 모드: 핸드북 ↔ 스킬',hb.paragraphs.join('\n').includes('과제 크기에 맞춰 분량')&&skill.includes('## Step 1.5 — 작성 모드 판정'));
check('출력 경로 대소문자 일치',!/docs\/prd\.(md|html)/.test(hb.paragraphs.join('\n'))&&hb.paragraphs.join('\n').includes('docs/PRD.md')&&skill.includes('docs/PRD.md'));
check('질문 수 규칙 일치',mapping.includes('최대 4문항')&&skill.includes('최대 4문항'));
check('내부 실행 계약 유지',['AI 판정 계약','NG-*','Playwright','data-testid','match rate','세 관문','EV-*','AI 판단 보류','11.6'].every(t=>skill.includes(t)));
check('AI 계약: 템플릿 PRD ↔ 게이트 ↔ 검증기',['### 11.5 AI 품질 평가','### 11.6 AI 운영 기준','| AI 판단 보류 |'].every(t=>read('assets/prd-template.md').includes(t))&&read('references/gate-checklist.md').includes('| HG-15 |')&&read('scripts/validate_prd.mjs').includes('11.5 AI 품질 평가'));
check('스키마 일치',[skill,mapping,read('assets/prd-template.md'),read('scripts/validate_prd.mjs')].every(t=>t.includes('screen-first-v3')));
for(const r of results)console.log((r.ok?'PASS ':'FAIL ')+r.name);
const fail=results.filter(r=>!r.ok).length;
console.log('Summary: PASS '+(results.length-fail)+', FAIL '+fail);
process.exitCode=fail?1:0;
