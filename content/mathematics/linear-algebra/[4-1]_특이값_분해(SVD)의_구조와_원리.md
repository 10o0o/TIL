---
title: "특이값 분해(SVD)의 구조와 원리"
description: "SVD의 핵심 식과 각 행렬의 역할을 이해하고, 특이값이 랭크와 저랭크 근사로 이어지는 과정을 작은 행렬 예제로 정리합니다."
date: 2026-08-05
updated: 2026-08-07
category: linear-algebra
tags:
  - mathematics
  - svd
  - matrix
  - NumPy
publish: false
---

# 특이값 분해(SVD)의 구조와 원리

## 오늘의 질문

- 정사각행렬이 아닌 행렬도 중요한 입력 방향과 출력 방향을 찾을 수 있을까?
- $A = U\Sigma V^\top$에서 $U$, $\Sigma$, $V^\top$는 각각 무슨 역할을 할까?
- 특이값은 왜 $A^\top A$의 고유값에 제곱근을 씌운 값일까?
- 특이값만 보고 행렬의 랭크와 좋은 저랭크 근사를 어떻게 알 수 있을까?

## 핵심 결론

SVD는 임의의 $m\times n$ 행렬 $A$를 **입력 방향 $V^\top$ → 방향별 크기 조절 $\Sigma$ → 출력 방향 $U$** 의 세 단계로 분해한다.

> 가장 먼저 기억할 식은 $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$이다. 행렬 $A$에 특별한 입력 방향 $\mathbf{v}_i$를 넣으면 크기가 $\sigma_i$배가 되어 특별한 출력 방향 $\mathbf{u}_i$로 나온다.

## 개념 정리

| 개념 | 아주 짧게 말하면 |
| --- | --- |
| 고유벡터 | 행렬을 통과해도 같은 직선 위에 남는 특별한 방향 |
| 고유값 | 그 방향이 몇 배 커지거나 작아졌는지 |
| 특이벡터 | 행렬이 특별하게 취급하는 입력 방향과 출력 방향 |
| 특이값 | 해당 입력 방향의 길이를 얼마나 크게 또는 작게 바꾸는지 |
| 랭크(rank) | 행렬이 실제로 사용하는 독립적인 방향의 개수 |
| 저랭크 근사 | 중요도가 낮은 방향을 버리고 중요한 몇 방향만 남기는 것 |
| SVD | 위의 중요한 방향과 세기를 전부 찾아주는 분해 |

### 왜 고유값만으로는 충분하지 않을까?

$A$가 $m\times n$ 행렬이라면 $A$는 $n$차원 입력을 받아 $m$차원 출력으로 보낸다.

$$
A:\mathbb{R}^n \rightarrow \mathbb{R}^m
$$

고유값 문제의 식은 다음과 같다.

$$
A\mathbf{x} = \lambda\mathbf{x}
$$

각 항의 크기를 비교해 보면 문제가 분명해진다.

| 항 | 크기(shape) |
| --- | --- |
| $A$ | $m\times n$ |
| $\mathbf{x}$ | $n\times1$ |
| $A\mathbf{x}$ | $m\times1$ |
| $\lambda\mathbf{x}$ | $n\times1$ |

$m\ne n$이면 왼쪽 $A\mathbf{x}$와 오른쪽 $\lambda\mathbf{x}$의 크기가 다르므로 두 벡터가 같다는 식을 세울 수 없다. 그래서 고유값과 고유벡터는 정사각행렬에서 정의한다.

SVD는 입력과 출력이 꼭 같은 공간에 있어야 한다는 조건을 버린다. 덕분에 직사각행렬도 다룰 수 있다.

### SVD에서 가장 중요한 식

SVD의 핵심은 다음 한 줄이다.

$$
A\mathbf{v}_i = \sigma_i\mathbf{u}_i
$$

| 기호 | 의미 | 크기(shape) |
| --- | --- | --- |
| $A$ | 입력을 출력으로 보내는 행렬 | $m\times n$ |
| $\mathbf{v}_i$ | $i$번째 특별한 입력 방향인 오른쪽 특이벡터 | $n\times1$ |
| $\sigma_i$ | 그 방향을 확대하거나 축소하는 특이값 | 스칼라 |
| $\mathbf{u}_i$ | $i$번째 특별한 출력 방향인 왼쪽 특이벡터 | $m\times1$ |

