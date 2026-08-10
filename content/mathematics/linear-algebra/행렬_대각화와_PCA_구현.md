---
title: "행렬 대각화와 PCA 구현"
description: "행렬 대각화의 원리와 조건을 알아보고, 공분산행렬의 고유분해를 이용해 PCA를 직접 구현한 뒤 scikit-learn 결과와 비교한다."
date: 2026-08-06
updated: 2026-08-06
category: linear-algebra
tags:
  - mathematics
  - diagonalization
  - PCA
  - NumPy
  - scikit-learn
publish: false
---

# 행렬 대각화와 PCA 구현

## 오늘의 질문

행렬을 고유값과 고유벡터로 분해하면 계산이 왜 간단해지며, 이 원리를 이용해 데이터의 중요한 정보를 유지하면서 차원을 어떻게 줄일 수 있을까?

## 핵심 결론

정사각행렬 $A$가 행렬의 차원만큼 선형독립인 고유벡터를 가지면 $A=PDP^{-1}$로 대각화할 수 있다. 대각화하면 복잡한 선형 변환을 고유벡터 좌표계에서 각 축을 독립적으로 확대하거나 축소하는 단순한 변환으로 해석할 수 있다.

PCA는 공분산행렬을 고유분해하고, 큰 고유값에 대응하는 고유벡터부터 새로운 축으로 선택한다. 데이터를 이 축에 투영하면 전체 분산을 최대한 보존하면서 차원을 줄일 수 있다.

## 개념 정리

### 행렬 대각화란

$n\times n$ 정사각행렬 $A$에 선형독립인 고유벡터 $v_1,v_2,\ldots,v_n$이 있다고 하자. 이 고유벡터들을 열로 쌓은 행렬을 $P$, 각 고유벡터에 대응하는 고유값을 대각선에 놓은 행렬을 $D$라고 한다.

$$
P=
\begin{bmatrix}
| & | & & | \\
v_1 & v_2 & \cdots & v_n \\
| & | & & |
\end{bmatrix},
\qquad
D=
\begin{bmatrix}
\lambda_1 & 0 & \cdots & 0 \\
0 & \lambda_2 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & \lambda_n
\end{bmatrix}
$$

각 고유벡터는 $Av_i=\lambda_i v_i$를 만족한다. 행렬 $A$를 $P$에 곱한다는 것은 $P$의 각 열벡터에 $A$를 하나씩 곱한다는 뜻이다.

$$
\begin{aligned}
AP
&=A
\begin{bmatrix}
| & | & & | \\
v_1 & v_2 & \cdots & v_n \\
| & | & & |
\end{bmatrix} \\
&=
\begin{bmatrix}
| & | & & | \\
Av_1 & Av_2 & \cdots & Av_n \\
| & | & & |
\end{bmatrix} \\
&=
\begin{bmatrix}
| & | & & | \\
\lambda_1v_1 & \lambda_2v_2 & \cdots & \lambda_nv_n \\
| & | & & |
\end{bmatrix}
\end{aligned}
$$

$P$의 오른쪽에 $D$를 곱해도 각 열벡터 $v_i$에 대응하는 고유값 $\lambda_i$가 곱해진다.

$$
PD=
\begin{bmatrix}
| & | & & | \\
\lambda_1v_1 & \lambda_2v_2 & \cdots & \lambda_nv_n \\
| & | & & |
\end{bmatrix}
$$

따라서 $AP$와 $PD$의 결과가 같다.

$$
AP=PD
$$

고유벡터들이 선형독립이면 $P$의 역행렬이 존재한다. $AP=PD$의 양변 오른쪽에 $P^{-1}$을 곱하면 다음 대각화 식을 얻는다.

$$
A=PDP^{-1}
$$

벡터 $x$에 $A=PDP^{-1}$을 곱한다고 생각하면, 대각화는 변환 과정을 다음 세 단계로 나누어 보여준다.

1. $P^{-1}$로 좌표를 고유벡터 기준으로 바꾼다.
2. $D$로 각 고유벡터 방향을 고유값만큼 확대하거나 축소한다.
3. $P$로 원래 좌표계로 돌아온다.

### 대각화를 사용하면 계산이 간단해지는 이유

행렬 $A$를 여러 번 곱할 때 대각화 식을 사용하면 서로 맞닿은 $P^{-1}P$가 단위행렬 $I$로 바뀐다.

$$
\begin{aligned}
A^2
&=(PDP^{-1})(PDP^{-1}) \\
&=PD(P^{-1}P)DP^{-1} \\
&=PD^2P^{-1}
\end{aligned}
$$

