<div align="center">

# Today I Learned

AI·ML·LLM Research Engineer를 목표로,
**회상·설명·적용·구현·복습으로 확인한 학습 결과를** 기록합니다.

[학습 운영 가이드](./GUIDE.md) · [학습 지도](./curriculum/course-map.md) · [진행 현황](./curriculum/progress.md) · [기존 노트 조사](./curriculum/note-inventory.md)

</div>

---

## 저장소의 목적

강의 PDF와 수업 자료는 학습의 원본(source), ChatGPT 프로젝트는 설명과 진단을 돕는 tutor, 이 GitHub 저장소는 학습 결과와 검증 증거를 남기는 장소입니다.

따라서 이 저장소는 강의 내용을 순서대로 옮긴 요약 모음을 목표로 하지 않습니다. 문서의 수나 길이보다 다음을 중요하게 봅니다.

- 자료 없이 핵심을 설명할 수 있는가
- 처음 보는 숫자·Tensor shape·적용 문제를 해결할 수 있는가
- 필요한 개념을 최소 코드로 구현하거나 디버깅할 수 있는가
- 며칠 뒤에도 다시 설명하고 적용할 수 있는가

설명을 보며 이해한 상태는 출발점일 뿐, Markdown 문서를 작성했다는 사실 자체는 이해의 증거가 아닙니다.

## 현재 학습 목표

- 주력: LLM Systems / Inference Optimization
- 확장: Post-training / Evaluation
- 기반: 선형대수, 확률·통계, 머신러닝 일반화, PyTorch, Transformer

기초 개념은 수식에서 끝내지 않고 Tensor 연산, PyTorch 구현, Transformer/LLM에서의 역할, 시스템 또는 평가 지표에 미치는 영향까지 연결합니다.

## 학습 루프

```text
closed-book recall
→ diagnostic questions
→ 부족한 부분 설명
→ 작은 숫자 예제
→ 수식과 shape
→ 코드 또는 적용 문제
→ learner teach-back
→ 최소한의 문서화
→ 1·3·7·14일 spaced review
```

자세한 판단 기준과 그대로 복사해 쓸 수 있는 ChatGPT 요청 예시는 [GUIDE.md](./GUIDE.md)에 있습니다.

## 저장 구조

| 위치 | 역할 |
|---|---|
| `content/` | 기존 강의 순서·개념 기반 문서와 학습 이력 보존 |
| `concepts/` | 설명과 적용을 통과한 개념별 canonical note |
| `til/` | 그날 실제로 바뀐 이해를 적는 짧은 learning log |
| `labs/` | 실행 가능한 코드, 실제 출력, 해석 |
| `curriculum/` | 자료 목록, 선수지식 지도, 진행 상태, migration 계획 |
| `reviews/` | 1·3·7·14일 복습과 주간 회고 |
| `templates/` | TIL, concept, lab, review의 최소 템플릿 |
| `assets/` | 기존 문서가 참조하는 이미지와 미디어 |

## 새 기록을 만드는 기준

| 상황 | 저장소 행동 |
|---|---|
| 읽었지만 자료 없이 설명하지 못함 | `curriculum/progress.md`만 정직하게 갱신 |
| 오개념이나 이해가 실제로 바뀜 | `til/`에 frontmatter 제외 핵심 내용 5~15줄 기록 |
| 하나의 개념을 설명하고 새 문제에 적용함 | 기존 `concepts/`를 갱신하거나 하나만 생성 |
| 코드가 이해의 핵심이고 실제로 실행함 | `labs/`에 재현 가능한 실험 저장 |
| 시간이 지난 뒤 다시 회상·적용함 | `reviews/`와 progress 갱신 |
| 새 증거도, 바뀐 이해도 없음 | 아무 문서도 만들지 않음 |

## 기존 `content/` 문서

기존 문서는 삭제 대상이 아니라 과거의 질문, 계산, 혼동, 설명을 보존한 source입니다.

- 이번 정비에서 기존 노트와 이미지를 이동하거나 다시 쓰지 않습니다.
- 같은 개념을 다시 학습할 때만 관련 내용을 검증해 canonical note로 점진 통합합니다.
- 원본은 링크 안정성과 학습 이력 보존을 위해 남깁니다.
- 오분류·중복·placeholder 후보와 안전한 처리 순서는 [note-inventory.md](./curriculum/note-inventory.md)에 기록합니다.

## 빠른 시작

1. 강의 PDF를 source로 준비하고 노트는 닫습니다.
2. [GUIDE.md](./GUIDE.md)의 closed-book 질문에 5~10분 답합니다.
3. ChatGPT에 진단 질문을 요청한 뒤, 틀린 부분과 빠진 선수지식만 설명받습니다.
4. 작은 숫자·shape·코드 또는 적용 문제를 풀고 자료 없이 teach-back합니다.
5. 위 표의 생성 기준을 통과한 파일만 최소한으로 남기고 다음 복습일을 예약합니다.

현재 개념 순서는 [course-map.md](./curriculum/course-map.md), 실제 증거와 다음 행동은 [progress.md](./curriculum/progress.md)에서 확인합니다.