왼쪽 $A\mathbf{v}_i$와 오른쪽 $\sigma_i\mathbf{u}_i$는 모두 $m\times1$ 벡터이므로 $m$과 $n$이 달라도 식이 성립한다.

말로 읽으면 다음과 같다.

> $\mathbf{v}_i$ 방향의 입력을 행렬 $A$에 넣으면 길이가 $\sigma_i$배가 되고, $\mathbf{u}_i$ 방향의 출력이 된다.

여기서 $\mathbf{v}_i$와 $\mathbf{u}_i$는 길이가 $1$인 단위벡터이고, 특이값 $\sigma_i$는 항상 $0$ 이상이다.

### 가장 작은 숫자 예제로 확인하기

다음 $3\times2$ 행렬을 생각해 보자.

$$
A =
\begin{bmatrix}
3 & 0 \\
0 & 1 \\
0 & 0
\end{bmatrix}
$$

입력 방향을 다음과 같이 잡는다.

$$
\mathbf{v}_1 =
\begin{bmatrix}
1 \\
0
\end{bmatrix},
\qquad
\mathbf{v}_2 =
\begin{bmatrix}
0 \\
1
\end{bmatrix}
$$

첫 번째 방향을 $A$에 넣으면

$$
A\mathbf{v}_1
=
\begin{bmatrix}
3 & 0 \\
0 & 1 \\
0 & 0
\end{bmatrix}
\begin{bmatrix}
1 \\
0
\end{bmatrix}
=
\begin{bmatrix}
3 \\
0 \\
0
\end{bmatrix}
=
3
\begin{bmatrix}
1 \\
0 \\
0
\end{bmatrix}
=
3\mathbf{u}_1
$$

이므로 $\sigma_1=3$이다. 두 번째 방향도 같은 방법으로 계산하면

$$
A\mathbf{v}_2
=
\begin{bmatrix}
0 \\
1 \\
0
\end{bmatrix}
=
1\mathbf{u}_2
$$

이므로 $\sigma_2=1$이다.

이 예제는 $2$차원 입력 $\mathbf{v}_i$가 $3$차원 출력 $\mathbf{u}_i$로 바뀌더라도 SVD 식이 자연스럽게 성립한다는 것을 보여 준다.

### 고유값과 특이값의 결정적 차이

| 구분 | 수식 | 입력과 출력 방향 |
| --- | --- | --- |
| 고유값 | $A\mathbf{x} = \lambda\mathbf{x}$ | 같은 직선 위에 있다. 음의 고유값이면 방향이 반대가 될 수 있다. |
| 특이값 | $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$ | 서로 다른 공간의 방향이어도 된다. |

고유값 문제는 하나의 공간 안에서 변하지 않는 축을 찾는다. SVD는 입력 공간에서 중요한 축 $\mathbf{v}_i$와 그에 대응하는 출력 공간의 축 $\mathbf{u}_i$를 따로 찾는다.

### 그러면 $U$, $\Sigma$, $V^\top$는 무엇인가?

각 방향에 대한 관계 $A\mathbf{v}_i=\sigma_i\mathbf{u}_i$를 한꺼번에 행렬로 모으면 다음 SVD 식이 된다.

$$
A = U\Sigma V^\top
$$

$r=\min(m,n)$이라고 할 때 축약형 SVD의 크기는 다음과 같다.

| 행렬 | 열 또는 대각 원소 | 크기(shape) |
| --- | --- | --- |
| $U$ | 출력 방향 $\mathbf{u}_1,\ldots,\mathbf{u}_r$ | $m\times r$ |
| $\Sigma$ | 특이값 $\sigma_1,\ldots,\sigma_r$ | $r\times r$ |
| $V^\top$ | 입력 방향의 전치 | $r\times n$ |

행렬 곱은 오른쪽부터 적용하므로 입력 $\mathbf{x}$는 다음 순서로 변환된다.

$$
\mathbf{x}
\xrightarrow{V^\top} V^\top\mathbf{x}
\xrightarrow{\Sigma} \Sigma V^\top\mathbf{x}
\xrightarrow{U} U\Sigma V^\top\mathbf{x}
= A\mathbf{x}
$$

| 단계 | 쉬운 의미 |
| --- | --- |
| $V^\top\mathbf{x}$ | 입력이 각 중요한 입력 방향 $\mathbf{v}_i$를 얼마나 포함하는지 좌표로 읽는다. |
| $\Sigma V^\top\mathbf{x}$ | 각 좌표를 해당 특이값 $\sigma_i$만큼 확대하거나 축소한다. |
| $U\Sigma V^\top\mathbf{x}$ | 조절된 좌표를 출력 방향 $\mathbf{u}_i$들로 조합한다. |