따라서 양의 정수 $k$에 대해 다음 식이 성립한다.

$$
A^k=PD^kP^{-1}
$$

대각행렬의 거듭제곱은 대각 원소만 각각 거듭제곱하면 된다.

$$
D^k=
\begin{bmatrix}
\lambda_1^k & 0 & \cdots & 0 \\
0 & \lambda_2^k & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & \lambda_n^k
\end{bmatrix}
$$

즉, 복잡한 행렬 $A$를 반복해서 곱하는 대신 고유값만 거듭제곱하면 된다. 이 성질은 반복되는 선형 변환이나 시간에 따른 시스템의 변화를 계산할 때 유용하다.

### 모든 행렬이 대각화되는 것은 아니다

$n\times n$ 행렬을 대각화하려면 $P^{-1}$이 존재해야 한다. $P$의 열에는 고유벡터가 들어가므로, 결국 선형독립인 고유벡터를 $n$개 선택할 수 있어야 한다.

서로 다른 고유값이 $n$개라면 각각에 대응하는 고유벡터들이 선형독립이므로 대각화할 수 있다. 그러나 고유값이 중복될 때는 중복 여부만 보고 판단할 수 없다. 해당 고유값에서 서로 독립인 고유벡터를 몇 개 얻을 수 있는지 확인해야 한다.

#### 중복된 고유값을 가지지만 대각화할 수 있는 경우

2차원 단위행렬 $I$의 특성방정식에서는 고유값 $1$이 두 번 나타난다.

$$
I=
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
$$

단위행렬은 모든 벡터를 그대로 유지하므로 0이 아닌 모든 벡터가 고유값 $1$에 대응하는 고유벡터이다.

$$
Iv=v=1v
$$

따라서 다음처럼 선형독립인 고유벡터 두 개를 선택할 수 있다.

$$
v_1=
\begin{bmatrix}
1 \\
0
\end{bmatrix},
\qquad
v_2=
\begin{bmatrix}
0 \\
1
\end{bmatrix}
$$

고유값은 하나뿐이지만 $2\times2$ 행렬에 필요한 독립적인 고유벡터 두 개를 선택할 수 있으므로 단위행렬은 대각화할 수 있다.

#### 중복된 고유값을 가지고 대각화할 수 없는 경우

반면 다음 행렬의 특성방정식에서도 고유값 $1$이 두 번 나타나지만, 이 행렬은 대각화할 수 없다.

$$
A=
\begin{bmatrix}
1 & 1 \\
0 & 1
\end{bmatrix}
$$

고유값 $1$에 대응하는 고유벡터를 찾으면 다음 식을 얻는다.

$$
(A-I)v=0
$$

$v=[x,y]^T$라고 하면 다음 계산에서 $y=0$이라는 조건을 얻는다.

$$
(A-I)v
=
\begin{bmatrix}
0 & 1 \\
0 & 0
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix}
=
\begin{bmatrix}
y \\
0
\end{bmatrix}
=
\begin{bmatrix}
0 \\
0
\end{bmatrix}
$$

따라서 모든 고유벡터는 다음 형태이다.

$$
v=
\begin{bmatrix}
x \\
0
\end{bmatrix},
\qquad x\ne0
$$

$[1,0]^T$, $[2,0]^T$, $[-3,0]^T$처럼 고유벡터를 여러 개 만들 수는 있지만, 모두 서로의 배수여서 같은 방향을 가리킨다. 따라서 선형독립인 고유벡터는 하나뿐이며, $P$의 두 열을 서로 독립인 고유벡터로 채울 수 없다. 결국 $P^{-1}$이 존재하지 않으므로 이 행렬은 대각화할 수 없다.

두 사례의 차이는 고유값 $1$이 중복된 횟수가 아니라 고유벡터들이 이루는 공간의 차원이다.

| 행렬 | 고유값 | 선택할 수 있는 독립적인 고유벡터 수 | 대각화 |
| --- | --- | --- | --- |
| $I$ | $1$이 두 번 나타남 | 2개 | 가능 |
| 위에서 살펴본 $A$ | $1$이 두 번 나타남 | 1개 | 불가능 |

#### 대칭행렬의 대각화

실수 대칭행렬에서는 서로 직교하는 단위 고유벡터를 $n$개 선택할 수 있으므로 항상 대각화할 수 있다. 이 고유벡터들을 열로 쌓은 행렬을 $Q$라고 하면 $Q^{-1}=Q^T$가 성립한다. 따라서 대칭행렬의 대각화는 다음처럼 나타낼 수 있다.

$$
A=QDQ^T
$$

### PCA와 공분산행렬

