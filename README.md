<div align="center">

# KANT AI/ML Learning System

강의 내용을 많이 옮겨 적는 저장소가 아니라,
**자료 없이 설명하고, 직접 계산하고, 코드로 검증한 지식만 남기는 학습 시스템**입니다.

[학습 가이드](./GUIDE.md) · [학습 지도](./curriculum/course-map.md) · [진행 현황](./curriculum/progress.md) · [Work Mode](./.agents/skills/kant-learning-cycle/SKILL.md)

</div>

---

## 이 저장소의 역할

KANT 강의 PDF와 수업 자료는 학습의 **입력(source)** 입니다. 이 저장소는 입력을 그대로 복제하지 않고 다음 결과만 보관합니다.

- 하나의 개념을 중복 없이 설명하는 canonical note
- 자료 없이 회상한 뒤 바뀐 이해를 적은 짧은 TIL
- 수식과 Tensor 연산을 실제로 확인한 코드 및 실험
- 며칠 뒤에도 설명할 수 있는지 확인한 복습 기록

노트 분량과 커밋 수는 진도가 아닙니다. 이해의 기준은 **설명, 적용, 구현, 유지(retention)** 입니다.

## 먼저 읽을 문서

처음에는 [GUIDE.md](./GUIDE.md)만 읽으면 됩니다. 그 문서에는 다음이 모두 들어 있습니다.

1. 강의 PDF를 프로젝트에 올린 뒤 무엇을 요청할지
2. 매 수업을 어떤 순서로 학습할지
3. `concepts/`, `til/`, `labs/`, `reviews/` 중 어디에 기록할지
4. 기존 긴 TIL을 어떻게 처리할지
5. `$kant-learning-cycle` Work Mode를 어떻게 사용할지
6. 이해 완료 여부를 어떤 기준으로 판단할지

## 학습 루프

```text
강의 PDF / 기존 노트
        ↓
자료 없이 회상
        ↓
진단 질문으로 빈틈 확인
        ↓
직관 → 작은 숫자 → 수식·shape → 코드
        ↓
새 문제에 적용
        ↓
내 말로 다시 설명
        ↓
통과한 내용만 최소 기록
        ↓
1·3·7·14일 뒤 재검증
```

## 저장소 구조

```text
.
├── curriculum/          # 전체 개념 지도, PDF 인덱스, 진행 상태
├── concepts/            # 개념별 단일 기준 문서
├── til/                 # 그날 바뀐 이해만 기록하는 짧은 로그
├── labs/                # 실행 가능한 코드, 계산, 실험
├── reviews/             # 주간 및 간격 반복 복습
├── content/             # 기존 v1 강의 중심 노트: 보존용 레거시 자료
├── archive/             # 마이그레이션 및 보존 정책
├── templates/           # concept, TIL, lab, review 템플릿
├── .agents/skills/      # 저장소 전용 Work Mode와 보조 스킬
├── GUIDE.md             # 앞으로의 학습 운영 설명서
└── AGENTS.md            # 저장소를 수정하는 에이전트의 작업 규칙
```

## 문서별 역할

| 위치 | 작성 시점 | 담는 내용 | 담지 않는 내용 |
|---|---|---|---|
| `curriculum/` | 전체 지도를 만들거나 상태가 변할 때 | 선수지식, 우선순위, 학습 상태 | 긴 개념 설명 |
| `concepts/` | 설명과 적용을 통과한 뒤 | 개념별 최신 이해 | 강의 순서, 날짜별 로그 |
| `til/` | 실제로 이해가 바뀐 날 | 오개념, 수정된 이해, 증거, 다음 질문 | 강의 전체 요약 |
| `labs/` | 코드를 실행하거나 실험했을 때 | 가설, 코드, 출력, 해석 | 실행하지 않은 예상 결과 |
| `reviews/` | 간격 복습 및 주간 회고 때 | 회상 성공·실패, 상태 변경 | 새 강의 복사 |
| `content/` | 새로 작성하지 않음 | 과거 노트와 원본 학습 기록 | 신규 canonical note |

## 학습 상태

| 상태 | 의미 |
|---|---|
| `seen` | 읽거나 수업에서 본 적이 있음 |
| `recognized` | 설명을 보면 이해됨 |
| `explained` | 자료 없이 내 말로 설명 가능 |
| `applied` | 새로운 숫자 예제나 문제에 적용 가능 |
| `implemented` | 최소 코드로 구현하거나 디버깅 가능 |
| `retained` | 며칠 뒤에도 설명·적용 가능 |

파일이 존재한다는 이유만으로 상태를 올리지 않습니다. 현재 상태는 [curriculum/progress.md](./curriculum/progress.md)에서 관리합니다.

## Work Mode

새 강의 학습, PDF 전체 재구성, 진단, 개념 문서 생성에는 저장소 스킬을 사용합니다.

```text
$kant-learning-cycle
```

이 모드는 설명부터 시작하지 않습니다. 먼저 기존 지식과 선수지식을 진단하고, 적용 및 teach-back을 거친 뒤 필요한 파일만 갱신합니다.

기존 긴 노트 하나를 명시적으로 다듬거나 canonical note로 이관할 때만 다음 보조 스킬을 사용합니다.

```text
$organize-til-notes
```

## 기존 노트 처리 원칙

`content/`의 기존 문서는 삭제하거나 전면 재작성하지 않습니다.

- 신규 학습은 새 구조에서 시작합니다.
- 과거 날짜의 TIL을 소급해서 채우지 않습니다.
- 같은 개념을 다시 공부할 때만 기존 노트에서 유효한 내용을 추출합니다.
- canonical note로 통합한 뒤에도 원본 경로는 링크 안정성을 위해 당분간 보존합니다.

자세한 정책은 [archive/README.md](./archive/README.md)를 참고합니다.

## 현재 목표

- 주력: LLM Systems / Inference Optimization Research Engineer
- 보조: Post-training / Evaluation
- 장기: Efficient LLM Algorithms / Architecture Research

따라서 개념을 배울 때 항상 다음 연결을 확인합니다.

```text
수학적 의미
→ Tensor 연산과 shape
→ PyTorch 구현
→ Transformer/LLM에서의 위치
→ 시스템 또는 평가 관점의 실제 영향
```