앞의 작은 예제에서는

$$
U =
\begin{bmatrix}
1 & 0 \\
0 & 1 \\
0 & 0
\end{bmatrix},
\qquad
\Sigma =
\begin{bmatrix}
3 & 0 \\
0 & 1
\end{bmatrix},
\qquad
V^\top =
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
$$

이므로 실제로 $A=U\Sigma V^\top$가 된다.

### 특이값 $\sigma$가 중요한 이유

예를 들어 특이값이 다음과 같다고 하자.

$$
\sigma_1 = 100, \quad \sigma_2 = 10, \quad \sigma_3 = 0.1
$$

그러면 행렬 $A$는 세 입력 방향에 각각 다음과 같은 크기로 작용한다.

| 입력 방향 | $A$의 작용 |
| --- | --- |
| $\mathbf{v}_1$ | $100$배 |
| $\mathbf{v}_2$ | $10$배 |
| $\mathbf{v}_3$ | $0.1$배 |

따라서 $\mathbf{v}_1$ 방향은 $A$의 동작에서 매우 강하고, $\mathbf{v}_3$ 방향은 상대적으로 매우 약하다.

SVD에서는 일반적으로 특이값을 다음과 같이 큰 순서로 정렬한다.

$$
\sigma_1 \ge \sigma_2 \ge \sigma_3 \ge \cdots \ge 0
$$

### 이제 랭크를 이해해야 한다

**랭크(rank)**를 쉽게 말하면, **행렬이 실제로 가지고 있는 독립적인 방향의 개수**다.

예를 들어 다음 행렬 $A$를 보자.

$$
A =
\begin{bmatrix}
1 & 2 \\
2 & 4 \\
3 & 6
\end{bmatrix}
$$

두 번째 열은 첫 번째 열의 $2$배이다.

$$
\begin{bmatrix}
2 \\
4 \\
6
\end{bmatrix}
=
2
\begin{bmatrix}
1 \\
2 \\
3
\end{bmatrix}
$$

즉, 두 번째 열은 새로운 정보를 전혀 추가하지 않는다. 따라서 독립적인 열 방향은 $1$개뿐이다.

$$
\operatorname{rank}(A) = 1
$$

### SVD에서는 랭크를 쉽게 볼 수 있다

SVD에서 행렬의 랭크는 **$0$이 아닌 특이값의 개수**와 같다.

$$
\operatorname{rank}(A) = \text{0이 아닌 특이값의 개수}
$$

예를 들어 $\Sigma$가 다음과 같다고 하자.

$$
\Sigma =
\begin{bmatrix}
10 & 0 & 0 \\
0 & 3 & 0 \\
0 & 0 & 0
\end{bmatrix}
$$

특이값은 $10$, $3$, $0$이고, 그중 $0$이 아닌 값은 $2$개이다. 따라서

$$
\operatorname{rank}(A) = 2
$$

즉, 행렬 $A$가 실제로 의미 있게 사용하는 독립적인 방향이 $2$개라는 뜻이다.

### 저랭크 근사

저랭크 근사는 **랭크가 낮은 행렬로 원래 행렬을 비슷하게 나타내는 것**을 뜻한다.

예를 들어 어떤 행렬의 특이값이 다음과 같다고 하자.

$$
100, \quad 20, \quad 3, \quad 0.2, \quad 0.01
$$

이 행렬은 원래 다섯 개의 방향을 사용한다. 하지만 뒤쪽의 특이값, 특히 $0.2$와 $0.01$은 앞의 $100$과 $20$에 비하면 매우 작다.

> “이 작은 방향들을 버려도 원래 행렬과 거의 비슷하지 않을까?”

이 아이디어가 바로 저랭크 근사이다.

### 예를 들어 랭크-$2$ 근사를 하면

원래 특이값 행렬은 다음과 같이 나타낼 수 있다.

$$
\Sigma = \operatorname{diag}(100, 20, 3, 0.2, 0.01)
$$

랭크-$2$ 근사에서는 가장 큰 특이값 $100$과 $20$만 남긴다.

$$
\Sigma_2 =
\begin{bmatrix}
100 & 0 \\
0 & 20
\end{bmatrix}
$$

즉, $100$과 $20$을 보존하고 나머지 값 $3$, $0.2$, $0.01$은 버린다. 그리고 $A$ 대신 다음 근사 행렬을 사용한다.

