# LLM Research Engineer Roadmap

이 문서는 상세한 진도표가 아니라 **다음 공부 방향을 잃지 않기 위한 참고 지도**입니다. 역량별 목표 깊이, 선수 관계, 현재 강의자료의 충족도와 보완 기준은 [`CURRICULUM.md`](./CURRICULUM.md)에서 관리합니다.

```text
수학과 Tensor
-> 머신러닝 기본과 실험
-> PyTorch와 딥러닝
-> Transformer와 Language Modeling
-> LLM Systems / Post-training / Evaluation
```

## 1. 수학과 Tensor

- 선형대수, 미분, 확률
- Tensor shape, broadcasting
- softmax, cross entropy, gradient

## 2. 머신러닝 기본과 실험

- train/validation/test와 data leakage
- loss, metric, generalization
- baseline과 error analysis
- 필요할 때 Kaggle 프로젝트 하나

## 3. PyTorch와 딥러닝

- forward, backward, optimizer
- 학습 루프와 디버깅
- normalization과 regularization

## 4. Transformer와 Language Modeling

- tokenization과 embedding
- attention과 Transformer block
- autoregressive training과 generation

## 5. 전문 분야

- LLM Systems: latency, throughput, memory, batching, KV cache
- Post-training: SFT, LoRA, preference optimization
- Evaluation: metric, failure analysis, contamination

현재 무엇을 공부할지는 가장 최근 TIL, `knowledge/`에 드러난 현재 이해, 실제 실습 결과를 보고 정합니다. 추가 실습은 성취 근거상 도움이 될 때만 하나 추천받고, 이미 충분하다면 다음 강의로 진행합니다.