PCA는 데이터가 가장 많이 퍼진 방향부터 새로운 좌표축으로 선택하는 차원 축소 방법이다. 데이터 행렬 $X$에서 각 행은 하나의 샘플을, 각 열은 하나의 특성을 나타낸다고 하자.

먼저 각 특성에서 해당 특성의 평균을 빼서 데이터의 중심을 원점으로 옮긴다. 이 과정을 중심화라고 한다.

$$
X_c=X-\bar{X}
$$

샘플이 $m$개일 때 표본 공분산행렬은 다음과 같다.

$$
C=\frac{1}{m-1}X_c^TX_c
$$

공분산행렬 $C$는 대칭행렬이자 양의 준정부호행렬이다. 따라서 고유값은 모두 0 이상이며, 서로 직교하는 단위 고유벡터들을 선택할 수 있다.

$$
C=Q\Lambda Q^T
$$

- 공분산행렬의 고유벡터: 데이터가 퍼져 있는 방향, 즉 주성분 축
- 고유벡터에 대응하는 고유값: 해당 주성분 축의 분산 크기

### 분산이 가장 큰 방향이 고유벡터가 되는 이유

길이가 1인 벡터 $w$를 새로운 축으로 선택하자. 중심화된 데이터를 $w$ 방향으로 투영하면 각 샘플의 새로운 좌표는 다음과 같다.

$$
z=X_cw
$$

이렇게 투영한 데이터의 분산은 공분산행렬을 이용해 다음처럼 나타낼 수 있다.

$$
\mathrm{Var}(z)=w^TCw
$$

$w$의 길이가 임의로 커져서 분산도 함께 커지는 것을 막기 위해 $w^Tw=1$이라는 조건을 둔다. 이 조건 아래에서 $w^TCw$를 가장 크게 만드는 방향을 구하면 다음 고유방정식으로 이어진다.

$$
Cw=\lambda w
$$

이 식에서 $\lambda$는 $w$ 방향으로 투영했을 때의 분산을 나타낸다. 따라서 가장 큰 고유값에 대응하는 고유벡터가 분산을 가장 많이 보존하는 첫 번째 주성분이 되고, 그다음으로 큰 고유값에 대응하는 고유벡터가 두 번째 주성분이 된다.

### PCA의 계산 순서

PCA를 직접 구현하는 과정은 다음과 같다.

1. 각 특성의 평균을 빼서 데이터를 중심화한다.
2. 필요하다면 각 특성을 표준편차로 나누어 표준화한다.
3. 공분산행렬을 계산한다.
4. 공분산행렬의 고유값과 고유벡터를 구한다.
5. 고유값을 큰 순서로 정렬한다.
6. 상위 $k$개의 고유벡터를 선택한다.
7. 데이터를 선택한 주성분 축에 투영한다.

상위 $k$개의 고유벡터를 열로 쌓은 행렬을 $W_k$라고 하자. 중심화된 데이터를 이 축들에 투영하면 차원이 축소된 데이터 $Z$를 얻는다.

$$
Z=X_cW_k
$$

표준화한 데이터를 사용했다면 위 식의 $X_c$ 대신 표준화된 데이터 행렬을 사용한다.

### 중심화와 표준화의 차이

PCA에서는 각 특성의 평균을 빼는 **중심화**가 기본적으로 필요하다. 반면 평균을 0으로 만들고 표준편차까지 1로 맞추는 **표준화**는 데이터의 단위와 분석 목적에 따라 선택한다.

키와 몸무게처럼 특성의 단위나 값의 범위가 크게 다르면 분산이 큰 특성이 주성분을 지배할 수 있으므로 표준화하는 것이 일반적이다. 반대로 모든 특성이 같은 단위를 가지고 실제 분산의 크기 자체가 중요한 경우에는 중심화만 적용할 수도 있다.

`sklearn.decomposition.PCA`는 중심화는 자동으로 수행하지만 표준화는 하지 않는다. 표준화가 필요하면 먼저 `StandardScaler`를 적용해야 한다.

### 설명 분산비와 차원 선택

모든 고유값의 합은 데이터의 전체 분산과 같다. 따라서 $i$번째 주성분의 고유값을 전체 고유값의 합으로 나누면 해당 주성분이 전체 분산 중 얼마를 설명하는지 알 수 있다.

$$
r_i=\frac{\lambda_i}{\sum_{j=1}^{n}\lambda_j}
$$

상위 $k$개 주성분의 누적 설명 분산비는 다음과 같다.

$$
R_k=\sum_{i=1}^{k}r_i
$$