$$
A_2 = U_2 \Sigma_2 V_2^\top
$$

이 식은 바깥곱의 합으로도 볼 수 있다.

$$
A
=
\sigma_1\mathbf{u}_1\mathbf{v}_1^\top
+\sigma_2\mathbf{u}_2\mathbf{v}_2^\top
+\cdots
+\sigma_r\mathbf{u}_r\mathbf{v}_r^\top
$$

$\mathbf{u}_i\mathbf{v}_i^\top$은 하나의 입력 방향과 하나의 출력 방향만 연결하는 랭크-$1$ 행렬이다. 따라서 상위 $k$개만 남기면

$$
A_k
=
\sum_{i=1}^{k}\sigma_i\mathbf{u}_i\mathbf{v}_i^\top
=
U_k\Sigma_kV_k^\top
$$

이 되고, 이 행렬의 랭크는 최대 $k$이다.

### 왜 큰 특이값을 남기는가?

특이값이 크다는 것은 행렬 $A$가 해당 방향에 강하게 작용한다는 뜻이다. 따라서 작은 특이값부터 버리면 원본과의 차이를 최소화할 수 있다.

여기서 **노름(norm)** 은 두 행렬 사이의 차이가 얼마나 큰지 재는 규칙이다.

더 엄밀히 말하면, 스펙트럴 노름 또는 프로베니우스 노름을 기준으로 상위 $k$개의 특이값과 특이벡터로 만든 $A_k$는 가능한 모든 랭크-$k$ 이하의 행렬 중 원래 행렬 $A$와 가장 가까운 행렬이다.

이것이 **에카르트–영 정리(Eckart–Young theorem)** 라는 유명한 결과이며, 이 의미에서 SVD를 이용한 저랭크 근사는 수학적으로 최적이다.

### $A^\top A$의 고유값과 특이값

특이값과 고유값의 관계는 다음과 같다.

$$
\sigma_i = \sqrt{\lambda_i}
\qquad\Longleftrightarrow\qquad
\lambda_i = \sigma_i^2
$$

여기서 반드시 구분해야 할 점이 있다.

> $\lambda_i$는 원래 행렬 $A$의 고유값이 아니라, 정사각행렬 $A^\top A$의 고유값이다.

$A$가 $m\times n$ 행렬이면 $A^\top A$는 $n\times n$ 정사각행렬이므로 고유값과 고유벡터를 구할 수 있다.

$$
A^\top A\mathbf{v}_i = \lambda_i\mathbf{v}_i
$$

이때 고유벡터 $\mathbf{v}_i$가 바로 $V$의 $i$번째 열인 오른쪽 특이벡터가 된다.

### 특이값에 왜 제곱근이 붙을까?

$\mathbf{v}_i$가 길이 $1$인 단위벡터라고 하자.

$$
\lVert\mathbf{v}_i\rVert = 1
\qquad\Longleftrightarrow\qquad
\mathbf{v}_i^\top\mathbf{v}_i = 1
$$

$A\mathbf{v}_i$의 길이를 바로 계산하는 대신 길이의 제곱부터 계산하면 다음과 같다.

$$
\begin{aligned}
\lVert A\mathbf{v}_i\rVert^2
&= (A\mathbf{v}_i)^\top(A\mathbf{v}_i) \\
&= \mathbf{v}_i^\top A^\top A\mathbf{v}_i \\
&= \mathbf{v}_i^\top(\lambda_i\mathbf{v}_i) \\
&= \lambda_i(\mathbf{v}_i^\top\mathbf{v}_i) \\
&= \lambda_i
\end{aligned}
$$

한 단계씩 보면 다음 규칙만 사용했다.

1. 벡터 $\mathbf{y}$의 길이 제곱은 $\lVert\mathbf{y}\rVert^2=\mathbf{y}^\top\mathbf{y}$이다.
2. $(A\mathbf{v}_i)^\top=\mathbf{v}_i^\top A^\top$이다.
3. $\mathbf{v}_i$는 $A^\top A$의 고유벡터이므로 $A^\top A\mathbf{v}_i=\lambda_i\mathbf{v}_i$이다.
4. $\mathbf{v}_i$는 단위벡터이므로 $\mathbf{v}_i^\top\mathbf{v}_i=1$이다.

따라서 실제 길이는

$$
\lVert A\mathbf{v}_i\rVert = \sqrt{\lambda_i}
$$

