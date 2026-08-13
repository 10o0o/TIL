# Practice

직접 실행한 Notebook과 실험을 모아둡니다.

```text
practice/<area>/<topic>.ipynb
```

예:

```text
practice/math/vector-normalization.ipynb
practice/ml/kaggle-titanic.ipynb
practice/llm/attention-score.ipynb
```

수학 계산, 데이터 분석, 모델 실험처럼 코드와 출력·그래프·해석을 함께 볼 때는 `.ipynb`를 기본으로 사용합니다. 반복 실행, 모듈화 또는 정확한 성능 측정이 중요한 작업만 `.py`로 분리합니다.

[실습 Notebook 템플릿](./template.ipynb)은 스킬이 워크북을 만들 때 사용하는 기본 구조입니다.

실습은 매 강의의 의무가 아닙니다. `$suggest-learning-practice`에 검토와 저장을 마친 날짜별 TIL 경로를 정확히 전달하면, 스킬이 TIL의 강의자료 링크와 학습 증거를 확인합니다. 재학습이 먼저이거나 추가 가치가 없으면 파일을 만들지 않고, 실습이 도움이 되면 별도 확인 없이 워크북 하나를 만듭니다. `today.md`나 자동으로 고른 최신 TIL은 입력으로 사용하지 않습니다.

워크북 난이도는 현재 증거에 맞춰 선택합니다.

- `Core`: 계산, shape 또는 최소 구현으로 핵심 동작 확인
- `Applied`: 작은 현실 데이터에서 기준선과 조건 하나 비교
- `Advanced`: 기반 이해가 확인된 경우 가설, ablation, 민감도 또는 실패 사례 분석

워크북 상단에는 기준 TIL과 강의자료 링크, 지금 필요한 이유와 완료 기준을 적습니다. 코드 실행 전 예상, 단계별 지시, 시작 코드, 힌트, 결과 해석과 자기 설명 칸도 포함합니다. 정답과 실행하지 않은 결과는 미리 채우지 않습니다.

짧은 코드 몇 줄은 TIL 안에 적어도 됩니다. 관련 [`knowledge/`](../knowledge/) 문서가 있다면 Notebook 상단에 링크 하나만 남겨도 충분합니다. 실행하지 않은 결과는 기록하지 않고, 데이터셋·모델 가중치·API 키와 큰 출력 파일은 Git에 올리지 않습니다.