누적 설명 분산비가 90~95% 이상이 되는 지점을 차원 수 $k$의 후보로 삼을 수 있다. 다만 이 값은 절대적인 기준이 아니다. 시각화가 목적이면 설명 분산비가 다소 낮더라도 $k=2$ 또는 $k=3$을 선택할 수 있고, 모델 성능이 목적이면 여러 $k$를 실제로 비교하여 결정하는 편이 좋다.

## 직접 확인

### 행렬 대각화 확인

```python
import numpy as np

A = np.array([
    [4.0, 2.0],
    [1.0, 3.0]
])

eigenvalues, eigenvectors = np.linalg.eig(A)

P = eigenvectors
D = np.diag(eigenvalues)
P_inverse = np.linalg.inv(P)
A_reconstructed = P @ D @ P_inverse

print(np.allclose(A, A_reconstructed))
```

실행 결과:

```text
True
```

`P`의 각 열에는 고유벡터가 들어 있고, `D`의 대각선에는 각 고유벡터에 대응하는 고유값이 같은 순서로 들어 있다. 예를 들어 `P`의 첫 번째 열이 고유값 `5`의 고유벡터라면 `D`의 첫 번째 대각 원소도 `5`여야 한다. 이 대응 순서가 일치해야 $A=PDP^{-1}$이 성립한다.

### NumPy로 PCA 직접 구현하기

다음 예제에서는 두 특성을 평균 0, 분산 1로 표준화한 뒤 PCA를 직접 구현한다.

```python
import numpy as np

np.set_printoptions(precision=4, suppress=True)

X = np.array([
    [2.5, 2.4],
    [0.5, 0.7],
    [2.2, 2.9],
    [1.9, 2.2],
    [3.1, 3.0],
    [2.3, 2.7],
    [2.0, 1.6],
    [1.0, 1.1],
    [1.5, 1.6],
    [1.1, 0.9]
])

# StandardScaler와 같은 방식으로 평균 0, 분산 1로 표준화한다.
mean = X.mean(axis=0)
standard_deviation = X.std(axis=0, ddof=0)
X_standardized = (X - mean) / standard_deviation

# 공분산행렬은 대칭행렬이므로 eigh()를 사용한다.
covariance = np.cov(X_standardized, rowvar=False)
eigenvalues, eigenvectors = np.linalg.eigh(covariance)

# eigh()는 고유값을 오름차순으로 반환하므로 순서를 뒤집는다.
order = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[order]
principal_axes = eigenvectors[:, order]

# 주성분 축으로 데이터를 투영한다.
X_pca_manual = X_standardized @ principal_axes
explained_variance_ratio = eigenvalues / eigenvalues.sum()

# 첫 번째 주성분만 선택하면 2차원 데이터가 1차원으로 줄어든다.
X_reduced = X_pca_manual[:, :1]

print("고유값:", eigenvalues)
print("설명 분산비:", explained_variance_ratio)
print("누적 설명 분산비:", np.cumsum(explained_variance_ratio))
print("축소된 데이터 shape:", X_reduced.shape)
```

실행 결과:

```text
고유값: [2.1399 0.0823]
설명 분산비: [0.963 0.037]
누적 설명 분산비: [0.963 1.   ]
축소된 데이터 shape: (10, 1)
```

첫 번째 주성분의 설명 분산비는 약 96.3%이다. 따라서 이 데이터에서는 첫 번째 주성분만 남겨 2차원 데이터를 1차원으로 줄여도 원래 분산의 대부분을 유지할 수 있다.

### scikit-learn PCA와 비교하기

같은 데이터를 scikit-learn으로 처리하여 직접 구현한 결과와 비교한다. 직접 구현과 동일한 조건을 만들기 위해 `StandardScaler`로 먼저 표준화한다.

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X_standardized_sklearn = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)
X_pca_sklearn = pca.fit_transform(X_standardized_sklearn)

print("직접 구현 고유값:", eigenvalues)
print("직접 구현 설명 분산비:", explained_variance_ratio)
print("sklearn 고유값:", pca.explained_variance_)
print("sklearn 설명 분산비:", pca.explained_variance_ratio_)