이다. 특이값은 이 길이의 변화량이므로

$$
\boxed{\sigma_i=\sqrt{\lambda_i}}
$$

가 된다.

앞의 숫자 예제에서는

$$
A^\top A =
\begin{bmatrix}
3 & 0 & 0 \\
0 & 1 & 0
\end{bmatrix}
\begin{bmatrix}
3 & 0 \\
0 & 1 \\
0 & 0
\end{bmatrix}
=
\begin{bmatrix}
9 & 0 \\
0 & 1
\end{bmatrix}
$$

이므로 $A^\top A$의 고유값은 $9$와 $1$이다. 여기에 제곱근을 씌우면 $A$의 특이값 $3$과 $1$이 나온다.

### $V$와 $U$는 어떻게 연결될까?

$A^\top A$와 $AA^\top$은 입력 공간과 출력 공간에서 각각 다음 역할을 한다.

| 행렬 | 크기(shape) | 고유벡터 |
| --- | --- | --- |
| $A^\top A$ | $n\times n$ | 입력 방향 $\mathbf{v}_i$, 즉 $V$의 열 |
| $AA^\top$ | $m\times m$ | 출력 방향 $\mathbf{u}_i$, 즉 $U$의 열 |

두 고유값 문제는 같은 특이값의 제곱 $\sigma_i^2$로 연결된다.

$$
A^\top A\mathbf{v}_i = \sigma_i^2\mathbf{v}_i
$$

$$
AA^\top\mathbf{u}_i = \sigma_i^2\mathbf{u}_i
$$

$\sigma_i>0$이면 핵심 식 $A\mathbf{v}_i=\sigma_i\mathbf{u}_i$를 다음처럼 바꿀 수 있다.

$$
\mathbf{u}_i = \frac{A\mathbf{v}_i}{\sigma_i}
$$

즉, $A^\top A$에서 입력 방향 $\mathbf{v}_i$를 찾고, 그 방향에 $A$를 적용한 뒤 길이를 $\sigma_i$로 나누면 대응하는 출력 방향 $\mathbf{u}_i$를 얻는다.

### 고유값과 특이값을 같은 값으로 보면 안 되는 이유

| 구분 | 고유값 | 특이값 |
| --- | --- | --- |
| 계산 대상 | 정사각행렬 $A$ | 모든 $m\times n$ 행렬 $A$ |
| 가능한 값 | 음수나 복소수도 가능 | 항상 $0$ 이상의 실수 |
| 의미 | 같은 축에서의 확대·축소와 방향 반전 | 입력 방향 길이의 확대·축소 정도 |

예를 들어 고유값 $\lambda=-5$는 크기를 $5$배로 만들면서 방향을 뒤집는다는 뜻일 수 있다. 반면 특이값은 길이의 배율이므로 음수가 될 수 없다.

또한 $A^\top A$의 고유값은 항상 $0$ 이상이다. 임의의 벡터 $\mathbf{x}$에 대해

$$
\mathbf{x}^\top A^\top A\mathbf{x}
=
(A\mathbf{x})^\top(A\mathbf{x})
=
\lVert A\mathbf{x}\rVert^2
\ge 0
$$

이기 때문이다. 따라서

$$
\boxed{\sigma_i\ge0}
$$

이다.

### SVD를 식 하나로 기억한다면

전체 분해식은

$$
A=U\Sigma V^\top
$$

이지만, 의미를 이해할 때는 다음 한 줄을 먼저 기억하는 편이 쉽다.

$$
\boxed{A\mathbf{v}_i=\sigma_i\mathbf{u}_i}
$$

행렬 $A$에 특별한 입력 방향 $\mathbf{v}_i$를 넣으면 크기가 $\sigma_i$배가 되어 특별한 출력 방향 $\mathbf{u}_i$로 나온다. 이 관계를 모든 중요한 방향에 대해 열 단위로 모은 식이 바로 $A=U\Sigma V^\top$이다.

## 직접 확인

다음 코드는 앞에서 손으로 계산한 $3\times2$ 행렬의 축약형 SVD를 확인한다.

