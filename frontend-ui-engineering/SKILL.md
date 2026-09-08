---
name: frontend-ui-engineering
description: 프로덕션에 가까운 품질의 사용자 인터페이스를 만든다. 사용자-facing 화면을 만들거나 수정할 때, 컴포넌트 작성, 레이아웃 구현, 상태 관리, 반응형 UI, 시각/UX 문제 개선, AI가 만든 듯한 제네릭 UI가 아니라 짜임새 있고 완성도 있는 목업 또는 제품 UI가 필요할 때 사용한다. docs/DESIGN.md를 기준으로 기존 디자인 토큰과 컴포넌트를 재사용하거나 확장해야 하는 UI 작업에 사용한다.
---

# Frontend UI Engineering

## 개요

접근 가능한 완성품 수준의 UI보다는, 빠르게 검증 가능한 목업과 프로토타입을 우선한다. 단, 빠르더라도 조잡한 AI 기본값처럼 보이지 않게 한다. 프로젝트의 디자인 시스템, 일관된 레이아웃, 현실적인 상태 설계, 적절한 상호작용 패턴을 지켜서 디자인 감각 있는 엔지니어가 만든 화면처럼 보이게 한다.

## 작업 전 컨텍스트 확인

UI 작업을 시작하기 전에 반드시 `docs/DESIGN.md`를 읽고, 정의된 디자인 원칙, 토큰, 컴포넌트, 레이아웃 규칙을 기준으로 삼는다.

작업 이해에 필요하면 다음 문서를 선택적으로 읽는다.

- `docs/userflow.md`: 화면 흐름, 사용자 행동, 상태 전이를 이해해야 할 때
- `docs/idea.md`: 서비스 컨셉, 문제 정의, 사용자 맥락, 카피 톤을 이해해야 할 때

문서가 없거나 내용이 불충분하면 임의로 크게 해석하지 말고, 기존 코드와 가까운 방향으로 보수적으로 구현한다.

## 컴포넌트 구조

### 파일 구조

컴포넌트와 관련된 파일은 가까이 둔다. 예를 들어:

```txt
src/components/
  TaskList/
    TaskList.tsx
    use-task-list.ts
    types.ts
```

커스텀 훅과 타입 파일은 컴포넌트 상태나 타입이 복잡해질 때만 추가한다.

### 컴포넌트 패턴

설정값이 많은 컴포넌트보다 합성 가능한 컴포넌트를 선호한다.

```tsx
// 좋음: 합성 가능한 구조
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// 피하기: 설정값이 과도한 구조
<Card
  title="Tasks"
  headerVariant="large"
  bodyPadding="md"
  content={<TaskList tasks={tasks} />}
/>
```

컴포넌트는 하나의 역할에 집중시킨다.

```tsx
export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-center gap-3 p-3">
      <Checkbox checked={task.done} onChange={() => onToggle(task.id)} />
      <span className={task.done ? 'line-through text-muted' : ''}>{task.title}</span>
      <Button variant="ghost" size="sm" onClick={() => onDelete(task.id)}>
        <TrashIcon />
      </Button>
    </li>
  );
}
```

데이터 로딩과 화면 표현은 분리한다.

```tsx
export function TaskListContainer() {
  const { tasks, isLoading, error, refetch } = useTasks();

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="할 일을 불러오지 못했습니다." retry={refetch} />;
  if (tasks.length === 0) return <EmptyState message="아직 등록된 할 일이 없습니다." />;

  return <TaskList tasks={tasks} />;
}

export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul className="divide-y">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  );
}
```

## 상태 관리

가능한 가장 단순한 방식을 선택한다.

```txt
로컬 상태(useState)          → 특정 컴포넌트 안의 UI 상태
상위로 끌어올린 상태         → 2~3개 형제 컴포넌트가 공유하는 상태
Context                     → 테마, 인증, 로케일처럼 읽기가 많고 변경이 드문 상태
URL 상태(searchParams)      → 필터, 정렬, 페이지네이션처럼 공유 가능한 화면 상태
서버 상태(React Query/SWR)  → 캐싱과 재검증이 필요한 원격 데이터
전역 스토어(Zustand)  → 앱 전체에서 공유되는 복잡한 클라이언트 상태
```

3단계 이상 prop drilling이 생기면 context, 컴포넌트 재구성, 상태 위치 변경을 검토한다.

## 디자인 시스템 준수

### 토큰과 컴포넌트 우선

새 UI를 만들 때는 먼저 기존에 정의된 디자인 토큰과 컴포넌트를 찾는다.

