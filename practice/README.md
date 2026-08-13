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

[실습 Notebook 템플릿](./template.ipynb)을 복사해서 시작할 수 있습니다.

실습은 매 강의의 의무가 아닙니다. `$suggest-learning-practice`가 학습자의 설명·계산·결과 해석을 확인한 뒤 도움이 된다고 판단했을 때만 가장 작은 활동 하나를 선택합니다. 이미 설명하고 적용할 수 있다면 추가 파일을 만들지 않고 다음 학습으로 진행합니다.

짧은 코드 몇 줄은 TIL 안에 적어도 됩니다. 관련 [`knowledge/`](../knowledge/) 문서가 있다면 Notebook 상단에 링크 하나만 남겨도 충분합니다. 실행하지 않은 결과는 기록하지 않고, 데이터셋·모델 가중치·API 키와 큰 출력 파일은 Git에 올리지 않습니다.
