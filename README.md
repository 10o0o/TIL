<div align="center">

# Today I Learned

소프트웨어 엔지니어링에서 AI·LLM 엔지니어링으로 확장해 나가는 과정에서
배운 내용, 잘못 이해했던 개념, 직접 검증한 코드를 기록합니다.

[전체 학습 기록](#topics) · [작성 원칙](#writing-principles) · [Blog](<BLOG_URL>)

</div>

---

## About

이 저장소는 Python, 수학, 머신러닝, 딥러닝 및 LLM 관련 학습 내용을 기록하는 공간입니다.

단순히 학습 자료를 요약하기보다 다음 내용을 중심으로 작성합니다.

- 처음에 무엇을 잘못 이해했는가
- 핵심 개념을 어떻게 다시 이해했는가
- 코드나 계산을 통해 어떻게 검증했는가
- 실제 프로젝트에서는 어디에 사용할 수 있는가

완성도가 높아진 일부 글은 기술 블로그에 별도로 정리합니다.

## Current Focus

현재 다음 내용을 중점적으로 학습하고 있습니다.

- Python과 NumPy
- 선형대수와 확률·통계
- PyTorch와 딥러닝
- Transformer 구조
- LLM Evaluation
- Fine-tuning과 Post-training

## Topics

| Category | Description | Notes |
|---|---|---:|
| [Python](./content/python/) | Python 문법, NumPy, 데이터 처리 | - |
| [Mathematics](./content/mathematics/) | 선형대수, 미적분, 확률·통계 | - |
| [Machine Learning](./content/machine-learning/) | 머신러닝 알고리즘과 구현 | - |
| [Deep Learning](./content/deep-learning/) | 신경망, 역전파, PyTorch | - |
| [LLM](./content/llm/) | Transformer, 평가, 파인튜닝 | - |
| [Algorithms](./content/algorithms/) | 자료구조와 알고리즘 | - |

## Recent Notes

<!-- RECENT_TIL:START -->

- [백터의 수학적 정의와 기하학적 해석](./content/mathematics/linear-algebra/백터의_수학적_정의와_기하학적_해석.md)

<!-- RECENT_TIL:END -->

## Repository Structure

```text
.
├── content/
│   ├── python/
│   ├── mathematics/
│   ├── machine-learning/
│   ├── deep-learning/
│   ├── llm/
│   └── algorithms/
├── assets/
│   └── images/
├── templates/
│   └── til.md
└── README.md
```

## Writing Principles

1. 이해하지 못한 내용을 아는 것처럼 작성하지 않는다.
2. 개념만 옮겨 적지 않고 직접 실행하거나 계산한다.
3. 잘못 이해했던 부분과 수정된 이해를 함께 기록한다.
4. 하나의 글에서는 하나의 핵심 질문을 다룬다.
5. 출처가 필요한 내용은 원문 링크와 함께 기록한다.
6. 나중에 다시 읽었을 때 이해할 수 있을 정도로 작성한다.

## Document Status

각 문서의 frontmatter에 `publish` 값을 지정합니다.

```yaml
publish: false
```

학습 과정에서 작성한 초안 또는 개인적인 TIL입니다.

```yaml
publish: true
```

블로그에 공개할 수 있을 정도로 검토한 문서입니다.

## License

학습 기록과 설명은 별도 표시가 없는 한 개인 학습 목적으로 작성되었습니다.
예제 코드의 사용 전에는 각 문서에 포함된 원본 자료와 라이선스를 확인해야 합니다.
