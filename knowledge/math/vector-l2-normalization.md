---
title: "벡터 L2 정규화의 axis와 broadcasting"
updated: 2026-08-14
tags:
  - vector
  - numpy
  - normalization
---

# 벡터 L2 정규화의 axis와 broadcasting

## 한 줄 설명

벡터 L2 정규화는 벡터의 성분 축을 따라 노름을 구하고 각 벡터를 그 노름으로 나누는 작업이며, Tensor에서는 줄일 `axis`와 나눗셈이 가능한 shape을 함께 확인해야 한다.

## 현재 이해

NumPy 배열의 차원과 벡터가 속한 수학적 공간의 차원은 다르다. 예를 들어 `v = np.array([3, 2])`의 `shape`은 `(2,)`이고 `ndim`은 1이지만, 성분이 두 개이므로 수학적으로는 $\mathbb{R}^2$에 속하는 벡터이다.

벡터의 L2 노름은 각 성분을 제곱해 더한 뒤 제곱근을 취한 값이다.

$$
\lVert \mathbf{v} \rVert_2
= \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}
$$

벡터를 자신의 노름으로 나누면 방향은 유지되고 크기는 1이 된다. 영벡터는 노름이 0이므로 같은 방식으로 정규화할 수 없다. 정규화하기 전에는 노름이 0이거나 너무 작은 값인지 확인하고, 그런 벡터를 어떻게 처리할지 별도의 규칙을 정해야 한다.

NumPy의 `axis`는 계산하면서 줄이는 축이다. `H.shape == (2, 3, 4)`이고 `H[batch_index, token_index, :]`를 벡터 하나로 보면, 마지막 축의 성분 4개를 하나의 노름으로 줄여야 하므로 `axis=2`를 사용한다.

`keepdims=True`는 줄인 축을 크기 1로 남긴다. 따라서 노름의 shape은 `(2, 3, 1)`이 되고, 이 마지막 `1`이 broadcasting으로 4개 성분에 맞게 확장되어 각 벡터를 같은 노름으로 나눌 수 있다. `keepdims=False`에서는 노름의 shape이 `(2, 3)`이 되어, `(2, 3, 4)`와 오른쪽부터 비교할 때 `4`와 `3`이 맞지 않으므로 바로 나눌 수 없다.

여러 축을 지정할 때도 원리는 같다. `axis=(0, 1)`은 0번과 1번 축을 줄이고 feature 축인 2번 축을 남긴다. 따라서 `keepdims=False`의 결과 shape은 `(4,)`이고, `keepdims=True`의 결과 shape은 `(1, 1, 4)`이다.

벡터별 L2 정규화와 feature별 스케일링은 서로 다른 작업이다. `axis=2`를 사용한 이번 실험은 각 벡터의 길이를 1로 만들었다. 반면 Min-max scaling은 각 feature의 최솟값과 최댓값을 이용해 범위를 조절한다. 현재 Tensor 전체에서 feature별 통계를 구한다면 0번과 1번 축을 줄여 feature 4개에 대한 통계를 남긴다.

## 예제 또는 적용

실습에서는 마지막 축의 벡터를 다음과 같이 개별적으로 정규화했다.

```python
norms = np.linalg.norm(H, axis=2, keepdims=True)
H_unit = H / norms
```

핵심 shape 흐름은 다음과 같았다.

```text
H:      (2, 3, 4)
norms:  (2, 3, 1)
H_unit: (2, 3, 4)
```

정규화 후 확인한 여섯 벡터의 노름이 모두 1이었으므로, Tensor 안의 벡터가 각각 개별적으로 정규화되었다.

## 주의점과 경계

- `keepdims=False`로 만든 `(2, 3)` 크기의 노름을 `H`와 바로 나누면 broadcasting이 오른쪽부터 `4`와 `3`을 비교하므로 오류가 발생한다.
- 영벡터를 노름으로 나누면 각 성분이 `0 / 0`이 되어 `[nan, nan, nan, nan]`이 된다. 정규화 전에 영벡터 처리 규칙이 필요하다.
- 0에 매우 가까운 노름에 어떤 임계값이나 처리 규칙을 적용할지는 이번 실습에서 검증하지 않았다.

## 관련 기록

- TIL: [2026-08-13](../../til/2026/08/2026-08-13.md)
- Practice: [벡터 정규화에서 axis와 keepdims 추론](../../practice/math/vector-normalization-axis.ipynb)
- Source: [1장 1강: 벡터의 수학적 정의와 기하학적 해석](../../materials/private/kant-basic-math/01-01_벡터의_정의와_기하학적_해석.pdf)
