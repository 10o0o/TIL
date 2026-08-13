# TIL

LLM Research Engineer를 목표로 공부하면서 배운 내용과 실습을 가볍게 모아두는 저장소입니다.

완벽한 학습 관리 시스템보다 **나중에 다시 찾을 수 있는 짧은 기록**을 우선합니다.

## 구조

| 위치 | 용도 |
|---|---|
| [`materials/`](./materials/) | 강의 PDF와 원본 자료 |
| [`til/`](./til/) | 공부한 내용을 주제별로 정리한 짧은 노트 |
| [`practice/`](./practice/) | 직접 실행한 코드, Kaggle, 모델 실험 |
| [`ROADMAP.md`](./ROADMAP.md) | LLM Research Engineer 학습 방향 참고 |
| [`archive/`](./archive/) | 구버전 TIL 보관 |

실제로 자주 쓰는 곳은 `til/`과 `practice/` 두 곳입니다.

## 공부한 날

1. `materials/`의 자료를 본다.
2. [`templates/til.md`](./templates/til.md)로 짧게 정리한다.
3. 필요하면 GPT에게 틀린 부분과 빠진 내용을 확인받아 같은 파일을 다듬는다.
4. 코드나 실험을 했다면 `practice/`에 저장한다.

매일 작성할 필요도 없고, 별도의 진도표나 복습 문서를 관리하지도 않습니다.

## 파일 예시

```text
til/math/2026-08-13-vector.md
til/ml/2026-08-20-data-split.md
practice/llm/attention-score/
```

노트에는 다음 정도만 있으면 충분합니다.

- 무엇을 배웠는가
- 무엇을 잘못 알았거나 추가로 확인했는가
- 직접 해본 것이 있는가
- 다음에 무엇을 볼 것인가

PDF 피드백이나 실습 추천이 필요할 때는 [`coach-llm-research-study`](./.agents/skills/coach-llm-research-study/SKILL.md)를 사용할 수 있습니다.