- 기존 컴포넌트로 해결 가능하면 새 컴포넌트를 만들지 않는다.
- 기존 컴포넌트가 거의 맞으면 복제하지 말고 variant, prop, composition으로 확장한다.
- 기존 토큰으로 표현 가능한 색상, 간격, radius, typography 값은 새 값을 만들지 않는다.
- 새 디자인 값이 필요하면 raw value로 직접 쓰지 말고 디자인 토큰으로 정의한 뒤 사용한다.

### AI 기본값 피하기

AI가 생성한 듯한 흔한 시각 패턴을 피한다.

| AI 기본값 | 문제 | 더 나은 방향 |
|---|---|---|
| 보라색/인디고 중심 팔레트 | 어디서나 비슷해 보인다 | 프로젝트의 실제 색상 체계 사용 |
| 과한 그라데이션 | 시각적 소음이 커진다 | 디자인 시스템에 맞는 단색 또는 아주 절제된 그라데이션 |
| 모든 요소에 큰 radius | 위계가 사라진다 | 정해진 radius scale 사용 |
| 제네릭 hero 섹션 | 실제 사용자 과제와 연결이 약하다 | 콘텐츠와 핵심 행동 중심 레이아웃 |
| lorem ipsum성 문구 | 실제 길이, 줄바꿈, overflow 문제를 숨긴다 | 현실적인 한국어/서비스 문구 |
| 과한 padding | 화면 밀도와 위계가 무너진다 | 일관된 spacing scale |
| 무의미한 카드 그리드 | 정보 우선순위가 보이지 않는다 | 스캔 흐름과 중요도에 맞는 레이아웃 |
| shadow-heavy 디자인 | 콘텐츠보다 장식이 튄다 | 필요한 곳에만 미묘한 shadow 사용 |

### 간격과 레이아웃

프로젝트의 spacing scale을 따른다. 임의 값을 만들지 않는다.

```css
/* 좋음 */
padding: 1rem;    /* 16px */
gap: 0.75rem;     /* 12px */

/* 피하기 */
padding: 13px;
margin-top: 2.3rem;
```

#### 콘텐츠 폭에는 티셔츠 키 유틸을 쓰지 않는다 (Tailwind v4 충돌)

Tailwind v4에서 `--spacing-*` 네임스페이스는 여백(`p-`, `m-`, `gap-`, `space-`)뿐
아니라 크기 유틸(`w-`, `h-`, `size-`, `max-w-`, `min-w-`, `max-h-`, `min-h-`,
`inset-`, `top/right/bottom/left-`, `translate-`)까지 함께 읽는다. 그래서
`docs/DESIGN.md`의 티셔츠 간격 이름(`sm`, `md`, `lg`, `xl`…)이 `--spacing-*`로
정의돼 있으면, `max-w-md` 같은 유틸이 같은 이름을 끌어다 써서 컨테이너 폭 대신
간격 값(예: 12px)으로 조용히 깨진다.

- 여백은 티셔츠 키를 그대로 쓴다 (의도된 용도). 예: `gap-md`, `px-base`, `py-xxl`, `mt-lg`.
- 콘텐츠 폭·크기에는 티셔츠 키 유틸을 쓰지 않는다.
  - ❌ `max-w-md`, `min-w-sm`, `max-h-lg`
  - ✅ 임의값으로 쓴다. 예: `max-w-[28rem]`, `max-w-[36rem]`.
- 충돌이 의심되면 컴파일된 CSS에서 `max-w-md`가 `var(--spacing-*)`로 해석되는지 확인한다.

### 타이포그래피

문서 구조에 맞는 위계를 사용한다.

```txt
h1    → 페이지 제목, 페이지당 하나
h2    → 주요 섹션 제목
h3    → 하위 섹션 제목
body  → 본문
small → 보조/도움말 텍스트
```

제목 레벨을 건너뛰지 말고, 제목이 아닌 텍스트에 제목 스타일을 남용하지 않는다.

### 색상

- raw hex보다 `text-primary`, `bg-surface`, `border-default` 같은 의미 기반 토큰을 사용한다.
- 색상은 정보의 유일한 표현 수단으로 쓰지 않는다. 필요한 경우 아이콘, 텍스트, 형태를 함께 사용한다.
- 목업이어도 실제 브랜드/제품 맥락과 맞는 팔레트를 우선한다.

## UI States

프로토타입이라도 로딩, 빈 상태, 에러 상태를 명확히 만든다. 이것은 장애인 접근성보다 화면 흐름의 완성도와 실제 제품처럼 보이는 설득력에 더 가깝다.

### 로딩 상태

데이터가 아직 준비되지 않았을 때 보여준다. 콘텐츠 영역에는 단순 spinner보다 실제 레이아웃을 암시하는 skeleton을 우선한다.