print(
    "고유값 일치:",
    np.allclose(eigenvalues, pca.explained_variance_)
)
print(
    "설명 분산비 일치:",
    np.allclose(explained_variance_ratio, pca.explained_variance_ratio_)
)
print(
    "주성분 방향 일치:",
    np.allclose(np.abs(principal_axes.T), np.abs(pca.components_))
)
```

실행 결과:

```text
직접 구현 고유값: [2.1399 0.0823]
직접 구현 설명 분산비: [0.963 0.037]
sklearn 고유값: [2.1399 0.0823]
sklearn 설명 분산비: [0.963 0.037]
고유값 일치: True
설명 분산비 일치: True
주성분 방향 일치: True
```

직접 구현한 `principal_axes`에서는 각 고유벡터가 열에 저장된다. 반면 scikit-learn의 `pca.components_`에서는 각 주성분 축이 행에 저장된다. 두 결과의 모양을 맞춰 비교하려면 `principal_axes.T`처럼 전치해야 한다.

고유벡터의 부호는 계산 방법에 따라 반대로 나올 수 있으므로 절댓값을 비교했다. 벡터 $v$와 $-v$는 화살표 방향만 반대일 뿐 같은 축을 나타낸다. 따라서 부호가 다르더라도 잘못된 PCA 결과는 아니다.

### PCA 결과 시각화하기

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].scatter(X_standardized[:, 0], X_standardized[:, 1])

colors = ["tab:red", "tab:green"]
for index in range(2):
    axis = principal_axes[:, index] * np.sqrt(eigenvalues[index])
    axes[0].quiver(
        0,
        0,
        axis[0],
        axis[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color=colors[index],
        label=f"PC{index + 1}"
    )

axes[0].set_title("표준화된 데이터와 주성분")
axes[0].set_xlabel("feature 1")
axes[0].set_ylabel("feature 2")
axes[0].axis("equal")
axes[0].legend()

axes[1].scatter(X_pca_manual[:, 0], X_pca_manual[:, 1])
axes[1].axhline(0, color="gray", linewidth=1)
axes[1].set_title("주성분 좌표계로 변환한 데이터")
axes[1].set_xlabel("PC1")
axes[1].set_ylabel("PC2")

plt.tight_layout()
plt.show()
```

왼쪽 그래프의 화살표는 원래 좌표계에서 바라본 두 주성분 축이다. 첫 번째 주성분은 데이터가 가장 길게 퍼진 방향과 나란하다. 오른쪽 그래프는 같은 데이터를 주성분 좌표계에서 나타낸 것으로, 대부분의 분산이 PC1 축에 모이고 PC2 방향의 분산은 매우 작다는 것을 보여준다.

## 헷갈렸던 부분

처음에는 고유값이 중복되면 행렬을 대각화할 수 없다고 생각했다. 하지만 고유값이 중복되는 것 자체는 문제가 아니다. 행렬의 차원만큼 선형독립인 고유벡터를 선택할 수 있는지가 대각화 가능 여부를 결정한다.

또한 PCA를 사용하려면 항상 표준화해야 한다고 생각했지만, 반드시 필요한 과정은 평균을 빼는 중심화이다. 표준화는 특성의 단위와 스케일이 다를 때 특정 특성이 분산을 지배하지 않도록 선택해서 적용한다.

마지막으로 직접 구현한 주성분과 scikit-learn의 주성분 부호가 반대로 나오면 서로 다른 결과처럼 보일 수 있다. 하지만 부호가 반대인 두 고유벡터는 같은 축을 나타내므로, 그 축이 설명하는 분산도 같다.

## 실제 활용

PCA는 이미지, 음성, 센서 데이터처럼 특성 수가 많은 데이터의 차원을 줄여 저장 공간과 모델 학습 시간을 절약하는 데 사용된다. 서로 연관된 여러 특성을 소수의 주성분으로 압축하므로 특성 사이의 중복된 정보를 줄이는 데에도 도움이 된다.

또한 고차원 데이터를 2차원이나 3차원으로 투영하면 데이터의 군집, 이상치, 전체적인 분포를 눈으로 살펴볼 수 있다. 다만 PCA는 분산을 많이 보존하는 선형 축을 찾는 방법이다. 분산이 크다고 해서 그 정보가 반드시 예측이나 분류에 중요한 것은 아니며, 데이터의 비선형 구조도 충분히 표현하지 못할 수 있다.

## 한 문장 요약

행렬 대각화는 선형 변환을 고유벡터 축에서 단순한 확대·축소로 표현하고, PCA는 공분산행렬에서 분산이 큰 고유벡터 축을 선택하여 전체 분산을 최대한 보존하면서 차원을 줄인다.

## 관련 글

- [고유값·고유벡터의 정의와 기하학적 의미](./고유값_고유벡터의_정의와_기하학적_의미.md)
- [특수 행렬과 행렬 연산의 성질](./특수_행렬과_행렬_연산_성질.md)
- [선형 변환의 기하학적 해석](./선형_변환의_기하학적_해석.md)

## 참고 자료

- 기초수학 3장 2강: 행렬 대각화와 PCA 구현