```python
import numpy as np

A = np.array([
    [3.0, 0.0],
    [0.0, 1.0],
    [0.0, 0.0],
])

U, singular_values, Vt = np.linalg.svd(A, full_matrices=False)
Sigma = np.diag(singular_values)
reconstructed = U @ Sigma @ Vt

# 첫 번째 특이벡터 관계 A @ v1 = sigma1 * u1 확인
v1 = Vt.T[:, 0]
u1 = U[:, 0]

# 가장 큰 특이값 하나만 남긴 랭크-1 근사
A1 = U[:, :1] @ np.diag(singular_values[:1]) @ Vt[:1, :]

print("A.shape:", A.shape)
print("U.shape:", U.shape)
print("Sigma.shape:", Sigma.shape)
print("Vt.shape:", Vt.shape)
print("singular values:", singular_values)
print("rank:", np.linalg.matrix_rank(A))
print("reconstruction:", np.allclose(A, reconstructed))
print("A @ v1 == sigma1 * u1:", np.allclose(A @ v1, singular_values[0] * u1))
print("rank-1 approximation:")
print(A1)
print("rank-1 error:", np.linalg.norm(A - A1, ord=2))
```

실행 결과:

```text
A.shape: (3, 2)
U.shape: (3, 2)
Sigma.shape: (2, 2)
Vt.shape: (2, 2)
singular values: [3. 1.]
rank: 2
reconstruction: True
A @ v1 == sigma1 * u1: True
rank-1 approximation:
[[3. 0.]
 [0. 0.]
 [0. 0.]]
rank-1 error: 1.0
```

shape를 곱셈 순서대로 확인하면

$$
(3\times2)
=
(3\times2)(2\times2)(2\times2)
$$

이다. 코드의 `ord=2`는 스펙트럴 노름을 뜻한다. 이 기준에서 랭크-$1$ 근사의 오차가 $1$인데, 이는 버린 다음 특이값 $\sigma_2=1$과 같다.

> 특이벡터의 부호는 하나로 고정되지 않는다. 실행 환경에 따라 $\mathbf{u}_i$와 $\mathbf{v}_i$의 부호가 동시에 반대로 나올 수 있지만, $A\mathbf{v}_i=\sigma_i\mathbf{u}_i$와 $A=U\Sigma V^\top$는 그대로 성립한다.

## 헷갈렸던 부분

| 헷갈리기 쉬운 부분 | 올바른 이해 |
| --- | --- |
| $\sigma_i$와 $\Sigma$ | $\sigma_i$는 그리스 문자 소문자 시그마이며, 하나의 특이값인 스칼라이다. $\Sigma$는 대문자 시그마로, 여러 특이값을 대각선에 모은 행렬이다. |
| $\lambda_i$와 $\sigma_i$ | $\lambda_i$가 $A^\top A$의 고유값일 때 $\sigma_i=\sqrt{\lambda_i}$이다. $A$의 고유값과 바로 비교하면 안 된다. |
| $V$와 $V^\top$ | $V$의 열이 입력 방향 $\mathbf{v}_i$이고, 실제 분해식에서는 그 전치인 $V^\top$가 오른쪽에 놓인다. $\top$은 아래 첨자 `T`가 아니라 전치를 뜻하는 위 첨자다. |
| 특이값이 $0$인 경우 | 그 입력 방향의 정보가 출력에서 완전히 사라진다는 뜻이다. $0$이 아닌 특이값의 개수가 랭크다. |
| 아주 작은 특이값 | 이론적으로는 $0$이 아니지만, 수치 계산에서는 오차 허용 범위를 정해 사실상 $0$으로 판단하기도 한다. |

## 실제 활용

| 활용 | SVD가 하는 일 |
| --- | --- |
| 이미지 압축 | 큰 특이값 몇 개만 남겨 픽셀 행렬을 적은 정보로 근사한다. |
| 노이즈 제거 | 신호를 잘 설명하는 큰 특이값은 남기고 작은 특이값 성분을 줄인다. |
| PCA | 중심화된 데이터 행렬의 중요한 변화 방향을 찾는다. |
| 추천 시스템·잠재 의미 분석 | 사용자–아이템 또는 단어–문서 행렬을 낮은 차원의 잠재 요인으로 표현한다. |
| 최소제곱·의사역행렬 | 역행렬이 없거나 해가 하나가 아닐 때 안정적으로 해를 구하는 데 사용한다. |

## 한 문장 요약

SVD는 행렬 $A$가 중요하게 다루는 입력 방향 $\mathbf{v}_i$, 출력 방향 $\mathbf{u}_i$, 방향별 세기 $\sigma_i$를 찾아 $A\mathbf{v}_i=\sigma_i\mathbf{u}_i$와 $A=U\Sigma V^\top$로 정리하는 방법이다.