```tsx
function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 3 }).map((_, index) => (
        <div key={index} className="h-12 rounded bg-muted animate-pulse" />
      ))}
    </div>
  );
}
```

### 빈 상태

데이터 로딩은 성공했지만 표시할 항목이 없을 때 보여준다. 빈 화면으로 두지 말고 현재 상황과 다음 행동을 제안한다.

```tsx
function EmptyState({ onCreateTask }: { onCreateTask: () => void }) {
  return (
    <div className="py-12 text-center">
      <TasksEmptyIcon className="mx-auto h-12 w-12 text-muted" />
      <h3 className="mt-2 text-sm font-medium">아직 할 일이 없습니다</h3>
      <p className="mt-1 text-sm text-muted">첫 번째 할 일을 만들어보세요.</p>
      <Button className="mt-4" onClick={onCreateTask}>할 일 추가</Button>
    </div>
  );
}
```

### 에러 상태

데이터 로딩이나 저장이 실패했을 때 보여준다. 무엇이 실패했는지와 사용자가 취할 수 있는 다음 행동을 함께 제공한다.

```tsx
function ErrorState({ retry }: { retry: () => void }) {
  return (
    <div className="rounded-lg border border-danger/20 bg-danger/5 p-4">
      <h3 className="text-sm font-medium text-danger">할 일을 불러오지 못했습니다</h3>
      <p className="mt-1 text-sm text-muted">잠시 후 다시 시도해주세요.</p>
      <Button className="mt-3" variant="outline" onClick={retry}>다시 시도</Button>
    </div>
  );
}
```

## 반응형 디자인

모바일을 먼저 설계하고 넓은 화면으로 확장한다.

```tsx
<div className="
  grid grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-3
  gap-4
">
```

최소한 320px, 768px, 1024px, 1440px에서 확인한다.

## 로딩과 전환

서버 데이터를 변경하는 화면에서는 체감 속도를 위해 optimistic update를 고려한다.

```tsx
function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previous = queryClient.getQueryData(['tasks']);

      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map((task) => task.id === taskId ? { ...task, done: !task.done } : task)
      );

      return { previous };
    },
    onError: (_error, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context?.previous);
    },
  });
}
```

애니메이션과 transition은 상태 변화를 이해시키는 정도로만 사용한다. 장식 목적의 과한 모션은 피한다.

## 흔한 합리화와 대응

| 합리화 | 실제로는 |
|---|---|
| "나중에 반응형으로 만들면 된다" | 반응형을 나중에 붙이는 작업은 처음부터 고려하는 것보다 훨씬 비싸다. |
| "디자인이 확정되지 않았으니 스타일링은 생략한다" | 디자인 시스템 기본값이라도 적용해야 리뷰어가 제품 흐름에 집중할 수 있다. |
| "프로토타입이니까 대충 둔다" | 프로토타입은 그대로 제품 코드가 되기 쉽다. 기반은 깔끔해야 한다. |
| "AI 느낌이어도 지금은 괜찮다" | 낮은 완성도로 보인다. 처음부터 프로젝트 맥락에 맞는 UI를 만든다. |

## Red Flags

- `docs/DESIGN.md`를 읽지 않고 UI를 구현함
- 기존 토큰/컴포넌트를 확인하지 않고 새 값을 직접 사용함
- raw hex, arbitrary spacing, one-off radius 등 토큰화되지 않은 디자인 값
- 200줄을 넘는 컴포넌트
- inline style 또는 임의 px 값
- 로딩, 에러, 빈 상태 누락
- 색상만으로 상태를 표현하는 UI
- 제네릭 AI 느낌의 UI: 보라색 그라데이션, 과한 rounded, 큰 카드 그리드, stock layout
- 실제 문구가 아니라 placeholder 문구만 있는 화면

## 검증

UI 구현 후 다음을 확인한다.

- [ ] `docs/DESIGN.md`를 읽고 디자인 시스템 기준을 반영했다.
- [ ] 기존 컴포넌트와 토큰을 먼저 재사용하거나 확장했다.
- [ ] 새 디자인 값은 raw value가 아니라 토큰으로 정의해 사용했다.
- [ ] 컴포넌트가 콘솔 에러 없이 렌더링된다.
- [ ] 320px, 768px, 1024px, 1440px에서 레이아웃이 깨지지 않는다.
- [ ] 로딩, 에러, 빈 상태가 처리되어 있다.
- [ ] spacing, color, typography가 프로젝트 디자인 시스템을 따른다.
- [ ] AI가 만든 듯한 제네릭 시각 패턴이 남아 있지 않다.
- [ ] 실제 서비스 문맥에 맞는 문구를 사용한다.
