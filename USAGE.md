# 사용법

## 공부한 날

1. `materials/`의 자료를 본다.
2. [`templates/til.md`](./templates/til.md)를 복사해 짧게 정리한다.
3. 필요하면 GPT에게 틀린 부분과 빠진 내용을 확인받아 같은 파일을 다듬는다.
4. 코드나 실험이 길어지면 Notebook으로 `practice/`에 분리한다.

매일 작성할 필요는 없습니다. 별도의 진도표나 복습 문서도 관리하지 않습니다.

## TIL 작성

주제별 폴더에 날짜와 주제가 드러나는 이름으로 저장합니다.

```text
til/math/2026-08-13-vector.md
til/ml/2026-08-20-data-split.md
til/llm/2026-09-01-attention.md
```

노트에는 다음 정도만 있으면 충분합니다.

- 배운 것
- 확인하거나 고친 것
- 직접 해본 것
- 다음에 볼 것

해당 내용이 없으면 템플릿의 섹션을 지웁니다. 짧은 코드는 TIL 안에 그대로 둡니다.

## 실습 저장

코드, 출력, 그래프와 설명이 길어질 때는 `.ipynb`로 저장합니다.

```text
practice/math/vector-normalization.ipynb
practice/ml/kaggle-titanic.ipynb
practice/llm/attention-score.ipynb
```

[`templates/practice.ipynb`](./templates/practice.ipynb)를 복사해서 사용할 수 있습니다. 반복 실행, 모듈화 또는 정확한 성능 측정이 중요한 training·systems 작업만 `.py`로 작성합니다.

실행하지 않은 결과는 기록하지 않고, 데이터셋·모델 가중치·API 키·큰 출력 파일은 Git에 올리지 않습니다. Notebook 출력도 결과를 이해하는 데 필요한 것만 남깁니다.

## GPT 스킬

### 학습 내용 피드백

[`coach-llm-research-study`](./.agents/skills/coach-llm-research-study/SKILL.md)는 강의 자료와 TIL을 비교해 틀린 부분, 빠진 개념, 해볼 실습 하나를 제안합니다.

```text
$coach-llm-research-study를 사용해 이 PDF와 내 TIL을 비교해줘.
고칠 부분과 보충할 내용, 해볼 것 하나만 알려줘.
```

### 기존 TIL 정리

[`organize-til-notes`](./.agents/skills/organize-til-notes/SKILL.md)는 이미 작성한 TIL의 내용과 표현을 보존하면서 구조, 수식, 코드, 링크를 정리합니다.

```text
$organize-til-notes를 사용해 이 TIL을 간결하게 정리하고 검증해줘.
```
