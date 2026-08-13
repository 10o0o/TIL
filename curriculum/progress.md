# Learning Progress

파일 수가 아니라 **자료 없이 설명하고 적용할 수 있는 정도를** 기록합니다. 기존 문서가 있다는 사실은 `seen`의 근거일 뿐, 더 높은 상태의 증거가 아닙니다.

## 상태 정의

| 상태 | 통과 기준 |
|---|---|
| `seen` | 수업 또는 저장된 노트에서 접함 |
| `recognized` | 설명을 보면 이해하지만 독립 설명은 어려움 |
| `explained` | 자료 없이 문제·이유·핵심 원리를 정확히 설명 |
| `applied` | 새로운 숫자·shape·해석 문제 해결 |
| `implemented` | 최소 코드를 실행·설명하거나 오류를 수정 |
| `retained` | 7~14일 뒤에도 다시 설명하고 적용 |

상태는 필요하면 내릴 수 있습니다. 상태의 단일 기준은 이 문서의 실제 증거와 최근 복습 결과이며, concept note의 frontmatter에 중복 기록하지 않습니다.

## 기존 노트로 확인된 진단 대상

[note-inventory.md](./note-inventory.md)에 있는 실제 파일만 근거로 등록했습니다. 아직 closed-book 진단 기록이 없으므로 모두 `seen`입니다.

| Priority | Concept | Status | Repository evidence | Next action |
|---|---|---|---|---|
| P0 | 벡터, 축, shape | `seen` | 벡터·행렬 개념 노트 | 정의와 shape를 자료 없이 설명 |
| P0 | 행렬곱과 축의 의미 | `seen` | 행렬 연산·딥러닝 레이어 노트 | 작은 행렬 계산 후 PyTorch와 대응 |
| P0 | 내적과 cosine similarity | `seen` | 내적 노트, Attention 노트 | 두 연산의 차이와 score 의미 설명 |
| P1 | 선형변환, 기저, rank | `seen` | 선형변환·벡터공간 노트 | 기하학적 의미와 rank 적용 진단 |
| P1 | 직교성과 최소제곱 | `seen` | 직교·최소제곱 노트 | $A^\top r=0$의 의미를 새 예제로 설명 |
| P1 | 고유값·대각화 | `seen` | 고유값·PCA 노트 | 손계산과 library algorithm을 구분 |
| P1 | SVD, PCA, low-rank | `seen` | SVD·PCA 관련 노트 3개 | 중복 진단 후 SVD → PCA → LoRA 연결 |
| P0 | ML 문제 정의, 데이터 분리, 지표 | `seen` | 강의 순서형 ML 노트 | 새로운 사례에서 split과 metric 선택 |
| P0 | 편향-분산과 일반화 | `seen` | 편향-분산, 모델 선택 노트 | 학습곡선 해석과 다음 실험 선택 |
| P1 | 배깅과 랜덤포레스트 | `seen` | 배깅·랜덤포레스트 노트 | 상관된 오차와 분산 감소 설명 |
| P0 | Attention과 $QK^\top$ | `seen` | Attention shape 노트 | 3-token 예제의 모든 축과 원소 의미 설명 |

## 목표 기반 미진단 대기열

다음은 진로 목표와 선수지식 지도에서 필요한 주제이지만, 현재 저장소만으로 학습 증거를 확인하지 못했습니다. 진단 또는 실제 source 등록 전에는 `seen`으로 올리지 않습니다.

| Priority | Concept | Why it matters | First evidence needed |
|---|---|---|---|
| P0 | 미분, gradient, chain rule | backpropagation과 optimization 기반 | 최소 신경망 손계산 |
| P0 | 확률분포, 기대값, 분산 | loss·일반화·평가 불확실성 기반 | 작은 분포 직접 계산 |
| P0 | 신경망과 backpropagation | Transformer 학습 기반 | forward/backward 최소 구현 |
| P0 | softmax와 cross entropy | language modeling loss 기반 | logits에서 loss까지 계산 |
| P0 | Transformer block | LLM 공통 구조 | component dependency와 shape 설명 |
| P1 | LLM Evaluation | 목표 분야 | metric·leakage·reliability 진단 |
| P1 | Post-training | 목표 분야 | SFT·LoRA·preference 학습 지도 |
| P1 | Inference Optimization | 주력 목표 | serving·KV cache·memory 선수지식 지도 |

## 현재 학습 단위

```text
미지정 — PDF source 등록 또는 첫 closed-book 진단 후 핵심 질문 하나를 선택한다.
```

## 복습 대기열

| Review date | Interval | Concept | Required evidence | Result |
|---|---|---|---|---|
| - | - | - | - | - |
