# Learning Progress

파일 수가 아니라 **자료 없이 설명하고 적용할 수 있는 정도**를 기록합니다.

## 상태 정의

| 상태 | 통과 기준 |
|---|---|
| `seen` | 수업 또는 노트에서 접함 |
| `recognized` | 설명을 보면 이해하지만 독립 설명은 어려움 |
| `explained` | 자료 없이 핵심을 정확히 설명 |
| `applied` | 새로운 숫자·shape·해석 문제 해결 |
| `implemented` | 최소 코드 구현 또는 디버깅 |
| `retained` | 7~14일 뒤에도 설명 및 적용 |

상태는 필요하면 내릴 수 있습니다. 오래된 문서가 있다는 이유로 자동 승급하지 않습니다.

## 초기 진단 대상

현재 저장소의 파일을 기준으로 임시 등록했습니다. 모두 `seen`에서 시작하고 실제 진단 후 조정합니다.

| Priority | Concept | Status | Evidence | Next action |
|---|---|---|---|---|
| P0 | 벡터와 shape | `seen` | 기존 개념 노트 | closed-book 정의 및 shape 진단 |
| P0 | 행렬곱과 축의 의미 | `seen` | 기존 행렬 노트 | 작은 행렬 계산 및 PyTorch 대응 |
| P0 | 내적과 cosine similarity | `seen` | 기존 개념 노트 | 차이와 Attention 연결 설명 |
| P1 | 선형변환과 기저 | `seen` | 기존 개념 노트 | 기하학적 의미 진단 |
| P1 | 직교성과 최소제곱 | `seen` | 기존 개념 노트 | $A^\top r=0$ 재설명 |
| P1 | 고유값·고유벡터 | `seen` | 기존 개념 노트 | 손계산과 라이브러리 계산 구분 |
| P1 | SVD·PCA·low-rank | `seen` | 기존 강의 노트 | SVD → PCA → LoRA 연결 진단 |
| P0 | 미분과 gradient | `seen` | 대화 학습 이력 | derivative/gradient 구분 진단 |
| P0 | 기대값과 분산 | `seen` | 편향-분산 강의 | 작은 분포 직접 계산 |
| P0 | 회귀·분류·손실·지표 | `seen` | 기존 강의 노트 | 용어 및 선택 기준 진단 |
| P0 | train/validation/test와 누수 | `seen` | 기존 강의 노트 | 그룹 누수 사례 적용 |
| P0 | 편향-분산과 일반화 | `seen` | 기존 강의 노트 | 분해식 의미와 학습곡선 진단 |
| P1 | 배깅과 랜덤포레스트 | `seen` | 기존 강의 노트 | 상관된 오차와 분산 감소 설명 |
| P0 | 신경망과 backpropagation | `seen` | 대화 학습 이력 | chain rule 기반 최소망 계산 |
| P0 | softmax와 cross entropy | `seen` | 향후 핵심 prerequisite | logits부터 loss까지 계산 |
| P0 | Attention과 $QK^\top$ | `seen` | 기존 강의 노트 | 3-token shape 및 의미 진단 |
| P0 | Transformer block | `seen` | Attention 학습 이력 | 구성요소 dependency 확인 |
| P1 | LLM evaluation | `seen` | 진로 목표 | 평가 설계·신뢰도 기초 진단 |
| P1 | Post-training | `seen` | 진로 목표 | SFT/LoRA/선호학습 지도 작성 |
| P1 | Inference optimization | `seen` | 주력 진로 목표 | serving·KV cache 선수지식 지도 |

## 현재 학습 단위

```text
전체 PDF 업로드 및 curriculum 재구성 전
```

PDF 전체 분석 후 한 번에 하나의 개념만 이 구역에 지정합니다.

## 복습 대기열

| Review date | Concept | Required evidence | Result |
|---|---|---|---|
| - | - | - | - |
